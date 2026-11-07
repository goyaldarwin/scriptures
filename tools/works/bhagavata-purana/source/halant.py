"""Find words whose ्य the e-book drops after a conjunct (बुद्धया for बुद्ध्या): a line one syllable too long for its metre,
whose only fix is one such ्य, decides the word; every occurrence of that word is then written with ्य. -> halant.json"""
import json,re,sys,collections
w=json.load(open(sys.argv[1]))
V='अआइईउऊऋॠऌएऐओऔ'
def syl(t):
    t=re.sub(r'[^ऀ-ॿ]','',t); n=0
    for i,ch in enumerate(t):
        if ch in V: n+=1
        elif 'क'<=ch<='ह' or ch=='ळ':
            j=i+1
            if j<len(t) and t[j]=='़': j+=1
            if not (j<len(t) and t[j]=='्'): n+=1
    return n
SP=re.compile(r'(वाच|ऊचुः|ूचुः|ऊचतुः|ूचतुः|ऊचे|ऊचिरे)$')
# a consonant (or conjunct) followed by य where the e-book may have dropped the halant: X + य, X not followed by a vowel sign
CAND=re.compile(r'(?<=द्ध|द्भ|द्व|ह्व|ग्र|द्र|ष्ट|ष्ण|ष्ठ|ह्न|ङ्ग|ह्म|द्ग|द्द|घ्र)य')
def cands(tok):
    out=[]
    for m in CAND.finditer(tok):
        i=m.start()
        out.append(tok[:i]+'्'+tok[i:])
    return out
fix=collections.defaultdict(list); amb=[]
for it in w['items']:
    if it['y'] not in ('shloka','mshloka'): continue
    lines=[l for l in it['v'] if not (SP.search(l) and '।' not in l and '॥' not in l)]
    ss=[syl(re.sub(r'॥.*','',l)) for l in lines]
    if len(lines)<2: continue
    if all(s in (16,17) for s in ss) and len(lines) in (2,3): want=16
    else:
        c=collections.Counter(ss); mode,k=c.most_common(1)[0]
        if k<2 or len(set(ss))>2: continue
        want=mode
    for l,s in zip(lines,ss):
        if s!=want+1: continue
        toks=re.findall(r'[ऀ-ॣ॰-ॿ]+',re.sub(r'॥.*','',l))
        opts=[(t,c) for t in toks for c in cands(t)]
        if len(opts)==1: fix[opts[0][0]].append((it['id'],opts[0][1]))
        elif opts: amb.append((it['id'],s,want,l,[c for t,c in opts]))
json.dump({k:v[0][1] for k,v in fix.items()},open('halant.json','w'),ensure_ascii=False,indent=0)
print(len(fix),'words decided;',len(amb),'lines with several candidates')
for k,v in sorted(fix.items()): print(k,'→',v[0][1],len(v),v[0][0])
print('--- ambiguous')
for a in amb[:400]: print(a)
