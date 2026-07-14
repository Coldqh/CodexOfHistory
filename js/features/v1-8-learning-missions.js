/* Codex v1.8 — learning-first mission engine */
PAGE_META.campaign=['Кампания','Учебный маршрут'];
PAGE_META.mission=['Урок','История, хронология и практика'];
NAV.find(x=>x[0]==='campaign')[2]='Обучение';

state.lessonStages=state.lessonStages||{};
state.lessonUnlockedStages=state.lessonUnlockedStages||{};
state.lessonChecks=state.lessonChecks||{};
state.lessonMatches=state.lessonMatches||{};
state.campaignChapter=state.campaignChapter||activeChapter()?.id||CAMPAIGN.chapters[0]?.id;

function lessonData(id){return CODEX_REGISTRY.lessonsByMission?.get(id)||CODEX_LESSONS?.[id];}
function lessonStage(id){return Number(state.lessonStages[id]||0);}
function lessonMaxStage(id){return missionCompleted(id)?3:Number(state.lessonUnlockedStages[id]||0);}
function setLessonStage(id,stage){
  const max=lessonMaxStage(id); if(stage<0||stage>max||stage>3)return;
  state.lessonStages[id]=stage;save();render();window.scrollTo({top:0,behavior:'smooth'});
}
function advanceLesson(id){
  const next=Math.min(3,lessonStage(id)+1);
  state.lessonUnlockedStages[id]=Math.max(Number(state.lessonUnlockedStages[id]||0),next);
  state.lessonStages[id]=next;save();render();window.scrollTo({top:0,behavior:'smooth'});
}
function resetLessonStage(id){state.lessonStages[id]=0;save();render();}
function markLessonCheck(id,passed=true){state.lessonChecks[id]={passed,at:new Date().toISOString()};save();}
function lessonCheckPassed(id){return missionCompleted(id)||!!state.lessonChecks[id]?.passed;}
function finishLearningMission(id){
  markLessonCheck(id,true);
  if(!missionCompleted(id))completeMission(id);else{save();render();showToast('Материал повторён','Главный вывод снова закреплён','✓');}
}
function answerLessonChoice(id,index){
  const a=lessonData(id)?.activity;if(!a||a.type!=='choice')return;
  if(index===a.correct){markLessonCheck(id,true);showToast('Верно',a.explanation||'Вывод собран.','✓');if(!missionCompleted(id))completeMission(id);else render();}
  else{state.lessonChecks[id]={passed:false,lastChoice:index};save();showToast('Подумай ещё',a.explanation||'Вернись к разбору миссии.','↻');render();}
}
function setLessonMatch(id,index,value){
  state.lessonMatches[id]=state.lessonMatches[id]||{};state.lessonMatches[id][index]=value;save();
}
function verifyLessonMatch(id){
  const a=lessonData(id)?.activity;if(!a||a.type!=='match')return;
  const answers=state.lessonMatches[id]||{};
  const ok=a.pairs.every((p,i)=>answers[i]===p.right);
  if(ok){markLessonCheck(id,true);showToast('Система собрана','Все связи распределены верно.','✓');if(!missionCompleted(id))completeMission(id);else render();}
  else{showToast('Есть ошибка','Проверь функции и попробуй снова.','↻');render();}
}
function setCampaignChapter(id){state.campaignChapter=id;state.mapChapter=id;save();render();requestAnimationFrame(()=>document.querySelector('.compact-chapter-switch button.active')?.scrollIntoView({behavior:'smooth',block:'nearest',inline:'center'}));}

missionTypeLabel=function(t){return ({LESSON:'Рассказ',SOURCE:'Работа с источником',CAUSE_EFFECT:'Причины и последствия',MATCH:'Система',MAP:'Карта',TIMELINE:'Хронология',FINAL:'Итог'})[t]||t;};
missionReady=function(m){
  if(!m)return false;
  if(['LESSON','SOURCE','CAUSE_EFFECT','MATCH'].includes(m.type))return lessonCheckPassed(m.id);
  if(m.type==='MAP')return lessonCheckPassed(m.id)&&!!state.mapTasks[m.id]?.passed;
  if(m.type==='TIMELINE')return lessonCheckPassed(m.id)&&!!state.timelineTasks[m.id]?.passed;
  if(m.type==='FINAL')return lessonCheckPassed(m.id)&&isQuizPassed(m.quiz);
  return false;
};

