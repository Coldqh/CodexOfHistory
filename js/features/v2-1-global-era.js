/* Codex v2.1 — global era and campaign system */
PAGE_META.world=['Мир','Эпохи и кампании'];
if(!NAV.some(item=>item[0]==='world')){
  const dailyIndex=NAV.findIndex(item=>item[0]==='daily');
  NAV.splice(dailyIndex>=0?dailyIndex+1:1,0,['world','◎','Мир']);
}
const WORLD_DATA=typeof CODEX_WORLD!=='undefined'?CODEX_WORLD:{
  eras:[
    {id:'ERA_DAWN',order:1,title:'Рождение цивилизаций',subtitle:'Первые города',dateLabel:'ок. 4500–2000 до н. э.',accent:'#c48b52',cover:'assets/eras/dawn.svg',description:'Первые города и государства.',campaignIds:['MESOPOTAMIA_DAWN']},
    {id:'ERA_HELLENISTIC_ROMAN',order:5,title:'Эллинистический и римский мир',subtitle:'Рим',dateLabel:'323 до н. э. – III век н. э.',accent:'#a26755',cover:'assets/eras/hellenistic.svg',description:'Римская ветка.',campaignIds:['ROME_CAMPAIGN']}
  ],
  campaigns:[
    {id:'MESOPOTAMIA_DAWN',eraId:'ERA_DAWN',order:1,title:'Месопотамия: первые города',subtitle:'Запланировано',period:'ок. 4500–2000 до н. э.',chapterCount:10,releasedChapters:0,status:'NEXT',region:'Месопотамия',description:'Кампания запланирована.',chapters:Array.from({length:10},(_,i)=>({number:i+1,title:`Глава ${i+1}`}))},
    {id:'ROME_CAMPAIGN',eraId:'ERA_HELLENISTIC_ROMAN',order:21,title:'Рим',subtitle:'Текущая кампания',period:'VIII век до н. э. – V век н. э.',chapterCount:12,releasedChapters:3,status:'PLAYABLE',region:'Италия',description:'Римская кампания.',chapters:Array.from({length:12},(_,i)=>({number:i+1,title:`Глава ${i+1}`}))}
  ],timeline:[]
};
const ERAS=WORLD_DATA.eras;
const WORLD_CAMPAIGNS=WORLD_DATA.campaigns;
const WORLD_TIMELINE=WORLD_DATA.timeline;
const ERA_BY_ID=new Map(ERAS.map(x=>[x.id,x]));
const WORLD_CAMPAIGN_BY_ID=new Map(WORLD_CAMPAIGNS.map(x=>[x.id,x]));
state.worldView=['ERAS','CAMPAIGNS','TIMELINE'].includes(state.worldView)?state.worldView:'ERAS';
state.worldEra=ERA_BY_ID.has(state.worldEra)?state.worldEra:'ERA_DAWN';
state.activeCampaign=WORLD_CAMPAIGN_BY_ID.has(state.activeCampaign)?state.activeCampaign:'ROME_CAMPAIGN';
state.worldCampaignPreview=WORLD_CAMPAIGN_BY_ID.has(state.worldCampaignPreview)?state.worldCampaignPreview:null;
save();

