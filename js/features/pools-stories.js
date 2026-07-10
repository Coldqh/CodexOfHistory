/* Codex v1.5 — campaign pools and personal stories */
const V09_RARITY_WEIGHTS=CODEX_CONFIG.packs.rarityWeights;
const V09_RARITY_RANK={RARE:1,EPIC:2,LEGENDARY:3,MYTHIC:4};
PAGE_META.storyline=['Личная история','Архивный квест'];
state.activeCampaign=state.activeCampaign||'ROME';
state.collectionMode=state.collectionMode||'ALL';
state.packPity=state.packPity||{epic:0,legendary:0};
state.personalStoryProgress=state.personalStoryProgress||{};
state.activeStoryline=state.activeStoryline||null;
state.poolUnlockModal=null;
state.storyChoice=null;

function save(){
  const snapshot={...state};
  delete snapshot.packModal;delete snapshot.masterySession;delete snapshot.poolUnlockModal;delete snapshot.storyChoice;
  localStorage.setItem(STORE,JSON.stringify(snapshot));
}
function acquisitionInfo(id){return V09_CONTENT.acquisition[id]||{kind:'STORY',campaign:'ROME',chapter:'UNKNOWN'};}
function isStoryCard(id){return acquisitionInfo(id).kind==='STORY';}
function isArchiveCard(id){return acquisitionInfo(id).kind==='ARCHIVE';}
function poolById(id){return V09_CONTENT.pools.find(p=>p.id===id);}
function poolForCard(id){const m=acquisitionInfo(id);return m.pool?poolById(m.pool):null;}
function poolUnlocked(pool){
  if(!pool||pool.campaign!==state.activeCampaign)return false;
  if(pool.unlockMission.startsWith('ROME_CHAPTER_'))return false;
  return missionCompleted(pool.unlockMission);
}
function unlockedPools(){return V09_CONTENT.pools.filter(poolUnlocked);}
function lockedPools(){return V09_CONTENT.pools.filter(p=>p.campaign===state.activeCampaign&&!poolUnlocked(p));}
function archiveAvailable(c){const p=poolForCard(c.id);return !!p&&poolUnlocked(p);}
const V09_isUnlocked=isUnlocked;
isUnlocked=function(id){const c=card(id);return V09_isUnlocked(id)&&(!c||!isArchiveCard(id)||archiveAvailable(c));};
function visibleKnowledgeCards(){return CARDS.filter(c=>isStoryCard(c.id)||archiveAvailable(c));}
function coreCardIds(){return new Set(CARDS.filter(c=>isStoryCard(c.id)).map(c=>c.id));}
function isCoreCard(id){return isStoryCard(id);}
function poolProgress(pool){const cards=pool.cardIds.map(card).filter(Boolean);return {opened:cards.filter(c=>isUnlocked(c.id)).length,total:cards.length};}
function storylineForCard(id){return Object.values(PERSONAL_STORIES).find(s=>s.cardId===id)||null;}
function storyProgress(id){return state.personalStoryProgress[id]||{completed:[],finished:false};}
function storyFinished(id){return !!storyProgress(id).finished;}
function personalStoriesAvailable(){return Object.values(PERSONAL_STORIES).filter(s=>isUnlocked(s.cardId));}
function rarityDepth(r){return ({RARE:'Короткая история',EPIC:'Цепочка заданий',LEGENDARY:'Большая личная линия',MYTHIC:'Боковая глава'})[r]||'Личная история';}

function syncDiscovery(){
  discover(state.unlocked);
  CAMPAIGN.nodes.filter(n=>missionOpen(n.id)).forEach(n=>discover((n.cards||[]).filter(isStoryCard)));
  state.read.forEach(id=>RELATIONS.filter(r=>r.source===id||r.target===id).forEach(r=>{const other=r.source===id?r.target:r.source;if(isStoryCard(other)||archiveAvailable(card(other)||{id:other}))discover([other]);}));
}
function masteryCount(key){return visibleKnowledgeCards().filter(c=>masteryInfo(c.id).key===key).length;}
function averageMastery(){const list=visibleKnowledgeCards();return Math.round(list.reduce((sum,c)=>sum+masteryPercent(c.id),0)/Math.max(1,list.length));}
function collectionProgress(){const list=visibleKnowledgeCards();return Math.round(list.filter(c=>isUnlocked(c.id)).length/Math.max(1,list.length)*100);}

