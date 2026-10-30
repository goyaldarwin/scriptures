"""Merge written and reviewed batches (tools/meanings/prepare.py → writers → reviewers) into a work's meaning files.

    python3 tools/meanings/apply_batches.py BATCH_DIR [--work manas] [--doubts docs/reviews/<work>-doubts.jsonl]
            (--work: the work's id, its folder in tools/works)

For every batch-NN.ids in BATCH_DIR: takes the writer's batch-NN.hi.json / .en.json / .topics.json, then applies the
reviewer's fixes from batch-NN.review.jsonl (lines with lang "hi", "en" or "topic" and a "fix"; the reviewer's fix
wins, as the second reader's). A meaning is a string or, line by line, a list with one piece per verse line; a fix with
"line" (0-based) replaces that one piece. Checks that each batch covers exactly its ids, both languages, no empty value and no
verse number. Writes into the work's folder, in its reading order:
  meanings/hi/scriptures.json, meanings/en/scriptures.json   our meanings (other entries and the settings are kept)
  topics.json                                                our topic headings {first verse id: {hi, en}}
Appends the writers' doubts (with the reviewer's comments on them) to --doubts, and gathers every word-meaning issue
(writer's .words.jsonl and reviewer's "word" lines) into BATCH_DIR/words-to-settle.jsonl for the dictionary step.
"""
import argparse, glob, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, 'tools')); import jsonio
NUM = re.compile(r'(?:।।|॥)\s*[०-९0-9]|\(\d+\)\s*$')

def jl(p): return [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()] if os.path.exists(p) else []

def dump_map(p, d):
    with open(p, 'w', encoding='utf-8') as f:
        f.write('{\n' + ',\n'.join(json.dumps(k, ensure_ascii=False) + ': ' + json.dumps(v, ensure_ascii=False) for k, v in d.items()) + '\n}\n')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dir'); ap.add_argument('--work', default='manas')
    ap.add_argument('--doubts')
    a = ap.parse_args()
    folder = os.path.join(REPO, 'tools', 'works', a.work)
    path = json.load(open(os.path.join(folder, 'work.json'), encoding='utf-8'))['path']
    W = json.load(open(os.path.join(REPO, 'library', path, 'work.json'), encoding='utf-8'))
    order = [x['id'] for x in W['items']]
    mine = lambda lg: os.path.join(folder, 'meanings', lg, 'scriptures.json')
    F = {lg: json.load(open(mine(lg), encoding='utf-8')) for lg in ('hi', 'en')}
    D = {lg: F[lg].setdefault('m', {}) for lg in ('hi', 'en')}
    tp = os.path.join(folder, 'topics.json')
    T = json.load(open(tp, encoding='utf-8')) if os.path.exists(tp) else {}
    doubts, words, fixed = [], [], {'hi': 0, 'en': 0, 'topic': 0}
    for idf in sorted(glob.glob(os.path.join(a.dir, 'batch-*.ids'))):
        b = idf[:-4]; ids = [l.strip() for l in open(idf) if l.strip()]
        M = {lg: json.load(open(f'{b}.{lg}.json', encoding='utf-8')) for lg in ('hi', 'en')}
        top = json.load(open(f'{b}.topics.json', encoding='utf-8')) if os.path.exists(f'{b}.topics.json') else {}
        rev = jl(f'{b}.review.jsonl')
        assert rev or os.path.exists(f'{b}.review.jsonl'), f'{b}: not reviewed yet'
        for r in rev:
            if r.get('lang') in ('hi', 'en') and r.get('fix') is not None:
                assert r['id'] in M[r['lang']], f"{b}: review fix for unknown id {r['id']}"
                cur = M[r['lang']][r['id']]
                if isinstance(cur, list) and r.get('line') is not None:   # line by line: the fix is one line's piece
                    assert 0 <= int(r['line']) < len(cur), f"{b}: review fix for {r['id']} line {r['line']} out of range"
                    cur[int(r['line'])] = r['fix'].strip()
                elif isinstance(r['fix'], list): M[r['lang']][r['id']] = [x.strip() for x in r['fix']]
                else: M[r['lang']][r['id']] = r['fix'].strip()
                fixed[r['lang']] += 1
            elif r.get('lang') == 'topic' and r.get('fix'):
                fx = r['fix']
                if isinstance(fx, str):   # a Hindi heading, or "hi | en"
                    h, _, e = fx.partition(' | ') if ' | ' in fx else (fx, '', '')
                    fx = {'hi': h.strip(), 'en': e.strip() or top.get(r['id'], {}).get('en', '')}
                top[r['id']] = {**top.get(r['id'], {}), **{k: v for k, v in fx.items() if v}}; fixed['topic'] += 1
            elif r.get('lang') == 'word':
                words.append({'source': 'review', 'batch': os.path.basename(b), **r})
            elif r.get('lang') == 'doubt':
                doubts.append({'review': r.get('problem'), 'id': r.get('id'), 'reviewer_fix': r.get('fix')})
        for lg in ('hi', 'en'):
            assert list(M[lg]) == ids, f'{b}.{lg}: ids differ from the batch'
            NL = {x['id']: len(x['v']) for x in W['items']}
            for i, t in M[lg].items():
                # a meaning is a string, or (line by line, owner 2026-10-23) one piece per verse line, "" where a line has none
                ps = t if isinstance(t, list) else [t]
                assert any(p and p.strip() for p in ps), f'{b}.{lg}: empty {i}'
                assert not isinstance(t, list) or len(t) == NL[i], f'{b}.{lg}: {i} has {len(t)} pieces for {NL[i]} verse lines'
                assert not any(NUM.search(p) for p in ps), f'{b}.{lg}: verse number in {i}'
            for i in ids:
                h, e = M['hi'].get(i), M['en'].get(i)
                if lg == 'en' and isinstance(h, list) and isinstance(e, list):
                    assert [not p.strip() for p in h] == [not p.strip() for p in e], f'{b}: {i}: Hindi and English must cut at the same lines'
            D[lg].update(M[lg])
        T.update(top)
        doubts += [dict(d, batch=os.path.basename(b)) for d in jl(f'{b}.doubts.jsonl')]
        words += [{'source': 'writer', 'batch': os.path.basename(b), **w} for w in jl(f'{b}.words.jsonl')]
    for lg in ('hi', 'en'):
        F[lg]['m'] = {i: D[lg][i] for i in order if i in D[lg]}
        jsonio.dump_meanings(mine(lg), F[lg])
    T = {i: T[i] for i in order if i in T}; dump_map(tp, T)
    if a.doubts:
        with open(os.path.join(REPO, a.doubts), 'a', encoding='utf-8') as f:
            for d in doubts: f.write(json.dumps(d, ensure_ascii=False) + '\n')
    with open(os.path.join(a.dir, 'words-to-settle.jsonl'), 'w', encoding='utf-8') as f:
        for w in words: f.write(json.dumps(w, ensure_ascii=False) + '\n')
    print(f"{len(D['hi'])} verses in our Hindi and English; review fixes applied {fixed}; {len(T)} topic headings; "
          f'{len(doubts)} doubts; {len(words)} word issues to settle')

if __name__ == '__main__':
    main()
