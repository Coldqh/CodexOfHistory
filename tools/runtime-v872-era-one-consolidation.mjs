#!/usr/bin/env node
import fs from 'node:fs';import vm from 'node:vm';import assert from 'node:assert/strict';
const state={missionsCompleted:['IND_01_02','IND_01_05','CHN_08_04','CMP_03_02','CIV_06_02'],currentMission:'IND_07_05',lessonStages:{IND_01_02:2,IND_01_01:1,CHN_08_04:4},lessonUnlockedStages:{CIV_06_02:3},mapTasks:{CMP_03_02:{done:true}},timelineTasks:{IND_07_05:{done:true}}};let saves=0;
const context={state,window:{CODEX_VERSION:''},save(){saves++;},console};vm.createContext(context);
vm.runInContext(fs.readFileSync('js/features/v8-7-2-era-one-consolidation.js','utf8'),context);
assert.deepEqual([...state.missionsCompleted],['IND_01_01','IND_01_06','CHN_08_06','CMP_03_04','CIV_06_05']);assert.equal(state.currentMission,'IND_07_06');assert.equal(state.lessonStages.IND_01_01,2);assert.equal(state.lessonStages.CHN_08_06,4);assert.equal(state.lessonUnlockedStages.CIV_06_05,3);assert.ok(state.mapTasks.CMP_03_04.done);assert.ok(state.timelineTasks.IND_07_06.done);assert.equal(context.window.CODEX_VERSION,'8.7.2');assert.equal(saves,1);console.log('✓ v8.7.2 mission consolidation preserves progress across remaining Era I campaigns');
