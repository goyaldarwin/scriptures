# Śrī Rāmacaritamānasa — reconciliation

**Witnesses.** The owner's two Gita Press (Gorakhpur) editions, read by the scripts in `source/` (`source/README.md`):
- **H**, the Hindi edition with Hanumānprasād Poddār's bhāvārtha: its glyphs decoded to Unicode, page by page; this is the text.
- **E**, the English edition: its transliteration of every verse, converted back to Devanagari (`source/tr2dev.py`) and compared with H word by word (`source/verify.py` → `source/verify_tr.json`).
- **O**, an OCR reading of H's pages (`source/ocr.sh`, `source/verify_ocr.py` → `source/verify_ocr.json`), to catch decoding slips.

**Choices.**

| Where | Choice |
|---|---|
| H and E differ in a word | H stands, unless the difference is a misprint or a decoding slip in H; then E's reading is taken. Each such correction is in `source/text_fixes.json` (`{verse id: [[H's reading, the corrected one]]}`), 30 in all; every one is a place where E reads the corrected form (`source/verify_tr.json`), e.g. रधुनाथ → रघुनाथ (`sundar.49.do49ख`), विरहँ → बिरहँ (`ayodhya.80.do80`, O flags it too), शुभम → शुभम् (`uttar.end.shloka2`). The other differences in `source/verify_tr.json` (about 215) are slips of E's transliteration or of its conversion back (र् अघुपति, छोते), or E's own spelling where H's is kept (निशिचर, निर्गुण, सिरु). |
| Joint caupāīs | Where H prints two or three caupāīs as one (॥३-५॥), each is its own verse, split where E numbers each caupāī (the owner's rule: one caupāī per verse; `source/make.py`). |
| Language of a verse | Awadhi (`awa`); Sanskrit (`sa`) for every śloka and the stutis in Sanskrit (Atri's, Sutīkṣṇa's, the Rudrāṣṭaka), as listed in `source/make.py`. |
| Kathā-visarjana (in the vidhi) | Not in either edition: typed from the owner's printed page; its readings kept as printed and its three corrected typesetting slips, **open** for the owner to confirm, are in `source/visarjan.md`. |

A new correction goes in `source/text_fixes.json` with the witness that supports it; then `source/README.md` → "Text corrections".
