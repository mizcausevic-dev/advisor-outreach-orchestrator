from __future__ import annotations

import html
from pathlib import Path

from app.services.outreach_service import build_service

service = build_service()


def page_shell(title: str, eyebrow: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #09111d;
      --panel: #101d2f;
      --panel-2: #17263c;
      --line: #29486f;
      --ink: #f3ecde;
      --muted: #b5c2d7;
      --blue: #6db2ff;
      --pink: #f0bfd7;
      --green: #8fe0bf;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        radial-gradient(circle at top left, rgba(54, 103, 164, 0.18), transparent 30%),
        linear-gradient(180deg, #08111c 0%, #0b1522 100%);
      color: var(--ink);
      font-family: Georgia, "Times New Roman", serif;
    }}
    .frame {{
      width: 1440px;
      min-height: 920px;
      margin: 0 auto;
      padding: 48px;
    }}
    .shell {{
      background: rgba(13, 24, 39, 0.94);
      border: 1px solid var(--line);
      border-radius: 36px;
      padding: 34px 36px 36px;
    }}
    .eyebrow {{
      margin: 0 0 22px;
      font: 700 13px/1.2 "Segoe UI", sans-serif;
      letter-spacing: 0.35em;
      text-transform: uppercase;
      color: var(--blue);
    }}
    h1 {{
      margin: 0;
      font-size: 72px;
      line-height: 1.02;
      max-width: 1160px;
      letter-spacing: -0.05em;
    }}
    p.lead {{
      margin: 24px 0 0;
      max-width: 1060px;
      color: var(--muted);
      font: 400 19px/1.55 "Segoe UI", sans-serif;
    }}
    .pills {{
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
      margin: 22px 0 26px;
    }}
    .pill {{
      background: #1d2d45;
      border: 1px solid #335a8d;
      color: #f5f7fb;
      padding: 10px 16px;
      border-radius: 999px;
      font: 700 15px/1 "Segoe UI", sans-serif;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      margin: 8px 0 34px;
    }}
    .card {{
      background: var(--panel-2);
      border: 1px solid #335885;
      border-radius: 24px;
      padding: 22px 22px 18px;
      min-height: 170px;
    }}
    .card h2 {{
      margin: 0 0 12px;
      color: #a8cbff;
      font: 700 12px/1.2 "Segoe UI", sans-serif;
      letter-spacing: 0.24em;
      text-transform: uppercase;
    }}
    .metric {{
      font-size: 58px;
      line-height: 1;
      margin: 0 0 10px;
    }}
    .card p, .card li, .table, .lane {{
      color: var(--muted);
      font: 400 18px/1.45 "Segoe UI", sans-serif;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1.2fr 0.9fr;
      gap: 18px;
    }}
    .table {{
      display: grid;
      gap: 12px;
    }}
    .row {{
      display: grid;
      grid-template-columns: 1.2fr 0.7fr 0.8fr 0.7fr;
      gap: 14px;
      align-items: center;
      padding: 16px 18px;
      background: #0c1728;
      border: 1px solid #223c5d;
      border-radius: 18px;
    }}
    .row strong {{
      color: var(--ink);
      display: block;
      font: 700 24px/1.1 Georgia, serif;
    }}
    .small {{
      font-size: 15px;
      color: #87a2c7;
    }}
    .lane {{
      padding: 16px 18px;
      background: #0c1728;
      border: 1px solid #223c5d;
      border-radius: 18px;
      margin-bottom: 12px;
    }}
    .lane strong {{
      display: block;
      color: var(--ink);
      font: 700 24px/1.15 Georgia, serif;
      margin-bottom: 6px;
    }}
    ol {{
      margin: 0;
      padding-left: 22px;
    }}
    li + li {{
      margin-top: 10px;
    }}
  </style>
</head>
<body>
  <div class="frame">
    <div class="shell">
      <p class="eyebrow">{html.escape(eyebrow)}</p>
      {body}
    </div>
  </div>
