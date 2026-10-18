"""Hand-checked verse starts for the Vande Guru Paramparaam recording, applied to the cached alignment
(transcripts/ZIDdE4SZAuw.align.json) before tools/audio/make_timings.py turns it into timings.

Speech recognition garbled or dropped some lines of the chant (e.g. "सन्नद्धः कवची…", the first line of
śloka 21), so the aligner gave those verses the next line's time. Each start below was read from
transcripts/ZIDdE4SZAuw.jsonl: the segment where the verse's own first words are heard.

python3 tools/works/ramraksha/audio/fix_align.py && python3 tools/audio/make_timings.py tools/works/ramraksha/audio/vande-guru-paramparaam
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'vande-guru-paramparaam', 'transcripts', 'ZIDdE4SZAuw.align.json')
START = {
    'dhyana': 66.5,   # "द्यानं द्याये दाजानु" — the heading ध्यानम् and the verse's first words
    'sh3': 127.0,     # "सासितूण…" inside the 126.0–134.7 segment, before "नक्तंचरान्तकम्"
    'sh4': 143.65,    # "ता वरक्शाम पदेद प्राग्ण्या" = रामरक्षां पठेत्प्राज्ञः
    'sh18': 331.0,    # "…ष्णाजिनाम्बरौ | फलमूलाशिनौ दान्तौ" (328.5–334.45), after śloka 17's last word
    'sh20': 358.0,    # "आत्तसज्जधनुषा…"
    'sh21': 372.6,    # "…गच्छन्मनोरथान्नश्च": the segment holds both lines; the first was not recognised
    'sh29': 508.5,    # "…शरणं भव राम राम | श्रीरामचन्द्र चरणौ" at the end of 503.05–511.6
    'sh38': 667.9,    # after śloka 37 ends ("रामे चित्तलयः…" 661.9–667.9); its second half is at 681.7
}
# In the rows the aligner made, a fixed verse keeps its length (so its neighbours' share of a long
# segment stays right) but is credited to the verse before it, whose start is already set earlier.
IDS = [x['id'] for x in json.load(open(os.path.join(HERE, '..', '..', '..', '..', 'library', 'stotra', 'ramraksha', 'work.json')))['items']]
rows = [r for r in json.load(open(P)) if len(r[2]) and not (len(r[2]) == 1 and r[2][0][0] in START and r[1] - r[0] == 0.5)]
for r in rows: r[2] = [[IDS[IDS.index(i) - 1], n] if i in START else [i, n] for i, n in r[2]]
rows += [[t, t + 0.5, [[i, 1]]] for i, t in START.items()]
json.dump(sorted(rows, key=lambda r: r[0]), open(P, 'w'), ensure_ascii=False)
print('fixed', len(START), 'verse starts')
