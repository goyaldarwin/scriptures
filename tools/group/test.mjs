// Protocol test of the group paath relay (worker.js), against `wrangler dev` with short timers (tools/group/README.md, "Test it here"):
//   npx wrangler dev --port 8787 --var SESSION_IDLE_MS:3000 --var CODE_TTL_MS:6000   (in tools/group/), then: node tools/group/test.mjs
import {execSync} from 'node:child_process';
const status = c => execSync("curl -s -o /dev/null -w '%{http_code}' -H 'Upgrade: websocket' -H 'Origin: https://evil.example' http://127.0.0.1:8787/s/" + c).toString();
const B = 'ws://127.0.0.1:8787/s/';
const open = (u) => new Promise((res, rej) => { const w = new WebSocket(u); w.msgs = []; w.closed = null; w.onmessage = e => w.msgs.push(e.data === 'pong' ? 'pong' : JSON.parse(e.data)); w.onclose = e => w.closed = e.code; w.onopen = () => res(w); w.onerror = rej; });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const ok = (c, m) => { if (!c) { console.log('FAIL', m); process.exitCode = 1; } else console.log('ok  ', m); };
const types = w => w.msgs.map(x => x === 'pong' ? 'pong' : x.type).join(',');
const rnd = () => String(100000 + Math.floor(Math.random() * 899999)), mkKey = () => 'k'.repeat(10) + Math.random().toString(36).slice(2, 12).replace(/[^a-z0-9]/g, 'x');
const code = rnd(), key = mkKey();
const lead = (c, k, m) => open(B + c + '?role=lead&key=' + k + (m ? '&m=' + m : ''));
const play = (L, p) => L.send(JSON.stringify({type: 'state', s: {w: 'manas', on: 1, t: 12.5, p}}));

