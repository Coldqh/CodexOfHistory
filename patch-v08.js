/* Codex of History — Patch v0.8: Collection & Mastery */

const MASTERY_META = {
  UNKNOWN:{label:'Неизвестна',percent:0,icon:'◌'},
  DISCOVERED:{label:'Обнаружена',percent:20,icon:'◇'},
  OPENED:{label:'Открыта',percent:40,icon:'▦'},
  STUDIED:{label:'Изучена',percent:65,icon:'✦'},
  MASTERED:{label:'Освоена',percent:85,icon:'◆'},
  CONSOLIDATED:{label:'Закреплена',percent:100,icon:'✓'}
};
const MASTERY_FILTERS=['ALL','UNKNOWN','DISCOVERED','OPENED','STUDIED','MASTERED','CONSOLIDATED'];
const PACK_DEFS={
  DAILY:{id:'DAILY',title:'Архивный пак дня',subtitle:'Один бесплатный пак в сутки',emoji:'☀',drops:3,cost:0},
  ROMAN:{id:'ROMAN',title:'Римский коллекционный пак',subtitle:'Четыре открытия за фрагменты',emoji:'SPQR',drops:4,cost:60}
};
const FRAGMENT_VALUES={RARE:10,EPIC:18,LEGENDARY:34,MYTHIC:60};
const CRAFT_COSTS={RARE:80,EPIC:120,LEGENDARY:180,MYTHIC:260};

state.discovered=Array.isArray(state.discovered)?state.discovered:[...state.unlocked];
state.masteryChecks=state.masteryChecks||{};
state.fragments=Number.isFinite(state.fragments)?state.fragments:0;
state.packHistory=Array.isArray(state.packHistory)?state.packHistory:[];
state.dailyPackDate=state.dailyPackDate||null;
state.masteryFilter=state.masteryFilter||'ALL';
state.packModal=null;
state.masterySession=null;

function save(){
  const snapshot={...state};
  delete snapshot.packModal;
  delete snapshot.masterySession;
  localStorage.setItem(STORE,JSON.stringify(snapshot));
}
function coreCardIds(){return new Set(CAMPAIGN.nodes.flatMap(n=>[...(n.cards||[]),...(n.unlockCards||[])]));}
function isCoreCard(id){return coreCardIds().has(id);}
function discover(ids){(ids||[]).filter(Boolean).forEach(id=>{if(!state.discovered.includes(id))state.discovered.push(id);});}
function isDiscovered(id){return state.discovered.includes(id)||isUnlocked(id);}
function syncDiscovery(){
  discover(state.unlocked);
  CAMPAIGN.nodes.filter(n=>missionOpen(n.id)).forEach(n=>discover(n.cards||[]));
  state.read.forEach(id=>RELATIONS.filter(r=>r.source===id||r.target===id).forEach(r=>discover([r.source===id?r.target:r.source])));
}
function unlock(ids){discover(ids);(ids||[]).filter(Boolean).forEach(id=>{if(!state.unlocked.includes(id))state.unlocked.push(id);});save();}
function relatedNodes(id){return CAMPAIGN.nodes.filter(n=>(n.cards||[]).includes(id)||(n.unlockCards||[]).includes(id));}
function learningActivityPassed(id){
  const nodes=relatedNodes(id);
  if(!nodes.length)return state.read.includes(id);
  return nodes.some(n=>n.quiz?isQuizPassed(n.quiz):missionCompleted(n.id));
}
function masteryInfo(id){
  if(!isDiscovered(id))return {key:'UNKNOWN',...MASTERY_META.UNKNOWN};
  if(!isUnlocked(id))return {key:'DISCOVERED',...MASTERY_META.DISCOVERED};
  if(!state.read.includes(id))return {key:'OPENED',...MASTERY_META.OPENED};
  if(!learningActivityPassed(id))return {key:'STUDIED',...MASTERY_META.STUDIED};
  if(!state.masteryChecks[id]?.passed)return {key:'MASTERED',...MASTERY_META.MASTERED};
  return {key:'CONSOLIDATED',...MASTERY_META.CONSOLIDATED};
}
function masteryPercent(id){return masteryInfo(id).percent;}
function masteryCount(key){return CARDS.filter(c=>masteryInfo(c.id).key===key).length;}
function averageMastery(){return Math.round(CARDS.reduce((sum,c)=>sum+masteryPercent(c.id),0)/Math.max(1,CARDS.length));}
function consolidatedCount(){return masteryCount('CONSOLIDATED');}
function nextMasteryStep(id){
  return ({UNKNOWN:'Найди связь с этой карточкой',DISCOVERED:'Открой через кампанию, пак или фрагменты',OPENED:'Прочитай историческое досье',STUDIED:'Заверши связанную миссию или квиз',MASTERED:'Пройди личную проверку карточки',CONSOLIDATED:'Знание закреплено'})[masteryInfo(id).key];
}
function todayKey(){const d=new Date();return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;}
function dailyPackReady(){return state.dailyPackDate!==todayKey();}
function fragmentValue(c){return FRAGMENT_VALUES[c.rarity]||8;}
function craftCost(c){return CRAFT_COSTS[c.rarity]||100;}
function shuffle(arr){return [...arr].sort(()=>Math.random()-.5);}
function randomDistinct(values,count,exclude=[]){return shuffle([...new Set(values)].filter(v=>v!=null&&!exclude.includes(v))).slice(0,count);}
function weightedPick(items){
  const weights={RARE:52,EPIC:28,LEGENDARY:14,MYTHIC:6};
  const total=items.reduce((s,c)=>s+(weights[c.rarity]||10),0);let roll=Math.random()*total;
  for(const c of items){roll-=weights[c.rarity]||10;if(roll<=0)return c;}return items[items.length-1];
}

