/* Codex of History — Patch v1.0: finished MVP library split + complete archive imagery */

const V10_IMAGE_FIXES = {
  CITY_ARC_001:{file:"Lo Scheggia, Reduction of Alba Longa by Tullus Hostilius, Circa 1430 - 35, Sotheby's.jpg",caption:'Разрушение Альба-Лонги Туллом Гостилием. Кассоне XV века',credit:'Wikimedia Commons / Lo Scheggia',license:'Public Domain',focus:'50% 50%'},
  REG_ARC_001:{file:'Tiber River, Rome (48494164807).jpg',caption:'Тибр в Риме',credit:'Wikimedia Commons / Gary Lee Todd',license:'Public Domain Mark',focus:'50% 52%'},
  REL_ARC_001:{file:'Augur, Nordisk familjebok.svg',caption:'Римский авгур с жезлом-литуусом',credit:'Wikimedia Commons / Nordisk familjebok',license:'Public Domain',focus:'50% 35%'},
  PER_ARC_001:{file:'P.P. Rubens - Twee Romeinse veldheren (Romulus en Titus Tatius) - NK2675 - Museum Boijmans Van Beuningen.jpg',caption:'Ромул и Тит Татий в поздней художественной традиции',credit:'Wikimedia Commons / Peter Paul Rubens',license:'Public Domain',focus:'50% 30%'},
  PER_ARC_002:{file:'Tarpeia Crushed by the Sabines Met DP888584.jpg',caption:'Гибель Тарпеи под щитами сабинян',credit:'Wikimedia Commons / The Met',license:'CC0',focus:'50% 45%'},
  LOC_ARC_001:{file:'Quirinal Hill Luigi Rossini.jpg',caption:'Квиринальский холм. Гравюра Луиджи Россини',credit:'Wikimedia Commons / Luigi Rossini',license:'Public Domain',focus:'50% 52%'},
  REL_ARC_002:{file:'Sesterce temple janus.JPG',caption:'Храм Януса на сестерции Нерона',credit:'Wikimedia Commons',license:'см. страницу файла',focus:'50% 50%'},
  PER_ARC_003:{file:'Ancus-Martius.jpg',caption:'Анк Марций в издании Promptuarii Iconum Insigniorum, 1553',credit:'Wikimedia Commons / Guillaume Rouillé',license:'Public Domain',focus:'50% 36%'},
  PER_ARC_004:{file:'Servius Tullius by Frans Huys.jpg',caption:'Сервий Туллий. Гравюра Франса Хейса',credit:'Wikimedia Commons / Frans Huys',license:'Public Domain',focus:'50% 34%'},
  ART_ARC_001:{file:'View of the Cloaca Maxima, Rome.jpg',caption:'Вид Клоаки Максимы в Риме. Кристоффер Эккерсберг, 1814',credit:'Wikimedia Commons / National Gallery of Art',license:'Public Domain',focus:'50% 52%'},
  ART_ARC_002:{file:'Servian Wall.JPG',caption:'Сохранившийся участок Сервиевой стены у Термини',credit:'Wikimedia Commons / Joris van Rooden',license:'Public Domain',focus:'50% 50%'},
  PER_ARC_005:{file:'Joerg Breu the Elder - The Suicide of Lucretia.JPG',caption:'История Лукреции. Йорг Брей Старший',credit:'Wikimedia Commons',license:'Public Domain',focus:'52% 42%'},
  PER_ARC_006:{file:'Capitoline Brutus Musei Capitolini MC1183.jpg',caption:'Капитолийский Брут, бронзовый бюст',credit:'Wikimedia Commons / Musei Capitolini',license:'см. страницу файла',focus:'50% 34%'},
  ORG_ARC_001:{file:'Consul with Lictors.png',caption:'Римский консул в сопровождении ликторов',credit:'Wikimedia Commons / John Williamson',license:'Public Domain',focus:'50% 44%'},
  ART_ARC_003:{file:'Fasces lictoriae.svg',caption:'Фасции — связка прутьев с топором, знак власти магистрата',credit:'Wikimedia Commons',license:'см. страницу файла',focus:'50% 50%'}
};

Object.entries(V10_IMAGE_FIXES).forEach(([id,image])=>{
  const target=card(id);
  if(target) target.image={...target.image,...image};
});

state.collectionView = state.collectionView === 'CATALOG' ? 'CATALOG' : 'ARCHIVE';
state.catalogScope = state.catalogScope || 'ALL';
PAGE_META.collection=['Библиотека','Архив и полный каталог'];

