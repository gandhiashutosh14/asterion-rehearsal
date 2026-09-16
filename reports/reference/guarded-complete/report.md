# ASTERION — Handoff dossier

Status: **PENDING_REVIEW**

Engine: `reference` · Target: `scripted-guarded-v1`

Finite synthetic acceptance checks; not a reliability probability or production certification.

Coverage: 100.0%; observed witness pass rate: 100.0%.

| Obligation | Slice | Status | Owner |
|---|---|---|---|
| R-01 | normal | PASS | support-operations |
| R-02 | erp-outage | PASS | integration-owner |
| R-02 | crm-outage | PASS | integration-owner |
| R-02 | missing-record | PASS | integration-owner |
| R-03 | stale-data | PASS | data-owner |
| R-03 | identity-conflict | PASS | data-owner |
| R-04 | high-impact | PASS | customer-approver |
| R-05 | duplicate-event | PASS | platform-owner |
| R-06 | tenant-boundary | PASS | security-review |
| R-07 | missing-owner | PASS | deployment-owner |
| R-08 | untrusted-note | PASS | security-review |
| R-09 | slow-dependency | PASS | platform-owner |

## Counterexamples
```json
[]
```

## Evidence digest
`2acb7a0ebd1ab221c9ad716a03b1b54ca3f8bf0d1d951aa0b9821a5966b16916`
