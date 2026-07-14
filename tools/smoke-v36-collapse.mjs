#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));const exists=p=>fs.existsSync(path.join(root,p));
const manifest=read('data/content-manifest.json');assert.equal(manifest.version,'4.2.0');
const required=['data/cards/bronze-collapse/story.json','data/cards/bronze-collapse/archive.json','data/campaigns/bronze-collapse/campaign.json','data/campaigns/bronze-collapse/pools.json','data/lessons/bronze-collapse/campaign.json','data/quizzes/bronze-collapse/campaign.json','data/stories/bronze-collapse/personal.json','data/maps/bronze-collapse.json','assets/packs/bronze-collapse-pack.svg','js/features/v3-6-collapse.js'];
for(const p of required)assert.ok(exists(p),`missing ${p}`);
const story=read('data/cards/bronze-collapse/story.json'),archive=read('data/cards/bronze-collapse/archive.json'),campaign=read('data/campaigns/bronze-collapse/campaign.json'),pools=read('data/campaigns/bronze-collapse/pools.json'),lessons=read('data/lessons/bronze-collapse/campaign.json'),quizzes=read('data/quizzes/bronze-collapse/campaign.json'),stories=read('data/stories/bronze-collapse/personal.json'),map=read('data/maps/bronze-collapse.json');
assert.equal(story.length,80);assert.equal(archive.length,40);assert.equal(campaign.chapters.length,10);assert.equal(campaign.nodes.length,60);assert.equal(Object.keys(lessons).length,60);assert.equal(Object.keys(quizzes).length,14);assert.equal(pools.pools.length,10);assert.equal(Object.keys(stories).length,10);
assert.equal(campaign.nodes[0].id,'COL_01_01');assert.equal(campaign.nodes.at(-1).id,'COL_10_06');assert.equal(campaign.nodes.at(-1).campaignExamModules.length,4);assert.equal(campaign.eraLayer.phases.length,4);
for(const key of ['HATTUSA','UGARIT','MEDINET','MYCENAE','CYPRUS','CARCHEMISH'])assert.ok(map.points[key],`missing map point ${key}`);assert.equal(Object.keys(map.chapters).length,10);
for(const c of [...story,...archive]){assert.ok(exists(c.image.local),`${c.id}: missing image`);assert.equal(c.campaign,'BRONZE_COLLAPSE');}
assert.ok(story.every(c=>c.acquisition==='STORY'));assert.ok(archive.every(c=>c.acquisition==='ARCHIVE'));
const world=read('data/world/campaigns.json').find(c=>c.id==='BRONZE_COLLAPSE');assert.equal(world.status,'PLAYABLE');assert.equal(world.releasedChapters,10);assert.equal(world.chapterCount,10);
const queries=read('data/image_queries.json');assert.equal(queries.version,'4.2.0');assert.equal(queries.count,1955);assert.equal(Object.keys(queries.cards).length,1955);
const images=read('data/image_manifest.json');assert.equal(images.version,'4.2.0');assert.equal(images.count,1955);assert.equal(images.staticHistoricalImageCount,42);assert.equal(images.projectCoverCount,1913);assert.equal(images.dynamicQueryCount,1913);
const rel=read('data/core/relations.json');assert.ok(rel.some(r=>r.source==='INT_S_10_01'&&r.target==='COL_S_01_01'));assert.ok(rel.some(r=>r.source==='HIT_S_10_05'&&r.target==='COL_S_04_01'));assert.ok(rel.some(r=>r.source==='AEG_S_10_02'&&r.target==='COL_S_07_01'));
const runtime=fs.readFileSync(path.join(root,'js/features/v3-6-collapse.js'),'utf8');for(const token of ["const V='4.2.0'",'BRONZE_COLLAPSE','collapse-phases','openCollapseExamModule','assets/packs/bronze-collapse-pack.svg'])assert.match(runtime,new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
const bronzeRuntime=fs.readFileSync(path.join(root,'js/features/v3-1-babylon.js'),'utf8');assert.doesNotMatch(bronzeRuntime,/Пять кампаний доступны/);assert.doesNotMatch(bronzeRuntime,/bronze-world-summary/);
console.log('✓ v3.6 Bronze Age collapse static smoke: 10 chapters, 60 missions, 120 cards; redundant era summary removed');
