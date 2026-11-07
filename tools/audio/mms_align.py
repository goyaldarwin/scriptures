"""Exact verse starts and ends with Meta's MMS forced aligner (tools/audio/METHOD.md, steps 2–3), one recording at a time.

    ONLY=<video id> DATA_DIR=<clone of scriptures-data> python3 tools/audio/mms_align.py tools/works/<work>/audio/<source>
        → <source>/mms/<video id>.json   {item id: [start, end, score]}   (seconds in the recording; score 0–1)

Runs in the `align` workflow (free in this public repository); needs ffmpeg and the CPU build of torch/torchaudio 2.8.
Reads the windows of mms_windows.py. In each window MMS (torchaudio MMS_FA, weights from dl.fbaipublicfiles.com) is given the
verses' plain-letter text with a wildcard (*) between every two verses and at both ends, so a refrain, a pause or an
announcement that is not in the text falls into a wildcard. A verse's start is its first letter's, its end its last
letter's; its score is the mean score of its letters. Emissions are made in 30-s pieces with 2 s of context each side
(the model's attention grows with the square of the length). The raw starts are kept here; their lean against the
owner's by-ear starts is removed when they are merged (mms_merge.py). The audio is only read.
"""
import json, os, subprocess, sys, time
import numpy as np
SR = 16000

def load(path, a, b):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-to', str(b), '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()

def main(src):
    import torch, torchaudio
    vid = os.environ['ONLY']
    rec = [r for r in json.load(open(os.path.join(src, 'recordings.json'))) if r['yt'] == vid][0]
    audio = os.path.join(os.environ.get('DATA_DIR', '.'), rec['data'])
    wins = [w for w in json.load(open(os.path.join(src, 'mms', 'windows.json'), encoding='utf-8')) if w['yt'] == vid]
    out_p = os.path.join(src, 'mms', vid + '.json')
    res = json.load(open(out_p)) if os.path.exists(out_p) else {}     # a run cut short goes on where it stopped
    bundle = torchaudio.pipelines.MMS_FA
    model = bundle.get_model(with_star=True).eval()
    D, aligner = bundle.get_dict(star='*'), bundle.get_aligner()
    torch.set_num_threads(int(os.environ.get('THREADS', '4')))
    t_all = time.time()
    for n, w in enumerate(wins):
        if all(k in res for k in w['keep']): continue
        t0 = time.time()
        x = torch.from_numpy(load(audio, w['a'], w['b']))[None]
        step, ctx, ems = 30 * SR, 2 * SR, []
        with torch.inference_mode():
            for s in range(0, x.shape[1], step):
                lo, hi = max(0, s - ctx), min(x.shape[1], s + step + ctx)
                e, _ = model(x[:, lo:hi])
                fr = e.shape[1] / (hi - lo)
                ems.append(e[:, int(round((s - lo) * fr)):int(round((min(s + step, x.shape[1]) - lo) * fr))])
        em = torch.cat(ems, 1); sec = (x.shape[1] / SR) / em.shape[1]
        words, owner = ['*'], [None]
        for k, l in enumerate(w['lines']):
            for wd in l['rom'].split(): words.append(wd); owner.append(k)
            words.append('*'); owner.append(None)
        try: spans = aligner(em[0], [[D[c] for c in wd] for wd in words])
        except Exception as e:   # audio shorter than the text (a window cut at the recording's end): left to the transcript
            print(vid, 'window', n, 'not aligned:', e, flush=True); continue
        for k, l in enumerate(w['lines']):
            if l['id'] not in w['keep']: continue
            sp = [spans[j] for j in range(len(words)) if owner[j] == k]
            if not sp: continue
            res[l['id']] = [round(w['a'] + sp[0][0].start * sec, 2), round(w['a'] + sp[-1][-1].end * sec, 2), round(float(np.mean([t.score for s in sp for t in s])), 3)]
        if n % 10 == 0 or n == len(wins) - 1:
            json.dump(res, open(out_p, 'w'), ensure_ascii=False, separators=(',', ':'))
            print(vid, f'window {n + 1}/{len(wins)}', round(time.time() - t0, 1), 's;', round((time.time() - t_all) / 60, 1), 'min in all', flush=True)
    json.dump(res, open(out_p, 'w'), ensure_ascii=False, separators=(',', ':'))
    print(vid, len(res), 'verses aligned', flush=True)

if __name__ == '__main__': main(os.path.abspath(sys.argv[1]))
