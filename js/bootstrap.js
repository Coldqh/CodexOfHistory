/* Codex of History v2.0.0 — versioned static bootstrap and forced refresh support */
(() => {
  const app = document.getElementById('app');
  const showBoot = (title, text, isError=false) => {
    app.innerHTML = `<main class="boot-screen ${isError?'boot-error':''}"><div class="boot-mark">C</div><div><div class="eyebrow">Content Engine v2.0.0</div><h1>${title}</h1><p>${text}</p></div></main>`;
  };
  const refreshToken=sessionStorage.getItem('codex_force_refresh')||'';
  const addVersion=(path,version='')=>{
    if(/^https?:/i.test(path)) return path;
    const url=new URL(path,location.href);
    if(version) url.searchParams.set('v',version);
    if(refreshToken) url.searchParams.set('refresh',refreshToken);
    return url.href;
  };
  const fetchJson = async (path,version='') => {
    const response = await fetch(addVersion(path,version), {cache:'no-store'});
    if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
    return response.json();
  };
  const loadScript = (path,version='') => new Promise((resolve,reject) => {
    const script=document.createElement('script'); script.src=addVersion(path,version); script.defer=false;
    script.onload=resolve; script.onerror=()=>reject(new Error(`Не загружен модуль ${path}`)); document.body.appendChild(script);
  });
  async function registerImageCache(){
    if(!('serviceWorker' in navigator)||location.protocol==='file:') return;
    try{ await navigator.serviceWorker.register('sw.js?v=2.0.0',{scope:'./'}); }
    catch(error){ console.warn('[Codex cache]',error); }
  }
  async function boot(){
    try {
      await registerImageCache();
      showBoot('Открываем Codex','Загружаем карточки, кампанию и игровые системы…');
      const manifest=await fetchJson('data/content-manifest.json');
      const version=manifest.version||'2.0.0';
      const d=manifest.datasets;
      window.CODEX_VENDOR_READY={leaflet:manifest.vendors?.leaflet?loadScript(manifest.vendors.leaflet,version).catch(error=>{console.warn('[Codex vendor]',error);return false;}):Promise.resolve(false)};
      const loadJsonBundle=async spec=>Array.isArray(spec)?Object.assign({},...(await Promise.all(spec.map(path=>fetchJson(path,version))))):fetchJson(spec,version);
      const [cardSets,relations,campaign,pools,quizzes,stories,mastery,packs,collection,maps,daily,lessons]=await Promise.all([
        Promise.all(d.cards.map(path=>fetchJson(path,version))),fetchJson(d.relations,version),fetchJson(d.campaign,version),fetchJson(d.pools,version),loadJsonBundle(d.quizzes),
        fetchJson(d.stories,version),fetchJson(d.mastery,version),fetchJson(d.packs,version),fetchJson(d.collection,version),fetchJson(d.maps,version),fetchJson(d.daily,version),loadJsonBundle(d.lessons)
      ]);
      const cards=cardSets.flat();
      window.CODEX_MANIFEST=manifest;
      window.CODEX_CONFIG={mastery,packs,collection,maps,daily};
      window.CARDS=cards; window.RELATIONS=relations; window.CAMPAIGN=campaign; window.V09_CONTENT=pools;
      window.QUIZZES=quizzes; window.PERSONAL_STORIES=stories; window.CODEX_LESSONS=lessons;
      window.CODEX_REGISTRY={
        cardsById:new Map(cards.map(x=>[x.id,x])),
        relationsByCard:new Map(cards.map(c=>[c.id,relations.filter(r=>r.source===c.id||r.target===c.id)])),
        missionsById:new Map(campaign.nodes.map(x=>[x.id,x])),
        poolsById:new Map(pools.pools.map(x=>[x.id,x])),
        lessonsByMission:new Map(Object.entries(lessons))
      };
      for(const path of manifest.scripts) await loadScript(path,version);
      if(refreshToken) sessionStorage.removeItem('codex_force_refresh');
    } catch(error) {
      console.error('[Codex boot]',error);
      const hint=location.protocol==='file:'?'Открой проект через GitHub Pages или локальный HTTP-сервер, а не двойным кликом по index.html.':'Проверь, что все файлы патча распакованы в корень репозитория.';
      showBoot('Codex не загрузился',`${error.message}. ${hint}`,true);
    }
  }
  boot();
})();
