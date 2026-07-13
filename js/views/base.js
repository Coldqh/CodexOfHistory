/* Codex v1.5 — base UI shell and screen renderers */
function navButtons(cls=''){
  return NAV.map(([id,ico,label])=>{const active=state.tab===id||(state.tab==='mission'&&id==='campaign');return `<button class="${cls} ${active?'active':''}" onclick="go('${id}')"><span>${ico}</span>${label}</button>`;}).join('');
}
function themeToggle(){
  const light=state.theme==='parchment';
  return `<button class="theme-toggle ${light?'is-light':''}" onclick="toggleTheme()" title="Переключить тему" aria-label="Переключить тему"><span class="theme-track"><i>☾</i><i>☀</i><b></b></span><em>${light?'Пергамент':'Ночь'}</em></button>`;
}
function shell(inner){
  const [section,title]=pageTitle();
  return `<div class="app-layout">
    <aside class="side-nav">
      <div class="brand-mark"><div class="seal">C</div><div class="brand-title"><small>Codex of History</small><h1>История</h1></div></div>
      <div class="nav-kicker">Навигация</div>
      <div class="nav-list">${navButtons('nav-btn')}</div>
      <div class="side-card">
        <div class="side-level"><strong>${state.level}</strong><em>УРОВЕНЬ</em></div>
        <p>${state.xp} XP · ${state.unlocked.length} из ${CARDS.length} карточек открыто</p>
        <div class="progress"><span style="width:${levelProgress()}%"></span></div>
        <div class="side-credit"><span>до нового уровня</span><span>${500-(state.xp%500)} XP</span></div>
        <div class="side-version"><span>Codex</span><b>v${appVersion()}</b></div>
      </div>
    </aside>
    <main class="main-wrap">
      <header class="command-bar">
        <div class="command-title"><span>${section}</span><span>·</span><b>${title}</b></div>
        <div class="command-actions">${themeToggle()}<div class="command-pill version-pill">v${appVersion()}</div><div class="command-pill">${state.level} уровень</div><div class="command-pill">${state.xp} XP</div><button class="command-icon" onclick="go('settings')" title="Настройки">⚙</button><button class="command-icon" onclick="openPack()" title="Открыть пак">✦</button></div>
      </header>
      <div class="top-mobile"><div class="mobile-brand"><img src="assets/ui/codex-mark.svg" alt=""><div><b>Codex</b><small>v${appVersion()}</small></div></div><div class="mobile-tools"><button class="mobile-command" onclick="toggleTheme()" title="Сменить тему">${state.theme==='parchment'?'☀':'☾'}</button><button class="mobile-command" onclick="go('settings')" title="Настройки">⚙</button></div></div>
      <div class="view">${inner}</div>
    </main>
    <nav class="mobile-tabs">${navButtons('')}</nav>
  </div>`;
}
function cardBadges(c, withDate=true){
  return `<div class="card-tags"><span class="badge gold">${rarityLabel(c.rarity)}</span><span class="badge">${typeIcon(c.type)} ${typeLabel(c.type)}</span>${withDate?`<span class="badge">${c.date}</span>`:''}</div>`;
}

