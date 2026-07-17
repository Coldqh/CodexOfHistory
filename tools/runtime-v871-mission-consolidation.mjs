import fs from 'node:fs';import path from 'node:path';import vm from 'node:vm';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const code=fs.readFileSync(path.join(root,'js/features/v8-7-1-mission-consolidation.js'),'utf8');
const state={missionsCompleted:['MES_01_02','MES_01_01','EGY_05_04'],currentMission:'EGY_05_05',lessonStages:{MES_01_02:2,MES_01_01:1},lessonUnlockedStages:{EGY_05_04:3},mapTasks:{EGY_05_04:{ok:true}},timelineTasks:{EGY_05_05:{ok:true}}};let saves=0;
vm.runInNewContext(code,{state,save:()=>saves++});
assert.deepEqual([...state.missionsCompleted],['MES_01_01','EGY_05_03']);assert.equal(state.currentMission,'EGY_05_06');assert.equal(state.lessonStages.MES_01_01,2);assert(state.mapTasks.EGY_05_03);assert(state.timelineTasks.EGY_05_06);assert.equal(saves,1);
console.log('✓ v8.7.2 mission consolidation runtime');
