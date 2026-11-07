# The Hindi of the Śiva Purāṇa, from the owner's scans

The scans (Gita Press code 2223; Kalyan's 2018 Śivamahāpurāṇāṅka) have no text layer. The owner's choice for them: the Hindi is read by OCR, and every word the checks flag is read by eye on the page image before it is used (`docs/PLAYBOOK.md` §11 stays the rule for every other book; the scans' `.meta.json` in `scriptures-data` say so too).

- `ocr.py`: the raw passes of one page range → `ocr/<book>/p<NNNN>.json` (the gutter; per Hindi column Tesseract's `hin` and `Devanagari` passes, the second with each em dash told from a hyphen by its ink; a whole-page `hin` pass for the lines that run across both columns). Run on GitHub by the `ocr` workflow (`docs/HOW-TO.md`, "OCR a scanned book"), or here.
- `ocr/shiv-1/`: Gita Press code 2223 (layout `sh`: Sanskrit left, Hindi right). `ocr/kalyan-2018/`: Kalyan 2018 (layout `hh`: Hindi in both columns).
