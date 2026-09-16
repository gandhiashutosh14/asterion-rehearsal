| Case | Cases | Covered / required | Failed cells | State | Evidence digest identical |
|---|---:|---:|---:|---|---|
| optimistic / happy-only | 2 | 1 / 12 | 0 | HOLD | yes |
| optimistic / complete | 13 | 12 / 12 | 10 | BLOCKED | yes |
| guarded / happy-only | 2 | 1 / 12 | 0 | HOLD | yes |
| guarded / complete | 13 | 12 / 12 | 0 | PENDING_REVIEW | yes |

All compared fields identical: True
Source files whose hash differs from the shipped summary: ['src/asterion/reporting.py']
Shipped run: Python 3.13.5 {'pydantic': '2.13.4', 'PyYAML': '6.0.3'} | fresh run: Python 3.11.9 {'pydantic': '2.13.5', 'PyYAML': '6.0.3'}