function pickWeighted(items,minRank=1){
  let candidates=items.filter(c=>(V09_RARITY_RANK[c.rarity]||1)>=minRank);if(!candidates.length)candidates=items;
  const total=candidates.reduce((s,c)=>s+(V09_RARITY_WEIGHTS[c.rarity]||1),0);let roll=Math.random()*total;
  for(const c of candidates){roll-=V09_RARITY_WEIGHTS[c.rarity]||1;if(roll<=0)return c;}return candidates[candidates.length-1];
}
function packPool(){return CARDS.filter(c=>isArchiveCard(c.id)&&archiveAvailable(c));}
function pityMinimumRank(){if(state.packPity.legendary>=23)return 3;if(state.packPity.epic>=7)return 2;return 1;}
function claimPack(kind){
  const def=PACK_DEFS[kind];if(!def)return;
  if(!unlockedPools().length){showToast('Архив ещё закрыт','Заверши первую сюжетную миссию, чтобы открыть пул карточек.','♜');return;}
  if(kind==='DAILY'&&!dailyLearningCompleteToday()){showToast('Сначала обучение','Заверши дневную сессию, чтобы разблокировать архивный пак.','◷');return;}
  if(kind==='DAILY'&&!dailyPackReady()){showToast('Пак уже открыт','Следующий архивный пак появится после новой дневной сессии завтра.','☀');return;}
  if(def.cost>state.fragments){showToast('Не хватает фрагментов',`Нужно ${def.cost}, сейчас ${state.fragments}`,'◇');return;}
  const pool=packPool();if(!pool.length){showToast('Пул собран','Все доступные архивные карты уже открыты. Продолжай кампанию.','✓');return;}
  if(def.cost)state.fragments-=def.cost;
  const drops=[];const locked=pool.filter(c=>!isUnlocked(c.id));
  if(locked.length)drops.push(pickWeighted(locked,pityMinimumRank()));
  while(drops.length<def.drops){const used=new Set(drops.map(c=>c.id));const unique=pool.filter(c=>!used.has(c.id));drops.push(pickWeighted(unique.length?unique:pool));}
  let gained=0;const result=drops.map(c=>{const fresh=!isUnlocked(c.id);if(fresh)unlock([c.id]);else{const value=fragmentValue(c);state.fragments+=value;gained+=value;}return{id:c.id,fresh,fragments:fresh?0:fragmentValue(c),storyId:storylineForCard(c.id)?.id||null};});
  const best=Math.max(...drops.map(c=>V09_RARITY_RANK[c.rarity]||1));state.packPity.epic=best>=2?0:state.packPity.epic+1;state.packPity.legendary=best>=3?0:state.packPity.legendary+1;
  if(kind==='DAILY')state.dailyPackDate=todayKey();
  state.packHistory.push({kind,date:new Date().toISOString(),campaign:state.activeCampaign,pools:unlockedPools().map(p=>p.id),drops:result});
  state.packModal={view:'result',kind,drops:result,gained};save();render();confetti();
}
function canCraftArchive(c){return isArchiveCard(c.id)&&archiveAvailable(c)&&isDiscovered(c.id)&&!isUnlocked(c.id);}
function craftCard(id){
  const c=card(id);if(!c||!canCraftArchive(c)){showToast('Карточка недоступна','Сначала открой нужный архивный пул в кампании.','♜');return;}
  const cost=craftCost(c);if(state.fragments<cost){showToast('Не хватает фрагментов',`Для «${c.title}» нужно ${cost}`,'◇');return;}
  state.fragments-=cost;unlock([id]);addXp(20);save();showToast('Архив восстановлен',`${c.title} · −${cost} фрагментов`,'◆');render();
}