function home(){
  const m=currentMission();
  return shell(`<section class="home-hero reveal">
    <div class="hero-layout">
      <div class="hero-content">
        <div class="eyebrow">Глава I · Рождение Рима</div>
        <h2>От легенды о волчице<br><span>к падению царей.</span></h2>
        <p>Семь связанных миссий: карточки, мифы, карта, сабиняне, религия, этрусский город, хронология и финальный экзамен.</p>
        <div class="hero-actions">
          <button class="btn" onclick="openMission('${m.id}')">${m.emoji} Продолжить: ${m.title}</button>
          <button class="btn secondary" onclick="go('collection')">▦ Коллекция главы</button>
        </div>
      </div>
      <div class="hero-orbit">
        <div class="orbit-core"><div class="core-value"><strong>${campaignProgress()}%</strong><span>первая глава</span></div></div>
        <div class="orbit-chip one">Миссии<b>${completedMissionCount()}/${CAMPAIGN.nodes.length}</b></div>
        <div class="orbit-chip two">Средний квиз<b>${averageQuiz()}%</b></div>
        <div class="orbit-chip three">Изучено<b>${state.read.length}</b></div>
      </div>
    </div>
  </section>
  <section class="home-stats reveal">
    <div class="stat-box"><div class="stat-icon">▦</div><b>${state.unlocked.length}/${CARDS.length}</b><span>карточек открыто</span></div>
    <div class="stat-box"><div class="stat-icon">✦</div><b>${state.read.length}</b><span>карточек изучено</span></div>
    <div class="stat-box"><div class="stat-icon">✓</div><b>${completedMissionCount()}/${CAMPAIGN.nodes.length}</b><span>миссий завершено</span></div>
    <div class="stat-box"><div class="stat-icon">♜</div><b>${campaignProgress()}%</b><span>глава пройдена</span></div>
  </section>`);
}

function campaign(){
  const current=currentMission();
  return shell(`<section class="campaign-header reveal birth-header">
    <div class="campaign-copy">
      <div class="eyebrow">Вертикальный срез · полноценная глава</div>
      <h2>${CAMPAIGN.title}</h2>
      <p>${CAMPAIGN.description}</p>
      <div class="hero-actions"><button class="btn" onclick="openMission('${current.id}')">${current.emoji} Продолжить миссию</button><button class="btn secondary" onclick="go('map')">⌖ Открыть атлас</button></div>
    </div>
    <div class="campaign-progress-card">
      <div class="campaign-ring" style="--p:${campaignProgress()}"><strong>${campaignProgress()}%</strong></div>
      <p>${completedMissionCount()} из ${CAMPAIGN.nodes.length} миссий завершено<br>Финальный зачёт — от ${PASS_PERCENT}%.</p>
    </div>
  </section>
  <section class="section reveal"><div class="section-head"><h2>Маршрут первой главы</h2><span>Карточки · карта · хронология · квизы</span></div>
    <div class="mission-road">${CAMPAIGN.nodes.map((m,i)=>{
      const open=missionOpen(m.id),done=missionCompleted(m.id),active=m.id===current.id;
      const detail=m.quiz&&quizResult(m.quiz)?`${quizResult(m.quiz).bestPercent}% лучший результат`:missionTypeLabel(m.type);
      return `<article class="mission-node ${open?'':'lock'} ${done?'done':''} ${active?'active':''}" onclick="${open?`openMission('${m.id}')`:''}"><span class="mission-line"></span><div class="mission-emblem">${done?'✓':m.emoji}</div><div class="mission-order">МИССИЯ ${String(i+1).padStart(2,'0')}</div><h3>${m.title}</h3><p>${m.description}</p><div class="mission-meta"><span>${detail}</span><b>+${m.xp} XP</b></div><button class="btn ${done?'secondary':''}" ${open?'':'disabled'}>${done?'Повторить':active?'Продолжить':'Открыть'}</button></article>`;
    }).join('')}</div>
  </section>`);
}

