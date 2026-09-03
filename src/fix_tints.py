#!/usr/bin/env python3
# Whiten all pale tinted fills in figure fragments (visual-only, zero layout change)
import io, os

fills = {'fill="#F4FAF6"': 'fill="#FFFFFF"',
         'fill="#FCFEFD"': 'fill="#FFFFFF"',
         'fill="#DDF3E4"': 'fill="#FFFFFF"',
         'fill="#FFF6E0"': 'fill="#FFFFFF"'}

base = '/home/ubuntu/projects/az-ebook/src/'
for fn in ('frag_fig_a.html', 'frag_fig_b.html', 'frag_fig_c.html'):
    p = base + fn
    s = open(p, encoding='utf-8').read()
    for a, b in fills.items():
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)
    print(fn, 'whitened')

# CSS: panels to white bg (keep borders for structure)
p = base + 'frag_css.html'
s = open(p, encoding='utf-8').read()
s = s.replace('figure.diag{margin:20px 0 22px;border:1px solid #BFE0CC;border-radius:14px;background:#FCFEFD;',
              'figure.diag{margin:20px 0 22px;border:1px solid #9DC8B2;border-radius:14px;background:#FFFFFF;')
s = s.replace('.lp3>div{flex:1;border:1px solid #BFE0CC;border-radius:12px;padding:12px 13px 11px;background:#F4FAF6}',
              '.lp3>div{flex:1;border:1px solid #9DC8B2;border-radius:12px;padding:12px 13px 11px;background:#FFFFFF}')
s = s.replace('.lp-links{margin:18px 0 0;border:1.5px solid #0E7A46;border-radius:14px;padding:16px 18px 14px;background:#F4FAF6}',
              '.lp-links{margin:18px 0 0;border:1.5px solid #0E7A46;border-radius:14px;padding:16px 18px 14px;background:#FFFFFF}')
s = s.replace('.lp-note{margin:14px 0 0;font-size:12px;line-height:1.5;color:#4D6255;background:#DDF3E4;border-radius:10px;padding:10px 14px}',
              '.lp-note{margin:14px 0 0;font-size:12px;line-height:1.5;color:#4D6255;background:#FFFFFF;border:1px solid #9DC8B2;border-radius:10px;padding:10px 14px}')
open(p, 'w', encoding='utf-8').write(s)
print('css whitened')

# Band strokes in fig A & C need definition on white: pale-green stroke -> brand green
for fn in ('frag_fig_a.html', 'frag_fig_c.html'):
    p = base + fn
    s = open(p, encoding='utf-8').read()
    n = s.count('stroke="#BFE0CC"')
    s = s.replace('stroke="#BFE0CC"', 'stroke="#0E7A46"')
    open(p, 'w', encoding='utf-8').write(s)
    print(fn, 'band strokes x', n)
