.PHONY: install test demo benchmark api smoke assets
install:
	python -m pip install -e ".[api,dev]"
test:
	python -m pytest -q
demo:
	python scripts/demo.py demo
benchmark:
	python scripts/benchmark.py
api:
	python scripts/serve.py
smoke:
	python scripts/api_smoke.py
assets:
	python scripts/check_assets.py
