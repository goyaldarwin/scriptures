# Hand-set data of the Shabad Guru recordings, with their evidence

## uEFQLir74Fo (1157.2): its track ends at 147 s (`recordings.json` "end")

The video (22 min) sings Sri Guru Granth Sahib 1157.2, ਇਹੁ ਧਨੁ ਮੇਰੇ ਹਰਿ ਕੋ ਨਾਉ, and then other shabads of Bhagat Kabir.
The letters MMS hears (`mms/uEFQLir74Fo.json` "read_at", from its whole length before the end was set) end the verse's
last line, ਕਹਿ ਕਬੀਰ ਹਉ ਤਾ ਕੋ ਦਾਸੁ, at about 140 s ("…udastahikbirahatako"), and from 147 s go on with another
shabad's words and its own rahao ("ajaniamirasampaanet…rahao…"), unlike any line of 1157.2. `mms_merge.py` flagged it
(`beyond`): the line search placed the verse's lines up to 114–119 s and then only scattered matches of its last two
lines over the rest of the video.

## mVXVLYxz-Ag (509.2): it sings 509.2 to 509.4 (`recordings.json` "to")

The video's title names the salok 509.2, ਸਾਹਿਬੁ ਮੇਰਾ ਸਦਾ ਹੈ, but it sings the stanza of the vaar it opens: the salok, the
next salok 509.3 and the pauri 509.4. The letters MMS hears (`mms/mVXVLYxz-Ag.json` "read_at", from the run that was
given 509.2 alone) end 509.2 with ਨਾਨਕ ਏਵ ਨ ਜਾਪਈ … ਦੇਇ ਸਜਾਇ at about 98–108 s ("naanakelajapaikaretaketide sajai"), then
sing a heading and 509.3 (108–175 s: "…mahalatinja", "…sajanahamdeaa…", "kathenibadanitaritaapirehukam…") and 509.4
(from about 185 s: "…jogavijogopaionsisttiikamulela…", "…jotijotamilaaya"). Given 509.2 alone, the line search
had placed the later saloks' lines as repeats of 509.2's.

## Starts checked in 5-s windows (`tools/audio/windows.py`, Whisper small, one window a second)

MMS's start (lean taken off) against the last window that still begins with the line's first words. Where they agree
within a second MMS's start stands and no hand start is kept.

| Recording, verse, line | MMS | Windows | |
|---|---|---|---|
| fLOzmgoLVEw, 110.1, line 2 ਬਿਨੁ ਤਕੜੀ ਤੋਲੈ ਸੰਸਾਰਾ | 43.9 s | 44 s ("बिन तक्री तो ले सन्सा"; 38 s hears the line before's end) | agrees |
| fLOzmgoLVEw, 110.1, line 9 ਜਿਸੁ ਆਪਿ ਭੁਲਾਏ ਸੁ ਕਿਥੈ ਹਥੁ ਪਾਏ | 132.8 s | 133 s ("जिस आप पुलाए सोग तेहाँ"; 134 s its middle) | agrees |
| fLOzmgoLVEw, 110.1, line 20 ਕਿਲਬਿਖ ਕਾਟਿ ਸਦਾ ਜਨ ਨਿਰਮਲ … | 242.6 s | 243 s ("विर्भिक खावा…"; 244 s "…कावाट्टु पना जान") | agrees |
| OtglEtAgD8w, 993.1, line 5 ਜਿਸ ਨੋ ਸਾਚਾ ਸਿਫਤੀ ਲਾਏ | 70.7 s | 71 s ("जिसे नो साचा सी फती"; 72 s "…सिफती लाई") | agrees |
| mVXVLYxz-Ag, 509.2, line 3 ਸਦਾ ਸਦਾ ਸੋ ਸੇਵੀਐ … | 43.5 s | 44 s ("सेदा, सादे, सो"; 46 s "…सीविये") | agrees |
| mVXVLYxz-Ag (given 509.2 alone), a repeat of line 3 at 123.5 s | — | 119–127 s hear "सजाल नाम…", not this line | the singing was 509.3's: the recording's "to" above |
