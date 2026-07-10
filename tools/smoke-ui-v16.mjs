import fs from 'node:fs';
const root=new URL('../',import.meta.url);
const read=p=>fs.readFileSync(new URL(p,root),'utf8');
const helpers=read('js/core/helpers.js');
const pools=read('js/features/pools-stories.js');
const polish=read('js/features/v1-5-polish.js');
const map=read('js/maps/engine.js');
const bootstrap=read('js/bootstrap.js');
const css=read('styles.css');
const checks=[
 ['thumbnail images',helpers.includes('Special:Redirect/file/')&&helpers.includes('?width=900')],
 ['service worker',bootstrap.includes("serviceWorker.register('sw.js?v=1.6.0")&&fs.existsSync(new URL('sw.js',root))],
 ['home campaign block removed',!pools.includes('Активная кампания · Рим</div><h3>${pools.length')],
 ['map focus function',map.includes('function focusAtlasCard(id)')&&polish.includes("focusAtlasCard('${c.id}')")],
 ['compact fragments',css.includes('v1.6 — compact fragment counter')],
];
for(const [name,ok] of checks){if(!ok)throw new Error(`FAIL: ${name}`);console.log(`✓ ${name}`)}
