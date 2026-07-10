/* Codex of History v1.1 — data-first static bootstrap */
(() => {
  const app = document.getElementById('app');
  const showBoot = (title, text, isError=false) => {
    app.innerHTML = `<main class="boot-screen ${isError?'boot-error':''}"><div class="boot-mark">C</div><div><div class="eyebrow">Content Engine v1.1</div><h1>${title}</h1><p>${text}</p></div></main>`;
  };
  const fetchJson = async path => {
    const response = await fetch(path, {cache:'no-cache'});
    if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
    return response.json();
  };
  const loadScript = path => new Promise((resolve,reject) => {
    const script=document.createElement('script'); script.src=path; script.defer=false;
    script.onload=resolve; script.onerror=()=>reject(new Error(`Не загружен модуль ${path}`)); document.body.appendChild(script);
  });
  async function boot(){
    try {
      showBoot('Открываем Codex','Загружаем карточки, кампанию и игровые системы…');
      const manifest=await fetchJson('data/content-manifest.json');
      const d=manifest.datasets;
      window.CODEX_VENDOR_READY={leaflet:manifest.vendors?.leaflet?loadScript(manifest.vendors.leaflet).catch(error=>{console.warn('[Codex vendor]',error);return false;}):Promise.resolve(false)};
      const [cardSets,relations,campaign,pools,quizzes,stories,mastery,packs,collection,maps]=await Promise.all([
        Promise.all(d.cards.map(fetchJson)),fetchJson(d.relations),fetchJson(d.campaign),fetchJson(d.pools),fetchJson(d.quizzes),
        fetchJson(d.stories),fetchJson(d.mastery),fetchJson(d.packs),fetchJson(d.collection),fetchJson(d.maps)
      ]);
      const cards=cardSets.flat();
      window.CODEX_MANIFEST=manifest;
      window.CODEX_CONFIG={mastery,packs,collection,maps};
      window.CARDS=cards; window.RELATIONS=relations; window.CAMPAIGN=campaign; window.V09_CONTENT=pools;
      window.QUIZZES=quizzes; window.PERSONAL_STORIES=stories;
      window.CODEX_REGISTRY={
        cardsById:new Map(cards.map(x=>[x.id,x])),
        relationsByCard:new Map(cards.map(c=>[c.id,relations.filter(r=>r.source===c.id||r.target===c.id)])),
        missionsById:new Map(campaign.nodes.map(x=>[x.id,x])),
        poolsById:new Map(pools.pools.map(x=>[x.id,x]))
      };
      for(const path of manifest.scripts) await loadScript(path);
    } catch(error) {
      console.error('[Codex boot]',error);
      const hint=location.protocol==='file:'?'Открой проект через GitHub Pages или локальный HTTP-сервер, а не двойным кликом по index.html.':'Проверь, что все файлы патча распакованы в корень репозитория.';
      showBoot('Codex не загрузился',`${error.message}. ${hint}`,true);
    }
  }
  boot();
})();
