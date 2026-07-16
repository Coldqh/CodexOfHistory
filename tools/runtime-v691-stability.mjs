import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const root=process.cwd();
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const manifest=JSON.parse(read('data/content-manifest.json'));
assert.equal(manifest.version,'8.0.0');
assert(manifest.scripts.includes('js/features/v6-9-1-stability.js'));
assert(manifest.scripts.indexOf('js/features/v6-9-1-stability.js')<manifest.scripts.indexOf('js/core/start.js'));
assert(fs.existsSync(path.join(root,'assets/packs/rome-pack.svg')));
const sw=read('sw.js');
for(const name of fs.readdirSync(path.join(root,'assets/packs')).filter(x=>x.endsWith('.svg'))){assert(sw.includes(`./assets/packs/${name}`),`pack not precached: ${name}`);}
const mobile=read('js/features/mobile-cleanup.js');
assert(mobile.includes('collectionWindow(list)'));
assert(mobile.includes('windowed.visible.map(catalogCard)'));
assert(!mobile.includes("list.map(catalogCard).join('')"));
const catalog=read('js/features/catalog.js');
assert(catalog.includes('const COLLECTION_BATCH_SIZE=48'));
assert(catalog.includes('state.collectionLimit=COLLECTION_BATCH_SIZE'));
assert(catalog.includes("if(tab==='collection'&&state.tab!=='collection')resetCollectionLimit()"));
assert(catalog.includes('function loadMoreCollection()'));

class StorageMock{
  constructor(entries={}){this.map=new Map(Object.entries(entries));}
  get length(){return this.map.size;} key(i){return [...this.map.keys()][i]??null;}
  getItem(k){return this.map.has(k)?this.map.get(k):null;} setItem(k,v){this.map.set(k,String(v));}
  removeItem(k){this.map.delete(k);}
}
const weak=JSON.stringify({xp:0,unlocked:[],missionsCompleted:[],quizResults:{}});
const rich=JSON.stringify({xp:1350,unlocked:['A','B'],missionsCompleted:['M1','M2'],quizResults:{Q1:{passed:true}},theme:'parchment'});
const storage=new StorageMock({codex_history_v02_ru:weak,codex_history_v01_ru:rich});
const context={
  STORE:'codex_history_v02_ru',localStorage:storage,
  state:{xp:0,unlocked:[],missionsCompleted:[],quizResults:{},theme:'night'},
  window:{CODEX_VERSION:'',addEventListener(){}},document:{addEventListener(){},visibilityState:'visible'},
  console,Date,JSON,Number,Math,Set,Object,Array
};
vm.createContext(context);vm.runInContext(read('js/features/v6-9-1-stability.js'),context);
assert.equal(context.state.xp,1350);
assert.deepEqual([...context.state.missionsCompleted],['M1','M2']);
assert(storage.getItem('codex_history_save_backup_v1'));
const saved=JSON.parse(storage.getItem('codex_history_v02_ru'));
assert.equal(saved._saveMeta.appVersion,'8.0.0');
console.log('v8.0.0 stability hotfix runtime: OK');
