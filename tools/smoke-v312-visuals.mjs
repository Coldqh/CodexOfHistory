#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';
const root=path.resolve(new URL('..',import.meta.url).pathname);const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const manifest=read('data/content-manifest.json'),cards=manifest.datasets.cards.flatMap(read),queries=read(manifest.datasets.imageQueries),images=read('data/image_manifest.json');
assert.equal(manifest.version,'3.1.2');assert.equal(queries.version,manifest.version);assert.equal(queries.count,cards.length);assert.equal(Object.keys(queries.cards).length,cards.length);
const staticHistorical=cards.filter(c=>c.image?.prefer_remote),dynamic=cards.filter(c=>!c.image?.prefer_remote);assert.equal(staticHistorical.length,42);assert.equal(dynamic.length,857);assert.equal(images.dynamicQueryCount,dynamic.length);
for(const c of cards){const q=queries.cards[c.id];assert.ok(q,`${c.id}: missing query`);assert.ok(q.candidates.length>=4,`${c.id}: too few candidates`);assert.ok(q.candidates.some(x=>x.title===c.title),`${c.id}: exact title absent`);for(const x of q.candidates){assert.ok(['ru','en'].includes(x.lang));assert.ok(x.title.trim());}}
for(const c of cards){assert.ok(c.image?.local);assert.ok(fs.existsSync(path.join(root,c.image.local)),`${c.id}: missing local fallback`);}
const lastFallbackUsage=new Map();for(const q of Object.values(queries.cards)){const title=q.candidates.at(-1).title;lastFallbackUsage.set(title,(lastFallbackUsage.get(title)||0)+1);}assert.ok(Math.max(...lastFallbackUsage.values())<=15,'fallback pool is too repetitive');
const module=fs.readFileSync(path.join(root,'js/features/v3-1-2-visual-archive.js'),'utf8');for(const token of ['pageimages','extmetadata','MAX_REUSE=9','data-card-image','refreshHistoricalImages','clearHistoricalImageCache'])assert.ok(module.includes(token),`missing ${token}`);
const sw=fs.readFileSync(path.join(root,'sw.js'),'utf8');assert.match(sw,/ru\.wikipedia\.org/);assert.match(sw,/commons\.wikimedia\.org/);assert.match(sw,/data\/image_queries\.json/);
console.log(`✓ v3.1.2 visual catalog: ${cards.length} profiles, ${staticHistorical.length} fixed images, ${dynamic.length} dynamic cards`);