function missionScreen(){
  const m=mission(state.currentMission)||currentMission(); const done=missionCompleted(m.id); const idx=missionIndex(m.id);
  const cardsHtml=m.cards.map(id=>card(id)).filter(Boolean).map(renderMiniCard).join('');
  let activity='';
  if(m.type==='READ'){
    const read=m.cards.filter(id=>state.read.includes(id)).length;
    activity=`<div class="mission-action panel"><div class="eyebrow">Задача</div><h3>Изучи все карточки миссии</h3><p>Открой каждую карточку и прочитай основные факты. Прогресс: <b>${read}/${m.cards.length}</b>.</p><div class="progress"><span style="width:${Math.round(read/m.cards.length*100)}%"></span></div><button class="btn" ${read===m.cards.length?`onclick="finishReadMission('${m.id}')"`:'disabled'}>${done?'Миссия завершена':'Завершить изучение'}</button></div>`;
  } else if(m.type==='QUIZ'||m.type==='FINAL'){
    const r=quizResult(m.quiz);
    activity=`<div class="mission-action panel"><div class="eyebrow">${m.type==='FINAL'?'Финальный экзамен':'Испытание'}</div><h3>${QUIZZES[m.quiz].title}</h3><p>${r?`Лучший результат: <b>${r.bestPercent}%</b>. ${r.passed?'Зачёт получен.':'Нужно минимум '+PASS_PERCENT+'%.'}`:'Проверь понимание миссии. Зачёт начинается от '+PASS_PERCENT+'%.'}</p><button class="btn" onclick="openQuiz('${m.quiz}','${m.id}')">${r?'Пройти ещё раз':'Начать испытание'} →</button></div>`;
  } else if(m.type==='MAP'){
    const task=state.mapTasks[m.id]||{step:0,mistakes:0,passed:false};
    const ask=task.passed?'География пройдена':task.step===0?'Найди Лаций на карте':'Приблизь Рим и найди Палатин';
    activity=`<div class="mission-action panel map-mission"><div class="eyebrow">Настоящая интерактивная карта</div><h3>${ask}</h3><p>Перетаскивай карту мышью или пальцем, приближай колёсиком, жестом или кнопками. Ошибок: <b id="map-error-count">${task.mistakes||0}</b>.</p><div class="map-shell mission-map-shell"><div id="mission-map" class="leaflet-map" data-mission="${m.id}"></div><div class="map-toolbar"><div class="eyebrow">Задание</div><h3>${ask}</h3><p>${task.step===0?'Нажми внутри выделенной территории древнего Лация.':'Найди отмеченную область Палатина внутри современного Рима.'}</p><div class="map-progress"><i class="${task.step>0?'done':''}"></i><i class="${task.passed?'done':''}"></i><b>${task.passed?'2/2':task.step+'/2'}</b></div></div><div class="map-legend"><span><i class="region-dot"></i> исторические области</span><span><i></i> места и карточки</span><span>© OpenStreetMap</span></div></div></div>`;
  } else if(m.type==='TIMELINE'){
    const task=state.timelineTasks[m.id]||{selected:[],passed:false};
    const options=TIMELINE_ORDER.slice().sort((a,b)=>['superbus','foundation','expulsion','numa','tarquin'].indexOf(a)-['superbus','foundation','expulsion','numa','tarquin'].indexOf(b));
    activity=`<div class="mission-action panel"><div class="eyebrow">Хронологическая сборка</div><h3>${task.passed?'Цепочка собрана':'Нажимай события от раннего к позднему'}</h3><div class="timeline-picked">${task.selected.length?task.selected.map((k,i)=>`<span><b>${i+1}</b>${TIMELINE_LABELS[k]}</span>`).join(''):'<em>Здесь появится выбранная последовательность</em>'}</div><div class="timeline-options">${options.filter(k=>!task.selected.includes(k)).map(k=>`<button onclick="chooseTimeline('${m.id}','${k}')">${TIMELINE_LABELS[k]}</button>`).join('')}</div><button class="btn secondary" onclick="undoTimeline('${m.id}')" ${!task.selected.length?'disabled':''}>← Отменить последний</button></div>`;
  }
  return shell(`<section class="mission-hero reveal"><div><div class="eyebrow">Миссия ${idx+1} из ${CAMPAIGN.nodes.length} · ${missionTypeLabel(m.type)}</div><h2>${m.emoji} ${m.title}</h2><p>${m.description}</p><div class="mission-reward"><span>Награда</span><b>+${m.xp} XP</b><span>${(m.unlockCards||[]).length} новых карточек</span></div></div><div class="mission-seal ${done?'done':''}">${done?'✓':String(idx+1).padStart(2,'0')}</div></section>
  <section class="section reveal"><div class="section-head"><h2>Материалы миссии</h2><span>${m.cards.length} карточек</span></div><div class="card-grid mission-cards">${cardsHtml}</div></section>
  <section class="section reveal">${activity}</section>
  <section class="mission-footer reveal"><button class="btn ghost" onclick="go('campaign')">← Ко всем миссиям</button>${idx>0?`<button class="btn secondary" onclick="openMission('${CAMPAIGN.nodes[idx-1].id}')">Предыдущая</button>`:''}${idx<CAMPAIGN.nodes.length-1&&missionOpen(CAMPAIGN.nodes[idx+1].id)?`<button class="btn" onclick="openMission('${CAMPAIGN.nodes[idx+1].id}')">Следующая →</button>`:''}</section>`);
}

