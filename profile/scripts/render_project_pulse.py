#!/usr/bin/env python3
"""Render AETHER X Live Project Pulse from governed project-state sources.

Public-output rule:
- Read only explicitly selected canonical/handoff status sources for product/system initiatives.
- Represent the Research unit only through a bounded approved organizational-state disclosure.
- Publish only a small allowlisted set of derived status fields.
- Never publish source bodies, secrets, private paths, security findings, unpublished research state, or arbitrary text.
- Do not infer completion percentages.
"""

from __future__ import annotations

import base64
import html
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

API = "https://api.github.com"
ORG = "AETHERXGLOBAL"
OUTPUT = Path("profile/assets/aether-x-live-project-pulse.svg")
TOKEN_ENV = "PROJECT_PULSE_READ_TOKEN"
TIMEOUT = 25


@dataclass
class Pulse:
    name: str
    domain: str
    phase: str
    signal: str
    next_step: str
    boundary: str
    source_label: str


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def clean(value: str, limit: int = 180) -> str:
    value = str(value or "").replace("`", "").replace("**", "")
    value = re.sub(r"\s+", " ", value).strip()
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "…"


def request_json(url: str):
    token = os.getenv(TOKEN_ENV, "").strip()
    if not token:
        raise RuntimeError(f"Missing required secret: {TOKEN_ENV}")
    req = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "AETHER-X-Live-Project-Pulse",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urlopen(req, timeout=TIMEOUT) as response:
        return json.load(response)


def fetch_text(repo: str, path: str) -> str:
    data = request_json(
        f"{API}/repos/{ORG}/{repo}/contents/{quote(path, safe='/')}?ref=main"
    )
    if data.get("type") != "file" or "content" not in data:
        raise RuntimeError(f"Unexpected contents response for {repo}:{path}")
    return base64.b64decode(data["content"]).decode("utf-8", errors="replace")


def section_first_line(text: str, heading: str) -> str:
    pattern = rf"^##\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s+|\Z)"
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        return ""
    for raw in match.group(1).splitlines():
        line = raw.strip().lstrip("- ").strip()
        if line:
            return clean(line, 190)
    return ""


