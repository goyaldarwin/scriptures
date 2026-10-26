"""Checks a store listing file (docs/store/*-listing.md) against Google Play's limits: name ≤ 30, short ≤ 80,
full description ≤ 4000 characters.  python3 tools/store/check_listing.py docs/store/hinduism-listing.md"""
import re, sys
s = open(sys.argv[1], encoding='utf-8').read(); ok = True
for lang in re.split(r'\n## ', s)[1:]:
    head = lang.split('\n', 1)[0]
    for sec, lim in (('App name', 30), ('Short description', 80), ('Full description', 4000)):
        m = re.search(r'### ' + sec + r'\n(.*?)(?=\n### |\n## |\Z)', lang, re.S)
        if not m: continue
        n = len(m.group(1).strip()); bad = n > lim; ok &= not bad
        print(f'{head[:28]:28} {sec:18} {n:5} / {lim}' + ('  TOO LONG' if bad else ''))
sys.exit(0 if ok else 1)