// a follower who comes before the leader: the code is unknown, then the leader starts and the follower learns the mode
const F0 = await open(B + code + '?role=follow'); await sleep(200);
ok(F0.msgs[0]?.type === 'wait' && F0.msgs[0].none === true, 'a code no leader holds: wait, none');
const L = await lead(code, key, 'apart'); await sleep(250);
ok(L.msgs[0]?.type === 'count' && L.msgs[0].n === 1, 'leader gets the count (1 waiting)');
ok(F0.msgs.at(-1)?.type === 'mode' && F0.msgs.at(-1).m === 'apart', 'the session starts: a waiting follower is told the mode (apart)');
const F1 = await open(B + code + '?role=follow'); await sleep(200);
ok(F1.msgs[0]?.type === 'mode' && F1.msgs[0].m === 'apart' && F1.msgs[1]?.type === 'wait' && F1.msgs[1].none === false, 'a follower joining a session before any state: mode, then wait');
play(L, 1); await sleep(200);
ok(F1.msgs.at(-1).type === 'state' && F1.msgs.at(-1).s.t === 12.5, 'follower gets state');
const F2 = await open(B + code + '?role=follow'); await sleep(200);
ok(F2.msgs[0]?.type === 'mode' && F2.msgs[1]?.type === 'state' && F2.msgs[1].age >= 150 && F2.msgs[1].age < 2000, 'late follower: mode, then the last state with its age (' + F2.msgs[1]?.age + ' ms)');
F2.send(JSON.stringify({type: 'state', s: {w: 'evil'}})); await sleep(200);
ok(F1.msgs.at(-1).s.w === 'manas', 'a follower cannot send state');
F1.send('ping'); await sleep(200); ok(F1.msgs.at(-1) === 'pong', 'ping answered');
const X = await lead(code, 'z'.repeat(20)); await sleep(300);
ok(X.msgs[0]?.type === 'taken', 'another leader key is refused (a code chosen by someone else)');
F2.close(); F0.close(); await sleep(300); ok(L.msgs.at(-1).n === 1, 'count back to 1 after followers leave');
// playing keeps the session going past the idle time
await sleep(3500); ok(!F1.closed && types(F1).indexOf('end') < 0, 'while playing, the session does not end');
L.close(1000); await sleep(300);
ok(F1.msgs.at(-1)?.type === 'away', 'the leader\'s device goes: followers are told');
const F3 = await open(B + code + '?role=follow'); await sleep(200);
ok(F3.msgs[0]?.type === 'mode' && F3.msgs[1]?.type === 'state' && F3.msgs[2]?.type === 'away', 'a follower who joins while the leader is away: mode, the last state, away');
const L2 = await lead(code, key, 'apart'); await sleep(200);
ok(!L2.closed && L2.msgs[0].type === 'count', 'the same leader key reconnects');
// End for today: followers go home, the code stays the leader's
L2.close(4100, 'end'); await sleep(400);
ok(F1.msgs.at(-1).type === 'end' && F1.msgs.at(-1).why === 'end' && F1.closed === 1000, 'End for today reaches followers (why: end)');
const F4 = await open(B + code + '?role=follow'); await sleep(200);
ok(F4.msgs[0]?.type === 'wait' && F4.msgs[0].none === false, 'after End for today, the code is still held: wait, not none');
const Y = await lead(code, 'y'.repeat(20)); await sleep(300);
ok(Y.msgs[0]?.type === 'taken', 'after End for today, no one else can take the code');
// the next day: the same code, a new sitting, no old place
const L3 = await lead(code, key, 'room'); await sleep(300);
ok(F4.msgs.at(-1)?.type === 'mode' && F4.msgs.at(-1).m === 'room', 'the next sitting with the same code: the waiting follower is told (room)');
const F5 = await open(B + code + '?role=follow'); await sleep(200);
ok(F5.msgs[0]?.type === 'mode' && F5.msgs[1]?.type === 'wait', 'a new sitting starts with no old place');
// nothing playing for the idle time: the session ends for everyone, the leader too
play(L3, 0); await sleep(4500);
ok(F5.msgs.at(-1)?.type === 'end' && F5.msgs.at(-1).why === 'idle' && L3.msgs.at(-1)?.type === 'end' && L3.msgs.at(-1).why === 'idle', 'nothing playing for the idle time: everyone is sent home (why: idle)');
// a leader who left without ending: the session ends after the idle time; the waiting follower too
const L4 = await lead(code, key, 'room'); await sleep(200); const F6 = await open(B + code + '?role=follow'); await sleep(200);
L4.close(1000); await sleep(4500);
ok(F6.msgs.at(-1)?.type === 'end' && F6.msgs.at(-1).why === 'idle', 'the leader\'s device gone and not back: the followers are sent home after the idle time');
// End the code: followers go home and the code is free
const L5 = await lead(code, key, 'room'); await sleep(200); const F7 = await open(B + code + '?role=follow'); await sleep(200);
L5.close(4101, 'end code'); await sleep(400);
ok(F7.msgs.at(-1)?.type === 'end' && F7.msgs.at(-1).why === 'code', 'End the code reaches followers (why: code)');
const Z = await lead(code, 'y'.repeat(20)); await sleep(300);
ok(!Z.closed && Z.msgs[0]?.type === 'count', 'after End the code, the code is free for anyone');
Z.close(4101);
// a code no device has been on for the code's time is let go
const c2 = rnd(), k2 = mkKey(); const L6 = await lead(c2, k2); await sleep(200); L6.close(4100); await sleep(7500);
const W = await lead(c2, 'w'.repeat(20)); await sleep(300);
ok(!W.closed && W.msgs[0]?.type === 'count', 'a code with no device on it for the code\'s time is free again');
W.close(4101);
// an old app (no m): a room session
const c3 = rnd(); const L7 = await lead(c3, mkKey()); await sleep(200); const F8 = await open(B + c3 + '?role=follow'); await sleep(200);
ok(F8.msgs[0]?.type === 'mode' && F8.msgs[0].m === 'room', 'a leader that does not say (an older app): room');
L7.close(4101); F3.close(); F4.close();
ok(+status(code) === 403, 'other origins refused');
process.exit();