const V09_completeMission=completeMission;
completeMission=function(id){
  const before=new Set(unlockedPools().map(p=>p.id));V09_completeMission(id);const opened=unlockedPools().filter(p=>!before.has(p.id));
  if(opened.length)state.poolUnlockModal={pools:opened.map(p=>p.id)};save();
};
function closePoolUnlock(){state.poolUnlockModal=null;render();}
function poolUnlockModal(){
  if(!state.poolUnlockModal)return'';const pools=state.poolUnlockModal.pools.map(poolById).filter(Boolean);
  return `<div class="game-modal-backdrop"><section class="game-modal pool-unlock-modal"><button class="modal-close" onclick="closePoolUnlock()">×</button><div class="pool-unlock-seal">⌁</div><div class="eyebrow">Архив расширен</div><h2>Открыт новый пул истории</h2><div class="pool-unlock-list">${pools.map(p=>`<article class="pool-unlock-card"><span>${p.cardIds.length} карт</span><h3>${p.title}</h3><p>Теперь эти карточки могут выпадать из паков активной кампании.</p></article>`).join('')}</div><div class="hero-actions" style="justify-content:center"><button class="btn" onclick="state.poolUnlockModal=null;openPackHub()">✦ Открыть архив</button><button class="btn secondary" onclick="closePoolUnlock()">Продолжить</button></div></section></div>`;
}

function openPersonalStory(id){if(!PERSONAL_STORIES[id]||!isUnlocked(PERSONAL_STORIES[id].cardId))return;state.activeStoryline=id;state.tab='storyline';state.storyChoice=null;save();render();window.scrollTo({top:0,behavior:'smooth'});}
function activeStory(){return PERSONAL_STORIES[state.activeStoryline]||null;}
function completeStoryStep(storyId,index){
  const story=PERSONAL_STORIES[storyId];if(!story)return;const p=storyProgress(storyId);if(!p.completed.includes(index)){p.completed.push(index);addXp(12);}
  if(p.completed.length>=story.steps.length&&!p.finished){p.finished=true;state.fragments+=story.rewardFragments;addXp(story.rewardXp);confetti();showToast('Личная история завершена',`+${story.rewardXp} XP · +${story.rewardFragments} ◇`,'♛');}
  state.personalStoryProgress[storyId]=p;save();render();
}
function answerStory(storyId,index,choice){
  const story=PERSONAL_STORIES[storyId];const step=story?.steps[index];if(!step||step.type!=='QUESTION')return;
  if(choice===step.correct){showToast('Верно',step.explanation,'✓');completeStoryStep(storyId,index);}else showToast('Неверно','Перечитай сцену и попробуй ещё раз.','↻');
}
function storylineScreen(){
  const s=activeStory();if(!s)return shell('<div class="empty">Личная история не найдена.</div>');const c=card(s.cardId);const p=storyProgress(s.id);const next=s.steps.findIndex((_,i)=>!p.completed.includes(i));const activeIndex=next<0?s.steps.length:next;const pct=Math.round(p.completed.length/s.steps.length*100);
  const step=s.steps[activeIndex];
  let activity=p.finished?`<div class="story-finale"><div class="result-mark">✓</div><h2>История завершена</h2><p>Ты раскрыл личную линию «${s.title}» и закрепил место персонажа в общей истории.</p><div class="score-display">${s.rewardXp} XP <small>+${s.rewardFragments} ◇</small></div><div class="hero-actions" style="justify-content:center"><button class="btn" onclick="openCard('${c.id}')">Открыть карточку</button><button class="btn secondary" onclick="go('collection')">К личным историям</button></div></div>`:'';
  if(!p.finished&&step){
    activity=step.type==='SCENE'?`<div class="story-scene"><div class="eyebrow">Сцена ${activeIndex+1}</div><h2>${step.title}</h2><p>${step.text}</p><button class="btn" onclick="completeStoryStep('${s.id}',${activeIndex})">Продолжить историю →</button></div>`:`<div class="story-question"><div class="eyebrow">Задание ${activeIndex+1}</div><h2>${step.title}</h2><p class="question">${step.question}</p><div class="answers">${step.options.map((o,i)=>`<button class="answer" onclick="answerStory('${s.id}',${activeIndex},${i})">${o}</button>`).join('')}</div></div>`;
  }
  return shell(`<section class="story-hero reveal"><div class="story-portrait">${imgTag(c)}<span>${rarityLabel(c.rarity)}</span></div><div class="story-copy"><div class="eyebrow">${rarityDepth(c.rarity)} · ${s.steps.length} задания</div><h2>${s.title}</h2><p>${s.subtitle}</p><div class="progress"><span style="width:${pct}%"></span></div><small>${p.completed.length} из ${s.steps.length} шагов · награда ${s.rewardXp} XP и ${s.rewardFragments} ◇</small></div></section><section class="story-road reveal">${s.steps.map((st,i)=>`<article class="story-step ${p.completed.includes(i)?'done':i===activeIndex?'active':'locked'}"><i>${p.completed.includes(i)?'✓':String(i+1).padStart(2,'0')}</i><div><b>${st.title}</b><span>${st.type==='SCENE'?'Сюжетная сцена':'Проверка знания'}</span></div></article>`).join('')}</section><section class="story-stage panel reveal">${activity}</section><section class="mission-footer reveal"><button class="btn ghost" onclick="openCard('${c.id}')">← К карточке</button><button class="btn secondary" onclick="go('collection')">Все личные истории</button></section>`);
}

