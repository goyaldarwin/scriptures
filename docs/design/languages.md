# Design: meaning languages, and room for the verse in more than one script

The owner's request: "design interface for supporting Punjabi and other languages. For now we will support only Punjabi", and "right now the text of the verse is fixed and we don't have different text in different languages. In future that might also change. Please keep this in mind."

Built: meaning languages as a list (§1), Punjabi meanings of the Sukhmani Sahib, and the app's support for Punjabi word meanings (§2). Designed, not built: Punjabi in the dictionaries (§2), a Punjabi interface (§3) and text sources (§4).

## 1. Meaning languages are a list (built)
- **Registry:** `library/glossary/languages.json` gives each language a reader can read a meaning in a `meaning` block: `{"short": "ਪੰ", "name": {"hi": "पंजाबी", "en": "Punjabi", "pa": "ਪੰਜਾਬੀ"}, "order": 3}`. The meaning languages are `hi`, `en` and `pa`. Adding one is one entry, with no app change (`docs/LIBRARY.md` §5).
- **Meaning files:** `lang` may be any meaning language (`pa-scriptures` is our Punjabi). `tools/site/library.py` refuses any other. Everything else (`order`, `title`, `m`, the line-by-line `p`) is the same for every language.
- **Header capsule: always four places — two meaning switches, then शब्द and 📖.** The reader's header has about 58 px free at 390 px and 28 px at 360 px, so a fifth switch would not fit smaller phones or larger text. A work with two meaning languages shows both (the Mānas: हिं · En · शब्द · 📖). A work with a third shows the reader's chosen pair; the default is **ਪੰ · En** in an English app and **ਪੰ · हिं** in a Hindi app. ☰ › More › Sources has "Meanings in the bar" to choose the pair, so the third meaning is never lost.
- **Settings:** `S.settings.layers` is `{h, e, w}` plus the code of any other meaning language (`pa`). The pair is `S.settings.pair`.
- **Reader:** under each verse (or each line, when the source gives `p`), the meanings of the switches that are on, in the languages' order. The first in full ink, the next lighter. Punjabi is set in a Gurmukhi font.
- **☰ › More › Sources:** one list per meaning language the work has.
- **Search:** one scope per meaning language (the ਪੰ chip shows only on works with a Punjabi source).

## 2. Word meanings in more languages
- **Built (app):** a dictionary entry may carry a `pa` meaning beside `hi` and `en`. The word sheet shows it, and the word list shows it while the ਪੰ switch is on. Entries without `pa` show Hindi and English, so the dictionaries can be filled in gradually.
- **Not built (data):** no dictionary entry has `pa` yet. It is to be filled in from the Gurmukhi words of the Sukhmani Sahib (`library/glossary/pa.json`), with the Mahan Kosh as the check (`tools/meanings/style.md` §11).

## 3. The interface language is Hindi or English (designed, not built)
- Labels are `{hi, en}`, and the interface language is chosen with हिं · En on the library, work and vidhi pages. A Punjabi interface would add `pa` to the labels with an English fallback, and a third button there.

## 4. The verse in another script or language (designed, not built)
The verse and its number are the core (`v`, ids permanent). Another rendering of the same text (the Sukhmani Sahib in Devanagari for Hindi readers, the Mānas in Gurmukhi, the Roman transliteration we already have) is a **text source**, like a meaning source:
- `library/<work>/texts/<id>.json`: `{"id": "hi-devanagari", "script": "Deva", "lang": "pa", "title": {…}, "v": {item id: [lines]}}`.
- **Same items, same lines:** every rendering has the item's ids and exactly its number of lines, and (for a transliteration) the same words per line. Line-by-line meanings, audio timings, bookmarks and notes stay attached, and a tapped word maps back to the dictionary word at the same position. `library.py` checks it.
- The reader chooses the script in ☰ › More › Sources; the transliteration switch becomes one such choice. A different recension (different words or lines) is a different work, not a text source.
- Nothing in the current data has to change for this: `v` is the default text source, `t` the Roman one.
- To be built when the owner wants a second script.
