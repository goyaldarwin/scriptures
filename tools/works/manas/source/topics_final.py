import json,glob,os
from make_appdata_helpers import en_fix
m=json.load(open('merged.json')); idx={it['id']:i for i,it in enumerate(m['items'])}
out=[]; miss=[]
for k in ['bal','ayodhya','aranya','kishkindha','sundar','lanka','uttar']:
    f=f'topic_starts_{k}.json'
    if not os.path.exists(f): continue
    tp={x['n']:x for x in json.load(open(f'topics_{k}.json'))}
    prev=-1
    for x in json.load(open(f)):
        i=idx.get(x['id'])
        if i is None: miss.append(x); continue
        if i<=prev: miss.append(('order',x)); continue
        prev=i
        en=en_fix(tp[x['n']]['en'])
        en={137:'A description of the autumn',149:'Trijaṭā’s dream; dialogue between Sītā and Trijaṭā',174:'The battle begins'}.get(x['n'],en)
        out.append({'i':i,'hi':tp[x['n']]['hi'],'en':en,'c':x.get('confidence','')})
json.dump(out,open('topics_final.json','w'),ensure_ascii=False)
print(len(out),'missing/order',miss)
