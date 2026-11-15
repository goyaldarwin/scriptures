"""Taittirīya Upaniṣad: the witnesses' raw downloads (scriptures-data, <work path>/printouts/) → witness/*.txt, in check.py's format.

A witness file: paragraphs separated by blank lines; a line "# 1.3" names the anuvāka (vallī.anuvāka) the paragraphs
after it belong to, "# shanti.2" / "# shanti.3" the śānti pāṭha that opens vallī 2 / 3, "# end.2" / "# end.3" the one
printed after it. Every witness's closing words of an anuvāka (इति … ऽनुवाकः) and of a vallī (इति … वल्ली समाप्ता) and
its invocations (हरिः ॐ, ॐ श्री गुरुभ्यो नमः) are left out: the witnesses word them differently, and check.py leaves
ours out too.

  upanishads.org.in: one page per anuvāka, upanishads-org/p-<vallī>.<anuvāka>.html (and p-2.invocation, p-3.invocation,
      the śānti pāṭhas of vallīs 2 and 3); the text is the page's <p class="sloka" lang="sa">, its paragraphs divided
      by an empty line. The pages of 2.9 and 3.10 end with the सह नाववतु (→ end.2, end.3). → witness/upanishads-org.txt
  IIT Kanpur Heritage: the reader API's JSON, iitk/batch-*.json; the text is each ref's primary मूलम्. Its ref 1.5.2
      holds the text of 1.5.3 again (with the anuvāka's closing words), so 1.5.2's own paragraph is missing; the copy is
      left out (check.py → LACKS). No śānti pāṭhas of vallīs 2 and 3. → witness/iitk.txt
  Sanskrit Wikisource: wikitext of the three vallīs, wikisource/{shikshavalli,brahmanandavalli,bhriguvalli}.wiki, with
      Śaṅkara's bhāṣya after the mūla in vallīs 2 and 3. A section is a "== … अनुवाकः ==" heading, numbered by its
      ordinal; its text is its <poem> (or, where it has none, its plain lines), and of that the paragraphs ending
      in a number (॥ १ ॥) or holding a śānti (the bhāṣya's paragraphs end in ।।). The Śīkṣāvallī's opening śānti (a copy of anuvāka 1) is not compared; the
      Brahmānandavallī opens with the सह नाववतु (→ shanti.2), the Bhṛguvallī ends with it (→ end.3). → witness/wikisource.txt
  Vedic Heritage Portal: the three vallīs' pages, vedicheritage/{shikshavalli,brahmanandavalli,bhriguvalli}.html, one <p>
      per paragraph, with svaras, which are taken out (the text has none); the centred lines are the śānti pāṭhas and
      the vallīs' closing words. An anuvāka ends at its closing words (the page runs 2.3 and 2.4 into one paragraph, closed
      इति चतुर्थोऽनुवाकः; it is split where 2.4 begins, यतो वाचो). → witness/vedicheritage.txt
  GRETIL: TEI XML with Śaṅkara's bhāṣya, gretil/sa_taittirIyopaniSad-zaMkarabhASya.xml (IAST); the mūla is each
      <p xml:id="TaittU_v.a.p">, read into Devanagari by taittiriya_text.tr2deva (the conversion this work uses for the
      base page's transliteration). Its śānti pāṭhas stand inside the bhāṣya's notes: the सह नाववतु before vallī 3
      (→ shanti.3) and after it (→ end.3) are taken; its vallī 2 opening runs into the commentary and is not.
      → witness/gretil.txt

Usage: python3 witnesses.py <the folder printouts/ of the work in a scriptures-data clone>
"""
import glob, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from taittiriya_text import tr2deva

ORD = ['प्रथम', 'द्वितीय', 'तृतीय', 'चतुर्थ', 'पञ्चम', 'षष्ठ', 'सप्तम', 'अष्टम', 'नवम', 'दशम', 'एकादश', 'द्वादश']
CLOSE = [re.compile(p) for p in (
    r'[।॥|\s]*इत(?:ि\s+|्य)(?:शिक्षावल्यां\s+)?\S*?(?:ऽ|ो)?नुवा?द?कः\s*[।॥|]*\s*(?:[०-९0-9]+\s*[।॥|]+)?',   # an anuvāka's
    r'[।॥|\s]*इति\s+\S*\s*वल्ली\s*समाप्ता\s*[।॥|]*',                                             # a vallī's
    r'[।॥|\s]*इति तैत्तिरीय\S*\s*[।॥|]*', r'हरिः\s*ॐ\s*[।॥]*', r'ॐ श्री गुरुभ्यो नमः\s*।?')]
SVARA = re.compile('[॑-॔᳐-̱᳹]')

def clean(t):
    for c in CLOSE: t = c.sub(' ', t)
    lines = [re.sub(r'[ \t]+', ' ', l).strip() for l in t.split('\n')]
    return '\n'.join(l for l in lines if l.strip(' ।॥|'))

def order(k):
    a, b = k.split('.')
    return (int(b), 2, 0) if a == 'end' else (int(b), 0, 0) if a == 'shanti' else (int(a), 1, int(b))

def write(name, secs):
    """secs: {section: [paragraph]}."""
    out, n = [], 0
    for k in sorted(secs, key=order):
        paras = [clean(p) for p in secs[k]]
        paras = [p for p in paras if p]
        if not paras: continue
        out.append('# ' + k); out += paras; n += len(paras)
    open(os.path.join(HERE, 'witness', name), 'w', encoding='utf-8').write('\n\n'.join(out) + '\n')
    print(name + ':', n, 'paragraphs in', len([k for k in secs if secs[k]]), 'sections')

