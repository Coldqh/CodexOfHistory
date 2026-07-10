/* Codex v1.4 — navigation, quizzes, basic rewards and feedback */
function go(tab){
  state.tab=tab; state.selected=null; state.quizFinished=false; state.quizLastResult=null;
  save(); render(); window.scrollTo({top:0,behavior:'smooth'});
}
function openCard(id){
  if(!isUnlocked(id)) return;
  state.currentCard=id; state.tab='detail';
  if(!state.read.includes(id)){ state.read.push(id); addXp(10); showToast('Новое знание','Карточка изучена · +10 XP','✦'); }
  const cm=mission(state.currentMission); if(cm?.type==='READ' && cm.cards.every(x=>state.read.includes(x))) completeMission(cm.id);
  save(); render(); window.scrollTo({top:0,behavior:'smooth'});
}
function openQuiz(id,missionId=null){
  state.currentQuiz=id; state.quizMissionId=missionId; state.quizIndex=0; state.quizScore=0; state.selected=null;
  state.quizFinished=false; state.quizLastResult=null; state.tab='quiz'; save(); render();
  window.scrollTo({top:0,behavior:'smooth'});
}
function answer(i){
  if(state.selected!==null) return;
  state.selected=i;
  if(i===currentQuestion().correct) state.quizScore++;
  save(); render();
}
function currentQuiz(){ return QUIZZES[state.currentQuiz] || QUIZZES[currentNode().quiz]; }
function currentQuestion(){ return currentQuiz().questions[state.quizIndex]; }
function nextQuestion(){
  const qz=currentQuiz();
  if(state.quizIndex < qz.questions.length-1){ state.quizIndex++; state.selected=null; save(); render(); return; }
  finishQuiz();
}
function finishQuiz(){
  const qz=currentQuiz();
  const quizId=state.currentQuiz || currentNode().quiz;
  const total=qz.questions.length;
  const score=state.quizScore;
  const percent=Math.round(score/total*100);
  const previous=quizResult(quizId);
  const best=Math.max(previous?.bestPercent || 0, percent);
  const passed=percent>=PASS_PERCENT;
  const wasPassed=!!previous?.passed;
  const result={score,total,percent,bestPercent:best,passed:wasPassed || passed,lastPassed:passed,attempts:(previous?.attempts||0)+1,completedAt:new Date().toISOString()};
  state.quizResults={...(state.quizResults||{}), [quizId]:result};
  state.quizLastResult={quizId,...result,title:qz.title};
  if(passed && !wasPassed){
    if(!state.quizDone.includes(quizId)) state.quizDone.push(quizId);
    const node=CAMPAIGN.nodes.find(n=>n.quiz===quizId);
    if(node) completeMission(node.id); else addXp(100);
  }
  state.quizFinished=true; state.selected=null; save(); render();
  if(passed && (wasPassed || !CAMPAIGN.nodes.find(n=>n.quiz===quizId))){ confetti(); showToast('Испытание пройдено',`${percent}% правильных · глава зачтена`,'✓'); }
  else showToast('Попытка завершена',`${percent}% · нужно минимум ${PASS_PERCENT}%`,'↻');
}
function openPack(){
  const locked=CARDS.filter(c=>!isUnlocked(c.id));
  if(!locked.length){ showToast('Коллекция собрана','Все карточки текущего модуля уже открыты','♛'); return; }
  const coreIds=new Set(CAMPAIGN.nodes.flatMap(n=>[...n.cards,...(n.unlockCards||[])]));
  const bonus=locked.filter(c=>!coreIds.has(c.id));
  if(!bonus.length){showToast('Сюжетные карточки','Продолжай кампанию — ключевые знания не выпадают случайно','♜');return;}
  const picks=[...bonus].sort(()=>Math.random()-.5).slice(0,2);
  unlock(picks.map(c=>c.id)); addXp(35);
  showToast('Пак открыт',picks.map(c=>c.title).join(' · ') + ' · +35 XP','✦');
  state.currentCard=picks[0].id; state.tab='detail'; save(); render();
}
function resetProgress(){
  if(!confirm('Сбросить весь локальный прогресс?')) return;
  localStorage.removeItem(STORE); state={...initial,quizResults:{},quizDone:[],missionsCompleted:[],mapTasks:{},timelineTasks:{}}; applyTheme(); render();
  showToast('Прогресс сброшен','Можно начать кампанию заново','↺');
}
function updateSearch(el){
  state.search=el.value; save(); const pos=el.selectionStart; render();
  requestAnimationFrame(()=>{const n=document.getElementById('collection-search');if(n){n.focus();n.setSelectionRange(pos,pos);}});
}
function setFilter(key,value){ state[key]=value; save(); render(); }

function showToast(title,text,icon='✦'){
  const root=document.getElementById('toast-root'); if(!root) return;
  const el=document.createElement('div'); el.className='toast';
  el.innerHTML=`<div class="toast-icon">${icon}</div><div><b>${esc(title)}</b><span>${esc(text)}</span></div>`;
  root.appendChild(el);
  setTimeout(()=>{el.classList.add('out');setTimeout(()=>el.remove(),420);},3300);
}
function confetti(){
  const colors=['#a8f0e5','#ef7c86','#6388d8','#eaf2ef','#76bc91'];
  for(let i=0;i<34;i++){
    const p=document.createElement('i'); p.className='confetti';
    p.style.background=colors[i%colors.length];
    p.style.setProperty('--x',`${(Math.random()-.5)*680}px`);
    p.style.setProperty('--y',`${120+Math.random()*430}px`);
    p.style.setProperty('--r',`${(Math.random()-.5)*900}deg`);
    p.style.left=`${46+Math.random()*8}%`; p.style.animationDelay=`${Math.random()*.18}s`;
    document.body.appendChild(p); setTimeout(()=>p.remove(),2100);
  }
}

