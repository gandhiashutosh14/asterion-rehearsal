# Contributing

Start with `AGENTS.md` and the implementation status. Keep changes narrow, add a failing test first for behavior changes, regenerate schemas when contracts change, and regenerate reports when their underlying source changes. Never update golden expectations only to fit target behavior.

Use Python 3.11+, run `python -m pytest -q`, `python scripts/benchmark.py --output artifacts/check`, and `python scripts/check_assets.py`. Native framework changes require the optional integration suite; note skips explicitly. Cloud changes require separate validation and must not add automatic apply or production rollout to a push workflow.

Do not include customer data, credentials, proprietary code, model private reasoning or misleading benchmark claims. Explain new assumptions, include negative cases and update the appropriate ADR. There is no guaranteed maintainer response time for this portfolio project.
