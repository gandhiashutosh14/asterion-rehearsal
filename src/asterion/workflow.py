"""Shared real nodes used by both the reference runner and optional LangGraph.

Reference mode is explicitly labeled; it is not a fake LangGraph implementation.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, TypedDict
from .catalog import load_catalog
from .evidence import assess, verify_observation
from .models import Contract, RunRequest, Scenario, Witness, digest
from .planning import BedrockPlanner, DeterministicPlanner, compile_proposal
from .telemetry import span
from .twin import ScriptedTarget

class State(TypedDict, total=False):
    run_id: str
    request: dict[str, Any]
    contract: dict[str, Any]
    scenarios: list[dict[str, Any]]
    target_version: str
    completed_ids: list[str]
    selected_ids: list[str]
    witnesses: list[dict[str, Any]]
    observations: list[dict[str, Any]]
    assessment: dict[str, Any]
    events: list[dict[str, Any]]
    rounds: int
    evidence_digest: str
    status: str
    review: dict[str, Any]


def event(state: State, stage: str, **details) -> list[dict[str, Any]]:
    # These are workflow events, not model private reasoning.
    return [*state.get("events", []), {"sequence": len(state.get("events", [])) + 1,
             "stage": stage, "at": datetime.now(timezone.utc).isoformat(), **details}]


def intake(state: State) -> dict:
    with span("asterion.intake"):
        request = RunRequest.model_validate(state["request"])
        contract, scenarios = load_catalog()
        return {"contract": contract.model_dump(), "scenarios": [s.model_dump() for s in scenarios],
                "target_version": ScriptedTarget(request.profile).version, "rounds": 0,
                "completed_ids": [], "witnesses": [], "observations": [],
                "events": event(state, "intake", contract_id=contract.id, classification="synthetic")}


def discover(state: State) -> dict:
    return {"events": event(state, "integration_cartographer", connectors=["synthetic-crm-v1", "synthetic-erp-v1"],
                             mode="in-process fixture; no external connections")}


def plan(state: State) -> dict:
    with span("asterion.plan"):
        req = RunRequest.model_validate(state["request"])
        available = [Scenario.model_validate(s) for s in state["scenarios"] if s["id"] not in state["completed_ids"]
                     and (req.suite != "happy-only" or s["slice"] == "normal")]
        contract = Contract.model_validate(state["contract"])
        planner = BedrockPlanner() if req.planner == "bedrock" else DeterministicPlanner()
        proposal = planner.propose(contract, available, state.get("assessment", {}).get("missing_cells", []))
        batch, rejected = compile_proposal(proposal, available, min(4, req.max_cases-len(state["completed_ids"])))
        return {"selected_ids": [s.id for s in batch], "rounds": state["rounds"] + 1,
                "events": event(state, "scenario_architect", planner=planner.name,
                                selected=[s.id for s in batch], rejected_ids=rejected)}


def rehearse(state: State) -> dict:
    with span("asterion.rehearse"):
        target = ScriptedTarget(state["request"]["profile"])
        contract = Contract.model_validate(state["contract"])
        by_id = {s["id"]: Scenario.model_validate(s) for s in state["scenarios"]}
        witnesses = list(state["witnesses"])
        observations = list(state["observations"])
        for sid in state["selected_ids"]:
            scenario = by_id[sid]
            observed = target.execute(scenario.inputs)  # Oracle intentionally absent.
            witnesses.extend(w.model_dump() for w in verify_observation(state["run_id"], contract, scenario,
                                                                        target.version, observed))
            observations.append({"scenario_id": sid, "observation": observed.model_dump()})
        return {"witnesses": witnesses, "observations": observations,
                "completed_ids": state["completed_ids"] + state["selected_ids"],
                "events": event(state, "rehearsal_fabric", count=len(state["selected_ids"]), external_writes=0)}


def evaluate(state: State) -> dict:
    with span("asterion.evaluate"):
        result = assess(Contract.model_validate(state["contract"]),
                        [Scenario.model_validate(s) for s in state["scenarios"]],
                        [Witness.model_validate(w) for w in state["witnesses"]],
                        state["target_version"], state["run_id"])
        return {"assessment": result.model_dump(), "events": event(state, "witness_gate", decision=result.decision,
                                                                   coverage=result.coverage)}


def next_step(state: State) -> str:
    req = RunRequest.model_validate(state["request"])
    eligible = [s for s in state["scenarios"] if s["id"] not in state["completed_ids"]
                and (req.suite != "happy-only" or s["slice"] == "normal")]
    # Continue after a failing case to produce a complete diagnostic dossier.
    if (eligible and state["selected_ids"] and len(state["completed_ids"]) < req.max_cases
            and state["rounds"] < req.max_rounds):
        return "plan"
    return "seal"


def seal(state: State) -> dict:
    payload = {"contract": state["contract"], "target_version": state["target_version"],
               "request": state["request"], "witnesses": state["witnesses"],
               "observations": state["observations"], "assessment": state["assessment"]}
    d = digest(payload)
    status = "PENDING_REVIEW" if state["assessment"]["decision"] == "READY_FOR_REVIEW" else state["assessment"]["decision"]
    return {"evidence_digest": d, "status": status,
            "events": event(state, "handoff_seal", evidence_digest=d, status=status)}


def run_reference(run_id: str, request: RunRequest) -> State:
    state: State = {"run_id": run_id, "request": request.model_dump(), "events": []}
    for node in (intake, discover):
        state.update(node(state))
    while True:
        for node in (plan, rehearse, evaluate):
            state.update(node(state))
        if next_step(state) == "seal":
            break
    state.update(seal(state))
    return state
