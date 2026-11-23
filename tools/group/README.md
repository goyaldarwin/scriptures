# The group paath relay

Group paath (`docs/PLAYBOOK.md` §7): people read together in one room, each on their own phone. One phone, the leader's,
plays the recording; every other phone follows it without sound, lighting and turning to the verse being recited. The
leader's phone sends where it is in the recording; this relay passes that on to the phones that joined with its code.

- `worker.js`: a Cloudflare Worker with one Durable Object per 6-digit code. It accepts WebSockets at
  `/s/<code>?role=lead&key=<key>` (the leader; the key reserves the code for its phone) and `/s/<code>?role=follow`,
  passes the leader's `{type: "state"}` messages to the followers, tells the leader how many follow (`{type: "count"}`),
  sends a follower that joins late the last state, tells the followers when the leader's phone goes (`{type: "away"}`, also
  to one that joins meanwhile) and when the leader ends it (`{type: "end"}`).
  WebSocket hibernation: an idle session costs nothing, and `ping` is answered (`pong`) without waking it. A session nobody
  is connected to is cleared after 8 hours. Only the origins in `wrangler.toml` → `ORIGINS` may connect.
- `wrangler.toml`: its name (`scriptures-group`), the Durable Object, and the allowed origins.
- `test.mjs`: its protocol test.
- `simulate.py`: real use, end to end: a leader and six follower phones (each its own browser) and 50 more on raw
  WebSockets, through the real relay, in 13 scenarios (joining by link, code and from another work; late joiners; quick
  pause/play; speed; ⏭; a recording's end; another part, work, recording; Sri Guru Granth Sahib's kirtan; refreshes; a
  dropped, a silent and a restarted relay connection; the leader's phone locking; wrong and taken codes; leaving and
  ending), with every follower's place sampled against the leader's throughout. Run it after any change to Group paath.
- The app reads the relay's address from `apps/app.json` → `group` (`wss://…`, written into `app.js` by `build.py`).
  While that is empty, the app does not offer Group paath.

It runs on Cloudflare's **Workers Free plan** (Durable Objects with SQLite storage are included). A session sends one
small message when the leader plays, pauses, seeks or changes the speed, and one every 5 seconds while it plays; the free
100,000 requests a day (WebSocket messages count 1 in 20) cover hundreds of sessions a day. Measured on `wrangler dev`: 300
phones in one session, every message delivered, the slowest in 39 ms.

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
cd tools/group && npx wrangler dev --port 8787 &     # the relay on this machine (it allows http://localhost:8000)
node tools/group/test.mjs                             # its protocol, message by message
```
The app against it: serve the site (`python3 -m http.server 8000` at the repository root) and open
`http://localhost:8000/` with `window.__GROUP_URL = 'ws://127.0.0.1:8787'` set before the app loads (a test's init
script). `tools/site/ux_test.py` checks Group paath without the relay, with a stand-in that speaks the same messages.
