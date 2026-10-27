#!/usr/bin/env python3
"""Put an ASYS 245 page on the shared SAFA chrome.

  restyle.py full <file> <mod> <page-key> [label]   legacy blue study page -> SAFA tokens + nav
  restyle.py nav  <file> <mod> <page-key> [label] [dark]   already-SAFA page -> nav only, page look untouched

Run from the repo root with paths like asys245/module-3/x.html. Idempotent."""
import re, sys, os

mode, f, mod, page = sys.argv[1:5]
label = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] not in ('', 'dark') else ''
dark = 'dark' in sys.argv[5:]
s = open(f, encoding='utf-8').read()
root = '../' * (len(os.path.normpath(f).split(os.sep)) - 1)
if 'assets/safa.js' in s:
    print('already done', f); sys.exit(0)

if mode == 'full':
    # 1. drop the three legacy token blocks (light, dark media query, forced dark)
    s = re.sub(r':root\{\s*--bg:#F4F6F8[^}]*\}', '', s, count=1)
    s = re.sub(r'@media \(prefers-color-scheme: dark\)\{\s*:root:not\(\[data-theme="light"\]\)\{[^}]*\}\s*\}', '', s, count=1)
    s = re.sub(r':root\[data-theme="dark"\]\{[^}]*\}', '', s, count=1)
    # 2. let safa.css own background, font and padding
    s = re.sub(r'body\{margin:0;background:var\(--bg\);color:var\(--ink\);font:[^}]*\}', 'body{margin:0}', s, count=1)
    # 3. fonts
    s = s.replace('"Source Sans 3",system-ui,-apple-system,Segoe UI,sans-serif', 'var(--font)')
    s = s.replace('"Source Sans 3",sans-serif', 'var(--font)').replace('"Source Sans 3"', '"Inter"')
    s = re.sub(r'family=Source\+Sans\+3:[^&"]*', 'family=Inter:wght@400;500;600', s)
    # 4. hard-coded blues in late style blocks
    for a, b in [('#1D5C8F', 'var(--accent)'), ('#1d5c8f', 'var(--accent)'), ('rgba(29,92,143,.08)', 'var(--cue)'),
                 ('#c9d3dd', 'var(--line)'), ('#b8c2cc', '#9aa5b1'), ('color:#111;', 'color:var(--ink);'), ('#8a949e', 'var(--ink-3)')]:
        s = s.replace(a, b)
    s = s.replace('padding:.5rem .7rem .4rem;background:#fff}', 'padding:.5rem .7rem .4rem;background:var(--surface)}')
    links = '<link rel="stylesheet" href="%sassets/safa-nav.css">\n<link rel="stylesheet" href="%sassets/safa.css">' % (root, root)
    cls = 'study-page'
else:
    links = '<link rel="stylesheet" href="%sassets/safa-nav.css">' % root
    cls = ''

# 5. app tags, sheets, theme colour, body attributes, script
HEAD = ('<link rel="manifest" href="{r}manifest.webmanifest">\n<link rel="icon" type="image/png" sizes="32x32" href="{r}assets/icons/favicon-32.png">\n'
        '<link rel="apple-touch-icon" href="{r}assets/icons/apple-touch-icon.png">\n<meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-title" content="ASYS 245"><meta name="apple-mobile-web-app-status-bar-style" content="black">\n').format(r=root)
links = HEAD + links.replace('assets/safa-nav.css">', 'assets/safa-nav.css">\n<link rel="stylesheet" href="%sassets/safa-touch.css">' % root, 1)
s = s.replace('</head>', links + '\n<meta name="theme-color" content="#0b0b0c">\n</head>', 1)
def body(m):
    attrs = m.group(1)
    extra = ''
    if cls:
        if 'class="' in attrs: attrs = attrs.replace('class="', 'class="%s ' % cls, 1)
        else: extra += ' class="%s"' % cls
    extra += ' data-mod="%s" data-page="%s"' % (mod, page)
    if label: extra += ' data-label="%s"' % label
    if dark: extra += ' data-nav-theme="dark"'
    return '<body%s%s>' % (attrs, extra)
s = re.sub(r'<body([^>]*)>', body, s, count=1)
s = s.replace('</body>', '<script src="%sassets/safa.js" defer></script>\n</body>' % root, 1)
open(f, 'w', encoding='utf-8').write(s)
print(mode, f)
