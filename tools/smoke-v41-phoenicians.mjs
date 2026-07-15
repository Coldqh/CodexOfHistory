#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));const exists=p=>fs.existsSync(path.join(root,p));
const manifest=read('data/content-manifest.json');assert.equal(manifest.version,'6.2.0');
const required=['data/cards/phoenicians/story.json','data/cards/phoenicians/archive.json','data/campaigns/phoenicians/campaign.json','data/campaigns/phoenicians/pools.json','data/lessons/phoenicians/campaign.json','data/quizzes/phoenicians/campaign.json','data/stories/phoenicians/personal.json','data/maps/phoenicians.json','assets/packs/phoenicians-pack.svg','js/features/v4-1-phoenicians.js'];
for(const p of required)assert.ok(exists(p),`missing ${p}`);
const story=read('data/cards/phoenicians/story.json'),archive=read('data/cards/phoenicians/archive.json'),campaign=read('data/campaigns/phoenicians/campaign.json'),pools=read('data/campaigns/phoenicians/pools.json'),lessons=read('data/lessons/phoenicians/campaign.json'),quizzes=read('data/quizzes/phoenicians/campaign.json'),stories=read('data/stories/phoenicians/personal.json'),map=read('data/maps/phoenicians.json');
assert.equal(story.length,80);assert.equal(archive.length,40);assert.equal(campaign.chapters.length,10);assert.equal(campaign.nodes.length,60);assert.equal(Object.keys(lessons).length,60);assert.equal(Object.keys(quizzes).length,14);assert.equal(pools.pools.length,10);assert.equal(Object.keys(stories).length,10);
assert.equal(campaign.nodes[0].id,'PHO_01_01');assert.equal(campaign.nodes.at(-1).id,'PHO_10_06');assert.equal(campaign.nodes.at(-1).campaignExamModules.length,4);assert.equal(campaign.eraLayer.phases.length,4);
for(const key of ['TYRE','SIDON','BYBLOS','CARTHAGE','GADIR','KITION','MOTYA'])assert.ok(map.points[key],`missing map point ${key}`);assert.equal(Object.keys(map.chapters).length,10);
for(const c of [...story,...archive]){assert.ok(exists(c.image.local),`${c.id}: missing image`);assert.equal(c.campaign,'PHOENICIANS');}
assert.ok(story.every(c=>c.acquisition==='STORY'));assert.ok(archive.every(c=>c.acquisition==='ARCHIVE'));
const world=read('data/world/campaigns.json').find(c=>c.id==='PHOENICIANS');assert.equal(world.status,'PLAYABLE');assert.equal(world.releasedChapters,10);assert.equal(world.chapterCount,10);
const era=read('data/world/eras.json').find(e=>e.id==='ERA_IRON');assert.ok(era.campaignIds.includes('PHOENICIANS'));
const queries=read('data/image_queries.json');assert.equal(queries.version,'6.2.0');assert.equal(queries.count,3052);assert.equal(Object.keys(queries.cards).length,3052);assert.equal(queries.cards.PHO_S_03_01.group,'PHOENICIANS');
const images=read('data/image_manifest.json');assert.equal(images.version,'6.2.0');assert.equal(images.count,3052);assert.equal(images.staticHistoricalImageCount,42);assert.equal(images.projectCoverCount,3010);assert.equal(images.dynamicQueryCount,3010);
const rel=read('data/core/relations.json');assert.ok(rel.some(r=>r.source==='COL_S_10_06'&&r.target==='PHO_S_01_01'));assert.ok(rel.some(r=>r.source==='INT_S_08_02'&&r.target==='PHO_S_04_08'));
const runtime=fs.readFileSync(path.join(root,'js/features/v4-1-phoenicians.js'),'utf8');for(const token of ["const V='6.2.0'",'PHOENICIANS','assyria-phases','openPhoeniciaExamModule','assets/packs/phoenicians-pack.svg'])assert.match(runtime,new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
const sw=fs.readFileSync(path.join(root,'sw.js'),'utf8');assert.match(sw,/v4-1-phoenicians\.js/);assert.match(sw,/phoenicians-pack\.svg/);
console.log('✓ v4.1 Phoenicians and western Mediterranean static smoke: 10 chapters, 60 missions, 120 cards');
