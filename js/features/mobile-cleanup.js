/* Codex v1.5 — compact library, mobile drawer, profile and pack cleanup */

function openMobileMenu(){ document.body?.classList?.add('mobile-menu-open'); }
function closeMobileMenu(){ document.body?.classList?.remove('mobile-menu-open'); }
function toggleMobileMenu(){ document.body?.classList?.toggle('mobile-menu-open'); }

function mobileDrawerNav(){
  return NAV.map(([id,ico,label])=>{
    const active=state.tab===id||(state.tab==='mission'&&id==='campaign');
    return `<button class="mobile-drawer-link ${active?'active':''}" onclick="closeMobileMenu();go('${id}')"><span>${ico}</span><b>${label}</b></button>`;
  }).join('');
}

function shell(inner){
  const [section,title]=pageTitle();
  return `<div class="app-layout">
    <aside class="side-nav">
      <div class="brand-mark"><div class="seal">C</div><div class="brand-title"><small>Codex of History</small><h1>История</h1></div></div>
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
        <div class="command-actions">${themeToggle()}<div class="command-pill version-pill">v${appVersion()}</div><div class="command-pill">◇ ${state.fragments}</div><div class="command-pill">${state.xp} XP</div><button class="command-icon" onclick="go('settings')" title="Настройки">⚙</button></div>
      </header>
      <div class="top-mobile">
        <button class="mobile-menu-button" onclick="toggleMobileMenu()" aria-label="Открыть меню">☰</button>
        <div class="mobile-brand"><img src="assets/ui/codex-mark.svg" alt=""><div><b>Codex</b><small>v${appVersion()}</small></div></div>
        <button class="mobile-command" onclick="go('settings')" title="Настройки">⚙</button>
      </div>
      <div class="view">${inner}</div></main><nav class="mobile-tabs legacy-mobile-tabs" aria-hidden="true"></nav>
    <button class="mobile-drawer-backdrop" onclick="closeMobileMenu()" aria-label="Закрыть меню"></button>
    <aside class="mobile-drawer" aria-label="Мобильная навигация">
      <div class="mobile-drawer-head"><div class="mobile-brand"><img src="assets/ui/codex-mark.svg" alt=""><div><b>Codex of History</b><small>v${appVersion()}</small></div></div><button onclick="closeMobileMenu()">×</button></div>
      <div class="mobile-drawer-progress"><span>Уровень ${state.level}</span><b>${state.xp} XP</b><div class="progress"><i style="width:${levelProgress()}%"></i></div></div>
      <nav class="mobile-drawer-nav">${mobileDrawerNav()}</nav>
      <div class="mobile-drawer-actions"><button onclick="closeMobileMenu();toggleTheme()">${state.theme==='parchment'?'☀ Пергамент':'☾ Чёрная тема'}</button><button onclick="closeMobileMenu();go('settings')">⚙ Настройки</button></div>
    </aside>
  </div>${packModal()}${masteryModal()}${typeof poolUnlockModal==='function'?poolUnlockModal():''}`;
}

function libraryMiniSwitch(){
  return `<div class="library-mini-switch" role="tablist" aria-label="Режим библиотеки"><button class="${state.collectionView==='ARCHIVE'?'active':''}" onclick="setCollectionView('ARCHIVE')">▦ Архив</button><button class="${state.collectionView==='CATALOG'?'active':''}" onclick="setCollectionView('CATALOG')">◫ Коллекция</button></div>`;
}

function compactFilterControls(placeholder,withMastery=false){
  const types=['ALL',...new Set(CARDS.map(c=>c.type))];
  const rarities=['ALL',...new Set(CARDS.map(c=>c.rarity))];
  const mastery=withMastery?`<select aria-label="Освоение" onchange="setFilter('masteryFilter',this.value)">${MASTERY_FILTERS.slice(2).map(k=>`<option value="${k}" ${state.masteryFilter===k?'selected':''}>${MASTERY_META[k].label}</option>`).join('')}<option value="ALL" ${state.masteryFilter==='ALL'?'selected':''}>Все стадии</option></select>`:'';
  return `<div class="compact-filter-row reveal"><div class="field-wrap"><input id="collection-search" placeholder="${placeholder}" value="${esc(state.search)}" oninput="updateSearch(this)"></div><select aria-label="Тип" onchange="setFilter('filter',this.value)">${types.map(t=>`<option value="${t}" ${state.filter===t?'selected':''}>${t==='ALL'?'Все типы':typeLabel(t)}</option>`).join('')}</select><select aria-label="Редкость" onchange="setFilter('rarity',this.value)">${rarities.map(r=>`<option value="${r}" ${state.rarity===r?'selected':''}>${r==='ALL'?'Все редкости':rarityLabel(r)}</option>`).join('')}</select>${mastery}</div>`;
}

