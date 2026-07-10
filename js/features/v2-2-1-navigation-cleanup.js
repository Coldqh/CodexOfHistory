/* Codex v2.2.1 — clean world navigation and Mesopotamia-first home */
(function(){
  const PATCH_KEY='v221NavigationClean';
  if(!state[PATCH_KEY]){
    state.activeCampaign='MESOPOTAMIA_DAWN';
    state.worldView='CAMPAIGNS';
    state.worldDepth='ERAS';
    state.worldEra=null;
    state.worldCampaignPreview=null;
    state[PATCH_KEY]=true;
    syncActiveCampaignRuntime();
    save();
  }
  state.worldView=state.worldView==='TIMELINE'?'TIMELINE':'CAMPAIGNS';
  state.worldDepth=state.worldDepth==='CAMPAIGNS'?'CAMPAIGNS':'ERAS';

  function availableCampaignsForEra(id){
    return worldEraCampaigns(id).filter(c=>c.status==='PLAYABLE');
  }
  function allCampaignsForEra(id){
    return worldEraCampaigns(id);
  }

  setWorldView=function(view){
    state.worldView=view==='TIMELINE'?'TIMELINE':'CAMPAIGNS';
    if(state.worldView==='CAMPAIGNS'&&!state.worldEra)state.worldDepth='ERAS';
    state.worldCampaignPreview=null;
    save();render();
  };
  selectWorldEra=function(id){
    state.worldEra=id;
    state.worldView='CAMPAIGNS';
    state.worldDepth='CAMPAIGNS';
    state.worldCampaignPreview=null;
    save();render();window.scrollTo({top:0,behavior:'smooth'});
  };
  window.openWorldEra=selectWorldEra;
  window.backWorldToEras=function(){
    state.worldView='CAMPAIGNS';state.worldDepth='ERAS';state.worldEra=null;state.worldCampaignPreview=null;
    save();render();window.scrollTo({top:0,behavior:'smooth'});
  };

  eraCard=function(era){
    const available=availableCampaignsForEra(era.id).length;
    const total=allCampaignsForEra(era.id).length;
    return `<button class="era-card era-card-clean" style="--era-accent:${era.accent}" onclick="selectWorldEra('${era.id}')"><img src="${era.cover}" alt="${esc(era.title)}"><div class="era-card-overlay"><div class="era-number">ЭПОХА ${String(era.order).padStart(2,'0')}</div><h3>${era.title}</h3><div class="era-meta"><span>${era.dateLabel}</span><span>${available?`${available} доступно`:`${total} в плане`}</span></div></div></button>`;
  };

  worldCampaignCard=function(c){
    const playable=c.status==='PLAYABLE';
    const progress=playable?campaignProgressFor(c.id):0;
    return `<button class="world-campaign-card world-campaign-card-clean ${c.status.toLowerCase()}" onclick="${playable?`startWorldCampaign('${c.id}')`:`showToast('Пока недоступно','Кампания появится в одном из следующих патчей','○')`}"><div class="world-campaign-cover"><img src="${campaignCover(c)}" alt=""><span>${worldStatusIcon(c.status)} ${worldStatusLabel(c.status)}</span></div><div class="world-campaign-copy"><small>${c.period} · ${c.region}</small><h3>${c.title}</h3><div class="campaign-publication"><b>${c.releasedChapters}/${c.chapterCount}</b><span>глав</span></div>${playable?`<div class="progress"><span style="width:${progress}%"></span></div>`:''}</div></button>`;
  };

  timelineView=function(){
    return `<div class="timeline-list timeline-list-clean reveal">${WORLD_TIMELINE.map(m=>{const c=worldCampaign(m.campaignId);return `<button onclick="selectWorldEra('${c?.eraId||'ERA_DAWN'}')"><time>${worldYearLabel(m.year)}</time><b>${m.label}</b><span>${c?.title||''}</span></button>`;}).join('')}</div>`;
  };

  worldScreen=function(){
    const tabs=`<div class="world-view-tabs world-view-tabs-clean"><button class="${state.worldView==='CAMPAIGNS'?'active':''}" onclick="setWorldView('CAMPAIGNS')">Доступные кампании</button><button class="${state.worldView==='TIMELINE'?'active':''}" onclick="setWorldView('TIMELINE')">Хронология</button></div>`;
    let content='';
    if(state.worldView==='TIMELINE'){
      content=timelineView();
    }else if(state.worldDepth==='CAMPAIGNS'&&state.worldEra&&worldEra(state.worldEra)){
      const era=worldEra(state.worldEra);
      const campaigns=allCampaignsForEra(era.id);
      content=`<section class="world-step-head reveal"><button class="world-back" onclick="backWorldToEras()">← Эпохи</button><div><small>${era.dateLabel}</small><h2>${era.title}</h2></div></section><div class="world-campaign-grid reveal">${campaigns.map(worldCampaignCard).join('')}</div>`;
    }else{
      content=`<section class="world-step-head reveal"><div><small>Шаг 1</small><h2>Выбери эпоху</h2></div></section><div class="era-grid reveal">${ERAS.map(eraCard).join('')}</div>`;
    }
    return shell(`${tabs}${content}`);
  };

  const previousGo=go;
  go=function(tab){
    if(tab==='world'){
      state.worldView='CAMPAIGNS';state.worldDepth='ERAS';state.worldEra=null;state.worldCampaignPreview=null;
    }
    previousGo(tab);
  };

  const previousCampaign=campaign;
  campaign=function(){
    let html=previousCampaign();
    html=html.replace(/onclick="state\.worldEra='([^']+)'\;state\.worldView='CAMPAIGNS'\;go\('world'\)"/g,`onclick="openWorldEra('$1')"`);
    return html;
  };

  home=function(){
    syncActiveCampaignRuntime();
    const m=currentMission();
    const chapter=CAMPAIGN.chapters.find(ch=>ch.id===state.campaignChapter)||CAMPAIGN.chapters[0];
    return shell(`<section class="home-hero home-hero-clean reveal"><div class="hero-layout"><div class="hero-content"><div class="eyebrow">${activeCampaignLabel()} · ${chapter?.title||''}</div><h2>${m.title}</h2><div class="hero-actions"><button class="btn" onclick="openMission('${m.id}')">${m.emoji} Продолжить</button><button class="btn secondary" onclick="go('collection')">▦ Коллекция</button></div></div><div class="hero-orbit"><div class="orbit-core"><div class="core-value"><strong>${campaignProgress()}%</strong><span>пройдено</span></div></div><div class="orbit-chip one">Миссии<b>${completedMissionCount()}/${CAMPAIGN.nodes.length}</b></div><div class="orbit-chip two">Карточки<b>${state.unlocked.filter(id=>card(id)?.campaign==='MESOPOTAMIA').length}</b></div><div class="orbit-chip three">Фрагменты<b>${state.fragments} ◇</b></div></div></div></section><section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">𒀭</div><b>${campaignProgress()}%</b><span>кампания</span></div><div class="stat-box"><div class="stat-icon">▤</div><b>${completedMissionCount()}/${CAMPAIGN.nodes.length}</b><span>миссий</span></div><div class="stat-box"><div class="stat-icon">▦</div><b>${state.unlocked.filter(id=>card(id)?.campaign==='MESOPOTAMIA').length}</b><span>карточек</span></div><div class="stat-box stat-action" onclick="openPackHub()"><div class="stat-icon">✦</div><b>${dailyPackStatusShort()}</b><span>пак дня</span></div></section><section class="daily-home-card reveal" onclick="openDaily()"><div class="daily-home-icon">◷</div><div><div class="eyebrow">Ежедневное обучение</div><h3>${dailyLearningCompleteToday()?'Сессия выполнена':`К повторению: ${dailyDueCards().length}`}</h3></div><button class="btn ${dailyLearningCompleteToday()?'secondary':''}">${dailyLearningCompleteToday()?'Открыть':'Начать'}</button></section>`);
  };

  const previousRender=render;
  render=function(){syncActiveCampaignRuntime();previousRender();};
})();
