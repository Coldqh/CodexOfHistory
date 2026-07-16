#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';

const root=path.resolve(new URL('..',import.meta.url).pathname);
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const manifest=read('data/content-manifest.json');
const cards=manifest.datasets.cards.flatMap(read);
const queries=read(manifest.datasets.imageQueries);
const images=read('data/image_manifest.json');

assert.equal(manifest.version,'7.3.0');
assert.equal(queries.version,manifest.version);
assert.equal(queries.count,cards.length);
assert.equal(Object.keys(queries.cards).length,cards.length);

const staticHistorical=cards.filter(c=>c.image?.prefer_remote);
const dynamic=cards.filter(c=>!c.image?.prefer_remote);
assert.equal(staticHistorical.length,42);
assert.equal(dynamic.length,cards.length-staticHistorical.length);
assert.equal(images.dynamicQueryCount,dynamic.length);

for(const c of cards){
  const q=queries.cards[c.id];
  assert.ok(q,`${c.id}: missing query`);
  assert.ok(q.semantic,`${c.id}: missing semantic profile`);
  assert.ok(Array.isArray(q.semantic.group_terms)&&q.semantic.group_terms.length>=4,`${c.id}: missing group terms`);
  assert.ok(Array.isArray(q.semantic.forbidden),`${c.id}: missing forbidden list`);
  assert.ok(Array.isArray(q.candidates)&&q.candidates.length>=2&&q.candidates.length<=6,`${c.id}: candidate count`);
  assert.ok(q.candidates.some(x=>x.scope==='exact'),`${c.id}: exact candidate absent`);
  assert.ok(q.candidates.some(x=>x.scope==='context'),`${c.id}: context candidate absent`);
  for(const x of q.candidates){
    assert.ok(['ru','en'].includes(x.lang),`${c.id}: bad language`);
    assert.ok(['exact','context'].includes(x.scope),`${c.id}: bad scope`);
    assert.ok(x.title.trim(),`${c.id}: blank title`);
    assert.notEqual(x.scope,'random',`${c.id}: random fallback returned`);
  }
  assert.ok(c.image?.local&&fs.existsSync(path.join(root,c.image.local)),`${c.id}: missing local fallback`);
}

const risky={
  REG_MES_002:'Тигр (река)',
  CITY_LOW_005:'Cosa',
  PER_EGY_002:'Ka (pharaoh)',
  BAB_S_03_02:'Мари (древний город)',
  CITY_MES_008:'Киш (город)',
  CITY_CIV_003:'Мемфис (Египет)',
  RIV_INDA_001:'Ravi River',
  PER_CHN_006:'King Wu of Zhou',
};
for(const [id,title] of Object.entries(risky)){
  assert.equal(queries.cards[id].candidates[0].title,title,`${id}: disambiguation must be first`);
  assert.equal(queries.cards[id].candidates[0].trusted,true,`${id}: disambiguation must be trusted`);
}
assert.notEqual(queries.cards.REG_MES_002.candidates[0].title,'Тигр');
assert.notEqual(queries.cards.CITY_LOW_005.candidates[0].title,'Коза');

const module=fs.readFileSync(path.join(root,'js/features/v3-1-3-visual-semantics.js'),'utf8');
for(const token of ['pageterms','extracts','categories','semanticDecision','wrong-history-context','forbidden-context','MAX_CONTEXT_REUSE=8','codex_history_visual_archive_session_v322','sessionStorage']){
  assert.ok(module.includes(token),`missing ${token}`);
}
const manifestText=fs.readFileSync(path.join(root,'data/content-manifest.json'),'utf8');
assert.match(manifestText,/v3-1-3-visual-semantics\.js/);
assert.doesNotMatch(manifestText,/v3-1-2-visual-archive\.js/);
const sw=fs.readFileSync(path.join(root,'sw.js'),'utf8');
assert.match(sw,/codex-v7\.3\.0/);
assert.match(sw,/v3-1-3-visual-semantics\.js/);

console.log(`✓ v7.3.0 semantic visual catalog: ${cards.length} profiles, ${staticHistorical.length} fixed, ${dynamic.length} validated dynamically`);
