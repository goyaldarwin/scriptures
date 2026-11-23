# The group paath relay

Group paath (`docs/PLAYBOOK.md` §7): people read together, each on their own device. One device, the leader's, plays the
recording; every other device follows it, lighting and turning to the verse being recited. Where the leader says some are
elsewhere, a follower may also play the recording itself, in step. The leader's device sends where it is in the recording;
this relay passes that on to the devices that joined with its code.

**A code and a sitting are two things.** The code is held for the leader's device (its random key) until the leader ends the
code or no device has been on it for 15 days, so a paath read every day keeps one link and one QR code. A sitting starts when
the leader connects and ends when the leader ends it for today, or after an hour with nothing playing; every follower is
then sent home. The relay stores per code only the key, the sitting's mode and the leader's last state (deleted when the
sitting ends), and when a device was last on it. There are no queues.

- `worker.js`: a Cloudflare Worker with one Durable Object per 6-digit code. It accepts WebSockets at
  `/s/<code>?role=lead&key=<key>&m=<room|apart>` (the leader; the key holds the code for its device; `m` the sitting's mode,
  `room` when absent) and `/s/<code>?role=follow`. It passes the leader's `{type: "state"}` messages to the followers, tells a
  follower the sitting's mode (`{type: "mode", m}`: on joining, and when a sitting starts), tells the leader how many follow
  (`{type: "count"}`), sends a follower that joins late the last state, tells the followers when the leader's device goes
  (`{type: "away"}`, also to one that joins meanwhile), and sends everyone home when the sitting ends (`{type: "end", why}`:
  `end` the leader closed with 4100, End for today; `code` the leader closed with 4101, End the code; `idle` an hour with
  nothing playing, the leader too). A follower on a code with no sitting gets `{type: "wait", none}` (`none`: no leader holds
  the code). Its alarm ends an idle sitting and lets an unused code go. WebSocket hibernation: an idle session costs nothing,
  and `ping` is answered (`pong`) without waking it. Only the origins in `wrangler.toml` → `ORIGINS` may connect.
- `wrangler.toml`: its name (`scriptures-group`), the Durable Object, and the allowed origins. The times can be set for a
  test (`SESSION_IDLE_MS`, default an hour; `CODE_TTL_MS`, default 15 days).
- `test.mjs`: its protocol test (run against `wrangler dev` with short times, below).
- `simulate.py`: real use, end to end: a leader and six follower devices (each its own browser) and 50 more on raw
  WebSockets, through the real relay, in 14 scenarios (joining by link, code and from another work; late joiners; quick
  pause/play; speed; ⏭; a recording's end; another part, work, recording; Sri Guru Granth Sahib's kirtan; refreshes; a
  dropped, a silent and a restarted relay connection; the leader's device locking; wrong and taken codes; leaving and
  ending; the next sitting on the same code with some elsewhere, a follower playing in step), with every follower's place
  sampled against the leader's throughout. Run it after any change to Group paath.
- The app reads the relay's address from `apps/app.json` → `group` (`wss://…`, written into `app.js` by `build.py`).
  While that is empty, the app does not offer Group paath.

It runs on Cloudflare's **Workers Free plan** (Durable Objects with SQLite storage are included). A session sends one
small message when the leader plays, pauses, seeks or changes the speed, and one every 5 seconds while it plays; the free
100,000 requests a day (WebSocket messages count 1 in 20) cover hundreds of sessions a day. Measured on `wrangler dev`: 300
devices in one session, every message delivered, the slowest in 39 ms.

## Where it runs