function lessonStageNav(m){
 const labels=[['▤','Рассказ'],['⌛','Хронология'],['◆','Разбор'],['◎','Практика']];const cur=lessonStage(m.id),max=lessonMaxStage(m.id);
 return `<nav class="learning-stage-nav">${labels.map(([icon,label],i)=>`<button class="${i===cur?'active':''} ${i<=max?'':'locked'}" ${i<=max?`onclick="setLessonStage('${m.id}',${i})"`:'disabled'}><i>${icon}</i><span>${label}</span><b>${i+1}</b></button>`).join('')}</nav>`;
}
function lessonObjectives(l){return `<div class="lesson-objectives"><span>После урока ты сможешь</span>${l.objectives.map(x=>`<p>✓ ${esc(x)}</p>`).join('')}</div>`;}
function lessonStory(m,l){return `<section class="lesson-stage learning-story"><div class="lesson-stage-head"><div><small>ЭТАП 1 · ${l.duration} МИН</small><h2>Исторический рассказ</h2></div><span class="lesson-stage-number">01</span></div>${lessonObjectives(l)}<div class="story-flow">${l.story.map((b,i)=>`<article><span>${String(i+1).padStart(2,'0')}</span><div><h3>${esc(b.title)}</h3><p>${esc(b.text)}</p></div></article>`).join('')}</div><div class="learning-next"><button class="btn" onclick="advanceLesson('${m.id}')">К хронологии →</button></div></section>`;}
function certaintyLabel(x){return ({traditional:'традиция',approximate:'примерно',attested:'подтверждено',mixed:'смешанные данные'})[x]||x||'';}
function lessonChronology(m,l){return `<section class="lesson-stage learning-chronology"><div class="lesson-stage-head"><div><small>ЭТАП 2</small><h2>Хронология и развитие</h2></div><span class="lesson-stage-number">02</span></div><div class="learning-timeline">${l.chronology.map((x,i)=>`<article><div class="timeline-pin"></div><time>${esc(x.date)}</time><div><h3>${esc(x.title)}</h3><p>${esc(x.note)}</p><span>${certaintyLabel(x.certainty)}</span></div></article>`).join('')}</div><div class="learning-note"><b>Важно</b><p>Даты ранней римской истории часто являются традиционными опорными точками. Они помогают увидеть порядок событий, но не всегда означают современную документальную точность.</p></div><div class="learning-next split"><button class="btn ghost" onclick="setLessonStage('${m.id}',0)">← Рассказ</button><button class="btn" onclick="advanceLesson('${m.id}')">К разбору →</button></div></section>`;}
function lessonAnalysis(m,l){return `<section class="lesson-stage learning-analysis"><div class="lesson-stage-head"><div><small>ЭТАП 3</small><h2>Как это работает</h2></div><span class="lesson-stage-number">03</span></div><div class="concept-grid">${l.concepts.map(x=>`<article><h3>${esc(x.term)}</h3><p>${esc(x.definition)}</p></article>`).join('')}</div><div class="cause-effect-grid"><article><small>ПРИЧИНЫ</small>${l.causeEffect.causes.map(x=>`<p><span>→</span>${esc(x)}</p>`).join('')}</article><article><small>ПОСЛЕДСТВИЯ</small>${l.causeEffect.consequences.map(x=>`<p><span>→</span>${esc(x)}</p>`).join('')}</article></div><div class="learning-sources"><span>Опорные источники</span>${(l.sources||[]).map(x=>`<a href="${x.url}" target="_blank" rel="noopener">${esc(x.title)} ↗</a>`).join('')}</div><div class="learning-next split"><button class="btn ghost" onclick="setLessonStage('${m.id}',1)">← Хронология</button><button class="btn" onclick="advanceLesson('${m.id}')">К практике →</button></div></section>`;}
function renderChoiceActivity(m,a){const checked=state.lessonChecks[m.id]?.lastChoice;return `<div class="learning-check"><small>СОБЕРИ ВЫВОД</small><h3>${esc(a.prompt)}</h3><div class="learning-choice-list">${a.options.map((x,i)=>`<button class="${checked===i?'wrong':''}" onclick="answerLessonChoice('${m.id}',${i})"><b>${String.fromCharCode(65+i)}</b><span>${esc(x)}</span></button>`).join('')}</div>${a.explanation?`<p class="check-hint">Выбирай не по знакомому слову, а по логике всего урока.</p>`:''}</div>`;}
function renderMatchActivity(m,a){const options=[...new Set(a.pairs.map(x=>x.right))].sort();const answers=state.lessonMatches[m.id]||{};return `<div class="learning-check"><small>СОБЕРИ СИСТЕМУ</small><h3>${esc(a.prompt)}</h3><div class="learning-match-list">${a.pairs.map((p,i)=>`<label><b>${esc(p.left)}</b><select onchange="setLessonMatch('${m.id}',${i},this.value)"><option value="">Выбери функцию</option>${options.map(o=>`<option value="${esc(o)}" ${answers[i]===o?'selected':''}>${esc(o)}</option>`).join('')}</select></label>`).join('')}</div><button class="btn" onclick="verifyLessonMatch('${m.id}')">Проверить систему</button></div>`;}
function renderMapActivity(m){const task=state.mapTasks[m.id]||{step:0,mistakes:0,passed:false};const targets=missionMapTargets(m.id);const target=targets[Math.min(task.step,targets.length-1)];return `<div class="learning-check map-learning-check"><small>ПРАКТИКА НА КАРТЕ</small><div class="map-task-head"><div><h3>${task.passed?'Маршрут найден':`Найди: ${target?.label||'точку'}`}</h3><p>Масштабируй карту и связывай рассказ с реальной географией. Ошибок: <b>${task.mistakes||0}</b>.</p></div><div class="map-progress">${targets.map((_,i)=>`<i class="${i<task.step||task.passed?'done':''}"></i>`).join('')}<b>${task.passed?targets.length:task.step}/${targets.length}</b></div></div><div class="map-shell mission-map-shell"><div id="mission-map" class="leaflet-map" data-mission="${m.id}"></div></div></div>`;}
function renderTimelineActivity(m){const task=state.timelineTasks[m.id]||{selected:[],passed:false};const cfg=timelineConfig(m.id);const options=(cfg.shuffle||cfg.order);return `<div class="learning-check"><small>СОБЕРИ ХРОНОЛОГИЮ</small><h3>${task.passed?'Цепочка собрана':'Нажимай события от раннего к позднему'}</h3><div class="timeline-picked">${task.selected.length?task.selected.map((k,i)=>`<span><b>${i+1}</b>${cfg.labels[k]}</span>`).join(''):'<em>Выбранные события появятся здесь</em>'}</div><div class="timeline-options">${options.filter(k=>!task.selected.includes(k)).map(k=>`<button onclick="chooseTimeline('${m.id}','${k}')">${cfg.labels[k]}</button>`).join('')}</div><button class="btn secondary" onclick="undoTimeline('${m.id}')" ${!task.selected.length?'disabled':''}>← Отменить</button></div>`;}
function renderFinalActivity(m){const r=quizResult(m.quiz);return `<div class="learning-check final-learning-check"><small>ИТОГОВОЕ ИСПЫТАНИЕ</small><h3>${QUIZZES[m.quiz].title}</h3><p>${r?`Лучший результат: <b>${r.bestPercent}%</b>`:`После рассказа и разбора проверь понимание всей главы. Зачёт — ${PASS_PERCENT}%.`}</p><button class="btn" onclick="markLessonCheck('${m.id}',true);openQuiz('${m.quiz}','${m.id}')">${r?'Повторить':'Начать испытание'} →</button></div>`;}
function lessonActivity(m,l){const a=l.activity||{type:'continue'};let content='';if(a.type==='continue')content=`<div class="learning-check conclusion-check"><small>ГЛАВНЫЙ ВЫВОД</small><blockquote>${esc(a.summary||'Материал изучен.')}</blockquote><button class="btn" onclick="finishLearningMission('${m.id}')">${missionCompleted(m.id)?'Повторить вывод':'Закрепить и завершить'}</button></div>`;else if(a.type==='choice')content=renderChoiceActivity(m,a);else if(a.type==='match')content=renderMatchActivity(m,a);else if(a.type==='map')content=renderMapActivity(m);else if(a.type==='timeline')content=renderTimelineActivity(m);else if(a.type==='final_quiz')content=renderFinalActivity(m);return `<section class="lesson-stage learning-practice"><div class="lesson-stage-head"><div><small>ЭТАП 4</small><h2>Практика и закрепление</h2></div><span class="lesson-stage-number">04</span></div>${content}<div class="learning-next"><button class="btn ghost" onclick="setLessonStage('${m.id}',2)">← Вернуться к разбору</button></div></section>`;}
function lessonArchive(m){const cards=m.cards.map(id=>card(id)).filter(Boolean);return `<details class="mission-archive"><summary><span>▦</span><div><b>Карточки миссии</b><small>Наглядные факты и архив · ${cards.length}</small></div><i>⌄</i></summary><div class="card-grid mission-cards compact-archive-cards">${cards.map(renderMiniCard).join('')}</div></details>`;}
function lessonBody(m,l){const stage=lessonStage(m.id);return [lessonStory,lessonChronology,lessonAnalysis,lessonActivity][stage](m,l);}

