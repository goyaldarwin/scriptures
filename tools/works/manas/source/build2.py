import json,re,collections
D=json.load(open('hi_items.json')); items=D['items']; pauses=D['pauses']
eu=json.load(open('en_units.json'))
KANDS=['bal','ayodhya','aranya','kishkindha','sundar','lanka','uttar']
src2item={it['src']:i for i,it in enumerate(items)}
en_groups={}   # eu idx -> group dict
item_en=collections.defaultdict(set); tr_assign=collections.defaultdict(list)
for k in KANDS:
    d=json.load(open(f'align_{k}.json')); H,E=d['H'],d['E']
    pairs=[]
    for op,i1,i2,j1,j2 in d['ops']:
        if op=='equal' or (op=='replace' and i2-i1==j2-j1):
            for a,b in zip(range(i1,i2),range(j1,j2)): pairs.append((a,b))
    e2h=collections.defaultdict(collections.Counter); line2h=collections.defaultdict(collections.Counter)
    for a,b in pairs:
        hsrc=H[a][1]; eidx,li=E[b][1],E[b][2]
        if hsrc in src2item:
            e2h[eidx][src2item[hsrc]]+=1; line2h[(eidx,li)][src2item[hsrc]]+=1
    h2e=collections.defaultdict(collections.Counter)
    for eidx,c in e2h.items():
        for i,n in c.items(): h2e[i][eidx]+=n
    grp_items=collections.defaultdict(list)
    for i,c in h2e.items():
        eidx=c.most_common(1)[0][0]; item_en[i].add(eidx); grp_items[eidx].append(i)
    for eidx in e2h:
        its=sorted(grp_items.get(eidx,[]))
        u=eu[eidx]
        en_groups[eidx]={'text':' '.join(u.get('en') or []).strip(),'label':u.get('label'),'fn':u.get('fn') or [],'items':its,'type':u.get('type')}
    for (eidx,li),c in line2h.items():
        i=c.most_common(1)[0][0]
        tr_assign[i].append((eidx,li,eu[eidx]['tr'][li]))
# coverage stats
no_en=[i for i in range(len(items)) if i not in item_en]
print('items without english',len(no_en))
for i in no_en[:15]: print('  ',items[i]['id'],items[i]['v'][0][:50])
unused=[e for e,u in enumerate(eu) if u.get('tr') and e not in en_groups]
print('english units unaligned',len(unused))
for e in unused[:10]: print('  ',eu[e]['p'],eu[e]['tr'][:1])
# attach
for i,it in enumerate(items):
    trs=sorted(tr_assign.get(i,[]))
    it['tr']=[t for _,_,t in trs]
    it['en_g']=sorted(item_en.get(i,[]))
mism=[(it['id'],len(it['v']),len(it['tr'])) for it in items if len(it['v'])!=len(it['tr'])]
print('line count mismatch',len(mism),mism[:15])
json.dump({'items':items,'pauses':pauses,'en_groups':{str(k):v for k,v in en_groups.items()}},open('merged.json','w'),ensure_ascii=False)
