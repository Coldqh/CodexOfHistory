/* Codex v1.6 — chapter-aware interactive map engine with focus controls */
const GEO=CODEX_CONFIG.maps.points;
const CARD_GEO=Object.fromEntries(Object.entries(CODEX_CONFIG.maps.cardPoints).map(([id,value])=>[id,typeof value==='string'?GEO[value]:value]));
const MAP_CHAPTERS=CODEX_CONFIG.maps.chapters||{ROME_CHAPTER_01:{title:'Рождение Рима',center:GEO.ROME,zoom:9}};
let activeMaps=[];
let atlasMarkers=new Map();
function destroyMaps(){activeMaps.forEach(m=>{try{m.remove();}catch(_){}});activeMaps=[];atlasMarkers=new Map();}
function geoForCard(c){return CARD_GEO[c.id]||GEO.ROME;}
function mapColors(){return state.theme==='parchment'?{line:'#68421f',fill:'#9b682f',wine:'#7f2f37',soft:'#f6ead2',text:'#2b1f15'}:{line:'#e5c78e',fill:'#a8793d',wine:'#b74d5a',soft:'#14110d',text:'#f6f1e8'};}
function markerIcon(c,target=false){return L.divIcon({className:'history-div-icon',html:`<div class="history-marker ${target?'mission-target':''}">${typeIcon(c.type)}</div>`,iconSize:[36,36],iconAnchor:[18,18],tooltipAnchor:[0,-21]});}
function createBaseMap(id,center,zoom){
  if(typeof L==='undefined'){const el=document.getElementById(id);if(el)el.innerHTML='<div class="map-load-error"><b>Карта не загрузилась</b><span>Проверь интернет и обнови страницу.</span></div>';return null;}
  const map=L.map(id,{zoomControl:false,attributionControl:false,minZoom:4,maxZoom:18,worldCopyJump:true,preferCanvas:true}).setView(center,zoom);
  L.control.zoom({position:'bottomright'}).addTo(map);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19}).addTo(map);
  L.control.attribution({position:'bottomleft',prefix:false}).addAttribution('&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noreferrer">OpenStreetMap</a>').addTo(map);
  activeMaps.push(map);return map;
}
function addCardMarkers(map,cards){
  cards.forEach(c=>{
    const point=geoForCard(c);
    const marker=L.marker(point,{icon:markerIcon(c)}).addTo(map);
    marker.bindTooltip(c.title,{direction:'top',className:'history-label',offset:[0,-2]});
    marker.bindPopup(`<div class="map-popup"><b>${esc(c.title)}</b><span>${esc(c.date)} · ${esc(c.loc?.label||c.region)}</span><small>Точка активной главы</small></div>`);
    marker.on('click',()=>map.flyTo(point,Math.max(map.getZoom(),14),{duration:.7}));
    atlasMarkers.set(c.id,{marker,map,point});
  });
}
function focusAtlasCard(id){
  const entry=atlasMarkers.get(id);if(!entry)return;
  const mapEl=document.getElementById('atlas-map');
  mapEl?.scrollIntoView({behavior:'smooth',block:'center'});
  entry.map.flyTo(entry.point,15,{duration:.8});
  setTimeout(()=>entry.marker.openPopup(),560);
}
function fitChapterMap(map,cards){
  const pts=cards.map(geoForCard);const cfg=MAP_CHAPTERS[state.mapChapter]||MAP_CHAPTERS.ROME_CHAPTER_01;
  if(!pts.length){map.setView(cfg.center||GEO.ROME,cfg.zoom||9);return;}
  if(pts.length===1)map.setView(pts[0],11);else map.fitBounds(L.latLngBounds(pts).pad(.28),{maxZoom:11});
}
function initAtlasMap(){
  const el=document.getElementById('atlas-map');if(!el)return;
  const cfg=MAP_CHAPTERS[state.mapChapter]||MAP_CHAPTERS.ROME_CHAPTER_01;
  const cards=typeof chapterMapCards==='function'?chapterMapCards():[...new Set(CAMPAIGN.nodes.flatMap(n=>n.cards))].map(card).filter(c=>c&&isUnlocked(c.id));
  const map=createBaseMap('atlas-map',cfg.center||GEO.ROME,cfg.zoom||9);if(!map)return;
  addCardMarkers(map,cards);fitChapterMap(map,cards);setTimeout(()=>map.invalidateSize(),120);
}
function resetAtlasView(){const m=activeMaps.find(x=>x.getContainer()?.id==='atlas-map');if(!m)return;const cfg=MAP_CHAPTERS[state.mapChapter]||MAP_CHAPTERS.ROME_CHAPTER_01;m.setView(cfg.center||GEO.ROME,cfg.zoom||9,{animate:true});}
function fitAtlasMarkers(){const m=activeMaps.find(x=>x.getContainer()?.id==='atlas-map');if(!m)return;const cards=typeof chapterMapCards==='function'?chapterMapCards():[];fitChapterMap(m,cards);}
function initMissionMap(){
  const el=document.getElementById('mission-map');if(!el)return;
  const id=el.dataset.mission;const task=state.mapTasks[id]||{step:0,mistakes:0,passed:false};const colors=mapColors();
  const map=createBaseMap('mission-map',task.step===0?[42.0,12.5]:GEO.PALATINE,task.step===0?6:15);if(!map)return;
  if(task.step===0){
    const rome=L.circle(GEO.ROME,{radius:18000,color:colors.wine,weight:3,fillColor:colors.wine,fillOpacity:.18}).addTo(map);
    rome.bindTooltip('Рим',{permanent:true,direction:'top',className:'history-label'});
    rome.on('click',e=>{if(e.originalEvent)L.DomEvent.stopPropagation(e.originalEvent);answerMapTask(id,'rome');});
  }else{
    const pal=L.circle(GEO.PALATINE,{radius:190,color:colors.line,weight:3,fillColor:colors.fill,fillOpacity:.34}).addTo(map);
    pal.bindTooltip('Палатин',{permanent:true,direction:'top',className:'history-label'});
    pal.on('click',e=>{if(e.originalEvent)L.DomEvent.stopPropagation(e.originalEvent);answerMapTask(id,'palatine');});
    L.marker(GEO.CAPITOL,{icon:L.divIcon({className:'history-div-icon',html:'<div class="history-marker">⌂</div>',iconSize:[36,36],iconAnchor:[18,18]})}).addTo(map).bindTooltip('Капитолий',{direction:'top',className:'history-label'});
  }
  map.on('click',()=>answerMapTask(id,'wrong'));setTimeout(()=>map.invalidateSize(),120);
}
function initMapsForView(){if(state.tab==='map')initAtlasMap();if(state.tab==='mission'&&mission(state.currentMission)?.type==='MAP')initMissionMap();}
