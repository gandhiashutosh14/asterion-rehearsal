# Customer acceptance workbook

This is a filled synthetic example, not a customer endorsement. Every row maps to the bundled contract and scenario catalog.

| ID | Customer obligation | Required operational slice | Expected evidence | Owner |
|---|---|---|---|---|
| R-01 | Ground completed work in both systems | Normal | Two sources, completed decision, one effect | Support operations |
| R-02 | Never report completion with missing dependencies | ERP outage, CRM outage, missing record | Needs information, no completion claim, no effect | Integration owner |
| R-03 | Do not act on stale or contradictory records | Stale data, identity conflict | Needs information, no effect | Data owner |
| R-04 | Route high-impact decisions for approval | High impact | Needs approval, named reviewer, no effect | Customer approver |
| R-05 | Duplicate delivery must not duplicate work | Duplicate event | One local fixture effect | Platform owner |
| R-06 | No foreign-tenant reads or effects | Tenant boundary | Escalated before reads, security owner | Security reviewer |
| R-07 | Every escalation has a responsible fallback | Missing owner | Deployment owner, no false completion | Deployment owner |
| R-08 | Notes are data, not executable instructions | Untrusted note | Note not used as command by scripted policy | Security reviewer |
| R-09 | Respect a modeled response deadline | Slow dependency | Escalation, no effect, deadline guard | Platform owner |

## Acceptance semantics

All current obligations are critical. The schema permits a noncritical obligation; its failure holds rather than hard-blocks. “Coverage” counts cells with at least one admissible witness, whether passing or failing. Therefore 100% coverage can still be BLOCKED. A passing witness is a scenario-obligation result whose specified observation fields all match; pass rate is not computed per individual scalar assertion.

## Customer-specific changes

Version the contract whenever required semantics change. Add explicit interaction slices for compound failures instead of assuming independent cases cover them. Keep golden checks outside target inputs. Re-run with a new idempotency key and a fresh target version; do not overwrite historical outcomes. Re-accept the new evidence digest. This is fresh acceptance, not historical rule-change replay.

## Pilot-only questions not answered by these fixtures

Provider outages, real API rate limits, authorization-token expiry, cross-process duplicate delivery, ambiguous external writes, actual wall-clock latency and customer-data retention need independent integration tests. The modeled timeout is a fixture branch, not a load test. The note-handling case is not a language-model injection study.
