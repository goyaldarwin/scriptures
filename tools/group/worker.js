// Group paath relay (docs/PLAYBOOK.md §7, "Group paath"; tools/group/README.md).
//
// One device leads: it plays the recording and sends where it is ("state": the work, the recording, the track, the time,
// playing or paused, the speed). Every other device in the session follows: it lights the verse from that state and the
// verse times it already has, and, where the leader said some are elsewhere and it chose to, plays the recording itself in
// step. This Worker only passes the leader's state on; it keeps nothing about a reader.
//
//   wss://<host>/s/<6-digit code>?role=lead&key=<leader key>&m=<room|apart>   the leader (the key holds the code for its device)
//   wss://<host>/s/<6-digit code>?role=follow                                 a follower
//
// A code and a session are two things (the owner: a paath read 3 hours a day for days keeps one link and one QR code):
// - the code is the leader's, kept for its key until 15 days pass with no device on it, or the leader ends the code;
// - a session is today's sitting: it starts when the leader connects, and ends when the leader ends it for today, or
//   after an hour with nothing playing (a leader who forgot, a device left open); every follower is then sent home.
//
// One Durable Object per code. WebSocket hibernation: an idle session costs nothing, and "ping" is answered without waking it.
// Messages: leader → {type: "state", s: {...}}; relay → follower {type: "mode", m} (the session's: "room", only the leader's
// device plays; "apart", a follower may play too), {type: "state", s, age} (age: ms since the leader sent it, for a device that
// joins later), {type: "wait", none} (no session now; none: no leader holds this code), {type: "away"} while the leader's
// device is not connected, {type: "end", why} (why: "end" the leader ended today's session, "code" the leader ended the code,
// "idle" an hour with nothing playing); relay → leader {type: "count", n}, {type: "end", why: "idle"}.
// Closing codes from the leader: 4100 end today's session, 4101 end the code.
// Refusals: {type: "taken"} then close 4009 (the code is another leader's), {type: "bad"} then close 4000 (a bad key).
import {DurableObject} from 'cloudflare:workers';

const MAX_MSG = 2048;   // a state is about 160 bytes

export default {
  async fetch(req, env){
    const url = new URL(req.url), m = url.pathname.match(/^\/s\/(\d{6})$/);
    if (url.pathname === '/') return new Response('Scriptures group paath relay\n');
    if (!m) return new Response('Not found\n', {status: 404});
    const origin = req.headers.get('Origin');
    const allowed = (env.ORIGINS || '').split(',').map(s => s.trim()).filter(Boolean);
    if (origin && allowed.length && !allowed.includes(origin)) return new Response('Forbidden\n', {status: 403});
    if (req.headers.get('Upgrade') !== 'websocket') return new Response('Expected a WebSocket\n', {status: 426});
    return env.SESSION.get(env.SESSION.idFromName(m[1])).fetch(req);
  }
};

