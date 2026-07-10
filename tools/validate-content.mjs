#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
const root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const read=async p=>JSON.parse(await fs.readFile(path.join(root,p),'utf8'));
const errors=[]; const warnings=[];
const req=(condition,msg)=>(condition?null:errors.push(msg));
const manifest=await read('data/content-manifest.json');
const d=manifest.datasets;
const cardGroups=await Promise.all(d.cards.map(read)); const cards=cardGroups.flat();
const readBundle=async spec=>Array.isArray(spec)?Object.assign({},...(await Promise.all(spec.map(read)))):read(spec);
const [relations,campaign,pools,quizzes,stories,daily]=await Promise.all([read(d.relations),read(d.campaign),read(d.pools),readBundle(d.quizzes),read(d.stories),read(d.daily)]);
const ids=new Set();
for(const c of cards){
 req(c&&typeof c==='object',`Некорректная карточка: ${String(c)}`); if(!c)continue;
 req(c.id,`Карточка без id: ${c.title||'?'}`); req(!ids.has(c.id),`Дубликат card id: ${c.id}`); ids.add(c.id);
 for(const key of ['type','title','subtitle','era','region','date','rarity','summary','importance','facts','tags','stats','image','source']) req(c[key]!==undefined,`${c.id}: отсутствует ${key}`);
 req(Array.isArray(c.facts)&&c.facts.length>=3,`${c.id}: нужно минимум 3 факта`);
 req(c.image?.file&&c.image?.caption&&c.image?.credit&&c.image?.license,`${c.id}: неполные данные изображения`);
 req(c.source?.type==='wikipedia'&&c.source?.url,`${c.id}: отсутствует Wikipedia source`);
}
for(const r of relations){req(ids.has(r.source),`Связь ${r.id||'?'}: нет source ${r.source}`);req(ids.has(r.target),`Связь ${r.id||'?'}: нет target ${r.target}`);}
const missionIds=new Set(campaign.nodes.map(x=>x.id));
for(const m of campaign.nodes){
 for(const id of [...(m.cards||[]),...(m.unlockCards||[])]) req(ids.has(id),`Миссия ${m.id}: нет карты ${id}`);
 if(m.quiz) req(!!quizzes[m.quiz],`Миссия ${m.id}: нет квиза ${m.quiz}`);
}
for(const p of pools.pools){for(const id of p.cardIds)req(ids.has(id),`Пул ${p.id}: нет карты ${id}`);if(!p.unlockMission.startsWith('ROME_CHAPTER_'))req(missionIds.has(p.unlockMission),`Пул ${p.id}: нет миссии ${p.unlockMission}`);}
for(const [id,a] of Object.entries(pools.acquisition)){req(ids.has(id),`Acquisition ссылается на отсутствующую карту ${id}`);if(a.pool)req(pools.pools.some(p=>p.id===a.pool),`${id}: нет пула ${a.pool}`);}
for(const [id,s] of Object.entries(stories)){req(ids.has(s.cardId),`${id}: нет карты ${s.cardId}`);req(Array.isArray(s.steps)&&s.steps.length>0,`${id}: нет шагов`);}
const rarityCounts=Object.fromEntries(['RARE','EPIC','LEGENDARY','MYTHIC'].map(r=>[r,cards.filter(c=>c.rarity===r).length]));
req(rarityCounts.RARE>rarityCounts.EPIC&&rarityCounts.EPIC>rarityCounts.LEGENDARY&&rarityCounts.LEGENDARY>rarityCounts.MYTHIC,`Нарушена пирамида редкости: ${JSON.stringify(rarityCounts)}`);
req(Array.isArray(daily.interval_days)&&daily.interval_days.length>0,'Daily learning: отсутствуют интервалы');
req(daily.interval_days.every((x,i,a)=>Number.isInteger(x)&&x>0&&(i===0||x>a[i-1])),'Daily learning: интервалы должны быть положительными и возрастающими');
req(daily.session?.review_cards>0,'Daily learning: review_cards должен быть больше нуля');
req(daily.session?.pass_percent>=0&&daily.session?.pass_percent<=100,'Daily learning: некорректный pass_percent');
const referenced=new Set([...relations.flatMap(r=>[r.source,r.target]),...campaign.nodes.flatMap(m=>[...(m.cards||[]),...(m.unlockCards||[])]),...pools.pools.flatMap(p=>p.cardIds)]);
for(const c of cards)if(!referenced.has(c.id))warnings.push(`${c.id}: карточка не связана с кампанией, пулом или графом`);
console.log(`Codex Content Validator v${manifest.version}`);console.log(`Карточки: ${cards.length}; связи: ${relations.length}; миссии: ${campaign.nodes.length}; пулы: ${pools.pools.length}; личные истории: ${Object.keys(stories).length}; редкость R/E/L/M: ${rarityCounts.RARE}/${rarityCounts.EPIC}/${rarityCounts.LEGENDARY}/${rarityCounts.MYTHIC}; интервалы: ${daily.interval_days.join('→')} дней`);
if(warnings.length){console.log(`\nПредупреждения (${warnings.length}):`);warnings.forEach(x=>console.log('  - '+x));}
if(errors.length){console.error(`\nОшибки (${errors.length}):`);errors.forEach(x=>console.error('  - '+x));process.exit(1);}console.log('\n✓ Контент валиден');
