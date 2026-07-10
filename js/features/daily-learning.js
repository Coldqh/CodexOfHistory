/* Codex v1.2 — daily learning, spaced repetition and error analytics */
const DAILY_CONFIG=CODEX_CONFIG.daily;
const DAILY_INTERVALS=DAILY_CONFIG.interval_days;
const DAILY_RULES=DAILY_CONFIG.session;
PAGE_META.daily=['Сегодня','Ежедневное обучение'];
if(!NAV.some(item=>item[0]==='daily')) NAV.splice(1,0,['daily','◷','Сегодня']);

state.reviewSchedule=state.reviewSchedule&&typeof state.reviewSchedule==='object'?state.reviewSchedule:{};
state.dailyHistory=state.dailyHistory&&typeof state.dailyHistory==='object'?state.dailyHistory:{};
state.learningDays=Array.isArray(state.learningDays)?state.learningDays:[];
state.dailySession=state.dailySession&&typeof state.dailySession==='object'?state.dailySession:null;
state.dailyStats=state.dailyStats&&typeof state.dailyStats==='object'?state.dailyStats:{sessions:0,answers:0,correct:0};

function dailyDateKey(date=new Date()){
  return `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
}
function dailyAddDays(key,days){
  const [y,m,d]=key.split('-').map(Number);const date=new Date(y,m-1,d);date.setDate(date.getDate()+days);return dailyDateKey(date);
}
function dailyFormatDate(key){
  if(!key)return 'не назначено';
  const [y,m,d]=key.split('-').map(Number);return new Intl.DateTimeFormat('ru-RU',{day:'numeric',month:'short'}).format(new Date(y,m-1,d));
}
function dailyHash(value){let h=0;for(const ch of String(value))h=(h*31+ch.charCodeAt(0))>>>0;return h;}
function dailyUnique(values){return [...new Set(values.filter(v=>v!==undefined&&v!==null&&String(v).trim()!==''))];}
function dailyOptions(correct,values,count=4){
  const reserve=['Другой исторический контекст','Другая датировка','Другой регион','Нет прямой связи'];
  const pool=dailyUnique([...values,...reserve]).filter(v=>v!==correct);
  const distractors=shuffle(pool).slice(0,Math.max(1,count-1));
  const answers=shuffle([correct,...distractors]);return {answers,correct:answers.indexOf(correct)};
}
function dailyOwnedStudied(){return ownedCards().filter(c=>state.read.includes(c.id));}
function dailyScheduleCard(id,due=dailyAddDays(dailyDateKey(),1)){
  if(!card(id)||state.reviewSchedule[id])return;
  state.reviewSchedule[id]={stage:0,due,lastReviewed:null,lastResult:null,attempts:0,correct:0,wrong:0};
}
function dailySyncSchedule(){
  const today=dailyDateKey();const firstMigration=Object.keys(state.reviewSchedule).length===0&&state.read.length>0;
  state.read.filter(id=>isUnlocked(id)).forEach(id=>dailyScheduleCard(id,firstMigration?today:dailyAddDays(today,1)));
}
function dailyDueCards(){
  dailySyncSchedule();const today=dailyDateKey();
  return dailyOwnedStudied().filter(c=>(state.reviewSchedule[c.id]?.due||'9999-12-31')<=today)
    .sort((a,b)=>(state.reviewSchedule[a.id]?.due||'').localeCompare(state.reviewSchedule[b.id]?.due||'')||(state.reviewSchedule[a.id]?.stage||0)-(state.reviewSchedule[b.id]?.stage||0));
}
function dailyLearningCompleteToday(){return !!state.dailyHistory[dailyDateKey()]?.completed;}
function dailyPackStatusShort(){
  if(!dailyLearningCompleteToday())return 'УРОК';
  return state.dailyPackDate===dailyDateKey()?'ОТКРЫТ':'ГОТОВ';
}
// The free archive pack is now earned by completing the daily study session.
dailyPackReady=function(){return dailyLearningCompleteToday()&&state.dailyPackDate!==dailyDateKey();};
function dailyRetention(){
  const rows=Object.values(state.reviewSchedule);const attempts=rows.reduce((s,r)=>s+(r.attempts||0),0);const correct=rows.reduce((s,r)=>s+(r.correct||0),0);
  return attempts?Math.round(correct/attempts*100):0;
}
function dailyNextDue(){
  dailySyncSchedule();const dates=Object.values(state.reviewSchedule).map(r=>r.due).filter(Boolean).sort();return dates[0]||null;
}
function dailyWeakCards(limit=4){
  return dailyOwnedStudied().map(c=>{const r=state.reviewSchedule[c.id]||{};const accuracy=r.attempts?Math.round((r.correct||0)/r.attempts*100):100;return {c,accuracy,attempts:r.attempts||0,stage:r.stage||0,due:r.due};})
    .filter(x=>x.attempts>0).sort((a,b)=>a.accuracy-b.accuracy||a.stage-b.stage).slice(0,limit);
}
function dailyBuildCardTask(c,offset=0){
  const learned=dailyOwnedStudied().filter(x=>x.id!==c.id);const mode=(dailyHash(c.id+dailyDateKey())+offset)%3;
  if(mode===0){
    const correct=c.facts[0];const choice=dailyOptions(correct,learned.map(x=>x.facts[0]));
    return {kind:'REVIEW',cardId:c.id,label:'Опорный факт',text:`Какой факт относится к карточке «${c.title}»?`,...choice,explanation:correct};
  }
  if(mode===1){
    const correct=c.date;const choice=dailyOptions(correct,learned.map(x=>x.date));
    return {kind:'REVIEW',cardId:c.id,label:'Хронология',text:`Какая датировка связана с карточкой «${c.title}»?`,...choice,explanation:`${c.title}: ${c.date}.`};
  }
  const correct=c.region;const choice=dailyOptions(correct,learned.map(x=>x.region));
  return {kind:'REVIEW',cardId:c.id,label:'География',text:`С каким регионом связана карточка «${c.title}»?`,...choice,explanation:`Основной регион карточки — ${c.region}.`};
}
function dailyBuildRelationTask(){
  const owned=new Set(ownedCards().map(c=>c.id));const edges=RELATIONS.filter(r=>owned.has(r.source)&&owned.has(r.target));
  if(!edges.length)return null;
  const edge=edges[dailyHash(dailyDateKey()+state.xp)%edges.length];const source=card(edge.source),target=card(edge.target);
  const choice=dailyOptions(target.title,ownedCards().filter(c=>c.id!==source.id&&c.id!==target.id).map(c=>c.title));
  return {kind:'RELATION',cardId:source.id,label:'Историческая связь',text:`Какая карточка напрямую связана с «${source.title}» отношением «${edge.type.replaceAll('_',' ')}»?`,...choice,explanation:edge.description};
}
function dailyBuildChallengeTask(){
  const cards=dailyOwnedStudied();if(!cards.length)return null;
  const c=cards[dailyHash(`${dailyDateKey()}-challenge`)%cards.length];
  const choice=dailyOptions(c.title,cards.filter(x=>x.id!==c.id).map(x=>x.title));
  return {kind:'CHALLENGE',cardId:c.id,label:'Угадай карточку',text:`О какой карточке идёт речь: «${c.summary}»`,...choice,explanation:`Это «${c.title}». ${c.importance}`};
}
function dailyBuildSession(replay=false){
  dailySyncSchedule();const due=dailyDueCards();const learned=dailyOwnedStudied();
  const selected=[...due.slice(0,DAILY_RULES.review_cards)];
  if(selected.length<DAILY_RULES.review_cards){
    const fallback=learned.filter(c=>!selected.some(x=>x.id===c.id)).sort((a,b)=>(state.reviewSchedule[a.id]?.stage||0)-(state.reviewSchedule[b.id]?.stage||0));
    selected.push(...fallback.slice(0,DAILY_RULES.review_cards-selected.length));
  }
  const tasks=selected.map((c,i)=>dailyBuildCardTask(c,i));
  const relation=dailyBuildRelationTask();if(relation)tasks.push(relation);
  const challenge=dailyBuildChallengeTask();if(challenge)tasks.push(challenge);
  return {date:dailyDateKey(),index:0,score:0,selected:null,answered:false,results:[],tasks,completed:false,rewardEligible:!dailyLearningCompleteToday()&&!replay,startedAt:new Date().toISOString()};
}
function startDailySession(replay=false){
  dailySyncSchedule();
  if(!dailyOwnedStudied().length){showToast('Пока нечего повторять','Открой и прочитай хотя бы одну карточку.','▦');go('campaign');return;}
  state.dailySession=dailyBuildSession(replay);state.tab='daily';save();render();window.scrollTo({top:0,behavior:'smooth'});
}
function dailyCurrentTask(){return state.dailySession?.tasks?.[state.dailySession.index]||null;}
function dailyApplyReview(cardId,correct){
  if(!cardId)return;dailyScheduleCard(cardId,dailyDateKey());const row=state.reviewSchedule[cardId];
  row.attempts=(row.attempts||0)+1;row.lastReviewed=new Date().toISOString();row.lastResult=correct?'correct':'wrong';
  if(correct){row.correct=(row.correct||0)+1;row.stage=Math.min((row.stage||0)+1,DAILY_INTERVALS.length-1);row.due=dailyAddDays(dailyDateKey(),DAILY_INTERVALS[row.stage]);}
  else{row.wrong=(row.wrong||0)+1;row.stage=0;row.due=dailyAddDays(dailyDateKey(),DAILY_INTERVALS[0]);}
}
function answerDaily(index){
  const session=state.dailySession,task=dailyCurrentTask();if(!session||!task||session.selected!==null)return;
  const correct=index===task.correct;session.selected=index;session.answered=true;if(correct)session.score++;
  session.results.push({kind:task.kind,cardId:task.cardId,correct,answered:index});
  state.dailyStats.answers=(state.dailyStats.answers||0)+1;if(correct)state.dailyStats.correct=(state.dailyStats.correct||0)+1;
  if(task.kind==='REVIEW')dailyApplyReview(task.cardId,correct);
  save();render();
}
function nextDailyTask(){
  const session=state.dailySession;if(!session||session.selected===null)return;
  if(session.index<session.tasks.length-1){session.index++;session.selected=null;session.answered=false;save();render();return;}
  finishDailySession();
}
function finishDailySession(){
  const session=state.dailySession;if(!session||session.completed)return;
  const total=session.tasks.length,percent=Math.round(session.score/Math.max(1,total)*100);const first=session.rewardEligible;
  let xp=0,fragments=0;
  if(first){xp=DAILY_RULES.xp_reward;fragments=DAILY_RULES.fragment_reward;if(percent===100){xp+=DAILY_RULES.perfect_bonus_xp;fragments+=DAILY_RULES.perfect_bonus_fragments;}addXp(xp);state.fragments+=fragments;}
  session.completed=true;session.percent=percent;session.finishedAt=new Date().toISOString();session.reward={xp,fragments};
  state.dailyHistory[dailyDateKey()]={completed:true,score:session.score,total,percent,xp,fragments,completedAt:session.finishedAt};
  if(!state.learningDays.includes(dailyDateKey()))state.learningDays.push(dailyDateKey());state.dailyStats.sessions=(state.dailyStats.sessions||0)+1;
  save();if(percent>=DAILY_RULES.pass_percent)confetti();render();showToast('Дневная сессия завершена',`${percent}% · архивный пак доступен`,'◷');
}
function abandonDailySession(){state.dailySession=null;save();go('home');}
function openDaily(){state.tab='daily';save();render();window.scrollTo({top:0,behavior:'smooth'});}

function dailyTaskArtwork(task){const c=card(task.cardId);return c?`<div class="daily-task-art">${imgTag(c)}</div>`:'<div class="daily-task-art daily-symbol">◷</div>';}
function dailySessionView(){
  const s=state.dailySession,task=dailyCurrentTask();if(!s||!task)return dailyOverview();
  if(s.completed){
    return shell(`<section class="daily-result reveal"><div class="daily-result-seal">${s.percent>=DAILY_RULES.pass_percent?'✓':'↻'}</div><div class="eyebrow">Сессия завершена</div><h2>${s.percent}% правильных</h2><p>${s.score} из ${s.tasks.length} заданий. Ошибочные карточки вернутся раньше, уверенные ответы увеличили интервал повторения.</p><div class="daily-reward-row"><span>+${s.reward?.xp||0} XP</span><span>+${s.reward?.fragments||0} ◇</span><span>✦ Пак дня открыт</span></div><div class="progress"><span style="width:${s.percent}%"></span></div><div class="hero-actions" style="justify-content:center"><button class="btn" onclick="openPackHub()">✦ Открыть архивный пак</button><button class="btn secondary" onclick="startDailySession(true)">↻ Повторить без награды</button><button class="btn ghost" onclick="abandonDailySession()">На главную</button></div></section>`);
  }
  const picked=s.selected!==null;const progress=Math.round((s.index+1)/s.tasks.length*100);const c=card(task.cardId);
  return shell(`<section class="daily-focus reveal"><header class="daily-focus-head"><div><div class="eyebrow">${task.label}</div><h2>Ежедневная сессия</h2></div><div class="daily-counter">${s.index+1}/${s.tasks.length}</div></header><div class="daily-lesson-card">${dailyTaskArtwork(task)}<div class="daily-task-copy"><div class="daily-task-meta"><span>${task.kind==='REVIEW'?'Повторение':task.kind==='RELATION'?'Связи':'Быстрый вызов'}</span><b>${c?.title||'Codex'}</b></div><div class="progress"><span style="width:${progress}%"></span></div><h3>${esc(task.text)}</h3><div class="answers daily-answers">${task.answers.map((a,i)=>`<button data-key="${String.fromCharCode(65+i)}" class="answer ${picked?(i===task.correct?'correct':(i===s.selected?'wrong':'')):''}" onclick="answerDaily(${i})">${esc(a)}</button>`).join('')}</div>${picked?`<div class="explain">${esc(task.explanation)}</div><button class="btn" onclick="nextDailyTask()">${s.index<s.tasks.length-1?'Следующее задание →':'Завершить сессию'}</button>`:''}</div></div><button class="daily-exit" onclick="abandonDailySession()">Сохранить и выйти</button></section>`);
}
function dailyOverview(){
  dailySyncSchedule();const due=dailyDueCards(),history=state.dailyHistory[dailyDateKey()],completed=!!history?.completed,weak=dailyWeakCards();const next=dailyNextDue();
  if(!dailyOwnedStudied().length){
    return shell(`<section class="daily-empty reveal"><div class="daily-empty-mark">◷</div><div class="eyebrow">Ежедневное обучение</div><h2>Сначала открой знания</h2><p>Прочитай хотя бы одну полученную карточку. После этого Codex начнёт строить персональный граф повторений.</p><button class="btn" onclick="go('campaign')">♜ Перейти в кампанию</button></section>`);
  }
  return shell(`<section class="daily-hero reveal"><div class="daily-hero-copy"><div class="eyebrow">Сегодня · ${dailyFormatDate(dailyDateKey())}</div><h2>${completed?'Дневная работа выполнена':'Верни знания в память.'}</h2><p>${completed?`Лучший результат сегодня — ${history.percent}%. Можно повторить сессию без награды или забрать архивный пак.`:`Codex подготовил ${Math.max(1,due.length)} карточки на повторение, связь и быстрый исторический вызов.`}</p><div class="hero-actions"><button class="btn" onclick="${completed?'startDailySession(true)':'startDailySession(false)'}">${completed?'↻ Повторить сессию':'◷ Начать на 5 минут'}</button>${completed&&dailyPackReady()?'<button class="btn secondary" onclick="openPackHub()">✦ Забрать пак дня</button>':''}</div></div><div class="daily-clock"><div class="daily-clock-ring" style="--daily:${completed?100:Math.min(100,due.length/Math.max(1,DAILY_RULES.review_cards)*100)}"><strong>${completed?'✓':due.length}</strong><span>${completed?'готово':'к повторению'}</span></div></div></section><section class="daily-metrics reveal"><article><i>◷</i><b>${due.length}</b><span>срок повторения наступил</span></article><article><i>◎</i><b>${dailyRetention()}%</b><span>точность повторений</span></article><article><i>▤</i><b>${state.learningDays.length}</b><span>учебных дней</span></article><article><i>→</i><b>${next?dailyFormatDate(next):'—'}</b><span>ближайшее повторение</span></article></section><section class="section reveal"><div class="section-head"><h2>Очередь памяти</h2><span>ошибки возвращаются раньше</span></div><div class="daily-queue">${(due.length?due:dailyOwnedStudied().slice(0,4)).slice(0,4).map(c=>{const r=state.reviewSchedule[c.id];return `<article onclick="openCard('${c.id}')">${imgTag(c)}<div><small>${(r?.due||dailyDateKey())<=dailyDateKey()?'нужно повторить':`повтор ${dailyFormatDate(r?.due)}`}</small><h3>${c.title}</h3><span>интервал ${DAILY_INTERVALS[r?.stage||0]} дн.</span></div></article>`;}).join('')}</div></section><section class="section reveal"><div class="section-head"><h2>Слабые места</h2><span>по истории ответов</span></div><div class="daily-weak-grid">${weak.length?weak.map(x=>`<article class="panel panel-click" onclick="openCard('${x.c.id}')"><div class="eyebrow">${x.accuracy}% верно</div><h3>${x.c.title}</h3><p>${x.attempts} ответов · следующее повторение ${dailyFormatDate(x.due)}</p><div class="progress"><span style="width:${x.accuracy}%"></span></div></article>`).join(''):'<div class="empty">Ошибок пока нет. Пройди первую дневную сессию.</div>'}</div></section>`);
}
function dailyScreen(){return state.dailySession&&state.dailySession.date===dailyDateKey()?dailySessionView():dailyOverview();}

const V12_openCard=openCard;
openCard=function(id){
  const firstRead=isUnlocked(id)&&!state.read.includes(id);if(firstRead)dailyScheduleCard(id,dailyAddDays(dailyDateKey(),1));V12_openCard(id);
};
const V12_home=home;
home=function(){
  const html=V12_home(),due=dailyDueCards(),done=dailyLearningCompleteToday();
  const block=`<section class="daily-home-card reveal" onclick="openDaily()"><div class="daily-home-icon">◷</div><div><div class="eyebrow">Ежедневное обучение</div><h3>${done?'Сессия выполнена':'Сегодня к повторению: '+due.length}</h3><p>${done?'Архивный пак разблокирован. Результат сохранён в статистике памяти.':'5 минут: карточки, связь и быстрый вызов. Без штрафа за пропущенные дни.'}</p></div><button class="btn ${done?'secondary':''}">${done?'Открыть результат':'Начать'}</button></section>`;
  return html.replace('</div></main><nav',`${block}</div></main><nav`);
};
const V12_profile=profile;
profile=function(){
  const html=V12_profile();const extra=`<section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">◷</div><b>${state.learningDays.length}</b><span>учебных дней</span></div><div class="stat-box"><div class="stat-icon">◎</div><b>${dailyRetention()}%</b><span>точность памяти</span></div><div class="stat-box"><div class="stat-icon">↻</div><b>${dailyDueCards().length}</b><span>ждут повторения</span></div><div class="stat-box"><div class="stat-icon">✓</div><b>${Object.keys(state.dailyHistory).length}</b><span>дневных сессий</span></div></section>`;return html.replace('</div></main><nav',`${extra}</div></main><nav`);
};
const V12_resetProgress=resetProgress;
resetProgress=function(){
  if(!confirm('Сбросить весь локальный прогресс?'))return;
  localStorage.removeItem(STORE);
  state={...initial,quizResults:{},quizDone:[],missionsCompleted:[],mapTasks:{},timelineTasks:{},discovered:[...initial.unlocked],masteryChecks:{},fragments:0,packHistory:[],dailyPackDate:null,masteryFilter:'ALL',packModal:null,masterySession:null,activeCampaign:'ROME',collectionMode:'ALL',collectionView:'ARCHIVE',catalogScope:'ALL',packPity:{epic:0,legendary:0},personalStoryProgress:{},activeStoryline:null,poolUnlockModal:null,storyChoice:null,reviewSchedule:{},dailyHistory:{},learningDays:[],dailySession:null,dailyStats:{sessions:0,answers:0,correct:0}};
  dailySyncSchedule();syncDiscovery();applyTheme();render();showToast('Прогресс сброшен','Можно начать кампанию заново','↺');
};
render=function(){
  dailySyncSchedule();syncDiscovery();applyTheme();destroyMaps();
  applyPreferences?.();
  document.getElementById('app').innerHTML=({home,daily:dailyScreen,campaign,mission:missionScreen,collection,detail,quiz,map:mapScreen,profile,storyline:storylineScreen,settings:settingsScreen}[state.tab]||home)();
  requestAnimationFrame(()=>{initEnhancements();initMapsForView();});
};

dailySyncSchedule();