</body>
</html>"""


def render_overview() -> str:
    summary = service.summary()
    queue = service.outreach_queue()[:3]
    queue_rows = "".join(
        f"""
        <div class="row">
          <div>
            <strong>{html.escape(student['name'])}</strong>
            <div class="small">{html.escape(student['program'])} · {html.escape(student['cohort'])}</div>
          </div>
          <div>{student['urgencyScore']}</div>
          <div>{html.escape(student['ownerLane'])}</div>
          <div>{html.escape(student['leadChannel'])}</div>
        </div>
        """
        for student in queue
    )
    body = f"""
      <h1>Turn student risk signals into a contact plan the institution can actually run.</h1>
      <p class="lead">
        Advisor Outreach Orchestrator sequences intervention queues across advising, faculty, care teams,
        and financial support so urgent cases stop waiting inside one generic retention dashboard.
      </p>
      <div class="pills">
        <div class="pill">channel-aware sequencing</div>
        <div class="pill">advisor + faculty lane routing</div>
        <div class="pill">same-week escalation planning</div>
        <div class="pill">proof-ready intervention queue</div>
      </div>
      <div class="stats">
        <div class="card"><h2>students queued</h2><div class="metric">{summary['studentCount']}</div><p>Active cases loaded into one intervention surface.</p></div>
        <div class="card"><h2>escalations</h2><div class="metric">{summary['escalationCount']}</div><p>Cases that need same-week action and deeper owner lanes.</p></div>
        <div class="card"><h2>priority follow-up</h2><div class="metric">{summary['priorityCount']}</div><p>Students who should get outreach before another signal slips.</p></div>
        <div class="card"><h2>avg. urgency</h2><div class="metric">{summary['averageUrgencyScore']}</div><p>{html.escape(summary['leadRecommendation'])}</p></div>
      </div>
      <div class="grid-2">
        <div class="card">
          <h2>intervention queue</h2>
          <div class="table">{queue_rows}</div>
        </div>
        <div class="card">
          <h2>lead recommendation</h2>
          <p>{html.escape(summary['leadRecommendation'])}</p>
          <p class="lead" style="margin-top:16px;font-size:17px;">Top owner lane: {html.escape(summary['topLane'])}</p>
        </div>
      </div>
    """
    return page_shell("Advisor Outreach Orchestrator", "Advisor Outreach Orchestrator", body)


def render_queue() -> str:
    queue = service.outreach_queue()
    rows = "".join(
        f"""
        <div class="row">
          <div>
            <strong>{html.escape(student['name'])}</strong>
            <div class="small">{html.escape(student['program'])}</div>
          </div>
          <div>{student['urgencyScore']}</div>
          <div>{html.escape(student['status'])}</div>
          <div>{html.escape(student['leadChannel'])}</div>
        </div>
        """
        for student in queue
    )
    body = f"""
      <h1>Queue the right outreach lane before another week of silence compounds the problem.</h1>
      <p class="lead">
        The queue combines response lag, academic drift, financial holds, and faculty concern so
        cases enter advising, care-team, or finance lanes with a clear channel strategy.
      </p>
      <div class="card">
        <h2>priority stack</h2>
        <div class="table">{rows}</div>
      </div>
    """
    return page_shell("Advisor Outreach Queue", "Intervention Queue", body)


def render_playbooks() -> str:
    playbooks = service.playbooks()[:3]
    lanes = service.lane_breakdown()
    playbook_cards = "".join(
        f"""
        <div class="lane">
          <strong>{html.escape(item['name'])} · {html.escape(item['ownerLane'])}</strong>
          <div class="small">{html.escape(item['status'])} via {html.escape(item['leadChannel'])}</div>
          <ol>{"".join(f"<li>{html.escape(step)}</li>" for step in item['steps'])}</ol>
        </div>
        """
        for item in playbooks
    )
    lane_cards = "".join(
        f'<div class="lane"><strong>{html.escape(lane["ownerLane"])}</strong><div>{lane["count"]} active cases</div></div>'
        for lane in lanes
    )
    body = f"""
      <h1>Every outreach case gets a next-best-action sequence instead of a vague “follow up soon.”</h1>
      <p class="lead">
        Playbooks combine status, channel fit, and owner lanes so advisors know when to text, call,
        escalate, or pull faculty and finance into the case.
      </p>
      <div class="grid-2">
        <div class="card"><h2>playbooks</h2>{playbook_cards}</div>
        <div class="card"><h2>owner lane load</h2>{lane_cards}</div>
      </div>
    """
    return page_shell("Advisor Outreach Playbooks", "Playbook Lanes", body)


def render_api_summary() -> str:
    payload = service.sample_payload()
    body = f"""
      <h1>The API exposes intervention logic in a shape that advising ops teams can actually use.</h1>
      <p class="lead">
        Summary metrics, queue state, and next-step recommendations are all surfaced together so the
        outreach engine can feed dashboards, CRMs, and advisor work queues.
      </p>
      <div class="card">
        <h2>sample payload</h2>
        <pre style="margin:0;color:#d7e8ff;font:16px/1.5 Consolas, monospace; white-space:pre-wrap;">{html.escape(str(payload))}</pre>
      </div>
    """
    return page_shell("Advisor Outreach API Summary", "API Summary", body)


def write_static_proof_pages(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = {
        "01-overview.html": render_overview(),
        "02-queue.html": render_queue(),
        "03-playbooks.html": render_playbooks(),
        "04-api-summary.html": render_api_summary(),
    }
    written: list[Path] = []
    for name, contents in pages.items():
        path = output_dir / name
        path.write_text(contents, encoding="utf-8")
        written.append(path)
    return written
