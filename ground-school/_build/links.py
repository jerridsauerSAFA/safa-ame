"""Render every page and list every link a student could tap. Flags anything outside this site except TC/ISED sources."""
import os, sys, collections
from playwright.sync_api import sync_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765/'
DIST = 'dist'
OK_EXT = ('https://tc.canada.ca/', 'https://ised-isde.canada.ca/')
pages = sorted(f for f in os.listdir(DIST) if f.endswith('.html'))
internal = set(); outside = collections.Counter(); broken = set()
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True)
    for fn in pages:
        pg = ctx.new_page(); pg.goto(BASE + ('' if fn == 'index.html' else fn), wait_until='networkidle'); pg.wait_for_timeout(300)
        for h in pg.eval_on_selector_all('a[href]', 'els => els.map(e => e.href)'):
            h = h.split('#')[0]
            if h.startswith(BASE): internal.add(h[len(BASE):] or 'index.html')
            elif not h.startswith(OK_EXT) and not h.startswith('javascript:') and h: outside[(fn, h)] += 1
        pg.close()
    b.close()
existing = set(os.listdir(DIST))
broken = sorted(x for x in internal if x not in existing)
print('internal targets:', len(internal), '| broken:', broken)
print('outside links:', dict(outside) if outside else 'none')