function renderMiniCard(c){
  const locked=!isUnlocked(c.id);
  return `<article class="history-card tilt ${locked?'lock':''}" ${locked?'':`onclick="openCard('${c.id}')"`}>
    <div class="image-card">${locked?'<img src="assets/ui/fallback-card.svg" alt="Закрытая карточка">':imgTag(c)}<span class="rarity-flag">${locked?'не открыта':rarityLabel(c.rarity)}</span><span class="card-number">${cardNumber(c)}</span></div>
    <div class="card-body"><div class="card-kicker"><span>${locked?'???':typeIcon(c.type)+' '+typeLabel(c.type)}</span><span>${locked?'закрыто':c.era}</span></div><h3>${locked?'Закрытая карточка':c.title}</h3><p>${locked?'Продвигайся по кампании или открой пак, чтобы получить эту карточку.':c.summary}</p><div class="card-tags">${(locked?['неизвестно']:c.tags.slice(0,3)).map(t=>`<span class="tag">${t}</span>`).join('')}</div></div>
  </article>`;
}
function collection(){
  const types=['ALL',...new Set(CARDS.map(c=>c.type))];
  const rarities=['ALL',...new Set(CARDS.map(c=>c.rarity))];
  const s=state.search.toLowerCase();
  const list=CARDS.filter(c=>(state.filter==='ALL'||c.type===state.filter)&&(state.rarity==='ALL'||c.rarity===state.rarity)&&(c.title.toLowerCase().includes(s)||c.original.toLowerCase().includes(s)||c.tags.join(' ').toLowerCase().includes(s)));
  return shell(`<section class="collection-header reveal"><div><div class="eyebrow">Твой архив знаний</div><h2>Коллекция</h2></div><div class="collection-count">${list.length} карточек найдено</div></section>
    <div class="search-row reveal"><div class="field-wrap"><input id="collection-search" placeholder="Цезарь, Канны, сенат..." value="${esc(state.search)}" oninput="updateSearch(this)"></div><select onchange="setFilter('filter',this.value)">${types.map(t=>`<option value="${t}" ${state.filter===t?'selected':''}>${t==='ALL'?'Все типы':typeLabel(t)}</option>`).join('')}</select><select onchange="setFilter('rarity',this.value)">${rarities.map(r=>`<option value="${r}" ${state.rarity===r?'selected':''}>${r==='ALL'?'Все редкости':rarityLabel(r)}</option>`).join('')}</select></div>
    <div class="card-grid reveal">${list.map(renderMiniCard).join('')}</div>`);
}

