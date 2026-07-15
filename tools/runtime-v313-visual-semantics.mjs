#!/usr/bin/env node
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

const code=fs.readFileSync(new URL('../js/features/v3-1-3-visual-semantics.js',import.meta.url),'utf8');
const river={id:'REG_MES_002',title:'Тигр',type:'RIVER',image:{local:'assets/tigris.svg',caption:'fallback',credit:'Codex',license:'Project asset',focus:'50% 50%'}};
const city={id:'CITY_LOW_005',title:'Коза',type:'CITY',image:{local:'assets/cosa.svg',caption:'fallback',credit:'Codex',license:'Project asset',focus:'50% 50%'}};
const fixed={id:'FIXED',title:'Рим',type:'CITY',image:{local:'assets/fixed.svg',prefer_remote:true,file:'Fixed.jpg',source_url:'https://commons.wikimedia.org/wiki/File:Fixed.jpg',caption:'fixed',credit:'Author',license:'PD'}};
const cards=[river,city,fixed],byId=new Map(cards.map(c=>[c.id,c]));
const queryPayload={version:'5.1.0',count:3,cards:{
  REG_MES_002:{type:'RIVER',semantic:{subject_terms:['тигр'],group_terms:['месопот','iraq'],required_any:['река','river'],forbidden:['животн','млекопита','animal','mammal','танк','tank'],strict_context:true},candidates:[{lang:'ru',title:'Тигр',scope:'exact',min_score:5},{lang:'ru',title:'Тигр (река)',scope:'exact',trusted:true,min_score:2},{lang:'ru',title:'Месопотамия',scope:'context',trusted:true,min_score:2}]},
  CITY_LOW_005:{type:'CITY',semantic:{subject_terms:['коза'],group_terms:['рим','roman','italy'],required_any:['город','city','ancient'],forbidden:['животн','species','mammal'],strict_context:true},candidates:[{lang:'ru',title:'Коза',scope:'exact',min_score:5},{lang:'en',title:'Cosa',scope:'exact',trusted:true,min_score:2},{lang:'en',title:'Ancient Rome',scope:'context',trusted:true,min_score:2}]},
  FIXED:{type:'CITY',semantic:{subject_terms:['рим'],group_terms:['рим'],required_any:['город'],forbidden:[],strict_context:true},candidates:[{lang:'ru',title:'Рим',scope:'exact'}]}
}};

const pages={
  ru:{
    'Тигр':{title:'Тигр',extract:'Тигр — вид хищных млекопитающих семейства кошачьих.',terms:{description:['вид млекопитающих']},categories:[{title:'Категория:Кошачьи'}],pageimage:'Tiger.jpg',thumbnail:{source:'https://upload.wikimedia.org/tiger.jpg'}},
    'Тигр (река)':{title:'Тигр (река)',extract:'Тигр — крупная река Месопотамии, протекающая через Ирак.',terms:{description:['река в Турции и Ираке']},categories:[{title:'Категория:Реки Ирака'}],pageimage:'TigrisRiver.jpg',thumbnail:{source:'https://upload.wikimedia.org/tigris.jpg'}},
    'Коза':{title:'Коза',extract:'Домашняя коза — животное и вид млекопитающих.',terms:{description:['домашнее животное']},categories:[{title:'Категория:Козы'}],pageimage:'Goat.jpg',thumbnail:{source:'https://upload.wikimedia.org/goat.jpg'}},
    'Месопотамия':{title:'Месопотамия',extract:'Исторический регион древнего мира.',terms:{description:['исторический регион']},categories:[],pageimage:'Mesopotamia.jpg',thumbnail:{source:'https://upload.wikimedia.org/meso.jpg'}},
  },
  en:{
    'Cosa':{title:'Cosa',extract:'Cosa was an ancient Roman colony and city in Italy.',terms:{description:['ancient Roman colony']},categories:[{title:'Category:Roman towns and cities in Italy'}],pageimage:'CosaRuins.jpg',thumbnail:{source:'https://upload.wikimedia.org/cosa.jpg'}},
    'Ancient Rome':{title:'Ancient Rome',extract:'Ancient Roman civilization in Italy.',terms:{description:['Roman civilization']},categories:[],pageimage:'Rome.jpg',thumbnail:{source:'https://upload.wikimedia.org/rome.jpg'}},
  }
};

