# Kirtan (Shabad Guru, Har Ki Oat, Gurmat Sangeet Darbar, Sehaj Path Kirtan)

The Granth's one kirtan source: every singer's recordings together, so a reader hears kirtan of every shabad that has one
without choosing a singer (`docs/PLAYBOOK.md` §8). The folder keeps its first channel's id, `shabad-guru`. Timed line by
line (`tools/audio/METHOD.md`, "Line by line"). `recordings.json` is made by `make_recordings.py` from the channels' tables
in `scriptures-data` (`sikhism/gurbani/guru-granth-sahib/printouts/<channel>/videos.csv`); each recording's `data` names
its file there (`sikhism/gurbani/guru-granth-sahib/audio/<channel>/`). How the starts were made and what is listed to
check: `aligned.md`; hand-set data and starts heard in 5-s windows: `fixes.md`.

| Channel | Recordings | What |
|---|---|---|
| Shabad Guru | 3363 | kirtan in raag, one shabad (or a salok with its vaar stanza, or a bani) per video |
| Har Ki Oat (Sri Darbar Sahib's hazuri ragis) | 50 | one item each, of the items Shabad Guru has no kirtan of (`../kirtan_recordings.py`) |
| Gurmat Sangeet Darbar | 13 | the same |
| Sehaj Path Kirtan (Bhai Parminder Singh, Bhai Jagjit Singh) | 7 | Ang 1353–1429 sung through, which Shabad Guru has no kirtan of (below) |

The other channels' videos of items Shabad Guru already sings are listed in `scriptures-data`, not used
(`printouts/<channel>/downloads.csv`).

## Videos left out

Twelve videos are not used and their audio is not kept in `scriptures-data` (the owner: the kirtan already here is enough): four whose title matches two shabads (YeAKLlAi5J4 and wIn9KsRHjjU: 32.1 or 64.2; blBZnwmAuBQ: 250.1 or 262.1; MCuHvD9UGQU: 522.1 or 524.2), six whose title matches no verse (C4k7dRTPHaY, Eh3J-L4ad7c, HSd1RzdBEPY, NlGUvGHOMQU, RGrLDJOmOQk, wIKmZXWnxeM) and the channel's two trailers (fQfO-SITz_c, p0zWiXiyaJY).


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

## Sehaj Path Kirtan's tracks

Each track starts at the heading of the banis its title names (`../kirtan_recordings.py`, `SPK`); the four over 40 minutes
(34, 35, 37, 38) are aligned in overlapping 8-minute pieces. The Raag Mala (1429.13) is in none.

| Track | Video | Items | Banis |
|---|---|---|---|
| 34 | n7URwrfz4Rk | 1353.1–1364.9 | Salok Sahaskriti (Mahalla 1 and 5), Gatha, Phunhe, Chaubole |
| 35 | a5b1rLmEhCA | 1364.10–1377.12 | Salok Bhagat Kabir |
| 36 | 9D8RHUl1o3s | 1377.13–1384.19 | Salok Sheikh Farid |
| 37 | VOHKq_zLdls | 1385.1–1409.6 | the Savaiye |
| 38 | 7SQfAZdZMUA | 1410.1–1426.7 | Salok Varan te Vadheek |
| 39 | f49qLLK8mPE | 1426.8–1429.10 | Salok Mahalla 9 |
| 40 | 3U383GeE7Fw | 1429.11–1429.12 | Mundavani, Salok Mahalla 5 |
