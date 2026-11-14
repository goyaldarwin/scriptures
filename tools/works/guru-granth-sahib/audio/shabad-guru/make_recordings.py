"""recordings.json of the Shabad Guru kirtan source, from the channel's table in scriptures-data.

    python3 tools/works/guru-granth-sahib/audio/shabad-guru/make_recordings.py <clone of scriptures-data>

Reads sikhism/gurbani/guru-granth-sahib/printouts/shabad-guru/videos.csv there: every video downloaded ("status"
downloaded; the "review" and "unmatched" rows are the owner's to decide) is a recording of the item its title matches
("verse_id"), and the items after it that the video sings with it:
  - a salok: the vaar's stanza it opens, its saloks and the pauri after them (509.2 → 509.4, fixes.md);
  - a pauri: the bani of pauris it opens, to the pauri whose closing number ends the composition (॥੪੦॥੧॥), else to the end
    of its topic in the work (the Bavan Akhri);
  - the Mool Mantar: the whole Japji (to its closing salok);
  - a shabad or pad: itself.
A video that sings more after its verses is found by mms_merge.py ("beyond") and its track ended by hand ("end", with the
evidence in fixes.md), kept here in END. The order is the Granth's (a verse's videos by video id). "dur" is the original's
length from its .meta.json.
"""
import bisect, csv, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
END = {'uEFQLir74Fo': 147.0}          # fixes.md
CLOSE = re.compile(r'॥\s*[੦-੯]+\s*॥\s*[੦-੯]+\s*॥(\s*[੦-੯]+\s*॥)*\s*(ਸੁਧੁ\s*)?$')
W = json.load(open(os.path.join(REPO, 'library/sikhism/gurbani/guru-granth-sahib/work.json')))
IT = W['items']; IX = {x['id']: n for n, x in enumerate(IT)}
TOP = sorted(IX[t['id']] for t in W['topics'] if t['id'] in IX)

def span(v, typ):
    if v == 'mool': return 'salok.close'
    n = IX[v]
    if typ == 'salok':
        m = n
        while m + 1 < len(IT) and IT[m + 1]['y'] in ('salok', 'pauri'):
            m += 1
            if IT[m]['y'] == 'pauri': return IT[m]['id']
        return v
    if typ == 'pauri':
        m = n
        while not CLOSE.search(IT[m]['v'][-1]) and m + 1 < len(IT) and IT[m + 1]['y'] in ('pauri', 'rahao', 'salok'): m += 1
        if CLOSE.search(IT[m]['v'][-1]): return IT[m]['id']
        k = bisect.bisect_right(TOP, n) - 1
        if TOP[k] == n and k + 1 < len(TOP): return IT[TOP[k + 1] - 1]['id']
        return IT[m]['id']
    return v

def main(data):
    D = os.path.join(data, 'sikhism/gurbani/guru-granth-sahib')
    rows = [r for r in csv.DictReader(open(os.path.join(D, 'printouts/shabad-guru/videos.csv'))) if r['status'] == 'downloaded']
    out = []
    for r in rows:
        v = r['video_id']; mp = os.path.join(D, 'audio/shabad-guru', v + '.opus.meta.json')
        dur = json.load(open(mp))['original']['duration_s'] if os.path.exists(mp) else float(r['duration_s'])
        rec = {'yt': v, 'file': r['file'], 'data': f'sikhism/gurbani/guru-granth-sahib/audio/shabad-guru/{v}.opus', 'dur': dur,
               'from': r['verse_id'], 'to': span(r['verse_id'], r['verse_type'])}
        if v in END: rec['end'] = END[v]
        out.append(rec)
    out.sort(key=lambda x: (IX[x['from']], x['yt']))
    for n, x in enumerate(out, 1): x['order'] = n
    keys = ['yt', 'file', 'data', 'dur', 'order', 'from', 'to', 'end']
    p = os.path.join(HERE, 'recordings.json')
    open(p, 'w').write('[\n' + ',\n'.join(json.dumps({k: x[k] for k in keys if k in x}, ensure_ascii=False) for x in out) + '\n]\n')
    print(len(out), 'recordings;', sum(1 for x in out if x['to'] != x['from']), 'sing more than one item')

if __name__ == '__main__': main(sys.argv[1])
