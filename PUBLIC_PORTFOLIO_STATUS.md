# AETHER X GLOBAL — Public GitHub Portfolio Status

Date: 2026-10-09
Scope: public repositories owned by `AETHERXGLOBAL`

## Purpose

This document is the canonical public-facing maturity map for the AETHER X GLOBAL GitHub organization.

It prevents three common errors:

1. treating research or architecture as a finished product;
2. treating a bounded product state as broader platform support, universal production readiness or independent validation;
3. treating public visibility, downloads, stars, forks, contributions or internal qualification as independent adoption.

`PUBLIC != PRODUCTION`

`QUALIFIED INTERNAL ENGINEERING EVIDENCE != INDEPENDENT EXTERNAL ADOPTION`

## Verified public repository set

At this audit point, the organization exposes four public repositories.

| Repository | Classification | Current public state | Canonical boundary |
|---|---|---|---|
| [`execsurface`](https://github.com/AETHERXGLOBAL/execsurface) | **SUPPORTED PRODUCT** | **Stable v1.0.0 — internally qualified, bounded support** | Linux x86_64; native ptrace reference observer; bounded execution-surface drift semantics |
| [`reprocert`](https://github.com/AETHERXGLOBAL/reprocert) | **SUPPORTED PRODUCT** | **Stable v1.0.0 — published and public-consumer qualified** | Exact PyPI 1.0.0, protected `@v1` Action, tested Python 3.11–3.14 on GitHub-hosted Ubuntu, Windows and macOS; bounded integrity semantics |
| [`aether-x-governed-intelligence`](https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence) | **ENTERPRISE R&D / CONTROLLED TECHNOLOGY SHOWCASE** | **R&D · pre-production evaluation** | Non-confidential public technology surface; not a public production runtime or supported SDK |
| [`.github`](https://github.com/AETHERXGLOBAL/.github) | **ORGANIZATION SURFACE** | Company profile / public portfolio navigation | Presentation and public maturity map; not a product repository |

Private repositories, unpublished research, internal product architecture and controlled engineering evidence are intentionally outside this public-repository table.

## Supported products

### ExecSurface

ExecSurface is a runtime behavioral-integrity and verification layer for execution-surface drift.

Current qualified state:

`V1_0_0_STABLE_INTERNALLY_QUALIFIED — LINUX_X86_64_PTRACE`

Public installation/distribution surfaces include crates.io, the stable GitHub Release `v1.0.0`, immutable Action pin `@v1.0.0`, and the moving stable GitHub Action channel `@v1`.

Important boundary: `ExecSurface: PASS` means no policy-relevant observed execution-surface drift under the selected baseline/policy. It does not prove that the wrapped target command succeeded or that software is safe.

Current authority: [`execsurface/docs/STATUS.md`](https://github.com/AETHERXGLOBAL/execsurface/blob/main/docs/STATUS.md)

### ReproCert

ReproCert turns an explicit technical claim, exact command, evidence and checks into a machine-readable certificate with an explicit verdict.

Current qualified state:

`REPROCERT_V1_0_0_PUBLIC_STABLE_QUALIFIED_WITH_DECLARED_LIMITATIONS`

Current public surfaces: [PyPI `aetherx-reprocert==1.0.0`](https://pypi.org/project/aetherx-reprocert/1.0.0/), immutable [GitHub Release `v1.0.0`](https://github.com/AETHERXGLOBAL/reprocert/releases/tag/v1.0.0), and protected `AETHERXGLOBAL/reprocert@v1` GitHub Action channel. The historical Alpha `0.2.2a1` and protected `@v0.2` rollback line remain preserved.

Evidence: [exact release and PyPI publication](https://github.com/AETHERXGLOBAL/reprocert/actions/runs/37844876488) and [public PyPI/Action consumer matrix — 14/14 SUCCESS](https://github.com/AETHERXGLOBAL/reprocert/actions/runs/37846420495). Internal/public self-qualification is **not** independent third-party adoption.

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

Repository-level change control is active on both supported public products, including immutable releases and ReproCert's protected movable stable channel. Public portfolio metadata is separately maintained through protected change review.

Verified at this audit point:

| Repository / ref | Protection state | Tracking |
|---|---|---|
| `execsurface/main` | **PROTECTED** | Active ruleset `Protect main`; `execsurface#133` closed completed |
| `execsurface/v1.*` exact release tags | **PROTECTED IMMUTABLE RELEASE TAGS** | Active no-bypass tag ruleset blocks update and deletion; `v1.0.0` is the current stable immutable release |
| `reprocert/main` | **PROTECTED** | Active ruleset `Protect main` |
| `reprocert/v0.2.2a1` | **PROTECTED RELEASE TAG** | Update and deletion blocked |
| `reprocert/v1.0.0` exact stable tag | **PROTECTED IMMUTABLE RELEASE TAG** | Active no-bypass ruleset #24747076 covering `refs/tags/v1.*` |
| `reprocert/v1` stable Action branch | **PROTECTED MOVABLE MAJOR CHANNEL** | Active no-bypass ruleset #24751782 blocking deletion/force pushes while allowing normal forward movement |
| `reprocert/v0.2` | **PROTECTED MOVABLE ALPHA ROLLBACK CHANNEL** | [`reprocert#25`](https://github.com/AETHERXGLOBAL/reprocert/issues/25) closed, governance PASS |
| `aether-x-governed-intelligence/main` | **PROTECTED** | Public controlled-disclosure/showcase surface; [`aether-x-governed-intelligence#13`](https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence/issues/13) closed |
| `.github/main` | **PROTECTED** | Organization presentation/governance surface; Classic Branch Protection |

For supported product `main` branches, the active controls include pull-request gating, selected required status checks, branch-current enforcement, deletion protection, non-fast-forward/force-push protection, and no configured bypass actors.

Immutable release identities are separately protected by tag rulesets that block update and deletion. Movable major-channel refs such as ExecSurface `v1` and ReproCert `v1` / `v0.2` are separate from immutable exact release identities; movement must remain deliberate, reviewable and auditable.

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
