#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=async p=>JSON.parse(await fs.readFile(path.join(root,p),'utf8'));
const fail=m=>{throw new Error(m)};
const assert=(value,message)=>value||fail(message);

const manifest=await read('data/content-manifest.json');
const campaign=await read('data/campaigns/egypt-middle-new/campaign.json');
const story=await read('data/cards/egypt/middle-new-story.json');
const archive=await read('data/cards/egypt/middle-new-archive.json');
const lessons=await read('data/lessons/egypt-middle-new/campaign.json');
const quizzes=await read('data/quizzes/egypt-middle-new/campaign.json');
const pools=await read('data/campaigns/egypt-middle-new/pools.json');
const stories=await read('data/stories/egypt-middle-new/personal.json');
const map=await read('data/maps/egypt-middle-new.json');
const catalog=await read('data/world/campaigns.json');
const timeline=await read('data/world/timeline.json');
const babylon=await read('data/campaigns/babylon/campaign.json');
const imageQueries=await read('data/image_queries.json');
const js=await fs.readFile(path.join(root,'js/features/v3-2-egypt-middle-new.js'),'utf8');
const sw=await fs.readFile(path.join(root,'sw.js'),'utf8');

assert(manifest.version==='7.3.0','manifest version');
assert(manifest.datasets.campaigns.includes('data/campaigns/egypt-middle-new/campaign.json'),'campaign manifest');
assert(manifest.datasets.cards.includes('data/cards/egypt/middle-new-story.json'),'story manifest');
assert(manifest.datasets.cards.includes('data/cards/egypt/middle-new-archive.json'),'archive manifest');
assert(manifest.datasets.maps.EGYPT_MIDDLE_NEW==='data/maps/egypt-middle-new.json','map manifest');
assert(campaign.chapters.length===10,'chapters');
assert(campaign.nodes.length===60,'missions');
assert(story.length===80,'story cards');
assert(archive.length===40,'archive cards');
assert(Object.keys(lessons).length===60,'lessons');
assert(Object.keys(quizzes).length===14,'quizzes');
assert(Object.values(quizzes).flatMap(q=>q.questions||[]).length===80,'quiz questions');
assert(pools.pools.length===10,'pools');
assert(pools.pools.flatMap(p=>p.cardIds).length===40,'pool cards');
assert(Object.keys(stories).length===10,'personal stories');
assert(campaign.nodes.find(x=>x.id==='EMN_10_06')?.campaignExamModules?.length===4,'campaign exam modules');
assert(campaign.eraLayer.phases.length===3,'campaign phases');
assert(Object.keys(map.points||{}).length===28,'campaign map points');
assert(catalog.find(x=>x.id==='EGYPT_MIDDLE_NEW')?.status==='PLAYABLE','world catalog status');
assert(catalog.find(x=>x.id==='EGYPT_MIDDLE_NEW')?.releasedChapters===10,'released chapters');
assert(babylon.eraLayer.regions.find(x=>x.id==='EGYPT_BRONZE')?.status==='PLAYABLE','Bronze world Egypt status');
assert(babylon.eraLayer.parallelTimeline.length>=8,'expanded Bronze timeline');
assert(timeline.filter(x=>x.campaignId==='EGYPT_MIDDLE_NEW').length>=12,'world timeline events');
assert(imageQueries.cards.EMN_S_04_02.candidates[0].title==='Avaris','Avaris semantic image query');
assert(imageQueries.cards.EMN_S_07_01.candidates[0].title==='Hatshepsut','Hatshepsut semantic image query');
assert(imageQueries.cards.EMN_S_10_03.candidates[0].title==='Battle of Kadesh','Kadesh semantic image query');
assert(js.includes("V22_CAMPAIGN_CODES.EGYPT_MIDDLE_NEW='EGYPT_BRONZE'"),'campaign runtime code');
assert(js.includes('renderEgyptBronzeExam')||js.includes('egyptBronzeExam'),'exam UI');
assert(js.includes('assets/packs/egypt-bronze-pack.svg'),'campaign pack cover');
assert(sw.includes('js/features/v3-2-egypt-middle-new.js'),'service worker runtime cache');
assert(sw.includes('assets/packs/egypt-bronze-pack.svg'),'service worker pack cache');

for(const card of [...story,...archive]){
 assert(await fs.access(path.join(root,card.image.local)).then(()=>true).catch(()=>false),`missing image ${card.id}`);
}

console.log('✓ v3.2 Egypt Middle and New Kingdom smoke passed');
