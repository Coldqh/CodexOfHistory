#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));const exists=p=>fs.existsSync(path.join(root,p));
const manifest=read('data/content-manifest.json');assert.equal(manifest.version,'6.1.0');
const required=['data/cards/achaemenid-persia/story.json','data/cards/achaemenid-persia/archive.json','data/campaigns/achaemenid-persia/campaign.json','data/campaigns/achaemenid-persia/pools.json','data/lessons/achaemenid-persia/campaign.json','data/quizzes/achaemenid-persia/campaign.json','data/stories/achaemenid-persia/personal.json','data/maps/achaemenid-persia.json','assets/packs/achaemenid-persia-pack.svg','js/features/v5-0-achaemenid-persia.js'];
for(const p of required)assert.ok(exists(p),`missing ${p}`);
const story=read(required[0]),archive=read(required[1]),campaign=read(required[2]),pools=read(required[3]),lessons=read(required[4]),quizzes=read(required[5]),stories=read(required[6]),map=read(required[7]);
assert.equal(story.length,80);assert.equal(archive.length,40);assert.equal(campaign.chapters.length,10);assert.equal(campaign.nodes.length,60);assert.equal(Object.keys(lessons).length,60);assert.equal(Object.keys(quizzes).length,14);assert.equal(pools.pools.length,10);assert.equal(Object.keys(stories).length,10);
assert.equal(campaign.nodes[0].id,'PER_01_01');assert.equal(campaign.nodes.at(-1).id,'PER_10_06');assert.equal(campaign.nodes.at(-1).campaignExamModules.length,4);assert.equal(campaign.eraLayer.phases.length,4);
for(const key of ['PARS','PASARGADAE','ECBATANA','BABYLON','BEHISTUN','PERSEPOLIS','SARDIS','SALAMIS','GAUGAMELA'])assert.ok(map.points[key],`missing map point ${key}`);assert.equal(Object.keys(map.chapters).length,10);
for(const c of [...story,...archive]){assert.ok(exists(c.image.local),`${c.id}: missing image`);assert.equal(c.campaign,'PERSIA');}
assert.ok(story.every(c=>c.acquisition==='STORY'));assert.ok(archive.every(c=>c.acquisition==='ARCHIVE'));
const world=read('data/world/campaigns.json').find(c=>c.id==='PERSIA');assert.equal(world.status,'PLAYABLE');assert.equal(world.releasedChapters,10);assert.equal(world.chapterCount,10);
const era=read('data/world/eras.json').find(e=>e.id==='ERA_CLASSICAL');assert.ok(era.campaignIds.includes('PERSIA'));
const queries=read('data/image_queries.json');assert.equal(queries.version,'6.1.0');assert.equal(queries.count,3018);assert.equal(Object.keys(queries.cards).length,3018);assert.equal(queries.cards.PER_S_05_02.group,'PERSIA');
const images=read('data/image_manifest.json');assert.equal(images.version,'6.1.0');assert.equal(images.count,3018);assert.equal(images.staticHistoricalImageCount,42);assert.equal(images.projectCoverCount,2976);assert.equal(images.dynamicQueryCount,2976);
const rel=read('data/core/relations.json');assert.ok(rel.some(r=>r.source==='ASB_S_10_07'&&r.target==='PER_S_02_07'));assert.ok(rel.some(r=>r.source==='ARC_S_09_08'&&r.target==='PER_S_09_01'));
const runtime=fs.readFileSync(path.join(root,'js/features/v5-0-achaemenid-persia.js'),'utf8');for(const token of ["const V='6.1.0'",'PERSIA','assyria-phases','openPersiaExamModule','assets/packs/achaemenid-persia-pack.svg'])assert.match(runtime,new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
const sw=fs.readFileSync(path.join(root,'sw.js'),'utf8');assert.match(sw,/v5-0-achaemenid-persia\.js/);assert.match(sw,/achaemenid-persia-pack\.svg/);
const allText=JSON.stringify({story,archive,campaign,lessons});assert.match(allText,/Кир|Дарий|Ахеменид/i);assert.match(allText,/сатрап|Персепол|Бехистун/i);assert.match(allText,/источник|надпис|архив/i);
assert.ok(!allText.includes('первая декларация прав человека — доказанный факт'));
console.log('✓ v5.0 Achaemenid Persia static smoke: 10 chapters, 60 missions, 120 cards');
