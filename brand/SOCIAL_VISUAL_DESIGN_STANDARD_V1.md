# AETHER X GLOBAL — Social Visual Design Standard

**Document ID:** AX-SOCIAL-VIS-001  
**Version:** 1.0  
**Date:** 2026-10-19  
**Decision:** Founder-approved visual direction for **new** social content; retrospective redesign of existing published posts is not required.  
**Scope:** LinkedIn, Facebook, and reusable corporate social visuals.  
**Authority:** Subordinate to approved AETHER X corporate identity, product/research truth, legal/IP standards, and verified website brand assets. This is a visual production standard, not an authorization to publish, change source repositories, or disclose confidential information.  
**Status:** Founder-approved working standard; proposed for canonical adoption through the linked GitHub Pull Request. Effective as the repository standard only after review and merge.

## 1. Visual North Star

**AETHER X should look like the same company on its website, GitHub, and social channels.**

Primary visual reference is the founder-supplied screenshot of the current AETHER X GLOBAL website (Products / AX-OS screen). The website visual direction is institutional, technically precise, calm, spacious, and premium: deep navy architecture, warm gold brand accents, crystalline cyan engineering light, strong typography, clean visual hierarchy. Use a predominantly light/white presentation for editorial explainers only where this matches the actual site UI; dark navy hero visuals remain the primary product-announcement system.

**Do not** imitate generic cyberpunk posters, chaotic hologram panels, stock AI robots, exaggerated skyscrapers, dense dashboards, glowing globes, or science-fiction architecture as substitutes for a real product mechanism.

## 2. Identity and exact official logo

- Use the **original, founder-supplied transparent AETHER X GLOBAL gold logo**, or a reviewed bit-identical official brand master/authorized derivative. The supplied PNG was 1254 × 1254 RGBA with transparency; preserve its geometry and gold appearance.
- **Never generate, trace, redraw, invent, replace, recolor, distort, rotate, bevel, or add glow to the logo using AI.** Build the scene and composite the unchanged approved logo above it. Do not enlarge a low-resolution asset until it becomes blurry.
- Show the complete wordmark only **once per image**, normally at upper left or upper center; keep generous clear space. Do not repeat the full company emblem inside a core/cube, floating UI, footer, or as a huge watermark.
- When a visual needs to convey the company's presence *inside* a product, the approved standalone head/circuit symbol may be used as a restrained identity marker **instead of** a repeated full lockup, subject to reviewed asset provenance.
- Third-party logos/names must not be presented as endorsements, affiliations, integrations, or partnerships without corresponding source evidence and approval.
- Website baseline reference: `AETHERXGLOBAL/aether-x-global-website-v2/docs/ASSET_MIGRATION_REGISTER.md` preserves the corporate primary-logo identity and forbids changing its original bytes.

## 3. Color system (working social design tokens)

These codes are **recommended production tokens approximating the user-supplied website screenshot**, not asserted extracts from authoritative website CSS. If source design tokens from the deployed site differ, defer to the verified site tokens and revise this derivative standard.

| Role | Recommended HEX | Usage |
|---|---|---|
| Deep corporate navy | `#082338` | Primary hero background |
| Navy shadow | `#061827` | Depth/contrast |
| Warm metallic gold | `#DDB66C` | Logo-adjacent accents, thin outlines, headline emphasis |
| Light gold | `#F0D49A` | Sparse specular highlights only |
| Technical cyan | `#4AADE7` | Data/control signal paths |
| White / cool ivory | `#F4F8FB` | Principal body and labels |
| Soft blue grey | `#A8C2D2` | Secondary information |
| Clean paper | `#F1F6F9` | Optional light editorial variants |

**Restraint:** gold is a highlight, not the whole background; cyan is a functional signal, not random decoration. Avoid high-saturation neon walls and uncontrolled bloom. Keep readable contrast at mobile scale.

## 4. Typography and text discipline

- Use the approved website Arabic and Latin typefaces where their exact identity and usage rights are verified. Do not claim that an arbitrary display font is the official website font.
- Prefer 1 short, high-value headline (3–8 English words or equivalent), optionally 1 short subtitle, product state, and a small CTA.
- Use no more than **4 functional micro-labels**, each preferably 1–3 words, in the visual. Complex details live in the actual post caption or linked technical evidence.
- English is the default for LinkedIn international B2B; Arabic may be used for dedicated Arabic/Facebook assets. Do not mix directions in complex generated image text unless typeset in a real graphics editor and reviewed.
- All product names, version numbers, platform claims, product stages, and CTA wording must be legible, manually proofread, and consistent with current authoritative project source.
- Image-generation output must NOT be trusted for precise text or logos. Typeset final text separately when feasible.

## 5. Common composition

1. **Header (top ~15%)**: a single correctly composited corporate logo; quiet whitespace.
2. **Headline (~15–30%)**: the problem or product name, immediately understandable at feed size.
3. **One main scene (~30–75%)**: visually faithful representation of the mechanism, with a single central area of attention, 2–4 subordinate elements maximum, and explicit directional flow where appropriate.
4. **Footer (~75–95%)**: the product maturity/status and one honest next step (`Try the Technical Evaluation`, `Explore the Research`, `Request a Scoped Enterprise Discussion`).
5. **Safe margins**: 6–8% on all sides. Text must still read when the visual appears at ~360 px width. No important text or content near crop edges.

Never automatically use a central cube, glass panel, globe, chart, or city skyline across every product. The **real technical workflow determines the illustration**.

## 6. Four approved image families

### A. Product / engineering
**Purpose:** show what technically goes in, how the tool acts, what comes out.

