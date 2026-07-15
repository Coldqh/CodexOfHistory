#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));const exists=p=>fs.existsSync(path.join(root,p));
const manifest=read('data/content-manifest.json');assert.equal(manifest.version,'6.8.0');
const required=['data/cards/maurya/story.json','data/cards/maurya/archive.json','data/campaigns/maurya/campaign.json','data/campaigns/maurya/pools.json','data/lessons/maurya/campaign.json','data/quizzes/maurya/campaign.json','data/stories/maurya/personal.json','data/maps/maurya.json','assets/packs/maurya-pack.svg','js/features/v6-4-maurya.js'];
for(const p of required)assert.ok(exists(p),`missing ${p}`);
const story=read(required[0]),archive=read(required[1]),campaign=read(required[2]),pools=read(required[3]),lessons=read(required[4]),quizzes=read(required[5]),stories=read(required[6]),map=read(required[7]);
assert.equal(story.length,88);assert.equal(archive.length,44);assert.equal(campaign.chapters.length,11);assert.equal(campaign.nodes.length,66);assert.equal(Object.keys(lessons).length,66);assert.equal(Object.keys(quizzes).length,15);assert.equal(pools.pools.length,11);assert.equal(Object.keys(stories).length,11);
assert.equal(campaign.id,'INDIA_MAURYA');assert.equal(campaign.nodes[0].id,'MAU_01_01');assert.equal(campaign.nodes.at(-1).id,'MAU_11_06');assert.equal(campaign.nodes.at(-1).campaignExamModules.length,4);assert.equal(campaign.eraLayer.phases.length,4);
for(const key of ['VAISHALI','RAJAGRIHA','BODH_GAYA','SARNATH','PATALIPUTRA','TAXILA','KALINGA','KANDAHAR','SANCHI','BARABAR','SRI_LANKA'])assert.ok(map.points[key],`missing map point ${key}`);assert.equal(Object.keys(map.chapters).length,11);
for(const c of [...story,...archive]){assert.ok(exists(c.image.local),`${c.id}: missing image`);assert.equal(c.campaign,'INDIA_MAURYA');}
assert.ok(story.every(c=>c.acquisition==='STORY'));assert.ok(archive.every(c=>c.acquisition==='ARCHIVE'));
const allCards=manifest.datasets.cards.flatMap(read);const olderTitles=new Set(allCards.filter(c=>c.campaign!=='INDIA_MAURYA').map(c=>c.title.toLocaleLowerCase('ru-RU')));for(const c of [...story,...archive])assert.ok(!olderTitles.has(c.title.toLocaleLowerCase('ru-RU')),`${c.id}: duplicate old title ${c.title}`);assert.equal(new Set([...story,...archive].map(c=>c.title.toLocaleLowerCase('ru-RU'))).size,132);
const world=read('data/world/campaigns.json').find(c=>c.id==='INDIA_MAURYA');assert.equal(world.status,'PLAYABLE');assert.equal(world.releasedChapters,11);assert.equal(world.chapterCount,11);
const era=read('data/world/eras.json').find(e=>e.id==='ERA_HELLENISTIC_ROMAN');assert.ok(era.campaignIds.includes('INDIA_MAURYA'));
const timeline=read('data/world/timeline.json').filter(x=>x.campaignId==='INDIA_MAURYA');assert.ok(timeline.length>=6);
const queries=read('data/image_queries.json');assert.equal(queries.version,'6.8.0');assert.equal(queries.count,3711);assert.equal(Object.keys(queries.cards).length,3711);assert.equal(queries.cards.MAU_S_01_01.group,'INDIA_MAURYA');
const images=read('data/image_manifest.json');assert.equal(images.version,'6.8.0');assert.equal(images.count,3711);assert.equal(images.staticHistoricalImageCount,42);assert.equal(images.projectCoverCount,3669);assert.equal(images.dynamicQueryCount,3669);
const rel=read('data/core/relations.json');assert.ok(rel.some(r=>r.source==='ALX_S_08_08'&&r.target==='MAU_S_07_04'));assert.ok(rel.some(r=>r.source==='HEL_S_04_01'&&r.target==='MAU_S_07_04'));
const runtime=fs.readFileSync(path.join(root,'js/features/v6-4-maurya.js'),'utf8');for(const token of ["const V='6.8.0'",'INDIA_MAURYA','mauryaPhase','CITIES_TEACHERS','openMauryaExamModule','assets/packs/maurya-pack.svg'])assert.match(runtime,new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
const sw=fs.readFileSync(path.join(root,'sw.js'),'utf8');assert.match(sw,/v6-4-maurya\.js/);assert.match(sw,/maurya-pack\.svg/);
const allText=JSON.stringify({story,archive,campaign,lessons});assert.match(allText,/Будд|сангх|дхамм/i);assert.match(allText,/Махавир|джайн/i);assert.match(allText,/Чандрагупт|Ашок|Маур/i);assert.match(allText,/эдикт|надпис|археолог|источник/i);assert.ok(!allText.includes('декларация прав человека'));
console.log('✓ v6.4 India, Buddha, Magadha and Mauryas static smoke: 11 chapters, 66 missions, 132 cards');
