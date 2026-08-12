#!/usr/bin/env python3
import html
import json
import math
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ORG = "AETHERXGLOBAL"
OUTPUT = Path("profile/assets/aether-x-engineering-pulse.svg")
API_ROOT = "https://api.github.com"
USER_AGENT = "AETHER-X-Public-GitHub-Activity"
TIMEOUT = 25


def esc(value):
    return html.escape(str(value), quote=True)


def request_json(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, headers=headers)
    with urlopen(req, timeout=TIMEOUT) as response:
        return json.load(response)


def paginate(url):
    page = 1
    items = []
    sep = "&" if "?" in url else "?"
    while True:
        batch = request_json(f"{url}{sep}per_page=100&page={page}")
        if not isinstance(batch, list):
            raise RuntimeError(f"Expected list response from {url}")
        items.extend(batch)
        if len(batch) < 100:
            break
        page += 1
        if page > 50:
            raise RuntimeError(f"Pagination safety limit exceeded for {url}")
    return items


def fetch_public_repos():
    repos = paginate(f"{API_ROOT}/orgs/{ORG}/repos?type=public&sort=updated")
    return [repo for repo in repos if repo.get("visibility") == "public"]


def fetch_repo_pulls(repo_name):
    return paginate(f"{API_ROOT}/repos/{ORG}/{repo_name}/pulls?state=all&sort=created&direction=asc")


def classify_pulls(repos):
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=90)
    rows = []
    latest_activity = None

    for repo in repos:
        name = repo["name"]
        pulls = fetch_repo_pulls(name)
        open_count = 0
        merged_count = 0
        closed_count = 0
        recent_90 = 0

        for pr in pulls:
            if pr.get("state") == "open":
                open_count += 1
            elif pr.get("merged_at"):
                merged_count += 1
            else:
                closed_count += 1

            updated_at = pr.get("updated_at")
            if updated_at:
                updated = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
                if latest_activity is None or updated > latest_activity:
                    latest_activity = updated
                if updated >= cutoff:
                    recent_90 += 1

        rows.append(
            {
                "name": name,
                "open": open_count,
                "merged": merged_count,
                "closed": closed_count,
                "total": len(pulls),
                "recent_90": recent_90,
            }
        )

    return rows, latest_activity


def kpi_card(x, title, value, note, accent):
    return f'''
  <g transform="translate({x} 178)">
    <rect width="330" height="142" rx="20" fill="#0F1726" stroke="#243247" stroke-width="1.5"/>
    <rect width="5" height="142" rx="2.5" fill="{accent}"/>
    <text x="27" y="35" fill="#8E9BAD" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="14" font-weight="700" letter-spacing="1.1">{esc(title)}</text>
    <text x="27" y="85" fill="#F4F4F3" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="34" font-weight="800">{esc(value)}</text>
    <text x="27" y="116" fill="#AAB3BD" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="14">{esc(note)}</text>
  </g>'''


