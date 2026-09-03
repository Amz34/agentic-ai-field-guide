#!/usr/bin/env python3
# Apply whitening to the ALREADY-SPLICED part_a/part_b (scoped: only added regions)
import re

base = '/home/ubuntu/projects/az-ebook/src/'

# ---- part_a: only inside the appended personalization <style> ----
p = base + 'part_a.html'
s = open(p, encoding='utf-8').read()
m = s.find('/* === AZ personalization + diagrams === */')
assert m >= 0, 'marker not found'
start = m
end = s.find('</style>', start)
assert end > start, 'style close not found'
seg = s[start:end]
repls = [
    ('background:#FCFEFD', 'background:#FFFFFF'),
    ('background:#F4FAF6', 'background:#FFFFFF'),
    ('background:#DDF3E4;border-radius:10px;padding:10px 14px',
     'background:#FFFFFF;border:1px solid #9DC8B2;border-radius:10px;padding:10px 14px'),
    ('border:1px solid #BFE0CC', 'border:1px solid #9DC8B2'),
]
for a, b in repls:
    n = seg.count(a)
    print('css token', repr(a[:34]), 'x', n)
    seg = seg.replace(a, b)
s = s[:start] + seg + s[end:]
open(p, 'w', encoding='utf-8').write(s)
print('part_a css whitened')

# ---- part_b: only inside <figure class="diag"> blocks ----
p = base + 'part_b.html'
s = open(p, encoding='utf-8').read()
fills = {'fill="#F4FAF6"': 'fill="#FFFFFF"', 'fill="#FCFEFD"': 'fill="#FFFFFF"',
         'fill="#DDF3E4"': 'fill="#FFFFFF"', 'fill="#FFF6E0"': 'fill="#FFFFFF"'}

def whiten_fig(mo):
    f = mo.group(0)
    for a, b in fills.items():
        f = f.replace(a, b)
    f = f.replace('stroke="#BFE0CC"', 'stroke="#0E7A46"')
    return f

s2, n = re.subn(r'<figure class="diag">.*?</figure>', whiten_fig, s, flags=re.S)
print('figures processed:', n)
assert n == 3, 'expected 3 figures'
open(p, 'w', encoding='utf-8').write(s2)
print('part_b figures whitened')
