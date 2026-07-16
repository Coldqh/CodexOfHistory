#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));const exists=p=>fs.existsSync(path.join(root,p));
const manifest=read('data/content-manifest.json');assert.equal(manifest.version,'7.6.0');
const required=['data/cards/hellenistic/story.json','data/cards/hellenistic/archive.json','data/campaigns/hellenistic/campaign.json','data/campaigns/hellenistic/pools.json','data/lessons/hellenistic/campaign.json','data/quizzes/hellenistic/campaign.json','data/stories/hellenistic/personal.json','data/maps/hellenistic.json','assets/packs/hellenistic-pack.svg','js/features/v6-0-hellenistic.js'];
for(const p of required)assert.ok(exists(p),`missing ${p}`);
const story=read(required[0]),archive=read(required[1]),campaign=read(required[2]),pools=read(required[3]),lessons=read(required[4]),quizzes=read(required[5]),stories=read(required[6]),map=read(required[7]);
assert.equal(story.length,80);assert.equal(archive.length,40);assert.equal(campaign.chapters.length,10);assert.equal(campaign.nodes.length,60);assert.equal(Object.keys(lessons).length,60);assert.equal(Object.keys(quizzes).length,14);assert.equal(pools.pools.length,10);assert.equal(Object.keys(stories).length,10);
assert.equal(campaign.id,'HELLENISTIC');assert.equal(campaign.nodes[0].id,'HEL_01_01');assert.equal(campaign.nodes.at(-1).id,'HEL_10_06');assert.equal(campaign.nodes.at(-1).campaignExamModules.length,4);assert.equal(campaign.eraLayer.phases.length,4);
for(const key of ['BABYLON','IPSUS','ALEXANDRIA','SELEUCIA','PELLA','PERGAMON','DELOS','ATHENS','JERUSALEM','ACTIUM'])assert.ok(map.points[key],`missing map point ${key}`);assert.equal(Object.keys(map.chapters).length,10);
for(const c of [...story,...archive]){assert.ok(exists(c.image.local),`${c.id}: missing image`);assert.equal(c.campaign,'HELLENISTIC');}
assert.ok(story.every(c=>c.acquisition==='STORY'));assert.ok(archive.every(c=>c.acquisition==='ARCHIVE'));
const allCards=manifest.datasets.cards.flatMap(read);const olderTitles=new Set(allCards.filter(c=>c.campaign!=='HELLENISTIC').map(c=>c.title.toLocaleLowerCase('ru-RU')));for(const c of [...story,...archive])assert.ok(!olderTitles.has(c.title.toLocaleLowerCase('ru-RU')),`${c.id}: duplicate old title ${c.title}`);assert.equal(new Set([...story,...archive].map(c=>c.title.toLocaleLowerCase('ru-RU'))).size,120);
const world=read('data/world/campaigns.json').find(c=>c.id==='HELLENISTIC');assert.equal(world.status,'PLAYABLE');assert.equal(world.releasedChapters,10);assert.equal(world.chapterCount,10);
const era=read('data/world/eras.json').find(e=>e.id==='ERA_HELLENISTIC_ROMAN');assert.ok(era.campaignIds.includes('HELLENISTIC'));
const queries=read('data/image_queries.json');assert.equal(queries.version,'7.6.0');assert.equal(queries.count,4767);assert.equal(Object.keys(queries.cards).length,4767);assert.equal(queries.cards.HEL_S_01_01.group,'HELLENISTIC');
const images=read('data/image_manifest.json');assert.equal(images.version,'7.6.0');assert.equal(images.count,4767);assert.equal(images.staticHistoricalImageCount,42);assert.equal(images.projectCoverCount,4725);assert.equal(images.dynamicQueryCount,4725);
const rel=read('data/core/relations.json');assert.ok(rel.some(r=>r.source==='ALX_S_10_01'&&r.target==='HEL_S_01_01'));assert.ok(rel.some(r=>r.source==='STATE_ROM_002'&&r.target==='HEL_S_10_01'));
const runtime=fs.readFileSync(path.join(root,'js/features/v6-0-hellenistic.js'),'utf8');for(const token of ["const V='7.6.0'",'HELLENISTIC','hellenisticPhase','openHellenisticExamModule','assets/packs/hellenistic-pack.svg'])assert.match(runtime,new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
const sw=fs.readFileSync(path.join(root,'sw.js'),'utf8');assert.match(sw,/v6-0-hellenistic\.js/);assert.match(sw,/hellenistic-pack\.svg/);
const allText=JSON.stringify({story,archive,campaign,lessons});assert.match(allText,/диадох|Птолеме|Селевкид/i);assert.match(allText,/Александрия|Пергам|Родос/i);assert.match(allText,/папирус|монет|надпис|источник/i);assert.ok(!allText.includes('полностью уничтожила местные языки'));
console.log('✓ v6.0 Hellenistic world static smoke: 10 chapters, 60 missions, 120 cards');
