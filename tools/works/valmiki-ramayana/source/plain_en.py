"""The English of the sarga headings (Gita Press's, IAST) in plain, common Indian English (docs/PLAYBOOK.md §6): Śrī Rāma →
Shri Ram, Lakṣmaṇa → Lakshman, Brāhmaṇas → Brahmins. A name the Mānas already spells (tools/works/manas/source/plain_en.json)
is spelt the same; OVR and UNM hold the rest by hand; any other marked word is transliterated plainly, a name's final short a
dropped (Ravan) except after two consonants (Vashishtha). Used by make_text.py.
"""
import json, os, re, collections, sys
MARK=re.compile('[À-ÖØ-öø-ɏḀ-ỿ]')
P=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'manas', 'source', 'plain_en.json'), encoding='utf-8'))
known={}
for a,b in P.items():
    wa=re.findall(r"[\wÀ-ÖØ-öø-ɏḀ-ỿ'-]+",a); wb=re.findall(r"[\wÀ-ÖØ-öø-ɏḀ-ỿ'-]+",b)
    if len(wa)==len(wb):
        for x,y in zip(wa,wb):
            if x!=y and MARK.search(x): known.setdefault(x,collections.Counter())[y]+=1
known={k:v.most_common(1)[0][0] for k,v in known.items()}
OVR={'Vālī':'Vali','Vālī’s':'Vali’s','Viśwāmitra':'Vishwamitra','Bharadwāja':'Bharadwaj','Kausalyā':'Kaushalya','Rākṣasas':'Rakshasas','Rākṣasa':'Rakshasa',
 'Brāhmaṇas':'Brahmins','Brāhmaṇa':'Brahmin','Ṛṣis':'Rishis','Ṛṣi':'Rishi','Maharṣi':'Maharshi','Brahmarṣi':'Brahmarshi','Āśrama':'Ashram','Aśvamedha':'Ashwamedh',
 'Vānara':'Vanar','Kṣatriyas':'Kshatriyas','Kṣatriya':'Kshatriya','Śūdra':'Shudra','Yakṣas':'Yakshas','Nāgas':'Nagas','Apsarās':'Apsaras','Cāraṇas':'Charanas',
 'Nāstikas':'Nastikas','Śāstras':'Shastras','Kiṅkaras':'Kinkaras','Niṣādas':'Nishads','Kiṁpuruṣīs':'Kimpurushis','Nivātakavacas':'Nivatakavachas','Kālakeyas':'Kalakeyas',
 'Rāmāyaṇa':'Ramayan','Himālayas':'Himalayas','Himālaya':'Himalaya','Kiṣkindhā':'Kishkindha','Citrakūṭa':'Chitrakoot','Śṛṅgaverapura':'Shringverpur','Ṛṣyamūka':'Rishyamook',
 'Ṛṣyaśṛṅga':'Rishyashring','Ikṣwāku':'Ikshvaku','Ikṣvāku':'Ikshvaku','Śiṁśapā':'Shinshapa','Aśoka-grove':'Ashok grove','Vālmīki-Āśrama':'Valmiki Ashram','ŚrīRāma':'Shri Ram',
 'Āditya-Hṛdaya’':'Aditya Hriday’','Surgīva':'Sugriv','Laṅka':'Lanka','Kumbhakarṇa':'Kumbhkaran','Kumbhakarṇa’s':'Kumbhkaran’s','Meghanāda':'Meghnad','Jāmbavān':'Jambavan',
 'Sampāti':'Sampati','Aṅgada':'Angad','Nīla':'Neel','Suṣeṇa':'Sushen','Śuka':'Shuk','Sāraṇa':'Saran','Mārīca':'Marich','Virādha':'Viradh','Virādha’s':'Viradh’s',
 'Śarabhaṅga':'Sharbhang','Puṣpaka':'Pushpak','Tāṭakā':'Tataka','Pañcavaṭī':'Panchavati','Lavaṇāsura':'Lavanasur','Śukrācārya':'Shukracharya','Samāvartana':'Samavartan',
 'Nāndīśrāddha':'Nandishraddh','Śrāddha':'Shraddh','Tarpaṇa':'Tarpan','sāla':'sal','Uccaiḥśravā':'Uchchaihshrava','Śunaḥśepa':'Shunahshep','Cāṇḍāla':'Chandal',
 'Rājasūya':'Rajasuya','Brahmahatyā':'Brahmahatya','Takṣaśilā':'Takshashila','Daṇḍakavana':'Dandakvan','Mataṅgavana':'Matangvan','Śaci':'Shachi','Śiva':'Shiv',
 'Viṣṇu':'Vishnu','Viṣṇu’s':'Vishnu’s','Gaṅgā':'Ganga','Gaṅgā’s':'Ganga’s','Garuḍa':'Garud','Kailāsa':'Kailash','Nandīśwara':'Nandishwar','Śaṅkara':'Shankar',
 'Daśaratha':'Dashrath','Daśaratha’s':'Dashrath’s','Vasiṣṭha':'Vashishtha','Vasiṣṭha’s':'Vashishtha’s','Śatrughna':'Shatrughna','Vibhīṣaṇa':'Vibhishan',
 'Mahāpārśwa':'Mahaparshva','Supārśwa':'Suparshva','Hariścandra':'Harishchandra','Triśaṅku':'Trishanku','Paraśurāma':'Parshuram','Aṁśumān':'Anshuman','Mālyavān':'Malyavan','Mālyavān’s':'Malyavan’s','Asamañja':'Asamanj'}
