/* Codex of History v8.7.1 — bounded GitHub Pages service worker with session-only remote card images */
const VERSION='codex-v8.7.1';
const APP_CACHE=`${VERSION}-app`;
const IMAGE_CACHE=`${VERSION}-images`;
const TILE_CACHE=`${VERSION}-tiles`;
const IMAGE_LIMIT=48;
const TILE_LIMIT=72;
const CORE=[
  './','./index.html','./styles.css','./manifest.webmanifest','./data/content-manifest.json',
  './js/bootstrap.js','./assets/ui/codex-logo-mark.png','./assets/ui/codex-logo-mark.svg','./assets/ui/codex-app-icon.svg','./assets/ui/codex-favicon-32.png','./assets/ui/codex-favicon-16.png','./assets/ui/codex-icon-192.png',
  './assets/ui/codex-icon-512.png','./assets/ui/codex-icon-maskable-512.png','./assets/ui/fallback-card.svg','./assets/eras/early-medieval.svg',
  './assets/packs/achaemenid-persia-pack.svg','./assets/packs/aegean-pack.svg','./assets/packs/alexander-pack.svg','./assets/packs/archaic-greece-pack.svg','./assets/packs/assyria-babylon-pack.svg','./assets/packs/babylon-pack.svg','./assets/packs/bronze-collapse-pack.svg','./assets/packs/bronze-era-pack.svg','./assets/packs/china-pack.svg','./assets/packs/civilizations-pack.svg','./assets/packs/classical-era-pack.svg','./assets/packs/classical-greece-pack.svg','./assets/packs/comparison-pack.svg','./assets/packs/egypt-bronze-pack.svg','./assets/packs/egypt-pack.svg','./assets/packs/han-pack.svg','./assets/packs/hellenistic-pack.svg','./assets/packs/hellenistic-roman-era-pack.svg','./assets/packs/hittites-pack.svg','./assets/packs/indus-pack.svg','./assets/packs/international-bronze-pack.svg','./assets/packs/iron-era-pack.svg','./assets/packs/israel-judah-pack.svg','./assets/packs/late-religions-pack.svg','./assets/packs/late-roman-pack.svg','./assets/packs/maurya-pack.svg','./assets/packs/migration-kingdoms-pack.svg','./assets/packs/eastern-roman-pack.svg','./assets/packs/sasanian-pack.svg','./assets/packs/central-asia-late-pack.svg','./assets/packs/india-gupta-pack.svg','./assets/packs/china-post-han-pack.svg','./assets/packs/aksum-nubia-arabia-pack.svg','./assets/packs/americas-late-pack.svg','./assets/packs/world-around-700-pack.svg','./assets/packs/islamic-origins-pack.svg','./assets/packs/abbasid-baghdad-pack.svg','./assets/packs/franks-transition-pack.svg','./assets/packs/byzantium-macedonian-pack.svg','./assets/packs/vikings-north-atlantic-pack.svg','./assets/packs/slavic-bulgaria-rus-pack.svg','./assets/packs/al-andalus-west-pack.svg','./assets/packs/tang-song-pack.svg','./assets/packs/mesopotamia-pack.svg','./assets/packs/phoenicians-pack.svg','./assets/packs/rome-pack.svg','./assets/packs/steppe-silk-pack.svg','./assets/packs/vedic-india-pack.svg','./assets/packs/zhou-warring-pack.svg','./data/image_manifest.json','./data/image_queries.json',
  './js/features/v3-2-egypt-middle-new.js','./js/features/v3-3-hittites.js','./js/features/v3-4-aegean.js','./js/features/v3-5-international.js','./js/features/v3-6-collapse.js','./js/features/v3-7-bronze-world.js','./js/features/v4-0-assyria-babylon.js','./js/features/v4-1-phoenicians.js','./js/features/v4-2-israel-judah.js','./js/features/v4-3-archaic-greece.js','./js/features/v4-4-zhou-warring.js','./js/features/v4-5-vedic-india.js','./js/features/v4-6-iron-world.js','./js/features/v5-0-achaemenid-persia.js','./js/features/v5-1-classical-greece.js','./js/features/v5-2-alexander.js','./js/features/v5-3-classical-world.js','./js/features/v6-0-hellenistic.js','./js/features/v6-4-maurya.js','./js/features/v6-5-han.js','./js/features/v6-6-steppe-silk.js','./js/features/v6-7-hellenistic-roman-world.js','./js/features/v6-8-late-roman.js','./js/features/v6-9-late-religions.js','./js/features/v7-0-migration-kingdoms.js','./js/features/v7-1-eastern-roman.js','./js/features/v7-2-sasanian.js','./js/features/v7-3-central-asia.js','./js/features/v7-4-india-gupta.js','./js/features/v7-5-china-post-han.js','./js/features/v7-6-aksum-nubia-arabia.js','./js/features/v7-7-americas-late.js','./js/features/v7-8-world-around-700.js','./js/features/v8-0-islamic-origins.js','./js/features/v8-1-abbasid-baghdad.js','./js/features/v8-2-franks-transition.js','./js/features/v8-3-byzantium-macedonian.js','./js/features/v8-4-vikings-north-atlantic.js','./js/features/v8-5-slavic-bulgaria-rus.js','./js/features/v8-6-al-andalus-west.js','./js/features/v8-7-tang-song.js','./js/features/v6-1-rome-middle.js','./js/features/v3-1-1-hotfix.js','./js/features/v3-1-3-visual-semantics.js'
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
    if(isTile){
      event.respondWith(boundedImage(req,TILE_CACHE,TILE_LIMIT));
      return;
    }

    // Remote historical card images are session-only: do not persist them in Cache Storage.
    const isWikimediaImage=['upload.wikimedia.org','commons.wikimedia.org'].includes(url.hostname);
    if(isWikimediaImage){
      event.respondWith(fetch(req).catch(async()=> (await caches.match('./assets/ui/fallback-card.svg'))||Response.error()));
      return;
    }

    if(url.origin===self.location.origin){
      event.respondWith(networkFirst(req));
      return;
    }

    event.respondWith(fetch(req).catch(()=>Response.error()));
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
