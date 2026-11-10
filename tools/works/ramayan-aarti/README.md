# आरति श्रीरामायनजी की (Ārati Śrīrāmāyanajī Kī)

The āratī of the Śrī Rāmacaritamānasa in Awadhi (`awa`), in a refrain and four stanzas, sung at the end of a pārāyaṇa of the Mānas. The Mānas's 30-day and 9-day plans list it after their last day ("Śrī Rāmāyaṇajī kī Āratī"); there it opens this work, so it plays with the Mānas's recording.

- **Text** (`text.txt`, made by `source/make.py`): the āratī printed at the end of the owner's Gita Press Mānas (`scriptures-data`: `hinduism/granth/tulsidas/ramcharitmanas/books/gitapress/hindi.pdf`), taken line by line from the Mānas's own extraction of that page (`tools/works/manas/book.json` → `vidhi.aarti`), so the two never differ. Every choice: `reconciliation.md`.
- **Meanings:** ours (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`); Gita Press prints no meaning of the āratī.
- **Word meanings:** the Awadhi dictionary (`library/glossary/awa.json`), which already had every word from the Mānas's āratī page.
- **Recording:** Pt. Kamlesh Upadhyay "Haripuri" (`audio/kamlesh-upadhyay`), the end of the 30th day of his Māsa-pārāyaṇa of the Mānas (YouTube `Yi9TFXQYL-4`, 55:12–57:37; the audio in `scriptures-data` at `hinduism/granth/tulsidas/ramcharitmanas/audio/kamlesh-upadhyay/masa-30_Yi9TFXQYL-4.opus`). Its transcript is the āratī's stretch (3300 s on) of the Mānas's transcript of the same video; the starts: `fixes.md`, `aligned.md`.

Verse types: टेक (refrain, `tek`, shown once at the start although it is sung after every stanza) and पद (stanza, `pad`). The folder's format: `tools/works/README.md`.

## Structure
- **Hierarchy:** one part (Aarti Shri Ramayanji Ki) › one section (`aarti`) › verses: the refrain (`aarti.tek`, type `tek`) and four stanzas (`aarti.pad1`–`pad4`, type `pad`), each of four printed lines.
- **Numbering:** each stanza's `n` is its number, and it is cited by it ("Stanza 3"); the book prints no numbers, so none is printed in the verse. The refrain has none.
- **Topics:** one, the āratī's title. **Reading plans:** none.

## Introduction
The readers' introduction (`intro` in `library/index.json`, shown in ⓘ About this work) states only what these support:
- The text itself (our text and meanings).
- The Gita Press Mānas, which prints it at the end of the book under the heading श्रीरामायणजीकी आरती.
- The recording: the āratī sung at the end of the 30th day of Pt. Kamlesh Upadhyay's Māsa-pārāyaṇa.
