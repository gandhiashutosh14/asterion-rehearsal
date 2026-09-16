# Start here

## Inspect without installing anything

Open `site/index.html` in a browser. Select the four measured case studies, compare required-cell coverage with observed witness pass rate, and inspect the counterexamples. This is an offline explorer of shipped results, not a live backend. Then read the [architecture](docs/ARCHITECTURE.md) and [verification scope](docs/IMPLEMENTATION_STATUS.md).

## Run the implemented slice

Install `.[api,dev]`, run `python scripts/demo.py demo`, then open `artifacts/latest/report.html`. Run the tests and `python scripts/benchmark.py --output artifacts/benchmark`. The default run is deterministic, synthetic, local and keyless after dependency installation. LangGraph and live model integrations are opt-in (`.[agent]`, `.[cloud]`).

## See what was actually verified

[`reports/verification/`](reports/verification/README.md) holds dated records: the original packaging run, the local run made before this repository was published, and GitHub Actions results. Each lists the commands that ran and what did not run.

## Continue the work

Read [`AGENTS.md`](AGENTS.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md) first. Keep changes narrow, keep the maturity labels, and record new verification in a new dated folder rather than editing an old one.

The codenames are branding, not novelty or trademark-clearance claims. Do not describe the optional or unvalidated integrations (live Bedrock, OTLP export, the cloud targets) as tested production systems. The research question is worth exploring without overstating what v0.1 proves.
