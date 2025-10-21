import sys, os, json, re
q = " ".join(sys.argv[1:]).strip()
if not q:
    print("Usage: amura ask <query>"); raise SystemExit(1)
idx = None
for p in ("data/index.json","data/dist/index.json"):
    if os.path.exists(p):
        idx = p; break
if not idx:
    print("No data loaded (run: amura load amura-offline.zip)"); raise SystemExit(1)
items = json.load(open(idx, encoding="utf-8"))
qw = [w.lower() for w in re.findall(r"\w+", q)]
hits=[]
for it in items:
    rel = it.get("out","")
    for cand in (os.path.join("data",rel), os.path.join("data","dist",os.path.basename(rel))):
        if os.path.exists(cand):
            txt = open(cand, encoding="utf-8", errors="ignore").read().lower()
            score = sum(txt.count(w) for w in qw)
            if score>0:
                hits.append((score,it,cand))
            break
hits.sort(reverse=True)
if not hits:
    print("No matches."); raise SystemExit(0)
for i,(s,it,path) in enumerate(hits[:5],1):
    print(f"[{i}] {it.get('id','')}  ({it.get('source','')})  score={s}")
    print(open(path,encoding="utf-8",errors="ignore").read()[:500].replace("\n"," "), "...")
