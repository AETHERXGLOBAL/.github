# AETHER X Public Technical Standards

**Status:** `PUBLIC ENGINEERING MATERIAL · CONTROLLED DISCLOSURE`  
**Organization:** AETHER X GLOBAL  

This directory contains selected public, technology-neutral engineering references published by AETHER X GLOBAL.

The purpose of these documents is to make parts of the company's **governed-intelligence engineering doctrine inspectable** without exposing proprietary product implementation, confidential architecture, private research records, credentials, customer information or unpublished intellectual property.

## Current Public Series

| ID | Title | Type | Public state |
|---|---|---|---|
| `AX-PUB-ARCH-001` | [Governed Intelligence Reference Architecture](./AX-PUB-ARCH-001_GOVERNED_INTELLIGENCE_REFERENCE_ARCHITECTURE.md) | Reference Architecture | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SPEC-002` | [Evidence, Authority & Verification Contract](./AX-PUB-SPEC-002_EVIDENCE_AUTHORITY_VERIFICATION_CONTRACT.md) | Control Specification | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SPEC-003` | [Point-in-Time Knowledge & Provenance Standard](./AX-PUB-SPEC-003_POINT_IN_TIME_KNOWLEDGE_PROVENANCE_STANDARD.md) | Data / Knowledge Integrity Specification | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |

## Relationship

```text
AX-PUB-ARCH-001
Governed Intelligence Reference Architecture
        ↓
AX-PUB-SPEC-002
Evidence, Authority & Verification Contract
        ↓
AX-PUB-SPEC-003
Point-in-Time Knowledge & Provenance Standard
```

Together, the current series establishes a public reference pattern for:

```text
GOVERNED KNOWLEDGE
→ TRACEABLE EVIDENCE
→ BOUNDED DECISION AUTHORITY
→ CONTROLLED EXECUTION
→ INDEPENDENT VERIFICATION
→ RECONSTRUCTABLE OUTCOMES
```

## Executable Companion

- **[AX-PUB-REF-001 — EAV Contract Validator](../reference-implementations/eav-contract-validator/README.md)** — `PUBLIC REFERENCE IMPLEMENTATION · CI-TESTED · EDUCATIONAL / NON-PRODUCTION`

The validator demonstrates selected `AX-PUB-SPEC-002` invariants in deterministic, standard-library Python code. It is intentionally bounded and does not represent a production authorization, security or policy-enforcement system.

See the **[Public Reference Implementations Index](../reference-implementations/README.md)**.

## Disclosure Boundary

Publication of a reference, specification or companion implementation does **not** establish:

- implementation by every AETHER X initiative;
- shared runtime or shared data infrastructure;
- technical integration between portfolio initiatives;
- production readiness;
- customer deployment;
- regulatory or security certification;
- commercial performance;
- predictive or investment performance.

`PUBLIC SPECIFICATION ≠ PRODUCT IMPLEMENTATION`

`REFERENCE IMPLEMENTATION ≠ PRODUCTION IMPLEMENTATION`

Each artifact defines its own additional claim boundary.

## Future Public Material

Additional specifications, reference implementations, developer tooling and research publications may be added only when they are technically ready and explicitly approved for public disclosure.

No future item should be inferred from this index until it is actually published.

---

**AETHER X GLOBAL**  
**Institutional Intelligence. Governed Autonomy.**
