/* Codex v1.6 — card layout, map focus, packs and settings polish */

if(!NAV.some(item=>item[0]==='packs')) NAV.splice(Math.max(0,NAV.findIndex(item=>item[0]==='map')),0,['packs','✦','Паки']);
PAGE_META.packs=['Архив','Паки знаний'];
PAGE_META.map=['Атлас','Карта главы'];
PAGE_META.detail=['Карточка','Историческое досье'];
state.mapFilter=state.mapFilter||'ALL';
state.mapChapter=state.mapChapter||'ROME_CHAPTER_01';
state.cardReturnTab=state.cardReturnTab||'collection';

function wikiSourceUrl(c){
  if(c?.source?.url)return c.source.url;
  return `https://ru.wikipedia.org/wiki/Special:Search?search=${encodeURIComponent(c?.title||'Древний Рим')}`;
}
function wikiSourceLabel(c){return c?.source?.title||`${c?.title||'Тема'} — Википедия`;}
function rememberCardReturn(){if(state.tab!=='detail')state.cardReturnTab=state.tab||'collection';}
function backFromCard(){const target=state.cardReturnTab&&state.cardReturnTab!=='detail'?state.cardReturnTab:'collection';go(target);}

const V15_openCard=openCard;
openCard=function(id){rememberCardReturn();V15_openCard(id);};
const V15_openCatalogCard=openCatalogCard;
openCatalogCard=function(id){rememberCardReturn();V15_openCatalogCard(id);};

function shell(inner){
  const [section,title]=pageTitle();
  return `<div class="app-layout">
    <aside class="side-nav">
      <div class="brand-mark"><img class="brand-logo" src="assets/ui/codex-logo-mark.png" alt="Codex of History"><div class="brand-title"><small>Codex of History</small><h1>История</h1></div></div>
      <div class="nav-kicker">Навигация</div>
      <div class="nav-list">${navButtons('nav-btn')}</div>
      <div class="side-card compact-side-card">
        <div class="side-level"><strong>${state.level}</strong><em>УРОВЕНЬ</em></div>
        <p>${state.xp} XP · ${averageMastery()}% освоено</p>
        <div class="progress"><span style="width:${levelProgress()}%"></span></div>
        <div class="side-version"><span>Codex</span><b>v${appVersion()}</b></div>
      </div>
    </aside>
    <main class="main-wrap">
      <header class="command-bar">
        <div class="command-title"><span>${section}</span><span>·</span><b>${title}</b></div>
        <div class="command-actions"><div class="command-pill version-pill">v${appVersion()}</div><div class="command-pill">◇ ${state.fragments}</div><div class="command-pill">${state.xp} XP</div><button class="command-icon" onclick="go('settings')" title="Настройки">⚙</button></div>
      </header>
      <div class="top-mobile">
        <button class="mobile-menu-button" onclick="toggleMobileMenu()" aria-label="Открыть меню">☰</button>
        <div class="mobile-brand"><img src="assets/ui/codex-logo-mark.png" alt=""><div><b>Codex</b><small>v${appVersion()}</small></div></div>
        <button class="mobile-command" onclick="go('settings')" title="Настройки">⚙</button>
      </div>
      <div class="view">${inner}</div></main><nav class="mobile-tabs legacy-mobile-tabs" aria-hidden="true"></nav>
    <button class="mobile-drawer-backdrop" onclick="closeMobileMenu()" aria-label="Закрыть меню"></button>
    <aside class="mobile-drawer" aria-label="Мобильная навигация">
      <div class="mobile-drawer-head"><div class="mobile-brand"><img src="assets/ui/codex-logo-mark.png" alt=""><div><b>Codex of History</b><small>v${appVersion()}</small></div></div><button onclick="closeMobileMenu()">×</button></div>
      <div class="mobile-drawer-progress"><span>Уровень ${state.level}</span><b>${state.xp} XP</b><div class="progress"><i style="width:${levelProgress()}%"></i></div></div>
      <nav class="mobile-drawer-nav">${mobileDrawerNav()}</nav>
      <div class="mobile-drawer-actions"><button onclick="closeMobileMenu();go('settings')">⚙ Настройки</button></div>
    </aside>
  </div>${packModal()}${masteryModal()}${typeof poolUnlockModal==='function'?poolUnlockModal():''}`;
}

