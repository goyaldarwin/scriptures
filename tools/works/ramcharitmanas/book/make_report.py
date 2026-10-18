import json
vo=json.load(open('verify_ocr.json')); vt=json.load(open('verify_tr.json')); V=json.load(open('variants.json'))
m=json.load(open('merged.json')); n=len(m['items'])
tr_clean=sum(1 for it in m['items'] if not vt.get(it['id']))
vw=sum(v['v'][1] for v in vo.values()); vok=sum(v['v'][0] for v in vo.values())
hw=sum(v['h'][1] for v in vo.values()); hok=sum(v['h'][0] for v in vo.values())
nvar=sum(len(v) for v in V.values()); ntypo=sum(1 for v in V.values() for x in v if x[2])
html=('<ul><li><b>%d</b> पद (श्लोक, दोहे, चौपाई, छंद) — इनमेंसे <b>%d</b> का मूल पाठ अंग्रेज़ी पुस्तकके रोमन लिप्यन्तरणसे शब्दशः मेल खाता है।</li>'%(n,tr_clean)+
 '<li>बाकी पदोंमें अधिकतर अंतर रोमन लिप्यन्तरणके लिखनेके ढंगके हैं (जैसे “भयउ/bhayau”)। जाँचके बाद <b>%d</b> स्थानोंपर दोनों पुस्तकोंमें सचमुच अलग शब्द मिले; उन पदोंपर <span class="tag">पाठभेद</span> लगा है — टैप करके दोनों रूप देखें। इनमें %d स्थान संभवतः आपकी हिंदी PDFकी छपाई-त्रुटि हैं।</li>'%(nvar,ntypo)+
 '<li>अलग OCR से तुलना: मूल पाठके %.1f%% और हिंदी भावार्थके %.1f%% शब्द OCR से अक्षरशः मिले। बचे अंतरोंकी जाँच की गई — वे OCR की अपनी गलतियाँ हैं (जैसे “गङ्गा” को “गड़ा” पढ़ना), पुस्तक-पाठ नहीं।</li>'%(vok/vw*100,hok/hw*100)+
 '<li>पुस्तक-फ़ाइलके अक्षर-चिह्नोंको पढ़नेका हर नियम पन्नोंकी तस्वीरोंसे मिलाकर जाँचा गया; अंग्रेज़ी अनुवाद PDFसे सीधे लिया गया है (OCR नहीं)।</li></ul>')
json.dump({'html':html,'n':n,'tr_clean':tr_clean,'nvar':nvar,'ntypo':ntypo,'vocr':round(vok/vw*100,1),'hocr':round(hok/hw*100,1)},open('report.json','w'),ensure_ascii=False)
print(json.load(open('report.json')))
