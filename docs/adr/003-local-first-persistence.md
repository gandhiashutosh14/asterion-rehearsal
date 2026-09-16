# 003 — Local SQLite, explicitly not distributed persistence

Status: accepted for preview.

## Context

Fast inspection and a keyless executable slice matter for this preview.

## Decision

Use SQLite WAL, scoped idempotency and serialized review. Keep native graph checkpoints in a separate database.

## Consequences

Admission holds a transaction during work; cross-store crash atomicity is absent. This is not a scalable job service.

## Revisit when

Add managed transactional admission, outbox, queue, worker leases and recovery tests together.
