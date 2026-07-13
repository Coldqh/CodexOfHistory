#!/usr/bin/env node
import fs from 'node:fs';import vm from 'node:vm';import assert from 'node:assert/strict';
const code=fs.readFileSync(new URL('../js/features/v3-1-1-hotfix.js',import.meta.url),'utf8');
const rome=['PER_ROM_001','PER_ROM_005','EVT_ROM_001'],bab=['BAB_S_01_01','BAB_S_01_02','BAB_S_01_03'];
const ctx={console,window:null,confirm:()=>true,CODEX_CAMPAIGNS:{
 ROME_CAMPAIGN:{id:'ROME_CAMPAIGN',chapters:[{id:'ROM_CH1'}],nodes:[{id:'MIS_BIRTH_01',chapterId:'ROM_CH1',cards:rome}]},
 BABYLON_OLD:{id:'BABYLON_OLD',chapters:[{id:'BAB_CH1'}],nodes:[{id:'BAB_01_01',chapterId:'BAB_CH1',cards:bab}]}
},initial:{tab:'home',xp:0,level:1,theme:'night',unlocked:[],read:[],currentCard:null,currentMission:null},
 state:{theme:'night',activeCampaign:'BABYLON_OLD',studyCampaign:'BABYLON_OLD',onboardingV26Done:true,unlocked:[...rome,...bab],discovered:[...rome],read:[rome[0]],xp:10,level:1,missionsCompleted:[],quizResults:{},packHistory:[],personalStoryProgress:{},masteryChecks:{}},
 syncDiscovery(){},startWorldCampaign(){},save(){},render(){},applyTheme(){},showToast(){},localStorage:{removeItem(){}},STORE:'codex_history_v02_ru'};
ctx.startWorldCampaign=(id)=>{ctx.state.activeCampaign=id;};
ctx.window=ctx;vm.createContext(ctx);vm.runInContext(code,ctx);
assert.deepEqual([...ctx.state.unlocked],bab,'Migration must remove leaked Rome starters');
assert.equal(ctx.state.xp,0);assert.equal(ctx.state.currentMission,'BAB_01_01');assert.equal(ctx.state.starterCampaignId,'BABYLON_OLD');
ctx.resetProgress();assert.deepEqual([...ctx.state.unlocked],[]);assert.deepEqual([...ctx.state.discovered],[]);assert.equal(ctx.state.onboardingV26Done,false);assert.equal(ctx.state.currentMission,null);
ctx.state.starterCampaignId=null;ctx.state.onboardingV26Done=true;ctx.startWorldCampaign('ROME_CAMPAIGN');assert.deepEqual([...ctx.state.unlocked],rome);assert.equal(ctx.state.currentMission,'MIS_BIRTH_01');
console.log('✓ v3.1.1 starter migration and reset runtime');
