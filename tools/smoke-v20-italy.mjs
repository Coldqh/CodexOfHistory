#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const manifest=read('data/content-manifest.json'),d=manifest.datasets;
const cards=d.cards.flatMap(read),campaign=read(d.campaign),pools=read(d.pools),maps=read(d.maps);
const lessons=Object.assign({},...d.lessons.map(read)),quizzes=Object.assign({},...d.quizzes.map(read));
const assert=(v,m)=>{if(!v)throw new Error(m)};
assert(manifest.version==='2.1.1','version');
assert(cards.length>=130,`Ожидалось 130 карт, получено ${cards.length}`);
const counts=Object.fromEntries(['COMMON','UNCOMMON','RARE','EPIC','LEGENDARY','MYTHIC'].map(r=>[r,cards.filter(c=>c.rarity===r).length]));
assert(counts.COMMON>counts.UNCOMMON&&counts.UNCOMMON>counts.RARE&&counts.RARE>counts.EPIC&&counts.EPIC>counts.LEGENDARY&&counts.LEGENDARY>counts.MYTHIC,'rarity pyramid');
const ch=campaign.chapters.find(x=>x.id==='ROME_CHAPTER_03');assert(ch&&ch.missionIds.length===12,'chapter III');
for(const id of ch.missionIds){assert(lessons[id],`${id}: lesson`);assert(lessons[id].theory.paragraphs.join(' ').split(/\s+/).length>=280,`${id}: theory`)}
assert(quizzes.QUIZ_ITALY_FINAL?.questions.length>=8,'final quiz');
for(const id of ['VEII','ALLIA','CAPUA','TRIFANUM','SAMNIUM','CAUDIUM','SENTINUM','TARENTUM','HERACLEA','BENEVENTUM'])assert(maps.points[id],`map ${id}`);
for(const c of cards.filter(x=>x.chapter==='ROME_CHAPTER_03')){assert(c.image.local,`${c.id}: local image`);assert(fs.existsSync(path.join(root,c.image.local)),`${c.id}: missing asset`)}
for(const id of ['ROME_ITALY_BORDERLANDS','ROME_LATIN_ORDER','ROME_SAMNIUM','ROME_ROADS_COLONIES','ROME_SOUTH_ITALY'])assert(pools.pools.some(p=>p.id===id),`pool ${id}`);
const css=fs.readFileSync(path.join(root,'styles.css'),'utf8');assert(css.includes('.home-stats .stat-box.stat-action > b'),'home pack status CSS');
console.log(`✓ v2.1 compatibility smoke: ${cards.length} cards, rarity ${counts.RARE}/${counts.EPIC}/${counts.LEGENDARY}/${counts.MYTHIC}, 12 missions`);
