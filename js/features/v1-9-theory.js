/* Codex v1.9 — encyclopedic theory layer */
PAGE_META.mission=['Урок','Рассказ, хронология, разбор, теория и практика'];
state.theoryProgress=state.theoryProgress||{};
state.theoryFontScale=Number(state.theoryFontScale||1);
let theorySaveTimer=null;

lessonMaxStage=function(id){return missionCompleted(id)?4:Number(state.lessonUnlockedStages[id]||0);};
setLessonStage=function(id,stage){
  const max=lessonMaxStage(id);if(stage<0||stage>max||stage>4)return;
  state.lessonStages[id]=stage;save();render();window.scrollTo({top:0,behavior:'smooth'});
};
advanceLesson=function(id){
  const next=Math.min(4,lessonStage(id)+1);
  state.lessonUnlockedStages[id]=Math.max(Number(state.lessonUnlockedStages[id]||0),next);
  state.lessonStages[id]=next;save();render();window.scrollTo({top:0,behavior:'smooth'});
};
lessonStageNav=function(m){
 const labels=[['▤','Рассказ'],['⌛','Хронология'],['◆','Разбор'],['▥','Теория'],['◎','Практика']];const cur=lessonStage(m.id),max=lessonMaxStage(m.id);
 return `<nav class="learning-stage-nav theory-five-stages">${labels.map(([icon,label],i)=>`<button class="${i===cur?'active':''} ${i<=max?'':'locked'}" ${i<=max?`onclick="setLessonStage('${m.id}',${i})"`:'disabled'}><i>${icon}</i><span>${label}</span><b>${i+1}</b></button>`).join('')}</nav>`;
};
lessonAnalysis=function(m,l){return `<section class="lesson-stage learning-analysis"><div class="lesson-stage-head"><div><small>ЭТАП 3</small><h2>Как это работает</h2></div><span class="lesson-stage-number">03</span></div><div class="concept-grid">${l.concepts.map(x=>`<article><h3>${esc(x.term)}</h3><p>${esc(x.definition)}</p></article>`).join('')}</div><div class="cause-effect-grid"><article><small>ПРИЧИНЫ</small>${l.causeEffect.causes.map(x=>`<p><span>→</span>${esc(x)}</p>`).join('')}</article><article><small>ПОСЛЕДСТВИЯ</small>${l.causeEffect.consequences.map(x=>`<p><span>→</span>${esc(x)}</p>`).join('')}</article></div><div class="learning-sources"><span>Опорные источники</span>${(l.sources||[]).map(x=>`<a href="${x.url}" target="_blank" rel="noopener">${esc(x.title)} ↗</a>`).join('')}</div><div class="learning-next split"><button class="btn ghost" onclick="setLessonStage('${m.id}',1)">← Хронология</button><button class="btn" onclick="advanceLesson('${m.id}')">К теории →</button></div></section>`;};

function theoryState(id){return state.theoryProgress[id]||{percent:0,read:false};}
function theoryWordCount(t){return (t?.paragraphs||[]).join(' ').trim().split(/\s+/).filter(Boolean).length;}
function updateTheoryUi(id,pct,read){
 const root=document.querySelector(`[data-theory-id="${id}"]`);if(!root)return;
 const label=root.querySelector('[data-theory-percent]');if(label)label.textContent=`${pct}%`;
 const bar=root.querySelector('[data-theory-bar]');if(bar)bar.style.width=`${pct}%`;
 const status=root.querySelector('[data-theory-status]');if(status){status.textContent=read?'Прочитано':'Чтение';status.classList.toggle('done',read);}
}
function trackTheoryReading(id,el){
 const max=Math.max(1,el.scrollHeight-el.clientHeight);const pct=Math.max(0,Math.min(100,Math.round(el.scrollTop/max*100)));
 const prev=theoryState(id);const read=prev.read||pct>=85;state.theoryProgress[id]={percent:Math.max(prev.percent||0,pct),read,at:read?(prev.at||new Date().toISOString()):null};
 updateTheoryUi(id,state.theoryProgress[id].percent,read);
 clearTimeout(theorySaveTimer);theorySaveTimer=setTimeout(()=>save(),250);
}
function restoreTheoryPosition(id){
 setTimeout(()=>{const el=document.querySelector(`[data-theory-scroll="${id}"]`);if(!el)return;const p=theoryState(id).percent||0;const max=Math.max(0,el.scrollHeight-el.clientHeight);if(p>0&&max>0)el.scrollTop=max*p/100;},30);
}
function adjustTheoryFont(delta){
 state.theoryFontScale=Math.max(.9,Math.min(1.3,Math.round((state.theoryFontScale+delta)*100)/100));save();
 document.documentElement?.style?.setProperty?.('--theory-scale',state.theoryFontScale);const el=document.querySelector('.theory-reader');if(el)el.style.setProperty('--reader-scale',state.theoryFontScale);
}
document.documentElement?.style?.setProperty?.('--theory-scale',state.theoryFontScale);

