"""Build the SAFA Student Pilot Permit study site (static, phone-first).
src/   = page files exactly as served by the Apps Script web app (from Drive)
site/  = hand-written shell files (spp-local.js, spp-local.css, index.html, icons)
dist/  = what gets published
"""
import json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import overview
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, SITE, DIST = (os.path.join(ROOT, d) for d in ('src', 'site', 'dist'))

def course(fn):
    s = open(os.path.join(SRC, fn), encoding='utf-8').read()
    return json.loads(re.search(r'const COURSE = (\{.*?\});\n', s, re.S).group(1))

KIDS = [('title', 'Overview'), ('notes', 'Cornell Notes'), ('cards', 'Flashcards'), ('quiz', 'Practice Quizzes'), ('lab', 'Skills Lab')]
def part(pid, n, title):
    return {'id': f'{pid}-title', 'file': f'{pid}-title.html', 'label': f'Part {n} · {title}', 'hubLabel': 'Overview',
            'alias': [f'{pid}'],
            'kids': [{'id': f'{pid}-{k}', 'file': f'{pid}-{k}.html', 'label': lab} for k, lab in KIDS[1:]]}

roca, pstar = course('roca.html'), course('pstar.html')
NAV = [
    {'id': 'index', 'file': 'index.html', 'label': 'Start here'},
    {'id': 'roca', 'file': 'roca.html', 'label': 'ROC-A (Radio)', 'hubLabel': 'ROC-A home · my progress', 'alias': ['spp-roca'],
     'kids': [part(u['pid'], u['part'], u['title']) for u in roca['units']] + [
         {'id': 'roca-mock', 'file': 'roca-mock.html', 'label': 'Mock Exams'},
         {'id': 'oral', 'file': 'oral.html', 'label': 'Oral Trainer'}]},
    {'id': 'pstar', 'file': 'pstar.html', 'label': 'PSTAR (Air Regulations)', 'hubLabel': 'PSTAR home · my progress', 'alias': ['spp-pstar'],
     'kids': [part(u['pid'], u['part'], u['title']) for u in pstar['units']] + [
         {'id': 'pstar-mock', 'file': 'pstar-mock.html', 'label': 'Mock Exams'}]},
    {'id': 'spp-glossary', 'file': 'spp-glossary.html', 'label': 'Glossary', 'alias': ['glossary']},
    {'id': 'c172', 'label': 'C172 Exam', 'soon': True},
    {'id': 'policy', 'label': 'Policy & Procedures', 'soon': True},
]
CONFIG = {'rocaPass': 70, 'rocaQs': 25, 'pstarPass': 90, 'pstarQs': 50}

def files(nodes):
    for n in nodes:
        if n.get('file'): yield n['file']
        yield from files(n.get('kids', []))

HEAD_TOP = '<script src="spp-local.js"></script>'
HEAD_END = ('<link rel="stylesheet" href="spp-local.css">\n'
            '<meta name="robots" content="noindex, nofollow">\n'
            '<meta name="theme-color" content="#000000">\n'
            '<link rel="manifest" href="manifest.webmanifest">\n'
            '<link rel="icon" href="icon-192.png">\n'
            '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n')

def process(html, name):
    if 'name="viewport"' not in html:
        html = html.replace('<head>', '<head>\n<meta name="viewport" content="width=device-width, initial-scale=1">', 1)
    # engine must run before any page script
    m = re.search(r'<meta charset="[^"]*">', html)
    html = (html[:m.end()] + '\n' + HEAD_TOP + html[m.end():]) if m else html.replace('<head>', '<head>\n' + HEAD_TOP, 1)
    html = html.replace('</head>', HEAD_END + '</head>', 1)
    for a, b in [("'Not signed in'", "'Progress saved on this device'"),
                 ('Only your score is saved for your teacher', 'Your score saves on this device only'),
                 ('Progress saves automatically and is shared with your teacher', 'Progress saves automatically on this device')]:
        html = html.replace(a, b)
    return html

def main():
    os.makedirs(DIST, exist_ok=True)
    for f in os.listdir(DIST):
        fp = os.path.join(DIST, f)
        shutil.rmtree(fp) if os.path.isdir(fp) else os.remove(fp)
    missing, generated = [], []
    for fn in files(NAV):
        if fn == 'index.html': continue
        p = os.path.join(SRC, fn)
        if os.path.exists(p):
            out = process(open(p, encoding='utf-8').read(), fn)
        elif fn.endswith('-title.html'):
            exam, hub, pct, units = ('ROC-A', 'roca.html', CONFIG['rocaPass'], roca['units']) if fn.startswith('roca') else ('PSTAR', 'pstar.html', CONFIG['pstarPass'], pstar['units'])
            i = [u['pid'] for u in units].index(fn[:-len('-title.html')])
            out = process(overview.page(exam, hub, pct, units, i), fn)
            generated.append(fn)
        else:
            missing.append(fn); continue
        open(os.path.join(DIST, fn), 'w', encoding='utf-8').write(out)
    for fn in os.listdir(SITE):
        src = os.path.join(SITE, fn)
        if fn == 'spp-local.js':
            js = ('window.SPP_NAV = ' + json.dumps(NAV, ensure_ascii=False) + ';\n'
                  'window.SPP_SITE = ' + json.dumps({'config': CONFIG}) + ';\n' + open(src, encoding='utf-8').read())
            open(os.path.join(DIST, fn), 'w', encoding='utf-8').write(js)
        elif fn == 'index.html':
            open(os.path.join(DIST, fn), 'w', encoding='utf-8').write(process(open(src, encoding='utf-8').read(), fn))
        else:
            shutil.copy(src, os.path.join(DIST, fn))
    open(os.path.join(DIST, '.nojekyll'), 'w').close()
    print('pages:', len(list(files(NAV))), 'generated:', generated, 'missing:', missing)
    return missing

if __name__ == '__main__':
    sys.exit(1 if main() else 0)
