"""Witness-Coverage Gate (WCG): coverage is not probability.

Every required obligation x operational-slice cell needs compatible evidence.
Repeated happy paths cannot fill an outage cell. A hash is content integrity,
not authenticity: a hostile evaluator can fabricate a self-consistent witness.
"""
from __future__ import annotations
from .models import Assessment, Cell, Contract, Observation, Scenario, Witness, digest


def witness_identity(w: Witness) -> str:
    return digest(w.model_dump(exclude={"id", "run_id"}))


def verify_observation(run_id: str, contract: Contract, scenario: Scenario,
                       target_version: str, observation: Observation) -> list[Witness]:
    out = []
    actual = observation.model_dump()
    for obligation_id, expected in scenario.expected.items():
        observed = {key: actual[key] for key in expected}
        mismatches = sorted(k for k in expected if (type(observed[k]) is not type(expected[k]) or observed[k] != expected[k]))
        w = Witness(id="pending", run_id=run_id, contract_digest=digest(contract),
                    target_version=target_version, scenario_digest=digest(scenario),
                    scenario_id=scenario.id, slice=scenario.slice,
                    obligation_id=obligation_id, passed=not mismatches,
                    expected=expected, observed=observed, mismatches=mismatches)
        w.id = witness_identity(w)
        out.append(w)
    return out


def assess(contract: Contract, scenarios: list[Scenario], witnesses: list[Witness],
           target_version: str, run_id: str | None = None) -> Assessment:
    catalog = {s.id: s for s in scenarios}
    accepted: dict[str, Witness] = {}
    invalid = 0
    for w in witnesses:
        s = catalog.get(w.scenario_id)
        expected = s.expected.get(w.obligation_id) if s else None
        valid = (s is not None and expected is not None and w.contract_digest == digest(contract)
                 and w.scenario_digest == digest(s) and w.target_version == target_version
                 and w.slice == s.slice and w.expected == expected
                 and (run_id is None or w.run_id == run_id)
                 and set(w.observed) == set(expected)
                 and w.mismatches == sorted(k for k in expected if (type(w.observed[k]) is not type(expected[k]) or w.observed[k] != expected[k]))
                 and w.passed == (not w.mismatches) and w.id == witness_identity(w))
        if not valid:
            invalid += 1
            continue
        accepted[w.id] = w
    cells: list[Cell] = []
    for obligation in contract.obligations:
        for sl in obligation.required_slices:
            matches = [w for w in accepted.values() if w.obligation_id == obligation.id and w.slice == sl]
            state = "MISSING" if not matches else ("FAIL" if any(not w.passed for w in matches) else "PASS")
            cells.append(Cell(obligation_id=obligation.id, slice=sl, critical=obligation.critical,
                              owner=obligation.owner, status=state, witness_ids=sorted(w.id for w in matches)))
    missing = [f"{c.obligation_id}:{c.slice}" for c in cells if c.status == "MISSING"]
    failed = [f"{c.obligation_id}:{c.slice}" for c in cells if c.status == "FAIL"]
    hard_fail = any(c.critical and c.status == "FAIL" for c in cells)
    decision = "BLOCKED" if hard_fail or invalid else ("HOLD" if missing or failed else "READY_FOR_REVIEW")
    counterexamples = [{"scenario_id": w.scenario_id, "obligation_id": w.obligation_id,
                       "slice": w.slice, "expected": w.expected, "observed": w.observed,
                       "mismatches": w.mismatches, "witness_id": w.id}
                      for w in accepted.values() if not w.passed]
    return Assessment(decision=decision,
                      coverage=sum(c.status != "MISSING" for c in cells)/len(cells),
                      observed_pass_rate=sum(w.passed for w in accepted.values())/len(accepted) if accepted else 0.0,
                      cells=cells, missing_cells=missing, failed_cells=failed,
                      counterexamples=counterexamples, invalid_witnesses=invalid)
