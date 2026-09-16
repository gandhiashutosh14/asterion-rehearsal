# Responsibility matrix

R = responsible for execution; A = accountable for the decision; C = consulted; I = informed. This is a suggested operating model for the synthetic engagement, not an implemented authorization policy.

| Activity | Sponsor | FDE | Integration owner | Platform/security | Acceptance reviewer |
|---|---|---|---|---|---|
| Define business acceptance | A | R | C | C | C |
| Approve source-of-truth assumptions | C | R | A | C | I |
| Author rehearsal contract | C | A/R | C | C | C |
| Approve sandbox access | I | C | R | A | I |
| Implement target adapter | I | A/R | C | C | I |
| Review independent expected outcomes | C | R | C | C | A |
| Execute and explain failures | I | A/R | C | C | I |
| Accept exact rehearsal evidence | C | R | C | C | A |
| Authorize actual production rollout | A | C | C | R | C |
| Own post-handoff incident | I | C | R | A | I |

Do not merge rehearsal approval with production-release authority. The local API's reviewer role is a development convenience; it does not enforce this entire matrix or dual control.
