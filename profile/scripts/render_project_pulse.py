#!/usr/bin/env python3
"""Render AETHER X Live Project Pulse from governed project-state sources.

Public-output rule:
- Read only explicitly selected canonical/handoff status sources.
- Publish only a small allowlisted set of derived status fields.
- Never publish source bodies, secrets, private paths, security findings, or arbitrary text.
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


def clean(value: str, limit: int = 150) -> str:
    value = re.sub(r"\s+", " ", str(value or "")).strip()
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


def fetch_dir(repo: str, path: str):
    data = request_json(
        f"{API}/repos/{ORG}/{repo}/contents/{quote(path, safe='/')}?ref=main"
    )
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected directory response for {repo}:{path}")
    return data


def section_first_line(text: str, heading: str) -> str:
    pattern = rf"^##\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s+|\Z)"
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        return ""
    for raw in match.group(1).splitlines():
        line = raw.strip().lstrip("- ").strip()
        if line:
            return line
    return ""


def parse_quantum() -> Pulse:
    text = fetch_text("aether-x-quantum", "START_HERE.md")
    match = re.search(
        r"<!-- AETHERX_HANDOFF_STATE_BEGIN -->\s*```json\s*(\{[\s\S]*?\})\s*```",
        text,
    )
    if not match:
        raise RuntimeError("Quantum machine-readable handoff state not found")
    state = json.loads(match.group(1))

    priority = clean(state.get("current_product_priority", ""), 220)
    gate_match = re.search(r"(Gate\s+\d+\s+—\s+[^.=]+)\s*=\s*([^.;]+)", priority)
    if gate_match:
        phase = f"{clean(gate_match.group(1), 64)} · {clean(gate_match.group(2), 34)}"
    else:
        phase = "ACTIVE DEVELOPMENT"

    accepted = clean(state.get("last_externally_accepted_gate", ""), 180)
    if accepted:
        gate_id = accepted.split("—", 1)[0].strip()
        signal = f"Latest externally accepted gate: {gate_id}"
    else:
        signal = "No externally accepted gate is asserted by the current handoff."

    next_step = clean(
        state.get("next_authorized_product_action_after_governance_acceptance")
        or state.get("next_authorized_governance_action")
        or "",
        150,
    )
    boundary = (
        "V1 live execution: PROHIBITED"
        if str(state.get("v1_live_execution_boundary", "")).lower() == "prohibited"
        else "Execution authority remains governed by the current project boundary."
    )
    return Pulse(
        "AETHER X QUANTUM",
        "FINANCIAL STRATEGY INTELLIGENCE",
        phase,
        signal,
        next_step or "Next bounded action is not asserted in the current handoff.",
        boundary,
        "START_HERE.md · governed handoff",
    )


def parse_axos() -> Pulse:
    text = fetch_text("AX-OS", "PROJECT_STATUS.md")
    phase_match = re.search(r"Project Phase / Gate:\s*`?([^`\n]+)`?", text)
    phase = clean(phase_match.group(1), 80) if phase_match else "G3 — BUILD"

    accepted = re.findall(r"^\-\s+`?AXOS-T\d+[^\n]*\*\*ACCEPTED\*\*", text, re.MULTILINE)
    signal = f"{len(accepted)} accepted build task{'s' if len(accepted) != 1 else ''} recorded in current status."

    next_step = section_first_line(text, "Next Authorized Build Outcome")
    if not next_step:
        ready = re.search(r"`?(AXOS-T\d+)`?:\s*\*\*READY / SELECTED NEXT\*\*", text)
        next_step = f"{ready.group(1)} · READY / SELECTED NEXT" if ready else ""

    boundary = "No Security GO, Pilot, Production or Release authority is asserted."
    return Pulse(
        "AX-OS",
        "GOVERNED AI OPERATIONS",
        phase,
        signal,
        clean(next_step, 150) or "Next bounded build outcome is not asserted.",
        boundary,
        "PROJECT_STATUS.md · current build state",
    )


def parse_aic() -> Pulse:
    text = fetch_text("aether-intelligence-core-AIC-", "05_AIC_CURRENT_STATE.md")
    phase_match = re.search(r"\*\*Phase\s+([^*\n]+)\*\*", text)
    phase = f"PHASE {clean(phase_match.group(1), 72)}" if phase_match else "PHASE 0"
    gate_match = re.search(r"Implementation Gate:\s*`([^`]+)`", text)
    if gate_match:
        phase = f"{phase} · {clean(gate_match.group(1), 44)}"

    signal = "Implementation has not started under the current baseline; architecture/governance phase remains active."
    next_step = section_first_line(text, "Next Authorized Step")
    boundary = "No platform, connector, ingestion pipeline or production data collection has started."
    return Pulse(
        "AETHER INTELLIGENCE CORE · AIC",
        "FINANCIAL INTELLIGENCE INFRASTRUCTURE",
        phase,
        signal,
        clean(next_step, 150) or "Next authorized step is not asserted.",
        boundary,
        "05_AIC_CURRENT_STATE.md · CURRENT",
    )


def parse_amii() -> Pulse:
    entries = fetch_dir("amii-research-lab", "governance")
    candidates = sorted(
        [
            item["path"]
            for item in entries
            if item.get("type") == "file"
            and "ACCEPTANCE" in item.get("name", "").upper()
            and item.get("name", "").lower().endswith(".md")
        ]
    )
    if not candidates:
        raise RuntimeError("No AMII acceptance record found")
    path = candidates[-1]
    text = fetch_text("amii-research-lab", path)
    status_match = re.search(r"\*\*Status:\*\*\s*`?([^`\n]+)`?", text)
    status = clean(status_match.group(1), 80) if status_match else "CURRENT RESEARCH PHASE"
    phase = "RESEARCH · CURRENT RESEARCH PHASE" if "CURRENT RESEARCH PHASE" in status.upper() else clean(status, 90)

    signal = "Latest governed acceptance record is established for the current research phase."
    boundary = "No empirical validity, predictive performance, profitability, production readiness or Quantum integration is asserted."
    return Pulse(
        "AMII RESEARCH LAB",
        "QUANTITATIVE MARKET RESEARCH",
        phase,
        signal,
        "Continue governed research and validation within the current authorized research scope.",
        boundary,
        f"{Path(path).name} · latest acceptance record",
    )


def wrap(text: str, max_chars: int) -> list[str]:
    words = clean(text, 500).split()
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
    return lines[:2]


def svg_text_lines(x: int, y: int, lines: list[str], cls: str, gap: int = 24) -> str:
    return "\n".join(
        f'<text x="{x}" y="{y + idx * gap}" class="{cls}">{esc(line)}</text>'
        for idx, line in enumerate(lines)
    )


def render_card(p: Pulse, x: int, y: int, accent: str, pill_fill: str, pill_stroke: str) -> str:
    phase_lines = wrap(p.phase, 48)
    signal_lines = wrap(p.signal, 62)
    next_lines = wrap(p.next_step, 62)
    boundary_lines = wrap(p.boundary, 64)
    return f'''
  <g transform="translate({x} {y})">
    <rect width="700" height="300" rx="24" fill="url(#panel)" stroke="{accent}" stroke-width="1.6"/>
    <rect x="30" y="28" width="112" height="3" rx="1.5" fill="{accent}"/>
    <text x="34" y="78" class="cardTitle">{esc(p.name)}</text>
    <text x="34" y="108" class="domain">{esc(p.domain)}</text>
    <rect x="34" y="130" width="632" height="48" rx="11" fill="{pill_fill}" stroke="{pill_stroke}"/>
    {svg_text_lines(52, 160, phase_lines, 'phase', 19)}
    <text x="34" y="208" class="label">VERIFIED SIGNAL</text>
    {svg_text_lines(34, 232, signal_lines, 'body', 21)}
    <text x="360" y="208" class="label">NEXT AUTHORIZED / GOVERNED STEP</text>
    {svg_text_lines(360, 232, next_lines, 'body', 21)}
    <line x1="34" y1="270" x2="666" y2="270" stroke="#26364b"/>
    <text x="34" y="289" class="source">{esc(clean(p.source_label, 84))}</text>
    <text x="666" y="289" text-anchor="end" class="boundary">{esc(clean(p.boundary, 104))}</text>
  </g>'''


def render(pulses: list[Pulse]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    cards = [
        render_card(pulses[0], 70, 210, "#DEB459", "#2b2418", "#9D753C"),
        render_card(pulses[1], 830, 210, "#4F86C6", "#11243a", "#4F86C6"),
        render_card(pulses[2], 70, 540, "#B08A4A", "#2b2418", "#9D753C"),
        render_card(pulses[3], 830, 540, "#8B5CA8", "#25192e", "#8B5CA8"),
    ]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="930" viewBox="0 0 1600 930" role="img" aria-labelledby="title desc">
<title id="title">AETHER X Live Project Pulse</title>
<desc id="desc">Automatically refreshed, public-safe project-state telemetry derived from governed private AETHER X project status sources. No completion percentages are inferred.</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#010D1D"/><stop offset="0.55" stop-color="#071426"/><stop offset="1" stop-color="#0B1A2C"/></linearGradient>
  <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#101B2B"/><stop offset="1" stop-color="#0B1524"/></linearGradient>
  <pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse"><path d="M34 0H0V34" fill="none" stroke="#8fa0b5" stroke-opacity="0.035"/></pattern>
  <style>
    .brand{{font:700 18px Inter,Segoe UI,Arial,sans-serif;letter-spacing:4.5px;fill:#DEB459}}
    .title{{font:800 38px Inter,Segoe UI,Arial,sans-serif;fill:#F4F4F3}}
    .subtitle{{font:400 17px Inter,Segoe UI,Arial,sans-serif;fill:#AAB3BD}}
    .cardTitle{{font:800 25px Inter,Segoe UI,Arial,sans-serif;fill:#F4F4F3}}
    .domain{{font:700 13px Inter,Segoe UI,Arial,sans-serif;letter-spacing:1.05px;fill:#C9A86A}}
    .phase{{font:800 13px Inter,Segoe UI,Arial,sans-serif;letter-spacing:.45px;fill:#F2D99F}}
    .label{{font:800 10.5px Inter,Segoe UI,Arial,sans-serif;letter-spacing:1.1px;fill:#7F90A6}}
    .body{{font:500 13.5px Inter,Segoe UI,Arial,sans-serif;fill:#D5DCE5}}
    .source{{font:500 10.5px Inter,Segoe UI,Arial,sans-serif;fill:#6F7D89}}
    .boundary{{font:600 9.6px Inter,Segoe UI,Arial,sans-serif;fill:#9B8A70}}
    .footer{{font:600 12px Inter,Segoe UI,Arial,sans-serif;fill:#8E9BAD}}
    .footerGold{{font:800 12px Inter,Segoe UI,Arial,sans-serif;letter-spacing:.8px;fill:#DEB459}}
  </style>
</defs>
<rect width="1600" height="930" rx="30" fill="url(#bg)"/>
<rect width="1600" height="930" rx="30" fill="url(#grid)"/>
<rect x="24" y="24" width="1552" height="882" rx="24" fill="none" stroke="#243247" stroke-width="1.5"/>
<text x="70" y="70" class="brand">AETHER X GLOBAL</text>
<text x="70" y="122" class="title">LIVE PROJECT PULSE</text>
<text x="70" y="154" class="subtitle">Verified execution telemetry · governed sources · no inferred completion percentages</text>
<text x="1530" y="72" text-anchor="end" class="footerGold">AUTO-REFRESH · PUBLIC-SAFE</text>
<text x="1530" y="100" text-anchor="end" class="footer">Last verified refresh: {esc(now)}</text>
<line x1="70" y1="184" x2="1530" y2="184" stroke="#9D753C" stroke-opacity=".7"/>
{''.join(cards)}
<rect x="70" y="865" width="1460" height="38" rx="12" fill="#0A1422" stroke="#243247"/>
<text x="95" y="889" class="footerGold">PROGRESS SIGNAL = GOVERNED STATE CHANGE / ACCEPTED MILESTONE</text>
<text x="1505" y="889" text-anchor="end" class="footer">COMMIT ≠ PROGRESS · MERGE ≠ ACCEPTANCE · RESEARCH ≠ PRODUCTION</text>
</svg>'''


def main() -> int:
    try:
        pulses = [parse_quantum(), parse_axos(), parse_aic(), parse_amii()]
        svg = render(pulses)
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(svg, encoding="utf-8")
        print("PROJECT_PULSE_RENDER_PASS")
        for pulse in pulses:
            print(f"{pulse.name}: {pulse.phase}")
        return 0
    except Exception as exc:  # fail closed; keep prior published SVG unchanged
        print(f"PROJECT_PULSE_RENDER_FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
