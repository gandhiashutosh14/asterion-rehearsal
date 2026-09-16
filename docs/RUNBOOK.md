# Local operations and incident runbook

## Healthy baseline

Install the documented dependencies, run `python scripts/benchmark.py`, then `python -m pytest -q`. The four case-study statuses are HOLD, BLOCKED, HOLD and PENDING_REVIEW. A run awaiting review is not an error. The API's `/healthz` is process health only; it does not prove model, database recovery or customer readiness.

## Failure response

| Symptom | First check | Recovery | What not to do |
|---|---|---|---|
| API 503 on protected endpoints | Missing token map | Use `scripts/serve.py` locally or configure principals | Do not disable authentication |
| API 401/403 | Token, role, expiry of local process context | Recreate local session; use appropriate role | Do not grant every token reviewer access |
| API 404 for an existing ID | Tenant scope | Confirm caller's server-side mapping | Do not add tenant override to request |
| API 409 on run create | Reused key with different request | Use a new key for a new rehearsal | Do not silently overwrite the old run |
| API 409 on review | Stale digest or terminal state | Reload and inspect exact evidence | Do not accept a mismatch by force |
| HOLD | Missing cells or insufficient run budget | Inspect matrix, raise bounded budget or complete catalog | Do not turn unknown into pass |
| BLOCKED | Critical failure / invalid witness | Fix target or investigate provenance; start new run | Do not edit expected values merely to pass |
| Missing LangGraph import | Optional dependency unavailable | Install `.[agent]` and rerun framework tests | Do not relabel reference execution as LangGraph |
| Bedrock JSON / transport failure | Model access, format, timeout | Inspect approved configuration; rerun with a new key | No unbounded repair or automatic access escalation |
| SQLite locked | Concurrent long-running admission | Stop extra processes; run one local worker | Do not share copied DBs across replicas |

## Backups and restore

For a consistent local backup, stop the CLI/API processes and copy the entire state directory, including ledger/checkpoint databases and any WAL companions that remain. Prefer SQLite's supported backup facility for live copies; this repository does not implement a live backup service. Restore to a separate directory, verify known run IDs and tenant visibility, inspect pending reviews, and rerun a synthetic acceptance case. No successful disaster-recovery drill is claimed in the supplied evidence.

Checkpoint and ledger persistence are not a single atomic unit. An interrupted framework run may leave an orphan checkpoint. Preserve evidence, inspect it offline, and create a new run rather than guessing that an orphan is approved. Do not delete a database to “fix” an approval mismatch without retaining the diagnostic copy.

## Handoff checklist

Record contract version, target identifier, tested scenario set, remaining gaps, rationale, owner, exact evidence digest and reproduction command. Verify the exported manifest with `python scripts/verify_dossier.py PATH`. The digest is useful for comparing bytes, not deciding whether the business requirement is sensible.

## Production readiness is a separate project

Before external exposure: identity provider, asynchronous admission, rate limits, cancellation, cloud egress policy, audited credentials, managed state, independent tenant tests, cross-store recovery, real adapter timeout/idempotency semantics and a named on-call owner. No incident SLA or uptime target is guaranteed by this local release.
