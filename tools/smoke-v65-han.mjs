#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));const exists=p=>fs.existsSync(path.join(root,p));
const manifest=read('data/content-manifest.json');assert.equal(manifest.version,'7.5.0');
const required=['data/cards/han/story.json','data/cards/han/archive.json','data/campaigns/han/campaign.json','data/campaigns/han/pools.json','data/lessons/han/campaign.json','data/quizzes/han/campaign.json','data/stories/han/personal.json','data/maps/han.json','assets/packs/han-pack.svg','js/features/v6-5-han.js'];
for(const p of required)assert.ok(exists(p),`missing ${p}`);
const story=read(required[0]),archive=read(required[1]),campaign=read(required[2]),pools=read(required[3]),lessons=read(required[4]),quizzes=read(required[5]),stories=read(required[6]),map=read(required[7]);
assert.equal(story.length,88);assert.equal(archive.length,44);assert.equal(campaign.chapters.length,11);assert.equal(campaign.nodes.length,66);assert.equal(Object.keys(lessons).length,66);assert.equal(Object.keys(quizzes).length,15);assert.equal(pools.pools.length,11);assert.equal(Object.keys(stories).length,11);
assert.equal(campaign.id,'HAN');assert.equal(campaign.nodes[0].id,'HAN_01_01');assert.equal(campaign.nodes.at(-1).id,'HAN_11_06');assert.equal(campaign.nodes.at(-1).campaignExamModules.length,4);assert.equal(campaign.eraLayer.phases.length,5);
for(const key of ['XIANYANG','CHANGAN','LUOYANG','JULU','GAIXIA','HEXICORRIDOR','DUNHUANG','YUMEN','FERGHANA','MAWANGDUI','KUNYANG'])assert.ok(map.points[key],`missing map point ${key}`);assert.equal(Object.keys(map.chapters).length,11);
for(const c of [...story,...archive]){assert.ok(exists(c.image.local),`${c.id}: missing image`);assert.equal(c.campaign,'HAN');}
assert.ok(story.every(c=>c.acquisition==='STORY'));assert.ok(archive.every(c=>c.acquisition==='ARCHIVE'));
const allCards=manifest.datasets.cards.flatMap(read);const olderTitles=new Set(allCards.filter(c=>c.campaign!=='HAN').map(c=>c.title.toLocaleLowerCase('ru-RU')));for(const c of [...story,...archive])assert.ok(!olderTitles.has(c.title.toLocaleLowerCase('ru-RU')),`${c.id}: duplicate old title ${c.title}`);assert.equal(new Set([...story,...archive].map(c=>c.title.toLocaleLowerCase('ru-RU'))).size,132);
const world=read('data/world/campaigns.json').find(c=>c.id==='HAN');assert.equal(world.status,'PLAYABLE');assert.equal(world.releasedChapters,11);assert.equal(world.chapterCount,11);
const era=read('data/world/eras.json').find(e=>e.id==='ERA_HELLENISTIC_ROMAN');assert.ok(era.campaignIds.includes('HAN'));
const timeline=read('data/world/timeline.json').filter(x=>x.campaignId==='HAN');assert.ok(timeline.length>=7);
const queries=read('data/image_queries.json');assert.equal(queries.version,'7.5.0');assert.equal(queries.count,4635);assert.equal(Object.keys(queries.cards).length,4635);assert.equal(queries.cards.HAN_S_01_01.group,'HAN');
const images=read('data/image_manifest.json');assert.equal(images.version,'7.5.0');assert.equal(images.count,4635);assert.equal(images.staticHistoricalImageCount,42);assert.equal(images.projectCoverCount,4593);assert.equal(images.dynamicQueryCount,4593);
const rel=read('data/core/relations.json');assert.ok(rel.some(r=>r.source==='ZHO_S_10_08'&&r.target==='HAN_S_01_02'));assert.ok(rel.some(r=>r.source==='HEL_S_04_05'&&r.target==='HAN_S_06_08'));
const runtime=fs.readFileSync(path.join(root,'js/features/v6-5-han.js'),'utf8');for(const token of ["const V='7.5.0'",'HAN','hanPhase','QIN_TRANSITION','openHanExamModule','assets/packs/han-pack.svg'])assert.match(runtime,new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
const sw=fs.readFileSync(path.join(root,'sw.js'),'utf8');assert.match(sw,/v6-5-han\.js/);assert.match(sw,/han-pack\.svg/);
const allText=JSON.stringify({story,archive,campaign,lessons});assert.match(allText,/Цинь|Сяньян/i);assert.match(allText,/У-ди|у-чжу|соль и железо/i);assert.match(allText,/сюнну|Хэси|Чжан Цян/i);assert.match(allText,/Сыма Цян|Хань шу|Маванду/i);assert.match(allText,/Ван Ман|Жёлтых повязок|220/i);assert.ok(!allText.includes('единый Шёлковый путь от Чанъаня до Рима'));
console.log('✓ v6.5 Han Empire static smoke: 11 chapters, 66 missions, 132 cards');
