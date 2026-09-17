# Implementation and verification status

Release: **0.1.0 preview / local prototype**. Packaged 2026-09-16; verified locally and published 2026-09-17.

| Capability | What exists | Validation so far |
|---|---|---|
| Typed contract and scenario catalog | Pydantic schemas + synthetic YAML/JSON | Unit and end-to-end tests (Linux packaging run; Windows local run; CI) |
| Bounded rehearsal reference runner | Shared Python domain nodes | Complete and budget-limited runs; benchmark evidence digests reproduced byte-for-byte across Linux/Python 3.13 and Windows/Python 3.11 |
| Witness-Coverage Gate | Binding validation, cell states, counterexamples | Positive, missing, invalid and tampered cases tested |
| Approval and idempotency | SQLite ledger, scoped keys, serialized review | Restart, conflict and concurrent tests; stale-digest refusal in a CLI run |
| API principals and roles | Token → server-side tenant/role mapping | TestClient covers 401/403/404/409/422/503; `scripts/api_smoke.py` passed 10 checks against the app under uvicorn on 127.0.0.1 |
| Native LangGraph state machine | StateGraph, SQLite saver, human interrupt/resume | 3 integration tests passed locally (skipped in the packaging run for lack of the dependency); a CLI run paused for review, was resumed by a separate process, and matched the reference runner's cells, witnesses and observations |
| Bedrock proposer | Boto3 Converse JSON proposal | Fake-client serialization tests only; no live API call |
| Digital twin | In-process CRM/ERP fixtures + scripted target policies | Executed; not a remote service or production connector |
| Report export | JSON, Markdown, HTML, JSONL, manifest | Escaped HTML and byte hashes tested; a Windows line-ending defect that broke manifest verification was found and fixed before publication |
| SSE journal | Replay of saved events | TestClient and uvicorn smoke test; not live execution streaming |
| OpenTelemetry | Optional node spans and OTLP setup | Span context exercised when the API is present; collector export not validated |
| Browser showcase | Offline interactive measured-results explorer | Browser-rendered and interaction-checked with Playwright during packaging; page unchanged since, and statically confirmed to embed exactly the committed reports |
| Packaging | setuptools project, `asterion` console script | Wheel and sdist built; the wheel ran the demo in a fresh environment with core dependencies only |
| Docker | Non-root recipe + local-only Compose | Built on GitHub Actions (`container-check`, 2026-09-17); the image loaded the 13-scenario catalog, and a read-only, capability-dropped container served `/healthz` as user 10001. Not built locally (Docker unavailable); not deployed anywhere |
| AWS foundation | ECR, S3, KMS, log group, OIDC image publisher Terraform | `terraform fmt -check`, `init -backend=false` and `validate` passed on GitHub Actions (Terraform 1.16.3, AWS provider 6.65.0); no lock file, plan or apply |
| AWS full service / Azure | Detailed reference topology | Architecture only; no queue, managed DB, SSO or cloud service |
| CI | Python 3.11–3.13 matrix including the framework tests, API smoke test, dossier verification and package build | Passed on all three versions for the first published commit: 73 passed, 0 skipped, 94% coverage, 10/10 smoke checks, sdist and wheel built. Later runs are on the Actions page |

Read the dated records under [`reports/verification/`](../reports/verification/README.md) for the exact commands, logs and dependency versions; this document is a scope table, not a CI badge. `requirements-core.txt` lists the core versions used by the packaging run.

## Do not infer

No autonomous production deployment, compliance certification, external audit, proven research novelty, signed attestation, measured cloud savings, reliability probability, production scale test or customer adoption. Passing a finite synthetic contract is not proof of safety. Application file hashes are not an authenticated chain of custody. A workflow definition is not a passing run; check the recorded results.

## Publishability

Published as an inspectable local prototype with these status labels. It is not suitable to advertise as a production-ready multi-tenant agent platform. No original resume, private contact data, outreach workbook, employer source or client record is included.
