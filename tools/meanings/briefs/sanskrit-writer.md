<!-- The first step for each batch of a Sanskrit work's reviewed meanings (docs/HOW-TO.md, "Write our own meanings for a Sanskrit work"). Paths are relative to the repository root. -->
# Brief for writing our own meanings of a Sanskrit work

You are writing the Hindi and English meanings ("bhāvārtha") for a batch of verses of a Sanskrit work, for a free, ad-free scripture-reading app owned by Darwin Goyal. The owner reads both languages and cares above all about **accuracy**, then unambiguity, clarity and consistency; accuracy and consistency are never traded for anything, including distance from another translation.

**Before anything else:** `python3 tools/meanings/sanskrit_dict.py fetch && python3 tools/meanings/sanskrit_dict.py check`. If it fails, stop and report it — never write a meaning without Monier-Williams and Apte.

## The works

| Work (`--work`) | Library folder | Traditional reading | Copied sources (the copy check) |
|---|---|---|---|
| `bhagavad-gita` | `library/hinduism/granth/vyasa/bhagavad-gita/` | Śaṅkara's bhāṣya; where Rāmānuja or Madhva read a verse materially otherwise, a short footnote | `meanings/en-besant.json`, `meanings/en-telang.json` (English) |
| `durga-saptashati` | `library/hinduism/stotra/durga/durga-saptashati/` | the plain reading of the words and the grammar, as the recitation tradition (Gita Press's edition, Nāgojībhaṭṭa, the Guptavatī) takes it; a footnote only for a well-known second reading | `meanings/en-pargiter.json` (English) |

## Read first
1. `tools/meanings/style.md` — the style sheet, all of it; §1, §2, §4, §5 and §8 above all. It is binding.
2. The voice to match: our reviewed Sanskrit meanings, the Kaṭha Upaniṣad's (`tools/works/katha-upanishad/meanings/hi/scriptures.json`, `en/scriptures.json`, with their `notes`) and the Āditya Hṛdayam's (`tools/works/aditya-hridayam/meanings/…`, one piece per verse line).
3. Your batch file `batch-NN.md` (named in your task): the verses just before it, then each verse with its transliteration, our word meanings for every word, and the work's present meaning (**Our Hindi / Our English**: the owner's drafts, ours, not yet reviewed).

## How to write each verse
1. **From the verse, its word meanings, the dictionaries and its context.** Work out exactly what the verse says: who speaks to whom (Sañjaya to Dhṛtarāṣṭra, the Lord to Arjuna; the sage Medhas to King Suratha and the merchant Samādhi, the gods to the Devī), what has just happened, what the moment means in the work. Look up every word of the verse in Monier-Williams and Apte (`python3 tools/meanings/sanskrit_dict.py look <word> …`, the stem where an inflected form is not found); split compounds and sandhi with care; follow the grammar (case, number, person, tense, the voice of the verb). Where the dictionaries and our word meaning disagree, follow the dictionaries and the grammar and note the word in `batch-NN.words.jsonl`.
2. **The present draft is ours** (the owner's, written from the verse): read it after you have worked out the verse. Keep any of its wording that is accurate and in the style sheet; correct everything that is not (a sense missed or added, a clause left out, the wrong subject or tense, a gloss in brackets, a moral drawn, style). Never keep a sentence only because it is there.
3. **Write the Hindi and the English** following the verse line by line and half-line by half-line (`style.md` §2, §8): one to three sentences for a śloka; a list of epithets one phrase per epithet in the verse's order, ending with the verse's verb. The speaker's line (सञ्जय उवाच, श्रीभगवानुवाच, ऋषिरुवाच, देव्युवाच) is its own verse line, and its piece is the opening: "सञ्जयने कहा —" / "Sañjaya said:", "श्रीभगवान्‌ने कहा —" / "The Lord said:", "ऋषिने कहा —" / "The sage said:", "देवीने कहा —" / "The Devī said:" (ZWNJ U+200C in श्रीभगवान्‌ने). The closing words (iti) say what the verse says ("Thus ends the …").
4. **Footnotes, rarely:** only where the traditional reading of the table above differs materially from another well-known reading, or where a term would otherwise mislead (one short sentence each, Hindi and English saying the same). Never a sermon, never a summary of the verse, never a doubt about the text.
5. **Then check the copy rule** for the English against the work's copied sources (the table): `python3 tools/meanings/overlap.py OUT/batch-NN.en.json <library folder>/meanings/<source>.json --report` for each. It must end with "0 with a shared run of 10+ words". A 6–9-word run is fine when it is the natural words or the verse's own list; reword in your own sentence shape only what follows their phrasing, changing **only the wording** (same subject, object, speaker, tense, every clause), and read the reworded piece against the verse again.

## Rules you must not break
- Accuracy: every clause of the verse is in the meaning; nothing invented; no commentary, no moral; no bracketed explanation (a short round-bracket gloss only where a word would otherwise be unclear, rarely; never square brackets).
- **No verse numbers** in your text — the exporter adds them.
- Address: the Lord addresses Arjuna (and anyone) with तुम; Arjuna and devotees address the Lord or the Devī with आप; honorific plural for the Lord, the Devī, sages, kings and elders in narration. An epithet in address is kept and, in English, translated: "हे महाबाहो!" / "O mighty-armed one", "हे कौन्तेय!" / "O son of Kuntī", "हे भारत!" / "O Bhārata" (a name stays a name).
- Hindi: `style.md` §4 (joined postpositions, लिये/गये/दिये, standard spelling of names: अर्जुन, श्रीकृष्ण, धृतराष्ट्र, सञ्जय, दुर्योधन, भीष्म; देवी, महिषासुर, शुम्भ, निशुम्भ, चण्ड, मुण्ड, रक्तबीज).
- English: `style.md` §5 (IAST names, ṃ for the anusvāra, lower-case pronouns for the Lord and the Devī, British spelling, a colon before speech, no quotation marks). Sanskrit terms that have no good English word stay in IAST and are glossed in the sentence once in the batch (dharma, yoga, ātman, brahman, guṇa, prakṛti, karma): "dharma, his sacred duty".
- Do **not** edit any file in the repository — write only in the batch folder.

## Output (in the batch folder; NN = your batch number)
- `batch-NN.hi.json` and `batch-NN.en.json`: `{"<id>": ["<piece for line 1>", …], …}` — exactly the ids of `batch-NN.ids`, in that order, each once; **one piece per verse line**, each reading on its own under its line. Where one sentence cannot be cut (the verb only in the later line), keep it in the later line's piece and give the earlier line `""`, but cut whenever the lines carry their own sense; Hindi and English cut at the same lines. UTF-8, `ensure_ascii=False`.
- `batch-NN.notes.json` (may be `{}`): `{"<id>": {"hi": ["…"], "en": ["…"]}}`.
- `batch-NN.doubts.jsonl` (may be empty): `{"id", "issue", "our reading", "alternatives"}` — only genuine doubts of reading (the session settles them).
- `batch-NN.words.jsonl` (may be empty): `{"id", "word", "current", "suggested": {"hi", "en"}, "reason"}` — a word meaning in our dictionary that is wrong or lacks the sense this line needs.
- Final reply (short, plain): verses written, how many drafts you changed in substance (not style), overlap result, number of footnotes, doubts and word issues.

Before finishing, verify with `python3 -c`: both json files load, have exactly the ids of the .ids file in order, each with exactly as many pieces as the verse has lines (`<library folder>/work.json` → `items[].v`), at least one non-empty piece, `""` at the same lines in Hindi and English, no "।।" or "॥" followed by a digit and no "(1)"-style numbers; and the overlap checks pass.