campaign=function(){
 const current=currentMission();const selected=chapterById(state.campaignChapter)||activeChapter();const missions=chapterMissions(selected);
 return shell(`<section class="learning-campaign-head reveal"><div><div class="eyebrow">РИМСКАЯ КАМПАНИЯ · ${completedMissionCount()}/${CAMPAIGN.nodes.length}</div><h2>${CAMPAIGN.title}</h2><p>История изучается внутри миссий: рассказ → хронология → разбор → практика.</p></div><button class="btn" onclick="openMission('${current.id}')">Продолжить →</button></section>
 <nav class="compact-chapter-switch reveal">${CAMPAIGN.chapters.map(ch=>`<button data-chapter-id="${ch.id}" class="${ch.id===selected.id?'active':''}" onclick="setCampaignChapter('${ch.id}')"><span>${ch.number}</span><div><b>${ch.title}</b><small>${chapterCompleted(ch)}/${chapterMissions(ch).length} · ${chapterProgress(ch)}%</small></div></button>`).join('')}</nav>
 <section class="compact-mission-list reveal"><div class="compact-mission-list-head"><div><small>ГЛАВА ${selected.number}</small><h2>${selected.title}</h2></div><p>${selected.subtitle}</p></div>${missions.map((m,i)=>{const open=missionOpen(m.id),done=missionCompleted(m.id),active=m.id===current.id,l=lessonData(m.id);return `<button class="learning-mission-row ${open?'':'lock'} ${done?'done':''} ${active?'active':''}" ${open?`onclick="openMission('${m.id}')"`:'disabled'}><span class="mission-row-icon">${done?'✓':m.emoji}</span><span class="mission-row-number">${String(i+1).padStart(2,'0')}</span><div><b>${m.title}</b><p>${m.description}</p></div><small>${missionTypeLabel(m.type)} · ${l?.duration||6} мин</small><i>${done?'100%':active?'Далее':'→'}</i></button>`;}).join('')}</section>`);
};

