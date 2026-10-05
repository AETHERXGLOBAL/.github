<p align="center">
  <img src="./assets/aether-x-premium-banner.png" alt="AETHER X GLOBAL" width="100%" />
</p>

<h1 align="center">AETHER X GLOBAL</h1>

<p align="center"><strong>Verification · Evidence · Governed Execution · Advanced Research</strong></p>
<p align="center"><strong>Financial Markets · Artificial Intelligence · Advanced Technology</strong></p>

<p align="center">
  AETHER X GLOBAL is a multidisciplinary research and technology company developing verifiable software systems, governed AI infrastructure, quantitative technologies and evidence-driven research.
</p>

<p align="center"><em>AETHER X GLOBAL is currently under formation.</em></p>

---

## Start Here — Public Products

AETHER X currently maintains two public open-source products intended for immediate hands-on use. Both have completed bounded final supported-Alpha qualification against their documented product scopes.

### [ExecSurface](https://github.com/AETHERXGLOBAL/execsurface)

**Runtime behavioral integrity for CI, dependencies, developer tools and AI-assisted workflows.**

```text
accepted runtime behavior -> observed execution -> deterministic drift -> PASS / REVIEW / BLOCK / ERROR
```

**Current state:** `FINAL SUPPORTED ALPHA — v0.1.0-alpha.5`

- Apache-2.0 open source
- Rust CLI + GitHub Action
- public supported scope: Linux x86_64
- native `ptrace` reference observer
- crates.io + GitHub Release distribution
- self-service: no signup, API key or approval required

Important boundary: `ExecSurface: PASS` means no policy-relevant observed execution-surface drift under the selected baseline/policy. It does not prove that the wrapped command succeeded or that software is safe.

