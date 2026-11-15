"""Nārāyaṇa Sūkta: the raw witness downloads → source/witness/<site>.txt (Devanagari runs for check.py).

Usage: python3 witnesses.py <dir>
<dir> holds the raw downloads as stored in scriptures-data at
hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/narayana-suktam/printouts/wikisource/:
  तैत्तिरीय-आरण्यकम्.wiki.txt   Sanskrit Wikisource, the whole Taittirīya Āraṇyaka with svaras, raw wikitext of
      https://sa.wikisource.org/wiki/तैत्तिरीय-आरण्यकम्; the page numbers the Mahānārāyaṇa prapāṭhaka (TA 10) as its 6.x:
      the sūkta is its 6.11.1–6.12.1, the Gāyatrī is in its 6.1.6, the śānti सह नाववतु closes its Upaniṣad prapāṭhakas.
      Its private-use characters are read as tools/works/sukta_witness.py → PUA says.
  महानारायणोपनिषत्.wiki.txt   Sanskrit Wikisource, the Mahānārāyaṇa Upaniṣad (Āndhra recension, unaccented), raw wikitext
      of https://sa.wikisource.org/wiki/महानारायणोपनिषत्: the sūkta is its anuvāka 13 and the first verse of 23, the śānti
      opens the page, the Gāyatrī is among its Gāyatrīs. The page holds the text twice (a run, then the same text line
      by line with {\\म्+} for ꣳ); the run is used.
Kept: the mantra text only; the site's verse numbers and anuvāka headings are dropped.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..'))
from sukta_witness import read_raw, between, write_witness

def write(name, runs): write_witness(os.path.join(HERE, 'witness', name), runs)

if __name__ == '__main__':
    ta = read_raw(os.path.join(sys.argv[1], 'तैत्तिरीय-आरण्यकम्.wiki.txt'))
    write('wikisource-ta.txt', [
        ('shanti.1', 'shanti.1', between(ta, '\nस॒हना॑ववतु', 'शान्तिः॑')),
        ('m01', 'm14', between(ta, 'स॒ह॒स्र॒शीर्॑षन्', 'स्व॒राट्') + ' ' +
                       between(ta, 'ऋ॒तꣳ स॒त्यं प॑रं', 'वै नमः॑')),
        ('gayatri', 'gayatri', between(ta, 'ना॒रा॒य॒णाय॑ वि॒द्महे॑', 'विष्णुः प्रचो॒दया᳚?त्'))])
    mn = read_raw(os.path.join(sys.argv[1], 'महानारायणोपनिषत्.wiki.txt'))
    run = mn[:mn.index('\n2\n')] if '\n2\n' in mn else mn
    write('wikisource-mnu.txt', [
        ('shanti.1', 'shanti.1', between(run, 'ॐ सह नाववतु', 'शान्तिः ॥')),
        ('m01', 'm14', between(run, 'सहस्रशीर्षं देवं', 'स्वराट् ॥') + ' ' + between(run, 'ऋतꣳ सत्यं परं', 'नमो नमः')),
        ('gayatri', 'gayatri', between(mn, 'नारायणाय विद्महे', 'प्रचोदयात्'))])
