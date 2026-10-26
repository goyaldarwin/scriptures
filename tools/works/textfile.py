"""The verse text of a work, tools/works/<work>/text.txt: one format for every work (tools/works/README.md).

    # a comment
    @part <key>                    the part the following verses belong to (a key of work.json → parts.list)
    @section <id>                  the section (page) the following verses belong to
    @lang <code>                   the language of the following verses (from the start: the work's language)
    @topic <hindi> | <english>     a topic heading that starts at the next verse
    [<id> <type> <number>]         a verse (the number is left out when the verse has none) …
    <line>                         … and its lines, one per line
    [take <work> <id>]             a verse of another work, unchanged; it joins this text's part and section
    [take <work> <id> .. <id>]     a run of another work's verses, with their sections and topics; it joins this text's part

write() makes the file from verses; source scripts use it, so a text made from a book or a PDF reads like a typed one.
"""
import re

HEAD = re.compile(r'\[(?P<id>[^\s\]]+) (?P<y>[a-z0-9_]+)(?: (?P<n>[^\s\]]+))?\]')
TAKE = re.compile(r'\[take (?P<w>[a-z0-9-]+) (?P<a>[^\s\]]+)(?: \.\. (?P<b>[^\s\]]+))?\]')

def write(path, items, topics, part_keys, lang, header):
    """items: [{id, p, s, y, n, v, l?}] in order; topics: [{id, hi, en}]; part_keys: the key of each part by index;
    lang: the work's language; header: comment lines at the top (the file's source and how it is made)."""
    T = {t['id']: t for t in topics}
    out = ['# ' + h if h else '#' for h in header]
    part = sec = None; cur = lang
    for x in items:
        if x['p'] != part: part = x['p']; out += ['', f'@part {part_keys[part]}']
        if x['s'] != sec: sec = x['s']; out.append(f'@section {sec}')
        l = x.get('l', lang)
        if l != cur: cur = l; out.append(f'@lang {l}')
        if x['id'] in T: out.append(f"@topic {T[x['id']]['hi']} | {T[x['id']]['en']}")
        out.append(f"[{x['id']} {x['y']}{' ' + x['n'] if x.get('n') else ''}]")
        out += x['v']
    open(path, 'w', encoding='utf-8').write('\n'.join(out) + '\n')

def read(path):
    """The verses a text writes itself (taken verses are left out): [{id, part, section, lang, topic, y, n, v}], with
    part, section and lang as the text gives them (None until it does). For checks that compare a text with a source."""
    out, cur = [], {'part': None, 'section': None, 'lang': None, 'topic': None}
    for raw in open(path, encoding='utf-8'):
        line = raw.strip()
        if not line or line.startswith('#'): continue
        if line.startswith('@'):
            k, _, v = line[1:].partition(' '); cur[k] = v.strip(); continue
        if TAKE.fullmatch(line): out.append(None); continue
        m = HEAD.fullmatch(line)
        if m:
            out.append({'id': m.group('id'), 'part': cur['part'], 'section': cur['section'], 'lang': cur['lang'], 'topic': cur['topic'],
                        'y': m.group('y'), 'n': m.group('n') or '', 'v': []}); cur['topic'] = None; continue
        out[-1]['v'].append(line)
    return [x for x in out if x]
