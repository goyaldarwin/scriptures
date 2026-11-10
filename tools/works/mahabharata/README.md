# महाभारत (Mahabharat)

Shelf: हिन्दू धर्म › ग्रन्थ › महर्षि वेदव्यास › महाभारत (`library/hinduism/granth/vyasa/mahabharata/`, work id `mahabharata`). The Mahābhārata of Maharṣi Vedavyāsa in its eighteen parvas, as printed by Gita Press, Gorakhpur, with its simple Hindi translation: 83,926 numbered verses and prose passages, 6,755 verses of the southern (dākṣiṇātya) reading that the book prints among them, in 2,107 adhyāyas, in Sanskrit (`sa`).

| Part | Parva | Adhyāyas | Numbered | Dākṣiṇātya |
|---|---|---|---|---|
| 1 | Ādi | 233 | 8,540 | 758 |
| 2 | Sabhā | 81 | 2,711 | 1,243 |
| 3 | Vana | 315 (and its श्रवण-महिमा) | 11,852 | 123 |
| 4 | Virāṭa | 72 (and its श्रवण-महिमा) | 2,279 | 284 |
| 5 | Udyoga | 196 | 6,613 | 84 |
| 6 | Bhīṣma | 122 (and its श्रवणमहिमा) | 5,874 | 108 |
| 7 | Droṇa | 202 | 9,631 | 152 |
| 8 | Karṇa | 96 | 5,017 | 174 |
| 9 | Śalya | 65 | 3,638 | 52 |
| 10 | Sauptika | 18 | 803 | 2 |
| 11 | Strī | 27 | 825 | 1 |
| 12 | Śānti | 365 | 13,765 | 454 |
| 13 | Anuśāsana | 168 | 7,674 | 2,070 |
| 14 | Āśvamedhika | 92 | 2,842 | 1,243 |
| 15 | Āśramavāsika | 39 | 1,089 | 3 |
| 16 | Mausala | 8 | 287 | 4 |
| 17 | Mahāprasthānika | 3 | 110 | 0 |
| 18 | Svargārohaṇa | 5 (and the Bhārata-śravaṇa-vidhi and Māhātmya) | 376 | 0 |

(`source/check.md`, made with the text, gives the exact counts of every kind.)

