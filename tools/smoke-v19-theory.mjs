#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const manifest=read('data/content-manifest.json'),d=manifest.datasets;
const bundle=spec=>Array.isArray(spec)?Object.assign({},...spec.map(read)):read(spec);
const cards=d.cards.flatMap(read),relations=read(d.relations),campaign=read(d.campaign),pools=read(d.pools),quizzes=bundle(d.quizzes),stories=read(d.stories),lessons=bundle(d.lessons);
const app={innerHTML:''},local=new Map();
const document={documentElement:{dataset:{},style:{setProperty(){}},classList:{add(){},remove(){}}},querySelector(){return null},querySelectorAll(){return[]},getElementById(id){return id==='app'?app:null},addEventListener(){},createElement(){return{className:'',style:{setProperty(){}},remove(){},classList:{add(){}},innerHTML:''}},body:{appendChild(){},classList:{add(){},remove(){},toggle(){}}}};
const context={console,Date,Math,JSON,Intl,Map,Set,URL,Blob,Promise,CustomEvent:class{},localStorage:{getItem:k=>local.get(k)||null,setItem:(k,v)=>local.set(k,v),removeItem:k=>local.delete(k)},sessionStorage:{getItem(){return null},setItem(){},removeItem(){}},confirm:()=>true,setTimeout:fn=>{if(typeof fn==='function')fn();return 0},clearTimeout(){},requestAnimationFrame(){},window:{scrollTo(){},dispatchEvent(){},matchMedia:()=>({matches:true}),innerWidth:1200},document,location:{protocol:'http:',href:'https://example.test/',replace(){},reload(){}},IntersectionObserver:class{},L:undefined,navigator:{}};
context.window.window=context.window;context.window.document=document;context.globalThis=context;
Object.assign(context,{CODEX_MANIFEST:manifest,CODEX_CONFIG:{mastery:read(d.mastery),packs:read(d.packs),collection:read(d.collection),maps:read(d.maps),daily:read(d.daily)},CARDS:cards,RELATIONS:relations,CAMPAIGN:campaign,V09_CONTENT:pools,QUIZZES:quizzes,PERSONAL_STORIES:stories,CODEX_LESSONS:lessons});
context.CODEX_REGISTRY={cardsById:new Map(cards.map(x=>[x.id,x])),relationsByCard:new Map(cards.map(c=>[c.id,relations.filter(r=>r.source===c.id||r.target===c.id)])),missionsById:new Map(campaign.nodes.map(x=>[x.id,x])),poolsById:new Map(pools.pools.map(x=>[x.id,x])),lessonsByMission:new Map(Object.entries(lessons))};
const ctx=vm.createContext(context);for(const script of manifest.scripts)vm.runInContext(fs.readFileSync(path.join(root,script),'utf8'),ctx,{filename:script});
const assert=(v,m)=>{if(!v)throw new Error(m)};
assert(manifest.version==='2.0.0','Версия не 2.0.0');
assert(Object.keys(lessons).length===campaign.nodes.length,'Каждая миссия должна иметь теорию');
for(const [id,l] of Object.entries(lessons)){
  assert(l.theory,`${id}: нет theory`);
  assert(l.theory.paragraphs.length>=5,`${id}: мало абзацев`);
  assert(l.theory.paragraphs.join(' ').split(/\s+/).length>=280,`${id}: теория слишком короткая`);
  assert(l.theory.sources.length>=1,`${id}: нет источников`);
  assert(l.theory.historicityNotes.length>=2,`${id}: нет оговорок`);
}
vm.runInContext("state.currentMission='MIS_REPUBLIC_03';state.lessonUnlockedStages['MIS_REPUBLIC_03']=4;state.lessonStages['MIS_REPUBLIC_03']=3;state.tab='mission';render();",ctx);
assert(app.innerHTML.includes('ПОЛНОЕ ЧТЕНИЕ'),'Нет режима полного чтения');
assert(app.innerHTML.includes('Формирование республиканской власти'),'Не отрисован заголовок теории');
assert(app.innerHTML.includes('Исторические оговорки'),'Нет блока исторических оговорок');
assert(app.innerHTML.includes('Материалы и дальнейшее чтение'),'Нет блока источников');
assert(app.innerHTML.includes('data-theory-scroll="MIS_REPUBLIC_03"'),'Нет reader scroll');
assert(app.innerHTML.includes('К практике'),'Нет перехода к практике');
vm.runInContext("state.lessonStages['MIS_REPUBLIC_03']=4;render();",ctx);
assert(app.innerHTML.includes('ЭТАП 5'),'Практика не стала пятым этапом');
console.log(`✓ v1.9 theory smoke: ${Object.keys(lessons).length} theories`);
