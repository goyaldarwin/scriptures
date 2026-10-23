'use strict';
/* =====================================================================
   Scripture reader — library of works; each work = text (verse + number)
   with selectable sources for Hindi meaning, English meaning and audio.
   Word meanings come from one dictionary per language (library/glossary), chosen by the verse's language.
   ===================================================================== */
const $ = s => document.querySelector(s);
const $$ = s => Array.from(document.querySelectorAll(s));
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const DIG = '०१२३४५६७८९';
const DEV = n => (typeof S !== 'undefined' && S && S.settings && LANG() === 'en') ? String(n) : String(n).replace(/[0-9]/g, d => DIG[d]);
const ORDH = ['', 'पहला', 'दूसरा', 'तीसरा', 'चौथा', 'पाँचवाँ', 'छठा', 'सातवाँ', 'आठवाँ', 'नवाँ', 'दसवाँ', 'ग्यारहवाँ', 'बारहवाँ', 'तेरहवाँ', 'चौदहवाँ', 'पंद्रहवाँ', 'सोलहवाँ', 'सत्रहवाँ', 'अठारहवाँ', 'उन्नीसवाँ', 'बीसवाँ', 'इक्कीसवाँ', 'बाईसवाँ', 'तेईसवाँ', 'चौबीसवाँ', 'पचीसवाँ', 'छब्बीसवाँ', 'सत्ताईसवाँ', 'अट्ठाईसवाँ', 'उनतीसवाँ', 'तीसवाँ'];
const TYPEN = {do: ['दोहा', 'Dohā'], so: ['सोरठा', 'Sorathā'], cha: ['छंद', 'Chhand'], shloka: ['श्लोक', 'Śloka'], cau: ['चौपाई', 'Chaupāī']};
const TYPE = new Proxy({}, {get: (o, k) => TYPEN[k] ? T(TYPEN[k][0], TYPEN[k][1]) : ''});
const TT = o => o ? (typeof o === 'string' ? o : T(o.hi, o.en || o.hi)) : '';

/* ---------------- loading ---------------- */
const BUNDLE = window.__BUNDLE || null;            // offline file / claude.ai link carry everything inside
async function getJSON(path){
  if (BUNDLE){ const v = BUNDLE.files[path]; if (v) return v; throw new Error('missing ' + path); }
  const r = await fetch('library/' + path + '.json', {cache: 'no-cache'}); if (!r.ok) throw new Error(path); return r.json();
}
let LIB = [], LANGS = {}, GL = {}, WG = {}, ALT = {hi: [], en: []}, W = null, IT = [], ID = {}, SRC = {hi: null, en: null, au: null};

/* ---------------- personal store ---------------- */
const LS = 'manas.personal.v1';
let canStore = true;
function newProfile(name){ return {id: 'p' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), name, notes: {}, bm: {}, done: {}, gloss: {}, fix: {}}; }
// a new reader starts in English (owner, 2026-10-19): English interface and English meaning; हिं adds the Hindi meaning
function defaults(){ const p = newProfile('Me'); return {v: 2, settings: {ui: 'en', layers: {h: false, e: true, w: false}, tr: false, size: 21, theme: 'light', wake: true, lightDefault: 1}, src: {}, w: {}, work: null, profiles: [p], active: p.id, show: [p.id]}; }
let S;
try { S = JSON.parse(localStorage.getItem(LS)); } catch (e) { canStore = false; }
if (!S || !S.profiles) S = defaults();
// timing review (Settings › Audio timing): on/off, and the starts set by ear, by "<work>:<audio source>" → {item id: [track, seconds]}
if (!S.timing) S.timing = {on: false, fix: {}, sent: {}};
if (!S.timing.sent) S.timing.sent = {};
// marks loaded from a helper's file and not yet checked by you: "<work>:<source>" → {item id: helper's name}. They are
// heard and shown like yours, but go to the library only after you tap ✓ under the verse.
if (!S.timing.from) S.timing.from = {};
// Audio timing is a tool for the person checking timings, never left on by chance: it turns itself off when the site is
// opened 12 hours after it was last used, and it never travels in a saved file
if (S.timing.on && Date.now() - (S.timing.used || 0) > 12 * 3600e3) S.timing.on = false;
function migrate(){
  if ((S.v || 1) < 2) migrate2();
  if (S.settings && !S.settings.ui) S.settings.ui = S.settings.layers && S.settings.layers.e ? 'en' : 'hi';   // earlier: the language followed the English meaning
  if (S.v < 3){ // v2 → v3: a reader's own word meanings are filed by language (“awa:राम”); earlier ones were all Awadhi
    S.profiles.forEach(p => { const n = {}; for (const k in p.gloss || {}) n[k.includes(':') ? k : 'awa:' + k] = p.gloss[k]; p.gloss = n; });
    S.v = 3;
  }
  oneReader();
}
// One reader per device (owner, 2026-10-19): there is no list of readers any more. A phone or file that had several keeps
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
    if (snap.exists){ const d = snap.data(); if (d && d.s && (d.ts || 0) > (S.ts || 0)){ const X = JSON.parse(d.s); if (X && X.profiles){ S = Object.assign(defaults(), X); migrate(); try { localStorage.setItem(LS, JSON.stringify(S)); } catch (e) {} applyTheme(); applyLang(); onView(CURVIEW); } } else if ((S.ts || 0) > (d.ts || 0)) cloudPush(); }
    else if (S.ts) cloudPush();
    canStore = true;
  } catch (e) {}
}
// the language of the app (owner, 2026-10-19): its own setting, chosen with हिं · En on the library and work pages (and in
// Settings); the meanings under the verses (हिं · En · शब्द in the reader) are separate and never change it
// Inside a work's text (the reader) the words around the verses follow the meanings chosen there (owner, 2026-10-19):
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
  rc: () => T('पाठ मोड', 'Recitation mode'), rcSub: () => T('केवल मूल पाठ, बड़े अक्षर', 'Verses only, larger letters'),
  size: () => T('अक्षरका आकार', 'Letter size'), theme: () => T('रंग', 'Theme'), more: () => T('और', 'More'), tour: () => T('परिचय (टूर)', 'Take the tour'),
  sections: () => T('प्रसंग', 'Sections'), search: () => T('खोजें', 'Search'),
  bm: () => T('बुकमार्क और टिप्पणियाँ', 'Bookmarks & notes'), verses: () => T('मूल पाठ', 'Verses'),
  lib: () => T('पुस्तकालय', 'Library'), src: () => T('स्रोत', 'Sources'), vidhi: () => T('पारायण-विधि', 'Pārāyaṇa vidhi')
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
  $$('.view').forEach(v => v.classList.toggle('on', v.id === id)); if (push) history.pushState(snap(id), ''); else history.replaceState(snap(id), ''); if (id !== 'reader') window.scrollTo(0, 0); onView(id); }
// Every page is an entry in the browser's history that carries where you are: the page, the open work and the library
// shelf (owner, 2026-10-19). Back (the button or the phone's gesture) returns to exactly the previous one — a shelf
// included — and a refresh reopens the same page, because the browser keeps these entries across a reload.
function snap(v){ return {v, w: W ? W.id : null, lib: libPath.slice(), scope: v === 'search' ? SCOPE : undefined}; }
let popping = Promise.resolve();
async function restore(st){
  closeSheet();
  if (!st || !st.v) st = {v: 'library', w: null, lib: []};
  libPath = Array.isArray(st.lib) ? st.lib.slice() : [];
  if (st.v !== 'library' && st.w && (!W || W.id !== st.w)) await openWork(st.w, true);
  const v = document.getElementById(st.v) && (W || !['home', 'reader', 'bookmarks', 'vidhi'].includes(st.v)) ? st.v : 'library';
  if (v === 'search') setScope(st.scope === 'lib' || !W ? 'lib' : 'text');   // Back to a search: the same kind of search, the query kept
  show(v, false); if (v === 'reader') reopenReader();
}
function back(){ history.back(); }
window.addEventListener('popstate', e => { const st = e.state; popping = popping.then(() => restore(st)); });
function onView(id){ if (id === 'library') renderLibrary(); if (id === 'home') renderHome(); if (id === 'bookmarks') renderBookmarks(); if (id === 'settings') renderSettings(); if (id === 'vidhi') renderVidhi(); wake(id === 'reader'); if (id === 'search') setTimeout(() => $('#q').focus(), 50); }
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
function closeSheet(){ $('#sheet').classList.remove('on'); $('#scrim').classList.remove('on'); $$('.w.sel').forEach(w => w.classList.remove('sel')); }
$('#scrim').onclick = () => closeSheet();
function sw(id, label, sub, on, icon){ return '<label class="sw">' + (icon ? '<svg class="swic"><use href="#i-' + icon + '"/></svg>' : '') + '<span' + (icon ? ' style="flex:1"' : '') + '>' + label + (sub ? '<small>' + sub + '</small>' : '') + '</span><span class="tg"><input type="checkbox" id="' + id + '"' + (on ? ' checked' : '') + '><span></span></span></label>'; }

/* ---------------- wake lock ---------------- */
let wl = null;
// the screen stays on while reading or playing — always, no setting (owner, 2026-10-22)
async function wake(on){ try { if (on && 'wakeLock' in navigator){ if (!wl){ wl = await navigator.wakeLock.request('screen'); wl.addEventListener('release', () => wl = null); } } else if (wl && !PL.on){ await wl.release(); wl = null; } } catch (e) {} }
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible' && ($('#reader').classList.contains('on') || PL.on)) wake(true); });

/* ---------------- word meanings: one dictionary per language (library/glossary/<lang>.json) ----------------
   A word is looked up in the language of the verse it is in, then in that language's fallbacks
   (languages.json). A work may refine a sense in <work>/glossary.json; a reader's own meaning wins. */
