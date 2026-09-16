# Verification snapshot — 2026-09-16

**70 tests passed; 1 optional native-framework module skipped.** The skipped module contains three LangGraph integration tests and was not executed. The pytest coverage report is approximately **89%**, including the unexecuted optional integration code in its denominator. Do not interpret coverage as correctness or production readiness.

## Commands actually executed

```bash
python -m pip install -e . --no-deps --no-build-isolation
python -m pytest -q --cov=asterion --cov-report=term-missing --cov-report=json:reports/verification/coverage.json --junitxml=reports/verification/junit.xml
python scripts/benchmark.py
python scripts/export_schemas.py
python scripts/check_assets.py
python scripts/verify_dossier.py reports/reference/guarded-complete
python scripts/browser_check.py
python -m compileall -q src scripts tests
python -m pip wheel . --no-deps --no-build-isolation
```

The installed `asterion` entry point also completed a synthetic reference demo. CLI demo/review behavior is included in the pytest run. A wheel was successfully built as a packaging check; it is not necessary to publish the binary in this source repository.

Browser inspection used the system Chromium executable through Playwright and loaded the local HTML via `page.set_content`. The environment blocked `file://` navigation, so a fresh browser's direct-file navigation was not tested here. The embedded page has no remote assets or fetch calls. Viewport checks and tab/counterexample selection succeeded. See `browser-check.json`.

## Not run

Native LangGraph execution, real Bedrock calls, an OTLP collector round trip, Docker build/run, Terraform init/validate/apply, GitHub-hosted CI, any cloud deployment, external connector access, production traffic or load testing. Sources for those integrations exist but require separate validation. No external state was modified.

Reference benchmark source hashes are in `../reference/summary.json`. Re-run into a new output directory to preserve the packaged snapshot. Timings, run IDs and event timestamps may differ; case outcomes and required-cell counts should match.
