import json,re,collections,sys
D='०१२३४५६७८९'
def num(s): return int(s.translate(str.maketrans(D,'0123456789')))
ORD={'प्रथम':1,'द्वितीय':2,'तृतीय':3,'चतुर्थ':4,'पञ्चम':5,'षष्ठ':6,'सप्तम':7,'अष्टम':8,'नवम':9,'दशम':10,'एकादश':11,'द्वादश':12}
def norm(t):
    t=re.sub(r'(?<=[\u0900-\u097f]):',r'ः',t)
    t=re.sub(r'\s*।\s*।\s*','॥',t)
    t=re.sub(r'[ \t ]+',' ',t).strip()
    return t
SPK=re.compile(r'(वाच|वाच ह|ऊचुः|ूचुः|ऊचतुः|ूचतुः|ऊचे|ऊचिरे)$')
COL=re.compile(r'^इति\s*श्री(मद्भागवते|पद्मपुराणे)')
END=re.compile(r'॥\s*([०-९]+)\s*(॥)?\s*$')
HW=set('है हैं था थे थी और भी नहीं यह वह उस इस उन कि तो जो हो गये गया गयी किया करते होकर होती उनके उनकी इसके इसलिये लिये वे ये मैं हम आप तुम'.split())
HS2=set('है हैं था थे थी और नहीं भी किया करते होकर होती उनके उनकी इसके इसलिये लिये मैं हम आप तुम गये गया गयी करके'.split())
HS=('ने','को','में','से','का','की','के','पर','सें')
def hscore(t):
    toks=re.findall(r'[\u0900-\u0963\u0970-\u097f]+',t)
    return sum(1 for w in toks if w in HW or (len(w)>3 and w.endswith(HS) and not w.endswith(('ाने','ोने')) ))
def is_verse(t,x):
    if x['bold']: return x['x']>=125
    h=hscore(t)
    if x['x']>=125:
        strong=sum(1 for w in re.findall(r'[\u0900-\u0963\u0970-\u097f]+',t) if w in HS2)
        return not ((strong>=1 and len(t)>45) or (h>=5 and len(t)>60))
    if x['x']<=108: return False
    return h==0 and len(t)<60
def is_caption_page(lines):
    return any(re.search('[A-Za-z]{3}',x['t']) for x in lines) and len(lines)<=4
