# Witness-Coverage Gate: research framing and limits

## Thesis

A deployment acceptance decision should depend on *which customer obligations have compatible evidence*, not only the average quality of examples that happened to run.

Let `R = {(o, s)}` be the required obligation × operational-slice cells. A witness `w` is admissible only when its run, contract digest, scenario digest, target version, expected checks and internal result are consistent. Let `W(o,s)` contain admissible witnesses for a cell.

```
cell(o,s) = MISSING  when W(o,s) is empty
          = FAIL     when any compatible witness fails
          = PASS     otherwise

coverage = count(cell != MISSING) / |R|
observed_witness_pass_rate = passing admissible witnesses / admissible witnesses

gate = BLOCKED           for invalid evidence or a critical failed cell
     = HOLD              for any missing cell or remaining noncritical failure
     = READY_FOR_REVIEW  otherwise
```

The empty-witness rate is represented as zero by implementation convention; it is not an estimate of true performance. The complete assessment retains the missing-cell list so that convention is not confused with measured failure.

## Hypothesis and experiment

**H1:** On a finite catalog with known required operational slices, obligation-linked coverage can expose acceptance gaps that an observed-only pass-rate threshold misses.

The supplied constructed counterexample is deliberate: both happy-only suites achieve a 100% observed witness rate while testing only the normal cell, so WCG holds them. The optimistic complete run covers all cells but fails ten; the guarded complete run satisfies this authored contract and waits for human review.

This is a mechanism demonstration and regression benchmark, not a statistical evaluation of production agents. The optimistic and guarded policies were written with their respective failure and guard behaviors. These outcomes cannot establish real-world generalization, novel scientific superiority, customer ROI or robustness against unseen attacks.

## Baselines and what would falsify a stronger claim

The simplest comparison is an observed-only threshold, for example accepting a run with observed pass rate at least 95%, without requiring missing slices. It would accept both happy-only runs in this case study. WCG does not. A complete static test checklist that already enforces every required cell can reach the same verdict as WCG; do not claim superiority over that baseline. The implementation's extra value is evidence binding and the handoff workflow.

A stronger empirical study would collect independently authored customer obligations, hold out new integrations, pre-register slice definitions, compare complete-checklist and observed-only baselines at equal test budgets, and measure false-ready decisions using independent adjudication. An ablation would remove binding checks, coverage checks or the human digest check one at a time. If WCG cannot reduce missed acceptance gaps relative to a carefully maintained checklist at similar cost, the claimed automation benefit weakens.

## Assumptions

The requirement set is complete enough for the acceptance decision; each slice has meaningful scenarios; the oracle is correct; the target's observations are truthful; the target version identifies the intended implementation; the reviewer understands the scope. These are substantive assumptions, not properties provided by a hash.

Cell coverage is coarse. A single passing scenario can satisfy a required cell. Another unexecuted scenario in that same cell may fail. A critical failure dominates only if it is observed. Interaction failures across two individually passing slices are not systematically generated. Expand the contract, require per-cell quotas or add independently specified interaction slices before making broader claims.

## Prior art and positioning

Requirements traceability, acceptance testing, operational readiness reviews, coverage criteria, safety/assurance cases and cryptographic content digests are established ideas. LangGraph provides orchestration and interruption, not the WCG novelty. The [Google SRE readiness practice](https://sre.google/sre-book/evolving-sre-engagement-model/) is a motivating predecessor, and [LangGraph documentation](https://docs.langchain.com/oss/python/langgraph/interrupts) is an implementation reference.

The portfolio contribution is a narrowly integrated customer-delivery artifact: operational-slice coverage, typed witnesses, concrete counterexamples and digest-bound human handoff on an agent rehearsal path. This package contains no exhaustive paper/patent search. No claim of patentability, first invention or formal proof is made. ASTERION is a working project name, not a trademark-clearance conclusion.

## Next defensible study

Use three independently specified customer workflows and two actual agent implementations, with a frozen hidden oracle and equal cost budgets. Measure false-ready, unnecessary-hold, reviewer time, evidence completeness and replay cost. Keep failure taxonomy authors separate from target-policy authors where possible. Publish negative results and distinguish customer outcomes from fixture pass rates.
