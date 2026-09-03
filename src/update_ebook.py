#!/usr/bin/env python3
# Splice personalization fragments into part_a / part_b
import re, sys

def load(p):
    return open(p, encoding='utf-8').read()

A = load('/home/ubuntu/projects/az-ebook/src/part_a.html')
B = load('/home/ubuntu/projects/az-ebook/src/part_b.html')
css  = load('/home/ubuntu/projects/az-ebook/src/frag_css.html')
fa   = load('/home/ubuntu/projects/az-ebook/src/frag_fig_a.html')
fb   = load('/home/ubuntu/projects/az-ebook/src/frag_fig_b.html')
fc   = load('/home/ubuntu/projects/az-ebook/src/frag_fig_c.html')
lp   = load('/home/ubuntu/projects/az-ebook/src/frag_lastpage.html')

report = []

# ---------- part_a (idempotent: skip if already spliced) ----------
if 'frag personalization CSS' not in A:
    # 1) extra CSS before </head>
    n = A.count('</head>')
    assert n == 1, f'</head> count {n}'
    A = A.replace('</head>', css + '\n</head>', 1)
    report.append('css inserted')

    # 2) footer element right after <div class="sheet">
    m = re.search(r'<div class="sheet">', A)
    assert m, 'sheet open not found'
    foot = '\n<div class="pgfoot">Aamir Zameer &nbsp;·&nbsp; AZ Engineering &nbsp;·&nbsp; Field Guide 2026</div>'
    A = A[:m.end()] + foot + A[m.end():]
    report.append('footer added')

    # 3) cover-meta Author row (first row)
    m = re.search(r'<div class="cover-meta">', A)
    assert m, 'cover-meta not found'
    row = '\n  <div><b>Author</b><span>Aamir Zameer — AZ Engineering</span></div>'
    A = A[:m.end()] + row + A[m.end():]
    report.append('cover author row added')
else:
    report.append('part_a already spliced — untouched')

# marker comment appended into css block for idempotency check
if 'frag personalization CSS' not in A:
    A = A.replace(css, css.replace('<style>', '<style>\n<!-- frag personalization CSS -->'), 1)

open('/home/ubuntu/projects/az-ebook/src/part_a.html', 'w', encoding='utf-8').write(A)

# ---------- part_b ----------
edits = []  # (insert_pos, text)

# Fig A: after the "One structural point matters" note paragraph in the intro
pat_small = re.compile(r'<p class="small"[^>]*>\s*One structural point.*?</p>', re.S)
m = pat_small.search(B)
if m:
    edits.append((m.end(), '\n' + fa))
    report.append('fig A after "One structural point" para')
else:
    # fallback: after the first paragraph following the intro agentic-flow heading
    mh = re.search(r'<h[23][^>]*>[^<]*[Hh]ow agentic[^<]*</h[23]>', B)
    assert mh, 'fig A anchors missing'
    mend = B.find('</p>', mh.end())
    assert mend != -1, 'no para after fig A heading'
    edits.append((mend + 4, '\n' + fa))
    report.append('fig A fallback after heading para')

# Fig B: in chapter 1 zone, after the paragraph whose lead strong mentions orchestration
zh = re.search(r'<h1[^>]*>The real challenge</h1>', B)
assert zh, 'ch1 heading missing'
suffix = B[zh.end():]
p_orch = re.compile(r'<p><strong>[^<]*[Oo]rchestrat[^<]*</strong>.*?</p>', re.S)
mm = p_orch.search(suffix)
if mm:
    edits.append((zh.end() + mm.end(), '\n' + fb))
    report.append('fig B after orchestration para')
else:
    mfirst = re.search(r'<p>.*?</p>', suffix, re.S)
    assert mfirst, 'no ch1 para for fig B'
    edits.append((zh.end() + mfirst.end(), '\n' + fb))
    report.append('fig B fallback after ch1 first para')

# Fig C: after the "Route by sensitivity and difficulty" paragraph (challenge 3)
p_route = re.compile(r'<p><strong>Route by sensitivity and difficulty\.</strong>.*?</p>', re.S)
mroute = p_route.search(B)
if mroute:
    edits.append((mroute.end(), '\n' + fc))
    report.append('fig C after routing para')
else:
    p_sens = re.compile(r'<p><strong>[^<]*[Ss]ensitivity[^<]*</strong>.*?</p>', re.S)
    ms = p_sens.search(B)
    if ms:
        edits.append((ms.end(), '\n' + fc))
        report.append('fig C fallback after sensitivity para')
    else:
        mcost = re.search(r'<p><strong>Route by sensitivity', B)
        assert mcost, 'fig C anchors missing'
        edits.append((mcost.end(), '\n' + fc))
        report.append('fig C minimal anchor')

# Last page: insert just before the sheet-closing comment
tail = re.search(r'</div><!-- /sheet -->', B)
assert tail, 'sheet close comment not found'
edits.append((tail.start(), '\n' + lp))
report.append('last page added')

# apply edits from last to first so offsets stay valid
for pos, txt in sorted(edits, key=lambda e: -e[0]):
    B = B[:pos] + txt + B[pos:]

open('/home/ubuntu/projects/az-ebook/src/part_b.html', 'w', encoding='utf-8').write(B)
print('OK — ' + ' | '.join(report))
