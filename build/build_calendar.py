import base64, html, datetime, json
from urllib.parse import quote

import os
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = f"{S}/thumbs"
OUT = f"{S}/index.html"
WA = "https://wa.me/917981827087?text="
# Web app URL from build/apps-script.gs. Empty means the shoot buttons stay hidden.
SHEETS_URL = "https://script.google.com/macros/s/AKfycbzjlY2giIQU7cHWO7zZzc6FTaKkujpWM4e24aApAQ-FFMhajAqkR6MGrqbxO7pvGhoT/exec"
SHOOTS = [
    dict(id="s-hitech", day=9, place="Hi-Tech City"),
    dict(id="s-kukatpally", day=12, place="Kukatpally"),
]

def img(n):
    return "data:image/jpeg;base64," + base64.b64encode(open(f"{T}/{n}.jpg", "rb").read()).decode()

def reel(d): return dict(t="reel", s=[f"previews/d{d:02d}.mp4"])
def slides(d): return dict(t="slides", s=[f"previews/d{d:02d}-{n}.mp4" for n in range(1, 9)])

P = {
    6:  dict(k="posted", img="stroke", title="After a stroke, rehab is the way back", meta="Reel · 0:30 · posted Oct 6",
             idea="Bed, sit, stand, balance, walk. Rehabilitation is the path to independence.", pv=reel(6)),
    11: dict(k="reel", img="branches", title="Our launch journey", meta="Reel · 1:22",
             idea="A look back at three launches, from Banjara Hills to LB Nagar, ending on what is coming next. Leads into the Banjara Hills opening.", pv=reel(7)),
    8:  dict(k="car", img="c-robotic", title="Robotic gait, quick guide", meta="Carousel · 8 slides",
             idea="What each part of the robotic gait system does, in plain words.", pv=slides(8)),
    13: dict(k="ai", img="ai-banjara", title="Banjara Hills, AI influencer reel", meta="Reel · AI influencer · to be made",
             idea="An AI influencer introduces the new Banjara Hills Rehab centre, coming this month."),
    31: dict(k="reel", img="emotional", title="Emotional reel", meta="Reel · 0:40",
             idea="Therapists and patients mid-session. A warm post to close the month.", pv=reel(10)),
    14: dict(k="reel", img="levels", title="6 levels of stroke rehab", meta="Reel · 1:03",
             idea="Rehab is not one exercise. Six levels, from assessment to the home programme.", pv=reel(13)),
    15: dict(k="car", img="c-kids", title="Kids rehab, quick guide", meta="Carousel · 8 slides",
             idea="For parents: how rehab works for little ones.", pv=slides(15)),
    16: dict(k="open", title="Testimonial", meta="Open slot · footage needed",
             idea="A stroke patient's family. Sits right after Wednesday's six-levels explainer."),
    17: dict(k="reel", img="comedy", title="30 Din skit", meta="Reel · 0:51",
             idea="The 30-day patient journey, starting from the Day 1 consultation. A lighter post to end the week.", pv=reel(17)),
    9:  dict(k="ai", img="ai-fd", title="Financial District, AI influencer reel", meta="Reel · AI influencer · 0:35",
             idea="An AI influencer introduces the Financial District branch, now open.", pv=reel(9)),
    20: dict(k="open", title="Open slot", meta="Open slot · footage needed",
             idea="Held for a testimonial or patient video."),
    22: dict(k="car", img="c-gait", title="Gait suspension, quick guide", meta="Carousel · 8 slides",
             idea="How supported walking builds confidence. Pairs with the stroke reel posted on Oct 6.", pv=slides(22)),
    23: dict(k="open", title="Patient video", meta="Open slot · footage needed",
             idea="A standing or walking milestone, right after Thursday's gait suspension carousel."),
    24: dict(k="reel", img="somali", title="A mother's words, from Somalia", meta="Reel · 0:40",
             idea="An international patient story: a mother on her daughter's therapy at Wellknox.", pv=reel(24)),
    27: dict(k="open", title="Open slot", meta="Open slot · footage needed",
             idea="Held for a testimonial or patient video."),
    29: dict(k="car", img="c-aqua", title="Aqua therapy, quick guide", meta="Carousel · 8 slides",
             idea="Let the water carry you: why water exercise is gentler on sore joints.", pv=slides(29)),
    30: dict(k="open", title="Testimonial", meta="Open slot · footage needed",
             idea="A parent from kids rehab, or an aqua therapy patient. Closes the month on a patient voice."),
}
KIND = {"car": "Carousel", "reel": "Reel", "open": "Open slot", "posted": "Posted", "ai": "AI reel"}
NOUN = {"car": "Carousel", "reel": "Reel", "open": "Slot", "posted": "Reel", "ai": "AI reel"}

