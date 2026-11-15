"""Durgā Sūkta: the raw witness downloads → source/witness/<site>.txt (Devanagari runs for check.py).

Usage: python3 witnesses.py <dir>
<dir> holds the raw downloads as stored in scriptures-data at
hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/durga-suktam/printouts/wikisource/:
  तैत्तिरीय-आरण्यकम्.wiki.txt   Sanskrit Wikisource, the whole Taittirīya Āraṇyaka with svaras, raw wikitext of
      https://sa.wikisource.org/wiki/तैत्तिरीय-आरण्यकम्; the page numbers the Mahānārāyaṇa prapāṭhaka (TA 10) as its 6.x:
      mantras 1–6 are in its 6.1.11 (it has no mantra 7, गोभिर्जुष्टम्), the Gāyatrī in its 6.1.6. Its private-use
      characters are read as tools/works/sukta_witness.py → PUA says.
  महानारायणोपनिषत्.wiki.txt   Sanskrit Wikisource, the Mahānārāyaṇa Upaniṣad (Āndhra recension, unaccented), raw wikitext
      of https://sa.wikisource.org/wiki/महानारायणोपनिषत्: mantras 1–7 are its anuvāka 2 (its heading "दुर्गा सूक्तम्" after
      mantra 1 is dropped), the Gāyatrī among its Gāyatrīs. The page holds the text twice; the first run is used.
Kept: the mantra text only; the site's verse numbers, labels and headings are dropped.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..'))
from sukta_witness import read_raw, between, write_witness

def write(name, runs): write_witness(os.path.join(HERE, 'witness', name), runs)

if __name__ == '__main__':
    ta = read_raw(os.path.join(sys.argv[1], 'तैत्तिरीय-आरण्यकम्.wiki.txt'))
    write('wikisource-ta.txt', [
        ('m01', 'm06', between(ta, 'जा॒तवे॑दसे', 'माय॑जस्व')),
        ('gayatri', 'gayatri', between(ta, 'का॒त्या॒य॒नाय॑ वि॒द्महे॑', 'दुर्गिः प्रचो॒दया᳚?त्'))])
    mn = read_raw(os.path.join(sys.argv[1], 'महानारायणोपनिषत्.wiki.txt'))
    a2 = between(mn, 'जातवेदसे सुनवाम', 'इह मादयन्ताम् ॥').replace('दुर्गा सूक्तम् ।', '')
    write('wikisource-mnu.txt', [
        ('m01', 'm07', a2),
        ('gayatri', 'gayatri', between(mn, 'कात्यायनाय विद्महे', 'प्रचोदयात्'))])
