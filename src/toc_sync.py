#!/usr/bin/env python3
# Sync TOC page numbers to actual section pages
import re
p = '/home/ubuntu/projects/az-ebook/src/part_b.html'
h = open(p, encoding='utf-8').read()
mp = {'Introduction': 3, 'The real challenge': 6, 'An open platform approach': 11,
      'Charting your agentic': 18, 'Reference architecture': 16, 'Glossary & sources': 24}
row = re.compile(r'<li><span class="n">([^<]+)</span><span class="t">([^<]*)<span class="d">.*?</span></span><span class="pg">(\d+)</span></li>', re.S)
def fix(m):
    title = m.group(2).strip().replace('&amp;', '&')
    for k, v in mp.items():
        if k.lower() in title.lower():
            return m.group(0).replace(f'<span class="pg">{m.group(3)}</span>', f'<span class="pg">{v:02d}</span>')
    print('UNMAPPED ROW:', m.group(1), title)
    return m.group(0)
h2, n = row.subn(fix, h)
open(p, 'w', encoding='utf-8').write(h2)
print('toc rows updated:', n)
