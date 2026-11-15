"""Nīlā Sūkta: the raw witness downloads → source/witness/<site>.txt (Devanagari runs for check.py).

Usage: python3 witnesses.py <dir>
<dir> holds the raw downloads as stored in scriptures-data at
hinduism/veda/yajurveda/krishna-yajurveda/samhita/neela-suktam/printouts/wikisource/:
  तैत्तिरीयसंहिता-१-४.wiki.txt   Sanskrit Wikisource, Taittirīya Saṃhitā kāṇḍas 1–4 with svaras, raw wikitext of
      https://sa.wikisource.org/wiki/तैत्तिरीयसंहिता-१-४: the sūkta's two mantras open its 4.4.12.5 (गृ॒णा॒हि॒ … विष्णु॑पत्नी).
      Its private-use characters are read as tools/works/sukta_witness.py → PUA says.
  तैत्तिरीयसंहिता(विस्वरः)__काण्डम् ४__प्रपाठकः ४.wiki.txt   Sanskrit Wikisource, the same prapāṭhaka unaccented, raw
      wikitext of https://sa.wikisource.org/wiki/तैत्तिरीयसंहिता(विस्वरः)/काण्डम्_४/प्रपाठकः_४: the same words in its
      section 5 (the page gives the section twice, as a run and line by line; the run is used).
Neither page has the invocation (नीळां देवीम्…) or the Gāyatrī: they are not the Saṃhitā's.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..'))
from sukta_witness import read_raw, between, write_witness

def write(name, runs): write_witness(os.path.join(HERE, 'witness', name), runs)

if __name__ == '__main__':
    ts = read_raw(os.path.join(sys.argv[1], 'तैत्तिरीयसंहिता-१-४.wiki.txt'))
    write('wikisource-ts.txt', [('m01', 'm02', between(ts, 'गृ॒णा॒हि॒ । घृ॒तव॑ती', 'जग॑तो॒ विष्णु॑पत्नी'))])
    tv = read_raw(os.path.join(sys.argv[1], 'तैत्तिरीयसंहिता(विस्वरः)__काण्डम् ४__प्रपाठकः ४.wiki.txt'))
    write('wikisource-ts-plain.txt', [('m01', 'm02', between(tv, 'गृणाहि । घृतवती', 'जगतो विष्णुपत्नी'))])
