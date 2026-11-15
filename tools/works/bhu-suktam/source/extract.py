"""Bhū Sūkta: Sanskrit Wikisource's accented Taittirīya Saṃhitā → source/ts-1.5.3_raw.txt (the passage the sūkta is).

Usage: python3 extract.py <dir>
<dir> holds the raw download as stored in scriptures-data at
hinduism/veda/yajurveda/krishna-yajurveda/samhita/bhu-suktam/printouts/wikisource/तैत्तिरीयसंहिता-१-४.wiki.txt, the raw
wikitext of https://sa.wikisource.org/wiki/तैत्तिरीयसंहिता-१-४ (Taittirīya Saṃhitā, kāṇḍas 1–4, with svaras; the page
names no edition). Kept: its 1.5.3.1 and 1.5.3.2 from भूमि॑र्भू॒म्ना to मा॑दयन्ताम् ।।, the sūkta as the Vaiṣṇava Pañca
Sūkta recites it and the recording sings it (../reconciliation.md); the rest of 1.5.3.2 (स॒प्त ते॑ अग्ने…) is the next
mantra of the Saṃhitā, not recited with it. The page's private-use characters are read as tools/works/sukta_witness.py
→ PUA says (its ꣳ in त्रि॒ꣳ॒शत् and य॒ज्ञꣳ); its label lines (1.5.3.2) and section numbers ([10]) are dropped, its
daṇḍas kept. settle.py makes text.txt from this file.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..'))
from sukta_witness import read_raw, between, clean

if __name__ == '__main__':
    t = read_raw(os.path.join(sys.argv[1], 'तैत्तिरीयसंहिता-१-४.wiki.txt'))
    p = clean(between(t, 'भूमि॑र्भू॒म्ना द्यौर्व॑रि॒णा', 'मा॑दयन्ताम् ।।'))
    open(os.path.join(HERE, 'ts-1.5.3_raw.txt'), 'w', encoding='utf-8').write(p + '\n')
    print(p)
