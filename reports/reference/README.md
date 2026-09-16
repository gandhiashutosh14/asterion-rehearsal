# Synthetic deployment rehearsal — measured reference results

No LLM, network, live connector, cloud deployment or production certification.

| Policy | Suite | Cases | Coverage | Witness pass rate | Failed cells | State |
|---|---|---:|---:|---:|---:|---|
| optimistic | happy-only | 2 | 8.3% | 100.0% | 0 | HOLD |
| optimistic | complete | 13 | 100.0% | 23.1% | 10 | BLOCKED |
| guarded | happy-only | 2 | 8.3% | 100.0% | 0 | HOLD |
| guarded | complete | 13 | 100.0% | 100.0% | 0 | PENDING_REVIEW |

The happy-only suites score perfectly on observed witnesses while leaving 11 of 12 required cells untested. These outcomes demonstrate the gate on authored fixtures, not statistical reliability or superiority over a frontier model.

Execution times are local wall-clock observations, not service latency measurements. Digests bind code inputs and evidence; they do not authenticate the evaluator.

Python 3.13.5. Command: `python scripts/benchmark.py`. Source hashes: `summary.json`.
