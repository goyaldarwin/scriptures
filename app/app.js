'use strict';
/* =====================================================================
   Scripture reader — library of works; each work = text (verse + number)
   with selectable sources for Hindi meaning, English meaning and audio.
   Word meanings come from one dictionary per language (library/glossary), chosen by the verse's language.
   ===================================================================== */
const $ = s => document.querySelector(s);
const $$ = s => Array.from(document.querySelectorAll(s));
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
// every number is shown as 1 2 3, in Hindi too (the owner: few read १ २ ३ today); the texts keep their own digits and are
// shown so: each Devanagari or Gurmukhi number on the page is written in Latin digits as it appears (a digit inside a word,
// the pluta ३ of ओ३म्, stays); a textarea keeps what it holds, so a correction or a note is saved as written
const DEV = n => String(n);
const LATD = /(^|[^\u0900-\u0963\u0971-\u097F\u0A00-\u0A65\u0A70-\u0A7F])([०-९੦-੯]+)/g;
const LAT = s => s.replace(LATD, (m, a, d) => a + d.replace(/[०-९੦-੯]/g, c => { const k = c.charCodeAt(0); return String(k >= 0x0A66 ? k - 0x0A66 : k - 0x0966); }));
function latNode(root){
  if (root.nodeType === 3){ if (!root.parentNode || root.parentNode.closest('textarea,script,style')) return; const v = LAT(root.data); if (v !== root.data) root.data = v; return; }
  if (root.nodeType !== 1 || root.closest('textarea,script,style')) return;
  const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT), ns = []; while (tw.nextNode()) if (/[०-९੦-੯]/.test(tw.currentNode.data)) ns.push(tw.currentNode);
  ns.forEach(latNode);
}
new MutationObserver(ms => ms.forEach(m => m.type === 'characterData' ? latNode(m.target) : m.addedNodes.forEach(latNode))).observe(document.documentElement, {childList: true, subtree: true, characterData: true});
latNode(document.body);
const ORDH = ['', 'पहला', 'दूसरा', 'तीसरा', 'चौथा', 'पाँचवाँ', 'छठा', 'सातवाँ', 'आठवाँ', 'नवाँ', 'दसवाँ', 'ग्यारहवाँ', 'बारहवाँ', 'तेरहवाँ', 'चौदहवाँ', 'पंद्रहवाँ', 'सोलहवाँ', 'सत्रहवाँ', 'अठारहवाँ', 'उन्नीसवाँ', 'बीसवाँ', 'इक्कीसवाँ', 'बाईसवाँ', 'तेईसवाँ', 'चौबीसवाँ', 'पचीसवाँ', 'छब्बीसवाँ', 'सत्ताईसवाँ', 'अट्ठाईसवाँ', 'उनतीसवाँ', 'तीसवाँ'];
const TYPEN = {do: ['दोहा', 'Doha'], so: ['सोरठा', 'Soratha'], cha: ['छंद', 'Chhand'], shloka: ['श्लोक', 'Shloka'], cau: ['चौपाई', 'Chaupai']};
const TYPE = new Proxy({}, {get: (o, k) => TYPEN[k] ? T(TYPEN[k][0], TYPEN[k][1]) : ''});
const TT = o => o ? (typeof o === 'string' ? o : T(o.hi, o.en || o.hi)) : '';

/* ---------------- loading ---------------- */
const BUNDLE = window.__BUNDLE || null;            // offline file / claude.ai link carry everything inside
async function getJSON(path){
  if (BUNDLE){ const v = BUNDLE.files[path]; if (v) return v; throw new Error('missing ' + path); }
  const r = await fetch('library/' + path + '.json', {cache: 'no-cache'}); if (!r.ok) throw new Error(path); return r.json();
}
let LIB = [], LANGS = {}, GL = {}, WG = {}, ALT = {hi: [], en: []}, W = null, IT = [], ID = {}, SRC = {hi: null, en: null, au: null};
// meaning languages: every language with a "meaning" block in glossary/languages.json (हिं, En, ਪੰ),
// in its order. A layer's switch is S.settings.layers[LK(kind)]: h and e for Hindi and English (so older saved settings read unchanged), else the code.
const MK = () => { const k = Object.keys(LANGS).filter(c => LANGS[c].meaning).sort((a, b) => (LANGS[a].meaning.order || 100) - (LANGS[b].meaning.order || 100)); return k.length ? k : ['hi', 'en']; };
const LK = kind => kind === 'hi' ? 'h' : kind === 'en' ? 'e' : kind;
const LCLS = kind => kind === 'hi' ? 'h' : kind === 'en' ? 'e' : 'x ' + kind;   // a meaning layer's class in the reader
// the work's meaning languages (those it has a source in); the two in the header capsule (always four places: two meaning
// switches, शब्द, 📖): हिं · En, or with a third language the reader's chosen pair, by default ਪੰ · En in
// an English app and ਪੰ · हिं in a Hindi one
function workKinds(){ return W ? MK().filter(k => ((W.sources || {})[k] || []).length) : []; }
function pairOptions(){ const ks = workKinds(), extra = ks.filter(k => k !== 'hi' && k !== 'en'), out = [];
  extra.forEach(x => { out.push([x, 'en'], [x, 'hi']); }); out.push(['hi', 'en']); for (let a = 0; a < extra.length; a++) for (let b = a + 1; b < extra.length; b++) out.push([extra[a], extra[b]]);
  return out.filter(p => p.every(k => ks.includes(k) || k === 'hi' || k === 'en')); }
function capKinds(){ const ks = workKinds(); if (ks.filter(k => k !== 'hi' && k !== 'en').length === 0) return ['hi', 'en'];
  const opts = pairOptions(), sel = (S.settings.pair || '').split(','), ok = opts.find(p => p.join(',') === sel.join(','));
  return ok || opts.find(p => p[1] === (S.settings.ui === 'hi' ? 'hi' : 'en')) || opts[0]; }
const LBM = kind => kind === 'hi' ? LB.h() : kind === 'en' ? LB.e() : TT((LANGS[kind] && LANGS[kind].meaning || {}).name || {hi: kind, en: kind}) + T(' अर्थ', ' meaning');

/* ---------------- personal store ---------------- */
const LS = 'manas.personal.v1';
let canStore = true;
function newProfile(name){ return {id: 'p' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), name, notes: {}, bm: {}, done: {}, gloss: {}, fix: {}}; }
// a new reader starts in English: English interface and English meaning; हिं adds the Hindi meaning
function defaults(){ const p = newProfile('Me'); return {v: 2, settings: {ui: 'en', layers: {h: false, e: true, w: false}, tr: false, size: 21, theme: 'light', lightDefault: 1}, src: {}, w: {}, work: null, profiles: [p], active: p.id, show: [p.id]}; }
let S;
try { S = JSON.parse(localStorage.getItem(LS)); } catch (e) { canStore = false; }
if (!S || !S.profiles) S = defaults();
// timing review (☰ › More settings › Audio timing): on/off, and the starts set by ear, by "<work>:<audio source>" → {item id: [track, seconds]};
// "from": marks loaded from a helper's file and not yet checked by you, "<work>:<source>" → {item id: helper's name} (they are
// heard and shown like yours, but go to the library only after you tap ✓ under the verse); "flags": timing flags a reader set
// while listening, by "<work>:<audio source>". Filled in for every state: this phone's, a file's (older ones have none) and the cloud's.
function fillTiming(){ S.timing = S.timing || {on: false}; ['fix', 'sent', 'from', 'flags'].forEach(k => { if (!S.timing[k]) S.timing[k] = {}; }); }
fillTiming();
// Audio timing is a tool for the person checking timings, never left on by chance: it turns itself off when the site is
// opened 12 hours after it was last used, and it never travels in a saved file
if (S.timing.on && Date.now() - (S.timing.used || 0) > 12 * 3600e3) S.timing.on = false;
function migrate(){
  if ((S.v || 1) < 2) migrate2();
  if (S.settings && !S.settings.ui) S.settings.ui = S.settings.layers && S.settings.layers.e ? 'en' : 'hi';   // an older saved file has no ui: it follows the English meaning
  if (S.v < 3){ // v2 → v3: a reader's own word meanings are filed by language (“awa:राम”); older ones are all Awadhi
    S.profiles.forEach(p => { const n = {}; for (const k in p.gloss || {}) n[k.includes(':') ? k : 'awa:' + k] = p.gloss[k]; p.gloss = n; });
    S.v = 3;
  }
  oneReader(); fillTiming();
}
// One reader per device: there is no list of readers. Older saved data that has several keeps
// everything — their notes, bookmarks, progress, own meanings and corrections are joined into the first one, nothing dropped.
function mergeInto(a, b){
  for (const k in b.notes || {}){ const arr = a.notes[k] = a.notes[k] || []; b.notes[k].forEach(n => { if (!arr.some(m => m.ts === n.ts && m.t === n.t)) arr.push(n); }); }
  for (const k in b.bm || {}) if (!a.bm[k]) a.bm[k] = b.bm[k];
  for (const w in b.done || {}){ const aw = a.done[w] = a.done[w] || {}; for (const pl in b.done[w]){ const ap = aw[pl] = aw[pl] || {}; for (const n in b.done[w][pl]) if (!ap[n]) ap[n] = b.done[w][pl][n]; } }
  for (const k in b.gloss || {}) if (!a.gloss[k]) a.gloss[k] = b.gloss[k];
  for (const k in b.fix || {}) if (!a.fix[k]) a.fix[k] = b.fix[k];
}
function oneReader(){
  if (!S.profiles || !S.profiles.length) return;
  const me = S.profiles.find(p => p.id === S.active) || S.profiles[0];
  ['notes', 'bm', 'done', 'gloss', 'fix'].forEach(k => me[k] = me[k] || {});
  S.profiles.filter(p => p !== me).forEach(p => mergeInto(me, p));
  S.profiles = [me]; S.active = me.id; S.show = [me.id];
}
function migrate2(){
  // v1 → v2: keys gain the work id, per-work positions and plan progress
  const pre = 'manas:';
  S.profiles.forEach(p => {
    const re = o => { const n = {}; for (const k in o || {}) n[k.includes(':') ? k : pre + k] = o[k]; return n; };
    p.bm = re(p.bm); p.notes = re(p.notes);
    const fx = {}; for (const k in p.fix || {}){ const f = p.fix[k]; if (k.startsWith('g')) continue; if (f.v) fx[pre + k] = {v: f.v}; if (f.h != null) fx[pre + 'hi-gitapress:' + k] = {m: f.h}; } p.fix = fx;
    if (p.done && (p.done.M || p.done.N)) p.done = {manas: {M: p.done.M || {}, N: p.done.N || {}}};
  });
  S.w = S.w || {}; S.w.manas = {pos: {}, last: null, org: S.settings.org || 'k'};
  S.src = S.src || {}; S.work = 'manas'; S.v = 2; delete S.pos; delete S.last;
}
migrate();
let CLOUD = null, cloudT = null, cloudBusy = false, cloudAgain = false;
function save(){ S.ts = Date.now(); if (S.timing && S.timing.on) S.timing.used = S.ts; if (canStore){ try { localStorage.setItem(LS, JSON.stringify(S)); } catch (e) { canStore = false; } } if (CLOUD){ clearTimeout(cloudT); cloudT = setTimeout(cloudPush, 1500); } }
async function cloudPush(){ if (!CLOUD) return; if (cloudBusy){ cloudAgain = true; return; } cloudBusy = true; try { await CLOUD.set({s: JSON.stringify(S), ts: S.ts || Date.now()}); } catch (e) { if (e && e.code === 'unavailable') setTimeout(cloudPush, 3000 + Math.random() * 2000); } cloudBusy = false; if (cloudAgain){ cloudAgain = false; cloudPush(); } }
async function cloudInit(){
  try {
    if (!window.claude || !window.claude.use) return;
    const [db, user] = await Promise.all([window.claude.use('db'), window.claude.use('user')]);
    if (!db || !user) return; const uid = await user.id(); if (!uid) return;
    const ref = db.doc('data/users/' + uid + '/state'); const snap = await ref.get(); CLOUD = ref;
    if (snap.exists){ const d = snap.data(); if (d && d.s && (d.ts || 0) > (S.ts || 0)){ const X = JSON.parse(d.s); if (X && X.profiles){ S = Object.assign(defaults(), X); migrate(); try { localStorage.setItem(LS, JSON.stringify(S)); } catch (e) {} applyState(); } } else if ((S.ts || 0) > (d.ts || 0)) cloudPush(); }
    else if (S.ts) cloudPush();
    canStore = true;
  } catch (e) {}
}
// the language of the app: its own setting (S.settings.ui), chosen with हिं · En on the library, work and vidhi pages;
// turning the English or the Hindi meaning on in the reader sets it too (the layer switch below)
// Inside a work's text (the reader) the words around the verses follow the meanings chosen there:
// English meaning on → English; only the Hindi meaning → Hindi; neither → the app's language.
let CURVIEW = 'library';
const LANG = () => CURVIEW === 'reader' ? (S.settings.layers.e ? 'en' : S.settings.layers.h ? 'hi' : (S.settings.ui === 'hi' ? 'hi' : 'en')) : (S.settings.ui === 'hi' ? 'hi' : 'en');
function T(hi, en){ return LANG() === 'en' ? en : hi; }
const ME = () => S.profiles.find(p => p.id === S.active) || S.profiles[0];
const SHOWN = () => S.profiles.filter(p => S.show.includes(p.id));
const WS = () => (S.w[W.id] = S.w[W.id] || {pos: {}, last: null, org: 'k'});
const KEY = id => W.id + ':' + id;
const DONE = (p, plan) => ((p.done[W.id] = p.done[W.id] || {})[plan] = p.done[W.id][plan] || {});

/* ---------------- shared labels ---------------- */
const LB = {
  h: () => T('हिंदी अर्थ', 'Hindi meaning'), e: () => T('अंग्रेज़ी अर्थ', 'English meaning'), w: () => T('शब्दार्थ', 'Word meanings'), au: () => T('ऑडियो', 'Audio'),
  tr: () => T('रोमन लिप्यन्तरण', 'Transliteration'), trSub: () => T('पदके नीचे रोमन अक्षरोंमें', 'The verse in Roman letters, under it'),
  lines: () => T('हर पंक्तिका अर्थ', 'Meaning per line'), linesSub: () => T('अर्थको पंक्ति-अनुसार बाँटें', 'Split the meanings by line'),
  rc: () => T('पाठ मोड', 'Recitation mode'), rcSub: () => T('केवल मूल पाठ, बड़े अक्षर', 'Verses only, larger letters'),
  size: () => T('अक्षरका आकार', 'Letter size'), theme: () => T('रंग', 'Theme'), more: () => T('और सेटिंग', 'More settings'), tour: () => T('परिचय (टूर)', 'Take the tour'),
  sections: () => T('प्रसंग', 'Sections'), search: () => T('खोजें', 'Search'),
  bm: () => T('बुकमार्क और टिप्पणियाँ', 'Bookmarks & notes'), verses: () => T('मूल पाठ', 'Verses'),
  lib: () => T('पुस्तकालय', 'Library'), src: () => T('स्रोत', 'Sources'), vidhi: () => T('पारायण-विधि', 'Parayan vidhi')
};

/* ---------------- ui helpers ---------------- */
let toastT;
// a toast with one action (e.g. “Continue ▶” after a verse has been played); it stays a little longer and can be tapped
function toastAct(msg, label, fn){ const t = $('#toast'); t.innerHTML = esc(msg) + ' <button class="tact">' + esc(label) + '</button>'; t.classList.add('on', 'act'); t.querySelector('.tact').onclick = () => { t.classList.remove('on', 'act'); fn(); }; clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove('on', 'act'), 8000); }
// a message in the light card of "Finished · ▶ Play on" (white and blue), without a button
function toastLight(msg, ms){ const t = $('#toast'); t.textContent = msg; t.classList.add('on', 'act'); clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove('on', 'act'), ms || 4000); }
function toast(msg){ $('#toast').classList.remove('act'); const t = $('#toast'); t.textContent = msg; t.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove('on'), 2600); }
function applyLang(){ const en = LANG() === 'en'; document.documentElement.lang = en ? 'en' : 'hi';
  $$('[data-en]').forEach(el => { if (el.dataset.hi == null) el.dataset.hi = el.innerHTML; el.innerHTML = en ? el.dataset.en : el.dataset.hi; });
  $$('[data-en-ph]').forEach(el => { if (el.dataset.hiPh == null) el.dataset.hiPh = el.placeholder; el.placeholder = en ? el.dataset.enPh : el.dataset.hiPh; }); }
function applyTheme(){ const r = document.documentElement; if (S.settings.theme === 'auto') r.removeAttribute('data-theme'); else r.setAttribute('data-theme', S.settings.theme); r.style.setProperty('--verse-size', S.settings.size + 'px'); r.style.setProperty('--mean-size', Math.round(S.settings.size * 0.78 * 10) / 10 + 'px'); r.style.setProperty('--ui-zoom', (1 + (S.settings.size - 21) * 0.025).toFixed(3)); }   // A−/A+ also scale the library and work pages
function show(id, push = true){ { const was = LANG(); CURVIEW = id; if (LANG() !== was) applyLang(); }
  if ((id === 'library' || id === 'home' || id === 'reader') && S.view !== id){ S.view = id; save(); }   // where the app opens next time
  $$('.view').forEach(v => v.classList.toggle('on', v.id === id)); if (push) history.pushState(snap(id), ''); else history.replaceState(snap(id), ''); if (id !== 'reader') window.scrollTo(0, 0); onView(id); }
// Every page is an entry in the browser's history that carries where you are: the page, the open work and the library
// shelf. Back (the button or the phone's gesture) returns to exactly the previous one — a shelf
// included — and a refresh reopens the same page, because the browser keeps these entries across a reload.
function snap(v){ return {v, w: W ? W.id : null, lib: libPath.slice(), scope: v === 'search' ? SCOPE : undefined, r: v === 'reader' && R.at ? Object.assign({}, R.at) : undefined}; }
let popping = Promise.resolve();
async function restore(st){
  closeSheet();
  if (!st || !st.v) st = {v: 'library', w: null, lib: []};
  libPath = Array.isArray(st.lib) ? st.lib.slice() : [];
  if (st.v !== 'library' && st.w && (!W || W.id !== st.w)) await openWork(st.w, true);
  const v = document.getElementById(st.v) && (W || !['home', 'reader', 'bookmarks', 'vidhi'].includes(st.v)) ? st.v : 'library';
  if (v === 'search') setScope(st.scope === 'lib' || !W ? 'lib' : 'text');   // Back to a search: the same kind of search, the query kept
  show(v, false);
  if (v === 'reader'){ const r = st.r, i = r && W && ID[r.id]; if (i != null && (r.org === 'k' || PLAN[r.org])) openReader(r.org, i); else reopenReader(); }   // the reader's own place: a plan day stays that day
}
function back(){ history.back(); }
// Back with a drawer open closes the drawer and stays on the page (its entry is put back)
window.addEventListener('popstate', e => { if ($('#sheet').classList.contains('on')){ closeSheet(); history.pushState(snap(CURVIEW), ''); return; } const st = e.state; popping = popping.then(() => restore(st)); });
function onView(id){ if (PL.on) pSub(); if (id === 'library') renderLibrary(); if (id === 'home') renderHome(); if (id === 'bookmarks') renderBookmarks(); if (id === 'settings') renderSettings(); if (id === 'vidhi') renderVidhi(); wake(id === 'reader'); if (id === 'search') setTimeout(() => $('#q').focus(), 50); }
$$('[data-back]').forEach(b => b.onclick = back);
$$('[data-go]').forEach(b => b.onclick = () => show(b.dataset.go));
function openSheet(html){ $('#sheetBody').innerHTML = html; $$('#sheetBody [data-tour]').forEach(b => b.onclick = () => { closeSheet(); startTour(); }); $('#sheet').classList.add('on'); $('#scrim').classList.add('on'); $('#sheet').scrollTop = 0; }
// the drawer closes by dragging it down (from its handle, or anywhere once it is scrolled to the top), as its handle suggests
(function(){ const sh = $('#sheet'); let y0 = null, dy = 0;
  sh.addEventListener('touchstart', e => { const fromGrab = !!e.target.closest('.grab'); if (!fromGrab && sh.scrollTop > 0) { y0 = null; return; } y0 = e.touches[0].clientY; dy = 0; }, {passive: true});
  sh.addEventListener('touchmove', e => { if (y0 == null) return; dy = e.touches[0].clientY - y0; if (dy > 0){ sh.style.transition = 'none'; sh.style.transform = 'translateY(' + dy + 'px)'; } }, {passive: true});
  sh.addEventListener('touchend', () => { if (y0 == null) return; sh.style.transition = ''; sh.style.transform = ''; if (dy > 80) closeSheet(); y0 = null; dy = 0; });
  sh.querySelector('.grab').addEventListener('click', () => closeSheet());
})();
function closeSheet(){ $('#sheet').classList.remove('on'); $('#scrim').classList.remove('on'); $$('.w.sel, .mw.sel').forEach(w => w.classList.remove('sel')); }
$('#scrim').onclick = () => closeSheet();
function sw(id, label, sub, on, icon){ return '<label class="sw">' + (icon ? '<svg class="swic"><use href="#i-' + icon + '"/></svg>' : '') + '<span' + (icon ? ' style="flex:1"' : '') + '>' + label + (sub ? '<small>' + sub + '</small>' : '') + '</span><span class="tg"><input type="checkbox" id="' + id + '"' + (on ? ' checked' : '') + '><span></span></span></label>'; }

/* ---------------- wake lock ---------------- */
let wl = null;
// the screen stays on while reading or playing — always, no setting
async function wake(on){ try { if (on && 'wakeLock' in navigator){ if (!wl){ wl = await navigator.wakeLock.request('screen'); wl.addEventListener('release', () => wl = null); } } else if (wl && !PL.on){ await wl.release(); wl = null; } } catch (e) {} }
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible' && ($('#reader').classList.contains('on') || PL.on)) wake(true); });

/* ---------------- word meanings: one dictionary per language (library/glossary/<lang>.json) ----------------
   A word is looked up in the language of the verse it is in, then in that language's fallbacks
   (languages.json). A work may refine a sense in <work>/glossary.json; a reader's own meaning wins. */