collection=function(){
  const top=`<section class="collection-header compact-collection-head reveal"><div><div class="eyebrow">${state.collectionView==='ARCHIVE'?'Личный архив':'Полный каталог'}</div><h2>${state.collectionView==='ARCHIVE'?'Архив':'Коллекция'}</h2></div><div class="collection-head-tools">${libraryMiniSwitch()}<button class="mini-pack-button" onclick="openPackHub()">✦ ${state.fragments} ◇</button></div></section>`;
  if(state.collectionView==='CATALOG'){
    const scopes=[['ALL','Все'],['OWNED','Полученные'],['OPEN_POOLS','Доступные'],['FUTURE','Будущие'],['STORY','Сюжет'],['ARCHIVE','Архивные']];
    const list=catalogCardsForScope();
    return shell(`${top}<div class="compact-chip-row reveal">${scopes.map(([id,label])=>`<button class="${state.catalogScope===id?'active':''}" onclick="setCatalogScope('${id}')">${label}</button>`).join('')}<span>${list.length}/${CARDS.length}</span></div>${compactFilterControls('Поиск по коллекции...')}<div class="catalog-grid reveal">${list.length?list.map(catalogCard).join(''):'<div class="empty">Карточек по этим фильтрам нет.</div>'}</div>`);
  }
  const modes=[['ALL','Все'],['STORY','Сюжет'],['ARCHIVE','Из паков'],['STORIES','Истории'],['MASTERED','Закреплены']];
  const list=ownedCards().filter(c=>{
    const mastery=masteryInfo(c.id);let allowed=true;
    if(state.collectionMode==='STORY')allowed=isStoryCard(c.id);
    if(state.collectionMode==='ARCHIVE')allowed=isArchiveCard(c.id);
    if(state.collectionMode==='STORIES')allowed=!!storylineForCard(c.id);
    if(state.collectionMode==='MASTERED')allowed=mastery.key==='CONSOLIDATED';
    return allowed&&(state.masteryFilter==='ALL'||mastery.key===state.masteryFilter)&&cardMatchesFilters(c);
  });
  const body=list.length?list.map(renderMiniCard).join(''):`<div class="empty archive-empty"><i>▦</i><h3>Здесь пока пусто</h3><button class="btn" onclick="setCollectionView('CATALOG')">Открыть коллекцию</button></div>`;
  return shell(`${top}<div class="compact-chip-row reveal">${modes.map(([id,label])=>`<button class="${state.collectionMode===id?'active':''}" onclick="setCollectionMode('${id}')">${label}</button>`).join('')}<span>${list.length}</span></div>${compactFilterControls('Поиск в архиве...',true)}<div class="card-grid reveal">${body}</div>`);
};

mapScreen=function(){
  const chapterIds=[...new Set(CAMPAIGN.nodes.flatMap(n=>n.cards))];
  const opened=chapterIds.map(card).filter(c=>c&&isUnlocked(c.id));
  return shell(`<section class="collection-header compact-collection-head reveal"><div><div class="eyebrow">Исторический атлас</div><h2>Лаций и ранний Рим</h2></div><div class="collection-count">${opened.length} узлов</div></section><div class="map-shell atlas-clean reveal"><div id="atlas-map" class="leaflet-map"></div><div class="map-actions"><button class="map-action" onclick="resetAtlasView()" title="Вернуться к Риму">⌂</button><button class="map-action" onclick="fitAtlasMarkers()" title="Показать открытые точки">◎</button></div></div><section class="section compact-section reveal"><div class="section-head"><h2>Открытые места</h2><span>${opened.length}</span></div><div class="location-grid">${opened.map(c=>`<article class="panel panel-click location-card" onclick="openCard('${c.id}')"><small>${c.region}</small><h3>${typeIcon(c.type)} ${c.title}</h3><p>${c.date}</p></article>`).join('')}</div></section>`);
};

