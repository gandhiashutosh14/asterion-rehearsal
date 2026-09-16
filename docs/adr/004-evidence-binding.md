# 004 — Bind approval to evidence, not a mutable success label

Status: accepted for preview.

## Context

A reviewer must know whether the artifact changed since inspection.

## Decision

Hash the complete evidence payload and recompute before serialized approval. Export a file manifest.

## Consequences

Hashes prove neither origin nor correctness. The local operator and evaluator remain trusted. Target version is a string, not binary attestation.

## Revisit when

Add authenticated artifact identities and independent verification before relying on cross-organization approval.