const PUNCT = /[\s।॥|,.;:!?\-—‘’“”'"()\[\]०-९੦-੯0-9]/g;   // Devanagari and Gurmukhi digits are verse numbers, not words
const SVARA = /[\u0951-\u0954\u1CD0-\u1CFF\uA8E0-\uA8F1]/g;   // Vedic accent marks: shown in the text, ignored when looking a word up
function cleanWord(w){ return w.replace(PUNCT, '').replace(SVARA, '').normalize('NFC'); }   // PUNCT takes spaces too: ॥ is kept with its word by a no-break space
function langOf(i){ return (i != null && IT[i] && IT[i].l) || W.lang; }
function langChain(lang){ return [lang].concat((LANGS[lang] || {}).fallback || []); }
async function loadGlossaries(){
  if (!Object.keys(LANGS).length) LANGS = await getJSON('glossary/languages');
  const need = new Set(['hi', 'en']); [W.lang].concat(IT.map(x => x.l).filter(Boolean)).forEach(l => langChain(l).forEach(c => need.add(c)));   // hi, en: the hard words of the meanings
  await Promise.all([...need].filter(c => !GL[c]).map(async c => { try { GL[c] = await getJSON('glossary/' + c); } catch (e) { GL[c] = {}; } }));
  WG = {}; if (W.glossary && !BYPART()){ try { WG = await getJSON(W.path + '/glossary'); } catch (e) {} }   // a work loaded by part: glossary/<part> (loadPart)
}
// a word's lookup form (fold() in tools/text/standard.py): a class nasal before its stop, ꣳ (also as typed, ग्ं) and a
// word-final म् are ं, so गङ्गा finds गंगा and इदम् finds इदं
function fold(w){ return w.replace(/ग्ं/g, 'ं').replace(/ꣳ/g, 'ं').replace(/[ङञणनम]्(?=[कखगघचछजझटठडढतथदधपफबभ])/g, 'ं').replace(/म्$/, 'ं'); }
function foldIndex(d){ if (!d) return null; if (!d.__fold){ const f = {}; for (const k in d){ const g = fold(k); if (!(g in f)) f[g] = d[k]; } Object.defineProperty(d, '__fold', {value: f}); } return d.__fold; }
function dictEntry(lang, w){
  const e = (WG[lang] && WG[lang][w]) || (GL[lang] && GL[lang][w]); if (e) return e;
  const f = fold(w); return (foldIndex(WG[lang]) || {})[f] || (foldIndex(GL[lang]) || {})[f] || null;
}
function lookup(w, lang){
  w = cleanWord(w); if (!w) return null; lang = lang || W.lang;
  const chain = langChain(lang);
  for (const c of chain){
    for (const p of SHOWN()) if (p.gloss[c + ':' + w]) return Object.assign({w, lang: c, mine: p.name}, dictEntry(c, w) || {}, p.gloss[c + ':' + w]);
    const e = dictEntry(c, w); if (e) return Object.assign({w, lang: c}, e);
  }
  for (const c of chain){ const L = LANGS[c] || {};
    for (const sfx of L.suffixes || []){ if (w.length > sfx.length + 1 && w.endsWith(sfx)){ const b = w.slice(0, -sfx.length); for (const st of L.stems || ['']){ const e = dictEntry(c, b + st); if (e) return Object.assign({w, lang: c, possible: b + st}, e); } } } }
  return {w, lang, none: true};
}
function wordsHTML(line){
  line = line.replace(/\s+(।|॥)/g, ' $1');
  const halves = line.split(/(?<=[।॥])\s+(?=[^\s।॥०-९੦-੯(])/).reduce((a, h) => { if (a.length && /^[।॥\s]+$/.test(a[a.length - 1])) a[a.length - 1] += ' ' + h; else a.push(h); return a; }, []);
  return halves.map(hf => '<span class="half">' + hf.split(/( +)/).map(tok => { if (/^ +$/.test(tok) || !cleanWord(tok)) return esc(tok); const m = tok.match(/^(.*?)( .*)?$/); return '<span class="w">' + esc(m[1]) + '</span>' + esc(m[2] || ''); }).join('') + '</span>').join(' ');
}
/* the hard words of our meanings: a word of a Hindi or English meaning whose entry in that language's dictionary
   (the work's own glossary first, then glossary/hi.json or en.json) has "hard": true is faintly underlined and opens its meaning like a verse word. A joined
   ending (मनमें, विषयोंसे, आसक्तियोंको), a name's जी (विभीषणजीने) or an English plural, tense or 's is looked through to the entry. */
const HARD_RE = {hi: /[\u0900-\u0963\u0966-\u097F\u200C\u200D]+/g, en: /[A-Za-zÀ-ɏḀ-ỿ]+(?:[’'][A-Za-zÀ-ɏḀ-ỿ]+)*/g};
const HI_POST = ['वाला', 'वाली', 'वाले', 'में', 'से', 'को', 'का', 'की', 'के', 'ने', 'पर', 'तक'];
function hardForms(w, lang){
  if (lang === 'en'){ const x = w.toLowerCase().replace(/[’']s$/, ''); return [x, x.replace(/ies$/, 'y'), x.replace(/es$/, ''), x.replace(/s$/, ''), x.replace(/ed$/, ''), x.replace(/ed$/, 'e'), x.replace(/ing$/, ''), x.replace(/ing$/, 'e'), x.replace(/ly$/, '')]; }
  w = w.replace(/[\u200C\u200D]/g, '');   // a joiner (जाम्बवान्‌ने) is not part of the word
  let base = [w].concat(HI_POST.filter(p => w.length > p.length + 1 && w.endsWith(p)).map(p => w.slice(0, -p.length)));
  base = base.concat(base.filter(x => x.length > 3 && x.endsWith('जी')).map(x => x.slice(0, -2)));   // विभीषणजीने → विभीषण
  return base.flatMap(x => [x, x.replace(/ियों$/, 'ि'), x.replace(/ियों$/, 'ी'), x.replace(/ियाँ$/, 'ी'), x.replace(/ियाँ$/, 'ि'), x.replace(/एँ$/, ''), x.replace(/ओं$/, ''), x.replace(/ों$/, ''), x.replace(/ों$/, 'ा'), x.replace(/ें$/, ''), x.replace(/ें$/, 'ा'), x.replace(/े$/, 'ा')]);
}
function hardKey(w, lang){ const Ds = [WG[lang], GL[lang]].filter(Boolean); for (const k of hardForms(w, lang)) if (Ds.some(D => D[k] && D[k].hard)) return k; return null; }
function hardWords(html, lang){   // html is already escaped; only whole words outside the tags are wrapped
  const re = HARD_RE[lang]; if (!re || !(GL[lang] || WG[lang])) return html;
  return html.split(/(<[^>]*>|&[a-z#0-9]+;)/).map((s, k) => k % 2 ? s : s.replace(re, w => { const key = hardKey(w, lang); return key ? '<span class="mw" data-mw="' + esc(key) + '" data-ml="' + lang + '">' + w + '</span>' : w; })).join('');
}
function wordList(lines){ const seen = new Set(), out = []; lines.forEach(l => l.split(/\s+/).forEach(t => { const w = cleanWord(t); if (w && !seen.has(w)){ seen.add(w); out.push(w); } })); return out; }
function wbHTML(lines, lang){
  return '<div class="wb">' + wordList(lines).map(w => { const g = lookup(w, lang); if (!g || g.none) return ''; const m = (g.pa && layerOn('pa') ? '<span class="gur">' + esc(g.pa) + '</span> · ' : '') + esc(g.hi || '') + (g.en ? ' <span class="en">· ' + esc(g.en) + '</span>' : '') + (g.possible ? ' <span class="q">(' + esc(g.possible) + ')</span>' : ''); return '<span class="ww w" data-w="' + esc(w) + '">' + esc(w) + '</span><span class="wm">' + m + '</span>'; }).join('') + '</div>';
}
function wordSheet(raw, alt, lang){
  const w = cleanWord(raw); if (!w) return; const g = (alt && alt[w]) || lookup(raw, lang);
  let h = '<h2>' + esc(w) + '</h2>';
  if (g && !g.none && g.lang && LANGS[g.lang]) h += '<p class="small muted">' + esc(TT(LANGS[g.lang].name)) + '</p>';
  if (g && !g.none){
    if (g.possible) h += '<p class="small muted">' + T('मूल शब्द: ', 'Root: ') + '<b>' + esc(g.possible) + '</b></p>';
    h += '<dl class="kv">' + (g.r && g.r !== w ? '<dt>' + T('मूल', 'Root') + '</dt><dd>' + esc(g.r) + '</dd>' : '') + (g.pa ? '<dt>' + T('पंजाबी', 'Punjabi') + '</dt><dd class="gur">' + esc(g.pa) + '</dd>' : '') + '<dt>' + T('हिंदी', 'Hindi') + '</dt><dd>' + esc(g.hi || '—') + '</dd><dt>English</dt><dd class="lat">' + esc(g.en || '—') + '</dd>' + (g.g ? '<dt>' + T('व्याकरण', 'Grammar') + '</dt><dd>' + esc(g.g) + '</dd>' : '') + (g.p && g.p.length ? '<dt>' + T('शब्द-खण्ड', 'Parts') + '</dt><dd>' + g.p.map(x => '<b>' + esc(x[0]) + '</b> (' + esc(x[1]) + ')').join(' + ') + '</dd>' : '') + '</dl>';
  }
  h += '<div class="acts"><button class="btn small ghost" id="gEdit">' + (g && !g.none ? T('अर्थ बदलें / जोड़ें', 'Edit meaning') : T('अर्थ जोड़ें', 'Add meaning')) + '</button></div>';
  openSheet(h); $('#gEdit').onclick = () => glossEdit(w, lang || W.lang);
}
function glossEdit(w, lang){
  const me = ME(), key = lang + ':' + w, cur = me.gloss[key] || {}, base = dictEntry(lang, w) || {};
  openSheet('<h2>' + T('शब्दार्थ: ', 'Meaning: ') + esc(w) + '</h2><div class="field"><label>' + LB.h() + '</label><input id="gh" value="' + esc(cur.hi || base.hi || '') + '"></div><div class="field"><label>' + LB.e() + '</label><input id="ge" class="lat" value="' + esc(cur.en || base.en || '') + '"></div><p class="small muted">' + T('यह आपकी फ़ाइलमें “' + esc(me.name) + '” के नामसे सेव होगा।', 'Saved in your file as “' + esc(me.name) + '”.') + '</p><div class="acts"><button class="btn" id="gSave">' + T('सेव करें', 'Save') + '</button>' + (me.gloss[key] ? '<button class="btn ghost" id="gDel">' + T('मेरा अर्थ हटाएँ', 'Remove my meaning') + '</button>' : '') + '</div>');
  $('#gSave').onclick = () => { me.gloss[key] = {hi: $('#gh').value.trim(), en: $('#ge').value.trim()}; save(); closeSheet(); toast(T('शब्दार्थ सेव हुआ', 'Meaning saved')); refreshReader(); };
  if ($('#gDel')) $('#gDel').onclick = () => { delete me.gloss[key]; save(); closeSheet(); refreshReader(); };
}

/* ---------------- work structure ---------------- */
let PAGES = [], itemPage = null, PARTS = [], TOPICS = [], topicAt = new Map(), PLANS = [], PLAN = {}, pauseAfter = {};
function buildWork(){
  applyTypes();
  IT = W.items; ID = {}; IT.forEach((x, i) => ID[x.id] = i);
  PAGES = []; itemPage = new Int32Array(IT.length); let cur = null;
  IT.forEach((it, i) => { if (!cur || cur.k !== it.p || cur.s !== it.s){ cur = {k: it.p, s: it.s, from: i, to: i}; PAGES.push(cur); } cur.to = i; itemPage[i] = PAGES.length - 1; });
  PARTS = W.parts.list.map((p, k) => { let a = -1, b = -1; IT.forEach((x, i) => { if (x.p === k){ if (a < 0) a = i; b = i; } }); return Object.assign({k, a, b}, p); });
  TOPICS = (W.topics || []).map(t => Object.assign({}, t, {i: ID[t.id]})).filter(t => t.i != null).sort((x, y) => x.i - y.i);
  TOPICS.forEach((t, n) => { const nx = TOPICS[n + 1]; const pe = PARTS[IT[t.i].p].b; t.end = nx && nx.i - 1 <= pe ? nx.i - 1 : pe; });
  topicAt = new Map(TOPICS.map(t => [t.i, t]));
  PLANS = (W.plans || []).map(p => Object.assign({}, p, {ends: p.end.map(id => ID[id])}));
  PLAN = {}; PLANS.forEach(p => PLAN[p.id] = p);
  pauseAfter = {}; PLANS.forEach(p => p.ends.forEach((e, n) => (pauseAfter[e] = pauseAfter[e] || []).push([p.id, n + 1])));
}
function topicOf(i){ let lo = 0, hi = TOPICS.length - 1, r = null; while (lo <= hi){ const m = (lo + hi) >> 1; if (TOPICS[m].i <= i){ r = TOPICS[m]; lo = m + 1; } else hi = m - 1; } return r && IT[r.i].p === IT[i].p ? r : null; }
function dayRange(plan, n){ const P = PLAN[plan]; return [n === 1 ? 0 : P.ends[n - 2] + 1, P.ends[n - 1]]; }
function dayOf(plan, i){ const P = PLAN[plan]; for (let n = 1; n <= P.n; n++){ if (i <= P.ends[n - 1]) return n; } return P.n; }
const KNAME = k => TT(W.parts.list[k]);
const TNAME = t => T(t.hi, t.en || t.hi);
const VN = n => T(ORDH[n] + ' विश्राम', 'Vishram ' + n);
const PNAME = id => TT(PLAN[id].long);

/* ---------------- labels ---------------- */
function vNum(n){ return n && !/^u/.test(n) ? DEV(n) : ''; }
function vLabel(it){ const n = vNum(it.n); return TYPE[it.y] + (n ? ' ' + n : ''); }
const isNum = s => /^[1-9]\d*$/.test(s);
// a work may name its sections (work.json → "sections": {section id: {hi, en}}, e.g. bala.1 → सर्ग १ / Sarga 1)
const SECN = s => W && W.sections && W.sections[s] ? TT(W.sections[s]) : '';
const hasSec = p => isNum(p.s) || !!SECN(p.s);
// two section labels as one range: the same words before a number are written once (Sarga 1–3, सर्ग १–३)
function secSpan(la, lb){ if (la === lb) return la; const x = /^(.*?)([0-9०-९੦-੯]+)$/.exec(la), y = /^(.*?)([0-9०-९੦-੯]+)$/.exec(lb); return x && y && x[1] === y[1] ? la + '–' + y[2] : la + ' – ' + lb; }
function secLabel(p){ if (SECN(p.s)) return SECN(p.s); if (isNum(p.s)) return T('दोहा ', 'Doha ') + DEV(p.s); const a = IT[p.from], z = IT[p.to]; if (a.y === z.y && vNum(a.n) && vNum(z.n)) return TYPE[a.y] + ' ' + vNum(a.n) + (z.n !== a.n ? '–' + vNum(z.n) : ''); return vLabel(a) === vLabel(z) ? vLabel(a) : vLabel(a) + ' – ' + vLabel(z); }
function posLabel(i){ const it = IT[i], p = PAGES[itemPage[i]]; if (SECN(p.s)) return secLabel(p) + ' · ' + vLabel(it); if (!isNum(p.s) || it.y === 'do' || it.y === 'so') return vLabel(it); return secLabel(p) + ' · ' + vLabel(it); }
function itemLabel(i){ return KNAME(IT[i].p) + ' · ' + posLabel(i); }
function spanLabel(a, b){
  const pa = PAGES[itemPage[a]], pb = PAGES[itemPage[b]];
  if (SECN(pa.s) && SECN(pb.s)) return secSpan(secLabel(pa), secLabel(pb));
  if (isNum(pa.s) && isNum(pb.s)) return T('दोहा ', 'Doha ') + DEV(pa.s) + (pb.s !== pa.s ? '–' + DEV(pb.s) : '');
  const la = hasSec(pa) ? secLabel(pa) : vLabel(IT[a]), lb = hasSec(pb) ? secLabel(pb) : vLabel(IT[b]);
  if (la === lb) return la;
  if (IT[a].y === IT[b].y && !hasSec(pa) && !hasSec(pb) && vNum(IT[a].n) && vNum(IT[b].n)) return TYPE[IT[a].y] + ' ' + vNum(IT[a].n) + '–' + vNum(IT[b].n);
  return la + ' – ' + lb;
}
function rangeDesc(a, b){ const ka = KNAME(IT[a].p), kb = KNAME(IT[b].p); if (ka === kb) return esc(ka + ': ' + spanLabel(a, b)); let h = '', p = IT[a].p; while (p <= IT[b].p){ const x = Math.max(a, PARTS[p].a), y = Math.min(b, PARTS[p].b); h += (h ? '<br>' : '') + esc(KNAME(p) + ': ' + spanLabel(x, y)); p++; } return h; }

/* ---------------- sources: meanings and audio ---------------- */
function srcList(kind){ return ((W.sources || {})[kind] || []).filter(s => !s.draft || S.timing.on); }   // a draft recording is heard only while reviewing timings
function srcChoice(kind){ const list = srcList(kind); const sel = ((S.src[W.id] || {})[kind]); if (sel === 'off') return null; return (list.find(s => s.id === sel) || list[0] || null); }
// only: 'au' the recording alone (all the work's page needs), 'meanings' the meaning sources alone; nothing: both. The
// sources are fetched together, not one after another; ALT keeps each kind's sources in their listed order.
async function loadSources(only){
  if (!Object.keys(LANGS).length) LANGS = await getJSON('glossary/languages');   // the meaning languages are listed there
  // a work loaded by part starts each meaning source empty; loadPart fills in each part it opens
  const get = async c => BYPART() ? {meta: c, id: c.id, title: c.title, m: {}, p: {}, got: new Set()} : Object.assign({meta: c}, await getJSON(W.path + '/' + c.file));
  if (only !== 'meanings'){ const c = srcChoice('au'); SRC.au = null; if (c){ try { SRC.au = Object.assign({meta: c}, await getJSON(W.path + '/' + c.file)); } catch (e) {} } buildAudio(); }
  if (only === 'au') return;
  await Promise.all(MK().map(async kind => { const c = srcChoice(kind); SRC[kind] = null; if (c){ try { SRC[kind] = await get(c); } catch (e) {} } }));
  // the other meaning sources of a kind fill in verses the chosen one doesn't cover (e.g. a stotra appended to a kāṇḍa)
  await Promise.all(MK().map(async kind => { const c = SRC[kind] && SRC[kind].meta;
    const got = await Promise.all(((W.sources || {})[kind] || []).filter(s => c && s.id !== c.id).map(s => get(s).catch(() => null)));
    ALT[kind] = got.filter(Boolean); }));
  for (let n = 0; n < 2 && BYPART(); n++) await Promise.all([...PWANT].map(loadPart));   // the parts already open, from the sources now chosen
  syncLayers();
}
/* A big work is loaded by part (work.json "load": "parts"): each meaning source is meanings/<source>/<part>.json and its own
   word senses glossary/<part>.json. A part is fetched when a verse of it is shown (pageHTML) or touched (a word, ⋮, copy,
   a correction), and kept in memory; search fetches every part, one at a time. The service worker keeps each part fetched,
   so a part opened once is readable offline. Other works load whole, as before. */
const BYPART = () => !!W && W.load === 'parts';
let PWANT = new Set(), PLOAD = {}, WGOT = new Set(), SLOADING = false, SFAIL = 0;   // the parts opened in this work; the loads under way; the parts of WG in
function partReset(){ PWANT = new Set(); PLOAD = {}; WGOT = new Set(); }
function partObjs(){ return MK().flatMap(k => [SRC[k]].concat(ALT[k] || [])).filter(Boolean); }
function partReady(k){ return !BYPART() || k == null || (partObjs().every(o => !o.got || o.got.has(k)) && (!W.glossary || WGOT.has(k))); }
// resolves true when something new came in (then the page is drawn again); false when nothing was needed or nothing could be fetched
function loadPart(k){
  if (partReady(k)) return Promise.resolve(false);
  if (PLOAD[k]) return PLOAD[k];
  const w = W, objs = partObjs().filter(o => o.got && !o.got.has(k)), gl = W.glossary && !WGOT.has(k), get = f => getJSON(W.path + '/' + f).catch(() => null);
  return PLOAD[k] = Promise.all([Promise.all(objs.map(o => get(o.meta.file + '/' + k))), gl ? get('glossary/' + k) : null]).then(([ms, g]) => {
    if (W !== w) return false; delete PLOAD[k]; let got = false;
    objs.forEach((o, n) => { const x = ms[n]; if (!x) return; Object.assign(o.m, x.m || {}); if (x.p) Object.assign(o.p, x.p); o.got.add(k); got = true; });
    if (g){ for (const lg in g) WG[lg] = Object.assign({}, WG[lg] || {}, g[lg]); WGOT.add(k); got = true; }   // a new object: its fold index is made again
    if (got){ PWANT.add(k); IDX = null; }
    return got;
  });
}
// a page drawn before its part is in shows the verses at once; the meanings and word meanings follow, without moving the page
function needPart(k){ if (!partReady(k)) loadPart(k).then(got => { if (got && CURVIEW === 'reader') refreshReader(); }); }
// search: every part's meanings, one part at a time; the verses (work.json) are searched at once, the meanings as each part comes
async function searchParts(){
  if (!BYPART() || SLOADING || Date.now() - SFAIL < 30000) return; SLOADING = true; const w = W;   // after a part could not be fetched (offline), tried again 30 s later
  let left = false;
  try { for (const P of PARTS){ if (W !== w || CURVIEW !== 'search' || SCOPE === 'lib'){ left = true; break; } if (await loadPart(P.k) && W === w && CURVIEW === 'search' && SCOPE !== 'lib') runSearch(); } }
  finally { SLOADING = false; }
  if (W !== w) return; if (!left && PARTS.some(P => !partReady(P.k))) SFAIL = Date.now();
  if (CURVIEW === 'search' && SCOPE !== 'lib' && $('#sRes .sload')) runSearch();   // the note goes: every part is searched, or what could be fetched
}
function verseOf(i){ const id = IT[i].id; for (const p of S.profiles){ const f = p.fix[KEY(id)]; if (f && f.v) return {v: f.v, edited: true}; } return {v: IT[i].v, edited: false}; }
function mean(kind, i){
  const src = SRC[kind]; if (!src) return null; const id = IT[i].id; const k = KEY(src.id + ':' + id);
  for (const p of S.profiles){ const f = p.fix[k]; if (f && f.m != null) return {x: f.m, edited: true, f: (src.m[id] || [])[1]}; }
  // p: the meaning line by line, one piece per verse line (meaning file "p")
  const e = src.m[id]; if (e) return {x: e[0], f: e[1], edited: false, p: (src.p || {})[id]};
  for (const a of ALT[kind] || []){ const x = a.m[id]; if (x) return {x: x[0], f: x[1], edited: false, from: TT(a.meta.title), p: (a.p || {})[id]}; }
  return null;
}
const layerOn = l => !!S.settings.layers[l];
const shownKinds = () => capKinds().filter(k => layerOn(LK(k)));   // the meaning layers on, in the capsule's order

/* ---------------- reader: continuous scroll over a kāṇḍa or a day's pāṭh ---------------- */
let R = {org: 'k', a: 0, b: 0, n: 0, pf: -1, pt: -1};
const VSHORT = {cau: ['चौ॰', 'Chau.'], do: ['दो॰', 'Do.'], so: ['सो॰', 'So.'], cha: ['छं॰', 'Cha.'], shloka: ['श्लो॰', 'Shl.']};
// A work may name its own verse types (work.json → "types": {type: {name, short}}); they add to or replace the built-in ones while it is open.
const TYPES0 = [[TYPEN, Object.assign({}, TYPEN)], [VSHORT, Object.assign({}, VSHORT)]];
function applyTypes(){
  TYPES0.forEach(([o, b]) => { for (const k in o) delete o[k]; Object.assign(o, b); });
  for (const [k, t] of Object.entries(W.types || {})){
    const nm = t.name || {hi: k, en: k};
    TYPEN[k] = [nm.hi, nm.en];
    if (t.short) VSHORT[k] = [t.short.hi, t.short.en];
  }
}
function verseHTML(i){
  const it = IT[i], id = it.id, me = ME(), vv = verseOf(i);
  const bm = SHOWN().some(p => p.bm[KEY(id)]);
  const sh = VSHORT[it.y];
  const vcls = '<div class="vtext' + (VEDIC.test(vv.v.join('')) ? ' vedic' : '') + '">';
  const pl = vv.v.map((l, y) => {
    const last = y === vv.v.length - 1;
    let ln = last && (it.y === 'cau' || it.y === 'cha') && it.n && /॥\s*$/.test(l) && !/॥[^॥]+॥\s*$/.test(l) ? l.replace(/\s*॥\s*$/, ' ॥' + it.n + '॥') : l;
    const w = wordsHTML(ln).replace(/॥\s*([0-9०-९੦-੯][^\s॥<]*)\s*॥/, '<span style="white-space:nowrap">॥$1॥</span>');
    // corners, each inside the gutter so they never touch the text: ▶ (top left, on the line of the bookmark),
    // bookmark (top right), ⋮ (bottom right). A one-line verse is given a second line's height so the corners stay apart.
    const top = y === 0 ? (hasAu(i) ? '<button class="vb vplay" data-a="play" aria-label="play"><svg><use href="#i-play"/></svg>' + (SRC.au && flagsNow()[id] && !(S.timing.flagsOn && !S.timing.on) ? REVB : '') + '</button>' : '') + '<button class="vb vbm' + (bm ? ' bm-on' : '') + '" data-a="bm" aria-label="bookmark"><svg><use href="#i-bm"/></svg></button>' : '';
    const undo = last && S.timing.on && SRC.au && myStarts()[id] ? '<span class="vundo"><button class="vb" data-a="tundo" aria-label="' + T('पहले जैसा', 'Undo') + '" title="' + T('पहले जैसा', 'Undo') + '"><svg><use href="#i-undo"/></svg></button></span>' : '';   // ↶ (bottom left) in timing mode, on a verse you set
    // ⚑ (bottom left) for the reader who turned on "Review timing" (☰ › More settings › Audio timing), outside timing
    // mode (where ↶ has that corner): shown while playing on the verse being recited and the verses just before and after it
    // (the light may already have moved on), and always once marked "Review audio timing" (filled blue; ▶ then needs no dot)
    const flagOn = S.timing.flagsOn && !S.timing.on, flag = last && flagOn && hasAu(i) ? '<span class="vflag"><button class="vb' + (SRC.au && flagsNow()[id] ? ' on' : '') + '" data-a="tflag" aria-label="' + T('ऑडियोका समय जाँचें', 'Review audio timing') + '"><svg><use href="#i-flag"/></svg></button></span>' : '';
    const tail = last ? '<span class="vend"><button class="vb" data-a="menu" aria-label="more"><svg><use href="#i-more"/></svg></button></span>' + undo + flag : '';
    return '<p' + (vv.v.length === 1 ? ' class="one"' : '') + '>' + top + w + tail + '</p>'; });
  let h = '<div class="verse' + (toCheck(i) ? ' tocheck' : '') + '" id="v' + i + '" data-i="' + i + '">';
  const trl = l => '<div>' + l.split(/(?<=,)\s+/).map(x => '<span class="half">' + esc(x).replace(/\s*॥\s*([^॥]*?)\s*॥((?:[^॥\s]+॥)*)/g, ' <span class="dd">॥$1॥$2</span>') + '</span>').join(' ') + '</div>';
  const num = x => esc(x).replace(/\s*(॥[^॥]*॥)\s*$/, '<span style="white-space:nowrap"> $1</span>');
  // one meaning layer: Hindi and Punjabi keep the verse number on its line; English only when line by line
  const lay = (kind, m, x, fn) => '<div class="layer ' + LCLS(kind) + '">' + hardWords(kind !== 'en' || m.p ? num(x) : esc(x), kind) + (m.edited ? '<span class="tag">' + (kind === 'en' ? 'edited' : T('संशोधित', 'edited')) + '</span>' : '') + (fn && m.f ? '<div class="fn">' + m.f.map(esc).join('<br>') + '</div>' : '') + '</div>';
  const ks = shownKinds(), MS = {}; ks.forEach(k => { const m = mean(k, i); if (m) MS[k] = m; });
  const on = ks.filter(k => MS[k]);
  // line by line (☰ › More settings › "Meaning per line", off by default): a source that gives one piece per verse line
  // shows each piece under its line; otherwise, and for a source without pieces (or a reader's own correction of the verse or
  // the meaning), the meaning is shown whole after the verse
  const lines = m => S.settings.lines && m && !m.edited && !vv.edited && Array.isArray(m.p) && m.p.length === vv.v.length ? m.p : null;
  const PS = {}; on.forEach(k => { PS[k] = lines(MS[k]); });
  const trOk = S.settings.tr && it.t && it.t.length === vv.v.length;
  // whole meanings: English after the word meanings, the others before them (as with हिं · En)
  const whole = (late) => on.filter(k => !PS[k] && (k === 'en') === late).map(k => lay(k, Object.assign({}, MS[k], {p: null}), MS[k].x, true)).join('');
  if (on.some(k => PS[k])){
    const lastOf = ps => ps ? ps.map(x => !!x.trim()).lastIndexOf(true) : -1, LAST = {}; on.forEach(k => { LAST[k] = lastOf(PS[k]); });
    pl.forEach((p, y) => {
      h += vcls.replace('vtext', 'vtext vline') + p + '</div>';
      if (trOk) h += '<div class="tr">' + trl(it.t[y]) + '</div>';
      on.forEach(k => { if (PS[k] && PS[k][y].trim()) h += lay(k, MS[k], PS[k][y], y === LAST[k]); });
    });
    if (S.timing.on && SRC.au) h += markBar(i);
    if (S.settings.tr && it.t && it.t.length && !trOk) h += '<div class="tr">' + it.t.map(trl).join('') + '</div>';
  } else {
    h += vcls + pl.join('') + '</div>';
    if (S.timing.on && SRC.au) h += markBar(i);
    if (S.settings.tr && it.t && it.t.length) h += '<div class="tr">' + it.t.map(trl).join('') + '</div>';
  }
  h += whole(false);
  if (layerOn('w')) h += '<div class="layer wl">' + wbHTML(vv.v, langOf(i)) + '</div>';
  h += whole(true);
  for (const p of SHOWN()) (p.notes[KEY(id)] || []).forEach((n, k) => { h += '<div class="note"><div class="who">' + new Date(n.ts).toLocaleDateString(LANG() === 'en' ? 'en-IN' : 'hi-IN') + (p.id === me.id ? '<button data-a="enote" data-k="' + k + '">' + T('बदलें', 'Edit') + '</button>' : '') + '</div>' + esc(n.t).replace(/\n/g, '<br>') + '</div>'; });
  return h + '</div>';
}
function pauseHTML(i){
  const list = pauseAfter[i]; if (!list) return '';
  return list.filter(([o]) => R.org === 'k' || R.org === o).map(([o, n]) => { const done = DONE(ME(), o)[n]; return '<div class="pause" data-pause="' + o + n + '"><b>' + PNAME(o) + ' · ' + VN(n) + '</b><div class="sub">' + T('यहाँ विश्राम करें', 'A place to pause the reading') + '</div><button class="btn small' + (done ? ' ghost' : '') + '" data-a="done" data-o="' + o + '" data-n="' + n + '" data-i="' + i + '">' + (done ? T('✓ पूर्ण — बदलें', '✓ Completed — undo') : T('विश्राम पूर्ण करें', 'Mark vishram complete')) + '</button></div>'; }).join('');
}
// the verse type as a heading above the verse, “॥ चौपाई ॥”, shown only where the type changes:
// before the first chaupāī of a run, then before the dohā that follows, and so on — and at the start of what is read
function typeHead(i){
  const y = IT[i].y, nm = TYPEN[y]; if (!nm) return '';
  if (i !== R.a && i > 0 && IT[i - 1].y === y && IT[i - 1].p === IT[i].p) return '';
  return '<div class="vtype">॥ ' + esc(T(nm[0], nm[1])) + ' ॥</div>';
}
function pageHTML(pg){
  const p = PAGES[pg], a = Math.max(p.from, R.a), b = Math.min(p.to, R.b); let h = '<div class="pg" data-pg="' + pg + '">';
  needPart(p.k);   // a work loaded by part: this page's part (a page never spans two)
  for (let i = a; i <= b; i++){
    if (i === PARTS[IT[i].p].a) h += '<div class="part-h"><b>' + esc(KNAME(IT[i].p)) + '</b></div>';
    const t = topicAt.get(i); if (t) h += '<div class="topic-h" id="t' + i + '"><b>' + esc(TNAME(t)) + '</b></div>';
    h += typeHead(i) + verseHTML(i) + pauseHTML(i);
  }
  return h + '</div>';
}
function rangeFor(org, i){ if (org === 'k'){ const P = PARTS[IT[i].p]; return [P.a, P.b, P.k]; } const n = dayOf(org, i); const [a, b] = dayRange(org, n); return [a, b, n]; }
const canNext = () => R.pt + 1 < PAGES.length && PAGES[R.pt + 1].from <= R.b;
const canPrev = () => R.pf - 1 >= 0 && PAGES[R.pf - 1].to >= R.a;
function endHTML(){
  if (canNext()) return '';
  let h = '<div class="endb">';
  if (R.b === IT.length - 1) h += '<div class="colo">' + esc(TT(W.colophon) || '') + '</div>';
  if (R.org === 'k'){ const nx = PARTS[R.n + 1]; if (nx) h += '<button class="btn" data-next="' + nx.a + '">' + esc(KNAME(nx.k)) + ' ›</button>'; }
  else { const P = PLAN[R.org]; if (R.n < P.n){ const [na, nb] = dayRange(R.org, R.n + 1), d = durLabel(spanSecs(na, nb)); h += '<button class="btn" data-next="' + na + '">' + VN(R.n + 1) + ' ›</button>' + (d ? '<div class="ndur">▶ ' + d + '</div>' : ''); } }   // the next vishram, and how long it plays
  return h + '</div>';
}
function renderAround(i, focus){
  const pg = itemPage[i]; R.pf = R.pt = pg;
  $('#rBody').innerHTML = '<div id="topS"></div><div id="pages">' + pageHTML(pg) + '</div><div id="botS"></div><div id="endB">' + endHTML() + '</div>';
  fill();
  if (focus !== false) scrollToItem(i, false);
  updateHeader();
}
function fill(){ let n = 0; while (canNext() && document.body.scrollHeight < scrollY + innerHeight * 3 && n++ < 6) appendNext(); }
function appendNext(){ if (!canNext()) return; R.pt++; $('#pages').insertAdjacentHTML('beforeend', pageHTML(R.pt)); $('#endB').innerHTML = endHTML(); }
function prependPrev(){ if (!canPrev()) return; const h0 = document.body.scrollHeight, y0 = scrollY; R.pf--; $('#pages').insertAdjacentHTML('afterbegin', pageHTML(R.pf)); window.scrollTo(0, y0 + document.body.scrollHeight - h0); }
function ensure(){
  if (!$('#reader').classList.contains('on')) return; const b = $('#botS'), t = $('#topS'); let n = 0;
  while (b && canNext() && b.getBoundingClientRect().top < innerHeight + 1800 && n++ < 4) appendNext();
  n = 0; while (t && canPrev() && scrollY > 0 && t.getBoundingClientRect().bottom > -1200 && n++ < 3) prependPrev();
}
const IO = new IntersectionObserver(es => { if (es.some(e => e.isIntersecting)) ensure(); }, {rootMargin: '1500px 0px'});
const MO = new MutationObserver(() => { const t = $('#topS'), b = $('#botS'); if (t && !t.dataset.o){ t.dataset.o = 1; IO.observe(t); } if (b && !b.dataset.o){ b.dataset.o = 1; IO.observe(b); } });
MO.observe($('#rBody'), {childList: true});
function scrollToItem(i, smooth){
  const t = topicAt.get(i); let el = (t && document.getElementById('t' + i)) || document.getElementById('v' + i);
  if (!el) return;
  // the headings just above it (the part, the topic, ॥ चौपाई ॥) come with it, just below the top bar
  while (el.previousElementSibling && el.previousElementSibling.matches('.part-h, .topic-h, .vtype')) el = el.previousElementSibling;
  const y = el.getBoundingClientRect().top + scrollY - $('#reader .bar').getBoundingClientRect().bottom - 6; window.scrollTo({top: Math.max(0, y), behavior: smooth ? 'smooth' : 'auto'});
}
function topVisibleItem(){
  for (const y of [96, 140, 200, 280]){ const el = document.elementFromPoint(innerWidth / 2, y); const v = el && el.closest && el.closest('.verse'); if (v) return +v.dataset.i; const nxt = el && el.closest && (el.closest('.topic-h, .part-h, .pause')); if (nxt){ let s = nxt.nextElementSibling; while (s && !s.classList.contains('verse')) s = s.nextElementSibling; if (s) return +s.dataset.i; } }
  const vs = $$('#rBody .verse'); for (const v of vs){ if (v.getBoundingClientRect().bottom > 80) return +v.dataset.i; } return R.a;
}
function curSection(i){ const t = topicOf(i); return t && t.i <= R.b && t.end >= R.a ? t : null; }
function updateHeader(){
  if (!IT.length) return; const i = topVisibleItem(), t = topicOf(i);
  const s = curSection(i), where = R.org === 'k' ? (PARTS.length > 1 ? KNAME(R.n) : '') : VN(R.n), topic = s ? TNAME(s) : '';
  $('#rMid').innerHTML = '<span class="ml">' + (s ? spanLabel(Math.max(s.i, R.a), Math.min(s.end, R.b)) : spanLabel(R.a, R.b)) + ' ▾</span><small>' + esc(where || TT(W.title)) + '</small>';   // only the part (or reading day): a small footer; the topic heads the page
}
let scT;
window.addEventListener('scroll', () => { if (!$('#reader').classList.contains('on')) return; ensure(); clearTimeout(scT); scT = setTimeout(() => { updateHeader(); savePos(); }, 200); }, {passive: true});
function savePos(i){ if (i == null) i = topVisibleItem(); const ws = WS(); ws.pos[R.org] = i; ws.last = {org: R.org, i, id: IT[i].id}; save();
  R.at = {org: R.org, id: IT[i].id}; if (CURVIEW === 'reader' && history.state && history.state.v === 'reader') history.replaceState(snap('reader'), ''); }   // Back and a refresh return here
/* ---------------- the reading anchor: Resume and “Back to” ----------------
   Where you were reading, not merely where the screen is. Each second while the reader is open and seen, the verse at the top
   of the screen is looked at. Calm movement (under half a screen in a second) is reading: after 3 calm seconds the anchor
   follows the top verse. A big move (more than 1.5 screens in a second, a fling) or a navigation (another section or day,
   search, a bookmark, the plan switch, Back) is a jump: the anchor stays where the reading was, and the new place is only a
   candidate. It becomes the anchor once it is read there: 20 calm seconds with two verses read forward, or 45 calm seconds
   (a page that fits on the screen), or as soon as a recording plays there: pressing play is reading, and while it plays the
   verse being recited is the anchor. Resume (on the work's page) goes to it; in the reader, “Back to …” (laid out like the
   recording's “Go to …”) shows when it is off the screen, was read in the last 15 minutes, no recording plays and Audio
   timing is off (marking timings jumps about by design). ws.anchor = {org, id, t}; ws.prev: anchors left for a new place, latest first, three kept. */
const AN = {cand: null, calm: 0, lastY: 0, going: false, playT0: 0, manual: false};
function anchorOf(){ const a = W && WS().anchor; return a && ID[a.id] != null && (a.org === 'k' || PLAN[a.org]) ? Object.assign({}, a, {i: ID[a.id]}) : null; }
function setAnchor(org, i, moved){
  const ws = WS(), a = ws.anchor; if (!IT[i]) return;
  if (a && a.id === IT[i].id && a.org === org){ a.t = Date.now(); return; }
  if (moved && a && a.id) ws.prev = [a].concat((ws.prev || []).filter(p => p.id !== a.id && p.id !== IT[i].id)).slice(0, 3);   // the place left behind
  ws.anchor = {org, id: IT[i].id, t: Date.now()}; save();
}
// a navigation to verse i: the reading may be elsewhere, so the anchor waits (with no anchor yet, this is where reading starts)
function anchorJump(i){
  if (AN.going){ AN.going = false; AN.cand = null; AN.calm = 0; return; }   // going back to the anchor itself
  if (!anchorOf()){ setAnchor(R.org, i); return; }
  AN.cand = {calm: 0, fwd: 0, top: i}; AN.calm = 0; AN.lastY = scrollY;
}
function anchorTick(force){
  if (AN.manual && !force) return;
  if (!W || CURVIEW !== 'reader' || document.hidden || S.timing.on) return;
  const y = scrollY, dy = Math.abs(y - AN.lastY), top = topVisibleItem(); AN.lastY = y;
  if (PL.on && playing()){ backPill(); return; }   // a recording: setCur keeps the anchor
  if (dy > 1.5 * innerHeight){ anchorJump(top); backPill(); return; }   // a fling
  if (dy >= 0.5 * innerHeight){ AN.calm = 0; if (AN.cand){ AN.cand.calm = 0; AN.cand.top = top; } backPill(); return; }   // moving fast: looking, not reading
  AN.calm++;
  const c = AN.cand;
  if (c){ c.calm++; if (top > c.top) c.fwd += top - c.top; c.top = top;
    if ((c.calm >= 20 && c.fwd >= 2) || c.calm >= 45){ AN.cand = null; setAnchor(R.org, top, true); } }
  else if (AN.calm >= 3) setAnchor(R.org, top);
  backPill();
}
setInterval(anchorTick, 1000);
// the recording: the verse being recited is the anchor (not while marking timings)
function anchorPlay(i){ if (!W || !PL.on || S.timing.on) return; const org = CURVIEW === 'reader' ? R.org : ((WS().anchor || {}).org || 'k');
  const moved = !!AN.cand || !anchorOf() || Math.abs(anchorOf().i - i) > 3; AN.cand = null; setAnchor(org, i, moved); }
// “↩ Back to …”: in the reader, when the anchor is off the screen (and no recording plays: then ▸ jumps to the recited verse)
function backPill(){
  const b = $('#rAnchor'), a = anchorOf(); let show = false;
  if (a && CURVIEW === 'reader' && !(PL.on && playing()) && !S.timing.on && Date.now() - (a.t || 0) < 15 * 60e3){
    const el = document.getElementById('v' + a.i), r = el && el.getBoundingClientRect();
    show = !(r && r.bottom > 70 && r.top < innerHeight - 90);
  }
  if (show){ const where = a.org === 'k' ? (PARTS.length > 1 ? KNAME(IT[a.i].p) : '') : VN(rangeFor(a.org, a.i)[2]);
    const h = '<b><span class="arr">' + (a.i >= topVisibleItem() ? '↓' : '↑') + '</span>' + T('', 'Back to ') + esc(posLabel(a.i)) + T(' पर लौटें', '') + '</b>' + (where ? '<small>' + esc(where) + '</small>' : '');   // as “Go to …”: an arrow pointing the way, the place, the part or day
    if (b.innerHTML !== h) b.innerHTML = h;
    // above the reader's bottom bar (the sections) and the player, never over them
    const nb = $('#reader .navbar'), pl = $('#player'), tops = [innerHeight];
    if (nb && nb.offsetHeight) tops.push(nb.getBoundingClientRect().top); if (!pl.hidden) tops.push(pl.getBoundingClientRect().top);
    b.style.bottom = (innerHeight - Math.min(...tops) + 10) + 'px'; }
  b.hidden = !show;
}
function goAnchor(){ const a = anchorOf(); if (!a) return; AN.going = true; openReader(a.org, a.i, true); backPill(); }
$('#rAnchor').onclick = goAnchor;
// a verse opened from search or a bookmark opens in the reading plan chosen on the work's home, on the day that holds it
function readOrg(){ const o = homeOrg(); return o !== 'k' && PLAN[o] ? o : 'k'; }
// A place is found again by its item id. Places saved before ids were kept are item positions; when a work later had
// verses put before its text (work.json "prepended": how many), such a place moves forward by that many, once.
// work.json "renamed" (old item id → new): a joint caupāī split into one item each. A reader's notes,
// bookmarks and place on the old id move to its first part; a meaning correction moves to the last part (where the
// joint meaning is); timing marks to the first part. A verse-text correction of the old joint verse is left as it was.
function moveRenamed(){
  const ren = W.renamed; if (!ren) return; let changed = false;
  const lastOf = old => { const m = /^(.+\.cau)\d+-(\d+)$/.exec(old); return m && ID[m[1] + m[2]] != null ? m[1] + m[2] : ren[old]; };
  for (const p of S.profiles) for (const store of ['notes', 'bm', 'fix']){
    const o = p[store] || {};
    for (const k of Object.keys(o)){
      if (!k.startsWith(W.id + ':')) continue;
      const old = Object.keys(ren).find(x => k.endsWith(':' + x)); if (!old || ID[old] != null) continue;
      const isMeaning = store === 'fix' && k.split(':').length > 2;
      if (store === 'fix' && !isMeaning) continue;   // a correction of the joint verse's text: kept under the old id
      const nk = k.slice(0, k.length - old.length) + (isMeaning ? lastOf(old) : ren[old]);
      if (store === 'notes') o[nk] = (o[nk] || []).concat(o[k]); else if (!(nk in o)) o[nk] = o[k];
      delete o[k]; changed = true;
    }
  }
  for (const box of ['fix', 'from', 'sent']){ const T0 = (S.timing || {})[box] || {};
    for (const tk in T0){ if (!tk.startsWith(W.id + ':')) continue; const m = T0[tk];
      for (const old in ren) if (old in m && ID[old] == null){ if (!(ren[old] in m)) m[ren[old]] = m[old]; delete m[old]; changed = true; } } }
  const l = (S.w[W.id] || {}).last; if (l && l.id && ren[l.id] && ID[l.id] == null){ l.id = ren[l.id]; changed = true; }
  if (changed) save();
}
function fixLast(){
  const ws = S.w[W.id], l = ws && ws.last; if (!l) return;
  if (l.id != null){ if (ID[l.id] != null) l.i = ID[l.id]; else { ws.last = null; delete ws.pos[l.org]; }   // a place at a verse no longer in the text is dropped
    for (const o in ws.pos) if (!IT[ws.pos[o]]) delete ws.pos[o]; return; }
  const sh = i => (W.prepended || 0) + (W.split || []).reduce((n, [at, add]) => n + (at < i ? add : 0), 0);   // items added before it since then ("split": joint caupāīs made separate)
  l.i += sh(l.i);
  if (IT[l.i]) l.id = IT[l.i].id; else ws.last = null;
  for (const o in ws.pos) ws.pos[o] += sh(ws.pos[o]);
}
function openReader(org, i, flash){
  if (!wReady){ whenReady().then(() => openReader(org, i, flash)); return; }   // the meanings are still on their way (openWork)
  if (!S.hinted && !TOUR){ S.hinted = 1; save(); setTimeout(() => toast(T('किसी शब्दको छूकर अर्थ देखें · नीचेसे प्रसंग चुनें', 'Tap any word for its meaning · choose a section at the bottom')), 900); }
  R.org = org; [R.a, R.b, R.n] = rangeFor(org, i);
  if (!$('#reader').classList.contains('on')) show('reader');
  renderAround(i); if (flash){ const el = document.getElementById('v' + i); if (el) el.classList.add('flash'); }
  savePos(i); anchorJump(i); setTimeout(backPill, 80);
}
function reopenReader(){ fixLast(); const l = WS().last; if (l && IT[l.i]) openReader(l.org, l.i); else show('home', false); }
function jumpTo(i){
  if (i < R.a || i > R.b){ openReader(R.org, i); return; }
  const pg = itemPage[i];
  if (pg >= R.pf && pg <= R.pt) scrollToItem(i, false); else renderAround(i);
  setTimeout(() => { updateHeader(); savePos(i); anchorJump(i); backPill(); }, 60);
}
function refreshReader(){
  if (!$('#reader').classList.contains('on')) return;
  const i = topVisibleItem(), el = document.getElementById('v' + i), off = el ? el.getBoundingClientRect().top : 80;
  const pf = R.pf, pt = R.pt; let h = ''; for (let p = pf; p <= pt; p++) h += pageHTML(p);
  $('#pages').innerHTML = h; $('#endB').innerHTML = endHTML();
  const el2 = document.getElementById('v' + i); if (el2) window.scrollBy(0, el2.getBoundingClientRect().top - off);
  if (PL.on && PL.cur >= 0){ const c = document.getElementById('v' + PL.cur); if (c) c.classList.add('now'); }
  markNear();
  updateHeader();
}
function rerenderItem(i){ const el = document.getElementById('v' + i); if (!el) return; const tmp = document.createElement('div'); tmp.innerHTML = verseHTML(i); el.replaceWith(tmp.firstChild); if (PL.on && PL.cur === i) document.getElementById('v' + i).classList.add('now'); if (PL.on && Math.abs(PL.cur - i) === 1) document.getElementById('v' + i).classList.add('near'); }
// The section picker: the row of kāṇḍas (or plan days) on top only chooses which list shows below; nothing opens until a
// section is tapped — the current one too.
function sectionSheet(n){
  const ti = topVisibleItem(), cur = curSection(ti), plan = R.org !== 'k';
  if (n == null) n = R.n;
  const [A, B] = plan ? dayRange(R.org, n) : [PARTS[n].a, PARTS[n].b];
  let h = '';
  if (!plan) h += '<div class="pick">' + PARTS.map(p => '<button data-pick="' + p.k + '" class="' + (p.k === n ? 'on' : '') + '">' + esc(KNAME(p.k)) + '</button>').join('') + '</div>';
  else { const P = PLAN[R.org]; h += '<div class="pick days">' + Array.from({length: P.n}, (_, x) => x + 1).map(d => '<button data-pick="' + d + '" class="' + (d === n ? 'on' : '') + (DONE(ME(), R.org)[d] ? ' done' : '') + '">' + DEV(d) + '</button>').join('') + '</div>'; }
  let secs = TOPICS.filter(t => t.i <= B && t.end >= A);
  if (!secs.length && W.sections) secs = PAGES.filter(p => p.to >= A && p.from <= B && SECN(p.s)).map(p => ({i: p.from, end: p.to, hi: '', en: '', sec: true}));   // its named sections (Sarga 1 …)
  const rows = []; if (!secs.length || secs[0].i > A) rows.push({i: A, end: (secs[0] ? secs[0].i - 1 : B), name: plan ? VN(n) : KNAME(n)});
  secs.forEach(t => rows.push({i: Math.max(t.i, A), end: Math.min(t.end, B), name: TNAME(t), t}));
  h += '<h2>' + (plan ? PNAME(R.org) + ' · ' + VN(n) : esc(KNAME(n))) + '</h2><div class="secs">' + rows.map(r => '<button data-to="' + r.i + '" class="' + ((cur && r.t === cur || r.t && r.t.sec && ti >= r.i && ti <= r.end) && n === R.n ? 'on' : '') + '"><span class="sr">' + spanLabel(r.i, r.end) + '</span><span class="sn">' + esc(r.name) + '</span></button>').join('') + '</div>';
  if ($('#sheet').classList.contains('on') && $('#sheetBody .pick')){ $('#sheetBody').innerHTML = h; $('#sheet').scrollTop = 0; } else openSheet(h);
  $$('#sheetBody [data-pick]').forEach(b => b.onclick = () => sectionSheet(+b.dataset.pick));
  $$('#sheetBody [data-to]').forEach(b => b.onclick = () => { closeSheet(); jumpTo(+b.dataset.to); });
  const on = $('#sheetBody .secs .on'); if (on) setTimeout(() => on.scrollIntoView({block: 'center'}), 60);
}
$('#rMid').onclick = () => sectionSheet();   // without the click event, which sectionSheet would take as its section n
$('#rBack').onclick = back;
// the same हिं · En · शब्द switch in every header (library, work, reader): one setting, shown and changed anywhere
$$('.lyr.layers button').forEach(b => b.onclick = () => { if (b.dataset.l === 'r'){ toggleRecite(); return; }
  if (S.settings.recite){ S.settings.recite = false; delete S.settings.preRecite; applyRecite(); }   // a meaning turned on ends recitation mode: only that meaning shows
  const was = LANG(), l = b.dataset.l; S.settings.layers[l] = !S.settings.layers[l];
  // the meanings and the app's language are coupled: English meaning on → English; only Hindi → Hindi; neither → unchanged
  if (S.settings.layers.e) S.settings.ui = 'en'; else if (S.settings.layers.h) S.settings.ui = 'hi';
  save(); syncLayers(); if (LANG() !== was) applyLang();
  const v = CURVIEW; if (v === 'reader') refreshReader(); });
// हिं · En on the library and work pages sets the language and the meaning with it: Hindi → the Hindi meaning only, English → the English meaning only
$$('.lyr.uilang button').forEach(b => b.onclick = () => { if (S.settings.ui === b.dataset.u) return; S.settings.ui = b.dataset.u; S.settings.layers.h = b.dataset.u === 'hi'; S.settings.layers.e = b.dataset.u === 'en'; if (S.settings.recite){ S.settings.recite = false; delete S.settings.preRecite; applyRecite(); } save(); applyLang(); syncLayers(); onView(CURVIEW); });
function syncLayers(){
  // the capsule's first two places are the two meaning switches shown for this work (capKinds)
  const cb = $$('#rLayers button'); if (cb.length >= 2 && Object.keys(LANGS).length) capKinds().forEach((k, n) => { const b = cb[n], M = LANGS[k] && LANGS[k].meaning; b.dataset.l = LK(k); b.textContent = M ? M.short : k; b.classList.toggle('lat', k === 'en'); b.classList.toggle('gur', k === 'pa'); });
  $$('.lyr.layers button').forEach(b => b.classList.toggle('on', b.dataset.l === 'r' ? !!S.settings.recite : layerOn(b.dataset.l))); $$('.lyr.uilang button').forEach(b => b.classList.toggle('on', S.settings.ui === b.dataset.u)); }
// a whole new state (a file opened with "Replace everything", or the cloud's): theme, language, meanings and the page all follow it
function applyState(){ applyTheme(); applyLang(); applyRecite(); applyTiming(); if (CURVIEW === 'reader' && W) refreshReader(); else onView(CURVIEW); }
function applyRecite(){ document.body.classList.toggle('recite', !!S.settings.recite); $('#rRecite').hidden = true; syncLayers(); }
// recitation mode is the fourth button of the reader's हिं · En · शब्द · 📖 capsule: turning it on hides
// the meanings (the layers that were on are remembered); turning it off — or turning any meaning on — brings them back
function toggleRecite(){
  const on = !S.settings.recite; S.settings.recite = on;
  if (on){ S.settings.preRecite = Object.assign({}, S.settings.layers); for (const k in S.settings.layers) S.settings.layers[k] = false; }
  else if (S.settings.preRecite){ Object.assign(S.settings.layers, S.settings.preRecite); delete S.settings.preRecite; }
  save(); applyRecite(); applyLang(); if (CURVIEW === 'reader') refreshReader();
  toast(on ? T('पाठ मोड: केवल मूल पाठ', 'Recitation mode: verses only') : T('अर्थ फिर दिखेंगे', 'Meanings shown again'));
}
$('#rRecite').onclick = toggleRecite;
// One ☰ sheet on every page: Bookmarks & notes (inside a work), the dark theme, the tour, and "More" — a
// page with the rare things (transliteration, sources, audio timing, privacy). Nothing here repeats the header:
// the meanings, recitation mode, the text size and the language are the header's capsules; sections are the reader's
// footer; the playing speed is in the player.
function mainMenu(){
  const inWork = !!W && CURVIEW !== 'library', th = S.settings.theme;
  openSheet('<div class="menu">' + (inWork ? '<button data-m="bm"><svg><use href="#i-bm"/></svg>' + LB.bm() + '</button>' : '') +
    '<div class="menusw">' + sw('mth', T('गहरा रंग (रात)', 'Dark theme'), '', th === 'dark', 'theme') + '</div>' +
    (S.timing.on && inWork ? '<div class="menusw"><label class="sw tsw"><svg class="swic" style="stroke:var(--saffron)"><use href="#i-clock"/></svg><span style="flex:1">' + T('ऑडियोका समय', 'Audio timing') + '</span><span class="tg"><input type="checkbox" id="mtm" checked><span></span></span></label></div>' + (SRC.au && Object.keys(myStarts()).filter(id => ID[id] != null).length ? '<button data-m="tclear" class="tsaf"><svg><use href="#i-undo"/></svg>' + T('मेरे बदलाव हटाएँ', 'Clear adjustments') + '</button>' : '') : '') +
    '<button data-m="share"><svg><use href="#i-share"/></svg>' + T('ऐप साझा करें', 'Share the app') + '</button>' +
    '<button data-tour><svg><use href="#i-tour"/></svg>' + LB.tour() + '</button>' +
    '<button data-m="set"><svg><use href="#i-set"/></svg>' + LB.more() + '</button></div>');
  if ($('#mtm')) $('#mtm').onchange = async () => { S.timing.on = false; save(); applyTiming(); stopAudio(); closeSheet(); await loadSources(); if (CURVIEW === 'reader') refreshReader(); if (CURVIEW === 'settings') renderSettings(); toast(T('ऑडियोका समय: बंद', 'Audio timing: off')); };   // while on, ☰ turns it off
  $('#mth').onchange = e => { S.settings.theme = e.target.checked ? 'dark' : 'light'; applyTheme(); save(); };   // light or dark, nothing else
}
$('#rMore').onclick = mainMenu;
$('#sheetBody').addEventListener('click', ev => {
  const b = ev.target.closest('[data-m]'); if (!b) return;
  const m = b.dataset.m; closeSheet();
  if (m === 'bm') show('bookmarks'); if (m === 'set') show('settings'); if (m === 'tclear') clearTimingAsk(); if (m === 'share') shareApp();
});
// ☰ › Share the app: one short line and one link, <site>/get, which sends an Android phone to the store app
// (library/apps.json → "store") and anything else to the website; chat apps show the site's card under it (title, the
// library's contents, the picture app/share-card.png). Through the phone's share sheet, or copied where there is none
async function shareApp(){
  // ?app=<id> only for a store app other than the first (library/apps.json): with one app the link stays short
  const app = new URLSearchParams(location.search).get('app'); let first = '';
  try { first = Object.keys(await getJSON('apps')).find(k => !k.startsWith('_')) || ''; } catch (e) {}
  const link = location.origin + '/get' + (app && app !== first ? '?app=' + encodeURIComponent(app) : '');
  const text = T('शास्त्र — पढ़ें, अर्थ समझें और पाठ सुनें। निःशुल्क, बिना विज्ञापन।', 'Scriptures — read, understand and listen. Free, no ads.') + '\n' + link;   // the card under the link says what is inside
  try { if (navigator.share){ await navigator.share({title: T('शास्त्र', 'Scriptures'), text}); return; } } catch (e) { if (e && e.name === 'AbortError') return; }
  try { await navigator.clipboard.writeText(text); toast(T('लिंक कॉपी हो गया — अब कहीं भी चिपकाएँ', 'Copied — paste it anywhere')); } catch (e) { toast(link); }
}
function setSize(d){
  const i = topVisibleItem(); S.settings.size = Math.max(16, Math.min(34, S.settings.size + d)); applyTheme(); save();
  if ($('#reader').classList.contains('on') && i != null) scrollToItem(i);
  toast(LB.size() + ' ' + DEV(S.settings.size));
}
$$('.szm').forEach(b => b.onclick = () => setSize(-2)); $$('.szp').forEach(b => b.onclick = () => setSize(2));
$('#rBody').addEventListener('click', ev => {
  // a work loaded by part: a tap on a verse whose part is not in yet (a word, ⋮, copy, a correction) waits for it
  const v0 = ev.target.closest('.verse'), k0 = v0 ? IT[+v0.dataset.i].p : null;
  if (!partReady(k0)){ loadPart(k0).then(() => readerTap(ev)); return; }
  readerTap(ev);
});
function readerTap(ev){
  const nx = ev.target.closest('[data-next]'); if (nx){ openReader(R.org, +nx.dataset.next); return; }
  const mw = ev.target.closest('.mw'); if (mw){ mw.classList.add('sel'); wordSheet(mw.dataset.mw, null, mw.dataset.ml); return; }   // a hard word of a meaning
  const v = ev.target.closest('.verse'), i = v ? +v.dataset.i : null;
  const a = ev.target.closest('[data-a]');
  if (a){
    const act = a.dataset.a;
    if (act === 'play') playFrom(i, i);   // ▶ beside a verse plays that verse; “Listen from here” keeps going
    else if (act === 'tstart' || act === 'tend'){
      if (!PL.on || !ytOK){ toast(T('पहले ऑडियो चलाएँ — फिर जिस पदको सुन रहे हैं उसीके बटन दबाएँ', 'Start the audio first, then tap the buttons of the verse you are hearing')); return; }
      setTime(i, act === 'tstart' ? 1 : 2, nowAt()); if (act === 'tstart'){ flagDone(IT[i].id); save(); } rerenderItem(i);
    }
    else if (act === 'tn'){ const x = SRC.au.at[IT[i].id], k = +a.dataset.k; if (setTime(i, k, Math.max(0, x[k] + a.dataset.d * step())) === false) return; if (k === 1){ flagDone(IT[i].id); save(); } rerenderItem(i); if (!livePlay()) snippet(i, k); }
    else if (act === 'tflag') toggleFlag(i);
    else if (act === 'tok'){ unfrom(IT[i].id); flagDone(IT[i].id); save(); rerenderItem(i); toast(T('जाँच लिया — अब यह आपका है', 'Checked — it is now yours')); }
    else if (act === 'tundo'){ clearStart(i); toast(T('पहले जैसा', 'Restored')); }
    else if (act === 'tnone'){ setTime(i, 2, null); rerenderItem(i); }
    else if (act === 'bm'){ const me = ME(), k = KEY(IT[i].id); const had = !!me.bm[k]; if (had) delete me.bm[k]; else { me.bm[k] = Date.now(); if (TOUR) TOUR.bmAdded = true; } save(); rerenderItem(i); toast(!had ? T('बुकमार्क जोड़ा', 'Bookmarked') : T('बुकमार्क हटाया', 'Bookmark removed')); }
    else if (act === 'enote') noteSheet(i, +a.dataset.k);
    else if (act === 'menu') itemMenu(i);
    else if (act === 'done'){ const o = a.dataset.o, n = +a.dataset.n, d = DONE(ME(), o); if (d[n]) delete d[n]; else d[n] = Date.now(); save(); const box = a.closest('.pause'); const tmp = document.createElement('div'); tmp.innerHTML = pauseHTML(+a.dataset.i); const nb = Array.from(tmp.children).find(x => x.dataset.pause === o + n); if (box && nb) box.replaceWith(nb); if (d[n]) toast(VN(n) + T(' पूर्ण — जय श्रीराम', ' complete — Jai Shri Ram')); }
    return;
  }
  const w = ev.target.closest('.w'); if (w){ w.classList.add('sel'); const vb = w.closest('.verse'); wordSheet(w.dataset.w || w.textContent, null, vb ? langOf(+vb.dataset.i) : W.lang); }
}
function noteSheet(i, k){
  const me = ME(), key = KEY(IT[i].id), arr = me.notes[key] || [], cur = k != null ? arr[k] : null;
  openSheet('<h2>' + (cur ? T('टिप्पणी बदलें', 'Edit note') : T('अपनी टिप्पणी लिखें', 'Write a note')) + '</h2><p class="small muted">' + esc(itemLabel(i)) + '</p><textarea id="nt" placeholder="' + T('अपने विचार, भाव या कथा यहाँ लिखें…', 'Your thoughts or the story behind this verse…') + '">' + esc(cur ? cur.t : '') + '</textarea><div class="acts"><button class="btn" id="nSave">' + T('सेव करें', 'Save') + '</button>' + (cur ? '<button class="btn ghost" id="nDel">' + T('हटाएँ', 'Delete') + '</button>' : '') + '</div>');
  setTimeout(() => $('#nt').focus(), 250);
  $('#nSave').onclick = () => { const t = $('#nt').value.trim(); if (!t){ closeSheet(); return; } if (cur){ cur.t = t; cur.ts = Date.now(); } else { (me.notes[key] = arr).push({t, ts: Date.now()}); } save(); closeSheet(); rerenderItem(i); toast(T('टिप्पणी सेव हुई', 'Note saved')); };
  if ($('#nDel')) $('#nDel').onclick = () => { arr.splice(k, 1); if (!arr.length) delete me.notes[key]; save(); closeSheet(); rerenderItem(i); };
}
function itemMenu(i){
  const id = IT[i].id, edited = verseOf(i).edited || MK().some(k => { const m = mean(k, i); return m && m.edited; });
  openSheet('<p class="small muted">' + esc(itemLabel(i)) + '</p><div class="menu">' + (hasAu(i) ? '<button data-x="play"><svg><use href="#i-play"/></svg>' + T('यहाँसे सुनें', 'Play from here') + '</button>' : '') + '<button data-x="note"><svg><use href="#i-note"/></svg>' + T('टिप्पणी लिखें', 'Write a note') + '</button>' + (hasAu(i) ? '<button data-x="flag"' + (SRC.au && flagsNow()[id] ? ' class="on"' : '') + '><svg><use href="#i-clock"/></svg>' + T('ऑडियोका समय जाँचें', 'Review audio timing') + (SRC.au && flagsNow()[id] ? REVB : '') + '</button>' : '') + '<button data-x="copy"><svg><use href="#i-copy"/></svg>' + T('पद और अर्थ कॉपी करें', 'Copy verse and meaning') + '</button><button data-x="edit"><svg><use href="#i-edit"/></svg>' + T('पद या अर्थ सुधारें', 'Improve verse or meaning') + '</button>' + (edited ? '<button data-x="revert"><svg><use href="#i-edit"/></svg>' + T('मेरा सुधार हटाएँ (पद लौटाएँ)', 'Remove my correction (restore the verse)') + '</button>' : '') + '</div>');
  $$('#sheetBody [data-x]').forEach(b => b.onclick = () => {
    const x = b.dataset.x; closeSheet();
    if (x === 'play'){ playFrom(i, R.b); PL.whole = false; PL.endMsg = (R.org === 'k' ? KNAME(R.n) : VN(R.n)) + T(' पूर्ण', ' finished'); }   // to the end of what is open: the kāṇḍa, or the vishram
    if (x === 'copy'){ const ks = shownKinds().length ? shownKinds() : capKinds(); const txt = verseOf(i).v.join('\n') + ks.map(k => mean(k, i)).filter(Boolean).map(m => '\n\n' + m.x).join(''); (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(() => toast(T('कॉपी हो गया', 'Copied'))).catch(() => toast(T('कॉपी नहीं हो सका', 'Could not copy'))); }
    if (x === 'note') noteSheet(i, null);
    if (x === 'edit') editSheet(i);
    if (x === 'flag') toggleFlag(i);
    if (x === 'revert'){ S.profiles.forEach(p => { delete p.fix[KEY(id)]; MK().forEach(k => { if (SRC[k]) delete p.fix[KEY(SRC[k].id + ':' + id)]; }); }); save(); rerenderItem(i); toast(T('पद लौटाया', 'Verse restored')); }
  });
}
function editSheet(i){
  const id = IT[i].id, vv = verseOf(i), EK = MK().filter(k => SRC[k] && mean(k, i));
  openSheet('<h2>' + T('सुधार करें', 'Correct') + '</h2><p class="small muted">' + T('अपनी छपी पुस्तकसे मिलाकर सुधारें। मूल डेटा नहीं बदलेगा — सुधार आपकी फ़ाइलमें रहेगा और कभी भी हटाया जा सकता है।', 'Your correction is kept in your file and can be removed any time.') + '</p><div class="field"><label>' + esc(itemLabel(i)) + '</label><textarea id="ev" style="font-weight:700">' + esc(vv.v.join('\n')) + '</textarea></div>' + EK.map(k => '<div class="field"><label>' + LBM(k) + ' · ' + esc(TT(SRC[k].meta.title)) + '</label><textarea id="em-' + k + '"' + (k === 'en' ? ' class="lat"' : '') + '>' + esc(mean(k, i).x) + '</textarea></div>').join('') + '<div class="acts"><button class="btn" id="eSave">' + T('सेव करें', 'Save') + '</button></div>');
  $('#eSave').onclick = () => {
    const me = ME(); const v = $('#ev').value.split('\n').map(s => s.trim()).filter(Boolean);
    if (v.join('\n') !== IT[i].v.join('\n')) me.fix[KEY(id)] = {v}; else delete me.fix[KEY(id)];
    EK.map(k => [k, '#em-' + k]).forEach(([k, sel]) => { if (!$(sel) || !SRC[k]) return; const x = $(sel).value.trim(), orig = (SRC[k].m[id] || [])[0], key = KEY(SRC[k].id + ':' + id); if (x !== orig) me.fix[key] = {m: x}; else delete me.fix[key]; });
    save(); closeSheet(); rerenderItem(i); toast(T('सुधार सेव हुआ', 'Correction saved'));
  };
}

/* ---------------- audio from YouTube: hands-free recitation ---------------- */
let AUT = [], ytVid = '', ytOK = false, ytInfo = {t: 0, st: -1, d: 0}, ytWait = null;
let PL = {on: false, t: -1, end: null, cur: -1};
function tkey(){ return W.id + ':' + SRC.au.meta.id; }
// timing review: under every verse, the verse's own buttons. You mark the verse you are looking at, never a guess:
// "Starts now" when you hear its first word, "Ends now" when it is over (a refrain or music follows), ▶ to hear it.
function markBar(i){
  const x = SRC.au.at[IT[i].id], mine = myStarts()[IT[i].id], own = ownAt(IT[i].id), est = toCheck(i), by = fromOf(IT[i].id);
  const when = x ? T('शुरू ', 'Start ') + fmtT(x[1]) + (x[2] != null ? T(' · अंत ', ' · end ') + fmtT(x[2]) : '') : T('ऑडियोमें समय नहीं', 'No time in the recording');
  // − / + sit on either side of "Starts now" / "Ends now", in the same line: for a start you set, and for an end that is set
  const grp = (k, act, label, on) => '<span class="tgrp">' + (on ? '<button class="tn" data-a="tn" data-k="' + k + '" data-d="-1" aria-label="−">−</button>' : '') + '<button data-a="' + act + '">' + label + '</button>' + (on ? '<button class="tn" data-a="tn" data-k="' + k + '" data-d="1" aria-label="+">+</button>' : '') + '</span>';
  // a time set by ear — on this phone ("yours") or by the owner and already in the library ("sent") — has − / + for fine-tuning
  // under the times: "Until next" when an end is set; ↶ Undo is the verse's bottom-left corner; the step is in the player bar; the ⋮ menu holds nothing about timing
  const chips = own && x && x[2] != null ? '<button class="tchip" data-a="tnone">' + T('अगले पद तक', 'Until next') + '</button>' : '';
  return '<div class="tmark">' + grp(1, 'tstart', '⏱ ' + T('अभी शुरू', 'Starts now'), !!(own && x)) + grp(2, 'tend', '⏹ ' + T('अभी समाप्त', 'Ends now'), !!(own && x && x[2] != null)) + (by ? '<button data-a="tok">✓ ' + T('सही है', 'Correct') + '</button>' : '') + 
    '<span class="tinfo">' + when + (by ? ' · <b class="test">' + T('', 'from ') + esc(by) + T(' का — जाँचें', ' — to check') + '</b>' : mine ? ' · <b>' + T('आपका', 'yours') + '</b>' : own ? ' · <b>' + T('भेजा हुआ', 'sent') + '</b>' : est && SRC.au.checkSet.has(IT[i].id) ? ' · <b class="test">' + T('अनुमान', 'estimated') + '</b>' : est ? ' · <b class="test">' + T('आपके समयके अनुसार खिसकाया', 'moved to fit your times') + '</b>' : '') + '</span>' + (chips ? '<span class="tchips">' + chips + '</span>' : '') + '</div>';
}
// how far each − / + moves a time: the saffron ±… s chip in the player bar, beside ✕, shown while timing is on
const STEPS = [0.1, 0.25, 0.5, 1];
function syncStep(){ const b = $('#pStep'); b.hidden = !S.timing.on; b.textContent = '±' + step() + ' s'; syncCheck(); }
// Next ▸ (saffron, beside the step while Audio timing is on): the next verse still to check after the one playing (or in view),
// round to the first; one tap goes there and plays it. It shows how many are left and hides when none is.
function toCheckIds(){ const A = SRC.au; if (!S.timing.on || !A || !A.checkSet) return []; return IT.map((x, i) => i).filter(toCheck); }
function syncCheck(){ const b = $('#pCheck'), n = toCheckIds().length; b.hidden = !n; b.textContent = T('अगला ▸ ', 'Next ▸ ') + DEV(n); }
$('#pCheck').onclick = () => {
  const ids = toCheckIds(); if (!ids.length){ syncCheck(); return; }
  const cur = PL.on && PL.cur >= 0 ? PL.cur : topVisibleItem(), i = ids.find(k => k > cur) ?? ids[0];
  jumpTo(i); const el = document.getElementById('v' + i); if (el){ el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash'); }
  playFrom(i);
};
$('#pStep').onclick = () => { S.timing.step = STEPS[(STEPS.indexOf(step()) + 1) % STEPS.length]; save(); syncStep(); toast('− / + = ' + step() + ' s'); };
function step(){ return S.timing.step || 0.5; }
// a start that is only a guess — listed to be checked by the library, or placed again by text length to fit the set times — and not set by ear on this phone
function toCheck(i){ const id = IT[i].id, A = SRC.au; return !!(S.timing.on && A && A.checkSet && (((A.checkSet.has(id) || (A.moved && A.moved.has(id))) && !myStarts()[id]) || FLAGGED.has(id))); }
// a timing flag (the owner: a listener hears where the recording and the verse part), set with "Review audio timing" in the
// verse's ⋮ menu; once set, one sign shows it in both places, a blue dot (REVB): on the verse's ▶ (timing belongs to
// playing) and at the end of the menu item: only a
// verse flagged joins the to-check list (also one whose start was set), and leaves it once its start is set (or ✓ Correct).
// {flagged id: when}
let FLAGGED = new Set();
const REVB = '<span class="revd"></span>';
function flagsNow(){ return (SRC.au && S.timing.flags[tkey()]) || {}; }
function syncFlags(){ FLAGGED = new Set(Object.keys(flagsNow())); }
function toggleFlag(i){
  const k = tkey(), F = S.timing.flags[k] = S.timing.flags[k] || {}, id = IT[i].id, had = !!F[id];
  if (had) delete F[id]; else F[id] = Date.now();
  if (!Object.keys(F).length) delete S.timing.flags[k]; save(); syncFlags(); rerenderItem(i); if (S.timing.on) syncCheck();
  toast(had ? T('ऑडियोका समय जाँचना — हटाया', 'Review audio timing — removed') : T('यह पद ऑडियोका समय जाँचनेकी सूचीमें', 'This verse is on the audio timing check list'));
}
// the verses next to the one being recited carry ⚑ too
function markNear(){ $$('#rBody .verse.near').forEach(v => v.classList.remove('near')); if (!PL.on || PL.cur < 0) return; [PL.cur - 1, PL.cur + 1].forEach(j => { const el = document.getElementById('v' + j); if (el) el.classList.add('near'); }); }
function flagDone(id){ const k = tkey(), F = S.timing.flags[k]; if (!F || !F[id]) return; delete F[id]; if (!Object.keys(F).length) delete S.timing.flags[k]; syncFlags(); }   // its start was set (or checked)
function myStarts(){ return (SRC.au && S.timing.fix[tkey()]) || {}; }
// a verse set by ear: on this phone (myStarts), or by the owner and published (the audio JSON's "own" list) — kept exactly as given
function ownAt(id){ const A = SRC.au; return myStarts()[id] || (A && A.ownSet && A.ownSet.has(id) ? A.at0[id] : undefined); }
function fromOf(id){ return SRC.au ? (S.timing.from[tkey()] || {})[id] : undefined; }
function unfrom(id){ const f = S.timing.from[tkey()]; if (f){ delete f[id]; if (!Object.keys(f).length) delete S.timing.from[tkey()]; } }
function buildAudio(){
  AUT = []; syncFlags(); const A = SRC.au; if (!A) return;
  if (!A.at0){   // the published times; A.at = those plus the starts set by ear on this phone, after the order rule below
    A.at0 = A.at; A.checkSet = new Set(A.check || []); A.guessSet = new Set(A.guess || []); A.ownSet = new Set(A.own || []); A.raw = A.raw || {};
  }
  A.at = Object.assign({}, A.at0, myStarts());
  A.tracks.forEach(t => { t.fi = ID[t.first]; t.li = ID[t.last]; }); AUT = A.tracks.map(() => []);
  // the rule starts from the start each verse had before any re-placing ("raw", kept by make_timings.py for the verses it
  // moved), so the app and the library, given the same set times, arrive at exactly the same figures
  for (const id in A.at){ const i = ID[id]; if (i == null) continue; const [t, s, e] = A.at[id]; AUT[t].push([i, A.raw[id] != null && !myStarts()[id] ? A.raw[id] : s, e == null ? null : e]); }
  // a recording covers every verse timed on it, also one set by ear after its last matched verse (else, at the recording's
  // end, "go on with the next verse" would find that verse and play it again: a loop)
  A.tracks.forEach((t, k) => AUT[k].forEach(([i]) => { if (i < t.fi) t.fi = i; if (i > t.li) t.li = i; }));
  // keep the times in the order of the text around the times set by ear (the same rule as tools/audio/order.py, used by
  // make_timings.py): a verse set by ear (on this phone, or by the owner and published) is kept as given; a verse not set
  // by ear cannot start before the one before it has started, or before its set end, or at or after the next set start —
  // such a verse is placed again, by its length, between the nearest good times on either side (at the next good start
  // when there is no room). A set end later than the next set start is cut back to it.
  A.moved = new Set();
  AUT.forEach((a, ti) => {
    a.sort((x, y) => x[0] - y[0]);
    const own = k => !!ownAt(IT[a[k][0]].id), len = k => Math.max(8, IT[a[k][0]].v.join('').length);
    const nextOwn = k => { for (let j = k + 1; j < a.length; j++) if (own(j)) return a[j][1]; return Infinity; };
    for (let k = 0; k < a.length; k++) if (a[k][2] != null && a[k][2] > nextOwn(k)) a[k] = [a[k][0], a[k][1], nextOwn(k)];
    const good = a.map(() => true); let lo = -1;
    for (let k = 0; k < a.length; k++){
      if (!own(k) && (a[k][1] <= lo || a[k][1] >= nextOwn(k))) { good[k] = false; continue; }
      lo = Math.max(a[k][1], a[k][2] != null ? a[k][2] - 0.01 : -1);
    }
    for (let k = 0; k < a.length; k++){
      if (good[k]) continue;
      let e = k; while (e + 1 < a.length && !good[e + 1]) e++;
      const p = k - 1, n = e + 1;
      let L = p >= 0 ? Math.max(a[p][1] + 0.5, a[p][2] != null ? a[p][2] : 0) : 0; const U = n < a.length ? a[n][1] : L + 4 * (e - k + 2);
      if (U < L) L = U;
      let tot = 0; for (let j = k; j <= e; j++) tot += len(j); let acc = 0;
      for (let j = k; j <= e; j++){ a[j] = [a[j][0], Math.round((L + (U - L) * acc / (tot + (n < a.length ? 0 : len(e)))) * 10) / 10, a[j][2]]; acc += len(j); A.moved.add(IT[a[j][0]].id); }
      k = e;
    }
    // starts only guessed by text length (never heard) next to a time set by ear are guessed again between that time and
    // the next good one (or the recording's end), so they move with it; a heard start is never re-guessed
    const gs = k => A.guessSet.has(IT[a[k][0]].id) && !own(k);
    for (let k = 0; k < a.length; k++){
      if (!gs(k)) continue;
      let e = k; while (e + 1 < a.length && gs(e + 1)) e++;
      const p = k - 1, n = e + 1;
      if ((p >= 0 && own(p)) || (n < a.length && own(n))){
        const pre = p >= 0 && a[p][2] == null ? len(p) : 0, L0 = p >= 0 ? (a[p][2] != null ? a[p][2] : a[p][1]) : a[k][1];
        const U = n < a.length ? a[n][1] : A.tracks[ti].dur * 0.98;
        let tot = pre; for (let j = k; j <= e; j++) tot += len(j); let acc = pre;
        if (U - L0 > 0.3 * (e - k + 1 + (pre ? 1 : 0))) for (let j = k; j <= e; j++){ const st = Math.round((L0 + (U - L0) * acc / tot) * 10) / 10; acc += len(j); if (st !== a[j][1]){ a[j] = [a[j][0], st, a[j][2]]; A.moved.add(IT[a[j][0]].id); } }
      }
      k = e;
    }
    a.forEach(([i, s, e]) => { const id = IT[i].id, t = A.at[id][0]; A.at[id] = e != null ? [t, s, e] : [t, s]; });   // the menus and buttons show these
    a.sort((x, y) => x[1] - y[1]);
  });
}
// Where a recording begins for this work: at 0, so the opening music is heard, when the first verse follows a short
// opening; at the first verse when the work is a part of a longer video (the Hanumān āratī at the end of a Sundarakāṇḍa video)
const INTRO_MAX = 90;
function trStart(tr){ const a = SRC.au && SRC.au.at[(IT[tr.fi] || {}).id]; const s = a ? a[1] : 0; return s <= INTRO_MAX ? 0 : s; }
function hasAu(i){ return !!(SRC.au && SRC.au.at[IT[i].id]); }
function firstAu(a, b){ for (let i = a; i <= b; i++) if (hasAu(i)) return i; return null; }
/* YouTube embed driven by postMessage (no external script needed) */
function ytFrame(){ return $('#ytf'); }
function ytPost(func, args){ const f = ytFrame(); if (f && f.contentWindow) f.contentWindow.postMessage(JSON.stringify({event: 'command', func, args: args || []}), '*'); }
function ytLoad(vid, start){
  ytVid = vid; ytOK = false; ytInfo = {t: start, st: -1, d: 0};
  // the page's address goes with the request (YouTube refuses an embed that comes without one: its error 153)
  $('#ytBox').innerHTML = '<iframe id="ytf" width="200" height="200" src="https://www.youtube.com/embed/' + vid + '?enablejsapi=1&autoplay=1&playsinline=1&rel=0&modestbranding=1&start=' + Math.floor(start) + (location.origin && location.origin !== 'null' ? '&origin=' + encodeURIComponent(location.origin) : '') + '" title="YouTube" frameborder="0" referrerpolicy="strict-origin-when-cross-origin" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>';
  const f = ytFrame(); let n = 0;
  // knock until the player answers: every 0.5 s, then every second, for up to two minutes (a slow phone network)
  const hello = () => { if (ytOK || f !== ytFrame() || n++ > 130) return; try { f.contentWindow.postMessage(JSON.stringify({event: 'listening', id: 'manas', channel: 'widget'}), '*'); } catch (e) {} setTimeout(hello, n < 20 ? 500 : 1000); };
  f.addEventListener('load', hello);
  ytWatch(10000);
}
// YouTube has not answered yet: it may still be loading on a slow network, or the phone was locked as it started. The player
// is never taken away for that: a note with "Play on YouTube" is laid over it, and goes as soon as the player answers. Only
// YouTube's own refusal (onError) says a recording may not be played here.
function ytWatch(ms){
  clearTimeout(ytWait);
  ytWait = setTimeout(() => {
    if (ytOK || !PL.on) return;
    if (document.hidden){ document.addEventListener('visibilitychange', () => ytWatch(6000), {once: true}); return; }   // in the background: wait until the app is seen again
    ytBlocked();
  }, ms);
}
function ytNote(html){ ytNoteOff(); const d = document.createElement('div'); d.className = 'ytno'; d.innerHTML = html; $('#ytBox').appendChild(d); }
function ytNoteOff(){ $$('#ytBox .ytno').forEach(x => x.remove()); }
// Playing speed: 0.5× to 2× — YouTube's own speed, so the verse times (in the recording's
// time) stay right; the light follows the recording. Chosen with the speed button in the player bar; kept for next time.
const RATES = [0.5, 0.75, 1, 1.25, 1.5, 2];
function RATE(){ return S.settings.rate || 1; }
// how long a stretch takes with the recording chosen, at the speed set: on each recording, from the start of its first verse
// to the end of its last (its set end, else the next verse's start, else the recording's end), pauses between verses included
function spanSecs(a, b){
  if (!SRC.au) return null; let s = 0;
  AUT.forEach((L, t) => { let k0 = -1, k1 = -1; L.forEach(([i], k) => { if (i >= a && i <= b){ if (k0 < 0) k0 = k; k1 = k; } }); if (k0 < 0) return;
    const e = L[k1][2] != null ? L[k1][2] : k1 + 1 < L.length ? L[k1 + 1][1] : SRC.au.tracks[t].dur; if (e > L[k0][1]) s += e - L[k0][1]; });
  return s ? s / RATE() : null;
}
// 48 m · 4 h 58 m (४ घं ५८ मि), to the nearest minute: a listening time, so it is shown with ▶, never as the time to read
function durLabel(sec){ if (!sec) return ''; const m = Math.max(1, Math.round(sec / 60)), h = Math.floor(m / 60), r = m % 60;
  return h ? DEV(h) + T(' घं', ' h') + (r ? ' ' + DEV(r) + T(' मि', ' m') : '') : DEV(m) + T(' मि', ' m'); }
function applyRate(){ if (ytOK) ytPost('setPlaybackRate', [RATE()]); if (PL.on) pSub(); $('#pRate').textContent = RATE() + '×'; }
// the speed button in the player bar: one tap moves to the next speed, round and round
$('#pRate').onclick = () => { S.settings.rate = RATES[(RATES.indexOf(RATE()) + 1) % RATES.length]; save(); applyRate(); toast(T('गति ', 'Speed ') + RATE() + '×'); };
/* outside the website (e.g. a claude.ai artifact) YouTube cannot be embedded: open YouTube's own player page, which can stop at the end of what was asked */
function ytWatchURL(){
  const A = SRC.au, st = Math.floor(ytInfo.t || 0); let end = '';
  if (PL.end != null){ const nx = A.at[(IT[PL.end + 1] || {}).id]; if (nx && nx[0] === PL.t) end = '&end=' + Math.ceil(nx[1]); }
  return 'https://www.youtube.com/embed/' + ytVid + '?autoplay=1&start=' + st + end;
}
// why: 'refused' (YouTube error 101 / 150 / 153: the recording may not be played outside YouTube), 'gone' (100: removed or
// private), otherwise slow to start. Offline: it needs the internet.
function ytBlocked(why){
  if (navigator.onLine === false){ ytNote('<p>' + T('सुननेके लिए इंटरनेट चाहिए।', 'Playing needs the internet.') + '</p>'); return; }   // offline: not a blocked page
  const msg = why === 'refused' ? T('यह रिकॉर्डिंग YouTube के बाहर नहीं चलती।', 'This recording plays only on YouTube.')
    : why === 'gone' ? T('यह रिकॉर्डिंग YouTube पर अब नहीं मिलती।', 'This recording is no longer on YouTube.')
    : T('YouTube शुरू होनेमें समय ले रहा है…', 'YouTube is taking a while to start…');
  ytNote('<p>' + msg + '</p>' + (why === 'gone' ? '' : '<a class="btn" target="_blank" rel="noopener" href="' + ytWatchURL() + '">' + T('YouTube पर इसी पदसे सुनें ↗', 'Play on YouTube from this verse ↗') + '</a>'));
}
window.addEventListener('message', e => {
  if (!/youtube(-nocookie)?\.com$/.test((e.origin || '').replace(/^https?:\/\/(www\.)?/, ''))) return;
  let d; try { d = typeof e.data === 'string' ? JSON.parse(e.data) : e.data; } catch (x) { return; }
  if (!d) return;
  if (d.event === 'onError'){ const c = +d.info; clearTimeout(ytWait); if (PL.on) ytBlocked(c === 101 || c === 150 || c === 153 ? 'refused' : c === 100 ? 'gone' : ''); return; }
  if (d.event === 'onReady' || d.event === 'initialDelivery' || d.event === 'infoDelivery'){ if (!ytOK){ ytOK = true; ytNoteOff(); clearTimeout(ytWait);if (RATE() !== 1) ytPost('setPlaybackRate', [RATE()]); if (PL.on) pSub(); if (PL.on && PL.snip != null && PL.seekT != null) ytPost('seekTo', [PL.seekT, true]); } }   // a preview in a freshly loaded player: the page can only start it at a whole second, so seek to the exact time
  const info = d.info || {};
  if (typeof info.currentTime === 'number'){ ytInfo.t = info.currentTime; ytInfo.at = performance.now(); }
  if (typeof info.playbackRate === 'number' && info.playbackRate !== RATE() && ytOK && PL.on) ytPost('setPlaybackRate', [RATE()]);
  if (typeof info.duration === 'number' && info.duration) ytInfo.d = info.duration;
  if (typeof info.playerState === 'number'){ ytInfo.st = info.playerState; syncPlayer(); if (info.playerState === 0) onEnded(); }
  if (d.event === 'onStateChange' && typeof d.info === 'number'){ ytInfo.st = d.info; syncPlayer(); if (d.info === 0) onEnded(); }
});
/* what is playing, in the app's own words: the reading (kāṇḍa or plan day) and the reciter — never the recording's title */
// the player's small line: outside the reader it says the label can be tapped (“Go to verse ›”); in the reader, what is playing
function pSub(){ const out = CURVIEW !== 'reader'; $('#pTrack').textContent = out ? T('पदपर जाएँ ›', 'Go to verse ›') : (PL.on && SRC.au ? playingName() : ''); $('#pInfo').classList.toggle('go', out);
  $('#pInfo').setAttribute('aria-label', T('चल रहे पदपर जाएँ', 'Go to the verse playing')); }
function playingName(){ return (R.org === 'k' ? KNAME(R.n) : TT(PLAN[R.org].name) + ' · ' + VN(R.n)) + ' · ' + TT(SRC.au.meta.title); }   // the speed has its own button in the bar
// Fine-tuning preview: after − / + on a start, the first 2 s of the verse play from the new start; on an
// end, the last 2 s up to the new end. Then the player pauses, so the next tap can follow at once.
let snipT = null;
// the preview plays only when nothing is playing live: while the recitation runs on, − / + just move the
// time, so marking can go on from what is heard; a preview that is itself playing is replaced by the next one
function livePlay(){ return PL.on && playing() && PL.snip == null; }
function snippet(i, k){
  const x = SRC.au.at[IT[i].id]; if (!x) return; const tr = SRC.au.tracks[x[0]];
  const t0 = k === 1 ? x[1] : Math.max(x[1], x[2] - 2), t1 = k === 1 ? (x[2] != null ? Math.min(x[2], x[1] + 2) : x[1] + 2) : x[2];
  PL.on = true; PL.t = x[0]; PL.end = null; PL.snip = t1; PL.whole = false; PL.endMsg = '';
  $('#player').hidden = false; document.body.classList.add('playing');
  seekGuard(t0);
  if (ytVid !== tr.yt || !ytFrame()) ytLoad(tr.yt, t0); else { ytPost('seekTo', [t0, true]); ytPost('playVideo'); ytInfo.t = t0; ytInfo.at = performance.now(); }
  setCur(i); pSub(); syncPlayer();
  clearInterval(snipT); snipT = setInterval(() => {   // checked often, from the player's last report and the time since
    if (PL.snip == null){ clearInterval(snipT); return; }
    const now = playTime() + (playing() && ytInfo.at && PL.seekT == null ? RATE() * (performance.now() - ytInfo.at) / 1000 : 0);
    if (now >= PL.snip - 0.05){ ytPost('pauseVideo'); PL.snip = null; clearInterval(snipT); setTimeout(syncPlayer, 300); }
  }, 50);
}
function playFrom(i, end){
  if (!SRC.au) return;
  PL.snip = null;
  if (!hasAu(i)){ const j = firstAu(i, Math.min(IT.length - 1, i + 80)); if (j == null) return; i = j; }
  const [t, st0] = SRC.au.at[IT[i].id], tr = SRC.au.tracks[t];
  const st = (end != null && i === tr.fi) ? trStart(tr) : st0;
  PL.on = true; PL.t = t; PL.end = end; PL.cur = -1; PL.whole = false; PL.endMsg = ''; AN.playT0 = Date.now();
  $('#player').hidden = false; document.body.classList.add('playing'); wake(true);
  seekGuard(st);
  if (ytVid !== tr.yt || !ytFrame()) ytLoad(tr.yt, st); else { ytPost('seekTo', [st, true]); ytPost('playVideo'); ytInfo.t = st; ytInfo.at = performance.now(); }
  setCur(i); pSub(); syncPlayer();
}
// Right after a seek the player still reports its old time (or a moment before the asked-for one), which would light the
// previous verse for a beat. Until it reports a time at the asked-for start (at most 4 s), use that start.
// seekFrom: where the player was when the seek was asked — a report of that time afterwards is the old one, not the new
function seekGuard(t){ PL.seekFrom = PL.seekT == null ? ytInfo.t : PL.seekFrom; PL.seekT = t; PL.seekAt = performance.now(); }
function playTime(){
  const t = ytInfo.t;
  if (PL.seekT == null) return t;
  const stale = PL.seekFrom != null && Math.abs(t - PL.seekFrom) < 0.3 && Math.abs(PL.seekFrom - PL.seekT) >= 1;   // still the time from before the seek
  if ((!stale && t >= PL.seekT - 0.05 && t <= PL.seekT + 3) || performance.now() - PL.seekAt > 4000){ PL.seekT = null; return t; }
  return PL.seekT;
}
function onEnded(){
  if (!PL.on) return;
  // go on with the next recording; where a stretch has no recording yet, skip ahead to the next verse that has one
  const tr = SRC.au.tracks[PL.t], last = PL.end == null ? IT.length - 1 : PL.end, nx = firstAu(tr.li + 1, last);
  if (nx != null){ if (nx > tr.li + 1) toast(T('आगेके अंशकी रिकॉर्डिंग नहीं है — अगली रिकॉर्डिंगसे जारी', 'No recording for the next part — continuing with the next one')); const whole = PL.whole, msg = PL.endMsg; playFrom(nx, PL.end); PL.whole = whole; PL.endMsg = msg; return; }   // the reading goes on in the next recording: what was asked for (the whole work, a part, a day) is kept
  stopAudio();
}
function endOf(i){ const x = SRC.au && SRC.au.at[IT[i].id]; return x && x[2] != null ? x[2] : null; }   // a verse's end, when one is set (otherwise it runs until the next verse starts)
function curAt(time){ const a = AUT[PL.t]; let lo = 0, hi = a.length - 1, r = a[0][0]; while (lo <= hi){ const m = (lo + hi) >> 1; if (a[m][1] <= time){ r = a[m][0]; lo = m + 1; } else hi = m - 1; } return r; }
// every 300 ms while playing: light the verse being recited, stop at the end of what was asked, move the progress bar
function tick(anchor){
  if (!PL.on || !ytOK) return; if (typeof anchor !== 'number') anchor = PL.cur;
  const time = playTime(); const i = curAt(time);
  const e = endOf(i);
  if (PL.end != null && (i > PL.end || (i === PL.end && e != null && time >= e))){
    // the verse or stretch asked for has ended: stop, and offer to go on from the next verse
    const last = PL.end, whole = PL.whole, msg = whole ? T('पाठ पूर्ण', 'Recitation complete') : PL.endMsg || T('पूर्ण', 'Finished');
    stopAudio(); const nx = whole ? null : firstAu(last + 1, Math.min(IT.length - 1, last + 80));
    if (TOUR && TOUR.waiting) return;   // the tour's verse has been heard: the tour finishes (no "Play on")
    if (nx == null) toast(msg); else toastAct(msg, T('▶ आगे सुनें', '▶ Play on'), () => { if (!$('#reader').classList.contains('on')) openReader(R.org, nx); playFrom(nx); });
    return;
  }
  // a verse's end matters only where playing stops (one verse, or the last verse of a reading): never skipped. While timings
  // are being reviewed, a verse that has ended hands the light to the next one at once, so its start can be marked.
  let show = i; const a = AUT[PL.t], at = id => a.findIndex(x => x[0] === id);
  if (S.timing.on){
    // the light waits for you: it never moves on to a verse whose start is only a guess. It stays on the verse you are on
    // until you mark the next one ("Starts now"), or that verse's set end passes; verses with checked times are followed.
    let k = at(i); const c = at(anchor);
    if (c >= 0 && k > c){ while (k > c && toCheck(a[k][0])) k--; show = a[k][0]; }
    else if (c > 0 && k === c - 1 && endOf(a[k][0]) != null && time >= endOf(a[k][0])) show = anchor;   // moved on by an end: stay
  }
  // a verse whose set end has passed hands the light to the next verse at once, in both modes — even when
  // that verse starts a little later; the same in ☰ › More settings › Audio timing on or off
  const m = at(show), e2 = endOf(show);
  if (e2 != null && time >= e2 && m >= 0 && m + 1 < a.length) show = a[m + 1][0];
  setCur(show); followLines(show, time);
  // the bar runs over this work's part of the recording only (a work that is a slice of a longer video starts at 0%)
  const tr = SRC.au.tracks[PL.t], d = ytInfo.d || tr.dur, s0 = trStart(tr);
  $('#pProg').style.width = Math.max(0, Math.min(100, 100 * (time - s0) / Math.max(1, d - s0))) + '%';
}
setInterval(tick, 300);
/* place the verse being recited in the space between the top bar and the player:
   centred if it fits, otherwise with its first line just below the top bar (never hidden under it) */
// The verse being recited is kept at the top, just below the bar, and the text moves up under it, so the next verses are
// always in view — even when the recording runs a little ahead of the timings. A verse-type heading
// (॥ चौपाई ॥) right above it stays with it.
function keepInView(el){
  const top = $('#reader .bar').getBoundingClientRect().bottom, prev = el.previousElementSibling;
  const head = prev && prev.classList && prev.classList.contains('vtype') ? prev : el;
  window.scrollTo({top: Math.max(0, scrollY + head.getBoundingClientRect().top - (top + 6)), behavior: 'smooth'});
}
// a verse taller than the space between the bar and the player: the page turns inside it while it is recited. The line being
// recited is guessed from the time spent in the verse (its lines share the verse's time by their length); when that line —
// line by line, with its meaning — runs under the player, it is brought up to just below the bar
function followLines(i, time){
  if (S.timing.on || !$('#reader').classList.contains('on')) return; const el = document.getElementById('v' + i); if (!el) return;
  const top = $('#reader .bar').getBoundingClientRect().bottom, bot = $('#player').getBoundingClientRect().top;
  if (el.offsetHeight <= bot - top - 12) return;
  const a = AUT[PL.t], m = a.findIndex(x => x[0] === i); if (m < 0) return;
  const s = a[m][1], e = endOf(i) ?? (m + 1 < a.length ? a[m + 1][1] : (ytInfo.d || SRC.au.tracks[PL.t].dur));
  const vl = [...el.querySelectorAll('.vline')], ls = vl.length ? vl : [...el.querySelectorAll('.vtext p')];
  if (!(e > s) || ls.length < 2) return;
  const w = ls.map(l => l.textContent.length || 1), f = (time - s) / (e - s) * w.reduce((x, y) => x + y);
  let k = 0, acc = w[0]; while (k < ls.length - 1 && acc <= f){ k++; acc += w[k]; }
  if (k === 0 || PL.line === i + ':' + k) return;   // once for each line, so the reader can still scroll by hand within the verse
  const r = ls[k].getBoundingClientRect(), end = !vl.length ? r.bottom : k + 1 < ls.length ? ls[k + 1].getBoundingClientRect().top : el.getBoundingClientRect().bottom;
  // in place (in view, or at the top when it is taller than the space): this line is done; otherwise each tick moves it up
  // until it is (a smooth scroll can be cut short when verses are added above)
  if (r.top >= top && (end <= bot - 4 || r.top <= top + 24)) PL.line = i + ':' + k;
  else window.scrollTo({top: Math.max(0, scrollY + r.top - (top + 6)), behavior: 'smooth'});
}
function setCur(i){
  if (PL.cur === i) return; PL.cur = i; PL.line = null;
  $$('#rBody .verse.now').forEach(v => v.classList.remove('now'));
  $('#pVerse').textContent = posLabel(i); pSub();   // only the place in the text (Doha 45 · Chaupai 3, Shloka 1), so it is seen to move verse by verse
  anchorPlay(i);
  if (!$('#reader').classList.contains('on')) return;
  if (i < R.a || i > R.b){ R.org = R.org; [R.a, R.b, R.n] = rangeFor(R.org, i); renderAround(i); }
  else if (!document.getElementById('v' + i)) renderAround(i, false);
  const el = document.getElementById('v' + i);
  // while timings are being marked the page is not moved under your finger: it only follows when the lit verse leaves the screen
  // the player's timing wins: the page follows the light every time a new verse starts, whatever was
  // touched or scrolled meanwhile — no pause after a touch
  if (el){ el.classList.add('now'); if (!(S.timing.on && inView(el))) keepInView(el); }
  markNear();
}
function stopAudio(){ ytPost('pauseVideo'); PL.on = false; PL.snip = null; $('#player').hidden = true; $('#pJump').hidden = true; document.body.classList.remove('playing'); $$('#rBody .verse.now').forEach(v => v.classList.remove('now')); }
function playing(){ return ytInfo.st === 1 || ytInfo.st === 3; }
function syncPlayer(){ $('#pPlay').innerHTML = '<svg><use href="#i-' + (playing() ? 'pause' : 'play') + '"/></svg>'; $('#pRate').textContent = RATE() + '×'; syncStep(); }
$('#pPlay').onclick = () => { if (playing()) ytPost('pauseVideo'); else ytPost('playVideo'); setTimeout(syncPlayer, 400); };
$('#pClose').onclick = stopAudio;
function stepVerse(d){ PL.snip = null; const a = AUT[PL.t]; const k = a.findIndex(x => x[0] === PL.cur); const n = k + d; if (k >= 0 && n >= 0 && n < a.length){ seekGuard(a[n][1]); ytPost('seekTo', [a[n][1], true]); ytInfo.t = a[n][1]; ytInfo.at = performance.now(); PL.cur = -1; tick(); } }
/* timing review: set a verse's start by ear. The player reports its time a few times a second, so the moment of the tap is
   worked out from the last report; 0.3 s is taken off for the time it takes to hear the word and tap. */
function nowAt(){ const t = playTime(), since = PL.seekT != null ? PL.seekAt : ytInfo.at; return Math.max(0, t + (playing() && since ? RATE() * (performance.now() - since) / 1000 : 0) - 0.3 * RATE()); }   // right after a seek, the player may still report its old time: the asked-for time is used (playTime)
// k = 1: the verse's start; k = 2: its end (null = it runs until the next verse starts). Returns false when refused (with the reason shown).
function setTime(i, k, sec){
  const id = IT[i].id, fx = S.timing.fix[tkey()] = S.timing.fix[tkey()] || {}, cur = SRC.au.at[id] || [PL.on ? PL.t : 0, 0, null];
  if (PL.on && SRC.au.at[id] && cur[0] !== PL.t && sec != null){ toast(T('यह पद दूसरी रिकॉर्डिंगमें है — उसी रिकॉर्डिंगको चलाकर लगाएँ', 'This verse is in another recording — play that recording to mark it')); return false; }
  if (k === 2 && sec == null && cur[2] == null) return false;   // "Until next" on a verse that has no end: nothing to remove
  const v = [cur[0], cur[1], cur[2] == null ? null : cur[2]]; v[k] = sec == null ? null : Math.round(sec * 10) / 10;
  // the verses set by ear nearest to this one, before and after, in the order of the text (estimates in between are placed
  // again by the order rule, so they never block a move)
  const a = AUT[v[0]] || [], j = a.findIndex(x => x[0] === i);
  const rows = a.slice().sort((x, y) => x[0] - y[0]), jj = rows.findIndex(x => x[0] === i);
  let pid = null, nid = null;
  for (let q = jj - 1; q >= 0; q--) if (ownAt(IT[rows[q][0]].id)){ pid = IT[rows[q][0]].id; break; }
  for (let q = jj + 1; q < rows.length; q++) if (ownAt(IT[rows[q][0]].id)){ nid = IT[rows[q][0]].id; break; }
  if (jj < 0) for (const r of rows){ const oid = IT[r[0]].id; if (ownAt(oid)){ if (r[0] < i) pid = oid; else if (nid == null) nid = oid; } }
  const p = pid && ownAt(pid), n = nid && ownAt(nid);
  if (k === 2 && v[2] != null && v[2] <= v[1]){
    // "Ends now" on a verse whose start is only an estimate that lies after now: the estimate was late. The light came to
    // this verse when the verse before it ended, so that end is its start; otherwise ask for the start.
    const pe = j > 0 ? endOf(a[j - 1][0]) : null, mine = !!ownAt(id);   // a start set by ear (here or sent) is never moved by this rule
    if (!mine && pe != null && pe < v[2]) v[1] = pe;
    else { toast(mine ? T('अंत शुरुआतके बाद होना चाहिये', 'The end must come after the start') : T('पहले “अभी शुरू” से इसकी शुरुआत लगाएँ', 'Mark its start first (Starts now)')); return false; }
  }
  if (k === 1 && v[2] != null && v[2] <= v[1]) v[2] = null;
  // Order is kept between the verses set by ear: a start cannot go before the previous set start, or at or past the
  // next set start — say which verse is in the way, so it can be moved first
  if (k === 1 && p && v[1] <= p[1] + 0.1){ toast(T('पिछला पद इसके बाद शुरू होता है (', 'The verse before starts later than that (') + fmtT(p[1]) + T(') — पहले उसकी शुरुआत आगे-पीछे करें', ') — move its start first')); return false; }
  if (k === 1 && n && v[1] >= n[1] - 0.1){ toast(T('अगला पद इससे पहले शुरू होता है (', 'The next verse starts before that (') + fmtT(n[1]) + T(') — पहले उसकी शुरुआत आगे करें', ') — move its start first')); return false; }
  // Neighbours move together: an end moved past the next set start carries that start with it; a start
  // moved before the previous verse's set end pulls that end back. Nothing is silently cut; refused only when a neighbour
  // would be squeezed to nothing (its start reaching its end, or the set start after it).
  const link = [];
  if (k === 2 && v[2] != null && n && v[2] > n[1] + 0.001){
    let nn = null; for (let q = rows.findIndex(x => IT[x[0]].id === nid) + 1; q < rows.length; q++) if (ownAt(IT[rows[q][0]].id)){ nn = ownAt(IT[rows[q][0]].id); break; }
    const room = n[2] != null ? n[2] : nn ? nn[1] : Infinity;
    if (room <= v[2] + 0.1){ toast(n[2] != null ? T('अगला पद इतनी जल्दी समाप्त होता है — पहले उसका अंत आगे करें', 'The next verse ends too soon for that — move its end first') : T('उसके बादका पद इससे पहले शुरू होता है — पहले उसकी शुरुआत आगे करें', 'The verse after next starts before that — move its start first')); return false; }
    link.push([nid, [n[0], v[2], n[2] == null ? null : n[2]]]);
  }
  if (k === 1 && p && p[2] != null && v[1] < p[2] - 0.001) link.push([pid, [p[0], p[1], v[1]]]);
  // "Ends now" also starts the next verse: an end on this verse gives the verse after it, when its start
  // is not set by ear, that end as its start — it is yours from then on, and while the two are equal the start follows the
  // end (− / + on the end move both), so no second tap is needed at the very moment the next verse begins.
  const nx = jj >= 0 ? rows[jj + 1] : null, nxid = nx ? IT[nx[0]].id : null;
  if (k === 2 && v[2] != null && nx){
    if (!ownAt(nxid)){
      if (n && v[2] >= n[1] - 0.1){ toast(T('आगेका पद इससे पहले शुरू होता है (', 'A verse after this starts before that (') + fmtT(n[1]) + T(') — पहले उसकी शुरुआत आगे करें', ') — move its start first')); return false; }
      link.push([nxid, [v[0], v[2], null]]);
    }
    else if (nid === nxid && cur[2] != null && Math.abs(n[1] - cur[2]) < 0.001 && !link.some(([lid]) => lid === nid)) link.push([nid, [n[0], v[2], n[2] == null ? null : n[2]]]);   // glued to the old end: moves back with it
  }
  const was = marksNow();
  fx[id] = v; unfrom(id); link.forEach(([lid, lv]) => { fx[lid] = lv; unfrom(lid); }); save(); buildAudio();
  refreshMarks(was, i);
  if (PL.on){ PL.cur = -1; tick(i); }   // the light moves at once, from this verse (after an end: to the next verse); the page stays where you are
  toast((k === 1 ? T('शुरुआत: ', 'Starts at ') : T('अंत: ', 'Ends at ')) + (sec == null ? '—' : fmtT(sec)));
}
// after a time was written or removed: every verse on screen whose time, label or buttons changed is drawn again
function refreshMarks(was, i){ Object.keys(was).forEach(q => { q = +q; if (q === i || was[q] !== JSON.stringify(SRC.au.at[IT[q].id]) + toCheck(q) + !!myStarts()[IT[q].id]) rerenderItem(q); }); syncCheck(); }
// (a verse index the work doesn't have is skipped: the reader may still hold a longer work's verses)
function marksNow(){ const was = {}; $$('#rBody .verse').forEach(el => { const q = +el.dataset.i; if (!IT[q]) return; was[q] = JSON.stringify(SRC.au.at[IT[q].id]) + toCheck(q) + !!myStarts()[IT[q].id]; }); return was; }
function clearStart(i){ const fx = S.timing.fix[tkey()] || {}, was = marksNow(); delete fx[IT[i].id]; unfrom(IT[i].id); if (!Object.keys(fx).length) delete S.timing.fix[tkey()]; save(); buildAudio(); refreshMarks(was, i); if (PL.on){ PL.cur = -1; tick(i); } }
function fmtT(sec){ const m = Math.floor(sec / 60), s = sec - m * 60; return m + ':' + (s < 10 ? '0' : '') + s.toFixed(1); }
function applyTiming(){ document.body.classList.toggle('timing', !!S.timing.on); syncStep(); }
$('#pPrev').onclick = () => stepVerse(-1);
$('#pNext').onclick = () => stepVerse(1);
function toPlaying(){ if (PL.cur < 0) return; if (!$('#reader').classList.contains('on')) openReader(R.org, PL.cur); const c = PL.cur; PL.cur = -1; setCur(c); }
$('#pInfo').onclick = toPlaying;
// “↓ now playing”: while the lit verse is off the screen, a pill above the player names it (as the footer
// would); a tap brings it back into view. It goes as soon as the verse is on the screen again, or at the next verse's start.
$('#pJump').onclick = toPlaying;
function jumpPill(){
  const b = $('#pJump'); if (!PL.on || PL.cur < 0 || CURVIEW !== 'reader' || $('#sheet').classList.contains('on')){ b.hidden = true; return; }
  const el = document.getElementById('v' + PL.cur), r = el && el.getBoundingClientRect(), top = $('#reader .bar').getBoundingClientRect().bottom, pl = $('#player').hidden ? {top: innerHeight} : $('#player').getBoundingClientRect();
  const seen = r && r.bottom > top + 24 && r.top < pl.top - 24;   // some of the verse is on the screen
  if (seen){ b.hidden = true; return; }
  const i = PL.cur, where = R.org === 'k' ? (PARTS.length > 1 ? KNAME(IT[i].p) : '') : VN(R.n);
  const h = '<b><span class="arr">' + (i >= topVisibleItem() ? '↓' : '↑') + '</span>' + T('', 'Go to ') + esc(posLabel(i)) + T(' पर जाएँ', '') + '</b>' + (where ? '<small>' + esc(where) + '</small>' : '');   // "Go to <verse>", a big arrow pointing the way
  if (b.innerHTML !== h) b.innerHTML = h; b.style.bottom = (innerHeight - pl.top + 10) + 'px'; b.hidden = false;
}
setInterval(jumpPill, 300);
function playRange(org, a, b){ const st = firstAu(a, b); if (st == null) return; openReader(org, st); playFrom(st, b); PL.whole = a === 0 && b === IT.length - 1; PL.endMsg = PL.whole ? '' : spanLabel(a, b) + T(' पूर्ण', ' finished'); }

/* ---------------- library (any depth: genre › group … › work) ---------------- */
// The library shows no tradition: index.json's top shelves (hinduism, sikhism) keep the paths, and the reader sees their
// genres as the top shelves. A genre with "shelf" is shown inside that genre (the Sikh gurbani among the Granthas), and
// shelves with the same id are one shelf. Work nodes are kept as they are, so their path and work id still find the files.
function libView(traditions){
  const out = [], copy = n => Object.assign({}, n, {children: []});
  const add = (into, n) => { if (n.work){ into.push(n); return; }
    let s = into.find(x => !x.work && x.id === n.id); if (!s){ s = copy(n); delete s.shelf; into.push(s); }
    n.children.forEach(c => add(s.children, c)); };
  const genres = traditions.flatMap(t => t.children || []);
  genres.filter(g => !g.shelf).forEach(g => add(out, g));
  genres.filter(g => g.shelf).forEach(g => { const to = out.find(x => x.id === g.shelf); if (to) g.children.forEach(c => add(to.children, c)); else add(out, g); });
  return out;
}
let libPath = [];
function libNode(){ let n = {children: LIB}; for (const id of libPath){ const c = (n.children || []).find(x => x.id === id); if (!c) { libPath = []; return {children: LIB}; } n = c; } return n; }
function renderLibrary(){
  const node = libNode(), kids = node.children || [];
  // the way back up, in the header: Library › Vedas › Yajurveda › … (the shelf you are on is the last, not a link)
  let crumbs = '<button data-lp="-1">' + LB.lib() + '</button>'; let n = {children: LIB};
  libPath.forEach((id, k) => { n = n.children.find(x => x.id === id); crumbs += '<span class="sep">›</span>' + (k === libPath.length - 1 ? '<span class="cur">' + esc(TT(n.title)) + '</span>' : '<button data-lp="' + k + '">' + esc(TT(n.title)) + '</button>'); });
  const cr = $('#libCrumbs'); cr.innerHTML = libPath.length ? crumbs : '';
  // too long for the header: shorten to Library › … › parent › this shelf, then Library › … › this shelf, then … › this shelf;
  // “…” lists every level
  if (libPath.length > 1 && cr.scrollWidth > cr.clientWidth + 1){
    const names = []; let m = {children: LIB}; libPath.forEach(id => { m = m.children.find(x => x.id === id); names.push(TT(m.title)); });
    const L = libPath.length, lib = '<button data-lp="-1">' + LB.lib() + '</button><span class="sep">›</span>', more = '<button class="crMore">…</button><span class="sep">›</span>', cur = '<span class="cur">' + esc(names[L - 1]) + '</span>';
    const par = L > 1 ? '<button data-lp="' + (L - 2) + '">' + esc(names[L - 2]) + '</button><span class="sep">›</span>' : '';
    for (const v of [lib + (L > 2 ? more : '') + par + cur, lib + more + cur, more + cur]){ cr.innerHTML = v; if (cr.scrollWidth <= cr.clientWidth + 1) break; }
    $$('#libCrumbs .crMore').forEach(b => b.onclick = () => { openSheet('<div class="menu"><button data-lpj="-1">' + LB.lib() + '</button>' + names.slice(0, -1).map((nm, j) => '<button data-lpj="' + j + '">' + '&nbsp;'.repeat((j + 1) * 3) + esc(nm) + '</button>').join('') + '</div>'); $$('#sheetBody [data-lpj]').forEach(x => x.onclick = () => { closeSheet(); libPath = libPath.slice(0, +x.dataset.lpj + 1); history.pushState(snap('library'), ''); renderLibrary(); window.scrollTo(0, 0); }); });
  }
  cr.scrollLeft = 1e5;   // if it still does not fit, the end (the shelf you are on) shows
  $('#libTitle').textContent = libPath.length ? TT(node.title) : LB.lib();
  // two levels per screen: a shelf inside this one is shown as a heading with its own items under it
  // a shelf shows the works on it by name: tap a work to open it straight away, or the shelf's name to browse it
  const worksIn = c => { const r = []; (function w(n){ (n.children || []).forEach(x => x.work ? r.push(x) : w(x)); })(c); return r; };
  const row = (c, key) => {
    // a shelf shows two works — the ones used most recently on this phone first (S.w[id].at: last opened, read or played) — then “+N” for the rest
    const at = w => (S.w[w.work] || {}).at || 0, ws = c.work ? [] : worksIn(c).map((w, k) => [w, k]).sort((x, y) => at(y[0]) - at(x[0]) || x[1] - y[1]).map(x => x[0]), MAX = 2;
    return '<li><button class="it" data-node="' + esc(key) + '"><span class="grow"><span class="ti">' + esc(TT(c.title)) + '</span>' + (ws.length ? '' : '<br><span class="ds">' + esc(TT(c.desc || c.by) || '') + '</span>') + '</span><span class="chev">›</span></button>' +
      (ws.length ? '<div class="lworks">' + ws.slice(0, MAX).map(w => '<button data-open-work="' + esc(w.work) + '">' + esc(TT(w.title)) + '</button>').join('') + (ws.length > MAX ? '<button class="more" data-node="' + esc(key) + '">+' + DEV(ws.length - MAX) + '</button>' : '') + '</div>' : '') + '</li>';
  };
  // the library itself is one row per genre, with no headings (the owner: no partitioning on the library screen). On a
  // shelf's page, a shelf that holds shelves is a heading over them and a shelf that holds only works is one row with its
  // works as buttons, so every shelf page looks the same however deep its shelves go (Āratī › Śrī Rāma like Vedas › Yajurveda)
  $('#libList').innerHTML = kids.map(c => libPath.length && c.children && c.children.some(g => g.children) ? '<li class="lhead">' + esc(TT(c.title)) + '</li>' + c.children.map(g => row(g, c.id + '/' + g.id)).join('') : row(c, c.id)).join('');
  $$('#libList [data-node]').forEach(b => b.onclick = () => {
    const ids = b.dataset.node.split('/'); let n = node, c = null; ids.forEach(id => { c = (n.children || []).find(x => x.id === id); n = c; });
    if (c.work) openWork(c.work); else { libPath.push(...ids); history.pushState(snap('library'), ''); renderLibrary(); window.scrollTo(0, 0); }
  });
  $$('#libList [data-open-work]').forEach(b => { b.onclick = () => { if (b.dataset.held){ delete b.dataset.held; return; } openWork(b.dataset.openWork); }; holdFor(b, () => aboutWork(b.dataset.openWork)); });
  $$('#libCrumbs [data-lp]').forEach(b => b.onclick = () => { libPath = libPath.slice(0, +b.dataset.lp + 1); history.pushState(snap('library'), ''); renderLibrary(); window.scrollTo(0, 0); });
}
// a long press (half a second, the finger kept still) on a work in the library opens About this work instead of the work;
// the click that follows the press is then ignored (data-held). Right-click (contextmenu) does the same on a computer.
function holdFor(el, fn){
  let t = null, x = 0, y = 0;
  const go = () => { t = null; el.dataset.held = 1; if (navigator.vibrate) try { navigator.vibrate(15); } catch (e) {} fn(); };
  el.addEventListener('pointerdown', e => { if (e.button > 0) return; delete el.dataset.held; x = e.clientX; y = e.clientY; clearTimeout(t); t = setTimeout(go, 500); });
  const stop = () => { clearTimeout(t); t = null; };
  el.addEventListener('pointermove', e => { if (t && Math.hypot(e.clientX - x, e.clientY - y) > 10) stop(); });   // a scroll is not a press
  ['pointerup', 'pointercancel', 'pointerleave'].forEach(k => el.addEventListener(k, stop));
  el.addEventListener('contextmenu', e => { e.preventDefault(); if (t){ stop(); go(); } else if (!el.dataset.held){ el.dataset.held = 1; fn(); } });
}
/* library search: finds works and shelves by title, author, edition, description or id, in either script */
const normQ = x => (x || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[\u093c]/g, '').normalize('NFC');
function libSearch(q){
  // as in verse search, both sides are folded to a sound key (fD, fL); a longer word may also differ by a letter or two
  // (none under 5 letters, one up to 7, then one in four): सुंदरकांड finds सुन्दरकाण्ड, Sunderkand finds Sundarakāṇḍa
  const nq = normQ(q.trim()), latin = /[a-zA-Z]/.test(q), fq = (latin ? fL(q) : fD(q)).join(''), k = fq.length < 5 ? 0 : fq.length < 8 ? 1 : Math.floor(fq.length / 4), out = [];
  (function walk(nodes, trail){ (nodes || []).forEach(n => {
    const raw = [n.id, n.path, n.work, ...['title', 'by', 'edition', 'desc'].map(k => n[k] ? (n[k].hi || '') + ' ' + (n[k].en || '') : '')].join(' ');
    if (normQ(raw).includes(nq) || (fq.length >= 2 && near(fq, (latin ? fL(raw) : fD(raw)).join(''), k) <= k)) out.push({n, trail});
    if (n.children) walk(n.children, trail.concat([n]));
  }); })(LIB, []);
  $('#sRes').innerHTML = out.length ? out.map((r, k) => '<button class="res" data-hit="' + k + '"><div class="where">' + esc(r.trail.map(x => TT(x.title)).join(' › ') || TT(r.n.desc || r.n.by) || '') + '</div><div class="snip" style="font-weight:700">' + esc(TT(r.n.title)) + '</div></button>').join('')
    : '<div class="empty">' + T('कुछ नहीं मिला', 'Nothing found') + '</div>';
  $$('#sRes [data-hit]').forEach(b => b.onclick = () => { const r = out[+b.dataset.hit]; if (r.n.work) openWork(r.n.work); else { libPath = r.trail.map(x => x.id).concat([r.n.id]); show('library'); } });
}
// one search page for the whole app: opened from the library it finds works and shelves; from a work, its verses
let SCOPE = 'text';
function setScope(scope){ SCOPE = scope; const lib = scope === 'lib'; $('#scope').hidden = lib;
  $$('#scope .chip').forEach(c => { if (!['v', 'h', 'e', 'n'].includes(c.dataset.s)) c.hidden = !workKinds().includes(c.dataset.s); });   // a third meaning language's chip, on works that have it
  $('#q').placeholder = lib ? T('ग्रन्थ, रचयिता या विषय खोजें', 'Search works, authors or shelves') : T('शब्द, अर्थ या English में खोजें', 'Search a verse or a meaning'); }
function openSearch(scope, stay){   // stay: only reset the page (the box was cleared), without another history entry
  setScope(scope); const lib = scope === 'lib';
  $('#q').value = '';
  $('#sRes').innerHTML = '<div class="empty">' + (lib ? T('ग्रन्थका नाम, रचयिता या विषय लिखें।', 'Type the name of a work, an author or a shelf.') : T('चौपाई, दोहे या अर्थका कोई भी शब्द लिखें।', 'Type any word from a verse, its Hindi meaning or its English meaning.')) + '</div>';
  if (!stay) show('search');
}
$('#libSearchBtn').onclick = () => openSearch('lib');
$('#hSearch').onclick = () => openSearch('text');
$('#rSearch').onclick = () => openSearch('text');
$('#libMenu').onclick = mainMenu;
function workPath(id){ let r = null; (function walk(n){ (n || []).forEach(c => { if (c.work === id) r = c.path; else walk(c.children); }); })(LIB); return r || id; }
// the salutation on the opening screen: the work's own (library/index.json "salute": जय श्रीराम for the
// Mānas and Sundarakāṇḍa, ॐ श्री साईं राम for the Dhūpa Āratī, ੴ for the Sukhmani Sahib …), otherwise ॐ श्री परमात्मने नमः.
// The phone remembers each work's, so the screen shown before anything has loaded already greets the work being opened.
const SALUTE = '॥ ॐ श्री परमात्मने नमः ॥';
function saluteOf(id){ let r = null; (function walk(n){ (n || []).forEach(c => { if (c.work === id) r = c.salute; else walk(c.children); }); })(LIB); return r || SALUTE; }
function showSalute(text){ $('#loading').textContent = text; }
// The greeting (the work's salutation) shows only when opening a work takes more than 0.2 s, so a quick open goes straight
// to the work's page; once shown it stays 0.3 s, so it does not flicker. Only for stepping into a work from the library (or
// the tour): never when the app starts, on a refresh, on Back, or for the work already open, when the screen just waits, blank.
const SALUTE_AFTER = typeof window.__SALUTE_MS === 'number' ? window.__SALUTE_MS : 200, SALUTE_HOLD = SALUTE_AFTER ? 300 : 0;
let saluteAt = 0, saluteT = null, greeted = false;
function coverOn(text, after){ clearTimeout(saluteT); showSalute(text); const on = () => { $('#loading').hidden = false; saluteAt = performance.now(); };
  if (after > 0) saluteT = setTimeout(on, after); else on(); }
async function coverOff(){ clearTimeout(saluteT); saluteT = null; if (!$('#loading').hidden && greeted){ const left = SALUTE_HOLD - (performance.now() - saluteAt); if (left > 0) await new Promise(r => setTimeout(r, left)); }
  $('#loading').hidden = true; greeted = false; }
const hideSalute = coverOff;
// The work's page needs only the work and its recording: it shows as soon as they are here. The meanings and the
// dictionaries (megabytes for the Manas) load behind it; the reader and search wait for them (WREADY) when opened sooner.
let WREADY = Promise.resolve(), wReady = true;
async function whenReady(){ if (wReady) return; coverOn('', 200); await WREADY; await coverOff(); }
async function openWork(id, noShow){
  greeted = !noShow && !(W && W.id === id);
  if (greeted) coverOn(saluteOf(id), SALUTE_AFTER);
  else if (W === null || W.id !== id) coverOn('', $('#loading').hidden ? 200 : 0);   // a quiet open: blank, and only if it is slow
  try {
    if (!W || W.id !== id){ const path = workPath(id); W = await getJSON(path + '/work'); W.path = path; partReset(); buildWork(); moveRenamed(); fixLast();
      await loadSources('au');
      wReady = false; const w = W;
      WREADY = Promise.all([loadSources('meanings'), loadGlossaries()]).then(() => { if (W !== w) return; if (BYPART()){ const l = WS().last; loadPart(l && IT[l.i] ? IT[l.i].p : 0); } })   // the part “Continue” opens
        .finally(() => { if (W === w) wReady = true; });
    }
    S.work = id; WS().at = Date.now(); save();   // when it was last used: the shelf lists recent works first
  } catch (e) { const off = navigator.onLine === false || await fetch('library/.ping?' + Date.now(), {cache: 'no-store'}).then(() => false, () => true);   // offline: not even a probe gets through
    toast(off ? T('इंटरनेट नहीं है — यह ग्रन्थ इस फ़ोनपर पहले खोला नहीं गया', 'No internet — this work has not been opened on this phone yet') : T('यह ग्रन्थ नहीं खुल सका', 'Could not open this work')); await coverOff(); return; }
  // from the library: the page shows now and the rest loads behind it. A quiet open (start, refresh, Back) keeps the cover until
  // the whole work is here, so the screen underneath (the library) never shows in between
  if (noShow){ await WREADY; await coverOff(); return; }
  await coverOff(); show('home');
  await WREADY;   // a caller that awaits openWork gets the whole work
}

/* ---------------- work home ---------------- */
function homeOrg(){ return WS().org || 'k'; }
// the work's title must fit the screen on one word per line even with the phone's text zoom: shrink it until it does
function fitTitle() {
  const h = $('#hTitle'); h.style.fontSize = ''; h.style.overflowWrap = 'normal';
  let fs = parseFloat(getComputedStyle(h).fontSize);
  while (h.scrollWidth > h.clientWidth + 1 && fs > 18) { fs -= 2; h.style.fontSize = fs + 'px'; }
  h.style.overflowWrap = '';
}
addEventListener('resize', () => { if ($('#hTitle') && $('#hTitle').offsetParent) fitTitle(); });
const VEDIC = /[\u0951\u0952\u1CD0-\u1CFF\uA8E0-\uA8FF]/;   // verses with svara marks are set in the Vedic font
function renderHome(){
  if (!W) return;
  $('#hTitle').textContent = TT(W.title); fitTitle(); $('#hSub').textContent = [TT(W.by), TT(W.from)].filter(Boolean).join(' · ');   // the author and, where there is one, the parent text — never the publisher or source
  // ▶ the whole work, start to end, across every part and recording
  const pa = $('#hPlayAll'), fa = firstAu(0, IT.length - 1); pa.hidden = fa == null; pa.onclick = () => playRange('k', 0, IT.length - 1);
  fixLast(); const L = WS().last, A = anchorOf() || (L && IT[L.i] ? {org: L.org, i: L.i} : null);
  // Resume: where you were reading (the reading anchor), named under the buttons; and the place before it, if you moved on
  $('#contCard').innerHTML = A ? '<button class="btn ghost cont" id="cGo">' + T('आगे पढ़ें', 'Resume') + ' ›</button>' : '';
  if ($('#cGo')) $('#cGo').onclick = () => { AN.going = true; openReader(A.org, A.i, true); };
  const prev = ((WS().prev || []).map(p => ID[p.id] != null && (p.org === 'k' || PLAN[p.org]) ? {org: p.org, i: ID[p.id]} : null).filter(p => p && (!A || p.i !== A.i)))[0];
  $('#contAt').innerHTML = A ? esc(T('पढ़ रहे थे: ', 'Reading: ') + itemLabel(A.i)) + (prev ? ' · <button class="lnk" id="cPrev">' + esc(T('उससे पहले: ', 'Before that: ') + itemLabel(prev.i)) + '</button>' : '') : '';
  $('#contAt').hidden = !A;
  if ($('#cPrev')) $('#cPrev').onclick = () => { AN.going = true; openReader(prev.org, prev.i, true); };
  const org = homeOrg();
  $('#orgSeg').innerHTML = '<button data-org="k">' + esc(TT(W.parts.name)) + '</button>' + PLANS.map(p => '<button data-org="' + p.id + '">' + esc(TT(p.name)) + '</button>').join('');
  $$('#orgSeg button').forEach(b => { b.classList.toggle('on', b.dataset.org === org); b.onclick = () => { WS().org = b.dataset.org; save(); renderHome(); }; });
  const play = (o, a, b) => firstAu(a, b) != null ? '<button class="lplay" data-po="' + o + '" data-pa="' + a + '" data-pb="' + b + '" aria-label="play"><svg><use href="#i-play"/></svg></button>' : '';
  let h = '';
  $('#orgSeg').hidden = !PLANS.length;   // a work without reading plans needs no switch
  if (org === 'k' && PARTS.length === 1){   // a single-part work (an āratī, a stotra): list its sections straight away
    const P = PARTS[0], ts = TOPICS.length || !W.sections ? TOPICS.slice() : PAGES.filter(p => SECN(p.s)).map(p => ({i: p.from, end: p.to})); if (!ts.length || ts[0].i > P.a) ts.unshift({i: P.a, end: ts.length ? ts[0].i - 1 : P.b});
    ts.forEach((t, n) => { const name = t.hi || t.en ? TNAME(t) : KNAME(P.k); h += '<li class="rowp">' + play('k', t.i, t.end) + '<button class="it" data-open="' + t.i + '"><span class="no">' + DEV(n + 1) + '</span><span class="grow"><span class="ti">' + esc(name) + '</span><br><span class="ds">' + esc(spanLabel(t.i, t.end)) + '</span></span><span class="chev">›</span></button></li>'; });
  }
  else if (org === 'k') PARTS.forEach(p => { const tps = TOPICS.filter(t => IT[t.i].p === p.k).length || (W.sections ? PAGES.filter(g => g.k === p.k && SECN(g.s)).length : 0);   /* its topics, else its named sections */ h += '<li class="rowp">' + play('k', p.a, p.b) + '<button class="it" data-open="' + p.a + '"><span class="no">' + DEV(p.k + 1) + '</span><span class="grow"><span class="ti">' + esc(KNAME(p.k)) + '</span><br><span class="ds">' + DEV(tps) + T(' प्रसंग', tps === 1 ? ' section' : ' sections') + '</span></span><span class="chev">›</span></button></li>'; });
  else { const P = PLAN[org]; const dn = Object.keys(DONE(ME(), org)).length; h += '<li class="pdone" aria-label="' + DEV(dn) + ' / ' + DEV(P.n) + T(' विश्राम पूर्ण', ' vishrams completed') + '"><span class="pdbar"><span style="width:' + Math.round(100 * dn / P.n) + '%"></span></span><span class="pdn">' + DEV(dn) + ' / ' + DEV(P.n) + '</span></li>';   // how much of the plan is done; a vishram's number marks it done
    // pages read before the first day and after the reading (pūrvāṅga / uttarāṅga), when the plan names them
    const page = (pg, when) => { const t = pg === 'aarti' ? T('श्रीरामायणजीकी आरती', 'Shri Ramayanji ki Aarti') : pg === 'visarjan' ? TT(W.vidhi.visarjan.title) : T('पारायण-विधि', 'Parayan vidhi'); if (pg === 'visarjan') when = T('पारायणके अन्तिम दिन', 'On the last day of the parayan'); return '<li class="rowp"><button class="it" data-page="' + pg + '"><span class="no pg"><svg><use href="#i-lamp"/></svg></span><span class="grow"><span class="ti">' + t + '</span><br><span class="ds">' + when + '</span></span><span class="chev">›</span></button></li>'; };
    (P.before || []).forEach(pg => h += page(pg, T('पाठसे पहले', 'Before the reading')));
    for (let n = 1; n <= P.n; n++){ const [a, b] = dayRange(org, n), d = DONE(ME(), org)[n], t = firstAu(a, b) != null ? durLabel(spanSecs(a, b)) : ''; h += '<li class="rowp"><button class="lmark" data-mark="' + n + '" aria-label="' + VN(n) + (d ? T(': पूर्ण — अपूर्ण करें', ': complete — mark not complete') : T(': पूर्ण करें', ': mark complete')) + '"></button>' + (t ? play(org, a, b).replace('class="lplay"', 'class="lplay timed"') + '<span class="ldur">' + t + '</span>' : play(org, a, b)) + '<button class="it" data-open="' + a + '"><span class="no' + (d ? ' done' : '') + '">' + (d ? '✓' : DEV(n)) + '</span><span class="grow"><span class="ti">' + VN(n) + '</span><br><span class="ds">' + rangeDesc(a, b) + '</span></span><span class="chev">›</span></button></li>'; }
    (P.after || []).forEach(pg => h += page(pg, T('पाठके बाद', 'After the reading'))); }
  $('#orgList').innerHTML = h;
  $$('#orgList [data-open]').forEach(b => b.onclick = () => openReader(org, +b.dataset.open));
  $$('#orgList [data-page]').forEach(b => b.onclick = () => { vidTab = b.dataset.page === 'vidhi' ? 'v' : b.dataset.page; show('vidhi'); });
  $$('#orgList [data-pa]').forEach(b => b.onclick = ev => { ev.stopPropagation(); playRange(b.dataset.po, +b.dataset.pa, +b.dataset.pb); });
  // a vishram's number: tap to mark it complete, tap again to mark it not complete (as “Mark vishram complete” at its end does)
  $$('#orgList [data-mark]').forEach(b => b.onclick = ev => { ev.stopPropagation(); const n = +b.dataset.mark, d = DONE(ME(), org); if (d[n]) delete d[n]; else d[n] = Date.now(); save(); renderHome();
    toast(VN(n) + (d[n] ? T(' पूर्ण — जय श्रीराम', ' complete — Jai Shri Ram') : T(' अपूर्ण किया', ' marked not complete'))); });
}
/* ⓘ About this work, under the title on the work's page: what the work is, so a reader
   can decide to read it. The shelf entry's introduction (library/index.json "intro": {hi: [paragraphs], en: [paragraphs]},
   written from the work's sources) comes first, else its one line ("desc"). On the work's page, the facts the library holds
   follow: language, length, listening time and reciter, the edition; from the library, a button opens the work. */
function workNode(id){ let r = null; (function walk(n){ (n || []).forEach(c => { if (c.work === id) r = c; else walk(c.children); }); })(LIB); return r || {}; }
function aboutWork(id){
  id = id || (W && W.id); if (!id) return; const nd = workNode(id), here = !!W && W.id === id && CURVIEW !== 'library';
  const intro = nd.intro ? [].concat(TT(nd.intro) || []) : nd.desc ? [TT(nd.desc)] : [];
  const by = here ? [TT(W.by), TT(W.from)] : [TT(nd.by)];
  let facts = '';
  if (here){
    const row = (k, v) => v ? '<dt>' + k + '</dt><dd>' + esc(v) + '</dd>' : '';
    const n = BYPART() ? 0 : IT.length, len = n ? DEV(n) + T(' पद', ' verses') : '';
    const au = SRC.au && firstAu(0, IT.length - 1) != null ? durLabel(spanSecs(0, IT.length - 1)) + ' · ' + TT(SRC.au.meta.title) : '';
    facts = '<dl>' + row(T('भाषा', 'Language'), LANGS[W.lang] ? TT(LANGS[W.lang].name) : '') + row(T('विस्तार', 'Length'), len) + row(T('सुनें', 'Listen'), au) + row(T('पाठ', 'Text'), TT(W.edition)) + '</dl>';
  }
  openSheet('<div class="about"><h2>' + esc(TT(nd.title || (W && W.title))) + '</h2>' + (by.some(Boolean) ? '<p class="muted small">' + esc(by.filter(Boolean).join(' · ')) + '</p>' : '')
    + intro.map(p => '<p>' + esc(p) + '</p>').join('') + facts
    + (here ? '' : '<div class="acts"><button class="btn" id="abOpen">' + T('पढ़ें', 'Open') + ' ›</button></div>') + '</div>');
  if ($('#abOpen')) $('#abOpen').onclick = () => { closeSheet(); openWork(id); };
}
$('#hAbout').onclick = () => aboutWork();
$('#hLib').onclick = () => { libPath = []; show('library'); };   // “‹ Library” goes to the library itself, not the shelf last visited
$('#hMenu').onclick = mainMenu;

/* ---------------- search ---------------- */
let IDX = null;
const normD = s => (s || '').normalize('NFC').replace(/[ँं़‌‍ऽ]/g, '').replace(/\s+/g, ' ');
const normL = s => (s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/r̥/g, 'r');
// Search forgives spelling: both the text and what is typed are folded to a sound key, so letters people use for one
// another count as one. Devanagari (and Gurmukhi, read as Devanagari): ि/ी, ु/ू, ब/व, श/ष/स, ण/न, ृ/रि, ै/अइ, ौ/अउ, a nasal
// before a consonant, ँ ं ़ ् and Vedic accents. Roman: long vowels, aspiration (bh = b), sh/s, ch/c, v/w/b, f/p, z/j, a nasal
// before a consonant, a word's final a. Both: a word's final u (Tulsīdās's तनु धनु धामु, काजु for तन धन धाम, काज). Then a verse is found by the words typed, with spaces ignored and about one letter in six
// allowed to differ, anywhere in it; or, failing that, by most of the words typed, in any order.
const GUR = s => s.replace(/[਀-੿]/g, c => c === 'ੰ' ? 'ं' : c === 'ੱ' ? '' : c === 'ੵ' ? '्य' : String.fromCharCode(c.charCodeAt(0) - 0x100));
const fD = s => GUR((s || '').normalize('NFC')).normalize('NFD').replace(/[ङञणनम]्(?=[क-ह])/g, '').replace(/[॑-॔᳐-᳿꣠-ꣿँं़‌‍ऽ्]/g, '')
  .replace(/[ीूईऊवशषणृऋैौऐऔॉ]/g, c => ({'ी': 'ि', 'ू': 'ु', 'ई': 'इ', 'ऊ': 'उ', 'व': 'ब', 'श': 'स', 'ष': 'स', 'ण': 'न', 'ृ': 'रि', 'ऋ': 'रि', 'ै': 'इ', 'ौ': 'उ', 'ऐ': 'अइ', 'औ': 'अउ', 'ॉ': 'ो'})[c])
  .replace(/[^ऀ-ॿ]+/g, ' ').replace(/[।॥०-९]/g, ' ').trim().split(/\s+/).filter(Boolean).map(w => w.length > 2 ? w.replace(/ु$/, '') : w);
const fL = s => normL((s || '').normalize('NFD').replace(/m[̇̐]/g, 'n')).replace(/[^a-z]+/g, ' ')
  .replace(/(aa|ee|ii|oo|uu)/g, m => ({aa: 'a', ee: 'i', ii: 'i', oo: 'u', uu: 'u'})[m]).replace(/([bcdgjkptsr])h/g, '$1').replace(/[vw]/g, 'b').replace(/f/g, 'p').replace(/z/g, 'j').replace(/q/g, 'k')
  .replace(/ri/g, 'r').replace(/[nm](?=[bcdgjklpqrstxyz])/g, '').trim().split(/\s+/).filter(Boolean).map(w => w.length > 2 ? w.replace(/[au]$/, '') : w);
let ROW0 = new Int32Array(256), ROW1 = new Int32Array(256);
// the fewest letters to change, add or drop for p to appear somewhere in t (more than k: k + 1)
function near(p, t, k){
  if (t.includes(p)) return 0; if (!k) return 1;
  const n = t.length; if (ROW0.length <= n){ ROW0 = new Int32Array(n + 1); ROW1 = new Int32Array(n + 1); }
  let prev = ROW0, cur = ROW1; prev.fill(0, 0, n + 1);
  for (let i = 1; i <= p.length; i++){
    const c = p.charCodeAt(i - 1); cur[0] = i; let lo = i;
    for (let j = 1; j <= n; j++){ let v = prev[j - 1] + (c === t.charCodeAt(j - 1) ? 0 : 1); if (prev[j] + 1 < v) v = prev[j] + 1; if (cur[j - 1] + 1 < v) v = cur[j - 1] + 1; cur[j] = v; if (v < lo) lo = v; }
    if (lo > k) return k + 1; const x = prev; prev = cur; cur = x;
  }
  let m = k + 1; for (let j = 0; j <= n; j++) if (prev[j] < m) m = prev[j]; return m;
}
const ed1 = (a, b) => { if (Math.abs(a.length - b.length) > 1) return false; let i = 0; while (i < a.length && a[i] === b[i]) i++; return a.slice(i + 1) === b.slice(i + 1) || a.slice(i) === b.slice(i + 1) || a.slice(i + 1) === b.slice(i); };
// how many of the words typed a text's words hold: whole (1), as the start of a word (0.9), one letter apart (0.8) or inside
// a joined word (0.7: दीन दयाल in दीनदयाल)
const wordsIn = (qs, ws) => qs.reduce((n, q) => n + (ws.includes(q) ? 1 : q.length >= 3 && ws.some(w => w.startsWith(q)) ? .9 : q.length >= 4 && ws.some(w => ed1(q, w)) ? .8 : q.length >= 3 && ws.some(w => w.includes(q)) ? .7 : 0), 0);
const idxKey = () => W.id + MK().map(k => (SRC[k] || {}).id).join('|');
// one search scope per meaning language (h, e, and the code of any other: pa); Latin script is searched as Latin
function buildIdx(){ IDX = IT.map((it, i) => { const h = SRC.hi && SRC.hi.m[it.id], e = SRC.en && SRC.en.m[it.id], vw = fD(it.v.join(' ')), tw = fL((it.t || []).join(' ')), r = {vw, v: vw.join(''), tw, t: tw.join(''), h: fD(h ? h[0] : '').join(' '), e: normL(e ? e[0] : '')};
  MK().forEach(k => { if (k !== 'hi' && k !== 'en'){ const x = SRC[k] && SRC[k].m[it.id]; r[k] = fD(x ? x[0] : '').join(' '); } }); return r; }); IDX.w = idxKey(); }
const scopes = new Set(['v', 'h', 'e', 'n', 'pa']);
$$('#scope .chip').forEach(c => c.onclick = () => { const s = c.dataset.s; if (scopes.has(s)) scopes.delete(s); else scopes.add(s); c.classList.toggle('on'); runSearch(); });
let sT; $('#q').addEventListener('input', () => { clearTimeout(sT); sT = setTimeout(runSearch, 250); });
function snip(text, q, latin){ const src = text; const low = latin ? normL(src) : normD(src); const nq = latin ? normL(q) : normD(q); let p = low.indexOf(nq); if (p < 0) return esc(src.slice(0, 160)) + (src.length > 160 ? '…' : ''); let a = Math.max(0, p - 60), b = Math.min(src.length, p + nq.length + 80); if (a > 0){ const sp = src.indexOf(' ', a); if (sp > -1 && sp < p) a = sp + 1; } const s = src.slice(a, b); const pp = (latin ? normL(s) : normD(s)).indexOf(nq); let out; if (pp >= 0 && (latin ? normL(s) : normD(s)).length === s.length) out = esc(s.slice(0, pp)) + '<mark>' + esc(s.slice(pp, pp + nq.length)) + '</mark>' + esc(s.slice(pp + nq.length)); else out = esc(s); return (a > 0 ? '…' : '') + out + (b < src.length ? '…' : ''); }
// A number typed into a work's search finds by number. In a work counted by dohas (the Manas, its kands), the doha is the main
// counter and the chaupais count again under each: "45" (or "दोहा ४५") finds Doha 45 in each part, "45.3" (or "45 3") Chaupai 3
// under Doha 45. In a work without dohas (a stotra, an Upanishad), a number finds the verse of that number.
function numQuery(q){
  const d = q.replace(/[०-९]/g, c => '०१२३४५६७८९'.indexOf(c)).toLowerCase().replace(/^(dohā|doha|dohe|दोहा|दोहे|soraṭhā|soratha|सोरठा)\s*/, '').trim();
  const m = /^(\d{1,4})(?:\s*[.\/:,\s]\s*(\d{1,3}))?$/.exec(d); return m ? [+m[1], m[2] ? +m[2] : null] : null;
}
function numHits([N, M], hits){
  const v = i => (IT[i].v || []).map(l => l.trim()).join(' '), add = i => hits.push([hits.length, i, LB.verses(), v(i), false]);
  if (PAGES.some(p => isNum(p.s))){
    for (const p of PAGES){ if (!isNum(p.s) || +p.s !== N) continue; let i = -1;
      if (M != null){ for (let j = p.from; j <= p.to; j++) if (IT[j].y === 'cau' && parseInt(IT[j].n, 10) === M){ i = j; break; } }
      else { for (let j = p.to; j >= p.from; j--) if (IT[j].y === 'do' || IT[j].y === 'so'){ i = j; break; } if (i < 0) i = p.to; }
      if (i >= 0) add(i); }
  } else IT.forEach((it, i) => { if (parseInt(it.n, 10) === N) add(i); });
}
function runSearch(){
  if (SCOPE === 'lib'){ const q = $('#q').value; if (q.trim()) libSearch(q); else openSearch('lib', true); return; }
  if (!wReady){ WREADY.then(runSearch); return; }   // searching a work needs its meanings
  const q = $('#q').value.trim(), box = $('#sRes'), num = numQuery(q);
  if (q.length < 2 && !num){ box.innerHTML = '<div class="empty">' + T('कम-से-कम दो अक्षर लिखें।', 'Type at least two letters.') + '</div>'; return; }
  if (!IDX || IDX.w !== idxKey()) buildIdx();
  if (BYPART() && PARTS.some(P => !partReady(P.k))) searchParts(); const loading = SLOADING;   // the meanings of the parts not in yet
  const latin = /[a-zA-Z]/.test(q), nq = latin ? normL(q) : normD(q);
  const qs = latin ? fL(q) : fD(q), qj = qs.join(''), k = Math.floor(qj.length / 6), need = qs.length >= 3 ? qs.length - Math.max(1, Math.floor(qs.length / 3)) : qs.length;   // most words: all of two, all but one of three to five, then two in three
  // verses whose letters hold what was typed (closest first), then meanings that do, then texts holding most of its words
  const ew = latin ? nq.split(/\s+/).filter(Boolean) : [], meanK = MK().filter(k => k !== 'hi' && k !== 'en' && scopes.has(k)), hits = [];
  const mean = (x, words) => { const qm = qs.join(' '); if (!latin){ if (scopes.has('h') && (words ? wordsIn(qs, x.h.split(' ')) >= need : x.h.includes(qm))) return ['h', LB.h(), SRC.hi.m[IT[x.i].id][0], false];
      for (const m of meanK) if (x[m] && (words ? wordsIn(qs, x[m].split(' ')) >= need : x[m].includes(qm))) return [m, LBM(m), SRC[m].m[IT[x.i].id][0], false]; }
    else if (scopes.has('e') && x.e && (words ? ew.every(w => x.e.includes(w)) : x.e.includes(nq))) return ['e', LB.e(), SRC.en.m[IT[x.i].id][0], true];
    return null; };
  if (num){ numHits(num, hits); }   // a number: the doha of that number (or a chaupai under it), not the digits in the text
  else if (qj) for (let i = 0; i < IT.length; i++){
    const x = IDX[i]; x.i = i; const vt = latin ? x.t : x.v, vw = latin ? x.tw : x.vw;
    // a near match that holds few of the words typed is chance; among matches as near, the one holding more words comes first
    if (scopes.has('v') && vt){ const d = near(qj, vt, k), sc = d <= k && qs.length > 1 ? wordsIn(qs, vw) : 1; if (d <= k && (d === 0 || qs.length < 2 || sc >= qs.length / 2)){ hits.push([d - sc / 100, i, LB.verses(), IT[i].v.join(' । '), false]); continue; } }
    const m = mean(x, false); if (m){ hits.push([k + 1, i, m[1], m[2], m[3]]); continue; }
    const sc = qs.length >= 2 && scopes.has('v') && vw.length ? wordsIn(qs, vw) : 0; if (sc && sc >= need - .25){ hits.push([k + 3 - sc / 100, i, LB.verses(), IT[i].v.join(' । '), false]); continue; }
    const w = qs.length >= 2 && mean(x, true); if (w) hits.push([k + 4, i, w[1], w[2], w[3]]);
  }
  hits.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  const res = hits.slice(0, 300).map(h => h.slice(1));
  if (scopes.has('n')) for (const p of SHOWN()) for (const k in p.notes){ if (!k.startsWith(W.id + ':')) continue; const i = ID[k.slice(W.id.length + 1)]; if (i == null) continue; p.notes[k].forEach(n => { if ((latin ? normL(n.t) : normD(n.t)).includes(nq)) res.push([i, T('टिप्पणी', 'Note'), n.t, latin]); }); }
  box.innerHTML = (loading ? '<p class="small muted sload">' + T('सभी भागोंके अर्थ खोजे जा रहे हैं…', 'Searching the meanings of every part…') + '</p>' : '') + (res.length ? '<p class="small muted">' + DEV(res.length) + (res.length >= 300 ? '+' : '') + T(' परिणाम', ' results') + '</p>' + res.map(r => '<button class="res" data-i="' + r[0] + '"><div class="where">' + esc(itemLabel(r[0])) + ' · ' + esc(r[1]) + '</div><div class="snip' + (r[3] ? ' lat' : '') + '">' + snip(r[2], q, r[3]) + '</div></button>').join('') : '<div class="empty">' + T('कुछ नहीं मिला। दूसरा रूप लिखकर देखें।', 'Nothing found. Try another spelling.') + '</div>');
  $$('#sRes .res').forEach(b => b.onclick = () => openReader(readOrg(), +b.dataset.i, true));
}

/* ---------------- bookmarks ---------------- */
function renderBookmarks(){
  const bms = [], notes = [], pre = W.id + ':';
  for (const p of SHOWN()){ for (const k in p.bm) if (k.startsWith(pre) && ID[k.slice(pre.length)] != null) bms.push([ID[k.slice(pre.length)], p]); for (const k in p.notes) if (k.startsWith(pre) && ID[k.slice(pre.length)] != null) p.notes[k].forEach(n => notes.push([ID[k.slice(pre.length)], p, n])); }
  bms.sort((a, b) => a[0] - b[0]); notes.sort((a, b) => a[0] - b[0]);
  // each list folds under its heading: open by default, and a fold is remembered
  const fold = S.settings.bmFold || {}, sec = (key, title, body) => '<details class="bmsec" data-fold="' + key + '"' + (fold[key] ? '' : ' open') + '><summary><h2>' + title + '</h2></summary>' + body + '</details>';
  let h = '', bmh = '';
  // each bookmark has its own ✕ to remove it
  bmh += bms.length ? bms.map(b => '<div class="bmrow"><button class="res" data-i="' + b[0] + '"><div class="where">' + esc(itemLabel(b[0])) + '</div><div class="snip" style="font-weight:700">' + esc(IT[b[0]].v[0]) + '</div></button><button class="bmdel" data-del="' + b[0] + '" aria-label="' + T('बुकमार्क हटाएँ', 'Remove bookmark') + '"><svg><use href="#i-x"/></svg></button></div>').join('') : '<p class="muted">' + T('किसी भी पदके पास बुकमार्क चिह्न दबाएँ।', 'Tap the bookmark sign beside any verse.') + '</p>';
  h += sec('bm', T('बुकमार्क (', 'Bookmarks (') + DEV(bms.length) + ')', bmh);
  h += sec('notes', T('टिप्पणियाँ (', 'Notes (') + DEV(notes.length) + ')', notes.length ? notes.map(n => '<button class="res" data-i="' + n[0] + '"><div class="where">' + esc(itemLabel(n[0])) + '</div><div class="snip">' + esc(n[2].t.slice(0, 200)) + '</div></button>').join('') : '<p class="muted">' + T('किसी पदके ⋮ मेनूसे अपनी टिप्पणी लिखें।', 'Use the ⋮ menu of any verse to write a note.') + '</p>');
  h += '<h2 style="font-size:19px;margin:26px 0 4px">' + T('मेरी फ़ाइल', 'My file') + '</h2><p class="small muted">' + T('आपके बुकमार्क, टिप्पणियाँ, प्रगति और सुधार इसी फ़ोनमें रहते हैं। फ़ाइल सेव करके बैकअप रखें या दूसरे फ़ोनपर खोलें।', 'Your bookmarks, notes, progress and corrections stay on this phone. Save the file as a backup, or open it on another phone.') + (canStore ? '' : ' <b>' + T('ध्यान दें: यह फ़ोन डेटा अपने-आप नहीं रख पा रहा — पाठके बाद “फ़ाइल सेव करें” दबाएँ।', 'This phone is not keeping app data — tap Save my file after each reading.') + '</b>') + '</p>' +
    '<div class="acts"><button class="btn" id="exp">' + T('फ़ाइल सेव करें', 'Save my file') + '</button><button class="btn ghost" id="imp">' + T('फ़ाइल खोलें', 'Open a file') + '</button></div>';
  $('#bmBody').innerHTML = h + '<div style="height:40px"></div>';
  $('#exp').onclick = exportFile; $('#imp').onclick = () => $('#fileIn').click();
  $$('#bmBody .bmsec').forEach(d => d.ontoggle = () => { S.settings.bmFold = S.settings.bmFold || {}; if (d.open) delete S.settings.bmFold[d.dataset.fold]; else S.settings.bmFold[d.dataset.fold] = 1; save(); });
  $$('#bmBody .res').forEach(b => b.onclick = () => openReader(readOrg(), +b.dataset.i, true));
  $$('#bmBody [data-del]').forEach(b => b.onclick = () => { const k = KEY(IT[+b.dataset.del].id); for (const p of S.profiles) delete p.bm[k]; save(); renderBookmarks(); toast(T('बुकमार्क हटाया', 'Bookmark removed')); });
}

/* ---------------- settings ---------------- */
// "Meanings in the bar": which two meaning switches the header capsule shows, for a work with more than two meaning languages
function pairPick(){ if (!W || workKinds().filter(k => k !== 'hi' && k !== 'en').length === 0) return ''; const cur = capKinds().join(','), nm = k => (LANGS[k].meaning || {}).short || k;
  return '<div class="field"><label>' + T('बारमें अर्थ', 'Meanings in the bar') + '</label><select id="sPair">' + pairOptions().map(p => '<option value="' + p.join(',') + '"' + (p.join(',') === cur ? ' selected' : '') + '>' + p.map(nm).join(' · ') + '</option>').join('') + '</select></div>'; }
function renderSettings(){   // the "More settings" page: the rare things only — transliteration, sources, audio timing, privacy
  const cur = S.src[W ? W.id : ''] || {};
  const pick = (kind, label, off) => { const list = W ? srcList(kind) : []; if (!list.length) return ''; const sel = cur[kind] || list[0].id; return '<div class="field"><label>' + label + '</label><select data-src="' + kind + '">' + list.map(s => '<option value="' + s.id + '"' + (sel === s.id ? ' selected' : '') + '>' + esc(TT(s.title)) + (s.draft ? T(' (जाँच बाकी)', ' (to be checked)') : '') + '</option>').join('') + (off ? '<option value="off"' + (sel === 'off' ? ' selected' : '') + '>' + T('बंद', 'Off') + '</option>' : '') + '</select></div>'; };
  let h = '<h2>' + T('पढ़ना', 'Reading') + '</h2>' + sw('str', LB.tr(), LB.trSub(), S.settings.tr) + sw('slines', LB.lines(), LB.linesSub(), S.settings.lines) +
    (W ? '<h2>' + LB.src() + ' · ' + esc(TT(W.title)) + '</h2>' + MK().map(k => pick(k, LBM(k))).join('') + pairPick() + pick('au', LB.au(), true) : '') +
    timingHTML() +
    '<h2>' + T('सहायता', 'Help') + '</h2><div class="acts"><a class="btn ghost" href="privacy.html" target="_blank" rel="noopener">' + T('गोपनीयता', 'Privacy') + '</a></div>' +
    '<div style="height:50px"></div>';
  $('#setBody').innerHTML = h;
  $('#str').onchange = e => { S.settings.tr = e.target.checked; save(); };   // seen in the reader on the next open
  $('#slines').onchange = e => { S.settings.lines = e.target.checked; save(); };
  bindTiming();
  if ($('#sPair')) $('#sPair').onchange = e => { S.settings.pair = e.target.value; save(); syncLayers(); toast(T('बार बदला', 'Bar changed')); };
  $$('[data-src]').forEach(s => s.onchange = async () => { const c = S.src[W.id] = S.src[W.id] || {}; c[s.dataset.src] = s.value; save(); if (s.dataset.src === 'au') stopAudio(); await loadSources(); IDX = null; toast(T('स्रोत बदला', 'Source changed')); });
}
/* timing review: ☰ › More settings › Audio timing. While it is on, each verse shows its times and “Starts now” / “Ends now” (markBar), and the player bar the ± step;
   recordings still being checked (drafts) can be played. Starts set by ear go to the library through a GitHub issue, which
   the workflow .github/workflows/timing.yml applies (tools/audio/apply_owner_timing.py). */
function pendingStarts(){ if (!SRC.au) return {}; const fx = myStarts(), sent = S.timing.sent[tkey()] || {}, out = {}; for (const id in fx) if (ID[id] != null && !fromOf(id) && JSON.stringify(sent[id]) !== JSON.stringify(fx[id])) out[id] = fx[id]; return out; }
function timingHTML(){
  if (!W) return '';
  let h = '<h2>' + T('ऑडियोका समय', 'Audio timing') + '</h2>' + sw('stm', T('ऑडियोका समय', 'Audio timing'), T('ऑडियो और पदका मेल ठीक करें', 'Fix audio and verse mismatches'), S.timing.on) +
    sw('stf', T('समय जाँचें', 'Review timing'), T('झंडा दबानेसे पद जाँच-सूचीमें जुड़ता है', 'Tapping the flag adds a verse to the checklist'), !!S.timing.flagsOn);
  if (S.timing.on && SRC.au){
    const n = Object.keys(myStarts()).filter(id => ID[id] != null).length, p = Object.keys(pendingStarts()).length;
    h += (SRC.au.meta.draft ? sw('stp', T('यह रिकॉर्डिंग जाँच ली — सबके लिये चालू करें', 'This recording is checked: publish it for everyone'), (Object.keys(pendingStarts()).length > SEND_MAX ? T('भेजनेके अन्तिम भागके साथ जाएगा', 'Goes with the last part of the send') : T('भेजनेके साथ जाएगा', 'Goes with the next send')), !!(S.timing.publish || {})[tkey()]) : '') +
      checkList() + helperList() +
      '<p class="small" style="margin:14px 0 8px">' + esc(TT(SRC.au.meta.title)) + ': ' + (n ? DEV(n) + T(' पदोंका समय आपने रखा', ' verses timed by you') : T('अभी आपने कोई समय नहीं रखा', 'none timed by you yet')) + (p ? ' · ' + DEV(p) + T(' प्रकाशित करने बाकी', ' to publish') : '') + '</p>' +
      '<div class="acts"><button class="btn" id="tSend"' + (p || (S.timing.publish || {})[tkey()] ? '' : ' disabled') + '>' + T('बदलाव प्रकाशित करें', 'Publish changes') + (p > SEND_MAX ? '<br><small>' + T('भाग १, कुल ', 'part 1 of ') + DEV(Math.ceil(p / SEND_MAX)) + T(' — फिर दोबारा दबाएँ', ' — then tap again') + '</small>' : '') + '</button><button class="btn ghost" id="tSave"' + (n ? '' : ' disabled') + '>' + T('सेव करें', 'Save') + '</button><button class="btn ghost" id="tOpen">' + T('खोलें', 'Open') + '</button>' + (n ? '<button class="btn ghost" id="tClear">' + T('रीसेट', 'Reset') + '</button>' : '') + '</div>' +
      '<p class="small muted">' + T('सहायता कर रहे हैं? “सेव करें” दबाकर फ़ाइल साइटके मालिकको भेजें; वे जाँचकर लाइब्रेरीमें जोड़ेंगे। सीधे प्रकाशित केवल मालिक कर सकते हैं।', 'Helping? Tap “Save” and send the file to the site’s owner, who checks it and adds it to the library. Only the owner can publish directly.') + '</p>';
  }
  return h;
}
function checkList(){
  const ids = [...new Set([...[...((SRC.au && SRC.au.checkSet) || [])].filter(id => !myStarts()[id]), ...FLAGGED])].filter(id => ID[id] != null).sort((a, b) => ID[a] - ID[b]); if (!ids.length) return '<p class="small muted">' + T('जाँचने लायक कोई पद नहीं बचा।', 'Nothing left to check.') + '</p>';
  return '<details class="tcheck"><summary>' + T('जाँचने हैं: ', 'To check: ') + DEV(ids.length) + T(' पद', ' verses') + '</summary><div class="tlist">' + ids.slice(0, 400).map(id => '<button data-go-i="' + ID[id] + '">' + esc(itemLabel(ID[id])) + ' <span class="muted">' + fmtT(SRC.au.at[id][1]) + '</span></button>').join('') + '</div></details>';
}
// marks loaded from helpers' files that you have not checked yet
function helperList(){
  const f = S.timing.from[tkey()] || {}, ids = Object.keys(f).filter(id => ID[id] != null).sort((a, b) => ID[a] - ID[b]); if (!ids.length) return '';
  const names = [...new Set(ids.map(id => f[id]))].map(esc).join(', ');
  return '<details class="tcheck" open><summary>' + names + T(' के ', ': ') + DEV(ids.length) + T(' पद जाँचने बाकी — हर पदके नीचे ▶ से सुनकर “✓ सही है” दबाएँ; जाँचे हुए ही लाइब्रेरीमें जाएँगे', ' verses still to check — play each with ▶ under it and tap “✓ Correct”; only checked ones go to the library') + '</summary><div class="tlist">' + ids.slice(0, 400).map(id => '<button data-go-i="' + ID[id] + '">' + esc(itemLabel(ID[id])) + ' <span class="muted">' + fmtT(SRC.au.at[id][1]) + '</span></button>').join('') + '</div><div class="acts"><button class="btn ghost small" id="tOkAll">' + T('सब सही हैं', 'All are correct') + '</button><button class="btn ghost small" id="tDropAll">' + T('ये सब हटाएँ', 'Remove these') + '</button></div></details>';
}
function clearTimingAsk(){ askYes(T('“' + esc(TT(W.title)) + '” की “' + esc(TT(SRC.au.meta.title)) + '” रिकॉर्डिंगमें इस फ़ोनपर आपके सेट किये सारे समय हट जाएँगे। जो लाइब्रेरीमें भेज चुके हैं, वे वहाँ रहेंगे। दूसरे पाठ, दूसरी रिकॉर्डिंग और आपकी पढ़ाईकी प्रगति वैसी ही रहेगी।', 'All the timings you set on this phone for the recording “' + esc(TT(SRC.au.meta.title)) + '” of “' + esc(TT(W.title)) + '” will be removed. Those already sent to the library stay there. Other works, other recordings and your reading progress are not touched.'), T('हाँ, हटाएँ', 'Yes, remove'), () => { delete S.timing.fix[tkey()]; delete S.timing.sent[tkey()]; delete S.timing.from[tkey()]; save(); buildAudio(); renderSettings(); }); }
function bindTiming(){
  $$('[data-go-i]').forEach(b => b.onclick = () => openReader('k', +b.dataset.goI, true));
  if (!$('#stm')) return;
  $('#stm').onchange = async e => { S.timing.on = e.target.checked; save(); applyTiming(); stopAudio(); await loadSources(); renderSettings(); };
  if ($('#stf')) $('#stf').onchange = e => { S.timing.flagsOn = e.target.checked; save(); renderSettings(); };
  if ($('#stp')) $('#stp').onchange = e => { S.timing.publish = S.timing.publish || {}; if (e.target.checked) S.timing.publish[tkey()] = true; else delete S.timing.publish[tkey()]; save(); renderSettings(); };
  if ($('#tClear')) $('#tClear').onclick = clearTimingAsk;
  if ($('#tSend')) $('#tSend').onclick = sendStarts;
  if ($('#tSave')) $('#tSave').onclick = saveTimingFile;
  if ($('#tOpen')) $('#tOpen').onclick = () => $('#fileIn').click();
  if ($('#tOkAll')) $('#tOkAll').onclick = () => askYes(T('सहायकके सारे समय बिना सुने आपके माने जाएँगे और अगली बार लाइब्रेरीमें भेजे जाएँगे।', 'All the helper’s times will count as yours without hearing them, and go with your next send.'), T('हाँ, सब सही हैं', 'Yes, all correct'), () => { delete S.timing.from[tkey()]; save(); renderSettings(); });
  if ($('#tDropAll')) $('#tDropAll').onclick = () => askYes(T('सहायकके जो समय आपने अभी नहीं जाँचे, वे हट जाएँगे।', 'The helper’s times you have not checked will be removed.'), T('हाँ, हटाएँ', 'Yes, remove'), () => { const f = S.timing.from[tkey()] || {}, fx = myStarts(); Object.keys(f).forEach(id => delete fx[id]); delete S.timing.from[tkey()]; if (!Object.keys(fx).length) delete S.timing.fix[tkey()]; save(); buildAudio(); renderSettings(); });
}
// a helper saves their marks to a file and sends it to the owner (on a phone, the share sheet: WhatsApp, e-mail…)
function timingDoc(by){
  const fx = myStarts(), starts = {};
  Object.keys(fx).filter(id => ID[id] != null).sort((a, b) => ID[a] - ID[b]).forEach(id => { const [t, sec, end] = fx[id], yt = SRC.au.tracks[t].yt; (starts[yt] = starts[yt] || {})[id] = end != null ? [sec, end] : sec; });
  return {kind: 'scriptures-timing', path: W.path, work: TT(W.title), source: SRC.au.meta.id, recording: TT(SRC.au.meta.title), by, made: new Date().toISOString(), starts};
}
function saveTimingFile(){
  if (!Object.keys(myStarts()).length) return;
  askText(T('आपका नाम (ताकि मालिक जानें किसने किया)', 'Your name (so the owner knows who did this)'), S.timing.name || (ME() || {}).name || '', async name => {
    S.timing.name = name; save();
    const text = JSON.stringify(timingDoc(name), null, 1), fname = 'timing-' + W.id + '-' + SRC.au.meta.id + '-' + todayStr() + '.json';
    try { const file = new File([text], fname, {type: 'application/json'}); if (navigator.canShare && navigator.canShare({files: [file]})){ await navigator.share({files: [file], title: fname}); return; } } catch (e) { if (e && e.name === 'AbortError') return; }
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], {type: 'application/json'})); a.download = fname; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1500);
    toast(T('फ़ाइल डाउनलोडमें सेव हुई — इसे मालिकको भेजें', 'File saved to Downloads — send it to the owner'));
  });
}
// the owner opens a helper's file: checked against this work and recording, then loaded as marks "from <helper>" to check
async function importTiming(X){
  if (!W || W.path !== X.path){ toast(T('यह फ़ाइल “', 'This file is for “') + (X.work || X.path) + T('” की है — पहले वह पाठ खोलें', '” — open that work first')); return; }
  if (!S.timing.on){ S.timing.on = true; save(); applyTiming(); }
  if (!SRC.au || SRC.au.meta.id !== X.source){
    if (!srcList('au').some(s => s.id === X.source)){ toast(T('इस फ़ाइलकी रिकॉर्डिंग इस पाठमें नहीं है', 'This file’s recording is not in this work')); return; }
    (S.src[W.id] = S.src[W.id] || {}).au = X.source; save(); stopAudio(); await loadSources();
  }
  buildAudio();
  const tr = {}; SRC.au.tracks.forEach((t, k) => { tr[t.yt] = k; });
  const got = {}; let bad = 0;
  for (const yt in (X.starts || {})) for (const id in X.starts[yt]){
    const v = X.starts[yt][id], s = Array.isArray(v) ? v[0] : v, e = Array.isArray(v) ? v[1] : null, t = tr[yt], tk = SRC.au.tracks[t], i = ID[id];
    const ok = t != null && i != null && i >= tk.fi && i <= tk.li && typeof s === 'number' && isFinite(s) && s >= 0 && (!tk.dur || s < tk.dur) && (e == null || (typeof e === 'number' && isFinite(e) && e > s));
    if (ok) got[id] = [t, Math.round(s * 10) / 10, e == null ? null : Math.round(e * 10) / 10]; else bad++;
  }
  const mine = myStarts(), ids = Object.keys(got), nw = ids.filter(id => !mine[id]), diff = ids.filter(id => mine[id] && JSON.stringify(mine[id]) !== JSON.stringify(got[id]));
  const who = esc(String(X.by || T('सहायक', 'a helper')).slice(0, 40));
  openSheet('<h2>' + T('सहायककी फ़ाइल', 'A helper’s file') + '</h2><p><b>' + who + '</b> · ' + esc(TT(SRC.au.meta.title)) + (X.made ? ' · ' + esc(String(X.made).slice(0, 10)) : '') + '</p><p class="small">' +
    DEV(ids.length) + T(' पद: ', ' verses: ') + DEV(nw.length) + T(' नये', ' new') + ' · ' + DEV(diff.length) + T(' आपके समयसे अलग', ' different from yours') + ' · ' + DEV(ids.length - nw.length - diff.length) + T(' आपके जैसे', ' the same as yours') + (bad ? ' · ' + DEV(bad) + T(' गलत, छोड़ दिये', ' not valid, skipped') : '') + '</p>' +
    '<p class="small muted">' + T('ये पदोंके नीचे “', 'They show under each verse as “from ') + who + T(' का — जाँचें” दिखेंगे। ▶ से सुनकर “✓ सही है” दबाएँ, या ⏱ से ठीक करें। जाँचे हुए ही लाइब्रेरीमें जाएँगे।', ' — to check”. Play each with ▶ and tap “✓ Correct”, or fix it with ⏱. Only checked ones go to the library.') + '</p>' +
    '<div class="menu">' + (nw.length + diff.length ? '<button id="tiAll">' + T('ले आएँ', 'Load them') + (diff.length ? '<br><small class="muted">' + T('जहाँ अलग हैं वहाँ आपके समयकी जगह', 'replacing yours where they differ') + '</small>' : '') + '</button>' : '') + (diff.length && nw.length ? '<button id="tiNew">' + T('केवल नये', 'Only the new ones') + '<br><small class="muted">' + T('आपके समय वैसे ही रहेंगे', 'yours stay as they are') + '</small></button>' : '') + '<button id="tiNo">' + T('रहने दें', 'Cancel') + '</button></div>');
  const load = list => { const fx = S.timing.fix[tkey()] = S.timing.fix[tkey()] || {}, fr = S.timing.from[tkey()] = S.timing.from[tkey()] || {}; list.forEach(id => { fx[id] = got[id]; fr[id] = String(X.by || T('सहायक', 'helper')).slice(0, 40); }); save(); buildAudio(); closeSheet(); toast(DEV(list.length) + T(' पद जाँचनेके लिये आये', ' verses loaded to check')); renderSettings(); };
  if ($('#tiAll')) $('#tiAll').onclick = () => load(nw.concat(diff));
  if ($('#tiNew')) $('#tiNew').onclick = () => load(nw);
  $('#tiNo').onclick = () => closeSheet();
}
const SEND_MAX = 150;   // verses in one GitHub issue (a longer link is refused); more go in further sends
function sendStarts(){
  const pend = pendingStarts(), ids = Object.keys(pend).sort((a, b) => ID[a] - ID[b]), part = ids.slice(0, SEND_MAX), starts = {};
  part.forEach(id => { const [t, sec, end] = pend[id], yt = SRC.au.tracks[t].yt; (starts[yt] = starts[yt] || {})[id] = end != null ? [sec, end] : sec; });
  const last = ids.length <= SEND_MAX, pub = last && !!(S.timing.publish || {})[tkey()], doc = {path: W.path, source: SRC.au.meta.id, starts}; if (pub) doc.publish = true;   // "publish" goes with the last part only
  const title = 'Timing: ' + W.path + ' / ' + SRC.au.meta.id;
  const body = T('ऐपसे भेजे गये ऑडियो-समय (कानसे जाँचे हुए)। इसे वैसे ही सबमिट करें; वर्कफ़्लो इन्हें लाइब्रेरीमें जोड़ देगा।', 'Audio starts set by ear in the app. Submit as it is; a workflow adds them to the library.') + '\n\n```json\n' + JSON.stringify(doc) + '\n```\n';
  const url = 'https://github.com/goyaldarwin/scriptures/issues/new?title=' + encodeURIComponent(title) + '&body=' + encodeURIComponent(body);
  window.open(url, '_blank', 'noopener');
  const sent = S.timing.sent[tkey()] = S.timing.sent[tkey()] || {}; part.forEach(id => sent[id] = pend[id]); if (pub) delete S.timing.publish[tkey()]; save();
  toast(last ? T('GitHub पर “Submit” दबाएँ', 'Tap “Submit” on GitHub') : T('GitHub पर “Submit” दबाएँ, फिर बाकी ', 'Tap “Submit” on GitHub, then send again: ') + DEV(ids.length - part.length) + T(' पदोंके लिये दोबारा भेजें', ' verses left'));
  setTimeout(renderSettings, 400);
}
function todayStr(){ const d = new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
async function exportFile(){
  const fname = 'scriptures-my-file-' + todayStr() + '.json', text = JSON.stringify(Object.assign({kind: 'manas-personal', exported: new Date().toISOString()}, S, {timing: Object.assign({}, S.timing, {on: false})}), null, 1);
  try { if (window.claude && window.claude.use){ const dl = await window.claude.use('downloads'); if (dl){ try { const r = await dl.save({filename: fname, data: text}); if (r && r.status === 'saved') toast(T('फ़ाइल सेव हुई', 'File saved')); } catch (e) {} return; } } } catch (e) {}
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], {type: 'application/json'})); a.download = fname; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1500); toast(T('फ़ाइल डाउनलोडमें सेव हुई', 'File saved to Downloads'));
}
$('#fileIn').onchange = async e => {
  const f = e.target.files[0]; e.target.value = ''; if (!f) return;
  let X; try { X = JSON.parse(await f.text()); } catch (err) { toast(T('यह फ़ाइल नहीं खुल सकी', 'Could not open this file')); return; }
  if (X && X.kind === 'scriptures-timing'){ importTiming(X); return; }
  if (!X || !X.profiles){ toast(T('यह इस ऐपकी फ़ाइल नहीं है', 'This is not a file from this app')); return; }
  const tmp = S; S = X; migrate(); X = S; S = tmp;
  openSheet('<h2>' + T('फ़ाइल खोलें', 'Open a file') + '</h2><p>' + T('इस फ़ाइलमें: ', 'This file has: ') + '<b>' + DEV(Object.values(X.profiles[0].bm).length) + T(' बुकमार्क · ', ' bookmarks · ') + DEV(Object.values(X.profiles[0].notes).reduce((a, b) => a + b.length, 0)) + T(' टिप्पणी', Object.values(X.profiles[0].notes).reduce((a, b) => a + b.length, 0) === 1 ? ' note' : ' notes') + '</b></p><div class="menu"><button id="imAdd">' + T('इन्हें इस फ़ोनमें जोड़ें', 'Add them to this phone') + '<br><small class="muted">' + T('यहाँकी आपकी चीज़ें भी रहेंगी', 'Your existing data stays') + '</small></button><button id="imRep">' + T('इस फ़ोनका सब कुछ इस फ़ाइलसे बदलें', 'Replace everything on this phone') + '<br><small class="muted">' + T('सेटिंग्स और प्रगति भी फ़ाइल जैसी हो जाएँगी', 'Settings and progress also come from the file') + '</small></button></div>');
  $('#imAdd').onclick = () => { X.profiles.forEach(p => mergeInto(ME(), p)); save(); closeSheet(); toast(T('फ़ाइल जोड़ी गई', 'File added')); onView(CURVIEW); };
  $('#imRep').onclick = () => askYes(T('इस फ़ोनका वर्तमान डेटा फ़ाइलके डेटासे बदल जाएगा।', 'Data on this phone will be replaced by the file.'), T('हाँ, बदलें', 'Yes, replace'), () => { const on = !!S.timing.on; S = Object.assign(defaults(), X); migrate(); delete S.kind; delete S.exported; S.timing.on = on; save(); closeSheet(); applyState(); toast(T('फ़ाइल खोली गई', 'File opened')); });
};
function askText(title, val, cb){ openSheet('<h2>' + esc(title) + '</h2><input id="askT" value="' + esc(val) + '"><div class="acts"><button class="btn" id="askOk">' + T('ठीक है', 'OK') + '</button><button class="btn ghost" id="askNo">' + T('रहने दें', 'Cancel') + '</button></div>'); setTimeout(() => $('#askT').focus(), 250); $('#askOk').onclick = () => { const v = $('#askT').value.trim(); closeSheet(); if (v) cb(v); }; $('#askNo').onclick = () => closeSheet(); }
function askYes(msg, yes, cb){ openSheet('<p style="font-size:17px">' + msg + '</p><div class="acts"><button class="btn" id="askOk">' + esc(yes) + '</button><button class="btn ghost" id="askNo">' + T('रहने दें', 'Cancel') + '</button></div>'); $('#askOk').onclick = () => { closeSheet(); cb(); }; $('#askNo').onclick = () => closeSheet(); }

/* ---------------- vidhi & āratī ---------------- */
let vidTab = 'v';
$$('#vidSeg button').forEach(b => b.onclick = () => { vidTab = b.dataset.v; renderVidhi(); });
$$('#vidLang button').forEach(b => b.onclick = () => { const en = b.dataset.l === 'e'; if (en === (LANG() === 'en')) return; S.settings.ui = en ? 'en' : 'hi'; save(); applyLang(); syncLayers(); renderVidhi(); });
const vW = l => wordsHTML(l);
function renderVidhi(){
  if (!W || !W.vidhi) return;
  if (vidTab === 'visarjan' && !W.vidhi.visarjan) vidTab = 'v';
  $$('#vidSeg button').forEach(b => { b.classList.toggle('on', b.dataset.v === vidTab); if (b.dataset.v === 'visarjan') b.hidden = !W.vidhi.visarjan; });
  const en = LANG() === 'en'; $$('#vidLang button').forEach(b => b.classList.toggle('on', (b.dataset.l === 'e') === en));
  const V = W.vidhi, L = en ? ' lat' : ''; let h = '';
  if (vidTab === 'aarti') h = '<div class="h' + L + '">' + T('श्रीरामायणजीकी आरती', 'Shri Ramayanji ki Aarti') + '</div>' + V.aarti.map(l => '<div class="v">' + vW(l) + '</div>').join('');
  else if (vidTab === 'visarjan'){ const X = V.visarjan; h = '<div class="h' + L + '">' + esc(TT(X.title)) + '</div><div class="vtip' + L + '">' + esc(TT(X.when)) + '</div>' + X.verses.map(x => '<div class="vcard"><div class="vcv">' + x.v.map(l => '<div>' + vW(l) + '</div>').join('') + '</div><div class="vce' + L + '">' + esc(en ? x.en : x.hi) + '</div></div>').join(''); }
  else (V[en ? 'en' : 'hi'] || []).forEach(([k, s]) => {
    if (k === 'h') h += Array.isArray(s) ? '<div class="h lat">' + esc(s[0]) + ' <span class="hh">' + esc(s[1]) + '</span></div>' : '<div class="h' + L + '">' + esc(s) + '</div>';
    else if (k === 'p') h += '<p class="vp' + L + '">' + esc(s) + '</p>';
    else if (k === 'tip') h += '<div class="vtip' + L + '">' + esc(s) + '</div>';
    else if (k === 'note') h += '<p class="vnote">' + (/इति/.test(s) ? vW(s) : esc(s)) + '</p>';
    else if (k === 'list') h += '<ol class="vlist' + L + '">' + s.map(x => '<li>' + esc(x) + '</li>').join('') + '</ol>';
    else if (k === 'card') h += '<div class="vcard">' + (s.t ? '<div class="vct' + L + '">' + esc(s.t) + (s.th ? ' <span class="hh">' + esc(s.th) + '</span>' : '') + '</div>' : '') + (s.v ? '<div class="vcv">' + s.v.map(l => '<div>' + vW(l) + '</div>').join('') + '</div>' : '') + (s.m ? '<div class="vcm">' + s.m.map(l => '<div>' + vW(l) + '</div>').join('') + '</div>' : '') + (s.e ? '<div class="vce' + L + '">' + esc(s.e) + '</div>' : '') + '</div>';
    else if (k === 'nyasa') h += '<div class="vny">' + s.map((r, n) => '<div class="vnr"><div class="vnn">' + DEV(n + 1) + '</div><div class="vnb"><div class="vcv">' + r.v.split(/(?<=।)\s+(?=[^।])/).map(x => '<div>' + vW(x) + '</div>').join('') + '</div>' + (r.e ? '<div class="vce' + L + '">' + esc(r.e) + '</div>' : '') + '<div class="vna"><span class="vcm">' + vW(r.m) + '</span>' + (r.a ? '<span class="' + L.trim() + '"> — ' + esc(r.a) + '</span>' : '') + '</div></div></div>').join('') + '</div>';
  });
  $('#vidBody').innerHTML = h;
}
$('#vidBody').addEventListener('click', ev => { const w = ev.target.closest('.w'); if (w){ w.classList.add('sel'); wordSheet(w.dataset.w || w.textContent, vidTab === 'v' ? W.vg : vidTab === 'visarjan' ? W.vidhi.visarjan.g : null, W.lang); } });

/* ---------------- first-run tour: done, not read ----------------
   A welcome card, then the reader is taken into the Sundarakāṇḍa and asked to do each thing for real — open the text, tap a
   word, close its drawer, switch a meaning on, play one verse — with that spot lit and the rest dimmed; each step moves on
   when it has been done. Shown once; ☰ › “Take the tour” shows it again. closeTour() ends it at any point. */
let TOUR = null;   // {k: step, t0, base}
function tourWork(){ const leafs = []; (function walk(n){ (n || []).forEach(c => c.work ? leafs.push(c.work) : walk(c.children)); })(LIB); return leafs.includes('sundarkand') ? 'sundarkand' : leafs[0]; }
function inView(el){ const r = el.getBoundingClientRect(); return r.width && r.top > 70 && r.bottom < innerHeight - 90; }
function firstVisible(sel){ const all = $$(sel); return all.find(inView) || all[0] || null; }
// the tour's first step finds the Sundarakāṇḍa part by its Hindi name, which does not change with the English spelling
function tourSteps(){
  return [
    {t: () => { const rows = $$('#orgList [data-open]'), k = PARTS.findIndex(p => (p.hi || '') === 'सुन्दरकाण्ड'); return (W && W.id === 'sundarkand' && k >= 0 && rows[k]) || rows[0]; }, allow: '#orgList .it', p: T('पढ़ना शुरू करनेके लिये यहाँ छुएँ।', 'Tap here to start reading.'), done: () => CURVIEW === 'reader' && !!$('#rBody .verse')},
    {t: () => firstVisible('#rBody .verse .vtext .w'), allow: '#rBody .vtext .w', p: T('किसी भी शब्दको छुएँ — उसका अर्थ दिखेगा।', 'Tap any word to see its meaning.'), done: () => $('#sheet').classList.contains('on')},
    {t: () => $('#sheet'), allow: '#sheet', p: T('इस पट्टीको नीचे खींचकर बंद करें।', 'Drag the drawer down to close it.'), done: () => !$('#sheet').classList.contains('on'), top: true},
    {t: () => $('#reader .szp'), allow: '#reader .szp', p: T('A+ छूकर अक्षर बड़े करें।', 'Tap A+ to make the letters larger.'), enter: () => { TOUR.base = S.settings.size; }, done: () => S.settings.size > TOUR.base || (TOUR.tap && TOUR.base >= 34)},   // already at the largest: the tap is enough
    // A− is a step of its own: after A+, people reach for it
    {t: () => $('#reader .szm'), allow: '#reader .szm', p: T('A− छूकर अक्षर छोटे करें।', 'Tap A− to make the letters smaller.'), enter: () => { TOUR.base = S.settings.size; }, done: () => S.settings.size < TOUR.base || (TOUR.tap && TOUR.base <= 16)},   // already at the smallest: the tap is enough
    {t: () => { const [a, b] = capKinds().map(LK); return $('#rLayers [data-l="' + (layerOn(a) ? b : a) + '"]'); }, allow: '#rLayers [data-l="h"], #rLayers [data-l="e"], #rLayers [data-l="pa"], #rLayers [data-l="w"]', p: () => S.settings.layers.h ? T('“En” छूकर हर पदके नीचे अंग्रेज़ी अर्थ दिखाएँ या छिपाएँ। “शब्द” से शब्दार्थ।', 'Tap “En” to show or hide the English meaning under every verse. “शब्द” gives word-by-word meanings.') : T('“हिं” छूकर हर पदके नीचे हिंदी अर्थ दिखाएँ। “En” अंग्रेज़ी, “शब्द” शब्दार्थ।', 'Tap “हिं” to show the Hindi meaning under every verse. “En” is English, “शब्द” word by word.'),
     enter: () => { TOUR.base = JSON.stringify(S.settings.layers); }, done: () => JSON.stringify(S.settings.layers) !== TOUR.base},
    {t: () => $('#rLayers [data-l="r"]'), allow: '#rLayers [data-l="r"]', p: T('पुस्तक छूकर पाठ मोड चालू करें — केवल मूल पाठ। फिर छूनेपर अर्थ लौट आते हैं।', 'Tap the book for recitation mode — the verses alone. Tap it again to bring the meanings back.'), done: () => !!S.settings.recite},
    {t: () => firstVisible('#rBody .vbm'), allow: '#rBody .vbm', p: T('बुकमार्क चिह्न छूकर यह पद सहेजें — ☰ › बुकमार्कमें मिलेगा।', 'Tap the bookmark sign to save this verse — find it in ☰ › Bookmarks.'),
     enter: () => { TOUR.bmAdded = false; }, done: () => !!TOUR.bmAdded},   // any bookmark made in this step — even one taken off and put back
    {t: () => firstVisible('#rBody .vplay'), allow: '#rBody .vplay', p: T('▶ छूकर केवल यह पद सुनें — जो गाया जा रहा है वह चमकेगा।', 'Tap ▶ to play just this verse — it lights up as it is sung.'), done: () => PL.on},
  ];
}
// while the tour runs, only what the current step asks for can be tapped (a ▶ on the work's page would start the audio
// and lose the tour); the tour's own bubble always works
document.addEventListener('click', e => {
  if (!TOUR || TOUR.k < 0) return; const x = tourSteps()[TOUR.k]; if (!x) return;
  if (e.target.closest('#cbub, #tour')) return;
  if (x.allow && e.target.closest(x.allow)){ TOUR.tap = true; return; }   // the step's own control was tapped
  e.preventDefault(); e.stopPropagation();
}, true);
function startTour(){
  closeTour(true); TOUR = {k: -1};
  $('#tourArt').innerHTML = '<div class="ta-om">ॐ</div>'; $('#tourT').textContent = T('स्वागत है', 'Welcome');
  $('#tourP').textContent = T('आइए, एक छोटा परिचय लें।', 'Let’s take a short tutorial.');
  $('#tourDots').innerHTML = ''; $('#tourSkip').textContent = T('छोड़ें', 'Skip'); $('#tourNext').textContent = T('शुरू करें', 'Start');
  $('#tourSkip').onclick = () => closeTour(); $('#tourNext').onclick = async () => { $('#tour').hidden = true; await openWork(tourWork()); WS().org = 'k'; renderHome(); tourStep(0); };
  $('#tour').hidden = false;
}
function tourStep(k){
  const st = tourSteps(); if (!TOUR) return;
  if (k >= st.length){ return tourEnd(); }
  TOUR.k = k; TOUR.t0 = Date.now(); TOUR.tap = false; const x = st[k]; if (x.enter) x.enter();
  const el = x.t(); if (el && el.scrollIntoView && !x.top && !inView(el)) el.scrollIntoView({block: 'center'});
  $('#coach').hidden = false; $('#cbText').textContent = typeof x.p === 'function' ? x.p() : x.p; $('#cbStep').textContent = DEV(k + 1) + ' / ' + DEV(st.length);
  $('#cbBack').hidden = k === 0;
}
// ‹ Back: the step before. A step whose action is already in effect (the drawer already closed, recitation
// mode already on) would move on at once, so Back goes to the step before that one; the first step needs the work's page.
function tourBack(){
  if (!TOUR || TOUR.k <= 0) return; const st = tourSteps(); let k = TOUR.k - 1;
  if (!$('#sheet').classList.contains('on') && k === 2) k = 1;   // "close the drawer" needs an open drawer: back to "tap a word"
  if (k === 1 && $('#sheet').classList.contains('on')) closeSheet();   // "tap a word" needs a closed drawer, or it would count as done at once
  if (k === 6 && S.settings.recite) toggleRecite();             // back to recitation mode: turn it off so it can be tried again
  if (k === 0 && CURVIEW !== 'home') show('home');
  TOUR.k = -1; $('#cspot').style.opacity = 0; setTimeout(() => tourStep(k), 250);
}
// After ▶ the tour lets the verse play for 5 seconds, then takes the reader to the library with a parting message.
// Closing the player sooner ends it the same way.
function tourEnd(){ if (!TOUR) return; TOUR.k = -1; TOUR.waiting = true; TOUR.until = Date.now() + 5000; $('#coach').hidden = true; if (!PL.on) tourFinish(); }
function tourFinish(){
  if (S.settings.recite) toggleRecite();   // the meanings come back after the tour
  closeTour(); libPath = []; show('library');
  toastLight(T('परिचय पूरा हुआ — आशा है ऐप आपको अच्छा लगेगा!', 'Tour complete — we hope you enjoy the app!'));
}
function closeTour(keep){ if (!keep) S.hinted = 1;  $('#tour').hidden = true; $('#coach').hidden = true; $('#tourSkip').hidden = false; TOUR = null; if (!keep){ S.settings.tour = 1; save(); } }
// keep the light on the step's spot as the page moves; move on when the step has been done (a step that cannot be shown is skipped)
setInterval(() => {
  if (TOUR && TOUR.waiting){ if (PL.on && Date.now() >= TOUR.until) stopAudio(); if (!PL.on) tourFinish(); return; }
  if (!TOUR || TOUR.k < 0) return; const x = tourSteps()[TOUR.k]; if (!x) return;
  if (x.done()){ const nx = TOUR.k + 1; TOUR.k = -1; $('#cspot').style.opacity = 0; setTimeout(() => tourStep(nx), 450); return; }
  const el = x.t(), sp = $('#cspot'), cb = $('#cbub');
  if (!el){ if (Date.now() - TOUR.t0 > 6000) tourStep(TOUR.k + 1); sp.style.opacity = 0; return; }
  const r = el.getBoundingClientRect(), pad = 6; sp.style.opacity = 1;
  Object.assign(sp.style, {left: (r.left - pad) + 'px', top: (r.top - pad) + 'px', width: (r.width + 2 * pad) + 'px', height: (r.height + 2 * pad) + 'px'});
  const below = x.top ? false : r.top < innerHeight / 2; cb.style.top = below ? Math.min(innerHeight - 160, r.bottom + 16) + 'px' : ''; cb.style.bottom = below ? '' : (x.top ? innerHeight - r.top + 16 : innerHeight - r.top + 16) + 'px';
}, 250);
$('#cbSkip').onclick = () => closeTour();
$('#cbBack').onclick = () => tourBack();

// keep only the shelves on the list (paths of shelf ids: "hinduism", "sikhism/gurbani/guru-arjan-dev/sukhmani-sahib")
function pruneLib(nodes, shelves){
  const want = shelves.map(x => x.split('/'));
  const walk = (ns, at) => ns.map(n => {
    const p = at.concat(n.id), whole = want.some(w => w.length <= p.length && w.every((x, k) => x === p[k]));
    if (whole) return n;
    if (!want.some(w => w.length > p.length && p.every((x, k) => x === w[k]))) return null;
    const kids = walk(n.children || [], p); return kids.length ? Object.assign({}, n, {children: kids}) : null;
  }).filter(Boolean);
  return walk(nodes, []);
}
/* ---------------- boot ---------------- */
(async function boot(){
  if (!S.settings.lightDefault){ if (S.settings.theme === 'auto') S.settings.theme = 'light'; S.settings.lightDefault = 1; save(); }
  applyTheme(); applyLang(); applyRecite(); syncLayers(); applyTiming();
  showSalute('');   // starting or refreshing: no greeting (it belongs to opening a work from the library)
  try { LIB = await getJSON('index'); } catch (e) { $('#loading').textContent = T('डेटा नहीं खुल सका। इंटरनेट जाँचें।', 'Could not load the data. Check the internet connection.'); return; }
  // one app per tradition: ?app=<id> shows only the shelves library/apps.json lists for that app
  // (the Hindu app also carries the Sukhmani Sahib). The address keeps it while you move around; changing the list
  // needs no app update. Without ?app the website shows the whole library.
  const appId = new URLSearchParams(location.search).get('app');
  if (appId){ try { const A = (await getJSON('apps'))[appId]; if (A) LIB = pruneLib(LIB, A.shelves); } catch (e) {} }
  LIB = libView(LIB);
  const leafs = []; (function walk(n){ (n || []).forEach(c => c.work ? leafs.push(c.work) : walk(c.children)); })(LIB);
  // a link may name a work (?w=<work id>): the app's shortcuts and store pages open straight to it
  const asked = new URLSearchParams(location.search).get('w');
  const start = asked && leafs.includes(asked) ? asked : S.work && leafs.includes(S.work) ? S.work : (leafs.length === 1 ? leafs[0] : null);
  const nav = (performance.getEntriesByType && performance.getEntriesByType('navigation')[0]) || {};
  const was = !asked && (nav.type === 'reload' || nav.type === 'back_forward') && history.state && history.state.v ? history.state : null;
  if (was){ await restore(was); if (!W) await hideSalute(); }   // a refresh: the same page, with the same way back
  // opened again: the screen last used — the library, or the work's page, or the reader at your place (S.view); a link to a work opens it
  else if (start && (asked || S.view !== 'library')){ const lastView = S.view; await openWork(start, true); history.replaceState(snap('library'), ''); show('home'); if (!asked && lastView === 'reader') reopenReader(); }
  else { history.replaceState(snap('library'), ''); renderLibrary(); await hideSalute(); }
  cloudInit();
  if (!S.settings.tour) startTour();
  // offline reading: the service worker keeps the app and every library file it has fetched (sw.js, build.py)
  if ('serviceWorker' in navigator && (location.protocol === 'https:' || window.__SW_TEST) && !BUNDLE) navigator.serviceWorker.register('sw.js').catch(() => {});
})();
