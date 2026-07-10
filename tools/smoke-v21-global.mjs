#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';
const root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const manifest=read('data/content-manifest.json');assert.equal(manifest.version,'2.1.1');
const eras=read(manifest.datasets.eras),campaigns=read(manifest.datasets.campaignCatalog),timeline=read(manifest.datasets.worldTimeline);
assert.equal(eras.length,7);assert.equal(campaigns.length,30);assert(timeline.length>=25);
assert(campaigns.some(c=>c.id==='ROME_CAMPAIGN'&&c.status==='PLAYABLE'&&c.releasedChapters===3));
assert(campaigns.some(c=>c.id==='MESOPOTAMIA_DAWN'&&c.status==='NEXT'&&c.chapterCount===10));
const ids=new Set(campaigns.map(c=>c.id));for(const e of eras)for(const id of e.campaignIds)assert(ids.has(id));
const feature=fs.readFileSync(path.join(root,'js/features/v2-1-global-era.js'),'utf8');
for(const token of ['worldScreen','global-timeline','MESOPOTAMIA_DAWN','ROME_CAMPAIGN','startWorldCampaign'])assert(feature.includes(token));
console.log(`✓ v2.1 global era smoke: ${eras.length} eras, ${campaigns.length} campaigns, ${timeline.length} milestones`);
