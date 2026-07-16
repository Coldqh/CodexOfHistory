/* Codex v8.4.0 — Bronze Age shared comparative layer and era exam */
(()=>{
  const V='8.4.0';
  window.CODEX_VERSION=V;
  V22_CAMPAIGN_CODES.BRONZE_ERA_EXAM='BRONZE_WORLD';
  state.bronzeWorldRegion=state.bronzeWorldRegion||'BABYLON';

  const oldSync=syncActiveCampaignRuntime;
  syncActiveCampaignRuntime=function(){
    oldSync();
    if(activeCampaignId()!=='BRONZE_ERA_EXAM')return;
    const first=CAMPAIGN.nodes[0];
    (first?.cards||[]).forEach(id=>{if(!state.unlocked.includes(id))state.unlocked.push(id);});
    CODEX_CONFIG.maps=CODEX_MAPS.BRONZE_ERA_EXAM||CODEX_CONFIG.maps;
  };

  const oldNoun=activeCampaignNoun;
  activeCampaignNoun=function(){return activeCampaignId()==='BRONZE_ERA_EXAM'?'ЭПОХА II · БРОНЗОВЫЙ ВЕК':oldNoun();};
  const oldPackTitle=activeCampaignPackTitle;
  activeCampaignPackTitle=function(){return activeCampaignId()==='BRONZE_ERA_EXAM'?'Общий архив бронзового века':oldPackTitle();};
  const oldPackCover=activeCampaignPackCover;
  activeCampaignPackCover=function(){return activeCampaignId()==='BRONZE_ERA_EXAM'?'assets/packs/bronze-era-pack.svg':oldPackCover();};

  const layer=()=>CODEX_CAMPAIGNS.BRONZE_ERA_EXAM?.eraLayer||{};
  const regionProgress=region=>typeof campaignProgressFor==='function'?campaignProgressFor(region.campaignId):0;
  window.focusBronzeWorldRegion=function(id){
    const region=(layer().regions||[]).find(x=>x.id===id);if(!region)return;
    state.bronzeWorldRegion=id;save();
    focusMapPoint(region.center,region.zoom||5,`<div class="map-popup dawn-popup"><b>${esc(region.title)}</b><span>${esc(region.summary)}</span><small>Прогресс кампании: ${regionProgress(region)}%</small><button onclick="startWorldCampaign('${region.campaignId}')">Открыть кампанию</button></div>`);
    document.querySelectorAll('[data-bronze-region]').forEach(el=>el.classList.toggle('active',el.dataset.bronzeRegion===id));
  };
  function regionStrip(){
    const icons={BABYLON:'𒀭',EGYPT:'𓂀',HATTI:'𒀱',AEGEAN:'◇',NETWORK:'≋',COLLAPSE:'◆'};
    return `<section class="dawn-region-strip bronze-region-strip reveal"><div class="section-head"><div><small>КАРТА ВТОРОЙ ЭПОХИ</small><h2>Шесть связанных кампаний</h2></div><span>нажми, чтобы приблизить</span></div><div class="dawn-region-grid">${(layer().regions||[]).map(r=>`<button data-bronze-region="${r.id}" class="${state.bronzeWorldRegion===r.id?'active':''}" onclick="focusBronzeWorldRegion('${r.id}')"><span>${icons[r.id]||'◇'}</span><div><b>${r.title}</b><small>${regionProgress(r)}% · ${r.summary}</small></div></button>`).join('')}</div></section>`;
  }
  function parallelTimeline(){
    return `<section class="parallel-era-timeline bronze-parallel-timeline reveal"><div class="section-head"><div><small>ПАРАЛЛЕЛЬНАЯ ХРОНОЛОГИЯ</small><h2>Разные регионы на одной шкале</h2></div><span>датировки заданы интервалами</span></div><div class="parallel-table-wrap"><table><thead><tr><th>Период</th><th>Вавилония</th><th>Египет</th><th>Хатти</th><th>Эгеида</th><th>Международная сеть</th></tr></thead><tbody>${(layer().parallelTimeline||[]).map(x=>`<tr><th><b>${x.date}</b><small>${x.certainty}</small></th><td>${x.BABYLON}</td><td>${x.EGYPT}</td><td>${x.HATTI}</td><td>${x.AEGEAN}</td><td>${x.NETWORK}</td></tr>`).join('')}</tbody></table></div></section>`;
  }

  const oldHome=home;
  home=function(){
    syncActiveCampaignRuntime();
    if(activeCampaignId()!=='BRONZE_ERA_EXAM')return oldHome();
    const m=currentMission(),ch=chapterForMission(m.id),owned=state.unlocked.filter(id=>card(id)?.campaign==='BRONZE_WORLD').length;
    return shell(`<section class="home-hero home-hero-clean bronze-world-home reveal"><div class="hero-layout"><div class="hero-content"><div class="eyebrow">Бронзовый век · итог второй эпохи</div><h2>${m.title}</h2><p>${ch.subtitle}</p><div class="hero-actions"><button class="btn" onclick="openMission('${m.id}')">${m.emoji} Продолжить</button><button class="btn secondary" onclick="go('campaign')">Все миссии</button></div></div><div class="collapse-seal"><span>◇</span><b>2000–1050</b><small>до н. э.</small></div></div></section><section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">◎</div><b>${campaignProgress()}%</b><span>кампания</span></div><div class="stat-box"><div class="stat-icon">▤</div><b>${completedMissionCount()}/${CAMPAIGN.nodes.length}</b><span>миссий</span></div><div class="stat-box"><div class="stat-icon">▦</div><b>${owned}/96</b><span>карточек</span></div><div class="stat-box stat-action" onclick="openPackHub()"><div class="stat-icon">✦</div><b>${dailyPackStatusShort()}</b><span>пак дня</span></div></section>${regionStrip()}<section class="daily-home-card reveal" onclick="openDaily()"><div class="daily-home-icon">◷</div><div><div class="eyebrow">Ежедневное обучение</div><h3>${dailyLearningCompleteToday()?'Сессия выполнена':`К повторению: ${dailyDueCards().length}`}</h3><p>${dailyLearningCompleteToday()?'Пак дня доступен.':'Повтори открытые знания за несколько минут.'}</p></div><button class="btn ${dailyLearningCompleteToday()?'secondary':''}">${dailyLearningCompleteToday()?'Открыть':'Начать'}</button></section>`);
  };

  const oldCampaign=campaign;
  campaign=function(){
    let html=oldCampaign();if(activeCampaignId()!=='BRONZE_ERA_EXAM')return html;
    html=html.replace(/РИМСКАЯ КАМПАНИЯ|МЕСОПОТАМСКАЯ КАМПАНИЯ|ЕГИПЕТСКАЯ КАМПАНИЯ|КАМПАНИЯ БРОНЗОВОГО ВЕКА|ЕГИПЕТ · СРЕДНЕЕ И НОВОЕ ЦАРСТВА|МИНОЙЦЫ · МИКЕНЦЫ · ЭГЕЙСКИЙ МИР|КРИЗИС · РАЗРУШЕНИЕ · ПЕРЕХОД/g,'ОБЩИЙ ЭКЗАМЕН ВТОРОЙ ЭПОХИ');
    return html.replace('</div></main><nav',`${parallelTimeline()}</div></main><nav`);
  };

  const oldMap=mapScreen;
  mapScreen=function(){
    if(activeCampaignId()!=='BRONZE_ERA_EXAM')return oldMap();
    const opened=[...new Set(CAMPAIGN.nodes.flatMap(n=>n.cards||[]))].map(card).filter(c=>c&&isUnlocked(c.id));
    return shell(`<section class="collection-header compact-collection-head reveal"><div><div class="eyebrow">Глобальная карта второй эпохи</div><h2>Державы, пути и центры кризиса</h2></div><div class="collection-count">${opened.length} точек</div></section>${regionStrip()}<div class="map-shell atlas-clean dawn-atlas reveal"><div id="atlas-map" class="leaflet-map"></div><div class="map-actions"><button class="map-action" onclick="resetAtlasView()" title="Общий обзор">⌂</button><button class="map-action" onclick="fitAtlasMarkers()" title="Показать точки">◎</button></div></div>${parallelTimeline()}<section class="section compact-section reveal"><div class="section-head"><h2>Открытые точки</h2><span>${opened.length}</span></div><div class="location-grid">${opened.map(c=>`<article class="panel panel-click location-card" onclick="focusAtlasCard('${c.id}')"><small>${c.region}</small><h3>${typeIcon(c.type)} ${c.title}</h3><p>${c.date}</p></article>`).join('')}</div></section>`);
  };

  syncActiveCampaignRuntime();save();
})();
