#!/usr/bin/env python3
"""Apply a strict public-presentation policy to the generated Project Pulse SVG.

The renderer may inspect detailed governed status records. This final publication layer
reduces next-step wording to allowlisted, public-safe summaries before the SVG is
validated or committed.
"""

from __future__ import annotations

import re
from pathlib import Path

PATH = Path("profile/assets/aether-x-live-project-pulse.svg")


def replace_next_step(svg: str, project: str, summary: str) -> str:
    project_pattern = re.escape(project)
    block_pattern = re.compile(
        rf'(<g transform="translate\([^\"]+\)">[\s\S]*?'
        rf'<text x="34" y="76" class="cardTitle">{project_pattern}</text>'
        rf'[\s\S]*?</g>)'
    )
    match = block_pattern.search(svg)
    if not match:
        raise RuntimeError(f"Card not found for public sanitization: {project}")

    block = match.group(1)
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


def main() -> int:
    svg = PATH.read_text(encoding="utf-8")

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
    svg = replace_next_step(
        svg,
        "AMII RESEARCH LAB",
        "No separate next authorized step is asserted by the current governed record.",
    )

    PATH.write_text(svg, encoding="utf-8")
    print("PROJECT_PULSE_PUBLIC_SANITIZE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
