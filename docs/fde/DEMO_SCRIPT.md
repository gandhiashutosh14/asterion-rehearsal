# Five-minute technical walkthrough

**0:00 — Frame the problem.** Open the offline explorer. “A perfect score on two normal examples does not tell a customer what happens during ERP failure, stale data or duplicate delivery.” Select happy-only. Point to 100% observed pass rate and 1/12 required-cell coverage.

**0:45 — Make the failure concrete.** Select optimistic/complete. Inspect the ERP outage counterexample: the policy claims completion without sufficient evidence. Explain that the deliberately flawed policy is a controlled fixture baseline, not a frontier model evaluation.

**1:30 — Show the mechanism.** Open `evidence.py`. Explain admissibility, cell status and gate precedence. Repeated normal witnesses cannot cover an outage cell. An incompatible digest is not silently trusted. Distinguish coverage from correctness and probability.

**2:15 — Show engineering controls.** Run a complete guarded case. Demonstrate duplicate request idempotency, a foreign-tenant 404, or a stale-digest review rejection using the test suite. Show where the target receives inputs without expected results.

**3:15 — Explain human authority.** The complete passing run stops at PENDING_REVIEW. The native LangGraph adapter implements an interrupt/resume path; disclose whether you have now executed its tests. Approval only accepts the synthetic handoff capsule.

**4:00 — Discuss the cloud seam.** Open the AWS target. Explain why a queue, managed ledger, identity provider and independent release authority are required before moving beyond a single-host prototype. Point out the narrower Terraform foundation.

**4:40 — Close with the next measured increment.** Propose one read-only customer sandbox adapter and independently reviewed expected outcomes. Do not promise production rollout or quote cost savings without pilot data.
