# Design: more meaning languages (Punjabi first), and room for the verse in more than one script

Owner, 2026-10-23: "design interface for supporting Punjabi and other languages. For now we will support only Punjabi" — and "right now the text of the verse is fixed and we don't have different text in different languages. In future that might also change. Please keep this in mind."

Status: **proposed**, to be built as shared-code changes (each its own pull request with UX tests) once the owner agrees.

## What is fixed today
- Meaning layers are hard-coded as two: `hi` and `en` (meaning files `lang: "hi" | "en"`; the header capsule हिं · En · शब्द · 📖; `S.settings.layers = {h, e, w}`; `mean('hi'|'en')`; search scopes h/e).
- Every label is `{hi, en}`; the interface is Hindi or English (`LANG()`).
- Word meanings are `{hi, en}` per dictionary entry.
- The verse is one text per item (`v`), plus an optional Roman transliteration (`t`).

## 1. Meaning languages become a list (Punjabi first)
- **Registry:** `library/glossary/languages.json` gains, for each language a reader can read a meaning in, a `meaning` block: `{"short": "ਪੰ", "name": {"hi": "पंजाबी", "en": "Punjabi", "pa": "ਪੰਜਾਬੀ"}, "font": "Gurmukhi", "order": 3}`. Today: `hi`, `en`, and the new `pa`. Adding a language later is one entry, no app change.
- **Meaning files:** `lang` may be any registered meaning language (`pa-scriptures` for our Punjabi). `build.py` refuses an unregistered one. Everything else (order, title, `m`, line-by-line `p`) is the same.
- **Header capsule:** shows a switch for each meaning language **the open work has a source for**, in registry order, then शब्द and 📖. The Mānas keeps हिं · En · शब्द · 📖; the Sukhmani Sahib shows ਪੰ · हिं · En · शब्द · 📖 (a work can name its own order: Gurbani puts ਪੰ first). Settings: `layers` becomes `{hi, en, pa, w}`; old phones' `{h, e, w}` are read as before.
- **Reader:** under each verse (or each line, when the source gives `p`), the layers in the work's order. Colours as today: the first layer in full ink, later ones lighter.
- **More › Sources:** one list per meaning language the work has.
- **Search:** one scope per meaning language.

## 2. Word meanings in more languages
- A dictionary entry may carry more meaning fields than `hi` and `en`, e.g. `"pa": "…"` in `pa.json` for a Gurmukhi word. The word sheet shows the fields for the meaning layers the reader has on (falling back to `hi` / `en`). Entries without `pa` simply show Hindi and English, so this can be filled in gradually.

## 3. The interface language stays Hindi / English for now
- Labels stay `{hi, en}`; a Punjabi interface later means adding `pa` to the label list with an English fallback, and a third choice in "Language of the app". Not part of this change.

## 4. Room for the verse in another script or language (not built now)
The verse and its number stay the core (`v`, ids permanent). An alternative rendering of the same text — the Sukhmani Sahib in Devanagari for Hindi readers, the Mānas in Gurmukhi, the Roman transliteration we already have — becomes a **text source**, like a meaning source:
- `library/<work>/texts/<id>.json`: `{"id": "hi-devanagari", "script": "Deva", "lang": "pa", "title": {…}, "v": {item id: [lines]}}`.
- **Same items, same lines:** every rendering has the item's ids and exactly its number of lines, and (for a transliteration) the same words per line — so line-by-line meanings, audio timings, bookmarks and notes stay attached, and a tapped word maps back to the dictionary word at the same position. `build.py` checks it.
- The reader chooses the script in More › Sources; the transliteration switch becomes one such choice. A different recension (different words or lines) is a different work, not a text source.
- Nothing in the current data has to change for this: today's `v` is the default text source, `t` the Roman one.

## Order of work
1. Meaning languages as a list, with `pa` registered; the ਪੰ switch appears only on works that have a Punjabi source (none until the next step).
2. Our Punjabi meaning of the Sukhmani Sahib (`pa-scriptures`), line by line, written from the Gurmukhi with the Mahan Kosh, the Faridkot Teeka and Sahib Singh's Darpan as checks (style.md §12).
3. Punjabi in the word sheet, filled in as the meanings are written.
4. Text sources: when the owner wants a second script.