function acquisitionBadge(c){const a=acquisitionInfo(c.id);if(a.kind==='STORY')return '<span class="badge story-badge">♜ Сюжетная</span>';const p=poolForCard(c.id);return `<span class="badge archive-badge">✦ Архивная${p?' · '+p.title:''}</span>`;}
const V09_cardBadges=cardBadges;
cardBadges=function(c,withDate=true){return V09_cardBadges(c,withDate).replace('</div>',`${acquisitionBadge(c)}</div>`);};
const V09_renderMiniCard=renderMiniCard;
renderMiniCard=function(c){
  let html=V09_renderMiniCard(c);const a=acquisitionInfo(c.id);const s=storylineForCard(c.id);const flag=`<span class="acquisition-corner ${a.kind.toLowerCase()}">${a.kind==='STORY'?'♜ сюжет':'✦ архив'}</span>${s&&isUnlocked(c.id)?'<span class="story-corner">⌁</span>':''}`;
  return html.replace('<div class="image-card">',`<div class="image-card">${flag}`);
};

function poolCardsSection(){
  const current=unlockedPools();const future=lockedPools();return `<section class="section reveal"><div class="section-head"><h2>Архивные пулы кампании</h2><span>Паки не выходят за пределы пройденной истории</span></div><div class="pool-grid">${[...current,...future].map(p=>{const pr=poolProgress(p),open=poolUnlocked(p);return `<article class="pool-card ${open?'open':'locked'}"><div class="pool-card-head"><i>${open?'✦':'⌁'}</i><span>${open?'ДОСТУПЕН':'ЗАКРЫТ'}</span></div><h3>${p.title}</h3><p>${open?`${pr.opened} из ${pr.total} карточек открыто`:'Откроется после следующего этапа кампании'}</p><div class="progress"><span style="width:${open?Math.round(pr.opened/pr.total*100):0}%"></span></div></article>`;}).join('')}</div></section>`;
}
const V09_campaign=campaign;
campaign=function(){let html=V09_campaign();return html.replace('</div></main><nav',`${poolCardsSection()}</div></main><nav`);};
const V09_home=home;
home=function(){
  let html=V09_home();const pools=unlockedPools(),available=packPool().filter(c=>!isUnlocked(c.id)).length;
  const extra=`<section class="archive-status reveal"><div><div class="eyebrow">Активная кампания · Рим</div><h3>${pools.length?pools.map(p=>p.title).join(' · '):'Архив пока закрыт'}</h3><p>${pools.length?`В доступных пулах осталось ${available} неоткрытых карточек.`:'Заверши первую миссию, чтобы архивные карты начали выпадать из паков.'}</p></div><button class="btn ${pools.length?'':'secondary'}" onclick="${pools.length?'openPackHub()':`openMission('MIS_BIRTH_01')`}">${pools.length?'✦ Открыть пак':'♜ Начать кампанию'}</button></section>`;
  return html.replace('</div></main><nav',`${extra}</div></main><nav`);
};