UNM={'Bharata':'Bharat','Janaka':'Janak','Lava':'Lav','Khara':'Khar','Prahasta':'Prahast','Dadhimukha':'Dadhimukh','Sagara':'Sagar','Kabandha':'Kabandh','Kubera':'Kuber',
 'Suvela':'Suvel','Arjuna':'Arjun','Kosala':'Kosal','Madhuvana':'Madhuvan','Akampana':'Akampan','Mahodara':'Mahodar','Nala':'Nal','Dwivida':'Dwivid','Jayanta':'Jayant',
 'Gautama':'Gautam','Kekaya':'Kekay','Malaya':'Malay','Nikumbha':'Nikumbh','Cyavana':'Chyavan','Brahmaloka':'Brahmalok','Bindusarovara':'Bindu Sarovar','Mandara':'Mandar',
 'Kaustubha':'Kaustubh','Brahmadatta':'Brahmadatt','Kapila':'Kapil','Budha':'Budh','Pratardana':'Pratardan','Kumbha':'Kumbh','Rama':'Ram','Sri':'Shri'}
def tr(w):
    s=w.replace('ś','sh').replace('Ś','Sh').replace('ṣ','sh').replace('Ṣ','Sh').replace('c','ch').replace('C','Ch').replace('ṛ','ri').replace('Ṛ','Ri')
    for a,b in [('ā','a'),('Ā','A'),('ī','i'),('Ī','I'),('ū','u'),('Ū','U'),('ṭ','t'),('ḍ','d'),('Ḍ','D'),('ṇ','n'),('ṅ','n'),('ñ','n'),('ṁ','n'),('ṃ','n'),('ḥ','h'),('ṭ','t'),('Ṭ','T')]: s=s.replace(a,b)
    return s
def word(w):
    base,pos=(w[:-2],'’s') if w.endswith('’s') else (w,'')
    for k in (w,):
        if k in OVR: return OVR[k]
        if k in known: return known[k]
    if base in OVR: return OVR[base]+pos
    if base in known: return known[base]+pos
    t=tr(base)
    # a name's final short a goes (Ravan, Lakshman), not after two consonants (Vashishtha) nor a long ā (Sita)
    if base.endswith('a') and not base.endswith('ā') and len(t)>4 and not re.search(r'[bcdfghjklmnpqrstvwxyz]{2}a$', t.lower().replace('sh','ś').replace('ch','c').replace('th','t').replace('dh','d').replace('bh','b').replace('gh','g').replace('kh','k').replace('ph','p').replace('jh','j')) and base[:1].isupper():
        t=t[:-1]
    return t+pos
def unm(w):
    base,pos=(w[:-2],'’s') if w.endswith('’s') else (w,'')
    return UNM[base]+pos if base in UNM else w
def plain(s):
    return re.sub(r"[\wÀ-ÖØ-öø-ɏḀ-ỿ’'-]+", lambda m: word(m.group(0)) if MARK.search(m.group(0)) else unm(m.group(0)), s)