function detailBackButton(){return `<button class="detail-back-button" onclick="backFromCard()" aria-label="Назад">← <span>Назад</span></button>`;}
function compactRelationLabel(type){return ({CAUSE:'Причина',CONSEQUENCE:'Следствие',ALLY:'Союз',ENEMY:'Конфликт',PART_OF:'Часть темы',RULED_BY:'Власть',FOUNDED_BY:'Основание',INFLUENCED:'Влияние',CONFLICT_WITH:'Конфликт',LOCATED_IN:'Место',SAME_ERA:'Одна эпоха',DYNASTIC_LINK:'Династия',RELIGIOUS_LINK:'Религия',CULTURAL_LINK:'Культура',ECONOMIC_LINK:'Экономика',MILITARY_LINK:'Война',MYTH_VS_FACT:'Миф и факт',SOURCE_FOR:'Источник',PRECEDES:'Раньше',FOLLOWS:'Позже'})[type]||String(type).replaceAll('_',' ');}
function cardSourcePanel(c){return `<div class="panel reveal source-panel"><div class="eyebrow">Источник по теме</div><h3>${wikiSourceLabel(c)}</h3><p class="credit">Краткая справка, даты, имена и связанные статьи.</p><a class="btn ghost" href="${wikiSourceUrl(c)}" target="_blank" rel="noreferrer">Открыть в Википедии ↗</a></div>`;}

