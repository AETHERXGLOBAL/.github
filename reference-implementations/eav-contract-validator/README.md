# EAV Contract Validator — Public Reference Implementation

**Artifact ID:** `AX-PUB-REF-001`  
**Status:** `PUBLIC REFERENCE IMPLEMENTATION · EDUCATIONAL / NON-PRODUCTION`  
**Related Specification:** `AX-PUB-SPEC-002 — Evidence, Authority & Verification Contract`  
**Organization:** AETHER X GLOBAL  

## Purpose

This small reference implementation demonstrates how selected invariants from `AX-PUB-SPEC-002` can be represented as deterministic validation rules.

It is intentionally simple, dependency-free and non-product-specific.

It validates a JSON bundle containing:

```text
Evidence Records
→ Decision Records
→ Authority Grants
→ Execution Records
→ Verification Records
→ Verified Outcome Records
```

The implementation is designed to make several governance boundaries inspectable in executable code.

## What It Checks

The validator currently checks, among other things:

- unique control-object identifiers;
- required evidence metadata;
- supported evidence classifications;
- decisions reference existing evidence;
- authority grants reference existing decisions;
- authority state is explicit;
- authority expiry is later than grant time when an expiry is supplied;
- execution references an existing decision and authority grant;
- execution requires `ACTIVE` authority;
- execution actor matches the granted principal;
- execution action matches the permitted action;
- execution resource remains inside the granted resource scope;
- execution does not begin before authority is granted or after it expires;
- verification references an execution;
- independent-verification requirements are respected when requested;
- only a `PASS` verification may produce a `VERIFIED` outcome.

## Public Claim Boundary

This artifact is **not** a production authorization system, security control plane, policy engine, identity system, transaction system or product SDK.

It does **not** establish or imply:

- implementation inside AETHER X Quantum, AX-OS, AIC or AETHER X Research;
- production readiness;
- secure authorization enforcement;
- cryptographic integrity;
- distributed-consistency guarantees;
- regulatory compliance;
- customer deployment;
- technical integration between AETHER X initiatives.

`REFERENCE IMPLEMENTATION ≠ PRODUCT IMPLEMENTATION`

`VALIDATOR PASS ≠ SECURITY APPROVAL`

`EXECUTION COMPLETE ≠ VERIFIED`

## Requirements

Python 3.10+ is recommended.

The implementation uses the Python standard library only.

## Run

Validate the passing example:

```bash
python3 validator.py examples/valid_bundle.json
```

Expected output:

```text
AX_EAV_REFERENCE_VALIDATION_PASS
```

Validate the intentionally failing example:

```bash
python3 validator.py examples/invalid_bundle.json
```

The process exits with code `1` and prints the detected contract violations.

For structured output:

```bash
python3 validator.py examples/invalid_bundle.json --json
```

## Tests

Run:

```bash
python3 -m unittest discover -s tests -v
```

The repository workflow also runs compilation, unit tests, the valid example and the expected-failure example automatically when this reference implementation changes.

## Design Intent

This implementation favors **semantic clarity over framework complexity**.

It is deliberately not an SDK. The objective is to make the governance concepts independently inspectable before any developer-facing package is considered mature enough to publish.

## Related Public Material

- `AX-PUB-ARCH-001 — Governed Intelligence Reference Architecture`
- `AX-PUB-SPEC-002 — Evidence, Authority & Verification Contract`
- `AX-PUB-SPEC-003 — Point-in-Time Knowledge & Provenance Standard`

---

**AETHER X GLOBAL**  
**Institutional Intelligence. Governed Autonomy.**
