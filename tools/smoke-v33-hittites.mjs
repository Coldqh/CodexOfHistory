#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));const exists=p=>fs.existsSync(path.join(root,p));
const manifest=read('data/content-manifest.json'),d=manifest.datasets;assert.equal(manifest.version,'4.6.0');
for(const p of ['data/cards/hittites/story.json','data/cards/hittites/archive.json','data/campaigns/hittites/campaign.json','data/campaigns/hittites/pools.json','data/lessons/hittites/campaign.json','data/quizzes/hittites/campaign.json','data/stories/hittites/personal.json','data/maps/hittites.json'])assert.ok(exists(p),`missing ${p}`);
const story=read('data/cards/hittites/story.json'),archive=read('data/cards/hittites/archive.json'),campaign=read('data/campaigns/hittites/campaign.json'),pools=read('data/campaigns/hittites/pools.json'),lessons=read('data/lessons/hittites/campaign.json'),quizzes=read('data/quizzes/hittites/campaign.json'),stories=read('data/stories/hittites/personal.json'),map=read('data/maps/hittites.json');
assert.equal(story.length,80);assert.equal(archive.length,40);assert.equal(campaign.chapters.length,10);assert.equal(campaign.nodes.length,60);assert.equal(Object.keys(lessons).length,60);assert.equal(Object.keys(quizzes).length,14);assert.equal(pools.pools.length,10);assert.equal(Object.keys(stories).length,10);
assert.equal(campaign.nodes[0].id,'HIT_01_01');assert.equal(campaign.nodes.at(-1).campaignExamModules.length,4);assert.equal(campaign.nodes.at(-1).id,'HIT_10_06');
assert.ok(map.points.HATTUSA);assert.ok(map.points.KADESH);assert.ok(map.points.UGARIT);assert.equal(Object.keys(map.chapters).length,10);
for(const c of [...story,...archive]){assert.ok(exists(c.image.local),`${c.id}: missing image`);assert.equal(c.campaign,'HITTITES');}
assert.ok(archive.every(c=>c.acquisition==='ARCHIVE'));assert.ok(story.every(c=>c.acquisition==='STORY'));
const world=read('data/world/campaigns.json').find(c=>c.id==='HITTITES');assert.equal(world.status,'PLAYABLE');assert.equal(world.releasedChapters,10);assert.equal(world.chapterCount,10);
const queries=read('data/image_queries.json');assert.equal(queries.count,2411);assert.equal(queries.cards.HIT_S_01_08.candidates[0].title,'Hatti');assert.equal(queries.cards.HIT_S_09_03.candidates[0].title,'Battle of Kadesh');
const rel=read('data/core/relations.json');assert.ok(rel.some(r=>r.source==='EMN_S_10_03'&&r.target==='HIT_S_09_03'));assert.ok(rel.some(r=>r.source==='BAB_S_08_08'&&r.target==='HIT_S_04_03'));
const runtime=fs.readFileSync(path.join(root,'js/features/v3-3-hittites.js'),'utf8');for(const token of ["const V='4.6.0'",'HITTITES','hittite-phases','openHittiteExamModule','assets/packs/hittites-pack.svg'])assert.match(runtime,new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
console.log('✓ v3.3 Hittites static smoke: 10 chapters, 60 missions, 120 cards');