function lessonTheory(m,l){
 const t=l.theory||{};const progress=theoryState(m.id);const words=theoryWordCount(t);restoreTheoryPosition(m.id);
 return `<section class="lesson-stage learning-theory" data-theory-id="${m.id}"><div class="lesson-stage-head"><div><small>ЭТАП 4 · ПОЛНОЕ ЧТЕНИЕ</small><h2>Теория</h2></div><span class="lesson-stage-number">04</span></div><div class="theory-toolbar"><div><b>${esc(t.title||m.title)}</b><small>${words} слов · около ${t.readingMinutes||Math.max(3,Math.ceil(words/150))} мин</small></div><div class="theory-controls"><button onclick="adjustTheoryFont(-.05)" aria-label="Уменьшить текст">A−</button><button onclick="adjustTheoryFont(.05)" aria-label="Увеличить текст">A+</button><span data-theory-status class="${progress.read?'done':''}">${progress.read?'Прочитано':'Чтение'}</span></div></div><div class="theory-progress"><i data-theory-bar style="width:${progress.percent||0}%"></i><span data-theory-percent>${progress.percent||0}%</span></div><article class="theory-reader" style="--reader-scale:${state.theoryFontScale}" data-theory-scroll="${m.id}" onscroll="trackTheoryReading('${m.id}',this)"><header><h1>${esc(t.title||m.title)}</h1>${t.lead?`<p class="theory-lead">${esc(t.lead)}</p>`:''}</header>${(t.paragraphs||[]).map(p=>`<p>${esc(p)}</p>`).join('')}${(t.historicityNotes||[]).length?`<aside class="theory-historicity"><b>Исторические оговорки</b>${t.historicityNotes.map(x=>`<p>— ${esc(x)}</p>`).join('')}</aside>`:''}<footer><b>Материалы и дальнейшее чтение</b><div>${(t.sources||l.sources||[]).map(x=>`<a href="${x.url}" target="_blank" rel="noopener">${esc(x.title)} ↗</a>`).join('')}</div>${t.license?`<small>${esc(t.license)}</small>`:''}${t.checkedAt?`<small>Проверено: ${esc(t.checkedAt)}</small>`:''}</footer></article><div class="theory-read-note">Статус «прочитано» ставится после 85% текста. Он сохраняет прогресс, но не блокирует прохождение миссии.</div><div class="learning-next split"><button class="btn ghost" onclick="setLessonStage('${m.id}',2)">← Разбор</button><button class="btn" onclick="advanceLesson('${m.id}')">К практике →</button></div></section>`;
}
lessonActivity=function(m,l){const a=l.activity||{type:'continue'};let content='';if(a.type==='continue')content=`<div class="learning-check conclusion-check"><small>ГЛАВНЫЙ ВЫВОД</small><blockquote>${esc(a.summary||'Материал изучен.')}</blockquote><button class="btn" onclick="finishLearningMission('${m.id}')">${missionCompleted(m.id)?'Повторить вывод':'Закрепить и завершить'}</button></div>`;else if(a.type==='choice')content=renderChoiceActivity(m,a);else if(a.type==='match')content=renderMatchActivity(m,a);else if(a.type==='map')content=renderMapActivity(m);else if(a.type==='timeline')content=renderTimelineActivity(m);else if(a.type==='final_quiz')content=renderFinalActivity(m);return `<section class="lesson-stage learning-practice"><div class="lesson-stage-head"><div><small>ЭТАП 5</small><h2>Практика и закрепление</h2></div><span class="lesson-stage-number">05</span></div>${content}<div class="learning-next"><button class="btn ghost" onclick="setLessonStage('${m.id}',3)">← Вернуться к теории</button></div></section>`;};
lessonBody=function(m,l){const stage=lessonStage(m.id);return [lessonStory,lessonChronology,lessonAnalysis,lessonTheory,lessonActivity][stage](m,l);};

const V19_campaign=campaign;
campaign=function(){return V19_campaign().replace('рассказ → хронология → разбор → практика','рассказ → хронология → разбор → теория → практика');};
