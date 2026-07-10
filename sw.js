const VERSION='codex-v2.0.0';
const APP_CACHE=`${VERSION}-app`;
const IMAGE_CACHE=`${VERSION}-images`;
const APP_SHELL=['./','./index.html','./styles.css','./manifest.webmanifest','./assets/ui/codex-mark.svg','./assets/ui/fallback-card.svg','./assets/ui/pack-daily.svg','./assets/ui/pack-rome.svg',
"./assets/cards/rome/chapter_02/per_rep_001.svg",
"./assets/cards/rome/chapter_02/per_rep_002.svg",
"./assets/cards/rome/chapter_02/evt_rep_001.svg",
"./assets/cards/rome/chapter_02/per_rep_003.svg",
"./assets/cards/rome/chapter_02/bat_rep_001.svg",
"./assets/cards/rome/chapter_02/cul_rep_001.svg",
"./assets/cards/rome/chapter_02/cul_rep_002.svg",
"./assets/cards/rome/chapter_02/evt_rep_002.svg",
"./assets/cards/rome/chapter_02/org_rep_001.svg",
"./assets/cards/rome/chapter_02/evt_rep_003.svg",
"./assets/cards/rome/chapter_02/law_rep_001.svg",
"./assets/cards/rome/chapter_02/org_rep_002.svg",
"./assets/cards/rome/chapter_02/per_rep_004.svg",
"./assets/cards/rome/chapter_02/per_rep_005.svg",
"./assets/cards/rome/chapter_02/evt_rep_004.svg",
"./assets/cards/rome/chapter_02/per_arep_001.svg",
"./assets/cards/rome/chapter_02/loc_arep_001.svg",
"./assets/cards/rome/chapter_02/loc_arep_002.svg",
"./assets/cards/rome/chapter_02/per_arep_002.svg",
"./assets/cards/rome/chapter_02/per_arep_003.svg",
"./assets/cards/rome/chapter_02/per_arep_004.svg",
"./assets/cards/rome/chapter_02/per_arep_005.svg",
"./assets/cards/rome/chapter_02/loc_arep_003.svg",
"./assets/cards/rome/chapter_02/bat_arep_001.svg",
"./assets/cards/rome/chapter_02/org_arep_001.svg",
"./assets/cards/rome/chapter_02/org_arep_002.svg",
"./assets/cards/rome/chapter_02/org_arep_003.svg",
"./assets/cards/rome/chapter_02/org_arep_004.svg",
"./assets/cards/rome/chapter_02/art_arep_001.svg",
"./assets/cards/rome/chapter_02/term_arep_001.svg",
"./assets/cards/rome/chapter_02/loc_arep_004.svg",
"./assets/cards/rome/chapter_02/loc_arep_005.svg",
"./assets/cards/rome/chapter_02/org_arep_005.svg",
"./assets/cards/rome/chapter_02/org_arep_006.svg",
"./assets/cards/rome/chapter_02/law_arep_001.svg",
"./assets/cards/rome/chapter_02/term_arep_002.svg",
"./assets/cards/rome/chapter_02/per_arep_006.svg",
"./assets/cards/rome/chapter_02/per_arep_007.svg",
"./assets/cards/rome/chapter_03/art_ita_001.svg",
"./assets/cards/rome/chapter_03/bat_ita_001.svg",
"./assets/cards/rome/chapter_03/bat_ita_002.svg",
"./assets/cards/rome/chapter_03/bat_ita_003.svg",
"./assets/cards/rome/chapter_03/bat_ita_004.svg",
"./assets/cards/rome/chapter_03/bat_ita_005.svg",
"./assets/cards/rome/chapter_03/bat_ita_006.svg",
"./assets/cards/rome/chapter_03/city_ita_001.svg",
"./assets/cards/rome/chapter_03/city_ita_002.svg",
"./assets/cards/rome/chapter_03/city_ita_003.svg",
"./assets/cards/rome/chapter_03/city_ita_004.svg",
"./assets/cards/rome/chapter_03/city_ita_005.svg",
"./assets/cards/rome/chapter_03/city_ita_006.svg",
"./assets/cards/rome/chapter_03/city_ita_007.svg",
"./assets/cards/rome/chapter_03/city_ita_008.svg",
"./assets/cards/rome/chapter_03/evt_ita_001.svg",
"./assets/cards/rome/chapter_03/evt_ita_002.svg",
"./assets/cards/rome/chapter_03/evt_ita_003.svg",
"./assets/cards/rome/chapter_03/evt_ita_004.svg",
"./assets/cards/rome/chapter_03/org_ita_001.svg",
"./assets/cards/rome/chapter_03/peo_ita_001.svg",
"./assets/cards/rome/chapter_03/peo_ita_002.svg",
"./assets/cards/rome/chapter_03/peo_ita_003.svg",
"./assets/cards/rome/chapter_03/peo_ita_004.svg",
"./assets/cards/rome/chapter_03/peo_ita_005.svg",
"./assets/cards/rome/chapter_03/peo_ita_006.svg",
"./assets/cards/rome/chapter_03/peo_ita_007.svg",
"./assets/cards/rome/chapter_03/peo_ita_008.svg",
"./assets/cards/rome/chapter_03/peo_ita_009.svg",
"./assets/cards/rome/chapter_03/peo_ita_010.svg",
"./assets/cards/rome/chapter_03/per_ita_001.svg",
"./assets/cards/rome/chapter_03/per_ita_002.svg",
"./assets/cards/rome/chapter_03/per_ita_003.svg",
"./assets/cards/rome/chapter_03/per_ita_004.svg",
"./assets/cards/rome/chapter_03/per_ita_005.svg",
"./assets/cards/rome/chapter_03/reg_ita_001.svg",
"./assets/cards/rome/chapter_03/reg_ita_002.svg",
"./assets/cards/rome/chapter_03/reg_ita_003.svg",
"./assets/cards/rome/chapter_03/road_ita_001.svg",
"./assets/cards/rome/chapter_03/state_ita_001.svg",
"./assets/cards/rome/chapter_03/sys_ita_001.svg",
"./assets/cards/rome/chapter_03/term_ita_001.svg",
"./assets/cards/rome/chapter_03/term_ita_002.svg",
"./assets/cards/rome/chapter_03/term_ita_003.svg",
"./assets/cards/rome/chapter_03/term_ita_004.svg",
"./assets/cards/rome/chapter_03/term_ita_005.svg",
"./assets/cards/rome/chapter_03/term_ita_006.svg",
"./assets/cards/rome/chapter_03/war_ita_001.svg",
"./assets/cards/rome/chapter_03/war_ita_002.svg",
"./assets/cards/rome/chapter_03/war_ita_003.svg"];
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
