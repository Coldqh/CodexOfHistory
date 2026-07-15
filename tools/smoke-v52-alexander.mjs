#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));const exists=p=>fs.existsSync(path.join(root,p));
const manifest=read('data/content-manifest.json');assert.equal(manifest.version,'6.9.0');
const required=['data/cards/alexander/story.json','data/cards/alexander/archive.json','data/campaigns/alexander/campaign.json','data/campaigns/alexander/pools.json','data/lessons/alexander/campaign.json','data/quizzes/alexander/campaign.json','data/stories/alexander/personal.json','data/maps/alexander.json','assets/packs/alexander-pack.svg','js/features/v5-2-alexander.js'];
for(const p of required)assert.ok(exists(p),`missing ${p}`);
const story=read(required[0]),archive=read(required[1]),campaign=read(required[2]),pools=read(required[3]),lessons=read(required[4]),quizzes=read(required[5]),stories=read(required[6]),map=read(required[7]);
assert.equal(story.length,80);assert.equal(archive.length,40);assert.equal(campaign.chapters.length,10);assert.equal(campaign.nodes.length,60);assert.equal(Object.keys(lessons).length,60);assert.equal(Object.keys(quizzes).length,14);assert.equal(pools.pools.length,10);assert.equal(Object.keys(stories).length,10);
assert.equal(campaign.id,'ALEXANDER');assert.equal(campaign.nodes[0].id,'ALX_01_01');assert.equal(campaign.nodes.at(-1).id,'ALX_10_06');assert.equal(campaign.nodes.at(-1).campaignExamModules.length,4);assert.equal(campaign.eraLayer.phases.length,4);
for(const key of ['PELLA','GRANICUS','ISSUS','TYRE','ALEXANDRIA','GAUGAMELA','PERSEPOLIS','BACTRA','HYDASPES','BABYLON_LAST'])assert.ok(map.points[key],`missing map point ${key}`);assert.equal(Object.keys(map.chapters).length,10);
for(const c of [...story,...archive]){assert.ok(exists(c.image.local),`${c.id}: missing image`);assert.equal(c.campaign,'ALEXANDER');}
assert.ok(story.every(c=>c.acquisition==='STORY'));assert.ok(archive.every(c=>c.acquisition==='ARCHIVE'));
const allCards=manifest.datasets.cards.flatMap(read);const olderTitles=new Set(allCards.filter(c=>c.campaign!=='ALEXANDER').map(c=>c.title.toLocaleLowerCase('ru-RU')));for(const c of [...story,...archive])assert.ok(!olderTitles.has(c.title.toLocaleLowerCase('ru-RU')),`${c.id}: duplicate old title ${c.title}`);
assert.equal(new Set([...story,...archive].map(c=>c.title.toLocaleLowerCase('ru-RU'))).size,120);
const world=read('data/world/campaigns.json').find(c=>c.id==='ALEXANDER');assert.equal(world.status,'PLAYABLE');assert.equal(world.releasedChapters,10);assert.equal(world.chapterCount,10);
const era=read('data/world/eras.json').find(e=>e.id==='ERA_CLASSICAL');assert.ok(era.campaignIds.includes('ALEXANDER'));
const queries=read('data/image_queries.json');assert.equal(queries.version,'6.9.0');assert.equal(queries.count,3843);assert.equal(Object.keys(queries.cards).length,3843);assert.equal(queries.cards.ALX_S_01_01.group,'ALEXANDER');
const images=read('data/image_manifest.json');assert.equal(images.version,'6.9.0');assert.equal(images.count,3843);assert.equal(images.staticHistoricalImageCount,42);assert.equal(images.projectCoverCount,3801);assert.equal(images.dynamicQueryCount,3801);
const rel=read('data/core/relations.json');assert.ok(rel.some(r=>r.source==='CLG_S_10_01'&&r.target==='ALX_S_01_01'));assert.ok(rel.some(r=>r.source==='PER_S_10_08'&&r.target==='ALX_S_05_07'));
const runtime=fs.readFileSync(path.join(root,'js/features/v5-2-alexander.js'),'utf8');for(const token of ["const V='6.9.0'",'ALEXANDER','alexanderPhase','openAlexanderExamModule','assets/packs/alexander-pack.svg'])assert.match(runtime,new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
const sw=fs.readFileSync(path.join(root,'sw.js'),'utf8');assert.match(sw,/v5-2-alexander\.js/);assert.match(sw,/alexander-pack\.svg/);
const allText=JSON.stringify({story,archive,campaign,lessons});assert.match(allText,/Граник|Гавгамел|Гидасп/i);assert.match(allText,/Дарий|сатрап|Вавилон/i);assert.match(allText,/источник|Арриан|археолог/i);assert.ok(!allText.includes('однородными сразу'));
console.log('✓ v5.2 Alexander static smoke: 10 chapters, 60 missions, 120 cards');
