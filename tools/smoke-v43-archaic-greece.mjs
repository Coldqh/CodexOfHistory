#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));const exists=p=>fs.existsSync(path.join(root,p));
const manifest=read('data/content-manifest.json');assert.equal(manifest.version,'8.7.2');
const required=['data/cards/archaic-greece/story.json','data/cards/archaic-greece/archive.json','data/campaigns/archaic-greece/campaign.json','data/campaigns/archaic-greece/pools.json','data/lessons/archaic-greece/campaign.json','data/quizzes/archaic-greece/campaign.json','data/stories/archaic-greece/personal.json','data/maps/archaic-greece.json','assets/packs/archaic-greece-pack.svg','js/features/v4-3-archaic-greece.js'];
for(const p of required)assert.ok(exists(p),`missing ${p}`);
const story=read('data/cards/archaic-greece/story.json'),archive=read('data/cards/archaic-greece/archive.json'),campaign=read('data/campaigns/archaic-greece/campaign.json'),pools=read('data/campaigns/archaic-greece/pools.json'),lessons=read('data/lessons/archaic-greece/campaign.json'),quizzes=read('data/quizzes/archaic-greece/campaign.json'),stories=read('data/stories/archaic-greece/personal.json'),map=read('data/maps/archaic-greece.json');
assert.equal(story.length,80);assert.equal(archive.length,40);assert.equal(campaign.chapters.length,10);assert.equal(campaign.nodes.length,60);assert.equal(Object.keys(lessons).length,60);assert.equal(Object.keys(quizzes).length,14);assert.equal(pools.pools.length,10);assert.equal(Object.keys(stories).length,10);
assert.equal(campaign.nodes[0].id,'ARC_01_01');assert.equal(campaign.nodes.at(-1).id,'ARC_10_06');assert.equal(campaign.nodes.at(-1).campaignExamModules.length,4);assert.equal(campaign.eraLayer.phases.length,4);
for(const key of ['ATHENS','SPARTA','CORINTH','DELPHI','OLYMPIA','MILETUS','SYRACUSE'])assert.ok(map.points[key],`missing map point ${key}`);assert.equal(Object.keys(map.chapters).length,10);
for(const c of [...story,...archive]){assert.ok(exists(c.image.local),`${c.id}: missing image`);assert.equal(c.campaign,'GREECE_ARCHAIC');}
assert.ok(story.every(c=>c.acquisition==='STORY'));assert.ok(archive.every(c=>c.acquisition==='ARCHIVE'));
const world=read('data/world/campaigns.json').find(c=>c.id==='GREECE_ARCHAIC');assert.equal(world.status,'PLAYABLE');assert.equal(world.releasedChapters,10);assert.equal(world.chapterCount,10);
const era=read('data/world/eras.json').find(e=>e.id==='ERA_IRON');assert.ok(era.campaignIds.includes('GREECE_ARCHAIC'));
const queries=read('data/image_queries.json');assert.equal(queries.version,'8.7.2');assert.equal(queries.count,6063);assert.equal(Object.keys(queries.cards).length,6063);assert.equal(queries.cards.ARC_S_03_01.group,'GREECE_ARCHAIC');
const images=read('data/image_manifest.json');assert.equal(images.version,'8.7.2');assert.equal(images.count,6063);assert.equal(images.staticHistoricalImageCount,42);assert.equal(images.projectCoverCount,6021);assert.equal(images.dynamicQueryCount,6021);
const rel=read('data/core/relations.json');assert.ok(rel.some(r=>r.source==='AEG_S_10_07'&&r.target==='ARC_S_01_01'));assert.ok(rel.some(r=>r.source==='PHO_S_02_07'&&r.target==='ARC_S_03_01'));
const runtime=fs.readFileSync(path.join(root,'js/features/v4-3-archaic-greece.js'),'utf8');for(const token of ["const V='8.7.2'",'GREECE_ARCHAIC','assyria-phases','openArchaicExamModule','assets/packs/archaic-greece-pack.svg'])assert.match(runtime,new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
const sw=fs.readFileSync(path.join(root,'sw.js'),'utf8');assert.match(sw,/v4-3-archaic-greece\.js/);assert.match(sw,/archaic-greece-pack\.svg/);
const allText=JSON.stringify({story,archive,campaign,lessons});assert.match(allText,/полис/i);assert.match(allText,/археолог/i);assert.match(allText,/алфавит|надпис/i);
console.log('✓ v4.3 Archaic Greece static smoke: 10 chapters, 60 missions, 120 cards');
