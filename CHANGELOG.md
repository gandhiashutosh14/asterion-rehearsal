# Changelog

## 0.1.0-preview — published 2026-09-17

Repository published from the packaged prototype after local verification on Windows 11 / Python 3.11. Behaviour of the rehearsal, gate and review is unchanged.

- Fixed: exported dossiers failed their own SHA-256 manifest on Windows because files were written in text mode (`src/asterion/reporting.py` now writes the exact hashed bytes).
- Fixed: the benchmark recorded source-hash paths with backslashes on Windows; helper scripts now read and write UTF-8 with LF explicitly.
- Added: `.gitattributes` to keep LF on checkout, so committed manifests and source hashes stay valid on every platform.
- Added: `scripts/api_smoke.py`, an HTTP smoke test of the API under uvicorn.
- Added: CI steps for the API smoke test, reference-dossier verification and package build; an `infra-validate` workflow for `terraform fmt`/`validate`; a `/healthz` probe in the manual container workflow.
- Changed: `pyproject.toml` requires setuptools 77+ and declares project URLs, classifiers and the licence file.
- Changed: verification records are now dated folders under `reports/verification/`; the packaging-time record and `PACKAGE_MANIFEST.json` were moved there unmodified.
- Changed: README, START_HERE, AGENTS and implementation status describe what has now been verified, including the native LangGraph tests.

## 0.1.0-preview — 2026-09-16

Initial local prototype: customer acceptance contract, 13 synthetic scenarios, witness gate, bounded reference execution, scoped SQLite ledger and review, FastAPI surface, report exports, optional native LangGraph and Bedrock integrations, architecture atlas, FDE delivery kit and cloud foundation source. See implementation status for what was and was not executed.