function ownedCards(){ return CARDS.filter(c=>isUnlocked(c.id)); }
function availablePackCards(){ return packPool().filter(c=>!isUnlocked(c.id)); }
function catalogLockedCount(){ return CARDS.length-ownedCards().length; }
function setCollectionView(view){
  state.collectionView=view;
  state.collectionMode='ALL';
  state.masteryFilter='ALL';
  save();render();
}
function setCatalogScope(scope){ state.catalogScope=scope;save();render(); }
function openCatalogCard(id){
  const c=card(id); if(!c)return;
  if(isUnlocked(id)){openCard(id);return;}
  state.currentCard=id;state.tab='detail';state.packModal=null;state.masterySession=null;
  save();render();window.scrollTo({top:0,behavior:'smooth'});
}
function catalogState(c){
  if(isUnlocked(c.id)) return 'OWNED';
  if(isStoryCard(c.id)) return isDiscovered(c.id)?'STORY_AVAILABLE':'STORY_LOCKED';
  return archiveAvailable(c)?'POOL_OPEN':'POOL_LOCKED';
}
function catalogStateLabel(c){
  const value=catalogState(c),pool=poolForCard(c.id);
  if(value==='OWNED')return 'Получена и хранится в архиве';
  if(value==='STORY_AVAILABLE')return 'Доступна в текущем сюжетном этапе';
  if(value==='STORY_LOCKED')return 'Откроется в основной кампании';
  if(value==='POOL_OPEN')return `Может выпасть · ${pool?.title||'открытый пул'}`;
  return `Будущий этап · ${pool?.title||'закрытый пул'}`;
}
function catalogStatusBadge(c){
  const value=catalogState(c);
  if(value==='OWNED')return '✓ ПОЛУЧЕНА';
  if(value==='POOL_OPEN')return '✦ МОЖЕТ ВЫПАСТЬ';
  if(value==='STORY_AVAILABLE')return '♜ ДОСТУПНА В СЮЖЕТЕ';
  return '⌁ ЗАКРЫТА';
}
function catalogCard(c){
  const value=catalogState(c),story=storylineForCard(c.id);
  return `<article class="catalog-card ${value.toLowerCase()} ${value==='OWNED'?'owned':''}" onclick="openCatalogCard('${c.id}')">
    <div class="catalog-art">${imgTag(c)}<div class="catalog-shade"></div><span class="catalog-status">${catalogStatusBadge(c)}</span><span class="catalog-index">${cardNumber(c)}</span></div>
    <div class="catalog-copy">
      <div class="card-kicker"><span>${typeIcon(c.type)} ${typeLabel(c.type)}</span><span>${rarityLabel(c.rarity)}</span></div>
      <h3>${c.title}</h3><p>${catalogStateLabel(c)}</p>
      <div class="card-tags">${acquisitionBadge(c)}${story?'<span class="tag">⌁ личная история</span>':''}</div>
    </div>
  </article>`;
}
function librarySwitch(){
  return `<div class="library-switch reveal" role="tablist" aria-label="Режим библиотеки">
    <button class="${state.collectionView==='ARCHIVE'?'active':''}" onclick="setCollectionView('ARCHIVE')"><i>▦</i><span><b>Архив</b><small>только полученные · ${ownedCards().length}</small></span></button>
    <button class="${state.collectionView==='CATALOG'?'active':''}" onclick="setCollectionView('CATALOG')"><i>◫</i><span><b>Коллекция</b><small>все карточки · ${CARDS.length}</small></span></button>
  </div>`;
}
function cardMatchesFilters(c){
  const query=state.search.toLowerCase();
  return (state.filter==='ALL'||c.type===state.filter)
    &&(state.rarity==='ALL'||c.rarity===state.rarity)
    &&(c.title.toLowerCase().includes(query)||c.original.toLowerCase().includes(query)||c.tags.join(' ').toLowerCase().includes(query));
}
function commonSearchControls(placeholder,withMastery=false){
  const types=['ALL',...new Set(CARDS.map(c=>c.type))];
  const rarities=['ALL',...new Set(CARDS.map(c=>c.rarity))];
  const mastery=withMastery?`<select onchange="setFilter('masteryFilter',this.value)"><option value="ALL">Все стадии</option>${MASTERY_FILTERS.slice(2).map(k=>`<option value="${k}" ${state.masteryFilter===k?'selected':''}>${MASTERY_META[k].label}</option>`).join('')}</select>`:'';
  return `<div class="search-row reveal"><div class="field-wrap"><input id="collection-search" placeholder="${placeholder}" value="${esc(state.search)}" oninput="updateSearch(this)"></div><select onchange="setFilter('filter',this.value)">${types.map(t=>`<option value="${t}" ${state.filter===t?'selected':''}>${t==='ALL'?'Все типы':typeLabel(t)}</option>`).join('')}</select><select onchange="setFilter('rarity',this.value)">${rarities.map(r=>`<option value="${r}" ${state.rarity===r?'selected':''}>${r==='ALL'?'Все редкости':rarityLabel(r)}</option>`).join('')}</select>${mastery}</div>`;
}

