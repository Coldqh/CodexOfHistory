#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));const exists=p=>fs.existsSync(path.join(root,p));
const manifest=read('data/content-manifest.json');assert.equal(manifest.version,'8.6.0');
const required=['data/cards/vedic-india/story.json','data/cards/vedic-india/archive.json','data/campaigns/vedic-india/campaign.json','data/campaigns/vedic-india/pools.json','data/lessons/vedic-india/campaign.json','data/quizzes/vedic-india/campaign.json','data/stories/vedic-india/personal.json','data/maps/vedic-india.json','assets/packs/vedic-india-pack.svg','js/features/v4-5-vedic-india.js'];
for(const p of required)assert.ok(exists(p),`missing ${p}`);
const story=read('data/cards/vedic-india/story.json'),archive=read('data/cards/vedic-india/archive.json'),campaign=read('data/campaigns/vedic-india/campaign.json'),pools=read('data/campaigns/vedic-india/pools.json'),lessons=read('data/lessons/vedic-india/campaign.json'),quizzes=read('data/quizzes/vedic-india/campaign.json'),stories=read('data/stories/vedic-india/personal.json'),map=read('data/maps/vedic-india.json');
assert.equal(story.length,80);assert.equal(archive.length,40);assert.equal(campaign.chapters.length,10);assert.equal(campaign.nodes.length,60);assert.equal(Object.keys(lessons).length,60);assert.equal(Object.keys(quizzes).length,14);assert.equal(pools.pools.length,10);assert.equal(Object.keys(stories).length,10);
assert.equal(campaign.nodes[0].id,'VED_01_01');assert.equal(campaign.nodes.at(-1).id,'VED_10_06');assert.equal(campaign.nodes.at(-1).campaignExamModules.length,4);assert.equal(campaign.eraLayer.phases.length,4);
for(const key of ['SINDHU','SAPTA','KURUKSHETRA','HASTINAPURA','DOAB','VIDEHA','RAJGIR'])assert.ok(map.points[key],`missing map point ${key}`);assert.equal(Object.keys(map.chapters).length,10);
for(const c of [...story,...archive]){assert.ok(exists(c.image.local),`${c.id}: missing image`);assert.equal(c.campaign,'INDIA_VEDIC');}
assert.ok(story.every(c=>c.acquisition==='STORY'));assert.ok(archive.every(c=>c.acquisition==='ARCHIVE'));
const world=read('data/world/campaigns.json').find(c=>c.id==='INDIA_VEDIC');assert.equal(world.status,'PLAYABLE');assert.equal(world.releasedChapters,10);assert.equal(world.chapterCount,10);
const era=read('data/world/eras.json').find(e=>e.id==='ERA_IRON');assert.ok(era.campaignIds.includes('INDIA_VEDIC'));
const queries=read('data/image_queries.json');assert.equal(queries.version,'8.6.0');assert.equal(queries.count,5931);assert.equal(Object.keys(queries.cards).length,5931);assert.equal(queries.cards.VED_S_03_01.group,'INDIA_VEDIC');
const images=read('data/image_manifest.json');assert.equal(images.version,'8.6.0');assert.equal(images.count,5931);assert.equal(images.staticHistoricalImageCount,42);assert.equal(images.projectCoverCount,5889);assert.equal(images.dynamicQueryCount,5889);
const rel=read('data/core/relations.json');assert.ok(rel.some(r=>r.source==='RIV_INDA_001'&&r.target==='VED_S_01_03'));assert.ok(rel.some(r=>r.source==='TEXT_IND_001'&&r.target==='VED_S_01_05'));
const runtime=fs.readFileSync(path.join(root,'js/features/v4-5-vedic-india.js'),'utf8');for(const token of ["const V='8.6.0'",'INDIA_VEDIC','assyria-phases','openVedicExamModule','assets/packs/vedic-india-pack.svg'])assert.match(runtime,new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
const sw=fs.readFileSync(path.join(root,'sw.js'),'utf8');assert.match(sw,/v4-5-vedic-india\.js/);assert.match(sw,/vedic-india-pack\.svg/);
const allText=JSON.stringify({story,archive,campaign,lessons});assert.match(allText,/ригвед|ведий/i);assert.match(allText,/археолог/i);assert.match(allText,/ритуал|санскрит|археолог/i);
console.log('✓ v4.5 Vedic India and early states static smoke: 10 chapters, 60 missions, 120 cards');
