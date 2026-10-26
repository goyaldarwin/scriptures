# Reconciliation: आरती कीजे श्रीरामलला की

## Source
The owner's printout (PDF) of jansatta.com, "श्री रामचंद्र जी की आरती, श्री राम चंद्र कृपालु भजमन हरण भव भय दारुणम्…" (Shivani Singh, updated 20 December 2024):
https://www.jansatta.com/religion/shri-ram-ji-ki-aarti-lyrics-in-hindi-ram-siya-ram-siya-ram-jay-jay-ram-lyrics-in-hindi/3170131/
It gives three āratīs: "श्री राम आरती" (the stuti श्रीरामचन्द्र कृपालु, followed by two verses of the Mānas), "श्री राम की दूसरी आरती" (आरती कीजे श्रीरामलला की) and "श्री राम की तीसरी आरती" (आरती कीजै रामचन्द्र जी की). It is the only witness for these texts. The three are separate works (the owner: "the 3 ram aarti's are independent of each other"). Copy for `scriptures-data`: `hinduism/aarti/rama/ram-aarti/printouts/jansatta/` (not there yet).

How it is read: the PDF's text layer (the page's own Unicode text), checked against the page images. A pop-up covers the first line of pages 3 and 4 in the images; those lines are read from the text layer by position (`pdftotext -bbox`), where the menu words that overlap them sit on a different baseline.

The rule, as for the Dhūpa Āratī: keep the source; correct it only where it is clearly wrong (a typing slip, a broken word, a sense that does not fit). Every correction is below. The library's writing standard (docs/PLAYBOOK.md §3) everywhere: ।/॥ for the daṇḍas, stanzas numbered (॥१॥); the refrain (टेक) shown once although it is sung after each stanza, hyphens only inside compounds (the page's spaced dashes " – " are written "-").

## 2. आरती कीजे श्रीरामलला की (language Awadhi, `awa`)
The page prints 18 lines, each a caupāī (two half-lines of 16 mātrās). The first is the refrain (टेक); the other 17 are numbered caupāīs 1–17.

| Line | Page | Ours | Why |
|---|---|---|---|
| टेक | पूण निपुण | पूरण निपुण | Broken word; पूरण makes the half-line 16 mātrās. |
| 1 | धनुष वान | धनुष बान | Typing slip: बान (arrow); वान is not a word here. |
| 5 | बखानैं (no end mark) | बखानैं ॥ | The line's closing dandas are missing. |
| 16 | कवनव भेदा | कवनउ भेदा | कवनव is not a word; कवनउ ("any at all") gives the sense "keeping no distinction" and the same 16 mātrās. **Open.** |

Kept as the page has them: कीजे, धनुवेद, शोभा, वाम, शिव, शेष, यश (the page mixes श and स, व and ब; we did not regularise them), महु, बधाये, नैवेदा, नहि, तिहुपुर, विभीषन, दुःख.

## Meanings
Our own (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`), one per verse, because the page gives none. The meaning of "मन दृढ़ करि नहि कवनउ भेदा" is an interpretation.