function setCollectionMode(mode){state.collectionMode=mode;save();render();}
collection=function(){
  const types=['ALL',...new Set(CARDS.map(c=>c.type))],rarities=['ALL',...new Set(CARDS.map(c=>c.rarity))],s=state.search.toLowerCase();const visible=visibleKnowledgeCards();
  const list=visible.filter(c=>{const m=masteryInfo(c.id);let mode=true;if(state.collectionMode==='STORY')mode=isStoryCard(c.id);if(state.collectionMode==='ARCHIVE')mode=isArchiveCard(c.id);if(state.collectionMode==='STORIES')mode=!!storylineForCard(c.id)&&isUnlocked(c.id);if(state.collectionMode==='MASTERED')mode=m.key==='CONSOLIDATED';if(state.collectionMode==='UNKNOWN')mode=m.key==='UNKNOWN'||m.key==='DISCOVERED';return mode&&(state.filter==='ALL'||c.type===state.filter)&&(state.rarity==='ALL'||c.rarity===state.rarity)&&(state.masteryFilter==='ALL'||m.key===state.masteryFilter)&&(c.title.toLowerCase().includes(s)||c.original.toLowerCase().includes(s)||c.tags.join(' ').toLowerCase().includes(s));});
  const modes=[['ALL','Все'],['STORY','Основной сюжет'],['ARCHIVE','Архив'],['STORIES','Личные истории'],['MASTERED','Закреплённые'],['UNKNOWN','Неизвестные']];
  return shell(`<section class="collection-header reveal"><div><div class="eyebrow">Твой архив знаний</div><h2>Сюжет и скрытые ветви истории</h2><p>Сюжетные карты открываются только кампанией. Архивные падают из паков доступных этапов и могут запускать личные квесты.</p></div><div class="collection-actions"><div class="collection-count">${list.length} найдено</div><button class="btn" onclick="openPackHub()">✦ Паки · ◇ ${state.fragments}</button></div></section><div class="collection-tabs reveal">${modes.map(([id,label])=>`<button class="${state.collectionMode===id?'active':''}" onclick="setCollectionMode('${id}')">${label}</button>`).join('')}</div><section class="mastery-overview reveal"><div class="mastery-total"><div class="mastery-big-ring" style="--mastery:${averageMastery()}"><strong>${averageMastery()}%</strong><span>освоение доступной истории</span></div></div><div class="mastery-stages">${MASTERY_FILTERS.slice(1).map(k=>{const m=MASTERY_META[k];return `<button class="mastery-stage ${state.masteryFilter===k?'active':''}" onclick="setFilter('masteryFilter','${state.masteryFilter===k?'ALL':k}')"><i>${m.icon}</i><b>${masteryCount(k)}</b><span>${m.label}</span></button>`;}).join('')}</div></section><div class="search-row reveal"><div class="field-wrap"><input id="collection-search" placeholder="Ромул, Тарпея, консулы..." value="${esc(state.search)}" oninput="updateSearch(this)"></div><select onchange="setFilter('filter',this.value)">${types.map(t=>`<option value="${t}" ${state.filter===t?'selected':''}>${t==='ALL'?'Все типы':typeLabel(t)}</option>`).join('')}</select><select onchange="setFilter('rarity',this.value)">${rarities.map(r=>`<option value="${r}" ${state.rarity===r?'selected':''}>${r==='ALL'?'Все редкости':rarityLabel(r)}</option>`).join('')}</select><select onchange="setFilter('masteryFilter',this.value)">${MASTERY_FILTERS.map(k=>`<option value="${k}" ${state.masteryFilter===k?'selected':''}>${k==='ALL'?'Все стадии':MASTERY_META[k].label}</option>`).join('')}</select></div><div class="card-grid reveal">${list.map(renderMiniCard).join('')||'<div class="empty">В этом разделе пока нет доступных карточек.</div>'}</div>`);
};

