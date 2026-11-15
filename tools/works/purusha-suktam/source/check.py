"""Checks text.txt (the Puruṣa Sūkta) against the Devanagari witnesses in source/witness/ (made by witnesses.py), with
the comparison shared by the six Sūktas (tools/works/sukta_witness.py: what is not compared and what is read alike).
The only differences allowed are those recorded in reconciliation.md (EXPECTED below).
Usage: python3 tools/works/purusha-suktam/source/check.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..')); import sukta_witness

EXPECTED = {   # witness file: [(witness, ours)]
    'wikisource-ta.txt': [('विद्वानमृतं इह', 'विद्वानमृत इह')],   # m17: the witness's slip (its own 3.13, m20, reads अमृत इह)
}

if __name__ == '__main__':
    sys.exit(1 if sukta_witness.compare(os.path.join(HERE, '..', 'text.txt'), os.path.join(HERE, 'witness'), EXPECTED) else 0)