const localStore=new Map();
const sessionStore=new Map();
let renders=0;
const fakeFetch=async input=>{
  const u=new URL(String(input));
  if(u.pathname.endsWith('/data/image_queries.json'))return{ok:true,json:async()=>queryPayload};
  if(u.hostname==='ru.wikipedia.org'||u.hostname==='en.wikipedia.org'){
    const lang=u.hostname.startsWith('ru.')?'ru':'en';
    const titles=(u.searchParams.get('titles')||'').split('|');
    return{ok:true,json:async()=>({query:{pages:titles.map(title=>pages[lang][title]||{title,missing:true})}})};
  }
  if(u.hostname==='commons.wikimedia.org'){
    const titles=(u.searchParams.get('titles')||'').split('|').map(x=>x.replace(/^File:/,''));
    return{ok:true,json:async()=>({query:{pages:titles.map(file=>({title:`File:${file}`,imageinfo:[{thumburl:`https://upload.wikimedia.org/thumb/${file}`,descriptionurl:`https://commons.wikimedia.org/wiki/File:${file}`,extmetadata:{Artist:{value:'Test Museum'},LicenseShortName:{value:'CC BY 4.0'},ImageDescription:{value:`Historical ${file}`}}}]}))}})};
  }
  throw new Error(`unexpected fetch ${u.href}`);
};

const app={querySelectorAll(){return[];}};
const context={
  console,URL,Date,Intl,Promise,Map,Set,JSON,Math,CARDS:cards,
  CODEX_MANIFEST:{version:'5.1.0',datasets:{imageQueries:'data/image_queries.json'}},
  localStorage:{getItem:k=>localStore.get(k)||null,setItem:(k,v)=>localStore.set(k,v),removeItem:k=>localStore.delete(k)},
  sessionStorage:{getItem:k=>sessionStore.get(k)||null,setItem:(k,v)=>sessionStore.set(k,v),removeItem:k=>sessionStore.delete(k)},
  location:{href:'https://example.test/'},
  navigator:{onLine:true,connection:{saveData:true}},
  fetch:fakeFetch,
  document:{getElementById:id=>id==='app'?app:null,querySelectorAll(){return[]}},
  requestAnimationFrame:fn=>fn(),
  setTimeout:fn=>{fn();return 0;},
  confirm:()=>true,
  showToast(){},
  render(){renders++;},
  settingsScreen(){return'<div><section class="settings-grid">BASE</section></div>';},
  card:id=>byId.get(id),
  imgUrl:file=>`https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(file)}?width=900`,
  filePage:file=>`https://commons.wikimedia.org/wiki/File:${file}`,
  esc:s=>String(s),
  cardImageSource(){},cardImageFallback(){},cardImageSourcePage(){},fallbackCardImage(){},imgTag(){},
  CustomEvent:class{constructor(type,init){this.type=type;this.detail=init?.detail}},
  addEventListener(){},dispatchEvent(){}
};
context.window=context;vm.createContext(context);vm.runInContext(code,context);
await vm.runInContext('resolveHistoricalImages()',context);

const status=vm.runInContext('visualArchiveStatus()',context);
assert.equal(status.resolved,3);
assert.equal(status.failed,0);
assert.ok(status.rejectedCandidates>=2,'animal matches must be rejected');
assert.match(vm.runInContext("cardImageSource(CARDS[0])",context),/TigrisRiver\.jpg/);
assert.match(vm.runInContext("cardImageSource(CARDS[1])",context),/CosaRuins\.jpg/);
assert.doesNotMatch(vm.runInContext("cardImageSource(CARDS[0])",context),/Tiger\.jpg/);
assert.doesNotMatch(vm.runInContext("cardImageSource(CARDS[1])",context),/Goat\.jpg/);
assert.equal(vm.runInContext("cardImageCredit(CARDS[0])",context),'Test Museum');
assert.match(vm.runInContext('settingsScreen()',context),/отклонено/);
assert.ok(sessionStore.has('codex_history_visual_archive_session_v322'));
assert.ok(!localStore.has('codex_history_visual_archive_session_v322'));
console.log('✓ v5.1.0 keeps validated visuals only in session storage and rejects tiger/goat pages');
