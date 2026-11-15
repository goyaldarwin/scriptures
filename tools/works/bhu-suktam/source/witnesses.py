"""Bhū Sūkta: the raw witness download → source/witness/<site>.txt (Devanagari runs for check.py).

Usage: python3 witnesses.py <dir>
The text itself is made from Sanskrit Wikisource's accented Taittirīya Saṃhitā (extract.py, settle.py); the same
passage is written here as a witness file, so that check.py proves the text keeps the page's words and svaras, letter
for letter, but for what reconciliation.md records. No second written witness of Taittirīya Saṃhitā 1.5.3 was found:
Wikisource's unaccented Saṃhitā is downloaded for kāṇḍa 4, prapāṭhaka 4 only, and GRETIL has no Taittirīya Saṃhitā
in Devanagari or a Bhū Sūkta.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..'))
from sukta_witness import read_raw, between, write_witness

if __name__ == '__main__':
    t = read_raw(os.path.join(sys.argv[1], 'तैत्तिरीयसंहिता-१-४.wiki.txt'))
    write_witness(os.path.join(HERE, 'witness', 'wikisource-ts.txt'), [('m01', 'm07', between(t, 'भूमि॑र्भू॒म्ना', 'मा॑दयन्ताम् ।।'))])
