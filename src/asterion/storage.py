"""Single-host SQLite ledger: idempotent admission and serialized review.

This is not distributed storage. Never run multiple app replicas over copied DBs.
"""
from __future__ import annotations
from contextlib import contextmanager
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from uuid import uuid4
from .models import ReviewRequest, RunRequest, canonical, digest
from .workflow import event, run_reference

class ConflictError(ValueError): pass
class NotFoundError(LookupError): pass

class Ledger:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / "ledger.sqlite"
        with self.connect() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("""CREATE TABLE IF NOT EXISTS runs(
                id TEXT PRIMARY KEY, tenant TEXT NOT NULL, idem TEXT NOT NULL,
                request_digest TEXT NOT NULL, state_json TEXT NOT NULL,
                UNIQUE(tenant, idem))""")
    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=30)
        db.row_factory = sqlite3.Row
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
    def get(self, tenant: str, run_id: str) -> dict:
        with self.connect() as db:
            row = db.execute("SELECT state_json FROM runs WHERE tenant=? AND id=?", (tenant, run_id)).fetchone()
        if row is None:
            raise NotFoundError(run_id)
        return json.loads(row[0])
    def list(self, tenant: str) -> list[dict]:
        with self.connect() as db:
            rows = db.execute("SELECT state_json FROM runs WHERE tenant=? ORDER BY rowid DESC LIMIT 100", (tenant,)).fetchall()
        return [{k: state.get(k) for k in ("run_id", "status", "evidence_digest", "target_version")}
                for state in (json.loads(row[0]) for row in rows)]
    def create(self, tenant: str, idem: str, request: RunRequest) -> tuple[dict, bool]:
        if not 1 <= len(idem) <= 100 or not 1 <= len(tenant) <= 60:
            raise ValueError("invalid idempotency key or tenant")
        # Short bounded offline runs are serialized for a simple, honest demo.
        # Move orchestration out of this transaction before live multi-tenant use.
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            old = db.execute("SELECT request_digest,state_json FROM runs WHERE tenant=? AND idem=?", (tenant, idem)).fetchone()
            rd = digest(request)
            if old:
                if old[0] != rd:
                    raise ConflictError("idempotency key reused for different request")
                return json.loads(old[1]), False
            run_id = uuid4().hex
            if request.engine == "langgraph":
                from .langgraph_runtime import invoke
                state = invoke(self.root / "checkpoints.sqlite", run_id, request=request)
            else:
                state = run_reference(run_id, request)
            state["tenant"] = tenant
            state["created_at"] = datetime.now(timezone.utc).isoformat()
            db.execute("INSERT INTO runs VALUES(?,?,?,?,?)", (run_id, tenant, idem, rd, canonical(state)))
            return state, True
    def review(self, tenant: str, run_id: str, request: ReviewRequest, actor: str) -> dict:
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT state_json FROM runs WHERE tenant=? AND id=?", (tenant, run_id)).fetchone()
            if row is None:
                raise NotFoundError(run_id)
            state = json.loads(row[0])
            if state["status"] != "PENDING_REVIEW":
                raise ConflictError("only a pending, complete dossier can be reviewed")
            if state["evidence_digest"] != request.expected_digest:
                raise ConflictError("evidence digest does not match; reload the dossier")
            # The complete evidence payload is recomputed before approval.
            from .workflow import seal
            if seal(state)["evidence_digest"] != state["evidence_digest"]:
                raise ConflictError("stored evidence was modified")
            if state["request"]["engine"] == "langgraph":
                from .langgraph_runtime import invoke
                revised = invoke(self.root / "checkpoints.sqlite", run_id, review_request=request)
                state.update(revised)
            else:
                state["status"] = "APPROVED" if request.decision == "approve" else "REJECTED"
                state["review"] = request.model_dump()
                state["events"] = event(state, "human_review", status=state["status"])
            state["review"]["actor"] = actor
            db.execute("UPDATE runs SET state_json=? WHERE id=? AND tenant=?", (canonical(state), run_id, tenant))
            return state
