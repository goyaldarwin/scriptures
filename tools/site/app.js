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
let LIB = [], LANGS = {}, GL = {}, WG = {}, W = null, IT = [], ID = {}, SRC = {hi: null, en: null, au: null};

/* ---------------- personal store ---------------- */
const LS = 'manas.personal.v1';
let canStore = true;
function newProfile(name){ return {id: 'p' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), name, notes: {}, bm: {}, done: {}, gloss: {}, fix: {}}; }
function defaults(){ const p = newProfile('मेरा'); return {v: 2, settings: {layers: {h: true, e: false, w: false}, tr: false, size: 21, theme: 'light', wake: true, lightDefault: 1}, src: {}, w: {}, work: null, profiles: [p], active: p.id, show: [p.id], timer: null}; }
let S;
try { S = JSON.parse(localStorage.getItem(LS)); } catch (e) { canStore = false; }
if (!S || !S.profiles) S = defaults();
function migrate(){
  if ((S.v || 1) < 2) migrate2();
  if (S.v < 3){ // v2 → v3: a reader's own word meanings are filed by language (“awa:राम”); earlier ones were all Awadhi
    S.profiles.forEach(p => { const n = {}; for (const k in p.gloss || {}) n[k.includes(':') ? k : 'awa:' + k] = p.gloss[k]; p.gloss = n; });
    S.v = 3;
  }
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
function save(){ S.ts = Date.now(); if (canStore){ try { localStorage.setItem(LS, JSON.stringify(S)); } catch (e) { canStore = false; } } if (CLOUD){ clearTimeout(cloudT); cloudT = setTimeout(cloudPush, 1500); } }
async function cloudPush(){ if (!CLOUD) return; if (cloudBusy){ cloudAgain = true; return; } cloudBusy = true; try { await CLOUD.set({s: JSON.stringify(S), ts: S.ts || Date.now()}); } catch (e) { if (e && e.code === 'unavailable') setTimeout(cloudPush, 3000 + Math.random() * 2000); } cloudBusy = false; if (cloudAgain){ cloudAgain = false; cloudPush(); } }
async function cloudInit(){
  try {
    if (!window.claude || !window.claude.use) return;
    const [db, user] = await Promise.all([window.claude.use('db'), window.claude.use('user')]);
    if (!db || !user) return; const uid = await user.id(); if (!uid) return;
    const ref = db.doc('data/users/' + uid + '/state'); const snap = await ref.get(); CLOUD = ref;
    if (snap.exists){ const d = snap.data(); if (d && d.s && (d.ts || 0) > (S.ts || 0)){ const X = JSON.parse(d.s); if (X && X.profiles){ S = Object.assign(defaults(), X); migrate(); try { localStorage.setItem(LS, JSON.stringify(S)); } catch (e) {} applyTheme(); applyLang(); onView(viewStack[viewStack.length - 1]); } } else if ((S.ts || 0) > (d.ts || 0)) cloudPush(); }
    else if (S.ts) cloudPush();
    canStore = true;
  } catch (e) {}
}
const LANG = () => S.settings.layers.e ? 'en' : 'hi';
function T(hi, en){ return LANG() === 'en' ? en : hi; }
const ME = () => S.profiles.find(p => p.id === S.active) || S.profiles[0];
const SHOWN = () => S.profiles.filter(p => S.show.includes(p.id));
const WS = () => (S.w[W.id] = S.w[W.id] || {pos: {}, last: null, org: 'k'});
const KEY = id => W.id + ':' + id;
const DONE = (p, plan) => ((p.done[W.id] = p.done[W.id] || {})[plan] = p.done[W.id][plan] || {});

/* ---------------- shared labels ---------------- */
const LB = {
  h: () => T('हिंदी अर्थ', 'Hindi meaning'), e: () => T('अंग्रेज़ी अर्थ', 'English meaning'), w: () => T('शब्दार्थ', 'Word meanings'), au: () => T('ऑडियो', 'Audio'),
  tr: () => T('रोमन लिप्यन्तरण', 'Transliteration'), trSub: () => T('मूल पाठके नीचे रोमन अक्षरोंमें', 'The verse in Roman letters, under the text'),
  rc: () => T('पाठ मोड', 'Recitation mode'), rcSub: () => T('केवल मूल पाठ, बड़े अक्षर', 'Verses only, larger text'),
  size: () => T('अक्षरका आकार', 'Text size'), wake: () => T('पढ़ते समय स्क्रीन जलती रहे', 'Keep screen on while reading'), theme: () => T('रंग', 'Theme'),
  timer: () => T('पाठ-टाइमर', 'Reading timer'), sections: () => T('प्रसंग', 'Sections'), search: () => T('खोजें', 'Search'),
  bm: () => T('बुकमार्क और टिप्पणियाँ', 'Bookmarks & notes'), set: () => T('सेटिंग्स', 'Settings'), verses: () => T('मूल पाठ', 'Verses'),
  lib: () => T('पुस्तकालय', 'Library'), src: () => T('स्रोत', 'Sources'), vidhi: () => T('पारायण-विधि', 'Pārāyaṇa vidhi')
};

/* ---------------- ui helpers ---------------- */
let toastT;
function toast(msg){ const t = $('#toast'); t.textContent = msg; t.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove('on'), 2600); }
function applyLang(){ const en = LANG() === 'en'; document.documentElement.lang = en ? 'en' : 'hi';
  $$('[data-en]').forEach(el => { if (el.dataset.hi == null) el.dataset.hi = el.innerHTML; el.innerHTML = en ? el.dataset.en : el.dataset.hi; });
  $$('[data-en-ph]').forEach(el => { if (el.dataset.hiPh == null) el.dataset.hiPh = el.placeholder; el.placeholder = en ? el.dataset.enPh : el.dataset.hiPh; }); }
function applyTheme(){ const r = document.documentElement; if (S.settings.theme === 'auto') r.removeAttribute('data-theme'); else r.setAttribute('data-theme', S.settings.theme); r.style.setProperty('--verse-size', S.settings.size + 'px'); r.style.setProperty('--mean-size', Math.round(S.settings.size * 0.78 * 10) / 10 + 'px'); }
const viewStack = ['library'];
function show(id, push = true){ $$('.view').forEach(v => v.classList.toggle('on', v.id === id)); if (push){ viewStack.push(id); history.pushState({v: id}, ''); } if (id !== 'reader') window.scrollTo(0, 0); onView(id); }
function back(){ history.back(); }
window.addEventListener('popstate', () => { closeSheet(); if (viewStack.length > 1) viewStack.pop(); const id = viewStack[viewStack.length - 1] || 'library'; show(id, false); if (id === 'reader') reopenReader(); });
function onView(id){ if (id === 'library') renderLibrary(); if (id === 'home') renderHome(); if (id === 'bookmarks') renderBookmarks(); if (id === 'settings') renderSettings(); if (id === 'vidhi') renderVidhi(); wake(id === 'reader'); if (id === 'search') setTimeout(() => $('#q').focus(), 50); }
$$('[data-back]').forEach(b => b.onclick = back);
$$('[data-go]').forEach(b => b.onclick = () => show(b.dataset.go));
function openSheet(html){ $('#sheetBody').innerHTML = html; $('#sheet').classList.add('on'); $('#scrim').classList.add('on'); $('#sheet').scrollTop = 0; }
function closeSheet(){ $('#sheet').classList.remove('on'); $('#scrim').classList.remove('on'); $$('.w.sel').forEach(w => w.classList.remove('sel')); }
$('#scrim').onclick = () => closeSheet();
function sw(id, label, sub, on){ return '<label class="sw"><span>' + label + (sub ? '<small>' + sub + '</small>' : '') + '</span><span class="tg"><input type="checkbox" id="' + id + '"' + (on ? ' checked' : '') + '><span></span></span></label>'; }

