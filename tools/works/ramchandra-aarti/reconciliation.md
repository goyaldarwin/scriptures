# Reconciliation: आरती कीजै रामचन्द्र जी की

## Source
The owner's printout (PDF) of jansatta.com, "श्री रामचंद्र जी की आरती, श्री राम चंद्र कृपालु भजमन हरण भव भय दारुणम्…" (Shivani Singh, updated 20 December 2024):
https://www.jansatta.com/religion/shri-ram-ji-ki-aarti-lyrics-in-hindi-ram-siya-ram-siya-ram-jay-jay-ram-lyrics-in-hindi/3170131/
It gives three āratīs: "श्री राम आरती" (the stuti श्रीरामचन्द्र कृपालु, followed by two verses of the Mānas), "श्री राम की दूसरी आरती" (आरती कीजे श्रीरामलला की) and "श्री राम की तीसरी आरती" (आरती कीजै रामचन्द्र जी की). It is the only witness for these texts. The three are separate works (the owner: "the 3 ram aarti's are independent of each other"). Copy for `scriptures-data`: `hinduism/aarti/rama/ramchandra-aarti/printouts/jansatta/` (not there yet).

How it is read: the PDF's text layer (the page's own Unicode text), checked against the page images. A pop-up covers the first line of pages 3 and 4 in the images; those lines are read from the text layer by position (`pdftotext -bbox`), where the menu words that overlap them sit on a different baseline.

The rule (docs/PLAYBOOK.md §2): keep the source; correct it only where it is clearly wrong (a typing slip, a broken word, a sense that does not fit). Every correction is below. The library's writing standard (docs/PLAYBOOK.md §3) everywhere: ।/॥ for the daṇḍas, stanzas numbered (॥१॥); the refrain (टेक) shown once although it is sung after each stanza, hyphens only inside compounds (the page's spaced dashes " – " are written "-").

## 3. आरती कीजै रामचन्द्र जी की (language Hindi, `hi`)
A refrain and five stanzas of two lines; the last names Nāmadeva. Corrections:

| Stanza | Page | Ours | Why |
|---|---|---|---|
| 3 | रत्‍‌न | रत्न | The page's word carries invisible joiner characters (U+200D, U+200C); removed. |

Kept: लाये, चहुं, पांचवीं, गावें, and "काली नाग नाथ" (the serpent Kāliya tamed, as the line means; our word meanings give काली and नाथ that sense in this work only, `glossary/hi.json`).

## Meanings
Our own (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`), one per verse, because the page gives none. The meaning of the Kāliya line, with "नाथ" as "tamed with a nose-rope", is an interpretation.
