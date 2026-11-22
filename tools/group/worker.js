// Group paath relay (docs/PLAYBOOK.md §7, "Group paath"; tools/group/README.md).
//
// One phone leads: it plays the recording and sends where it is ("state": the work, the recording, the track, the time,
// playing or paused, the speed). Every other phone in the session follows silently: it lights the verse from that state
// and the verse times it already has. This Worker only passes the leader's state on; it keeps nothing about a reader.
//
//   wss://<host>/s/<6-digit code>?role=lead&key=<leader key>   the leader (the key reserves the code for its phone)
//   wss://<host>/s/<6-digit code>?role=follow                  a follower
//
// One Durable Object per code. WebSocket hibernation: an idle session costs nothing, and "ping" is answered without waking it.
// Messages: leader → {type: "state", s: {...}}; relay → follower {type: "state", s}; relay → leader {type: "count", n}.
// Refusals: {type: "taken"} then close 4009 (the code is another leader's), {type: "bad"} then close 4000 (a bad key).
import {DurableObject} from 'cloudflare:workers';

const MAX_MSG = 2048;              // a state is about 150 bytes
const IDLE_MS = 8 * 3600 * 1000;   // a session nobody is connected to is cleared after this

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
    this.ctx.setWebSocketAutoResponse(new WebSocketRequestResponsePair('ping', 'pong'));   // keep-alive and round-trip time, never waking the object
  }
  async fetch(req){
    const url = new URL(req.url), role = url.searchParams.get('role'), key = url.searchParams.get('key') || '';
    const [client, server] = Object.values(new WebSocketPair());
    if (role === 'lead'){
      const owner = await this.ctx.storage.get('key');
      this.ctx.acceptWebSocket(server, ['lead']);
      if (!/^[A-Za-z0-9]{16,64}$/.test(key)){ server.send(JSON.stringify({type: 'bad'})); server.close(4000, 'bad key'); return new Response(null, {status: 101, webSocket: client}); }
      if (owner && owner !== key){ server.send(JSON.stringify({type: 'taken'})); server.close(4009, 'taken'); return new Response(null, {status: 101, webSocket: client}); }
      if (!owner) await this.ctx.storage.put('key', key);
      this.ctx.getWebSockets('lead').forEach(w => { if (w !== server) try { w.close(4001, 'replaced'); } catch (e) {} });   // the same phone again (a refresh)
      server.serializeAttachment({lead: true});
      server.send(JSON.stringify({type: 'count', n: this.followers().length}));
    } else if (role === 'follow'){
      this.ctx.acceptWebSocket(server, ['follow']);
      const s = await this.lastState();
      if (s) server.send(JSON.stringify({type: 'state', s}));
      else server.send(JSON.stringify({type: 'wait'}));
      this.count();
    } else return new Response('role?\n', {status: 400});
    await this.ctx.storage.setAlarm(Date.now() + IDLE_MS);
    return new Response(null, {status: 101, webSocket: client});
  }
  followers(){ return this.ctx.getWebSockets('follow'); }
  // the leader's last state: on its socket while it is connected (no storage write per message), else the copy kept when it left
  lastState(){
    for (const w of this.ctx.getWebSockets('lead')){ const a = w.deserializeAttachment(); if (a && a.s) return Promise.resolve(a.s); }
    return this.ctx.storage.get('state');
  }
  count(except){ const n = this.followers().filter(w => w !== except).length; this.ctx.getWebSockets('lead').forEach(w => { try { w.send(JSON.stringify({type: 'count', n})); } catch (e) {} }); }
  async webSocketMessage(ws, msg){
    if (typeof msg !== 'string' || msg.length > MAX_MSG) return;
    const a = ws.deserializeAttachment(); if (!a || !a.lead) return;   // only the leader speaks
    let d; try { d = JSON.parse(msg); } catch (e) { return; }
    if (!d || d.type !== 'state' || typeof d.s !== 'object') return;
    ws.serializeAttachment({lead: true, s: d.s});
    const out = JSON.stringify({type: 'state', s: d.s});
    this.followers().forEach(w => { try { w.send(out); } catch (e) {} });
  }
  async webSocketClose(ws, code){
    const a = ws.deserializeAttachment();
    if (a && a.lead && a.s) await this.ctx.storage.put('state', a.s);   // a follower joining while the leader is away still opens the reading
    if (a && a.lead && code === 4100){ await this.end(); return; }      // the leader ended the session
    if (!a || !a.lead) this.count(ws);
    try { ws.close(); } catch (e) {}
    await this.ctx.storage.setAlarm(Date.now() + IDLE_MS);
  }
  async webSocketError(ws){ await this.webSocketClose(ws, 1006); }
  async end(){ const out = JSON.stringify({type: 'end'}); this.followers().forEach(w => { try { w.send(out); w.close(1000, 'ended'); } catch (e) {} }); await this.ctx.storage.deleteAll(); }
  async alarm(){
    if (this.ctx.getWebSockets().length){ await this.ctx.storage.setAlarm(Date.now() + IDLE_MS); return; }
    await this.ctx.storage.deleteAll();
  }
}
