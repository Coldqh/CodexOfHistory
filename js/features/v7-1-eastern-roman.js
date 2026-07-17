/* Codex v8.7.1 — Eastern Roman Empire */
(()=>{
  const V='8.7.1';
  window.CODEX_VERSION=V;
  V22_CAMPAIGN_CODES.EASTERN_ROMAN='EASTERN_ROMAN';
  state.easternRomanPhase=state.easternRomanPhase||'EASTERN_COURT';
  state.easternRomanExam=state.easternRomanExam||{};

  const oldSync=syncActiveCampaignRuntime;
  syncActiveCampaignRuntime=function(){
    oldSync();
    if(activeCampaignId()!=='EASTERN_ROMAN')return;
    const first=CAMPAIGN.nodes[0];
    (first?.cards||[]).forEach(id=>{if(!state.unlocked.includes(id))state.unlocked.push(id);});
    CODEX_CONFIG.maps=CODEX_MAPS.EASTERN_ROMAN||CODEX_CONFIG.maps;
  };

  const oldNoun=activeCampaignNoun;
  activeCampaignNoun=function(){return activeCampaignId()==='EASTERN_ROMAN'?'ВОСТОЧНАЯ РИМСКАЯ ИМПЕРИЯ':oldNoun();};
  const oldPackTitle=activeCampaignPackTitle;
  activeCampaignPackTitle=function(){return activeCampaignId()==='EASTERN_ROMAN'?'Архив Восточной Римской империи':oldPackTitle();};
  const oldPackCover=activeCampaignPackCover;
  activeCampaignPackCover=function(){return activeCampaignId()==='EASTERN_ROMAN'?'assets/packs/eastern-roman-pack.svg':oldPackCover();};

  function phases(){return CODEX_CAMPAIGNS.EASTERN_ROMAN?.eraLayer?.phases||[];}
  function phaseForChapter(number){return phases().find(p=>(p.chapters||[]).includes(number))||phases()[0];}
  function phaseProgress(phase){
    const ids=(phase.chapters||[]).flatMap(n=>CAMPAIGN.chapters.find(ch=>ch.number===n)?.missionIds||[]);
    return Math.round(ids.filter(id=>missionCompleted(id)).length/Math.max(1,ids.length)*100);
  }
  function phaseStrip(){
    return `<section class="assyria-phases reveal">${phases().map(p=>`<button class="${state.easternRomanPhase===p.id?'active':''}" onclick="state.easternRomanPhase='${p.id}';save();render()"><small>${p.date}</small><b>${p.title}</b><i><span style="width:${phaseProgress(p)}%"></span></i></button>`).join('')}</section>`;
  }

  const oldHome=home;
  home=function(){
    syncActiveCampaignRuntime();
    if(activeCampaignId()!=='EASTERN_ROMAN')return oldHome();
    const m=currentMission(),ch=chapterForMission(m.id),phase=phaseForChapter(ch.number),owned=state.unlocked.filter(id=>card(id)?.campaign==='EASTERN_ROMAN').length;
    return shell(`<section class="home-hero home-hero-clean assyria-home reveal"><div class="hero-layout"><div class="hero-content"><div class="eyebrow">Поздняя Античность · ${phase.title}</div><h2>${m.title}</h2><p>${ch.subtitle}</p><div class="hero-actions"><button class="btn" onclick="openMission('${m.id}')">${m.emoji} Продолжить</button><button class="btn secondary" onclick="go('campaign')">Все миссии</button></div></div><div class="assyria-seal"><span>☧</span><b>395–641</b><small>столица и право</small></div></div></section>${phaseStrip()}<section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">V</div><b>${campaignProgress()}%</b><span>кампания</span></div><div class="stat-box"><div class="stat-icon">▤</div><b>${completedMissionCount()}/${CAMPAIGN.nodes.length}</b><span>миссий</span></div><div class="stat-box"><div class="stat-icon">♜</div><b>${owned}/132</b><span>карточек</span></div><div class="stat-box stat-action" onclick="openPackHub()"><div class="stat-icon">✦</div><b>${dailyPackStatusShort()}</b><span>пак дня</span></div></section><section class="daily-home-card reveal" onclick="openDaily()"><div class="daily-home-icon">◷</div><div><div class="eyebrow">Ежедневное обучение</div><h3>${dailyLearningCompleteToday()?'Сессия выполнена':`К повторению: ${dailyDueCards().length}`}</h3><p>${dailyLearningCompleteToday()?'Пак дня доступен.':'Повтори открытые знания за несколько минут.'}</p></div><button class="btn ${dailyLearningCompleteToday()?'secondary':''}">${dailyLearningCompleteToday()?'Открыть':'Начать'}</button></section>`);
  };

  const oldCampaign=campaign;
  campaign=function(){
    let html=oldCampaign();
    if(activeCampaignId()!=='EASTERN_ROMAN')return html;
    html=html.replace(/РИМСКАЯ КАМПАНИЯ|МЕСОПОТАМСКАЯ КАМПАНИЯ|ЕГИПЕТСКАЯ КАМПАНИЯ|КАМПАНИЯ БРОНЗОВОГО ВЕКА|ЖЕЛЕЗНЫЙ ВЕК[^<]*|КЛАССИЧЕСКИЙ МИР[^<]*|ЭЛЛИНИСТИЧЕСКИЙ И РИМСКИЙ МИР[^<]*|ПОЗДНЯЯ АНТИЧНОСТЬ[^<]*/g,'ПОЗДНЯЯ АНТИЧНОСТЬ · ВОСТОЧНАЯ РИМСКАЯ ИМПЕРИЯ');
    return html.replace('</div></main><nav',`${phaseStrip()}</div></main><nav`);
  };

  const oldPacks=packsScreen;
  packsScreen=function(){
    if(activeCampaignId()!=='EASTERN_ROMAN')return oldPacks();
    const pools=unlockedPools();
    return shell(`<section class="packs-page-head reveal"><div class="packs-title-block"><div class="eyebrow">Архив · Восточная Римская империя</div><h2>Паки знаний</h2><p>Выпадают только архивные карточки из уже открытых глав кампании.</p><div class="fragment-balance compact-fragment-balance"><span>◇</span><b>${state.fragments}</b><small>фрагментов</small></div></div></section><section class="packs-page-grid reveal"><article class="pack-page-card ${dailyPackReady()?'ready':''}"><img src="${packCover('DAILY')}" alt="Архивный пак дня"><div class="pack-page-copy"><small>ЕЖЕДНЕВНЫЙ · 3 КАРТЫ</small><h3>Архивный пак дня</h3><p>${dailyPackReady()?'Готов к открытию.':dailyLearningCompleteToday()?'Сегодня уже открыт.':'Сначала заверши дневную сессию.'}</p>${packAction('DAILY')}</div></article><article class="pack-page-card campaign-pack ${campaignPackStatusClass()}"><img src="assets/packs/eastern-roman-pack.svg" alt="Архив Восточной Римской империи"><div class="pack-page-copy"><small>ПОЗДНЯЯ АНТИЧНОСТЬ · 4 КАРТЫ</small><h3>Архив Восточной Римской империи</h3><p>${campaignPackDescription()}</p><div class="pack-page-meta">${campaignPackMeta()}</div>${campaignPackAction()}</div></article></section>${pools.length?`<section class="section reveal"><div class="section-head"><h2>Открытые пулы</h2><span>${pools.length}</span></div><div class="active-pools compact-pools">${pools.map(p=>{const pr=poolProgress(p);return `<span>${p.title} ${pr.opened}/${pr.total}</span>`;}).join('')}</div></section>`:''}`);
  };

  const oldMap=mapScreen;
  mapScreen=function(){
    if(activeCampaignId()!=='EASTERN_ROMAN')return oldMap();
    let html=oldMap().replace('Карта кампании','Карта столицы, границ и имперских войн');
    return html.replace('</div></main><nav',`${phaseStrip()}</div></main><nav`);
  };

  window.openEasternRomanExamModule=function(quizId,missionId){
    state.easternRomanExam.current=quizId;markLessonCheck(missionId,true);save();openQuiz(quizId,missionId);
  };
  const oldActivity=lessonActivity;
  lessonActivity=function(m,l){
    if(!String(m?.id||'').startsWith('ERM_')||!m.campaignExamModules)return oldActivity(m,l);
    const modules=m.campaignExamModules||[],passed=modules.filter(x=>isQuizPassed(x.id)).length,all=passed===modules.length;
    const exam=`<div class="era-exam assyria-exam"><header><small>ИТОГ КАМПАНИИ</small><h3>${all?'Экзамен завершён':`${passed}/${modules.length} модулей`}</h3><p>Карта, хронология, право, ресурсы, войны и критика источников проверяются отдельно.</p><div class="progress"><span style="width:${Math.round(passed/Math.max(1,modules.length)*100)}%"></span></div></header><div class="era-exam-grid">${modules.map((x,i)=>{const r=quizResult(x.id),done=isQuizPassed(x.id);return `<article class="${done?'done':''}"><span>${done?'✓':String(i+1).padStart(2,'0')}</span><div><b>${x.title}</b><small>${r?`лучший результат ${r.bestPercent}%`:'5 вопросов'}</small></div><button class="btn ${done?'secondary':''}" onclick="openEasternRomanExamModule('${x.id}','${m.id}')">${done?'Повторить':'Начать'}</button></article>`;}).join('')}</div>${all?`<button class="btn" onclick="if(!missionCompleted('${m.id}'))completeMission('${m.id}')">Завершить кампанию</button>`:''}</div>`;
    return `<section class="lesson-stage learning-practice"><div class="lesson-stage-head"><div><small>ЭТАП 5</small><h2>Практика и закрепление</h2></div><span class="lesson-stage-number">05</span></div>${exam}<div class="learning-next"><button class="btn ghost" onclick="setLessonStage('${m.id}',3)">← Вернуться к теории</button></div></section>`;
  };

  syncActiveCampaignRuntime();save();
})();
