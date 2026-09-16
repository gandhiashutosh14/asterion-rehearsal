# 001 — Bounded orchestration over a free-form swarm

Status: accepted for preview.

## Context

An FDE needs repeatable evidence and clear termination more than unconstrained agent dialogue.

## Decision

Use a planner/executor/verifier flow. The planner selects only catalog IDs; reference and LangGraph runners share domain nodes.

## Consequences

A free-form agent might explore novel failure modes but cannot alter an accepted oracle or test catalog without review. The restricted proposer trades discovery breadth for inspectability.

## Revisit when

A separate, non-authoritative research stage could propose new cases for human review, then version the catalog.
