# The Android and iPhone apps

**Decision (owner, 2026-10-19): Android first; the iPhone app is parked** until the owner asks (no Apple account needed for now).

**Decision (owner, 2026-10-18):** one app for the whole library, published by the owner's Canadian corporation (organization developer accounts), in every country except mainland China (Apple needs a government ICP number there, and YouTube is blocked). Each work gets its own store page (Apple custom product pages tied to search keywords; Play's full description names every work), and `?w=<work id>` links open the app straight to that work.

## How it works
- **The app shows the website.** New works, corrections and audio timings reach every phone as soon as `main` is published; the app is rebuilt only when its shell changes (name, icon, version).
- **Android:** a Trusted Web Activity made by Google's Bubblewrap (`apps/android/generate.mjs`) from `apps/app.json` and the site's `manifest.json`; built by `.github/workflows/android.yml` (a test APK always; the signed `.aab` for Play with `release: true`).
- **iPhone (parked, 2026-10-19):** a Capacitor app that ships the reader inside and loads the library from the website, with offline reading and a daily-reading reminder, so it is more than a website in a frame (App Store guideline 4.2). Needs a Mac build (GitHub macOS runner) and testing on a real iPhone — in particular that YouTube's player works inside the app.

## What is in this repository
| Path | What |
|---|---|
| `apps/app.json` | the app's identity: name, `packageId` (**fill in before the first upload; it can never change**), host, start path, version |
| `apps/android/` | the project generator; `project/` is made on every build and not committed |
| `tools/store/make_icons.py` → `tools/store/icons/` | every icon from one design (ॐ on indigo); the web ones are copied into `app/` by build.py |
| `tools/store/screenshots.py` → `tools/store/out/` | captioned store screenshots made from the real app: App Store 6.9" (1320×2868) and Play phone (1080×1920), English and Hindi, plus the Play feature graphic |
| `privacy.html` (from `tools/site/privacy.html`) | the privacy policy both stores ask for |
| first-run tour (`tourSteps()` in app.js) | six steps, shown once; Settings › Help › "Show the tour again" |

## Settled (2026-10-19)
- Publisher: 16493041 Canada Inc., D-U-N-S 245128343, email darwin@craadle.org, website craadle.org.
- **One app per tradition** (owner, 2026-10-19): the Hindu app first, package id `org.craadle.scriptures.hinduism` (permanent), opening `/?app=hinduism`; it also carries the Sukhmani Sahib (owner's choice). Which shelves an app shows is `library/apps.json` (checked by build.py; changing it needs no app update). A Sikh app can follow as `org.craadle.scriptures.sikhism`. `apps/app.json` holds each app's identity; build with the `android` workflow's `app` input.
- library address `scriptures.craadle.org` — live since 2026-10-19: Cloudflare DNS CNAME `scriptures` → goyaldarwin.github.io (DNS only, grey cloud); `build.py` writes the `CNAME` file from apps/app.json's host (Pages deploys from the branch, so that file sets the custom domain; the old goyaldarwin.github.io/scriptures/ link redirects). Removing the record breaks the site — change the file first.
- **craadle.org** is a one-page company site from the public repo `goyaldarwin/craadle-site` (GitHub Pages from `main`, `CNAME` craadle.org; Cloudflare A records @ → 185.199.108–111.153, DNS only). Verified in Google Search Console (TXT record — keep it) for Play's website check. Developer name on Play: Craadle; support email support@craadle.org.
- The public developer profile shows the business name, email and phone (address in some regions); name/address changes go through D&B first, then re-verification in Play Console.

## The owner's steps
1. **D-U-N-S number** for the corporation (free from Dun & Bradstreet; Apple looks it up during enrolment).
2. **A domain and email for the app** (e.g. the corporation's site). Point the website at it (GitHub Pages custom domain): Android verifies the app against `https://<domain>/.well-known/assetlinks.json`, which must sit at the domain's root — not possible on `goyaldarwin.github.io/scriptures/`.
3. **Google Play Console** — organization account ($25 once). (Apple Developer Program, $99/year, only when the iPhone app is taken up.)
4. Choose the **app name** and the **package id** (reverse domain, e.g. `ca.<company>.scriptures`); put them in `apps/app.json`.
5. **Content rights:** decide what launches while permissions are pending (Gita Press meanings, Sant Singh Khalsa's English, the shirdisaibabakripa.org English, the Ram Raksha meanings). The app can hide sources not yet cleared.

## Releasing (once the steps above are done)
1. Make the upload key once: `keytool -genkeypair -v -keystore upload.keystore -alias upload -keyalg RSA -keysize 2048 -validity 10000`; keep the file and passwords safe outside the repository; store them as repository secrets `ANDROID_KEYSTORE_B64` (`base64 -w0 upload.keystore`), `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_PASSWORD`.
2. Run the `android` workflow with `release: true`; upload the `.aab` to Play (internal testing first). Turn on Play App Signing.
3. Publish `/.well-known/assetlinks.json` on the domain with the SHA-256 fingerprints of Play's app-signing key and the upload key (Play Console › App integrity), so the app opens without a browser bar.
4. Store listing: icon `tools/store/icons/play-512.png`, feature graphic and screenshots from `tools/store/out/play/`, privacy policy `https://<domain>/privacy.html`, category Books & Reference, content rating questionnaire (no user content, no ads).
5. Raise `versionCode` in `apps/app.json` for every new upload.