KEYS = {6: "stroke", 8: "robotic", 9: "ai-fd", 11: "launch", 13: "ai-bh", 14: "levels", 15: "kids", 16: "slot-16",
        17: "30din", 20: "slot-20", 22: "gait", 23: "slot-23", 24: "somali", 27: "slot-27", 29: "aqua", 30: "slot-30", 31: "emotional"}
for _d, _p in P.items():
    _p["key"] = KEYS[_d]

WEEKS = [
    ("Week 1", "Oct 7 to 11", "Trust and technology", "Show the robotic gait technology, introduce the Financial District branch, then look back at how far Wellknox has come."),
    ("Week 2", "Oct 12 to 18", "Understand rehab", "Introduce the new Banjara Hills centre, explain how stroke and kids rehab work, and add a first patient voice on Friday."),
    ("Week 3", "Oct 19 to 25", "Recovery you can see", "A supported-walking guide, a patient video, and an international patient story."),
    ("Week 4", "Oct 26 to 31", "Water therapy", "An aqua therapy guide, a last testimonial, and the emotional reel to close the month."),
]
WK_DAYS = [(7, 11), (12, 18), (19, 25), (26, 31)]
DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
def dow(d): return DOW[datetime.date(2026, 10, d).weekday()]
def label(d, p): return f"{dow(d)} {d} Oct · {NOUN[p['k']]}: {p['title']}"

def wa(text): return WA + quote(text, safe="")
def approve_link(d, p): return wa(f"✅ Approved\n{label(d, p)}")
def change_link(d, p): return wa(f"✏️ Changes needed\n{label(d, p)}\nWhat to change: ")

PLAY = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>'
TICK = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PEN = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M4 20l4.2-1 10-10a2 2 0 0 0-2.8-2.8l-10 10L4 20z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/></svg>'

UP = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M12 16V5m0 0L7.5 9.5M12 5l4.5 4.5M5 19h14" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def thumb(p, cls="th"):
    if p["k"] == "open":
        return f'<div class="{cls} ph open" aria-hidden="true"><span>+</span></div>'
    if p["k"] == "ai" and "img" not in p:
        return f'<div class="{cls} ph ai" aria-hidden="true"><span>AI</span></div>'
    return f'<img class="{cls} {p["k"]}" src="{img(p["img"])}" alt="" loading="lazy">'

# ---- month grid
cells = []
for _ in range(datetime.date(2026, 10, 1).weekday()):
    cells.append('<div class="cell blank"></div>')
for d in range(1, 32):
    p = P.get(d)
    past = d <= 5
    cls = "cell" + (" past" if past else "") + (" has " + p["k"] if p else "")
    inner = f'<div class="dn">{d}</div>'
    if p:
        pk = "" if p["k"] == "posted" else f' data-pkey="{p["key"]}" data-status="pending"'
        pill = "" if p["k"] == "posted" else '<span class="gst" data-pill></span>'
        inner += (f'<a class="chip {p["k"]}" href="#d{d}"{pk}>{thumb(p, "gth")}'
                  f'<span class="ct"><span class="badge {p["k"]}">{KIND[p["k"]]}</span>'
                  f'<span class="gt">{html.escape(p["title"])}</span>{pill}</span></a>')
    for sh in SHOOTS:
        if sh["day"] == d:
            inner += (f'<a class="gshoot" data-sid="{sh["id"]}" href="#shoots"><i class="pip"></i>'
                      f'<span class="gs-n">Shoot · {sh["place"]}</span><span class="gs-t">Planned</span></a>')
    cells.append(f'<div class="{cls}" data-day="{d}">{inner}</div>')
while len(cells) % 7: cells.append('<div class="cell blank"></div>')
grid = "".join(cells)
dow_head = "".join(f"<div>{d}</div>" for d in DOW)

# ---- row builder
def row(d, p):
    acts = []
    if p.get("pv"):
        acts.append(f'<button class="btn pv" type="button" data-day="{d}">{PLAY}Preview</button>')
    live = p["k"] != "posted"
    if live:
        acts.append(f'<a class="btn ok" data-act="approved" href="{approve_link(d, p)}" target="_blank" rel="noopener">{TICK}<span class="lb">Approve</span></a>')
        acts.append(f'<a class="btn ch" data-act="changes" href="{change_link(d, p)}" target="_blank" rel="noopener">{PEN}<span class="lb">Make changes</span></a>')
        acts.append(f'<button class="btn up" type="button" data-act="uploaded">{UP}<span class="lb">Mark uploaded</span></button>')
        acts.append('<button class="lnk" type="button" data-act="pending" hidden>Reset</button>')
    if p["k"] == "open":
        acts.insert(0, '<span class="nopv">Preview opens once footage is in</span>')
    if p["k"] == "ai" and not p.get("pv"):
        acts.insert(0, '<span class="nopv">Preview opens once the reel is made</span>')
    pk = f' data-pkey="{p["key"]}" data-status="pending"' if live else ""
    pill = '<span class="spill" data-pill data-s="pending">Awaiting approval</span>' if live else ""
    return (f'<article class="row {p["k"]}" id="d{d}"{pk}>'
            f'<div class="when"><b>{d}</b><span>{dow(d)}</span></div>{thumb(p)}'
            f'<div class="body"><div class="top"><span class="badge {p["k"]}">{KIND[p["k"]]}</span>{pill}<span class="meta">{html.escape(p["meta"])}</span></div>'
            f'<h4>{html.escape(p["title"])}</h4><p>{html.escape(p["idea"])}</p>'
            f'<div class="acts">{"".join(acts)}</div></div></article>')

