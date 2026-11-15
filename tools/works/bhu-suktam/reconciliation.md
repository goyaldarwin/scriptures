# Bhū Sūkta — how the text is settled

**Which text.** The recording (Soul Sadhana, `RBrq8UeM1N4`, "Bhu Suktam") sings, by its Whisper transcript (`audio/soul-sadhana/transcripts/`): "बूमिर बहुम नान्दियोर बरिना … तरिक्शम महित्वाः उपस्तेः … तन्ना द्याया ददे" (भूमिर्भूम्ना द्यौर्वरिणाऽन्तरिक्षं महित्वा । उपस्थे … अन्नाद्यायाऽऽदधे), "मातरं पुनः पितरं" (आयं गौः … मातरं पुनः । पितरं च प्रयन्त्सुवः), "विराजति … पतंगाय" (त्रिꣳशद्धाम वि राजति वाक्पतङ्गाय शिश्रिये), "प्राणादपान…", "यत्त्वा क्रुद्धः परोवप मन्युना यदवर्त्या सुकल्पमग्ने … पुनस्त्वोद्दीपयामसि", "यत्ते मन्युपरोप्तस्य पृथिवीमनु दध्वसे आदित्या विश्वे तद्देवा", "मनो ज्योतिर्जुषताम् … बृहस्पतिस्तनुतामिमं … मादयन्ताम्", then the śānti. That is Taittirīya Saṃhitā 1.5.3.1–2, not the Atharvaveda's Pṛthivī Sūkta (12.1) that shlokam.org gives as "Bhoomi Suktam". A written witness of it is in the owner's download folder, so the text is made from that witness, and the work moves from the Atharvaveda's shelf to the Kṛṣṇa Yajurveda's Saṃhitā (its ids were not published).

**Source of truth:** Sanskrit Wikisource's Taittirīya Saṃhitā kāṇḍas 1–4 with svaras (`तैत्तिरीयसंहिता-१-४`, raw wikitext, fetched by the owner's download script; private copy in scriptures-data at `hinduism/veda/yajurveda/krishna-yajurveda/samhita/bhu-suktam/printouts/wikisource/`). The page names no edition; it is a user transcription with svaras throughout, the same site's Saṃhitā that witnesses the Nīlā Sūkta.

## Method
1. **Extract.** `source/extract.py` takes the page's 1.5.3.1 and 1.5.3.2 from भूमि॑र्भू॒म्ना to मा॑दयन्ताम् ।।: the sūkta as the Pañca Sūkta recites it and the recording sings it. The rest of 1.5.3.2 (स॒प्त ते॑ अग्ने…) is the Saṃhitā's next mantra, not recited with it. The page writes ꣳ, the svarita ᳚ and a visarga with private-use characters of its font, read by their places (`tools/works/sukta_witness.py` → `PUA`): here त्रि॒ꣳ॒शद्धाम॒, य॒ज्ञꣳ and त्वा᳚. Its labels (1.5.3.2) and section numbers ([10]) are dropped.
2. **Settle.** `source/settle.py`: one item per ṛk, as the page ends each with ।।; the lines at its daṇḍas (।).
3. **Check.** `source/check.py` compares the text with the page word for word and svara for svara: the only difference is the ॐ below.
4. **The writing standard** (docs/PLAYBOOK.md §3) applies at export: ॥, Pāṇini's spelling, ꣳ (a Yajurveda text), the ISO 15919 transliteration with the svaras as accents.

## Added from the recording
- **ॐ before the first ṛk:** the recording opens with it (its transcript).
- **The closing śānti,** ॐ शान्ति॒-श्शान्ति॒-श्शान्तिः॑ ॥, which the recording sings after the sūkta: worded as the same site's accented Taittirīya Āraṇyaka closes its Upaniṣad prapāṭhakas (ओं शान्ति॒श्शान्ति॒श्शान्तिः॑), in the hyphenated spelling of the Sūktas' other texts.

## Kept as the page has it
- **The Taittirīya spellings:** पृश्ञि॑ (pṛśni, as the Taittirīya reciters say it), आऽयं, स॒माभ॑रन्न् (the doubled final न्न्), यत् त्वा and तत् तव written apart.
- **No second written witness** of Taittirīya Saṃhitā 1.5.3 was found: Wikisource's unaccented Saṃhitā is downloaded for 4.4 only, and GRETIL has no Taittirīya Saṃhitā or Bhū Sūkta. Nothing in the passage is a non-word or broken, so the page stands as it is.

## Structure (not on the page as such)
- **Numbering:** the ṛks 1–7 by their place.
- **Sections:** `sukta` (the seven ṛks), `end` (the śānti).

## Word meanings
Every word has an entry in the shared dictionary (`library/glossary/sa.json`), checked in Monier-Williams and Apte. Sāyaṇa's commentary is not at hand here, so where a reading is open the dictionaries and the grammar decide, and no sense is put to any commentator. A word the recitation joins with a hyphen (the Taittirīya way) is one key, its words in `p`.
- **भूम्ना** (1): both senses, भूमन् "abundance" and "the earth" (Monier-Williams).
- **परोवप** (5): परा + उवप (√वप्, perfect), "scattered away"; **दध्वसे** (6): the Vedic perfect of √ध्वंस्, "fell scattered".
