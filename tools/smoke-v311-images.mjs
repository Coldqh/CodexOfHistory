#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';
const root=path.resolve(new URL('..',import.meta.url).pathname);const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const manifest=read('data/content-manifest.json');const cards=manifest.datasets.cards.flatMap(p=>read(p));
const historical=cards.filter(c=>c.image?.prefer_remote),covers=cards.filter(c=>!c.image?.prefer_remote);
assert.equal(historical.length,42);assert.equal(covers.length,857);
for(const c of cards){assert.ok(c.image?.local,`${c.id}: no fallback`);assert.ok(fs.existsSync(path.join(root,c.image.local)),`${c.id}: missing fallback`);assert.ok(['historical-image','project-cover'].includes(c.image.kind),`${c.id}: bad kind`);}
for(const c of historical){assert.match(c.image.source_url,/^https:\/\/commons\.wikimedia\.org\/wiki\/File:/);assert.ok(c.image.file);}
const helper=fs.readFileSync(path.join(root,'js/core/helpers.js'),'utf8');assert.match(helper,/image\.prefer_remote&&image\.file/);assert.match(helper,/data-fallback/);assert.match(helper,/fallbackCardImage/);
console.log(`✓ v3.1.1 images: ${historical.length} historical, ${covers.length} project covers with local fallback`);