const PUNCT = /[।॥|,.;:!?\-—‘’“”'"()\[\]०-९੦-੯0-9]/g;   // Devanagari and Gurmukhi digits are verse numbers, not words
const SVARA = /[\u0951-\u0954\u1CD0-\u1CFF\uA8E0-\uA8F1]/g;   // Vedic accent marks: shown in the text, ignored when looking a word up
function cleanWord(w){ return w.replace(PUNCT, '').replace(SVARA, '').normalize('NFC'); }
function langOf(i){ return (i != null && IT[i] && IT[i].l) || W.lang; }
function langChain(lang){ return [lang].concat((LANGS[lang] || {}).fallback || []); }
async function loadGlossaries(){
  if (!Object.keys(LANGS).length) LANGS = await getJSON('glossary/languages');
  const need = new Set(); [W.lang].concat(IT.map(x => x.l).filter(Boolean)).forEach(l => langChain(l).forEach(c => need.add(c)));
  await Promise.all([...need].filter(c => !GL[c]).map(async c => { try { GL[c] = await getJSON('glossary/' + c); } catch (e) { GL[c] = {}; } }));
  WG = {}; if (W.glossary){ try { WG = await getJSON(W.path + '/glossary'); } catch (e) {} }
}
function dictEntry(lang, w){ return (WG[lang] && WG[lang][w]) || (GL[lang] && GL[lang][w]) || null; }
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
  line = line.replace(/\s+(।।|।|॥)/g, ' $1');
  const halves = line.split(/(?<=[।॥])\s+(?=[^\s।॥०-९੦-੯(])/).reduce((a, h) => { if (a.length && /^[।॥\s]+$/.test(a[a.length - 1])) a[a.length - 1] += ' ' + h; else a.push(h); return a; }, []);
  return halves.map(hf => '<span class="half">' + hf.split(/( +)/).map(tok => { if (/^ +$/.test(tok) || !cleanWord(tok)) return esc(tok); const m = tok.match(/^(.*?)( .*)?$/); return '<span class="w">' + esc(m[1]) + '</span>' + esc(m[2] || ''); }).join('') + '</span>').join(' ');
}
function wordList(lines){ const seen = new Set(), out = []; lines.forEach(l => l.split(/\s+/).forEach(t => { const w = cleanWord(t); if (w && !seen.has(w)){ seen.add(w); out.push(w); } })); return out; }
function wbHTML(lines, lang){
  return '<div class="wb">' + wordList(lines).map(w => { const g = lookup(w, lang); if (!g || g.none) return ''; const m = esc(g.hi || '') + (g.en ? ' <span class="en">· ' + esc(g.en) + '</span>' : '') + (g.possible ? ' <span class="q">(' + esc(g.possible) + ')</span>' : ''); return '<span class="ww w" data-w="' + esc(w) + '">' + esc(w) + '</span><span class="wm">' + m + '</span>'; }).join('') + '</div>';
}
function wordSheet(raw, alt, lang){
  const w = cleanWord(raw); const g = (alt && alt[w]) || lookup(raw, lang);
  let h = '<h2>' + esc(w) + '</h2>';
  if (g && !g.none && g.lang && LANGS[g.lang]) h += '<p class="small muted">' + esc(TT(LANGS[g.lang].name)) + '</p>';
  if (g && !g.none){
    if (g.possible) h += '<p class="small muted">' + T('मूल शब्द: ', 'Root: ') + '<b>' + esc(g.possible) + '</b></p>';
    h += '<dl class="kv">' + (g.r && g.r !== w ? '<dt>' + T('मूल', 'Root') + '</dt><dd>' + esc(g.r) + '</dd>' : '') + '<dt>' + T('हिंदी', 'Hindi') + '</dt><dd>' + esc(g.hi || '—') + '</dd><dt>English</dt><dd class="lat">' + esc(g.en || '—') + '</dd>' + (g.g ? '<dt>' + T('व्याकरण', 'Grammar') + '</dt><dd>' + esc(g.g) + '</dd>' : '') + (g.p && g.p.length ? '<dt>' + T('शब्द-खण्ड', 'Parts') + '</dt><dd>' + g.p.map(x => '<b>' + esc(x[0]) + '</b> (' + esc(x[1]) + ')').join(' + ') + '</dd>' : '') + '</dl>';
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
function secLabel(p){ if (isNum(p.s)) return T('दोहा ', 'Dohā ') + DEV(p.s); const a = IT[p.from], z = IT[p.to]; if (a.y === z.y && vNum(a.n) && vNum(z.n)) return TYPE[a.y] + ' ' + vNum(a.n) + (z.n !== a.n ? '–' + vNum(z.n) : ''); return vLabel(a) === vLabel(z) ? vLabel(a) : vLabel(a) + ' – ' + vLabel(z); }
function posLabel(i){ const it = IT[i], p = PAGES[itemPage[i]]; if (!isNum(p.s) || it.y === 'do' || it.y === 'so') return vLabel(it); return secLabel(p) + ' · ' + vLabel(it); }
function itemLabel(i){ return KNAME(IT[i].p) + ' · ' + posLabel(i); }
function spanLabel(a, b){
  const pa = PAGES[itemPage[a]], pb = PAGES[itemPage[b]];
  if (isNum(pa.s) && isNum(pb.s)) return T('दोहा ', 'Dohā ') + DEV(pa.s) + (pb.s !== pa.s ? '–' + DEV(pb.s) : '');
  const la = isNum(pa.s) ? secLabel(pa) : vLabel(IT[a]), lb = isNum(pb.s) ? secLabel(pb) : vLabel(IT[b]);
  if (la === lb) return la;
  if (IT[a].y === IT[b].y && !isNum(pa.s) && !isNum(pb.s) && vNum(IT[a].n) && vNum(IT[b].n)) return TYPE[IT[a].y] + ' ' + vNum(IT[a].n) + '–' + vNum(IT[b].n);
  return la + ' – ' + lb;
}
function rangeDesc(a, b){ const ka = KNAME(IT[a].p), kb = KNAME(IT[b].p); if (ka === kb) return esc(ka + ': ' + spanLabel(a, b)); let h = '', p = IT[a].p; while (p <= IT[b].p){ const x = Math.max(a, PARTS[p].a), y = Math.min(b, PARTS[p].b); h += (h ? '<br>' : '') + esc(KNAME(p) + ': ' + spanLabel(x, y)); p++; } return h; }

/* ---------------- sources: meanings and audio ---------------- */
function srcList(kind){ return ((W.sources || {})[kind] || []).filter(s => !s.draft || S.timing.on); }   // a draft recording is heard only while reviewing timings
function srcChoice(kind){ const list = srcList(kind); const sel = ((S.src[W.id] || {})[kind]); if (sel === 'off') return null; return (list.find(s => s.id === sel) || list[0] || null); }
async function loadSources(){
  for (const kind of ['hi', 'en', 'au']){ const c = srcChoice(kind); SRC[kind] = null; if (c){ try { SRC[kind] = Object.assign({meta: c}, await getJSON(W.path + '/' + c.file)); } catch (e) {} } }
  // the other meaning sources of a kind fill in verses the chosen one doesn't cover (e.g. a stotra appended to a kāṇḍa)
  for (const kind of ['hi', 'en']){ ALT[kind] = []; const c = SRC[kind] && SRC[kind].meta;
    for (const s of ((W.sources || {})[kind] || [])) if (c && s.id !== c.id){ try { ALT[kind].push(Object.assign({meta: s}, await getJSON(W.path + '/' + s.file))); } catch (e) {} } }
  buildAudio();
}
function verseOf(i){ const id = IT[i].id; for (const p of S.profiles){ const f = p.fix[KEY(id)]; if (f && f.v) return {v: f.v, edited: true}; } return {v: IT[i].v, edited: false}; }
function mean(kind, i){
  const src = SRC[kind]; if (!src) return null; const id = IT[i].id; const k = KEY(src.id + ':' + id);
  for (const p of S.profiles){ const f = p.fix[k]; if (f && f.m != null) return {x: f.m, edited: true, f: (src.m[id] || [])[1]}; }
  const e = src.m[id]; if (e) return {x: e[0], f: e[1], edited: false};
  for (const a of ALT[kind] || []){ const x = a.m[id]; if (x) return {x: x[0], f: x[1], edited: false, from: TT(a.meta.title)}; }
  return null;
}
const layerOn = l => !!S.settings.layers[l];

/* ---------------- reader: continuous scroll over a kāṇḍa or a day's pāṭh ---------------- */
let R = {org: 'k', a: 0, b: 0, n: 0, pf: -1, pt: -1};
const VSHORT = {cau: ['चौ॰', 'Cau.'], do: ['दो॰', 'Do.'], so: ['सो॰', 'So.'], cha: ['छं॰', 'Cha.'], shloka: ['श्लो॰', 'Śl.']};
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
  let h = '<div class="verse' + (toCheck(i) ? ' tocheck' : '') + '" id="v' + i + '" data-i="' + i + '"><div class="vtext' + (VEDIC.test(vv.v.join('')) ? ' vedic' : '') + '">' + vv.v.map((l, y) => {
    const last = y === vv.v.length - 1;
    let ln = last && it.y === 'cau' && it.n && /।।\s*$/.test(l) ? l.replace(/\s*।।\s*$/, ' ।।' + String(it.n).replace(/\d/g, d => DIG[d]) + '।।') : l;
    if (LANG() === 'en') ln = ln.replace(/[०-९]/g, d => DIG.indexOf(d)).replace(/[੦-੯]/g, d => d.charCodeAt(0) - 0x0A66);
    const w = wordsHTML(ln).replace(/।।\s*([0-9०-९][^\s।<]*)\s*।।/, '<span style="white-space:nowrap">।।$1।।</span>').replace(/॥\s*([0-9०-९੦-੯][^\s॥<]*)\s*॥/, '<span style="white-space:nowrap">॥$1॥</span>');
    const lead = '';   // the verse type is no longer a corner tag: it is a heading above a run of verses (typeHead)
    // corners, each inside the gutter so they never touch the text: ▶ (top left, on the line of the bookmark — owner,
    // 2026-10-20), bookmark (top right), ⋮ (bottom right). A one-line verse is given a second line's height so the corners stay apart.
    const top = y === 0 ? (hasAu(i) ? '<button class="vb vplay" data-a="play" aria-label="play"><svg><use href="#i-play"/></svg></button>' : '') + '<button class="vb vbm' + (bm ? ' bm-on' : '') + '" data-a="bm" aria-label="bookmark"><svg><use href="#i-bm"/></svg></button>' : '';
    const undo = last && S.timing.on && SRC.au && myStarts()[id] ? '<span class="vundo"><button class="vb" data-a="tundo" aria-label="' + T('पहले जैसा', 'Undo') + '" title="' + T('पहले जैसा', 'Undo') + '"><svg><use href="#i-undo"/></svg></button></span>' : '';   // ↶ (bottom left) in timing mode, on a verse you set
    const tail = last ? '<span class="vend"><button class="vb" data-a="menu" aria-label="more"><svg><use href="#i-more"/></svg></button></span>' + undo : '';
    return '<p' + (vv.v.length === 1 ? ' class="one"' : '') + '>' + lead + top + w + tail + '</p>'; }).join('') + '</div>';
  if (S.timing.on && SRC.au) h += markBar(i);
  if (S.settings.tr && it.t && it.t.length) h += '<div class="tr">' + it.t.map(l => '<div>' + l.split(/(?<=,)\s+/).map(x => '<span class="half">' + esc(x).replace(/\s*॥\s*([^॥]*?)\s*॥/g, ' <span class="dd">॥$1॥</span>') + '</span>').join(' ') + '</div>').join('') + '</div>';
  if (layerOn('h')){ const m = mean('hi', i); if (m) h += '<div class="layer h">' + esc(m.x).replace(/\s*(।।[^।]*।।)\s*$/, '<span style="white-space:nowrap"> $1</span>') + (m.edited ? '<span class="tag">' + T('संशोधित', 'edited') + '</span>' : '') + (m.f ? '<div class="fn">' + m.f.map(esc).join('<br>') + '</div>' : '') + '</div>'; }
  if (layerOn('w')) h += '<div class="layer wl">' + wbHTML(vv.v, langOf(i)) + '</div>';
  if (layerOn('e')){ const m = mean('en', i); if (m) h += '<div class="layer e">' + esc(m.x) + (m.edited ? '<span class="tag">edited</span>' : '') + (m.f ? '<div class="fn">' + m.f.map(esc).join('<br>') + '</div>' : '') + '</div>'; }
  for (const p of SHOWN()) (p.notes[KEY(id)] || []).forEach((n, k) => { h += '<div class="note"><div class="who">' + new Date(n.ts).toLocaleDateString(LANG() === 'en' ? 'en-IN' : 'hi-IN') + (p.id === me.id ? '<button data-a="enote" data-k="' + k + '">' + T('बदलें', 'Edit') + '</button>' : '') + '</div>' + esc(n.t).replace(/\n/g, '<br>') + '</div>'; });
  return h + '</div>';
}
function pauseHTML(i){
  const list = pauseAfter[i]; if (!list) return '';
  return list.filter(([o]) => R.org === 'k' || R.org === o).map(([o, n]) => { const done = DONE(ME(), o)[n]; return '<div class="pause" data-pause="' + o + n + '"><b>' + PNAME(o) + ' · ' + VN(n) + '</b><div class="sub">' + T('यहाँ विश्राम करें', 'A place to pause the reading') + '</div><button class="btn small' + (done ? ' ghost' : '') + '" data-a="done" data-o="' + o + '" data-n="' + n + '" data-i="' + i + '">' + (done ? T('✓ पूर्ण — बदलें', '✓ Completed — undo') : T('विश्राम पूर्ण करें', 'Mark vishram complete')) + '</button></div>'; }).join('');
}
// the verse type as a heading above the verse, “॥ चौपाई ॥” (owner, 2026-10-19), shown only where the type changes:
// before the first chaupāī of a run, then before the dohā that follows, and so on — and at the start of what is read
function typeHead(i){
  const y = IT[i].y, nm = TYPEN[y]; if (!nm) return '';
  if (i !== R.a && i > 0 && IT[i - 1].y === y && IT[i - 1].p === IT[i].p) return '';
  return '<div class="vtype">॥ ' + esc(T(nm[0], nm[1])) + ' ॥</div>';
}
function pageHTML(pg){
  const p = PAGES[pg], a = Math.max(p.from, R.a), b = Math.min(p.to, R.b); let h = '<div class="pg" data-pg="' + pg + '">';
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
  else { const P = PLAN[R.org]; if (R.n < P.n) h += '<button class="btn" data-next="' + dayRange(R.org, R.n + 1)[0] + '">' + VN(R.n + 1) + ' ›</button>'; }
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
  const t = topicAt.get(i), el = (t && document.getElementById('t' + i)) || document.getElementById('v' + i);
  if (!el) return; const y = el.getBoundingClientRect().top + scrollY - 70; window.scrollTo({top: Math.max(0, y), behavior: smooth ? 'smooth' : 'auto'});
}
function topVisibleItem(){
  for (const y of [96, 140, 200, 280]){ const el = document.elementFromPoint(innerWidth / 2, y); const v = el && el.closest && el.closest('.verse'); if (v) return +v.dataset.i; const nxt = el && el.closest && (el.closest('.topic-h, .part-h, .pause')); if (nxt){ let s = nxt.nextElementSibling; while (s && !s.classList.contains('verse')) s = s.nextElementSibling; if (s) return +s.dataset.i; } }
  const vs = $$('#rBody .verse'); for (const v of vs){ if (v.getBoundingClientRect().bottom > 80) return +v.dataset.i; } return R.a;
}
function curSection(i){ const t = topicOf(i); return t && t.i <= R.b && t.end >= R.a ? t : null; }
function updateHeader(){
  if (!IT.length) return; const i = topVisibleItem(), t = topicOf(i);
  const s = curSection(i), where = R.org === 'k' ? (PARTS.length > 1 ? KNAME(R.n) : '') : VN(R.n), topic = s ? TNAME(s) : '';
  $('#rMid').innerHTML = '<span class="ml">' + (s ? spanLabel(Math.max(s.i, R.a), Math.min(s.end, R.b)) : spanLabel(R.a, R.b)) + ' ▾</span><small>' + esc(where || TT(W.title)) + '</small>';   // only the part (or reading day): a small footer (owner, 2026-10-19); the topic heads the page
}
let scT;
window.addEventListener('scroll', () => { if (!$('#reader').classList.contains('on')) return; ensure(); clearTimeout(scT); scT = setTimeout(() => { updateHeader(); savePos(); }, 200); }, {passive: true});
function savePos(i){ if (i == null) i = topVisibleItem(); const ws = WS(); ws.pos[R.org] = i; ws.last = {org: R.org, i, id: IT[i].id}; save(); }
// A place is found again by its item id. Places saved before ids were kept are item positions; when a work later had
// verses put before its text (work.json "prepended": how many), such a place moves forward by that many, once.
// work.json "renamed" (old item id → new): a joint caupāī split into one item each (owner, 2026-10-20). A reader's notes,
// bookmarks and place on the old id move to its first part; a meaning correction moves to the last part (where the
// joint meaning now is); timing marks to the first part. A verse-text correction of the old joint verse is left as it was.
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
  if (l.id != null){ if (ID[l.id] != null) l.i = ID[l.id]; else { ws.last = null; delete ws.pos[l.org]; }   // a place at a verse no longer in the text is dropped (2026-10-20)
    for (const o in ws.pos) if (!IT[ws.pos[o]]) delete ws.pos[o]; return; }
  const sh = i => (W.prepended || 0) + (W.split || []).reduce((n, [at, add]) => n + (at < i ? add : 0), 0);   // items added before it since then ("split": joint caupāīs made separate)
  l.i += sh(l.i);
  if (IT[l.i]) l.id = IT[l.i].id; else ws.last = null;
  for (const o in ws.pos) ws.pos[o] += sh(ws.pos[o]);
}
function openReader(org, i, flash){
  if (!S.hinted && !TOUR){ S.hinted = 1; save(); setTimeout(() => toast(T('किसी शब्दको छूकर अर्थ देखें · नीचेसे प्रसंग चुनें', 'Tap any word for its meaning · choose a section at the bottom')), 900); }
  R.org = org; [R.a, R.b, R.n] = rangeFor(org, i);
  if (!$('#reader').classList.contains('on')) show('reader');
  renderAround(i); if (flash){ const el = document.getElementById('v' + i); if (el) el.classList.add('flash'); }
  savePos(i);
}
function reopenReader(){ fixLast(); const l = WS().last; if (l && IT[l.i]) openReader(l.org, l.i); else show('home', false); }
function jumpTo(i){
  if (i < R.a || i > R.b){ openReader(R.org, i); return; }
  const pg = itemPage[i];
  if (pg >= R.pf && pg <= R.pt) scrollToItem(i, false); else renderAround(i);
  setTimeout(() => { updateHeader(); savePos(i); }, 60);
}
function refreshReader(){
  if (!$('#reader').classList.contains('on')) return;
  const i = topVisibleItem(), el = document.getElementById('v' + i), off = el ? el.getBoundingClientRect().top : 80;
  const pf = R.pf, pt = R.pt; let h = ''; for (let p = pf; p <= pt; p++) h += pageHTML(p);
  $('#pages').innerHTML = h; $('#endB').innerHTML = endHTML();
  const el2 = document.getElementById('v' + i); if (el2) window.scrollBy(0, el2.getBoundingClientRect().top - off);
  if (PL.on && PL.cur >= 0){ const c = document.getElementById('v' + PL.cur); if (c) c.classList.add('now'); }
  updateHeader();
}
function rerenderItem(i){ const el = document.getElementById('v' + i); if (!el) return; const tmp = document.createElement('div'); tmp.innerHTML = verseHTML(i); el.replaceWith(tmp.firstChild); if (PL.on && PL.cur === i) document.getElementById('v' + i).classList.add('now'); }
// The section picker: the row of kāṇḍas (or plan days) on top only chooses which list shows below; nothing opens until a
// section is tapped — the current one too (owner, 2026-10-19).
function sectionSheet(n){
  const cur = curSection(topVisibleItem()), plan = R.org !== 'k';
  if (n == null) n = R.n;
  const [A, B] = plan ? dayRange(R.org, n) : [PARTS[n].a, PARTS[n].b];
  let h = '';
  if (!plan) h += '<div class="pick">' + PARTS.map(p => '<button data-pick="' + p.k + '" class="' + (p.k === n ? 'on' : '') + '">' + esc(KNAME(p.k)) + '</button>').join('') + '</div>';
  else { const P = PLAN[R.org]; h += '<div class="pick days">' + Array.from({length: P.n}, (_, x) => x + 1).map(d => '<button data-pick="' + d + '" class="' + (d === n ? 'on' : '') + (DONE(ME(), R.org)[d] ? ' done' : '') + '">' + DEV(d) + '</button>').join('') + '</div>'; }
  const secs = TOPICS.filter(t => t.i <= B && t.end >= A);
  const rows = []; if (!secs.length || secs[0].i > A) rows.push({i: A, end: (secs[0] ? secs[0].i - 1 : B), name: plan ? VN(n) : KNAME(n)});
  secs.forEach(t => rows.push({i: Math.max(t.i, A), end: Math.min(t.end, B), name: TNAME(t), t}));
  h += '<h2>' + (plan ? PNAME(R.org) + ' · ' + VN(n) : esc(KNAME(n))) + '</h2><div class="secs">' + rows.map(r => '<button data-to="' + r.i + '" class="' + (cur && r.t === cur && n === R.n ? 'on' : '') + '"><span class="sr">' + spanLabel(r.i, r.end) + '</span><span class="sn">' + esc(r.name) + '</span></button>').join('') + '</div>';
  if ($('#sheet').classList.contains('on') && $('#sheetBody .pick')){ $('#sheetBody').innerHTML = h; $('#sheet').scrollTop = 0; } else openSheet(h);
  $$('#sheetBody [data-pick]').forEach(b => b.onclick = () => sectionSheet(+b.dataset.pick));
  $$('#sheetBody [data-to]').forEach(b => b.onclick = () => { closeSheet(); jumpTo(+b.dataset.to); });
  const on = $('#sheetBody .secs .on'); if (on) setTimeout(() => on.scrollIntoView({block: 'center'}), 60);
}
$('#rMid').onclick = () => sectionSheet();   // not the click event as the part (that broke the footer, 2026-10-20)
$('#rBack').onclick = back;
// the same हिं · En · शब्द switch in every header (library, work, reader): one setting, shown and changed anywhere
$$('.lyr.layers button').forEach(b => b.onclick = () => { if (b.dataset.l === 'r'){ toggleRecite(); return; }
  if (S.settings.recite){ S.settings.recite = false; delete S.settings.preRecite; applyRecite(); }   // a meaning turned on ends recitation mode
  const was = LANG(), l = b.dataset.l; S.settings.layers[l] = !S.settings.layers[l]; save(); syncLayers();
  if (LANG() !== was) applyLang();
  const v = CURVIEW; if (v === 'reader') refreshReader(); });
// हिं · En on the library and work pages: one choice, the language of the app
$$('.lyr.uilang button').forEach(b => b.onclick = () => { if (S.settings.ui === b.dataset.u) return; S.settings.ui = b.dataset.u; save(); applyLang(); syncLayers(); onView(CURVIEW); });
function syncLayers(){ $$('.lyr.layers button').forEach(b => b.classList.toggle('on', b.dataset.l === 'r' ? !!S.settings.recite : layerOn(b.dataset.l))); $$('.lyr.uilang button').forEach(b => b.classList.toggle('on', S.settings.ui === b.dataset.u)); }
function applyRecite(){ document.body.classList.toggle('recite', !!S.settings.recite); $('#rRecite').hidden = true; syncLayers(); }
// recitation mode is the fourth button of the reader's हिं · En · शब्द · 📖 capsule (owner, 2026-10-19): turning it on hides
// the meanings (the layers that were on are remembered); turning it off — or turning any meaning on — brings them back
function toggleRecite(){
  const on = !S.settings.recite; S.settings.recite = on;
  if (on){ S.settings.preRecite = Object.assign({}, S.settings.layers); S.settings.layers.h = S.settings.layers.e = S.settings.layers.w = false; }
  else if (S.settings.preRecite){ Object.assign(S.settings.layers, S.settings.preRecite); delete S.settings.preRecite; }
  save(); applyRecite(); applyLang(); if (CURVIEW === 'reader') refreshReader();
  toast(on ? T('पाठ मोड: केवल मूल पाठ', 'Recitation mode: verses only') : T('अर्थ फिर दिखेंगे', 'Meanings shown again'));
}
$('#rRecite').onclick = toggleRecite;
// One ☰ sheet on every page (owner, 2026-10-22): Bookmarks & notes (inside a work), the dark theme, the tour, and "More" — a
// page with the rare things (transliteration, sources, audio timing, my file, privacy). Nothing here repeats the header:
// the meanings, recitation mode, the text size and the language are the header's capsules; sections are the reader's
// footer; the playing speed is in the player.
function mainMenu(){
  const inWork = !!W && CURVIEW !== 'library', th = S.settings.theme;
  openSheet('<div class="menu">' + (inWork ? '<button data-m="bm"><svg><use href="#i-bm"/></svg>' + LB.bm() + '</button>' : '') +
    '<div class="menusw">' + sw('mth', T('गहरा रंग (रात)', 'Dark theme'), '', th === 'dark', 'theme') + '</div>' +
    (S.timing.on && inWork ? '<div class="menusw"><label class="sw tsw"><svg class="swic" style="stroke:var(--saffron)"><use href="#i-clock"/></svg><span style="flex:1">' + T('ऑडियोका समय', 'Audio timing') + '</span><span class="tg"><input type="checkbox" id="mtm" checked><span></span></span></label></div>' + (SRC.au && Object.keys(myStarts()).filter(id => ID[id] != null).length ? '<button data-m="tclear" class="tsaf"><svg><use href="#i-undo"/></svg>' + T('मेरे बदलाव हटाएँ', 'Clear adjustments') + '</button>' : '') : '') +
    '<button data-tour><svg><use href="#i-tour"/></svg>' + LB.tour() + '</button>' +
    '<button data-m="set"><svg><use href="#i-set"/></svg>' + LB.more() + '</button></div>');
  if ($('#mtm')) $('#mtm').onchange = async () => { S.timing.on = false; save(); applyTiming(); stopAudio(); closeSheet(); await loadSources(); if (CURVIEW === 'reader') refreshReader(); if (CURVIEW === 'settings') renderSettings(); toast(T('ऑडियोका समय: बंद', 'Audio timing: off')); };   // while on, ☰ turns it off (owner, 2026-10-22)
  $('#mth').onchange = e => { S.settings.theme = e.target.checked ? 'dark' : 'light'; applyTheme(); save(); };   // light or dark, nothing else (owner, 2026-10-22)
}
$('#rMore').onclick = mainMenu;
$('#sheetBody').addEventListener('click', ev => {
  const b = ev.target.closest('[data-m]'); if (!b) return;
  const m = b.dataset.m; closeSheet();
  if (m === 'search') openSearch('text'); if (m === 'sec') sectionSheet();
  if (m === 'font') fontSheet(); if (m === 'bm') show('bookmarks'); if (m === 'set') show('settings'); if (m === 'tclear') clearTimingAsk();
});
function setSize(d){
  const i = topVisibleItem(); S.settings.size = Math.max(16, Math.min(34, S.settings.size + d)); applyTheme(); save();
  if ($('#reader').classList.contains('on') && i != null) scrollToItem(i);
  toast(LB.size() + ' ' + DEV(S.settings.size));
}
$$('.szm').forEach(b => b.onclick = () => setSize(-2)); $$('.szp').forEach(b => b.onclick = () => setSize(2));
function fontSheet(){
  openSheet('<h2>' + LB.size() + '</h2><input type="range" id="fs" min="16" max="34" step="1" value="' + S.settings.size + '" style="border:0;padding:0"><p class="vtext" id="fsDemo" style="font-size:' + S.settings.size + 'px">' + esc(IT[0] ? IT[0].v[0].slice(0, 28) : '') + '</p>');
  $('#fs').oninput = () => { S.settings.size = +$('#fs').value; $('#fsDemo').style.fontSize = S.settings.size + 'px'; applyTheme(); save(); };
}
$('#rBody').addEventListener('click', ev => {
  const nx = ev.target.closest('[data-next]'); if (nx){ openReader(R.org, +nx.dataset.next); return; }
  const v = ev.target.closest('.verse'), i = v ? +v.dataset.i : null;
  const a = ev.target.closest('[data-a]');
  if (a){
    const act = a.dataset.a;
    if (act === 'play') playFrom(i, i);   // ▶ beside a verse plays that verse; “Listen from here” keeps going
    else if (act === 'tstart' || act === 'tend'){
      if (!PL.on || !ytOK){ toast(T('पहले ऑडियो चलाएँ — फिर जिस पदको सुन रहे हैं उसीके बटन दबाएँ', 'Start the audio first, then tap the buttons of the verse you are hearing')); return; }
      setTime(i, act === 'tstart' ? 1 : 2, nowAt()); rerenderItem(i);
    }
    else if (act === 'tn'){ const x = SRC.au.at[IT[i].id], k = +a.dataset.k; if (setTime(i, k, Math.max(0, x[k] + a.dataset.d * step())) === false) return; rerenderItem(i); if (!livePlay()) snippet(i, k); }
    else if (act === 'tok'){ unfrom(IT[i].id); save(); rerenderItem(i); toast(T('जाँच लिया — अब यह आपका है', 'Checked — it is now yours')); }
    else if (act === 'tundo'){ clearStart(i); toast(T('पहले जैसा', 'Restored')); }
    else if (act === 'tnone'){ setTime(i, 2, null); rerenderItem(i); }
    else if (act === 'bm'){ const me = ME(), k = KEY(IT[i].id); const had = !!me.bm[k]; if (had) delete me.bm[k]; else { me.bm[k] = Date.now(); if (TOUR) TOUR.bmAdded = true; } save(); rerenderItem(i); toast(!had ? T('बुकमार्क जोड़ा', 'Bookmarked') : T('बुकमार्क हटाया', 'Bookmark removed')); }
    else if (act === 'enote') noteSheet(i, +a.dataset.k);
    else if (act === 'menu') itemMenu(i);
    else if (act === 'done'){ const o = a.dataset.o, n = +a.dataset.n, d = DONE(ME(), o); if (d[n]) delete d[n]; else d[n] = Date.now(); save(); const box = a.closest('.pause'); const tmp = document.createElement('div'); tmp.innerHTML = pauseHTML(+a.dataset.i); const nb = Array.from(tmp.children).find(x => x.dataset.pause === o + n); if (box && nb) box.replaceWith(nb); if (d[n]) toast(VN(n) + T(' पूर्ण — जय श्रीराम', ' complete — Jai Shri Ram')); }
    return;
  }
  const w = ev.target.closest('.w'); if (w){ w.classList.add('sel'); const vb = w.closest('.verse'); wordSheet(w.dataset.w || w.textContent, null, vb ? langOf(+vb.dataset.i) : W.lang); }
});
function noteSheet(i, k){
  const me = ME(), key = KEY(IT[i].id), arr = me.notes[key] || [], cur = k != null ? arr[k] : null;
  openSheet('<h2>' + (cur ? T('टिप्पणी बदलें', 'Edit note') : T('अपनी टिप्पणी लिखें', 'Write a note')) + '</h2><p class="small muted">' + esc(itemLabel(i)) + '</p><textarea id="nt" placeholder="' + T('अपने विचार, भाव या कथा यहाँ लिखें…', 'Your thoughts or the story behind this verse…') + '">' + esc(cur ? cur.t : '') + '</textarea><div class="acts"><button class="btn" id="nSave">' + T('सेव करें', 'Save') + '</button>' + (cur ? '<button class="btn ghost" id="nDel">' + T('हटाएँ', 'Delete') + '</button>' : '') + '</div>');
  setTimeout(() => $('#nt').focus(), 250);
  $('#nSave').onclick = () => { const t = $('#nt').value.trim(); if (!t){ closeSheet(); return; } if (cur){ cur.t = t; cur.ts = Date.now(); } else { (me.notes[key] = arr).push({t, ts: Date.now()}); } save(); closeSheet(); rerenderItem(i); toast(T('टिप्पणी सेव हुई', 'Note saved')); };
  if ($('#nDel')) $('#nDel').onclick = () => { arr.splice(k, 1); if (!arr.length) delete me.notes[key]; save(); closeSheet(); rerenderItem(i); };
}
function itemMenu(i){
  const id = IT[i].id, edited = verseOf(i).edited || ['hi', 'en'].some(k => { const m = mean(k, i); return m && m.edited; });
  openSheet('<p class="small muted">' + esc(itemLabel(i)) + '</p><div class="menu">' + (hasAu(i) ? '<button data-x="play"><svg><use href="#i-play"/></svg>' + T('यहाँसे सुनें', 'Play from here') + '</button>' : '') + '<button data-x="copy"><svg><use href="#i-copy"/></svg>' + T('मूल पाठ और अर्थ कॉपी करें', 'Copy verse and meaning') + '</button><button data-x="note"><svg><use href="#i-note"/></svg>' + T('टिप्पणी लिखें', 'Write a note') + '</button><button data-x="edit"><svg><use href="#i-edit"/></svg>' + T('पद या अर्थमें सुधार करें', 'Correct the verse or meaning') + '</button>' + (edited ? '<button data-x="revert"><svg><use href="#i-edit"/></svg>' + T('मेरा सुधार हटाएँ (पद लौटाएँ)', 'Remove my correction (restore the verse)') + '</button>' : '') + '</div>');
  $$('#sheetBody [data-x]').forEach(b => b.onclick = () => {
    const x = b.dataset.x; closeSheet();
    if (x === 'play') playFrom(i, null);
    if (x === 'copy'){ const mh = mean('hi', i), me_ = mean('en', i); const txt = verseOf(i).v.join('\n') + (mh ? '\n\n' + mh.x : '') + (me_ ? '\n\n' + me_.x : ''); (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(() => toast(T('कॉपी हो गया', 'Copied'))).catch(() => toast(T('कॉपी नहीं हो सका', 'Could not copy'))); }
    if (x === 'note') noteSheet(i, null);
    if (x === 'edit') editSheet(i);
    if (x === 'revert'){ S.profiles.forEach(p => { delete p.fix[KEY(id)]; ['hi', 'en'].forEach(k => { if (SRC[k]) delete p.fix[KEY(SRC[k].id + ':' + id)]; }); }); save(); rerenderItem(i); toast(T('पद लौटाया', 'Verse restored')); }
  });
}
function editSheet(i){
  const id = IT[i].id, vv = verseOf(i), mh = mean('hi', i), me_ = mean('en', i);
  openSheet('<h2>' + T('सुधार करें', 'Correct') + '</h2><p class="small muted">' + T('अपनी छपी पुस्तकसे मिलाकर सुधारें। मूल डेटा नहीं बदलेगा — सुधार आपकी फ़ाइलमें रहेगा और कभी भी हटाया जा सकता है।', 'Your correction is kept in your file and can be removed any time.') + '</p><div class="field"><label>' + esc(itemLabel(i)) + '</label><textarea id="ev" style="font-weight:700">' + esc(vv.v.join('\n')) + '</textarea></div>' + (mh ? '<div class="field"><label>' + LB.h() + ' · ' + esc(TT(SRC.hi.meta.title)) + '</label><textarea id="eh">' + esc(mh.x) + '</textarea></div>' : '') + (me_ ? '<div class="field"><label>' + LB.e() + ' · ' + esc(TT(SRC.en.meta.title)) + '</label><textarea id="ee" class="lat">' + esc(me_.x) + '</textarea></div>' : '') + '<div class="acts"><button class="btn" id="eSave">' + T('सेव करें', 'Save') + '</button></div>');
  $('#eSave').onclick = () => {
    const me = ME(); const v = $('#ev').value.split('\n').map(s => s.trim()).filter(Boolean);
    if (v.join('\n') !== IT[i].v.join('\n')) me.fix[KEY(id)] = {v}; else delete me.fix[KEY(id)];
    [['hi', '#eh'], ['en', '#ee']].forEach(([k, sel]) => { if (!$(sel) || !SRC[k]) return; const x = $(sel).value.trim(), orig = (SRC[k].m[id] || [])[0], key = KEY(SRC[k].id + ':' + id); if (x !== orig) me.fix[key] = {m: x}; else delete me.fix[key]; });
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
  // − / + sit on either side of "Starts now" / "Ends now", in the same line (owner, 2026-10-19): for a start you set, and for an end that is set
  const grp = (k, act, label, on) => '<span class="tgrp">' + (on ? '<button class="tn" data-a="tn" data-k="' + k + '" data-d="-1" aria-label="−">−</button>' : '') + '<button data-a="' + act + '">' + label + '</button>' + (on ? '<button class="tn" data-a="tn" data-k="' + k + '" data-d="1" aria-label="+">+</button>' : '') + '</span>';
  // a time set by ear — on this phone ("yours") or by the owner and already in the library ("sent") — has − / + for fine-tuning
  // under the times: "Until next" when an end is set; ↶ Undo is the verse's bottom-left corner; the step is in the player bar (owner, 2026-10-22) — nothing timing-related is left in the ⋮ menu (owner, 2026-10-22)
  const chips = own && x && x[2] != null ? '<button class="tchip" data-a="tnone">' + T('अगले पद तक', 'Until next') + '</button>' : '';
  return '<div class="tmark">' + grp(1, 'tstart', '⏱ ' + T('अभी शुरू', 'Starts now'), !!(own && x)) + grp(2, 'tend', '⏹ ' + T('अभी समाप्त', 'Ends now'), !!(own && x && x[2] != null)) + (by ? '<button data-a="tok">✓ ' + T('सही है', 'Correct') + '</button>' : '') + 
    '<span class="tinfo">' + when + (by ? ' · <b class="test">' + T('', 'from ') + esc(by) + T(' का — जाँचें', ' — to check') + '</b>' : mine ? ' · <b>' + T('आपका', 'yours') + '</b>' : own ? ' · <b>' + T('भेजा हुआ', 'sent') + '</b>' : est && SRC.au.checkSet.has(IT[i].id) ? ' · <b class="test">' + T('अनुमान', 'estimated') + '</b>' : est ? ' · <b class="test">' + T('आपके समयके अनुसार खिसकाया', 'moved to fit your times') + '</b>' : '') + '</span>' + (chips ? '<span class="tchips">' + chips + '</span>' : '') + '</div>';
}
// how far each − / + moves a time: the saffron ±… s chip in the player bar, beside ✕, shown while timing is on (owner, 2026-10-22; it was in the ⋮ menu)
const STEPS = [0.1, 0.25, 0.5, 1];
function syncStep(){ const b = $('#pStep'); b.hidden = !S.timing.on; b.textContent = '±' + step() + ' s'; }
$('#pStep').onclick = () => { S.timing.step = STEPS[(STEPS.indexOf(step()) + 1) % STEPS.length]; save(); syncStep(); toast('− / + = ' + step() + ' s'); };
function step(){ return S.timing.step || 0.5; }
// a start that is only a guess — listed to be checked by the library, or placed again by text length to fit the set times — and not set by ear on this phone
function toCheck(i){ const id = IT[i].id, A = SRC.au; return !!(S.timing.on && A && A.checkSet && (A.checkSet.has(id) || (A.moved && A.moved.has(id))) && !myStarts()[id]); }
function myStarts(){ return (SRC.au && S.timing.fix[tkey()]) || {}; }
// a verse set by ear: on this phone (myStarts), or by the owner and published (the audio JSON's "own" list) — kept exactly as given
function ownAt(id){ const A = SRC.au; return myStarts()[id] || (A && A.ownSet && A.ownSet.has(id) ? A.at0[id] : undefined); }
function fromOf(id){ return SRC.au ? (S.timing.from[tkey()] || {})[id] : undefined; }
function unfrom(id){ const f = S.timing.from[tkey()]; if (f){ delete f[id]; if (!Object.keys(f).length) delete S.timing.from[tkey()]; } }
function buildAudio(){
  AUT = []; const A = SRC.au; if (!A) return;
  if (!A.at0){   // the published times; A.at = those plus the starts set by ear on this phone, after the order rule below
    A.at0 = A.at; A.checkSet = new Set(A.check || []); A.guessSet = new Set(A.guess || []); A.ownSet = new Set(A.own || []); A.raw = A.raw || {};
  }
  A.at = Object.assign({}, A.at0, myStarts());
  A.tracks.forEach(t => { t.fi = ID[t.first]; t.li = ID[t.last]; }); AUT = A.tracks.map(() => []);
  // the rule starts from the start each verse had before any re-placing ("raw", kept by make_timings.py for the verses it
  // moved), so the app and the library, given the same set times, arrive at exactly the same figures
  for (const id in A.at){ const i = ID[id]; if (i == null) continue; const [t, s, e] = A.at[id]; AUT[t].push([i, A.raw[id] != null && !myStarts()[id] ? A.raw[id] : s, e == null ? null : e]); }
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
function hasAu(i){ return !!(SRC.au && SRC.au.at[IT[i].id]); }
function firstAu(a, b){ for (let i = a; i <= b; i++) if (hasAu(i)) return i; return null; }
/* YouTube embed driven by postMessage (no external script needed) */
function ytFrame(){ return $('#ytf'); }
function ytPost(func, args){ const f = ytFrame(); if (f && f.contentWindow) f.contentWindow.postMessage(JSON.stringify({event: 'command', func, args: args || []}), '*'); }
function ytLoad(vid, start){
  ytVid = vid; ytOK = false; ytInfo = {t: start, st: -1, d: 0};
  $('#ytBox').innerHTML = '<iframe id="ytf" width="200" height="200" src="https://www.youtube.com/embed/' + vid + '?enablejsapi=1&autoplay=1&playsinline=1&rel=0&modestbranding=1&start=' + Math.floor(start) + (location.origin && location.origin !== 'null' ? '&origin=' + encodeURIComponent(location.origin) : '') + '" title="YouTube" frameborder="0" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>';
  const f = ytFrame(); let n = 0;
  const hello = () => { if (ytOK || n++ > 20) return; try { f.contentWindow.postMessage(JSON.stringify({event: 'listening', id: 'manas', channel: 'widget'}), '*'); } catch (e) {} setTimeout(hello, 500); };
  f.addEventListener('load', hello);
  clearTimeout(ytWait); ytWait = setTimeout(() => { if (!ytOK && PL.on) ytBlocked(); }, 5000);
}
// Playing speed (owner, 2026-10-20): 0.5× to 2× — YouTube's own speed, so the verse times (in the recording's
// time) stay right; the light follows the recording. Chosen in the reader's ☰ and in Settings; kept for next time.
const RATES = [0.5, 0.75, 1, 1.25, 1.5, 2];
function RATE(){ return S.settings.rate || 1; }
function applyRate(){ if (ytOK) ytPost('setPlaybackRate', [RATE()]); if (PL.on) $('#pTrack').textContent = playingName(); $('#pRate').textContent = RATE() + '×'; }
// the speed button in the player bar (owner, 2026-10-22): one tap moves to the next speed, round and round
$('#pRate').onclick = () => { S.settings.rate = RATES[(RATES.indexOf(RATE()) + 1) % RATES.length]; save(); applyRate(); toast(T('गति ', 'Speed ') + RATE() + '×'); };
/* outside the website (e.g. a claude.ai artifact) YouTube cannot be embedded: open YouTube's own player page, which can stop at the end of what was asked */
function ytWatchURL(){
  const A = SRC.au, st = Math.floor(ytInfo.t || 0); let end = '';
  if (PL.end != null){ const nx = A.at[(IT[PL.end + 1] || {}).id]; if (nx && nx[0] === PL.t) end = '&end=' + Math.ceil(nx[1]); }
  return 'https://www.youtube.com/embed/' + ytVid + '?autoplay=1&start=' + st + end;
}
function ytBlocked(){
  $('#ytBox').innerHTML = '<div class="ytno"><p>' + T('यह पन्ना YouTube वीडियो नहीं चला पा रहा।', 'This page is not allowed to play YouTube here.') + '</p><a class="btn" target="_blank" rel="noopener" href="' + ytWatchURL() + '">' + T('YouTube पर इसी दोहे से सुनें ↗', 'Play on YouTube from this verse ↗') + '</a></div>';
}
window.addEventListener('message', e => {
  if (!/youtube(-nocookie)?\.com$/.test((e.origin || '').replace(/^https?:\/\/(www\.)?/, ''))) return;
  let d; try { d = typeof e.data === 'string' ? JSON.parse(e.data) : e.data; } catch (x) { return; }
  if (!d) return;
  if (d.event === 'onReady' || d.event === 'initialDelivery' || d.event === 'infoDelivery'){ if (!ytOK){ ytOK = true; if (RATE() !== 1) ytPost('setPlaybackRate', [RATE()]); if (PL.on) $('#pTrack').textContent = playingName(); if (PL.on && PL.snip != null && PL.seekT != null) ytPost('seekTo', [PL.seekT, true]); } }   // a preview in a freshly loaded player: the page can only start it at a whole second, so seek to the exact time
  const info = d.info || {};
  if (typeof info.currentTime === 'number'){ ytInfo.t = info.currentTime; ytInfo.at = performance.now(); }
  if (typeof info.playbackRate === 'number' && info.playbackRate !== RATE() && ytOK && PL.on) ytPost('setPlaybackRate', [RATE()]);
  if (typeof info.duration === 'number' && info.duration) ytInfo.d = info.duration;
  if (typeof info.playerState === 'number'){ ytInfo.st = info.playerState; syncPlayer(); if (info.playerState === 0) onEnded(); }
  if (d.event === 'onStateChange' && typeof d.info === 'number'){ ytInfo.st = d.info; syncPlayer(); if (d.info === 0) onEnded(); }
});
/* what is playing, in the app's own words: the reading (kāṇḍa or plan day) and the reciter — never the recording's title */
function playingName(){ return (R.org === 'k' ? KNAME(R.n) : TT(PLAN[R.org].name) + ' · ' + VN(R.n)) + ' · ' + TT(SRC.au.meta.title); }   // the speed has its own button in the bar
// Fine-tuning preview (owner, 2026-10-19): after − / + on a start, the first 2 s of the verse play from the new start; on an
// end, the last 2 s up to the new end. Then the player pauses, so the next tap can follow at once.
let snipT = null;
// the preview plays only when nothing is playing live (owner, 2026-10-20): while the recitation runs on, − / + just move the
// time, so marking can go on from what is heard; a preview that is itself playing is replaced by the next one
function livePlay(){ return PL.on && playing() && PL.snip == null; }
function snippet(i, k){
  const x = SRC.au.at[IT[i].id]; if (!x) return; const tr = SRC.au.tracks[x[0]];
  const t0 = k === 1 ? x[1] : Math.max(x[1], x[2] - 2), t1 = k === 1 ? (x[2] != null ? Math.min(x[2], x[1] + 2) : x[1] + 2) : x[2];
  PL.on = true; PL.t = x[0]; PL.end = null; PL.snip = t1; PL.whole = false; PL.endMsg = '';
  $('#player').hidden = false; document.body.classList.add('playing');
  seekGuard(t0);
  if (ytVid !== tr.yt || !ytFrame()) ytLoad(tr.yt, t0); else { ytPost('seekTo', [t0, true]); ytPost('playVideo'); ytInfo.t = t0; ytInfo.at = performance.now(); }
  setCur(i); $('#pTrack').textContent = playingName(); syncPlayer();
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
  const st = (end != null && i === tr.fi) ? 0 : st0;
  PL.on = true; PL.t = t; PL.end = end; PL.cur = -1; PL.whole = false; PL.endMsg = '';
  $('#player').hidden = false; document.body.classList.add('playing'); wake(true);
  seekGuard(st);
  if (ytVid !== tr.yt || !ytFrame()) ytLoad(tr.yt, st); else { ytPost('seekTo', [st, true]); ytPost('playVideo'); ytInfo.t = st; ytInfo.at = performance.now(); }
  setCur(i); $('#pTrack').textContent = playingName(); syncPlayer();
}
// Right after a seek the player still reports its old time (or a moment before the asked-for one), which would light the
// previous verse for a beat (owner, 2026-10-19). Until it reports a time at the asked-for start (at most 4 s), use that start.
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
    // the verse or stretch asked for has ended: stop, and offer to go on from the next verse (owner, 2026-10-19)
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
  // a verse whose set end has passed hands the light to the next verse at once, in both modes (owner, 2026-10-20) — even when
  // that verse starts a little later; the same in Settings › Audio timing on or off
  const m = at(show), e2 = endOf(show);
  if (e2 != null && time >= e2 && m >= 0 && m + 1 < a.length) show = a[m + 1][0];
  setCur(show);
  const d = ytInfo.d || SRC.au.tracks[PL.t].dur; $('#pProg').style.width = (100 * time / d) + '%';
}
setInterval(tick, 300);
/* place the verse being recited in the space between the top bar and the player:
   centred if it fits, otherwise with its first line just below the top bar (never hidden under it) */
// The verse being recited is kept at the top, just below the bar, and the text moves up under it, so the next verses are
// always in view — even when the recording runs a little ahead of the timings (owner, 2026-10-20). A verse-type heading
// (॥ चौपाई ॥) right above it stays with it.
function keepInView(el){
  const top = $('#reader .bar').getBoundingClientRect().bottom, prev = el.previousElementSibling;
  const head = prev && prev.classList && prev.classList.contains('vtype') ? prev : el;
  window.scrollTo({top: Math.max(0, scrollY + head.getBoundingClientRect().top - (top + 6)), behavior: 'smooth'});
}
function setCur(i){
  if (PL.cur === i) return; PL.cur = i;
  $$('#rBody .verse.now').forEach(v => v.classList.remove('now'));
  $('#pVerse').textContent = KNAME(IT[i].p) + ' · ' + posLabel(i); $('#pTrack').textContent = playingName();
  if (!$('#reader').classList.contains('on')) return;
  if (i < R.a || i > R.b){ R.org = R.org; [R.a, R.b, R.n] = rangeFor(R.org, i); renderAround(i); }
  else if (!document.getElementById('v' + i)) renderAround(i, false);
  const el = document.getElementById('v' + i);
  // while timings are being marked the page is not moved under your finger: it only follows when the lit verse leaves the screen
  // the player's timing wins (owner, 2026-10-20): the page follows the light every time a new verse starts, whatever was
  // touched or scrolled meanwhile — no pause after a touch
  if (el){ el.classList.add('now'); if (!(S.timing.on && inView(el))) keepInView(el); }
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
    // this verse when the verse before it ended, so that end is its start (owner, 2026-10-19); otherwise ask for the start.
    const pe = j > 0 ? endOf(a[j - 1][0]) : null, mine = !!ownAt(id);   // a start set by ear (here or sent) is never moved by this rule
    if (!mine && pe != null && pe < v[2]) v[1] = pe;
    else { toast(mine ? T('अंत शुरुआतके बाद होना चाहिये', 'The end must come after the start') : T('पहले “अभी शुरू” से इसकी शुरुआत लगाएँ', 'Mark its start first (Starts now)')); return false; }
  }
  if (k === 1 && v[2] != null && v[2] <= v[1]) v[2] = null;
  // Order is kept between the verses set by ear (owner): a start cannot go before the previous set start, or at or past the
  // next set start — say which verse is in the way, so it can be moved first
  if (k === 1 && p && v[1] <= p[1] + 0.1){ toast(T('पिछला पद इसके बाद शुरू होता है (', 'The verse before starts later than that (') + fmtT(p[1]) + T(') — पहले उसकी शुरुआत आगे-पीछे करें', ') — move its start first')); return false; }
  if (k === 1 && n && v[1] >= n[1] - 0.1){ toast(T('अगला पद इससे पहले शुरू होता है (', 'The next verse starts before that (') + fmtT(n[1]) + T(') — पहले उसकी शुरुआत आगे करें', ') — move its start first')); return false; }
  // Neighbours move together (owner, 2026-10-19): an end moved past the next set start carries that start with it; a start
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
  // "Ends now" also starts the next verse (owner, 2026-10-20): an end on this verse gives the verse after it, when its start
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
function refreshMarks(was, i){ Object.keys(was).forEach(q => { q = +q; if (q === i || was[q] !== JSON.stringify(SRC.au.at[IT[q].id]) + toCheck(q) + !!myStarts()[IT[q].id]) rerenderItem(q); }); }
function marksNow(){ const was = {}; $$('#rBody .verse').forEach(el => { const q = +el.dataset.i; was[q] = JSON.stringify(SRC.au.at[IT[q].id]) + toCheck(q) + !!myStarts()[IT[q].id]; }); return was; }
function setStart(i, sec){ setTime(i, 1, sec); }
function clearStart(i){ const fx = S.timing.fix[tkey()] || {}, was = marksNow(); delete fx[IT[i].id]; unfrom(IT[i].id); if (!Object.keys(fx).length) delete S.timing.fix[tkey()]; save(); buildAudio(); refreshMarks(was, i); if (PL.on){ PL.cur = -1; tick(i); } }
function fmtT(sec){ const m = Math.floor(sec / 60), s = sec - m * 60; return m + ':' + (s < 10 ? '0' : '') + s.toFixed(1); }
function applyTiming(){ document.body.classList.toggle('timing', !!S.timing.on); syncStep(); }
$('#pPrev').onclick = () => stepVerse(-1);
$('#pNext').onclick = () => stepVerse(1);
function toPlaying(){ if (PL.cur < 0) return; if (!$('#reader').classList.contains('on')) openReader(R.org, PL.cur); const c = PL.cur; PL.cur = -1; setCur(c); }
$('#pInfo').onclick = toPlaying;
// “↓ now playing” (owner, 2026-10-20): while the lit verse is off the screen, a pill above the player names it (as the footer
// would); a tap brings it back into view. It goes as soon as the verse is on the screen again, or at the next verse's start.
$('#pJump').onclick = toPlaying;
function jumpPill(){
  const b = $('#pJump'); if (!PL.on || PL.cur < 0 || CURVIEW !== 'reader' || $('#sheet').classList.contains('on')){ b.hidden = true; return; }
  const el = document.getElementById('v' + PL.cur), r = el && el.getBoundingClientRect(), top = $('#reader .bar').getBoundingClientRect().bottom, pl = $('#player').hidden ? {top: innerHeight} : $('#player').getBoundingClientRect();
  const seen = r && r.bottom > top + 24 && r.top < pl.top - 24;   // some of the verse is on the screen
  if (seen){ b.hidden = true; return; }
  const i = PL.cur, where = R.org === 'k' ? (PARTS.length > 1 ? KNAME(IT[i].p) : '') : VN(R.n);
  const h = '<b>' + (i >= topVisibleItem() ? '↓ ' : '↑ ') + T('अभी चल रहा · ', 'Now playing · ') + esc(posLabel(i)) + '</b>'   // says what it is, not only where (owner, 2026-10-22) + (where ? '<small>' + esc(where) + '</small>' : '');
  if (b.innerHTML !== h) b.innerHTML = h; b.style.bottom = (innerHeight - pl.top + 10) + 'px'; b.hidden = false;
}
setInterval(jumpPill, 300);
function playRange(org, a, b){ const st = firstAu(a, b); if (st == null) return; openReader(org, st); playFrom(st, b); PL.whole = a === 0 && b === IT.length - 1; PL.endMsg = PL.whole ? '' : spanLabel(a, b) + T(' पूर्ण', ' finished'); }

/* ---------------- library (any depth: tradition › text › part › work) ---------------- */
let libPath = [];
function libNode(){ let n = {children: LIB}; for (const id of libPath){ const c = (n.children || []).find(x => x.id === id); if (!c) { libPath = []; return {children: LIB}; } n = c; } return n; }
function renderLibrary(){
  const node = libNode(), kids = node.children || [];
  // the way back up, in the header: Library › Hinduism › Vedas › … (the shelf you are on is the last, not a link)
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
  // a shelf shows the works on it by name (owner, 2026-10-19): tap a work to open it straight away, or the shelf's name to browse it
  const worksIn = c => { const r = []; (function w(n){ (n.children || []).forEach(x => x.work ? r.push(x) : w(x)); })(c); return r; };
  const row = (c, key) => {
    // a shelf shows two works — the ones used most recently on this phone first (S.w[id].at: last opened, read or played) — then “+N” for the rest (owner, 2026-10-23)
    const at = w => (S.w[w.work] || {}).at || 0, ws = c.work ? [] : worksIn(c).map((w, k) => [w, k]).sort((x, y) => at(y[0]) - at(x[0]) || x[1] - y[1]).map(x => x[0]), MAX = 2;
    return '<li><button class="it" data-node="' + esc(key) + '"><span class="grow"><span class="ti">' + esc(TT(c.title)) + '</span>' + (ws.length ? '' : '<br><span class="ds">' + esc(TT(c.desc || c.by) || '') + '</span>') + '</span><span class="chev">›</span></button>' +
      (ws.length ? '<div class="lworks">' + ws.slice(0, MAX).map(w => '<button data-open-work="' + esc(w.work) + '">' + esc(TT(w.title)) + '</button>').join('') + (ws.length > MAX ? '<button class="more" data-node="' + esc(key) + '">+' + DEV(ws.length - MAX) + '</button>' : '') + '</div>' : '') + '</li>';
  };
  $('#libList').innerHTML = kids.map(c => c.children ? '<li class="lhead">' + esc(TT(c.title)) + '</li>' + c.children.map(g => row(g, c.id + '/' + g.id)).join('') : row(c, c.id)).join('');
  $$('#libList [data-node]').forEach(b => b.onclick = () => {
    const ids = b.dataset.node.split('/'); let n = node, c = null; ids.forEach(id => { c = (n.children || []).find(x => x.id === id); n = c; });
    if (c.work) openWork(c.work); else { libPath.push(...ids); history.pushState(snap('library'), ''); renderLibrary(); window.scrollTo(0, 0); }
  });
  $$('#libList [data-open-work]').forEach(b => b.onclick = () => openWork(b.dataset.openWork));
  $$('#libCrumbs [data-lp]').forEach(b => b.onclick = () => { libPath = libPath.slice(0, +b.dataset.lp + 1); history.pushState(snap('library'), ''); renderLibrary(); window.scrollTo(0, 0); });
}
/* library search: finds works and shelves by title, author, edition, description or id, in either script */
const normQ = x => (x || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[\u093c]/g, '').normalize('NFC');
function libSearch(q){
  const nq = normQ(q.trim()), out = [];
  (function walk(nodes, trail){ (nodes || []).forEach(n => {
    const hay = normQ([n.id, n.path, n.work, ...['title', 'by', 'edition', 'desc'].map(k => n[k] ? (n[k].hi || '') + ' ' + (n[k].en || '') : '')].join(' '));
    if (hay.includes(nq)) out.push({n, trail});
    if (n.children) walk(n.children, trail.concat([n]));
  }); })(LIB, []);
  $('#sRes').innerHTML = out.length ? out.map((r, k) => '<button class="res" data-hit="' + k + '"><div class="where">' + esc(r.trail.map(x => TT(x.title)).join(' › ') || TT(r.n.desc || r.n.by) || '') + '</div><div class="snip" style="font-weight:700">' + esc(TT(r.n.title)) + '</div></button>').join('')
    : '<div class="empty">' + T('कुछ नहीं मिला', 'Nothing found') + '</div>';
  $$('#sRes [data-hit]').forEach(b => b.onclick = () => { const r = out[+b.dataset.hit]; if (r.n.work) openWork(r.n.work); else { libPath = r.trail.map(x => x.id).concat([r.n.id]); show('library'); } });
}
// one search page for the whole app: opened from the library it finds works and shelves; from a work, its verses
let SCOPE = 'text';
function setScope(scope){ SCOPE = scope; const lib = scope === 'lib'; $('#scope').hidden = lib; $('#q').placeholder = lib ? T('ग्रन्थ, रचयिता या विषय खोजें', 'Search works, authors or shelves') : T('शब्द, अर्थ या English में खोजें', 'Search a verse or a meaning'); }
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
// the salutation on the opening screen (owner, 2026-10-19): the work's own (library/index.json "salute": जय श्रीराम for the
// Mānas and Sundarakāṇḍa, ॐ श्री साईं राम for the Dhūpa Āratī, ੴ for the Sukhmani Sahib …), otherwise ॐ श्री परमात्मने नमः.
// The phone remembers each work's, so the screen shown before anything has loaded already greets the work being opened.
const SALUTE = '॥ ॐ श्री परमात्मने नमः ॥';
function saluteOf(id){ let r = null; (function walk(n){ (n || []).forEach(c => { if (c.work === id) r = c.salute; else walk(c.children); }); })(LIB); return r || SALUTE; }
function showSalute(text){ $('#loading').textContent = text; }
// the greeting stays at least 1.5 s so it can be read (owner, 2026-10-19); the time spent loading counts towards it
const SALUTE_MS = typeof window.__SALUTE_MS === 'number' ? window.__SALUTE_MS : 1500;
// The greeting is only for stepping into a work from the library (or the tour): never when the app starts, on a refresh
// or on Back (owner, 2026-10-19). Then the screen just waits, blank, for as long as loading takes.
let saluteAt = 0, greeted = false;
async function hideSalute(){ const left = greeted ? SALUTE_MS - (performance.now() - saluteAt) : 0; if (left > 0) await new Promise(r => setTimeout(r, left)); $('#loading').hidden = true; greeted = false; }
async function openWork(id, noShow){
  greeted = !noShow; showSalute(greeted ? saluteOf(id) : '');
  if (greeted || W === null || W.id !== id){ if ($('#loading').hidden){ $('#loading').hidden = false; } saluteAt = performance.now(); }
  try {
    if (!W || W.id !== id){ const path = workPath(id); W = await getJSON(path + '/work'); W.path = path; buildWork(); moveRenamed(); fixLast(); await Promise.all([loadSources(), loadGlossaries()]); }
    S.work = id; WS().at = Date.now(); save();   // when it was last used: the shelf lists recent works first
  } catch (e) { const off = navigator.onLine === false || await fetch('library/.ping?' + Date.now(), {cache: 'no-store'}).then(() => false, () => true);   // offline: not even a probe gets through
    toast(off ? T('इंटरनेट नहीं है — यह ग्रन्थ इस फ़ोनपर पहले खोला नहीं गया', 'No internet — this work has not been opened on this phone yet') : T('यह ग्रन्थ नहीं खुल सका', 'Could not open this work')); $('#loading').hidden = true; return; }
  await hideSalute();
  if (!noShow) show('home');
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
  $('#hTitle').textContent = TT(W.title); fitTitle(); $('#hSub').textContent = [TT(W.by), TT(W.from)].filter(Boolean).join(' · ');   // the author and, where there is one, the parent text — never the publisher or source (owner, 2026-10-19)
  // ▶ the whole work, start to end, across every part and recording
  const pa = $('#hPlayAll'), fa = firstAu(0, IT.length - 1); pa.hidden = fa == null; pa.onclick = () => playRange('k', 0, IT.length - 1);
  fixLast(); const L = WS().last;
  // one short button: continue where you left off (the reader shows where you are)
  $('#contCard').innerHTML = L && IT[L.i] ? '<button class="btn ghost cont" id="cGo">' + T('आगे पढ़ें', 'Continue') + ' ›</button>' : '';
  if ($('#cGo')) $('#cGo').onclick = () => openReader(L.org, L.i);
  const org = homeOrg();
  $('#orgSeg').innerHTML = '<button data-org="k">' + esc(TT(W.parts.name)) + '</button>' + PLANS.map(p => '<button data-org="' + p.id + '">' + esc(TT(p.name)) + '</button>').join('');
  $$('#orgSeg button').forEach(b => { b.classList.toggle('on', b.dataset.org === org); b.onclick = () => { WS().org = b.dataset.org; save(); renderHome(); }; });
  const play = (o, a, b) => firstAu(a, b) != null ? '<button class="lplay" data-po="' + o + '" data-pa="' + a + '" data-pb="' + b + '" aria-label="play"><svg><use href="#i-play"/></svg></button>' : '';
  let h = '';
  $('#orgSeg').hidden = !PLANS.length;   // a work without reading plans needs no switch
  if (org === 'k' && PARTS.length === 1){   // a single-part work (an āratī, a stotra): list its sections straight away
    const P = PARTS[0], ts = TOPICS.slice(); if (!ts.length || ts[0].i > P.a) ts.unshift({i: P.a, end: ts.length ? ts[0].i - 1 : P.b});
    ts.forEach((t, n) => { const name = t.hi || t.en ? TNAME(t) : KNAME(P.k); h += '<li class="rowp">' + play('k', t.i, t.end) + '<button class="it" data-open="' + t.i + '"><span class="no">' + DEV(n + 1) + '</span><span class="grow"><span class="ti">' + esc(name) + '</span><br><span class="ds">' + esc(spanLabel(t.i, t.end)) + '</span></span><span class="chev">›</span></button></li>'; });
  }
  else if (org === 'k') PARTS.forEach(p => { const tps = TOPICS.filter(t => IT[t.i].p === p.k).length; h += '<li class="rowp">' + play('k', p.a, p.b) + '<button class="it" data-open="' + p.a + '"><span class="no">' + DEV(p.k + 1) + '</span><span class="grow"><span class="ti">' + esc(KNAME(p.k)) + '</span><br><span class="ds">' + DEV(tps) + T(' प्रसंग', ' sections') + '</span></span><span class="chev">›</span></button></li>'; });
  else { const P = PLAN[org]; const dn = Object.keys(DONE(ME(), org)).length; h += '<li class="small muted" style="padding:6px 2px;border:0">' + DEV(dn) + ' / ' + DEV(P.n) + T(' विश्राम पूर्ण · विश्रामके अन्तमें “विश्राम पूर्ण करें” दबाएँ', ' vishrams completed · tap “Mark vishram complete” at the end of each') + '</li>';
    // pages read before the first day and after the reading (pūrvāṅga / uttarāṅga), when the plan names them
    const page = (pg, when) => { const t = pg === 'aarti' ? T('श्रीरामायणजीकी आरती', 'Śrī Rāmāyaṇajī kī Āratī') : pg === 'visarjan' ? TT(W.vidhi.visarjan.title) : T('पारायण-विधि', 'Pārāyaṇa vidhi'); if (pg === 'visarjan') when = T('पारायणके अन्तिम दिन', 'On the last day of the pārāyaṇa'); return '<li class="rowp"><button class="it" data-page="' + pg + '"><span class="no pg"><svg><use href="#i-lamp"/></svg></span><span class="grow"><span class="ti">' + t + '</span><br><span class="ds">' + when + '</span></span><span class="chev">›</span></button></li>'; };
    (P.before || []).forEach(pg => h += page(pg, T('पाठसे पहले', 'Before the reading')));
    for (let n = 1; n <= P.n; n++){ const [a, b] = dayRange(org, n), d = DONE(ME(), org)[n]; h += '<li class="rowp">' + play(org, a, b) + '<button class="it" data-open="' + a + '"><span class="no' + (d ? ' done' : '') + '">' + (d ? '✓' : DEV(n)) + '</span><span class="grow"><span class="ti">' + VN(n) + '</span><br><span class="ds">' + rangeDesc(a, b) + '</span></span><span class="chev">›</span></button></li>'; }
    (P.after || []).forEach(pg => h += page(pg, T('पाठके बाद', 'After the reading'))); }
  $('#orgList').innerHTML = h;
  $$('#orgList [data-open]').forEach(b => b.onclick = () => openReader(org, +b.dataset.open));
  $$('#orgList [data-page]').forEach(b => b.onclick = () => { vidTab = b.dataset.page === 'vidhi' ? 'v' : b.dataset.page; show('vidhi'); });
  $$('#orgList [data-pa]').forEach(b => b.onclick = ev => { ev.stopPropagation(); playRange(b.dataset.po, +b.dataset.pa, +b.dataset.pb); });
}
$('#hLib').onclick = () => { libPath = []; show('library'); };   // “‹ Library” goes to the library itself, not the shelf last visited
$('#hMenu').onclick = mainMenu;

/* ---------------- search ---------------- */
let IDX = null;
const normD = s => (s || '').normalize('NFC').replace(/[ँं़‌‍ऽ]/g, '').replace(/\s+/g, ' ');
const normL = s => (s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/r̥/g, 'r');
const fzL = s => ' ' + normL(s).replace(/[^a-z\s]/g, ' ').replace(/(aa|ee|ii|oo|uu)/g, m => ({aa: 'a', ee: 'i', ii: 'i', oo: 'u', uu: 'u'})[m]).replace(/sh/g, 's').replace(/ch/g, 'c').replace(/w/g, 'v').replace(/ri/g, 'r').replace(/m(?=[bcdfghjklnpqrstvwxyz])/g, 'n').replace(/\s+/g, ' ').split(' ').map(w => w.length > 2 ? w.replace(/a$/, '') : w).join(' ').trim() + ' ';
function buildIdx(){ IDX = IT.map((it, i) => { const h = SRC.hi && SRC.hi.m[it.id], e = SRC.en && SRC.en.m[it.id]; return {v: normD(it.v.join(' ')), h: normD(h ? h[0] : ''), t: fzL((it.t || []).join(' ')), e: normL(e ? e[0] : '')}; }); IDX.w = W.id + (SRC.hi || {}).id + (SRC.en || {}).id; }
const scopes = new Set(['v', 'h', 'e', 'n']);
$$('#scope .chip').forEach(c => c.onclick = () => { const s = c.dataset.s; if (scopes.has(s)) scopes.delete(s); else scopes.add(s); c.classList.toggle('on'); runSearch(); });
let sT; $('#q').addEventListener('input', () => { clearTimeout(sT); sT = setTimeout(runSearch, 250); });
function snip(text, q, latin){ const src = text; const low = latin ? normL(src) : normD(src); const nq = latin ? normL(q) : normD(q); let p = low.indexOf(nq); if (p < 0) return esc(src.slice(0, 160)) + (src.length > 160 ? '…' : ''); let a = Math.max(0, p - 60), b = Math.min(src.length, p + nq.length + 80); if (a > 0){ const sp = src.indexOf(' ', a); if (sp > -1 && sp < p) a = sp + 1; } const s = src.slice(a, b); const pp = (latin ? normL(s) : normD(s)).indexOf(nq); let out; if (pp >= 0 && (latin ? normL(s) : normD(s)).length === s.length) out = esc(s.slice(0, pp)) + '<mark>' + esc(s.slice(pp, pp + nq.length)) + '</mark>' + esc(s.slice(pp + nq.length)); else out = esc(s); return (a > 0 ? '…' : '') + out + (b < src.length ? '…' : ''); }
function runSearch(){
  if (SCOPE === 'lib'){ const q = $('#q').value; if (q.trim()) libSearch(q); else openSearch('lib', true); return; }
  const q = $('#q').value.trim(), box = $('#sRes');
  if (q.length < 2){ box.innerHTML = '<div class="empty">' + T('कम-से-कम दो अक्षर लिखें।', 'Type at least two letters.') + '</div>'; return; }
  if (!IDX || IDX.w !== W.id + (SRC.hi || {}).id + (SRC.en || {}).id) buildIdx();
  const latin = /[a-zA-Z]/.test(q), nq = latin ? normL(q) : normD(q);
  const fqs = latin ? [...new Set([q, q.replace(/([aeiouāīū])n\b/gi, '$1'), q.replace(/([aeiouāīū])[nm](?=[bcdfghjklpqrstvz])/gi, '$1'), q.replace(/([aeiouāīū])n\b/gi, '$1').replace(/([aeiouāīū])[nm](?=[bcdfghjklpqrstvz])/gi, '$1')].map(x => fzL(x).trim()).filter(Boolean))] : [];
  const res = [];
  for (let i = 0; i < IT.length && res.length < 300; i++){
    const x = IDX[i];
    if (!latin && scopes.has('v') && x.v.includes(nq)) res.push([i, LB.verses(), IT[i].v.join(' । '), false]);
    else if (!latin && scopes.has('h') && x.h.includes(nq)) res.push([i, LB.h(), SRC.hi.m[IT[i].id][0], false]);
    else if (latin && scopes.has('v') && fqs.some(f => x.t.includes(' ' + f))) res.push([i, LB.tr(), IT[i].t.join(' '), true]);
    else if (latin && scopes.has('e') && x.e.includes(nq)) res.push([i, LB.e(), SRC.en.m[IT[i].id][0], true]);
  }
  if (scopes.has('n')) for (const p of SHOWN()) for (const k in p.notes){ if (!k.startsWith(W.id + ':')) continue; const i = ID[k.slice(W.id.length + 1)]; if (i == null) continue; p.notes[k].forEach(n => { if ((latin ? normL(n.t) : normD(n.t)).includes(nq)) res.push([i, T('टिप्पणी', 'Note'), n.t, latin]); }); }
  box.innerHTML = res.length ? '<p class="small muted">' + DEV(res.length) + (res.length >= 300 ? '+' : '') + T(' परिणाम', ' results') + '</p>' + res.map(r => '<button class="res" data-i="' + r[0] + '"><div class="where">' + esc(itemLabel(r[0])) + ' · ' + esc(r[1]) + '</div><div class="snip' + (r[3] ? ' lat' : '') + '">' + snip(r[2], q, r[3]) + '</div></button>').join('') : '<div class="empty">' + T('कुछ नहीं मिला। दूसरा रूप लिखकर देखें।', 'Nothing found. Try another spelling.') + '</div>';
  $$('#sRes .res').forEach(b => b.onclick = () => openReader('k', +b.dataset.i, true));
}

/* ---------------- bookmarks ---------------- */
function renderBookmarks(){
  const bms = [], notes = [], pre = W.id + ':';
  for (const p of SHOWN()){ for (const k in p.bm) if (k.startsWith(pre) && ID[k.slice(pre.length)] != null) bms.push([ID[k.slice(pre.length)], p]); for (const k in p.notes) if (k.startsWith(pre) && ID[k.slice(pre.length)] != null) p.notes[k].forEach(n => notes.push([ID[k.slice(pre.length)], p, n])); }
  bms.sort((a, b) => a[0] - b[0]); notes.sort((a, b) => a[0] - b[0]);
  // each list folds under its heading (owner, 2026-10-22): open by default, and a fold is remembered
  const fold = S.settings.bmFold || {}, sec = (key, title, body) => '<details class="bmsec" data-fold="' + key + '"' + (fold[key] ? '' : ' open') + '><summary><h2>' + title + '</h2></summary>' + body + '</details>';
  let h = '', bmh = '';
  // each bookmark has its own ✕ to remove it (owner, 2026-10-20)
  bmh += bms.length ? bms.map(b => '<div class="bmrow"><button class="res" data-i="' + b[0] + '"><div class="where">' + esc(itemLabel(b[0])) + '</div><div class="snip" style="font-weight:700">' + esc(IT[b[0]].v[0]) + '</div></button><button class="bmdel" data-del="' + b[0] + '" aria-label="' + T('बुकमार्क हटाएँ', 'Remove bookmark') + '"><svg><use href="#i-x"/></svg></button></div>').join('') : '<p class="muted">' + T('किसी भी पदके पास बुकमार्क चिह्न दबाएँ।', 'Tap the bookmark sign beside any verse.') + '</p>';
  h += sec('bm', T('बुकमार्क (', 'Bookmarks (') + DEV(bms.length) + ')', bmh);
  h += sec('notes', T('टिप्पणियाँ (', 'Notes (') + DEV(notes.length) + ')', notes.length ? notes.map(n => '<button class="res" data-i="' + n[0] + '"><div class="where">' + esc(itemLabel(n[0])) + '</div><div class="snip">' + esc(n[2].t.slice(0, 200)) + '</div></button>').join('') : '<p class="muted">' + T('किसी पदके ⋮ मेनूसे अपनी टिप्पणी लिखें।', 'Use the ⋮ menu of any verse to write a note.') + '</p>');
  h += '<h2 style="font-size:19px;margin:26px 0 4px">' + T('मेरी फ़ाइल', 'My file') + '</h2><p class="small muted">' + T('आपके बुकमार्क, टिप्पणियाँ, प्रगति और सुधार इसी फ़ोनमें रहते हैं। फ़ाइल सेव करके बैकअप रखें या दूसरे फ़ोनपर खोलें।', 'Your bookmarks, notes, progress and corrections stay on this phone. Save the file as a backup, or open it on another phone.') + (canStore ? '' : ' <b>' + T('ध्यान दें: यह फ़ोन डेटा अपने-आप नहीं रख पा रहा — पाठके बाद “फ़ाइल सेव करें” दबाएँ।', 'This phone is not keeping app data — tap Save my file after each reading.') + '</b>') + '</p>' +
    '<div class="acts"><button class="btn" id="exp">' + T('फ़ाइल सेव करें', 'Save my file') + '</button><button class="btn ghost" id="imp">' + T('फ़ाइल खोलें', 'Open a file') + '</button></div>';
  $('#bmBody').innerHTML = h + '<div style="height:40px"></div>';
  $('#exp').onclick = exportFile; $('#imp').onclick = () => $('#fileIn').click();
  $$('#bmBody .bmsec').forEach(d => d.ontoggle = () => { S.settings.bmFold = S.settings.bmFold || {}; if (d.open) delete S.settings.bmFold[d.dataset.fold]; else S.settings.bmFold[d.dataset.fold] = 1; save(); });
  $$('#bmBody .res').forEach(b => b.onclick = () => openReader('k', +b.dataset.i, true));
  $$('#bmBody [data-del]').forEach(b => b.onclick = () => { const k = KEY(IT[+b.dataset.del].id); for (const p of S.profiles) delete p.bm[k]; save(); renderBookmarks(); toast(T('बुकमार्क हटाया', 'Bookmark removed')); });
}

/* ---------------- settings ---------------- */
function renderSettings(){   // the "More" page (owner, 2026-10-22): the rare things only — sources, audio timing, my file, privacy
  const cur = S.src[W ? W.id : ''] || {};
  const pick = (kind, label, off) => { const list = W ? srcList(kind) : []; if (!list.length) return ''; const sel = cur[kind] || list[0].id; return '<div class="field"><label>' + label + '</label><select data-src="' + kind + '">' + list.map(s => '<option value="' + s.id + '"' + (sel === s.id ? ' selected' : '') + '>' + esc(TT(s.title)) + (s.draft ? T(' (जाँच बाकी)', ' (to be checked)') : '') + '</option>').join('') + (off ? '<option value="off"' + (sel === 'off' ? ' selected' : '') + '>' + T('बंद', 'Off') + '</option>' : '') + '</select></div>'; };
  let h = '<h2>' + T('पढ़ना', 'Reading') + '</h2>' + sw('str', LB.tr(), LB.trSub(), S.settings.tr) +
    (W ? '<h2>' + LB.src() + ' · ' + esc(TT(W.title)) + '</h2>' + pick('hi', LB.h()) + pick('en', LB.e()) + pick('au', LB.au(), true) : '') +
    timingHTML() +
    '<h2>' + T('सहायता', 'Help') + '</h2><div class="acts"><a class="btn ghost" href="privacy.html" target="_blank" rel="noopener">' + T('गोपनीयता', 'Privacy') + '</a></div>' +
    '<div style="height:50px"></div>';
  $('#setBody').innerHTML = h;
  $('#str').onchange = e => { S.settings.tr = e.target.checked; save(); };   // seen in the reader on the next open
  bindTiming();
  $$('[data-src]').forEach(s => s.onchange = async () => { const c = S.src[W.id] = S.src[W.id] || {}; c[s.dataset.src] = s.value; save(); if (s.dataset.src === 'au') stopAudio(); await loadSources(); IDX = null; toast(T('स्रोत बदला', 'Source changed')); });
}
/* timing review: Settings › Audio timing. While it is on, a ⏱ row appears in the player and each verse's ⋮ menu shows its start;
   recordings still being checked (drafts) can be played. Starts set by ear go to the library through a GitHub issue, which
   the workflow .github/workflows/timing.yml applies (tools/audio/apply_owner_timing.py). */
function pendingStarts(){ if (!SRC.au) return {}; const fx = myStarts(), sent = S.timing.sent[tkey()] || {}, out = {}; for (const id in fx) if (ID[id] != null && !fromOf(id) && JSON.stringify(sent[id]) !== JSON.stringify(fx[id])) out[id] = fx[id]; return out; }
function timingHTML(){
  if (!W) return '';
  let h = '<h2>' + T('ऑडियोका समय', 'Audio timing') + '</h2><p class="small muted">' + T('जहाँ पद और आवाज़ मेल न खाएँ, वहाँ ठीक करनेके लिये।', 'For fixing places where the lit verse and the voice do not match.') + '</p>' + sw('stm', T('ऑडियोका समय', 'Audio timing'), '', S.timing.on);
  if (S.timing.on && SRC.au){
    const n = Object.keys(myStarts()).filter(id => ID[id] != null).length, p = Object.keys(pendingStarts()).length;
    h += (SRC.au.meta.draft ? sw('stp', T('यह रिकॉर्डिंग जाँच ली — सबके लिये चालू करें', 'This recording is checked: publish it for everyone'), T('भेजनेके साथ जाएगा', 'Goes with the next send'), !!(S.timing.publish || {})[tkey()]) : '') +
      checkList() + helperList() +
      '<p class="small" style="margin:14px 0 8px">' + esc(TT(SRC.au.meta.title)) + ': ' + DEV(n) + T(' पद आपने ठीक किये', ' verses set by you') + (p ? ' · ' + DEV(p) + T(' भेजने बाकी', ' not sent yet') : '') + '</p>' +
      '<div class="acts"><button class="btn" id="tSend"' + (p || (S.timing.publish || {})[tkey()] ? '' : ' disabled') + '>' + T('लाइब्रेरीमें भेजें (GitHub)', 'Send to the library (GitHub)') + '</button><button class="btn ghost" id="tSave"' + (n ? '' : ' disabled') + '>' + T('फ़ाइलमें सेव करें', 'Save timings as a file') + '</button><button class="btn ghost" id="tOpen">' + T('फ़ाइल खोलें', 'Open a file') + '</button>' + (n ? '<button class="btn ghost" id="tClear">' + T('मेरे बदलाव हटाएँ', 'Clear adjustments') + '</button>' : '') + '</div>' +
      '<p class="small muted">' + T('सहायता कर रहे हैं? “फ़ाइलमें सेव करें” दबाकर फ़ाइल साइटके मालिकको भेजें; वे जाँचकर लाइब्रेरीमें जोड़ेंगे। लाइब्रेरीमें सीधे केवल मालिक भेज सकते हैं।', 'Helping? Tap “Save timings as a file” and send the file to the site’s owner, who checks it and adds it to the library. Only the owner can send to the library directly.') + '</p>';
  }
  return h;
}
function checkList(){
  const ids = [...SRC.au.checkSet].filter(id => ID[id] != null && !myStarts()[id]).sort((a, b) => ID[a] - ID[b]); if (!ids.length) return '<p class="small muted">' + T('जाँचने लायक कोई पद नहीं बचा।', 'Nothing left to check.') + '</p>';
  return '<details class="tcheck"><summary>' + T('जाँचने हैं: ', 'To check: ') + DEV(ids.length) + T(' पद — इनकी शुरुआत अनुमानसे रखी गयी है', ' verses — their starts are estimated') + '</summary><div class="tlist">' + ids.slice(0, 400).map(id => '<button data-go-i="' + ID[id] + '">' + esc(itemLabel(ID[id])) + ' <span class="muted">' + fmtT(SRC.au.at[id][1]) + '</span></button>').join('') + '</div></details>';
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
function sendStarts(){
  const pend = pendingStarts(), ids = Object.keys(pend).sort((a, b) => ID[a] - ID[b]), part = ids.slice(0, 150), starts = {};
  part.forEach(id => { const [t, sec, end] = pend[id], yt = SRC.au.tracks[t].yt; (starts[yt] = starts[yt] || {})[id] = end != null ? [sec, end] : sec; });
  const pub = !!(S.timing.publish || {})[tkey()], doc = {path: W.path, source: SRC.au.meta.id, starts}; if (pub) doc.publish = true;
  const title = 'Timing: ' + W.path + ' / ' + SRC.au.meta.id;
  const body = T('ऐपसे भेजे गये ऑडियो-समय (कानसे जाँचे हुए)। इसे वैसे ही सबमिट करें; वर्कफ़्लो इन्हें लाइब्रेरीमें जोड़ देगा।', 'Audio starts set by ear in the app. Submit as it is; a workflow adds them to the library.') + '\n\n```json\n' + JSON.stringify(doc) + '\n```\n';
  const url = 'https://github.com/goyaldarwin/scriptures/issues/new?title=' + encodeURIComponent(title) + '&body=' + encodeURIComponent(body);
  window.open(url, '_blank', 'noopener');
  const sent = S.timing.sent[tkey()] = S.timing.sent[tkey()] || {}; part.forEach(id => sent[id] = pend[id]); if (pub) delete S.timing.publish[tkey()]; save();
  toast(ids.length > part.length ? T('पहले १५० भेजे — बाकी अगली बार', 'First 150 sent — send again for the rest') : T('GitHub पर “Submit” दबाएँ', 'Tap “Submit” on GitHub'));
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
  openSheet('<h2>' + T('फ़ाइल खोलें', 'Open a file') + '</h2><p>' + T('इस फ़ाइलमें: ', 'This file has: ') + '<b>' + DEV(Object.values(X.profiles[0].bm).length) + T(' बुकमार्क · ', ' bookmarks · ') + DEV(Object.values(X.profiles[0].notes).reduce((a, b) => a + b.length, 0)) + T(' टिप्पणी', ' notes') + '</b></p><div class="menu"><button id="imAdd">' + T('इन्हें इस फ़ोनमें जोड़ें', 'Add them to this phone') + '<br><small class="muted">' + T('यहाँकी आपकी चीज़ें भी रहेंगी', 'Your existing data stays') + '</small></button><button id="imRep">' + T('इस फ़ोनका सब कुछ इस फ़ाइलसे बदलें', 'Replace everything on this phone') + '<br><small class="muted">' + T('सेटिंग्स और प्रगति भी फ़ाइल जैसी हो जाएँगी', 'Settings and progress also come from the file') + '</small></button></div>');
  $('#imAdd').onclick = () => { X.profiles.forEach(p => mergeInto(ME(), p)); save(); closeSheet(); toast(T('फ़ाइल जोड़ी गई', 'File added')); renderSettings(); };
  $('#imRep').onclick = () => askYes(T('इस फ़ोनका वर्तमान डेटा फ़ाइलके डेटासे बदल जाएगा।', 'Data on this phone will be replaced by the file.'), T('हाँ, बदलें', 'Yes, replace'), () => { const on = !!S.timing.on; S = Object.assign(defaults(), X); delete S.kind; delete S.exported; if (S.timing) S.timing.on = on; save(); applyTheme(); closeSheet(); toast(T('फ़ाइल खोली गई', 'File opened')); renderSettings(); });
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
  if (vidTab === 'aarti') h = '<div class="h' + L + '">' + T('श्रीरामायणजीकी आरती', 'Śrī Rāmāyaṇajī kī Āratī') + '</div>' + V.aarti.map(l => '<div class="v">' + vW(l) + '</div>').join('');
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

/* ---------------- first-run tour: done, not read (owner, 2026-10-19) ----------------
   A welcome card, then the reader is taken into the Sundarakāṇḍa and asked to do each thing for real — open the text, tap a
   word, close its drawer, switch a meaning on, play one verse — with that spot lit and the rest dimmed; each step moves on
   when it has been done. Shown once; ☰ › “Take the tour” shows it again (owner, 2026-10-20). closeTour() ends it at any point. */
let TOUR = null;   // {k: step, t0, base}
function tourWork(){ const leafs = []; (function walk(n){ (n || []).forEach(c => c.work ? leafs.push(c.work) : walk(c.children)); })(LIB); return leafs.includes('sundarkand') ? 'sundarkand' : leafs[0]; }
function inView(el){ const r = el.getBoundingClientRect(); return r.width && r.top > 70 && r.bottom < innerHeight - 90; }
function firstVisible(sel){ const all = $$(sel); return all.find(inView) || all[0] || null; }
function tourSteps(){
  return [
    {t: () => { const rows = $$('#orgList [data-open]'), k = PARTS.findIndex(p => /^Sundara/.test(p.en || '')); return (W && W.id === 'sundarkand' && k >= 0 && rows[k]) || rows[0]; }, allow: '#orgList .it', p: T('पढ़ना शुरू करनेके लिये यहाँ छुएँ।', 'Tap here to start reading.'), done: () => CURVIEW === 'reader' && !!$('#rBody .verse')},
    {t: () => firstVisible('#rBody .verse .vtext .w'), allow: '#rBody .vtext .w', p: T('किसी भी शब्दको छुएँ — उसका अर्थ दिखेगा।', 'Tap any word to see its meaning.'), done: () => $('#sheet').classList.contains('on')},
    {t: () => $('#sheet'), allow: '#sheet', p: T('इस पट्टीको नीचे खींचकर बंद करें।', 'Drag the drawer down to close it.'), done: () => !$('#sheet').classList.contains('on'), top: true},
    {t: () => $('#reader .szp'), allow: '#reader .szp', p: T('A+ छूकर अक्षर बड़े करें।', 'Tap A+ to make the letters larger.'), enter: () => { TOUR.base = S.settings.size; }, done: () => S.settings.size > TOUR.base || (TOUR.tap && TOUR.base >= 34)},   // already at the largest: the tap is enough (owner, 2026-10-20)
    // A− is a step of its own: after A+, people reach for it (owner, 2026-10-20)
    {t: () => $('#reader .szm'), allow: '#reader .szm', p: T('A− छूकर अक्षर छोटे करें।', 'Tap A− to make the letters smaller.'), enter: () => { TOUR.base = S.settings.size; }, done: () => S.settings.size < TOUR.base || (TOUR.tap && TOUR.base <= 16)},   // already at the smallest: the tap is enough
    {t: () => $('#rLayers [data-l="' + (S.settings.layers.h ? 'e' : 'h') + '"]'), allow: '#rLayers [data-l="h"], #rLayers [data-l="e"], #rLayers [data-l="w"]', p: () => S.settings.layers.h ? T('“En” छूकर हर पदके नीचे अंग्रेज़ी अर्थ दिखाएँ या छिपाएँ। “शब्द” से शब्दार्थ।', 'Tap “En” to show or hide the English meaning under every verse. “शब्द” gives word-by-word meanings.') : T('“हिं” छूकर हर पदके नीचे हिंदी अर्थ दिखाएँ। “En” अंग्रेज़ी, “शब्द” शब्दार्थ।', 'Tap “हिं” to show the Hindi meaning under every verse. “En” is English, “शब्द” word by word.'),
     enter: () => { TOUR.base = JSON.stringify(S.settings.layers); }, done: () => JSON.stringify(S.settings.layers) !== TOUR.base},
    {t: () => $('#rLayers [data-l="r"]'), allow: '#rLayers [data-l="r"]', p: T('पुस्तक छूकर पाठ मोड चालू करें — केवल मूल पाठ, बड़े अक्षरोंमें। फिर छूनेपर अर्थ लौट आते हैं।', 'Tap the book for recitation mode — the verses alone, in larger type. Tap it again to bring the meanings back.'), done: () => !!S.settings.recite},
    {t: () => firstVisible('#rBody .vbm'), allow: '#rBody .vbm', p: T('बुकमार्क चिह्न छूकर यह पद सहेजें — ☰ › बुकमार्कमें मिलेगा।', 'Tap the bookmark sign to save this verse — find it in ☰ › Bookmarks.'),
     enter: () => { TOUR.bmAdded = false; }, done: () => !!TOUR.bmAdded},   // any bookmark made in this step — even one taken off and put back (owner, 2026-10-20)
    {t: () => firstVisible('#rBody .vplay'), allow: '#rBody .vplay', p: T('▶ छूकर केवल यह पद सुनें — जो गाया जा रहा है वह चमकेगा।', 'Tap ▶ to play just this verse — it lights up as it is sung.'), done: () => PL.on},
  ];
}
// while the tour runs, only what the current step asks for can be tapped (a ▶ on the work's page would start the audio
// and lose the tour — owner, 2026-10-19); the tour's own bubble always works
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
// ‹ Back: the step before (owner, 2026-10-20). A step whose action is already in effect (the drawer already closed, recitation
// mode already on) would move on at once, so Back goes to the step before that one; the first step needs the work's page.
function tourBack(){
  if (!TOUR || TOUR.k <= 0) return; const st = tourSteps(); let k = TOUR.k - 1;
  if (!$('#sheet').classList.contains('on') && k === 2) k = 1;   // "close the drawer" needs an open drawer: back to "tap a word"
  if (k === 1 && $('#sheet').classList.contains('on')) closeSheet();   // "tap a word" needs a closed drawer, or it would count as done at once (owner, 2026-10-20)
  if (k === 6 && S.settings.recite) toggleRecite();             // back to recitation mode: turn it off so it can be tried again
  if (k === 0 && CURVIEW !== 'home') show('home');
  TOUR.k = -1; $('#cspot').style.opacity = 0; setTimeout(() => tourStep(k), 250);
}
// After ▶ the tour lets the verse play for 5 seconds, then takes the reader to the library with a parting message
// (owner, 2026-10-20). Closing the player sooner ends it the same way.
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
  // one app per tradition (owner, 2026-10-19): ?app=<id> shows only the shelves library/apps.json lists for that app
  // (the Hindu app also carries the Sukhmani Sahib). The address keeps it while you move around; changing the list
  // needs no app update. Without ?app the website shows the whole library.
  const appId = new URLSearchParams(location.search).get('app');
  if (appId){ try { const A = (await getJSON('apps'))[appId]; if (A) LIB = pruneLib(LIB, A.shelves); } catch (e) {} }
  const leafs = []; (function walk(n){ (n || []).forEach(c => c.work ? leafs.push(c.work) : walk(c.children)); })(LIB);
  // a link may name a work (?w=<work id>): the app's shortcuts and store pages open straight to it
  const asked = new URLSearchParams(location.search).get('w');
  const start = asked && leafs.includes(asked) ? asked : S.work && leafs.includes(S.work) ? S.work : (leafs.length === 1 ? leafs[0] : null);
  const nav = (performance.getEntriesByType && performance.getEntriesByType('navigation')[0]) || {};
  const was = !asked && (nav.type === 'reload' || nav.type === 'back_forward') && history.state && history.state.v ? history.state : null;
  if (was){ await restore(was); if (!W) await hideSalute(); }   // a refresh: the same page, with the same way back
  else if (start){ await openWork(start, true); history.replaceState(snap('library'), ''); show('home'); }
  else { history.replaceState(snap('library'), ''); renderLibrary(); await hideSalute(); }
  cloudInit();
  if (!S.settings.tour) startTour();
  // offline reading (owner, 2026-10-21): the service worker keeps the app and every library file it has fetched (sw.js, build.py)
  if ('serviceWorker' in navigator && (location.protocol === 'https:' || window.__SW_TEST) && !BUNDLE) navigator.serviceWorker.register('sw.js').catch(() => {});
})();
