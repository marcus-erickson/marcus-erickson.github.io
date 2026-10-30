#!/usr/bin/env python3
"""Build index.html from projects.json. Run: python3 build.py"""
import html, json
from pathlib import Path

root = Path(__file__).parent
data = json.loads((root / "projects.json").read_text(encoding="utf-8"))
e = html.escape

def card(it):
    repo = f"https://github.com/marcus-erickson/{it['repo']}"
    links = []
    if it.get("page"):
        links.append(f'<a class="btn primary" href="{e(it["page"])}">Open the page</a>')
    if it.get("download"):
        links.append(f'<a class="btn" href="{e(it["download"])}" download>Download</a>')
    links.append(f'<a class="btn" href="{e(repo)}">GitHub</a>')
    tags = "".join(f"<li>{e(t)}</li>" for t in it.get("tags", []))
    return (f'<article class="card"><h3>{e(it["name"])}</h3><ul class="tags">{tags}</ul>'
            f'<p>{e(it["description"])}</p><div class="links">{"".join(links)}</div></article>')

groups = "\n".join(
    f'<section><h2>{e(g["name"])}</h2><div class="grid">{"".join(card(i) for i in g["items"])}</div></section>'
    for g in data["groups"]
)

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(data["title"])}</title>
<style>
:root {{ --bg:#f4f6f9; --paper:#fff; --ink:#1b2430; --muted:#5b6675; --line:#d9dfe7; --accent:#1f4f7a; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#10151c; --paper:#18202a; --ink:#e6ebf1; --muted:#9aa6b5; --line:#2a3544; --accent:#7db3e6; }} }}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; }}
main {{ max-width:1000px; margin:0 auto; padding:40px 16px 56px; }}
h1 {{ margin:0 0 8px; font-size:30px; line-height:1.2; }}
.lede {{ margin:0 0 8px; max-width:62ch; color:var(--muted); }}
h2 {{ margin:36px 0 14px; font-size:12px; letter-spacing:.09em; text-transform:uppercase; color:var(--muted); }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(290px,1fr)); gap:16px; }}
.card {{ display:flex; flex-direction:column; padding:18px; background:var(--paper); border:1px solid var(--line); border-radius:8px; }}
.card h3 {{ margin:0 0 6px; font-size:18px; }}
.card p {{ margin:10px 0 16px; flex:1; font-size:15px; }}
.tags {{ display:flex; flex-wrap:wrap; gap:6px; margin:0; padding:0; list-style:none; }}
.tags li {{ padding:1px 8px; border:1px solid var(--line); border-radius:99px; font-size:12px; color:var(--muted); }}
.links {{ display:flex; flex-wrap:nowrap; gap:6px; }}
.btn {{ flex:1 1 auto; min-width:0; padding:6px 6px; border:1px solid var(--line); border-radius:6px; color:var(--ink); font-size:13px; font-weight:500; text-align:center; white-space:nowrap; text-decoration:none; }}
.btn.primary {{ background:var(--accent); border-color:var(--accent); color:var(--paper); }}
.btn:hover {{ text-decoration:underline; }}
footer {{ margin-top:40px; font-size:13px; color:var(--muted); }}
</style></head>
<body><main>
<h1>{e(data["title"])}</h1>
<p class="lede">{e(data["intro"])}</p>
{groups}
<footer>Examples and starting points. Check anything they produce before relying on it.</footer>
</main></body></html>
"""
(root / "index.html").write_text(page, encoding="utf-8")
print(f"Wrote index.html with {sum(len(g['items']) for g in data['groups'])} items")
