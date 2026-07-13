/* Codex v3.0 — campaign-aware Leaflet map engine */
let activeMaps=[];
let atlasMarkers=new Map();
function mapConfig(){return CODEX_CONFIG.maps||{};}
function geoPoints(){return mapConfig().points||{};}
function mapChapters(){return mapConfig().chapters||{};}
function fallbackPoint(){const g=geoPoints();return g.DAWN_CENTER||g.CHINA_CENTER||g.INDUS_CENTER||g.COMPARISON_CENTER||g.MESOPOTAMIA_CENTER||g.EGYPT_CENTER||g.ROME||[31,35];}
function cardGeo(){
  const g=geoPoints(),raw=mapConfig().cardPoints||{};
  return Object.fromEntries(Object.entries(raw).map(([id,value])=>[id,typeof value==='string'?(g[value]||fallbackPoint()):value]));
}
function destroyMaps(){activeMaps.forEach(m=>{try{m.remove();}catch(_){}});activeMaps=[];atlasMarkers=new Map();}
function geoForCard(c){return cardGeo()[c.id]||c.loc&&[c.loc.lat,c.loc.lng]||fallbackPoint();}
function mapColors(){return state.theme==='parchment'?{line:'#68421f',fill:'#9b682f',wine:'#7f2f37',soft:'#f6ead2',text:'#2b1f15'}:{line:'#e5c78e',fill:'#a8793d',wine:'#b74d5a',soft:'#14110d',text:'#f6f1e8'};}
function markerIcon(c,target=false){return L.divIcon({className:'history-div-icon',html:`<div class="history-marker ${target?'mission-target':''}">${typeIcon(c.type)}</div>`,iconSize:[36,36],iconAnchor:[18,18],tooltipAnchor:[0,-21]});}
function createBaseMap(id,center,zoom){
  if(typeof L==='undefined'){const el=document.getElementById(id);if(el)el.innerHTML='<div class="map-load-error"><b>Карта не загрузилась</b><span>Проверь подключение и обнови страницу из настроек.</span></div>';return null;}
  const map=L.map(id,{zoomControl:false,attributionControl:false,minZoom:2,maxZoom:18,worldCopyJump:true,preferCanvas:true}).setView(center||fallbackPoint(),zoom||5);
  L.control.zoom({position:'bottomright'}).addTo(map);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,crossOrigin:true}).addTo(map);
  L.control.attribution({position:'bottomleft',prefix:false}).addAttribution('&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noreferrer">OpenStreetMap</a>').addTo(map);
  activeMaps.push(map);return map;
}
function atlasMap(){return activeMaps.find(x=>x.getContainer()?.id==='atlas-map')||null;}
function addCardMarkers(map,cards){
  cards.forEach(c=>{
    const point=geoForCard(c);if(!point)return;
    const marker=L.marker(point,{icon:markerIcon(c)}).addTo(map);
    marker.bindTooltip(c.title,{direction:'top',className:'history-label',offset:[0,-2]});
    marker.bindPopup(`<div class="map-popup"><b>${esc(c.title)}</b><span>${esc(c.date)} · ${esc(c.loc?.label||c.region)}</span><small>Точка активной кампании</small></div>`);
    marker.on('click',()=>map.flyTo(point,Math.max(map.getZoom(),8),{duration:.7}));
    atlasMarkers.set(c.id,{marker,map,point});
  });
}
function focusAtlasCard(id){const entry=atlasMarkers.get(id);if(!entry)return;document.getElementById('atlas-map')?.scrollIntoView({behavior:'smooth',block:'center'});entry.map.flyTo(entry.point,Math.max(8,entry.map.getZoom()),{duration:.8});setTimeout(()=>entry.marker.openPopup(),560);}
function activeChapterMapConfig(){const chapters=mapChapters();return chapters[state.mapChapter]||Object.values(chapters)[0]||{title:activeCampaignLabel?.()||'Карта',center:fallbackPoint(),zoom:5};}
function fitChapterMap(map,cards){const pts=cards.map(geoForCard).filter(Boolean),cfg=activeChapterMapConfig();if(!pts.length){map.setView(cfg.center||fallbackPoint(),cfg.zoom||5);return;}if(pts.length===1)map.setView(pts[0],Math.max(cfg.zoom||5,8));else map.fitBounds(L.latLngBounds(pts).pad(.28),{maxZoom:9});}
function initAtlasMap(){
  const el=document.getElementById('atlas-map');if(!el)return;
  const cfg=activeChapterMapConfig();
  const cards=typeof chapterMapCards==='function'?chapterMapCards():[...new Set(CAMPAIGN.nodes.flatMap(n=>n.cards||[]))].map(card).filter(c=>c&&isUnlocked(c.id));
  const map=createBaseMap('atlas-map',cfg.center||fallbackPoint(),cfg.zoom||5);if(!map)return;
  addCardMarkers(map,cards);fitChapterMap(map,cards);setTimeout(()=>map.invalidateSize(),120);
}
function resetAtlasView(){const m=atlasMap();if(!m)return;const cfg=activeChapterMapConfig();m.setView(cfg.center||fallbackPoint(),cfg.zoom||5,{animate:true});}
function fitAtlasMarkers(){const m=atlasMap();if(!m)return;const cards=typeof chapterMapCards==='function'?chapterMapCards():[];fitChapterMap(m,cards);}
function focusMapPoint(point,zoom=6,popupHtml=''){
  const map=atlasMap(),g=geoPoints();if(!map)return;const p=typeof point==='string'?g[point]:point;if(!p)return;
  document.getElementById('atlas-map')?.scrollIntoView({behavior:'smooth',block:'center'});map.flyTo(p,zoom,{duration:.8});
  if(popupHtml){const popup=L.popup().setLatLng(p).setContent(popupHtml);setTimeout(()=>popup.openOn(map),560);}
}
function initMissionMap(){
  const el=document.getElementById('mission-map');if(!el)return;
  const id=el.dataset.mission,targets=typeof missionMapTargets==='function'?missionMapTargets(id):[],task=state.mapTasks[id]||{step:0,mistakes:0,passed:false},colors=mapColors(),g=geoPoints();
  const target=targets[Math.min(task.step,Math.max(0,targets.length-1))],point=target?(typeof target.point==='string'?(g[target.point]||fallbackPoint()):target.point):fallbackPoint();
  const map=createBaseMap('mission-map',task.step===0?(mapConfig().missionCenter||fallbackPoint()):point,task.step===0?(mapConfig().missionZoom||3):(target?.zoom||7));if(!map)return;
  if(target){const circle=L.circle(point,{radius:target.radius||350,color:colors.wine,weight:3,fillColor:colors.fill,fillOpacity:.28}).addTo(map);circle.bindTooltip(target.label,{permanent:true,direction:'top',className:'history-label'});circle.on('click',e=>{if(e.originalEvent)L.DomEvent.stopPropagation(e.originalEvent);answerMapTask(id,target.key);});}
  targets.forEach((t,i)=>{if(i===task.step)return;const p=typeof t.point==='string'?(g[t.point]||fallbackPoint()):t.point;L.marker(p,{icon:L.divIcon({className:'history-div-icon',html:`<div class="history-marker muted">${i<task.step?'✓':'·'}</div>`,iconSize:[30,30],iconAnchor:[15,15]})}).addTo(map).bindTooltip(t.label,{direction:'top',className:'history-label'});});
  map.on('click',()=>answerMapTask(id,'wrong'));setTimeout(()=>map.invalidateSize(),120);
}
function initMapsForView(){if(state.tab==='map')initAtlasMap();if(state.tab==='mission'&&mission(state.currentMission)?.type==='MAP')initMissionMap();}