const V09_detail=detail;
detail=function(){
  const c=currentCard(),a=acquisitionInfo(c.id),p=poolForCard(c.id),s=storylineForCard(c.id);
  if(!isUnlocked(c.id)&&a.kind==='ARCHIVE'&&!archiveAvailable(c))return shell(`<div class="detail-grid"><main class="detail-main"><div class="detail-cover reveal discovered-cover">${imgTag(c)}<div class="detail-lock-veil"><span>⌁ ПУЛ ЗАКРЫТ</span><h2>Архив будущего этапа</h2><p>Эта карточка относится к ещё не пройденной части кампании.</p></div></div></main><aside class="detail-aside"><div class="panel"><div class="eyebrow">Историческая последовательность</div><h3>${p?.title||'Будущая глава'}</h3><p>Карточка не может выпасть из пака и не собирается за фрагменты, пока соответствующий этап истории не открыт.</p><button class="btn secondary" onclick="go('campaign')">♜ К кампании</button></div></aside></div>`);
  let html=V09_detail();const extra=`<div class="panel acquisition-panel reveal"><div class="eyebrow">Способ получения</div><h3>${a.kind==='STORY'?'♜ Сюжетная карточка':'✦ Архивная карточка'}</h3><p>${a.kind==='STORY'?'Открывается только в основной кампании и никогда не выпадает случайно.':`Доступна из пула «${p?.title||'Архив'}» активной кампании.`}</p></div>${s&&isUnlocked(c.id)?`<div class="panel personal-story-panel reveal"><div class="eyebrow">${rarityDepth(c.rarity)}</div><h3>⌁ ${s.title}</h3><p>${s.steps.length} задания · награда ${s.rewardXp} XP и ${s.rewardFragments} ◇</p><button class="btn" onclick="openPersonalStory('${s.id}')">${storyFinished(s.id)?'Повторить историю':'Начать личную историю'} →</button></div>`:''}`;
  return html.replace('</aside>',`${extra}</aside>`);
};

function packModal(){
  if(!state.packModal)return'';
  if(state.packModal.view==='result'){const def=PACK_DEFS[state.packModal.kind];return `<div class="game-modal-backdrop" onclick="if(event.target===this)closePack()"><section class="game-modal pack-result-modal"><button class="modal-close" onclick="closePack()">×</button><div class="pack-emblem">${def.emoji}</div><div class="eyebrow">Архив активной кампании</div><h2>${def.title}</h2><p>${state.packModal.gained?`Дубликаты превращены в <b>${state.packModal.gained}</b> фрагментов.`:'Открыты новые части истории.'}</p><div class="pack-drops">${state.packModal.drops.map((d,i)=>{const c=card(d.id),story=d.storyId?PERSONAL_STORIES[d.storyId]:null;return `<article class="pack-drop ${d.fresh?'fresh':'duplicate'}" style="--delay:${i*100}ms" onclick="closePack();openCard('${c.id}')"><div>${imgTag(c)}</div><span>${d.fresh?'НОВАЯ':`+${d.fragments} ◇`}</span><h3>${c.title}</h3><small>${rarityLabel(c.rarity)} · ${poolForCard(c.id)?.title||''}</small>${story&&d.fresh?'<b class="story-drop-label">⌁ Личная история</b>':''}</article>`;}).join('')}</div><div class="hero-actions" style="justify-content:center"><button class="btn" onclick="closePack()">Забрать</button><button class="btn secondary" onclick="state.packModal={view:'hub'};render()">Ещё паки</button></div></section></div>`;}
  const pools=unlockedPools(),available=packPool().filter(c=>!isUnlocked(c.id)).length;
  return `<div class="game-modal-backdrop" onclick="if(event.target===this)closePack()"><section class="game-modal pack-hub-modal"><button class="modal-close" onclick="closePack()">×</button><div class="pack-hub-head"><div><div class="eyebrow">Активная кампания · Рим</div><h2>Архивные паки</h2><p>Выпадают только карточки из уже открытых этапов. Будущие эпохи и главы полностью исключены.</p></div><div class="fragment-balance"><span>◇</span><b>${state.fragments}</b><small>фрагментов</small></div></div><div class="active-pools">${pools.length?pools.map(p=>{const pr=poolProgress(p);return `<span>✦ ${p.title} · ${pr.opened}/${pr.total}</span>`;}).join(''):'<span>⌁ Заверши первую миссию, чтобы открыть архив</span>'}</div><div class="pack-options"><article class="pack-option ${dailyPackReady()&&pools.length?'ready':''}"><div class="pack-option-icon">☀</div><div><div class="eyebrow">Ежедневный</div><h3>Архивный пак дня</h3><p>3 карточки · открывается после ежедневной учебной сессии.</p><small>До гарантии Epic: ${Math.max(0,8-state.packPity.epic)} паков · Legendary: ${Math.max(0,24-state.packPity.legendary)}</small></div><button class="btn" onclick="claimPack('DAILY')" ${!dailyPackReady()||!pools.length?'disabled':''}>${dailyPackReady()?'Открыть бесплатно':dailyLearningCompleteToday()?'Уже открыт':'Сначала урок'}</button></article><article class="pack-option"><div class="pack-option-icon">SPQR</div><div><div class="eyebrow">Коллекционный</div><h3>Римский архивный пак</h3><p>4 карточки из всех доступных пулов кампании.</p><small>Доступно новых карточек: ${available}</small></div><button class="btn secondary" onclick="claimPack('ROMAN')" ${state.fragments<PACK_DEFS.ROMAN.cost||!pools.length?'disabled':''}>60 ◇</button></article></div></section></div>`;
}

