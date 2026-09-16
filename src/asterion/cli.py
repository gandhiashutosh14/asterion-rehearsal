"""Local CLI; defaults to an honest no-key reference run."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from uuid import uuid4
from .models import ReviewRequest, RunRequest
from .reporting import export_dossier
from .storage import Ledger


def main() -> None:
    parser = argparse.ArgumentParser(prog="asterion")
    parser.add_argument("--state-dir", type=Path, default=Path(".asterion"))
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("demo", help="Execute a bounded synthetic deployment rehearsal")
    run.add_argument("--profile", choices=["guarded", "optimistic"], default="guarded")
    run.add_argument("--suite", choices=["complete", "happy-only"], default="complete")
    run.add_argument("--engine", choices=["reference", "langgraph"], default="reference")
    run.add_argument("--planner", choices=["deterministic", "bedrock"], default="deterministic")
    run.add_argument("--max-cases", type=int, default=32)
    run.add_argument("--max-rounds", type=int, default=4)
    run.add_argument("--output", type=Path, default=Path("artifacts/latest"))
    run.add_argument("--idempotency-key", default=None)
    review = sub.add_parser("review", help="Approve/reject a pending synthetic handoff")
    review.add_argument("run_id")
    review.add_argument("--digest", required=True)
    review.add_argument("--decision", choices=["approve", "reject"], required=True)
    review.add_argument("--rationale", required=True)
    review.add_argument("--output", type=Path, default=Path("artifacts/reviewed"))
    args = parser.parse_args()
    from .telemetry import configure
    configure()
    ledger = Ledger(args.state_dir)
    if args.command == "demo":
        req = RunRequest(profile=args.profile, suite=args.suite, engine=args.engine,
                         planner=args.planner, max_cases=args.max_cases, max_rounds=args.max_rounds)
        state, created = ledger.create("local-demo", args.idempotency_key or uuid4().hex, req)
    else:
        state = ledger.review("local-demo", args.run_id, ReviewRequest(decision=args.decision,
                              expected_digest=args.digest, rationale=args.rationale), "local-operator")
    export_dossier(state, args.output)
    print(json.dumps({"run_id": state["run_id"], "status": state["status"],
                      "coverage": state["assessment"]["coverage"], "evidence_digest": state["evidence_digest"],
                      "output": str(args.output.resolve())}, indent=2))

if __name__ == "__main__":
    main()
