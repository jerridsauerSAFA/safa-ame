"""Load every page at phone + desktop width; report console/page errors, sideways scroll, failed requests.
usage: check.py [base_url] [--shots]"""
import sys, os, json, re
from playwright.sync_api import sync_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 'http://127.0.0.1:8765/'
SHOTS = '--shots' in sys.argv
DIST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dist')
OUT = '/home/claude/spp/shots'; os.makedirs(OUT, exist_ok=True)
pages = sorted(f for f in os.listdir(DIST) if f.endswith('.html'))
pages.remove('index.html'); pages.insert(0, 'index.html')
VIEWS = {'phone': dict(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True),
         'desk': dict(viewport={'width': 1280, 'height': 800})}
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for vname, opts in VIEWS.items():
        ctx = b.new_context(**opts)
        for fn in pages:
            pg = ctx.new_page(); errs = []
            pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type in ('error',) else None)
            pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
            pg.on('requestfailed', lambda r: errs.append('reqfail: ' + r.url[:120]) if 'fonts.g' not in r.url else None)
            pg.goto(BASE + ('' if fn == 'index.html' else fn), wait_until='networkidle')
            pg.wait_for_timeout(300)
            info = pg.evaluate('''() => {
              const W = document.documentElement.clientWidth;
              const over = [];
              document.querySelectorAll('body *').forEach(el => {
                const r = el.getBoundingClientRect();
                if (r.width && r.right > W + 1 && getComputedStyle(el).position !== 'fixed') {
                  // ignore elements clipped by a scrolling/hidden ancestor
                  let a = el.parentElement, clipped = false;
                  while (a && a !== document.body) { const o = getComputedStyle(a).overflowX; if (o === 'auto' || o === 'scroll' || o === 'hidden') { clipped = true; break; } a = a.parentElement; }
                  if (!clipped) over.push((el.id ? '#' + el.id : el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : '')) + ' →' + Math.round(r.right));
                }
              });
              return {sw: document.documentElement.scrollWidth, W, over: over.slice(0, 6), bar: !!document.getElementById('spp-bar'),
                      h: document.documentElement.scrollHeight, title: document.title};
            }''')
            flag = []
            if errs: flag.append('ERR ' + ' | '.join(errs[:4]))
            if info['sw'] > info['W'] + 1: flag.append(f"SIDEWAYS {info['sw']}>{info['W']}")
            if info['over']: flag.append('OVERFLOW ' + ', '.join(info['over']))
            if not info['bar']: flag.append('NO BAR')
            if info['h'] < 900 and fn != 'index.html': flag.append(f"SHORT {info['h']}")
            if flag: bad += 1
            print(f"{vname:5} {fn:22} {'OK' if not flag else '; '.join(flag)}")
            if SHOTS: pg.screenshot(path=f'{OUT}/{vname}-{fn[:-5]}.png', full_page=False)
            pg.close()
        ctx.close()
    b.close()
print('pages with issues:', bad)