| What | Where |
|---|---|
| Cloudflare account | Darwingoyal007@gmail.com's Account, **Workers Free plan** (no charge: past a free daily limit, requests fail until 00:00 UTC; nothing is billed) |
| The Worker | **scriptures-group** (Workers & Pages), its Durable Object class `Session` (SQLite) |
| Its addresses | **`wss://group.craadle.org`** (the custom domain, Production; the app uses it: `apps/app.json` → `group`), and `https://scriptures-group.darwingoyal007.workers.dev` (Cloudflare's own; Preview addresses off) |
| The check | https://group.craadle.org/ shows "Scriptures group paath relay" |
| The API token | **scriptures-group-recitation-relay** (Account API tokens; no expiry): the entire account → Workers Scripts Edit, Account Settings Read; craadle.org → Workers Routes Edit |
| GitHub secrets | `CLOUDFLARE_API_TOKEN` (that token) and `CLOUDFLARE_ACCOUNT_ID` (Settings → Secrets and variables → Actions) |
| The deploy | the `group` workflow (`.github/workflows/group.yml`): by hand (Actions → group → Run workflow), and by itself when `worker.js`, `wrangler.toml` or the workflow changes on `main` |
| Who may connect | the origins in `wrangler.toml` → `ORIGINS` (the site, and `http://localhost:8000` for tests) |

To change the relay: edit `worker.js`, run `test.mjs` and `simulate.py`, merge to `main` (it deploys). To replace the token:
make a new one as in step 1 below and paste it into the `CLOUDFLARE_API_TOKEN` secret. To switch Group paath off in the app:
empty `apps/app.json` → `group` and publish (the relay can stay).

## Deploy it (the owner, once)

The `group` workflow of this repository deploys it with your Cloudflare token; nothing needs installing on a computer.

1. **Create an API token.** Cloudflare dashboard → **Manage account** → **Account API tokens** → **Create a token**, named
   `scriptures-group-recitation-relay`, with two permission policies:
   - scope **the entire account**: **Workers Scripts → Edit** and **Account Settings → Read** (these must be on the
     account: in a domain's policy the deploy fails with "No access to the specified resource");
   - scope **Specified Domains → craadle.org**: **Workers Routes → Edit**.
   **Continue to summary** (it lists Workers Scripts and Account Settings under "Entire … account") → **Create token**,
   and copy the token (it is shown once).
2. **Find your Account ID.** Dashboard → **Workers & Pages** (left menu). The Account ID is on the right of that page
   (or under any domain's Overview). If Cloudflare asks you to choose a `workers.dev` subdomain the first time, choose any.
3. **Add both to GitHub.** github.com/goyaldarwin/scriptures → **Settings** → **Secrets and variables** → **Actions** →
   **New repository secret**, twice: `CLOUDFLARE_API_TOKEN` (the token) and `CLOUDFLARE_ACCOUNT_ID` (the ID).
4. **Run the workflow.** **Actions** → **group** → **Run workflow** (branch `main`). In about a minute the log ends with
   the Worker's address, `https://scriptures-group.darwingoyal007.workers.dev`.
5. **Give it the library's own address.** Dashboard → **Workers & Pages** → **scriptures-group** → **Domains** →
   **+ Add Domain** → subdomain `group` (.craadle.org), enable for Production → **Add domain** (not the "Connect your
   domain" page, which adds a whole new site). Cloudflare makes the DNS record and the certificate itself.
6. **Check it.** Open https://group.craadle.org/ in a browser: it says "Scriptures group paath relay".
7. **Turn it on in the app.** Set `apps/app.json` → `"group": "wss://group.craadle.org"`, build and publish
   (or ask a session to). ☰ › Group paath then appears for everyone.

Later changes to `worker.js` or `wrangler.toml` deploy by themselves when they reach `main`.

## Test it here

```bash
cd tools/group && npx wrangler dev --port 8787 --var SESSION_IDLE_MS:3000 --var CODE_TTL_MS:6000 &   # short times
node tools/group/test.mjs                             # its protocol, message by message
```
The app against it: serve the site (`python3 -m http.server 8000` at the repository root) and open
`http://localhost:8000/` with `window.__GROUP_URL = 'ws://127.0.0.1:8787'` set before the app loads (a test's init
script). `tools/site/ux_test.py` checks Group paath without the relay, with a stand-in that speaks the same messages.