function detail(){
  const c=currentCard();const unlocked=isUnlocked(c.id);const info=masteryInfo(c.id);const acquisition=acquisitionInfo(c.id);const pool=poolForCard(c.id);const story=storylineForCard(c.id);
  const edges=RELATIONS.filter(r=>r.source===c.id||r.target===c.id);
  if(!unlocked){
    const value=state.collectionView==='CATALOG'?catalogState(c):null;
    const available=value==='POOL_OPEN'||value==='STORY_AVAILABLE';
    return shell(`<div class="detail-grid catalog-locked-detail"><main class="detail-main"><div class="detail-cover compact-detail-cover reveal">${detailBackButton()}${imgTag(c)}<div class="catalog-detail-veil"><span>${isStoryCard(c.id)?'♜ СЮЖЕТНАЯ КАРТА':'✦ АРХИВНАЯ КАРТА'}</span><h2>${c.title}</h2><p>${c.subtitle}</p></div></div><section class="section compact-info-grid reveal"><div class="panel info-panel compact-content-card"><div class="eyebrow">Статус</div><h3>${state.collectionView==='CATALOG'?catalogStateLabel(c):'Историческое досье закрыто'}</h3><p>${available?'Карта уже доступна в текущем этапе и ждёт получения.':'Продолжай кампанию, чтобы открыть эту часть истории.'}</p></div><div class="panel info-panel compact-content-card"><div class="eyebrow">Способ получения</div><h3>${acquisition.kind==='STORY'?'Основная кампания':`Пул «${pool?.title||'Архив'}»`}</h3><p>${acquisition.kind==='STORY'?'Сюжетные карты открываются гарантированно.':'Архивные карты выпадают из паков после открытия нужной главы.'}</p></div></section></main><aside class="detail-aside"><div class="panel mastery-panel"><div class="eyebrow">Стадия знания</div><div class="detail-mastery-ring" style="--mastery:${info.percent}"><strong>${info.percent}%</strong></div>${masteryPill(c.id)}<p>${nextMasteryStep(c.id)}</p>${acquisition.kind==='STORY'?`<button class="btn secondary" onclick="go('campaign')">♜ В кампанию</button>`:(archiveAvailable(c)?`<button class="btn" onclick="go('packs')">✦ К пакам</button>`:`<button class="btn secondary" onclick="go('campaign')">♜ Открыть этап</button>`)}</div>${cardSourcePanel(c)}</aside></div>`);
  }
  const relationHtml=edges.map(r=>{const other=card(r.source===c.id?r.target:r.source);const known=isDiscovered(other.id);return `<article class="edge compact-edge ${known?'':'unknown-edge'}" onclick="${known?`openCard('${other.id}')`:''}"><div><b>${compactRelationLabel(r.type)}</b><strong>${known?other.title:'Неизвестный узел'}</strong></div><p>${known?r.description:'Изучи больше карточек, чтобы раскрыть связь.'}</p><span>↗</span></article>`;}).join('')||'<div class="empty">Связей пока нет.</div>';
  return shell(`<div class="detail-grid compact-detail-grid"><main class="detail-main"><div class="detail-cover compact-detail-cover reveal">${detailBackButton()}${imgTag(c)}<div class="detail-title">${cardBadges(c)}<h2>${c.title}</h2><p>${c.subtitle} · ${c.region}</p></div></div><section class="section compact-info-grid reveal"><article class="panel compact-content-card"><div class="eyebrow">Коротко</div><h3>Суть карточки</h3><p>${c.summary}</p></article><article class="panel compact-content-card"><div class="eyebrow">Контекст</div><h3>Почему это важно</h3><p>${c.importance}</p></article></section><section class="section compact-card-section reveal"><div class="section-head"><h2>Опорные факты</h2><span>${c.era}</span></div><div class="fact-list compact-fact-list">${c.facts.map((f,i)=>`<article class="fact compact-fact"><b>${String(i+1).padStart(2,'0')}</b><p>${f}</p></article>`).join('')}</div></section><section class="section compact-card-section reveal"><div class="section-head"><h2>Связи в истории</h2><span>${edges.length}</span></div><div class="edge-list compact-edge-list">${relationHtml}</div></section></main><aside class="detail-aside"><div class="panel mastery-panel reveal"><div class="eyebrow">Освоение карточки</div><div class="mastery-panel-row"><div class="detail-mastery-ring" style="--mastery:${info.percent}"><strong>${info.percent}%</strong></div><div>${masteryPill(c.id)}<h3>${nextMasteryStep(c.id)}</h3></div></div><div class="mastery-steps-mini">${['DISCOVERED','OPENED','STUDIED','MASTERED','CONSOLIDATED'].map(k=>`<i class="${MASTERY_META[k].percent<=info.percent?'done':''}" title="${MASTERY_META[k].label}"></i>`).join('')}</div>${masteryAction(c)}</div><div class="panel reveal compact-stats-panel"><div class="eyebrow">Учебные характеристики</div><div class="bars">${Object.entries(c.stats).map(([k,v])=>`<div class="bar-row"><span>${STAT_LABELS[k]||k}</span><div class="bar-bg"><div class="bar-fill" style="width:${v*10}%"></div></div><b>${v}</b></div>`).join('')}</div></div>${cardSourcePanel(c)}<div class="panel reveal detail-tags-panel"><div class="eyebrow">Теги</div><div class="card-tags">${c.tags.map(t=>`<span class="tag">#${t}</span>`).join('')}</div></div><div class="panel acquisition-panel reveal"><div class="eyebrow">Получение</div><h3>${acquisition.kind==='STORY'?'♜ Сюжетная':'✦ Архивная'}</h3><p>${acquisition.kind==='STORY'?'Открыта в основной кампании.':`Получена из пула «${pool?.title||'Архив'}».`}</p></div>${story?`<div class="panel personal-story-panel reveal"><div class="eyebrow">${rarityDepth(c.rarity)}</div><h3>⌁ ${story.title}</h3><p>${story.steps.length} задания · ${story.rewardXp} XP · ${story.rewardFragments} ◇</p><button class="btn" onclick="openPersonalStory('${story.id}')">${storyFinished(story.id)?'Повторить историю':'Начать историю'} →</button></div>`:''}</aside></div>`);
}

const V15_campaign=campaign;
campaign=function(){
  let html=V15_campaign();
  html=html.replace(/<section class="section reveal"><div class="section-head"><h2>Архивные пулы кампании[\s\S]*?<\/section>/,'');
  return html;
};

function missionScreen(){
  const m=mission(state.currentMission)||currentMission();const done=missionCompleted(m.id);const idx=missionIndex(m.id);const cardsHtml=m.cards.map(id=>card(id)).filter(Boolean).map(renderMiniCard).join('');let activity='';
  if(m.type==='READ'){
    const read=m.cards.filter(id=>state.read.includes(id)).length;
    activity=`<div class="mission-action panel compact-mission-action"><div><div class="eyebrow">Задача</div><h3>Изучи карточки миссии</h3><p>Прогресс: <b>${read}/${m.cards.length}</b></p></div><div class="mission-action-controls"><div class="progress"><span style="width:${Math.round(read/m.cards.length*100)}%"></span></div><button class="btn" ${read===m.cards.length?`onclick="finishReadMission('${m.id}')"`:'disabled'}>${done?'Завершено':'Завершить'}</button></div></div>`;
  }else if(m.type==='QUIZ'||m.type==='FINAL'){
    const r=quizResult(m.quiz);activity=`<div class="mission-action panel compact-mission-action"><div><div class="eyebrow">${m.type==='FINAL'?'Финальный экзамен':'Испытание'}</div><h3>${QUIZZES[m.quiz].title}</h3><p>${r?`Лучший результат: <b>${r.bestPercent}%</b>`:`Зачёт начинается от ${PASS_PERCENT}%`}</p></div><button class="btn" onclick="openQuiz('${m.quiz}','${m.id}')">${r?'Повторить':'Начать'} →</button></div>`;
  }else if(m.type==='MAP'){
    const task=state.mapTasks[m.id]||{step:0,mistakes:0,passed:false};const ask=task.passed?'География пройдена':task.step===0?'Найди Рим в Центральной Италии':'Приблизь город и найди Палатин';
    activity=`<div class="mission-action panel map-mission compact-map-mission"><div class="map-task-head"><div><div class="eyebrow">Карта главы</div><h3>${ask}</h3><p>${task.step===0?'Найди точку Рима на реальной карте.':'Найди Палатин внутри современного города.'} Ошибок: <b id="map-error-count">${task.mistakes||0}</b>.</p></div><div class="map-progress"><i class="${task.step>0?'done':''}"></i><i class="${task.passed?'done':''}"></i><b>${task.passed?'2/2':task.step+'/2'}</b></div></div><div class="map-shell mission-map-shell"><div id="mission-map" class="leaflet-map" data-mission="${m.id}"></div></div></div>`;
  }else if(m.type==='TIMELINE'){
    const task=state.timelineTasks[m.id]||{selected:[],passed:false};const options=TIMELINE_ORDER.slice().sort((a,b)=>['superbus','foundation','expulsion','numa','tarquin'].indexOf(a)-['superbus','foundation','expulsion','numa','tarquin'].indexOf(b));
    activity=`<div class="mission-action panel compact-timeline-action"><div class="eyebrow">Хронология</div><h3>${task.passed?'Цепочка собрана':'Выбери события от раннего к позднему'}</h3><div class="timeline-picked">${task.selected.length?task.selected.map((k,i)=>`<span><b>${i+1}</b>${TIMELINE_LABELS[k]}</span>`).join(''):'<em>Выбранные события появятся здесь</em>'}</div><div class="timeline-options">${options.filter(k=>!task.selected.includes(k)).map(k=>`<button onclick="chooseTimeline('${m.id}','${k}')">${TIMELINE_LABELS[k]}</button>`).join('')}</div><button class="btn secondary" onclick="undoTimeline('${m.id}')" ${!task.selected.length?'disabled':''}>← Отменить</button></div>`;
  }
  return shell(`<section class="mission-hero compact-mission-hero reveal"><div><div class="eyebrow">Миссия ${idx+1} из ${CAMPAIGN.nodes.length} · ${missionTypeLabel(m.type)}</div><h2>${m.emoji} ${m.title}</h2><p>${m.description}</p><div class="mission-reward"><span>+${m.xp} XP</span><span>${(m.unlockCards||[]).length} карт</span></div></div><div class="mission-seal compact-mission-seal ${done?'done':''}">${done?'✓':String(idx+1).padStart(2,'0')}</div></section><section class="section compact-card-section reveal"><div class="section-head"><h2>Материалы</h2><span>${m.cards.length}</span></div><div class="card-grid mission-cards">${cardsHtml}</div></section><section class="section reveal">${activity}</section><section class="mission-footer compact-mission-footer reveal"><button class="btn ghost" onclick="go('campaign')">← Миссии</button>${idx>0?`<button class="btn secondary" onclick="openMission('${CAMPAIGN.nodes[idx-1].id}')">Предыдущая</button>`:''}${idx<CAMPAIGN.nodes.length-1&&missionOpen(CAMPAIGN.nodes[idx+1].id)?`<button class="btn" onclick="openMission('${CAMPAIGN.nodes[idx+1].id}')">Следующая →</button>`:''}</section>`);
}

function setMapFilter(value){state.mapFilter=value;save();render();}
function mapFilterMatches(c){if(state.mapFilter==='ALL')return true;if(state.mapFilter==='PERSON')return c.type==='PERSON';if(state.mapFilter==='PLACE')return ['CITY','STATE','CULTURE'].includes(c.type);if(state.mapFilter==='EVENT')return ['EVENT','BATTLE','FACTION','RELIGION','ARTIFACT'].includes(c.type);return true;}
function chapterMapCards(){const ids=[...new Set(CAMPAIGN.nodes.flatMap(n=>n.cards))];return ids.map(card).filter(c=>c&&isUnlocked(c.id)&&mapFilterMatches(c));}
function mapScreen(){
  const cards=chapterMapCards();const filters=[['ALL','Все'],['PERSON','Личности'],['PLACE','Места'],['EVENT','События']];
  return shell(`<section class="collection-header compact-collection-head map-page-head reveal"><div><div class="eyebrow">Глава I · Рождение Рима</div><h2>Карта кампании</h2><p>Маркеры показывают полученные карточки текущей главы. Нажми на точку, чтобы приблизить её на карте.</p></div><div class="map-filter-row">${filters.map(([id,label])=>`<button class="${state.mapFilter===id?'active':''}" onclick="setMapFilter('${id}')">${label}</button>`).join('')}</div></section><div class="map-shell atlas-clean reveal"><div id="atlas-map" class="leaflet-map"></div><div class="map-actions"><button class="map-action" onclick="resetAtlasView()" title="Вернуться к Риму">⌂</button><button class="map-action" onclick="fitAtlasMarkers()" title="Показать точки">◎</button></div></div><section class="section compact-section reveal"><div class="section-head"><h2>Точки главы</h2><span>${cards.length}</span></div><div class="location-grid compact-location-grid">${cards.map(c=>`<button class="location-card compact-location-card" onclick="focusAtlasCard('${c.id}')"><span>${typeIcon(c.type)}</span><div><small>${c.loc?.label||c.region}</small><h3>${c.title}</h3><p>${c.date}</p></div></button>`).join('')||'<div class="empty">По этому фильтру точек нет.</div>'}</div></section>`);
}

function packCover(kind){return kind==='DAILY'?'assets/ui/pack-daily.svg':'assets/ui/pack-rome.svg';}
function packAction(kind){
  const pools=unlockedPools();
  if(!pools.length)return `<button class="btn secondary" onclick="go('campaign')">Открыть первый пул</button>`;
  if(kind==='DAILY'){
    if(dailyPackReady())return `<button class="btn" onclick="claimPack('DAILY')">Открыть бесплатно</button>`;
    if(!dailyLearningCompleteToday())return `<button class="btn secondary" onclick="go('daily')">Сначала дневной урок</button>`;
    return `<button class="btn secondary" disabled>Открыт сегодня</button>`;
  }
  return `<button class="btn secondary" onclick="claimPack('ROMAN')" ${state.fragments<PACK_DEFS.ROMAN.cost?'disabled':''}>Открыть · 60 ◇</button>`;
}
function packsScreen(){
  const available=packPool().filter(c=>!isUnlocked(c.id)).length;const history=state.packHistory.slice(-5).reverse();
  return shell(`<section class="packs-page-head reveal"><div class="packs-title-block"><div class="eyebrow">Архив активной кампании</div><h2>Паки знаний</h2><p>Получай дополнительные личности, места, артефакты и личные истории.</p><div class="fragment-balance compact-fragment-balance"><span>◇</span><b>${state.fragments}</b><small>фрагментов</small></div></div></section><section class="packs-page-grid reveal"><article class="pack-page-card ${dailyPackReady()?'ready':''}"><img src="${packCover('DAILY')}" alt="Архивный пак дня"><div class="pack-page-copy"><small>ЕЖЕДНЕВНЫЙ · 3 КАРТЫ</small><h3>Архивный пак дня</h3><p>${dailyPackReady()?'Награда за сегодняшнюю учебную сессию готова.':dailyLearningCompleteToday()?'Сегодняшний пак уже открыт.':'Заверши короткую дневную сессию.'}</p><div class="pack-page-meta"><span>Epic через ${Math.max(0,8-state.packPity.epic)}</span><span>Legendary через ${Math.max(0,24-state.packPity.legendary)}</span></div>${packAction('DAILY')}</div></article><article class="pack-page-card roman"><img src="${packCover('ROMAN')}" alt="Римский архивный пак"><div class="pack-page-copy"><small>РИМСКИЙ · 4 КАРТЫ</small><h3>Римский архивный пак</h3><p>${available} новых карточек доступно в открытых этапах кампании.</p><div class="pack-page-meta"><span>Стоимость 60 ◇</span><span>${unlockedPools().length} пулов открыто</span></div>${packAction('ROMAN')}</div></article></section>${history.length?`<section class="section compact-card-section reveal"><div class="section-head"><h2>Последние открытия</h2><span>${history.length}</span></div><div class="pack-history-list">${history.map(h=>`<article><span>${h.kind==='DAILY'?'☀':'SPQR'}</span><div><b>${PACK_DEFS[h.kind]?.title||h.kind}</b><small>${new Intl.DateTimeFormat('ru-RU',{day:'numeric',month:'short'}).format(new Date(h.date))}</small></div><em>${h.drops.filter(d=>d.fresh).length} новых</em></article>`).join('')}</div></section>`:''}`);
}
function openPackHub(){state.packModal=null;state.masterySession=null;state.tab='packs';save();render();window.scrollTo({top:0,behavior:'smooth'});}
function closePack(){state.packModal=null;save();render();}
function packModal(){
  if(!state.packModal||state.packModal.view!=='result')return'';const def=PACK_DEFS[state.packModal.kind];
  return `<div class="game-modal-backdrop" onclick="if(event.target===this)closePack()"><section class="game-modal pack-result-modal v15-pack-result"><button class="modal-close" onclick="closePack()">×</button><div class="pack-result-balance">◇ ${state.fragments}</div><img class="pack-result-cover" src="${packCover(state.packModal.kind)}" alt="${def.title}"><div class="eyebrow">Пак открыт</div><h2>${def.title}</h2><p>${state.packModal.gained?`Дубликаты дали <b>${state.packModal.gained}</b> фрагментов.`:'Открыты новые карточки.'}</p><div class="pack-drops">${state.packModal.drops.map((d,i)=>{const c=card(d.id),s=d.storyId?PERSONAL_STORIES[d.storyId]:null;return `<article class="pack-drop ${d.fresh?'fresh':'duplicate'}" style="--delay:${i*100}ms" onclick="closePack();openCard('${c.id}')"><div>${imgTag(c)}</div><span>${d.fresh?'НОВАЯ':`+${d.fragments} ◇`}</span><h3>${c.title}</h3><small>${rarityLabel(c.rarity)}</small>${s&&d.fresh?'<b class="story-drop-label">⌁ История</b>':''}</article>`;}).join('')}</div><div class="hero-actions" style="justify-content:center"><button class="btn" onclick="closePack()">Забрать</button><button class="btn secondary" onclick="state.packModal=null;go('packs')">К пакам</button></div></section></div>`;
}

function profile(){
  const finished=Object.values(PERSONAL_STORIES).filter(s=>storyFinished(s.id)).length;
  return shell(`<section class="profile-summary reveal"><div class="profile-avatar">${state.level}</div><div><div class="eyebrow">Хранитель Codex</div><h2>${state.xp} XP</h2><p>${completedMissionCount()}/${CAMPAIGN.nodes.length} миссий · ${ownedCards().length}/${CARDS.length} карточек</p></div></section><section class="home-stats compact-profile-stats reveal"><div class="stat-box"><b>${averageMastery()}%</b><span>освоение</span></div><div class="stat-box"><b>${state.read.length}</b><span>изучено</span></div><div class="stat-box"><b>${dailyRetention()}%</b><span>память</span></div><div class="stat-box"><b>${finished}</b><span>историй</span></div></section><section class="profile-progress-grid reveal"><article class="panel"><div class="eyebrow">Кампания</div><h3>Рождение Рима · ${campaignProgress()}%</h3><div class="progress"><span style="width:${campaignProgress()}%"></span></div></article><article class="panel"><div class="eyebrow">Коллекция</div><h3>${ownedCards().length}/${CARDS.length} карточек</h3><div class="progress"><span style="width:${collectionProgress()}%"></span></div></article></section><section class="section profile-danger-zone reveal"><div class="panel"><div><div class="eyebrow">Управление данными</div><h3>Сбросить игровой прогресс</h3><p>Карточки, XP и прохождение будут удалены.</p></div><button class="btn danger" onclick="resetProgress()">↺ Сбросить прогресс</button></div></section>`);
}

function settingsScreen(){
  const dark=state.theme==='night';
  return shell(`<section class="settings-hero compact-settings-hero reveal"><div><div class="eyebrow">Система Codex</div><h2>Настройки</h2><p>Тема, обновление и резервная копия прогресса.</p></div><div class="version-medallion"><small>ВЕРСИЯ</small><b>v${appVersion()}</b><span>Content Engine</span></div></section><section class="settings-grid compact-settings-grid reveal"><article class="settings-card settings-wide"><div class="settings-card-head"><span>◐</span><div><h3>Тема интерфейса</h3><p>Выбор сохраняется на устройстве.</p></div></div><div class="theme-choice-row"><button class="${dark?'selected':''}" onclick="if(state.theme!=='night')toggleTheme()"><i>☾</i><b>Тёмная тема</b></button><button class="${!dark?'selected':''}" onclick="if(state.theme!=='parchment')toggleTheme()"><i>☀</i><b>Пергаментная</b></button></div></article><article class="settings-card"><div class="settings-card-head"><span>↻</span><div><h3>Обновление</h3><p>Загрузить свежие файлы GitHub Pages.</p></div></div><div class="version-table"><span>Версия</span><b>v${appVersion()}</b><span>Контент</span><b>${CARDS.length} карт · ${CAMPAIGN.nodes.length} миссий</b><span>Последнее обновление</span><b>${formatSettingDate(preferences.lastForcedRefresh)}</b></div><button class="btn settings-main-btn" onclick="forceRefresh()">↻ Принудительно обновить</button><p class="settings-note">Прогресс не удаляется.</p></article><article class="settings-card"><div class="settings-card-head"><span>▣</span><div><h3>Сохранение</h3><p>Перенос между браузерами и устройствами.</p></div></div><div class="settings-actions"><button class="btn secondary" onclick="exportSave()">⇩ Экспорт</button><button class="btn secondary" onclick="requestImport()">⇧ Импорт</button><input id="settings-import" type="file" accept="application/json,.json" hidden onchange="importSave(event)"></div></article><article class="settings-card settings-wide settings-about"><div class="settings-card-head"><span>i</span><div><h3>О приложении</h3><p>Статическое приложение для GitHub Pages. Прогресс хранится локально.</p></div></div><div class="about-pills"><span>Static</span><span>LocalStorage</span><span>GitHub Pages</span><span>v${appVersion()}</span></div></article></section>`);
}

const V15_answerMapTask=answerMapTask;
answerMapTask=function(id,key){
  const expected=['rome','palatine'];const cur=state.mapTasks[id]||{step:0,mistakes:0,passed:false};if(cur.passed)return;
  if(key===expected[cur.step]){cur.step++;state.mapTasks[id]=cur;save();showToast('Верно',cur.step===1?'Рим найден. Теперь приблизь карту и найди Палатин.':'Палатин найден — миссия пройдена.','⌖');if(cur.step>=expected.length){cur.passed=true;state.mapTasks[id]=cur;save();completeMission(id);render();}else render();}
  else{cur.mistakes++;state.mapTasks[id]=cur;save();updateMapMissionStatus(id);showToast('Не туда','Перемещай карту и ориентируйся по современным подписям.','↻');}
};

function render(){
  closeMobileMenu();dailySyncSchedule();syncDiscovery();applyTheme();destroyMaps();applyPreferences?.();
  const screens={home,daily:dailyScreen,campaign,mission:missionScreen,collection,detail,quiz,map:mapScreen,packs:packsScreen,profile,storyline:storylineScreen,settings:settingsScreen};
  document.getElementById('app').innerHTML=(screens[state.tab]||home)();
  requestAnimationFrame(()=>{initEnhancements();initMapsForView();});
}

const V15_collectionScreen=collection;
collection=function(){
  return V15_collectionScreen().replace(/<button class="mini-pack-button"[\s\S]*?<\/button>/,'');
};
