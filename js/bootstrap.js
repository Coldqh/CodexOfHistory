/* Codex of History v2.2 — multi-campaign static bootstrap */
(() => {
  const app=document.getElementById('app');
  const showBoot=(title,text,isError=false)=>{app.innerHTML=`<main class="boot-screen ${isError?'boot-error':''}"><div class="boot-mark"><img src="assets/ui/codex-logo-mark.png" alt="Codex of History"></div><div><div class="eyebrow">Content Engine v6.9.0</div><h1>${title}</h1><p>${text}</p></div></main>`;};
  const refreshToken=sessionStorage.getItem('codex_force_refresh')||'';
  const addVersion=(path,version='')=>{if(/^https?:/i.test(path))return path;const url=new URL(path,location.href);if(version)url.searchParams.set('v',version);if(refreshToken)url.searchParams.set('refresh',refreshToken);return url.href;};
  const fetchJson=async(path,version='')=>{const response=await fetch(addVersion(path,version),{cache:'no-store'});if(!response.ok)throw new Error(`${path}: HTTP ${response.status}`);return response.json();};
  const loadScript=(path,version='')=>new Promise((resolve,reject)=>{const script=document.createElement('script');script.src=addVersion(path,version);script.defer=false;script.onload=resolve;script.onerror=()=>reject(new Error(`Не загружен модуль ${path}`));document.body.appendChild(script);});
  const readMany=async(spec,version)=>Array.isArray(spec)?Promise.all(spec.map(path=>fetchJson(path,version))):[await fetchJson(spec,version)];
  const mergeObjects=list=>Object.assign({},...list);
  async function registerImageCache(){if(!('serviceWorker'in navigator)||location.protocol==='file:')return;try{await navigator.serviceWorker.register('sw.js?v=6.9.0',{scope:'./',updateViaCache:'none'});}catch(error){console.warn('[Codex cache]',error);}}
  async function boot(){
    try{
      await registerImageCache();showBoot('Открываем Codex','Загружаем эпохи, кампании, карточки и учебные системы…');
      const manifest=await fetchJson('data/content-manifest.json');const version=manifest.version||'6.9.0';const d=manifest.datasets;
      window.CODEX_VENDOR_READY={leaflet:manifest.vendors?.leaflet?loadScript(manifest.vendors.leaflet,version).catch(error=>{console.warn('[Codex vendor]',error);return false;}):Promise.resolve(false)};
      const [cardSets,relations,campaignSets,poolSets,quizSets,storySets,mastery,packs,collection,mapEntries,daily,lessonSets,eras,campaignCatalog,worldTimeline]=await Promise.all([
        Promise.all(d.cards.map(path=>fetchJson(path,version))),fetchJson(d.relations,version),readMany(d.campaigns||d.campaign,version),readMany(d.pools,version),readMany(d.quizzes,version),readMany(d.stories,version),fetchJson(d.mastery,version),fetchJson(d.packs,version),fetchJson(d.collection,version),
        Promise.all(Object.entries(d.maps||{}).map(async([id,path])=>[id,await fetchJson(path,version)])),fetchJson(d.daily,version),readMany(d.lessons,version),fetchJson(d.eras,version),fetchJson(d.campaignCatalog,version),fetchJson(d.worldTimeline,version)
      ]);
      const cards=cardSets.flat();const campaigns=Object.fromEntries(campaignSets.map(c=>[c.id,c]));
      const pools={campaigns:mergeObjects(poolSets.map(p=>p.campaigns||{})),pools:poolSets.flatMap(p=>p.pools||[]),acquisition:mergeObjects(poolSets.map(p=>p.acquisition||{}))};
      const quizzes=mergeObjects(quizSets);const stories=mergeObjects(storySets);const lessons=mergeObjects(lessonSets);const maps=Object.fromEntries(mapEntries);
      const defaultCampaign=campaigns.ROME_CAMPAIGN||campaignSets[0];
      window.CODEX_MANIFEST=manifest;window.CODEX_CONFIG={mastery,packs,collection,maps:maps[defaultCampaign.id],daily};window.CODEX_MAPS=maps;window.CODEX_CAMPAIGNS=campaigns;window.CODEX_ALL_POOLS=pools;
      window.CODEX_WORLD={eras,campaigns:campaignCatalog,timeline:worldTimeline};window.CARDS=cards;window.RELATIONS=relations;window.CAMPAIGN=defaultCampaign;window.V09_CONTENT=pools;window.QUIZZES=quizzes;window.PERSONAL_STORIES=stories;window.CODEX_LESSONS=lessons;
      window.CODEX_REGISTRY={cardsById:new Map(cards.map(x=>[x.id,x])),relationsByCard:new Map(cards.map(c=>[c.id,relations.filter(r=>r.source===c.id||r.target===c.id)])),missionsById:new Map(campaignSets.flatMap(c=>c.nodes).map(x=>[x.id,x])),campaignsById:new Map(campaignSets.map(c=>[c.id,c])),poolsById:new Map(pools.pools.map(x=>[x.id,x])),lessonsByMission:new Map(Object.entries(lessons))};
      for(const path of manifest.scripts)await loadScript(path,version);if(refreshToken)sessionStorage.removeItem('codex_force_refresh');
    }catch(error){console.error('[Codex boot]',error);const hint=location.protocol==='file:'?'Открой проект через GitHub Pages или локальный HTTP-сервер.':'Проверь, что все файлы патча распакованы в корень репозитория.';showBoot('Codex не загрузился',`${error.message}. ${hint}`,true);}
  }
  boot();
})();
