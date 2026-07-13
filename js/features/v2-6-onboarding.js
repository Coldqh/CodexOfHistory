/* Codex v2.6 — cinematic onboarding for new players */
(function(){
  const V='2.6.0';
  window.CODEX_VERSION=V;
  state.onboardingV26Done=!!state.onboardingV26Done;
  state.onboardingV26Step=Number.isInteger(state.onboardingV26Step)?state.onboardingV26Step:0;
  state.onboardingV26Era=state.onboardingV26Era||null;
  state.onboardingV26Replay=!!state.onboardingV26Replay;
  const realProgress=()=>state.xp>0||(state.missionsCompleted?.length||0)>0||Object.keys(state.quizResults||{}).length>0;
  const shouldShowOnboarding=()=>state.onboardingV26Replay||(!state.onboardingV26Done&&!realProgress());
  const steps=[
    {k:'welcome',n:'01',title:'История становится маршрутом',text:'Codex объединяет глубокие уроки, живую карту, коллекцию и систему повторения. Ты не листаешь справочник — ты последовательно собираешь картину прошлого.',icon:'C'},
    {k:'navigation',n:'02',title:'Всё приложение в одной системе',text:'Каждый раздел отвечает за отдельный способ изучения. Между ними можно свободно переключаться, а прогресс сохраняется автоматически.',icon:'◎'},
    {k:'learning',n:'03',title:'Уроки построены в пять этапов',text:'Сначала ты входишь в тему, затем видишь время и причинные связи, читаешь полную теорию и только после этого закрепляешь материал практикой.',icon:'▤'},
    {k:'cards',n:'04',title:'Карточки — твой исторический архив',text:'Сюжетные карты открываются в кампаниях. Архивные выпадают из паков и раскрывают места, понятия, людей, предметы и локальные истории.',icon:'▦'},
    {k:'routine',n:'05',title:'Знания остаются с тобой',text:'Раздел «Сегодня» возвращает изученные темы через интервалы. Карта показывает географию, а коллекция позволяет быстро восстановить любой факт.',icon:'◷'},
    {k:'era',n:'06',title:'Выбери эпоху',text:'Это определит пространство первого маршрута. Позже ты сможешь сменить эпоху в разделе «Мир» без потери прогресса.',icon:'⌛'},
    {k:'campaign',n:'07',title:'Выбери первую кампанию',text:'Кампания станет активной веткой на главной. Остальные останутся доступными через раздел «Мир».',icon:'▶'}
  ];
  function onboardingEraProgress(era){
    const cs=worldEraCampaigns(era.id).filter(c=>c.status==='PLAYABLE');
    if(!cs.length)return 0;
    return Math.round(cs.reduce((s,c)=>s+campaignProgressFor(c.id),0)/cs.length);
  }
  function onboardingNavPreview(){
    const items=[['◎','Мир','эпохи и кампании'],['♜','Кампания','главы и уроки'],['◷','Сегодня','повторение'],['▦','Коллекция','карточки и архив'],['⌖','Карта','места и маршруты'],['✦','Паки','дополнительные знания']];
    return `<div class="onboarding-feature-grid">${items.map(([i,t,d])=>`<article><span>${i}</span><div><b>${t}</b><small>${d}</small></div></article>`).join('')}</div>`;
  }
  function onboardingLearningPreview(){
    const items=[['▤','Рассказ','короткий вход в тему'],['⌛','Хронология','даты и последовательность'],['◆','Разбор','причины, последствия, понятия'],['▥','Теория','полный нейтральный текст'],['◎','Практика','карта, связи и проверка']];
    return `<div class="onboarding-learning-road">${items.map(([i,t,d],n)=>`<article style="--delay:${n*70}ms"><span>${i}</span><b>${t}</b><small>${d}</small></article>`).join('')}</div>`;
  }
  function onboardingCardPreview(){
    return `<div class="onboarding-card-stage"><article class="onboarding-demo-card story"><div class="onboarding-card-art">♜</div><small>СЮЖЕТНАЯ</small><h3>Главная линия</h3><p>Открывается уроками и ведёт кампанию вперёд.</p></article><article class="onboarding-demo-card archive"><div class="onboarding-card-art">◇</div><small>АРХИВНАЯ</small><h3>Боковая история</h3><p>Выпадает из открытых пулов и расширяет знания.</p></article><div class="onboarding-rarity-line"><i class="common"></i><i class="uncommon"></i><i class="rare"></i><i class="epic"></i><i class="legendary"></i><i class="mythic"></i></div></div>`;
  }
  function onboardingRoutinePreview(){
    return `<div class="onboarding-cycle"><div class="onboarding-cycle-core"><b>5 мин</b><span>в день</span></div><article class="one"><b>1</b><span>Повтори карты</span></article><article class="two"><b>2</b><span>Ответь на вопросы</span></article><article class="three"><b>3</b><span>Получай пак</span></article><article class="four"><b>4</b><span>Продолжай кампанию</span></article></div>`;
  }
  function onboardingEraGrid(){
    return `<div class="onboarding-era-grid">${ERAS.map(era=>{const playable=worldEraCampaigns(era.id).some(c=>c.status==='PLAYABLE'),selected=state.onboardingV26Era===era.id;return `<button class="onboarding-era ${selected?'selected':''} ${playable?'':'planned'}" style="--era-accent:${era.accent}" onclick="selectOnboardingEra('${era.id}')"><img src="${era.cover}" alt=""><div><small>${era.dateLabel}</small><h3>${era.title}</h3><span>${playable?'Есть доступные кампании':'В разработке'}</span></div>${selected?'<b>✓</b>':''}</button>`;}).join('')}</div>`;
  }
  function onboardingCampaignGrid(){
    const era=worldEra(state.onboardingV26Era)||ERAS.find(e=>worldEraCampaigns(e.id).some(c=>c.status==='PLAYABLE'));
    const campaigns=worldEraCampaigns(era.id);
    return `<div class="onboarding-choice-head"><button onclick="onboardingBackToEras()">← Эпохи</button><div><small>${era.dateLabel}</small><h3>${era.title}</h3></div></div><div class="onboarding-campaign-grid">${campaigns.map(c=>{const playable=c.status==='PLAYABLE';return `<button class="onboarding-campaign ${playable?'playable':'planned'}" onclick="${playable?`finishOnboarding('${c.id}')`:`showToast('Кампания в разработке','Выбери доступный маршрут','○')`}"><img src="${campaignCover(c)}" alt=""><div><small>${c.period}</small><h3>${c.title}</h3><span>${playable?`${c.releasedChapters} глав доступно`:'Запланирована'}</span></div><b>${playable?'Начать →':'○'}</b></button>`;}).join('')}</div>`;
  }
  function stepVisual(k){
    if(k==='welcome')return `<div class="onboarding-codex-mark"><div>C</div><i></i><i></i><i></i></div>`;
    if(k==='navigation')return onboardingNavPreview();
    if(k==='learning')return onboardingLearningPreview();
    if(k==='cards')return onboardingCardPreview();
    if(k==='routine')return onboardingRoutinePreview();
    if(k==='era')return onboardingEraGrid();
    if(k==='campaign')return onboardingCampaignGrid();
    return '';
  }
  function onboardingScreen(){
    const index=Math.max(0,Math.min(steps.length-1,state.onboardingV26Step));
    const s=steps[index];
    const isChoice=s.k==='era'||s.k==='campaign';
    const nextDisabled=s.k==='era'&&!state.onboardingV26Era;
    return `<main class="onboarding-v26" data-step="${s.k}"><div class="onboarding-ambient"><i></i><i></i><i></i></div><header class="onboarding-top"><div class="onboarding-brand"><img src="assets/ui/codex-mark.svg" alt=""><div><b>Codex of History</b><small>Первое знакомство</small></div></div><div class="onboarding-version">v${appVersion()}</div></header><section class="onboarding-frame"><div class="onboarding-copy"><div class="onboarding-step-label"><span>${s.n}</span><i></i><b>${String(steps.length).padStart(2,'0')}</b></div><div class="eyebrow">${index===0?'ДОБРО ПОЖАЛОВАТЬ':'КАК РАБОТАЕТ CODEX'}</div><h1>${s.title}</h1><p>${s.text}</p>${!isChoice?`<div class="onboarding-tip"><span>✦</span><p>${index===0?'Весь прогресс хранится автоматически прямо на устройстве.':index===1?'На телефоне разделы находятся в боковом меню.':index===2?'Тест — только финальная часть урока, а не само обучение.':index===3?'Чем выше редкость, тем глубже боковая история и меньше шанс выпадения.':'Пропущенные дни ничего не отнимают.'}</p></div>`:''}</div><div class="onboarding-visual">${stepVisual(s.k)}</div></section><footer class="onboarding-footer"><div class="onboarding-dots">${steps.map((_,i)=>`<i class="${i===index?'active':''} ${i<index?'done':''}"></i>`).join('')}</div><div class="onboarding-actions">${index>0?`<button class="onboarding-back" onclick="onboardingPrev()">← Назад</button>`:'<span></span>'}${index<steps.length-1?`<button class="onboarding-next" onclick="onboardingNext()" ${nextDisabled?'disabled':''}>${s.k==='era'?'К кампаниям':'Дальше'} <span>→</span></button>`:'<span></span>'}</div></footer></main>`;
  }
  window.selectOnboardingEra=function(id){state.onboardingV26Era=id;save();render();};
  window.onboardingNext=function(){
    const s=steps[state.onboardingV26Step];
    if(s?.k==='era'&&!state.onboardingV26Era)return;
    state.onboardingV26Step=Math.min(steps.length-1,state.onboardingV26Step+1);save();render();window.scrollTo({top:0});
  };
  window.onboardingPrev=function(){state.onboardingV26Step=Math.max(0,state.onboardingV26Step-1);save();render();window.scrollTo({top:0});};
  window.onboardingBackToEras=function(){state.onboardingV26Step=5;save();render();};
  window.finishOnboarding=function(campaignId){
    const c=worldCampaign(campaignId);if(!c||c.status!=='PLAYABLE')return;
    state.onboardingV26Done=true;state.onboardingV26Replay=false;state.onboardingV26Step=0;state.onboardingV26Era=c.eraId;state.studyOnboardingSeen=true;state.studyEra=c.eraId;state.studyCampaign=campaignId;save();startWorldCampaign(campaignId);showToast('Маршрут выбран',c.title,'▶');
  };
  window.replayOnboarding=function(){state.onboardingV26Replay=true;state.onboardingV26Step=0;state.onboardingV26Era=null;save();render();};
  const previousSettings=settingsScreen;
  settingsScreen=function(){
    let html=previousSettings();
    const block=`<article class="settings-card"><div class="settings-card-head"><span>◎</span><div><h3>Обучение интерфейсу</h3><p>Повтори знакомство с разделами, уроками, карточками и выбором кампании.</p></div></div><button class="btn secondary settings-main-btn" onclick="replayOnboarding()">Запустить обучение заново</button></article>`;
    return html.replace('<article class="settings-card settings-wide settings-about">',block+'<article class="settings-card settings-wide settings-about">');
  };
  const previousRender=render;
  render=function(){
    if(shouldShowOnboarding()){
      destroyMaps();applyTheme();document.body?.classList?.add?.('onboarding-active');document.getElementById('app').innerHTML=onboardingScreen();requestAnimationFrame(()=>initEnhancements());return;
    }
    document.body?.classList?.remove?.('onboarding-active');previousRender();
  };
})();