function compactPackImage(id){const c=card(id)||ownedCards()[0]||CARDS[0];return c?imgTag(c):'<img src="assets/ui/fallback-card.svg" alt="">';}
packModal=function(){
  if(!state.packModal)return'';
  if(state.packModal.view==='result'){
    const def=PACK_DEFS[state.packModal.kind];
    return `<div class="game-modal-backdrop" onclick="if(event.target===this)closePack()"><section class="game-modal pack-result-modal"><button class="modal-close" onclick="closePack()">×</button><div class="pack-emblem">${def.emoji}</div><div class="eyebrow">Пак открыт</div><h2>${def.title}</h2><p>${state.packModal.gained?`Получено <b>${state.packModal.gained}</b> фрагментов за дубликаты.`:'Открыты новые карточки.'}</p><div class="pack-drops">${state.packModal.drops.map((d,i)=>{const c=card(d.id),story=d.storyId?PERSONAL_STORIES[d.storyId]:null;return `<article class="pack-drop ${d.fresh?'fresh':'duplicate'}" style="--delay:${i*100}ms" onclick="closePack();openCard('${c.id}')"><div>${imgTag(c)}</div><span>${d.fresh?'НОВАЯ':`+${d.fragments} ◇`}</span><h3>${c.title}</h3><small>${rarityLabel(c.rarity)}</small>${story&&d.fresh?'<b class="story-drop-label">⌁ История</b>':''}</article>`;}).join('')}</div><button class="btn" onclick="closePack()">Забрать</button></section></div>`;
  }
  const pools=unlockedPools(),available=packPool().filter(c=>!isUnlocked(c.id)).length;
  return `<div class="game-modal-backdrop" onclick="if(event.target===this)closePack()"><section class="game-modal pack-hub-modal compact-pack-hub"><button class="modal-close" onclick="closePack()">×</button><div class="pack-hub-head compact"><div><div class="eyebrow">Архив Рима</div><h2>Паки</h2></div><div class="fragment-balance"><span>◇</span><b>${state.fragments}</b></div></div><div class="pack-options compact-pack-row"><article class="pack-option compact-pack ${dailyPackReady()&&pools.length?'ready':''}"><div class="pack-cover">${compactPackImage('ART_ROM_001')}</div><div class="pack-copy"><small>3 карточки</small><h3>Пак дня</h3><b>${dailyPackReady()?'Бесплатно':dailyLearningCompleteToday()?'Открыт сегодня':'После урока'}</b></div><button class="btn" onclick="claimPack('DAILY')" ${!dailyPackReady()||!pools.length?'disabled':''}>Открыть</button></article><article class="pack-option compact-pack roman"><div class="pack-cover">${compactPackImage('STA_ROM_002')}</div><div class="pack-copy"><small>4 карточки</small><h3>Римский пак</h3><b>${available} новых · 60 ◇</b></div><button class="btn secondary" onclick="claimPack('ROMAN')" ${state.fragments<PACK_DEFS.ROMAN.cost||!pools.length?'disabled':''}>Открыть</button></article></div>${pools.length?`<div class="active-pools compact-pools">${pools.map(p=>{const pr=poolProgress(p);return `<span>${p.title} ${pr.opened}/${pr.total}</span>`;}).join('')}</div>`:''}</section></div>`;
};

profile=function(){
  const finished=Object.values(PERSONAL_STORIES).filter(s=>storyFinished(s.id)).length;
  return shell(`<section class="profile-compact-hero reveal"><div class="profile-avatar">${state.level}</div><div><div class="eyebrow">Профиль</div><h2>Хранитель Codex</h2><p>${state.xp} XP · ${completedMissionCount()}/${CAMPAIGN.nodes.length} миссий</p></div><button class="btn secondary" onclick="go('settings')">⚙ Настройки</button></section><section class="home-stats compact-profile-stats reveal"><div class="stat-box"><b>${averageMastery()}%</b><span>освоение</span></div><div class="stat-box"><b>${state.read.length}</b><span>изучено</span></div><div class="stat-box"><b>${dailyRetention()}%</b><span>память</span></div><div class="stat-box"><b>${finished}</b><span>историй</span></div></section><section class="profile-progress-grid reveal"><article class="panel"><div class="eyebrow">Кампания</div><h3>Рождение Рима · ${campaignProgress()}%</h3><div class="progress"><span style="width:${campaignProgress()}%"></span></div></article><article class="panel"><div class="eyebrow">Коллекция</div><h3>${ownedCards().length}/${CARDS.length} карточек</h3><div class="progress"><span style="width:${collectionProgress()}%"></span></div></article></section><section class="section profile-danger-zone reveal"><div class="panel"><div><div class="eyebrow">Управление данными</div><h3>Сбросить игровой прогресс</h3><p>Настройки интерфейса останутся. Карточки, XP и прохождение будут удалены.</p></div><button class="btn danger" onclick="resetProgress()">↺ Сбросить прогресс</button></div></section>`);
};

const V14_render=render;
render=function(){ closeMobileMenu();V14_render(); };
