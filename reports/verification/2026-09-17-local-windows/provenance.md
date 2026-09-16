# Provenance against the package as received

`../2026-09-16-packaging/PACKAGE_MANIFEST.json` lists the SHA-256 of every file in the original package. This table compares it with the files published in this repository (this file excluded).

| Category | Files |
|---|---:|
| Byte-identical at the original path | 115 |
| Byte-identical, moved (plus the manifest itself) | 9 |
| Modified | 20 |
| Added | 15 |
| Removed | 0 |

## Moved unchanged

- `PACKAGE_MANIFEST.json` → `reports/verification/2026-09-16-packaging/PACKAGE_MANIFEST.json`
- `reports/verification/README.md` → `reports/verification/2026-09-16-packaging/README.md`
- `reports/verification/browser-check.json` → `reports/verification/2026-09-16-packaging/browser-check.json`
- `reports/verification/coverage.json` → `reports/verification/2026-09-16-packaging/coverage.json`
- `reports/verification/editable-install.txt` → `reports/verification/2026-09-16-packaging/editable-install.txt`
- `reports/verification/environment.json` → `reports/verification/2026-09-16-packaging/environment.json`
- `reports/verification/junit.xml` → `reports/verification/2026-09-16-packaging/junit.xml`
- `reports/verification/pytest.txt` → `reports/verification/2026-09-16-packaging/pytest.txt`
- `reports/verification/wheel-build.txt` → `reports/verification/2026-09-16-packaging/wheel-build.txt`

## Modified

- `.github/workflows/ci.yml`: adds skip check, dossier verification, API smoke test and package build
- `.github/workflows/container-check.yml`: adds a read-only container start and `/healthz` probe
- `AGENTS.md`: unpublished codenames removed; LangGraph and release status updated
- `CHANGELOG.md`: publication entry
- `Makefile`: `smoke` target
- `README.md`: badges, verified-results summary, clone and smoke-test commands, LangGraph status
- `START_HERE.md`: packaging-time publishing instructions replaced by pointers to verification records
- `docs/DEVELOPMENT_NOTES.md`: replaces the package's collaboration note; records what was checked and changed at publication
- `docs/CLOUD_ARCHITECTURE.md`: verification ladder: level 2 now runs in CI
- `docs/IMPLEMENTATION_STATUS.md`: validation column updated to what has now run
- `infra/aws/README.md`: verification status: fmt/validate result from CI
- `infra/aws/main.tf`: `=` alignment for `terraform fmt`; no resource change
- `pyproject.toml`: setuptools 77+, licence file, URLs, keywords, classifiers
- `scripts/benchmark.py`: POSIX paths in the source manifest; explicit UTF-8/LF output
- `scripts/browser_check.py`: explicit UTF-8 input and output
- `scripts/build_site.py`: explicit UTF-8 input and LF output
- `scripts/export_schemas.py`: explicit UTF-8/LF output
- `scripts/render_diagrams.py`: explicit UTF-8/LF SVG output
- `scripts/verify_dossier.py`: explicit UTF-8 manifest read
- `src/asterion/reporting.py`: writes the exact bytes it hashes (Windows CRLF defect)

## Added

- `.gitattributes`: keeps LF on checkout so manifests and source hashes stay valid
- `.github/workflows/infra-validate.yml`: new: `terraform fmt -check`, `init -backend=false`, `validate`
- `reports/verification/2026-09-17-local-windows/README.md`: this publication's verification record
- `reports/verification/2026-09-17-local-windows/api-smoke.txt`
- `reports/verification/2026-09-17-local-windows/benchmark-comparison.md`
- `reports/verification/2026-09-17-local-windows/benchmark-summary.json`
- `reports/verification/2026-09-17-local-windows/cli-flows.txt`
- `reports/verification/2026-09-17-local-windows/environment.json`
- `reports/verification/2026-09-17-local-windows/junit.xml`
- `reports/verification/2026-09-17-local-windows/package-build.txt`
- `reports/verification/2026-09-17-local-windows/pytest.txt`
- `reports/verification/2026-09-17-local-windows/site-check.txt`
- `reports/verification/2026-09-17-local-windows/wheel-smoke.txt`
- `reports/verification/README.md`: new index of the dated verification records
- `scripts/api_smoke.py`: new: HTTP smoke test under uvicorn
