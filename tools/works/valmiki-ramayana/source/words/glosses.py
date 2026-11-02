"""Every word-by-word gloss the two witnesses give for a verse and the verses either side of it, from the
verse_glosses.json that packets.py writes beside its batches:

    python3 glosses.py <packets dir>/verse_glosses.json <verse id> [<verse id> …]
"""
import json, sys
G = json.load(open(sys.argv[1]))
for i in sys.argv[2:]:
    g = G.get(i, {})
    print(f'== {i}')
    for w in ('iitk', 'vr'):
        print(f'  [{w}]')
        for sa, en in g.get(w, []):
            print(f'    {sa} = {en}')
