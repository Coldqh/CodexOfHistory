/* Codex of History v3.1.1 — GitHub Pages service worker */
const VERSION='codex-v3.1.1';
const APP_CACHE=`${VERSION}-app`;
const IMAGE_CACHE=`${VERSION}-images`;
const CORE=['./','./index.html','./styles.css','./manifest.webmanifest','./data/content-manifest.json','./js/bootstrap.js','./assets/ui/codex-mark.svg','./assets/ui/fallback-card.svg','./assets/packs/civilizations-pack.svg','./assets/packs/babylon-pack.svg','./data/image_manifest.json','./js/features/v3-1-1-hotfix.js'];
self.addEventListener('install',event=>{
  event.waitUntil(caches.open(APP_CACHE).then(cache=>cache.addAll(CORE)).then(()=>self.skipWaiting()));
});
self.addEventListener('activate',event=>{
  event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('codex-')&&!k.startsWith(VERSION)).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));
});
async function networkFirst(req){
  const cache=await caches.open(APP_CACHE);
  try{const response=await fetch(req);if(response&&response.ok)cache.put(req,response.clone());return response;}
  catch(_){return (await cache.match(req))||(req.mode==='navigate'?await cache.match('./index.html'):Response.error());}
}
async function cacheFirstImage(req){
  const cache=await caches.open(IMAGE_CACHE),hit=await cache.match(req);if(hit)return hit;
  try{const response=await fetch(req);if(response&&(response.ok||response.type==='opaque'))cache.put(req,response.clone());return response;}
  catch(_){return (await caches.match('./assets/ui/fallback-card.svg'))||Response.error();}
}
async function cacheFirstExternal(req){
  const cache=await caches.open(APP_CACHE),hit=await cache.match(req);if(hit)return hit;
  try{const response=await fetch(req);if(response&&(response.ok||response.type==='opaque'))cache.put(req,response.clone());return response;}
  catch(_){return Response.error();}
}
self.addEventListener('fetch',event=>{
  const req=event.request;if(req.method!=='GET')return;const url=new URL(req.url);
  if(req.destination==='image'){event.respondWith(cacheFirstImage(req));return;}
  if(url.origin===self.location.origin){event.respondWith(networkFirst(req));return;}
  if(url.hostname==='tile.openstreetmap.org'){event.respondWith(cacheFirstImage(req));return;}
  if(url.hostname==='unpkg.com'){event.respondWith(cacheFirstExternal(req));}
});
