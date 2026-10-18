"""Copy finished transcripts from the private repo (written there by its cloud workflow) into this repo.

Usage:  python3 tools/audio/sync_transcripts.py <clone of goyaldarwin/scriptures-data>

For every audio source here (tools/works/<work id>/audio/<source id>/source.json) it looks in
<data>/<work path>/audio/<source id>/transcripts/ and copies each <video id>.jsonl that is finished there
(has .jsonl.done) and not yet finished here. A finished transcript here is never overwritten. It prints what it
copied; then run tools/audio/make_timings.py for those sources.
"""
import glob, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.abspath(sys.argv[1])
copied = []
for sj in sorted(glob.glob(os.path.join(REPO, 'tools', 'works', '*', 'audio', '*', 'source.json'))):
    src = os.path.dirname(sj); meta = json.load(open(sj))
    there = os.path.join(DATA, meta['work'], 'audio', meta['id'], 'transcripts'); here = os.path.join(src, 'transcripts')
    if not os.path.isdir(there): continue
    os.makedirs(here, exist_ok=True)
    for done in sorted(glob.glob(os.path.join(there, '*.jsonl.done'))):
        vid = os.path.basename(done)[:-len('.jsonl.done')]
        if os.path.exists(os.path.join(here, vid + '.jsonl.done')): continue
        shutil.copy(os.path.join(there, vid + '.jsonl'), os.path.join(here, vid + '.jsonl'))
        shutil.copy(done, os.path.join(here, vid + '.jsonl.done'))
        stale = os.path.join(here, vid + '.align.json')
        if os.path.exists(stale): os.remove(stale)          # the alignment of a partial transcript is out of date
        copied.append(os.path.relpath(os.path.join(here, vid + '.jsonl'), REPO))
print('\n'.join(copied) if copied else 'nothing new')
