// Makes the Android app project (a Trusted Web Activity: the website, full screen, as a Play Store app) from
// apps/app.json and the site's manifest.json, with Google's Bubblewrap library. Used by .github/workflows/android.yml;
// the generated project (apps/android/project/) is not committed — it is made fresh on every build.
//   node apps/android/generate.mjs [--app=hinduism] [--site-url=http://127.0.0.1:8000/]   (default: https://<host>/)
import {TwaManifest, TwaGenerator, ConsoleLog} from '@bubblewrap/core';
import {createRequire} from 'module';
import fs from 'fs'; import path from 'path'; import {fileURLToPath} from 'url';
const HERE = path.dirname(fileURLToPath(import.meta.url)), ROOT = path.resolve(HERE, '..', '..');
const {ShortcutInfo} = createRequire(import.meta.url)('@bubblewrap/core/dist/lib/ShortcutInfo.js');
const cfg = JSON.parse(fs.readFileSync(path.join(ROOT, 'apps', 'app.json'), 'utf8'));
const opt = k => { const a = process.argv.find(x => x.startsWith('--' + k + '=')); return a ? a.slice(k.length + 3) : null; };
const appId = opt('app') || 'hinduism', app = Object.assign({host: cfg.host}, cfg.apps[appId]);
if (!cfg.apps[appId]) { console.error('no app ' + appId + ' in apps/app.json'); process.exit(1); }
const site = opt('site-url') || 'https://' + app.host + '/';
// the app's shortcuts: its first four works, opened inside the app (?app=<id>&w=<work>)
const shelves = JSON.parse(fs.readFileSync(path.join(ROOT, 'library', 'apps.json'), 'utf8'))[appId].shelves;
const works = []; (function walk(ns, at){ for (const n of ns){ const p = at.concat(n.id).join('/');
  const inside = shelves.some(s => p === s || p.startsWith(s + '/')), above = shelves.some(s => s.startsWith(p + '/'));
  if (n.work && inside) works.push(n); else if (!n.work && (inside || above)) walk(n.children || [], at.concat(n.id)); } })(JSON.parse(fs.readFileSync(path.join(ROOT, 'library', 'index.json'), 'utf8')), []);
const web = JSON.parse(fs.readFileSync(path.join(ROOT, 'manifest.json'), 'utf8'));
const tm = TwaManifest.fromWebManifestJson(new URL('manifest.json', site), web);
Object.assign(tm, {packageId: app.packageId, host: app.host, name: app.name, launcherName: app.launcherName,
  startUrl: app.startPath, appVersionName: app.versionName, appVersionCode: app.versionCode,
  fallbackType: 'customtabs', enableNotifications: false, orientation: 'portrait', minSdkVersion: 24,
  signingKey: {path: path.join(HERE, 'upload.keystore'), alias: 'upload'}});
tm.iconUrl = new URL('app/icon-512.png', site).toString(); tm.maskableIconUrl = new URL('app/maskable-512.png', site).toString();
tm.webManifestUrl = new URL('manifest.json', site);
tm.shortcuts = works.slice(0, 4).map(w => new ShortcutInfo(w.title.en, w.title.en.slice(0, 12), app.startPath + '&w=' + w.work, new URL('app/icon-192.png', site).toString()));
const err = tm.validate(); if (err) { console.error(err); process.exit(1); }
const out = path.join(HERE, 'project'); fs.rmSync(out, {recursive: true, force: true}); fs.mkdirSync(out, {recursive: true});
await tm.saveToFile(path.join(out, 'twa-manifest.json'));
await new TwaGenerator().createTwaProject(out, tm, new ConsoleLog('generate'));
console.log('Android project →', path.relative(ROOT, out), '·', appId, app.packageId, app.versionName, '(' + app.versionCode + ')');
