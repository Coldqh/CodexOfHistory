/* Codex v5.1.0 — Egypt from Middle to New Kingdom */
(()=>{
  const V='5.1.0';
  window.CODEX_VERSION=V;
  V22_CAMPAIGN_CODES.EGYPT_MIDDLE_NEW='EGYPT_BRONZE';
  state.egyptBronzePhase=state.egyptBronzePhase||'MIDDLE';
  state.egyptBronzeExam=state.egyptBronzeExam||{};

  const oldSync=syncActiveCampaignRuntime;
  syncActiveCampaignRuntime=function(){
    oldSync();
    if(activeCampaignId()!=='EGYPT_MIDDLE_NEW')return;
    const first=CAMPAIGN.nodes[0];
    (first?.cards||[]).forEach(id=>{if(!state.unlocked.includes(id))state.unlocked.push(id);});
    CODEX_CONFIG.maps=CODEX_MAPS.EGYPT_MIDDLE_NEW||CODEX_CONFIG.maps;
  };

  const oldNoun=activeCampaignNoun;
  activeCampaignNoun=function(){return activeCampaignId()==='EGYPT_MIDDLE_NEW'?'ЕГИПЕТ БРОНЗОВОГО ВЕКА':oldNoun();};
  const oldPackTitle=activeCampaignPackTitle;
  activeCampaignPackTitle=function(){return activeCampaignId()==='EGYPT_MIDDLE_NEW'?'Египетский архив Среднего и Нового царства':oldPackTitle();};
  const oldPackCover=activeCampaignPackCover;
  activeCampaignPackCover=function(){return activeCampaignId()==='EGYPT_MIDDLE_NEW'?'assets/packs/egypt-bronze-pack.svg':oldPackCover();};

  function phases(){return CODEX_CAMPAIGNS.EGYPT_MIDDLE_NEW?.eraLayer?.phases||[];}
  function phaseForChapter(number){return phases().find(p=>(p.chapters||[]).includes(number))||phases()[0];}
  function phaseProgress(phase){
    const ids=(phase.chapters||[]).flatMap(n=>CAMPAIGN.chapters.find(ch=>ch.number===n)?.missionIds||[]);
    return Math.round(ids.filter(id=>missionCompleted(id)).length/Math.max(1,ids.length)*100);
  }
  function phaseStrip(){
    return `<section class="egypt-bronze-phases reveal">${phases().map(p=>`<button class="${state.egyptBronzePhase===p.id?'active':''}" onclick="state.egyptBronzePhase='${p.id}';save();render()"><small>${p.date}</small><b>${p.title}</b><i><span style="width:${phaseProgress(p)}%"></span></i></button>`).join('')}</section>`;
  }

  const oldHome=home;
  home=function(){
    syncActiveCampaignRuntime();
    if(activeCampaignId()!=='EGYPT_MIDDLE_NEW')return oldHome();
    const m=currentMission(),ch=chapterForMission(m.id),phase=phaseForChapter(ch.number),owned=state.unlocked.filter(id=>card(id)?.campaign==='EGYPT_BRONZE').length;
    return shell(`<section class="home-hero home-hero-clean egypt-bronze-home reveal"><div class="hero-layout"><div class="hero-content"><div class="eyebrow">Царства бронзового века · ${phase.title}</div><h2>${m.title}</h2><p>${ch.subtitle}</p><div class="hero-actions"><button class="btn" onclick="openMission('${m.id}')">${m.emoji} Продолжить</button><button class="btn secondary" onclick="go('campaign')">Все миссии</button></div></div><div class="egypt-bronze-seal"><span>𓂀</span><b>2055–1070</b><small>до н. э.</small></div></div></section>${phaseStrip()}<section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">𓋹</div><b>${campaignProgress()}%</b><span>кампания</span></div><div class="stat-box"><div class="stat-icon">▤</div><b>${completedMissionCount()}/${CAMPAIGN.nodes.length}</b><span>миссий</span></div><div class="stat-box"><div class="stat-icon">𓂀</div><b>${owned}/120</b><span>карточек</span></div><div class="stat-box stat-action" onclick="openPackHub()"><div class="stat-icon">✦</div><b>${dailyPackStatusShort()}</b><span>пак дня</span></div></section><section class="daily-home-card reveal" onclick="openDaily()"><div class="daily-home-icon">◷</div><div><div class="eyebrow">Ежедневное обучение</div><h3>${dailyLearningCompleteToday()?'Сессия выполнена':`К повторению: ${dailyDueCards().length}`}</h3><p>${dailyLearningCompleteToday()?'Пак дня доступен.':'Повторение не наказывает за пропущенный день.'}</p></div><button class="btn ${dailyLearningCompleteToday()?'secondary':''}">${dailyLearningCompleteToday()?'Открыть':'Начать'}</button></section>`);
  };

  const oldCampaign=campaign;
  campaign=function(){
    let html=oldCampaign();
    if(activeCampaignId()!=='EGYPT_MIDDLE_NEW')return html;
    html=html.replace(/РИМСКАЯ КАМПАНИЯ|МЕСОПОТАМСКАЯ КАМПАНИЯ|ЕГИПЕТСКАЯ КАМПАНИЯ|КАМПАНИЯ БРОНЗОВОГО ВЕКА/g,'ЕГИПЕТ · СРЕДНЕЕ И НОВОЕ ЦАРСТВА');
    return html.replace('</div></main><nav',`${phaseStrip()}</div></main><nav`);
  };

  const oldPacks=packsScreen;
  packsScreen=function(){
    if(activeCampaignId()!=='EGYPT_MIDDLE_NEW')return oldPacks();
    const pools=unlockedPools(),available=packPool().filter(c=>!isUnlocked(c.id)).length;
    return shell(`<section class="packs-page-head reveal"><div class="packs-title-block"><div class="eyebrow">Архив · Египет Среднего и Нового царства</div><h2>Паки знаний</h2><p>Выпадают только архивные карточки из уже открытых глав этой кампании.</p><div class="fragment-balance compact-fragment-balance"><span>◇</span><b>${state.fragments}</b><small>фрагментов</small></div></div></section><section class="packs-page-grid reveal"><article class="pack-page-card ${dailyPackReady()?'ready':''}"><img src="${packCover('DAILY')}" alt="Архивный пак дня"><div class="pack-page-copy"><small>ЕЖЕДНЕВНЫЙ · 3 КАРТЫ</small><h3>Архивный пак дня</h3><p>${dailyPackReady()?'Готов к открытию.':dailyLearningCompleteToday()?'Сегодня уже открыт.':'Сначала заверши дневную сессию.'}</p>${packAction('DAILY')}</div></article><article class="pack-page-card campaign-pack ${campaignPackStatusClass()}"><img src="assets/packs/egypt-bronze-pack.svg" alt="Египетский архив"><div class="pack-page-copy"><small>ЕГИПЕТ · 4 КАРТЫ</small><h3>Архив Среднего и Нового царства</h3><p>${campaignPackDescription()}</p><div class="pack-page-meta">${campaignPackMeta()}</div>${campaignPackAction()}</div></article></section>${pools.length?`<section class="section reveal"><div class="section-head"><h2>Открытые пулы</h2><span>${pools.length}</span></div><div class="active-pools compact-pools">${pools.map(p=>{const pr=poolProgress(p);return `<span>${p.title} ${pr.opened}/${pr.total}</span>`;}).join('')}</div></section>`:''}`);
  };

  const oldMapScreen=mapScreen;
  mapScreen=function(){
    if(activeCampaignId()!=='EGYPT_MIDDLE_NEW')return oldMapScreen();
    let html=oldMapScreen();
    html=html.replace('Карта кампании','Карта Египта и его внешних связей');
    return html.replace('</div></main><nav',`${phaseStrip()}</div></main><nav`);
  };

  window.openEgyptBronzeExamModule=function(quizId,missionId){
    state.egyptBronzeExam.current=quizId;
    markLessonCheck(missionId,true);
    save();openQuiz(quizId,missionId);
  };
  const priorLessonActivity=lessonActivity;
  lessonActivity=function(m,l){
    if(!String(m?.id||'').startsWith('EMN_')||!m.campaignExamModules)return priorLessonActivity(m,l);
    const modules=m.campaignExamModules||[],passed=modules.filter(x=>isQuizPassed(x.id)).length,all=passed===modules.length;
    const exam=`<div class="era-exam egypt-bronze-exam"><header><small>ИТОГ КАМПАНИИ</small><h3>${all?'Экзамен завершён':`${passed}/${modules.length} модулей`}</h3><p>Карта, хронология, источники и устройство Египта проверяются отдельно.</p><div class="progress"><span style="width:${Math.round(passed/Math.max(1,modules.length)*100)}%"></span></div></header><div class="era-exam-grid">${modules.map((x,i)=>{const r=quizResult(x.id),done=isQuizPassed(x.id);return `<article class="${done?'done':''}"><span>${done?'✓':String(i+1).padStart(2,'0')}</span><div><b>${x.title}</b><small>${r?`лучший результат ${r.bestPercent}%`:'5 вопросов'}</small></div><button class="btn ${done?'secondary':''}" onclick="openEgyptBronzeExamModule('${x.id}','${m.id}')">${done?'Повторить':'Начать'}</button></article>`;}).join('')}</div>${all?`<button class="btn" onclick="if(!missionCompleted('${m.id}'))completeMission('${m.id}')">Завершить кампанию</button>`:''}</div>`;
    return `<section class="lesson-stage learning-practice"><div class="lesson-stage-head"><div><small>ЭТАП 5</small><h2>Практика и закрепление</h2></div><span class="lesson-stage-number">05</span></div>${exam}<div class="learning-next"><button class="btn ghost" onclick="setLessonStage('${m.id}',3)">← Вернуться к теории</button></div></section>`;
  };

  syncActiveCampaignRuntime();save();
})();
