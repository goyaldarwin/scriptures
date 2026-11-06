"""Gita Press's Hindi paragraphs (hindi/decode.py → hi_book.json) under the verses of the settled text.

A paragraph's mark is a certain boundary only when it is a whole number (॥ २२ ॥, ॥ ३-४ ॥) higher than the last
boundary and within the sarga, or when it ends the sarga. A ½ mark (॥ २० १/२ ॥: the translation runs into the next
verse) or a bare ॥ (the book prints no number) is not. Between two boundaries: if every paragraph is a bare one
covering exactly one verse in order, each goes under its verse; otherwise the paragraphs form one joint meaning
under the last verse, with every mark kept as printed between them.
"""
import json, re, sys

def mark_text(p):
    return p['mark'] if p['mark'] else '॥'

def map_hindi(H, items):
    last = {}
    for i in items:
        last[i['s']] = int(i['n'])
    m, notes, stats = {}, {}, {'single': 0, 'joint': 0, 'bare_single': 0}
    for k in H:
        reg = pr = 0
        for s in k['sargas']:
            if 'प्रक्षिप्त' in s['heading']:
                pr += 1; key = f"{k['kanda']}.p{pr}"
            else:
                reg += 1; key = f"{k['kanda']}.{reg}"
            end = last[key]
            prev, group = 0, []
            paras = s['paras']
            for idx, p in enumerate(paras):
                group.append(p)
                certain = (p['mark'] and p['mark'] != '॥' and not p.get('half') and prev < p['to'] <= end
                           and not p.get('inferred'))
                if idx == len(paras) - 1:
                    certain, p_to = True, end
                else:
                    p_to = p['to']
                if not certain:
                    continue
                n_verses = p_to - prev
                bare = [g for g in group[:-1]]
                if len(group) == n_verses and all((not g['mark'] or g['mark'] == '॥') and not g.get('half') for g in bare) \
                        and (len(group) == 1 or True):
                    for j, g in enumerate(group):
                        vid = f"{key}.{prev + 1 + j}"
                        m[vid] = (g['text'].strip() + ' ' + mark_text(g)).strip()
                        if g.get('notes'): notes[vid] = g['notes']
                        stats['single' if j == len(group) - 1 and g['mark'] not in ('', '॥') else 'bare_single'] += 1
                else:
                    vid = f"{key}.{p_to}"
                    m[vid] = ' '.join((g['text'].strip() + ' ' + mark_text(g)).strip() for g in group)
                    ns = [n for g in group for n in (g.get('notes') or [])]
                    if ns: notes[vid] = ns
                    stats['joint'] += 1
                prev, group = p_to, []
    return m, notes, stats

if __name__ == '__main__':
    H = json.load(open(sys.argv[1])); items = json.load(open(sys.argv[2]))['items']
    ids = {i['id'] for i in items}
    m, notes, stats = map_hindi(H, items)
    bad = [k for k in m if k not in ids]
    print(stats, len(m), 'meanings,', len(notes), 'with notes; ids not in the text:', bad[:10])
    json.dump({'m': m, 'notes': notes}, open(sys.argv[3], 'w'), ensure_ascii=False)