**[Explore ExecSurface →](https://github.com/AETHERXGLOBAL/execsurface)** · [Five-Minute Start](https://github.com/AETHERXGLOBAL/execsurface/blob/main/docs/QUICKSTART_5_MIN.md) · [Current Status](https://github.com/AETHERXGLOBAL/execsurface/blob/main/docs/STATUS.md)

### [ReproCert](https://github.com/AETHERXGLOBAL/reprocert)

**Claim-to-evidence reproducibility certificates for software, AI and research workflows.**

```text
CLAIM -> EXACT COMMAND -> EVIDENCE -> VERDICT -> CERTIFICATE
```

**Current state:** `FINAL SUPPORTED ALPHA — v0.2.2a1`

- Apache-2.0 open source
- Python CLI + GitHub Action
- PyPI distribution
- qualified on Python 3.11–3.14 across tested GitHub-hosted Ubuntu, Windows and macOS environments
- pytest, JUnit, suite, policy, predicate and hardened Docker integration paths
- self-service project scaffolding

Important boundary: certificate integrity does not by itself authenticate the producer, establish evidence-source truth, prove scientific validity or constitute security certification.

**[Explore ReproCert →](https://github.com/AETHERXGLOBAL/reprocert)** · [Five-Minute Start](https://github.com/AETHERXGLOBAL/reprocert/blob/main/docs/QUICKSTART_5_MIN.md) · [Current Status](https://github.com/AETHERXGLOBAL/reprocert/blob/main/docs/STATUS.md)

Technical criticism, failed reproductions, portability defects, counterexamples and independent integrations are welcome. AETHER X does not relabel its own tests, downloads, stars or internally controlled use as independent adoption.


---

## External Technical Impact

AETHER X contributes technical analysis to external engineering discussions where its runtime-integrity and evidence-boundary work is directly relevant.

### OpenAI Codex — daemon restart / execution-continuity bug

In `openai/codex#50299`, AETHER X contributed a runtime-continuity framing that separated **daemon reachability** from **restoration of the same in-flight execution**. The external reporter explicitly confirmed that this distinction matched the failure they had been debugging. An OpenAI maintainer later stated that a fix was in place and expected in a future Codex release.

**Primary sources:** [OpenAI Codex issue #50299](https://github.com/openai/codex/issues/50299) · [AETHER X technical comment](https://github.com/openai/codex/issues/50299#issuecomment-5953229001) · [External acknowledgement](https://github.com/openai/codex/issues/50299#issuecomment-5953856631) · [OpenAI maintainer fix note](https://github.com/openai/codex/issues/50299#issuecomment-5970421966)

**Evidence boundary:** this is external technical engagement and impact evidence. It does **not** mean OpenAI adopted, integrated, endorsed, or used ExecSurface itself, and it is not represented as product validation.

[ExecSurface impact record →](https://github.com/AETHERXGLOBAL/execsurface/issues/160)

---

## Enterprise R&D

### [AETHER X Governed Intelligence](https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence)

**Institutional AI execution with explicit evidence, authority, controlled action, state and verification.**

```text
AI AGENT / MODEL / AUTOMATION
            ↓ proposed action
AETHER X GOVERNED INTELLIGENCE
            ↓ approved, bounded request
APPROVED ENTERPRISE API / CONNECTOR
            ↓
ENTERPRISE SYSTEM
            ↓ result / state / evidence
AETHER X GOVERNED INTELLIGENCE
```

**Current state:** `R&D · PRE-PRODUCTION EVALUATION`

The public repository is a controlled, non-confidential technology surface. It is not a public production runtime or supported SDK. Proprietary implementation, detailed schemas, validators, private test suites and internal release evidence remain controlled.

**[Explore Governed Intelligence →](https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence)** · [Executive Brief](https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence/blob/main/docs/EXECUTIVE_BRIEF.md) · [Enterprise Evaluation](https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence/blob/main/docs/ENTERPRISE_EVALUATION.md)

`PUBLIC TECHNOLOGY SHOWCASE · CONTROLLED DISCLOSURE · NO GENERAL OPEN-SOURCE LICENCE`

---

## Research

AETHER X Research operates through a private canonical research system with explicit source authority, provenance, reproducibility, negative-evidence retention, publication-state controls and disclosure gates.

### Verified public research output

**AXR-2026-009 — Localizable Bipartite Rank-One Ideal Measurements Have a Block-Replicated Nice-Bell Structure**

- field: Quantum Physics (`quant-ph`)
- public record: [arXiv:2609.22181](https://arxiv.org/abs/2609.22181)
- DOI: [10.48550/arXiv.2609.22181](https://doi.org/10.48550/arXiv.2609.22181)
- public state: `PUBLIC ARXIV PREPRINT`

The public manuscript lists the author affiliation as **Independent Researcher**. AETHER X therefore presents it accurately as an AETHER X-associated research output rather than changing the scholarly affiliation recorded by arXiv.

`PUBLIC PREPRINT != PEER REVIEW` · `PUBLICATION != INDEPENDENT VERIFICATION`

[Public Research Publication Record →](./RESEARCH_PUBLICATIONS.md)

---

## Public Portfolio Map

| Public surface | Classification | Current state | What the label means |
|---|---|---|---|
| **ExecSurface** | `SUPPORTED PRODUCT` | `FINAL SUPPORTED ALPHA` | Bounded, qualified public product; not stable v1 or universal production-readiness claim |
| **ReproCert** | `SUPPORTED PRODUCT` | `FINAL SUPPORTED ALPHA` | Bounded, qualified public product; not stable v1 or independent-adoption claim |
| **AETHER X Governed Intelligence** | `ENTERPRISE R&D` | `PRE-PRODUCTION EVALUATION` | Controlled technology evaluation surface; not public production runtime |
| **AETHER X Research** | `RESEARCH` | `ACTIVE` | Evidence-controlled research program; public outputs disclosed separately after applicable gates |

For the canonical repository-by-repository maturity and governance audit, see **[Public GitHub Portfolio Status](../PUBLIC_PORTFOLIO_STATUS.md)**.

---

## Broader Private Portfolio

AETHER X maintains additional private or controlled initiatives. Public mention does not imply public source availability, production deployment or commercial readiness.

| Initiative | Disclosed state | Primary role |
|---|---|---|
| **AETHER X Quantum** | `UNDER ACTIVE DEVELOPMENT` | Financial-markets platform initiative for technical analysis, strategy engineering, quantitative validation and controlled decision workflows |
| **AX-OS** | `APPROVED ARCHITECTURE · IMPLEMENTATION NOT STARTED` | Institutional intelligence operating-system architecture for objectives, teams, governed execution, evidence and verification |
| **AETHER Intelligence Core (AIC)** | `APPROVED ARCHITECTURE · PRE-IMPLEMENTATION` | Separate strategic infrastructure direction for high-integrity financial information, point-in-time correctness and provenance |
| **AETHER X Research** | `INSTITUTIONAL RESEARCH UNIT · ACTIVE` | Applied research across AI, computing, quantitative methods, financial markets and selected scientific and technological domains |

AIC is separate from AX-OS. Architecture approval is not product implementation evidence.

---

## Engineering & Research Discipline

AETHER X engineering and research work is organized around explicit evidence boundaries rather than maturity by assertion.

Core operating principles include:

`OUTPUT != FACT`  
`RECOMMENDATION != DECISION`  
`CAPABILITY != AUTHORITY`  
`TOOL AVAILABILITY != TOOL PERMISSION`  
`EXECUTION COMPLETE != VERIFIED OUTCOME`  
`PUBLICATION != SCIENTIFIC VERIFICATION`  
`INTERNAL QUALIFICATION != INDEPENDENT ADOPTION`

Material failures, negative results, portability defects, conflicting evidence and external criticism are retained rather than silently rewritten into positive evidence.

---

## Public / Private Boundary

AETHER X uses progressive disclosure.

### Public surfaces may include

- supported open-source products and public release artifacts;
- company and portfolio positioning;
- public-safe architecture and engineering summaries;
- explicit maturity and limitation statements;
- research publications approved for public disclosure;
- enterprise evaluation pathways and licensing boundaries.

### Private or controlled systems may include

- proprietary source code and implementation contracts;
- internal SDKs, validators and schemas;
- private test corpora and adversarial suites;
- unpublished hypotheses and research evidence;
- confidential datasets and data-rights records;
- internal release, provenance and diligence artifacts;
- customer-specific or commercial implementations.

`PUBLIC DISCLOSURE != IMPLEMENTATION DISCLOSURE`

---

## Enterprise Engagement

Qualified organizations evaluating proprietary AETHER X technology use a progressive-disclosure path:

```text
NON-CONFIDENTIAL DISCUSSION
→ NDA / EVALUATION TERMS
→ CONTROLLED TECHNICAL DILIGENCE
→ BOUNDED EVALUATION / PILOT
→ COMMERCIAL LICENCE / STRATEGIC AGREEMENT
```

AETHER X's default commercial objective is to retain ownership of underlying proprietary technology while granting clearly scoped usage rights appropriate to the transaction.

[Enterprise Evaluation & Licensing →](https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence/blob/main/docs/ENTERPRISE_EVALUATION.md)

---

## Current Governance Boundary

The two supported public products now use active repository rulesets on `main`, with pull-request gating, selected required CI checks, deletion/force-push protection and no configured bypass actors. Their current immutable release tags are separately protected from update and deletion.

Remaining governance work is explicitly limited to mutable stable-channel and public presentation surfaces; it does not reduce the already-qualified product state. The public Governed Intelligence repository is a controlled-disclosure/showcase surface, not the proprietary core implementation repository.

See **[Public GitHub Portfolio Status](../PUBLIC_PORTFOLIO_STATUS.md)** for the current verified governance state.

---

## Company Status

AETHER X GLOBAL is currently under formation. Portfolio labels describe disclosed engineering, research and product maturity only. They do not imply customer adoption, regulatory approval, commercial deployment, peer review, independent validation or stable-v1 compatibility unless separately evidenced.

<p align="center"><strong>AETHER X GLOBAL</strong></p>
<p align="center"><strong>Verification · Evidence · Governed Execution · Advanced Research</strong></p>
