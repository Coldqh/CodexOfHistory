#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';

const root=path.resolve(new URL('..',import.meta.url).pathname);
const readText=rel=>fs.readFileSync(path.join(root,rel),'utf8');
const readJson=rel=>JSON.parse(readText(rel));
const manifest=readJson('data/content-manifest.json');
const css=readText('styles.css');

assert.equal(manifest.version,'8.2.0');
for(const token of [
  '--accent:var(--gold)',
  '--accent-2:var(--wine-bright)',
  '--panel:var(--surface-strong)',
  '--panel-2:',
  '--soft:var(--line)',
  '--success:var(--green)',
  '--display:'
]) assert.ok(css.includes(token),`missing CSS alias ${token}`);

assert.match(css,/\.compact-chapter-switch button\{[^}]*flex:0 0 188px[^}]*min-width:188px[^}]*max-width:188px/);
assert.match(css,/\.compact-chapter-switch button\{[^}]*flex-basis:158px[^}]*min-width:158px[^}]*max-width:158px/);
assert.match(css,/scroll-snap-type:x proximity/);
assert.match(css,/\.world-view-tabs button\.active\{background:var\(--accent\);color:#101010\}/);
assert.match(css,/\.pack-page-card\.locked/);
assert.match(css,/\.pack-page-card\.campaign-pack img\{object-fit:contain/);

const chapter=readText('js/features/v1-8-learning-missions.js');
assert.match(chapter,/scrollIntoView\(\{behavior:'smooth',block:'nearest',inline:'center'\}\)/);
assert.match(chapter,/data-chapter-id=/);

const packCore=readText('js/features/v1-5-polish.js');
for(const token of ['campaignPackStatusClass','campaignPackDescription','campaignPackMeta','campaignPackAction','Пак пока закрыт','Откроется после первой миссии']){
  assert.ok(packCore.includes(token),`missing pack state helper ${token}`);
}

const packFiles=[
  'js/features/v2-2-mesopotamia.js','js/features/v2-4-egypt.js','js/features/v2-7-parallel-civilizations.js',
  'js/features/v2-8-indus.js','js/features/v2-9-china.js','js/features/v3-0-dawn-world.js',
  'js/features/v3-1-babylon.js','js/features/v3-2-egypt-middle-new.js','js/features/v3-3-hittites.js',
  'js/features/v3-4-aegean.js','js/features/v3-5-international.js'
];
for(const rel of packFiles){
  const source=readText(rel);
  assert.match(source,/campaignPackStatusClass\(\)/,`${rel}: missing locked class`);
  assert.match(source,/campaignPackDescription\(\)/,`${rel}: missing locked copy`);
  assert.match(source,/campaignPackMeta\(\)/,`${rel}: missing locked meta`);
  assert.match(source,/campaignPackAction\(\)/,`${rel}: missing locked action`);
}

for(const rel of ['assets/packs/egypt-bronze-pack.svg','assets/packs/hittites-pack.svg','assets/packs/aegean-pack.svg','assets/packs/international-bronze-pack.svg']){
  const svg=readText(rel);
  assert.match(svg,/viewBox="0 0 720 960"/,`${rel}: pack cover is not vertical`);
}

const refs=new Set([...css.matchAll(/var\(--([\w-]+)/g)].map(x=>x[1]));
const defs=new Set([...css.matchAll(/--([\w-]+)\s*:/g)].map(x=>x[1]));
const runtimeVars=new Set(['delay','hx','hy','r','row','tier','x','y']);
const unexpected=[...refs].filter(x=>!defs.has(x)&&!runtimeVars.has(x));
assert.deepEqual(unexpected,[],`undefined CSS variables: ${unexpected.join(', ')}`);

console.log('✓ v8.2.0 mobile chapter strip, world tabs, vertical packs and locked pack state');