missionScreen=function(){
 const m=mission(state.currentMission)||currentMission();const l=lessonData(m.id);const ch=chapterForMission(m.id);const idx=chapterMissions(ch).findIndex(x=>x.id===m.id);const globalIdx=missionIndex(m.id);if(!l)return shell(`<div class="empty">Для миссии не найден учебный материал.</div>`);
 return shell(`<section class="learning-mission-head reveal"><button class="lesson-back" onclick="go('campaign')">←</button><div><div class="eyebrow">${chapterHeader(ch)} · ${idx+1}/${chapterMissions(ch).length}</div><h1>${m.emoji} ${m.title}</h1><p>${m.description}</p></div><div class="lesson-meta"><b>${l.duration}</b><span>мин</span></div></section>${lessonStageNav(m)}<main class="learning-mission-content reveal">${lessonBody(m,l)}</main>${lessonArchive(m)}<footer class="learning-mission-footer reveal">${globalIdx>0?`<button class="btn ghost" onclick="openMission('${CAMPAIGN.nodes[globalIdx-1].id}')">← Предыдущая</button>`:'<span></span>'}<button class="btn secondary" onclick="go('campaign')">Все миссии</button>${globalIdx<CAMPAIGN.nodes.length-1&&missionOpen(CAMPAIGN.nodes[globalIdx+1].id)?`<button class="btn" onclick="openMission('${CAMPAIGN.nodes[globalIdx+1].id}')">Следующая →</button>`:'<span></span>'}</footer>`);
};

const V18_completeMission=completeMission;
completeMission=function(id){
  if(CODEX_LESSONS?.[id])state.lessonChecks[id]={passed:true,at:new Date().toISOString()};
  V18_completeMission(id);
  render();
};