def upanishads_org(P):
    secs = {}
    for p in glob.glob(os.path.join(P, 'upanishads-org', 'p-*.html')):
        ref = re.search(r'p-(.+)\.html$', p).group(1)
        (m,) = re.findall(r'<p class="sloka" lang="sa">(.*?)</p>', open(p, encoding='utf-8').read(), re.S)
        paras = [html.unescape(re.sub(r'<br\s*/?>', '\n', x)) for x in re.split(r'<br\s*/?>\s*<br\s*/?>', m)]
        if ref.endswith('invocation'): secs['shanti.' + ref[0]] = paras; continue
        if ref in ('2.9', '3.10') and 'सह नाववतु' in paras[-1]: secs['end.' + ref[0]] = [paras.pop()]
        secs[ref] = paras
    write('upanishads-org.txt', secs)

def iitk(P):
    refs = {}
    for p in sorted(glob.glob(os.path.join(P, 'iitk', 'batch-[0-9][0-9][0-9].json'))):
        for v in json.load(open(p, encoding='utf-8'))['verses']:
            (m,) = [x for x in v['moolams'] if x['is_primary']]
            refs[v['ref']] = m['text']
    assert len(refs) == 51, len(refs)
    del refs['1.5.2']                     # a copy of 1.5.3 (above)
    secs = {}
    for r in sorted(refs, key=lambda r: tuple(map(int, r.split('.')))):
        secs.setdefault(r.rsplit('.', 1)[0], []).append(refs[r])
    write('iitk.txt', secs)

def wikisource(P):
    secs = {}
    for v, f in enumerate(['shikshavalli', 'brahmanandavalli', 'bhriguvalli'], 1):
        s = open(os.path.join(P, 'wikisource', f + '.wiki'), encoding='utf-8').read()
        s = re.sub(r'\{\{टिप्पणी\|.*?\}\}|\[\[[^\]]*\]\]|&nbsp;', '', s, flags=re.S)
        parts = re.split(r'^==(.*?)==\s*$', s, flags=re.M)
        if v == 2:
            secs['shanti.2'] = [x for x in re.split(r'\n\s*\n', parts[0]) if 'सह नाववतु' in x]
        for head, body in zip(parts[1::2], parts[2::2]):
            h = head.replace('॥', '').strip()
            if not h: continue
            (a,) = [i for i, o in enumerate(ORD, 1) if h.startswith(o) and not any(h.startswith(p) for p in ORD[i:] if len(p) > len(o))]
            poems = re.findall(r'<poem>(.*?)</poem>', body, re.S)
            body = '\n\n'.join(poems) if any(x.strip() for x in poems) else body
            paras = []
            for x in re.split(r'\n\s*\n', body.strip()):
                x = x.strip()
                if re.search(r'॥\s*[०-९]+\s*॥$', x) or 'शान्तिः' in x: paras.append(x)
            if v == 3 and a == 10 and 'सह नाववतु' in paras[-1]: secs['end.3'] = [paras.pop()]
            secs['%d.%d' % (v, a)] = paras
    write('wikisource.txt', secs)

def vedicheritage(P):
    secs = {}
    for v, f in enumerate(['shikshavalli', 'brahmanandavalli', 'bhriguvalli'], 1):
        s = open(os.path.join(P, 'vedicheritage', f + '.html'), encoding='utf-8').read()
        s = s[s.index('<video'):]; s = s[:s.index('</div>')]
        ps = [(('center' in a), html.unescape(re.sub(r'<[^>]+>', '', t)).replace('\xa0', ' ').strip())
              for a, t in re.findall(r'<p([^>]*)>(.*?)</p>', s, re.S)]
        ps = [(c, SVARA.sub('', t)) for c, t in ps if t]
        a, cur, shanti = 0, None, []
        for c, t in ps:
            if c:
                if 'वल्ली' in t and 'इति' not in t: continue                  # the vallī's title
                if 'इति' in t: continue                                       # its closing words
                shanti.append(t)
                if 'शान्तिः' in t:
                    secs['shanti.%d' % v if a == 0 else 'end.%d' % v] = ['\n'.join(shanti)]; shanti = []
                continue
            if a == 0 or cur is None: a += 1; cur = secs.setdefault('%d.%d' % (v, a), [])
            if (v, a) == (2, 3):                                              # 2.3 and 2.4 in one paragraph
                i = t.index('यतो वाचो'); cur.append(t[:i]); t = t[i:]; a += 1; cur = secs.setdefault('%d.%d' % (v, a), [])
            cur.append(t)
            if 'नुवाकः' in t: cur = None                                      # the anuvāka's last paragraph
    write('vedicheritage.txt', secs)

def gretil(P):
    s = open(os.path.join(P, 'gretil', 'sa_taittirIyopaniSad-zaMkarabhASya.xml'), encoding='utf-8').read()
    deva = lambda t: tr2deva(re.sub(r"\biti (?:\S+ ){1,2}'?nuv(?:ādak|āk)aḥ\s*/*", ' ', re.sub(r'<[^>]+>', '', t)).replace('//', '॥').replace('/', '।'))
    secs = {}
    for ref, t in re.findall(r'<p xml:id="TaittU_(\d+\.\d+)\.\d+">(.*?)</p>', s, re.S):
        secs.setdefault(ref, []).append(deva(t))
    saha = [m for m in re.findall(r'<note type="commentary"[^>]*>\s*<p>(oṃ ?/? ?saha nāv.*?)</p>', s, re.S)]
    assert len(saha) == 2, len(saha)
    secs['shanti.3'], secs['end.3'] = [deva(saha[0])], [deva(saha[1])]
    write('gretil.txt', secs)

def main(P):
    os.makedirs(os.path.join(HERE, 'witness'), exist_ok=True)
    upanishads_org(P); iitk(P); wikisource(P); vedicheritage(P); gretil(P)

if __name__ == '__main__':
    main(sys.argv[1])
