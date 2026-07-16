/* Codex v8.0.0 — Iron Age shared comparative layer and era exam */
(()=>{
  const V='8.0.0';
  window.CODEX_VERSION=V;
  V22_CAMPAIGN_CODES.IRON_ERA_EXAM='IRON_WORLD';
  state.ironWorldRegion=state.ironWorldRegion||'ASSYRIA';

  const oldSync=syncActiveCampaignRuntime;
  syncActiveCampaignRuntime=function(){
    oldSync();
    if(activeCampaignId()!=='IRON_ERA_EXAM')return;
    const first=CAMPAIGN.nodes[0];
    (first?.cards||[]).forEach(id=>{if(!state.unlocked.includes(id))state.unlocked.push(id);});
    CODEX_CONFIG.maps=CODEX_MAPS.IRON_ERA_EXAM||CODEX_CONFIG.maps;
  };
  const oldNoun=activeCampaignNoun;
  activeCampaignNoun=function(){return activeCampaignId()==='IRON_ERA_EXAM'?'ЭПОХА III · ЖЕЛЕЗНЫЙ ВЕК':oldNoun();};
  const oldPackTitle=activeCampaignPackTitle;
  activeCampaignPackTitle=function(){return activeCampaignId()==='IRON_ERA_EXAM'?'Общий архив железного века':oldPackTitle();};
  const oldPackCover=activeCampaignPackCover;
  activeCampaignPackCover=function(){return activeCampaignId()==='IRON_ERA_EXAM'?'assets/packs/iron-era-pack.svg':oldPackCover();};

  const layer=()=>CODEX_CAMPAIGNS.IRON_ERA_EXAM?.eraLayer||{};
  const regionProgress=region=>typeof campaignProgressFor==='function'?campaignProgressFor(region.campaignId):0;
  window.focusIronWorldRegion=function(id){
    const region=(layer().regions||[]).find(x=>x.id===id);if(!region)return;
    state.ironWorldRegion=id;save();
    focusMapPoint(region.center,region.zoom||5,`<div class="map-popup dawn-popup"><b>${esc(region.title)}</b><span>${esc(region.summary)}</span><small>Прогресс кампании: ${regionProgress(region)}%</small><button onclick="startWorldCampaign('${region.campaignId}')">Открыть кампанию</button></div>`);
    document.querySelectorAll('[data-iron-region]').forEach(el=>el.classList.toggle('active',el.dataset.ironRegion===id));
  };
  function regionStrip(){
    const icons={ASSYRIA:'𒀭',PHOENICIA:'≋',LEVANT:'⌂',GREECE:'Ω',ZHOU:'鼎',INDIA:'ऋ'};
    return `<section class="dawn-region-strip bronze-region-strip reveal"><div class="section-head"><div><small>КАРТА ТРЕТЬЕЙ ЭПОХИ</small><h2>Шесть связанных кампаний</h2></div><span>нажми, чтобы приблизить</span></div><div class="dawn-region-grid">${(layer().regions||[]).map(r=>`<button data-iron-region="${r.id}" class="${state.ironWorldRegion===r.id?'active':''}" onclick="focusIronWorldRegion('${r.id}')"><span>${icons[r.id]||'◇'}</span><div><b>${r.title}</b><small>${regionProgress(r)}% · ${r.summary}</small></div></button>`).join('')}</div></section>`;
  }
  function parallelTimeline(){
    return `<section class="parallel-era-timeline bronze-parallel-timeline reveal"><div class="section-head"><div><small>ПАРАЛЛЕЛЬНАЯ ХРОНОЛОГИЯ</small><h2>Шесть регионов на одной шкале</h2></div><span>датировки заданы интервалами</span></div><div class="parallel-table-wrap"><table><thead><tr><th>Период</th><th>Ассирия</th><th>Финикия</th><th>Левант</th><th>Греция</th><th>Чжоу</th><th>Индия</th></tr></thead><tbody>${(layer().parallelTimeline||[]).map(x=>`<tr><th><b>${x.date}</b><small>${x.certainty}</small></th><td>${x.ASSYRIA}</td><td>${x.PHOENICIA}</td><td>${x.LEVANT}</td><td>${x.GREECE}</td><td>${x.ZHOU}</td><td>${x.INDIA}</td></tr>`).join('')}</tbody></table></div></section>`;
  }

  const oldHome=home;
  home=function(){
    syncActiveCampaignRuntime();
    if(activeCampaignId()!=='IRON_ERA_EXAM')return oldHome();
    const m=currentMission(),ch=chapterForMission(m.id),owned=state.unlocked.filter(id=>card(id)?.campaign==='IRON_WORLD').length;
    return shell(`<section class="home-hero home-hero-clean bronze-world-home reveal"><div class="hero-layout"><div class="hero-content"><div class="eyebrow">Железный век · итог третьей эпохи</div><h2>${m.title}</h2><p>${ch.subtitle}</p><div class="hero-actions"><button class="btn" onclick="openMission('${m.id}')">${m.emoji} Продолжить</button><button class="btn secondary" onclick="go('campaign')">Все миссии</button></div></div><div class="collapse-seal"><span>⚒</span><b>1200–500</b><small>до н. э.</small></div></div></section><section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">◎</div><b>${campaignProgress()}%</b><span>кампания</span></div><div class="stat-box"><div class="stat-icon">▤</div><b>${completedMissionCount()}/${CAMPAIGN.nodes.length}</b><span>миссий</span></div><div class="stat-box"><div class="stat-icon">▦</div><b>${owned}/96</b><span>карточек</span></div><div class="stat-box stat-action" onclick="openPackHub()"><div class="stat-icon">✦</div><b>${dailyPackStatusShort()}</b><span>пак дня</span></div></section>${regionStrip()}<section class="daily-home-card reveal" onclick="openDaily()"><div class="daily-home-icon">◷</div><div><div class="eyebrow">Ежедневное обучение</div><h3>${dailyLearningCompleteToday()?'Сессия выполнена':`К повторению: ${dailyDueCards().length}`}</h3><p>${dailyLearningCompleteToday()?'Пак дня доступен.':'Повтори открытые знания за несколько минут.'}</p></div><button class="btn ${dailyLearningCompleteToday()?'secondary':''}">${dailyLearningCompleteToday()?'Открыть':'Начать'}</button></section>`);
  };
  const oldCampaign=campaign;
  campaign=function(){
    let html=oldCampaign();if(activeCampaignId()!=='IRON_ERA_EXAM')return html;
    html=html.replace(/РИМСКАЯ КАМПАНИЯ|МЕСОПОТАМСКАЯ КАМПАНИЯ|ЕГИПЕТСКАЯ КАМПАНИЯ|КАМПАНИЯ БРОНЗОВОГО ВЕКА|ЕГИПЕТ · СРЕДНЕЕ И НОВОЕ ЦАРСТВА|МИНОЙЦЫ · МИКЕНЦЫ · ЭГЕЙСКИЙ МИР|КРИЗИС · РАЗРУШЕНИЕ · ПЕРЕХОД|ЖЕЛЕЗНЫЙ ВЕК · [^<]+/g,'ОБЩИЙ ЭКЗАМЕН ТРЕТЬЕЙ ЭПОХИ');
    return html.replace('</div></main><nav',`${parallelTimeline()}</div></main><nav`);
  };
  const oldMap=mapScreen;
  mapScreen=function(){
    if(activeCampaignId()!=='IRON_ERA_EXAM')return oldMap();
    const opened=[...new Set(CAMPAIGN.nodes.flatMap(n=>n.cards||[]))].map(card).filter(c=>c&&isUnlocked(c.id));
    return shell(`<section class="collection-header compact-collection-head reveal"><div><div class="eyebrow">Глобальная карта третьей эпохи</div><h2>Империи, города и региональные сети</h2></div><div class="collection-count">${opened.length} точек</div></section>${regionStrip()}<div class="map-shell atlas-clean dawn-atlas reveal"><div id="atlas-map" class="leaflet-map"></div><div class="map-actions"><button class="map-action" onclick="resetAtlasView()" title="Общий обзор">⌂</button><button class="map-action" onclick="fitAtlasMarkers()" title="Показать точки">◎</button></div></div>${parallelTimeline()}<section class="section compact-section reveal"><div class="section-head"><h2>Открытые точки</h2><span>${opened.length}</span></div><div class="location-grid">${opened.map(c=>`<article class="panel panel-click location-card" onclick="focusAtlasCard('${c.id}')"><small>${c.region}</small><h3>${typeIcon(c.type)} ${c.title}</h3><p>${c.date}</p></article>`).join('')}</div></section>`);
  };
  window.openIronExamModule=function(quizId,missionId){state.ironExamCurrent=quizId;markLessonCheck(missionId,true);save();openQuiz(quizId,missionId);};
  const oldActivity=lessonActivity;
  lessonActivity=function(m,l){
    if(!String(m?.id||'').startsWith('IRN_')||!m.examModules)return oldActivity(m,l);
    const modules=m.examModules||[],passed=modules.filter(x=>isQuizPassed(x.id)).length,all=passed===modules.length;
    const exam=`<div class="era-exam assyria-exam"><header><small>ИТОГ ЭПОХИ</small><h3>${all?'Экзамен завершён':`${passed}/${modules.length} модулей`}</h3><p>Карта, хронология, государство, письмо, сети и исторический метод проверяются отдельно.</p><div class="progress"><span style="width:${Math.round(passed/Math.max(1,modules.length)*100)}%"></span></div></header><div class="era-exam-grid">${modules.map((x,i)=>{const r=quizResult(x.id),done=isQuizPassed(x.id);return `<article class="${done?'done':''}"><span>${done?'✓':String(i+1).padStart(2,'0')}</span><div><b>${x.title}</b><small>${r?`лучший результат ${r.bestPercent}%`:'5 вопросов'}</small></div><button class="btn ${done?'secondary':''}" onclick="openIronExamModule('${x.id}','${m.id}')">${done?'Повторить':'Начать'}</button></article>`;}).join('')}</div>${all?`<button class="btn" onclick="if(!missionCompleted('${m.id}'))completeMission('${m.id}')">Завершить эпоху</button>`:''}</div>`;
    return `<section class="lesson-stage learning-practice"><div class="lesson-stage-head"><div><small>ЭТАП 5</small><h2>Практика и закрепление</h2></div><span class="lesson-stage-number">05</span></div>${exam}<div class="learning-next"><button class="btn ghost" onclick="setLessonStage('${m.id}',3)">← Вернуться к теории</button></div></section>`;
  };
  syncActiveCampaignRuntime();save();
})();
