# आदित्यहृदयम् (Āditya Hṛdayam)

Shelf: हिन्दू धर्म › स्तोत्र › भगवान सूर्य › आदित्यहृदयम् (`library/hinduism/stotra/surya/aditya-hridayam/`, work id
`aditya-hridayam`). The hymn to the Sun that the sage Agastya teaches Śrī Rāma on the battlefield before his last fight
with Rāvaṇa, in Sanskrit (`sa`): Śrīmad Vālmīki Rāmāyaṇa, Yuddha-kāṇḍa, sarga 105 in the Gita Press edition (107 in the
southern recension). Recited as a stotra: the viniyoga, three nyāsas, the 31 ślokas and the sarga's closing words.

## Sources
- **Text:** the owner's printout of sanskritdocuments.org, *आदित्यहृदयम्* (M. Giridhar; <https://sanskritdocuments.org>,
  file `adityahriday.itx`; private copy in scriptures-data at
  `hinduism/stotra/surya/aditya-hridayam/printouts/sanskritdocuments/adityahriday.pdf`), its recitation text (स्तोत्रपाठ).
  Checked word for word against this library's Vālmīki Rāmāyaṇa (Gita Press, `yuddha.105`), the owner's IIT Kanpur copy
  of the sarga (scriptures-data `hinduism/granth/valmiki/ramayana/printouts/iitk/`, Yuddha 107) and the recording.
  The closing words are the Gita Press book's colophon of the sarga, which the recording sings. Every choice is in
  `reconciliation.md`; `source/compare.py` prints every difference from the printout and the Gita Press sarga.
- **Meanings:** ours (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`), line by line, shown first.
- **Word meanings:** written for this library, in `library/glossary/sa.json`; the 19 words that another work's own dictionary
  already gives with the same sense (the Gītā's, the Durgā Saptaśatī's, the Vālmīki Rāmāyaṇa's) are in this work's
  `glossary/sa.json`, since the shared dictionary may not repeat a work's sense.
- **Recordings:** the owner's three, each with its speech-quality copy in scriptures-data under
  `hinduism/stotra/surya/aditya-hridayam/audio/<source>/`:
  - `sri-sathya-sai` (the default): Sri Sathya Sai Official, "Aditya Hrudayam Stotram – Prayer that Pleases the Heart of
    Sun God | Offering on Ratha Saptami Day" (YouTube `Z7W59S6fH98`): the 31 ślokas, then a closing Om śānti, which no
    written source gives, so it is not in the text and stays untimed after śloka 31.
  - `braja-beats`: Braja Beats, "Aditya Hrudaya Stotram – chanted by Lord Rama in Srimad Valmiki Ramayana" (YouTube
    `I8Xg_2RC5Vk`): the 31 ślokas and the closing words.
  - `the-sanskrit-channel`: The Sanskrit Channel, "Aditya hRdaya stOtram – Sanskrit Guided Chant & Meanings –
    Uninterrupted" (YouTube `qLXRj4HIdJA`): the title अथ श्रीआदित्यहृदयस्तोत्रम्, the 31 ślokas, then इति
    आदित्यहृदयस्तोत्रम्; the title and the closing line are not in the printout and stay untimed.
  Neither recites the viniyoga or the nyāsas, which stay untimed (`recordings.json` → `from` `sh1`). Transcripts by
  `tools/audio/transcribe_onnx.py` (Whisper small, Hindi decoding), starts by MMS (`aligned.md`).

## Files
The folder's format: `tools/works/README.md`.
- `text.txt`: the settled text, one item per śloka, the viniyoga and each nyāsa one item.
- `source/compare.py`: the word-by-word comparison with the witnesses.

## Structure
- **Hierarchy:** one part › each item its own section › the item.
- **Numbering:** a śloka's `n` is its printed number, and it is cited by it (Shloka 5); the viniyoga, the nyāsas and the
  closing words have none and are named by their type.
Items: `viniyoga` (type `viniyoga`); `rishyadi`, `kara`, `anga` (type `nyasa`: the ṛṣyādi-, kara- and
hṛdayādi-ṣaḍaṅga-nyāsa); `sh1`–`sh31` (`shloka`); `iti` (`iti`). Topics: the viniyoga and nyāsas; Agastya comes to
Śrī Rāma (1–5); the praise of the Sun (6–24); the phalaśruti (25–27, as the printout heads it); Śrī Rāma recites it and
goes to battle (28–31). Item ids are permanent.

## Introduction
The readers' introduction (`intro` in `library/index.json`, shown in ⓘ About this work) states only what these support:
- The owner's printout: the hymn is part of sarga 105 of the Yuddha-kāṇḍa (Gita Press); the setting, the battle with
  Rāvaṇa paused, Agastya teaching Rāma the praise of the Sun.
- The text itself: Agastya's words in ślokas 3–5 and 25–27 (what reciting it gives), the names of the Sun in 6–24, and
  Rāma's recitation in 28–31 (our text and meanings).
