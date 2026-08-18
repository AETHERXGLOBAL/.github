# AETHER X GLOBAL — Public Investor Evidence

## Purpose

This page is a bounded public due-diligence entry point for investors, strategic partners and institutional reviewers evaluating AETHER X GLOBAL through GitHub.

It is not a fundraising claim, investment recommendation or substitute for controlled legal, financial, security, commercial or IP diligence.

The governing principle is:

```text
PUBLIC CLAIM
→ TRACEABLE PUBLIC EVIDENCE
→ CURRENT MATURITY
→ EXPLICIT LIMITATION
```

---

## What GitHub Can Establish Publicly

| Evidence dimension | Current public evidence | State |
|---|---|---|
| Corporate identity & engineering thesis | Organization profile | `PUBLICLY DISCLOSED` |
| Governed-intelligence architecture | `AX-PUB-ARCH-001` | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| Evidence / Authority / Verification contracts | `AX-PUB-SPEC-002/003/004` | `PUBLICLY INSPECTABLE` |
| Machine-readable contracts | `AX-PUB-SCHEMA-001/002/003` | `PUBLICLY INSPECTABLE` |
| Reference validators | `AX-PUB-REF-001/002/003` | `CI-TESTED / EDUCATIONAL / NON-PRODUCTION` |
| Conformance surfaces | `AX-PUB-TEST-001/002` | `BOUNDED / SYNTHETIC / NON-PRODUCTION` |
| Artifact governance | `AX-PUB-MANIFEST-001 v1.21` + compatibility policy | `MACHINE-READABLE BASELINE` |
| Formal public engineering release | `public-engineering-vnext-1.0` + `AX-PUB-REL-001` | `PUBLIC ENGINEERING RELEASE / NON-PRODUCT` |
| Developer Contract Baseline | `AX-PUB-DEV-002` + `AX-PUB-CI-003` | `DEV-GATE-00 CLOSED` |
| Reproducible Developer Experience | `AX-PUB-DEV-003` + `AX-PUB-CI-004` | `DEV-GATE-01 CLOSED` |
| SDK Candidate | `AX-PUB-DEV-004` + `AX-PUB-CI-005` | `DEV-GATE-02 CLOSED` |
| Supply-Chain / Release Candidate | `AX-PUB-DEV-005` + `AX-PUB-CI-006 v1.1` | `DEV-GATE-03 CLOSED` |
| External Evaluation Readiness | `AX-PUB-DEV-006` + `AX-PUB-CI-007` | `DEV-GATE-04 CLOSED` |
| SDK Release Decision Baseline | `AX-PUB-DEV-007` + `AX-PUB-CI-008` | `DEV-GATE-05A CLOSED` |
| Installable Package Candidate | `AX-PUB-DEV-008` + `AX-PUB-CI-009` | `DEV-GATE-05B CLOSED` |
| Distribution & External Validation | `AX-PUB-DEV-009` + `AX-PUB-CI-010` | `DEV-GATE-05C ACTIVE · LOCAL INDEX VERIFIED` |
| Human external evaluation | No completed independent human evaluation is established | `NOT ESTABLISHED` |
| External adoption | No external developer/partner adoption is established | `NOT ESTABLISHED` |
| Public SDK publication | `AX-PUB-GATE-001` | `NOT AUTHORIZED` |
| Registry ownership | No PyPI/TestPyPI ownership claim | `NOT ESTABLISHED` |
| Public SDK licence | Target direction exists; no grant | `NOT GRANTED` |
| Production readiness | No company-wide production claim | `NOT ESTABLISHED BY THIS SURFACE` |
| Customer / pilot traction | No such evidence is asserted here | `NOT PUBLICLY ESTABLISHED` |
| Revenue / ARR / financial performance | No such evidence is asserted here | `NOT PUBLICLY ESTABLISHED` |
| Regulatory / security certification | No certification or regulatory approval is implied | `NOT ASSERTED` |

---

## Current Developer / SDK Program

```text
PROGRAM: ACTIVE / UNDER DEVELOPMENT

DEV-GATE-00  CLOSED
DEV-GATE-01  CLOSED
DEV-GATE-02  CLOSED
DEV-GATE-03  CLOSED
DEV-GATE-04  CLOSED

DEV-GATE-05  ACTIVE
  DEV-GATE-05A  CLOSED
  DEV-GATE-05B  CLOSED
  DEV-GATE-05C  ACTIVE
  DEV-GATE-05D  NOT AUTHORIZED
```

Current installable engineering candidate:

```text
Distribution: aetherxglobal-governed-intelligence
Version:      0.1.0rc1
Import:       aetherxglobal.governed_intelligence
Runtime:      Python 3.11–3.14 verified
```

Current distribution evidence:

```text
LOCAL SIMPLE-INDEX VALIDATION: VERIFIED / LOCAL ONLY
EXTERNAL REGISTRY VALIDATION: NOT ESTABLISHED / NOT AUTHORIZED
HUMAN EXTERNAL EVALUATION: NOT ESTABLISHED
EXTERNAL ADOPTION: NOT ESTABLISHED
SUPPORTED SDK: NOT ESTABLISHED
SDK PUBLICATION: NOT AUTHORIZED
```

Canonical current-state view:

**[AETHER X Governed Intelligence — Current Public Engineering State](https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence/blob/main/docs/PUBLIC_ENGINEERING_STATE.md)**

---

## Public Engineering Evidence Model

The public engineering surface is designed to be evaluated through a traceable chain rather than a capability narrative alone:

```text
SPECIFICATION
→ MACHINE-READABLE CONTRACT
→ REFERENCE / SDK BEHAVIOR
→ CONFORMANCE
→ CI RESULT
→ EVIDENCE RECORD
→ GOVERNED MATURITY STATE
```

This permits a reviewer to distinguish:

- what is conceptual;
- what is machine-readable;
- what has executable reference code;
- what has CI evidence;
- what remains under development;
- what has not been authorized.

---

## Recent Developer Evidence

### AX-PUB-CI-008

Direct validation of `DEV-GATE-05A — SDK Release Decision Baseline` across Python 3.11–3.14.

### AX-PUB-CI-009

Direct validation of the deterministic installable package candidate, including exact wheel/sdist identities and Python 3.11–3.14 installed-package verification.

Validated artifact identities:

```text
Wheel SHA-256:
bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac

sdist SHA-256:
2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99
```

### AX-PUB-CI-010

Direct validation that the exact Gate-05B package candidate can be discovered and installed through a loopback-only Python Simple Repository API-compatible index on Python 3.11–3.14.

This is local distribution engineering evidence only.

`LOCAL INDEX PASS ≠ TESTPYPI PASS`

---

## Engineering / Product Claim Boundary

The following distinctions are mandatory when interpreting this GitHub surface:

```text
PUBLIC ENGINEERING ≠ PRODUCT IMPLEMENTATION
REFERENCE VALIDATOR ≠ PRODUCTION SERVICE
CI PASS ≠ EXTERNAL CERTIFICATION
RELEASE CANDIDATE ≠ SUPPORTED SDK
INSTALLABLE CANDIDATE ≠ PUBLIC PACKAGE
LOCAL INDEX PASS ≠ EXTERNAL REGISTRY VALIDATION
HUMAN EVALUATION ≠ CI
RESEARCH ≠ PRODUCTION
DESIGN ≠ IMPLEMENTATION
```

---

## Licensing & Registry Boundary

No general open-source licence or public SDK licence is granted by publication of the current repository.

The current release-decision baseline identifies **Apache-2.0 as a target SDK licensing direction only after IP/copyright clearance and separate authority**.

Current state:

```text
LICENCE GRANTED: NO
REGISTRY OWNERSHIP: NOT ESTABLISHED
PYPI PUBLICATION: NOT AUTHORIZED
TESTPYPI VALIDATION: NOT AUTHORIZED / NOT ESTABLISHED
```

A prior exact-name reconnaissance did not discover an exact project for the candidate distribution name at that time. That observation is not ownership, reservation or a guarantee of availability at a later date.

---

## Public / Private Boundary

Core product implementations and canonical research remain private unless intentionally released.

This public GitHub surface does not expose or establish:

- private product code;
- unpublished research or invention mechanisms;
- confidential system architecture;
- customer information;
- production credentials/endpoints;
- integration between private portfolio initiatives;
- patentability or freedom-to-operate conclusions.

A public reviewer can inspect the engineering doctrine and bounded public implementation/evidence paths without being given access to confidential implementation or research.

---

## Portfolio Disclosure Boundary

Current public organization-level states include:

| Initiative / Unit | Public maturity / state |
|---|---|
| AETHER X Quantum | `UNDER ACTIVE DEVELOPMENT` |
| AX-OS | `UNDER DEVELOPMENT · ACTIVE BUILD` |
| AETHER Intelligence Core (AIC) | `APPROVED ARCHITECTURE · PRE-IMPLEMENTATION` |
| AETHER X Research | `INSTITUTIONAL RESEARCH UNIT · ACTIVE` |

Shared company doctrine does not establish technical integration among these initiatives.

---

## What Requires Controlled Diligence

A serious diligence process may require evidence that cannot or should not be inferred from a public repository, including as applicable:

- corporate/legal structure;
- capitalization;
- financial statements and revenue;
- customer or partner agreements;
- private product architecture;
- cybersecurity controls and assessments;
- IP ownership and patent/FTO analysis;
- private research evidence;
- commercial pipeline;
- regulated activity and jurisdiction-specific status.

GitHub should be treated as **one technical evidence surface**, not the total company diligence package.

---

## Diligence Principle

> **AETHER X should be evaluated on what can be evidenced at the maturity level claimed — not on what a repository name, diagram, prototype or research direction might imply.**

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**