function worldCampaign(id){return WORLD_CAMPAIGN_BY_ID.get(id);}
function worldEra(id){return ERA_BY_ID.get(id);}
function worldYearLabel(year){return year<0?`${Math.abs(year)} до н. э.`:`${year} н. э.`;}
function worldStatusLabel(status){return ({PLAYABLE:'Доступна',NEXT:'Следующая',PLANNED:'Запланирована'})[status]||status;}
function worldStatusIcon(status){return ({PLAYABLE:'▶',NEXT:'◆',PLANNED:'○'})[status]||'○';}
function worldEraCampaigns(id){return WORLD_CAMPAIGNS.filter(c=>c.eraId===id).sort((a,b)=>a.order-b.order);}
function setWorldView(view){state.worldView=view;save();render();}
function selectWorldEra(id){state.worldEra=id;state.worldView='CAMPAIGNS';state.worldCampaignPreview=null;save();render();}
function previewWorldCampaign(id){state.worldCampaignPreview=id;save();render();requestAnimationFrame(()=>document.getElementById('world-campaign-preview')?.scrollIntoView({behavior:'smooth',block:'center'}));}
function closeWorldCampaignPreview(){state.worldCampaignPreview=null;save();render();}
function startWorldCampaign(id){
  const c=worldCampaign(id);if(!c)return;
  if(c.status!=='PLAYABLE'){showToast('Кампания недоступна',`План: ${c.chapterCount} глав.`,'◎');return;}
  state.activeCampaign=id;state.tab='campaign';save();render();window.scrollTo({top:0,behavior:'smooth'});
}
function eraPublishedChapters(era){return worldEraCampaigns(era.id).reduce((n,c)=>n+(c.releasedChapters||0),0);}
function eraTotalChapters(era){return worldEraCampaigns(era.id).reduce((n,c)=>n+c.chapterCount,0);}
function eraProgress(era){const total=eraTotalChapters(era);return total?Math.round(eraPublishedChapters(era)/total*100):0;}
function globalPublishedChapters(){return WORLD_CAMPAIGNS.reduce((n,c)=>n+(c.releasedChapters||0),0);}
function globalTotalChapters(){return WORLD_CAMPAIGNS.reduce((n,c)=>n+c.chapterCount,0);}
function campaignCover(c){return worldEra(c.eraId)?.cover||'assets/ui/fallback-card.svg';}

