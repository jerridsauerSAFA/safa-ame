"""Part overview pages for the static site.
The Drive originals (<pid>-title.html) can't be pulled through the connector, so these are rebuilt from the
same COURSE data the hub pages use. If a real <pid>-title.html is ever placed in src/, build.py uses that instead."""
import html

CSS = """
:root{--bg:#000;--panel:#121110;--panel2:#1b1915;--line:#2e2a23;--fg:#fff;--muted:#a8a39a;--soft:#d8d4cc;--gold:#d8b358;
  --display:"Poppins","Helvetica Neue",Arial,sans-serif;--body:"Source Sans 3","Segoe UI",Arial,sans-serif;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--body);font-size:17px;line-height:1.5}
.wrap{max-width:980px;margin:0 auto;padding:0 16px 48px}
.crumb{display:inline-block;margin:20px 0 0;color:var(--muted);font-size:15px;text-decoration:none}
.crumb:hover{color:var(--gold)}
.hero{padding:14px 0 22px;border-bottom:1px solid var(--line)}
.eyebrow{font-family:var(--display);font-weight:600;font-size:12px;letter-spacing:.16em;color:var(--gold);text-transform:uppercase}
h1{font-family:var(--display);font-weight:800;font-size:clamp(28px,6.5vw,44px);line-height:1.08;margin:8px 0 12px;letter-spacing:-.01em}
h1 span{color:var(--gold)}
.lede{margin:0;color:var(--soft);font-size:18px;max-width:38em}
.lessons{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 0;padding:0;list-style:none}
.lessons li{padding:6px 12px;border-radius:999px;background:var(--panel2);border:1px solid var(--line);font-size:15px}
.lessons b{color:var(--gold);font-family:var(--display);font-weight:700;margin-right:6px}
h2{font-family:var(--display);font-weight:700;font-size:20px;margin:30px 0 12px}
h2 small{display:block;font-family:var(--body);font-weight:400;font-size:15px;color:var(--muted);margin-top:2px}
.tiles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;list-style:none;margin:0;padding:0;counter-reset:s}
.tiles a{counter-increment:s;display:grid;grid-template-columns:36px minmax(0,1fr);column-gap:14px;align-items:start;height:100%;
  background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:16px 18px;color:var(--fg);text-decoration:none;transition:border-color .15s,transform .15s}
.tiles a::before{content:counter(s);grid-row:span 3;display:grid;place-items:center;width:36px;height:36px;border-radius:50%;background:var(--gold);color:#000;font-family:var(--display);font-weight:800}
.tiles a:hover,.tiles a:focus-visible{border-color:var(--gold);transform:translateY(-2px);outline:none}
.tiles b{font-family:var(--display);font-weight:700;font-size:18px}
.tiles span{color:var(--soft);font-size:15px;line-height:1.4;margin-top:2px}
.tiles em{font-style:normal;color:var(--gold);font-family:var(--display);font-weight:600;font-size:14px;margin-top:8px}
.pass{margin:14px 0 0;padding:12px 14px;border-left:3px solid var(--gold);background:var(--panel2);border-radius:0 12px 12px 0;color:var(--soft);font-size:16px}
.pass b{color:var(--fg)}
.pager{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:30px}
.pager a{display:flex;flex-direction:column;gap:2px;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 16px;color:var(--fg);text-decoration:none;min-height:64px}
.pager a:hover,.pager a:focus-visible{border-color:var(--gold);outline:none}
.pager a.next{text-align:right;grid-column:2}
.pager small{color:var(--muted);font-size:13px;text-transform:uppercase;letter-spacing:.08em}
.pager b{font-family:var(--display);font-weight:700;font-size:15px}
footer{margin-top:40px;padding-top:18px;border-top:1px solid var(--line);text-align:center}
footer img{width:60px}
footer div{font-family:var(--display);font-weight:700;font-size:12px;letter-spacing:.3em;color:var(--gold);margin-top:4px}
@media (max-width:640px){.tiles,.pager{grid-template-columns:1fr}.pager a.next{grid-column:auto}}
"""


def page(exam, hub_file, pass_pct, units, i):
    u = units[i]
    e = html.escape
    pid = u['pid']
    n_less = len(u['lessons'])
    lessons = ''.join(f'<li><b>{e(c)}</b>{e(t)}</li>' for c, t in u['lessons'])
    tiles = [
        (f'{pid}-notes.html', 'Cornell Notes', 'Read each lesson, then turn on study mode and quiz yourself with the cue questions.',
         f'{n_less} lesson{"s" if n_less != 1 else ""}'),
        (f'{pid}-cards.html', 'Flashcards', 'Short daily sessions. Keep going until every card is mastered.', f'{u["cards"]} cards'),
        (f'{pid}-quiz.html', 'Practice Quizzes', 'Exam A and Exam B for every lesson, plus a mixed review of the whole part.',
         f'{u["questions"]} questions'),
        (f'{pid}-lab.html', 'Skills Lab', f'{u["lab"]["name"]}: put the part to work, hands-on.', f'{u["lab"]["n"]} tasks'),
    ]
    tiles_html = ''.join(f'<li><a href="{f}"><b>{e(t)}</b><span>{e(d)}</span><em>{e(m)}</em></a></li>' for f, t, d, m in tiles)
    prev_ = units[i - 1] if i > 0 else None
    next_ = units[i + 1] if i + 1 < len(units) else None
    pager = ''
    if prev_:
        pager += f'<a href="{prev_["pid"]}-title.html"><small>← Part {prev_["part"]}</small><b>{e(prev_["title"])}</b></a>'
    if next_:
        pager += f'<a class="next" href="{next_["pid"]}-title.html"><small>Part {next_["part"]} →</small><b>{e(next_["title"])}</b></a>'
    else:
        pager += f'<a class="next" href="{hub_file.replace(".html", "-mock.html")}"><small>When every part is done →</small><b>{e(exam)} Mock Exams</b></a>'
    return f"""<!doctype html>
<!-- SAFA-PAGE id={pid}-title kind=title template=static-overview@1 by=claude date=2026-11-06 -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SAFA Ground School – {e(exam)} · Part {u['part']} Overview</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Source+Sans+3:wght@400;600;700&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <a class="crumb" href="{hub_file}">← {e(exam)} home</a>
  <section class="hero">
    <div class="eyebrow">Student Pilot Permit · {e(exam)} · Part {u['part']} of {len(units)}</div>
    <h1>{e(u['title'])}</h1>
    <p class="lede">{e(u['lede'])}</p>
    <ul class="lessons">{lessons}</ul>
  </section>
  <h2>Study this part<small>Work through them in order.</small></h2>
  <ol class="tiles">{tiles_html}</ol>
  <p class="pass"><b>Pass mark: {pass_pct}%.</b> Aim well above it on both quizzes for every lesson before you move on.</p>
  <nav class="pager" aria-label="Parts">{pager}</nav>
  <footer><img src="safa-mark.png" alt=""><div>LEARN. FLY. BUILD. LEAD.</div></footer>
</div>
<script>try {{ google.script.run.withFailureHandler(function () {{}}).track('{pid}-title', {u['no']}, 'visit', '{{}}', ''); }} catch (e) {{}}</script>
</body>
</html>
"""