agenda = [
    '<section class="week"><header><div><span class="wn">Already posted</span><span class="wr">Oct 6</span></div>'
    '<h3>Out today</h3><p>Posted before the plan starts, so it is not scheduled again.</p></header>' + row(6, P[6]) + '</section>'
]
for (wn, wr, wt, wd), (a, b) in zip(WEEKS, WK_DAYS):
    rows = "".join(row(d, P[d]) for d in range(a, b + 1) if d in P)
    agenda.append(f'<section class="week"><header><div><span class="wn">{wn}</span><span class="wr">{wr}</span></div>'
                  f'<h3>{html.escape(wt)}</h3><p>{html.escape(wd)}</p></header>{rows}</section>')

cnt = lambda k: sum(1 for d, p in P.items() if p["k"] == k)
n_car, n_reel, n_open, n_ai = cnt("car"), cnt("reel"), cnt("open"), cnt("ai")
all_ok = wa("✅ Approved: the full October 2026 calendar for Wellknox.")
all_ch = wa("✏️ Changes needed on the October 2026 calendar.\nWhat to change: ")
launch = wa("📅 Launch date for the Banjara Hills Rehab branch:\n")

EXTRA_CSS = open(f"{S}/build/extra.css").read()
LIVE_JS = open(f"{S}/build/live.js").read().replace("__URL__", json.dumps(SHEETS_URL))

shoot_cards = "".join(
    f'<div class="shoot" data-sid="{sh["id"]}" data-date="2026-10-{sh["day"]:02d}"><div class="sd"><b>{sh["day"]}</b><span>{dow(sh["day"])}</span></div>'
    f'<div class="sb"><h4>{sh["place"]}</h4><p class="ss" data-sstat>Planned</p></div>'
    f'<button class="btn sbtn" type="button">Mark shoot done</button></div>'
    for sh in SHOOTS)

