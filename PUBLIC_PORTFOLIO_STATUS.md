# AETHER X GLOBAL — Public GitHub Portfolio Status

Date: 2026-10-03
Scope: public repositories owned by `AETHERXGLOBAL`

## Purpose

This document is the canonical public-facing maturity map for the AETHER X GLOBAL GitHub organization.

It prevents three common errors:

1. treating research or architecture as a finished product;
2. treating a supported Alpha as stable v1 or universal production readiness;
3. treating public visibility, downloads, stars, forks, contributions or internal qualification as independent adoption.

`PUBLIC != PRODUCTION`

`QUALIFIED INTERNAL ENGINEERING EVIDENCE != INDEPENDENT EXTERNAL ADOPTION`

## Verified public repository set

At this audit point, the organization exposes four public repositories.

| Repository | Classification | Current public state | Canonical boundary |
|---|---|---|---|
| [`execsurface`](https://github.com/AETHERXGLOBAL/execsurface) | **SUPPORTED PRODUCT** | **Final Supported Alpha — v0.1.0-alpha.5** | Linux x86_64; native ptrace reference observer; bounded execution-surface drift semantics |
| [`reprocert`](https://github.com/AETHERXGLOBAL/reprocert) | **SUPPORTED PRODUCT** | **Final Supported Alpha — v0.2.2a1** | Python/CLI/GitHub Action product boundary; tested Python 3.11–3.14 on GitHub-hosted Ubuntu, Windows and macOS |
| [`aether-x-governed-intelligence`](https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence) | **ENTERPRISE R&D / CONTROLLED TECHNOLOGY SHOWCASE** | **R&D · pre-production evaluation** | Non-confidential public technology surface; not a public production runtime or supported SDK |
| [`.github`](https://github.com/AETHERXGLOBAL/.github) | **ORGANIZATION SURFACE** | Company profile / public portfolio navigation | Presentation and public maturity map; not a product repository |

Private repositories, unpublished research, internal product architecture and controlled engineering evidence are intentionally outside this public-repository table.

## Supported products

### ExecSurface

ExecSurface is a runtime behavioral-integrity and verification layer for execution-surface drift.

Current qualified state:

`ALPHA5_FINAL_SUPPORTED_ALPHA_WITH_DECLARED_LIMITATIONS — LINUX_X86_64_PTRACE`

Public installation/distribution surfaces include crates.io, GitHub Releases and a stable GitHub Action channel.

Important boundary: `ExecSurface: PASS` means no policy-relevant observed execution-surface drift under the selected baseline/policy. It does not prove that the wrapped target command succeeded or that software is safe.

Current authority: [`execsurface/docs/STATUS.md`](https://github.com/AETHERXGLOBAL/execsurface/blob/main/docs/STATUS.md)

### ReproCert

ReproCert turns an explicit technical claim, exact command, evidence and checks into a machine-readable certificate with an explicit verdict.

Current qualified state:

`REPROCERT_0_2_2A1_FINAL_SUPPORTED_ALPHA_WITH_DECLARED_LIMITATIONS`

Public installation/distribution surfaces include PyPI and the stable `AETHERXGLOBAL/reprocert@v0.2` GitHub Action channel.

Important boundary: certificate integrity does not by itself authenticate the producer, prove evidence-source truth, establish scientific validity or constitute security certification.

Current authority: [`reprocert/docs/STATUS.md`](https://github.com/AETHERXGLOBAL/reprocert/blob/main/docs/STATUS.md)

## Enterprise R&D

### AETHER X Governed Intelligence

Governed Intelligence is the current public enterprise-technology direction for governed AI execution where evidence, authority, controlled action, state and verification must remain explicit.

Its public repository is intentionally a controlled, non-confidential technology surface.

Current state:

`R&D · PRE-PRODUCTION EVALUATION`

It must not be represented as a publicly supported production runtime, open-source SDK, deployed customer system or independently validated commercial platform without separate evidence.

## Research

AETHER X Research remains primarily private and evidence-controlled. Public research output is disclosed separately only after the applicable publication, affiliation, rights and disclosure gates are satisfied.

A public preprint or DOI is a public research artifact; it is not equivalent to peer review, independent verification, product readiness or customer adoption.

## Repository-governance audit

Repository-level change control is now active on both supported public products. Remaining open governance work is limited to mutable/public presentation surfaces and the ReproCert stable channel.

Verified at this audit point:

| Repository / ref | Protection state | Tracking |
|---|---|---|
| `execsurface/main` | **PROTECTED** | Active ruleset `Protect main`; `execsurface#133` closed completed |
| `execsurface/v0.1.0-alpha.5` | **PROTECTED RELEASE TAG** | Update and deletion blocked |
| `reprocert/main` | **PROTECTED** | Active ruleset `Protect main` |
| `reprocert/v0.2.2a1` | **PROTECTED RELEASE TAG** | Update and deletion blocked |
| `reprocert/v0.2` | **NOT PROTECTED** | Remaining governance task: [`reprocert#25`](https://github.com/AETHERXGLOBAL/reprocert/issues/25) |
| `aether-x-governed-intelligence/main` | **NOT PROTECTED** | Public controlled-disclosure/showcase surface; tracked by [`aether-x-governed-intelligence#13`](https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence/issues/13) |
| `.github/main` | **NOT PROTECTED** | Organization presentation/governance surface; repository Issues are disabled |

For supported product `main` branches, the active controls include pull-request gating, selected required status checks, branch-current enforcement, deletion protection, non-fast-forward/force-push protection, and no configured bypass actors.

Immutable release identities are separately protected by tag rulesets that block update and deletion. Stable channel refs such as ReproCert `v0.2` are intentionally movable only when their movement is deliberate, reviewable and auditable.

The public Governed Intelligence repository is not the proprietary core implementation repository. Its role is controlled public technology disclosure and evaluation positioning; protection of that presentation surface is separate from governance of the private core.

Repository protection is a governance control. It does not retroactively change the technical qualification evidence for already-published release artifacts.

## External-adoption boundary

AETHER X does not count its own tests, synthetic fixtures, package publication, downloads, stars, outreach or internally controlled integrations as independent adoption.

Independent adoption requires attributable third-party use or integration evidence that satisfies the relevant product's evidence rules.

External criticism, failed reproductions, portability defects and negative integration results remain valid evidence and must not be filtered out merely because they are unfavorable.

## Portfolio operating rule

Public repositories should use one of these maturity labels unless a more specific product-defined status is required:

- **SUPPORTED PRODUCT** — a bounded product state with an explicit support/qualification contract;
- **R&D / PRE-PRODUCTION** — implemented or evaluated technology not yet represented as a supported production product;
- **RESEARCH** — scientific or technical investigation with explicit evidence and publication boundaries;
- **ARCHIVE / HISTORICAL** — retained provenance or superseded material not presented as current operating state;
- **ORGANIZATION SURFACE** — company/profile/navigation material, not a product.

When two documents disagree, the current repository-specific status authority and immutable release evidence take precedence over older milestone, roadmap or marketing text.
