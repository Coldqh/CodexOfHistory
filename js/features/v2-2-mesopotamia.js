/* Codex v2.2 — playable Mesopotamia campaign and multi-campaign runtime */
const V22_CAMPAIGN_CODES={ROME_CAMPAIGN:'ROME',MESOPOTAMIA_DAWN:'MESOPOTAMIA'};
function activeCampaignId(){return CODEX_CAMPAIGNS[state.activeCampaign]?state.activeCampaign:'ROME_CAMPAIGN';}
function activeCampaignCode(){return V22_CAMPAIGN_CODES[activeCampaignId()]||activeCampaignId();}
function activeCampaignRuntime(){return CODEX_CAMPAIGNS[activeCampaignId()]||CODEX_CAMPAIGNS.ROME_CAMPAIGN;}
function activeCampaignWorld(){return worldCampaign(activeCampaignId());}
function syncActiveCampaignRuntime(){
  const next=activeCampaignRuntime();window.CAMPAIGN=next;CODEX_CONFIG.maps=CODEX_MAPS[next.id]||CODEX_MAPS.ROME_CAMPAIGN;
  if(!next.chapters.some(ch=>ch.id===state.campaignChapter))state.campaignChapter=next.chapters[0]?.id;
  if(!next.chapters.some(ch=>ch.id===state.mapChapter))state.mapChapter=next.chapters[0]?.id;
  if(!next.nodes.some(m=>m.id===state.currentMission))state.currentMission=next.nodes.find(m=>!missionCompleted(m.id))?.id||next.nodes[0]?.id;
  if(next.id==='MESOPOTAMIA_DAWN'){
    const first=next.nodes[0];(first?.cards||[]).forEach(id=>{if(!state.unlocked.includes(id))state.unlocked.push(id);});
  }
}
syncActiveCampaignRuntime();save();

poolUnlocked=function(pool){if(!pool||pool.campaign!==activeCampaignCode())return false;if(String(pool.unlockMission).includes('_CHAPTER_')&&!mission(pool.unlockMission))return false;return missionCompleted(pool.unlockMission);};
function campaignProgressFor(id){const c=CODEX_CAMPAIGNS[id];if(!c)return 0;return Math.round(c.nodes.filter(n=>missionCompleted(n.id)).length/Math.max(1,c.nodes.length)*100);}

const V22_startWorldCampaign=startWorldCampaign;
startWorldCampaign=function(id){const c=worldCampaign(id);if(!c)return;if(c.status!=='PLAYABLE'){return V22_startWorldCampaign(id);}state.activeCampaign=id;syncActiveCampaignRuntime();state.tab='campaign';state.worldCampaignPreview=null;save();render();window.scrollTo({top:0,behavior:'smooth'});};
worldCampaignCard=function(c){const progress=c.status==='PLAYABLE'?campaignProgressFor(c.id):0;return `<article class="world-campaign-card ${c.status.toLowerCase()}" onclick="previewWorldCampaign('${c.id}')"><div class="world-campaign-cover"><img src="${campaignCover(c)}" alt=""><span>${worldStatusIcon(c.status)} ${worldStatusLabel(c.status)}</span></div><div class="world-campaign-copy"><small>${c.period} · ${c.region}</small><h3>${c.title}</h3><p>${c.subtitle}</p><div class="campaign-publication"><b>${c.releasedChapters}/${c.chapterCount}</b><span>глав опубликовано</span></div>${c.status==='PLAYABLE'?`<div class="progress"><span style="width:${progress}%"></span></div>`:''}</div></article>`;};

const V22_go=go;
go=function(tab){if(tab==='campaign')syncActiveCampaignRuntime();V22_go(tab);};
const V22_openMission=openMission;
openMission=function(id){const found=Object.values(CODEX_CAMPAIGNS).find(c=>c.nodes.some(n=>n.id===id));if(found&&found.id!==CAMPAIGN.id){state.activeCampaign=found.id;syncActiveCampaignRuntime();}V22_openMission(id);};

function activeCampaignLabel(){return activeCampaignWorld()?.title||CAMPAIGN.title;}
function activeCampaignPackTitle(){return activeCampaignId()==='MESOPOTAMIA_DAWN'?'Месопотамский архивный пак':'Римский архивный пак';}
function activeCampaignPackCover(){return activeCampaignId()==='MESOPOTAMIA_DAWN'?'assets/packs/mesopotamia-pack.svg':'assets/packs/rome-pack.svg';}
PACK_DEFS.ROMAN.title='Коллекционный пак кампании';PACK_DEFS.ROMAN.emoji=activeCampaignId()==='MESOPOTAMIA_DAWN'?'𒀭':'SPQR';

