const VERSION='codex-v1.6.0';
const APP_CACHE=`${VERSION}-app`;
const IMAGE_CACHE=`${VERSION}-images`;
const APP_SHELL=['./','./index.html','./styles.css','./manifest.webmanifest','./assets/ui/codex-mark.svg','./assets/ui/fallback-card.svg','./assets/ui/pack-daily.svg','./assets/ui/pack-rome.svg'];
self.addEventListener('install',event=>{event.waitUntil(caches.open(APP_CACHE).then(cache=>cache.addAll(APP_SHELL)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('codex-')&&!k.startsWith(VERSION)).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',event=>{
  const req=event.request;
  if(req.method!=='GET')return;
  const url=new URL(req.url);
  const isCommons=url.hostname==='commons.wikimedia.org'||url.hostname.endsWith('.wikimedia.org');
  if(isCommons&&req.destination==='image'){
    event.respondWith(caches.open(IMAGE_CACHE).then(async cache=>{
      const hit=await cache.match(req);if(hit)return hit;
      try{const response=await fetch(req);if(response&&(response.ok||response.type==='opaque'))cache.put(req,response.clone());return response;}
      catch(_){return caches.match('./assets/ui/fallback-card.svg');}
    }));
    return;
  }
  if(url.origin===self.location.origin){
    event.respondWith(fetch(req).then(response=>{const copy=response.clone();caches.open(APP_CACHE).then(cache=>cache.put(req,copy));return response;}).catch(()=>caches.match(req).then(hit=>hit||caches.match('./index.html'))));
  }
});
