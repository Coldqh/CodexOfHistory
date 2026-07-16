#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const manifest=read('data/content-manifest.json'),d=manifest.datasets;
assert.equal(manifest.version,'8.4.0');
const story=read('data/cards/classical-world/story.json'),archive=read('data/cards/classical-world/archive.json');
const cards=[...story,...archive],campaign=read('data/campaigns/classical-world/campaign.json'),pools=read('data/campaigns/classical-world/pools.json'),lessons=read('data/lessons/classical-world/campaign.json'),quizzes=read('data/quizzes/classical-world/campaign.json'),stories=read('data/stories/classical-world/personal.json'),map=read('data/maps/classical-world-exam.json'),relations=read('data/core/relations-v53-classical-world.json');
assert.equal(story.length,72);assert.equal(archive.length,24);assert.equal(cards.length,96);assert.equal(campaign.id,'CLASSICAL_ERA_EXAM');assert.equal(campaign.chapters.length,8);assert.equal(campaign.nodes.length,48);assert.equal(Object.keys(lessons).length,48);assert.equal(Object.keys(quizzes).length,14);assert.equal(pools.pools.length,8);assert.equal(Object.keys(stories).length,8);assert.equal(relations.length,99);assert.equal(campaign.nodes.at(-1).examModules.length,6);assert.equal(campaign.eraLayer.regions.length,3);assert.equal(campaign.eraLayer.parallelTimeline.length,7);assert.equal(Object.keys(map.cardPoints).length,96);
const rarities=['COMMON','UNCOMMON','RARE','EPIC','LEGENDARY','MYTHIC'];const counts=Object.fromEntries(rarities.map(r=>[r,cards.filter(c=>c.rarity===r).length]));assert.deepEqual(counts,{COMMON:34,UNCOMMON:28,RARE:18,EPIC:10,LEGENDARY:5,MYTHIC:1});
for(const c of cards){assert.ok(c.image?.local&&fs.existsSync(path.join(root,c.image.local)),`${c.id}: image`);assert.equal(c.campaign,'CLASSICAL_WORLD');}
const oldCards=d.cards.filter(p=>!p.includes('/classical-world/')).flatMap(read);const oldTitles=new Set(oldCards.map(c=>c.title));for(const c of cards)assert.ok(!oldTitles.has(c.title),`${c.id}: duplicate title ${c.title}`);
assert.ok(d.cards.includes('data/cards/classical-world/story.json'));assert.ok(d.campaigns.includes('data/campaigns/classical-world/campaign.json'));assert.equal(d.maps.CLASSICAL_ERA_EXAM,'data/maps/classical-world-exam.json');assert.ok(manifest.scripts.includes('js/features/v5-3-classical-world.js'));
const eras=read(d.eras),world=read(d.campaignCatalog);assert.ok(eras.find(e=>e.id==='ERA_CLASSICAL').campaignIds.includes('CLASSICAL_ERA_EXAM'));assert.ok(world.some(c=>c.id==='CLASSICAL_ERA_EXAM'&&c.status==='PLAYABLE'));
const allRelations=read(d.relations);for(const r of relations)assert.ok(allRelations.some(x=>x.id===r.id),`${r.id}: missing aggregate relation`);
console.log('✓ v5.3 classical world: 96 cards, 48 missions, shared map and six-part exam');