pv_data = {str(d): dict(title=p["title"], meta=p["meta"], **p["pv"]) for d, p in P.items() if p.get("pv")}

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<title>Wellknox October Calendar</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Manrope:wght@400;500;700&display=swap" rel="stylesheet">
<style>
/* Layout: a month overview on top, then every post week by week with Preview, Approve and Make changes. */
:root {{
  --bg: #f1f5f4; --surface: #ffffff; --ink: #11201f; --muted: #5b6d6b; --line: #d7e2e0;
  --teal: #0b8277; --teal-ink: #ffffff; --teal-soft: #dff1ee;
  --navy: #26396a; --navy-soft: #e3e8f5;
  --amber: #a15e08; --amber-soft: #fbefd9;
  --slate: #66727a; --slate-soft: #e8ecee;
  --plum: #7a3b8f; --plum-soft: #f1e4f6;
  --display: "Bricolage Grotesque", "Trebuchet MS", system-ui, sans-serif;
  --body: "Manrope", system-ui, -apple-system, "Segoe UI", sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #0d1a19; --surface: #142624; --ink: #e6f1ef; --muted: #98b0ac; --line: #254240;
  --teal: #3cc4b4; --teal-ink: #072723; --teal-soft: #14403b; --navy: #9db3ee; --navy-soft: #1c2a4d;
  --amber: #f0b45c; --amber-soft: #3a2a10; --slate: #a9b6bd; --slate-soft: #22302f; --plum: #d6a6e8; --plum-soft: #35223d; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #0d1a19; --surface: #142624; --ink: #e6f1ef; --muted: #98b0ac; --line: #254240;
  --teal: #3cc4b4; --teal-ink: #072723; --teal-soft: #14403b; --navy: #9db3ee; --navy-soft: #1c2a4d;
  --amber: #f0b45c; --amber-soft: #3a2a10; --slate: #a9b6bd; --slate-soft: #22302f; --plum: #d6a6e8; --plum-soft: #35223d; color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--ink); font-family: var(--body); font-size: 15px; line-height: 1.5; }}
.wrap {{ max-width: 1180px; margin-inline: auto; padding-inline: 16px; padding-block: 28px 56px; }}
h1, h3, h4 {{ font-family: var(--display); margin: 0; text-wrap: balance; }}
.kick {{ font-size: 12px; letter-spacing: .14em; text-transform: uppercase; color: var(--teal); font-weight: 700; }}
h1 {{ font-size: clamp(34px, 6vw, 56px); line-height: 1.02; letter-spacing: -.02em; margin-top: 6px; }}
.lede {{ max-width: 62ch; color: var(--muted); margin: 10px 0 0; }}
.stats {{ display: flex; flex-wrap: wrap; gap: 8px 10px; margin-top: 18px; }}
.stat {{ display: flex; align-items: baseline; gap: 8px; padding: 8px 14px; border-radius: 999px; background: var(--surface); border: 1px solid var(--line); font-size: 14px; }}
.stat b {{ font-family: var(--display); font-size: 22px; font-variant-numeric: tabular-nums; }}
.dot {{ width: 9px; height: 9px; border-radius: 50%; align-self: center; }}
.dot.car, .dot.posted {{ background: var(--teal); }} .dot.reel {{ background: var(--navy); }} .dot.ai {{ background: var(--plum); }} .dot.open {{ background: var(--amber); }}
.allacts {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }}

.btn {{ display: inline-flex; align-items: center; justify-content: center; gap: 7px; min-height: 40px; padding: 0 16px; border-radius: 999px; font: 700 14px/1 var(--body); text-decoration: none; cursor: pointer; border: 1.5px solid var(--line); background: var(--surface); color: var(--ink); }}
.btn:focus-visible {{ outline: 3px solid var(--teal); outline-offset: 2px; }}
.btn.ok {{ background: var(--teal); border-color: var(--teal); color: var(--teal-ink); }}
.btn.ch {{ border-color: var(--amber); color: var(--amber); }}
.btn.pv {{ border-color: var(--navy); color: var(--navy); }}
.btn:hover {{ filter: brightness(1.06); }}

.shoots {{ margin-top: 26px; }}
.shoots h2 {{ margin: 0; font-size: 24px; }}
.sh-head {{ display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 14px; margin-bottom: 10px; }}
.live {{ font-size: 13px; color: var(--muted); }}
.live::before {{ content: ""; display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: var(--slate); margin-right: 7px; }}
.live.on::before {{ background: var(--teal); }}
.live:empty {{ display: none; }}
.sh-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 340px), 1fr)); gap: 12px; }}
.shoot {{ display: grid; grid-template-columns: 52px minmax(0, 1fr) auto; gap: 14px; align-items: center; background: var(--surface); border: 1.5px solid var(--amber); border-radius: 14px; padding: 12px 14px; }}
.shoot.done {{ border-color: var(--teal); background: var(--teal-soft); }}
.sd {{ display: flex; flex-direction: column; align-items: center; line-height: 1.1; }}
.sd b {{ font-family: var(--display); font-size: 28px; font-variant-numeric: tabular-nums; }}
.sd span {{ font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); font-weight: 700; }}
.sb h4 {{ font-size: 18px; }}
.ss {{ margin: 2px 0 0; font-size: 14px; color: var(--amber); font-weight: 700; }}
.shoot.done .ss {{ color: var(--teal); }}
.shoot.nobtn {{ grid-template-columns: 52px minmax(0, 1fr); }}
.gshoot {{ display: flex; flex-wrap: wrap; align-items: center; gap: 2px 6px; font-size: 11px; line-height: 1.25; font-weight: 700; color: var(--amber); background: var(--amber-soft); border-radius: 6px; padding: 5px 7px; text-decoration: none; }}
.gshoot .pip {{ width: 8px; height: 8px; border-radius: 50%; background: var(--amber); }}
.gshoot .gs-t {{ flex-basis: 100%; font-weight: 500; color: var(--muted); }}
.gshoot.done {{ color: var(--teal); background: var(--teal-soft); }}
.gshoot.done .pip {{ background: var(--teal); }}
.cal {{ margin-top: 26px; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 14px; }}
.dows, .grid {{ display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 6px; }}
.dows div {{ font-size: 11px; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); font-weight: 700; padding: 0 4px 6px; }}
.cell {{ min-height: 150px; border: 1px solid var(--line); border-radius: 8px; padding: 6px; display: flex; flex-direction: column; gap: 6px; min-width: 0; }}
.cell.blank {{ border-style: dashed; opacity: .35; }}
.cell.past {{ opacity: .45; background: var(--slate-soft); }}
.dn {{ font-family: var(--display); font-weight: 700; font-size: 15px; font-variant-numeric: tabular-nums; }}
.chip {{ display: flex; flex-direction: column; gap: 6px; min-width: 0; color: inherit; text-decoration: none; }}
.gth {{ width: 100%; height: 84px; object-fit: cover; border-radius: 6px; display: block; background: var(--slate-soft); }}
.gth.car {{ object-position: 50% 0; }}
.ph {{ display: grid; place-items: center; font-family: var(--display); font-size: 30px; border-radius: 6px; }}
.ph.open {{ border: 1.5px dashed var(--amber); color: var(--amber); background: var(--amber-soft); }}
.ct {{ display: flex; flex-direction: column; gap: 3px; min-width: 0; }}
.gt {{ font-size: 12px; line-height: 1.25; font-weight: 500; overflow-wrap: anywhere; }}
.badge {{ display: inline-block; align-self: flex-start; font-size: 10px; letter-spacing: .1em; text-transform: uppercase; font-weight: 700; padding: 2px 7px; border-radius: 4px; }}
.badge.car {{ background: var(--teal-soft); color: var(--teal); }}
.badge.reel {{ background: var(--navy-soft); color: var(--navy); }}
.badge.open {{ background: var(--amber-soft); color: var(--amber); }}
.badge.ai {{ background: var(--plum-soft); color: var(--plum); }}
.ph.ai {{ border: 1.5px dashed var(--plum); color: var(--plum); background: var(--plum-soft); font-size: 22px; }}
.badge.posted {{ background: var(--teal); color: var(--teal-ink); }}
.note-past {{ font-size: 12px; color: var(--muted); margin: 10px 4px 0; }}

