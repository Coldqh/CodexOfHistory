/* Codex v2.0 — Rome Chapter Three: struggle for Italy */
TYPE_META.WAR=['⚔','Война'];
TYPE_META.PEOPLE=['◈','Народ'];
TYPE_META.REGION=['⌖','Регион'];
TYPE_META.TERM=['§','Понятие'];
TYPE_META.SYSTEM=['⚖','Система'];
TYPE_META.ROAD=['↠','Дорога'];
TYPE_META.ORGANIZATION=['◆','Объединение'];
PAGE_META.campaign=['Кампания','Рим: три главы'];
if(missionCompleted('MIS_REPUBLIC_12')){['CITY_ITA_001','PER_ITA_001','EVT_ITA_001'].forEach(id=>{if(!state.unlocked.includes(id))state.unlocked.push(id);});save();}

const V20_home=home;
home=function(){
  let html=V20_home();
  const ch=activeChapter();
  if(ch?.id==='ROME_CHAPTER_03'){
    html=html
      .replace(/Глава (I|II|III) · [^<]+/g,'Глава III · Борьба за Италию')
      .replace(/От легенды о волчице<br><span>к падению царей\.<\/span>/g,'От Вейев и Аллии<br><span>к господству над Италией.</span>')
      .replace(/От изгнания царей<br><span>к публичному закону\.<\/span>/g,'От Вейев и Аллии<br><span>к господству над Италией.</span>');
  }
  return html;
};
