import json,collections,sys
I=json.load(open(sys.argv[1]))['diffs']; V=json.load(open(sys.argv[2]))['diffs']
byv=collections.defaultdict(list)
for d in V: byv[(d['kanda'],d['sarga'])].append(d)
both=[];iitk_only=0;vr_differs_otherwise=0
for d in I:
    lo,hi=d['i'],d['i']+len(d['gp'])
    ov=[v for v in byv[(d['kanda'],d['sarga'])] if (v['i']<=hi and v['i']+len(v['gp'])>=lo)]
    same=[v for v in ov if v['gp']==d['gp'] and v['wit']==d['wit'] and v['i']==d['i']]
    if same: both.append(d)
    elif ov: vr_differs_otherwise+=1
    else: iitk_only+=1
json.dump(both,open(sys.argv[3],'w'),ensure_ascii=False)
print('IITK differences',len(I),'| VR.net reads like Gita Press there:',iitk_only,'| VR.net differs another way:',vr_differs_otherwise,'| both witnesses agree against Gita Press:',len(both))
c=collections.Counter((d['gp'],d['wit']) for d in both); print(c.most_common(40))
