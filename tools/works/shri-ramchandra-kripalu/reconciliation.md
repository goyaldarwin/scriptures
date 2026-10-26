# Reconciliation: श्रीरामचन्द्र कृपालु

## Source
The owner's printout (PDF) of jansatta.com, "श्री रामचंद्र जी की आरती, श्री राम चंद्र कृपालु भजमन हरण भव भय दारुणम्…" (Shivani Singh, updated 20 December 2024):
https://www.jansatta.com/religion/shri-ram-ji-ki-aarti-lyrics-in-hindi-ram-siya-ram-siya-ram-jay-jay-ram-lyrics-in-hindi/3170131/
It gives three āratīs: "श्री राम आरती" (the stuti श्रीरामचन्द्र कृपालु, followed by two verses of the Mānas), "श्री राम की दूसरी आरती" (आरती कीजे श्रीरामलला की) and "श्री राम की तीसरी आरती" (आरती कीजै रामचन्द्र जी की). It is the only witness for these texts. The three are separate works (the owner: "the 3 ram aarti's are independent of each other"). Copy for `scriptures-data`: `hinduism/aarti/rama/ram-aarti/printouts/jansatta/` (not there yet).

How it is read: the PDF's text layer (the page's own Unicode text), checked against the page images. A pop-up covers the first line of pages 3 and 4 in the images; those lines are read from the text layer by position (`pdftotext -bbox`), where the menu words that overlap them sit on a different baseline.

The rule, as for the Dhūpa Āratī: keep the source; correct it only where it is clearly wrong (a typing slip, a broken word, a sense that does not fit). Every correction is below. The library's writing standard (docs/PLAYBOOK.md §3) everywhere: ।/॥ for the daṇḍas, stanzas numbered (॥१॥); the refrain (टेक) shown once although it is sung after each stanza, hyphens only inside compounds (the page's spaced dashes " – " are written "-").

## 1. श्रीरामचन्द्र कृपालु (Tulasīdāsa's stuti, from the Vinaya-patrikā; language Braj, `bra`)
The page prints five two-line stanzas. Corrections (one witness, so each is **open**: to confirm against a printed Vinaya-patrikā, e.g. Gita Press, when the owner can share one):

| Stanza | Page | Ours | Why |
|---|---|---|---|
| 2 | जनक सुतवरं | जनक सुता वरं | "सुतवरं" (best of sons) does not fit: the line bows to the husband (वर) of Janaka's daughter (सुता). |
| 3 | निकन्दंन | निकंदनं | Broken word (anusvāra misplaced); the stanza's other lines end in -नं. |
| 3 | रधुनन्द | रघुनंद | Typing slip (ध for घ). |
| 3 | कौशलचन्द | कोशलचन्द | Kośala is Rāma's kingdom; कौशल means "skill", which does not fit. |
| 4 | सिरा | सिर | Typing slip ("on the head"). |
| 4 | चारू | चारु | Spelling of the Sanskrit word ("lovely"). |
| 4 | विभूषां | विभूषणं | Broken word; the rhyme of the stuti is -णं / -नं. |
| 4 | सग्राम | संग्राम | Missing anusvāra ("battle"). |
| 4 | खरदूषणमं | खरदूषणं | Broken ending. |
| 5 | हृदय-कंच | हृदय-कंज | Typing slip: the lotus (कंज) of the heart, the stuti's image throughout. |

Kept as the page has them: भजु, दारुणं, कंदर्प, छबि, तडित, उदारु, the compounds and their hyphens.

### The two Mānas verses after the stuti
The page goes on with "मनु जाहिं राचेउ…" and the dohā "जानि गौरी अनुकूल…". These are the Mānas's Bāla-kāṇḍa chhand 236 and sorathā 236 (the page calls the sorathā a dohā). They are taken from our Mānas text (Gita Press), `[manas bal.236.cha1]` and `[manas bal.236.so236]`, never copied from the page, which has several slips: मिलहि (मिलिहि), सिलु (सीलु), एही (एहि), सिया (सिय), पूजी पुनिपुनि (पूजि पुनि पुनि), मन्दिरचली (मंदिर चली), गौरी (गौरि). Their meanings are the Mānas's: Gita Press in both languages, because our own Mānas meanings do not cover Bāla 236 yet; the exporter takes ours there once they do.

## Meanings
Our own (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`) for the stuti's five chhandas, because the page gives none. The two Mānas verses have the Mānas's meanings (above).
