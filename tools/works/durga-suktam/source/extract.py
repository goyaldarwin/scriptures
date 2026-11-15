"""Durgā Sūkta: the shlokam.org page (HTML) → source/durga-suktam_raw.json.

Usage: python3 extract.py <durga-suktam.html>
The page is private (scriptures-data:
hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/durga-suktam/printouts/shlokam/durga-suktam.html, fetched from
https://shlokam.org/shloka/durga-suktam.htm). For every verse block of the page (div.verse-section) this keeps, in reading
order, the page's verse number (data-verse), its Devanagari lines (div.detail-sanskrit) and its transliteration lines,
split at <br>, zero-width spaces removed, empty lines dropped (tools/works/shlokam.py → page). The page's English is the
publisher's and is not kept. settle.py makes text.txt from this file (../reconciliation.md).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..')); import shlokam

if __name__ == '__main__':
    B = shlokam.page(sys.argv[1])
    json.dump(B, open(os.path.join(HERE, 'durga-suktam_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(len(B), 'blocks,', sum(len(b['v']) for b in B), 'Devanagari lines')
