# Gita Press Vālmīki-Rāmāyaṇa, Hindi translation (code 77) — extraction report

Source: `scriptures-data/hinduism/granth/valmiki/ramayana/books/gitapress/hindi.pdf` (2,406 pages, sha256 a820aadf…). It is a calibre/Ghostscript print of an e-book, not a scan of the printed book: one column, no running heads, Devanagari in an embedded Noto Sans Devanagari subset, Latin punctuation in Times New Roman. No OCR was used anywhere.

## Files

| file | what |
|---|---|
| `decode.py` | the decoder: glyph ids → Unicode, with the shaping round-trip check (documented at the top) |
| `glyphs.json` | `meta` (reference font, outline check, method, validation) and `glyphs`: glyph id → name, role, Unicode value, shaping evidence, count in the book |
| `hi_book.json` | the seven kāṇḍas → sargas → verse-numbered paragraphs, as specified |
| `frontmatter.json` | नम्र निवेदन, the contents page range, पाठविधि (blocks) and the five māhātmya chapters (blocks and verse paragraphs) |
| `report.md` | this report |
| `anomalies.json` | every anomaly and every correction, machine-readable (with page numbers) |
| `manual_fixes.json` | the hand-checked misprint corrections (rule C) |
| `wordfreq.json, hapax.json` | word-frequency list; words that occur once |
| `build_glyphs.py, survey_shapes.py, validate_table.py, hb.py` | how glyphs.json was made and checked |
| `extract_trace.py, normalize.py, parse.py, frontmatter.py, words.py, screen_typos.py, wellformed.py, pagecheck.py, make_report.py` | the rest of the pipeline; `check/` holds the line-by-line page comparison images |
| `NotoSansDevanagari-Regular-2.000.ttf` | the official reference font used for shaping |

Re-run: `python3 extract_trace.py && python3 survey_shapes.py && python3 build_glyphs.py && python3 validate_table.py && python3 decode.py && python3 parse.py && python3 frontmatter.py && python3 words.py && python3 make_report.py`.

## Result

| kāṇḍa | sargas (expected) | prakṣipta | paragraphs | footnotes | marks printed without number (incl. 1 paragraph with no mark) |
|---|---|---|---|---|---|
| Bāla | 77 (77) | 0 | 1917 | 15 | 113 |
| Ayodhyā | 119 (119) | 0 | 3948 | 42 | 282 |
| Araṇya | 75 (75) | 1 | 2158 | 36 | 127 |
| Kiṣkindhā | 67 (67) | 0 | 2225 | 27 | 122 |
| Sundara | 68 (68) | 0 | 2565 | 22 | 156 |
| Yuddha | 128 (128) | 0 | 5199 | 62 | 444 |
| Uttara | 111 (111) | 2 | 3216 | 19 | 169 |
| **total** | **645** (645) | **3** | **21228** | **223** | **1413** |

Every sarga count matches Gita Press (Bāla 77, Ayodhyā 119, Araṇya 75 + 1 prakṣipta after sarga 56, Kiṣkindhā 67, Sundara 68, Yuddha 128, Uttara 111 + 2 prakṣipta after sarga 59). The sarga order also matches the PDF bookmarks one-to-one (the n-th heading has the n-th bookmark, on the same page). Footnote count counts a note once per paragraph it is attached to.

## Method

1. **Glyph ids, not ToUnicode.** `page.get_texttrace()` gives every character with its glyph id (Identity-H, so the code is the glyph id). The Devanagari font is one subset, `IYECGW+NotoSansDevanagari-Regular`, on every page (2,396 pages); 251 distinct glyph ids occur.
2. **Same font.** all 254 non-empty embedded glyphs have the same contour points, end points and advance width as the same glyph id in the reference font (fontTools); 2.002 and 2.007 releases have 954/845 glyphs and do not match. Reference: https://raw.githubusercontent.com/googlefonts/noto-fonts/v2017-10-24-phase3-second-cleanup/hinted/NotoSansDevanagari-Regular.ttf (sha1 7da7ce9e40ba7c51f4a8080aa152b99a6951e88b).
3. **Each glyph settled by shaping** the reference font with HarfBuzz (uharfbuzz 0.x) on 187,394 generated clusters (every consonant ± nukta with every vowel sign and ं ँ ः; all 2-consonant conjuncts with every vowel sign; ्र/्य/्व clusters; all 3-consonant conjuncts; reph forms of all of these; independent vowels, digits, punctuation). Every one of the 251 glyph ids in the book is produced by that survey, so no glyph had to be read by eye. Each glyph got a value and a role (base, half form, pre-base ि variant, post-base mark, reph, dummy, dotted circle); `glyphs.json` keeps the shortest producing inputs as evidence. There are 12 widths of the pre-base ि (ivowelsign00–11), 8 ि+anusvāra and 9 reph+ि forms, 3 widths of ी, combined े/ै/ो/ौ + ं/reph forms, 32 half forms and about 100 ligature conjuncts.
4. **Table check.** Decoding the glyphs of every survey string whose glyphs all occur in the book gave the input back exactly for 93,565 strings; 11 did not — all are reph + independent ई/ऐ/ओ/औ, which this font decomposes (ई → इ + reph-shaped mark); that sequence never occurs in the book (step 6 proves it).
5. **Logical order rebuilt** (decode.py): a pre-base ि is written after the consonant cluster that follows it (half forms + base); a reph drawn after its syllable is written as र् at the syllable start; combined glyphs split accordingly; dotted circles and the dummy mark dropped; NFC.
6. **Round trip of the whole book.** Every Devanagari run (text between two Times characters, cut at line breaks: 664,983 runs) was decoded and then shaped again with the reference font: the glyph-id sequence equals the PDF's in all runs but 8. Those 8 are the last word of Uttara sarga titles (pp2199, 2209, 2215, 2221, 2228, 2231, 2237, 2239; p2203 is a ninth, split by the font style): the e-book closed its bold before the final ा, so the page prints ा on a dotted circle ("देन◌ा"); it decodes to the plain word (देना).
7. **Times New Roman** text (spaces, ‘ ’ — , ; : ! ? ( ) [ ] / * ½, a few Latin words) is taken from its ToUnicode: its 103 glyph ids map one-to-one to code points.
8. **Bold** Devanagari is drawn fill+stroke and reported with fill alpha 0; that is used only to recognise headings and titles. **Links** (blue text) tie footnote numbers and markers.
9. **Lines and paragraphs.** A line ends where the pen jumps back left or moves >12pt vertically. A space at a line end is not drawn, so lines are joined with a space — except after a hyphen, after an em dash, or before an em dash (mid-line the text never has a space there: "—x" 3,700 times vs "— x" 306; "x—" 3,863 vs "x —" 3). Paragraphs are cut only at verse marks, not at indentation (the e-book often starts an indented line in mid-sentence where the printed book turned a page).

## Checks run

