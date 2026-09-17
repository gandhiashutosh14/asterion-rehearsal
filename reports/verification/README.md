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

Workflow definitions live in `.github/workflows/`. Results for the first published commit, `79e48ac`, on 2026-09-17. The runs below executed before that commit's author metadata was rewritten; the code they tested is unchanged.

| Workflow | Trigger | Result |
|---|---|---|
| [reference-and-framework-tests](https://github.com/gandhiashutosh14/asterion-rehearsal/actions/runs/35153403237) | push | Passed on Python 3.11, 3.12 and 3.13. Each job: 73 passed, 0 skipped, 0 failures; 94% coverage; benchmark exported; all eight dossier manifests (four committed, four fresh) verified; asset check passed; 10 of 10 API smoke checks; sdist and wheel built |
| [infra-validate](https://github.com/gandhiashutosh14/asterion-rehearsal/actions/runs/35153443028) | manual (path filters do not fire on a repository's first push) | Passed: Terraform 1.16.3, hashicorp/aws 6.64.0, `fmt -check`, `init -backend=false`, `validate` ("The configuration is valid") |
| [container-recipe-check](https://github.com/gandhiashutosh14/asterion-rehearsal/actions/runs/35153419324) | manual | Passed: image built; catalog loaded 13 scenarios inside it; a read-only container with all capabilities dropped returned `{"status":"ok","mode":"synthetic-only","version":"0.1.0"}` from `/healthz`, running as user `10001:10001` |
| publish-image-with-oidc | manual only | Not run: it needs an AWS account, role and protected environment that do not exist |

Later runs are listed on the [Actions page](https://github.com/gandhiashutosh14/asterion-rehearsal/actions).
