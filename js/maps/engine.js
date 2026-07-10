/* Codex v1.1 — interactive map engine */
const GEO=CODEX_CONFIG.maps.points;
const LATIUM_POLYGON=CODEX_CONFIG.maps.regions.latium.polygon;
const ETRURIA_POLYGON=CODEX_CONFIG.maps.regions.etruria.polygon;
const SABINE_POLYGON=CODEX_CONFIG.maps.regions.sabines.polygon;
const CARD_GEO=Object.fromEntries(Object.entries(CODEX_CONFIG.maps.cardPoints).map(([id,value])=>[id,typeof value==='string'?GEO[value]:value]));
let activeMaps=[];
function destroyMaps(){ activeMaps.forEach(m=>{try{m.remove();}catch(_){}}); activeMaps=[]; }
function geoForCard(c){ return CARD_GEO[c.id] || GEO.ROME; }
function mapColors(){ return state.theme==='parchment'
  ? {line:'#68421f',fill:'#9b682f',wine:'#7f2f37',soft:'#f6ead2',text:'#2b1f15'}
  : {line:'#f0d9aa',fill:'#c69b5c',wine:'#cf6471',soft:'#17120d',text:'#f6f1e8'};
}
function markerIcon(c,target=false){
  return L.divIcon({className:'history-div-icon',html:`<div class="history-marker ${target?'mission-target':''}">${typeIcon(c.type)}</div>`,iconSize:[42,42],iconAnchor:[21,21],tooltipAnchor:[0,-25]});
}
function createBaseMap(id,center,zoom){
  if(typeof L==='undefined'){ const el=document.getElementById(id); if(el) el.innerHTML='<div class="map-load-error"><b>Карта не загрузилась</b><span>Проверь подключение к интернету и обнови страницу.</span></div>'; return null; }
  const map=L.map(id,{zoomControl:false,minZoom:5,maxZoom:18,worldCopyJump:true,preferCanvas:true}).setView(center,zoom);
  L.control.zoom({position:'bottomright'}).addTo(map);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}).addTo(map);
  activeMaps.push(map); return map;
}
function addRegionLayers(map,interactive=false,missionId=null){
  const c=mapColors();
  const regions=[
    {key:'latium',name:'Лаций',poly:LATIUM_POLYGON,color:c.wine,fill:.12},
    {key:'etruria',name:'Этрурия',poly:ETRURIA_POLYGON,color:c.fill,fill:.07},
    {key:'sabines',name:'Сабинская область',poly:SABINE_POLYGON,color:c.line,fill:.06}
  ];
  regions.forEach(r=>{
    const layer=L.polygon(r.poly,{color:r.color,weight:r.key==='latium'?2.2:1.3,fillColor:r.color,fillOpacity:r.fill,dashArray:r.key==='latium'?null:'7 7'}).addTo(map);
    layer.bindTooltip(r.name,{sticky:true,className:'history-label'});
    if(interactive && r.key==='latium') layer.on('click',e=>{if(e.originalEvent)L.DomEvent.stopPropagation(e.originalEvent);answerMapTask(missionId,'latium');});
  });
  L.polyline([[42.15,12.31],[41.97,12.38],[41.90,12.47],[41.72,12.31],[41.35,12.07]],{color:c.line,weight:3,opacity:.55}).addTo(map).bindTooltip('Тибр',{sticky:true,className:'history-label'});
}
function addCardMarkers(map,cards){
  cards.forEach(c=>{
    const marker=L.marker(geoForCard(c),{icon:markerIcon(c)}).addTo(map);
    marker.bindTooltip(c.loc?.label||c.title,{direction:'top',className:'history-label',offset:[0,-3]});
    marker.bindPopup(`<div class="map-popup"><b>${esc(c.title)}</b><span>${esc(c.date)} · ${esc(c.region)}</span><button onclick="openCard('${c.id}')">Открыть карточку</button></div>`);
  });
}
function fitChapterMap(map,cards){
  const pts=cards.map(geoForCard); if(!pts.length) return;
  if(pts.length===1) map.setView(pts[0],11); else map.fitBounds(L.latLngBounds(pts).pad(.35),{maxZoom:11});
}
function initAtlasMap(){
  const el=document.getElementById('atlas-map'); if(!el) return;
  const chapterIds=[...new Set(CAMPAIGN.nodes.flatMap(n=>n.cards))];
  const cards=chapterIds.map(card).filter(c=>c&&isUnlocked(c.id));
  const map=createBaseMap('atlas-map',GEO.ROME,8); if(!map) return;
  addRegionLayers(map); addCardMarkers(map,cards); fitChapterMap(map,cards);
  setTimeout(()=>map.invalidateSize(),120);
}
function resetAtlasView(){ const m=activeMaps.find(x=>x.getContainer()?.id==='atlas-map'); if(m)m.setView(GEO.ROME,8,{animate:true}); }
function fitAtlasMarkers(){
  const m=activeMaps.find(x=>x.getContainer()?.id==='atlas-map'); if(!m)return;
  const ids=[...new Set(CAMPAIGN.nodes.flatMap(n=>n.cards))]; const cards=ids.map(card).filter(c=>c&&isUnlocked(c.id)); fitChapterMap(m,cards);
}
function initMissionMap(){
  const el=document.getElementById('mission-map'); if(!el) return;
  const id=el.dataset.mission; const task=state.mapTasks[id]||{step:0,mistakes:0,passed:false};
  const map=createBaseMap('mission-map',task.step===0?GEO.LATIUM:GEO.PALATINE,task.step===0?7:15); if(!map) return;
  addRegionLayers(map,true,id);
  const c=mapColors();
  const pal=L.circle(GEO.PALATINE,{radius:170,color:c.line,weight:3,fillColor:c.fill,fillOpacity:task.step===0?.08:.30,dashArray:task.step===0?'6 7':null}).addTo(map);
  pal.bindTooltip('Палатин',{permanent:task.step>0,direction:'top',className:'history-label'});
  pal.on('click',e=>{if(e.originalEvent)L.DomEvent.stopPropagation(e.originalEvent);answerMapTask(id,'palatine');});
  L.marker(GEO.CAPITOL,{icon:L.divIcon({className:'history-div-icon',html:'<div class="history-marker">⌂</div>',iconSize:[42,42],iconAnchor:[21,21]})}).addTo(map).bindTooltip('Капитолий',{direction:'top',className:'history-label'});
  map.on('click',()=>answerMapTask(id,'wrong'));
  setTimeout(()=>map.invalidateSize(),120);
}
function initMapsForView(){ if(state.tab==='map') initAtlasMap(); if(state.tab==='mission'&&mission(state.currentMission)?.type==='MAP') initMissionMap(); }