const V09_shell=shell;
shell=function(inner){return V09_shell(inner)+poolUnlockModal();};
const V09_profile=profile;
profile=function(){let html=V09_profile();const finished=Object.values(PERSONAL_STORIES).filter(s=>storyFinished(s.id)).length;const extra=`<section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">♜</div><b>${CARDS.filter(c=>isStoryCard(c.id)&&isUnlocked(c.id)).length}</b><span>сюжетных карт</span></div><div class="stat-box"><div class="stat-icon">✦</div><b>${CARDS.filter(c=>isArchiveCard(c.id)&&isUnlocked(c.id)).length}</b><span>архивных карт</span></div><div class="stat-box"><div class="stat-icon">⌁</div><b>${finished}/${personalStoriesAvailable().length}</b><span>личных историй</span></div><div class="stat-box"><div class="stat-icon">▤</div><b>${unlockedPools().length}</b><span>пулов открыто</span></div></section>`;return html.replace('</div></main><nav',`${extra}</div></main><nav`);};

function resetProgress(){
  if(!confirm('Сбросить весь локальный прогресс?'))return;localStorage.removeItem(STORE);
  state={...initial,quizResults:{},quizDone:[],missionsCompleted:[],mapTasks:{},timelineTasks:{},discovered:[...initial.unlocked],masteryChecks:{},fragments:0,packHistory:[],dailyPackDate:null,masteryFilter:'ALL',packModal:null,masterySession:null,activeCampaign:'ROME',collectionMode:'ALL',packPity:{epic:0,legendary:0},personalStoryProgress:{},activeStoryline:null,poolUnlockModal:null,storyChoice:null};
  syncDiscovery();applyTheme();render();showToast('Прогресс сброшен','Можно начать кампанию заново','↺');
}
function render(){
  syncDiscovery();applyTheme();destroyMaps();
  document.getElementById('app').innerHTML=({home,campaign,mission:missionScreen,collection,detail,quiz,map:mapScreen,profile,storyline:storylineScreen}[state.tab]||home)();
  requestAnimationFrame(()=>{initEnhancements();initMapsForView();});
}

document.addEventListener('keydown',e=>{if(e.key==='Escape'&&state.tab==='storyline'){e.preventDefault();openCard(PERSONAL_STORIES[state.activeStoryline].cardId);}},true);

