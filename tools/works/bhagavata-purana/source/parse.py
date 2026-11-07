import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
L=json.load(open('lines.json'))
pages=collections.defaultdict(list)
for x in L: pages[(x['b'],x['pg'])].append(x)
book=[]; sk=None; adh=None; mode=None
for key in sorted(pages):
    PL=pages[key]
    if is_caption_page(PL): continue
    xs=[x['x'] for x in PL if x['size']==15.0 and x['x'] and not x['bold']]
    margin=min(xs) if xs and min(xs)<110 else 72.0
    TH=margin+45
    for x in PL:
        t=norm(x['t'])
        if not t: continue
        if x['size']>15.5:
            m=re.match(r'^(\S+?)ः?\s*स्कन्धः$',t)
            if m and m.group(1).rstrip('ः') in ORD:
                n=ORD[m.group(1).rstrip('ः')]
                if not book or book[-1]['n']!=n: sk=dict(n=n,adh=[]); book.append(sk)
                adh=None; mode=None; continue
            if t=='श्रीमद्भागवतमाहात्म्यम्' and not book:
                sk=dict(n=0,adh=[],pre=[]); book.append(sk); adh=None; mode=None; continue
            if sk is None: continue
            if t.startswith('अथ') and t.endswith('ध्यायः'):
                adh=dict(n=len(sk['adh'])+1,head=t,title='',heads=[],san=[],hindi=[],col=[],notes=[],pg=key); sk['adh'].append(adh); mode='title'; continue
            if adh is None: continue
            if re.search(r'इति|इत्य',t) and 'स्कन्धः' in t:
                mode='end'
                if sk['n']==12: sk=None; adh=None
                continue
            if mode=='title' and abs(x['size']-17.2)<0.2: adh['title']=(adh['title']+' '+t).strip(); continue
            adh['heads'].append((t,len(adh['san']))); continue
        if sk is not None and sk['n']==0 and adh is None: sk['pre'].append(t); continue
        if adh is None: continue
        if mode=='end':
            if 'तत्सत्' not in t: adh['notes'].append((t,x['x'],x['marks'],x['bold'],norm(x['tm'])))
            continue
        if mode=='title' and x['bold'] and hscore(t)>0 and not END.search(t):
            adh['title']=(adh['title']+' '+t).strip(); continue
        if mode=='title' and not adh['title'] and hscore(t)>0 and not END.search(t) and x['x']>110:
            adh['title']=(adh['title']+' '+t).strip(); continue
        if mode=='title': mode='text'
        if COL.match(t) and mode!='notes': mode='col'
        if mode=='col':
            adh['col'].append(t)
            if re.search(r'॥\s*[०-९]+\s*॥\s*$',t): mode='notes'
            continue
        if mode=='notes': adh['notes'].append((t,x['x'],x['marks'],x['bold'],norm(x['tm']))); continue
        if is_verse(t,x):
            kind='spk' if ((SPK.search(t) or re.match(r'^\[.*\]$',t)) and '।' not in t and '॥' not in t and len(t)<40) else 'v'
            adh['san'].append((kind,t,x['marks'],key,x['x'],x['y']))
        elif x['bold'] and x['x']<=TH:
            adh['san'].append(('g',t,x['marks'],key,x['x'],x['y']))
        else:
            adh['hindi'].append((norm(x['tm']),x['x']>margin+10,x['marks'],key,x['y']))
for s_ in book:
    for a_ in s_['adh']:
        if not a_['title']:
            h=[x for x in a_['heads'] if hscore(x[0])>0]
            if h: a_['title']=h[0][0]; a_['heads'].remove(h[0])
json.dump(book,open('raw.json','w'),ensure_ascii=False)
for s in book: print(s['n'],len(s['adh']))
