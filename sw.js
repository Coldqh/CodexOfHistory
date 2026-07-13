/* Codex of History v3.2.0 — bounded GitHub Pages service worker */
const VERSION='codex-v3.2.0';
const APP_CACHE=`${VERSION}-app`;
const IMAGE_CACHE=`${VERSION}-images`;
const TILE_CACHE=`${VERSION}-tiles`;
const IMAGE_LIMIT=48;
const TILE_LIMIT=72;
const CORE=[
  './','./index.html','./styles.css','./manifest.webmanifest','./data/content-manifest.json',
  './js/bootstrap.js','./assets/ui/codex-mark.svg','./assets/ui/codex-icon-192.png',
  './assets/ui/codex-icon-512.png','./assets/ui/fallback-card.svg',
  './assets/packs/civilizations-pack.svg','./assets/packs/babylon-pack.svg','./assets/packs/egypt-bronze-pack.svg',
  './data/image_manifest.json','./data/image_queries.json',
  './js/features/v3-2-egypt-middle-new.js','./js/features/v3-1-1-hotfix.js','./js/features/v3-1-3-visual-semantics.js'
];

self.addEventListener('install',event=>{
  event.waitUntil((async()=>{
    const cache=await caches.open(APP_CACHE);
    await Promise.allSettled(CORE.map(url=>cache.add(url)));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate',event=>{
  event.waitUntil((async()=>{
    const keys=await caches.keys();
    await Promise.all(keys.filter(key=>key.startsWith('codex-')&&!key.startsWith(VERSION)).map(key=>caches.delete(key)));
    await self.clients.claim();
  })());
});

async function trim(cacheName,limit){
  const cache=await caches.open(cacheName);
  const keys=await cache.keys();
  if(keys.length<=limit)return;
  await Promise.all(keys.slice(0,keys.length-limit).map(key=>cache.delete(key)));
}

async function networkFirst(req){
  const cache=await caches.open(APP_CACHE);
  try{
    const response=await fetch(req);
    if(response?.ok)eventualPut(cache,req,response.clone());
    return response;
  }catch{
    return (await cache.match(req))||(req.mode==='navigate'?await cache.match('./index.html'):Response.error());
  }
}

function eventualPut(cache,req,response){
  cache.put(req,response).catch(()=>{});
}

async function boundedImage(req,cacheName,limit){
  const cache=await caches.open(cacheName);
  const hit=await cache.match(req);
  if(hit)return hit;
  try{
    const response=await fetch(req);
    if(response&&(response.ok||response.type==='opaque')){
      try{await cache.put(req,response.clone());await trim(cacheName,limit);}catch{}
    }
    return response;
  }catch{
    return (await caches.match('./assets/ui/fallback-card.svg'))||Response.error();
  }
}

self.addEventListener('fetch',event=>{
  const req=event.request;
  if(req.method!=='GET')return;
  const url=new URL(req.url);

  if(req.mode==='navigate'){
    event.respondWith(networkFirst(req));
    return;
  }

  if(req.destination==='image'){
    const isTile=url.hostname==='tile.openstreetmap.org';
    event.respondWith(boundedImage(req,isTile?TILE_CACHE:IMAGE_CACHE,isTile?TILE_LIMIT:IMAGE_LIMIT));
    return;
  }

  if(url.origin===self.location.origin){
    event.respondWith(networkFirst(req));
    return;
  }

  // Wikipedia and Commons API payloads are deliberately not stored in Cache Storage.
  // The old worker cached every semantic lookup and could exhaust iOS PWA storage/memory.
  if(['ru.wikipedia.org','en.wikipedia.org','commons.wikimedia.org'].includes(url.hostname)){
    event.respondWith(fetch(req));
    return;
  }

  if(url.hostname==='unpkg.com')event.respondWith(fetch(req));
});
