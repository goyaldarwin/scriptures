import pickle,sys,json,collections
sys.path.insert(0,sys.argv[1]);import layout,chanakya as K
P=pickle.load(open(sys.argv[2],'rb'))
stream=[];bad=collections.Counter();ex=collections.defaultdict(list)
for pi in range(len(P)):
    for l in layout.lines(P[pi]):
        l['page']=pi+1; stream.append({k:l[k] for k in ('page','col','y','kind','text','size','fonts')})
        if l['kind']=='sa' and pi>=58:
            for w in l['text'].split():
                for r in K.problems(w):
                    bad[r]+=1; ex[r].append((pi+1,w))
json.dump(stream,open(sys.argv[3],'w'),ensure_ascii=False)
print(bad)
for r,e in ex.items(): print(r,len(e),e[:60])
