# 005 — Publish cloud architecture without pretending to deploy it

Status: accepted for preview.

## Context

Cloud design demonstrates delivery judgment, but packaging cannot validate infrastructure it has not provisioned.

## Decision

Supply detailed AWS/Azure target diagrams and a deliberately narrow AWS foundation module. No automatic apply or rollout.

## Consequences

The reader must distinguish IaC source from tested infrastructure. Additional implementation is required for queue, identity, managed state and egress policy.

## Revisit when

Review in a sandbox, plan cost, apply explicitly, validate permissions/recovery and document teardown.
