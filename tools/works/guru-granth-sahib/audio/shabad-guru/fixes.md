# Hand-set data of the Shabad Guru recordings, with their evidence

## uEFQLir74Fo (1157.2): its track ends at 147 s (`recordings.json` "end")

The video (22 min) sings Sri Guru Granth Sahib 1157.2, ਇਹੁ ਧਨੁ ਮੇਰੇ ਹਰਿ ਕੋ ਨਾਉ, and then other shabads of Bhagat Kabir.
The letters MMS hears (`mms/uEFQLir74Fo.json` "read_at", from its whole length before the end was set) end the verse's
last line, ਕਹਿ ਕਬੀਰ ਹਉ ਤਾ ਕੋ ਦਾਸੁ, at about 140 s ("…udastahikbirahatako"), and from 147 s go on with another
shabad's words and its own rahao ("ajaniamirasampaanet…rahao…"), unlike any line of 1157.2. `mms_merge.py` flagged it
(`beyond`): the line search placed the verse's lines up to 114–119 s and then only scattered matches of its last two
lines over the rest of the video.
