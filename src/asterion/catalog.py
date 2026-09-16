"""Bundled synthetic case catalog with structural and oracle integrity checks."""
from __future__ import annotations
from importlib.resources import files
import json
import yaml
from .models import Contract, Observation, Scenario


def load_catalog() -> tuple[Contract, list[Scenario]]:
    root = files("asterion").joinpath("data")
    contract = Contract.model_validate(yaml.safe_load(root.joinpath("contract.synthetic.yaml").read_text()))
    scenarios = [Scenario.model_validate(x) for x in json.loads(root.joinpath("scenarios.synthetic.json").read_text())]
    validate_catalog(contract, scenarios)
    return contract, scenarios


def validate_catalog(contract: Contract, scenarios: list[Scenario]) -> None:
    by_id = {r.id: r for r in contract.obligations}
    if len({s.id for s in scenarios}) != len(scenarios):
        raise ValueError("duplicate scenario id")
    allowed_fields = set(Observation.model_fields) - {"trace"}
    covered = set()
    for s in scenarios:
        for rid, assertions in s.expected.items():
            if rid not in by_id or s.slice not in by_id[rid].required_slices:
                raise ValueError(f"undeclared obligation/slice {rid}:{s.slice}")
            if not set(assertions) <= allowed_fields:
                raise ValueError("oracle uses unknown observation field")
            covered.add((rid, s.slice))
    required = {(r.id, sl) for r in contract.obligations for sl in r.required_slices}
    if required - covered:
        raise ValueError(f"catalog has no scenario for {sorted(required-covered)}")