- ExecSurface: `accepted runtime baseline → observed execution → difference/REVIEW`; show bounded process/filesystem/network observations, not malware detection, real-time enforcement, or a security certification.
- ReproCert: `claim → exact command → evidence → explicit verdict → certificate`; do not imply certificate proves scientific truth or producer authenticity.
- Governed Intelligence: `AI intent → evidence/decision/authority → controlled execution interface → result verification`; label **R&D / Pre-Production Evaluation**. Do not depict it as a deployed enterprise product.
- AETHER X Quantum: describe intended analysis/strategy/validation/evidence workflow as **under development**, never guaranteed returns or live deployment unless explicitly established.

### B. Scientific research
Scientific apparatus/equations or verifiable reasoning structure; one main scientific claim and visible `Research / Preprint / Under Review` status as warranted. No fabricated awards, acceptance, peer review, or breakthroughs.

### C. Enterprise collaboration
Quiet architectural visualization of an organization's problem plus specific integration/evaluation boundary. Never show a customer's/partner's corporate logo without proven authorization. CTA can be `Scoped Technical Evaluation` when a real evaluation path exists.

### D. Institutional identity
Corporate mission/positioning, human-understandable use cases, coherent portfolio. More restrained and spacious than a product engineering diagram. Avoid meaningless tech effects.

## 7. Commercial messaging and CTA

- Every asset must answer: **Who is it for? What problem? What can be shown? What is the next action?**
- Use one CTA per post. Put working URLs in the LinkedIn/Facebook caption, rather than embedding illegible URLs in the image.
- For supported public tools, CTA may link to official public README/Quickstart/Technical Evaluation.
- For pre-production enterprise R&D, CTA is a non-confidential scoping discussion or bounded, isolated evaluation (not a ready-to-deploy procurement offer).
- Distinguish **internally qualified**, **externally reproduced**, **independently adopted**, **production deployed**, and **commercially available**. Never equate them.
- AETHER X is a multidisciplinary advanced-technology and governed-intelligence company, **not** a traditional cybersecurity firm. Product-specific safety caveats must remain intact.

## 8. Deliverable specifications

- **Master:** editable layout with logo as an imported locked asset, text as editable text, illustration as replaceable media, and clearly versioned project source.
- **Export:** PNG, sRGB, crisp text, no unsupported visual metrics.
- **Default cross-channel size:** 1200 × 1200 square; **mobile-first vertical variant:** 1080 × 1350 when the extra vertical space helps. Re-compose text, do not simply crop the master.
- **Alt text:** one factual sentence describing what the visual communicates.
- **Naming:** `AX_SOCIAL_<YYYYMMDD>_<CHANNEL>_<TOPIC>_V01.png` and corresponding source file.
- Deliver a short proof pack with every asset: product source link, verified feature/status, rights check, file version, and approved caption.

## 9. Mandatory pre-publication review / rejection gates

Mark `REVISE` if **any** are true:

- Logo is redrawn, duplicated, cropped, subtly mutated, recolored, or mismatched.
- Visual does not explain the actual product mechanism or implies capabilities the source does not support.
- Style reads as generic sci-fi/cybersecurity artwork rather than the approved website identity.
- Dense or tiny text, clipped edges, weak contrast, distorted product name/English/Arabic.
- Incorrect version, maturity, platform support, certification, external adoption, customer, or partnership claim.
- A fake software screenshot, numerical result, workflow, or endorsement is visually presented as real.
- Missing direct source evidence for a substantive claim.
- One design is exported without checking real LinkedIn/Facebook feed/mobile preview.
- No clear single CTA; or CTA promises more than an actual evaluation channel offers.
- The user has not approved the final **post + image + account + time** for publication.

## 10. Production sequence

1. Check current remote HEAD and official status/capability sources of the named product.
2. Write the visual brief: audience, product-specific causal mechanism, one headline, status, and source-backed CTA.
3. Select visual family and correct logo source; generate/illustrate **background mechanism only**.
4. Composite exact approved logo and manually typeset text in final layout; no generative alteration of marks.
5. Inspect full-resolution, 360-pixel mobile view, exact text, and website-side visual comparison.
6. Independent claim-and-identity review; mark `ACCEPT` or `REVISE`.
7. Prepare user-review package with caption, image, alt text, source URL, and account/time; **do not publish without separate approval**.

## 11. Reference and continuity notes

- Founder-supplied official transparent gold logo (chat attachment, 2026-10-19): `شعار الشركة(1).png` (SHA-256 `68f969c190e7854226dc9adb1c4065e415a54c5e4aa6fb0131372ab80365e102`, 1254×1254 RGBA, original user-supplied). Do not substitute a different logo or claim byte identity without hash verification.
- Founder-supplied website Products/AX-OS screenshot (chat attachment, 2026-10-19): `Screenshot 2026-10-17 133144(1).png`.
- Historical published LinkedIn visuals for Governed Intelligence and ExecSurface are **precedents for continuity, not canonical design masters**. Their publishing history is preserved; no retroactive rework.
- Source of company brand/identity: `https://github.com/AETHERXGLOBAL/aether-x-governance/blob/main/sources/AETHER_X_GLOBAL.md`.
- Brand source register: `https://github.com/AETHERXGLOBAL/aether-x-global-website-v2/blob/main/docs/ASSET_MIGRATION_REGISTER.md`.
- Public product maturity map: `https://github.com/AETHERXGLOBAL/.github/blob/main/PUBLIC_PORTFOLIO_STATUS.md`.

**Approval boundary:** The Founder has approved adopting this design system for **future visuals**, with repository publication separately authorized on 2026-10-19. The repository PR/merge gate controls canonical GitHub adoption; this document does not itself authorize external social posting.