def parse_quantum() -> Pulse:
    """Strict public status boundary for the current V4 Quantum handoff schema.

    Never interpolate internal gate titles, accepted-gate text, next steps, or
    arbitrary source strings into a publicly rendered SVG. Canonical state is
    used only to validate restrictive execution boundaries.
    """
    text = fetch_text("aether-x-quantum", "START_HERE.md")
    begin = "<!-- AETHERX_HANDOFF_STATE_BEGIN -->"
    end = "<!-- AETHERX_HANDOFF_STATE_END -->"
    if text.count(begin) != 1 or text.count(end) != 1:
        raise RuntimeError("Quantum must have exactly one complete state block")
    first = text.index(begin)
    last = text.index(end)
    if last <= first:
        raise RuntimeError("Quantum state block marker order invalid")
    block = text[first:last + len(end)]
    match = re.fullmatch(
        r"<!-- AETHERX_HANDOFF_STATE_BEGIN -->[ \t]*\r?\n"
        r"```json[ \t]*\r?\n"
        r"(?P<state>\{[\s\S]*?\})[ \t]*\r?\n"
        r"```[ \t]*\r?\n"
        r"<!-- AETHERX_HANDOFF_STATE_END -->",
        block,
    )
    if not match:
        raise RuntimeError("Quantum state block must be complete and structurally unique")

    def unique_keys(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise RuntimeError("Quantum JSON has duplicate field names")
            obj[key] = value
        return obj

    state = json.loads(match.group("state"), object_pairs_hook=unique_keys)
    if not isinstance(state, dict):
        raise RuntimeError("Quantum handoff must be a JSON object")
    required = {
        "schema_version": "4.0.0",
        "v1_live_execution": "PROHIBITED",
        "mt5_v1": "READ_ONLY",
        "production_security_go": "NOT_GRANTED",
        "risk_acceptance": "NOT_GRANTED",
        "production_authority": "NOT_GRANTED",
        "live_trading_authority": "NOT_GRANTED",
    }
    if any(type(state.get(key)) is not str or state[key] != value
           for key, value in required.items()):
        raise RuntimeError("Quantum state schema or non-live authorization boundary changed")
    return Pulse(
        "AETHER X QUANTUM",
        "FINANCIAL STRATEGY INTELLIGENCE",
        "GOVERNED DEVELOPMENT · NO PUBLIC GATE ASSERTED",
        "No live execution or production authority is claimed.",
        "Any next step requires explicit project-gate authorization.",
        "V1 live execution: PROHIBITED",
        "START_HERE.md · limited public authorization boundary",
    )


def parse_axos() -> Pulse:
    """Treat the current canonical AX-OS status as a frozen design, not a build.

    Fail closed if the approved status schema changes. A future implementation
    transition requires an explicit public-status mapping review.
    """
    text = fetch_text("AX-OS", "PROJECT_STATUS.md")
    architecture = re.search(
        r"^Architecture:\s*\*\*FINAL v1\.1 FROZEN / APPROVED\*\*",
        text, re.MULTILINE,
    )
    implementation = re.search(
        r"^Product implementation:\s*\*\*NOT STARTED\*\*",
        text, re.MULTILINE,
    )
    kickoff = re.search(
        r"^First future engineering task:\s*\*\*(AXOS-\d{3}) READY / CONTRACT PREPARED / NOT ISSUED\*\*",
        text, re.MULTILINE,
    )
    if not (architecture and implementation and kickoff):
        raise RuntimeError("AX-OS status schema changed; public milestone qualification required")

    return Pulse(
        "AX-OS",
        "GOVERNED AI OPERATIONS",
        "ARCHITECTURE APPROVED · PRODUCT NOT STARTED",
        "Frozen architecture and pre-implementation design only; no product runtime is asserted.",
        f"{kickoff.group(1)} · CONTRACT PREPARED / NOT ISSUED",
        "NO IMPLEMENTATION, PILOT, PRODUCTION OR RELEASE AUTHORITY",
        "PROJECT_STATUS.md · canonical pre-implementation state",
    )


def governed_core_public_boundary() -> Pulse:
    """Bounded, non-live entry until a canonical approved source is readable.

    The retired AIC repository name is not a valid source for the successor.
    Do not turn an inaccessible project into a claimed verified milestone.
    """
    return Pulse(
        "AETHER X GOVERNED INTELLIGENCE CORE",
        "VERIFIABLE AUTONOMOUS INTELLIGENCE INFRASTRUCTURE",
        "DEVELOPMENT · NOT PUBLICLY VERIFIED",
        "No current externally verified project gate is asserted by this dashboard.",
        "Consult canonical project evidence before publishing a milestone.",
        "NO PRODUCTION OR RELEASE READINESS IS ASSERTED",
        "Public disclosure boundary · no live project status",
    )


def research_unit_state() -> Pulse:
    """Return only the approved public organizational state of AETHER X Research.

    Individual research records remain private by default and are intentionally not
    queried or summarized by the public pulse.
    """
    return Pulse(
        "AETHER X RESEARCH",
        "RESEARCH & DECISION INTEGRITY",
        "INSTITUTIONAL RESEARCH UNIT · ACTIVE",
        "Dedicated company Research unit established; AMII is managed as a research program within the governed research lifecycle.",
        "Individual research remains private and subject to evidence, validation, IP and publication controls.",
        "RESEARCH ≠ PRODUCTION · PUBLIC DISCLOSURE REQUIRES APPROVAL",
        "AETHER X public organizational state",
    )


def wrap(text: str, max_chars: int, max_lines: int = 2) -> list[str]:
    words = clean(text, 600).split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join(current + [word])
        if current and len(candidate) > max_chars:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = clean(lines[-1], max_chars - 1) + "…"
    return lines


def svg_lines(x: int, y: int, lines: list[str], cls: str, gap: int = 23) -> str:
    return "\n".join(
        f'<text x="{x}" y="{y + i * gap}" class="{cls}">{esc(line)}</text>'
        for i, line in enumerate(lines)
    )


def render_card(p: Pulse, x: int, y: int, accent: str, pill_fill: str) -> str:
    phase_lines = wrap(p.phase, 73, 2)
    signal_lines = wrap(p.signal, 92, 2)
    next_lines = wrap(p.next_step, 92, 2)
    boundary_lines = wrap(p.boundary, 102, 1)
    return f'''
  <g transform="translate({x} {y})">
    <rect width="700" height="390" rx="24" fill="url(#panel)" stroke="{accent}" stroke-width="1.6"/>
    <rect x="30" y="28" width="112" height="3" rx="1.5" fill="{accent}"/>
    <text x="34" y="76" class="cardTitle">{esc(p.name)}</text>
    <text x="34" y="106" class="domain">{esc(p.domain)}</text>
    <rect x="34" y="128" width="632" height="58" rx="11" fill="{pill_fill}" stroke="{accent}" stroke-opacity=".75"/>
    {svg_lines(52, 155, phase_lines, 'phase', 20)}

    <text x="34" y="222" class="label">VERIFIED SIGNAL</text>
    {svg_lines(34, 247, signal_lines, 'body', 22)}

    <text x="34" y="304" class="label">NEXT AUTHORIZED / GOVERNED STEP</text>
    {svg_lines(34, 329, next_lines, 'body', 22)}

    <line x1="34" y1="365" x2="666" y2="365" stroke="#26364b"/>
    <text x="34" y="383" class="source">{esc(clean(p.source_label, 82))}</text>
    {svg_lines(666, 383, boundary_lines, 'boundaryEnd', 18)}
  </g>'''


def render(pulses: list[Pulse]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    cards = [
        render_card(pulses[0], 70, 210, "#DEB459", "#2B2418"),
        render_card(pulses[1], 830, 210, "#4F86C6", "#11243A"),
        render_card(pulses[2], 70, 630, "#B08A4A", "#2B2418"),
        render_card(pulses[3], 830, 630, "#8B5CA8", "#25192E"),
    ]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1100" viewBox="0 0 1600 1100" role="img" aria-labelledby="title desc">
<title id="title">AETHER X Live Project Pulse</title>
<desc id="desc">Automatically refreshed, public-safe project-state telemetry for selected AETHER X system initiatives plus a bounded public organizational-state disclosure for the Research unit. No completion percentages are inferred.</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#010D1D"/><stop offset="0.55" stop-color="#071426"/><stop offset="1" stop-color="#0B1A2C"/></linearGradient>
  <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#101B2B"/><stop offset="1" stop-color="#0B1524"/></linearGradient>
  <pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse"><path d="M34 0H0V34" fill="none" stroke="#8FA0B5" stroke-opacity="0.035"/></pattern>
  <style>
    .brand{{font:700 18px Inter,Segoe UI,Arial,sans-serif;letter-spacing:4.5px;fill:#DEB459}}
    .title{{font:800 38px Inter,Segoe UI,Arial,sans-serif;fill:#F4F4F3}}
    .subtitle{{font:400 17px Inter,Segoe UI,Arial,sans-serif;fill:#AAB3BD}}
    .cardTitle{{font:800 25px Inter,Segoe UI,Arial,sans-serif;fill:#F4F4F3}}
    .domain{{font:700 13px Inter,Segoe UI,Arial,sans-serif;letter-spacing:1.05px;fill:#C9A86A}}
    .phase{{font:800 13px Inter,Segoe UI,Arial,sans-serif;letter-spacing:.4px;fill:#F2D99F}}
    .label{{font:800 10.5px Inter,Segoe UI,Arial,sans-serif;letter-spacing:1.1px;fill:#7F90A6}}
    .body{{font:500 13.5px Inter,Segoe UI,Arial,sans-serif;fill:#D5DCE5}}
    .source{{font:500 10.5px Inter,Segoe UI,Arial,sans-serif;fill:#6F7D89}}
    .boundaryEnd{{font:600 9.5px Inter,Segoe UI,Arial,sans-serif;fill:#9B8A70;text-anchor:end}}
    .footer{{font:600 12px Inter,Segoe UI,Arial,sans-serif;fill:#8E9BAD}}
    .footerGold{{font:800 12px Inter,Segoe UI,Arial,sans-serif;letter-spacing:.8px;fill:#DEB459}}
  </style>
</defs>
<rect width="1600" height="1100" rx="30" fill="url(#bg)"/>
<rect width="1600" height="1100" rx="30" fill="url(#grid)"/>
<rect x="24" y="24" width="1552" height="1052" rx="24" fill="none" stroke="#243247" stroke-width="1.5"/>
<text x="70" y="70" class="brand">AETHER X GLOBAL</text>
<text x="70" y="122" class="title">LIVE PROJECT PULSE</text>
<text x="70" y="154" class="subtitle">Selected live project telemetry · governed sources · bounded Research-unit disclosure</text>
<text x="1530" y="72" text-anchor="end" class="footerGold">AUTO-REFRESH · PUBLIC-SAFE</text>
<text x="1530" y="100" text-anchor="end" class="footer">Last verified refresh: {esc(now)}</text>
<line x1="70" y1="184" x2="1530" y2="184" stroke="#9D753C" stroke-opacity=".7"/>
{''.join(cards)}
<rect x="70" y="1040" width="1460" height="38" rx="12" fill="#0A1422" stroke="#243247"/>
<text x="95" y="1064" class="footerGold">PROGRESS SIGNAL = GOVERNED STATE CHANGE / ACCEPTED MILESTONE</text>
<text x="1505" y="1064" text-anchor="end" class="footer">COMMIT ≠ PROGRESS · MERGE ≠ ACCEPTANCE · RESEARCH ≠ PRODUCTION</text>
</svg>'''


def main() -> int:
    try:
        pulses = [parse_quantum(), parse_axos(), governed_core_public_boundary(), research_unit_state()]
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(render(pulses), encoding="utf-8")
        print("PROJECT_PULSE_RENDER_PASS")
        for pulse in pulses:
            print(f"{pulse.name}: {pulse.phase}")
        return 0
    except Exception as exc:
        print(f"PROJECT_PULSE_RENDER_FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
