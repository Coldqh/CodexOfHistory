#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const m=read('data/content-manifest.json'),cards=m.datasets.cards.flatMap(read),packs=read(m.datasets.packs),pools=read(m.datasets.pools);
const assert=(v,x)=>{if(!v)throw new Error(x)};const order=['COMMON','UNCOMMON','RARE','EPIC','LEGENDARY','MYTHIC'];const c=Object.fromEntries(order.map(r=>[r,cards.filter(x=>x.rarity===r).length]));
assert(m.version==='2.1.1','version');assert(cards.length===200,`cards ${cards.length}`);for(let i=1;i<order.length;i++)assert(c[order[i-1]]>c[order[i]],`pyramid ${JSON.stringify(c)}`);
assert(c.COMMON===80&&c.UNCOMMON===55&&c.RARE===36&&c.EPIC===19&&c.LEGENDARY===8&&c.MYTHIC===2,`unexpected counts ${JSON.stringify(c)}`);
assert(Object.keys(packs.rarityWeights).length===6,'pack weights');assert(pools.pools.flatMap(p=>p.cardIds).filter(id=>id.startsWith('LOC_LOW_')||id.startsWith('TERM_LOW_')).length>20,'new pool cards');
for(const card of cards.filter(x=>x.id.includes('_LOW_')))assert(card.image.local&&fs.existsSync(path.join(root,card.image.local)),`${card.id} asset`);
console.log(`✓ v2.1.1 rarity smoke: ${cards.length} cards · ${order.map(r=>c[r]).join('/')}`);
