/* Codex v8.7.2 — preserve progress after researched mission consolidation */
(()=>{
  const MAP={"MES_01_02":"MES_01_01","MES_01_04":"MES_01_03","MES_01_05":"MES_01_06","MES_02_02":"MES_02_01","MES_02_04":"MES_02_03","MES_02_05":"MES_02_06","MES_03_02":"MES_03_01","MES_03_04":"MES_03_03","MES_03_05":"MES_03_06","MES_04_02":"MES_04_01","MES_04_04":"MES_04_03","MES_04_05":"MES_04_06","MES_05_02":"MES_05_01","MES_05_04":"MES_05_03","MES_05_05":"MES_05_06","MES_06_02":"MES_06_01","MES_06_04":"MES_06_03","MES_06_05":"MES_06_06","MES_07_02":"MES_07_01","MES_07_04":"MES_07_03","MES_07_05":"MES_07_06","MES_08_02":"MES_08_01","MES_08_04":"MES_08_03","MES_08_05":"MES_08_06","MES_09_02":"MES_09_01","MES_09_04":"MES_09_03","MES_09_05":"MES_09_06","MES_10_02":"MES_10_01","MES_10_04":"MES_10_03","MES_10_05":"MES_10_06","EGY_01_02":"EGY_01_01","EGY_01_04":"EGY_01_03","EGY_01_05":"EGY_01_06","EGY_02_02":"EGY_02_01","EGY_02_04":"EGY_02_03","EGY_02_05":"EGY_02_06","EGY_03_02":"EGY_03_01","EGY_03_04":"EGY_03_03","EGY_03_05":"EGY_03_06","EGY_04_02":"EGY_04_01","EGY_04_04":"EGY_04_03","EGY_04_05":"EGY_04_06","EGY_05_02":"EGY_05_01","EGY_05_04":"EGY_05_03","EGY_05_05":"EGY_05_06","EGY_06_02":"EGY_06_01","EGY_06_04":"EGY_06_03","EGY_06_05":"EGY_06_06","EGY_07_02":"EGY_07_01","EGY_07_04":"EGY_07_03","EGY_07_05":"EGY_07_06","EGY_08_02":"EGY_08_01","EGY_08_04":"EGY_08_03","EGY_08_05":"EGY_08_06","EGY_09_02":"EGY_09_01","EGY_09_04":"EGY_09_03","EGY_09_05":"EGY_09_06","EGY_10_02":"EGY_10_01","EGY_10_04":"EGY_10_03","EGY_10_05":"EGY_10_06"};
  const remap=id=>MAP[id]||id;
  const uniq=list=>[...new Set((Array.isArray(list)?list:[]).map(remap).filter(Boolean))];
  state.missionsCompleted=uniq(state.missionsCompleted);
  state.currentMission=remap(state.currentMission||'');
  for(const key of ['lessonStages','lessonUnlockedStages','mapTasks','timelineTasks']){
    const source=state[key]&&typeof state[key]==='object'?state[key]:{};
    const next={};
    for(const [id,value] of Object.entries(source)){
      const target=remap(id);
      if(key==='lessonStages'||key==='lessonUnlockedStages')next[target]=Math.max(Number(next[target]||0),Number(value||0));
      else next[target]=next[target]||value;
    }
    state[key]=next;
  }
  state._missionConsolidation871=true;
  save();
})();
