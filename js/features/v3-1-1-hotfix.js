/* Codex v3.7.0 — starter campaign and image-state hotfix */
(()=>{
  const V='3.7.0';
  window.CODEX_VERSION=V;
  const LEGACY_ROME_STARTERS=['PER_ROM_001','PER_ROM_005','EVT_ROM_001'];

  function firstMission(campaignId){return CODEX_CAMPAIGNS[campaignId]?.nodes?.[0]||null;}
  function starterCards(campaignId){return [...new Set(firstMission(campaignId)?.cards||[])];}
  function noCompletedLearning(){
    return !(state.missionsCompleted?.length)
      && !Object.keys(state.quizResults||{}).length
      && !(state.packHistory?.length)
      && !Object.keys(state.personalStoryProgress||{}).length
      && !Object.values(state.masteryChecks||{}).some(x=>x?.passed);
  }
  function onlyAccidentalStarterProgress(campaignId){
    const allowed=new Set([...LEGACY_ROME_STARTERS,...starterCards(campaignId)]);
    const unlocked=Array.isArray(state.unlocked)?state.unlocked:[];
    const read=Array.isArray(state.read)?state.read:[];
    return noCompletedLearning()
      && unlocked.every(id=>allowed.has(id))
      && read.every(id=>LEGACY_ROME_STARTERS.includes(id))
      && Number(state.xp||0)<=40;
  }
  function seedStarterCampaign(campaignId,{replace=false}={}){
    const campaign=CODEX_CAMPAIGNS[campaignId];if(!campaign)return false;
    const first=firstMission(campaignId),cards=starterCards(campaignId);if(!first||!cards.length)return false;
    if(replace){
      state.unlocked=[];state.discovered=[];state.read=[];state.masteryChecks={};state.reviewSchedule={};
      state.xp=0;state.level=1;
    }
    state.activeCampaign=campaignId;
    state.starterCampaignId=state.starterCampaignId||campaignId;
    state.currentMission=first.id;
    state.currentCard=cards[0];
    state.campaignChapter=first.chapterId||campaign.chapters?.[0]?.id||null;
    state.mapChapter=first.chapterId||campaign.chapters?.[0]?.id||null;
    state.unlocked=Array.isArray(state.unlocked)?state.unlocked:[];
    state.discovered=Array.isArray(state.discovered)?state.discovered:[];
    cards.forEach(id=>{if(!state.unlocked.includes(id))state.unlocked.push(id);if(!state.discovered.includes(id))state.discovered.push(id);});
    return true;
  }

  // Repair profiles created by v3.0/v3.1 where Roman starter cards leaked into another first campaign.
  const chosen=CODEX_CAMPAIGNS[state.studyCampaign]?state.studyCampaign:state.activeCampaign;
  if(chosen&&chosen!=='ROME_CAMPAIGN'&&onlyAccidentalStarterProgress(chosen)){
    seedStarterCampaign(chosen,{replace:true});
    state.starterMigrationV311=true;
  }

  const previousSyncDiscovery=syncDiscovery;
  syncDiscovery=function(){
    const waitingForFirstChoice=!state.onboardingV26Done&&!state.starterCampaignId&&noCompletedLearning()&&!(state.unlocked?.length);
    if(waitingForFirstChoice){state.discovered=[];return;}
    previousSyncDiscovery();
  };

  const previousStartWorldCampaign=startWorldCampaign;
  startWorldCampaign=function(id){
    const shouldSeed=!state.starterCampaignId&&noCompletedLearning();
    previousStartWorldCampaign(id);
    if(shouldSeed&&seedStarterCampaign(id)){save();render();}
  };

  // This definition is last in the script chain and replaces every old Rome-biased reset.
  resetProgress=function(){
    if(!confirm('Сбросить весь локальный прогресс?'))return;
    const theme=state.theme==='parchment'?'parchment':'night';
    localStorage.removeItem(STORE);
    state={
      ...initial,theme,unlocked:[],discovered:[],read:[],quizResults:{},quizDone:[],missionsCompleted:[],
      mapTasks:{},timelineTasks:{},masteryChecks:{},reviewSchedule:{},fragments:0,packHistory:[],dailyPackDate:null,
      masteryFilter:'ALL',packModal:null,masterySession:null,collectionMode:'ALL',collectionView:'ARCHIVE',catalogScope:'ALL',
      packPity:{uncommon:0,rare:0,epic:0,legendary:0},personalStoryProgress:{},activeStoryline:null,poolUnlockModal:null,
      storyChoice:null,dailyHistory:{},learningDays:[],dailySession:null,dailyStats:{sessions:0,answers:0,correct:0},
      onboardingV26Done:false,onboardingV26Step:0,onboardingV26Era:null,onboardingV26Replay:false,starterCampaignId:null,
      studyCampaign:null,studyEra:null,activeCampaign:'ROME_CAMPAIGN',currentMission:null,currentCard:null
    };
    applyTheme();save();render();showToast('Прогресс сброшен','Выбери первую эпоху и кампанию','↺');
  };

  save();
})();
