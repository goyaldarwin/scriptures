const V='s-7b1fa2af9e';const LIB='lib-v1';const CORE=["./", "index.html", "manifest.json", "app/icon.svg", "app/icon-192.png", "app/icon-512.png", "app/apple-touch-icon.png", "app/app.js?v=70f752bee5", "app/style.css?v=1b899aa0e2", "app/fonts.css?v=6ce0da9346", "app/fonts/noto-serif-devanagari-devanagari-400-normal.woff2", "app/fonts/noto-serif-devanagari-devanagari-700-normal.woff2", "app/fonts/literata-latin-400-normal.woff2", "app/fonts/literata-latin-600-normal.woff2", "app/fonts/literata-latin-ext-400-normal.woff2", "app/fonts/literata-latin-400-italic.woff2", "app/fonts/literata-latin-ext-400-italic.woff2", "app/fonts/gentium-tr-italic.woff2", "app/fonts/gentium-tr-regular.woff2", "app/fonts/literata-latin-ext-600-normal.woff2", "app/fonts/noto-serif-gurmukhi-gurmukhi-400-normal.woff2", "app/fonts/noto-serif-gurmukhi-gurmukhi-700-normal.woff2", "app/fonts/tiro-devanagari-sanskrit-devanagari-400-normal.woff2"];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(CORE)));self.skipWaiting();});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V&&k!==LIB).map(k=>caches.delete(k)))));self.clients.claim();});
function netFirst(req,name,ms){
 const net=fetch(req,{cache:'no-cache'}).then(r=>{if(r.ok){const c=r.clone();caches.open(name).then(x=>x.put(req,c));}return r;});
 const timed=ms?Promise.race([net,new Promise((_,rej)=>setTimeout(()=>rej('slow'),ms))]):net;
 return timed.catch(()=>caches.match(req,{ignoreSearch:req.mode==='navigate'}).then(c=>c||(req.mode==='navigate'?caches.match('index.html'):undefined)).then(c=>c||net));
}
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(u.origin!==location.origin||e.request.method!=='GET')return;
 e.respondWith(u.pathname.includes('/library/')?netFirst(e.request,LIB,2500):netFirst(e.request,V,0));});
