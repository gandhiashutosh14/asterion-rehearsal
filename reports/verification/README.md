# Verification records

Each folder is a dated record of commands that actually ran and what they produced. A skipped
test is recorded as skipped, not passed. Nothing here is a production-readiness claim.

| Record | Where it ran | Summary |
|---|---|---|
| [2026-09-16-packaging](2026-09-16-packaging/README.md) | The Linux sandbox that produced the original package (Python 3.13.5), without network access to install LangGraph | 70 passed, the native LangGraph module skipped, about 89% coverage; benchmark, schema export, asset check, dossier verification, a Playwright check of the offline explorer, and a wheel build |
| [2026-09-17-local-windows](2026-09-17-local-windows/README.md) | Windows 11, Python 3.11.9, before the first push | 73 passed with no skips, including the LangGraph interrupt/resume tests; 94% coverage; benchmark evidence digests identical to the packaging run; CLI on both engines; HTTP API under uvicorn; wheel built and run outside the source tree; one Windows defect in dossier export found and fixed |
| [GitHub Actions](https://github.com/gandhiashutosh14/asterion-rehearsal/actions) | Hosted runners, on every push | See the section below |

## About the packaging record

The files in `2026-09-16-packaging/` are byte-identical to the package as received; only their
folder changed. `PACKAGE_MANIFEST.json` in that folder lists the SHA-256 of every file in the
original package, with paths relative to the original root (for example, the packaging
`reports/verification/pytest.txt` is now `2026-09-16-packaging/pytest.txt`, and the manifest
itself was at the repository root). Its `README.md` refers to paths from that original location.
[`2026-09-17-local-windows/provenance.md`](2026-09-17-local-windows/provenance.md) lists which
files were changed, moved or added before publication.

## GitHub Actions

Workflow definitions live in `.github/workflows/`. Results are recorded here once runs complete.
