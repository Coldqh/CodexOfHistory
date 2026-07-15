/* Codex v6.9.0 — Babylon and early Bronze Age */
(()=>{
  const V='6.9.0';
  window.CODEX_VERSION=V;
  V22_CAMPAIGN_CODES.BABYLON_OLD='BABYLON';
  state.bronzeMapMode=state.bronzeMapMode==='ERA'?'ERA':'CAMPAIGN';
  state.babylonExam=state.babylonExam||{};

  const oldSync=syncActiveCampaignRuntime;
  syncActiveCampaignRuntime=function(){
    oldSync();
    if(activeCampaignId()!=='BABYLON_OLD')return;
    const first=CAMPAIGN.nodes[0];
    (first?.cards||[]).forEach(id=>{if(!state.unlocked.includes(id))state.unlocked.push(id);});
    CODEX_CONFIG.maps=state.bronzeMapMode==='ERA'?(CODEX_MAPS.BRONZE_WORLD||CODEX_MAPS.BABYLON_OLD):CODEX_MAPS.BABYLON_OLD;
  };

  const oldNoun=activeCampaignNoun;
  activeCampaignNoun=function(){return activeCampaignId()==='BABYLON_OLD'?'БРОНЗОВЫЙ ВЕК':oldNoun();};
  const oldPackTitle=activeCampaignPackTitle;
  activeCampaignPackTitle=function(){return activeCampaignId()==='BABYLON_OLD'?'Вавилонский архивный пак':oldPackTitle();};
  const oldPackCover=activeCampaignPackCover;
  activeCampaignPackCover=function(){return activeCampaignId()==='BABYLON_OLD'?'assets/packs/babylon-pack.svg':oldPackCover();};

  function babylon(){return CODEX_CAMPAIGNS.BABYLON_OLD;}
  function bronzeLayer(){return babylon()?.eraLayer||{};}
  function bronzeRegionProgress(region){return region.status==='PLAYABLE'&&typeof campaignProgressFor==='function'?campaignProgressFor(region.campaignId):0;}

  window.setBronzeMapMode=function(mode){
    state.bronzeMapMode=mode==='ERA'?'ERA':'CAMPAIGN';
    if(state.bronzeMapMode==='CAMPAIGN'&&!CAMPAIGN.chapters.some(ch=>ch.id===state.mapChapter))state.mapChapter=CAMPAIGN.chapters[0].id;
    save();render();
  };
  window.focusBronzeRegion=function(id){
    const region=bronzeLayer().regions?.find(x=>x.id===id);if(!region)return;
    const run=()=>{
      const action=region.status==='PLAYABLE'?`<button onclick="startWorldCampaign('${region.campaignId}')">Открыть кампанию</button>`:'<small>Кампания пока в плане</small>';
      focusMapPoint(id,region.zoom||5,`<div class="map-popup bronze-popup"><b>${esc(region.title)}</b><span>${esc(region.summary)}</span><small>${region.status==='PLAYABLE'?`Прогресс: ${bronzeRegionProgress(region)}%`:'Следующая ветка эпохи'}</small>${action}</div>`);
      state.bronzeRegion=id;save();
      document.querySelectorAll('[data-bronze-region]').forEach(el=>el.classList.toggle('active',el.dataset.bronzeRegion===id));
    };
    if(state.bronzeMapMode!=='ERA'){state.bronzeMapMode='ERA';save();render();setTimeout(run,180);}else run();
  };

  function modeTabs(){return `<div class="bronze-map-tabs"><button class="${state.bronzeMapMode==='CAMPAIGN'?'active':''}" onclick="setBronzeMapMode('CAMPAIGN')">Карта кампании</button><button class="${state.bronzeMapMode==='ERA'?'active':''}" onclick="setBronzeMapMode('ERA')">Обзор эпохи</button></div>`;}
  function regionStrip(){
    return `<section class="bronze-region-panel reveal"><div class="section-head"><div><small>ЦАРСТВА БРОНЗОВОГО ВЕКА</small><h2>Шесть регионов</h2></div><span>одна эпоха, разные процессы</span></div><div class="bronze-region-grid">${(bronzeLayer().regions||[]).map((r,i)=>`<button data-bronze-region="${r.id}" class="${state.bronzeRegion===r.id?'active':''}" onclick="focusBronzeRegion('${r.id}')"><span>${['𒆍','𓂀','𒆜','ϟ','𒈗','◇'][i]||'◇'}</span><div><b>${r.title}</b><small>${r.status==='PLAYABLE'?`${bronzeRegionProgress(r)}% пройдено`:'в плане'} · ${r.summary}</small></div></button>`).join('')}</div></section>`;
  }
  function parallelTimeline(){
    return `<section class="bronze-parallel reveal"><div class="section-head"><div><small>ПАРАЛЛЕЛЬНАЯ ХРОНОЛОГИЯ</small><h2>Мир между 2000 и 1600 годами до н. э.</h2></div><span>интервалы не равны точной синхронности</span></div><div class="parallel-table-wrap"><table><thead><tr><th>Период</th><th>Вавилония</th><th>Египет</th><th>Анатолия</th><th>Эгейский мир</th><th>Сирия и Левант</th></tr></thead><tbody>${(bronzeLayer().parallelTimeline||[]).map(x=>`<tr><th><b>${x.date}</b><small>${x.certainty}</small></th><td>${x.BABYLONIA}</td><td>${x.EGYPT}</td><td>${x.ANATOLIA}</td><td>${x.AEGEAN}</td><td>${x.LEVANT}</td></tr>`).join('')}</tbody></table></div></section>`;
  }

  const oldHome=home;
  home=function(){
    syncActiveCampaignRuntime();if(activeCampaignId()!=='BABYLON_OLD')return oldHome();
    const m=currentMission(),ch=chapterForMission(m.id),owned=state.unlocked.filter(id=>card(id)?.campaign==='BABYLON').length;
    return shell(`<section class="home-hero home-hero-clean babylon-home reveal"><div class="hero-layout"><div class="hero-content"><div class="eyebrow">Царства бронзового века · Глава ${ch.number}</div><h2>${m.title}</h2><p>${ch.subtitle}</p><div class="hero-actions"><button class="btn" onclick="openMission('${m.id}')">${m.emoji} Продолжить</button><button class="btn secondary" onclick="go('campaign')">Все уроки</button></div></div><div class="babylon-gate"><span>𒆍𒀭</span><i></i><b>2004–1595</b><small>до н. э.</small></div></div></section><section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">𒈗</div><b>${campaignProgress()}%</b><span>кампания</span></div><div class="stat-box"><div class="stat-icon">▤</div><b>${completedMissionCount()}/${CAMPAIGN.nodes.length}</b><span>уроков</span></div><div class="stat-box"><div class="stat-icon">▦</div><b>${owned}/96</b><span>карточек</span></div><div class="stat-box stat-action" onclick="openPackHub()"><div class="stat-icon">✦</div><b>${dailyPackStatusShort()}</b><span>пак дня</span></div></section><section class="daily-home-card reveal" onclick="openDaily()"><div class="daily-home-icon">◷</div><div><div class="eyebrow">Ежедневное обучение</div><h3>${dailyLearningCompleteToday()?'Сессия выполнена':`К повторению: ${dailyDueCards().length}`}</h3><p>${dailyLearningCompleteToday()?'Пак дня доступен.':'Повторение не наказывает за пропущенный день.'}</p></div><button class="btn ${dailyLearningCompleteToday()?'secondary':''}">${dailyLearningCompleteToday()?'Открыть':'Начать'}</button></section>`);
  };

  const oldCampaign=campaign;
  campaign=function(){
    let html=oldCampaign();if(activeCampaignId()!=='BABYLON_OLD')return html;
    html=html.replace(/РИМСКАЯ КАМПАНИЯ|МЕСОПОТАМСКАЯ КАМПАНИЯ|ЕГИПЕТСКАЯ КАМПАНИЯ|СРАВНИТЕЛЬНАЯ КАМПАНИЯ|ИНДСКАЯ КАМПАНИЯ|КАМПАНИЯ РАННЕГО КИТАЯ|КАМПАНИЯ ПЕРВОЙ ЭПОХИ/g,'КАМПАНИЯ БРОНЗОВОГО ВЕКА');
    return html.replace('</div></main><nav',`${parallelTimeline()}</div></main><nav`);
  };

  const oldPacks=packsScreen;
  packsScreen=function(){
    if(activeCampaignId()!=='BABYLON_OLD')return oldPacks();
    const pools=unlockedPools(),available=packPool().filter(c=>!isUnlocked(c.id)).length;
    return shell(`<section class="packs-page-head reveal"><div class="packs-title-block"><div class="eyebrow">Архив · Вавилон и аморейские царства</div><h2>Паки знаний</h2><p>Выпадают только архивные карточки из уже открытых глав этой кампании.</p><div class="fragment-balance compact-fragment-balance"><span>◇</span><b>${state.fragments}</b><small>фрагментов</small></div></div></section><section class="packs-page-grid reveal"><article class="pack-page-card ${dailyPackReady()?'ready':''}"><img src="${packCover('DAILY')}" alt="Архивный пак дня"><div class="pack-page-copy"><small>ЕЖЕДНЕВНЫЙ · 3 КАРТЫ</small><h3>Архивный пак дня</h3><p>${dailyPackReady()?'Готов к открытию.':dailyLearningCompleteToday()?'Сегодня уже открыт.':'Сначала заверши дневную сессию.'}</p>${packAction('DAILY')}</div></article><article class="pack-page-card campaign-pack ${campaignPackStatusClass()}"><img src="assets/packs/babylon-pack.svg" alt="Вавилонский архивный пак"><div class="pack-page-copy"><small>БРОНЗОВЫЙ ВЕК · 4 КАРТЫ</small><h3>Вавилонский архивный пак</h3><p>${campaignPackDescription()}</p><div class="pack-page-meta">${campaignPackMeta()}</div>${campaignPackAction()}</div></article></section>${pools.length?`<section class="section reveal"><div class="section-head"><h2>Открытые пулы</h2><span>${pools.length}</span></div><div class="active-pools compact-pools">${pools.map(p=>{const pr=poolProgress(p);return `<span>${p.title} ${pr.opened}/${pr.total}</span>`;}).join('')}</div></section>`:''}`);
  };

  const oldChapterMapCards=chapterMapCards;
  chapterMapCards=function(){return activeCampaignId()==='BABYLON_OLD'&&state.bronzeMapMode==='ERA'?[]:oldChapterMapCards();};
  const oldMapScreen=mapScreen;
  mapScreen=function(){
    if(activeCampaignId()!=='BABYLON_OLD')return oldMapScreen();
    const opened=[...new Set(CAMPAIGN.nodes.flatMap(n=>n.cards||[]))].map(card).filter(c=>c&&isUnlocked(c.id));
    if(state.bronzeMapMode==='ERA'){
      return shell(`<section class="collection-header compact-collection-head reveal"><div><div class="eyebrow">Глобальная карта второй эпохи</div><h2>Царства бронзового века</h2></div><div class="collection-count">6 регионов</div></section>${modeTabs()}${regionStrip()}<div class="map-shell atlas-clean bronze-atlas reveal"><div id="atlas-map" class="leaflet-map"></div><div class="map-actions"><button class="map-action" onclick="resetAtlasView()" title="Общий обзор">⌂</button></div></div>${parallelTimeline()}`);
    }
    return shell(`<section class="collection-header compact-collection-head reveal"><div><div class="eyebrow">Карта активной кампании</div><h2>Вавилон и аморейские царства</h2></div><div class="collection-count">${opened.length} точек</div></section>${modeTabs()}<div class="map-shell atlas-clean babylon-atlas reveal"><div id="atlas-map" class="leaflet-map"></div><div class="map-actions"><button class="map-action" onclick="resetAtlasView()" title="Вернуть обзор">⌂</button><button class="map-action" onclick="fitAtlasMarkers()" title="Показать точки">◎</button></div></div><section class="section compact-section reveal"><div class="section-head"><h2>Открытые места</h2><span>${opened.length}</span></div><div class="location-grid">${opened.map(c=>`<article class="panel panel-click location-card" onclick="focusAtlasCard('${c.id}')"><small>${c.region}</small><h3>${typeIcon(c.type)} ${c.title}</h3><p>${c.date}</p></article>`).join('')}</div></section>`);
  };

  function babylonExamPassed(m){return (m.campaignExamModules||[]).every(x=>isQuizPassed(x.id));}
  window.openBabylonExamModule=function(quizId,missionId){state.babylonExam.current=quizId;markLessonCheck(missionId,true);save();openQuiz(quizId,missionId);};
  function renderBabylonExam(m){
    const modules=m.campaignExamModules||[],passed=modules.filter(x=>isQuizPassed(x.id)).length,all=passed===modules.length;
    return `<div class="era-exam babylon-exam"><header><small>ИТОГ КАМПАНИИ</small><h3>${all?'Экзамен завершён':`${passed}/${modules.length} модулей`}</h3><p>Карта, хронология, источники и устройство старовавилонского мира проверяются отдельно.</p><div class="progress"><span style="width:${Math.round(passed/Math.max(1,modules.length)*100)}%"></span></div></header><div class="era-exam-grid">${modules.map((x,i)=>{const r=quizResult(x.id),done=isQuizPassed(x.id);return `<article class="${done?'done':''}"><span>${done?'✓':String(i+1).padStart(2,'0')}</span><div><b>${x.title}</b><small>${r?`лучший результат ${r.bestPercent}%`:'5 вопросов'}</small></div><button class="btn ${done?'secondary':''}" onclick="openBabylonExamModule('${x.id}','${m.id}')">${done?'Повторить':'Начать'}</button></article>`;}).join('')}</div>${all?`<button class="btn" onclick="if(!missionCompleted('${m.id}'))completeMission('${m.id}')">Завершить кампанию</button>`:''}</div>`;
  }
  const oldLessonActivity=lessonActivity;
  lessonActivity=function(m,l){
    if(!m.campaignExamModules)return oldLessonActivity(m,l);
    return `<section class="lesson-stage learning-practice"><div class="lesson-stage-head"><div><small>ЭТАП 5</small><h2>Практика и закрепление</h2></div><span class="lesson-stage-number">05</span></div>${renderBabylonExam(m)}<div class="learning-next"><button class="btn ghost" onclick="setLessonStage('${m.id}',3)">← Вернуться к теории</button></div></section>`;
  };
  const oldMissionReady=missionReady;
  missionReady=function(m){return m?.campaignExamModules?lessonCheckPassed(m.id)&&babylonExamPassed(m):oldMissionReady(m);};
  const oldFinishQuiz=finishQuiz;
  finishQuiz=function(){
    const qid=state.currentQuiz,mid=state.quizMissionId;oldFinishQuiz();
    const m=mission(mid);if(m?.campaignExamModules&&isQuizPassed(qid)&&babylonExamPassed(m)&&!missionCompleted(m.id)){completeMission(m.id);showToast('Кампания завершена','Все четыре модуля пройдены','✓');}
  };

  syncActiveCampaignRuntime();save();
})();