/* ---------------- wake lock & timer ---------------- */
let wl = null;
async function wake(on){ try { if (on && S.settings.wake && 'wakeLock' in navigator){ if (!wl){ wl = await navigator.wakeLock.request('screen'); wl.addEventListener('release', () => wl = null); } } else if (wl && !PL.on){ await wl.release(); wl = null; } } catch (e) {} }
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible' && ($('#reader').classList.contains('on') || PL.on)) wake(true); });
function timerText(){ const t = S.timer; if (!t) return ''; const sec = Math.floor(((t.run ? Date.now() - t.start : 0) + t.acc) / 1000); const h = Math.floor(sec / 3600), m = Math.floor(sec % 3600 / 60), s = sec % 60; return (h ? h + ':' + String(m).padStart(2, '0') : m) + ':' + String(s).padStart(2, '0'); }
function tickTimer(){ const p = $('#timerPill'); if (S.timer){ p.classList.add('on'); p.textContent = (S.timer.run ? '' : '❚❚ ') + timerText(); } else p.classList.remove('on'); }
function timerToggle(){ if (!S.timer) S.timer = {start: Date.now(), acc: 0, run: true}; else if (S.timer.run){ S.timer.acc += Date.now() - S.timer.start; S.timer.run = false; } else { S.timer.start = Date.now(); S.timer.run = true; } save(); tickTimer(); }
function timerReset(){ S.timer = null; save(); tickTimer(); }
setInterval(tickTimer, 1000);
$('#timerPill').onclick = timerToggle;

/* ---------------- word meanings: one dictionary per language (library/glossary/<lang>.json) ----------------
   A word is looked up in the language of the verse it is in, then in that language's fallbacks
   (languages.json). A work may refine a sense in <work>/glossary.json; a reader's own meaning wins. */
