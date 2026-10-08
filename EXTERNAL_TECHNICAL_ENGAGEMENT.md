# AETHER X GLOBAL — Selected External Technical Engagements

This is the full source-preserving engagement record moved from the public organization profile for readability. Source issue/comment links, technical caveats and non-adoption disclaimers are retained. The canonical original wording and history also remain available in earlier `profile/README.md` commits.

## Selected External Technical Impact

AETHER X contributes architecture-level technical analysis where runtime identity, evidence, authority and execution semantics intersect with real engineering failures. The records below link directly to primary-source discussions and preserve strict claim boundaries.

### NVIDIA OpenShell — execution-generation lifecycle safety

In [NVIDIA/OpenShell #4009](https://github.com/NVIDIA/OpenShell/issues/4009), AETHER X separated **target identity** from **target execution generation** and proposed a serialized compare-and-act contract for lifecycle operations:

`request_id != expected_execution`

The analysis distinguishes idempotency from causal targeting, requires stale or unverifiable execution preconditions to fail closed, and defines retry semantics so an old stop request cannot silently retarget a replacement execution.

After the initial discussion, the issue author published a [live Go SDK reproduction](https://github.com/danehans/openshell-4009-repro) showing the stale-target class across both **stop/start** and **delete/recreate** replacement paths. AETHER X then contributed a tighter execution-incarnation and conformance-test contract.

**Primary sources:** [OpenShell issue #4009](https://github.com/NVIDIA/OpenShell/issues/4009) · [initial AETHER X invariant](https://github.com/NVIDIA/OpenShell/issues/4009#issuecomment-5952940030) · [external live reproduction](https://github.com/NVIDIA/OpenShell/issues/4009#issuecomment-6002850688) · [AETHER X follow-up contract](https://github.com/NVIDIA/OpenShell/issues/4009#issuecomment-6015380839)

**Evidence boundary:** this establishes substantive external technical engagement and independently published evidence for the same stale-target problem class. It does **not** mean NVIDIA adopted, integrated, endorsed or used ExecSurface.

[ExecSurface impact record →](https://github.com/AETHERXGLOBAL/execsurface/issues/161)

### OpenAI Codex — thread identity and control-surface addressability

In [openai/codex #49729](https://github.com/openai/codex/issues/49729), AETHER X framed a cross-control-surface contract:

`thread existence / validity != addressability from every control surface`

The analysis proposed a canonical opaque thread reference, typed placement/routing incompatibility instead of generic `NOT_FOUND`, and explicit capability-generation state for delegated native tools.

Subsequent Windows and macOS reports supplied useful positive controls: the same local conversation could remain valid through native or fresh-helper routes while the parent Dot route still failed. AETHER X synthesized those reports into a narrower routing/placement conformance matrix.

**Primary sources:** [Codex issue #49729](https://github.com/openai/codex/issues/49729) · [AETHER X identity/placement analysis](https://github.com/openai/codex/issues/49729#issuecomment-5968783804) · [Windows positive control](https://github.com/openai/codex/issues/49729#issuecomment-6004491806) · [macOS positive control](https://github.com/openai/codex/issues/49729#issuecomment-6012498003) · [AETHER X synthesis](https://github.com/openai/codex/issues/49729#issuecomment-6015514240)

**Evidence boundary:** this is multi-reporter external evidence for a real identity/routing failure class plus an AETHER X technical synthesis. It does **not** mean OpenAI adopted the proposed design or used ExecSurface.

[ExecSurface impact record →](https://github.com/AETHERXGLOBAL/execsurface/issues/162)

### OpenAI Codex — daemon restart / execution continuity

In [openai/codex #50299](https://github.com/openai/codex/issues/50299), AETHER X contributed a runtime-continuity framing that separated **daemon reachability** from **restoration of the same in-flight execution**. The external reporter explicitly confirmed that this distinction matched the failure they had been debugging. An OpenAI maintainer later stated that a fix was in place and expected in a future Codex release.

**Primary sources:** [OpenAI Codex issue #50299](https://github.com/openai/codex/issues/50299) · [AETHER X technical comment](https://github.com/openai/codex/issues/50299#issuecomment-5953229001) · [external acknowledgement](https://github.com/openai/codex/issues/50299#issuecomment-5953856631) · [OpenAI maintainer fix note](https://github.com/openai/codex/issues/50299#issuecomment-5970421966)

**Evidence boundary:** this is external technical engagement and impact evidence. It does **not** mean OpenAI adopted, integrated, endorsed or used ExecSurface itself, and it is not represented as product validation.

[ExecSurface impact record →](https://github.com/AETHERXGLOBAL/execsurface/issues/160)

### in-toto Attestation — AI generation provenance and runtime authority

In [in-toto Attestation #604](https://github.com/in-toto/attestation/issues/604), AETHER X proposed that provenance for generated code ranges, human/agent sign-off evidence and observed runtime effects represent **distinct claims**, not interchangeable certificates or authorization decisions. The initial [AETHER X contribution](https://github.com/in-toto/attestation/issues/604#issuecomment-5949924701) explicitly separated authorship, review approval and execution-effect evidence.

A [predicate specification participant's reply](https://github.com/in-toto/attestation/issues/604#issuecomment-5958028833) explicitly agreed with that trust boundary, noted related language already present in the normative acceptance-check contract, and said the registration document would explicitly state that generation/review provenance does not attest runtime behavior. This **does not** prove AETHER X authored the specification, that a final normative document incorporated novel AETHER X code, or that in-toto adopted ExecSurface.

**Primary sources:** [Issue #604](https://github.com/in-toto/attestation/issues/604) · [AETHER X boundary comment](https://github.com/in-toto/attestation/issues/604#issuecomment-5949924701) · [specification participant acknowledgement](https://github.com/in-toto/attestation/issues/604#issuecomment-5958028833)

**Evidence boundary:** source-supported acknowledgement of a technical distinction in an open standards discussion; **not** project adoption, standards-body endorsement, partnership or independent product validation.

> **Evidence standard:** external discussion, reproduction, acknowledgement and fix-path evidence are recorded separately from product adoption, endorsement and independent validation. AETHER X does not collapse those categories.


---