function go(tab){
  state.tab=tab;state.selected=null;state.quizFinished=false;state.quizLastResult=null;state.packModal=null;state.masterySession=null;
  save();render();window.scrollTo({top:0,behavior:'smooth'});
}
function openMission(id){
  if(!missionOpen(id))return;
  discover(mission(id)?.cards||[]);
  state.currentMission=id;state.tab='mission';state.selected=null;state.packModal=null;state.masterySession=null;
  save();render();window.scrollTo({top:0,behavior:'smooth'});
}
function openCard(id){
  if(!isDiscovered(id))return;
  state.currentCard=id;state.tab='detail';state.packModal=null;state.masterySession=null;
  if(isUnlocked(id)&&!state.read.includes(id)){
    state.read.push(id);addXp(10);syncDiscovery();showToast('Новое знание','Карточка изучена · +10 XP','✦');
  }
  if(isUnlocked(id)){
    const cm=mission(state.currentMission);
    if(cm?.type==='READ'&&cm.cards.every(x=>state.read.includes(x)))completeMission(cm.id);
  }
  save();render();window.scrollTo({top:0,behavior:'smooth'});
}

function openPack(){openPackHub();}
function openPackHub(){state.packModal={view:'hub'};state.masterySession=null;render();}
function closePack(){state.packModal=null;render();}
function packPool(){const core=coreCardIds();return CARDS.filter(c=>!core.has(c.id));}
function claimPack(kind){
  const def=PACK_DEFS[kind];if(!def)return;
  if(kind==='DAILY'&&!dailyPackReady()){showToast('Пак уже открыт','Следующий архивный пак появится завтра','☀');return;}
  if(def.cost>state.fragments){showToast('Не хватает фрагментов',`Нужно ${def.cost}, сейчас ${state.fragments}`,'◇');return;}
  const pool=packPool();if(!pool.length){showToast('Пул пуст','Бонусные карточки появятся в следующих главах','▦');return;}
  if(def.cost)state.fragments-=def.cost;
  const drops=[];const locked=pool.filter(c=>!isUnlocked(c.id));
  if(locked.length)drops.push(weightedPick(locked));
  while(drops.length<def.drops){const used=new Set(drops.map(c=>c.id));const candidates=pool.filter(c=>!used.has(c.id));drops.push(weightedPick(candidates.length?candidates:pool));}
  let gained=0;
  const result=drops.map(c=>{
    const fresh=!isUnlocked(c.id);
    if(fresh)unlock([c.id]);
    else{const value=fragmentValue(c);state.fragments+=value;gained+=value;}
    return{id:c.id,fresh,fragments:fresh?0:fragmentValue(c)};
  });
  if(kind==='DAILY')state.dailyPackDate=todayKey();
  state.packHistory.push({kind,date:new Date().toISOString(),drops:result});
  state.packModal={view:'result',kind,drops:result,gained};
  save();render();confetti();
}
function craftCard(id){
  const c=card(id);if(!c||isUnlocked(id)||!isDiscovered(id)||isCoreCard(id))return;
  const cost=craftCost(c);
  if(state.fragments<cost){showToast('Не хватает фрагментов',`Для «${c.title}» нужно ${cost}`,'◇');return;}
  state.fragments-=cost;unlock([id]);addXp(20);save();showToast('Карточка создана',`${c.title} · −${cost} фрагментов`,'◆');render();
}
function packModal(){
  if(!state.packModal)return'';
  if(state.packModal.view==='result'){
    const def=PACK_DEFS[state.packModal.kind];
    return `<div class="game-modal-backdrop" onclick="if(event.target===this)closePack()"><section class="game-modal pack-result-modal"><button class="modal-close" onclick="closePack()">×</button><div class="pack-emblem">${def.emoji}</div><div class="eyebrow">Пак открыт</div><h2>${def.title}</h2><p>${state.packModal.gained?`Дубликаты превращены в <b>${state.packModal.gained}</b> фрагментов.`:'Все выпавшие карточки новые.'}</p><div class="pack-drops">${state.packModal.drops.map((d,i)=>{const c=card(d.id);return `<article class="pack-drop ${d.fresh?'fresh':'duplicate'}" style="--delay:${i*100}ms" onclick="closePack();openCard('${c.id}')"><div>${imgTag(c)}</div><span>${d.fresh?'НОВАЯ':`+${d.fragments} ◇`}</span><h3>${c.title}</h3><small>${rarityLabel(c.rarity)}</small></article>`;}).join('')}</div><div class="hero-actions" style="justify-content:center"><button class="btn" onclick="closePack()">Забрать</button><button class="btn secondary" onclick="state.packModal={view:'hub'};render()">Другие паки</button></div></section></div>`;
  }
  return `<div class="game-modal-backdrop" onclick="if(event.target===this)closePack()"><section class="game-modal pack-hub"><button class="modal-close" onclick="closePack()">×</button><div class="pack-hub-head"><div><div class="eyebrow">Коллекционный архив</div><h2>Паки знаний</h2><p>Ключевые знания открываются только кампанией. Паки дают боковые личности, битвы и события.</p></div><div class="fragment-vault"><span>◇</span><b>${state.fragments}</b><small>фрагментов</small></div></div><div class="pack-options">${Object.values(PACK_DEFS).map(def=>{const ready=def.id!=='DAILY'||dailyPackReady();const affordable=state.fragments>=def.cost;return `<article class="pack-option ${def.id.toLowerCase()}"><div class="pack-art">${def.emoji}</div><div class="pack-copy"><small>${def.drops} открытия</small><h3>${def.title}</h3><p>${def.subtitle}. Пока есть закрытые бонусные карточки, первый слот гарантирует новую.</p></div><button class="btn" onclick="claimPack('${def.id}')" ${(!ready||!affordable)?'disabled':''}>${def.id==='DAILY'?(ready?'Открыть бесплатно':'Уже открыт сегодня'):`Открыть · ${def.cost} ◇`}</button></article>`;}).join('')}</div><div class="pack-rules"><b>Правила архива</b><span>Новая карточка добавляется в коллекцию.</span><span>Дубликат распадается на фрагменты.</span><span>Фрагменты собирают обнаруженные бонусные карточки напрямую.</span></div></section></div>`;
}

