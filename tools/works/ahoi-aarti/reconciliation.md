# Reconciliation: जय अहोई माता

## Witnesses
- **Aarti Mala (base):** scriptures-data `hinduism/chalisa/books/aarti-chalisa-sangrah/` (page image i-335, "श्री अहोई माता की आरती", a printout of indif.com), read on the page image. Eight printed lines, each two halves joined by a daṇḍa and followed by the refrain cue (जय·): the refrain (जय अहोई माता), ब्रह्माणी रूद्राणी, माता रूप, तू ही है पाताल, जिस घर, तुम बिन, शुभ गुण, and the closing श्री अहोई माँ की आरती. (Its page i-339, also listed in the kit, is the Durgā āratī अम्बे तू है काली.)
- **Drik Panchang** (`hinduism/aarti/ahoi/ahoi-aarti/printouts/drikpanchang/ahoi-mata-aarti.html`): the same text in the same order, a half-line per line.
- **The Randhir book** (५१ चालीसा संग्रह आरतियों सहित, Randhir Prakashan, pp. 190–191, page images i-189, i-190) has no Ahoī āratī: the pages the kit lists are its Lakṣmī āratī (जय लक्ष्मी माता), which shares this āratī's frame and many lines. It is not a witness of this text and was not used.

The rule: keep the base; correct it only where it is clearly wrong. The library's writing standard (docs/PLAYBOOK.md §3): an āratī's verse has no comma; the refrain (टेक) is shown once; stanzas numbered (॥१॥).

| Place | Base | Ours | Why |
|---|---|---|---|
| every stanza | one printed line, its halves joined by a daṇḍa | two lines, ending । and ॥N॥ (the refrain ॥) | The standard; the daṇḍa marks the half. |
| refrain, line 2 | हरि विष्णु धाता | हर विष्णु विधाता | The line names the three gods (Hara, Viṣṇu, the Creator); हरि is Viṣṇu himself, named twice, and the half is a mātrā short of the ten every other second half has. Drik Panchang has हर विष्णु विधाता. |
| stanza 1, line 1 | जग दाता | जग माता | A slip for माता: Drik Panchang (जगमाता) and India TV's text of this āratī (indiatvnews.com, Ahoi Ashtami 2017) have माता, and the line is the Lakṣmī āratī's, whose frame this āratī takes (the Randhir book, p. 191, page image i-190: ब्रह्माणी कमला तू ही है जग माता). See "Readings settled". |
| stanza 1, line 1 | रूद्राणी | रुद्राणी | रुद्र has a short u; Drik Panchang has रुद्राणी. |
| stanza 4, line 1 | वही मे | वही में | A dropped anusvāra (मे is not the postposition). |
| stanzas 4, 5, 6 | नही (घबराता, आता, पाता) | नहीं | A dropped anusvāra; Drik Panchang has नहीं. |
| after every stanza | जय· | not written | The refrain cue; the refrain is shown once. |
| stanza numbers | none | ॥१॥ … ॥७॥ | The standard. |
| stanza 3, line 1 | तू ही है पाताल बसन्ती तू ही है सुख दाता | तू ही पाताल बसन्ती तू ही है शुभदाता | The recording (Ambey Bhakti) sings Drik Panchang’s words (तुही पाताल बसन्ती … शुभ दाता); an āratī follows its recording (PLAYBOOK §3). The base’s spelling बसन्ती is kept. |
| stanza 4, line 1 | थारो वास वही में | थारो वासा वाहि में | Sung वासा, as Drik Panchang prints it with वाहि; the base’s घबराता (Drik धड़काता) is kept in line 2, where the recording is not clear. |
| stanza 5, line 1 | पुत्र न कोई पाता | न कोई पुत्र पाता | Sung in Drik Panchang’s order (ना कोई पुत्र पाता). |

Kept as the base has them: निसदिन, सूर्य चन्द्रमा (Drik सूर्य-चन्द्रमा), सुख सम्पत्ति (Drik सुख-सम्पत्ति), कर्म प्रभाव (Drik कर्म-प्रभाव), कर ले, घबराता (Drik धड़काता), खान-पान, क्षीर निधि, तोकूं (Drik तोकू).

## Meanings
Our own, one per verse (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`).

## Readings settled
- **aarti.pad1** (जग दाता or जगमाता): जग माता. The base's दाता is a valid word, but independent sources show it is a slip: Drik Panchang and India TV (indiatvnews.com, Ahoi Ashtami 2017) read माता, and the line is taken whole from the Lakṣmī āratī, which the Randhir book prints as ब्रह्माणी कमला तू ही है जग माता (i-190); the address to the goddesses (Brahmāṇī, Rudrāṇī, Kamalā) calls for "mother". Text corrected; meaning changed: "you alone are the mother of the world" (was "the giver to the world").
- **aarti.pad6** (रतन चतुर्दश तोकूं कोई नहीं पाता): as printed: तोकूं is "you" (object), so "of the fourteen jewels, none attains to you"; the Lakṣmī āratī's तुम बिन ("without you") is not in this text (the base, Drik Panchang and the Randhir book's ताको all lack it), and जगनिधि stays "the ocean of the world" (as भवनिधि). Meaning unchanged.

## The recording
Ambey Bhakti (YouTube `ecr8xZKBBOo`, `audio/ambey-bhakti/`) sings this text.
- Sung with a few words that no written witness has, so the text keeps its own there: `aarti.pad7`.
- The text follows the words it sings from another written witness (docs/PLAYBOOK.md §3): `aarti.pad3`, `aarti.pad4`, `aarti.pad5`, Drik Panchang’s (the table above).
- Every verse it sings is timed: MMS scored them too low, so the starts were read by hand on 5-s windows (`audio/ambey-bhakti/fixes.md`).
