# Bhaja Govindam — how the text is settled

**Source of truth:** the owner's printout of sanskritdocuments.org, *भज गोविन्दम्*
(<https://sanskritdocuments.org/doc_vishhnu/bhajagovindam.html>): verses 1–31, a verse 13अ after verse 13, and two more
(32, 33) that it says "are not found in standard text". It gives some variant readings beside the lines ("var …"). Its text
layer is Unicode; the printout's layout breaks a few words (कु रु, डुकृ ङ्करणे, लुञ्छितके शः, सकृ दपि), read as one word.

**Second witness:** the owner's recording, Chinmaya Mission Boston, "Bhaja Govindam full, Verses 1 to 31" (YouTube
`xrNOEva86pA`), through its transcript (`audio/chinmaya-mission-boston/`) and, at the variant readings, the same speech
model on 2.5–3 s windows.

The library's writing standard (docs/PLAYBOOK.md §3) applies when the text is exported (॥ and compact verse numbers,
Pāṇini's spelling: सुरमंदिर… is written सुरमन्दिर…, the ISO 15919 transliteration made from the verse).

## Which verses, in which order
The recording sings verses 1–31 in the printout's order (the owner: the verses follow the recording). It does not sing
13अ or 32–33.
- **1–31** are the text.
- **13अ** (द्वादशमञ्जरिकाभिरशेषः…, the close of the twelve verses) is kept, as the printout numbers it, without a time
  (`audio/chinmaya-mission-boston/fixes.md`).
- **32, 33** are left out: the printout itself puts them outside the standard text, and the recording does not sing them.

## Readings
Where the printout gives a variant and the recording sings it, the text follows the recording:

| Verse | Printout | Variant it gives | Recording | Text |
|---|---|---|---|---|
| 7 | परमे ब्रह्मणि | परे | "परमें" | परमे (the printout) |
| 11 | मायामयमिदमखिलं हित्वा | बुध्वा | "अदिलं बिद्वाँ" | बुद्ध्वा: the recording's reading, in correct Sanskrit (budh + ktvā is बुद्ध्वा; the printout's बुध्वा drops a द्) |
| 17 | मुक्तिं न भजति जन्मशतेन | भजति न मुक्तिं | "बजज़िना मोग… विना मुँ" | भजति न मुक्तिं जन्मशतेन (the same words) |
| 26 | त्यक्त्वाऽऽत्मानं भावय कोऽहम् | पश्यति सोऽहम् | "परश्वेटि सोबं" | त्यक्त्वाऽऽत्मानं पश्यति सोऽहम् |

Corrected: नास्तिततः (29) is two words in the printout's own word list and in sense, नास्ति ततः ("there is not… in it"):
a missing space. **Open** (one witness for the spelling; the recording cannot show a space).

Kept as printed: the line ends where two pādas are printed on one line by sandhi (5, 8, 12, 16, 24, 26: e.g.
यावद्वित्तोपार्जनसक्तस्तावन्निजपरिवारो रक्तः), so those verses have three lines; नित्यानित्य विवेकविचारम् (30) with its
space; बिभ्यति (6), a plural form used of the wife, as the tradition reads it.

## Divisions
The topics follow the printout's introduction: verse 1, the refrain; 2–13, the Dvādaśa-mañjarikā; 14–27, the
Caturdaśa-mañjarikā, which it ascribes verse by verse to fourteen disciples; 28–31, the closing verses (the printout
ascribes 28 to Sumati, as it does 27, and gives no ascription for 29–31, so the heading names no author).

## Meanings
Our own Hindi and English, line by line, from the Sanskrit, in the Advaita reading (tools/meanings/style.md). The copied
English (`meanings/en/sanskritdocuments.json`) is the printout's English under each verse, kept as printed except
"vairgya" → "vairagya" and the space it types before ! and ?. It translates the printout's main readings (verse 26:
"Ponder over your real nature").
