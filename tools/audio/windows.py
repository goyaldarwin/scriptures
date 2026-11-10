"""Where does a line begin? Hear a stretch of a recording in 5-s windows one second apart.

A transcript segment's start is not the line's start (the segment may open on music or on the line before), so a
start set by hand is checked this way: a window that begins at or a little before a line hears the line's first
words first (music before it is not heard as words); a window that begins after the line started hears its middle.
The last window that still begins with the line's first words is at or just before the start; the first that does
not is after it. Read the windows with the line beside them: a line that opens like its neighbour (सत्य … / सत्य …)
or a refrain sung twice needs the words after the first ones.

python3 tools/audio/windows.py <audio file> <model dir> <from s> <to s> [whisper language, default hi]
The model is Whisper small's ONNX export, as for tools/audio/transcribe_onnx.py (the int8 encoder if present).
"""
import base64, os, subprocess, sys
import numpy as np, onnxruntime as ort, librosa

audio, md, a, b = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
LANG = sys.argv[5] if len(sys.argv) > 5 else 'hi'
LANGS = ['en', 'zh', 'de', 'es', 'ru', 'ko', 'fr', 'ja', 'pt', 'tr', 'pl', 'ca', 'nl', 'ar', 'sv', 'it', 'id', 'hi', 'fi', 'vi', 'he', 'uk', 'el', 'ms', 'cs', 'ro', 'da', 'hu', 'ta', 'no', 'th', 'ur', 'hr', 'bg', 'lt', 'la', 'mi', 'ml', 'cy', 'sk', 'te', 'fa', 'lv', 'bn', 'sr', 'az', 'sl', 'kn', 'et', 'mk', 'br', 'eu', 'is', 'hy', 'ne', 'mn', 'bs', 'kk', 'sq', 'sw', 'gl', 'mr', 'pa', 'si', 'km', 'sn', 'yo', 'so', 'af', 'oc', 'ka', 'be', 'tg', 'sd', 'gu', 'am', 'yi', 'lo', 'uz', 'fo', 'ht', 'ps', 'tk', 'nn', 'mt', 'sa']
SR, HOP, N, WIN = 16000, 160, 3000, 5.0
SOT, EOT, TRANSCRIBE = 50258, 50257, 50359
so = ort.SessionOptions(); so.intra_op_num_threads = 1
e8 = md + '/small-encoder.int8.onnx'
enc = ort.InferenceSession(e8 if os.path.exists(e8) else md + '/small-encoder.onnx', so, providers=['CPUExecutionProvider'])
dec = ort.InferenceSession(md + '/small-decoder.onnx', so, providers=['CPUExecutionProvider'])
TOK = {int(i): base64.b64decode(t) for t, i in (l.split() for l in open(md + '/small-tokens.txt'))}
MEL = librosa.filters.mel(sr=SR, n_fft=400, n_mels=80)

def logmel(x):
    x = np.pad(x, (0, max(0, N * HOP - len(x))))[:N * HOP]
    st = librosa.stft(x, n_fft=400, hop_length=HOP, window='hann', center=True)[:, :N]
    m = np.log10(np.maximum(MEL @ (np.abs(st) ** 2), 1e-10)); m = np.maximum(m, m.max() - 8.0)
    return ((m + 4.0) / 4.0)[None].astype(np.float32)

def piece(x):
    """Greedy decode of one window (no timestamps) → text."""
    ck, cv = enc.run(None, {'mel': logmel(x)})
    sk = np.zeros((12, 1, 448, 768), np.float32); sv = np.zeros_like(sk)
    toks = [SOT, 50259 + LANGS.index(LANG), TRANSCRIBE, 50363]; off = 0; out = []
    while len(out) < 40:
        lg, sk, sv = dec.run(None, {'tokens': np.array([toks], np.int64), 'in_n_layer_self_k_cache': sk, 'in_n_layer_self_v_cache': sv,
                                    'n_layer_cross_k': ck, 'n_layer_cross_v': cv, 'offset': np.array([off], np.int64)})
        off += len(toks); l = lg[0, -1]; l[EOT + 1:] = -np.inf; t = int(l.argmax())
        if t == EOT: break
        out.append(t); toks = [t]
        rep = next((p for p in range(1, 16) if len(out) >= 2 * p and out[-p:] == out[-2 * p:-p]), 0)
        if rep and (rep > 3 or len(out) >= 3 * rep and out[-rep:] == out[-3 * rep:-2 * rep]): del out[-rep:]; break
    return b''.join(TOK.get(t, b'') for t in out).decode('utf-8', 'ignore').strip()

a = max(0.0, a)
pcm = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-ss', str(a), '-to', str(b + WIN), '-i', audio,
                      '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
t = a
while t <= b + 1e-6:
    print(f'{t:9.1f}  {piece(x[int((t - a) * SR): int((t - a + WIN) * SR)])}', flush=True); t += 1.0
