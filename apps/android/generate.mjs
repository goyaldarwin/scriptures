// Makes the Android app project (a Trusted Web Activity: the website, full screen, as a Play Store app) from
// apps/app.json and the site's manifest.json, with Google's Bubblewrap library. Used by .github/workflows/android.yml;
// the generated project (apps/android/project/) is not committed — it is made fresh on every build.
//   node apps/android/generate.mjs [--site-url=http://127.0.0.1:8000/]   (default: https://<host><startPath>)
import {TwaManifest, TwaGenerator, ConsoleLog} from '@bubblewrap/core';
import fs from 'fs'; import path from 'path'; import {fileURLToPath} from 'url';
const HERE = path.dirname(fileURLToPath(import.meta.url)), ROOT = path.resolve(HERE, '..', '..');
const app = JSON.parse(fs.readFileSync(path.join(ROOT, 'apps', 'app.json'), 'utf8'));
const arg = process.argv.find(a => a.startsWith('--site-url=')); const site = arg ? arg.split('=')[1] : 'https://' + app.host + app.startPath;
const web = JSON.parse(fs.readFileSync(path.join(ROOT, 'manifest.json'), 'utf8'));
const tm = TwaManifest.fromWebManifestJson(new URL('manifest.json', site), web);
Object.assign(tm, {packageId: app.packageId, host: app.host, name: app.name, launcherName: app.launcherName,
  startUrl: app.startPath, themeColor: tm.themeColor, appVersionName: app.versionName, appVersionCode: app.versionCode,
  fallbackType: 'customtabs', enableNotifications: false, orientation: 'portrait', minSdkVersion: 21,
  signingKey: {path: path.join(HERE, 'upload.keystore'), alias: 'upload'}});
tm.iconUrl = new URL('app/icon-512.png', site).toString(); tm.maskableIconUrl = new URL('app/maskable-512.png', site).toString();
tm.webManifestUrl = new URL('manifest.json', site);
const err = tm.validate(); if (err) { console.error(err); process.exit(1); }
const out = path.join(HERE, 'project'); fs.rmSync(out, {recursive: true, force: true}); fs.mkdirSync(out, {recursive: true});
await tm.saveToFile(path.join(out, 'twa-manifest.json'));
await new TwaGenerator().createTwaProject(out, tm, new ConsoleLog('generate'));
console.log('Android project →', path.relative(ROOT, out), '·', app.packageId, app.versionName, '(' + app.versionCode + ')');