collection=function(){
  if(state.collectionView==='CATALOG'){
    const scopes=[['ALL','Все карты'],['OWNED','Полученные'],['OPEN_POOLS','Доступные сейчас'],['FUTURE','Будущие этапы'],['STORY','Сюжетные'],['ARCHIVE','Архивные']];
    const list=CARDS.filter(c=>{
      const value=catalogState(c);
      let allowed=true;
      if(state.catalogScope==='OWNED')allowed=value==='OWNED';
      if(state.catalogScope==='OPEN_POOLS')allowed=value==='POOL_OPEN'||value==='STORY_AVAILABLE';
      if(state.catalogScope==='FUTURE')allowed=value==='POOL_LOCKED'||value==='STORY_LOCKED';
      if(state.catalogScope==='STORY')allowed=isStoryCard(c.id);
      if(state.catalogScope==='ARCHIVE')allowed=isArchiveCard(c.id);
      return allowed&&cardMatchesFilters(c);
    });
    const cardsHtml=list.length?list.map(catalogCard).join(''):'<div class="empty">В выбранном разделе карточек нет.</div>';
    return shell(`<section class="collection-header reveal"><div><div class="eyebrow">Полный исторический каталог</div><h2>Коллекция всех карточек</h2><p>Здесь виден весь контент проекта. Закрытые карты показывают способ получения и этап, но не раскрывают досье, факты и связи раньше времени.</p></div><div class="collection-actions"><div class="collection-count">${list.length}/${CARDS.length}</div><button class="btn" onclick="openPackHub()">✦ Паки · ◇ ${state.fragments}</button></div></section>
      ${librarySwitch()}
      <div class="collection-tabs catalog-tabs reveal">${scopes.map(([id,label])=>`<button class="${state.catalogScope===id?'active':''}" onclick="setCatalogScope('${id}')">${label}</button>`).join('')}</div>
      ${commonSearchControls('Найти карточку в полном каталоге...')}
      <section class="catalog-summary reveal"><div><b>${ownedCards().length}</b><span>получено</span></div><div><b>${availablePackCards().length}</b><span>может выпасть сейчас</span></div><div><b>${catalogLockedCount()}</b><span>ещё не получено</span></div></section>
      <div class="catalog-grid reveal">${cardsHtml}</div>`);
  }

  const modes=[['ALL','Все полученные'],['STORY','Сюжетные'],['ARCHIVE','Из паков'],['STORIES','Личные истории'],['MASTERED','Закреплённые']];
  const list=ownedCards().filter(c=>{
    const mastery=masteryInfo(c.id);
    let allowed=true;
    if(state.collectionMode==='STORY')allowed=isStoryCard(c.id);
    if(state.collectionMode==='ARCHIVE')allowed=isArchiveCard(c.id);
    if(state.collectionMode==='STORIES')allowed=!!storylineForCard(c.id);
    if(state.collectionMode==='MASTERED')allowed=mastery.key==='CONSOLIDATED';
    return allowed&&(state.masteryFilter==='ALL'||mastery.key===state.masteryFilter)&&cardMatchesFilters(c);
  });
  const archiveCards=list.length?list.map(renderMiniCard).join(''):`<div class="empty archive-empty"><i>▦</i><h3>В этом разделе пока пусто</h3><p>Получи карту в сюжете, из пака или за фрагменты. Закрытые карты находятся только во вкладке «Коллекция».</p><button class="btn" onclick="setCollectionView('CATALOG')">Открыть полный каталог</button></div>`;
  return shell(`<section class="collection-header reveal"><div><div class="eyebrow">Личный архив</div><h2>Только полученные карточки</h2><p>Архив больше не показывает закрытые силуэты. Здесь лежат только карты, которые ты реально открыл в кампании, получил из пака или собрал за фрагменты.</p></div><div class="collection-actions"><div class="collection-count">${list.length} в разделе</div><button class="btn" onclick="openPackHub()">✦ Паки · ◇ ${state.fragments}</button></div></section>
    ${librarySwitch()}
    <div class="collection-tabs reveal">${modes.map(([id,label])=>`<button class="${state.collectionMode===id?'active':''}" onclick="setCollectionMode('${id}')">${label}</button>`).join('')}</div>
    <section class="mastery-overview reveal"><div class="mastery-total"><div class="mastery-big-ring" style="--mastery:${averageMastery()}"><strong>${averageMastery()}%</strong><span>освоение доступной истории</span></div></div><div class="mastery-stages">${MASTERY_FILTERS.slice(2).map(k=>{const meta=MASTERY_META[k];const count=ownedCards().filter(c=>masteryInfo(c.id).key===k).length;return `<button class="mastery-stage ${state.masteryFilter===k?'active':''}" onclick="setFilter('masteryFilter','${state.masteryFilter===k?'ALL':k}')"><i>${meta.icon}</i><b>${count}</b><span>${meta.label}</span></button>`;}).join('')}</div></section>
    ${commonSearchControls('Поиск в личном архиве...',true)}
    <div class="card-grid reveal">${archiveCards}</div>`);
};