def render(rows, latest_activity):
    rows = sorted(rows, key=lambda item: (-item["total"], item["name"].lower()))
    display_rows = [row for row in rows if row["total"] > 0][:6]
    total_prs = sum(row["total"] for row in rows)
    total_open = sum(row["open"] for row in rows)
    total_merged = sum(row["merged"] for row in rows)
    total_closed = sum(row["closed"] for row in rows)
    recent_90 = sum(row["recent_90"] for row in rows)
    repos_with_prs = sum(1 for row in rows if row["total"] > 0)
    public_repos = len(rows)

    merge_rate = (100.0 * total_merged / total_prs) if total_prs else 0.0
    top_repo = display_rows[0]["name"] if display_rows else "NO PUBLIC PR ACTIVITY"
    top_repo_total = display_rows[0]["total"] if display_rows else 0

    updated = latest_activity or datetime.now(timezone.utc)
    updated_label = updated.strftime("%Y-%m-%d %H:%M UTC")

    cards = [
        kpi_card(80, "PUBLIC PULL REQUESTS", total_prs, "All-time public PR records", "#DEB459"),
        kpi_card(430, "MERGED", total_merged, f"{merge_rate:.1f}% of public PRs", "#8B5CF6"),
        kpi_card(780, "OPEN", total_open, "Currently open public PRs", "#2EA043"),
        kpi_card(1130, "PUBLIC REPOS", public_repos, f"{repos_with_prs} with PR activity", "#3E8BFF"),
    ]

    chart = []
    chart.append('''
  <g transform="translate(80 350)">
    <rect width="1000" height="410" rx="22" fill="#0D1522" stroke="#243247" stroke-width="1.5"/>
    <text x="28" y="42" fill="#F4F4F3" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="24" font-weight="800">Pull Requests by Repository</text>
    <text x="28" y="69" fill="#8E9BAD" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="14">Public repositories only • all-time status distribution</text>
    <circle cx="590" cy="39" r="5" fill="#2EA043"/><text x="604" y="44" fill="#AAB3BD" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="13">Open</text>
    <circle cx="672" cy="39" r="5" fill="#8B5CF6"/><text x="686" y="44" fill="#AAB3BD" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="13">Merged</text>
    <circle cx="770" cy="39" r="5" fill="#F85149"/><text x="784" y="44" fill="#AAB3BD" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="13">Closed</text>
  </g>''')

    if not display_rows:
        chart.append('''
  <text x="580" y="560" text-anchor="middle" fill="#64748B" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="18">No public pull-request activity is available.</text>''')
    else:
        max_total = max(row["total"] for row in display_rows) or 1
        bar_x = 390
        bar_max = 620
        start_y = 455
        row_gap = 49
        for idx, row in enumerate(display_rows):
            y = start_y + idx * row_gap
            safe_name = row["name"] if len(row["name"]) <= 29 else row["name"][:27] + "…"
            total_width = bar_max * row["total"] / max_total
            open_w = total_width * row["open"] / row["total"] if row["total"] else 0
            merged_w = total_width * row["merged"] / row["total"] if row["total"] else 0
            closed_w = total_width * row["closed"] / row["total"] if row["total"] else 0
            chart.append(f'''
  <text x="108" y="{y+17}" fill="#CBD5E1" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="14">{esc(safe_name)}</text>
  <rect x="{bar_x}" y="{y}" width="{bar_max}" height="26" rx="7" fill="#111C2C"/>
  <rect x="{bar_x}" y="{y}" width="{open_w:.2f}" height="26" rx="7" fill="#2EA043"/>
  <rect x="{bar_x+open_w:.2f}" y="{y}" width="{merged_w:.2f}" height="26" fill="#8B5CF6"/>
  <rect x="{bar_x+open_w+merged_w:.2f}" y="{y}" width="{closed_w:.2f}" height="26" rx="7" fill="#F85149"/>
  <text x="1032" y="{y+18}" text-anchor="end" fill="#F4F4F3" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="14" font-weight="700">{row["total"]}</text>''')

    radius = 68
    circumference = 2 * math.pi * radius
    segments = [
        ("open", total_open, "#2EA043"),
        ("merged", total_merged, "#8B5CF6"),
        ("closed", total_closed, "#F85149"),
    ]
    donut = []
    offset = 0.0
    for _, value, color in segments:
        if total_prs <= 0 or value <= 0:
            continue
        length = circumference * value / total_prs
        donut.append(
            f'<circle cx="1270" cy="493" r="{radius}" fill="none" stroke="{color}" '
            f'stroke-width="24" stroke-dasharray="{length:.2f} {circumference-length:.2f}" '
            f'stroke-dashoffset="{-offset:.2f}" transform="rotate(-90 1270 493)"/>'
        )
        offset += length

    side = f'''
  <g transform="translate(1100 350)">
    <rect width="420" height="410" rx="22" fill="#0D1522" stroke="#243247" stroke-width="1.5"/>
    <text x="28" y="42" fill="#F4F4F3" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="24" font-weight="800">Activity Insights</text>
    <text x="28" y="69" fill="#8E9BAD" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="14">Live public GitHub telemetry</text>
  </g>
  <circle cx="1270" cy="493" r="{radius}" fill="none" stroke="#162235" stroke-width="24"/>
  {''.join(donut)}
  <text x="1270" y="489" text-anchor="middle" fill="#F4F4F3" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="30" font-weight="800">{total_prs}</text>
  <text x="1270" y="514" text-anchor="middle" fill="#8E9BAD" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="13">PUBLIC PRs</text>

  <text x="1392" y="445" fill="#8E9BAD" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="12" font-weight="700">MERGE RATE</text>
  <text x="1392" y="474" fill="#F4F4F3" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="24" font-weight="800">{merge_rate:.1f}%</text>

  <text x="1130" y="602" fill="#8E9BAD" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="12" font-weight="700">RECENT ACTIVITY / 90D</text>
  <text x="1130" y="632" fill="#3E8BFF" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="24" font-weight="800">{recent_90} PRs</text>

  <text x="1130" y="682" fill="#8E9BAD" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="12" font-weight="700">TOP PUBLIC REPOSITORY</text>
  <text x="1130" y="710" fill="#F4F4F3" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="16" font-weight="700">{esc(top_repo)}</text>
  <text x="1130" y="735" fill="#DEB459" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="14">{top_repo_total} public PRs</text>
'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="840" viewBox="0 0 1600 840" role="img" aria-labelledby="title desc">
  <title id="title">AETHER X Live GitHub Activity</title>
  <desc id="desc">Professional public-only GitHub pull-request activity dashboard for AETHER X GLOBAL.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#010D1D"/>
      <stop offset="0.58" stop-color="#071426"/>
      <stop offset="1" stop-color="#0B1A2C"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#DEB459"/>
      <stop offset="0.50" stop-color="#8B5CF6"/>
      <stop offset="1" stop-color="#3E8BFF"/>
    </linearGradient>
  </defs>

  <rect width="1600" height="840" rx="30" fill="url(#bg)"/>
  <rect x="24" y="24" width="1552" height="792" rx="24" fill="none" stroke="#243247" stroke-width="1.5"/>
  <rect x="80" y="58" width="150" height="5" rx="2.5" fill="url(#accent)"/>

  <text x="80" y="108" fill="#F4F4F3" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="34" font-weight="800">AETHER X • LIVE GITHUB ACTIVITY</text>
  <text x="80" y="140" fill="#AAB3BD" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="17">Professional pull-request telemetry generated directly from public GitHub organization data.</text>
  <text x="1520" y="92" text-anchor="end" fill="#DEB459" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="14" font-weight="800">PUBLIC-ONLY • AUTO-REFRESH</text>
  <text x="1520" y="120" text-anchor="end" fill="#6F7D89" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="13">Latest PR activity: {esc(updated_label)}</text>

  {''.join(cards)}
  {''.join(chart)}
  {side}

  <line x1="80" y1="790" x2="1520" y2="790" stroke="#243247" stroke-width="1"/>
  <text x="80" y="817" fill="#6F7D89" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="13">Disclosure boundary: only public repositories and public pull-request metadata are queried. Private repository names, private activity and confidential engineering metadata are excluded.</text>
</svg>
'''


def main():
    repos = fetch_public_repos()
    rows, latest_activity = classify_pulls(repos)
    svg = render(rows, latest_activity)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    previous = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else None
    if previous == svg:
        print("Public GitHub activity dashboard unchanged")
        return 0
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"Updated public GitHub activity dashboard from {len(repos)} public repositories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