## Sources
- **Text and Hindi meaning:** the owner's Gita Press *Mahābhārata, saral Hindī-anuvādasahit*, parts 1–6 (codes 32–37, the 2017 e-books), in `scriptures-data` at `hinduism/granth/vyasa/mahabharata/books/gitapress/bhag-1.epub` … `bhag-6.epub`. The e-books carry Unicode text, so the text is read as it is, never by OCR (`source/epub.py`): calibre names its styles afresh in each volume, so every block is classed by its resolved style (font, size, alignment, margins), and every block that fits no class is logged and was read.
- **Meanings:** Gita Press's Hindi (`meanings/hi/gitapress.json`), copied as printed, with the book's footnotes. No English, no word meanings yet (`"words": "partial"`, the owner's choice: the verses and Hindi first; English, word meanings and recordings later).

## Sources and permissions
The Gita Press e-books are the owner's, used for personal study; the text and the Hindi are shown as published. No permission has been requested from Gita Press.

## Structure
- **Hierarchy:** eighteen parts (the parvas: Adi Parv … Swargarohan Parv) › adhyāyas (sections `1.1` … `18.5`, numbered as the book numbers them in each parva, through its sub-parvas; `work.json` → `cite.sec` names them "Adhyay" / "अध्याय") › verses. Five closing pieces with no adhyāya number are sections of their own, named in `work.json` → `sections`: the hearing's merit after the Vana, Virāṭa and Bhīṣma parvas (`3.mahima`, `4.mahima`, `6.mahima`), and after the Svargārohaṇa the Bhārata-śravaṇa-vidhi (`18.vidhi`) and the Mahābhārata-māhātmya (`18.mahatmya`).
- **Numbering:** a verse's id is `<parva>.<adhyāya>.<verse>` with the book's numbers (`1.1.1`, `6.25.1`); its `n` is the number that ends it (॥१॥; a half verse ॥१६½॥ is `16½`, id `3.176.16h`). A verse is cited parva.adhyāya.verse (`work.json` → `cite`: "Shloka 6.25.1"). Unnumbered items are named by their type and have ids by place: a dākṣiṇātya verse `<p>.<a>.<n>d<k>` (the k-th after verse n, 0 before the first), the opening verse of a parva `<p>.<a>.0` (नारायणं नमस्कृत्य …) and the Ādiparva's opening invocation `1.1.om`, the closing words `<p>.<a>.iti`, a closing piece's unnumbered verses `<p>.<piece>.u<k>`.
- **Types:** `shloka`; `gadya` (Sanskrit prose, one item per numbered passage); `dshloka`, `dgadya` (the dākṣiṇātya reading: printed by the book in ( … ) or, in the long passages of the Anuśāsana and Āśvamedhika, without brackets, always without a number; the book counts them under each adhyāya, "दाक्षिणात्य अधिक पाठके … श्लोक"); `mangalacharan` (the opening verse and invocation); `iti` (the closing words, with the book's Hindi closing words as their meaning).
- **Lines:** as the e-book prints them: one per half-verse for anuṣṭubh, one per pāda for longer metres. A speaker's line (सौतिरुवाच, वैशम्पायन उवाच) is a line of the verse it opens, or stands where the book prints it inside a verse.
- **Topics:** each adhyāya's Hindi title as printed (the Gītā's adhyāyas with the book's "(श्रीमद्भगवद्गीतायां प्रथमोऽध्यायः)" before it); in English its sub-parva and number ("Paulom Parv · Adhyay 5", `source/upaparva_en.tsv`) until English headings are written. The book's bracketed headings inside a few long dākṣiṇātya passages (95) are not shown yet.
- **Meanings:** each of the book's Hindi paragraphs sits under the last verse its mark names (॥ ९—११ ॥ under 11), else under the last verse before it; a paragraph printed before its verse ends (॥ ८½ ॥) joins the next one; every mark is kept as printed. The book's notes go under the meaning that carries their mark (१. …, as printed), or, for a mark in a verse line, under that verse's meaning. The Gītā's "सम्बन्ध—" paragraphs (215, linking a verse to the ones before) are notes on the meaning of the verse they introduce. **Loading:** by part, the verses too (`"load": "parts"`, `"verses": "parts"`: the verses alone are 44 MB).
- **Reading plan:** none (the owner's choice; the book prints no day-wise method).
- **The Śrīmad Bhagavad Gītā** is Bhīṣma 25–42 here, as Gita Press prints it in the Mahābhārata; the library's own Gītā (`granth/vyasa/bhagavad-gita`) is a separate work from another source, and neither takes from the other.

## How it is made
Run from an empty working folder; the steps write `v1.json` … `v6.json` there.
```bash
S=<this repository>/tools/works/mahabharata/source
D=<clone of scriptures-data>/hinduism/granth/vyasa/mahabharata/books/gitapress
for n in 1 2 3 4 5 6; do python3 $S/epub.py $D/bhag-$n.epub v$n.json; done   # each volume: parvas › adhyāyas › blocks, and a log of every odd block
python3 $S/make_text.py <this repository>/tools/works/mahabharata              # text.txt, meanings/hi/gitapress.json, source/check.md
```
The steps read the owner's e-books from `scriptures-data`, so `regen_check.py` cannot run them: after changing a script, run them and diff `text.txt`. `source/check.md` lists every place the checks found (the book's own numbers and dākṣiṇātya counts, every correction made); `source/corrections.json` holds the corrections made by hand; `reconciliation.md` gives the rules.
