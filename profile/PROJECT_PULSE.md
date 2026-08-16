# AETHER X Live Project Pulse

## Purpose

`AETHER X Live Project Pulse` is a public-safe, automatically refreshed view of selected AETHER X project-state signals.

It is designed to show **governed state, accepted milestones, current phase/gate and the next authorized or governed step** without exposing private repository content.

## Public-claim boundary

The dashboard must not infer or publish:

- aggregate product-completion percentages without an approved deterministic weighting contract;
- profitability, predictive performance, production readiness or investment outcomes;
- technical integration between AETHER X projects unless separately approved and evidenced;
- private source text, private branch names, credentials, security findings, unpublished architecture or confidential execution detail.

The dashboard follows these semantics:

`COMMIT ≠ PROGRESS`  
`MERGE ≠ ACCEPTANCE`  
`RESEARCH ≠ PRODUCTION`  
`DESIGN ≠ IMPLEMENTATION`  

A public progress signal is derived only from an allowlisted governed state source or acceptance record.

## Read-only source scope

The renderer reads only selected status/handoff material from these private repositories using the repository secret `PROJECT_PULSE_READ_TOKEN` with `Contents: Read-only` access:

- `AETHERXGLOBAL/aether-x-quantum`
- `AETHERXGLOBAL/AX-OS`
- `AETHERXGLOBAL/aether-intelligence-core-AIC-`
- `AETHERXGLOBAL/amii-research-lab`

Current allowlisted source paths:

- Quantum: `START_HERE.md` machine-readable durable handoff state.
- AX-OS: `PROJECT_STATUS.md`.
- AIC: `05_AIC_CURRENT_STATE.md`.
- AMII: the latest governance acceptance record matching `*ACCEPTANCE*.md` in `governance/`.

## Update model

The public SVG is generated at:

`profile/assets/aether-x-live-project-pulse.svg`

The GitHub Actions workflow refreshes it on a five-minute schedule, on manual dispatch, and when the renderer/workflow changes. A `repository_dispatch` hook is also supported for a future event-driven `project_state_changed` signal.

If a required source cannot be read or parsed, rendering fails closed and the last successfully verified public SVG remains unchanged. The visible `Last verified refresh` timestamp therefore also acts as a freshness signal.

## Security model

- Private-project credential: read-only, repository-scoped fine-grained token.
- Public profile repository write: the workflow's local `GITHUB_TOKEN` only.
- No private source body is copied into the public repository.
- Published fields are deliberately allowlisted and condensed.
- The secret value must never be printed, committed or embedded in generated output.
