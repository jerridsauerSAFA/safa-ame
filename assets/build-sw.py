#!/usr/bin/env python3
"""Rebuild sw.js: refresh the offline list and bump the version.
Run from the repo root after adding or changing any page:   python3 assets/build-sw.py
Saved on first visit: every HTML page, the notes photos, shared CSS/JS, logos and icons.
Saved only when opened: print JPGs and PDFs (they are large)."""
import os, json, datetime, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
skip_dirs = {'.git'}
keep_ext = {'.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.svg', '.webmanifest', '.webp'}
files = []
for d, dirs, fs in os.walk('.'):
    dirs[:] = [x for x in dirs if x not in skip_dirs]
    for f in fs:
        p = os.path.join(d, f)[2:].replace(os.sep, '/')
        ext = os.path.splitext(f)[1].lower()
        if ext not in keep_ext: continue
        if p in ('sw.js', 'assets/sw.template.js') or p.endswith('.py'): continue
        if '/pdf/' in p and ext != '.html': continue        # print JPG/PDF: runtime only
        files.append(p)
files.sort()
dirs_with_index = sorted({os.path.dirname(p) + '/' for p in files if p.endswith('/index.html')})
precache = ['./'] + dirs_with_index + files
h = hashlib.sha1()
for p in files:
    with open(p, 'rb') as fh: h.update(p.encode()); h.update(fh.read())
version = datetime.date.today().isoformat() + '-' + h.hexdigest()[:8]
size = sum(os.path.getsize(p) for p in files)

tpl = open('assets/sw.template.js', encoding='utf-8').read()
out = tpl.replace('__VERSION__', version).replace('__PRECACHE__', json.dumps(precache, indent=0))
open('sw.js', 'w', encoding='utf-8').write(out)
print('sw.js version', version, '·', len(precache), 'entries ·', round(size / 1e6, 2), 'MB saved on first visit')