function eraCard(era){
 const camps=worldEraCampaigns(era.id),published=eraPublishedChapters(era),total=eraTotalChapters(era),progress=eraProgress(era);
 return `<article class="era-card ${state.worldEra===era.id?'active':''}" style="--era-accent:${era.accent}" onclick="selectWorldEra('${era.id}')"><img src="${era.cover}" alt="${esc(era.title)}"><div class="era-card-overlay"><div class="era-number">ЭПОХА ${String(era.order).padStart(2,'0')}</div><h3>${era.title}</h3><p>${era.subtitle}</p><div class="era-meta"><span>${era.dateLabel}</span><span>${camps.length} кампаний</span></div><div class="era-progress"><i style="width:${progress}%"></i></div><small>${published}/${total} глав опубликовано</small></div></article>`;
}
function worldCampaignCard(c){
 const progress=c.id==='ROME_CAMPAIGN'?campaignProgress():0;
 return `<article class="world-campaign-card ${c.status.toLowerCase()}" onclick="previewWorldCampaign('${c.id}')"><div class="world-campaign-cover"><img src="${campaignCover(c)}" alt=""><span>${worldStatusIcon(c.status)} ${worldStatusLabel(c.status)}</span></div><div class="world-campaign-copy"><small>${c.period} · ${c.region}</small><h3>${c.title}</h3><p>${c.subtitle}</p><div class="campaign-publication"><b>${c.releasedChapters}/${c.chapterCount}</b><span>глав опубликовано</span></div>${c.status==='PLAYABLE'?`<div class="progress"><span style="width:${progress}%"></span></div>`:''}</div></article>`;
}
function campaignPreviewPanel(c){
 if(!c)return'';
 return `<section id="world-campaign-preview" class="world-campaign-preview reveal"><button class="world-preview-close" onclick="closeWorldCampaignPreview()">×</button><div class="world-preview-head"><img src="${campaignCover(c)}" alt=""><div><div class="eyebrow">${worldEra(c.eraId).title}</div><h2>${c.title}</h2><p>${c.description||c.subtitle}</p><div class="world-preview-meta"><span>${c.period}</span><span>${c.region}</span><span>${c.chapterCount} глав</span><span>${worldStatusLabel(c.status)}</span></div></div></div><div class="world-chapter-plan">${c.chapters.map(ch=>`<article class="${ch.number<=c.releasedChapters?'released':''}"><b>${String(ch.number).padStart(2,'0')}</b><span>${ch.title}</span><i>${ch.number<=c.releasedChapters?'Доступно':'План'}</i></article>`).join('')}</div><div class="hero-actions">${c.status==='PLAYABLE'?`<button class="btn" onclick="startWorldCampaign('${c.id}')">▶ Продолжить кампанию</button>`:`<button class="btn secondary" onclick="startWorldCampaign('${c.id}')">○ В плане</button>`}<button class="btn ghost" onclick="closeWorldCampaignPreview()">Закрыть</button></div></section>`;
}
function timelineView(){
 const min=-4500,max=750,span=max-min;
 return `<section class="global-timeline reveal"><div class="global-timeline-axis"><span>4500 до н. э.</span><span>2000 до н. э.</span><span>500 до н. э.</span><span>1 н. э.</span><span>750 н. э.</span></div><div class="global-timeline-track">${ERAS.map(e=>{const left=(e.startYear-min)/span*100,width=(e.endYear-e.startYear)/span*100;return `<button class="timeline-era-band" style="left:${left}%;width:${Math.max(width,3)}%;--era-accent:${e.accent}" onclick="selectWorldEra('${e.id}')" title="${esc(e.title)}"><span>${e.order}</span></button>`;}).join('')}${WORLD_TIMELINE.map((m,i)=>{const left=(m.year-min)/span*100;return `<button class="timeline-event-dot" style="left:${left}%;--row:${i%4}" onclick="previewWorldCampaign('${m.campaignId}')"><i></i><b>${worldYearLabel(m.year)}</b><span>${m.label}</span></button>`;}).join('')}</div></section><div class="timeline-list reveal">${WORLD_TIMELINE.map(m=>{const c=worldCampaign(m.campaignId);return `<article onclick="previewWorldCampaign('${m.campaignId}')"><time>${worldYearLabel(m.year)}</time><div><b>${m.label}</b><p>${m.detail}</p></div><span>${c?.title||''}</span></article>`;}).join('')}</div>`;
}
function worldScreen(){
 const era=worldEra(state.worldEra),campaigns=worldEraCampaigns(era.id),preview=worldCampaign(state.worldCampaignPreview);
 const tabs=`<div class="world-view-tabs"><button class="${state.worldView==='ERAS'?'active':''}" onclick="setWorldView('ERAS')">Эпохи</button><button class="${state.worldView==='CAMPAIGNS'?'active':''}" onclick="setWorldView('CAMPAIGNS')">Кампании</button><button class="${state.worldView==='TIMELINE'?'active':''}" onclick="setWorldView('TIMELINE')">Хронология</button></div>`;
 let content='';
 if(state.worldView==='ERAS') content=`<div class="era-grid reveal">${ERAS.map(eraCard).join('')}</div>`;
 if(state.worldView==='CAMPAIGNS') content=`<section class="selected-era-head reveal" style="--era-accent:${era.accent}"><img src="${era.cover}" alt=""><div><div class="eyebrow">Эпоха ${era.order}</div><h2>${era.title}</h2><p>${era.description}</p><div class="world-preview-meta"><span>${era.dateLabel}</span><span>${campaigns.length} кампаний</span><span>${eraTotalChapters(era)} глав в плане</span></div></div></section><div class="world-campaign-grid reveal">${campaigns.map(worldCampaignCard).join('')}</div>`;
 if(state.worldView==='TIMELINE') content=timelineView();
 return shell(`<section class="world-hero reveal"><div><div class="eyebrow">Глобальная история</div><h2>Мир развивается<br><span>параллельными путями.</span></h2><p>Сначала выбери эпоху, затем доступную кампанию.</p><div class="hero-actions"><button class="btn" onclick="selectWorldEra('ERA_DAWN')">𒀭 Начать с истоков</button><button class="btn secondary" onclick="startWorldCampaign('ROME_CAMPAIGN')">Открыть кампанию</button></div></div><div class="world-globe"><div class="world-globe-core"><strong>${ERAS.length}</strong><span>эпох</span></div><i></i><i></i><i></i></div></section><section class="world-stats reveal"><article><b>${WORLD_CAMPAIGNS.length}</b><span>кампаний в плане</span></article><article><b>${globalPublishedChapters()}/${globalTotalChapters()}</b><span>глав опубликовано</span></article><article><b>${CARDS.length}</b><span>карточек сейчас</span></article><article><b>v${appVersion()}</b><span>глобальная система</span></article></section>${tabs}${content}${campaignPreviewPanel(preview)}`);
}

