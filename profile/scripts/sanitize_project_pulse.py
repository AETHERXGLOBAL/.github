#!/usr/bin/env python3
"""Apply a strict public-presentation policy to the generated Portfolio Pulse SVG.

The renderer may inspect detailed governed status records for selected product/system
initiatives. This final publication layer reduces next-step wording to allowlisted,
public-safe summaries and keeps the Research unit at organizational-state level only.
"""

from __future__ import annotations

import re
from pathlib import Path

PATH = Path("profile/assets/aether-x-live-project-pulse.svg")
CARD_PATTERN = re.compile(r'<g transform="translate\([^\"]+\)">[\s\S]*?</g>')


def card_match(svg: str, project: str):
    marker = f'class="cardTitle">{project}</text>'
    return next((item for item in CARD_PATTERN.finditer(svg) if marker in item.group(0)), None)


def replace_next_step(svg: str, project: str, summary: str) -> str:
    match = card_match(svg, project)
    if not match:
        raise RuntimeError(f"Card not found for public sanitization: {project}")

    block = match.group(0)
    section_pattern = re.compile(
        r'(<text x="34" y="304" class="label">NEXT AUTHORIZED / GOVERNED STEP</text>\s*)'
        r'[\s\S]*?'
        r'(\s*<line x1="34" y1="365")'
    )
    replacement = (
        r'\1'
        + f'<text x="34" y="329" class="body">{summary}</text>'
        + r'\2'
    )
    new_block, count = section_pattern.subn(replacement, block, count=1)
    if count != 1:
        raise RuntimeError(f"Next-step section not found for public sanitization: {project}")
    return svg[: match.start()] + new_block + svg[match.end() :]


def refine_research_card(svg: str) -> str:
    project = "AETHER X RESEARCH"
    match = card_match(svg, project)
    if not match:
        raise RuntimeError("Research card not found for public identity refinement")

    block = match.group(0)
    block = block.replace(
        '<text x="34" y="106" class="domain">RESEARCH &amp; DECISION INTEGRITY</text>',
        '<text x="34" y="106" class="domain">DATA · FINANCIAL · AI RESEARCH</text>',
    )
    block = block.replace(
        '<text x="34" y="222" class="label">VERIFIED SIGNAL</text>',
        '<text x="34" y="222" class="label">ORGANIZATIONAL STATE</text>',
    )
    signal_pattern = re.compile(
        r'(<text x="34" y="222" class="label">ORGANIZATIONAL STATE</text>\s*)'
        r'[\s\S]*?'
        r'(\s*<text x="34" y="304" class="label">NEXT AUTHORIZED / GOVERNED STEP</text>)'
    )
    signal = (
        '<text x="34" y="247" class="body">Dedicated institutional research unit spanning data, financial and quantitative</text>\n'
        '<text x="34" y="269" class="body">intelligence, and artificial intelligence.</text>'
    )
    block, count = signal_pattern.subn(r'\1' + signal + r'\2', block, count=1)
    if count != 1:
        raise RuntimeError("Research organizational-state section not found")

    return svg[: match.start()] + block + svg[match.end() :]


def main() -> int:
    svg = PATH.read_text(encoding="utf-8")

    # Public naming: the surface spans system initiatives plus the institutional
    # Research unit, so Portfolio Pulse is the accurate public label.
    svg = svg.replace("AETHER X Live Project Pulse", "AETHER X Live Portfolio Pulse")
    svg = svg.replace(">LIVE PROJECT PULSE<", ">LIVE PORTFOLIO PULSE<")
    svg = svg.replace(
        "Selected live project telemetry · governed sources · bounded Research-unit disclosure",
        "Selected live portfolio telemetry · governed sources · bounded Research-unit disclosure",
    )

    # This timestamp is the time of the last state that was actually published,
    # not proof that every scheduled poll produced a new public state.
    svg = svg.replace("Last verified refresh:", "Last published state update:")

    axos = re.search(r"AXOS-T\d+", svg)
    aic = re.search(r"AIC-\d+", svg)

    svg = replace_next_step(
        svg,
        "AETHER X QUANTUM",
        "Next bounded action requires explicit authorization under the current gate.",
    )
    svg = replace_next_step(
        svg,
        "AX-OS",
        (
            f"{axos.group(0)} is selected as the next bounded build task."
            if axos
            else "The next bounded build task is selected in the current governed status."
        ),
    )
    svg = replace_next_step(
        svg,
        "AETHER INTELLIGENCE CORE · AIC",
        (
            f"{aic.group(0)} is the next authorized pre-implementation step."
            if aic
            else "The next authorized pre-implementation step is recorded in the current state."
        ),
    )
    svg = refine_research_card(svg)
    svg = replace_next_step(
        svg,
        "AETHER X RESEARCH",
        "Individual research remains private and governed by evidence, validation, IP and publication controls.",
    )

    PATH.write_text(svg, encoding="utf-8")
    print("PORTFOLIO_PULSE_PUBLIC_SANITIZE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
