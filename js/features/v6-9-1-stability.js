/* Codex v8.0.0 — stable saves, pack fallback and update recovery */
(()=>{
  const V='8.0.0';
  const SAVE_BACKUP='codex_history_save_backup_v1';
  const SAVE_PREVIOUS='codex_history_save_previous_v1';
  window.CODEX_VERSION=V;

  const parseSave=value=>{try{const data=JSON.parse(value||'null');return data&&typeof data==='object'&&!Array.isArray(data)?data:null;}catch{return null;}};
  const progressLike=data=>!!data&&(Array.isArray(data.unlocked)||Array.isArray(data.missionsCompleted)||Number.isFinite(data.xp)||data.quizResults&&typeof data.quizResults==='object');
  const progressScore=data=>{
    if(!progressLike(data))return -1;
    return Number(data.xp||0)
      +(data.unlocked?.length||0)*40
      +(data.missionsCompleted?.length||0)*500
      +Object.keys(data.quizResults||{}).length*180
      +(data.packHistory?.length||0)*90
      +(data.read?.length||0)*15
      +Object.keys(data.personalStoryProgress||{}).length*220;
  };
  const saveTime=data=>Number(data?._saveMeta?.updatedAt||0);
  const candidateKeys=()=>{
    const keys=[STORE,SAVE_BACKUP,SAVE_PREVIOUS];
    try{
      for(let i=0;i<localStorage.length;i++){
        const key=localStorage.key(i)||'';
        if(/^codex_history_(?:v\d+.*|save_.*)$/i.test(key)&&!/(visual|preferences)/i.test(key))keys.push(key);
      }
    }catch{}
    return [...new Set(keys)];
  };
  const candidates=candidateKeys().map(key=>({key,data:parseSave(localStorage.getItem(key))})).filter(x=>progressLike(x.data));
  candidates.sort((a,b)=>saveTime(b.data)-saveTime(a.data)||progressScore(b.data)-progressScore(a.data)||(a.key===STORE?-1:1));
  const recovered=candidates[0]?.data;
  if(recovered&&progressScore(recovered)>progressScore(state))state={...state,...recovered};

  const arrays=['unlocked','discovered','read','quizDone','missionsCompleted','packHistory','learningDays'];
  arrays.forEach(key=>{state[key]=Array.isArray(state[key])?[...new Set(state[key].filter(Boolean))]:[];});
  const objects=['quizResults','mapTasks','timelineTasks','masteryChecks','reviewSchedule','packPity','personalStoryProgress','dailyHistory','dailyStats'];
  objects.forEach(key=>{state[key]=state[key]&&typeof state[key]==='object'&&!Array.isArray(state[key])?state[key]:{};});
  state.xp=Number.isFinite(Number(state.xp))?Number(state.xp):0;
  state.level=Math.max(1,Math.floor(state.xp/500)+1);
  state.theme=state.theme==='parchment'?'parchment':'night';

  function compactSnapshot(){
    const snapshot={...state,_saveMeta:{schema:1,appVersion:V,updatedAt:Date.now()}};
    delete snapshot.packModal;delete snapshot.masterySession;delete snapshot.poolUnlockModal;
    return snapshot;
  }
  function writeSave(){
    const payload=JSON.stringify(compactSnapshot());
    const write=()=>{
      const current=localStorage.getItem(STORE);
      if(current&&current!==payload)localStorage.setItem(SAVE_PREVIOUS,current);
      localStorage.setItem(STORE,payload);
      localStorage.setItem(SAVE_BACKUP,payload);
    };
    try{write();}
    catch(error){
      try{
        ['codex_history_visual_archive_v312','codex_history_visual_archive_v313'].forEach(key=>localStorage.removeItem(key));
        write();
      }catch(second){console.error('[Codex save]',second||error);}
    }
  }
  save=writeSave;
  window.addEventListener?.('pagehide',writeSave);
  document.addEventListener?.('visibilitychange',()=>{if(document.visibilityState==='hidden')writeSave();});
  document.addEventListener?.('error',event=>{
    const image=event.target;
    if(image?.tagName==='IMG'&&image.closest?.('.pack-page-card,.pack-option,.compact-pack')){
      image.onerror=null;image.src='assets/ui/pack-rome.svg';
    }
  },true);
  writeSave();
})();
