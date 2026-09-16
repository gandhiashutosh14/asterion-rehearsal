"""In-process synthetic CRM/ERP twin. No sockets, vendor SDKs, or customer writes.

This is a finite behavioral fixture, not a calibrated digital twin of a real business.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .models import CaseInput, Observation


@dataclass
class FixtureTwin:
    inputs: CaseInput
    effects: dict[str, dict[str, Any]] = field(default_factory=dict)
    trace: list[dict[str, Any]] = field(default_factory=list)
    def read(self, system: str) -> dict[str, Any] | None:
        self.trace.append({"tool": f"{system}.read", "mode": "synthetic"})
        available = self.inputs.erp_available if system == "erp" else self.inputs.crm_available
        if not available or (system == "erp" and not self.inputs.order_exists):
            return None
        return {"tenant": self.inputs.record_tenant, "order_id": self.inputs.order_id if system == "erp" else self.inputs.crm_order_id,
                "age_seconds": self.inputs.age_seconds, "amount_units": self.inputs.amount_units}
    def record_effect(self, payload: dict[str, Any], *, idempotent: bool) -> None:
        key = self.inputs.event_id if idempotent else f"{self.inputs.event_id}-{len(self.effects)}"
        if key not in self.effects:
            self.effects[key] = payload
            self.trace.append({"tool": "crm.record_simulated_action", "key": key, "mode": "synthetic"})


class ScriptedTarget:
    """Two transparent policies for testing the gate, not model-performance claims."""
    def __init__(self, profile: str):
        if profile not in {"guarded", "optimistic"}:
            raise ValueError("unknown target profile")
        self.profile = profile
        self.version = f"scripted-{profile}-v1"

    def execute(self, inputs: CaseInput) -> Observation:
        world = FixtureTwin(inputs)
        decision = "resolved"
        completed = True
        owner = "support-operations"
        sources = 0
        cross = False
        delay_ok = inputs.simulated_delay_ms <= 2000
        scope_allowed = inputs.record_tenant == inputs.tenant
        erp = world.read("erp") if scope_allowed or self.profile == "optimistic" else None
        crm = world.read("crm") if scope_allowed or self.profile == "optimistic" else None
        sources = int(erp is not None) + int(crm is not None)
        if self.profile == "guarded":
            if inputs.record_tenant != inputs.tenant:
                # Scope is checked BEFORE any synthetic record is read.
                decision, completed, sources, owner = "escalated", False, 0, "security-review"
            elif not delay_ok:
                decision, completed = "escalated", False
            elif erp is None or crm is None:
                decision, completed = "needs_information", False
            elif inputs.age_seconds > 300 or inputs.crm_order_id != inputs.order_id:
                decision, completed = "needs_information", False
            elif not inputs.has_owner:
                decision, completed, owner = "escalated", False, "deployment-owner"
            elif inputs.amount_units > 1000:
                decision, completed, owner = "needs_approval", False, "customer-approver"
            delay_ok = True  # modeled deadline guard, not a wall-clock measurement
        else:
            cross = inputs.record_tenant != inputs.tenant
            if not inputs.has_owner:
                owner = "unassigned"
        if completed:
            world.record_effect({"decision": decision}, idempotent=self.profile == "guarded")
            if inputs.duplicate:
                world.record_effect({"decision": decision}, idempotent=self.profile == "guarded")
        return Observation(decision=decision, owner=owner, claim_completed=completed,
                           evidence_sources=sources, effect_count=len(world.effects),
                           cross_tenant_read=cross, note_as_instruction=False,
                           within_deadline=delay_ok, trace=world.trace)
