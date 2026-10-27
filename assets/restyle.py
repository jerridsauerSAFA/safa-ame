#!/usr/bin/env python3
"""Move a pre-Oct-2026 ASYS 245 study page onto the shared SAFA sheet.
Usage: restyle.py <file> <mod> <page-key>   e.g. restyle.py 01_Cornell_Notes_Module4.html 4 notes
Idempotent: skips files already carrying safa.css."""
import re, sys, os
f, mod, page = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(f, encoding='utf-8').read()
if 'assets/safa.css' in s:
    print('already restyled', f); sys.exit(0)
depth = f.count('/')  # files passed as asys245/module-N/x.html from repo root
root = '../' * (len(os.path.normpath(f).split(os.sep)) - 1)

# 1. drop the three legacy :root token blocks
s = re.sub(r':root\{\s*--bg:#F4F6F8[^}]*\}', '', s, count=1, flags=re.S)
s = re.sub(r'@media \(prefers-color-scheme: dark\)\{\s*:root:not\(\[data-theme="light"\]\)\{.*?\}\s*\}', '', s, count=1, flags=re.S)
s = re.sub(r':root\[data-theme="dark"\]\{.*?\n?\}', '', s, count=1, flags=re.S)
# 2. body rule: let safa.css own background, font and padding
s = re.sub(r'body\{margin:0;background:var\(--bg\);color:var\(--ink\);font:[^}]*\}', 'body{margin:0}', s, count=1)
# 3. fonts
s = s.replace('"Source Sans 3",system-ui,-apple-system,Segoe UI,sans-serif', 'var(--font)')
s = s.replace('"Source Sans 3",sans-serif', 'var(--font)').replace('"Source Sans 3"', '"Inter"')
s = re.sub(r'family=Source\+Sans\+3:[^&"]*', 'family=Inter:wght@400;500;600', s)
# 4. hard-coded blues in late style blocks
s = s.replace('#1D5C8F', 'var(--accent)').replace('rgba(29,92,143,.08)', 'var(--cue)')
s = s.replace('#c9d3dd', 'var(--line)').replace('#b8c2cc', '#9aa5b1').replace('color:#111;', 'color:var(--ink);').replace('#8a949e', 'var(--ink-3)')
s = s.replace('.mine{margin:.9rem 0 .4rem;border:1px solid var(--line);border-radius:6px;padding:.5rem .7rem .4rem;background:#fff}',
              '.mine{margin:.9rem 0 .4rem;border:1px solid var(--line);border-radius:6px;padding:.5rem .7rem .4rem;background:var(--surface)}')
# 5. shared sheet + script + body attributes
s = s.replace('</head>', '<link rel="stylesheet" href="%sassets/safa.css">\n<meta name="theme-color" content="#0b0b0c">\n</head>' % root, 1)
s = re.sub(r'<body([^>]*)>', lambda m: '<body%s class="study-page" data-mod="%s" data-page="%s">' % (m.group(1), mod, page), s, count=1)
s = s.replace('</body>', '<script src="%sassets/safa.js" defer></script>\n</body>' % root, 1)
open(f, 'w', encoding='utf-8').write(s)
print('restyled', f)
