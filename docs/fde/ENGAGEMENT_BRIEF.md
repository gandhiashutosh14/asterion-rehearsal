# Northstar launch rehearsal — synthetic engagement brief

**Customer:** Northstar Distribution, an invented organization. **Use case:** an internal support-resolution agent consulting CRM and ERP. **Audience:** customer operations sponsor, integration engineer, platform/security owner, FDE and acceptance reviewer.

## Discovery narrative

The sponsor wants faster resolution, but “resolve correctly” is underspecified. What counts as a completed action? Which system owns order identity? What happens when ERP is unavailable? Who reviews a high-impact decision? How should a duplicate event behave? Is source freshness part of correctness? The FDE's first deliverable is not an agent prompt; it is agreement on these semantics.

The local case study narrows the decision to a structured resolution result. No email is sent, no order is changed and no refund occurs. A synthetic effect counter allows duplicate behavior to be observed without an external write. The monetary-looking `amount_units` field is a synthetic impact proxy, not a financial workflow or underwriting model.

## Scope and measurable acceptance

The customer accepts a versioned set of nine obligations across twelve operational cells. Rehearsal outcomes include resolution, need for information, escalation or need for approval. Owners are named for unresolved situations. Every required cell must have compatible evidence; critical failures block; missing cells hold. A complete passing dossier reaches a reviewer, not an automatic launch.

This first artifact measures coverage and observed witness outcomes. It does not measure saved labor, revenue, customer satisfaction, production uptime or model quality. Those require a separately designed pilot and baseline.

## Delivery artifacts

The FDE owns the problem brief, acceptance workbook, architecture and demonstration. Integration owners confirm dependency assumptions. The platform owner reviews access and failure recovery. The reviewer signs off on the exact evidence set. Use the [RACI](RACI.md) to avoid treating “human in the loop” as an anonymous escape hatch.

## Customer implementation plan

First validate the decision boundary and owners. Then obtain approved sandbox access and frozen, de-identified test records. Add a single read-only target adapter with explicit timeout/identity semantics. Have someone other than the target implementation author review expected outcomes. Execute positive and negative cases, investigate mismatches, and preserve both successful and failing evidence. Move to a controlled pilot only after the production gaps in `IMPLEMENTATION_STATUS.md` are addressed.

## Questions to ask in a live workshop

Which mistakes are reversible, and which are not? What is the source of truth per field? Is stale-but-available data acceptable? Who owns a blocked handoff? Who may approve the actual rollout? How will a customer identify the tested target version? What evidence must remain after the engagement ends? What would cause the pilot to stop immediately?

These questions demonstrate solution discovery and operational judgment without pretending that a beautiful diagram is a deployed system.