const V22_packsScreen=packsScreen;
packsScreen=function(){
  const pools=unlockedPools(),available=packPool().filter(c=>!isUnlocked(c.id)).length,history=state.packHistory.slice(-6).reverse();
  return shell(`<section class="packs-page-head reveal"><div class="packs-title-block"><div class="eyebrow">Архив · ${activeCampaignLabel()}</div><h2>Паки знаний</h2><p>Дополнительные места, предметы, профессии и микроистории только из открытых глав активной кампании.</p><div class="fragment-balance compact-fragment-balance"><span>◇</span><b>${state.fragments}</b><small>фрагментов</small></div></div></section><section class="packs-page-grid reveal"><article class="pack-page-card ${dailyPackReady()?'ready':''}"><img src="${packCover('DAILY')}" alt="Архивный пак дня"><div class="pack-page-copy"><small>ЕЖЕДНЕВНЫЙ · 3 КАРТЫ</small><h3>Архивный пак дня</h3><p>${dailyPackReady()?'Награда за сегодняшнюю учебную сессию готова.':dailyLearningCompleteToday()?'Сегодняшний пак уже открыт.':'Заверши короткую дневную сессию.'}</p>${packAction('DAILY')}</div></article><article class="pack-page-card campaign-pack"><img src="${activeCampaignPackCover()}" alt="${activeCampaignPackTitle()}"><div class="pack-page-copy"><small>${activeCampaignId()==='MESOPOTAMIA_DAWN'?'МЕСОПОТАМИЯ':'РИМ'} · 4 КАРТЫ</small><h3>${activeCampaignPackTitle()}</h3><p>${available} новых карточек доступно в ${pools.length} открытых пулах.</p><div class="pack-page-meta"><span>Стоимость 60 ◇</span><span>${pools.length} пулов открыто</span></div>${packAction('ROMAN')}</div></article></section>${history.length?`<section class="section compact-card-section reveal"><div class="section-head"><h2>Последние открытия</h2><span>${history.length}</span></div><div class="pack-history-list">${history.map(h=>`<article><span>${h.kind==='DAILY'?'☀':(h.campaign==='MESOPOTAMIA_DAWN'?'𒀭':'SPQR')}</span><div><b>${h.kind==='DAILY'?'Архивный пак дня':'Коллекционный пак'}</b><small>${new Intl.DateTimeFormat('ru-RU',{day:'numeric',month:'short'}).format(new Date(h.date))}</small></div><em>${h.drops.filter(d=>d.fresh).length} новых</em></article>`).join('')}</div></section>`:''}`);
};

const V22_campaign=campaign;
campaign=function(){syncActiveCampaignRuntime();let html=V22_campaign();const wc=activeCampaignWorld(),era=worldEra(wc?.eraId);return html.replace(/РИМСКАЯ КАМПАНИЯ/g,activeCampaignId()==='MESOPOTAMIA_DAWN'?'МЕСОПОТАМСКАЯ КАМПАНИЯ':'РИМСКАЯ КАМПАНИЯ').replace('<div class="view">',`<div class="view"><nav class="world-breadcrumb"><button onclick="go('world')">◎ Мир</button><span>›</span><button onclick="state.worldEra='${era?.id||'ERA_DAWN'}';state.worldView='CAMPAIGNS';go('world')">${era?.title||'Эпоха'}</button><span>›</span><b>${wc?.title||CAMPAIGN.title}</b></nav>`);};

const V22_home=home;
home=function(){syncActiveCampaignRuntime();const m=currentMission(),wc=activeCampaignWorld();if(activeCampaignId()==='MESOPOTAMIA_DAWN')return shell(`<section class="global-home-hero mesopotamia-home reveal"><div class="global-home-copy"><div class="eyebrow">Рождение цивилизаций · v${appVersion()}</div><h2>Земля между реками<br><span>становится городским миром.</span></h2><p>Пять глав о географии, каналах, Убейдском периоде, Уруке и первых системах административного учёта.</p><div class="hero-actions"><button class="btn" onclick="openMission('${m.id}')">${m.emoji} Продолжить: ${m.title}</button><button class="btn secondary" onclick="go('world')">◎ Другие эпохи</button></div></div><div class="global-home-era"><img src="assets/eras/dawn.svg" alt=""><div><small>АКТИВНАЯ КАМПАНИЯ</small><h3>${wc.title}</h3><p>${completedMissionCount()}/${CAMPAIGN.nodes.length} миссий · ${campaignProgress()}%</p><button onclick="go('campaign')">Открыть маршрут →</button></div></div></section><section class="home-stats reveal"><div class="stat-box"><div class="stat-icon">𒀭</div><b>${campaignProgress()}%</b><span>кампания</span></div><div class="stat-box"><div class="stat-icon">▤</div><b>${completedMissionCount()}/${CAMPAIGN.nodes.length}</b><span>миссий</span></div><div class="stat-box"><div class="stat-icon">▦</div><b>${state.unlocked.filter(id=>card(id)?.campaign==='MESOPOTAMIA').length}</b><span>карточек Месопотамии</span></div><div class="stat-box stat-action" onclick="openPackHub()"><div class="stat-icon">✦</div><b>${dailyPackStatusShort()}</b><span>архивный пак дня</span></div></section><section class="daily-home-card reveal" onclick="openDaily()"><div class="daily-home-icon">◷</div><div><div class="eyebrow">Ежедневное обучение</div><h3>${dailyLearningCompleteToday()?'Сессия выполнена':`Сегодня к повторению: ${dailyDueCards().length}`}</h3><p>${dailyLearningCompleteToday()?'Архивный пак разблокирован.':'Повтори открытые знания за пять минут.'}</p></div><button class="btn ${dailyLearningCompleteToday()?'secondary':''}">${dailyLearningCompleteToday()?'Открыть':'Начать'}</button></section>`);return V22_home();};

const V22_profile=profile;
profile=function(){syncActiveCampaignRuntime();let html=V22_profile();return html.replace(/Рождение Рима/g,activeCampaignLabel()).replace(/Римская кампания/g,activeCampaignLabel());};

const V22_render=render;
render=function(){syncActiveCampaignRuntime();V22_render();};