function detail(){
  const c=currentCard();
  const edges=RELATIONS.filter(r=>r.source===c.id||r.target===c.id);
  return shell(`<div class="detail-grid">
    <main class="detail-main">
      <div class="detail-cover reveal">${imgTag(c)}<div class="detail-title">${cardBadges(c)}<h2>${c.title}</h2><p>${c.subtitle} · ${c.region}</p></div></div>
      <section class="section info-pair reveal"><div class="panel info-panel"><div class="eyebrow">Коротко</div><h3>Суть карточки</h3><p>${c.summary}</p></div><div class="panel info-panel"><div class="eyebrow">Контекст</div><h3>Почему это важно</h3><p>${c.importance}</p></div></section>
      <section class="section reveal"><div class="section-head"><h2>Три опорных факта</h2><span>${c.era}</span></div><div class="fact-list">${c.facts.map(f=>`<div class="fact">${f}</div>`).join('')}</div></section>
      <section class="section reveal"><div class="section-head"><h2>Связи в истории</h2><span>${edges.length} узлов</span></div><div class="edge-list">${edges.map(r=>{const other=card(r.source===c.id?r.target:r.source);return `<article class="edge" onclick="openCard('${other.id}')"><b>${r.type.replaceAll('_',' ')}</b><strong>${other.title}</strong><br>${r.description}</article>`;}).join('')||'<div class="empty">Связей пока нет.</div>'}</div></section>
    </main>
    <aside class="detail-aside">
      <div class="panel reveal"><div class="eyebrow">Профиль знания</div><h3>Учебные характеристики</h3><div class="bars">${Object.entries(c.stats).map(([k,v])=>`<div class="bar-row"><span>${STAT_LABELS[k]||k}</span><div class="bar-bg"><div class="bar-fill" style="width:${v*10}%"></div></div><b>${v}</b></div>`).join('')}</div></div>
      <div class="panel reveal"><div class="eyebrow">Источник изображения</div><h3>${c.image.caption}</h3><p class="credit">${c.image.credit} · ${c.image.license}</p><div class="hero-actions"><a class="btn ghost" href="${filePage(c.image.file)}" target="_blank" rel="noreferrer">Открыть источник ↗</a></div></div>
      <div class="panel reveal"><div class="eyebrow">Навигация</div><div class="hero-actions" style="margin:0 0 14px"><button class="btn secondary" onclick="openMission(state.currentMission)">← Вернуться к миссии</button></div><h3>Теги карточки</h3><div class="card-tags">${c.tags.map(t=>`<span class="tag">#${t}</span>`).join('')}</div></div>
    </aside>
  </div>`);
}

function quiz(){
  const qz=currentQuiz();
  if(state.quizFinished && state.quizLastResult){
    const r=state.quizLastResult;
    return shell(`<section class="quiz-focus reveal"><div class="quiz-card quiz-result ${r.lastPassed?'passed':'failed'}"><div class="result-mark">${r.lastPassed?'✓':'↻'}</div><div class="eyebrow" style="justify-content:center">Результат испытания</div><h2>${r.lastPassed?'Глава пройдена':'Нужна ещё попытка'}</h2><div class="score-display">${r.percent}% <small>${r.score}/${r.total} верно</small></div><div class="progress"><span style="width:${r.percent}%"></span></div><p class="muted">Зачёт начинается от ${PASS_PERCENT}%. Твой лучший результат: ${r.bestPercent}%.</p><div class="hero-actions" style="justify-content:center"><button class="btn" onclick="openQuiz('${r.quizId}')">↻ Пройти ещё раз</button><button class="btn secondary" onclick="state.quizMissionId?openMission(state.quizMissionId):go('campaign')">♜ Вернуться к миссии</button></div></div></section>`);
  }
  const q=currentQuestion(); const picked=state.selected!==null;
  const questionProgress=Math.round((state.quizIndex+1)/qz.questions.length*100);
  return shell(`<section class="quiz-focus reveal"><div class="quiz-topline"><div class="quiz-title"><div class="eyebrow">Испытание главы</div><h2>${qz.title}</h2></div><div class="quiz-counter">${state.quizIndex+1}/${qz.questions.length}</div></div><div class="quiz-card"><div class="quiz-meter"><span>Правильно сейчас: ${state.quizScore}</span><b>зачёт от ${PASS_PERCENT}%</b></div><div class="progress" style="margin-bottom:27px"><span style="width:${questionProgress}%"></span></div><h3 class="question">${q.text}</h3><div class="answers">${q.answers.map((a,i)=>`<button data-key="${String.fromCharCode(65+i)}" class="answer ${picked?(i===q.correct?'correct':(i===state.selected?'wrong':'')):''}" onclick="answer(${i})">${a}</button>`).join('')}</div>${picked?`<div class="explain">${q.explanation}</div><button class="btn" onclick="nextQuestion()">${state.quizIndex<qz.questions.length-1?'Следующий вопрос →':'Завершить испытание'}</button>`:''}</div></section>`);
}

function mapScreen(){
  const chapterIds=[...new Set(CAMPAIGN.nodes.flatMap(n=>n.cards))];
  const opened=chapterIds.map(card).filter(c=>c&&isUnlocked(c.id));
  return shell(`<section class="collection-header reveal"><div><div class="eyebrow">Живой исторический атлас</div><h2>Лаций и ранний Рим</h2></div><div class="collection-count">${opened.length} узлов открыто</div></section>
  <div class="map-shell reveal"><div id="atlas-map" class="leaflet-map"></div><div class="map-toolbar"><div class="eyebrow">Интерактивная карта</div><h3>Перемещайся по настоящей карте</h3><p>Приближай Рим, открывай маркеры карточек и изучай соседние области. Исторические границы показаны учебными контурами поверх современной географии.</p></div><div class="map-actions"><button class="map-action" onclick="resetAtlasView()" title="Вернуться к Риму">⌂</button><button class="map-action" onclick="fitAtlasMarkers()" title="Показать все открытые точки">◎</button></div><div class="map-legend"><span><i class="region-dot"></i> исторические области</span><span><i></i> открытые карточки</span><span>колесо / жест — масштаб</span></div></div>
  <section class="section reveal"><div class="section-head"><h2>Ключевые пространства</h2><span>Нажми карточку — карта откроет досье</span></div><div class="location-grid">${opened.map(c=>`<article class="panel panel-click location-card" onclick="openCard('${c.id}')"><small>${c.region}</small><h3>${typeIcon(c.type)} ${c.title}</h3><p>${c.date}</p></article>`).join('')}</div></section>`);
}

function profile(){
  return shell(`<section class="profile-hero reveal"><div class="profile-main"><div class="eyebrow">Личная хроника</div><h2>Хранитель Codex</h2><p>Твой прогресс живёт прямо в браузере. Каждая карточка, глава и попытка формируют личную карту знаний.</p><div class="profile-level"><b>${state.level}</b><span>уровень исследователя<br>${state.xp} опыта</span></div><div class="hero-actions"><button class="btn secondary" onclick="go('settings')">⚙ Настройки</button><button class="btn danger" onclick="resetProgress()">↺ Сбросить прогресс</button><a class="btn ghost" href="docs/PATCH_NOTES_v1_3.md" target="_blank">Что нового ↗</a></div></div><div class="achievement-card"><div class="achievement-medal">${campaignProgress()===100?'♛':'✦'}</div><h3>${campaignProgress()===100?'Покоритель Рима':'Исследователь Рима'}</h3><p>${campaignProgress()===100?'Первая кампания полностью завершена.':'Заверши все главы первой кампании, чтобы получить высший знак.'}</p><div class="progress" style="margin-top:20px"><span style="width:${campaignProgress()}%"></span></div></div></section><section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">XP</div><b>${state.xp}</b><span>всего опыта</span></div><div class="stat-box"><div class="stat-icon">▦</div><b>${collectionProgress()}%</b><span>коллекция собрана</span></div><div class="stat-box"><div class="stat-icon">◉</div><b>${averageQuiz()}%</b><span>средний результат</span></div><div class="stat-box"><div class="stat-icon">✦</div><b>${state.read.length}</b><span>знаний изучено</span></div></section><section class="section reveal"><div class="panel"><div class="eyebrow">Техническая основа</div><h3>Твой прогресс остаётся у тебя</h3><p>Codex остаётся полностью статичным и работает на GitHub Pages. Авторизация и сервер не нужны: данные сохраняются локально через localStorage.</p></div></section>`);
}

