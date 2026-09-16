# ASTERION — Handoff dossier

Status: **BLOCKED**

Engine: `reference` · Target: `scripted-optimistic-v1`

Finite synthetic acceptance checks; not a reliability probability or production certification.

Coverage: 100.0%; observed witness pass rate: 23.1%.

| Obligation | Slice | Status | Owner |
|---|---|---|---|
| R-01 | normal | PASS | support-operations |
| R-02 | erp-outage | FAIL | integration-owner |
| R-02 | crm-outage | FAIL | integration-owner |
| R-02 | missing-record | FAIL | integration-owner |
| R-03 | stale-data | FAIL | data-owner |
| R-03 | identity-conflict | FAIL | data-owner |
| R-04 | high-impact | FAIL | customer-approver |
| R-05 | duplicate-event | FAIL | platform-owner |
| R-06 | tenant-boundary | FAIL | security-review |
| R-07 | missing-owner | FAIL | deployment-owner |
| R-08 | untrusted-note | PASS | security-review |
| R-09 | slow-dependency | FAIL | platform-owner |

## Counterexamples
```json
[
  {
    "scenario_id": "crm-unavailable",
    "obligation_id": "R-02",
    "slice": "crm-outage",
    "expected": {
      "decision": "needs_information",
      "claim_completed": false,
      "effect_count": 0
    },
    "observed": {
      "decision": "resolved",
      "claim_completed": true,
      "effect_count": 1
    },
    "mismatches": [
      "claim_completed",
      "decision",
      "effect_count"
    ],
    "witness_id": "c214546eddc5a24dc7843ef22bd9823ac50af97ccf288c0fd8a2145062126d2c"
  },
  {
    "scenario_id": "duplicate-event",
    "obligation_id": "R-05",
    "slice": "duplicate-event",
    "expected": {
      "effect_count": 1
    },
    "observed": {
      "effect_count": 2
    },
    "mismatches": [
      "effect_count"
    ],
    "witness_id": "68680c012e488c70c07db24d18625349789dde202340bc73a005fc99f78a354e"
  },
  {
    "scenario_id": "erp-unavailable",
    "obligation_id": "R-02",
    "slice": "erp-outage",
    "expected": {
      "decision": "needs_information",
      "claim_completed": false,
      "effect_count": 0
    },
    "observed": {
      "decision": "resolved",
      "claim_completed": true,
      "effect_count": 1
    },
    "mismatches": [
      "claim_completed",
      "decision",
      "effect_count"
    ],
    "witness_id": "217a3d630613f2d907ac0ffd4e5bf8f1b2ad651e6e873b604311baf58c4d8c20"
  },
  {
    "scenario_id": "foreign-tenant",
    "obligation_id": "R-06",
    "slice": "tenant-boundary",
    "expected": {
      "decision": "escalated",
      "cross_tenant_read": false,
      "evidence_sources": 0,
      "effect_count": 0,
      "owner": "security-review"
    },
    "observed": {
      "decision": "resolved",
      "cross_tenant_read": true,
      "evidence_sources": 2,
      "effect_count": 1,
      "owner": "support-operations"
    },
    "mismatches": [
      "cross_tenant_read",
      "decision",
      "effect_count",
      "evidence_sources",
      "owner"
    ],
    "witness_id": "ef9ae3c0ad92351595f40e7a3c376853a23bf6ef90fe5b755f025ae8805b342a"
  },
  {
    "scenario_id": "high-impact",
    "obligation_id": "R-04",
    "slice": "high-impact",
    "expected": {
      "decision": "needs_approval",
      "claim_completed": false,
      "effect_count": 0,
      "owner": "customer-approver"
    },
    "observed": {
      "decision": "resolved",
      "claim_completed": true,
      "effect_count": 1,
      "owner": "support-operations"
    },
    "mismatches": [
      "claim_completed",
      "decision",
      "effect_count",
      "owner"
    ],
    "witness_id": "642e73fe39fd5976cf4b89d5d6ca079587bc784d7501fde6529270b4159ee281"
  },
  {
    "scenario_id": "mismatched-order",
    "obligation_id": "R-03",
    "slice": "identity-conflict",
    "expected": {
      "decision": "needs_information",
      "claim_completed": false,
      "effect_count": 0
    },
    "observed": {
      "decision": "resolved",
      "claim_completed": true,
      "effect_count": 1
    },
    "mismatches": [
      "claim_completed",
      "decision",
      "effect_count"
    ],
    "witness_id": "f5d86fa23f8feb1e29e22e3ae20a6a8f576d712f20d4ed0e3e0bb6780bf72638"
  },
  {
    "scenario_id": "missing-owner",
    "obligation_id": "R-07",
    "slice": "missing-owner",
    "expected": {
      "decision": "escalated",
      "claim_completed": false,
      "effect_count": 0,
      "owner": "deployment-owner"
    },
    "observed": {
      "decision": "resolved",
      "claim_completed": true,
      "effect_count": 1,
      "owner": "unassigned"
    },
    "mismatches": [
      "claim_completed",
      "decision",
      "effect_count",
      "owner"
    ],
    "witness_id": "7b2a647ecadd227604ddee963eb7199448d7386ea9827157c365b39a16420486"
  },
  {
    "scenario_id": "record-missing",
    "obligation_id": "R-02",
    "slice": "missing-record",
    "expected": {
      "decision": "needs_information",
      "claim_completed": false,
      "effect_count": 0
    },
    "observed": {
      "decision": "resolved",
      "claim_completed": true,
      "effect_count": 1
    },
    "mismatches": [
      "claim_completed",
      "decision",
      "effect_count"
    ],
    "witness_id": "6f6592c2b60c0682f7bffa8334e4c8dbc1f7ca71a6c7d6aff11b50e843a4a9d7"
  },
  {
    "scenario_id": "slow-dependency",
    "obligation_id": "R-09",
    "slice": "slow-dependency",
    "expected": {
      "decision": "escalated",
      "claim_completed": false,
      "effect_count": 0,
      "within_deadline": true
    },
    "observed": {
      "decision": "resolved",
      "claim_completed": true,
      "effect_count": 1,
      "within_deadline": false
    },
    "mismatches": [
      "claim_completed",
      "decision",
      "effect_count",
      "within_deadline"
    ],
    "witness_id": "bd78296a8c8465114432eae0a9ce4906f43c3a3c91a21208d7a46db3700aa99e"
  },
  {
    "scenario_id": "stale-snapshot",
    "obligation_id": "R-03",
    "slice": "stale-data",
    "expected": {
      "decision": "needs_information",
      "claim_completed": false,
      "effect_count": 0
    },
    "observed": {
      "decision": "resolved",
      "claim_completed": true,
      "effect_count": 1
    },
    "mismatches": [
      "claim_completed",
      "decision",
      "effect_count"
    ],
    "witness_id": "7ae5b84c122d0ad2a3a78b8ae85b5814b8e3749c9151f37584d465327a1b22a3"
  }
]
```

## Evidence digest
`c33c1406a47025199f168983fc2fc2e830e480619ba72012cd0ae074416bdad1`
