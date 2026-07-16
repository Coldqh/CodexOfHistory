/* Codex v8.7.0 — complete Rome campaign: Republic, principate, high empire and western transformation */
(()=>{
  const V='8.7.0';
  window.CODEX_VERSION=V;
  state.romeMiddlePhase=state.romeMiddlePhase||'FOUNDATIONS';
  state.romeCheckpoint=state.romeCheckpoint||{};

  const phases=[
    {id:'FOUNDATIONS',title:'Основание и ранняя Республика',date:'VIII–IV века до н. э.',chapters:[1,2]},
    {id:'ITALY',title:'Борьба за Италию',date:'IV–III века до н. э.',chapters:[3]},
    {id:'PUNIC',title:'Пунические войны',date:'264–201 до н. э.',chapters:[4]},
    {id:'EAST',title:'Восточное Средиземноморье',date:'215–146 до н. э.',chapters:[5]},
    {id:'SYSTEM',title:'Механика Республики',date:'III–II века до н. э.',chapters:[6]},
    {id:'GRACCHI',title:'Гракхи и социальный кризис',date:'133–121 до н. э.',chapters:[7]},
    {id:'ARMIES',title:'Марий, союзники и Сулла',date:'112–79 до н. э.',chapters:[8]},
    {id:'CIVIL',title:'Цезарь и гражданская война',date:'70–44 до н. э.',chapters:[9]},
    {id:'AUGUSTUS',title:'Август и принципат',date:'44 до н. э. – 14 н. э.',chapters:[10]},
    {id:'HIGH',title:'Расцвет Империи',date:'14–180 н. э.',chapters:[11]},
    {id:'LATE',title:'Поздняя Империя и Запад',date:'193–476 н. э.',chapters:[12]}
  ];
  function isRome(){return activeCampaignId()==='ROME_CAMPAIGN';}
  function phaseForChapter(number){return phases.find(p=>p.chapters.includes(number))||phases[0];}
  function phaseProgress(phase){
    const ids=phase.chapters.flatMap(n=>CAMPAIGN.chapters.find(ch=>ch.number===n)?.missionIds||[]);
    return Math.round(ids.filter(id=>missionCompleted(id)).length/Math.max(1,ids.length)*100);
  }
  function phaseStrip(){
    return `<section class="assyria-phases rome-middle-phases reveal">${phases.map(p=>`<button class="${state.romeMiddlePhase===p.id?'active':''}" onclick="state.romeMiddlePhase='${p.id}';save();render()"><small>${p.date}</small><b>${p.title}</b><i><span style="width:${phaseProgress(p)}%"></span></i></button>`).join('')}</section>`;
  }

  const oldSync=syncActiveCampaignRuntime;
  syncActiveCampaignRuntime=function(){
    oldSync();
    if(!isRome())return;
    CODEX_CONFIG.maps=CODEX_MAPS.ROME_CAMPAIGN||CODEX_CONFIG.maps;
    const m=mission(state.currentMission)||currentMission();
    const ch=chapterForMission(m?.id);
    if(ch)state.romeMiddlePhase=phaseForChapter(ch.number).id;
  };

  const oldHome=home;
  home=function(){
    syncActiveCampaignRuntime();
    if(!isRome())return oldHome();
    const m=currentMission(),ch=chapterForMission(m.id),phase=phaseForChapter(ch.number),owned=state.unlocked.filter(id=>card(id)?.campaign==='ROME').length;
    return shell(`<section class="home-hero home-hero-clean assyria-home reveal"><div class="hero-layout"><div class="hero-content"><div class="eyebrow">Рим · ${phase.title}</div><h2>${m.title}</h2><p>${ch.subtitle}</p><div class="hero-actions"><button class="btn" onclick="openMission('${m.id}')">${m.emoji} Продолжить</button><button class="btn secondary" onclick="go('campaign')">Все миссии</button></div></div><div class="assyria-seal"><span>SPQR</span><b>${ch.number}/12</b><small>глава</small></div></div></section>${phaseStrip()}<section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">♜</div><b>${campaignProgress()}%</b><span>кампания</span></div><div class="stat-box"><div class="stat-icon">▤</div><b>${completedMissionCount()}/${CAMPAIGN.nodes.length}</b><span>миссий</span></div><div class="stat-box"><div class="stat-icon">⌂</div><b>${owned}</b><span>римских карточек</span></div><div class="stat-box stat-action" onclick="openPackHub()"><div class="stat-icon">✦</div><b>${dailyPackStatusShort()}</b><span>пак дня</span></div></section><section class="daily-home-card reveal" onclick="openDaily()"><div class="daily-home-icon">◷</div><div><div class="eyebrow">Ежедневное обучение</div><h3>${dailyLearningCompleteToday()?'Сессия выполнена':`К повторению: ${dailyDueCards().length}`}</h3><p>${dailyLearningCompleteToday()?'Пак дня доступен.':'Повтори открытые знания за несколько минут.'}</p></div><button class="btn ${dailyLearningCompleteToday()?'secondary':''}">${dailyLearningCompleteToday()?'Открыть':'Начать'}</button></section>`);
  };

  const oldCampaign=campaign;
  campaign=function(){
    let html=oldCampaign();
    if(!isRome())return html;
    html=html.replace(/РИМСКАЯ КАМПАНИЯ/g,'РИМ · ОТ РЕСПУБЛИКИ К ИМПЕРИИ');
    return html.replace('</div></main><nav',`${phaseStrip()}</div></main><nav`);
  };

  const oldMap=mapScreen;
  mapScreen=function(){
    if(!isRome())return oldMap();
    let html=oldMap().replace('Карта кампании','Карта Римского мира');
    return html.replace('</div></main><nav',`${phaseStrip()}</div></main><nav`);
  };

  window.openRomeCheckpointModule=function(quizId,missionId){
    state.romeCheckpoint.current=quizId;markLessonCheck(missionId,true);save();openQuiz(quizId,missionId);
  };
  const oldActivity=lessonActivity;
  lessonActivity=function(m,l){
    if(!m?.romeCheckpointModules&&!m?.romeFinalModules)return oldActivity(m,l);
    const finalExam=Array.isArray(m.romeFinalModules),modules=finalExam?m.romeFinalModules:(m.romeCheckpointModules||[]),passed=modules.filter(x=>isQuizPassed(x.id)).length,all=passed===modules.length;
    const late=String(m.id).startsWith('ROM_09_');
    const checkpointTitle=finalExam?'Римская кампания завершена':late?'Поздняя Республика закреплена':'Средняя Республика закреплена';
    const checkpointText=finalExam?'Шесть модулей проверяют географию, хронологию, Республику, принципат, позднюю Империю и работу с источниками.':late?'Карта, хронология, социальный кризис, армии и критика источников проверяются отдельно.':'Карта, хронология, устройство Республики и критика источников проверяются отдельно.';
    const exam=`<div class="era-exam assyria-exam"><header><small>${finalExam?'ФИНАЛЬНЫЙ ЭКЗАМЕН':'КОНТРОЛЬНАЯ ТОЧКА'}</small><h3>${all?checkpointTitle:`${passed}/${modules.length} модулей`}</h3><p>${checkpointText}</p><div class="progress"><span style="width:${Math.round(passed/Math.max(1,modules.length)*100)}%"></span></div></header><div class="era-exam-grid">${modules.map((x,i)=>{const r=quizResult(x.id),done=isQuizPassed(x.id);return `<article class="${done?'done':''}"><span>${done?'✓':String(i+1).padStart(2,'0')}</span><div><b>${x.title}</b><small>${r?`лучший результат ${r.bestPercent}%`:'5 вопросов'}</small></div><button class="btn ${done?'secondary':''}" onclick="openRomeCheckpointModule('${x.id}','${m.id}')">${done?'Повторить':'Начать'}</button></article>`;}).join('')}</div>${all?`<button class="btn" onclick="if(!missionCompleted('${m.id}'))completeMission('${m.id}')">${finalExam?'Завершить римскую кампанию':'Завершить главу'}</button>`:''}</div>`;
    return `<section class="lesson-stage learning-practice"><div class="lesson-stage-head"><div><small>ЭТАП 5</small><h2>Практика и закрепление</h2></div><span class="lesson-stage-number">05</span></div>${exam}<div class="learning-next"><button class="btn ghost" onclick="setLessonStage('${m.id}',3)">← Вернуться к теории</button></div></section>`;
  };

  syncActiveCampaignRuntime();save();
})();