const PUNCT = /[।॥|,.;:!?\-—‘’“”'"()\[\]०-९0-9]/g;
function cleanWord(w){ return w.replace(PUNCT, '').normalize('NFC'); }
function langOf(i){ return (i != null && IT[i] && IT[i].l) || W.lang; }
function langChain(lang){ return [lang].concat((LANGS[lang] || {}).fallback || []); }
async function loadGlossaries(){
  if (!Object.keys(LANGS).length) LANGS = await getJSON('glossary/languages');
  const need = new Set(); [W.lang].concat(IT.map(x => x.l).filter(Boolean)).forEach(l => langChain(l).forEach(c => need.add(c)));
  await Promise.all([...need].filter(c => !GL[c]).map(async c => { try { GL[c] = await getJSON('glossary/' + c); } catch (e) { GL[c] = {}; } }));
  try { WG = await getJSON(W.path + '/glossary'); } catch (e) { WG = {}; }
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
  const halves = line.split(/(?<=।)\s+(?=[^\s।०-९(])/);
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
function srcChoice(kind){ const list = (W.sources || {})[kind] || []; const sel = ((S.src[W.id] || {})[kind]); if (sel === 'off') return null; return (list.find(s => s.id === sel) || list[0] || null); }
async function loadSources(){
  for (const kind of ['hi', 'en', 'au']){ const c = srcChoice(kind); SRC[kind] = null; if (c){ try { SRC[kind] = Object.assign({meta: c}, await getJSON(W.path + '/' + c.file)); } catch (e) {} } }
  buildAudio();
}
function verseOf(i){ const id = IT[i].id; for (const p of S.profiles){ const f = p.fix[KEY(id)]; if (f && f.v) return {v: f.v, edited: true}; } return {v: IT[i].v, edited: false}; }
function mean(kind, i){
  const src = SRC[kind]; if (!src) return null; const id = IT[i].id; const k = KEY(src.id + ':' + id);
  for (const p of S.profiles){ const f = p.fix[k]; if (f && f.m != null) return {x: f.m, edited: true, f: (src.m[id] || [])[1]}; }
  const e = src.m[id]; return e ? {x: e[0], f: e[1], edited: false} : null;
}
const layerOn = l => !!S.settings.layers[l];

/* ---------------- reader: continuous scroll over a kāṇḍa or a day's pāṭh ---------------- */
let R = {org: 'k', a: 0, b: 0, n: 0, pf: -1, pt: -1};
const VSHORT = {cau: ['चौ॰', 'Cau.'], do: ['दो॰', 'Do.'], so: ['सो॰', 'So.'], cha: ['छं॰', 'Cha.'], shloka: ['श्लो॰', 'Śl.']};
function verseHTML(i){
  const it = IT[i], id = it.id, me = ME(), vv = verseOf(i);
  const bm = SHOWN().some(p => p.bm[KEY(id)]);
  const sh = VSHORT[it.y];
  let h = '<div class="verse" id="v' + i + '" data-i="' + i + '"><div class="vtext">' + vv.v.map((l, y) => {
    const last = y === vv.v.length - 1;
    let ln = last && it.y === 'cau' && it.n && /।।\s*$/.test(l) ? l.replace(/\s*।।\s*$/, ' ।।' + String(it.n).replace(/\d/g, d => DIG[d]) + '।।') : l;
    if (LANG() === 'en') ln = ln.replace(/[०-९]/g, d => DIG.indexOf(d));
    const w = wordsHTML(ln).replace(/।।\s*([0-9०-९][^\s।<]*)\s*।।/, '<span style="white-space:nowrap">।।$1।।</span>');
    const lead = y === 0 && sh ? '<span class="vt">' + T(sh[0], sh[1]) + '</span>' : '';
    const tail = last ? '<span class="vend"><button class="vb' + (bm ? ' bm-on' : '') + '" data-a="bm" aria-label="bookmark"><svg><use href="#i-bm"/></svg></button><button class="vb" data-a="menu" aria-label="more"><svg><use href="#i-more"/></svg></button></span>' + (hasAu(i) ? '<button class="vb vplay" data-a="play" aria-label="play"><svg><use href="#i-play"/></svg></button>' : '') : '';
    return '<p>' + lead + w + tail + '</p>'; }).join('') + '</div>';
  if (S.settings.tr && it.t && it.t.length) h += '<div class="tr">' + it.t.map(l => '<div>' + l.split(/(?<=,)\s+/).map(x => '<span class="half">' + esc(x).replace(/\s*॥\s*([^॥]*?)\s*॥/g, ' <span class="dd">॥$1॥</span>') + '</span>').join(' ') + '</div>').join('') + '</div>';
  if (layerOn('h')){ const m = mean('hi', i); if (m) h += '<div class="layer h">' + esc(m.x).replace(/\s*(।।[^।]*।।)\s*$/, '<span style="white-space:nowrap"> $1</span>') + (m.edited ? '<span class="tag">' + T('संशोधित', 'edited') + '</span>' : '') + (m.f ? '<div class="fn">' + m.f.map(esc).join('<br>') + '</div>' : '') + '</div>'; }
  if (layerOn('w')) h += '<div class="layer wl">' + wbHTML(vv.v, langOf(i)) + '</div>';
  if (layerOn('e')){ const m = mean('en', i); if (m) h += '<div class="layer e">' + esc(m.x) + (m.edited ? '<span class="tag">edited</span>' : '') + (m.f ? '<div class="fn">' + m.f.map(esc).join('<br>') + '</div>' : '') + '</div>'; }
  for (const p of SHOWN()) (p.notes[KEY(id)] || []).forEach((n, k) => { h += '<div class="note"><div class="who">' + esc(p.name) + ' · ' + new Date(n.ts).toLocaleDateString(LANG() === 'en' ? 'en-IN' : 'hi-IN') + (p.id === me.id ? '<button data-a="enote" data-k="' + k + '">' + T('बदलें', 'Edit') + '</button>' : '') + '</div>' + esc(n.t).replace(/\n/g, '<br>') + '</div>'; });
  return h + '</div>';
}
function pauseHTML(i){
  const list = pauseAfter[i]; if (!list) return '';
  return list.filter(([o]) => R.org === 'k' || R.org === o).map(([o, n]) => { const done = DONE(ME(), o)[n]; return '<div class="pause" data-pause="' + o + n + '"><b>' + PNAME(o) + ' · ' + VN(n) + '</b><div class="sub">' + T('यहाँ विश्राम करें', 'A place to pause the reading') + '</div><button class="btn small' + (done ? ' ghost' : '') + '" data-a="done" data-o="' + o + '" data-n="' + n + '" data-i="' + i + '">' + (done ? T('✓ पूर्ण — बदलें', '✓ Completed — undo') : T('विश्राम पूर्ण करें', 'Mark vishram complete')) + '</button></div>'; }).join('');
}
function pageHTML(pg){
  const p = PAGES[pg], a = Math.max(p.from, R.a), b = Math.min(p.to, R.b); let h = '<div class="pg" data-pg="' + pg + '">';
  for (let i = a; i <= b; i++){
    if (i === PARTS[IT[i].p].a) h += '<div class="part-h"><b>' + esc(KNAME(IT[i].p)) + '</b></div>';
    const t = topicAt.get(i); if (t) h += '<div class="topic-h" id="t' + i + '"><b>' + esc(TNAME(t)) + '</b></div>';
    h += verseHTML(i) + pauseHTML(i);
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
  $('#rTopic').textContent = t ? TNAME(t) : KNAME(IT[i].p);
  let k = KNAME(IT[i].p) + ' · ' + posLabel(i); if (R.org !== 'k') k = VN(R.n) + ' · ' + k;
  $('#rKand').textContent = k;
  const s = curSection(i);
  $('#rMid').innerHTML = '<span class="ml">' + (s ? spanLabel(Math.max(s.i, R.a), Math.min(s.end, R.b)) : spanLabel(R.a, R.b)) + ' ▾</span><small>' + esc(s ? TNAME(s) : (R.org === 'k' ? KNAME(R.n) : VN(R.n))) + '</small>';
}
let scT;
window.addEventListener('scroll', () => { if (!$('#reader').classList.contains('on')) return; ensure(); clearTimeout(scT); scT = setTimeout(() => { updateHeader(); savePos(); }, 200); }, {passive: true});
function savePos(i){ if (i == null) i = topVisibleItem(); const ws = WS(); ws.pos[R.org] = i; ws.last = {org: R.org, i}; save(); }
function openReader(org, i, flash){
  if (!S.hinted){ S.hinted = 1; save(); setTimeout(() => toast(T('किसी शब्दको छूकर अर्थ देखें · नीचेसे प्रसंग चुनें', 'Tap any word for its meaning · choose a section at the bottom')), 900); }
  R.org = org; [R.a, R.b, R.n] = rangeFor(org, i);
  if (!$('#reader').classList.contains('on')) show('reader');
  renderAround(i); if (flash){ const el = document.getElementById('v' + i); if (el) el.classList.add('flash'); }
  savePos(i);
}
function reopenReader(){ const l = WS().last; if (l) openReader(l.org, l.i); }
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
function sectionSheet(){
  const cur = curSection(topVisibleItem());
  let h = '';
  if (R.org === 'k') h += '<div class="pick">' + PARTS.map(p => '<button data-to="' + p.a + '" class="' + (p.k === R.n ? 'on' : '') + '">' + esc(KNAME(p.k)) + '</button>').join('') + '</div>';
  else { const P = PLAN[R.org]; h += '<div class="pick days">' + Array.from({length: P.n}, (_, x) => x + 1).map(n => '<button data-to="' + dayRange(R.org, n)[0] + '" class="' + (n === R.n ? 'on' : '') + (DONE(ME(), R.org)[n] ? ' done' : '') + '">' + DEV(n) + '</button>').join('') + '</div>'; }
  const secs = TOPICS.filter(t => t.i <= R.b && t.end >= R.a);
  const rows = []; if (!secs.length || secs[0].i > R.a) rows.push({i: R.a, end: (secs[0] ? secs[0].i - 1 : R.b), name: R.org === 'k' ? KNAME(R.n) : VN(R.n)});
  secs.forEach(t => rows.push({i: Math.max(t.i, R.a), end: Math.min(t.end, R.b), name: TNAME(t), t}));
  h += '<h2>' + (R.org === 'k' ? esc(KNAME(R.n)) : PNAME(R.org) + ' · ' + VN(R.n)) + '</h2><div class="secs">' + rows.map(r => '<button data-to="' + r.i + '" class="' + (cur && r.t === cur ? 'on' : '') + '"><span class="sr">' + spanLabel(r.i, r.end) + '</span><span class="sn">' + esc(r.name) + '</span></button>').join('') + '</div>';
  openSheet(h);
  $$('#sheetBody [data-to]').forEach(b => b.onclick = () => { closeSheet(); jumpTo(+b.dataset.to); });
  const on = $('#sheetBody .secs .on'); if (on) setTimeout(() => on.scrollIntoView({block: 'center'}), 60);
}
$('#rMid').onclick = sectionSheet;
$('#rBack').onclick = back;
$$('#rLayers button').forEach(b => b.onclick = () => { const l = b.dataset.l; S.settings.layers[l] = !S.settings.layers[l]; save(); if (l === 'e') applyLang(); syncLayers(); refreshReader(); });
function syncLayers(){ $$('#rLayers button').forEach(b => b.classList.toggle('on', layerOn(b.dataset.l))); }
function applyRecite(){ document.body.classList.toggle('recite', !!S.settings.recite); $('#rRecite').hidden = !S.settings.recite; }
function toggleRecite(){ S.settings.recite = !S.settings.recite; save(); applyRecite(); toast(S.settings.recite ? T('पाठ मोड: केवल मूल पाठ', 'Recitation mode: verses only') : T('अर्थ फिर दिखेंगे', 'Meanings shown again')); }
$('#rRecite').onclick = toggleRecite;
$('#rMore').onclick = () => { openSheet('<div class="menu">' +
  '<button data-m="search"><svg><use href="#i-search"/></svg>' + LB.search() + '</button>' +
  '<button data-m="sec"><svg><use href="#i-jump"/></svg>' + LB.sections() + '</button>' +
  '<button data-m="bm"><svg><use href="#i-bm"/></svg>' + LB.bm() + '</button>' +
  '<button data-m="timer"><svg><use href="#i-clock"/></svg>' + LB.timer() + (S.timer ? ' · ' + timerText() + (S.timer.run ? T(' (रोकें)', ' (pause)') : T(' (चलाएँ)', ' (resume)')) : T(' (शुरू करें)', ' (start)')) + '</button>' +
  (S.timer ? '<button data-m="treset"><svg><use href="#i-clock"/></svg>' + LB.timer() + T(' — शून्य करें', ' — reset') + '</button>' : '') +
  '<button data-m="font"><svg><use href="#i-text"/></svg>' + LB.size() + '</button>' +
  '<button data-m="set"><svg><use href="#i-set"/></svg>' + LB.set() + '</button></div>' +
  '<div class="menusw">' + sw('mtr', LB.tr(), LB.trSub(), S.settings.tr) + sw('mrc', LB.rc(), LB.rcSub(), S.settings.recite) + '</div>');
  $('#mtr').onchange = e => { S.settings.tr = e.target.checked; save(); refreshReader(); };
  $('#mrc').onchange = e => { if (!!S.settings.recite !== e.target.checked) toggleRecite(); };
};
$('#sheetBody').addEventListener('click', ev => {
  const b = ev.target.closest('[data-m]'); if (!b) return;
  const m = b.dataset.m; closeSheet();
  if (m === 'search') show('search'); if (m === 'sec') sectionSheet(); if (m === 'timer') timerToggle(); if (m === 'treset') timerReset();
  if (m === 'font') fontSheet(); if (m === 'bm') show('bookmarks'); if (m === 'set') show('settings');
});
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
    else if (act === 'bm'){ const me = ME(), k = KEY(IT[i].id); const had = !!me.bm[k]; if (had) delete me.bm[k]; else me.bm[k] = Date.now(); save(); rerenderItem(i); toast(!had ? T('बुकमार्क जोड़ा', 'Bookmarked') : T('बुकमार्क हटाया', 'Bookmark removed')); }
    else if (act === 'enote') noteSheet(i, +a.dataset.k);
    else if (act === 'menu') itemMenu(i);
    else if (act === 'done'){ const o = a.dataset.o, n = +a.dataset.n, d = DONE(ME(), o); if (d[n]) delete d[n]; else d[n] = Date.now(); save(); const box = a.closest('.pause'); const tmp = document.createElement('div'); tmp.innerHTML = pauseHTML(+a.dataset.i); const nb = Array.from(tmp.children).find(x => x.dataset.pause === o + n); if (box && nb) box.replaceWith(nb); if (d[n]) toast(VN(n) + T(' पूर्ण — जय श्रीराम', ' complete — Jai Shri Ram')); }
    return;
  }
  const w = ev.target.closest('.w'); if (w){ w.classList.add('sel'); const vb = w.closest('.verse'); wordSheet(w.dataset.w || w.textContent, null, vb ? langOf(+vb.dataset.i) : W.lang); }
});
function noteSheet(i, k){
  const me = ME(), key = KEY(IT[i].id), arr = me.notes[key] || [], cur = k != null ? arr[k] : null;
  openSheet('<h2>' + (cur ? T('टिप्पणी बदलें', 'Edit note') : T('अपनी टिप्पणी लिखें', 'Write your note')) + '</h2><p class="small muted">' + esc(itemLabel(i)) + T(' · लेखक: ', ' · by ') + esc(me.name) + '</p><textarea id="nt" placeholder="' + T('अपने विचार, भाव या कथा यहाँ लिखें…', 'Your thoughts or the story behind this verse…') + '">' + esc(cur ? cur.t : '') + '</textarea><div class="acts"><button class="btn" id="nSave">' + T('सेव करें', 'Save') + '</button>' + (cur ? '<button class="btn ghost" id="nDel">' + T('हटाएँ', 'Delete') + '</button>' : '') + '</div>');
  setTimeout(() => $('#nt').focus(), 250);
  $('#nSave').onclick = () => { const t = $('#nt').value.trim(); if (!t){ closeSheet(); return; } if (cur){ cur.t = t; cur.ts = Date.now(); } else { (me.notes[key] = arr).push({t, ts: Date.now()}); } save(); closeSheet(); rerenderItem(i); toast(T('टिप्पणी सेव हुई', 'Note saved')); };
  if ($('#nDel')) $('#nDel').onclick = () => { arr.splice(k, 1); if (!arr.length) delete me.notes[key]; save(); closeSheet(); rerenderItem(i); };
}
function itemMenu(i){
  const id = IT[i].id, edited = verseOf(i).edited || ['hi', 'en'].some(k => { const m = mean(k, i); return m && m.edited; });
  openSheet('<p class="small muted">' + esc(itemLabel(i)) + '</p><div class="menu">' + (hasAu(i) ? '<button data-x="play"><svg><use href="#i-play"/></svg>' + T('यहाँसे सुनें', 'Listen from here') + '</button>' : '') + '<button data-x="copy"><svg><use href="#i-copy"/></svg>' + T('मूल पाठ और अर्थ कॉपी करें', 'Copy verse and meaning') + '</button><button data-x="note"><svg><use href="#i-note"/></svg>' + T('टिप्पणी लिखें', 'Write a note') + '</button><button data-x="edit"><svg><use href="#i-edit"/></svg>' + T('पाठ या अर्थमें सुधार करें', 'Correct the text or meaning') + '</button>' + (edited ? '<button data-x="revert"><svg><use href="#i-edit"/></svg>' + T('मेरा सुधार हटाएँ (पुस्तकका पाठ लौटाएँ)', 'Remove my correction (restore book text)') + '</button>' : '') + '</div>');
  $$('#sheetBody [data-x]').forEach(b => b.onclick = () => {
    const x = b.dataset.x; closeSheet();
    if (x === 'play') playFrom(i, null);
    if (x === 'copy'){ const mh = mean('hi', i), me_ = mean('en', i); const txt = verseOf(i).v.join('\n') + (mh ? '\n\n' + mh.x : '') + (me_ ? '\n\n' + me_.x : ''); (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(() => toast(T('कॉपी हो गया', 'Copied'))).catch(() => toast(T('कॉपी नहीं हो सका', 'Could not copy'))); }
    if (x === 'note') noteSheet(i, null);
    if (x === 'edit') editSheet(i);
    if (x === 'revert'){ S.profiles.forEach(p => { delete p.fix[KEY(id)]; ['hi', 'en'].forEach(k => { if (SRC[k]) delete p.fix[KEY(SRC[k].id + ':' + id)]; }); }); save(); rerenderItem(i); toast(T('पुस्तकका पाठ लौटाया', 'Book text restored')); }
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
let PL = {on: false, t: -1, end: null, cur: -1, hold: 0};
function buildAudio(){ AUT = []; const A = SRC.au; if (!A) return; A.tracks.forEach(t => { t.fi = ID[t.first]; t.li = ID[t.last]; }); AUT = A.tracks.map(() => []); for (const id in A.at){ const i = ID[id]; if (i == null) continue; const [t, s] = A.at[id]; AUT[t].push([i, s]); } AUT.forEach(a => a.sort((x, y) => x[1] - y[1])); }
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
/* outside the website (e.g. a claude.ai artifact) YouTube cannot be embedded: open YouTube's own player page, which can stop at the end of what was asked */
function ytWatchURL(){
  const A = SRC.au, st = Math.floor(ytInfo.t || 0); let end = '';
  if (PL.end != null){ const nx = A.at[(IT[PL.end + 1] || {}).id]; if (nx && nx[0] === PL.t) end = '&end=' + Math.ceil(nx[1]); }
  return 'https://www.youtube.com/embed/' + ytVid + '?autoplay=1&start=' + st + end;
}
function ytBlocked(){
  $('#ytBox').innerHTML = '<div class="ytno"><p>' + T('यह पन्ना YouTube वीडियो नहीं चला पा रहा।', 'This page is not allowed to play YouTube here.') + '</p><a class="btn" target="_blank" rel="noopener" href="' + ytWatchURL() + '">' + T('YouTube पर इसी दोहे से सुनें ↗', 'Listen on YouTube from this verse ↗') + '</a></div>';
}
window.addEventListener('message', e => {
  if (!/youtube(-nocookie)?\.com$/.test((e.origin || '').replace(/^https?:\/\/(www\.)?/, ''))) return;
  let d; try { d = typeof e.data === 'string' ? JSON.parse(e.data) : e.data; } catch (x) { return; }
  if (!d) return;
  if (d.event === 'onReady' || d.event === 'initialDelivery' || d.event === 'infoDelivery'){ if (!ytOK){ ytOK = true; if (PL.on) $('#pTrack').textContent = playingName(); } }
  const info = d.info || {};
  if (typeof info.currentTime === 'number') ytInfo.t = info.currentTime;
  if (typeof info.duration === 'number' && info.duration) ytInfo.d = info.duration;
  if (typeof info.playerState === 'number'){ ytInfo.st = info.playerState; syncPlayer(); if (info.playerState === 0) onEnded(); }
  if (d.event === 'onStateChange' && typeof d.info === 'number'){ ytInfo.st = d.info; syncPlayer(); if (d.info === 0) onEnded(); }
});
/* what is playing, in the app's own words: the reading (kāṇḍa or plan day) and the reciter — never the recording's title */
function playingName(){ return (R.org === 'k' ? KNAME(R.n) : TT(PLAN[R.org].name) + ' · ' + VN(R.n)) + ' · ' + TT(SRC.au.meta.title); }
function playFrom(i, end){
  if (!SRC.au) return;
  if (!hasAu(i)){ const j = firstAu(i, Math.min(IT.length - 1, i + 80)); if (j == null) return; i = j; }
  const [t, st0] = SRC.au.at[IT[i].id], tr = SRC.au.tracks[t];
  const st = (end != null && i === tr.fi) ? 0 : st0;
  PL.on = true; PL.t = t; PL.end = end; PL.cur = -1; PL.hold = 0;
  $('#player').hidden = false; document.body.classList.add('playing'); wake(true);
  if (ytVid !== tr.yt || !ytFrame()) ytLoad(tr.yt, st); else { ytPost('seekTo', [st, true]); ytPost('playVideo'); ytInfo.t = st; }
  setCur(i); $('#pTrack').textContent = playingName(); syncPlayer();
}
function onEnded(){ if (!PL.on) return; const tr = SRC.au.tracks[PL.t]; const nx = tr.li + 1; if ((PL.end == null || PL.end >= nx) && hasAu(nx)){ playFrom(nx, PL.end); return; } stopAudio(); }
function curAt(time){ const a = AUT[PL.t]; let lo = 0, hi = a.length - 1, r = a[0][0]; while (lo <= hi){ const m = (lo + hi) >> 1; if (a[m][1] <= time){ r = a[m][0]; lo = m + 1; } else hi = m - 1; } return r; }
setInterval(() => {
  if (!PL.on || !ytOK) return;
  const time = ytInfo.t; const i = curAt(time);
  if (PL.end != null && i > PL.end){ stopAudio(); toast(T('पाठ पूर्ण — जय श्रीराम', 'Recitation complete — Jai Shri Ram')); return; }
  setCur(i); const d = ytInfo.d || SRC.au.tracks[PL.t].dur; $('#pProg').style.width = (100 * time / d) + '%';
}, 300);
/* place the verse being recited in the space between the top bar and the player:
   centred if it fits, otherwise with its first line just below the top bar (never hidden under it) */
function keepInView(el){
  const top = $('#reader .bar').getBoundingClientRect().bottom, pl = $('#player'), bottom = pl.hidden ? innerHeight : pl.getBoundingClientRect().top;
  const r = el.getBoundingClientRect(), room = bottom - top, gap = room - r.height;
  const want = gap > 16 ? top + gap / 2 : top + 8;
  window.scrollTo({top: Math.max(0, scrollY + r.top - want), behavior: 'smooth'});
}
function setCur(i){
  if (PL.cur === i) return; PL.cur = i;
  $$('#rBody .verse.now').forEach(v => v.classList.remove('now'));
  $('#pVerse').textContent = KNAME(IT[i].p) + ' · ' + posLabel(i); $('#pTrack').textContent = playingName();
  if (!$('#reader').classList.contains('on')) return;
  if (i < R.a || i > R.b){ R.org = R.org; [R.a, R.b, R.n] = rangeFor(R.org, i); renderAround(i); }
  else if (!document.getElementById('v' + i)) renderAround(i, false);
  const el = document.getElementById('v' + i);
  if (el){ el.classList.add('now'); if (Date.now() > PL.hold) keepInView(el); }
}
function stopAudio(){ ytPost('pauseVideo'); PL.on = false; $('#player').hidden = true; document.body.classList.remove('playing'); $$('#rBody .verse.now').forEach(v => v.classList.remove('now')); }
function playing(){ return ytInfo.st === 1 || ytInfo.st === 3; }
function syncPlayer(){ $('#pPlay').innerHTML = '<svg><use href="#i-' + (playing() ? 'pause' : 'play') + '"/></svg>'; }
['touchstart', 'wheel'].forEach(e => window.addEventListener(e, ev => { if (PL.on && !ev.target.closest('#player')) PL.hold = Date.now() + 8000; }, {passive: true}));
$('#pPlay').onclick = () => { if (playing()) ytPost('pauseVideo'); else ytPost('playVideo'); setTimeout(syncPlayer, 400); };
$('#pClose').onclick = stopAudio;
function stepVerse(d){ const a = AUT[PL.t]; const k = a.findIndex(x => x[0] === PL.cur); const n = k + d; if (k >= 0 && n >= 0 && n < a.length){ ytPost('seekTo', [a[n][1], true]); ytInfo.t = a[n][1]; PL.hold = 0; } }
$('#pPrev').onclick = () => stepVerse(-1);
$('#pNext').onclick = () => stepVerse(1);
$('#pInfo').onclick = () => { if (PL.cur < 0) return; if (!$('#reader').classList.contains('on')) openReader(R.org, PL.cur); PL.hold = 0; const c = PL.cur; PL.cur = -1; setCur(c); };
function playRange(org, a, b){ const st = firstAu(a, b); if (st == null) return; openReader(org, st); playFrom(st, b); }

/* ---------------- library (any depth: tradition › text › part › work) ---------------- */
let libPath = [];
function libNode(){ let n = {children: LIB}; for (const id of libPath){ const c = (n.children || []).find(x => x.id === id); if (!c) { libPath = []; return {children: LIB}; } n = c; } return n; }
function renderLibrary(){
  const node = libNode(), kids = node.children || [];
  let crumbs = '<button data-lp="-1">' + LB.lib() + '</button>'; let n = {children: LIB};
  libPath.forEach((id, k) => { n = n.children.find(x => x.id === id); crumbs += ' › <button data-lp="' + k + '">' + esc(TT(n.title)) + '</button>'; });
  $('#libCrumbs').innerHTML = libPath.length ? crumbs : '';
  $('#libTitle').textContent = libPath.length ? TT(node.title) : LB.lib();
  $('#libList').innerHTML = kids.map(c => '<li><button class="it" data-node="' + esc(c.id) + '"><span class="grow"><span class="ti">' + esc(TT(c.title)) + '</span><br><span class="ds">' + esc(TT(c.desc || c.by) || (c.children ? DEV(c.children.length) + T(' ग्रन्थ', ' texts') : '')) + '</span></span><span class="chev">›</span></button></li>').join('');
  $$('#libList [data-node]').forEach(b => b.onclick = () => { const c = kids.find(x => x.id === b.dataset.node); if (c.work) openWork(c.work); else { libPath.push(c.id); renderLibrary(); window.scrollTo(0, 0); } });
  $$('#libCrumbs [data-lp]').forEach(b => b.onclick = () => { libPath = libPath.slice(0, +b.dataset.lp + 1); renderLibrary(); });
}
function workPath(id){ let r = null; (function walk(n){ (n || []).forEach(c => { if (c.work === id) r = c.path; else walk(c.children); }); })(LIB); return r || id; }
async function openWork(id, noShow){
  $('#loading').hidden = false;
  try {
    if (!W || W.id !== id){ const path = workPath(id); W = await getJSON(path + '/work'); W.path = path; buildWork(); await Promise.all([loadSources(), loadGlossaries()]); }
    S.work = id; save();
  } catch (e) { toast(T('यह ग्रन्थ नहीं खुल सका', 'Could not open this text')); $('#loading').hidden = true; return; }
  $('#loading').hidden = true;
  if (!noShow) show('home');
}

/* ---------------- work home ---------------- */
function homeOrg(){ return WS().org || 'k'; }
function renderHome(){
  if (!W) return;
  $('#hTitle').textContent = TT(W.title); $('#hSub').textContent = TT(W.by) + ' · ' + TT(W.edition);
  $('#qVidhi').hidden = !W.vidhi;
  const L = WS().last;
  $('#contCard').innerHTML = L && IT[L.i] ? '<div class="card"><div class="row"><div class="grow"><h3>' + T('जहाँ छोड़ा था', 'Continue where you left off') + '</h3><div class="big" style="font-size:17px">' + esc(KNAME(IT[L.i].p) + (topicOf(L.i) ? ' / ' + TNAME(topicOf(L.i)) : '')) + '</div><div class="sub">' + (L.org !== 'k' && PLAN[L.org] ? PNAME(L.org) + ' · ' + VN(dayOf(L.org, L.i)) + ' · ' : '') + posLabel(L.i) + '</div></div><button class="btn" id="cGo">' + T('आगे पढ़ें', 'Continue') + '</button></div></div>' : '';
  if ($('#cGo')) $('#cGo').onclick = () => openReader(L.org, L.i);
  const org = homeOrg();
  $('#orgSeg').innerHTML = '<button data-org="k">' + esc(TT(W.parts.name)) + '</button>' + PLANS.map(p => '<button data-org="' + p.id + '">' + esc(TT(p.name)) + '</button>').join('');
  $$('#orgSeg button').forEach(b => { b.classList.toggle('on', b.dataset.org === org); b.onclick = () => { WS().org = b.dataset.org; save(); renderHome(); }; });
  const play = (o, a, b) => firstAu(a, b) != null ? '<button class="lplay" data-po="' + o + '" data-pa="' + a + '" data-pb="' + b + '" aria-label="play"><svg><use href="#i-play"/></svg></button>' : '';
  let h = '';
  if (org === 'k') PARTS.forEach(p => { const tps = TOPICS.filter(t => IT[t.i].p === p.k).length; h += '<li class="rowp">' + play('k', p.a, p.b) + '<button class="it" data-open="' + p.a + '"><span class="no">' + DEV(p.k + 1) + '</span><span class="grow"><span class="ti">' + esc(KNAME(p.k)) + '</span><br><span class="ds">' + DEV(tps) + T(' प्रसंग', ' sections') + '</span></span><span class="chev">›</span></button></li>'; });
  else { const P = PLAN[org]; const dn = Object.keys(DONE(ME(), org)).length; h += '<li class="small muted" style="padding:6px 2px;border:0">' + DEV(dn) + ' / ' + DEV(P.n) + T(' विश्राम पूर्ण · विश्रामके अन्तमें “विश्राम पूर्ण करें” दबाएँ', ' vishrams completed · tap “Mark vishram complete” at the end of each') + '</li>';
    for (let n = 1; n <= P.n; n++){ const [a, b] = dayRange(org, n), d = DONE(ME(), org)[n]; h += '<li class="rowp">' + play(org, a, b) + '<button class="it" data-open="' + a + '"><span class="no' + (d ? ' done' : '') + '">' + (d ? '✓' : DEV(n)) + '</span><span class="grow"><span class="ti">' + VN(n) + '</span><br><span class="ds">' + rangeDesc(a, b) + '</span></span><span class="chev">›</span></button></li>'; } }
  $('#orgList').innerHTML = h;
  $$('#orgList [data-open]').forEach(b => b.onclick = () => openReader(org, +b.dataset.open));
  $$('#orgList [data-pa]').forEach(b => b.onclick = ev => { ev.stopPropagation(); playRange(b.dataset.po, +b.dataset.pa, +b.dataset.pb); });
}
$('#hLib').onclick = () => show('library');

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
  if (scopes.has('n')) for (const p of SHOWN()) for (const k in p.notes){ if (!k.startsWith(W.id + ':')) continue; const i = ID[k.slice(W.id.length + 1)]; if (i == null) continue; p.notes[k].forEach(n => { if ((latin ? normL(n.t) : normD(n.t)).includes(nq)) res.push([i, T('टिप्पणी · ', 'Note · ') + p.name, n.t, latin]); }); }
  box.innerHTML = res.length ? '<p class="small muted">' + DEV(res.length) + (res.length >= 300 ? '+' : '') + T(' परिणाम', ' results') + '</p>' + res.map(r => '<button class="res" data-i="' + r[0] + '"><div class="where">' + esc(itemLabel(r[0])) + ' · ' + esc(r[1]) + '</div><div class="snip' + (r[3] ? ' lat' : '') + '">' + snip(r[2], q, r[3]) + '</div></button>').join('') : '<div class="empty">' + T('कुछ नहीं मिला। दूसरा रूप लिखकर देखें।', 'Nothing found. Try another spelling.') + '</div>';
  $$('#sRes .res').forEach(b => b.onclick = () => openReader('k', +b.dataset.i, true));
}

/* ---------------- bookmarks ---------------- */
function renderBookmarks(){
  const bms = [], notes = [], pre = W.id + ':';
  for (const p of SHOWN()){ for (const k in p.bm) if (k.startsWith(pre) && ID[k.slice(pre.length)] != null) bms.push([ID[k.slice(pre.length)], p]); for (const k in p.notes) if (k.startsWith(pre) && ID[k.slice(pre.length)] != null) p.notes[k].forEach(n => notes.push([ID[k.slice(pre.length)], p, n])); }
  bms.sort((a, b) => a[0] - b[0]); notes.sort((a, b) => a[0] - b[0]);
  let h = '<h2 style="font-size:19px;margin:20px 0 4px">' + T('बुकमार्क (', 'Bookmarks (') + DEV(bms.length) + ')</h2>';
  h += bms.length ? bms.map(b => '<button class="res" data-i="' + b[0] + '"><div class="where">' + esc(itemLabel(b[0])) + (S.profiles.length > 1 ? ' · ' + esc(b[1].name) : '') + '</div><div class="snip" style="font-weight:700">' + esc(IT[b[0]].v[0]) + '</div></button>').join('') : '<p class="muted">' + T('किसी भी पदकी पंक्तिके अन्तमें बुकमार्क चिह्न दबाएँ।', 'Tap the bookmark sign at the end of any verse.') + '</p>';
  h += '<h2 style="font-size:19px;margin:26px 0 4px">' + T('टिप्पणियाँ (', 'Notes (') + DEV(notes.length) + ')</h2>';
  h += notes.length ? notes.map(n => '<button class="res" data-i="' + n[0] + '"><div class="where">' + esc(itemLabel(n[0])) + ' · ' + esc(n[1].name) + '</div><div class="snip">' + esc(n[2].t.slice(0, 200)) + '</div></button>').join('') : '<p class="muted">' + T('किसी पदके ⋮ मेनूसे अपनी टिप्पणी लिखें।', 'Use the ⋮ menu of any verse to write a note.') + '</p>';
  $('#bmBody').innerHTML = h + '<div style="height:40px"></div>';
  $$('#bmBody .res').forEach(b => b.onclick = () => openReader('k', +b.dataset.i, true));
}

/* ---------------- settings ---------------- */
function renderSettings(){
  const st = S.settings, srcs = (W && W.sources) || {}, cur = S.src[W ? W.id : ''] || {};
  const pick = (kind, label, off) => { const list = srcs[kind] || []; if (!list.length) return ''; const sel = cur[kind] || list[0].id; return '<div class="field"><label>' + label + '</label><select data-src="' + kind + '">' + list.map(s => '<option value="' + s.id + '"' + (sel === s.id ? ' selected' : '') + '>' + esc(TT(s.title)) + '</option>').join('') + (off ? '<option value="off"' + (sel === 'off' ? ' selected' : '') + '>' + T('बंद', 'Off') + '</option>' : '') + '</select></div>'; };
  let h = '<h2>' + T('पढ़ते समय दिखाएँ', 'Show while reading') + '</h2><p class="small muted">' + T('ये वही हैं जो पढ़नेके पन्नेपर ऊपर “हिं · En · शब्द” और ⋮ मेनूमें हैं। ऐप उसी भाषामें दिखता है: अंग्रेज़ी अर्थ चालू हो तो English, नहीं तो हिंदी।', 'These are the same as “हिं · En · शब्द” at the top of the reading page and the switches in its ⋮ menu. The app follows your choice of language: English if English meaning is on, otherwise Hindi.') + '</p>' +
    sw('sh', LB.h() + ' (हिं)', '', st.layers.h) + sw('se', LB.e() + ' (En)', '', st.layers.e) + sw('sw', LB.w() + ' (शब्द)', T('हर शब्दका हिंदी और English अर्थ', 'Hindi and English meaning of each word'), st.layers.w) +
    sw('str', LB.tr(), LB.trSub(), st.tr) + sw('src', LB.rc(), LB.rcSub(), st.recite) +
    (W ? '<h2>' + LB.src() + ' · ' + esc(TT(W.title)) + '</h2><p class="small muted">' + T('मूल पाठ वही रहता है; अर्थ और ऑडियो किस स्रोतसे आएँ, यहाँ चुनें। शब्दार्थ सब स्रोतोंके लिये एक ही है।', 'The verses stay the same; choose where the meanings and the audio come from. Word meanings are the same for every source.') + '</p>' + pick('hi', LB.h()) + pick('en', LB.e()) + pick('au', LB.au(), true) : '') +
    '<h2>' + T('पढ़नेकी सुविधा', 'Reading comfort') + '</h2>' + sw('swk', LB.wake(), '', st.wake) +
    '<div class="field"><label>' + LB.size() + '</label><input type="range" id="ssz" min="16" max="34" value="' + st.size + '" style="border:0;padding:0"></div>' +
    '<div class="field"><label>' + LB.theme() + '</label><select id="sth"><option value="light">' + T('दिन (हल्का)', 'Light') + '</option><option value="dark">' + T('रात (गहरा)', 'Dark') + '</option><option value="auto">' + T('फ़ोनके अनुसार', 'Same as phone') + '</option></select></div>' +
    '<h2>' + T('मेरी फ़ाइल', 'My file') + '</h2><p class="small muted">' + T('आपकी टिप्पणियाँ, बुकमार्क, प्रगति, सेटिंग्स और सुधार इसी फ़ोनमें रहते हैं। फ़ाइल सेव करके बैकअप रखें या दूसरे फ़ोनपर खोलें।', 'Your notes, bookmarks, progress, settings and corrections stay on this phone. Save the file as a backup or to open it on another phone.') + (canStore ? '' : ' <b>' + T('ध्यान दें: यह फ़ोन डेटा अपने-आप नहीं रख पा रहा — पाठके बाद “फ़ाइल सेव करें” दबाएँ।', 'This phone is not keeping app data — tap Save my file after each reading.') + '</b>') + '</p>' +
    '<div class="acts"><button class="btn" id="exp">' + T('फ़ाइल सेव करें', 'Save my file') + '</button><button class="btn ghost" id="imp">' + T('फ़ाइल खोलें', 'Open a file') + '</button></div>' +
    '<h2>' + T('पढ़नेवाले', 'Readers') + '</h2><p class="small muted">' + T('टिप्पणियाँ लिखनेवालेके नामसे सेव होती हैं। गोल बटन: अभी कौन लिख रहा है। चौकोर बटन: किसकी टिप्पणियाँ दिखें।', 'Notes are saved under the writer’s name. Round button: who is writing now. Square box: whose notes to show.') + '</p>' +
    S.profiles.map(p => '<div class="sw"><span class="row grow"><input type="radio" name="act" value="' + p.id + '"' + (p.id === S.active ? ' checked' : '') + ' style="width:auto"> <span class="grow">' + esc(p.name) + '<small>' + Object.values(p.notes).reduce((a, b) => a + b.length, 0) + T(' टिप्पणी · ', ' notes · ') + Object.keys(p.bm).length + T(' बुकमार्क', ' bookmarks') + '</small></span></span><input type="checkbox" data-show="' + p.id + '"' + (S.show.includes(p.id) ? ' checked' : '') + ' style="width:auto"><button class="small" data-ren="' + p.id + '" style="text-decoration:underline;margin-left:8px">' + T('नाम', 'Rename') + '</button>' + (S.profiles.length > 1 ? '<button class="small" data-del="' + p.id + '" style="text-decoration:underline;margin-left:8px">' + T('हटाएँ', 'Delete') + '</button>' : '') + '</div>').join('') +
    '<div class="acts" style="margin-top:12px"><button class="btn ghost small" id="addp">' + T('+ नया व्यक्ति', '+ Add reader') + '</button></div><div style="height:50px"></div>';
  $('#setBody').innerHTML = h; $('#sth').value = st.theme;
  const bind = (id, f) => $('#' + id).onchange = e => { f(e.target.checked); save(); };
  bind('sh', v => st.layers.h = v); bind('se', v => { st.layers.e = v; applyLang(); renderSettings(); }); bind('sw', v => st.layers.w = v); bind('str', v => st.tr = v); bind('src', v => { if (!!st.recite !== v) toggleRecite(); }); bind('swk', v => st.wake = v);
  $$('[data-src]').forEach(s => s.onchange = async () => { const c = S.src[W.id] = S.src[W.id] || {}; c[s.dataset.src] = s.value; save(); if (s.dataset.src === 'au') stopAudio(); await loadSources(); IDX = null; toast(T('स्रोत बदला', 'Source changed')); });
  $('#ssz').oninput = e => { st.size = +e.target.value; applyTheme(); save(); };
  $('#sth').onchange = e => { st.theme = e.target.value; applyTheme(); save(); };
  $('#exp').onclick = exportFile; $('#imp').onclick = () => $('#fileIn').click();
  $$('[name=act]').forEach(r => r.onchange = () => { S.active = r.value; if (!S.show.includes(r.value)) S.show.push(r.value); save(); renderSettings(); });
  $$('[data-show]').forEach(c => c.onchange = () => { const id = c.dataset.show; if (c.checked){ if (!S.show.includes(id)) S.show.push(id); } else S.show = S.show.filter(x => x !== id); save(); });
  $$('[data-ren]').forEach(b => b.onclick = () => { const p = S.profiles.find(x => x.id === b.dataset.ren); askText(T('नाम बदलें', 'Rename'), p.name, n => { p.name = n; save(); renderSettings(); }); });
  $$('[data-del]').forEach(b => b.onclick = () => { const p = S.profiles.find(x => x.id === b.dataset.del); askYes('“' + esc(p.name) + T('” की सारी टिप्पणियाँ, बुकमार्क और प्रगति हट जाएगी।', '”: all notes, bookmarks and progress will be deleted.'), T('हाँ, हटाएँ', 'Yes, delete'), () => { S.profiles = S.profiles.filter(x => x !== p); S.show = S.show.filter(x => x !== p.id); if (S.active === p.id) S.active = S.profiles[0].id; save(); renderSettings(); }); });
  $('#addp').onclick = () => askText(T('नये व्यक्तिका नाम', 'New reader’s name'), '', n => { const p = newProfile(n); S.profiles.push(p); S.show.push(p.id); S.active = p.id; save(); renderSettings(); });
}
function todayStr(){ const d = new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
async function exportFile(){
  const fname = 'scriptures-my-file-' + todayStr() + '.json', text = JSON.stringify(Object.assign({kind: 'manas-personal', exported: new Date().toISOString()}, S), null, 1);
  try { if (window.claude && window.claude.use){ const dl = await window.claude.use('downloads'); if (dl){ try { const r = await dl.save({filename: fname, data: text}); if (r && r.status === 'saved') toast(T('फ़ाइल सेव हुई', 'File saved')); } catch (e) {} return; } } } catch (e) {}
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], {type: 'application/json'})); a.download = fname; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1500); toast(T('फ़ाइल डाउनलोडमें सेव हुई', 'File saved to Downloads'));
}
$('#fileIn').onchange = async e => {
  const f = e.target.files[0]; e.target.value = ''; if (!f) return;
  let X; try { X = JSON.parse(await f.text()); } catch (err) { toast(T('यह फ़ाइल नहीं खुल सकी', 'Could not open this file')); return; }
  if (!X || !X.profiles){ toast(T('यह इस ऐपकी फ़ाइल नहीं है', 'This is not a file from this app')); return; }
  const tmp = S; S = X; migrate(); X = S; S = tmp;
  openSheet('<h2>' + T('फ़ाइल खोलें', 'Open a file') + '</h2><p>' + T('इस फ़ाइलमें: ', 'This file has: ') + '<b>' + X.profiles.map(p => esc(p.name)).join(', ') + '</b></p><div class="menu"><button id="imAdd">' + T('इन्हें इस फ़ोनमें जोड़ें', 'Add them to this phone') + '<br><small class="muted">' + T('यहाँकी आपकी चीज़ें भी रहेंगी', 'Your existing data stays') + '</small></button><button id="imRep">' + T('इस फ़ोनका सब कुछ इस फ़ाइलसे बदलें', 'Replace everything on this phone') + '<br><small class="muted">' + T('सेटिंग्स और प्रगति भी फ़ाइल जैसी हो जाएँगी', 'Settings and progress also come from the file') + '</small></button></div>');
  $('#imAdd').onclick = () => { X.profiles.forEach(p => { const ex = S.profiles.find(q => q.id === p.id); if (ex) Object.assign(ex, p); else S.profiles.push(p); if (!S.show.includes(p.id)) S.show.push(p.id); }); save(); closeSheet(); toast(T('फ़ाइल जोड़ी गई', 'File added')); renderSettings(); };
  $('#imRep').onclick = () => askYes(T('इस फ़ोनका वर्तमान डेटा फ़ाइलके डेटासे बदल जाएगा।', 'Data on this phone will be replaced by the file.'), T('हाँ, बदलें', 'Yes, replace'), () => { S = Object.assign(defaults(), X); delete S.kind; delete S.exported; save(); applyTheme(); closeSheet(); toast(T('फ़ाइल खोली गई', 'File opened')); renderSettings(); });
};
function askText(title, val, cb){ openSheet('<h2>' + esc(title) + '</h2><input id="askT" value="' + esc(val) + '"><div class="acts"><button class="btn" id="askOk">' + T('ठीक है', 'OK') + '</button><button class="btn ghost" id="askNo">' + T('रहने दें', 'Cancel') + '</button></div>'); setTimeout(() => $('#askT').focus(), 250); $('#askOk').onclick = () => { const v = $('#askT').value.trim(); closeSheet(); if (v) cb(v); }; $('#askNo').onclick = () => closeSheet(); }
function askYes(msg, yes, cb){ openSheet('<p style="font-size:17px">' + msg + '</p><div class="acts"><button class="btn" id="askOk">' + esc(yes) + '</button><button class="btn ghost" id="askNo">' + T('रहने दें', 'Cancel') + '</button></div>'); $('#askOk').onclick = () => { closeSheet(); cb(); }; $('#askNo').onclick = () => closeSheet(); }

/* ---------------- vidhi & āratī ---------------- */
let vidTab = 'v';
$$('#vidSeg button').forEach(b => b.onclick = () => { vidTab = b.dataset.v; renderVidhi(); });
$$('#vidLang button').forEach(b => b.onclick = () => { const en = b.dataset.l === 'e'; if (en === (LANG() === 'en')) return; S.settings.layers.e = en; if (!en) S.settings.layers.h = true; save(); applyLang(); renderVidhi(); });
const vW = l => wordsHTML(l);
function renderVidhi(){
  if (!W || !W.vidhi) return;
  $$('#vidSeg button').forEach(b => b.classList.toggle('on', b.dataset.v === vidTab));
  const en = LANG() === 'en'; $$('#vidLang button').forEach(b => b.classList.toggle('on', (b.dataset.l === 'e') === en));
  const V = W.vidhi, L = en ? ' lat' : ''; let h = '';
  if (vidTab === 'aarti') h = '<div class="h' + L + '">' + T('श्रीरामायणजीकी आरती', 'Śrī Rāmāyaṇajī kī Āratī') + '</div>' + V.aarti.map(l => '<div class="v">' + vW(l) + '</div>').join('');
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
$('#vidBody').addEventListener('click', ev => { const w = ev.target.closest('.w'); if (w){ w.classList.add('sel'); wordSheet(w.dataset.w || w.textContent, vidTab === 'v' ? W.vg : null, W.lang); } });

/* ---------------- boot ---------------- */
(async function boot(){
  if (!S.settings.lightDefault){ if (S.settings.theme === 'auto') S.settings.theme = 'light'; S.settings.lightDefault = 1; save(); }
  applyTheme(); applyLang(); applyRecite(); syncLayers(); tickTimer();
  history.replaceState({v: 'library'}, '');
  try { LIB = await getJSON('index'); } catch (e) { $('#loading').textContent = T('डेटा नहीं खुल सका। इंटरनेट जाँचें।', 'Could not load the data. Check the internet connection.'); return; }
  const leafs = []; (function walk(n){ (n || []).forEach(c => c.work ? leafs.push(c.work) : walk(c.children)); })(LIB);
  const start = S.work && leafs.includes(S.work) ? S.work : (leafs.length === 1 ? leafs[0] : null);
  if (start){ await openWork(start, true); viewStack.push('home'); history.pushState({v: 'home'}, ''); show('home', false); }
  else { $('#loading').hidden = true; renderLibrary(); }
  cloudInit();
  if ('serviceWorker' in navigator && location.protocol === 'https:' && !BUNDLE) navigator.serviceWorker.register('sw.js').catch(() => {});
})();
