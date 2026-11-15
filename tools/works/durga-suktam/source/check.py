"""Checks text.txt (the Durgā Sūkta) against the Devanagari witnesses in source/witness/ (made by witnesses.py), with
the comparison shared by the six Sūktas (tools/works/sukta_witness.py: what is not compared and what is read alike).
The only differences allowed are those recorded in reconciliation.md (EXPECTED below).
Usage: python3 tools/works/durga-suktam/source/check.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..')); import sukta_witness

EXPECTED = {   # witness file: [(witness, ours)]
    'wikisource-ta.txt': [('', 'ओम्'),                   # the ॐ the recitation opens the sūkta and the Gāyatrī with
                          ('निजहाति', 'निदहाति'),
                          ('सहमानमग्निमुग्रꣳ हुवेम', 'सहमानमुग्रमग्निꣳ हुवेम')],     # the two words in the other order
    'wikisource-mnu.txt': [('', 'ओम्'),
                           ('सिन्धुं न वावा', 'सिन्धुं न नावा'), ('सहमानमुग्नमग्निꣳ', 'सहमानमुग्रमग्निꣳ'),   # the page's slips
                           ('सधस्तात्', 'सधस्थात्'), ('कन्याकुमारि', 'कन्यकुमारि')],
}

if __name__ == '__main__':
    sys.exit(1 if sukta_witness.compare(os.path.join(HERE, '..', 'text.txt'), os.path.join(HERE, 'witness'), EXPECTED) else 0)
