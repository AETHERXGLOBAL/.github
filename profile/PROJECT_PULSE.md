# AETHER X Live Project Pulse

## Purpose

`AETHER X Live Project Pulse` is a public-safe, automatically refreshed view of selected AETHER X project-state signals plus a bounded organizational-state disclosure for the dedicated AETHER X Research unit.

It is designed to show **governed state, accepted milestones, current phase/gate and the next authorized or governed step** for selected product/system initiatives without exposing private repository content. The Research card is intentionally different: it confirms only the public organizational state of the institutional Research unit and does not publish internal scientific status, hypotheses, experiments, unpublished results or other private research records.

## Public-claim boundary

The dashboard must not infer or publish:

- aggregate product-completion percentages without an approved deterministic weighting contract;
- profitability, predictive performance, production readiness or investment outcomes;
- technical integration between AETHER X projects unless separately approved and evidenced;
- private research state, unpublished scientific results or internal research records;
- private source text, private branch names, credentials, security findings, unpublished architecture or confidential execution detail.

The dashboard follows these semantics:

`COMMIT ≠ PROGRESS`  
`MERGE ≠ ACCEPTANCE`  
`RESEARCH ≠ PRODUCTION`  
`DESIGN ≠ IMPLEMENTATION`  

A public progress signal for a product/system initiative is derived only from an allowlisted governed state source or acceptance record. The Research-unit card is a bounded organizational disclosure, not research-result telemetry.

## Read-only source scope

The renderer reads only selected status/handoff material from these private product/system repositories using the repository secret `PROJECT_PULSE_READ_TOKEN` with `Contents: Read-only` access:

- `AETHERXGLOBAL/aether-x-quantum`
- `AETHERXGLOBAL/AX-OS`
- `AETHERXGLOBAL/aether-intelligence-core-AIC-`

Current allowlisted source paths:

- Quantum: `START_HERE.md` machine-readable durable handoff state.
- AX-OS: `PROJECT_STATUS.md`.
- AIC: `05_AIC_CURRENT_STATE.md`.

### Research-unit publication boundary

`AETHER X Research` is presented as an **institutional Research unit**, not as a fourth product project and not as a public feed of private research records.

The public card may state only the approved organizational facts needed to understand the company structure, including that **AMII / AETHER Market Intent Index is managed as a research program within the Research unit**. It must not expose the private research registry, additional unpublished research programs, scientific evidence, experimental status, IP analysis, publication-gate details or any claim not separately approved for public disclosure.

The former standalone `amii-research-lab` repository is not a Live Project Pulse source.

## Update model

The public SVG is generated at:

`profile/assets/aether-x-live-project-pulse.svg`

The GitHub Actions workflow refreshes it on a five-minute schedule, on manual dispatch, and when the renderer/workflow changes. A `repository_dispatch` hook is also supported for a future event-driven `project_state_changed` signal.

If a required product/system source cannot be read or parsed, rendering fails closed and the last successfully verified public SVG remains unchanged. The visible `Last published state update` timestamp records the time of the last public state actually committed; it is not a claim that every scheduled poll produced a new state.

## Security model

- Private-project credential: read-only, repository-scoped fine-grained token.
- Public profile repository write: the workflow's local `GITHUB_TOKEN` only.
- No private source body is copied into the public repository.
- Published fields are deliberately allowlisted and condensed.
- Research-unit disclosure is constrained to approved public organizational state rather than private research telemetry.
- The secret value must never be printed, committed or embedded in generated output.
