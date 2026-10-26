# Re-organise the Pārāyaṇa-vidhi into meaningful blocks (text from the Gita Press books, unchanged
# except obvious typos). Block types:
#   ['h', heading]  ['p', paragraph]  ['note', small note]
#   ['card', {'t': title, 'v': [verse lines], 'm': [mantra lines], 'e': translation}]
#   ['list', [items]]   ['nyasa', [{'v': verse line, 'm': mantra, 'a': action, 'e': meaning}]]

def build(hb, eb, items=None):
    H = [x[1] for x in hb]
    E = [x[1] for x in eb]
    def hv(*idx): return [H[i] for i in idx]
    inv = [  # (hindi title, english title + direction, verse idx, mantra idx, english idx)
        ('श्रीतुलसीदासजी', 'Gosvāmī Tulasīdāsa · south-west', (3, 4), 5, (4, 5)),
        ('श्रीवाल्मीकिजी', 'Sage Vālmīki · north-east', (6, 7), 8, (6,)),
        ('श्रीशिवजी', 'Lord Śiva · south-east', (9, 10), 11, (7, 8)),
        ('श्रीलक्ष्मणजी (सपत्नीक)', 'Lakṣmaṇa with Ūrmilā · south', (12, 13), 14, (9, 10)),
        ('श्रीशत्रुघ्नजी (सपत्नीक)', 'Śatrughna with Śrutakīrti · west', (15, 16), 17, (11, 12)),
        ('श्रीभरतजी (सपत्नीक)', 'Bharata with Māṇḍavī · north', (18, 19), 20, (13, 14)),
        ('श्रीहनुमान्‌जी', 'Hanumān · east', (21, 22), 23, (15, 16)),
    ]
    ny_v = [H[i] for i in (44, 46, 48, 50, 52, 54)]
    kara_m = [H[i] for i in (45, 47, 49, 51, 53, 55)]
    anga_v = [H[i] for i in (57, 59, 61, 63, 65, 67)]
    anga_m = [H[i] for i in (58, 60, 62, 64, 66, 68)]
    kara_en_raw = [E[28], E[30], E[31], E[32], E[33], E[34]]
    import re
    kara_e, kara_a = [], []
    for s in kara_en_raw:
        m = re.match(r'^\((.*)\)\s*(.*)$', s.strip())
        a = m.group(2).strip()
        if len(a) < 3: a = E[29]
        a = re.sub(r'^Uttering (this|these words)\s*', '', a); a = a[:1].upper() + a[1:]
        kara_e.append(m.group(1).strip()); kara_a.append(a)
    anga_a_en = [
        'Touch the heart with all five fingers of the right hand.',
        'Touch the forehead.',
        'Touch the tuft of hair (śikhā) on the head.',
        'Touch the right shoulder with the fingers of the left hand, and the left shoulder with the right.',
        'Touch both eyes with the finger-tips of the right hand.',
        'Take the right hand round the head counter-clockwise, from the forehead to the back of the head and back to the forehead, then strike the left palm with the index and middle fingers of the right hand.',
    ]
    viniyoga = ' '.join(H[36:40])
    acamana = ['श्रीसीतारामाभ्यां नमः ।', 'श्रीरामचन्द्राय नमः ।', 'श्रीरामभद्राय नमः ।']
    dhyana = H[70:79]
    sixteen = [s.strip() for s in re.split(r'\s*\d+\.\s*', E[24]) if s.strip()]
    sixteen = [s.rstrip(';.').replace(' and', '') if i == len(sixteen) - 2 else s.rstrip(';.') for i, s in enumerate(sixteen)]
    dh_en = E[45]
    nb = ''
    if 'N.B.' in dh_en:
        dh_en, nb = dh_en.split('N.B.', 1)
        nb = nb.strip()
    dh_en = dh_en.strip().strip('()').replace('drinking in he ', 'drinking in the ').replace('a brateater of the humble', 'a caretaker of the humble')

    intro = E[1].rstrip('.') + ', ' + E[2]
    intro = intro.replace('worship the author, Gosvāmī', 'worship the author Gosvāmī')
    en = [['h', ['Procedure of reciting the Rāmacaritamānasa', 'पारायण-विधि']], ['p', intro],
          ['tip', 'Before you begin: bathe and sit on a clean seat (āsana), facing east or north. Place a picture or idol of Śrī Sītā-Rāma and the Rāmacaritamānasa on a raised, clean stand (pīṭha). Keep ready a small pot of water with a spoon, flowers, a little rice (akṣata), sandal paste, an incense stick, a lamp, and some fruit or sweets to offer.'],
          ['h', ['Invocation', 'आवाहन']],
          ['p', 'Invoke each in turn with the verse and mantra below, offering a seat in the direction shown.'],
          ['tip', 'How to do it: for each card, recite the verse and then the mantra, and place a flower or a few grains of rice at the side of the altar shown (south-west, north-east, and so on), imagining that saint or deity seated there. The directions are around the altar, as you face it.']]
    for t_hi, t_en, vi, mi, ei in inv:
        en.append(['card', {'t': t_en, 'th': t_hi, 'v': hv(*vi), 'm': [H[mi]], 'e': ' '.join(E[i] for i in ei).replace('“', '').replace('”', '')}])
    en += [['h', ['Worship of the principal deity', 'प्रधान पूजा']],
           ['p', E[17].replace(' in the light of the following verse:—', '.')],
           ['card', {'v': hv(24, 25), 'e': 'Now the principal worship should be performed according to the rules: taking flowers in the joined palms, one should meditate on the Supreme Lord.'}],
           ['card', {'t': 'Meditation', 'th': 'ध्यान', 'v': hv(26, 27, 28, 29), 'e': E[18].strip('“”')}],
           ['card', {'t': 'Invitation', 'th': 'आवाहन', 'v': hv(30, 31), 'm': [H[32]], 'e': E[19].strip('“”')}],
           ['card', {'t': 'Offering the seat', 'th': 'आसन', 'v': hv(33, 34), 'e': E[20].strip('“”')}],
           ['note', H[35]],
           ['p', 'Then worship the Lord with the sixteen offerings (ṣoḍaśopacāra · षोडशोपचार):'],
           ['list', sixteen],
           ['tip', 'If you cannot offer all sixteen, the short five-fold worship (pañcopacāra · पञ्चोपचार) is widely accepted: sandal paste, a flower, incense, the lamp and the food offering, made with devotion.'],
           ['h', ['Statement of purpose', 'विनियोग']],
           ['tip', 'What this is: a formal declaration of what you are about to recite: its seers (ṛṣi), deity (devatā), seed (bīja), power (śakti) and your purpose. Take a little water in your right palm, recite the text below, then let the water fall into a plate or on the ground.'],
           ['card', {'m': [viniyoga], 'e': E[21].split('scriptures.*', 1)[-1].strip().strip('“”').replace('“Mānasa-Rāmāyaṇa,”', '‘Mānasa-Rāmāyaṇa’,')}],
           ['h', ['Sipping water and breath control', 'आचमन और प्राणायाम']],
           ['p', 'Sip water three times, reciting these three mantras one after another. Then perform a Prāṇāyāma with the Bīja-Mantra sacred to Sītā and Rāma.'],
           ['tip', 'How to do it: pour a spoonful of water into the hollow of your right palm, say the first mantra and sip it; repeat for the second and third. Then wash or wipe your hand. For prāṇāyāma, breathe in slowly, hold briefly and breathe out slowly while mentally repeating the mantra. If no bīja-mantra has been given to you by a guru or elder, simply repeat “Sītārāma” in the mind.'],
           ['card', {'m': acamana}],
           ['note', 'इति मन्त्रत्रितयेन आचमनं कुर्यात् । श्रीयुगलबीजमन्त्रेण प्राणायामं कुर्यात् ।।'],
           ['h', ['Karanyāsa', 'करन्यास']],
           ['tip', 'What this is: nyāsa means “placing”. Before the reading you place sacred chaupāīs of the Mānasa on your fingers and hands, so that the hands that hold the book are sanctified. For each step: recite the chaupāī, then the Sanskrit phrase, and make the touch described. Fingers: thumb = aṅguṣṭha, index = tarjanī, middle = madhyamā, ring = anāmikā, little = kaniṣṭhikā.'],
           ['p', E[26].replace('that the touched', 'that are touched').replace('indentified', 'identified')],
           ['nyasa', [{'v': v, 'm': m, 'e': e, 'a': a} for v, m, e, a in zip(ny_v, kara_m, kara_e, kara_a)]],
           ['note', H[56]],
           ['h', ['Aṅganyāsa', 'हृदयादिन्यास']],
           ['p', E[36]],
           ['tip', 'What this is: the same six chaupāīs are now placed on the body: heart, forehead (head), the tuft on the crown (śikhā), the shoulders as armour (kavaca), the eyes, and finally a clap as a protective weapon (astra) all around you.'],
           ['nyasa', [{'v': v, 'm': m, 'e': e, 'a': a} for v, m, e, a in zip(anga_v, anga_m, kara_e, anga_a_en)]],
           ['note', H[69]],
           ['h', ['Meditation', 'ध्यान']],
           ['p', E[44].replace(' with the help of the following lines:—', '.')],
           ['tip', 'Sit quietly, close your eyes after reading each line if you like, and picture Śrī Rāma as described. After this, light the lamp and incense if not already lit, and begin the pāṭha from where your plan says (the start of the day’s vishram). At the end of the day’s reading, sing the Āratī (next tab).'],
           ['card', {'v': dhyana, 'e': dh_en}],
           ['note', H[79]]]
    if nb: en.append(['note', nb])

    # ---------- Hindi version: same structure, Hindi meanings and explanations ----------
    dirs = ['नैऋत्य (दक्षिण-पश्चिम)', 'ईशान (उत्तर-पूर्व)', 'आग्नेय (पूर्व-दक्षिण)', 'दक्षिण', 'पश्चिम', 'उत्तर', 'पूर्व']
    inv_hi = [
        'हे पवित्र व्रतवाले तुलसीदासजी! आपको नमस्कार है। आप यहाँ पधारिये और नैऋत्य कोणमें बैठकर यह पूजन स्वीकार कीजिये। श्रीतुलसीदासजीको नमस्कार।',
        'हे कल्याण देनेवाले वाल्मीकिजी! आपको नमस्कार है। आप यहाँ पधारिये और उत्तर-पूर्व (ईशान) के मध्यमें विराजकर मेरी पूजा ग्रहण कीजिये। श्रीवाल्मीकिजीको नमस्कार।',
        'हे गौरीपति महेश्वर! आपको नमस्कार है। आप यहाँ पधारिये और पूर्व-दक्षिण (आग्नेय) के मध्यमें विराजकर मेरी पूजा ग्रहण कीजिये। गौरीपतिको नमस्कार।',
        'हे श्रीलक्ष्मणजी! आपको नमस्कार है। आप अपनी प्रिया (उर्मिलाजी) सहित यहाँ पधारिये और दक्षिण भागमें विराजकर मेरा पूजन स्वीकार कीजिये। पत्नीसहित श्रीलक्ष्मणजीको नमस्कार।',
        'हे श्रीशत्रुघ्नजी! आपको नमस्कार है। आप अपनी प्रिया (श्रुतकीर्तिजी) सहित यहाँ पधारिये और पीठके पश्चिम भागमें विराजकर मेरा पूजन स्वीकार कीजिये। पत्नीसहित श्रीशत्रुघ्नजीको नमस्कार।',
        'हे श्रीभरतजी! आपको नमस्कार है। आप अपनी प्रिया (माण्डवीजी) सहित यहाँ पधारिये और पीठके उत्तर भागमें विराजकर मेरी पूजा ग्रहण कीजिये। पत्नीसहित श्रीभरतजीको नमस्कार।',
        'हे कृपानिधान हनुमान्‌जी! आपको नमस्कार है। आप यहाँ पधारिये और पूर्व भागमें विराजकर, हे प्रभो! मेरा पूजन स्वीकार कीजिये। श्रीहनुमान्‌जीको नमस्कार।']
    kara_e_hi = [
        'श्रीरामजीके गुणसमूह जगत्‌का कल्याण करनेवाले और मुक्ति, धन, धर्म और परमधामके देनेवाले हैं।',
        'जो जँभाई लेते समय भी “राम-राम” कहते हैं, पापोंके समूह उनके सामने नहीं आते।',
        'हे नाथ! आपका “राम” नाम सब नामोंसे बढ़कर हो और पापरूपी पक्षियोंके समूहके लिये बधिक (शिकारी) बने।',
        'हे उमा! स्वामी श्रीरामजी सबको कठपुतलीकी तरह नचाते हैं।',
        'जीव ज्यों ही मेरे सम्मुख होता है, त्यों ही उसके करोड़ों जन्मोंके पाप नष्ट हो जाते हैं।',
        'हे रघुकुलके स्वामी! सुन्दर हाथोंमें श्रेष्ठ धनुष और सुन्दर बाण धारण किये हुए आप मेरी रक्षा कीजिये।']
    kara_a_hi = [
        'दोनों हाथोंकी तर्जनीसे अँगूठोंका स्पर्श करें।',
        'अँगूठोंसे दोनों तर्जनियोंका स्पर्श करें।',
        'अँगूठोंसे दोनों मध्यमाओंका स्पर्श करें।',
        'अँगूठोंसे दोनों अनामिकाओंका स्पर्श करें।',
        'अँगूठोंसे दोनों कनिष्ठिकाओंका स्पर्श करें।',
        'एक-एक हाथसे दूसरे हाथकी हथेली और पीठका क्रमसे स्पर्श करें।']
    anga_a_hi = [
        'दाहिने हाथकी पाँचों उँगलियोंसे हृदयका स्पर्श करें।',
        'मस्तकका स्पर्श करें।',
        'सिरकी शिखाका स्पर्श करें।',
        'बायें हाथकी उँगलियोंसे दाहिने कंधेका और दाहिने हाथकी उँगलियोंसे बायें कंधेका स्पर्श करें।',
        'दाहिने हाथकी उँगलियोंके अग्रभागसे दोनों नेत्रोंका स्पर्श करें।',
        'दाहिने हाथको मस्तकसे सिरके पीछे और फिर मस्तकतक उलटी दिशा (वामावर्त) में घुमाएँ, फिर दाहिने हाथकी तर्जनी और मध्यमासे बायीं हथेलीपर ताली दें।']
    sixteen_hi = ['पाद्य (चरण धोनेके लिये जल)', 'अर्घ्य (हाथ धोनेके लिये जल)', 'आचमनीय (आचमनके लिये जल)', 'स्नानीय (स्नानके लिये जल)', 'वस्त्र', 'आभूषण', 'गन्ध (चन्दन)', 'पुष्प (फूल)', 'धूप', 'दीप', 'नैवेद्य (भोग)', 'आचमनीय (भोगके बाद आचमनके लिये जल)', 'ताम्बूल (पान)', 'स्तवपाठ (स्तुति)', 'तर्पण (तृप्तिके लिये जल)', 'नमस्कार']
    dh_hi = ''
    if items:
        I = {x['id']: x for x in items}
        dh_hi = ' '.join(re.sub(r'\s*।।[^।]*।।\s*$', '', I['uttar.51.cau%d' % k]['h']).strip() for k in range(1, 6) if 'uttar.51.cau%d' % k in I)
    hi = [['h', 'पारायण-विधि'], ['p', H[1]],
          ['tip', 'आरम्भसे पहले: स्नान करके स्वच्छ आसनपर पूर्व या उत्तरकी ओर मुख करके बैठें। श्रीसीतारामजीका चित्र या विग्रह और श्रीरामचरितमानसकी पोथी ऊँचे, स्वच्छ पीठ (चौकी) पर रखें। जलसे भरा छोटा पात्र और चम्मच, फूल, थोड़े अक्षत (चावल), चन्दन, धूपबत्ती, दीपक और भोगके लिये कुछ फल या मिठाई पास रख लें।'],
          ['h', 'आवाहन'],
          ['p', 'नीचे दिये श्लोक और मन्त्रसे क्रमशः प्रत्येकका आवाहन करें और बताई गयी दिशामें उन्हें आसन दें।'],
          ['tip', 'कैसे करें: प्रत्येक श्लोक और फिर मन्त्र बोलें, और पीठकी बताई गयी दिशामें एक फूल या थोड़े अक्षत रखें—यह भाव करते हुए कि वे संत या देवता वहाँ विराजमान हैं। दिशाएँ पीठ (चौकी) के चारों ओर, उसके सामने बैठकर देखते हुए हैं।']]
    for (t_hi, t_en, vi, mi, ei), dr, mean in zip(inv, dirs, inv_hi):
        hi.append(['card', {'t': t_hi + ' · ' + dr, 'v': hv(*vi), 'm': [H[mi]], 'e': mean}])
    hi += [['h', 'प्रधान पूजा'],
           ['p', 'इसके बाद प्रधान देवता (श्रीसीताजीसहित श्रीरामजी) की विधिपूर्वक पूजा करें। दोनों हाथोंकी अंजलिमें फूल लेकर नीचेके श्लोकसे परमात्मा श्रीरामजीका ध्यान करें।'],
           ['card', {'v': hv(24, 25), 'e': 'अब विधिपूर्वक प्रधान पूजा करनी चाहिये। अंजलिमें फूल लेकर परमात्माका ध्यान करे।'}],
           ['card', {'t': 'ध्यान', 'v': hv(26, 27, 28, 29), 'e': 'जिनके मनोहर नेत्र लाल कमलकी पँखुड़ियोंके समान हैं, जो पीताम्बरसे सुशोभित हैं, जिनका शरीर श्याम है, दो भुजाएँ हैं, मुख प्रसन्न है और जो श्रीसीताजीसे शोभित हैं; जो करुणारूपी अमृतके समुद्र हैं, भाइयों आदि प्रिय परिकरसे घिरे हैं, विष्णु, शिव आदिसे सदा सेवित हैं और भक्तोंके मनोरथ पूर्ण करनेवाले हैं—उन श्रीरामजीकी मैं वन्दना करता हूँ।'}],
           ['card', {'t': 'आवाहन', 'v': hv(30, 31), 'm': [H[32]], 'e': 'हे जानकीनाथ राघव! आप श्रीजानकीजीके साथ और पवनपुत्र हनुमान्‌जी आदिसहित यहाँ पधारिये और मेरी पूजा ग्रहण कीजिये।'}],
           ['card', {'t': 'आसन', 'v': hv(33, 34), 'e': 'हे राम! सोनेका बना, मणियोंसे जड़ा और सुन्दर दिव्य बिछौनेसे सुशोभित यह आसन मैंने आपको अर्पित किया है, इसे ग्रहण कीजिये।'}],
           ['note', H[35]],
           ['p', 'इसके बाद षोडशोपचार (सोलह उपचारों) से भगवान्‌की पूजा करें:'],
           ['list', sixteen_hi],
           ['tip', 'यदि सोलहों उपचार सम्भव न हों तो पञ्चोपचार पूजा भी मान्य है—चन्दन, पुष्प, धूप, दीप और नैवेद्य, श्रद्धाके साथ अर्पित करें।'],
           ['h', 'विनियोग'],
           ['tip', 'यह क्या है: जिस ग्रन्थका पाठ करने जा रहे हैं, उसका संकल्प-वाक्य—उसके ऋषि, देवता, बीज, शक्ति और पाठका उद्देश्य। दाहिनी हथेलीमें थोड़ा जल लेकर नीचेका पाठ बोलें, फिर जल थाली या भूमिपर छोड़ दें।'],
           ['card', {'m': [viniyoga], 'e': 'इस मानसरामायण श्रीरामचरितके श्रीशिवजी, काकभुशुण्डिजी, याज्ञवल्क्यजी और गोस्वामी तुलसीदासजी ऋषि हैं; श्रीसीतारामजी देवता हैं; श्रीरामनाम बीज है; भवरोगको हरनेवाली भक्ति शक्ति है; और समस्त विघ्नोंको दूर करके श्रीसीतारामजीकी प्रसन्नताके द्वारा सब मनोरथोंकी सिद्धिके लिये इस पाठमें इसका विनियोग है।'}],
           ['h', 'आचमन और प्राणायाम'],
           ['p', 'नीचेके तीन मन्त्र एक-एक करके बोलते हुए तीन बार आचमन करें। फिर श्रीसीतारामजीके युगल बीजमन्त्रसे प्राणायाम करें।'],
           ['tip', 'कैसे करें: दाहिनी हथेलीमें एक चम्मच जल लें, पहला मन्त्र बोलकर उसे पी लें; दूसरे और तीसरे मन्त्रके साथ यही दोहराएँ। फिर हाथ धो या पोंछ लें। प्राणायाममें धीरे-धीरे श्वास लें, थोड़ा रोकें और धीरे-धीरे छोड़ें, साथ-साथ मनमें मन्त्र जपते रहें। यदि गुरु या बड़ोंसे कोई बीजमन्त्र न मिला हो तो मनमें “सीताराम” का जप करें।'],
           ['card', {'m': acamana}],
           ['note', 'इति मन्त्रत्रितयेन आचमनं कुर्यात् । श्रीयुगलबीजमन्त्रेण प्राणायामं कुर्यात् ।।'],
           ['h', 'करन्यास'],
           ['tip', 'यह क्या है: न्यासका अर्थ है “स्थापित करना”। पाठसे पहले मानसकी पवित्र चौपाइयोंको अपनी उँगलियों और हाथोंमें स्थापित किया जाता है, जिससे पोथी पकड़नेवाले हाथ पवित्र हो जाते हैं। प्रत्येक चरणमें चौपाई बोलें, फिर संस्कृत वाक्य बोलें और बताया गया स्पर्श करें। उँगलियाँ: अँगूठा (अङ्गुष्ठ), पहली (तर्जनी), बीचकी (मध्यमा), तीसरी (अनामिका), सबसे छोटी (कनिष्ठिका)।'],
           ['p', 'करन्यासमें विशेष मन्त्रोंको उँगलियों, हथेलियों और हाथोंके पृष्ठभागपर स्थापित किया जाता है। करन्यास और अङ्गन्यास दोनोंमें मन्त्रोंको सजीव रूपवाला माना जाता है, और अंगोंके नाम लेकर उन्हींका स्पर्श और अभिवादन किया जाता है। इससे पाठ करनेवाला मन्त्रसे एकरूप होकर मन्त्र-देवताकी पूर्ण रक्षामें आ जाता है, भीतर-बाहरसे पवित्र होता है और दिव्य शक्तिसे भर जाता है। उसकी साधना अन्ततक निर्विघ्न चलती है और कल्याणकारी होती है।'],
           ['nyasa', [{'v': v, 'm': m, 'e': e, 'a': a} for v, m, e, a in zip(ny_v, kara_m, kara_e_hi, kara_a_hi)]],
           ['note', H[56]],
           ['h', 'हृदयादिन्यास (अङ्गन्यास)'],
           ['p', 'अङ्गन्यासमें दाहिने हाथकी सब उँगलियाँ मिलाकर हृदय आदि अंगोंका स्पर्श किया जाता है।'],
           ['tip', 'यह क्या है: वही छः चौपाइयाँ अब शरीरपर स्थापित की जाती हैं—हृदय, मस्तक, शिखा, कवचरूपमें दोनों कंधे, नेत्र, और अन्तमें चारों ओर रक्षाके लिये अस्त्ररूपी ताली।'],
           ['nyasa', [{'v': v, 'm': m, 'e': e, 'a': a} for v, m, e, a in zip(anga_v, anga_m, kara_e_hi, anga_a_hi)]],
           ['note', H[69]],
           ['h', 'ध्यान'],
           ['p', 'इसके बाद नीचेकी चौपाइयोंसे भगवान्‌के स्वरूपका ध्यान करें।'],
           ['tip', 'शान्त होकर बैठें, चाहें तो प्रत्येक पंक्तिके बाद आँखें बंद करके श्रीरामजीके वर्णित स्वरूपका ध्यान करें। इसके बाद दीपक और धूप जलाएँ (यदि पहले न जलाये हों) और अपनी योजनाके अनुसार उस दिनके विश्रामके आरम्भसे पाठ शुरू करें। दिनके पाठके अन्तमें आरती (अगला टैब) गाएँ।'],
           ['card', {'v': dhyana, 'e': dh_hi}],
           ['note', H[79]],
           ['note', 'नवाह्न और मासपारायणके विश्राम मूल पाठमें ही दिये गये हैं, इसलिये अलगसे नहीं लिखे गये।']]
    return hi, en
