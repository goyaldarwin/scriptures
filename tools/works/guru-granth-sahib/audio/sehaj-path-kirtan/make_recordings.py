"""recordings.json of Sehaj Path Kirtan (Bhai Parminder Singh, Bhai Jagjit Singh): the whole Granth sung through in 40 tracks.

    python3 tools/works/guru-granth-sahib/audio/sehaj-path-kirtan/make_recordings.py <clone of scriptures-data>

The series' table in scriptures-data (sikhism/gurbani/guru-granth-sahib/printouts/sehaj-path-kirtan/videos.csv) gives each
track's video and number ("Track #n" in its title). A track sings whole parts of the Granth (work.json "parts"), in order:
TRACKS below; Gauri, sung in two tracks, is cut at Ang 250, where its second track begins (its title: Ang 250–346; the first
track's title gives 151–346). The Raag Mala (the last part) is in no track. "dur" is the original's length from its
.meta.json. The tracks must follow one another item after item.
"""
import csv, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
W = json.load(open(os.path.join(REPO, 'library/sikhism/gurbani/guru-granth-sahib/work.json'), encoding='utf-8'))
IT = W['items']; IX = {x['id']: n for n, x in enumerate(IT)}
D = 'sikhism/gurbani/guru-granth-sahib'
# track → the parts it sings (indexes into work.json parts: 0 Jap … 34 Raag Jaijavanti, 35 Salok Sahaskriti … 50 Raag Mala)
TRACKS = {1: (0, 3), **{t: (t + 2, t + 2) for t in range(2, 4)}, 4: (6, 6), 5: (6, 6), **{t: (t + 1, t + 1) for t in range(6, 34)},
          34: (35, 38), 35: (39, 39), 36: (40, 40), 37: (41, 46), 38: (47, 47), 39: (48, 48), 40: (49, 49)}
GAURI_SPLIT = 250

def ang(x):
    m = re.match(r'(\d+)\.', x['id']); return int(m.group(1)) if m else None

def span(t):
    a, b = TRACKS[t]
    idx = [n for n, x in enumerate(IT) if a <= x['p'] <= b]
    if t in (4, 5):   # Gauri: the first item of Ang 250 and on is track 5's
        cut = next(k for k, n in enumerate(idx) if (ang(IT[n]) or 0) >= GAURI_SPLIT)
        idx = idx[:cut] if t == 4 else idx[cut:]
    assert idx == list(range(idx[0], idx[-1] + 1)), t
    return IT[idx[0]]['id'], IT[idx[-1]]['id']

def main(data):
    out = []
    for r in csv.DictReader(open(os.path.join(data, D, 'printouts', 'sehaj-path-kirtan', 'videos.csv'), encoding='utf-8')):
        if r['status'] != 'downloaded': continue
        t = int(re.search(r'Track ?#\s*(\d+)', r['video_title']).group(1)); v = r['video_id']
        meta = json.load(open(os.path.join(data, D, 'audio', 'sehaj-path-kirtan', v + '.opus.meta.json'), encoding='utf-8'))
        a, b = span(t)
        out.append({'yt': v, 'file': r['file'], 'data': f'{D}/audio/sehaj-path-kirtan/{v}.opus', 'dur': meta['original']['duration_s'],
                    'order': t, 'from': a, 'to': b})
    out.sort(key=lambda x: x['order'])
    assert [x['order'] for x in out] == list(range(1, 41)), [x['order'] for x in out]
    assert all(IX[out[k + 1]['from']] == IX[out[k]['to']] + 1 for k in range(len(out) - 1))
    keys = ['yt', 'file', 'data', 'dur', 'order', 'from', 'to']
    open(os.path.join(HERE, 'recordings.json'), 'w', encoding='utf-8').write(
        '[\n' + ',\n'.join(json.dumps({k: x[k] for k in keys}, ensure_ascii=False) for x in out) + '\n]\n')
    print(f'{len(out)} tracks, {IX[out[-1]["to"]] - IX[out[0]["from"]] + 1} items, {sum(x["dur"] for x in out) / 3600:.1f} h')

if __name__ == '__main__': main(sys.argv[1])
