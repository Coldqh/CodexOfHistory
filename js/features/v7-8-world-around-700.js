/* Codex v8.2.0 — World around 700 comparative exam */
(()=>{
  const V='8.2.0';
  window.CODEX_VERSION=V;
  V22_CAMPAIGN_CODES.WORLD_AROUND_700='WORLD_AROUND_700';
  state.lateWorldRegion=state.lateWorldRegion||'EAST_ROMAN';
  state.lateWorldPhase=state.lateWorldPhase||'SYNCHRONY';
  state.lateWorldExam=state.lateWorldExam||{};

  const oldSync=syncActiveCampaignRuntime;
  syncActiveCampaignRuntime=function(){
    oldSync();
    if(activeCampaignId()!=='WORLD_AROUND_700')return;
    const first=CAMPAIGN.nodes[0];
    (first?.cards||[]).forEach(id=>{if(!state.unlocked.includes(id))state.unlocked.push(id);});
    CODEX_CONFIG.maps=CODEX_MAPS.WORLD_AROUND_700||CODEX_CONFIG.maps;
  };

  const oldNoun=activeCampaignNoun;
  activeCampaignNoun=function(){return activeCampaignId()==='WORLD_AROUND_700'?'ПЕРЕХОД К СРЕДНЕВЕКОВЬЮ · СРАВНИТЕЛЬНЫЙ МИР':oldNoun();};
  const oldPackTitle=activeCampaignPackTitle;
  activeCampaignPackTitle=function(){return activeCampaignId()==='WORLD_AROUND_700'?'Общий архив мира около 700 года':oldPackTitle();};
  const oldPackCover=activeCampaignPackCover;
  activeCampaignPackCover=function(){return activeCampaignId()==='WORLD_AROUND_700'?'assets/packs/world-around-700-pack.svg':oldPackCover();};

  const layer=()=>CODEX_CAMPAIGNS.WORLD_AROUND_700?.eraLayer||{};
  const regionProgress=r=>typeof campaignProgressFor==='function'?campaignProgressFor(r.campaignId):0;
  const phases=()=>layer().phases||[];
  const phaseForChapter=n=>phases().find(p=>(p.chapters||[]).includes(n))||phases()[0];
  const phaseProgress=p=>{const ids=(p.chapters||[]).flatMap(n=>CAMPAIGN.chapters.find(ch=>ch.number===n)?.missionIds||[]);return Math.round(ids.filter(id=>missionCompleted(id)).length/Math.max(1,ids.length)*100);};

  window.focusLateWorldRegion=function(id){
    const r=(layer().regions||[]).find(x=>x.id===id);if(!r)return;
    state.lateWorldRegion=id;save();
    focusMapPoint(r.center,r.zoom||3,`<div class="map-popup dawn-popup"><b>${esc(r.title)}</b><span>${esc(r.summary)}</span><small>Прогресс кампании: ${regionProgress(r)}%</small><button onclick="startWorldCampaign('${r.campaignId}')">Открыть кампанию</button></div>`);
    document.querySelectorAll('[data-late-world-region]').forEach(el=>el.classList.toggle('active',el.dataset.lateWorldRegion===id));
  };

  function phaseStrip(){return `<section class="assyria-phases reveal">${phases().map(p=>`<button class="${state.lateWorldPhase===p.id?'active':''}" onclick="state.lateWorldPhase='${p.id}';save();render()"><small>${p.date}</small><b>${p.title}</b><i><span style="width:${phaseProgress(p)}%"></span></i></button>`).join('')}</section>`;}
  function regionStrip(){const icons={WEST:'♜',EAST_ROMAN:'☩',IRAN:'☀',CENTRAL_ASIA:'↟',INDIA:'☸',CHINA:'漢',RED_SEA:'≋',AMERICAS:'◎'};return `<section class="dawn-region-strip bronze-region-strip reveal"><div class="section-head"><div><small>ГЛОБАЛЬНАЯ КАРТА ОКОЛО 700 ГОДА</small><h2>Восемь самостоятельных регионов</h2></div><span>нажми, чтобы приблизить</span></div><div class="dawn-region-grid classical-region-grid">${(layer().regions||[]).map(r=>`<button data-late-world-region="${r.id}" class="${state.lateWorldRegion===r.id?'active':''}" onclick="focusLateWorldRegion('${r.id}')"><span>${icons[r.id]||'◇'}</span><div><b>${r.title}</b><small>${regionProgress(r)}% · ${r.summary}</small></div></button>`).join('')}</div></section>`;}
  function parallelTimeline(){return `<section class="parallel-era-timeline bronze-parallel-timeline reveal"><div class="section-head"><div><small>ПАРАЛЛЕЛЬНАЯ ХРОНОЛОГИЯ</small><h2>550–750 годы без единого мирового рубежа</h2></div><span>совпадение дат не доказывает прямую связь</span></div><div class="parallel-table-wrap"><table><thead><tr><th>Период</th><th>Запад</th><th>Восточный Рим</th><th>Иран</th><th>Центральная Азия</th><th>Индия</th><th>Китай</th><th>Красное море</th><th>Америки</th></tr></thead><tbody>${(layer().parallelTimeline||[]).map(x=>`<tr><th><b>${x.date}</b><small>${x.certainty}</small></th><td>${x.WEST}</td><td>${x.EAST_ROMAN}</td><td>${x.IRAN}</td><td>${x.CENTRAL_ASIA}</td><td>${x.INDIA}</td><td>${x.CHINA}</td><td>${x.RED_SEA}</td><td>${x.AMERICAS}</td></tr>`).join('')}</tbody></table></div></section>`;}

  const oldHome=home;
  home=function(){
    syncActiveCampaignRuntime();
    if(activeCampaignId()!=='WORLD_AROUND_700')return oldHome();
    const m=currentMission(),ch=chapterForMission(m.id),phase=phaseForChapter(ch.number),owned=state.unlocked.filter(id=>card(id)?.campaign==='WORLD_AROUND_700').length;
    return shell(`<section class="home-hero home-hero-clean bronze-world-home reveal"><div class="hero-layout"><div class="hero-content"><div class="eyebrow">Переход к Средневековью · ${phase.title}</div><h2>${m.title}</h2><p>${ch.subtitle}</p><div class="hero-actions"><button class="btn" onclick="openMission('${m.id}')">${m.emoji} Продолжить</button><button class="btn secondary" onclick="go('campaign')">Все миссии</button></div></div><div class="collapse-seal"><span>∞</span><b>550–750</b><small>восемь регионов на одной шкале</small></div></div></section>${phaseStrip()}<section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">VIII</div><b>${campaignProgress()}%</b><span>экзамен</span></div><div class="stat-box"><div class="stat-icon">▤</div><b>${completedMissionCount()}/${CAMPAIGN.nodes.length}</b><span>миссий</span></div><div class="stat-box"><div class="stat-icon">▦</div><b>${owned}/96</b><span>карточек</span></div><div class="stat-box stat-action" onclick="openPackHub()"><div class="stat-icon">✦</div><b>${dailyPackStatusShort()}</b><span>пак дня</span></div></section>${regionStrip()}<section class="daily-home-card reveal" onclick="openDaily()"><div class="daily-home-icon">◷</div><div><div class="eyebrow">Ежедневное обучение</div><h3>${dailyLearningCompleteToday()?'Сессия выполнена':`К повторению: ${dailyDueCards().length}`}</h3><p>${dailyLearningCompleteToday()?'Пак дня доступен.':'Повтори открытые знания за несколько минут.'}</p></div><button class="btn ${dailyLearningCompleteToday()?'secondary':''}">${dailyLearningCompleteToday()?'Открыть':'Начать'}</button></section>`);
  };

  const oldCampaign=campaign;
  campaign=function(){
    let html=oldCampaign();if(activeCampaignId()!=='WORLD_AROUND_700')return html;
    html=html.replace(/РИМСКАЯ КАМПАНИЯ|МЕСОПОТАМСКАЯ КАМПАНИЯ|ЕГИПЕТСКАЯ КАМПАНИЯ|КАМПАНИЯ БРОНЗОВОГО ВЕКА|ЖЕЛЕЗНЫЙ ВЕК[^<]*|КЛАССИЧЕСКИЙ МИР[^<]*|ЭЛЛИНИСТИЧЕСКИЙ И РИМСКИЙ МИР[^<]*|ПОЗДНЯЯ АНТИЧНОСТЬ[^<]*/g,'ПЕРЕХОД К СРЕДНЕВЕКОВЬЮ · МИР ОКОЛО 700 ГОДА');
    return html.replace('</div></main><nav',`${phaseStrip()}${parallelTimeline()}</div></main><nav`);
  };

  const oldPacks=packsScreen;
  packsScreen=function(){
    if(activeCampaignId()!=='WORLD_AROUND_700')return oldPacks();const pools=unlockedPools();
    return shell(`<section class="packs-page-head reveal"><div class="packs-title-block"><div class="eyebrow">Архив · Мир около 700 года</div><h2>Общий архив эпохи</h2><p>Архивные карточки открываются по мере прохождения сравнительных глав.</p><div class="fragment-balance compact-fragment-balance"><span>◇</span><b>${state.fragments}</b><small>фрагментов</small></div></div></section><section class="packs-page-grid reveal"><article class="pack-page-card ${dailyPackReady()?'ready':''}"><img src="${packCover('DAILY')}" alt="Архивный пак дня"><div class="pack-page-copy"><small>ЕЖЕДНЕВНЫЙ · 3 КАРТЫ</small><h3>Архивный пак дня</h3><p>${dailyPackReady()?'Готов к открытию.':dailyLearningCompleteToday()?'Сегодня уже открыт.':'Сначала заверши дневную сессию.'}</p>${packAction('DAILY')}</div></article><article class="pack-page-card campaign-pack ${campaignPackStatusClass()}"><img src="assets/packs/world-around-700-pack.svg" alt="Мир около 700 года"><div class="pack-page-copy"><small>ИТОГ ЭПОХИ · 4 КАРТЫ</small><h3>Мир около 700 года</h3><p>${campaignPackDescription()}</p><div class="pack-page-meta">${campaignPackMeta()}</div>${campaignPackAction()}</div></article></section>${pools.length?`<section class="section reveal"><div class="section-head"><h2>Открытые пулы</h2><span>${pools.length}</span></div><div class="active-pools compact-pools">${pools.map(p=>{const pr=poolProgress(p);return `<span>${p.title} ${pr.opened}/${pr.total}</span>`;}).join('')}</div></section>`:''}`);
  };

  const oldMap=mapScreen;
  mapScreen=function(){
    if(activeCampaignId()!=='WORLD_AROUND_700')return oldMap();
    const opened=[...new Set(CAMPAIGN.nodes.flatMap(n=>n.cards||[]))].map(card).filter(c=>c&&isUnlocked(c.id));
    return shell(`<section class="collection-header compact-collection-head reveal"><div><div class="eyebrow">Глобальная карта перехода</div><h2>Мир около 700 года</h2></div><div class="collection-count">${opened.length} точек</div></section>${regionStrip()}<div class="map-shell atlas-clean dawn-atlas reveal"><div id="atlas-map" class="leaflet-map"></div><div class="map-actions"><button class="map-action" onclick="resetAtlasView()" title="Общий обзор">⌂</button><button class="map-action" onclick="fitAtlasMarkers()" title="Показать точки">◎</button></div></div>${parallelTimeline()}<section class="section compact-section reveal"><div class="section-head"><h2>Открытые точки</h2><span>${opened.length}</span></div><div class="location-grid">${opened.map(c=>`<article class="panel panel-click location-card" onclick="focusAtlasCard('${c.id}')"><small>${c.region}</small><h3>${typeIcon(c.type)} ${c.title}</h3><p>${c.date}</p></article>`).join('')}</div></section>`);
  };

  window.openLateWorldExamModule=function(quizId,missionId){state.lateWorldExam.current=quizId;markLessonCheck(missionId,true);save();openQuiz(quizId,missionId);};
  const oldActivity=lessonActivity;
  lessonActivity=function(m,l){
    if(!String(m?.id||'').startsWith('WAE_')||!m.lateWorldExamModules)return oldActivity(m,l);
    const modules=m.lateWorldExamModules||[],passed=modules.filter(x=>isQuizPassed(x.id)).length,all=passed===modules.length;
    const exam=`<div class="era-exam assyria-exam"><header><small>СРАВНИТЕЛЬНЫЙ МИР ОКОЛО 700 ГОДА</small><h3>${all?'Экзамен завершён':`${passed}/${modules.length} модулей`}</h3><p>Карта, хронология, власть, хозяйство, религии и исторический метод проверяются отдельно.</p><div class="progress"><span style="width:${Math.round(passed/Math.max(1,modules.length)*100)}%"></span></div></header><div class="era-exam-grid">${modules.map((x,i)=>{const r=quizResult(x.id),done=isQuizPassed(x.id);return `<article class="${done?'done':''}"><span>${done?'✓':String(i+1).padStart(2,'0')}</span><div><b>${x.title}</b><small>${r?`лучший результат ${r.bestPercent}%`:'5 вопросов'}</small></div><button class="btn ${done?'secondary':''}" onclick="openLateWorldExamModule('${x.id}','${m.id}')">${done?'Повторить':'Начать'}</button></article>`;}).join('')}</div>${all?`<button class="btn" onclick="if(!missionCompleted('${m.id}'))completeMission('${m.id}')">Завершить кампанию</button>`:''}</div>`;
    return `<section class="lesson-stage learning-practice"><div class="lesson-stage-head"><div><small>ЭТАП 5</small><h2>Практика и закрепление</h2></div><span class="lesson-stage-number">05</span></div>${exam}<div class="learning-next"><button class="btn ghost" onclick="setLessonStage('${m.id}',3)">← Вернуться к теории</button></div></section>`;
  };

  syncActiveCampaignRuntime();save();
})();
