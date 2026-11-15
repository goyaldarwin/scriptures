"""Puruṣa Sūkta: the raw witness downloads → source/witness/<site>.txt (Devanagari runs for check.py).

Usage: python3 witnesses.py <dir>
<dir> holds the raw downloads as stored in scriptures-data at
hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/purusha-suktam/printouts/wikisource/:
  तैत्तिरीयारण्यकम्(विस्वर)__प्रपाठकः ३.wiki.txt  Sanskrit Wikisource, Taittirīya Āraṇyaka (unaccented), prapāṭhaka 3, raw
      wikitext of https://sa.wikisource.org/wiki/तैत्तिरीयारण्यकम्(विस्वर)/प्रपाठकः_३: anuvāka 3.12 (mantras 1–18),
      3.13 (the Uttaranārāyaṇa, 19–24) and the prapāṭhaka's closing śānti (तच्छं योः), compared with both of our śāntis.
Kept: the mantra text only. Dropped: the site's ", इति" after each ṛk, its section numbers "( १)", the anuvāka's closing
index of first words (after ।।, पूरुषः पुरोऽग्रतोऽजायत …) and the <ref> tag.
Wikisource's separate page पुरुषसूक्तम् is not used: it is the Ṛgveda's sixteen-verse order (10.90), not the Āraṇyaka's,
typed with S for ऽ and slips (यद्न्नेना, ड्ड for ङ्गु), by one contributor.
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))

def clean(s):
    s = re.sub(r'<ref>.*?</ref>', '', s)
    s = re.sub(r'\(\s*[०-९]+\s*\)', ' ', s)
    s = re.sub(r',\s*इति', ' ', s)
    return re.sub(r'[ \t]+', ' ', s).strip()

if __name__ == '__main__':
    t = open(os.path.join(sys.argv[1], 'तैत्तिरीयारण्यकम्(विस्वर)__प्रपाठकः ३.wiki.txt'), encoding='utf-8').read()
    a12 = t.split('3.12 अनुवाक १२')[1].split('।।')[0]
    a12 = a12[:a12.rindex('इति')]                       # the index of first words after the last ṛk
    a13 = t.split('3.13 अनुवाक १३')[1].split('।।')[0]
    sh = re.search(r'\n(तच्छं योरावृणीमहे.*?)\nइति', t, re.S).group(1)
    out = ['# shanti.1 shanti.1', clean(sh), '', '# m01 m18', clean(a12), '', '# m19 m24', clean(a13), '', '# shanti.end shanti.end', clean(sh), '']
    open(os.path.join(HERE, 'witness', 'wikisource-ta.txt'), 'w', encoding='utf-8').write('\n'.join(out))
