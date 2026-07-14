#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));const exists=p=>fs.existsSync(path.join(root,p));
const manifest=read('data/content-manifest.json');assert.equal(manifest.version,'4.6.0');
const required=['data/cards/zhou-warring/story.json','data/cards/zhou-warring/archive.json','data/campaigns/zhou-warring/campaign.json','data/campaigns/zhou-warring/pools.json','data/lessons/zhou-warring/campaign.json','data/quizzes/zhou-warring/campaign.json','data/stories/zhou-warring/personal.json','data/maps/zhou-warring.json','assets/packs/zhou-warring-pack.svg','js/features/v4-4-zhou-warring.js'];
for(const p of required)assert.ok(exists(p),`missing ${p}`);
const story=read('data/cards/zhou-warring/story.json'),archive=read('data/cards/zhou-warring/archive.json'),campaign=read('data/campaigns/zhou-warring/campaign.json'),pools=read('data/campaigns/zhou-warring/pools.json'),lessons=read('data/lessons/zhou-warring/campaign.json'),quizzes=read('data/quizzes/zhou-warring/campaign.json'),stories=read('data/stories/zhou-warring/personal.json'),map=read('data/maps/zhou-warring.json');
assert.equal(story.length,80);assert.equal(archive.length,40);assert.equal(campaign.chapters.length,10);assert.equal(campaign.nodes.length,60);assert.equal(Object.keys(lessons).length,60);assert.equal(Object.keys(quizzes).length,14);assert.equal(pools.pools.length,10);assert.equal(Object.keys(stories).length,10);
assert.equal(campaign.nodes[0].id,'ZHO_01_01');assert.equal(campaign.nodes.at(-1).id,'ZHO_10_06');assert.equal(campaign.nodes.at(-1).campaignExamModules.length,4);assert.equal(campaign.eraLayer.phases.length,4);
for(const key of ['ZHOUYUAN','FENGHAO','MUYE','LUOYI','LINZI','XIANYANG','CHANGPING'])assert.ok(map.points[key],`missing map point ${key}`);assert.equal(Object.keys(map.chapters).length,10);
for(const c of [...story,...archive]){assert.ok(exists(c.image.local),`${c.id}: missing image`);assert.equal(c.campaign,'ZHOU_WARRING');}
assert.ok(story.every(c=>c.acquisition==='STORY'));assert.ok(archive.every(c=>c.acquisition==='ARCHIVE'));
const world=read('data/world/campaigns.json').find(c=>c.id==='ZHOU_WARRING');assert.equal(world.status,'PLAYABLE');assert.equal(world.releasedChapters,10);assert.equal(world.chapterCount,10);
const era=read('data/world/eras.json').find(e=>e.id==='ERA_IRON');assert.ok(era.campaignIds.includes('ZHOU_WARRING'));
const queries=read('data/image_queries.json');assert.equal(queries.version,'4.6.0');assert.equal(queries.count,2411);assert.equal(Object.keys(queries.cards).length,2411);assert.equal(queries.cards.ZHO_S_03_01.group,'ZHOU_WARRING');
const images=read('data/image_manifest.json');assert.equal(images.version,'4.6.0');assert.equal(images.count,2411);assert.equal(images.staticHistoricalImageCount,42);assert.equal(images.projectCoverCount,2369);assert.equal(images.dynamicQueryCount,2369);
const rel=read('data/core/relations.json');assert.ok(rel.some(r=>r.source==='STATE_CHN_002'&&r.target==='ZHO_S_01_01'));assert.ok(rel.some(r=>r.source==='TEXT_CHN_001'&&r.target==='ZHO_A_01_03'));
const runtime=fs.readFileSync(path.join(root,'js/features/v4-4-zhou-warring.js'),'utf8');for(const token of ["const V='4.6.0'",'ZHOU_WARRING','assyria-phases','openZhouExamModule','assets/packs/zhou-warring-pack.svg'])assert.match(runtime,new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
const sw=fs.readFileSync(path.join(root,'sw.js'),'utf8');assert.match(sw,/v4-4-zhou-warring\.js/);assert.match(sw,/zhou-warring-pack\.svg/);
const allText=JSON.stringify({story,archive,campaign,lessons});assert.match(allText,/мандат|чжоу/i);assert.match(allText,/археолог/i);assert.match(allText,/бронз|надпис|конфуц/i);
console.log('✓ v4.4 Zhou and Warring States static smoke: 10 chapters, 60 missions, 120 cards');