function buildChoice(correct,pool){const answers=shuffle([correct,...randomDistinct(pool,3,[correct])]);return{answers,correct:answers.indexOf(correct)};}
function buildMasteryQuestions(c){
  const others=CARDS.filter(x=>x.id!==c.id);
  const fact=buildChoice(c.facts[Math.floor(Math.random()*c.facts.length)],others.flatMap(x=>x.facts));
  const date=buildChoice(c.date,others.map(x=>x.date));
  const region=buildChoice(c.region,others.map(x=>x.region));
  return[
    {text:`Какой факт относится к карточке «${c.title}»?`,...fact},
    {text:`Какая датировка связана с карточкой «${c.title}»?`,...date},
    {text:`С каким регионом связана карточка «${c.title}»?`,...region}
  ];
}
function openMasteryCheck(id){
  if(masteryPercent(id)<85){showToast('Проверка пока закрыта',nextMasteryStep(id),'◇');return;}
  const c=card(id);state.masterySession={cardId:id,questions:buildMasteryQuestions(c),index:0,score:0,selected:null,finished:false};state.packModal=null;render();
}
function closeMastery(){state.masterySession=null;render();}
function answerMastery(i){const s=state.masterySession;if(!s||s.selected!==null)return;s.selected=i;if(i===s.questions[s.index].correct)s.score++;render();}
function nextMasteryQuestion(){
  const s=state.masterySession;if(!s)return;
  if(s.index<s.questions.length-1){s.index++;s.selected=null;render();return;}
  const percent=Math.round(s.score/s.questions.length*100);const prev=state.masteryChecks[s.cardId]||{};const passed=percent>=67;const first=passed&&!prev.passed;
  state.masteryChecks[s.cardId]={passed:prev.passed||passed,bestPercent:Math.max(prev.bestPercent||0,percent),attempts:(prev.attempts||0)+1,lastPercent:percent};
  if(first){state.fragments+=10;addXp(35);confetti();}
  s.finished=true;s.percent=percent;s.passed=passed;s.first=first;save();render();
}
function masteryModal(){
  const s=state.masterySession;if(!s)return'';const c=card(s.cardId);
  if(s.finished)return `<div class="game-modal-backdrop" onclick="if(event.target===this)closeMastery()"><section class="game-modal mastery-modal result"><button class="modal-close" onclick="closeMastery()">×</button><div class="mastery-result-icon">${s.passed?'✓':'↻'}</div><div class="eyebrow">Проверка карточки</div><h2>${s.passed?'Знание закреплено':'Нужна ещё попытка'}</h2><p><b>${s.percent}%</b> · ${s.score}/${s.questions.length} правильных. ${s.first?'Награда: +35 XP и +10 ◇.':''}</p><div class="hero-actions" style="justify-content:center"><button class="btn" onclick="openMasteryCheck('${c.id}')">↻ Повторить</button><button class="btn secondary" onclick="closeMastery()">Готово</button></div></section></div>`;
  const q=s.questions[s.index];const picked=s.selected!==null;
  return `<div class="game-modal-backdrop"><section class="game-modal mastery-modal"><button class="modal-close" onclick="closeMastery()">×</button><div class="mastery-modal-head"><div><div class="eyebrow">Личная проверка</div><h2>${c.title}</h2></div><div class="mastery-question-count">${s.index+1}/3</div></div><div class="progress"><span style="width:${(s.index+1)/3*100}%"></span></div><h3>${q.text}</h3><div class="answers mastery-answers">${q.answers.map((a,i)=>`<button data-key="${String.fromCharCode(65+i)}" class="answer ${picked?(i===q.correct?'correct':(i===s.selected?'wrong':'')):''}" onclick="answerMastery(${i})">${esc(a)}</button>`).join('')}</div>${picked?`<button class="btn" onclick="nextMasteryQuestion()">${s.index<2?'Следующий вопрос →':'Завершить проверку'}</button>`:''}</section></div>`;
}

