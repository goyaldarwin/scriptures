# The Android and iPhone apps

**Android first; the iPhone app is parked** until the owner asks (no Apple account needed for now).

One app per tradition, published by the owner's Canadian corporation (organization developer accounts), in every country except mainland China (Apple needs a government ICP number there, and YouTube is blocked). Each work gets its own store page (Apple custom product pages tied to search keywords; Play's full description names every work), and `?w=<work id>` links open the app straight to that work.

## How it works
- **The app shows the website.** New works, corrections and audio timings reach every phone as soon as `main` is published; the app is rebuilt only when its shell changes (name, icon, version).
- **One app per tradition.** The Hindu app, package id `org.craadle.scriptures.hinduism` (permanent), opens `/?app=hinduism`; it also carries the Sukhmani Sahib (the owner's choice). Which shelves an app shows is `library/apps.json` (checked by `build.py`; changing it needs no app update). A Sikh app can follow as `org.craadle.scriptures.sikhism`.
- **Android:** a Trusted Web Activity made by Google's Bubblewrap (`apps/android/generate.mjs`) from `apps/app.json` and the site's `manifest.json`; built by `.github/workflows/android.yml` with its `app` input (a test APK always; the signed `.aab` for Play with `release: true`).
- **App links:** `build.py` writes `.well-known/assetlinks.json` from `apps/app.json` → `sha256` (Play's app-signing key, then the upload key), so the app opens without a browser bar.
- **iPhone (parked):** a Capacitor app that ships the reader inside and loads the library from the website, with offline reading and a daily-reading reminder, so it is more than a website in a frame (App Store guideline 4.2). Needs a Mac build (GitHub macOS runner) and testing on a real iPhone, in particular that YouTube's player works inside the app.

## What is in this repository
| Path | What |
|---|---|
| `apps/app.json` | the company, the site's host, and each app's identity: name, `packageId` (it can never change after the first upload), start path, version, signing fingerprints |
| `apps/android/` | the project generator; `project/` is made on every build and not committed |
| `library/apps.json` | which shelves each app shows, and its public store page (`store`, shared by ☰ › Share the app) |
| `tools/store/make_icons.py` → `tools/store/icons/` | every icon from one design (ॐ on indigo); the web ones are copied into `app/` by build.py |
| `tools/store/screenshots.py` → `tools/store/out/` | captioned store screenshots made from the real app: App Store 6.9" (1320×2868) and Play phone (1080×1920), English and Hindi, plus the Play feature graphic |
| `docs/store/<app>-listing.md` | the store listing text; `tools/store/check_listing.py` checks its lengths |
| `privacy.html` (from `tools/site/privacy.html`) | the privacy policy both stores ask for |
| first-run tour (`tourSteps()` in app.js) | nine steps, each after the first with ‹ Back; ☰ › "Take the tour" |

## The publisher
- 16493041 Canada Inc., D-U-N-S 245128343, email darwin@craadle.org, website craadle.org. Developer name on Play: Craadle; support email support@craadle.org.
- The library's address is `scriptures.craadle.org`: Cloudflare DNS CNAME `scriptures` → goyaldarwin.github.io (DNS only, grey cloud). `build.py` writes the `CNAME` file from `apps/app.json` → `host`; Pages deploys from the branch, so that file sets the custom domain, and goyaldarwin.github.io/scriptures/ redirects to it. Removing the DNS record breaks the site; change the file first.
- **craadle.org** is a one-page company site from the public repo `goyaldarwin/craadle-site` (GitHub Pages from `main`, `CNAME` craadle.org; Cloudflare A records @ → 185.199.108–111.153, DNS only). It is verified in Google Search Console (TXT record: keep it) for Play's website check.
- The public developer profile shows the business name, email and phone (address in some regions); name and address changes go through D&B first, then re-verification in Play Console.
- The Hindu app's Play content rating: IARC Everyone / PEGI 3 / USK 0 / 3+ (contact support@craadle.org); "primarily a news or educational product?" → No.

## The owner's open decision
**Content rights:** decide what launches while permissions are pending (Sant Singh Khalsa's English, the shirdisaibabakripa.org English, the Rāma Rakṣā video's English and the स्तुति चालीसा संग्रह Hindi). The app can hide sources not yet cleared. The Gita Press meanings need no permission letter (the owner).

## Releasing
1. The upload key: `upload.keystore`, kept with its passwords outside the repository and stored as repository secrets `ANDROID_KEYSTORE_B64` (`base64 -w0 upload.keystore`), `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_PASSWORD`. Play App Signing holds the app-signing key.
2. Raise `versionCode` (and `versionName`) in `apps/app.json` for every new upload.
3. Run the `android` workflow with `release: true`; upload the `.aab` to Play (internal testing first).
4. Store listing: icon `tools/store/icons/play-512.png`, feature graphic and screenshots from `tools/store/out/play/`, the text from `docs/store/<app>-listing.md`, privacy policy `https://scriptures.craadle.org/privacy.html`, category Books & Reference.
5. A new signing key (a new upload key, or a new app) needs its SHA-256 fingerprint in `apps/app.json` → `sha256` (Play Console › App integrity), then a build and push, so the app keeps opening without a browser bar.