h2 {{ font-family: var(--display); font-size: 28px; margin: 44px 0 4px; letter-spacing: -.01em; }}
.sub {{ color: var(--muted); margin: 0 0 14px; }}
.week {{ margin-top: 18px; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; overflow: hidden; }}
.week > header {{ padding: 16px 18px 12px; border-bottom: 1px solid var(--line); }}
.wn {{ font-size: 12px; letter-spacing: .12em; text-transform: uppercase; font-weight: 700; color: var(--teal); margin-right: 10px; }}
.wr {{ font-size: 13px; color: var(--muted); }}
.week h3 {{ font-size: 22px; margin-top: 4px; }}
.week header p {{ margin: 2px 0 0; color: var(--muted); font-size: 14px; max-width: 70ch; }}
.row {{ display: grid; grid-template-columns: 56px 92px minmax(0, 1fr); gap: 16px; padding: 16px 18px; border-top: 1px solid var(--line); align-items: start; scroll-margin-top: 12px; }}
.week > header + .row {{ border-top: 0; }}
.when {{ display: flex; flex-direction: column; align-items: center; line-height: 1.1; }}
.when b {{ font-family: var(--display); font-size: 30px; font-variant-numeric: tabular-nums; }}
.when span {{ font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); font-weight: 700; }}
.th {{ width: 92px; border-radius: 8px; display: block; object-fit: cover; background: var(--slate-soft); }}
img.th.reel, img.th.posted, img.th.ai {{ aspect-ratio: 9 / 16; }} img.th.car {{ aspect-ratio: 4 / 5; }}
.ph.th {{ aspect-ratio: 9 / 16; }}
.body {{ min-width: 0; }}
.top {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 4px; }}
.meta {{ font-size: 13px; color: var(--muted); }}
.row h4 {{ font-size: 19px; line-height: 1.2; }}
.row p {{ margin: 4px 0 12px; max-width: 62ch; }}
.acts {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
.nopv {{ font-size: 13px; color: var(--muted); flex-basis: 100%; }}
.row.open {{ background: color-mix(in srgb, var(--amber-soft) 40%, transparent); }}

.cols {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap: 14px; margin-top: 12px; }}
.card {{ background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 16px 18px; }}
.card h4 {{ font-size: 18px; margin-bottom: 8px; }}
.card ul {{ margin: 0 0 12px; padding-left: 18px; }}
.card li {{ margin: 4px 0; }}
.foot {{ margin-top: 36px; color: var(--muted); font-size: 14px; }}
.foot a {{ color: var(--teal); font-weight: 700; }}

{EXTRA_CSS}