export class Session extends DurableObject {
  constructor(ctx, env){
    super(ctx, env);
    this.IDLE = +env.SESSION_IDLE_MS || 3600 * 1000;       // a session with nothing playing this long ends (wrangler.toml; tests shorten it)
    this.TTL = +env.CODE_TTL_MS || 15 * 24 * 3600 * 1000;   // a code no device has been on this long is let go
    this.ctx.setWebSocketAutoResponse(new WebSocketRequestResponsePair('ping', 'pong'));   // keep-alive and round-trip time, never waking the object
  }
  async fetch(req){
    const url = new URL(req.url), role = url.searchParams.get('role'), key = url.searchParams.get('key') || '';
    const [client, server] = Object.values(new WebSocketPair()), st = this.ctx.storage, now = Date.now();
    if (role === 'lead'){
      const owner = await st.get('key');
      this.ctx.acceptWebSocket(server, ['lead']);
      if (!/^[A-Za-z0-9]{16,64}$/.test(key)){ server.send(JSON.stringify({type: 'bad'})); server.close(4000, 'bad key'); return new Response(null, {status: 101, webSocket: client}); }
      if (owner && owner !== key){ server.send(JSON.stringify({type: 'taken'})); server.close(4009, 'taken'); return new Response(null, {status: 101, webSocket: client}); }
      const m = url.searchParams.get('m') === 'apart' ? 'apart' : 'room';
      const was = await st.get(['live', 'mode']);
      await st.put({key, live: true, mode: m, used: now}); await st.delete(was.get('live') ? ['idle'] : ['idle', 'state']);   // a new sitting starts with no old place
      this.ctx.getWebSockets('lead').forEach(w => { if (w !== server) try { w.close(4001, 'replaced'); } catch (e) {} });   // the same device again (a refresh)
      server.serializeAttachment({lead: true, idle: now});   // nothing playing yet
      server.send(JSON.stringify({type: 'count', n: this.followers().length}));
      if (!was.get('live') || was.get('mode') !== m) this.toFollowers({type: 'mode', m});   // a session starts: the waiting followers learn how to listen
      await this.schedule(now + this.IDLE);
    } else if (role === 'follow'){
      this.ctx.acceptWebSocket(server, ['follow']);
      const v = await st.get(['key', 'live', 'mode']), lead = this.ctx.getWebSockets('lead').length;
      if (v.get('live')){
        server.send(JSON.stringify({type: 'mode', m: v.get('mode') || 'room'}));
        const last = await this.lastState();
        if (last) server.send(JSON.stringify({type: 'state', s: last.s, age: Date.now() - last.at}));   // how old it is, as it is sent: the follower allows for it
        else server.send(JSON.stringify({type: 'wait', none: false}));
        if (!lead) server.send(JSON.stringify({type: 'away'}));   // the leader's device is not here now
      } else server.send(JSON.stringify({type: 'wait', none: !v.get('key')}));   // none: no leader holds this code (a mistyped code)
      await st.put('used', now);
      if (!lead && !(await st.get('idle'))) await st.put('idle', now);   // waiting with no leader: the hour counts from now
      this.count();
      if (!(await st.getAlarm())) await this.schedule(now + this.IDLE);
    } else return new Response('role?\n', {status: 400});
    return new Response(null, {status: 101, webSocket: client});
  }
  followers(){ return this.ctx.getWebSockets('follow'); }
  toFollowers(d){ const out = JSON.stringify(d); this.followers().forEach(w => { try { w.send(out); } catch (e) {} }); }
  async schedule(t){ await this.ctx.storage.setAlarm(t); }
  // the leader's last state and when it came ({s, at}): on its socket while it is connected (no storage write per message), else
  // the copy kept when it left
  async lastState(){
    for (const w of this.ctx.getWebSockets('lead')){ const a = w.deserializeAttachment(); if (a && a.s) return {s: a.s, at: a.at}; }
    return (await this.ctx.storage.get('state')) || null;
  }
  count(except){ const n = this.followers().filter(w => w !== except).length; this.ctx.getWebSockets('lead').forEach(w => { try { w.send(JSON.stringify({type: 'count', n})); } catch (e) {} }); }
  async webSocketMessage(ws, msg){
    if (typeof msg !== 'string' || msg.length > MAX_MSG) return;
    const a = ws.deserializeAttachment(); if (!a || !a.lead) return;   // only the leader speaks
    let d; try { d = JSON.parse(msg); } catch (e) { return; }
    if (!d || d.type !== 'state' || typeof d.s !== 'object' || !d.s) return;
    const now = Date.now(), playing = !!(d.s.on && d.s.p), idle = playing ? null : (a.idle || now);
    ws.serializeAttachment({lead: true, s: d.s, at: now, idle});
    if (!playing && !a.idle) await this.schedule(now + this.IDLE);   // it stopped playing: the hour starts now
    this.toFollowers({type: 'state', s: d.s});
  }
  async webSocketClose(ws, code){
    const a = ws.deserializeAttachment(), st = this.ctx.storage, now = Date.now();
    try { ws.close(); } catch (e) {}
    if (a && a.lead && code === 4100){ await this.endSession('end'); return; }   // the leader ended today's session
    if (a && a.lead && code === 4101){ await this.endSession('code'); await st.deleteAll(); return; }   // the leader ended the code
    if (a && a.lead && !this.ctx.getWebSockets('lead').some(w => w !== ws)){   // the leader's device has gone (not replaced by itself)
      if (await st.get('live')){
        if (a.s) await st.put('state', {s: a.s, at: a.at});   // a follower joining meanwhile still opens the reading
        const idle = a.idle || now; await st.put('idle', idle);   // the hour with nothing playing counts from when it stopped
        this.toFollowers({type: 'away'}); await this.schedule(idle + this.IDLE);
      }
    }
    if (!a || !a.lead) this.count(ws);
    await st.put('used', now);
  }
  async webSocketError(ws){ await this.webSocketClose(ws, 1006); }
  // today's session ends: every follower (and the leader, when the relay ends it) is sent home; the code stays the leader's
  async endSession(why){
    const out = JSON.stringify({type: 'end', why});
    this.ctx.getWebSockets().forEach(w => { try { w.send(out); w.close(1000, 'ended'); } catch (e) {} });
    const st = this.ctx.storage; await st.delete(['live', 'mode', 'state', 'idle']); await st.put('used', Date.now());
    await this.schedule(Date.now() + this.TTL);
  }
  async alarm(){
    const st = this.ctx.storage, now = Date.now(), socks = this.ctx.getWebSockets();
    if ((await st.get('live')) || socks.length){
      const lead = this.ctx.getWebSockets('lead').map(w => w.deserializeAttachment()).find(x => x && x.lead);
      let idle = lead ? lead.idle : await st.get('idle');
      if (!lead && !idle){ idle = now; await st.put('idle', now); }
      if (idle == null){ await this.schedule(now + this.IDLE); return; }   // playing
      if (now - idle >= this.IDLE){ await this.endSession('idle'); return; }
      await this.schedule(idle + this.IDLE); return;
    }
    const used = (await st.get('used')) || 0;
    if (await st.get('key') && now - used < this.TTL){ await this.schedule(used + this.TTL); return; }
    await st.deleteAll();   // no device for 15 days: the code is free again
  }
}
