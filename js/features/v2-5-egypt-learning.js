/* Codex v2.5 — modern learning experience and study-era selection */
(function(){
  const V='4.2.0';
  window.CODEX_VERSION=V;
  state.studyEra=state.studyEra||null;
  state.studyCampaign=state.studyCampaign||null;
  state.studyOnboardingSeen=!!state.studyOnboardingSeen;
  const isFresh=()=>!state.missionsCompleted?.length&&!state.studyOnboardingSeen;
  const stageLabels=[['▤','Рассказ'],['⌛','Время'],['◆','Смысл'],['▥','Теория'],['◎','Практика']];

  function studyEraProgress(era){
    const cs=worldEraCampaigns(era.id).filter(c=>c.status==='PLAYABLE');
    if(!cs.length)return 0;
    return Math.round(cs.reduce((sum,c)=>sum+campaignProgressFor(c.id),0)/cs.length);
  }
  function modernEraCard(era){
    const available=worldEraCampaigns(era.id).filter(c=>c.status==='PLAYABLE').length;
    const p=studyEraProgress(era);
    return `<button class="study-era-card" style="--era-accent:${era.accent}" onclick="chooseStudyEra('${era.id}')"><img src="${era.cover}" alt=""><div class="study-era-shade"></div><div class="study-era-content"><small>${era.dateLabel}</small><h3>${era.title}</h3><div class="study-era-bottom"><span>${available?`${available} доступно`:'в разработке'}</span>${available?`<b>${p}%</b>`:''}</div></div></button>`;
  }
  window.chooseStudyEra=function(id){state.studyEra=id;state.worldEra=id;state.worldDepth='CAMPAIGNS';state.worldView='CAMPAIGNS';state.studyOnboardingSeen=true;save();render();window.scrollTo({top:0,behavior:'smooth'});};
  const oldStart=startWorldCampaign;
  startWorldCampaign=function(id){const c=worldCampaign(id);if(c?.status==='PLAYABLE'){state.studyEra=c.eraId;state.studyCampaign=id;state.studyOnboardingSeen=true;}oldStart(id);};
  window.resetStudyPath=function(){state.worldDepth='ERAS';state.worldEra=null;state.worldView='CAMPAIGNS';save();go('world');};

  worldScreen=function(){
    const tabs=`<div class="world-view-tabs world-view-tabs-clean"><button class="${state.worldView==='CAMPAIGNS'?'active':''}" onclick="setWorldView('CAMPAIGNS')">Доступные кампании</button><button class="${state.worldView==='TIMELINE'?'active':''}" onclick="setWorldView('TIMELINE')">Хронология</button></div>`;
    if(state.worldView==='TIMELINE')return shell(`${tabs}${timelineView()}`);
    if(state.worldDepth==='CAMPAIGNS'&&state.worldEra&&worldEra(state.worldEra)){
      const era=worldEra(state.worldEra), campaigns=worldEraCampaigns(era.id);
      return shell(`${tabs}<section class="study-step-head reveal"><button onclick="backWorldToEras()">←</button><div><small>ШАГ 2 · КАМПАНИЯ</small><h2>${era.title}</h2></div></section><div class="study-campaign-grid reveal">${campaigns.map(c=>{const playable=c.status==='PLAYABLE',progress=playable?campaignProgressFor(c.id):0;return `<button class="study-campaign-card ${playable?'playable':'planned'}" onclick="${playable?`startWorldCampaign('${c.id}')`:`showToast('Пока недоступно','Кампания запланирована','○')`}"><img src="${campaignCover(c)}" alt=""><div><small>${c.period}</small><h3>${c.title}</h3><div class="study-campaign-meta"><span>${c.releasedChapters}/${c.chapterCount} глав</span>${playable?`<b>${progress}%</b>`:'<b>план</b>'}</div>${playable?`<i><span style="width:${progress}%"></span></i>`:''}</div></button>`;}).join('')}</div>`);
    }
    return shell(`${tabs}<section class="study-step-head reveal"><span class="study-step-mark">01</span><div><small>ШАГ 1 · ЭПОХА</small><h2>Выбери эпоху</h2></div></section><div class="study-era-grid reveal">${ERAS.map(modernEraCard).join('')}</div>`);
  };

  const oldGo=go;
  go=function(tab){if(tab==='world'&&!state.worldEra){state.worldDepth='ERAS';state.worldView='CAMPAIGNS';}oldGo(tab);};

  function modernStageNav(m){const cur=lessonStage(m.id),max=lessonMaxStage(m.id);return `<nav class="learning-path-v25">${stageLabels.map(([icon,label],i)=>`<button class="${i===cur?'active':''} ${i<cur?'done':''} ${i<=max?'':'locked'}" ${i<=max?`onclick="setLessonStage('${m.id}',${i})"`:'disabled'}><span>${i<cur?'✓':icon}</span><b>${label}</b><i>${i+1}</i></button>`).join('')}<div class="learning-path-line"><span style="width:${cur/4*100}%"></span></div></nav>`;}
  lessonStageNav=modernStageNav;

  missionScreen=function(){
    const m=mission(state.currentMission)||currentMission(),l=lessonData(m.id),ch=chapterForMission(m.id),idx=chapterMissions(ch).findIndex(x=>x.id===m.id),globalIdx=missionIndex(m.id);if(!l)return shell(`<div class="empty">Для миссии не найден учебный материал.</div>`);
    const progress=Math.round((lessonStage(m.id)+1)/5*100),theory=theoryState(m.id);
    return shell(`<section class="learning-shell-v25 reveal"><header class="learning-top-v25"><button class="learning-exit-v25" onclick="go('campaign')">←</button><div class="learning-title-v25"><small>${activeCampaignLabel()} · ГЛАВА ${ch.number} · УРОК ${idx+1}</small><h1>${m.title}</h1></div><div class="learning-score-v25"><b>${progress}%</b><span>${l.duration} мин</span></div></header>${modernStageNav(m)}<div class="learning-grid-v25"><main class="learning-focus-v25">${lessonBody(m,l)}</main><aside class="learning-side-v25"><div class="learning-side-card"><small>ЦЕЛИ УРОКА</small>${l.objectives.map(x=>`<p>✓ ${esc(x)}</p>`).join('')}</div><div class="learning-side-card"><small>ПРОГРЕСС</small><div><span>Этап</span><b>${lessonStage(m.id)+1}/5</b></div><div><span>Теория</span><b>${theory.percent||0}%</b></div><div><span>Статус</span><b>${missionCompleted(m.id)?'готово':'в процессе'}</b></div></div><button class="btn secondary" onclick="resetStudyPath()">Сменить эпоху</button></aside></div><footer class="learning-dock-v25">${globalIdx>0?`<button onclick="openMission('${CAMPAIGN.nodes[globalIdx-1].id}')">← Предыдущий</button>`:'<span></span>'}<button onclick="go('campaign')">Все уроки</button>${globalIdx<CAMPAIGN.nodes.length-1&&missionOpen(CAMPAIGN.nodes[globalIdx+1].id)?`<button onclick="openMission('${CAMPAIGN.nodes[globalIdx+1].id}')">Следующий →</button>`:'<span></span>'}</footer></section>`);
  };

  const oldCampaign=campaign;
  campaign=function(){let html=oldCampaign();return html.replace('<section class="compact-mission-list reveal">',`<div class="study-route-bar reveal"><span>${worldEra(worldCampaign(activeCampaignId())?.eraId)?.title||'Эпоха'}</span><button onclick="resetStudyPath()">Сменить эпоху</button></div><section class="compact-mission-list reveal">`);};

  const oldRender=render;
  render=function(){if(isFresh()&&state.tab==='home'){state.studyOnboardingSeen=true;state.tab='world';state.worldView='CAMPAIGNS';state.worldDepth='ERAS';state.worldEra=null;save();}oldRender();};
})();
