#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));const exists=p=>fs.existsSync(path.join(root,p));
const manifest=read('data/content-manifest.json');assert.equal(manifest.version,'8.6.0');
const required=['data/cards/assyria-babylon/story.json','data/cards/assyria-babylon/archive.json','data/campaigns/assyria-babylon/campaign.json','data/campaigns/assyria-babylon/pools.json','data/lessons/assyria-babylon/campaign.json','data/quizzes/assyria-babylon/campaign.json','data/stories/assyria-babylon/personal.json','data/maps/assyria-babylon.json','assets/packs/assyria-babylon-pack.svg','js/features/v4-0-assyria-babylon.js'];
for(const p of required)assert.ok(exists(p),`missing ${p}`);
const story=read('data/cards/assyria-babylon/story.json'),archive=read('data/cards/assyria-babylon/archive.json'),campaign=read('data/campaigns/assyria-babylon/campaign.json'),pools=read('data/campaigns/assyria-babylon/pools.json'),lessons=read('data/lessons/assyria-babylon/campaign.json'),quizzes=read('data/quizzes/assyria-babylon/campaign.json'),stories=read('data/stories/assyria-babylon/personal.json'),map=read('data/maps/assyria-babylon.json');
assert.equal(story.length,80);assert.equal(archive.length,40);assert.equal(campaign.chapters.length,10);assert.equal(campaign.nodes.length,60);assert.equal(Object.keys(lessons).length,60);assert.equal(Object.keys(quizzes).length,14);assert.equal(pools.pools.length,10);assert.equal(Object.keys(stories).length,10);
assert.equal(campaign.nodes[0].id,'ASB_01_01');assert.equal(campaign.nodes.at(-1).id,'ASB_10_06');assert.equal(campaign.nodes.at(-1).campaignExamModules.length,4);assert.equal(campaign.eraLayer.phases.length,4);
for(const key of ['ASSUR','KALHU','DUR_SHARRUKIN','NINEVEH','LACHISH','BABYLON','JERUSALEM'])assert.ok(map.points[key],`missing map point ${key}`);assert.equal(Object.keys(map.chapters).length,10);
for(const c of [...story,...archive]){assert.ok(exists(c.image.local),`${c.id}: missing image`);assert.equal(c.campaign,'ASSYRIA_BABYLON');}
assert.ok(story.every(c=>c.acquisition==='STORY'));assert.ok(archive.every(c=>c.acquisition==='ARCHIVE'));
const world=read('data/world/campaigns.json').find(c=>c.id==='ASSYRIA_BABYLON');assert.equal(world.status,'PLAYABLE');assert.equal(world.releasedChapters,10);assert.equal(world.chapterCount,10);
const era=read('data/world/eras.json').find(e=>e.id==='ERA_IRON');assert.ok(era.campaignIds.includes('ASSYRIA_BABYLON'));
const queries=read('data/image_queries.json');assert.equal(queries.version,'8.6.0');assert.equal(queries.count,5931);assert.equal(Object.keys(queries.cards).length,5931);assert.equal(queries.cards.ASB_S_03_01.group,'ASSYRIA_BABYLON');
const images=read('data/image_manifest.json');assert.equal(images.version,'8.6.0');assert.equal(images.count,5931);assert.equal(images.staticHistoricalImageCount,42);assert.equal(images.projectCoverCount,5889);assert.equal(images.dynamicQueryCount,5889);
const rel=read('data/core/relations.json');assert.ok(rel.some(r=>r.source==='COL_S_09_02'&&r.target==='ASB_S_01_01'));assert.ok(rel.some(r=>r.source==='BAB_S_07_01'&&r.target==='ASB_S_01_03'));
const runtime=fs.readFileSync(path.join(root,'js/features/v4-0-assyria-babylon.js'),'utf8');for(const token of ["const V='8.6.0'",'ASSYRIA_BABYLON','assyria-phases','openAssyriaExamModule','assets/packs/assyria-babylon-pack.svg'])assert.match(runtime,new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
const sw=fs.readFileSync(path.join(root,'sw.js'),'utf8');assert.match(sw,/v4-0-assyria-babylon\.js/);assert.match(sw,/assyria-babylon-pack\.svg/);
console.log('✓ v4.0 Assyria and Neo-Babylonian static smoke: 10 chapters, 60 missions, 120 cards');
