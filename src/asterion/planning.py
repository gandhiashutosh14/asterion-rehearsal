"""Bounded planning policies. Only catalog IDs can be proposed, never code or tools."""
from __future__ import annotations
import json
import os
from typing import Protocol
from .models import Contract, PlanProposal, Scenario

class Planner(Protocol):
    name: str
    def propose(self, contract: Contract, available: list[Scenario], missing: list[str]) -> PlanProposal: ...

class DeterministicPlanner:
    name = "deterministic"
    def propose(self, contract: Contract, available: list[Scenario], missing: list[str]) -> PlanProposal:
        priorities = {r.id: int(r.critical) for r in contract.obligations}
        scored = sorted(available, key=lambda s: (-sum(priorities[r] for r in s.expected), s.id))
        return PlanProposal(scenario_ids=[s.id for s in scored],
                            rationale="Cover missing critical acceptance cells before lower-risk cells.")

class BedrockPlanner:
    """Optional live model proposer; no oracle, raw notes, or secrets enter its prompt.

    SDK request is unit-tested with a fake client. Live inference is not validated
    by the offline artifact. Model IDs and region are supplied by the operator.
    """
    name = "bedrock"
    def __init__(self, model_id: str | None = None, region: str | None = None, client=None):
        self.model_id = model_id or os.environ.get("ASTERION_BEDROCK_MODEL_ID")
        if not self.model_id:
            raise ValueError("Set ASTERION_BEDROCK_MODEL_ID to an enabled Converse-compatible model")
        if client is None:
            import boto3
            from botocore.config import Config
            client = boto3.client("bedrock-runtime", region_name=region or os.environ.get("AWS_REGION", "us-east-1"),
                                  config=Config(connect_timeout=5, read_timeout=30,
                                                retries={"mode": "standard", "total_max_attempts": 1}))
        self.client = client
    def propose(self, contract: Contract, available: list[Scenario], missing: list[str]) -> PlanProposal:
        brief = {"objective": contract.objective, "missing_cells": missing,
                 "catalog": [{"id": s.id, "slice": s.slice, "obligations": sorted(s.expected)} for s in available]}
        response = self.client.converse(
            modelId=self.model_id,
            system=[{"text": "You are the ASTERION scenario architect. Return JSON only: scenario_ids (ordered catalog IDs), rationale (short). Do not invent IDs. You cannot approve releases or change acceptance criteria."}],
            messages=[{"role": "user", "content": [{"text": json.dumps(brief)}]}],
            inferenceConfig={"maxTokens": 700, "temperature": 0.0},
        )
        text = "".join(block.get("text", "") for block in response["output"]["message"]["content"])
        return PlanProposal.model_validate_json(text)


def compile_proposal(proposal: PlanProposal, available: list[Scenario], remaining: int) -> tuple[list[Scenario], list[str]]:
    """Model suggestions have no authority to create cases or bypass the run budget."""
    by_id = {s.id: s for s in available}
    chosen, rejected, seen = [], [], set()
    for sid in proposal.scenario_ids:
        if sid not in by_id:
            rejected.append(sid)
        elif sid not in seen and len(chosen) < remaining:
            chosen.append(by_id[sid])
            seen.add(sid)
    return chosen, rejected
