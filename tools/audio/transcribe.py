"""Transcribe the recordings of an audio source with Whisper (speech → text with times).

Usage:  DATA_DIR=<clone of goyaldarwin/scriptures-data> WHISPER_MODEL=<model folder> \
        (or AUDIO_DIR=<folder with the original files named as in recordings.json "file">)
        python3 tools/audio/transcribe.py tools/works/<work>/audio/<source-id> [WORKER WORKERS]
Run several workers in parallel by giving each its number: `… 0 2` and `… 1 2`. Each recording is claimed
with transcripts/<id>.lock, so workers never transcribe the same recording; delete a lock left by a stopped worker.
Recordings come from recordings.json: "data" is the file in scriptures-data (used with DATA_DIR), "file" the original download name (used with AUDIO_DIR). Output: transcripts/<video id>.jsonl,
plus .done when finished. A stopped run resumes from its last 10-minute chunk.
Model: Whisper small in CTranslate2 int8 format (e.g. Systran/faster-whisper-small; WHISPER_MODEL=small downloads it).
Optional env: THREADS (CPU threads, default 1), ONLY (comma-separated video ids to do).
source.json may set "window": seconds (6 works well for chant). Then each stretch of that length is transcribed on its own, so the recogniser
cannot skip minutes at a time; use it for chant and singing (Vedic recitation, āratīs), where Whisper otherwise drops
long passages it takes for music.
"""
import sys,json,os,subprocess,time,numpy as np
from faster_whisper import WhisperModel
SRC=os.path.abspath(sys.argv[1]); TR=os.path.join(SRC,'transcripts'); os.makedirs(TR,exist_ok=True)
DATA=os.environ.get('DATA_DIR'); AUD=os.environ.get('AUDIO_DIR',''); LANG=json.load(open(os.path.join(SRC,'source.json'))).get('lang','hi')
# Whisper's own Sanskrit mode writes Latin letters; its Hindi mode writes Devanagari, which align.py needs. Awadhi likewise.
LANG={'sa':'hi','awa':'hi'}.get(LANG,LANG)
WIN=json.load(open(os.path.join(SRC,'source.json'))).get('window')
# with windows: no temperature fallback and no "no speech" dropping (both made Whisper loop on, or drop, sung passages),
# at most 60 tokens per window, and word times
NOFALLBACK=dict(temperature=0.0,compression_ratio_threshold=None,log_prob_threshold=None,no_speech_threshold=None,max_new_tokens=60) if WIN else {}
W,K=(int(sys.argv[2]),int(sys.argv[3])) if len(sys.argv)>3 else (0,1)
m=WhisperModel(os.environ['WHISPER_MODEL'],device='cpu',compute_type='int8',cpu_threads=int(os.environ.get('THREADS','1')))
REC=sorted(json.load(open(os.path.join(SRC,'recordings.json'))),key=lambda r:r['order'])
todo=[r for r in REC if not os.path.exists(os.path.join(TR,r['yt']+'.jsonl.done'))]
todo=todo[W::K]+[r for k,r in enumerate(todo) if k%K!=W]   # own share first, then help with the rest
if os.environ.get('ONLY'): todo=[r for r in todo if r['yt'] in os.environ['ONLY'].split(',')]   # e.g. one recording per cloud job
files=[(r['yt'],os.path.join(DATA,r['data']) if DATA and r.get('data') else os.path.join(AUD,r['file'])) for r in todo]
def claim(vid):
    # one worker per recording: a lock file created atomically; a stale lock (dead worker) can be deleted by hand
    try: os.close(os.open(os.path.join(TR,vid+'.lock'),os.O_CREAT|os.O_EXCL|os.O_WRONLY)); return True
    except FileExistsError: return False
for vid,f in files:
    if os.path.exists(os.path.join(TR,vid+'.jsonl.done')) or not claim(vid): continue
    out=os.path.join(TR,vid+'.jsonl')
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
    nch=int(dur//600)+1
    done=-1
    if os.path.exists(out):
        L=[json.loads(l) for l in open(out)]
        if L: done=max(x['chunk'] for x in L)
        if os.path.exists(out+'.done'): continue
    t=time.time()
    with open(out,'a') as fo:
        for c in range(done+1,nch):
            raw=subprocess.run(['ffmpeg','-v','error','-ss',str(c*600),'-t','600','-i',f,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout
            a=np.frombuffer(raw,dtype=np.int16).astype(np.float32)/32768
            if len(a)<16000: continue
            step=int(WIN*16000) if WIN else len(a)
            for o in range(0,len(a),step):          # whole chunk at once, or window by window (see "window" above)
                piece=a[o:o+step]; off=c*600+o/16000
                if len(piece)<8000: continue
                segs,_=m.transcribe(piece,language=LANG,beam_size=1,condition_on_previous_text=False,word_timestamps=bool(WIN),**NOFALLBACK)
                for s in segs:
                    fo.write(json.dumps({'chunk':c,'s':round(s.start+off,2),'e':round(min(s.end,len(piece)/16000)+off,2),'t':s.text,'w':[[round(x.start+off,2),round(x.end+off,2),x.word] for x in (s.words or [])]},ensure_ascii=False)+'\n')
            fo.flush(); print(vid,'chunk',c,'/',nch,round(time.time()-t),flush=True)
    open(out+'.done','w').write('ok'); os.remove(os.path.join(TR,vid+'.lock'))
print('ALL DONE')
