# 002 — Separate target inputs from expected outcomes

Status: accepted for preview.

## Context

A tested policy must not receive its own golden labels.

## Decision

The target adapter accepts CaseInput only. The independent verifier consumes Scenario.expected after observation.

## Consequences

The public fixture dataset can still be memorized; authored tests and scripted policies are not an unbiased model benchmark.

## Revisit when

Freeze held-out customer labels and separate case authors from target authors before a model comparison.
