"""The Granth's kirtan beside Shabad Guru's: the recordings of the other channels, from their tables in scriptures-data.

The Granth has one kirtan source (shabad-guru/, "Kirtan"), every singer's recordings in it; shabad-guru/make_recordings.py
adds these (others) to Shabad Guru's in its recordings.json. The channels, each for items Shabad Guru has no kirtan of:
  - Har Ki Oat, Gurmat Sangeet Darbar: one item per video. Each video downloaded in the channel's table
    (sikhism/gurbani/guru-granth-sahib/printouts/<source>/videos.csv in scriptures-data, "status" downloaded) sings the item
    its title matches ("verse_id") and only that item: a shabad, or a single salok or pauri sung as a shabad (a pauri of the
    Sukhmani, a salok of a vaar), so "from" and "to" are that item. A video that sings more is found by mms_merge.py
    ("beyond"), one that sings another item by its "title" flag.
  - Sehaj Path Kirtan: seven long tracks, each a whole bani or run of banis of Ang 1353-1429 sung through (SPK below: the
    first and last item of each, at the headings of the banis the video title names). The Raag Mala (1429.13) is in none.
"dur" is the original's length from its .meta.json.
"""
import csv, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
W = json.load(open(os.path.join(REPO, 'library/sikhism/gurbani/guru-granth-sahib/work.json'), encoding='utf-8'))
IT = W['items']; IX = {x['id']: n for n, x in enumerate(IT)}
D = 'sikhism/gurbani/guru-granth-sahib'
# Sehaj Path Kirtan's tracks: video id → (first item, last item); each track starts at the heading of the bani its title names
SPK = {
    'n7URwrfz4Rk': ('1353.1', '1364.9'),    # Track 34: Salok Sahaskriti M1 and M5, Gatha, Phunhe, Chaubole (Ang 1353-1364)
    'a5b1rLmEhCA': ('1364.10', '1377.12'),  # Track 35: Salok Bhagat Kabir (1364-1377)
    '9D8RHUl1o3s': ('1377.13', '1384.19'),  # Track 36: Salok Sheikh Farid (1377-1384)
    'VOHKq_zLdls': ('1385.1', '1409.6'),    # Track 37: the Savaiye (1385-1409)
    '7SQfAZdZMUA': ('1410.1', '1426.7'),    # Track 38: Salok Varan te Vadheek (1410-1426)
    'f49qLLK8mPE': ('1426.8', '1429.10'),   # Track 39: Salok Mahalla 9 (1426-1429)
    '3U383GeE7Fw': ('1429.11', '1429.12'),  # Track 40: Mundavani and Salok Mahalla 5 (1429)
}

def dur(data, src, v, fallback):
    mp = os.path.join(data, D, 'audio', src, v + '.opus.meta.json')
    return json.load(open(mp, encoding='utf-8'))['original']['duration_s'] if os.path.exists(mp) else float(fallback)

def others(data):
    """The other channels' recordings (yt, file, data, dur, from, to), in no order."""
    res = []
    for src in ('har-ki-oat', 'gurmat-sangeet-darbar'):
        out = []
        for r in csv.DictReader(open(os.path.join(data, D, 'printouts', src, 'videos.csv'), encoding='utf-8')):
            if r['status'] != 'downloaded': continue
            v = r['video_id']; assert r['verse_id'] in IX, (src, v, r['verse_id'])
            out.append({'yt': v, 'file': r['file'], 'data': f'{D}/audio/{src}/{v}.opus', 'dur': dur(data, src, v, r['duration_s']),
                        'from': r['verse_id'], 'to': r['verse_id']})
        res += out
    out = []
    for r in csv.DictReader(open(os.path.join(data, D, 'printouts', 'sehaj-path-kirtan', 'videos.csv'), encoding='utf-8')):
        if r['status'] != 'downloaded': continue
        v = r['video_id']; a, b = SPK[v]; assert IX[a] <= IX[b]
        out.append({'yt': v, 'file': r['file'], 'data': f'{D}/audio/sehaj-path-kirtan/{v}.opus',
                    'dur': dur(data, 'sehaj-path-kirtan', v, r['duration_s']), 'from': a, 'to': b})
    assert len(out) == len(SPK)
    s = sorted(out, key=lambda x: IX[x['from']])   # the tracks follow one another, item after item
    assert all(IX[s[k + 1]['from']] == IX[s[k]['to']] + 1 for k in range(len(s) - 1))
    return res + out
