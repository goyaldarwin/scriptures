# Shabad Guru (Kirtan)

Kirtan in raag from the YouTube channel Shabad Guru: one shabad (or a salok with its vaar stanza, or a bani) per video,
timed line by line (`tools/audio/METHOD.md`, "Line by line"). `recordings.json` is made by `make_recordings.py` from the
channel's table in `scriptures-data` (`sikhism/gurbani/guru-granth-sahib/printouts/shabad-guru/videos.csv`); the
recordings are in `scriptures-data` at `sikhism/gurbani/guru-granth-sahib/audio/shabad-guru/`. How the starts were made
and what is listed to check: `aligned.md`; hand-set data and starts heard in 5-s windows: `fixes.md`.

## Videos left out

A verse sung in two videos alike (the same song, the lines MMS found in both largely the same) keeps the video MMS fits
best (the most lines found); the other is left out (`make_recordings.py` → `DROP`):

| Verse | Kept | Left out | Lines found (kept, left out) |
|---|---|---|---|
| 41.2 ਰਸੁ ਅੰਮ੍ਰਿਤੁ ਨਾਮੁ ਰਸੁ ਅਤਿ ਭਲਾ | gl1Afsh1UBI | u3MgY7-tOq0 | 13, 10 (64% the same lines) |
| 353.3 ਕਿਸ ਕਉ ਕਹਹਿ ਸੁਣਾਵਹਿ ਕਿਸ ਕਉ | ElGxkIy-ipw | zkEKqNFvmhM | 14, 4 (both titled with its first line) |
| 528.1 ਹਰਿ ਗੁਣ ਗਾਵੈ ਹਉ ਤਿਸੁ ਬਲਿਹਾਰੀ | 99BzjWIfuyw | IDDWa0LeJfw | 1, 1 (the same line; one video with the raag in its title, both 110 s) |

Videos of the same verse that sing different parts of it (a chhant's stanzas: 80.1, 577.1, 704.1, 926.1; 374.2 and
1321.3) are all kept; the app plays them in turn. The Anand Sahib's two videos (917.1–922.6, 12 and 55 minutes) are both
kept.

## Long videos

Three videos longer than 40 minutes are aligned in overlapping 8-minute pieces (METHOD.md): QiPepd5nRs8 (the Anand
Sahib, 55 min, 66% of its lines found), 0R00aEoBFek (the Oankar, 929.9–938.1, 84 min, 52%) and -k1q_bxnErk (the Sidh
Gosht, 938.2–946.6, 75 min, 63%); in each, the first singings of the verses come in the bani's order.