dialog {{ width: min(460px, calc(100vw - 24px)); max-height: 94vh; padding: 0; border: 1px solid var(--line); border-radius: 16px; background: var(--surface); color: var(--ink); overflow: hidden; }}
dialog::backdrop {{ background: rgba(6, 16, 15, .72); }}
.dh {{ display: flex; align-items: center; gap: 12px; padding: 12px 14px 12px 18px; border-bottom: 1px solid var(--line); }}
.dh div {{ flex: 1; min-width: 0; }}
.dh b {{ display: block; font-family: var(--display); font-size: 17px; line-height: 1.2; }}
.dh span {{ font-size: 12px; color: var(--muted); }}
.x {{ width: 40px; height: 40px; border-radius: 50%; border: 1px solid var(--line); background: var(--bg); color: var(--ink); font-size: 20px; cursor: pointer; }}
.dbody {{ padding: 12px; display: flex; flex-direction: column; align-items: center; gap: 10px; background: #0a1413; }}
.dbody video {{ display: block; max-width: 100%; max-height: 68vh; border-radius: 10px; background: #000; }}
.slides {{ display: flex; width: 100%; overflow-x: auto; scroll-snap-type: x mandatory; gap: 10px; scrollbar-width: none; }}
.slides::-webkit-scrollbar {{ display: none; }}
.slides video {{ flex: 0 0 100%; scroll-snap-align: center; max-height: 62vh; object-fit: contain; }}
.nav {{ display: flex; align-items: center; gap: 12px; color: #e6f1ef; font-size: 14px; }}
.nav .btn {{ min-height: 40px; padding: 0 14px; background: transparent; color: #e6f1ef; border-color: #3a5a57; }}
.dfoot {{ display: flex; flex-wrap: wrap; gap: 8px; padding: 12px 14px; border-top: 1px solid var(--line); }}

@media (max-width: 860px) {{
  .cal {{ display: none; }}
  .row {{ grid-template-columns: 48px 76px minmax(0, 1fr); gap: 12px; padding: 14px; }}
  .th {{ width: 76px; }}
}}
@media (max-width: 560px) {{
  body {{ font-size: 16px; }}
  .wrap {{ padding-block: 20px 40px; }}
  .btn {{ min-height: 46px; font-size: 15px; }}
  .stats {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
  .stat {{ border-radius: 14px; padding: 8px 12px; font-size: 13px; line-height: 1.25; align-items: center; }}
  .stat b {{ font-size: 20px; }}
  .allacts .btn {{ flex: 1 1 100%; }}
  .sh-head {{ gap: 8px 12px; }}
  .sh-head .live {{ flex: 1 1 100%; order: 3; }}
  .shoot {{ grid-template-columns: 48px minmax(0, 1fr); gap: 8px 12px; }}
  .shoot .sbtn {{ grid-column: 1 / -1; width: 100%; }}
  .addform label {{ flex: 1 1 100%; }}
  .addform input {{ width: 100%; min-height: 46px; font-size: 16px; }}
  .addform .btn {{ flex: 1 1 calc(50% - 6px); }}
  .week > header {{ padding: 14px; }}
  .row {{ grid-template-columns: 52px minmax(0, 1fr); gap: 4px 12px; padding: 16px 14px; }}
  .row .body {{ display: contents; }}
  .row .when {{ grid-column: 1; grid-row: 1; }}
  .row .th {{ grid-column: 1; grid-row: 2 / span 2; width: 52px; margin-top: 6px; }}
  .row .top {{ grid-column: 2; grid-row: 1; margin: 0; }}
  .row h4 {{ grid-column: 2; grid-row: 2; font-size: 18px; margin-top: 2px; }}
  .row p {{ grid-column: 2; grid-row: 3; margin: 2px 0 10px; }}
  .row .acts {{ grid-column: 1 / -1; grid-row: 4; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
  .row .acts .btn {{ width: 100%; padding: 0 8px; }}
  .row .acts .nopv, .row .acts .lnk {{ grid-column: 1 / -1; text-align: center; }}
  .row.open .acts .btn.up, .row.ai .acts .btn.up {{ grid-column: 1 / -1; }}
  dialog {{ width: calc(100vw - 16px); max-height: 96vh; }}
  .dbody video {{ max-height: 58vh; }}
  .dfoot .btn {{ flex: 1 1 calc(50% - 4px); }}
}}
@media (prefers-reduced-motion: no-preference) {{ .slides {{ scroll-behavior: smooth; }} }}
</style>
</head>
<body>
<div class="wrap">
  <div class="kick">Wellknox · content plan</div>
  <h1>October 2026</h1>
  <p class="lede">Open Preview to watch each post. Tap Approve or Make changes, and both open WhatsApp with the post filled in, so you only press send. When a post goes live, tap Mark uploaded.</p>
  <div class="stats">
    <div class="stat"><span class="dot car"></span><b>{n_car}</b> carousels, Thursdays</div>
    <div class="stat"><span class="dot reel"></span><b>{n_reel}</b> reels</div>
    <div class="stat"><span class="dot ai"></span><b>{n_ai}</b> AI influencer reels</div>
    <div class="stat"><span class="dot open"></span><b>{n_open}</b> open slots</div>
    <div class="stat"><span class="dot posted"></span><b>1</b> posted Oct 6</div>
  </div>
  <div class="legend" aria-label="Status colours">
    <span><i style="background:var(--slate)"></i>Awaiting approval</span>
    <span><i style="background:var(--approved)"></i>Approved</span>
    <span><i style="background:var(--changes)"></i>Changes requested</span>
    <span><i style="background:var(--uploaded)"></i>Uploaded</span>
  </div>
  <div class="allacts">
    <a class="btn ok solid" href="{all_ok}" target="_blank" rel="noopener">{TICK}Approve the whole month</a>
    <a class="btn ch" href="{all_ch}" target="_blank" rel="noopener">{PEN}Make changes</a>
  </div>

  <section class="shoots" id="shoots" aria-labelledby="sh-h">
    <div class="sh-head"><h2 id="sh-h">Shoots this month</h2><span class="live" id="live" role="status"></span>
      <button class="btn add" id="addshoot" type="button" aria-expanded="false" aria-controls="addform"><span class="plus" aria-hidden="true">+</span>Add shoot</button></div>
    <form class="addform" id="addform" hidden>
      <label>Place<input id="ash-place" maxlength="40" required placeholder="e.g. Madhapur"></label>
      <label>Date<input id="ash-date" type="date" min="2026-10-01" max="2026-10-31" required></label>
      <button class="btn ok solid" type="submit">Add shoot</button>
      <button class="btn" type="button" id="ash-cancel">Cancel</button>
      <span id="ash-msg" role="status"></span>
    </form>
    <div class="sh-grid">{shoot_cards}</div>
  </section>

  <div class="cal" aria-label="October 2026 calendar">
    <div class="dows">{dow_head}</div>
    <div class="grid">{grid}</div>
    <p class="note-past">Tap a post to jump to its details. Oct 1 to 5 are shaded because they have passed.</p>
  </div>

  <h2>The thinking behind October</h2>
  <p class="sub">Why the month is laid out this way.</p>
  <div class="cols">
    <div class="card"><h4>Learn on Thursday</h4><p>One carousel every Thursday: robotic gait, kids rehab, gait suspension and aqua therapy. Each one is a short guide families can save and share, and it explains a therapy in plain words before anyone has to ask.</p></div>
    <div class="card"><h4>Hear from patients on Friday</h4><p>Fridays from Oct 16, plus Oct 20 and 27, are held for testimonials and patient videos. A guide on Thursday, then a real person the next day. The shoots on Oct 9 and 12 come first, so there is time to edit.</p></div>
    <div class="card"><h4>Reels with four jobs</h4><p>Brand story (the launch journey and the AI branch introductions), education (6 levels of stroke rehab), emotion (the emotional reel and the Somali patient story) and a lighter skit (30 Din).</p></div>
    <div class="card"><h4>A four-week arc</h4><p>Week 1 builds trust and shows the technology. Week 2 explains how rehab works. Week 3 shows recovery you can see. Week 4 turns to water therapy and ends the month on emotion.</p></div>
    <div class="card"><h4>Two branches in focus</h4><p>The Financial District reel (Oct 9) introduces the branch that is already open. The Banjara Hills reel (Oct 13) builds awareness before that centre opens, and the launch journey (Oct 11) shows the track record behind both. A free day is kept for a launch-day post once the Banjara Hills date is fixed.</p></div>
    <div class="card"><h4>Posts that pair up</h4><p>The stroke reel posted on Oct 6 leads into the gait suspension carousel on Oct 22. The 6 levels reel on Oct 14 leads into the stroke family testimonial on Oct 16.</p></div>
  </div>
  <p class="sub" style="margin-top:14px">Nothing goes out unchecked: every post has Preview, Approve and Make changes, and each status is shared live.</p>

  <h2>Week by week</h2>
  <p class="sub">Every post with its idea. Approve or ask for changes on each one.</p>
  {"".join(agenda)}

  <h2>For the open slots</h2>
  <div class="cols">
    <div class="card"><h4>What we need from you</h4><ul>
      <li>Open slots: Fri 16, Tue 20, Fri 23, Tue 27 and Fri 30 Oct.</li>
      <li>Raw clips by Monday: 12, 19 and 26 Oct.</li>
      <li>We edit within two days of receiving them.</li>
      <li>If a slot is not ready, we move a finished reel into it.</li></ul></div>
    <div class="card"><h4>What to shoot</h4><ul>
      <li>Vertical, 9:16, 30 to 45 seconds, patient or family speaking to camera.</li>
      <li>Ask for their own words: what changed, and what they can do now.</li>
      </ul></div>
    <div class="card"><h4>Launch dates</h4><ul>
      <li>The Financial District branch is already open. The Banjara Hills Rehab centre opens this month.</li>
      <li>Send us the date and we will plan the launch-day post.</li></ul>
      <a class="btn pv" href="{launch}" target="_blank" rel="noopener">Send launch date</a></div>
  </div>
  <p class="foot">Questions? WhatsApp <a href="{wa('Hi, a question about the October calendar: ')}" target="_blank" rel="noopener">+91 79818 27087</a></p>
</div>

<dialog id="pv" aria-labelledby="pvt">
  <div class="dh"><div><b id="pvt"></b><span id="pvm"></span></div><button class="x" type="button" id="pvx" aria-label="Close preview">×</button></div>
  <div class="dbody" id="pvb"></div>
  <div class="dfoot" id="pvf"></div>
</dialog>
<script>
(function () {{
  var PV = {json.dumps(pv_data)};
  var LINKS = {json.dumps({str(d): dict(ok=approve_link(d, p), ch=change_link(d, p), key=p["key"]) for d, p in P.items() if p["k"] != "posted"})};
  var dlg = document.getElementById("pv"), body = document.getElementById("pvb"), foot = document.getElementById("pvf");
  function close() {{ try {{ dlg.close(); }} catch (e) {{}} }}
  function clear() {{ body.querySelectorAll("video").forEach(function (v) {{ v.pause(); v.removeAttribute("src"); v.load(); }}); body.textContent = ""; foot.textContent = ""; }}
  function mk(src, o) {{ var v = document.createElement("video"); v.src = src; v.playsInline = true; v.preload = "metadata"; for (var k in o) v[k] = o[k]; return v; }}
  function open(day) {{
    var d = PV[day]; if (!d) return;
    clear();
    document.getElementById("pvt").textContent = d.title;
    document.getElementById("pvm").textContent = d.meta;
    if (d.t === "reel") {{
      var v = mk(d.s[0], {{ controls: true }}); body.appendChild(v);
      dlg.showModal(); var pr = v.play(); if (pr && pr.catch) pr.catch(function () {{}});
    }} else {{
      var wrap = document.createElement("div"); wrap.className = "slides"; wrap.setAttribute("tabindex", "0");
      var vids = d.s.map(function (s) {{ var v = mk(s, {{ muted: true, loop: true }}); wrap.appendChild(v); return v; }});
      var nav = document.createElement("div"); nav.className = "nav";
      var prev = document.createElement("button"), next = document.createElement("button"), cnt = document.createElement("span");
      prev.className = next.className = "btn"; prev.type = next.type = "button"; prev.textContent = "Back"; next.textContent = "Next";
      nav.appendChild(prev); nav.appendChild(cnt); nav.appendChild(next);
      body.appendChild(wrap); body.appendChild(nav);
      var cur = 0;
      function show(i) {{
        cur = Math.max(0, Math.min(vids.length - 1, i));
        vids.forEach(function (v, j) {{ if (j === cur) {{ var p = v.play(); if (p && p.catch) p.catch(function () {{}}); }} else v.pause(); }});
        cnt.textContent = "Slide " + (cur + 1) + " of " + vids.length;
      }}
      prev.onclick = function () {{ wrap.scrollTo({{ left: (cur - 1) * wrap.clientWidth, behavior: "smooth" }}); show(cur - 1); }};
      next.onclick = function () {{ wrap.scrollTo({{ left: (cur + 1) * wrap.clientWidth, behavior: "smooth" }}); show(cur + 1); }};
      var t; wrap.addEventListener("scroll", function () {{ clearTimeout(t); t = setTimeout(function () {{ var i = Math.round(wrap.scrollLeft / wrap.clientWidth); if (i !== cur) show(i); }}, 80); }});
      dlg.showModal(); show(0);
    }}
    var L = LINKS[day];
    if (L) {{
      [["ok", "Approve", "btn ok", "approved"], ["ch", "Make changes", "btn ch", "changes"]].forEach(function (x) {{
        var a = document.createElement("a"); a.className = x[2]; a.setAttribute("data-pkey", L.key); a.setAttribute("data-act", x[3]); a.textContent = x[1]; a.href = L[x[0]]; a.target = "_blank"; a.rel = "noopener"; foot.appendChild(a);
      }});
    }}
  }}
  document.querySelectorAll(".btn.pv[data-day]").forEach(function (b) {{ b.addEventListener("click", function () {{ open(b.getAttribute("data-day")); }}); }});
  document.getElementById("pvx").addEventListener("click", close);
  dlg.addEventListener("click", function (e) {{ if (e.target === dlg) close(); }});
  dlg.addEventListener("close", clear);
}})();
</script>
<script>
{LIVE_JS}
</script>
</body>
</html>
"""
open(OUT, "w").write(page)
import os
files = sorted(os.listdir(f"{S}/previews"))
print("bytes", len(page.encode()), "previews", len(files), "counts", n_car, n_reel, n_open)