| check | result |
|---|---|
| embedded outlines = official Noto Sans Devanagari 2.000 | 254 / 254 identical (points, contours, advance) |
| unknown glyph ids | none (251 used, 251 mapped) |
| table vs HarfBuzz survey | 93,565 exact, 11 differ (reph + independent ई/ऐ/ओ/औ; absent from the book) |
| re-shaping every decoded run | 664,975 / 664,983 identical; 8 = dotted-circle title endings (explained above) |
| Times glyph ↔ code point | 103 glyph ids, one-to-one |
| well-formed Devanagari (no sign without consonant, no two signs, no sign after virama, no stray ि) | raw decoding: 169 spots, every one a slip of the source text (ि typed before a virama; orphaned signs after a stray space) — all corrected by rules B and C; final text of hi_book.json: **0** |
| 12 pages compared with the 150-dpi render line by line (decoded text re-typeset under each printed line) | pp 70, 95, 108, 330, 600, 780, 1050, 1300, 1600, 1968, 2100, 2277 — all identical letter for letter (images in `check/`) |
| word list | 589,747 words, 33,325 distinct, 15,407 occur once (`hapax.json`) |
| words occurring once | all screened by machine (grammar; reph at word start; vowel sign at word start; legacy-slip patterns न्त/त्न, रु after a conjunct, ऋरु, anusvāra after the next consonant, compared against the frequency list); 48 random ones compared with the page image: all identical. Every non-word found is a slip of the source text, not a decoding error (listed below) |
| 648 sarga titles vs the PDF bookmarks (an independent Unicode copy) | 635 identical (ignoring ङ्ग/ंग style); 13 differ — in each the page is right and the bookmark has its own slip (see below) |
| sarga counts, colophon numbers, verse-mark sequence | see Result and Anomalies |
| footnotes | 220 notes, all attached (216 by the marker's link, 4 by symbol; see below) |

## Corrections applied to the decoded text

All corrections are logged in `anomalies.json` (fixes_*) and, for C, in the paragraph's `fixes`.

- **A — र्इ → ई** (4,662 times). The source types ई as र्+इ; it prints as a reph over इ on a dotted circle, which reads as ई (भाई, हुई, कोई…). र्इ is never a real spelling. र्ऋ (12, e.g. नैर्ऋत, निर्ऋति) is real and kept.
- **B — ि typed before a virama** (149 times): C+ि+्+C… → C+्+C…+ि (दृषि्ट → दृष्टि, अगि्न → अग्नि, पति्न → पत्नि…, स्ति्व → स्त्वि). The page shows ि at the left of the cluster with a visible halant; the word is unambiguous. Patterns: ि्ट×79, ि्न×31, ि्ठ×16, ि्व×14, ि्त×8, ि्क×1.
- **E — other legacy-conversion slips** (71 times), each a non-word whose right form the book prints elsewhere: पन्ती→पत्नी ×37, ग्नरु→ग्न ×16, ऋरु→ऋ ×12, ग्निरु→ग्नि ×5, क्वरु→क्व ×1. (पन्ती for पत्नी — पत्नी occurs ~150 times; a stray रु after ग्न/ग्नि/क्व: उद्विग्नरु, निमग्नरु, अग्निरु…; ऋरु for ऋ: नैर्ऋरुत्य.)
- **C — hand-checked misprints** (each looked at on the page):

| page | printed (decoded) | corrected | why |
|---|---|---|---|
| 202 | क्षत्रियध र्मके | क्षत्रियधर्मके | stray space inside the word in the source text (the page shows the gap; a word cannot begin with a reph) |
| 287 | मौनव ्रत | मौनव्रत | misprint in the source text: a stray space and an orphaned sign inside the word; the page prints it with a dotted circle (seen on the rendered page) |
| 562 | रमणीशि् ारोमणि | रमणीशिरोमणि | misprint in the source text: a stray space and an orphaned sign inside the word; the page prints it with a dotted circle (seen on the rendered page) |
| 784 | वैरविर ोधके | वैरविरोधके | misprint in the source text: a stray space and an orphaned sign inside the word; the page prints it with a dotted circle (seen on the rendered page) |
| 812 | तुहिनबिन्दुअ ोंसे | तुहिनबिन्दुओंसे | misprint in the source text: a stray space and an orphaned sign inside the word; the page prints it with a dotted circle (seen on the rendered page) |
| 873 | नष्टभ ्रष्ट | नष्टभ्रष्ट | misprint in the source text: a stray space and an orphaned sign inside the word; the page prints it with a dotted circle (seen on the rendered page) |
| 921 | पर्वतशि् ाखरके | पर्वतशिखरके | misprint in the source text: a stray space and an orphaned sign inside the word; the page prints it with a dotted circle (seen on the rendered page) |
| 980 | भेटं | भेंट | misprint in the source text: the anusvāra is typed after ट instead of after े (the book has भेंट 49 times); seen on the page |
| 1141 | वानरवीर ोंके | वानरवीरोंके | misprint in the source text: a stray space and an orphaned sign inside the word; the page prints it with a dotted circle (seen on the rendered page) |
| 1300 | विमाननि र्माणोचित | विमाननिर्माणोचित | stray space inside the word in the source text (the page shows the gap; a word cannot begin with a reph) |
| 1650 | हरीभर ी | हरीभरी | misprint in the source text: a stray space and an orphaned sign inside the word; the page prints it with a dotted circle (seen on the rendered page) |
| 1707 | वानरशि् ारोमणियो | वानरशिरोमणियो | misprint in the source text: a stray space and an orphaned sign inside the word; the page prints it with a dotted circle (seen on the rendered page) |
| 1749 | आग्नेयास्त्रयुक्त रु बाणका | आग्नेयास्त्रयुक्त बाणका | a stray “रु” begins the next printed line (same legacy-conversion slip as the “रु” after ग्न/क्व, rule E); owner to confirm |
| 1776 | कामनाविश् ोषके | कामनाविशेषके | misprint in the source text: a stray space and an orphaned sign inside the word; the page prints it with a dotted circle (seen on the rendered page) |
| 1808 | वानरशि् ारोमणियोंको | वानरशिरोमणियोंको | misprint in the source text: a stray space and an orphaned sign inside the word; the page prints it with a dotted circle (seen on the rendered page) |
| 1987 | अश्रुबिन्दुअ ोंसे | अश्रुबिन्दुओंसे | misprint in the source text: a stray space and an orphaned sign inside the word; the page prints it with a dotted circle (seen on the rendered page) |
| 2097 | सालकटङ्कटवंश् ामें | सालकटङ्कटवंशमें | misprint in the source text: a stray space and an orphaned sign inside the word; the page prints it with a dotted circle (seen on the rendered page) |
| 2246 | उन्होंन े | उन्होंने | misprint in the source text: a stray space and an orphaned sign inside the word; the page prints it with a dotted circle (seen on the rendered page) |
| 2261 | क्षत्रियध र्मके | क्षत्रियधर्मके | stray space inside the word in the source text (the page shows the gap; a word cannot begin with a reph) |
| 2283 | यमुनातीरनिवास ी | यमुनातीरनिवासी | misprint in the source text: a stray space and an orphaned sign inside the word; the page prints it with a dotted circle (seen on the rendered page) |

- **D — print-edition page numbers** that leaked into the e-book text, removed (number ≈ PDF page ÷ 2.03, standing alone): p331 “१६१”, p737 “३६५”, p948 “४६७”, p999 “४९१”, p1087 “५३५”, p1140 “५६१”, p1218 “६०१”, p1255 “६१९”, p1275 “६२९”, p1280 “६३३”, p1336 “६६१”, p1466 “७२५”, p1627 “८०७”, p1690 “८३९”, p1856 “९२५”, p1955 “९७३”, p1971 “९८१”, p2252 “१११६”, p2281 “११२७”, p2341 “११५६”.
- Left out: p2196 "1099-1193 Last coding done" (an e-book production note); p2341 a stray running title "*श्रीमद्वाल्मीकीय रामायण*" after a footnote.
- Dotted circles (U+25CC) inserted by the shaper are never part of the text.

## Decisions on layout

- **Hyphens at line ends (519):** this e-book never breaks a word at a line end; every line-end hyphen is a character of the text. Checked: 341 of the joined compounds occur hyphenated elsewhere, 168 nowhere else, 33 only solid elsewhere — the same proportions as mid-line hyphens (10.5 % of mid-line hyphenated pairs also occur only solid elsewhere). All hyphens are kept (`hyphens.json`). Three line-end hyphens before a parenthesis (pp1484, 1760, 1817: "वस्त्र-(चादर-)से") are kept as printed.
- **Em dash at a line end (79) / line start (188):** joined without a space (see Method 9). This is the only spacing that cannot be read off the page.
- **Footnote markers** stay in the paragraph text as printed: superscript * or digits glued to the word (e.g. "श्लोकरूप*", "स्थान१"); in three places in Uttara 36 (p2209) the markers are full-size digits ("युग्मोंसे१ … मूर्ति२ … दशाओंसे३"). One marker is a Latin "2" (p108 "मूर्च्छनाके2").
- **Half-verse marks** are kept as printed: "॥ २५ १/२ ॥" (superscript 1, subscript 2 → "१/२"), "॥ ७१/२ ॥" (no space, Kiṣkindhā 51–52), and "॥ ५६½ ॥" with the Times ½ (79 marks in Uttara 35–49). `half` is true for all of them.
- **Marks printed without a number** ("॥" alone): mark kept as "॥", `mark_inferred: true`, `from` = previous verse + 1, `to` = next printed verse − 1 (at least `from`; one verse each when several follow each other). One last paragraph has no mark at all (`mark: ""`, Yuddha 125, p2045).
- **Sarga notes:** a note whose marker is on the heading, title or colophon is in the sarga's `notes` (Ayodhyā 101, Araṇya prakṣipta, Yuddha 105 title, Uttara prakṣipta 1). Prakṣipta sargas carry `"prakshipta": true` and stand in their place.
- **Colophons** are kept as printed, joined to one line; the Gita Press heading/colophon misprints listed below are not corrected.

## Anomalies in the book (all kept as printed unless said otherwise)

### Verse numbering

**Marks printed without a number: 1412** paragraphs end with a bare ॥ (checked on the page images: the number is not there; nothing invisible is in the text layer). By sarga, with the verse numbers given to them:

- Bāla पहला सर्ग (p93): 9, 44–45, 54–55, 58, 60, 61, 70, 71, 80, 94–96, 98
- Bāla तीसरा सर्ग (p105): 10
- Bāla चौथा सर्ग (p108): 14–16, 19, 28–32
- Bāla पाँचवाँ सर्ग (p112): 16, 17, 23
- Bāla छठा सर्ग (p115): 14
- Bāla आठवाँ सर्ग (p130): 2, 18
- Bāla नवाँ सर्ग (p132): 7–8, 11
- Bāla दसवाँ सर्ग (p134): 3
- Bāla ग्यारहवाँ सर्ग (p137): 1, 10, 16–17, 31
- Bāla बारहवाँ सर्ग (p140): 4–5
- Bāla तेरहवाँ सर्ग (p142): 1, 6–8, 14, 16–17
- Bāla चौदहवाँ सर्ग (p146): 50, 53, 57
- Bāla सत्रहवाँ सर्ग (p158): 2–4, 32–34
- Bāla अठारहवाँ सर्ग (p161): 8–10, 26, 27–29, 50–52, 54–55
- Bāla उन्नीसवाँ सर्ग (p167): 7, 9–10, 19, 21
- Bāla बीसवाँ सर्ग (p169): 15–17
- Bāla बाईसवाँ सर्ग (p175): 4–5, 9, 10–12
- Bāla चौबीसवाँ सर्ग (p180): 18, 19, 20, 21–22
- Bāla पचीसवाँ सर्ग (p183): 21
- Bāla सत्ताईसवाँ सर्ग (p188): 2, 11
- Bāla उनतीसवाँ सर्ग (p193): 2–3, 6
- Bāla इकतीसवाँ सर्ग (p199): 19–20
- Bāla बत्तीसवाँ सर्ग (p202): 15, 16
- Bāla चौंतीसवाँ सर्ग (p208): 21
- Bāla सैंतीसवाँ सर्ग (p215): 6, 17, 32
- Bāla अड़तीसवाँ सर्ग (p218): 18
- Bāla उनतालीसवाँ सर्ग (p220): 3, 8, 9–12
- Bāla चालीसवाँ सर्ग (p223): 4
- Bāla इकतालीसवाँ सर्ग (p226): 11, 22
- Bāla तैंतालीसवाँ सर्ग (p231): 25, 27–28
- Bāla चौवालीसवाँ सर्ग (p235): 13
- Bāla सैंतालीसवाँ सर्ग (p243): 21
- Bāla अड़तालीसवाँ सर्ग (p245): 3, 19
- Bāla उनचासवाँ सर्ग (p248): 16
- Bāla पचासवाँ सर्ग (p250): 11–12, 15
- Bāla इक्यावनवाँ सर्ग (p253): 6
- Bāla चौवनवाँ सर्ग (p261): 14
- Bāla पचपनवाँ सर्ग (p263): 9, 16
- Bāla छप्पनवाँ सर्ग (p266): 6
- Bāla सत्तावनवाँ सर्ग (p268): 11, 14–15
- Bāla अट्ठावनवाँ सर्ग (p270): 6–7
- Bāla साठवाँ सर्ग (p274): 25, 28, 29–32
- Bāla एकसठवाँ सर्ग (p277): 8, 24
- Bāla तिरसठवाँ सर्ग (p282): 1, 25
- Bāla चौंसठवाँ सर्ग (p285): 13
- Bāla पैंसठवाँ सर्ग (p287): 12–13, 17, 31–32
- Bāla छाछठवाँ सर्ग (p291): 17
- Bāla सरसठवाँ सर्ग (p294): 1, 5, 21
- Bāla उनहत्तरवाँ सर्ग (p299): 8
- Bāla सत्तरवाँ सर्ग (p301): 34–35, 41
- Bāla इकहत्तरवाँ सर्ग (p305): 11, 14
- Bāla बहत्तरवाँ सर्ग (p308): 10
- Bāla चौहत्तरवाँ सर्ग (p314): 15–16
- Ayodhyā पहला सर्ग (p326): 15
- Ayodhyā दूसरा सर्ग (p332): 4, 37–38
- Ayodhyā तीसरा सर्ग (p337): 38
- Ayodhyā चौथा सर्ग (p342): 20, 35–36, 39
- Ayodhyā पाँचवाँ सर्ग (p346): 16
- Ayodhyā छठा सर्ग (p349): 19–20
- Ayodhyā सातवाँ सर्ग (p352): 18–19
- Ayodhyā आठवाँ सर्ग (p356): 7, 14, 39
- Ayodhyā नवाँ सर्ग (p360): 6, 33, 34, 42, 52
- Ayodhyā दसवाँ सर्ग (p366): 4, 28
- Ayodhyā ग्यारहवाँ सर्ग (p370): 5, 28
- Ayodhyā बारहवाँ सर्ग (p373): 24, 31, 34, 39, 49, 74–75, 85, 112
- Ayodhyā तेरहवाँ सर्ग (p383): 17
- Ayodhyā पंद्रहवाँ सर्ग (p392): 38
- Ayodhyā सोलहवाँ सर्ग (p397): 11, 18, 21
- Ayodhyā सत्रहवाँ सर्ग (p402): 12
- Ayodhyā अठारहवाँ सर्ग (p404): 39
- Ayodhyā उन्नीसवाँ सर्ग (p408): 7
- Ayodhyā बीसवाँ सर्ग (p412): 1, 4, 25, 27, 28, 31, 37, 42, 51
- Ayodhyā इक्कीसवाँ सर्ग (p417): 7, 14, 23, 35, 37, 64
- Ayodhyā बाईसवाँ सर्ग (p423): 7
- Ayodhyā तेईसवाँ सर्ग (p426): 1, 2, 40
- Ayodhyā चौबीसवाँ सर्ग (p431): 30
- Ayodhyā पचीसवाँ सर्ग (p435): 6, 27
- Ayodhyā छब्बीसवाँ सर्ग (p439): 3, 4, 5, 20
- Ayodhyā अट्ठाईसवाँ सर्ग (p446): 3, 8, 15
- Ayodhyā उनतीसवाँ सर्ग (p449): 2, 9, 13, 22
- Ayodhyā तीसवाँ सर्ग (p452): 11, 12, 31, 38, 47
- Ayodhyā इकतीसवाँ सर्ग (p457): 15, 20–22
- Ayodhyā बत्तीसवाँ सर्ग (p461): 18–20, 37
- Ayodhyā तैंतीसवाँ सर्ग (p465): 11, 13
- Ayodhyā चौंतीसवाँ सर्ग (p468): 3–4, 14, 16, 22, 40, 43–44, 49, 50, 55
- Ayodhyā छत्तीसवाँ सर्ग (p476): 6, 25–26
- Ayodhyā सैंतीसवाँ सर्ग (p480): 5, 9–12, 25–26, 36
- Ayodhyā उनतालीसवाँ सर्ग (p485): 10, 12, 23, 27
- Ayodhyā चालीसवाँ सर्ग (p489): 6
- Ayodhyā इकतालीसवाँ सर्ग (p494): 5, 11, 14, 16
- Ayodhyā बयालीसवाँ सर्ग (p496): 17
- Ayodhyā तैंतालीसवाँ सर्ग (p499): 7
- Ayodhyā पैंतालीसवाँ सर्ग (p504): 3, 10, 11, 17, 27, 28, 29
- Ayodhyā सैंतालीसवाँ सर्ग (p511): 17
- Ayodhyā अड़तालीसवाँ सर्ग (p513): 11, 14
- Ayodhyā उनचासवाँ सर्ग (p517): 1, 3
- Ayodhyā पचासवाँ सर्ग (p519): 21, 22, 30, 43, 51
- Ayodhyā बावनवाँ सर्ग (p527): 3, 4, 36, 44, 54, 66
- Ayodhyā तिरपनवाँ सर्ग (p536): 24, 27, 32, 34
- Ayodhyā चौवनवाँ सर्ग (p540): 10, 19–20, 24–25, 29, 38
- Ayodhyā पचपनवाँ सर्ग (p544): 11
- Ayodhyā अट्ठावनवाँ सर्ग (p555): 3–4, 7, 13, 17–18, 24–25, 36
- Ayodhyā उनसठवाँ सर्ग (p559): 5, 13, 19
- Ayodhyā साठवाँ सर्ग (p562): 13
- Ayodhyā इकसठवाँ सर्ग (p565): 5
- Ayodhyā बासठवाँ सर्ग (p568): 8
- Ayodhyā तिरसठवाँ सर्ग (p570): 10, 12, 33
- Ayodhyā चौंसठवाँ सर्ग (p575): 23, 35, 37, 39, 43–44
- Ayodhyā पैंसठवाँ सर्ग (p582): 26
- Ayodhyā छाछठवाँ सर्ग (p585): 4, 15, 20, 23, 25
- Ayodhyā सरसठवाँ सर्ग (p588): 13, 16, 25
- Ayodhyā अड़सठवाँ सर्ग (p592): 7, 9, 16
- Ayodhyā उनहत्तरवाँ सर्ग (p594): 1, 15, 18–19
- Ayodhyā सत्तरवाँ सर्ग (p596): 15, 26
- Ayodhyā इकहत्तरहवाँ सर्ग (p599): 11
- Ayodhyā बहत्तरवाँ सर्ग (p604): 12, 38
- Ayodhyā चौहत्तरवाँ सर्ग (p612): 31
- Ayodhyā पचहत्तरवाँ सर्ग (p615): 11, 33, 34
- Ayodhyā छिहत्तरवाँ सर्ग (p621): 12, 15, 16–17
- Ayodhyā अठहत्तरवाँ सर्ग (p626): 9
- Ayodhyā उन्नासीवाँ सर्ग (p629): 5, 17
- Ayodhyā अस्सीवाँ सर्ग (p631): 13–14
- Ayodhyā बयासीवाँ सर्ग (p636): 21, 25
- Ayodhyā तिरासीवाँ सर्ग (p639): 3, 6
- Ayodhyā चौरासीवाँ सर्ग (p642): 6
- Ayodhyā सतासीवाँ सर्ग (p650): 8, 16
- Ayodhyā अट्ठासीवाँ सर्ग (p653): 2
- Ayodhyā नवासीवाँ सर्ग (p656): 5, 19
- Ayodhyā नब्बेवाँ सर्ग (p659): 16
- Ayodhyā इक्यानबेवाँ सर्ग (p661): 7, 9, 16, 53, 67–68, 78, 81
- Ayodhyā बानबेवाँ सर्ग (p668): 3, 7, 13, 14, 15, 30, 33
- Ayodhyā तिरानबेवाँ सर्ग (p672): 15, 22
- Ayodhyā चौरानबेवाँ सर्ग (p675): 1–2
- Ayodhyā पंचानबेवाँ सर्ग (p678): 7
- Ayodhyā सत्तानबेवाँ सर्ग (p683): 1, 6, 30
- Ayodhyā अट्ठानबेवाँ सर्ग (p686): 13
- Ayodhyā निन्यानबेवाँ सर्ग (p688): 14, 31, 41
- Ayodhyā सौवाँ सर्ग (p692): 4, 33
- Ayodhyā एक सौ एकवाँ सर्ग (p700): 19
- Ayodhyā एक सौ तीनवाँ सर्ग (p704): 7, 24–25, 36, 47
- Ayodhyā एक सौ पाँचवाँ सर्ग (p711): 35, 39, 45
- Ayodhyā एक सौ छठाँ सर्ग (p716): 5, 27
- Ayodhyā एक सौ सातवाँ सर्ग (p720): 2, 6, 7, 8, 12, 15
- Ayodhyā एक सौ आठवाँ सर्ग (p722): 13, 18
- Ayodhyā एक सौ नौवाँ सर्ग (p724): 19, 28
- Ayodhyā एक सौ दसवाँ सर्ग (p728): 5, 9, 17, 18–19, 25, 29, 31
- Ayodhyā एक सौ ग्यारहवाँ सर्ग (p731): 7, 9–10, 18
- Ayodhyā एक सौ बारहवाँ सर्ग (p734): 14, 23, 24–26, 29, 30
- Ayodhyā एक सौ तेरहवाँ सर्ग (p737): 12
- Ayodhyā एक सौ चौदहवाँ सर्ग (p740): 24, 27–28
- Ayodhyā एक सौ पंद्रहवाँ सर्ग (p743): 24
- Ayodhyā एक सौ सोलहवाँ सर्ग (p746): 13
- Ayodhyā एक सौ सत्रहवाँ सर्ग (p749): 2, 4, 18
- Ayodhyā एक सौ अठारहवाँ सर्ग (p752): 15, 16, 18, 19, 20–22, 28, 31, 36
- Ayodhyā एक सौ उन्नीसवाँ सर्ग (p757): 23
- Araṇya दूसरा सर्ग (p763): 8–9, 13, 23
- Araṇya तीसरा सर्ग (p766): 13
- Araṇya चौथा सर्ग (p769): 19, 32
- Araṇya पाँचवाँ सर्ग (p772): 24
- Araṇya सातवाँ सर्ग (p779): 12
- Araṇya आठवाँ सर्ग (p782): 8–9
- Araṇya दसवाँ सर्ग (p787): 5, 21
- Araṇya ग्यारहवाँ सर्ग (p790): 55, 56–57, 79
- Araṇya बारहवाँ सर्ग (p798): 2, 10–11
- Araṇya तेरहवाँ सर्ग (p801): 6, 10, 13, 17
- Araṇya चौदहवाँ सर्ग (p804): 13, 29
- Araṇya पंद्रहवाँ सर्ग (p808): 10, 19
- Araṇya सोलहवाँ सर्ग (p811): 19, 42
- Araṇya सत्रहवाँ सर्ग (p815): 19, 20, 21–22
- Araṇya अठारहवाँ सर्ग (p818): 21, 25, 26
- Araṇya उन्नीसवाँ सर्ग (p821): 11, 17, 24
- Araṇya बीसवाँ सर्ग (p824): 6
- Araṇya इक्कीसवाँ सर्ग (p827): 6, 10, 13
- Araṇya चौबीसवाँ सर्ग (p835): 15, 20–21
- Araṇya पचीसवाँ सर्ग (p838): 11
- Araṇya छब्बीसवाँ सर्ग (p842): 11, 19, 20–21
- Araṇya सत्ताईसवाँ सर्ग (p845): 2, 19
- Araṇya अट्ठाईसवाँ सर्ग (p847): 7, 13, 29
- Araṇya तीसवाँ सर्ग (p853): 37
- Araṇya इकतीसवाँ सर्ग (p857): 43
- Araṇya बत्तीसवाँ सर्ग (p862): 6–7, 10, 12
- Araṇya पैंतीसवाँ सर्ग (p871): 13
- Araṇya छत्तीसवाँ सर्ग (p875): 22
- Araṇya अड़तीसवाँ सर्ग (p880): 13, 17, 19, 23
- Araṇya उनतालीसवाँ सर्ग (p883): 13, 18
- Araṇya चालीसवाँ सर्ग (p886): 5–6
- Araṇya इकतालीसवाँ सर्ग (p889): 2, 6
- Araṇya बयालीसवाँ सर्ग (p891): 30–31
- Araṇya तैंतालीसवाँ सर्ग (p894): 6, 7, 18
- Araṇya चौवालीसवाँ सर्ग (p899): 17, 18–19
- Araṇya पैंतालीसवाँ सर्ग (p902): 24, 39
- Araṇya छियालीसवाँ सर्ग (p906): 9, 13, 23–24, 27, 34
- Araṇya सैंतालीसवाँ सर्ग (p910): 9, 11, 39–41
- Araṇya उनचासवाँ सर्ग (p917): 1, 2, 12, 39
- Araṇya पचासवाँ सर्ग (p921): 1, 6–7, 11, 18, 21, 22
- Araṇya इक्यावनवाँ सर्ग (p924): 19, 20, 24
- Araṇya बावनवाँ सर्ग (p928): 4, 8–9, 19, 20–22
- Araṇya तिरपनवाँ सर्ग (p932): 10
- Araṇya चौवनवाँ सर्ग (p935): 17–18
- Araṇya छप्पनवाँ सर्ग (p942): 24–25, 32
- Araṇya सत्तावनवाँ सर्ग (p949): 4, 18
- Araṇya अट्ठावनवाँ सर्ग (p952): 4
- Araṇya साठवाँ सर्ग (p957): 14
- Araṇya इकसठवाँ सर्ग (p961): 11, 23, 24
- Araṇya बासठवाँ सर्ग (p964): 13
- Araṇya तिरसठवाँ सर्ग (p966): 15
- Araṇya चौंसठवाँ सर्ग (p969): 11, 33, 41, 46, 60–61
- Araṇya पैंसठवाँ सर्ग (p976): 13–15
- Araṇya सरसठवाँ सर्ग (p980): 12
- Araṇya अरसठवाँ सर्ग (p983): 31
- Araṇya उनहत्तरवाँ सर्ग (p987): 11, 27
- Araṇya सत्तरवाँ सर्ग (p992): 17
- Araṇya एकहत्तरवाँ सर्ग (p994): 12, 33
- Araṇya तिहत्तरवाँ सर्ग (p1000): 46
- Araṇya चौहत्तरवाँ सर्ग (p1004): 4
- Kiṣkindhā पहला सर्ग (p1010): 37, 71, 97
- Kiṣkindhā दूसरा सर्ग (p1022): 3, 11
- Kiṣkindhā तीसरा सर्ग (p1025): 1, 34
- Kiṣkindhā चौथा सर्ग (p1029): 15–16, 22–23
- Kiṣkindhā सातवाँ सर्ग (p1038): 18
- Kiṣkindhā आठवाँ सर्ग (p1041): 2
- Kiṣkindhā दसवाँ सर्ग (p1048): 3, 15–16, 25
- Kiṣkindhā ग्यारहवाँ सर्ग (p1051): 7
- Kiṣkindhā बारहवाँ सर्ग (p1059): 20
- Kiṣkindhā तेरहवाँ सर्ग (p1063): 29
- Kiṣkindhā चौदहवाँ सर्ग (p1066): 17, 18
- Kiṣkindhā पंद्रहवाँ सर्ग (p1069): 23, 30
- Kiṣkindhā सोलहवाँ सर्ग (p1072): 1, 18, 25, 26, 32
- Kiṣkindhā सत्रहवाँ सर्ग (p1076): 14, 15, 31, 50, 53
- Kiṣkindhā अठारहवाँ सर्ग (p1081): 24
- Kiṣkindhā बाईसवाँ सर्ग (p1096): 5, 27–28
- Kiṣkindhā पचीसवाँ सर्ग (p1107): 12, 46
- Kiṣkindhā छब्बीसवाँ सर्ग (p1112): 20, 39, 41
- Kiṣkindhā सत्ताईसवाँ सर्ग (p1116): 20, 26
- Kiṣkindhā अट्ठाईसवाँ सर्ग (p1121): 8, 21, 23, 29, 42, 45, 50, 58
- Kiṣkindhā उनतीसवाँ सर्ग (p1128): 10, 13, 23
- Kiṣkindhā तीसवाँ सर्ग (p1132): 17, 25, 29, 33, 40, 76
- Kiṣkindhā इकतीसवाँ सर्ग (p1141): 9
- Kiṣkindhā तैंतीसवाँ सर्ग (p1149): 47, 62
- Kiṣkindhā चौंतीसवाँ सर्ग (p1156): 7, 18
- Kiṣkindhā पैंतीसवाँ सर्ग (p1158): 15
- Kiṣkindhā छत्तीसवाँ सर्ग (p1161): 13, 14
- Kiṣkindhā सैंतीसवाँ सर्ग (p1163): 15, 21
- Kiṣkindhā अड़तीसवाँ सर्ग (p1166): 19
- Kiṣkindhā उनतालीसवाँ सर्ग (p1169): 36
- Kiṣkindhā चालीसवाँ सर्ग (p1173): 2, 4, 44, 51–52
- Kiṣkindhā इकतालीसवाँ सर्ग (p1180): 18, 19–20, 23–24, 32, 33, 40–41, 44
- Kiṣkindhā बयालीसवाँ सर्ग (p1185): 11–12, 17, 19, 44, 48, 50, 51, 56
- Kiṣkindhā तैंतालीसवाँ सर्ग (p1190): 14, 18, 33
- Kiṣkindhā चौवालीसवाँ सर्ग (p1196): 11
- Kiṣkindhā सैंतालीसवाँ सर्ग (p1202): 11–12
- Kiṣkindhā अड़तालीसवाँ सर्ग (p1204): 1, 15–16
- Kiṣkindhā उनचासवाँ सर्ग (p1207): 8
- Kiṣkindhā पचासवाँ सर्ग (p1209): 25
- Kiṣkindhā इक्यावनवाँ सर्ग (p1213): 5–6, 15, 16
- Kiṣkindhā बावनवाँ सर्ग (p1215): 1, 24, 25–26, 31
- Kiṣkindhā तिरपनवाँ सर्ग (p1218): 4, 8–9
- Kiṣkindhā चौवनवाँ सर्ग (p1221): 17
- Kiṣkindhā पचपनवाँ सर्ग (p1224): 6, 13
- Kiṣkindhā छप्पनवाँ सर्ग (p1226): 6–7
- Kiṣkindhā अट्ठावनवाँ सर्ग (p1230): 2, 13, 16, 18
- Kiṣkindhā उनसठवाँ सर्ग (p1233): 26
- Kiṣkindhā साठवाँ सर्ग (p1236): 5
- Kiṣkindhā इकसठवाँ सर्ग (p1238): 17
- Kiṣkindhā पैंसठवाँ सर्ग (p1246): 5, 11–13
- Kiṣkindhā छाछठवाँ सर्ग (p1249): 14
- Kiṣkindhā सरसठवाँ सर्ग (p1253): 17–18
- Sundara पहला सर्ग (p1258): 7, 62, 90, 96, 163, 193, 195
- Sundara तीसरा सर्ग (p1281): 33, 35, 42, 44
- Sundara चौथा सर्ग (p1286): 15–16
- Sundara पाँचवाँ सर्ग (p1289): 4
- Sundara छठा सर्ग (p1293): 6, 7, 34–35, 38–39, 42–43
- Sundara सातवाँ सर्ग (p1297): 7, 17
- Sundara आठवाँ सर्ग (p1300): 6
- Sundara नवाँ सर्ग (p1302): 22, 23–24, 32, 60, 66
- Sundara दसवाँ सर्ग (p1309): 3, 18, 26, 27, 28, 52–53
- Sundara ग्यारहवाँ सर्ग (p1314): 1, 4, 35
- Sundara बारहवाँ सर्ग (p1319): 17, 24
- Sundara तेरहवाँ सर्ग (p1322): 17, 35
- Sundara चौदहवाँ सर्ग (p1328): 5–6, 10, 27–28, 51
- Sundara पंद्रहवाँ सर्ग (p1333): 9, 52
- Sundara सोलहवाँ सर्ग (p1338): 1, 5
- Sundara सत्रहवाँ सर्ग (p1341): 8, 26
- Sundara अठारहवाँ सर्ग (p1345): 13
- Sundara उन्नीसवाँ सर्ग (p1348): 20, 21
- Sundara बीसवाँ सर्ग (p1350): 1, 6, 11
- Sundara इक्कीसवाँ सर्ग (p1354): 5–6
- Sundara बाईसवाँ सर्ग (p1357): 13, 42
- Sundara तेईसवाँ सर्ग (p1361): 8, 9–10
- Sundara पचीसवाँ सर्ग (p1367): 3
- Sundara छब्बीसवाँ सर्ग (p1369): 5, 31, 34, 35, 40
- Sundara सत्ताईसवाँ सर्ग (p1374): 9–10, 29–30, 50
- Sundara तीसवाँ सर्ग (p1383): 21, 22, 25, 32, 42
- Sundara तैंतीसवाँ सर्ग (p1391): 14
- Sundara चौंतीसवाँ सर्ग (p1394): 18, 23, 29
- Sundara पैंतीसवाँ सर्ग (p1398): 29, 32, 67, 68–70, 87
- Sundara छत्तीसवाँ सर्ग (p1406): 8, 19, 23, 47
- Sundara सैंतीसवाँ सर्ग (p1411): 3, 30, 37, 43, 47, 58, 61
- Sundara अड़तीसवाँ सर्ग (p1417): 20, 32, 46
- Sundara उनतालीसवाँ सर्ग (p1423): 9, 18, 54
- Sundara चालीसवाँ सर्ग (p1428): 12
- Sundara इकतालीसवाँ सर्ग (p1431): 6, 11, 14, 17–18
- Sundara बयालीसवाँ सर्ग (p1434): 9, 33–36, 40
- Sundara छियालीसवाँ सर्ग (p1444): 24
- Sundara अड़तालीसवाँ सर्ग (p1453): 12, 17, 49, 50–52, 57
- Sundara पचासवाँ सर्ग (p1461): 5
- Sundara इक्यावनवाँ सर्ग (p1463): 4, 7, 42
- Sundara बावनवाँ सर्ग (p1467): 5, 10, 15
- Sundara तिरपनवाँ सर्ग (p1470): 2, 7
- Sundara चौवनवाँ सर्ग (p1474): 21, 25, 33
- Sundara छप्पनवाँ सर्ग (p1483): 36, 42–43
- Sundara सत्तावनवाँ सर्ग (p1488): 29, 34, 37–38, 40
- Sundara अट्ठावनवाँ सर्ग (p1492): 5, 22, 66, 102, 139, 147, 165–166
- Sundara उनसठवाँ सर्ग (p1505): 2, 28
- Sundara इकसठवाँ सर्ग (p1510): 4, 17
- Sundara बासठवाँ सर्ग (p1513): 1, 6–7, 18, 19
- Sundara तिरसठवाँ सर्ग (p1517): 6, 14, 20
- Sundara चौंसठवाँ सर्ग (p1520): 2, 12, 27, 45
- Sundara सरसठवाँ सर्ग (p1529): 24, 40–41
- Yuddha पहला सर्ग (p1536): 8, 15
- Yuddha दूसरा सर्ग (p1538): 1
- Yuddha तीसरा सर्ग (p1541): 24, 28, 31
- Yuddha चौथा सर्ग (p1544): 5, 11, 20, 29, 52, 68–69, 71, 79, 82–83, 107
- Yuddha पाँचवाँ सर्ग (p1554): 7, 15
- Yuddha छठा सर्ग (p1556): 1
- Yuddha आठवाँ सर्ग (p1561): 1, 8
- Yuddha नवाँ सर्ग (p1563): 23
- Yuddha दसवाँ सर्ग (p1565): 23
- Yuddha बारहवाँ सर्ग (p1571): 3, 7
- Yuddha तेरहवाँ सर्ग (p1575): 11
- Yuddha चौदहवाँ सर्ग (p1577): 17
- Yuddha सोलहवाँ सर्ग (p1582): 13, 18
- Yuddha सत्रहवाँ सर्ग (p1585): 45, 49, 63
- Yuddha अठारहवाँ सर्ग (p1591): 6–7, 28
- Yuddha बीसवाँ सर्ग (p1599): 8
- Yuddha इक्कीसवाँ सर्ग (p1603): 10, 16
- Yuddha बाईसवाँ सर्ग (p1607): 19, 53, 72, 75, 83
- Yuddha तेईसवाँ सर्ग (p1614): 1, 2, 12
- Yuddha चौबीसवाँ सर्ग (p1616): 12, 17, 19, 35, 40
- Yuddha पचीसवाँ सर्ग (p1620): 4–8, 18, 26
- Yuddha छब्बीसवाँ सर्ग (p1623): 26–27
- Yuddha अट्ठाईसवाँ सर्ग (p1631): 24, 26–27
- Yuddha उनतीसवाँ सर्ग (p1634): 24
- Yuddha तीसवाँ सर्ग (p1637): 29, 33
- Yuddha इकतीसवाँ सर्ग (p1640): 8, 11–12, 28
- Yuddha बत्तीसवाँ सर्ग (p1644): 14, 15, 17, 23, 31, 32, 42
- Yuddha तैंतीसवाँ सर्ग (p1648): 1, 8, 9, 36
- Yuddha चौंतीसवाँ सर्ग (p1652): 1, 2, 4, 16, 18, 19
- Yuddha पैंतीसवाँ सर्ग (p1655): 10, 15, 30
- Yuddha छत्तीसवाँ सर्ग (p1658): 22
- Yuddha सैंतीसवाँ सर्ग (p1660): 11, 25
- Yuddha अड़तीसवाँ सर्ग (p1663): 15
- Yuddha उनतालीसवाँ सर्ग (p1665): 21, 24, 27
- Yuddha चालीसवाँ सर्ग (p1668): 2, 12, 24–26
- Yuddha इकतालीसवाँ सर्ग (p1672): 4–5, 16, 21, 30, 37, 82, 84, 89
- Yuddha बयालीसवाँ सर्ग (p1680): 8, 16, 30, 34, 36, 46
- Yuddha तैंतालीसवाँ सर्ग (p1684): 10
- Yuddha चौवालीसवाँ सर्ग (p1688): 5, 14–15, 27
- Yuddha पैंतालीसवाँ सर्ग (p1692): 9
- Yuddha छियालीसवाँ सर्ग (p1695): 11, 26, 38, 39
- Yuddha सैंतालीसवाँ सर्ग (p1699): 20
- Yuddha अड़तालीसवाँ सर्ग (p1701): 36
- Yuddha उनचासवाँ सर्ग (p1705): 10, 18, 21
- Yuddha पचासवाँ सर्ग (p1708): 51
- Yuddha इक्यावनवाँ सर्ग (p1714): 1, 18, 24–25, 35
- Yuddha बावनवाँ सर्ग (p1717): 7
- Yuddha तिरपनवाँ सर्ग (p1720): 4, 6, 10, 13, 20
- Yuddha चौवनवाँ सर्ग (p1723): 1, 13, 35
- Yuddha पचपनवाँ सर्ग (p1727): 10
- Yuddha छप्पनवाँ सर्ग (p1730): 8, 28
- Yuddha सत्तावनवाँ सर्ग (p1733): 15, 18, 20, 25, 30, 32
- Yuddha अट्ठावनवाँ सर्ग (p1737): 5–6, 12, 23, 38–39, 58
- Yuddha उनसठवाँ सर्ग (p1742): 28, 37, 44, 54, 58, 69, 73–74, 78, 84, 95, 117, 121, 126–128, 138, 143, 145
- Yuddha साठवाँ सर्ग (p1755): 5, 12, 34–35, 41, 50, 55, 59, 88
- Yuddha इकसठवाँ सर्ग (p1763): 11, 13, 19, 24, 34
- Yuddha बासठवाँ सर्ग (p1767): 21–22
- Yuddha तिरसठवाँ सर्ग (p1769): 1, 9, 15, 18, 20, 21, 26, 39, 58
- Yuddha चौंसठवाँ सर्ग (p1775): 17, 30–31
- Yuddha पैंसठवाँ सर्ग (p1779): 9, 15, 51
- Yuddha छाछठवाँ सर्ग (p1784): 2
- Yuddha सरसठवाँ सर्ग (p1787): 4, 18, 30, 51, 65, 69, 71, 72–73, 77, 89, 91, 93, 104, 114–115, 124, 149, 151, 153, 172
- Yuddha अड़सठवाँ सर्ग (p1803): 15
- Yuddha उनहत्तरवाँ सर्ग (p1805): 10, 14, 32, 36, 50, 52, 90, 93
- Yuddha सत्तरवाँ सर्ग (p1813): 19, 29, 30, 34, 42, 50–51
- Yuddha इकहत्तरवाँ सर्ग (p1819): 34, 46, 65, 72, 90, 108
- Yuddha तिहत्तरवाँ सर्ग (p1831): 2, 11–12, 28, 35, 38, 43, 45, 46, 51, 61, 62–65, 69
- Yuddha चौहत्तरवाँ सर्ग (p1838): 1, 29, 33, 38, 41, 49, 62, 72, 73–74
- Yuddha पचहत्तरवाँ सर्ग (p1845): 11–12, 18–20, 23, 27, 46, 58, 66
- Yuddha छिहत्तरवाँ सर्ग (p1851): 2, 4, 15, 52–54, 71–72
- Yuddha अठहत्तरवाँ सर्ग (p1861): 10, 16, 20, 21
- Yuddha उन्नासीवाँ सर्ग (p1863): 19–20, 24, 32
- Yuddha अस्सीवाँ सर्ग (p1867): 20, 41, 43
- Yuddha इक्यासीवाँ सर्ग (p1871): 6
- Yuddha बयासीवाँ सर्ग (p1874): 21, 25–27
- Yuddha तिरासीवाँ सर्ग (p1877): 11, 23
- Yuddha चौरासीवाँ सर्ग (p1882): 17–18, 22
- Yuddha पचासीवाँ सर्ग (p1884): 6, 16, 35
- Yuddha छियासीवाँ सर्ग (p1887): 19, 35
- Yuddha सतासीवाँ सर्ग (p1890): 6, 19, 28, 29
- Yuddha अट्ठासीवाँ सर्ग (p1893): 20, 24, 27, 29, 41, 53
- Yuddha नवासीवाँ सर्ग (p1900): 10, 22, 33, 40, 41–43, 46, 52
- Yuddha नब्बेवाँ सर्ग (p1905): 2, 17, 21, 58, 62, 74, 83, 84
- Yuddha इक्यानबेवाँ सर्ग (p1913): 17, 22–23
- Yuddha बानबेवाँ सर्ग (p1916): 24, 29, 37, 49, 65
- Yuddha तिरानबेवाँ सर्ग (p1922): 9, 12–13, 21, 23, 39
- Yuddha पञ्चानबेवाँ सर्ग (p1929): 11, 25–26, 36, 40, 48, 52
- Yuddha छानबेवाँ सर्ग (p1933): 31–32
- Yuddha सत्तानबेवाँ सर्ग (p1936): 19, 29–30, 37
- Yuddha अट्ठानबेवाँ सर्ग (p1939): 1, 7, 8–9, 21
- Yuddha निन्यानबेवाँ सर्ग (p1942): 20
- Yuddha सौवाँ सर्ग (p1946): 13, 21, 22, 55
- Yuddha एक सौ एकवाँ सर्ग (p1951): 4, 12, 15, 17, 23, 40, 52–53
- Yuddha एक सौ दोवाँ सर्ग (p1956): 7–8, 19, 41, 58
- Yuddha एक सौ चारवाँ सर्ग (p1965): 13
- Yuddha एक सौ पाँचवाँ सर्ग (p1968): 3, 8–9, 16, 24
- Yuddha एक सौ छठाँ सर्ग (p1972): 5, 20, 34
- Yuddha एक सौ सातवाँ सर्ग (p1975): 35, 51, 52–54, 57, 58, 59–61, 65, 67
- Yuddha एक सौ आठवाँ सर्ग (p1981): 4, 19, 28
- Yuddha एक सौ नवाँ सर्ग (p1984): 2, 5, 10, 15, 23
- Yuddha एक सौ ग्यारहवाँ सर्ग (p1990): 5, 7, 15, 20–21, 27, 39, 41, 45, 46–47, 59, 63, 72–73, 79, 97, 103, 106, 110, 112–113
- Yuddha एक सौ बारहवाँ सर्ग (p2000): 10, 14–16
- Yuddha एक सौ तेरहवाँ सर्ग (p2002): 7
- Yuddha एक सौ चौदहवाँ सर्ग (p2007): 22, 31
- Yuddha एक सौ पंद्रहवाँ सर्ग (p2011): 3, 7, 16, 25
- Yuddha एक सौ सोलहवाँ सर्ग (p2014): 5
- Yuddha एक सौ उन्नीसवाँ सर्ग (p2024): 27
- Yuddha एक सौ बीसवाँ सर्ग (p2027): 2
- Yuddha एक सौ इक्कीसवाँ सर्ग (p2029): 25
- Yuddha एक सौ बाईसवाँ सर्ग (p2032): 11–12, 14, 18
- Yuddha एक सौ तेईसवाँ सर्ग (p2035): 3, 24–25, 40, 41, 45, 47–48, 50, 57
- Yuddha एक सौ चौबीसवाँ सर्ग (p2040): 8, 10
- Yuddha एक सौ पचीसवाँ सर्ग (p2042): 43, 46
- Yuddha एक सौ छब्बीसवाँ सर्ग (p2046): 3, 20, 21–22, 35, 41, 42, 43
- Yuddha एक सौ सत्ताईसवाँ सर्ग (p2051): 39, 46
- Yuddha एक सौ अट्ठाईसवाँ सर्ग (p2057): 1, 4, 6–8, 36, 41, 68, 80, 91, 95, 117
- Uttara पहला सर्ग (p2067): 5–6, 9–10, 18, 27
- Uttara तीसरा सर्ग (p2074): 28
- Uttara चौथा सर्ग (p2077): 1, 17, 25
- Uttara छठाँ सर्ग (p2084): 29, 39, 40, 58, 63
- Uttara सातवाँ सर्ग (p2090): 23, 38, 48
- Uttara आठवाँ सर्ग (p2095): 1, 14, 23
- Uttara नवाँ सर्ग (p2098): 6–7, 10, 33
- Uttara दसवाँ सर्ग (p2102): 11, 16, 28, 29–30
- Uttara ग्यारहवाँ सर्ग (p2106): 4, 6, 25–26, 32, 46, 47
- Uttara बारहवाँ सर्ग (p2110): 27
- Uttara तेरहवाँ सर्ग (p2113): 32
- Uttara चौदहवाँ सर्ग (p2117): 1, 2, 3–5, 7, 16
- Uttara पंद्रहवाँ सर्ग (p2120): 22, 23
- Uttara सोलहवाँ सर्ग (p2124): 23, 24, 35, 47
- Uttara सत्रहवाँ सर्ग (p2128): 33, 43
- Uttara उन्नीसवाँ सर्ग (p2135): 19
- Uttara बीसवाँ सर्ग (p2138): 10, 20–21, 24, 26
- Uttara इक्कीसवाँ सर्ग (p2141): 9, 28, 29–30, 42
- Uttara बाईसवाँ सर्ग (p2145): 24, 33
- Uttara तेईसवाँ सर्ग (p2149): 11, 30, 52
- Uttara चौबीसवाँ सर्ग (p2154): 13, 19
- Uttara पचीसवाँ सर्ग (p2158): 20, 50
- Uttara सत्ताईसवाँ सर्ग (p2169): 1, 27, 37
- Uttara अट्ठाईसवाँ सर्ग (p2174): 37
- Uttara उनतीसवाँ सर्ग (p2178): 2, 3, 34
- Uttara तीसवाँ सर्ग (p2182): 38, 44, 48
- Uttara इकतीसवाँ सर्ग (p2187): 2, 5, 27
- Uttara बत्तीसवाँ सर्ग (p2191): 10, 47, 48
- Uttara चौंतीसवाँ सर्ग (p2199): 30, 46
- Uttara पैंतीसवाँ सर्ग (p2203): 9, 13, 20, 28, 58, 59
- Uttara छत्तीसवाँ सर्ग (p2209): 18
- Uttara सैंतीसवाँ सर्ग (p2215): 5
- Uttara उनतालीसवाँ सर्ग (p2221): 6
- Uttara चालीसवाँ सर्ग (p2223): 15
- Uttara इकतालीसवाँ सर्ग (p2226): 16, 20
- Uttara तैंतालीसवाँ सर्ग (p2231): 22, 22
- Uttara अड़तालीसवाँ सर्ग (p2245): 20, 26
- Uttara उनचासवाँ सर्ग (p2248): 21
- Uttara पचासवाँ सर्ग (p2250): 6, 9
- Uttara इक्यावनवाँ सर्ग (p2252): 9, 17
- Uttara तिरपनवाँ सर्ग (p2257): 1, 7, 17
- Uttara छप्पनवाँ सर्ग (p2264): 3, 6, 9–10, 17–18, 25
- Uttara सत्तावनवाँ सर्ग (p2267): 13
- Uttara अट्ठावनवाँ सर्ग (p2269): 8, 15
- Uttara प्रक्षिप्त सर्ग १ (p2274): 18
- Uttara प्रक्षिप्त सर्ग २ (p2277): 47
- Uttara बासठवाँ सर्ग (p2287): 8, 10–11, 18
- Uttara पैंसठवाँ सर्ग (p2294): 36
- Uttara सरसठवाँ सर्ग (p2300): 13
- Uttara तिहत्तरवाँ सर्ग (p2314): 3, 18
- Uttara पचहत्तरवाँ सर्ग (p2319): 8
- Uttara छिहत्तरवाँ सर्ग (p2321): 9, 11, 50
- Uttara अठहत्तरवाँ सर्ग (p2327): 16
- Uttara इक्यासीवाँ सर्ग (p2334): 3, 15
- Uttara तिरासीवाँ सर्ग (p2338): 2, 5, 12, 18
- Uttara चौरासीवाँ सर्ग (p2340): 18
- Uttara पचासीवाँ सर्ग (p2342): 10, 12
- Uttara छियासीवाँ सर्ग (p2344): 6
- Uttara सतासीवाँ सर्ग (p2346): 21–22
- Uttara अट्ठासीवाँ सर्ग (p2349): 14, 21
- Uttara नब्बेवाँ सर्ग (p2354): 14, 22
- Uttara इक्यानबेवाँ सर्ग (p2357): 14
- Uttara बानबेवाँ सर्ग (p2360): 4
- Uttara चौरानबेवाँ सर्ग (p2364): 23
- Uttara पञ्चानबेवाँ सर्ग (p2367): 6
- Uttara छानबेवाँ सर्ग (p2369): 9
- Uttara सत्तानबेवाँ सर्ग (p2371): 19
- Uttara अट्ठानबेवाँ सर्ग (p2374): 18
- Uttara सौवाँ सर्ग (p2379): 1, 7, 11, 21, 25
- Uttara एक सौ दोवाँ सर्ग (p2383): 12
- Uttara एक सौ तीनवाँ सर्ग (p2385): 14
- Uttara एक सौ छठाँ सर्ग (p2391): 14, 16
- Uttara एक सौ सातवाँ सर्ग (p2393): 9, 20
- Uttara एक सौ आठवाँ सर्ग (p2395): 15
- Uttara एक सौ नवाँ सर्ग (p2399): 8, 9, 21
- Uttara एक सौ दसवाँ सर्ग (p2401): 9, 12, 28

**Gaps, repeats and out-of-order marks** (expected → printed; the context shows the printed marks around it):

| page | kāṇḍa | sarga | finding | printed marks around it |
|---|---|---|---|---|
| 143 | Bāla | तेरहवाँ सर्ग | expected 19, printed ॥ २० ॥ | ॥ १८ १/२ २० २१-२२ २३ |
| 258 | Bāla | तिरपनवाँ सर्ग | expected 7, printed ॥ ८ ॥ | ५ ६ ८ ९ १/२ १० १/२ |
| 259 | Bāla | तिरपनवाँ सर्ग | expected 11, printed ॥ १२ ॥ | ९ १/२ १० १/२ १२ १३ १४ |
| 265 | Bāla | पचपनवाँ सर्ग | expected 26, printed ॥ २७ ॥ | २४ २५ २७ २८ |
| 303 | Bāla | सत्तरवाँ सर्ग | expected 31, printed ॥ ३० १/२ ॥ | २९ ३० ३० १/२ ३१—३३ ॥ |
| 311 | Bāla | तिहत्तरवाँ सर्ग | expected 3, printed ॥ ४ १/२ ॥ | १-२ ४ १/२ ५ १/२ ६ १/२ |
| 320 | Bāla | छिहत्तरवाँ सर्ग | expected 1, printed ॥ २ ॥ | २ ३ ४ |
| 402 | Ayodhyā | सत्रहवाँ सर्ग | expected 1, printed ॥ २ १/२ ॥ | २ १/२ ३—६ १/२ ७ १/२ |
| 404 | Ayodhyā | अठारहवाँ सर्ग | expected 1, printed ॥ २ ॥ | २ २ ३ |
| 404 | Ayodhyā | अठारहवाँ सर्ग | expected 5, printed ॥ ६ ॥ | ३ ४ ६ ७ ८ |
| 404 | Ayodhyā | अठारहवाँ सर्ग | expected 3, printed ॥ २ ॥ | २ २ ३ ४ |
| 438 | Ayodhyā | पचीसवाँ सर्ग | expected 42, printed ॥ ४३ ॥ | ३९ ४०-४१ ४३ ४३ ४४ |
| 438 | Ayodhyā | पचीसवाँ सर्ग | expected 44, printed ॥ ४३ ॥ | ४०-४१ ४३ ४३ ४४ ४५ |
| 459 | Ayodhyā | इकतीसवाँ सर्ग | expected 34, printed ॥ ३५ ॥ | ३२ ३३ ३५ ३५ ३६ |
| 459 | Ayodhyā | इकतीसवाँ सर्ग | expected 36, printed ॥ ३५ ॥ | ३३ ३५ ३५ ३६ ३७ |
| 464 | Ayodhyā | बत्तीसवाँ सर्ग | expected 35, printed ॥ ३६ ॥ | ३३ ३४ १/२ ३६ ॥ ३८ |
| 517 | Ayodhyā | उनचासवाँ सर्ग | expected 7, printed ॥ ८ ॥ | ५ ६ ८ ९ १० |
| 544 | Ayodhyā | पचपनवाँ सर्ग | expected 3, printed ॥ ४ ॥ | १ २ ४ ५ ६-७ |
| 574 | Ayodhyā | तिरसठवाँ सर्ग | expected 52, printed ॥ ५३ ॥ | ५० ५१ ५३ |
| 621 | Ayodhyā | छिहत्तरवाँ सर्ग | expected 1, printed ॥ २ ॥ | २ ३ ४ |
| 634 | Ayodhyā | इक्यासीवाँ सर्ग | expected 4, printed ॥ ५ ॥ | २ ३ ५ ६ ७ |
| 674 | Ayodhyā | तिरानबेवाँ सर्ग | expected 27, printed ॥ १७ ॥ | २५ २६ १७ |
| 681 | Ayodhyā | छियानबेवाँ सर्ग | expected 21, printed ॥ २२ ॥ | १९ २० २२ २३ २४ |
| 705 | Ayodhyā | एक सौ तीनवाँ सर्ग | expected 19, printed ॥ २० ॥ | १७ १८ २० २१ २२-२३ |
| 743 | Ayodhyā | एक सौ पंद्रहवाँ सर्ग | expected 1, printed ॥ २ ॥ | २ ३ ४ |
| 753 | Ayodhyā | एक सौ अठारहवाँ सर्ग | expected 13, printed ॥ १४ ॥ | ११ १२ १४ ॥ ॥ |
| 754 | Ayodhyā | एक सौ अठारहवाँ सर्ग | expected 26, printed ॥ २७ ॥ | २४ २५ २७ ॥ २९ |
| 757 | Ayodhyā | एक सौ उन्नीसवाँ सर्ग | expected 1, printed ॥ २ ॥ | २ ३-४ ५ |
| 794 | Araṇya | ग्यारहवाँ सर्ग | expected 63, printed ॥ ६४ ॥ | ६१ ६२ ६४ ६५ ६६ |
| 795 | Araṇya | ग्यारहवाँ सर्ग | expected 71, printed ॥ ७२ ॥ | ६९ ७० ७२ ७३ ७४—७६ |
| 819 | Araṇya | अठारहवाँ सर्ग | expected 18, printed ॥ १९ ॥ | १६ १७ १९ २० ॥ |
| 858 | Araṇya | इकतीसवाँ सर्ग | expected 14, printed ॥ १५ ॥ | १२ १३ १५ १६ १७ |
| 880 | Araṇya | अड़तीसवाँ सर्ग | expected 5, printed ॥ ६-७ १/२ ॥ | ३ १/२ ४ १/२ ६-७ १/२ ८ १/२ ९ १/२ |
| 894 | Araṇya | तैंतालीसवाँ सर्ग | expected 9, printed ॥ १० ॥ | ॥ ८ १० ११—१३ १४ |
| 912 | Araṇya | सैंतालीसवाँ सर्ग | expected 25, printed ॥ २६ ॥ | २१-२२ १/२ २३-२४ २६ २७ २८ |
| 932 | Araṇya | तिरपनवाँ सर्ग | expected 2, printed ॥ ३ ॥ | १ ३ ४ ५ |
| 1187 | Kiṣkindhā | बयालीसवाँ सर्ग | expected 36, printed ॥ ३७ ॥ | ३४ ३५ ३७ ३८—४० ४१-४२ |
| 1190 | Kiṣkindhā | तैंतालीसवाँ सर्ग | expected 11, printed ॥ १२ ॥ | ९ १० १२ १३ ॥ |
| 1213 | Kiṣkindhā | इक्यावनवाँ सर्ग | expected 11, printed ॥ १९१/२ ॥ | ९१/२ १०१/२ १९१/२ १२१/२ १३१/२ |
| 1213 | Kiṣkindhā | इक्यावनवाँ सर्ग | expected 20, printed ॥ १२१/२ ॥ | १०१/२ १९१/२ १२१/२ १३१/२ १४१/२ |
| 1216 | Kiṣkindhā | बावनवाँ सर्ग | expected 18, printed ॥ १९१/२ ॥ | १६१/२ १७१/२ १९१/२ २०१/२ २१-२२ |
| 1230 | Kiṣkindhā | अट्ठावनवाँ सर्ग | expected 8, printed ॥ ९ ॥ | ६ ७ ९ १० ११ |
| 1240 | Kiṣkindhā | बासठवाँ सर्ग | expected 1, printed ॥ २ ॥ | २ ३ ४ |
| 1414 | Sundara | सैंतीसवाँ सर्ग | expected 41, printed ॥ ४२ ॥ | ३९ ४० ४२ ॥ ४४ |
| 1494 | Sundara | अट्ठावनवाँ सर्ग | expected 32, printed ॥ ३३ ॥ | २९-३० ३१ ३३ ३४ ३५ |
| 1597 | Yuddha | उन्नीसवाँ सर्ग | expected 28, printed ॥ २९ ॥ | २६ २७ २९ ३० ३१ |
| 1635 | Yuddha | उनतीसवाँ सर्ग | expected 18, printed ॥ १९ ॥ | १६ १७ १९ २० २१ |
| 1642 | Yuddha | इकतीसवाँ सर्ग | expected 39, printed ॥ ४० ॥ | ३७ ३८ ४० ४१ ४२ |
| 1669 | Yuddha | चालीसवाँ सर्ग | expected 22, printed ॥ २३ ॥ | २० २१ २३ २३ ॥ |
| 1670 | Yuddha | चालीसवाँ सर्ग | expected 24, printed ॥ २३ ॥ | २१ २३ २३ ॥ २७-२८ |
| 1684 | Yuddha | तैंतालीसवाँ सर्ग | expected 2, printed ॥ ३-४ ॥ | १ ३-४ ४ ५ |
| 1684 | Yuddha | तैंतालीसवाँ सर्ग | expected 5, printed ॥ ४ ॥ | १ ३-४ ४ ५ ६ |
| 1718 | Yuddha | बावनवाँ सर्ग | expected 21, printed ॥ २२ ॥ | १९ २० २२ २२ २३ |
| 1718 | Yuddha | बावनवाँ सर्ग | expected 23, printed ॥ २२ ॥ | २० २२ २२ २३ २४ |
| 1806 | Yuddha | उनहत्तरवाँ सर्ग | expected 18, printed ॥ १९ ॥ | १६ १७ १९ २० २१ |
| 1957 | Yuddha | एक सौ दोवाँ सर्ग | expected 13, printed ॥ १४ ॥ | ९ १०—१२ १४ १५ १६ |
| 1996 | Yuddha | एक सौ ग्यारहवाँ सर्ग | expected 80, printed ॥ ७९ १/२ ॥ | ७८ ॥ ७९ १/२ ८० १/२ ८१ १/२ |
| 2060 | Yuddha | एक सौ अट्ठाईसवाँ सर्ग | expected 49, printed ॥ ५० ॥ | ४७ ४८ ५० ५१ ५२ १/२ |
| 2068 | Uttara | पहला सर्ग | expected 16, printed ॥ १५ १/२ ॥ | १३ १४-१५ १५ १/२ १६-१७ ॥ |
| 2138 | Uttara | बीसवाँ सर्ग | expected 3, printed ॥ ६ ॥ | १ २ ६ ४ ५ |
| 2138 | Uttara | बीसवाँ सर्ग | expected 7, printed ॥ ४ ॥ | २ ६ ४ ५ ६ |
| 2193 | Uttara | बत्तीसवाँ सर्ग | expected 27, printed ॥ २८ १/२ ॥ | २५ १/२ २६ १/२ २८ १/२ २९ १/२ ३० |
| 2223 | Uttara | चालीसवाँ सर्ग | expected 9, printed ॥ १० ॥ | ७ ८ १० ११ १२ |
| 2225 | Uttara | चालीसवाँ सर्ग | expected 29, printed ॥ ३१ ॥ | २७ २८ ३१ २९ ३० |
| 2225 | Uttara | चालीसवाँ सर्ग | expected 32, printed ॥ २९ ॥ | २८ ३१ २९ ३० |
| 2232 | Uttara | तैंतालीसवाँ सर्ग | expected 24, printed ॥ ७ ॥ | ॥ २३ ७ ८ ९-१० |
| 2243 | Uttara | सैंतालीसवाँ सर्ग | expected 12, printed ॥ ३ ॥ | १० ११ ३ ४ ५ |
| 2263 | Uttara | पचपनवाँ सर्ग | expected 16, printed ॥ १७ ॥ | १३ १/२ १४-१५ १७ १८ १९ |

Most gaps are one verse missing between two printed marks (e.g. "५ ६ ८"): either a verse is folded into a neighbour or the e-book lost the number; the text is not short there. Clear misprints: Ayodhyā 18 starts "२ २" (first should be १); Ayodhyā 93 "१७" for २७; Kiṣkindhā 51 "१९१/२" for ११½; Uttara 20 "६" for ३; Uttara 40 "३१ २९ ३०"; Uttara 43 "७" for २४ (then 8, 9… continue the wrong series); Uttara 47 "३" for १२ (series continues).

**Other mark problems:**

- p239 Bāla, पैंतालीसवाँ सर्ग: verse mark without its closing ॥: ॥ २७ (taken as the mark)
- p543 Ayodhyā, चौवनवाँ सर्ग: verse mark without its closing ॥: ॥ ३९-४० (taken as the mark)
- p2157 Uttara, चौबीसवाँ सर्ग: verse mark without its closing ॥: ॥ ४०—४२ (taken as the mark)
- p2237 Uttara, पैंतालीसवाँ सर्ग: verse mark without its closing ॥: ॥ ५ (taken as the mark)
- p2245 Uttara, अड़तालीसवाँ सर्ग: verse mark without its closing ॥: ॥ ८ (taken as the mark)
- p418: a new paragraph starts on the same line after ॥ १२॥ (split there)
- p1061: a new paragraph starts on the same line after ॥ ३१॥ (split there)
- p1061: a new paragraph starts on the same line after ॥ ३२॥ (split there)
- p1061: a new paragraph starts on the same line after ॥ ३३॥ (split there)
- p1061: a new paragraph starts on the same line after ॥ ३४॥ (split there)
- p2045 Yuddha एक सौ पचीसवाँ सर्ग: last paragraph of the sarga has no verse mark at all — "…ष हुआ और उस हर्षातिरेकसे ही वे फिर इस प्रकार बोले—"
- Kiṣkindhā अट्ठाईसवाँ सर्ग (from p1121): mark printed "॥ ६६।" (danda instead of the closing ॥; taken as the mark)
- Yuddha अट्ठाईसवाँ सर्ग (from p1631): mark printed "॥ ११।" (danda instead of the closing ॥; taken as the mark)
- p2073 Uttara 2: "॥ ३० १/२ ॥॥" (doubled ॥, kept in the mark).

**Indented line in mid-paragraph (43):** an indented (new-paragraph) line follows text that has no verse mark; the two are joined into one paragraph. In most the sentence plainly runs on (the e-book broke the paragraph where the printed book turned a page, often next to a leaked page number or a footnote):

- p130 Bāla 8: …ाज! यज्ञ-सामग्रीका संग्रह किया जाय। ⟂ भूमण्डलमें भ्रमणके लिये यज्ञसम…
- p251 Bāla 50: …ी पधारे हैं? जैसे चन्द्रमा और सूर्य ⟂ आकाशकी शोभा बढ़ाते हैं, उसी प्…
- p320 Bāla 76: …न रह सके। उन्होंने परशुरामजीसे कहा— ⟂ ‘भृगुनन्दन! ब्रह्मन्! आपने पित…
- p471 Ayodhyā 34: …मनाओंके बदले आज यहाँसे निकल जाना ही ⟂ अच्छा समझता हूँ और इसीका वरण क…
- p551 Ayodhyā 56: …ड़ा ही रमणीय था। वहाँ उत्तम तीर्थों ⟂ (तीर्थस्थान, सीढ़ी और घाटों) स…
- p621 Ayodhyā 76: … महर्षि वसिष्ठने उत्तम वाणीमें कहा— ⟂ ‘महायशस्वी राजकुमार! तुम्हारा …
- p657 Ayodhyā 89: …कुछ सैनिक बड़ी-बड़ी मशालें जलाकर१ ⟂ अपने खेमोंमें छूटी हुई वस्तुओं…
- p705 Ayodhyā 103: …ने अत्यन्त दु:खी हुए लक्ष्मणसे कहा— ⟂ ‘भाई! तुम इङ्गुदीका पिसा हुआ फ…
- p754 Ayodhyā 118: …उस कथाको इस प्रकार कहना आरम्भ किया— ⟂ ‘मिथिला जनपदके वीर राजा ‘जनक’ …
- p847 Araṇya 28: …त्र श्रीरामने महान् बलशाली और असह्य ⟂ राक्षस-सेनाका वध कर डाला। दूषण…
- p878 Araṇya 37: …रज्वलित अग्निकी ज्वालाके समान असह्य ⟂ हैं, अत: उन सुन्दरी सीतापर बला…
- p1046 Kiṣkindhā 9: …ोनेके कारण मेरी बुद्धिमें ऐसा विचार ⟂ नहीं हुआ॥ २३ १/२ ॥…
- p1084 Kiṣkindhā 18: …तुम तो धर्मके स्वरूपको न समझकर केवल ⟂ रोषके वशीभूत हो गये हो, इसलिये…
- p1181 Kiṣkindhā 41: …ेजसे सम्पन्न मुनिश्रेष्ठ अगस्त्यका५ ⟂ दर्शन करना॥ १५ १/२ ॥…
- p1210 Kiṣkindhā 50: …होंने देखा, वह स्थान बहुत ही उत्तम, ⟂ प्रकाशमान और मनोहर था॥ २०१/२ ॥…
- p1216 Kiṣkindhā 52: … यूथपतियोंको इस प्रकार उत्तर दिया’— ⟂ ‘मैं तुम सभी वेगशाली वानरोंपर …
- p1221 Kiṣkindhā 54: …री आज्ञाका पालन करना इनके लिये सह्य ⟂ नहीं होगा॥ ९ ॥…
- p1230 Kiṣkindhā 58: … युवराज अङ्गदने उनसे इस प्रकार कहा— ⟂ ‘गृध्रराज! यदि आप जटायुके भाई …
- p1236 Kiṣkindhā 60: …भी बड़ा सम्मान करते थे। उस आश्रममें ⟂ निशाकर (चन्द्रमा) नामधारी एक ऋ…
- p1238 Kiṣkindhā 61: …ा, तब यहाँके जंगल हरी-हरी घासकी तरह ⟂ दिखायी देते थे॥ ७ ॥…
- p1240 Kiṣkindhā 62: …नेके बाद महर्षि भगवान् निशाकर बोले— ⟂ ‘सम्पाते! चिन्ता न करो। तुम्हा…
- p1255 Kiṣkindhā 67: …रकारके वृक्ष फैले हुए हैं तथा गैरिक ⟂ आदि धातुओंके समुदाय शोभा दे रह…
- p1263 Sundara 1: …उनकी कमरके नीचेका भाग बहुत लाल था। ⟂ इससे वे महाकपि हनुमान् फटे हुए…
- p1280 Sundara 2: …ियाँ भी उन महलोंकी शोभा बढ़ाती थीं। ⟂ उन सबके कारण राक्षसोंके वे भवन…
- p1294 Sundara 6: … ये महोदर, विरूपाक्ष, विद्युज्जिह्व ⟂ और विद्युन्मालिके घरमें गये॥ १…
- p1345 Sundara 18: …अद्भुत पक्षियोंके कारण उसकी विचित्र ⟂ शोभा होती थी। कितने ही नयनाभिर…
- p1508 Sundara 60: …न दोनोंको यह अनुपम वरदान दिया था कि ⟂ तुम्हें कोई भी मार नहीं सकता। …
- p1614 Yuddha 23: …े विपरीत ताप दे रहे हैं। ये काली और ⟂ लाल किरणोंसे व्याप्त हो इस तरह…
- p1666 Yuddha 39: …ा बढ़ाते हैं, उसी प्रकार प्रासादों१ ⟂ और विमानोंसे२ लङ्कापुरी अत्यन्…
- p1681 Yuddha 42: …िने (आग्नेयकोणमें स्थित हो) दक्षिण२ ⟂ द्वारपर आकर बीस करोड़ वानरोंके…
- p1690 Yuddha 44: …ी बन्धु अपने सभी अङ्गोंमें चोट खाकर ⟂ क्षत-विक्षत हो रहे थे॥ ३५ १/२ …
- p1749 Yuddha 59: … राक्षसराज रावणने आग्नेयास्त्रयुक्त ⟂ रु बाणका संधान करके उसके द्वार…
- p1843 Yuddha 74: …े। ओषधियोंका छिपाना उनके लिये असह्य ⟂ हो गया। उनकी आँखें अग्निके समा…
- p2060 Yuddha 128: …े विभूषित चार सोनेके घड़े देकर कहा— ⟂ ‘वानरो! तुमलोग कल प्रात:काल ही…
- p2193 Uttara 32: …़े हो गये और रावणसे इस प्रकार बोले— ⟂ ‘वाह रे रावण! वाह! तुम्हें युद…
- p2209 Uttara 36: …ोंसे१ सम्पन्न, प्रधानत: तीन मूर्ति२ ⟂ धारण करनेवाले, त्रिलोकरूपी गृह…
- p2212 Uttara 36: …के साथ वायुकी स्वाभाविक मित्रता है, ⟂ उसी प्रकार सुग्रीवके साथ वालीक…
- p2219 Uttara 38: …ठकर प्रतर्दनको छातीसे लगा उनका गाढ़ ⟂ आलिङ्गन किया॥ १९ ॥…
- p2223 Uttara 40: …ा और फिर मधुर वाणीमें विभीषणसे कहा— ⟂ ‘राक्षसराज! तुम धर्मपूर्वक लङ्…
- p2239 Uttara 46: …र उस रथमें सीताजीके लिये सुन्दर आसन ⟂ सुखद शय्यासे युक्त सुन्दर बिछा…
- p2246 Uttara 48: …ावपर चढ़ गये। नावपर चढ़कर उन्होंन े ⟂ मल्लाहको उसे चलानेकी आज्ञा दी॥…
- p2249 Uttara 49: …ह मेरा दिया हुआ अर्घ्य ग्रहण करो और ⟂ निश्चिन्त एवं निर्भय हो जाओ। अ…
- p2263 Uttara 55: …वे राजर्षिको लक्ष्य करके बोलने लगे— ⟂ ‘भूपाल निमे! तुमने मेरी अवहेलन…

### Headings, titles, colophons

- Colophon numbers: p2294 Uttara 65 has the colophon "छाछठवाँ सर्ग … ॥ ६६॥" and p2298 Uttara 66 has "पैंसठवाँ सर्ग … ॥ ६५॥" (swapped); p2381 Uttara 101: "एक सौ एकवाँ सर्ग पूरा हुआ॥ १०२ ॥".
- p1065: colophon misspelt: "इस प्रकार श्रीवाल्मीकिनिर्मित आर्षरामयाण आदिकाव्यके किष्किन्…" (kept)
- p1892: colophon misspelt: "इस प्रकार श्रीवाल्मीकिर्निमित आर्षरामायण आदिकाव्यके युद्धकाण…" (kept)
- p182 and p190 (Bāla 24, 27): the colophon is set in the 21.25pt heading size (recognised by its text).
- p2277 Uttara prakṣipta 2: the title is not bold (delimited with the bookmark text).
- The Araṇya prakṣipta heading is "प्रक्षिप्त सर्ग" (15pt bold, p946); Uttara ones "प्रक्षिप्त सर्ग १", "प्रक्षिप्त सर्ग २" (pp2274, 2277). Their colophons read "…प्रक्षिप्त सर्ग पूरा हुआ॥" (Araṇya, no number) and "॥ १॥", "॥ २॥".

**Titles that differ from the PDF bookmarks** (page text kept; in every case the bookmark is the one with the slip):

- p237: page “देवताओं और दैत्योंद्वारा क्षीर-समुद्र-मन्थन, भगवान् रुद्रद्वारा हालाहल…” / bookmark “४५ देवताओं और दैत्योंद्वारा क्षीर-समुद्र-मन्थन, भगवान् रुद्रद्वारा हाल…”
- p268: page “विश्वामित्रकी तपस्या, राजा त्रिशंकुका अपना यज्ञ करानेके लिये पहले वसिष…” / bookmark “५७ विश्वामित्रकी तपस्या, राजा त्रिशङ्कुका अपना यज्ञ करानेके लिये पहले …”
- p461: page “सीतासहित श्रीरामका वसिष्ठपुत्र सुयज्ञको बुलाकर उनके तथा उनकी पत्नीके ल…” / bookmark “३२ सीतासहित श्रीरामका वसिष्ठपुत्र सुयज्ञको बुलाकर उनके तथा उनकी पन्तीक…”
- p527: page “श्रीरामकी आज्ञासे गुहका नाव मँगाना, श्रीरामका सुमन्त्रको समझा-बुझाकर अ…” / bookmark “५२ श्रीरामकी आज्ञासे गुहका नाव मँगाना,श्रीरामका सुमन्त्रको समझा-बुझाकर…”
- p623: page “भरतका पिताके श्राद्धमें ब्राह्मणोंको बहुत धन-रत्न आदिका दान देना, तेरह…” / bookmark “७७ भरतका पिताके श्राद्धमें ब्राह्मणोंको बहुत धन-रन्त आदिका दान देना, त…”
- p829: page “चौदह हजार राक्षसोंकी सेनाके साथ खर-दूषणका जनस्थानसे पञ्चवटीकी ओर प्रस्…” / bookmark “२२ चौदह हजार राक्षसोंकी सेनाके साथ खर-दूषणका जनस्थानसे पञ्चवटीकी ओर प्…”
- p980: page “श्रीराम और लक्ष्मणकी पक्षिराज जटायुसे भेटं तथा श्रीरामका उन्हें गलेसे …” / bookmark “६७ श्रीराम और लक्ष्मणकी पक्षिराज जटायुसे भेंट तथा श्रीरामका उन्हें गले…”
- p1527: page “चूडामणिको देखकर और सीताका समाचार पाकर श्रीरामका उनके लिये विलाप…” / bookmark “६६- चूड़ामणिको देखकर और सीताका समाचार पाकर श्रीरामका उनके लिये विलाप…”
- p1742: page “प्रहस्तके मारे जानेसे दु:खी हुए रावणका स्वयं ही युद्धके लिये पधारना, उ…” / bookmark “५९- प्रहस्तके मारे जानेसे दु:खी हुए रावणका स्वयं ही युद्धके लिये पधारन…”
- p1861: page “रावणकी आज्ञासे मकराक्षका युद्धके लिये प्रस्थान…” / bookmark “७८- रावणकी आज्ञासे मकराक्षका युद्धके लिये पस्र थान…”
- p1962: page “श्रीरामका रावणको फटकारना और उनके द्वारा घायल किये गये रावणको सारथिका र…” / bookmark “१०३- श्रीरामका रावणको फटकारना और उनके द्वार घायल किये गये रावणको सारथि…”
- p1968: page “अगस्त्य मुनिका श्रीरामको विजयके लिये ‘आदित्यहृदय’* के पाठकी सम्मति देन…” / bookmark “१०५- अगस्त्य मुनिका श्रीरामको विजयके लिये ‘आदित्यहृदय’ के पाठकी सम्मति…”
- p2067: page “श्रीरामके दरबारमें महर्षियोंका आगमन, उनके साथ उनकी बातचीत तथा श्रीरामक…” / bookmark “१- श्रीरामके दरबारमें महर्षियोंका आगमन, उनके साथ उनकी बातचीत तथा श्रीर…”

The differences: 237 bookmark carries stray contents-page text; 268 ङ्कु/ंकु; 461 & 623 bookmark पन्ती/रन्त for पत्नी/रत्न; 527 bookmark adds “को” and has माता-पता; 829 bookmark adds a page number; 980 page भेटं (corrected to भेंट, rule C) / bookmark भेंट; 1527 चूडामणि (page) / चूड़ामणि; 1742 bookmark मूचिर्छत; 1861 bookmark पस्र थान; 1962 bookmark द्वार for द्वारा; 1968 the page title carries the footnote marker *; 2067 bookmark पश्र न.

### Footnotes

- 220 footnotes. They are not at the page foot in this e-book: each stands after a paragraph or after the colophon, at the place where the printed book's page ended, numbered १., २., … or *, at 11.25pt (most) or 15pt (some). Notes run on over following small-type lines, bold Sanskrit quotations and continuation lines.
- Attached by the link from the marker in the text (216). Some note numbers link back to the wrong marker (e.g. p1028 notes १ and २ both point to marker १), so the marker → note link is used first.
- p1288: note without link; attached to the nearest preceding marker “१” (॥ ७१/२ ॥)
- p1288: note without link; attached to the nearest preceding marker “२” (॥ ७१/२ ॥)
- p2210: note without link; attached by its full-size marker “१” in the text (॥ ७ ॥)
- p2210: note without link; attached by its full-size marker “२” in the text (॥ ७ ॥)
- p2210: note without link; attached by its full-size marker “३” in the text (॥ ७ ॥)
- p1683 Yuddha 42: one note "१, २, ३, ४—…" serves four markers; it is attached to each of the four paragraphs.
- p1288 Sundara 4: the note "१-२ वाराहमिहिरकी संहितामें…" (15pt, no link) runs on into an indented paragraph "चार शालाओंसे युक्त गृहको…" before the colophon; kept in the note.
- p111: note २ belongs to the Latin marker "2" on p108.

### Word-level slips of the source text left as printed

After rules A–E and C the machine screen finds no further non-word patterns. Single-occurrence words are overwhelmingly real compounds and inflections; they were not all read by a person — the full list is in `hapax.json` (with the page of each) for a human pass. Spellings that are real words but unusual (e.g. चूडामणि without nukta in a title) are kept as printed.

## Front matter (frontmatter.json)

- pp2–3 are images (no text). नम्र निवेदन pp4–14 (71 blocks, 13 of them notes); विषय-सूची pp15–52 (contents; only its page range is recorded — its entries are the sarga titles and the PDF bookmarks); पाठविधि pp53–66 (blocks); माहात्म्य chapters 1–5 pp67–92, each with heading, title, blocks, verse paragraphs and colophon. The same decoding and corrections apply. Front-matter blocks are separated by indentation, which is good enough for reading but was not proof-read paragraph by paragraph.
- Māhātmya numbering as printed has gaps and a repeat (ch.1 jumps 30→34 and ends “४२-४३”; ch.4 has “१५” then “१५ १/२”, “४४ १/२” twice and “४५-४५”); bare ॥ marks there are kept as separate paragraphs with `from: null`.

## Unresolved / for the owner

1. **1412 verse marks have no number in this PDF**; their `from`/`to` are inferred from the neighbours. They should be checked against the printed book or the Sanskrit edition (the sanskrit-english PDF).
2. The 68 numbering gaps/repeats above are as printed; the inferred ranges next to them may need adjusting once the missing numbers are known.
3. Rule C entries (manual_fixes.json), especially p1749 “आग्नेयास्त्रयुक्त रु बाणका” → “…युक्त बाणका”, and rule E, are corrections of the e-book text; please confirm them.
4. Spacing after a line-end em dash is a convention choice (no space), not something the page shows.
