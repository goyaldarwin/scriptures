# Bilvāṣṭakam — how the text is settled

**Source of truth:** the owner's pasted text, the words of the Sounds of Isha recording (`source/owner-text.txt`).

**Second witness:** the owner's printout of sanskritdocuments.org, N. Balasubramanian, *सार्थ बिल्वाष्टकम्*
(<https://sanskritdocuments.org/doc_shiva/bilva8mean.html>, file `bilva8mean.itx`, updated 15 August 2004), which gives the
same ten verses with word meanings and an English meaning. Its text layer is Unicode; a few words are broken by the
printout's layout (नन्दिके श्वरे, कु ठरायुधपाणिः), which are read as one word.

**Third witness:** the recording itself, Sounds of Isha (YouTube `6rJExE8HGVg`), through its transcript
(`audio/sounds-of-isha/transcripts/`). It sings ślokas 1, 3–7, the Kāśī śloka and 8 (and 1 again at the end), in the
text's order; it does not sing śloka 2 or the phalaśruti (`audio/sounds-of-isha/fixes.md`).

The library's writing standard (docs/PLAYBOOK.md §3) applies when the text is exported: ॥ and compact verse numbers (`॥१॥`), Pāṇini's spelling
(a word-final m before a vowel is written म् in the library, though `text.txt` keeps ं: त्रिजन्मपापसंहारम् एकबिल्वं, सोमयज्ञ महापुण्यम् एक…, कोटिकन्या महादानम् एक…,
अघोरपापसंहारम् एक…), the ISO 15919 transliteration made from the verse.

## Choices
| Verse | Owner's text | Printout | Text | Why |
|---|---|---|---|---|
| sh1 | त्रिनेत्रं **च** त्रियायुधम् | त्रिनेत्रं त्रियायुधम् | as the owner's | the pāda needs eight syllables (anuṣṭubh): without च it has seven; the recording sings च (“चत्रिया आयुदं”) |
| sh1 | शिवार्पणम् | शिवार्पण्म् | शिवार्पणम् | the printout's typing slip |
| sh3 | अखण्ड बिल्व पत्रेण | अखण्ड बिल्वपत्रेण | अखण्ड बिल्वपत्रेण | the compound बिल्वपत्र is one word (the printout, and the owner's own बिल्वपत्रैः in śloka 2) |
| sh5 | सहस्राणि | सहस्राणी | सहस्राणि | the printout's slip (its own word meanings write सहस्राणि) |
| sh7 | शिवार्पणम् | शिवर्पणम् | शिवार्पणम् | the printout's slip |
| kashi | प्रयागमाधवं | प्रयाघमाधवं | प्रयागमाधवं | Prayāga; the printout's slip |

Kept as both witnesses write them: the spaced compounds अखण्ड बिल्वपत्रेण, शालिग्राम शिलामेकां, सोमयज्ञ महापुण्यं,
दन्तिकोटि सहस्राणि, वाजपेय शतानि, सर्वपाप विनिर्मुक्तः; त्रिशाखैः बिल्वपत्रैश्च (visarga kept before ब); पठेत्
शिवसन्निधौ (unjoined; strict sandhi gives पठेच्छिवसन्निधौ); ह्येकबिल्वं in ślokas 2, 3, 6, the Kāśī śloka and 8 and
एकबिल्वं in 1, 4, 5 and 7, as each witness has it verse by verse.

## Numbering (open)
The owner's text numbers ślokas 1–7, leaves the Kāśī śloka without a number, numbers मूलतो ब्रह्मरूपाय… as 8 and leaves
the phalaśruti unnumbered: eight numbered ślokas, an aṣṭaka. The printout numbers all ten, 1–10 (Kāśī 8, मूलतो 9,
phalaśruti 10). The text follows the owner's text. **Open:** the owner may prefer the printout's 1–10; item ids would stay (`docs/reviews/bilvashtakam-doubts.jsonl`).

## Title and closing words
The owner's heading is बिल्वाष्टक; the title is बिल्वाष्टकम्, as the closing words (॥ इति बिल्वाष्टकम् ॥) and the
printout have it. The printout ends with ॥ ॐ तत्सत् ॥ instead of closing words; the text keeps the owner's.

## Meanings
Our own Hindi and English, line by line, from the Sanskrit (tools/meanings/style.md). The refrain एकबिल्वं शिवार्पणम् is
rendered the same way each time it stands alone (“एक बिल्वपत्र शिवजीको अर्पण है” / “one bilva leaf is offered to Śiva”);
in ślokas 4, 5, 7 and the Kāśī śloka the line reads it as what the gifts and pilgrimages are equal to, which the
grammar gives (the bilva offering stands in apposition to the merits listed). Many read them as “surpasses”; our
footnote says so, and the question is in `docs/reviews/bilvashtakam-doubts.jsonl`.

The copied English (`meanings/en/sanskritdocuments.json`) is each verse's “Meaning of the verse” in the printout (for
śloka 1, the translation given after its word meanings). Fixed: “bila” → “bilva”, “uttereing” → “uttering”. Its
meanings of ślokas 8–10 are given to `kashi`, `sh8` and `phala` by their words.