const V21_home=home;
home=function(){
 const m=currentMission();const active=worldCampaign(state.activeCampaign)||worldCampaign('ROME_CAMPAIGN');const dawn=worldCampaign('MESOPOTAMIA_DAWN');
 return shell(`<section class="global-home-hero reveal"><div class="global-home-copy"><div class="eyebrow">Codex World · v${appVersion()}</div><h2>Текущая кампания</h2><p>Продолжи текущую миссию или перейди к выбору эпохи.</p><div class="hero-actions"><button class="btn" onclick="go('world')">Перейти к эпохам</button><button class="btn secondary" onclick="openMission('${m.id}')">Открыть кампанию</button></div></div><div class="global-home-era"><img src="assets/eras/dawn.svg" alt=""><div><small>КАМПАНИЯ</small><h3>${dawn.title}</h3><p>${dawn.chapterCount} глав · ${dawn.period}</p><button onclick="previewWorldCampaign('${dawn.id}');go('world')">Открыть кампанию →</button></div></div></section><section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">◎</div><b>${ERAS.length}</b><span>эпох мира</span></div><div class="stat-box"><div class="stat-icon">▤</div><b>${WORLD_CAMPAIGNS.length}</b><span>кампаний в плане</span></div><div class="stat-box"><div class="stat-icon">SPQR</div><b>${campaignProgress()}%</b><span>текущая кампания</span></div><div class="stat-box"><div class="stat-icon">▦</div><b>${state.unlocked.length}</b><span>карточек открыто</span></div></section><section class="section reveal"><div class="section-head"><h2>Активная ветка</h2><span>${worldEra(active.eraId).title}</span></div><article class="active-world-campaign"><img src="${campaignCover(active)}" alt=""><div><small>${active.period}</small><h3>${active.title}</h3><p>${completedMissionCount()}/${CAMPAIGN.nodes.length} миссий текущего релиза · ${active.releasedChapters}/${active.chapterCount} глав кампании опубликовано</p><div class="progress"><span style="width:${campaignProgress()}%"></span></div></div><button class="btn" onclick="go('campaign')">Продолжить</button></article></section><section class="daily-home-card reveal" onclick="openDaily()"><div class="daily-home-icon">◷</div><div><div class="eyebrow">Ежедневное обучение</div><h3>${dailyLearningCompleteToday()?'Сессия выполнена':`Сегодня к повторению: ${dailyDueCards().length}`}</h3><p>${dailyLearningCompleteToday()?'Архивный пак разблокирован.':'Повтори открытые знания за пять минут.'}</p></div><button class="btn ${dailyLearningCompleteToday()?'secondary':''}">${dailyLearningCompleteToday()?'Открыть':'Начать'}</button></section>`);
};

const V21_campaign=campaign;
campaign=function(){
 const html=V21_campaign();const c=worldCampaign('ROME_CAMPAIGN'),era=worldEra(c.eraId);
 return html.replace('<div class="view">',`<div class="view"><nav class="world-breadcrumb"><button onclick="go('world')">◎ Мир</button><span>›</span><button onclick="state.worldEra='${era.id}';state.worldView='CAMPAIGNS';go('world')">${era.title}</button><span>›</span><b>Рим</b></nav>`);
};

const V21_profile=profile;
profile=function(){return V21_profile().replace('Рождение Рима ·','Римская кампания ·').replace('Кампания</div>','Активная кампания</div>');};

const V21_render=render;
render=function(){
 if(state.tab!=='world')return V21_render();
 closeMobileMenu?.();dailySyncSchedule?.();syncDiscovery?.();applyTheme();destroyMaps();applyPreferences?.();
 document.getElementById('app').innerHTML=worldScreen();
 requestAnimationFrame(()=>{initEnhancements();});
};
