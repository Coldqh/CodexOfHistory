#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));const exists=p=>fs.existsSync(path.join(root,p));
const manifest=read('data/content-manifest.json');assert.equal(manifest.version,'6.9.1');
for(const p of ['data/cards/aegean/story.json','data/cards/aegean/archive.json','data/campaigns/aegean/campaign.json','data/campaigns/aegean/pools.json','data/lessons/aegean/campaign.json','data/quizzes/aegean/campaign.json','data/stories/aegean/personal.json','data/maps/aegean.json','assets/packs/aegean-pack.svg','js/features/v3-4-aegean.js'])assert.ok(exists(p),`missing ${p}`);
const story=read('data/cards/aegean/story.json'),archive=read('data/cards/aegean/archive.json'),campaign=read('data/campaigns/aegean/campaign.json'),pools=read('data/campaigns/aegean/pools.json'),lessons=read('data/lessons/aegean/campaign.json'),quizzes=read('data/quizzes/aegean/campaign.json'),stories=read('data/stories/aegean/personal.json'),map=read('data/maps/aegean.json');
assert.equal(story.length,80);assert.equal(archive.length,40);assert.equal(campaign.chapters.length,10);assert.equal(campaign.nodes.length,60);assert.equal(Object.keys(lessons).length,60);assert.equal(Object.keys(quizzes).length,14);assert.equal(pools.pools.length,10);assert.equal(Object.keys(stories).length,10);
assert.equal(campaign.nodes[0].id,'AEG_01_01');assert.equal(campaign.nodes.at(-1).campaignExamModules.length,4);assert.equal(campaign.nodes.at(-1).id,'AEG_10_06');
assert.ok(map.points.KNOSSOS);assert.ok(map.points.MYCENAE);assert.ok(map.points.AKROTIRI);assert.ok(map.points.PYLOS);assert.equal(Object.keys(map.chapters).length,10);
for(const c of [...story,...archive]){assert.ok(exists(c.image.local),`${c.id}: missing image`);assert.equal(c.campaign,'AEGEAN_BRONZE');}
assert.ok(archive.every(c=>c.acquisition==='ARCHIVE'));assert.ok(story.every(c=>c.acquisition==='STORY'));
const world=read('data/world/campaigns.json').find(c=>c.id==='AEGEAN_BRONZE');assert.equal(world.status,'PLAYABLE');assert.equal(world.releasedChapters,10);assert.equal(world.chapterCount,10);
const queries=read('data/image_queries.json');assert.equal(queries.count,3843);assert.equal(queries.cards.AEG_S_04_01.candidates[0].title,'Linear A');assert.equal(queries.cards.AEG_S_08_01.candidates[0].title,'Linear B');assert.equal(queries.cards.AEG_S_09_02.candidates[0].title,'Ahhiyawa');
const rel=read('data/core/relations.json');assert.ok(rel.some(r=>r.source==='HIT_S_08_05'&&r.target==='AEG_S_09_02'));assert.ok(rel.some(r=>r.source==='EMN_S_10_08'&&r.target==='AEG_S_10_02'));
const runtime=fs.readFileSync(path.join(root,'js/features/v3-4-aegean.js'),'utf8');for(const token of ["const V='6.9.1'",'AEGEAN_BRONZE','aegean-phases','openAegeanExamModule','assets/packs/aegean-pack.svg'])assert.match(runtime,new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
console.log('✓ v3.4 Aegean static smoke: 10 chapters, 60 missions, 120 cards');
