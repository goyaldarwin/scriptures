# Kaṭha Upaniṣad — how the text was settled

## The source and its limits (2026-10-26)
The owner's book (Swami Gurubhaktananda, Sandeepany Text 20) prints every mantra three times: in Devanagari (font "BRH Devanagari"), in IAST, and as the author's word-by-word. The Devanagari text layer is the font's own byte codes (`Á EzÉlÉç Wû uÉæ …`) and cannot be read; the IAST layer is clean once sixteen Latin-1 symbols the font uses for the accented letters are decoded (`¡` ā, `£` e, `µ` o, `¯` ṃ, `§` ī, `¾` ś, `»` ṛ, `¦` ḥ, `½` ṣ, `³` ṇ, `°` m̐, `À` ū, `¿` ṭ, `±` ṅ, `²` ñ, `¢` ḍ; the avagraha comes out as `:'`). The text is therefore the book's transliteration converted letter for letter to Devanagari (`source/settle.py` → `iast2deva`). The conversion is deterministic: every IAST letter has exactly one Devanagari spelling, and anusvāra (ṃ) and candrabindu (m̐) are kept as the book writes them.

## The witnesses
- **shlokam.org** (<https://shlokam.org/text/kathopanishad.htm>): the page serves mantras 1.1.1–1.1.20 and the śānti mantra to a reader (the rest loads only in a browser). These 21 verses are in `source/witness/shlokam-1.1.1-20.txt`, and `check.py` finds **no difference** in words between them and our text. The two sources are independent (the book's IAST, the site's Devanagari), so this agreement is the check that the decoding and the conversion are right.
- **sanskritdocuments.org** (`doc_upanishhat/katha.html`): the standard Devanagari text, 119 mantras in six vallīs, as counted above. To be added to `source/witness/` when the owner provides the file (the session cannot download it); `check.py` then compares every verse.

## Decisions
- **Mantra count and numbering.** The standard count: 1.1 (29), 1.2 (25), 1.3 (17), 2.1 (15), 2.2 (15), 2.3 (18). The book numbers the closing śānti mantra as 2.3.19; it is the same सह नाववतु as the opening, and is item `shanti.2`.
- **Line division** follows the book (which follows the metre): two lines for an anuṣṭubh, four for a triṣṭubh; a word broken across lines keeps the hyphen at the line end, as the witnesses print it (1.1.9 मे-/ऽनश्नन्, 1.1.20, 1.2.1, 1.2.20, 2.1.2, 2.2.2, 2.3.16, 2.3.18). The refrain एतद्वै तत् is on its own line when the book sets it so (2.1.3, 2.1.5 …) and at the end of the last line where the book puts it there (2.3.1). 1.3.17 has three lines as in the book.
- **Punctuation.** The book's `|` and `||` become । and ।।; each mantra's last line ends with its number within the vallī in Devanagari digits (।।१।।). The book's two commas (1.1.1 after वाजश्रवसः, 1.3.14 after जाग्रत) are the author's and are dropped.
- **ॐ** is written with the sign ॐ (as shlokam.org), the book's `om̐`.
- **Candrabindu** (तँ ह, कुमारँ, किँ स्वित्, सुखँ, हँसः …): kept where the book's IAST has `m̐` (the font's `°`), which is exactly where shlokam.org has ँ.
- **Transliteration `t`** is made back from the settled Devanagari in the library's convention (ṁ for anusvāra, ’ for the avagraha, ॥N॥), so it always spells the text; `check.py` proves it.

## Open
- Full-text witness from sanskritdocuments.org (above).
