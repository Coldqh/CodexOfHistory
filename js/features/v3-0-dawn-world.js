/* Codex v3.7.0 — first civilizations shared era layer */
(()=>{
  const V='3.7.0';window.CODEX_VERSION=V;V22_CAMPAIGN_CODES.DAWN_WORLD='CIVILIZATIONS';
  state.eraExam=state.eraExam||{};

  const oldSync=syncActiveCampaignRuntime;
  syncActiveCampaignRuntime=function(){
    oldSync();
    if(activeCampaignId()==='DAWN_WORLD'){
      const first=CAMPAIGN.nodes[0];
      (first?.cards||[]).forEach(id=>{if(!state.unlocked.includes(id))state.unlocked.push(id);});
    }
  };
  const oldNoun=activeCampaignNoun;activeCampaignNoun=function(){return activeCampaignId()==='DAWN_WORLD'?'ПЕРВАЯ ЭПОХА':oldNoun();};
  const oldPackTitle=activeCampaignPackTitle;activeCampaignPackTitle=function(){return activeCampaignId()==='DAWN_WORLD'?'Архивный пак первой эпохи':oldPackTitle();};
  const oldPackCover=activeCampaignPackCover;activeCampaignPackCover=function(){return activeCampaignId()==='DAWN_WORLD'?'assets/packs/civilizations-pack.svg':oldPackCover();};

  function dawnCampaign(){return CODEX_CAMPAIGNS.DAWN_WORLD;}
  function dawnLayer(){return dawnCampaign()?.eraLayer||{};}
  function regionProgress(region){return typeof campaignProgressFor==='function'?campaignProgressFor(region.campaignId):0;}
  window.focusDawnRegion=function(id){
    const region=dawnLayer().regions?.find(x=>x.id===id);if(!region)return;
    focusMapPoint(region.center,region.zoom||5,`<div class="map-popup dawn-popup"><b>${esc(region.title)}</b><span>${esc(region.summary)}</span><small>Прогресс кампании: ${regionProgress(region)}%</small><button onclick="startWorldCampaign('${region.campaignId}')">Открыть кампанию</button></div>`);
    state.dawnRegion=id;save();
    document.querySelectorAll('[data-dawn-region]').forEach(el=>el.classList.toggle('active',el.dataset.dawnRegion===id));
  };
  function regionStrip(){return `<section class="dawn-region-strip reveal"><div class="section-head"><div><small>ГЛОБАЛЬНАЯ КАРТА ЭПОХИ</small><h2>Четыре региона</h2></div><span>нажми, чтобы приблизить</span></div><div class="dawn-region-grid">${(dawnLayer().regions||[]).map(r=>`<button data-dawn-region="${r.id}" class="${state.dawnRegion===r.id?'active':''}" onclick="focusDawnRegion('${r.id}')"><span>${r.id==='MESOPOTAMIA'?'𒀭':r.id==='EGYPT'?'𓂀':r.id==='INDUS'?'◇':'鼎'}</span><div><b>${r.title}</b><small>${regionProgress(r)}% · ${r.summary}</small></div></button>`).join('')}</div></section>`;}
  function parallelTimeline(){return `<section class="parallel-era-timeline reveal"><div class="section-head"><div><small>ПАРАЛЛЕЛЬНАЯ ХРОНОЛОГИЯ</small><h2>Одно время, разные процессы</h2></div><span>широкие интервалы</span></div><div class="parallel-table-wrap"><table><thead><tr><th>Период</th><th>Месопотамия</th><th>Египет</th><th>Инд</th><th>Китай</th></tr></thead><tbody>${(dawnLayer().parallelTimeline||[]).map(x=>`<tr><th><b>${x.date}</b><small>${x.certainty}</small></th><td>${x.MESOPOTAMIA}</td><td>${x.EGYPT}</td><td>${x.INDUS}</td><td>${x.CHINA}</td></tr>`).join('')}</tbody></table></div></section>`;}

  const oldHome=home;
  home=function(){
    syncActiveCampaignRuntime();if(activeCampaignId()!=='DAWN_WORLD')return oldHome();
    const m=currentMission(),ch=chapterForMission(m.id),owned=state.unlocked.filter(id=>card(id)?.campaign==='CIVILIZATIONS').length;
    return shell(`<section class="home-hero home-hero-clean dawn-world-home reveal"><div class="hero-layout"><div class="hero-content"><div class="eyebrow">Рождение цивилизаций · Глава ${ch.number}</div><h2>${m.title}</h2><p>${ch.subtitle}</p><div class="hero-actions"><button class="btn" onclick="openMission('${m.id}')">${m.emoji} Продолжить</button><button class="btn secondary" onclick="go('campaign')">Все уроки</button></div></div><div class="dawn-world-symbols"><span>𒀭</span><span>𓂀</span><span>◇</span><span>鼎</span></div></div></section><section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">◎</div><b>${campaignProgress()}%</b><span>кампания</span></div><div class="stat-box"><div class="stat-icon">▤</div><b>${completedMissionCount()}/${CAMPAIGN.nodes.length}</b><span>уроков</span></div><div class="stat-box"><div class="stat-icon">▦</div><b>${owned}/60</b><span>карточек</span></div><div class="stat-box stat-action" onclick="openPackHub()"><div class="stat-icon">✦</div><b>${dailyPackStatusShort()}</b><span>пак дня</span></div></section><section class="daily-home-card reveal" onclick="openDaily()"><div class="daily-home-icon">◷</div><div><div class="eyebrow">Ежедневное обучение</div><h3>${dailyLearningCompleteToday()?'Сессия выполнена':`К повторению: ${dailyDueCards().length}`}</h3><p>${dailyLearningCompleteToday()?'Пак дня доступен.':'Карточки повторяются по интервалам 1, 3, 7, 14 и 30 дней.'}</p></div><button class="btn ${dailyLearningCompleteToday()?'secondary':''}">${dailyLearningCompleteToday()?'Открыть':'Начать'}</button></section>`);
  };

  const oldCampaign=campaign;
  campaign=function(){
    let html=oldCampaign();if(activeCampaignId()!=='DAWN_WORLD')return html;
    html=html.replace(/РИМСКАЯ КАМПАНИЯ|МЕСОПОТАМСКАЯ КАМПАНИЯ|ЕГИПЕТСКАЯ КАМПАНИЯ|СРАВНИТЕЛЬНАЯ КАМПАНИЯ|ИНДСКАЯ КАМПАНИЯ|КАМПАНИЯ РАННЕГО КИТАЯ/g,'КАМПАНИЯ ПЕРВОЙ ЭПОХИ');
    return html.replace('</div></main><nav',`${parallelTimeline()}</div></main><nav`);
  };

  const oldPacks=packsScreen;
  packsScreen=function(){
    if(activeCampaignId()!=='DAWN_WORLD')return oldPacks();
    const pools=unlockedPools(),available=packPool().filter(c=>!isUnlocked(c.id)).length;
    return shell(`<section class="packs-page-head reveal"><div class="packs-title-block"><div class="eyebrow">Архив · Рождение цивилизаций</div><h2>Паки знаний</h2><p>Выпадают только архивные карточки из уже открытых глав.</p><div class="fragment-balance compact-fragment-balance"><span>◇</span><b>${state.fragments}</b><small>фрагментов</small></div></div></section><section class="packs-page-grid reveal"><article class="pack-page-card ${dailyPackReady()?'ready':''}"><img src="${packCover('DAILY')}" alt="Архивный пак дня"><div class="pack-page-copy"><small>ЕЖЕДНЕВНЫЙ · 3 КАРТЫ</small><h3>Архивный пак дня</h3><p>${dailyPackReady()?'Готов к открытию.':dailyLearningCompleteToday()?'Сегодня уже открыт.':'Сначала заверши дневную сессию.'}</p>${packAction('DAILY')}</div></article><article class="pack-page-card campaign-pack ${campaignPackStatusClass()}"><img src="assets/packs/civilizations-pack.svg" alt="Архивный пак первой эпохи"><div class="pack-page-copy"><small>ПЕРВАЯ ЭПОХА · 4 КАРТЫ</small><h3>Архивный пак первой эпохи</h3><p>${campaignPackDescription()}</p><div class="pack-page-meta">${campaignPackMeta()}</div>${campaignPackAction()}</div></article></section>${pools.length?`<section class="section reveal"><div class="section-head"><h2>Открытые пулы</h2><span>${pools.length}</span></div><div class="active-pools compact-pools">${pools.map(p=>{const pr=poolProgress(p);return `<span>${p.title} ${pr.opened}/${pr.total}</span>`;}).join('')}</div></section>`:''}`);
  };

  const oldMapScreen=mapScreen;
  mapScreen=function(){
    if(activeCampaignId()!=='DAWN_WORLD'){
      const chapterIds=[...new Set(CAMPAIGN.nodes.flatMap(n=>n.cards||[]))],opened=chapterIds.map(card).filter(c=>c&&isUnlocked(c.id));
      return shell(`<section class="collection-header compact-collection-head reveal"><div><div class="eyebrow">Исторический атлас</div><h2>${activeCampaignLabel()}</h2></div><div class="collection-count">${opened.length} точек</div></section><div class="map-shell atlas-clean reveal"><div id="atlas-map" class="leaflet-map"></div><div class="map-actions"><button class="map-action" onclick="resetAtlasView()" title="Вернуть обзор">⌂</button><button class="map-action" onclick="fitAtlasMarkers()" title="Показать точки">◎</button></div></div><section class="section compact-section reveal"><div class="section-head"><h2>Открытые места</h2><span>${opened.length}</span></div><div class="location-grid">${opened.map(c=>`<article class="panel panel-click location-card" onclick="focusAtlasCard('${c.id}')"><small>${c.region}</small><h3>${typeIcon(c.type)} ${c.title}</h3><p>${c.date}</p></article>`).join('')}</div></section>`);
    }
    const opened=[...new Set(CAMPAIGN.nodes.flatMap(n=>n.cards||[]))].map(card).filter(c=>c&&isUnlocked(c.id));
    return shell(`<section class="collection-header compact-collection-head reveal"><div><div class="eyebrow">Глобальная карта первой эпохи</div><h2>Месопотамия, Египет, Инд и Китай</h2></div><div class="collection-count">${opened.length} точек</div></section>${regionStrip()}<div class="map-shell atlas-clean dawn-atlas reveal"><div id="atlas-map" class="leaflet-map"></div><div class="map-actions"><button class="map-action" onclick="resetAtlasView()" title="Общий обзор">⌂</button><button class="map-action" onclick="fitAtlasMarkers()" title="Показать открытые точки">◎</button></div></div>${parallelTimeline()}<section class="section compact-section reveal"><div class="section-head"><h2>Открытые точки</h2><span>${opened.length}</span></div><div class="location-grid">${opened.map(c=>`<article class="panel panel-click location-card" onclick="focusAtlasCard('${c.id}')"><small>${c.region}</small><h3>${typeIcon(c.type)} ${c.title}</h3><p>${c.date}</p></article>`).join('')}</div></section>`);
  };

  function examPassed(m){return (m.examModules||[]).every(x=>isQuizPassed(x.id));}
  window.openEraExamModule=function(quizId,missionId){state.eraExam.current=quizId;save();openQuiz(quizId,missionId);};
  function renderEraExam(m){
    const passed=(m.examModules||[]).filter(x=>isQuizPassed(x.id)).length,all=passed===(m.examModules||[]).length;
    return `<div class="era-exam"><header><small>ЭКЗАМЕН ЭПОХИ</small><h3>${all?'Экзамен завершён':`${passed}/${m.examModules.length} модулей`}</h3><p>Карта, хронология, сравнение, источники, причины и итоговый вывод проходят отдельно.</p><div class="progress"><span style="width:${Math.round(passed/m.examModules.length*100)}%"></span></div></header><div class="era-exam-grid">${m.examModules.map((x,i)=>{const r=quizResult(x.id),done=isQuizPassed(x.id);return `<article class="${done?'done':''}"><span>${done?'✓':String(i+1).padStart(2,'0')}</span><div><b>${x.title}</b><small>${r?`лучший результат ${r.bestPercent}%`:'4 вопроса'}</small></div><button class="btn ${done?'secondary':''}" onclick="openEraExamModule('${x.id}','${m.id}')">${done?'Повторить':'Начать'}</button></article>`;}).join('')}</div>${all?`<button class="btn" onclick="if(!missionCompleted('${m.id}'))completeMission('${m.id}')">Завершить эпоху</button>`:''}</div>`;
  }
  const oldLessonActivity=lessonActivity;
  lessonActivity=function(m,l){
    if(!m.examModules)return oldLessonActivity(m,l);
    return `<section class="lesson-stage learning-practice"><div class="lesson-stage-head"><div><small>ЭТАП 5</small><h2>Практика и закрепление</h2></div><span class="lesson-stage-number">05</span></div>${renderEraExam(m)}<div class="learning-next"><button class="btn ghost" onclick="setLessonStage('${m.id}',3)">← Вернуться к теории</button></div></section>`;
  };
  const oldMissionReady=missionReady;missionReady=function(m){return m?.examModules?lessonCheckPassed(m.id)&&examPassed(m):oldMissionReady(m);};
  const oldFinishQuiz=finishQuiz;
  finishQuiz=function(){
    const qid=state.currentQuiz,mid=state.quizMissionId;oldFinishQuiz();
    const m=mission(mid);if(m?.examModules&&isQuizPassed(qid)&&examPassed(m)&&!missionCompleted(m.id)){completeMission(m.id);showToast('Экзамен эпохи пройден','Все шесть модулей завершены','✓');}
  };

  settingsScreen=function(){
    const dark=state.theme==='night';
    return shell(`<section class="settings-hero compact-settings-hero reveal"><div><div class="eyebrow">Система Codex</div><h2>Настройки</h2><p>Тема, обновление, сохранение и сброс данных.</p></div><div class="version-medallion"><small>ВЕРСИЯ</small><b>v${appVersion()}</b><span>${CARDS.length} карточек</span></div></section><section class="settings-grid compact-settings-grid reveal"><article class="settings-card settings-wide"><div class="settings-card-head"><span>◐</span><div><h3>Тема интерфейса</h3><p>Выбор хранится на этом устройстве.</p></div></div><div class="theme-choice-row"><button class="${dark?'selected':''}" onclick="if(state.theme!=='night')toggleTheme()"><i>☾</i><b>Тёмная тема</b></button><button class="${!dark?'selected':''}" onclick="if(state.theme!=='parchment')toggleTheme()"><i>☀</i><b>Пергаментная тема</b></button></div></article><article class="settings-card"><div class="settings-card-head"><span>↻</span><div><h3>Обновление</h3><p>Очистить кэш и загрузить свежие файлы.</p></div></div><div class="version-table"><span>Версия</span><b>v${appVersion()}</b><span>Активная кампания</span><b>${activeCampaignLabel()}</b><span>Последнее обновление</span><b>${formatSettingDate(preferences.lastForcedRefresh)}</b></div><button class="btn settings-main-btn" onclick="forceRefresh()">↻ Принудительно обновить</button><p class="settings-note">Игровой прогресс не удаляется.</p></article><article class="settings-card"><div class="settings-card-head"><span>▣</span><div><h3>Сохранение</h3><p>Перенос прогресса между браузерами.</p></div></div><div class="settings-actions"><button class="btn secondary" onclick="exportSave()">⇩ Экспорт</button><button class="btn secondary" onclick="requestImport()">⇧ Импорт</button><input id="settings-import" type="file" accept="application/json,.json" hidden onchange="importSave(event)"></div></article><article class="settings-card"><div class="settings-card-head"><span>?</span><div><h3>Обучение</h3><p>Повторно открыть вводный маршрут.</p></div></div><button class="btn secondary" onclick="replayOnboarding()">Запустить обучение заново</button></article><article class="settings-card settings-wide"><div class="settings-card-head"><span>⌁</span><div><h3>Управление данными</h3><p>Настройки и игровой прогресс сбрасываются отдельно.</p></div></div><div class="settings-actions"><button class="btn ghost" onclick="clearInterfacePreferences()">↺ Сбросить настройки</button><button class="btn danger" onclick="resetProgress()">Полный сброс игры</button></div></article></section>`);
  };

  const oldRender=render;
  render=function(){syncActiveCampaignRuntime();oldRender();};
})();
