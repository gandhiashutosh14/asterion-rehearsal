"""Tenant-scoped demo API. Keys map to principals; clients cannot pick a tenant.

No production identity provider or distributed admission queue is implemented.
"""
from dataclasses import dataclass
import hmac
import json
import os
from pathlib import Path
from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException, Response
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict
from .models import ReviewRequest, RunRequest
from .reporting import render_html
from .storage import ConflictError, Ledger, NotFoundError

@dataclass(frozen=True)
class Principal:
    tenant: str
    role: str
    actor: str

class TokenRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tenant: str
    role: str
    actor: str


def create_app(root: Path | None = None, token_map: dict | None = None) -> FastAPI:
    from .telemetry import configure
    configure()
    app = FastAPI(title="ASTERION — Deployment Rehearsal API", version="0.1.0",
                  description="Synthetic-only rehearsal and handoff. No production deployment endpoints.")
    ledger = Ledger(root or Path(os.environ.get("ASTERION_STATE_DIR", ".asterion")))
    tokens = token_map if token_map is not None else json.loads(os.environ.get("ASTERION_API_TOKENS", "{}"))
    for token, record in tokens.items():
        r = TokenRecord.model_validate(record)
        if len(token) < 24 or r.role not in {"viewer", "operator", "reviewer"} or not r.tenant or not r.actor:
            raise ValueError("tokens must be >=24 chars with a valid role, tenant, and actor")
    bearer = HTTPBearer(auto_error=False)
    def principal(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]) -> Principal:
        if not tokens:
            raise HTTPException(503, "Configure ASTERION_API_TOKENS before using the API")
        if credentials is None:
            raise HTTPException(401, "Bearer token required", headers={"WWW-Authenticate": "Bearer"})
        for token, record in tokens.items():
            if hmac.compare_digest(token.encode("utf-8"), credentials.credentials.encode("utf-8")):
                return Principal(**record)
        raise HTTPException(401, "Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    def obtain(tenant: str, run_id: str) -> dict:
        try:
            return ledger.get(tenant, run_id)
        except NotFoundError:
            raise HTTPException(404, "Run not found") from None
    @app.middleware("http")
    async def headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Frame-Options"] = "DENY"
        return response
    @app.get("/healthz")
    def health():
        return {"status": "ok", "mode": "synthetic-only", "version": "0.1.0"}
    @app.get("/v1/runs")
    def runs(p: Annotated[Principal, Depends(principal)]):
        return ledger.list(p.tenant)
    @app.post("/v1/runs", status_code=201)
    def create(req: RunRequest, response: Response, p: Annotated[Principal, Depends(principal)],
               idempotency_key: Annotated[str, Header(min_length=1, max_length=100)]):
        if p.role not in {"operator", "reviewer"}:
            raise HTTPException(403, "Operator role required")
        if req.planner != "deterministic":
            raise HTTPException(422, "Live model planning is CLI-only until asynchronous admission is implemented")
        try:
            state, fresh = ledger.create(p.tenant, idempotency_key, req)
        except ConflictError as exc:
            raise HTTPException(409, str(exc)) from None
        except ImportError:
            raise HTTPException(503, "Install the optional framework dependencies for LangGraph mode") from None
        response.status_code = 201 if fresh else 200
        return state
    @app.get("/v1/runs/{run_id}")
    def get(run_id: str, p: Annotated[Principal, Depends(principal)]):
        return obtain(p.tenant, run_id)
    @app.post("/v1/runs/{run_id}/review")
    def review(run_id: str, req: ReviewRequest, p: Annotated[Principal, Depends(principal)]):
        if p.role != "reviewer":
            raise HTTPException(403, "Reviewer role required")
        try:
            return ledger.review(p.tenant, run_id, req, p.actor)
        except NotFoundError:
            raise HTTPException(404, "Run not found") from None
        except ConflictError as exc:
            raise HTTPException(409, str(exc)) from None
    @app.get("/v1/runs/{run_id}/report", response_class=HTMLResponse)
    def report(run_id: str, p: Annotated[Principal, Depends(principal)]):
        return render_html(obtain(p.tenant, run_id))
    @app.get("/v1/runs/{run_id}/events")
    def events(run_id: str, p: Annotated[Principal, Depends(principal)]):
        state = obtain(p.tenant, run_id)
        def stream():
            # A replay of stored events, explicitly not live progress streaming.
            for e in state["events"]:
                yield f"id: {e['sequence']}\nevent: journal\ndata: {json.dumps(e)}\n\n"
        return StreamingResponse(stream(), media_type="text/event-stream")
    return app
