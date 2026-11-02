import re
V_IND='अआइईउऊऋॠऌएऐओऔ'
def syllables(s):
    """vowel nuclei: independent vowels + consonants not followed by virama"""
    n=sum(1 for c in s if c in V_IND)
    n+=len(re.findall('[क-हळ](?!्)',s))
    return n
