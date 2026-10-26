import pickle,re,json,collections
I='ि'
# (font-variant, gid) -> (string, kind)
R={}; B={}
def add(tab,spec):
    for k,v in spec.items():
        if isinstance(v,tuple): tab[k]=v
        else: tab[k]=(v,'n')
plain_i_R=[561,562,559,560,563,565,564,566,558,567,568,569]
plain_i_B=[565,567,563,564,566,569,568,571,562,572,573]
for g in plain_i_R: R[g]=('', 'pi')
for g in plain_i_B: B[g]=('', 'pi')
for g in [573,575,574,571,576,578,572]: R[g]=('', 'pia')
for g in [577]: B[g]=('', 'pia')
for g in [585,588,586,587,584,589]: R[g]=('', 'pir')
for g in [591,592]: B[g]=('', 'pir')
for g in [606]: R[g]=('', 'e')
for g in [610]: B[g]=('', 'e')
# reph combos: (extra string after cluster)
for g,x in {181:'',452:'ों',430:'ी',439:'े',451:'ो',459:'ं',442:'ै',454:'ौ',440:'ें',613:'ी'}.items(): R[g]=(x,'r')
for g,x in {181:'',455:'ो',463:'ं'}.items(): B[g]=(x,'r')
add(R,{202:'न्',274:'प्र',438:'ें',450:'ों',441:'ैं',609:'ी',403:'हु',429:'ीं',284:'श्र',215:'स्',269:'त्र',
 413:'रु',198:'त्',271:'द्र',414:'रू',415:'दु',207:'म्',607:'ी',179:'क्ष',404:'हू',405:'हृ',509:'द्ध',185:'ग्',180:'ज्ञ',416:'दू',
 276:'ब्र',483:'क्त',530:'ह्म',467:'ओं',188:'च्',183:'क्',210:'ल्',197:'ण्',254:'क्र',515:'न्न',524:'ष्ट',219:'क्ष्',214:'ष्',502:'त्त',
 256:'ग्र',517:'व्य',453:'ौं',201:'ध्',484:'ङ्ग',203:'प्',190:'ज्',526:'ष्ठ',520:'श्व',508:'द्व',461:'ईं',205:'ब्',199:'थ्',277:'भ्र',513:'द्य',
 417:'दृ',213:'श्',608:'ी',518:'श्च',186:'घ्',516:'प्न',503:'त्त्',283:'व्र',192:'ञ्',261:'ज्र',184:'ख्',286:'स्र',257:'घ्र',523:'श्न',610:'ीं',488:'ञ्ज',278:'म्र',
 529:'ह्न',489:'ट्ट',507:'द्भ',612:'ीं',675:'ु',206:'भ्',611:'ीं',531:'ह्य',491:'ट्ठ',533:'ह्व',272:'ध्र',620:'़ु',505:'द्ग',497:'ड्ड',511:'द्द',522:'श्ल',
 532:'ह्ल',621:'ु',208:'य्',623:'़ू',493:'ट्य',512:'द्म',464:'ऐं',499:'ड्य',496:'ड्ढ',287:'ह्र',501:'ढ्य',528:'ह्ण',266:'ड्र',468:'औं',212:'व्',525:'ष्ट्र'})
add(B,{215:'स्',613:'ी',202:'न्',442:'ें',284:'श्र',274:'प्र',454:'ों',203:'प्',198:'त्',256:'ग्र',433:'ीं',445:'ैं',179:'क्ष',487:'क्त',201:'ध्',271:'द्र',513:'द्ध',403:'हु',
 197:'ण्',210:'ल्',180:'ज्ञ',269:'त्र',611:'ी',521:'व्य',471:'ओं',519:'न्न',512:'द्व',506:'त्त',417:'रु',207:'म्',213:'श्',418:'रू',214:'ष्',488:'ङ्ग',421:'दृ',528:'ष्ट',
 188:'च्',199:'थ्',420:'दू',183:'क्',283:'व्र',277:'भ्र',185:'ग्',507:'त्त्',205:'ब्',517:'द्य',522:'श्च',419:'दु',190:'ज्',278:'म्र',186:'घ्',192:'ञ्',530:'ष्ठ'})
CONS=set('कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहळ')|set(chr(c) for c in range(0x958,0x960))
MATRA=set('ािीुूृॄेैोौंँः़ॅॉ')
def is_cons_tok(s): return bool(s) and s[-1] in CONS or (len(s)>1 and s[-1]=='़' and s[-2] in CONS)
def is_half(s): return bool(s) and s.endswith('्') and s[0] in CONS
def decode(chars, tab):
    """chars: list of (unicode,gid). returns logical string"""
    toks=[]
    for u,g in chars:
        if u==65533:
            s,k=tab.get(g,(f'⟨{g}⟩','n'))
        else: s,k=chr(u),'n'
        toks.append((s,k))
    out=[]  # list of strings
    i=0
    while i<len(toks):
        s,k=toks[i]
        if k in ('pi','pia','pir'):
            # gather cluster
            j=i+1; cl=[]
            while j<len(toks) and toks[j][1]=='e': j+=1
            while j<len(toks) and (is_half(toks[j][0]) or toks[j][0]=='्' or (toks[j][0] in CONS and j+1<len(toks) and toks[j+1][0]=='्')):
                cl.append(toks[j][0]); j+=1
            if j<len(toks) and toks[j][1]=='n' and (toks[j][0][:1] in CONS or toks[j][0][:1] in 'अआइईउऊएऐओऔ'):
                cl.append(toks[j][0]); j+=1
            while j<len(toks) and toks[j][0]=='़': cl.append('़'); j+=1
            pre='र्' if k=='pir' else ''
            out.append(pre+''.join(cl)+I+('ं' if k=='pia' else ''))
            i=j; continue
        if k=='e': i+=1; continue
        if k=='r':
            # insert र् before last cluster in out
            buf=''.join(out); p=len(buf)
            while p>0 and buf[p-1] in MATRA: p-=1
            # now buf[p-1] should be consonant; walk back cluster
            q=p
            if q>0 and buf[q-1] in CONS:
                q-=1
                while q>=2 and buf[q-1]=='्' and buf[q-2] in CONS: q-=2
            buf=buf[:q]+'र्'+buf[q:]+s
            out=[buf]; i+=1; continue
        out.append(s); i+=1
    return ''.join(out)