function masteryPill(id){const m=masteryInfo(id);return `<span class="mastery-pill ${m.key.toLowerCase()}">${m.icon} ${m.label}</span>`;}
function masteryAction(c){
  const m=masteryInfo(c.id);
  if(m.key==='MASTERED')return `<button class="btn" onclick="openMasteryCheck('${c.id}')">◆ Закрепить карточку</button>`;
  if(m.key==='CONSOLIDATED')return `<button class="btn secondary" onclick="openMasteryCheck('${c.id}')">✓ Проверить снова</button>`;
  return `<button class="btn secondary" disabled>${nextMasteryStep(c.id)}</button>`;
}
function shell(inner){
  const [section,title]=pageTitle();
  return `<div class="app-layout"><aside class="side-nav"><div class="brand-mark"><img class="brand-logo" src="assets/ui/codex-logo-mark.png" alt="Codex of History"><div class="brand-title"><small>Codex of History</small><h1>История</h1></div></div><div class="nav-kicker">Навигация</div><div class="nav-list">${navButtons('nav-btn')}</div><div class="side-card"><div class="side-level"><strong>${state.level}</strong><em>УРОВЕНЬ</em></div><p>${state.xp} XP · освоение коллекции ${averageMastery()}%</p><div class="progress"><span style="width:${levelProgress()}%"></span></div><div class="side-credit"><span>до нового уровня</span><span>${500-(state.xp%500)} XP</span></div><div class="side-fragments"><span>◇</span><b>${state.fragments}</b> фрагментов</div></div></aside><main class="main-wrap"><header class="command-bar"><div class="command-title"><span>${section}</span><span>·</span><b>${title}</b></div><div class="command-actions">${themeToggle()}<div class="command-pill">◇ ${state.fragments}</div><div class="command-pill">${state.xp} XP</div><button class="command-icon ${dailyPackReady()?'pack-ready':''}" onclick="openPackHub()" title="Паки знаний">✦</button></div></header><div class="top-mobile"><div class="mobile-brand"><img src="assets/ui/codex-logo-mark.png" alt=""><b>Codex</b></div><div class="mobile-tools">${themeToggle()}<button class="mobile-fragments" onclick="openPackHub()">◇ ${state.fragments}</button></div></div><div class="view">${inner}</div></main><nav class="mobile-tabs">${navButtons('')}</nav></div>${packModal()}${masteryModal()}`;
}
function home(){
  const m=currentMission();
  return shell(`<section class="home-hero reveal"><div class="hero-layout"><div class="hero-content"><div class="eyebrow">Глава I · Рождение Рима</div><h2>От легенды о волчице<br><span>к падению царей.</span></h2><p>Семь связанных миссий: карточки, мифы, карта, сабиняне, религия, этрусский город, хронология и финальный экзамен.</p><div class="hero-actions"><button class="btn" onclick="openMission('${m.id}')">${m.emoji} Продолжить: ${m.title}</button><button class="btn secondary" onclick="go('collection')">▦ Коллекция и освоение</button></div></div><div class="hero-orbit"><div class="orbit-core"><div class="core-value"><strong>${averageMastery()}%</strong><span>освоение знаний</span></div></div><div class="orbit-chip one">Закреплено<b>${consolidatedCount()}</b></div><div class="orbit-chip two">Фрагменты<b>${state.fragments} ◇</b></div><div class="orbit-chip three">Миссии<b>${completedMissionCount()}/${CAMPAIGN.nodes.length}</b></div></div></div></section><section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">◇</div><b>${state.discovered.length}/${CARDS.length}</b><span>карточек обнаружено</span></div><div class="stat-box"><div class="stat-icon">▦</div><b>${state.unlocked.length}</b><span>карточек открыто</span></div><div class="stat-box"><div class="stat-icon">✓</div><b>${consolidatedCount()}</b><span>знаний закреплено</span></div><div class="stat-box stat-action" onclick="openPackHub()"><div class="stat-icon">✦</div><b>${dailyPackReady()?'ГОТОВ':'ЗАВТРА'}</b><span>архивный пак дня</span></div></section>`);
}
function renderMiniCard(c){
  const info=masteryInfo(c.id);const unknown=info.key==='UNKNOWN';const discovered=info.key==='DISCOVERED';const clickable=!unknown;
  return `<article class="history-card tilt mastery-${info.key.toLowerCase()} ${unknown?'lock':''}" ${clickable?`onclick="openCard('${c.id}')"`:''}><div class="image-card">${unknown?'<img src="assets/ui/fallback-card.svg" alt="Неизвестная карточка">':imgTag(c)}<span class="rarity-flag">${unknown?'неизвестна':discovered?'обнаружена':rarityLabel(c.rarity)}</span><span class="card-number">${unknown?'??':cardNumber(c)}</span><div class="card-mastery-ring" style="--mastery:${info.percent}"><b>${info.percent}%</b></div></div><div class="card-body"><div class="card-kicker"><span>${unknown?'???':typeIcon(c.type)+' '+typeLabel(c.type)}</span><span>${unknown?'скрыто':c.era}</span></div><h3>${unknown?'Неизвестная карточка':c.title}</h3><p>${unknown?'Исследуй связи и кампании, чтобы обнаружить это знание.':discovered?'Название найдено в исторической сети. Открой карточку через кампанию, пак или фрагменты.':c.summary}</p><div class="card-tags">${unknown?'<span class="tag">неизвестно</span>':masteryPill(c.id)+(discovered?`<span class="tag">${craftCost(c)} ◇</span>`:c.tags.slice(0,2).map(t=>`<span class="tag">${t}</span>`).join(''))}</div><div class="mastery-strip"><span style="width:${info.percent}%"></span></div></div></article>`;
}
function collection(){
  const types=['ALL',...new Set(CARDS.map(c=>c.type))];const rarities=['ALL',...new Set(CARDS.map(c=>c.rarity))];const s=state.search.toLowerCase();
  const list=CARDS.filter(c=>(state.filter==='ALL'||c.type===state.filter)&&(state.rarity==='ALL'||c.rarity===state.rarity)&&(state.masteryFilter==='ALL'||masteryInfo(c.id).key===state.masteryFilter)&&(c.title.toLowerCase().includes(s)||c.original.toLowerCase().includes(s)||c.tags.join(' ').toLowerCase().includes(s)));
  return shell(`<section class="collection-header reveal"><div><div class="eyebrow">Твой архив знаний</div><h2>Коллекция и освоение</h2><p>Карточка не заканчивается на открытии: изучи её, пройди связанное задание и закрепи знание личной проверкой.</p></div><div class="collection-actions"><div class="collection-count">${list.length} найдено</div><button class="btn" onclick="openPackHub()">✦ Паки · ◇ ${state.fragments}</button></div></section><section class="mastery-overview reveal"><div class="mastery-total"><div class="mastery-big-ring" style="--mastery:${averageMastery()}"><strong>${averageMastery()}%</strong><span>общее освоение</span></div></div><div class="mastery-stages">${MASTERY_FILTERS.slice(1).map(k=>{const m=MASTERY_META[k];return `<button class="mastery-stage ${state.masteryFilter===k?'active':''}" onclick="setFilter('masteryFilter','${state.masteryFilter===k?'ALL':k}')"><i>${m.icon}</i><b>${masteryCount(k)}</b><span>${m.label}</span></button>`;}).join('')}</div></section><div class="search-row reveal"><div class="field-wrap"><input id="collection-search" placeholder="Цезарь, Канны, сенат..." value="${esc(state.search)}" oninput="updateSearch(this)"></div><select onchange="setFilter('filter',this.value)">${types.map(t=>`<option value="${t}" ${state.filter===t?'selected':''}>${t==='ALL'?'Все типы':typeLabel(t)}</option>`).join('')}</select><select onchange="setFilter('rarity',this.value)">${rarities.map(r=>`<option value="${r}" ${state.rarity===r?'selected':''}>${r==='ALL'?'Все редкости':rarityLabel(r)}</option>`).join('')}</select><select onchange="setFilter('masteryFilter',this.value)">${MASTERY_FILTERS.map(k=>`<option value="${k}" ${state.masteryFilter===k?'selected':''}>${k==='ALL'?'Все стадии':MASTERY_META[k].label}</option>`).join('')}</select></div><div class="card-grid reveal">${list.map(renderMiniCard).join('')||'<div class="empty">По выбранным фильтрам карточек нет.</div>'}</div>`);
}
function detail(){
  const c=currentCard();const unlocked=isUnlocked(c.id);const info=masteryInfo(c.id);const edges=RELATIONS.filter(r=>r.source===c.id||r.target===c.id);
  if(!unlocked){
    const craftable=!isCoreCard(c.id);
    return shell(`<div class="detail-grid"><main class="detail-main"><div class="detail-cover reveal discovered-cover">${imgTag(c)}<div class="detail-lock-veil"><span>◇ ОБНАРУЖЕНО</span><h2>${c.title}</h2><p>${c.subtitle} · ${c.era}</p></div></div><section class="section info-pair reveal"><div class="panel info-panel"><div class="eyebrow">След в истории</div><h3>Ты обнаружил карточку</h3><p>Название и образ уже видны, но полное досье закрыто. ${craftable?'Бонусную карточку можно получить из пака или собрать из фрагментов.':'Это ключевое знание кампании — его нельзя купить или выбить случайно.'}</p></div><div class="panel info-panel"><div class="eyebrow">Следующий шаг</div><h3>${craftable?`${craftCost(c)} фрагментов`:'Продолжай кампанию'}</h3><p>${craftable?'Дубликаты из паков распадаются на фрагменты. Накопив нужное число, ты откроешь карточку напрямую.':'Ключевые знания всегда открываются честно через миссии.'}</p></div></section></main><aside class="detail-aside"><div class="panel mastery-panel"><div class="eyebrow">Стадия знания</div><div class="detail-mastery-ring" style="--mastery:${info.percent}"><strong>${info.percent}%</strong></div>${masteryPill(c.id)}<p>${nextMasteryStep(c.id)}</p>${craftable?`<button class="btn" onclick="craftCard('${c.id}')" ${state.fragments<craftCost(c)?'disabled':''}>Собрать · ${craftCost(c)} ◇</button>`:`<button class="btn secondary" onclick="go('campaign')">♜ В кампанию</button>`}</div><div class="panel"><div class="eyebrow">Баланс</div><h3>◇ ${state.fragments} фрагментов</h3><p>Открой ежедневный пак, чтобы получить новые карточки и дубликаты.</p><button class="btn secondary" onclick="openPackHub()">✦ Открыть паки</button></div></aside></div>`);
  }
  return shell(`<div class="detail-grid"><main class="detail-main"><div class="detail-cover reveal">${imgTag(c)}<div class="detail-title">${cardBadges(c)}<h2>${c.title}</h2><p>${c.subtitle} · ${c.region}</p></div></div><section class="section info-pair reveal"><div class="panel info-panel"><div class="eyebrow">Коротко</div><h3>Суть карточки</h3><p>${c.summary}</p></div><div class="panel info-panel"><div class="eyebrow">Контекст</div><h3>Почему это важно</h3><p>${c.importance}</p></div></section><section class="section reveal"><div class="section-head"><h2>Три опорных факта</h2><span>${c.era}</span></div><div class="fact-list">${c.facts.map(f=>`<div class="fact">${f}</div>`).join('')}</div></section><section class="section reveal"><div class="section-head"><h2>Связи в истории</h2><span>${edges.length} узлов</span></div><div class="edge-list">${edges.map(r=>{const other=card(r.source===c.id?r.target:r.source);const known=isDiscovered(other.id);return `<article class="edge ${known?'':'unknown-edge'}" onclick="${known?`openCard('${other.id}')`:''}"><b>${r.type.replaceAll('_',' ')}</b><strong>${known?other.title:'Неизвестный узел'}</strong><br>${known?r.description:'Изучи больше карточек, чтобы раскрыть связь.'}</article>`;}).join('')||'<div class="empty">Связей пока нет.</div>'}</div></section></main><aside class="detail-aside"><div class="panel mastery-panel reveal"><div class="eyebrow">Освоение карточки</div><div class="mastery-panel-row"><div class="detail-mastery-ring" style="--mastery:${info.percent}"><strong>${info.percent}%</strong></div><div>${masteryPill(c.id)}<h3>${nextMasteryStep(c.id)}</h3></div></div><div class="mastery-steps-mini">${['DISCOVERED','OPENED','STUDIED','MASTERED','CONSOLIDATED'].map(k=>`<i class="${MASTERY_META[k].percent<=info.percent?'done':''}" title="${MASTERY_META[k].label}"></i>`).join('')}</div>${masteryAction(c)}</div><div class="panel reveal"><div class="eyebrow">Учебные характеристики</div><h3>Профиль знания</h3><div class="bars">${Object.entries(c.stats).map(([k,v])=>`<div class="bar-row"><span>${STAT_LABELS[k]||k}</span><div class="bar-bg"><div class="bar-fill" style="width:${v*10}%"></div></div><b>${v}</b></div>`).join('')}</div></div><div class="panel reveal"><div class="eyebrow">Источник изображения</div><h3>${c.image.caption}</h3><p class="credit">${c.image.credit} · ${c.image.license}</p><div class="hero-actions"><a class="btn ghost" href="${filePage(c.image.file)}" target="_blank" rel="noreferrer">Открыть источник ↗</a></div></div><div class="panel reveal"><div class="eyebrow">Теги</div><div class="card-tags">${c.tags.map(t=>`<span class="tag">#${t}</span>`).join('')}</div></div></aside></div>`);
}
function profile(){
  return shell(`<section class="profile-hero reveal"><div class="profile-main"><div class="eyebrow">Личная хроника</div><h2>Хранитель Codex</h2><p>Прогресс показывает не только число открытых карт, но и реальное освоение знаний.</p><div class="profile-level"><b>${state.level}</b><span>уровень исследователя<br>${state.xp} опыта</span></div><div class="hero-actions"><button class="btn" onclick="openPackHub()">✦ Паки · ◇ ${state.fragments}</button><button class="btn danger" onclick="resetProgress()">↺ Сбросить прогресс</button></div></div><div class="achievement-card"><div class="achievement-medal">${averageMastery()>=80?'♛':'◆'}</div><h3>${averageMastery()>=80?'Мастер архива':'Собиратель знаний'}</h3><p>Общее освоение коллекции: ${averageMastery()}%. Закреплено карточек: ${consolidatedCount()}.</p><div class="progress" style="margin-top:20px"><span style="width:${averageMastery()}%"></span></div></div></section><section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">◆</div><b>${averageMastery()}%</b><span>общее освоение</span></div><div class="stat-box"><div class="stat-icon">✓</div><b>${consolidatedCount()}</b><span>закреплено</span></div><div class="stat-box"><div class="stat-icon">◇</div><b>${state.fragments}</b><span>фрагментов</span></div><div class="stat-box"><div class="stat-icon">✦</div><b>${state.packHistory.length}</b><span>паков открыто</span></div></section><section class="section reveal"><div class="mastery-profile-grid">${MASTERY_FILTERS.slice(1).map(k=>{const m=MASTERY_META[k];return `<div class="panel"><div class="stat-icon">${m.icon}</div><h3>${masteryCount(k)}</h3><p>${m.label}</p></div>`;}).join('')}</div></section>`);
}
function resetProgress(){
  if(!confirm('Сбросить весь локальный прогресс?'))return;
  localStorage.removeItem(STORE);
  state={...initial,quizResults:{},quizDone:[],missionsCompleted:[],mapTasks:{},timelineTasks:{},discovered:[...initial.unlocked],masteryChecks:{},fragments:0,packHistory:[],dailyPackDate:null,masteryFilter:'ALL',packModal:null,masterySession:null};
  syncDiscovery();applyTheme();render();showToast('Прогресс сброшен','Можно начать кампанию заново','↺');
}
function render(){
  syncDiscovery();applyTheme();destroyMaps();
  document.getElementById('app').innerHTML=({home,campaign,mission:missionScreen,collection,detail,quiz,map:mapScreen,profile}[state.tab]||home)();
  requestAnimationFrame(()=>{initEnhancements();initMapsForView();});
}

document.addEventListener('keydown',e=>{
  if(e.key==='Escape'&&state.packModal){e.preventDefault();e.stopImmediatePropagation();closePack();}
  else if(e.key==='Escape'&&state.masterySession){e.preventDefault();e.stopImmediatePropagation();closeMastery();}
},true);

syncDiscovery();
save();
render();
