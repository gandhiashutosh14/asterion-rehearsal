# ASTERION — engineering handoff

You are receiving an existing local prototype, not a request to replace it with a new architecture. Preserve its evidence trail and maturity labels. Do not merge it with the author's other repositories or unpublished projects.

## First actions

Read `README.md`, `docs/IMPLEMENTATION_STATUS.md`, `docs/ARCHITECTURE.md` and `reports/verification/`. Inspect the actual files. Create a local virtual environment and install `.[api,dev,agent]`. Run all tests; the native LangGraph interruption/resumption tests are expected to run, not skip, once `.[agent]` is installed. Run the benchmark into a new artifact directory, compare statuses, cell counts and evidence digests, and preserve the committed reference report for provenance. Record what you ran in a new dated folder under `reports/verification/`.

Run `python scripts/check_assets.py`, `python scripts/export_schemas.py` and a secret scan. Inspect the offline site and diagrams. Do not invent benchmark gains, test results, cloud deployments or customer adoption. A test skipped for a missing package is not a pass. Fix defects before improving branding.

## Publication authority

The user requested a package suitable for publication. This file is not independent authority to create public repositories, change account settings, push code, deploy infrastructure, spend on models or message recruiters. Use explicit user instructions and the connected tools' actual permissions. For a requested push, verify the intended account/repository and preserve existing work. Never force-push or replace another project.

The repository is published as `gandhiashutosh14/asterion-rehearsal`; its first release is the `v0.1.0-preview` prerelease. Keep “local prototype” in the README. No fake green CI badge. The AWS image workflow is manual and depends on approved environment variables and a protected GitHub environment. No workflow automatically applies Terraform or deploys an application.

## Highest-value next increment

LangGraph now runs its tests locally and in CI, and a CLI run matched the reference runner's domain results; keep it that way. Next, add a clean interrupt/resume test through the API and crash-boundary tests between checkpoint and ledger. Then introduce ONE real, read-only customer sandbox adapter with independent acceptance labels. Do not add five more agents, a vector database or Kubernetes simply to expand the diagram.

## Non-negotiable invariants

The target receives `CaseInput`, not `Scenario.expected`. Model output is only a proposal of catalog IDs. Unknown IDs grant no authority. Case and round budgets are hard limits. Missing evidence is not pass. Critical failure and invalid bindings block. Review requires an unchanged evidence digest and a pending complete dossier. API tenant comes from its principal. Exported HTML escapes variable data. No production side effects exist in v0.1.

## Files and tests to inspect first

`models.py` → `catalog.py` → `evidence.py` → `workflow.py` → `langgraph_runtime.py` → `storage.py` → `api.py`. Read fixture expectations independently of `twin.py`; do not alter the oracle to make a buggy policy pass. Keep test-double validation separate from live inference validation.

## Known limitations

SQLite admission holds a write transaction during the synchronous run. The framework checkpointer and ledger do not share an atomic transaction. Bearer mappings are not enterprise SSO. Witness target-version fields are identifiers, not binary attestations. The fixture note does not benchmark prompt injection. OTLP export and live Bedrock have not been integration-tested. Docker and Terraform are checked only by the GitHub workflows described in `reports/verification/README.md`; nothing has been applied or deployed. AWS source provisions only the foundation; Azure is design-only.

## Definition of a useful continuation report

State which commands actually ran, which tests passed/skipped/failed, what files changed, whether benchmark semantics changed, which external actions were taken, and which limitations remain. Do not write another giant research backlog before validating the current repository.