const V10_PREVIOUS_DETAIL=detail;
detail=function(){
  const c=currentCard();
  if(!isUnlocked(c.id)&&state.collectionView==='CATALOG'){
    const acquisition=acquisitionInfo(c.id),pool=poolForCard(c.id),value=catalogState(c);
    let instruction='Соответствующий этап истории ещё не пройден.';
    if(value==='POOL_OPEN')instruction='Карта уже входит в доступный пул и может выпасть из следующего архивного пака.';
    if(value==='STORY_AVAILABLE')instruction='Карта открывается гарантированно в доступной сюжетной миссии.';
    const action=acquisition.kind==='STORY'?`<button class="btn secondary" onclick="go('campaign')">♜ К кампании</button>`:(archiveAvailable(c)?`<button class="btn" onclick="openPackHub()">✦ Открыть паки</button>`:`<button class="btn secondary" onclick="go('campaign')">♜ Открыть этап</button>`);
    return shell(`<div class="detail-grid catalog-locked-detail"><main class="detail-main"><div class="detail-cover reveal catalog-detail-cover">${imgTag(c)}<div class="catalog-detail-veil"><span>${isStoryCard(c.id)?'♜ СЮЖЕТНАЯ КАРТА':'✦ АРХИВНАЯ КАРТА'}</span><h2>${c.title}</h2><p>${c.subtitle}</p></div></div><section class="section info-pair reveal"><div class="panel info-panel"><div class="eyebrow">Статус</div><h3>${catalogStateLabel(c)}</h3><p>${instruction}</p></div><div class="panel info-panel"><div class="eyebrow">Без спойлеров</div><h3>Историческое досье закрыто</h3><p>Описание, факты, связи, характеристики и личные задания появятся после получения карточки.</p></div></section></main><aside class="detail-aside"><div class="panel"><div class="eyebrow">Способ получения</div><h3>${acquisition.kind==='STORY'?'Основная кампания':`Пул «${pool?.title||'Архив'}»`}</h3><p>${acquisition.kind==='STORY'?'Сюжетные карты никогда не выпадают случайно.':'Архивная карта подчиняется прогрессу активной кампании.'}</p>${action}</div><div class="panel"><button class="btn ghost" onclick="setCollectionView('CATALOG');go('collection')">← Назад в коллекцию</button></div></aside></div>`);
  }
  return V10_PREVIOUS_DETAIL();
};

const V10_PREVIOUS_PROFILE=profile;
profile=function(){
  const html=V10_PREVIOUS_PROFILE();
  const extra=`<section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">▦</div><b>${ownedCards().length}</b><span>карт в архиве</span></div><div class="stat-box"><div class="stat-icon">◫</div><b>${CARDS.length}</b><span>карт в коллекции</span></div><div class="stat-box"><div class="stat-icon">✦</div><b>${availablePackCards().length}</b><span>доступно из паков</span></div><div class="stat-box"><div class="stat-icon">⌁</div><b>${catalogLockedCount()}</b><span>ещё не получено</span></div></section>`;
  return html.replace('</div></main><nav',`${extra}</div></main><nav`);
};

function resetProgress(){
  if(!confirm('Сбросить весь локальный прогресс?'))return;
  localStorage.removeItem(STORE);
  state={...initial,quizResults:{},quizDone:[],missionsCompleted:[],mapTasks:{},timelineTasks:{},discovered:[...initial.unlocked],masteryChecks:{},fragments:0,packHistory:[],dailyPackDate:null,masteryFilter:'ALL',packModal:null,masterySession:null,activeCampaign:'ROME',collectionMode:'ALL',collectionView:'ARCHIVE',catalogScope:'ALL',packPity:{epic:0,legendary:0},personalStoryProgress:{},activeStoryline:null,poolUnlockModal:null,storyChoice:null};
  syncDiscovery();applyTheme();render();showToast('Прогресс сброшен','Можно начать кампанию заново','↺');
}

save();render();
