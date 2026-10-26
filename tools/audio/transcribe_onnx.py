"""Transcribe one recording with Whisper small (ONNX export from github.com/k2-fsa/sherpa-onnx,
release "asr-models", sherpa-onnx-whisper-small.tar.bz2) into the transcript format that
tools/audio/align.py reads: one JSON line per segment {"s", "e", "t"}.

Use it instead of tools/audio/transcribe.py when Hugging Face (where faster-whisper's model comes from)
cannot be reached; this model comes from GitHub. sherpa-onnx's own decoder decodes each
token separately and loses Devanagari bytes, so this script runs the ONNX encoder/decoder itself
(greedy) and decodes the byte tokens together. Whisper gives no timestamps inside a chant, so the
recording is cut into 4–9 s pieces at its quietest points and each piece is one segment.

python3 tools/audio/transcribe_onnx.py <audio file> <model dir> <out .jsonl> [whisper language, default hi]
Needs onnxruntime, librosa, numpy, ffmpeg. About 1× real time on 2 cores.
"""
import base64, json, subprocess, sys
import numpy as np, onnxruntime as ort, librosa

audio, md, out = sys.argv[1:4]; LANG = sys.argv[4] if len(sys.argv) > 4 else 'hi'
LANGS = ['en', 'zh', 'de', 'es', 'ru', 'ko', 'fr', 'ja', 'pt', 'tr', 'pl', 'ca', 'nl', 'ar', 'sv', 'it', 'id', 'hi', 'fi', 'vi', 'he', 'uk', 'el', 'ms', 'cs', 'ro', 'da', 'hu', 'ta', 'no', 'th', 'ur', 'hr', 'bg', 'lt', 'la', 'mi', 'ml', 'cy', 'sk', 'te', 'fa', 'lv', 'bn', 'sr', 'az', 'sl', 'kn', 'et', 'mk', 'br', 'eu', 'is', 'hy', 'ne', 'mn', 'bs', 'kk', 'sq', 'sw', 'gl', 'mr', 'pa', 'si', 'km', 'sn', 'yo', 'so', 'af', 'oc', 'ka', 'be', 'tg', 'sd', 'gu', 'am', 'yi', 'lo', 'uz', 'fo', 'ht', 'ps', 'tk', 'nn', 'mt', 'sa']
SR, HOP, N = 16000, 160, 3000                     # 30 s windows of 10 ms frames
SOT, EOT, TRANSCRIBE, TS0 = 50258, 50257, 50359, 50364
enc = ort.InferenceSession(md + '/small-encoder.onnx', providers=['CPUExecutionProvider'])
dec = ort.InferenceSession(md + '/small-decoder.onnx', providers=['CPUExecutionProvider'])
TOK = {}
for line in open(md + '/small-tokens.txt'):
    b, i = line.split(); TOK[int(i)] = base64.b64decode(b)
MEL = librosa.filters.mel(sr=SR, n_fft=400, n_mels=80)

pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', audio, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768

def logmel(a):
    a = np.pad(a, (0, max(0, N * HOP - len(a))))[:N * HOP]
    st = librosa.stft(a, n_fft=400, hop_length=HOP, window='hann', center=True)[:, :N]
    m = np.log10(np.maximum(MEL @ (np.abs(st) ** 2), 1e-10)); m = np.maximum(m, m.max() - 8.0)
    return ((m + 4.0) / 4.0)[None].astype(np.float32)

def cuts(x, lo=4.0, hi=9.0):
    """Cut points (samples) at the quietest 50 ms frame 4–9 s after the previous cut: a chant has no
    clean silences (drone, group voices), but it dips between half-lines."""
    fr = SR // 20; e = np.sqrt(np.convolve((x[:len(x) // fr * fr].reshape(-1, fr) ** 2).mean(1), np.ones(5) / 5, 'same'))
    out, c = [0], 0
    while c + hi * 20 < len(e):
        a, b = c + int(lo * 20), c + int(hi * 20); c = a + int(e[a:b].argmin()); out.append(c * fr)
    return out + [len(x)]

def piece(a):
    """Greedy decode of one short piece (no timestamps) → text."""
    ck, cv = enc.run(None, {'mel': logmel(a)})
    sk = np.zeros((12, 1, 448, 768), np.float32); sv = np.zeros_like(sk)
    toks = [SOT, 50259 + LANGS.index(LANG), TRANSCRIBE, 50363]; off = 0; outt = []
    while len(outt) < 120:
        lg, sk, sv = dec.run(None, {'tokens': np.array([toks], np.int64), 'in_n_layer_self_k_cache': sk, 'in_n_layer_self_v_cache': sv,
                                    'n_layer_cross_k': ck, 'n_layer_cross_v': cv, 'offset': np.array([off], np.int64)})
        off += len(toks); l = lg[0, -1]; l[EOT + 1:] = -np.inf
        t = int(l.argmax())
        if t == EOT: break
        outt.append(t); toks = [t]
        rep = next((p for p in range(1, 16) if len(outt) >= 2 * p and outt[-p:] == outt[-2 * p:-p]), 0)
        if rep and (rep > 3 or len(outt) >= 3 * rep and outt[-rep:] == outt[-3 * rep:-2 * rep]):   # a phrase repeating itself
            del outt[-rep:]; break
    return b''.join(TOK.get(t, b'') for t in outt).decode('utf-8', 'ignore').strip()

C = cuts(x); n = 0
with open(out, 'w') as f:
    for a, b in zip(C, C[1:]):
        t = piece(x[a:b])
        if t: f.write(json.dumps({'s': round(a / SR, 2), 'e': round(b / SR, 2), 't': ' ' + t}, ensure_ascii=False) + '\n'); f.flush(); n += 1
print(n, 'segments of', len(C) - 1)
