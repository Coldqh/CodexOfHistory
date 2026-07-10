/* Codex v1.1 — campaign engine */
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
function openMission(id){ if(!missionOpen(id)) return; state.currentMission=id; state.tab='mission'; state.selected=null; save(); render(); window.scrollTo({top:0,behavior:'smooth'}); }
function missionTypeLabel(t){ return ({READ:'Изучение',QUIZ:'Испытание',MAP:'Карта',TIMELINE:'Хронология',FINAL:'Финал'})[t]||t; }
function missionReady(m){
  if(m.type==='READ') return m.cards.every(id=>state.read.includes(id));
  if(m.type==='QUIZ'||m.type==='FINAL') return isQuizPassed(m.quiz);
  if(m.type==='MAP') return !!state.mapTasks[m.id]?.passed;
  if(m.type==='TIMELINE') return !!state.timelineTasks[m.id]?.passed;
  return false;
}
function finishReadMission(id){ const m=mission(id); if(m && missionReady(m)) completeMission(id); }
function answerMapTask(id,key){
  const expected=['latium','palatine']; const cur=state.mapTasks[id]||{step:0,mistakes:0,passed:false};
  if(cur.passed) return;
  if(key===expected[cur.step]){
    cur.step++;
    state.mapTasks[id]=cur; save();
    showToast('Верно',cur.step===1?'Лаций найден. Теперь приблизь карту и найди Палатин.':'Палатин найден — география миссии пройдена.','⌖');
    if(cur.step>=expected.length){ cur.passed=true; state.mapTasks[id]=cur; save(); completeMission(id); render(); }
    else render();
  } else {
    cur.mistakes++; state.mapTasks[id]=cur; save(); updateMapMissionStatus(id);
    showToast('Не туда','Перемещай карту, меняй масштаб и ориентируйся по подписям.','↻');
  }
}
const TIMELINE_ORDER=['foundation','numa','tarquin','superbus','expulsion'];
const TIMELINE_LABELS={foundation:'753 до н. э. · традиционное основание',numa:'Нума и священный порядок',tarquin:'Этрусские цари и городской рост',superbus:'Тарквиний Гордый',expulsion:'509 до н. э. · изгнание царей'};
function chooseTimeline(id,key){
  const cur=state.timelineTasks[id]||{selected:[],attempts:0,passed:false}; if(cur.passed||cur.selected.includes(key)) return;
  cur.selected.push(key); state.timelineTasks[id]=cur;
  if(cur.selected.length===TIMELINE_ORDER.length){
    const ok=cur.selected.every((x,i)=>x===TIMELINE_ORDER[i]); cur.attempts++;
    if(ok){cur.passed=true;state.timelineTasks[id]=cur;completeMission(id);return;}
    showToast('Порядок неверный','Цепочка сброшена. Начни от основания города.','↻'); cur.selected=[];
  }
  state.timelineTasks[id]=cur;save();render();
}
function undoTimeline(id){ const cur=state.timelineTasks[id]||{selected:[]};cur.selected.pop();state.timelineTasks[id]=cur;save();render(); }
