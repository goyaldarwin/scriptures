# Hand-checked starts (fixes.json)

Every start here was found by reading the recording's transcript (`transcripts/<video id>.jsonl`, Whisper in 6-second windows, with word times): the time of the first word heard of the verse's first line, or, where the opening is garbled, of its first clearly recognisable word (said in the note). The verses between two heard or fixed starts are placed by length (`make_timings.py`, gaps of up to 8 verses).

## Last verses of a sarga the alignment did not find

The speech recogniser garbles many sargas' closing verses (often in a longer metre). Each was looked for between the last verse heard and the closing words (इत्यार्षे श्रीमद्रामायणे … सर्गः).

| Recording | Verse | Start (s) | Heard in the transcript | The verse |
|---|---|---|---|---|
| `Xy5YUe0I7pw` | bala.1.100 | 955.7 | पर्दन्दिजोबाग्र्शबत्व | पठन् द्विजो वागृषभत्व… |
| `MnXhn-F5l-4` | bala.2.43 | 404.8 | तदुबबखत स बच्चा बचा चण्ते यो गंवा | तदुपगतसमाससन्धियोगं |
| `FkUqTiTcTPM` | bala.7.24 | 233.6 | ता एग … ब्रुदोन रखते एकुशा ले समर (237.6: कुशलैः समर्थैः, the end of the line) | तैर्मन्त्रिभिर्मन्त्रहिते निविष्टैर्वृतोऽनुरक्तैः कुशलैः समर्थैः |
| `BAzQltCL_U0` | bala.17.37 | 348.0 | ताईर में खवरंदा चलकोटजन | तैर्मेघवृन्दाचलकूट… |
| `9pxlTPhOLgQ` | bala.18.59 | 563.0 | इते हो देख … सोखम निशम याव आख्यम्श्रते सुखमात | इति हृदयसुखं निशम्य वाक्यं श्रुतिसुखमात्मवता |
| `aXFH1tSzOQo` | bala.37.32 | 298.6 | वग्त्टश्च्च्याज्कार्ज् | भक्तश्च यः कार्तिकेये |
| `2fp2DjPIN1o` | bala.55.28 | 250.6 | ब्राँब्रुद्द्धवादन्द | (इत्युक्त्वा) परमक्रुद्धो दण्डम्… |
| `JxSd-3juPSQ` | ayodhya.4.45 | 424.6 | वालक्श्वनम्रामोग | (इत्युक्त्वा) लक्ष्मणं रामो |
| `Dy-Oce0tYgU` | ayodhya.49.18 | 168.0 | तम्त्ताः … प्रज़ाँ (after 162.0 अम्रुगयावने काले करतां: the end of verse 17) | स तमध्वानमैक्ष्वाकः |
| `6wkcaYKxgMs` | ayodhya.84.18 | 169.6 | आशम से | आशंसे स्वाशिता सेना |
| `4G9qq88vlVY` | ayodhya.97.31 | 289.8 | साचित्र कुते बर तेना से ना | सा चित्रकूटे भरतेन सेना |
| `dX6wWjWe4nA` | ayodhya.108.18 | 178.0 | अदिया बाज़ा … 180.0 अद्यान दरषिनीम राज्यम (…निदर्शिनीम्, the end of the line) | सतां बुद्धिं पुरस्कृत्य सर्वलोकनिदर्शिनीम् |
| `xU5ci1BwPWQ` | aranya.40.27 | 261.5 | आसाद जदम ज भी विदावाँ | आसाद्य तं जीवितसंशयस्ते |
| `KyQ1m_OB9xo` | aranya.43.51 | 487.9 | बदख्ष्याने लख्ष्मना | प्रदक्षिणेनातिबलेन पक्षिणा |
| `Wp7B5Q3tRYU` | aranya.45.40 | 382.6 | तदस्तम्ब्रातरम्… अब आख्श्मना | ततस्तु सीतामभिवाद्य लक्ष्मणः |
| `ogsEhZmydxQ` | aranya.61.31 | 304.1 | तवाख्यम लक्ष्माण वो प्रज बड़च्योटम | (अनादृत्य तु) तद् वाक्यं लक्ष्मणोष्ठपुटच्युतम् |
| `PU2d8daaqTU` | aranya.68.38 | 373.0 | गुतोडा काउताबा पेबक् | कृतोदकौ तावपि पक्षि… |
| `FswHpViSn3U` | yuddha.30.35 | 334.1 | आद बवाश्वाद … 336.0 ख्यातम | इति सर्वं समाख्यातं |
| `kSfPT9gh3T4` | yuddha.39.28 | 284.8 | ताम्रत्दपुन्नाम्बहुसंवि | तां रत्नपूर्णां बहुसंविधानां |

