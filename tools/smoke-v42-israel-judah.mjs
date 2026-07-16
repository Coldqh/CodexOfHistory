#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));const exists=p=>fs.existsSync(path.join(root,p));
const manifest=read('data/content-manifest.json');assert.equal(manifest.version,'7.4.0');
const required=['data/cards/israel-judah/story.json','data/cards/israel-judah/archive.json','data/campaigns/israel-judah/campaign.json','data/campaigns/israel-judah/pools.json','data/lessons/israel-judah/campaign.json','data/quizzes/israel-judah/campaign.json','data/stories/israel-judah/personal.json','data/maps/israel-judah.json','assets/packs/israel-judah-pack.svg','js/features/v4-2-israel-judah.js'];
for(const p of required)assert.ok(exists(p),`missing ${p}`);
const story=read('data/cards/israel-judah/story.json'),archive=read('data/cards/israel-judah/archive.json'),campaign=read('data/campaigns/israel-judah/campaign.json'),pools=read('data/campaigns/israel-judah/pools.json'),lessons=read('data/lessons/israel-judah/campaign.json'),quizzes=read('data/quizzes/israel-judah/campaign.json'),stories=read('data/stories/israel-judah/personal.json'),map=read('data/maps/israel-judah.json');
assert.equal(story.length,80);assert.equal(archive.length,40);assert.equal(campaign.chapters.length,10);assert.equal(campaign.nodes.length,60);assert.equal(Object.keys(lessons).length,60);assert.equal(Object.keys(quizzes).length,14);assert.equal(pools.pools.length,10);assert.equal(Object.keys(stories).length,10);
assert.equal(campaign.nodes[0].id,'LEV_01_01');assert.equal(campaign.nodes.at(-1).id,'LEV_10_06');assert.equal(campaign.nodes.at(-1).campaignExamModules.length,4);assert.equal(campaign.eraLayer.phases.length,4);
for(const key of ['JERUSALEM','SAMARIA','LACHISH','MEGIDDO','DIBON','DAMASCUS','BABYLON'])assert.ok(map.points[key],`missing map point ${key}`);assert.equal(Object.keys(map.chapters).length,10);
for(const c of [...story,...archive]){assert.ok(exists(c.image.local),`${c.id}: missing image`);assert.equal(c.campaign,'ISRAEL_JUDAH');}
assert.ok(story.every(c=>c.acquisition==='STORY'));assert.ok(archive.every(c=>c.acquisition==='ARCHIVE'));
const world=read('data/world/campaigns.json').find(c=>c.id==='ISRAEL_JUDAH');assert.equal(world.status,'PLAYABLE');assert.equal(world.releasedChapters,10);assert.equal(world.chapterCount,10);
const era=read('data/world/eras.json').find(e=>e.id==='ERA_IRON');assert.ok(era.campaignIds.includes('ISRAEL_JUDAH'));
const queries=read('data/image_queries.json');assert.equal(queries.version,'7.4.0');assert.equal(queries.count,4503);assert.equal(Object.keys(queries.cards).length,4503);assert.equal(queries.cards.LEV_S_03_01.group,'ISRAEL_JUDAH');
const images=read('data/image_manifest.json');assert.equal(images.version,'7.4.0');assert.equal(images.count,4503);assert.equal(images.staticHistoricalImageCount,42);assert.equal(images.projectCoverCount,4461);assert.equal(images.dynamicQueryCount,4461);
const rel=read('data/core/relations.json');assert.ok(rel.some(r=>r.source==='COL_S_10_06'&&r.target==='LEV_S_01_01'));assert.ok(rel.some(r=>r.source==='ASB_S_07_03'&&r.target==='LEV_S_09_02'));
const runtime=fs.readFileSync(path.join(root,'js/features/v4-2-israel-judah.js'),'utf8');for(const token of ["const V='7.4.0'",'ISRAEL_JUDAH','assyria-phases','openLevantExamModule','assets/packs/israel-judah-pack.svg'])assert.match(runtime,new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
const sw=fs.readFileSync(path.join(root,'sw.js'),'utf8');assert.match(sw,/v4-2-israel-judah\.js/);assert.match(sw,/israel-judah-pack\.svg/);
const allText=JSON.stringify({story,archive,campaign,lessons});assert.match(allText,/библейск/i);assert.match(allText,/археолог/i);assert.match(allText,/надпис/i);
console.log('✓ v4.2 Israel, Judah and Southern Levant static smoke: 10 chapters, 60 missions, 120 cards');
