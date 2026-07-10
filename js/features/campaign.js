/* Codex v1.5 — campaign engine */
function mission(id){ return CODEX_REGISTRY.missionsById.get(id); }
function missionIndex(id){ return CAMPAIGN.nodes.findIndex(n=>n.id===id); }
function missionCompleted(id){ return state.missionsCompleted.includes(id); }
function missionOpen(id){ const i=missionIndex(id); return i===0 || CAMPAIGN.nodes.slice(0,i).every(n=>missionCompleted(n.id)); }
function currentMission(){ return CAMPAIGN.nodes.find(n=>!missionCompleted(n.id)) || CAMPAIGN.nodes[CAMPAIGN.nodes.length-1]; }
function completedMissionCount(){ return CAMPAIGN.nodes.filter(n=>missionCompleted(n.id)).length; }
function completeMission(id){
  const m=mission(id); if(!m || missionCompleted(id)) return;
  state.missionsCompleted.push(id); unlock(m.unlockCards||[]); addXp(m.xp||80);
  const next=CAMPAIGN.nodes[missionIndex(id)+1]; if(next) state.currentMission=next.id;
  save(); confetti(); showToast('Миссия выполнена',`${m.title} · +${m.xp||80} XP`,'✓');
}
function openMission(id){ if(!missionOpen(id)) return; const target=mission(id); state.currentMission=id; if(target?.chapterId)state.mapChapter=target.chapterId; state.tab='mission'; state.selected=null; save(); render(); window.scrollTo({top:0,behavior:'smooth'}); }
function missionTypeLabel(t){ return ({READ:'Изучение',QUIZ:'Испытание',MAP:'Карта',TIMELINE:'Хронология',FINAL:'Финал'})[t]||t; }
function missionReady(m){
  if(m.type==='READ') return m.cards.every(id=>state.read.includes(id));
  if(m.type==='QUIZ'||m.type==='FINAL') return isQuizPassed(m.quiz);
  if(m.type==='MAP') return !!state.mapTasks[m.id]?.passed;
  if(m.type==='TIMELINE') return !!state.timelineTasks[m.id]?.passed;
  return false;
}
function finishReadMission(id){ const m=mission(id); if(m && missionReady(m)) completeMission(id); }
function missionMapTargets(id){return mission(id)?.mapTargets||[{key:'rome',label:'Рим',point:'ROME',zoom:7,radius:18000},{key:'palatine',label:'Палатин',point:'PALATINE',zoom:15,radius:190}];}
function answerMapTask(id,key){
  const targets=missionMapTargets(id);const cur=state.mapTasks[id]||{step:0,mistakes:0,passed:false};
  if(cur.passed)return;const expected=targets[cur.step]?.key;
  if(key===expected){cur.step++;state.mapTasks[id]=cur;save();const next=targets[cur.step];showToast('Верно',next?`Теперь найди: ${next.label}`:'География миссии пройдена.','⌖');if(cur.step>=targets.length){cur.passed=true;state.mapTasks[id]=cur;save();completeMission(id);render();}else render();}
  else{cur.mistakes++;state.mapTasks[id]=cur;save();updateMapMissionStatus?.(id);showToast('Не туда',`Нужная цель: ${targets[cur.step]?.label||'точка задания'}.`,'↻');}
}
function timelineConfig(id){const m=mission(id);return m?.timeline||{order:['foundation','numa','tarquin','superbus','expulsion'],labels:{foundation:'753 до н. э. · традиционное основание',numa:'Нума и священный порядок',tarquin:'Этрусские цари и городской рост',superbus:'Тарквиний Гордый',expulsion:'509 до н. э. · изгнание царей'},shuffle:['superbus','foundation','expulsion','numa','tarquin']};}
function chooseTimeline(id,key){
  const cfg=timelineConfig(id);const cur=state.timelineTasks[id]||{selected:[],attempts:0,passed:false};if(cur.passed||cur.selected.includes(key))return;
  cur.selected.push(key);state.timelineTasks[id]=cur;
  if(cur.selected.length===cfg.order.length){const ok=cur.selected.every((x,i)=>x===cfg.order[i]);cur.attempts++;if(ok){cur.passed=true;state.timelineTasks[id]=cur;completeMission(id);return;}showToast('Порядок неверный','Цепочка сброшена. Попробуй ещё раз.','↻');cur.selected=[];}
  state.timelineTasks[id]=cur;save();render();
}
function undoTimeline(id){const cur=state.timelineTasks[id]||{selected:[]};cur.selected.pop();state.timelineTasks[id]=cur;save();render();}