## Starts matched in the wrong place

With `"align": "anchors"` a verse can be matched to a later line that sounds like it (a verse that opens like another, a repeated name), so that it starts far sooner or later than the reciter's pace allows. Every verse that a start made shorter than 0.3 or longer than 3.5 times the recording's usual time per letter was read in the transcript with its neighbours, and these starts set.

| Recording | Verse | Start (s) | Heard in the transcript | Why |
|---|---|---|---|---|
| `AO4XcJBrhLQ` | bala.3.11 | 111.1 | नाना | नाना चित्राः follows सत्कशीलताम (end of 3.10); current 112.99 is late |
| `AO4XcJBrhLQ` | bala.3.12 | 121.7 | राम राम विबाद | रामरामविवादं right after विबेदनम (end of 3.11) |
| `AO4XcJBrhLQ` | bala.3.13 | 132.0 | बिखातम चाभिषे | विघातं चाभिषेकस्य; 125.6 was inside 3.12 (गुणान् दाशरथेस्तथा) |
| `imIMNbt7MY8` | bala.11.7 | 65.3 | प्रत्ट्ट्ट | प्रतिगृह्यं right after end of 11.6 (ब्रतारमात्मवान); 72.0 बवर्श्टे नान्तरात मना = प्रहृष्टेनान्तरात्मना closes it |
| `imIMNbt7MY8` | bala.11.8 | 74.5 | तम्च | तं च, followed by जाएशरता यशस्खामाख = राजा दशरथो यशस्कामः; 80.88 was mid-verse (ऋष्यशृङ्गं) |
| `_8FEID9wr4g` | bala.12.8 | 72.3 | ज़र्मार तासवे तम् | धर्मार्थसहितं, right after 12.7 line 2 (तान् पूजयित्वा धर्मात्मा राजा दशरथस्तदा, 69.2-72.0); 66.2 is inside 12.7 |
| `_8FEID9wr4g` | bala.12.9 | 81.9 | प वो त्रा थामभायमे | पुत्रार्थं हयमेधेन, right after 'वैसुखम' (end of 12.8); 78.9-81.9 is still 12.8 line 2 (तप्यमानस्य पुत्रार्थं नास्ति वै सुखम्) |
| `_syYI150p54` | bala.13.22 | 204.8 | तमानयमहा | तमानय महाभागं right after बादिनम (सत्यवादिनम्) at 204.0 |
| `_syYI150p54` | bala.13.23 | 214.3 | तदा खाशे | तथा काशिपतिं after बवाँब्रवी मिते (ब्रवीमि ते) |
| `WqffCVRAus4` | bala.22.11 | 96.4 | श्दानम देवा मेवाच्ण्ट | स्थाणुं देवमिवाचिन्त्यं; preceding तो is end of शोभयेतामनिन्दितौ |
| `WqffCVRAus4` | bala.22.12 | 105.5 | रामे ते | रामेति right after दक्षिणे तटे (end of 22.11) |
| `WqffCVRAus4` | bala.22.13 | 115.7 | बद्रग्रावंग्र रहानत्कम | मन्त्रग्रामं गृहाण त्वं; 109.26 was inside 22.12 (गृहाण वत्स सलिलं at 110.9) |
| `WqffCVRAus4` | bala.22.14 | 124.9 | नाजा सोब | न च सुप्तं, followed by प्रमत्तं वा धर्षयिष्यन्ति at 126.0; 122.69 was inside 22.13 line 2 (न रूपस्य विपर्ययः) |
| `49ccj9kjoSg` | bala.26.6 | 52.0 | एडा मुभ्ट्व | एवमुक्त्वा after end of 26.5 (मुद्यता), then अर्म = धनुर्मध्ये; 58.18 was mid-verse (बद्ध्वा मुष्टिमरिन्दमः) |
| `49ccj9kjoSg` | bala.26.7 | 61.4 | तेनशवदेन | तेन शब्देन after नादयन (end of 26.6) |
| `49ccj9kjoSg` | bala.26.8 | 70.5 | तामशब | तं शब्दम after मोहिता (end of 26.7) |
| `49ccj9kjoSg` | bala.26.9 | 80.8 | तान्द्रश्ट्वाराग़ा | तां दृष्ट्वा राघवः |
| `tROa8K4jn4o` | bala.31.2 | 15.9 | ब्रबादायान्दु सर्वर्याः | प्रभातायां तु शर्वर्यां; 23.25 is late (end of verse area) |
| `tROa8K4jn4o` | bala.31.6 | 52.8 | मैं तेलास्च | मैथिलस्य, right after 'वचना मप्रुवनना' (end of 31.5) |
| `NAHl3Kjt4rc` | bala.46.3 | 22.5 | साहम्द प | साहं तपश् after जितम (दीर्घतपोऽर्जितम्) |
| `P-DzbJflKtI` | bala.49.21 | 193.9 | गव्टम अपे महातेज | गौतमोऽपि महातेजा; वशानुगा (end of 49.20) at 192.6 |
| `P-DzbJflKtI` | bala.49.22 | 202.7 | रामो पे पाज | रामोऽपि परमां; 197.6 was matched to राम सम्पुज्य (रामं सम्पूज्य, line 2 of 49.21) at 198.0 |
| `jG6UQnG-O6Y` | bala.52.1 | 6.0 | वंद्रष्ट्वा परमब्रीदो | तं दृष्ट्वा परमप्रीतो; verse runs to वसिष्ठं जपतां वरम् ~14.6 |
| `jG6UQnG-O6Y` | bala.52.3 | 24.0 | अपा मिष्टाये चददा विष्व | उपविष्टाय च तदा विश्वा(मित्राय) |
| `jG6UQnG-O6Y` | bala.52.5 | 42.0 | विश्वा मित्रो महातेजा | विश्वामित्रो महातेजा; 7.6 was the विश्वामित्रो of 52.1 |
| `OCFJlevK9AA` | bala.58.7 | 59.1 | सराज़ा | स राजा, directly after 'लाखशरम' (क्रोधपर्याकुलाक्षरम्, end of 58.6); the 65.3 'बद्याजा पुन रेवाईता निद' is a squashed window tail |
| `OCFJlevK9AA` | bala.58.8 | 67.6 | अन्यांग तिंगम विश्यामे | अन्यां गतिं गमिष्यामि |
| `RPxwW8mWLbk` | bala.61.18 | 155.2 | ममाँ़ प्रज� | ममापि right after 'बाहा बार गवाहा' (भगवानाह भार्गवः, end of 61.17); then 'बद्यदए तम विद्धे कनिष्ट' = दयितं विद्धि कनिष्ठं, 'बार्ठिवाद' = पार्थिव |
| `RPxwW8mWLbk` | bala.61.19 | 163.5 | प्राय | प्रायेण right after 'वाद्यादा बार्ठिवाद' (तव पार्थिव, end of 61.18); 168.0 'बाद्रनाचकनी यान सस्तस्माद्र' = line 2 |
| `3aLXVv_bmE0` | bala.74.15 | 130.0 | बस्मना चावर | भस्मना चावृतं, after नावेदिषुर्दिशः (end of 74.14); 124.39 was inside 74.14 (तमसा at 126.0). 74.14 at 121.65 left as is (first line not heard, plausible) |
| `o_tklWKS4Cg` | ayodhya.3.21 | 201.3 | चाक्रदोश् | चक्रतुश्चैव, right after 'तरबिनेश्विताउ' (तत्र विनिष्ठितौ, end of 3.20); 208.6 is 'पार्थिवाय निवेद्य' inside 3.21 |
| `o_tklWKS4Cg` | ayodhya.3.23 | 219.8 | रामब | रामः, after 'वचणम ब्रविते' (end of 3.22), followed by 'बवाग्रतात मा भवाज़्ुव' (कृतात्मा भवता) |
| `o_tklWKS4Cg` | ayodhya.3.25 | 236.7 | ब्राज्यो दिच्या | प्राच्योदीच्या, after 3.24 line 2 'अखा तद्रसा हासीना स्तदादशर' (234.0) |
| `Xjd0TzYfchc` | ayodhya.22.21 | 190.2 | खष्चा दे | कश्च दैवेन after 'पर्ये' (विपर्ययः, end of 22.20); then 'बेना सावो में त्रेवाग' = वेन सौमित्रे, 192.0 योद्धुमुत्सहते |
| `Xjd0TzYfchc` | ayodhya.22.22 | 198.8 | सुखा दोखे बायक्र | सुखदुःखे भयक्रोधौ after 'विर्श्यते' (दृश्यते, end of 22.21); 201.1 'लबा लपो' = लाभालाभौ |
| `Xjd0TzYfchc` | ayodhya.22.25 | 226.3 | एदधया | एतया right after 'अदेवस्जकर्म्बत्द' (ननु दैवस्य कर्म तत्, end of 22.24); then 'तवाया' = तत्त्वया |
| `KUsNfNtDYGI` | ayodhya.23.12 | 114.0 | तदम तवं कर मडा सक्ताछ कै के ये | कथं त्वं कर्मणा शक्तः कैकेयी |
| `KUsNfNtDYGI` | ayodhya.23.13 | 122.3 | भीदा यंकल भीशाद भीदा | यदयं किल्बिषाद् भेदः, right after दर्मश्छन्दिगर्हित (अधर्मिष्ठं विगर्हितम्) |
| `IQuo2y55cMc` | ayodhya.25.33 | 308.0 | यन्मंगल | यन्मङ्गलं right after तत् ते भवतु मङ्गलम् ending 25.32 |
| `IQuo2y55cMc` | ayodhya.25.34 | 316.2 | आम्रुतोद | अमृतोत्पादने; 309.38 was matched to अमृतं प्रार्थयानस्य (line 2 of 25.33, at 312.0) |
| `IQuo2y55cMc` | ayodhya.25.35 | 325.3 | त्रीन विक्रमान | त्रिविक्रमान् after भवत मंगलम (end of 25.34) at 324.0-324.3 |
| `SR2mfWGmrMM` | ayodhya.33.11 | 99.8 | बद्रश्या का खंश्याद | first recognisable word is पुत्रस्य (कथं स्याद्), 2nd word of line; true start (निर्गुणस्यापि) about 1.5 s earlier, not heard |
| `SR2mfWGmrMM` | ayodhya.33.14 | 126.0 | भी बाद़ा प्रद तम सर्वम जग | पीडया पीडितं सर्वं जग(दस्य); then मुलस्ये वो = मूलस्येवोपघातेन |
| `CjeY7Q9y-8k` | ayodhya.36.6 | 55.3 | निग्रन | निघ्नन् right after 'बाज़ा विदाजा' (व्याधाश्चारण्यकोविदाः, end of 36.5); 60.0 'नदेश च़विदाव पश्यन' = line 2 |
| `TFvY6kAvSzs` | ayodhya.74.28 | 271.1 | यास्या वकोद्र साहस् | यस्याः पुत्रसहस्राणि; line 2 किं पुनर्या at 276.0 |
| `Sss3Imu2FCg` | ayodhya.85.13 | 121.5 | शाष्वती खलु ते | शाश्वती खलु ते after मिहेच्छसि (end of 85.12) |
| `BY6pBP8TwN0` | ayodhya.103.40 | 399.6 | चाबो मेर बजगर्या | सा भूमिर्बहुभिर्यानै right after 'अदे में समा को' (खुरनेमिसमाकुलैः, end of 103.39); 103.41 at 408.0 'तेन वित्रास' so its current 407.6 is fine |
| `pQqMOB1o5EU` | ayodhya.105.4 | 37.0 | सान्फिर्ता मामिका मात | सान्त्विता मामिका माता; whole verse heard 37.0-46.1 |
| `pQqMOB1o5EU` | ayodhya.105.5 | 46.8 | महते | महतेवाम्बुवेगेन after तकम (अकण्टकम्) |
| `pQqMOB1o5EU` | ayodhya.105.7 | 66.6 | सुजीव, | सुजीवं नित्यशस्तस्य |
| `pQqMOB1o5EU` | ayodhya.105.8 | 74.8 | लेठा तो रोपि तो | यथा तु रोपितो after दूजीवम यप पारानु पजी (end of 7) |
| `pQqMOB1o5EU` | ayodhya.105.10 | 95.0 | एशो पमाँ | एषोपमा after परो पिता (प्ररोपितः) |
| `pQqMOB1o5EU` | ayodhya.105.11 | 104.7 | शेन्यस्वा म | श्रेणयस्त्वां महाराज after ब्रत्यान्शादिः (भृत्यान् न शाधि हि) |
| `iVnnipo0a94` | aranya.11.57 | 558.0 | ब्रातरम सम्स्कतंगर्ट्वादतस | भ्रातरं संस्कृतं कृत्वा ततस्, followed by 'तम्येशरूपिनम' (तं मेषरूपिणम्) |
| `iVnnipo0a94` | aranya.11.61 | 598.3 | आगस्तिये न | अगस्त्येन right after 'पिषिताशा नाईए' (पिशिताशनैः, end of 11.60); 604.6 'देवाईव प्रार्थि' = देवैः प्रार्थितेन |
| `iVnnipo0a94` | aranya.11.62 | 607.5 | तदस्समपन्मि� | ततः सम्पन्नम् right after 'तश्समहा सुरहा' (स महासुरः, end of 11.61); 609.6 'वादखा रष्टे' = दत्त्वा हस्ते |
| `0vvvIrHt5ek` | aranya.20.22 | 207.3 | निपेतो | निपेतुः शोणित after अद्रुमाः (end of 21) |
| `53UWT72sPHU` | aranya.31.48 | 480.0 | चापा पाहरे भुजबेग पंके | चापापहारे भुजवेगपङ्के; 31.47 ends at ~479 |
| `ogsEhZmydxQ` | aranya.61.30 | 290.2 | साँच्टाः | 'तम साँच्टाः' = तं सान्त्वया; 'तम' has the window-start time 288.0 and 61.29 line 2 (हा...) begins 287.6, so the first reliable word is 'साँच्टाः'; line 2 'प्रश्रितः प्रश्रिताञ्जलिः' heard at 300.0-301.8; 303.68 is 61.31 |
| `6KKvI1c-Plk` | aranya.70.9 | 86.1 | दक्शन अदक्शन आम बाहु मसक्त | दक्षिणो दक्षिणं बाहुमसक्तम् in a new segment after 'तश्याम सदेश' (तस्यांसदेशतः, end of 70.8) |
| `JKexnb34x6Q` | sundara.14.11 | 110.4 | पुष्पा� | पुष्पावकीर्णः after बच्पावच्ताया हा (पुष्पवृष्टयः) |
| `JKexnb34x6Q` | sundara.14.12 | 120.0 | जिशा सर्वा भिदावन्तम | दिशः सर्वाभिधावन्तं after गिरी ही (गिरिः) |
| `JKexnb34x6Q` | sundara.14.13 | 129.2 | ब्र्ख्शे ब्याफ़े दाईईप | वृक्षेभ्यः पतितैः पुष्पै |
| `gnsgzQDFFX8` | sundara.67.19 | 178.9 | के मर्टाएग | किमर्थमस्त्रं right after आँची बानबे (सत्त्ववाञ्छीलवानपि, end of 67.18) |
| `gnsgzQDFFX8` | sundara.67.22 | 206.4 | सके मर्ठमना रवरो | स किमर्थं नरवरो; 205.7 is inside परन्तपः (end of 67.21) |
| `gnsgzQDFFX8` | sundara.67.24 | 225.2 | समर्ठो | समर्थौ after न संशयः (end of 67.23) |
| `WNuQA8TslNU` | yuddha.1.7 | 74.4 | यो विद्यों योटस्सन भद्रज | यो हि भृत्यो नियुक्तः सन् भर्त्रा |
| `WNuQA8TslNU` | yuddha.1.9 | 94.2 | नियोख्तो | नियुक्तो after मध्यमं नरम् (end of 1.8); 85.0 was inside 1.8 (heard from 84.0 यो ने योगता, current 83.6 fine) |
| `tJXrwnLb4zA` | yuddha.17.61 | 580.1 | आ� बच्च्यम्सबज़गाँ़ाराव | अशक्यं सहसा राजन्, directly after 'सुखागतम' (end of 17.60); 'वो बोद्ध्वं' at 586.6 is a squashed window tail |
| `tJXrwnLb4zA` | yuddha.17.63 | 600.0 | आशांगेतमते स्वस्थो | अशङ्कितमतिः स्वस्थो; 598.1-599.2 is still 'नास्ति संशयः' of 17.62 (window-start time, real start about 599.5-600) |
| `tJXrwnLb4zA` | yuddha.17.64 | 608.8 | आखार अश्चाद यमानो | आकारश्छाद्यमानो; 608.4 is 'हा' (end of संशयः, 17.63) |
| `CbT4-ce-RrA` | yuddha.42.28 | 273.5 | गोलां गोला महाका | गोलाङ्गूलो महाकायो right after 'बदिश्वरहा' (हरीश्वरः, end of 42.27); 276.0 'गवाखशो भी मदरशना' = गवाक्षो भीमदर्शना |
| `CbT4-ce-RrA` | yuddha.42.29 | 284.6 | बच्चानाम भी मखो पानाम धूम् | ऋक्षाणां भीमकोपानां धूम्रः after 'रा मस्या पार्ष्वता हा' (रामस्य पार्श्वतः, end of 42.28); the aligner had matched the shared second line |
| `5CflAk9aw8s` | yuddha.43.33 | 308.0 | दिविदं | द्विविदं वानरेन्द्रं after सर्वरक्षासाँ (end of 32) |
| `5CflAk9aw8s` | yuddha.43.34 | 316.6 | सचा रहे | स शरैर् after बदाशनिप प्रभाखा (विव्याधाशनिप्रभः); then विर्दान्गोद विदाख्रोद (विद्धाङ्गो द्विविदः क्रोध) |
| `igIrybdPJW0` | yuddha.57.26 | 250.1 | महा जलदाने गोगु | महाजलदनिर्घोषं right after सुसंयतम (end of 57.25) |
| `igIrybdPJW0` | yuddha.57.27 | 259.5 | सुवरन जाल | सुवर्णजाल after स्वपस्करम (end of 57.26); 253.18 was inside 57.26 |
| `6jZna_DwNOI` | yuddha.62.2 | 16.2 | राख्षा सान | राक्षसानां after ययौ विपुलविक्रमः (end of 62.1) |
| `X5PX55vTlNc` | yuddha.67.51 | 517.7 | तमा | तमापतन्तं (continued 'अपतन्तम सम्प्रेखष्य'), after 'वमभिदुद्रूवे' (end of 67.50); followed by उत्पपात...सुग्रीवो |
| `X5PX55vTlNc` | yuddha.67.52 | 526.7 | सपर्वता | स पर्वताग्रम्, right after 'आन रादिपःा' (वानराधिपः, end of 67.51); 532.6 'बद्याग्र मुच्ख्षिप्या' is a squashed window tail |
| `X5PX55vTlNc` | yuddha.67.53 | 535.4 | तमापतन्तम सम्प्रेक्ष्य कुम् | second तमापतन्तं (67.53), confirmed by 'तस्तो विवरत्त सर्वांगो' (तस्थौ विवृत्तसर्वाङ्गो) at 540.0 |
| `X5PX55vTlNc` | yuddha.67.154 | 1611.2 | तदस्तो रक्शा | ततस्तु रक्षः right after 'मुद्गर मुग्र बद्याबेगम' (मुद्गरमुग्रवेगम्, end of 67.153; same quarter-line recurs in 154); 1613.0 'शाटा जानो लेप' = क्षतजानुलिप्तं. 67.153 at 1598.58 is plausible (its line 2 'बन चरीरेन' at 1602.7) |
| `9sa2dGZmwbY` | yuddha.70.36 | 344.1 | तमा पा | तमापतन्तम् after अद्रमवर्शम प्रत्टी (द्रुमवर्षं ... प्रति, end of 35); then आखाशे द्रमवर्शम |
| `RJ_h1WjpqCA` | yuddha.91.12 | 106.9 | मुर्� | मूर्ध्नि right after निश्वास पेडितम (निःश्वासपीडितम्, end of 91.11); line 2 उवाच लक्ष्मणं at 111.5 |
| `GIv3yTdJ4wA` | yuddha.93.33 | 321.2 | देवास अस्याश्ट | दिवसस्याष्ट(भागेन), after पदातिनाम् (end of 93.32); then बागे लश़र = भागेन शरैर |
| `vIaRd6iqzkk` | yuddha.100.1 | 6.0 | बिन्प्रतिहाते स्ट्रे तुराव | तस्मिन् प्रतिहतेऽस्त्रे तु रावणो: the opening it shares with 100.6 (…राघवेण), which is heard again at 54.0 |
| `vIaRd6iqzkk` | yuddha.100.6 | 54.0 | तस्मिन प्रतिहाते स्ट्रे तु र | followed by 'अग्रोदा ताम्राख्षा सुरा मस' (क्रोधताम्राक्षः सौरमस्त्र) and 'बदियर या' (उदीरयत्); the 6.0 'बिन्प्रतिहाते स्ट्रे तुराव' is another verse with the same opening (it goes on to 'मजेन विधम रोद्' = मयेन विहितं रौद्रम्), not 100.6 |
| `vIaRd6iqzkk` | yuddha.100.7 | 64.2 | तब अश्चक्राले नेश्पेत | ततश्चक्राणि निष्पेतुः; 63.06 is still उदीरयत् of 100.6 |
| `vtBz_PsmiWM` | yuddha.118.10 | 94.2 | विषुध्� | विशुद्धभावां after नान्तरात्मना (end of 9) |
| `vtBz_PsmiWM` | yuddha.118.11 | 103.6 | तदफ प्री� | ततः प्रीतमना after अग्छ्या पयामिते (अहमाज्ञापयामि ते) |
| `u4UoCycTV6o` | yuddha.123.26 | 246.0 | एवा मुक्तो तवाईदे श्यारा | एवमुक्तोऽथ वैदेह्या after राजधानीं त्वया सह |
| `u4UoCycTV6o` | yuddha.123.27 | 256.7 | बिमानम | विमानं after प्राप्य संस्थाप्य राघवः (end of 123.26); 246.88 was inside 123.26 |
| `u4UoCycTV6o` | yuddha.123.28 | 266.7 | व्स्त्रीभिख परीव्र्ता | स्त्रीभिः परिवृताः after वानर पुं(गवान्) ending 123.27 |
| `ezj1sI8l82g` | yuddha.128.123 | 1215.9 | बच्यारा मस्यायेट्याट्याट्य | भक्त्या रामस्य ये, after रामायणस्य श्रवणे तृप्यन्ति; ends वासस्त्रिविष्टपे ~1229 |
| `ezj1sI8l82g` | yuddha.128.125 | 1239.7 | आयुश्य | आयुष्यम् right after चार्थसिद्धिम् (वाद्दादिएं) |
