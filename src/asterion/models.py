"""Strict contracts; the target never receives its evaluation oracle."""
from __future__ import annotations
from hashlib import sha256
import json
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

class Obligation(StrictModel):
    id: str = Field(pattern=r"^R-[0-9]{2}$")
    title: str = Field(min_length=3, max_length=180)
    owner: str = Field(min_length=1, max_length=80)
    critical: bool = True
    required_slices: list[str] = Field(min_length=1, max_length=20)

    @model_validator(mode="after")
    def distinct(self):
        if len(set(self.required_slices)) != len(self.required_slices):
            raise ValueError("required slices must be unique")
        return self

class Contract(StrictModel):
    id: str = Field(pattern=r"^[a-z0-9-]{1,60}$")
    version: str = Field(min_length=1, max_length=40)
    customer: str = Field(min_length=1, max_length=100)
    objective: str = Field(min_length=10, max_length=1000)
    data_classification: Literal["synthetic"] = "synthetic"
    obligations: list[Obligation] = Field(min_length=1, max_length=40)
    @model_validator(mode="after")
    def distinct(self):
        ids = [r.id for r in self.obligations]
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate obligation id")
        return self

class CaseInput(StrictModel):
    tenant: str = Field(pattern=r"^[a-z0-9-]{1,60}$")
    record_tenant: str = Field(pattern=r"^[a-z0-9-]{1,60}$")
    order_id: str = Field(min_length=1, max_length=60)
    event_id: str = Field(min_length=1, max_length=60)
    crm_order_id: str = Field(min_length=1, max_length=60)
    amount_units: int = Field(ge=0, le=1_000_000)
    age_seconds: int = Field(ge=0, le=100000)
    erp_available: bool = True
    crm_available: bool = True
    order_exists: bool = True
    has_owner: bool = True
    duplicate: bool = False
    simulated_delay_ms: int = Field(ge=0, le=100000)
    note: str = Field(max_length=1000)

class Scenario(StrictModel):
    id: str = Field(pattern=r"^[a-z0-9-]{1,60}$")
    title: str = Field(min_length=1, max_length=180)
    slice: str = Field(min_length=1, max_length=60)
    inputs: CaseInput
    # Independent curated assertions. Never supplied to a target adapter.
    expected: dict[str, dict[str, Any]]
    @model_validator(mode="after")
    def not_empty(self):
        if not self.expected or any(not checks for checks in self.expected.values()):
            raise ValueError("scenario must contain nonempty assertions")
        return self

class Observation(StrictModel):
    decision: Literal["resolved", "escalated", "needs_approval", "needs_information"]
    owner: str
    claim_completed: bool
    evidence_sources: int = Field(ge=0)
    effect_count: int = Field(ge=0)
    cross_tenant_read: bool = False
    note_as_instruction: bool = False
    within_deadline: bool = True
    trace: list[dict[str, Any]] = Field(default_factory=list)

class Witness(StrictModel):
    id: str
    run_id: str
    contract_digest: str
    target_version: str
    scenario_digest: str
    scenario_id: str
    slice: str
    obligation_id: str
    passed: bool
    expected: dict[str, Any]
    observed: dict[str, Any]
    mismatches: list[str]

class Cell(StrictModel):
    obligation_id: str
    slice: str
    critical: bool
    owner: str
    status: Literal["PASS", "FAIL", "MISSING"]
    witness_ids: list[str]

class Assessment(StrictModel):
    decision: Literal["BLOCKED", "HOLD", "READY_FOR_REVIEW"]
    coverage: float = Field(ge=0, le=1)
    observed_pass_rate: float = Field(ge=0, le=1)
    cells: list[Cell]
    missing_cells: list[str]
    failed_cells: list[str]
    counterexamples: list[dict[str, Any]]
    invalid_witnesses: int = 0
    disclaimer: str = "Finite synthetic acceptance checks; not a reliability probability or production certification."

class RunRequest(StrictModel):
    profile: Literal["guarded", "optimistic"] = "guarded"
    suite: Literal["complete", "happy-only"] = "complete"
    engine: Literal["reference", "langgraph"] = "reference"
    planner: Literal["deterministic", "bedrock"] = "deterministic"
    max_cases: int = Field(default=32, ge=1, le=64)
    max_rounds: int = Field(default=4, ge=1, le=8)

class ReviewRequest(StrictModel):
    decision: Literal["approve", "reject"]
    expected_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    rationale: str = Field(min_length=5, max_length=2000)

class PlanProposal(StrictModel):
    scenario_ids: list[str] = Field(max_length=32)
    rationale: str = Field(min_length=1, max_length=1000)


def canonical(value: Any) -> str:
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json")
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def digest(value: Any) -> str:
    return sha256(canonical(value).encode()).hexdigest()
