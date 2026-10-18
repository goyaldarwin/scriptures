REP=[('( ⁄U and ◊)','( र and म)'),('“⁄U”','“र”'),('“∑¸§”','“र्क”'),('“´¸§”','“र्ऋ”'),('“´§”','“ऋ”'),('“◊˜Ô”','“म्”'),('“„ṭU”','“हं”'),('“⁄˜UÔ”','“र्”'),
('(∑È§øÊśË)','(कुचाली)'),('“EÿÈﬂ◊ÉÊÊŸÊ◊ÎÃÁhÃ”','“श्वयुवमघोनामतद्धिते”'),('XIII.7ñ11','XIII.7—11'),('(SﬂÃ— ¬˝◊ÊáÊ)','(स्वतः प्रमाण)'),
('§Rṣyamūka','Ṛṣyamūka'),('§Rṣi','Ṛṣi'),('(¡Êª˝Ã˜)','(जाग्रत्)'),('(Sﬂ¬A)','(स्वप्न)'),('(‚ÈcÊÈÁ#)','(सुषुप्ति)'),('(ÃÈ⁄UËÿ)','(तुरीय)'),
('(•ÁSàÊ)','(अस्ति)'),('(¡ÊÿÃ)','(जायते)'),('(Áﬂ¬Á⁄UáÊ◊Ã)','(विपरिणमते)'),('(ﬂh¸Ã)','(वर्धते)'),('(ˇÊËÿÃ)','(क्षीयते)'),('(Ÿ‡ÿÁàÊ)','(नश्यति)'),
('(üÊË⁄UÊ◊Êÿ Ÿ◊—)','(श्रीरामाय नमः)'),('cuckcﬂos','cuckoos'),('(¬˝śÿ)','(प्रलय)'),('(˙ Ÿ◊Ê ÷ªﬂÃ ﬂÊ‚ÈḍﬂÊÿ)','(ॐ नमो भगवते वासुदेवाय)')]
def fix(groups):
    n=0
    for k,v in groups.items():
        for a,b in REP:
            if a in v['x']: v['x']=v['x'].replace(a,b); n+=1
            if v.get('f'):
                nf=[s.replace(a,b) for s in v['f']]
                if nf!=v['f']: n+=1; v['f']=nf
    # footnote † of doha 20 continued on the next page and was attached to doha 21
    a=groups.get('104'); b=groups.get('102')
    if a and b and a.get('f') and a['f'][0].startswith('vowel'):
        b['f']=b['f']+a['f']; del a['f']; n+=1
    # footnotes continued from the previous page that landed on the next group
    ks=sorted(groups,key=int); prev=None
    for k in ks:
        f=groups[k].get('f')
        if not f: continue
        if prev and f[0][:1].islower():
            groups[prev]['f']=groups[prev]['f']+f; del groups[k]['f']; n+=1; print('moved fn',k,'->',prev); continue
        prev=k
    print('en fixes',n)
