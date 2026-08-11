#!/usr/bin/env python3
import html
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import Request, urlopen

ORG = "AETHERXGLOBAL"
OUTPUT = Path("profile/assets/aether-x-engineering-pulse.svg")
API = f"https://api.github.com/orgs/{ORG}/repos?type=public&per_page=100&sort=updated"


def fetch_public_repos():
    req = Request(
        API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "AETHER-X-Public-Engineering-Pulse",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urlopen(req, timeout=20) as response:
        return json.load(response)


def esc(value):
    return html.escape(str(value), quote=True)


def render(repos):
    now = datetime.now(timezone.utc)
    public_count = len(repos)
    total_stars = sum(int(r.get("stargazers_count") or 0) for r in repos)
    total_forks = sum(int(r.get("forks_count") or 0) for r in repos)

    active_90 = 0
    latest = None
    for repo in repos:
        pushed = repo.get("pushed_at")
        if not pushed:
            continue
        dt = datetime.fromisoformat(pushed.replace("Z", "+00:00"))
        latest = dt if latest is None or dt > latest else latest
        if dt >= now - timedelta(days=90):
            active_90 += 1

    representative = public_count >= 3
    if representative:
        mode = "REPRESENTATIVE PUBLIC METRICS"
        c1_title, c1_value, c1_note = "PUBLIC REPOSITORIES", public_count, "Approved public engineering surfaces"
        c2_title, c2_value, c2_note = "PUBLIC STARS", total_stars, "Aggregate public GitHub stars"
        c3_title, c3_value, c3_note = "ACTIVE / 90 DAYS", active_90, "Public repositories with recent pushes"
        c4_title, c4_value, c4_note = "PUBLIC FORKS", total_forks, "Aggregate public forks"
    else:
        mode = "CURATED PUBLIC SURFACE"
        c1_title, c1_value, c1_note = "PUBLIC ENGINEERING", "CURATED", "Only approved public surfaces are exposed"
        c2_title, c2_value, c2_note = "TELEMETRY", "PUBLIC-ONLY", "No private repository metadata is queried"
        c3_title, c3_value, c3_note = "DISCLOSURE", "CONTROLLED", "Metrics publish only when representative"
        c4_title, c4_value, c4_note = "NUMERIC MODE", "ARMED", "Activates automatically at 3+ public repos"

    latest_label = latest.strftime("%Y-%m-%d") if latest else "NO PUBLIC PUSH"

    cards = [
        (80, c1_title, c1_value, c1_note, "#22D3EE"),
        (455, c2_title, c2_value, c2_note, "#60A5FA"),
        (830, c3_title, c3_value, c3_note, "#A78BFA"),
        (1205, c4_title, c4_value, c4_note, "#D6A84B"),
    ]

    card_svg = []
    for x, title, value, note, accent in cards:
        size = 31 if isinstance(value, int) else 24
        card_svg.append(f'''\n  <g transform="translate({x} 210)">\n    <rect width="315" height="190" rx="22" fill="#111827" stroke="#273244" stroke-width="2"/>\n    <rect width="6" height="190" rx="3" fill="{accent}"/>\n    <text x="28" y="42" fill="#94A3B8" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="15" font-weight="700" letter-spacing="1.2">{esc(title)}</text>\n    <text x="28" y="94" fill="#F8FAFC" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="800">{esc(value)}</text>\n    <text x="28" y="134" fill="#CBD5E1" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="15">{esc(note)}</text>\n  </g>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="500" viewBox="0 0 1600 500" role="img" aria-labelledby="title desc">
  <title id="title">AETHER X Engineering Pulse</title>
  <desc id="desc">A public-safe engineering telemetry panel generated only from publicly visible GitHub organization data.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0B1018"/><stop offset="1" stop-color="#111827"/></linearGradient>
    <linearGradient id="bar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22D3EE"/><stop offset="0.55" stop-color="#8B5CF6"/><stop offset="1" stop-color="#D6A84B"/></linearGradient>
  </defs>
  <rect width="1600" height="500" rx="32" fill="url(#bg)"/>
  <rect x="24" y="24" width="1552" height="452" rx="26" fill="none" stroke="#273244" stroke-width="2"/>
  <rect x="80" y="62" width="140" height="5" rx="2.5" fill="url(#bar)"/>
  <text x="80" y="112" fill="#F8FAFC" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="36" font-weight="800">LIVE ENGINEERING PULSE</text>
  <text x="80" y="149" fill="#94A3B8" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="19">GitHub-native public telemetry • disclosure-safe by design • private engineering remains private.</text>
  <text x="1520" y="93" text-anchor="end" fill="#D6A84B" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="16" font-weight="700">{esc(mode)}</text>
  <text x="1520" y="122" text-anchor="end" fill="#64748B" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="14">Latest public push: {esc(latest_label)}</text>
  {''.join(card_svg)}
  <text x="80" y="449" fill="#64748B" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="15">Metrics are generated from GitHub public organization data only. Private repositories, private activity and confidential engineering metadata are never queried or published.</text>
</svg>
'''


def main():
    repos = fetch_public_repos()
    svg = render(repos)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    previous = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else None
    if previous == svg:
        print("Engineering Pulse unchanged")
        return 0
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"Engineering Pulse updated from {len(repos)} public repositories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
