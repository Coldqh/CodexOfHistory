/* Codex of History v3.1.2 — historical image resolver and browser cache · Wikipedia PageImages + Commons extmetadata */
(() => {
  const CACHE_KEY='codex_history_visual_archive_v312';
  const QUERY_PATH=CODEX_MANIFEST?.datasets?.imageQueries||'data/image_queries.json';
  const STATIC_COUNT=CARDS.filter(c=>c.image?.prefer_remote&&c.image?.file).length;
  const MAX_REUSE=9;
  const stateVisual={queries:null,records:{},running:false,resolved:0,failed:0,total:CARDS.length,lastRun:null,error:null};
  try{
    const saved=JSON.parse(localStorage.getItem(CACHE_KEY)||'{}');
    if(saved&&saved.version==='3.1.2'&&saved.records&&typeof saved.records==='object'){
      stateVisual.records=saved.records;stateVisual.lastRun=saved.lastRun||null;
    }
  }catch(error){console.warn('[Codex visuals] cache read failed',error);}

  const cleanHtml=value=>{
    if(!value)return'';
    const text=String(value).replace(/<br\s*\/?>/gi,' ').replace(/<[^>]+>/g,' ').replace(/&nbsp;/gi,' ').replace(/&amp;/gi,'&').replace(/&quot;/gi,'"').replace(/&#39;|&apos;/gi,"'").replace(/\s+/g,' ').trim();
    return text.length>220?`${text.slice(0,217)}…`:text;
  };
  const saveVisualCache=()=>{
    try{localStorage.setItem(CACHE_KEY,JSON.stringify({version:'3.1.2',lastRun:stateVisual.lastRun,records:stateVisual.records}));}
    catch(error){console.warn('[Codex visuals] cache write failed',error);}
  };
  const visualRecord=c=>stateVisual.records[c?.id]||null;
  const localFallback=c=>c?.image?.local||'assets/ui/fallback-card.svg';
  const staticRecord=c=>c?.image?.prefer_remote&&c.image.file?{
    url:imgUrl(c.image.file),source_url:c.image.source_url||filePage(c.image.file),caption:c.image.caption,credit:c.image.credit,license:c.image.license,file:c.image.file,kind:'static-historical'
  }:null;
  const effectiveRecord=c=>visualRecord(c)||staticRecord(c);
  const imageUsage=()=>{
    const usage=new Map();
    for(const rec of Object.values(stateVisual.records))if(rec?.file)usage.set(rec.file,(usage.get(rec.file)||0)+1);
    return usage;
  };
  const status=()=>{
    const dynamic=Object.keys(stateVisual.records).length;
    return {static:STATIC_COUNT,dynamic,total:CARDS.length,resolved:Math.min(CARDS.length,STATIC_COUNT+dynamic),running:stateVisual.running,failed:stateVisual.failed,lastRun:stateVisual.lastRun,error:stateVisual.error};
  };
  window.CODEX_VISUAL_ARCHIVE=stateVisual;
  window.visualArchiveStatus=status;

  cardImageSource=function(c){const rec=effectiveRecord(c);return rec?.url||localFallback(c);};
  cardImageFallback=function(c){return localFallback(c);};
  cardImageSourcePage=function(c){const rec=effectiveRecord(c);return rec?.source_url||c?.image?.source_url||filePage(c?.image?.file);};
  window.cardImageCaption=function(c){return effectiveRecord(c)?.caption||c?.image?.caption||`Изображение: ${c?.title||''}`;};
  window.cardImageCredit=function(c){return effectiveRecord(c)?.credit||c?.image?.credit||'Codex of History';};
  window.cardImageLicense=function(c){return effectiveRecord(c)?.license||c?.image?.license||'См. источник';};
  fallbackCardImage=function(el){
    const fallback=el.dataset.fallback||'assets/ui/fallback-card.svg';
    if(el.src.endsWith(fallback.replace(/^\.\//,''))){el.onerror=null;return;}
    el.dataset.visualFailed='true';el.src=fallback;el.onerror=()=>{el.onerror=null;el.src='assets/ui/fallback-card.svg';};
  };
  imgTag=function(c,cls=''){
    const source=cardImageSource(c),fallback=cardImageFallback(c),kind=effectiveRecord(c)?'historical':'fallback';
    return `<img class="${cls} codex-card-visual" src="${source}" data-card-image="${esc(c.id)}" data-visual-kind="${kind}" data-fallback="${fallback}" alt="${esc(c.title)}" loading="lazy" decoding="async" style="object-position:${c.image?.focus||'50% 50%'}" referrerpolicy="no-referrer" onerror="fallbackCardImage(this)">`;
  };

  function hydrateMountedImages(root=document){
    if(!root?.querySelectorAll)return;
    root.querySelectorAll('img[data-card-image]').forEach(el=>{
      const c=card(el.dataset.cardImage),rec=effectiveRecord(c);if(!c||!rec?.url)return;
      el.dataset.visualKind='historical';el.dataset.fallback=localFallback(c);
      if(el.src!==rec.url&&!el.src.endsWith(encodeURI(rec.url))){el.src=rec.url;}
    });
  }
  window.hydrateHistoricalImages=hydrateMountedImages;

  async function loadQueries(force=false){
    if(stateVisual.queries&&!force)return stateVisual.queries;
    if(typeof fetch!=='function')return null;
    const url=new URL(QUERY_PATH,location.href);url.searchParams.set('v',CODEX_MANIFEST?.version||'3.1.2');
    const response=await fetch(url.href,{cache:'no-store'});if(!response.ok)throw new Error(`image queries HTTP ${response.status}`);
    const payload=await response.json();if(payload.count!==CARDS.length)throw new Error(`image queries ${payload.count}/${CARDS.length}`);
    stateVisual.queries=payload.cards;return stateVisual.queries;
  }
  function chunkTitles(entries,max=28){
    const out=[];let cur=[],size=0;
    for(const entry of entries){const add=encodeURIComponent(entry.title).length+3;if(cur.length>=max||size+add>6500){out.push(cur);cur=[];size=0;}cur.push(entry);size+=add;}
    if(cur.length)out.push(cur);return out;
  }
  function aliasMap(query){
    const map=new Map();
    for(const x of query?.normalized||[])map.set(x.from,x.to);
    for(const x of query?.redirects||[])map.set(x.from,x.to);
    const resolve=title=>{let current=title;const seen=new Set();while(map.has(current)&&!seen.has(current)){seen.add(current);current=map.get(current);}return current;};
    return resolve;
  }
  async function wikipediaPages(lang,entries){
    const titles=[...new Set(entries.map(x=>x.title))];
    const api=new URL(`https://${lang}.wikipedia.org/w/api.php`);
    Object.entries({origin:'*',action:'query',format:'json',formatversion:'2',redirects:'1',prop:'pageimages|info',piprop:'thumbnail|name',pithumbsize:'900',inprop:'url',titles:titles.join('|')}).forEach(([k,v])=>api.searchParams.set(k,v));
    const response=await fetch(api.href,{cache:'force-cache'});if(!response.ok)throw new Error(`Wikipedia ${lang}: ${response.status}`);
    const payload=await response.json(),resolve=aliasMap(payload.query),pages=new Map((payload.query?.pages||[]).filter(p=>!p.missing).map(p=>[p.title,p]));
    return entries.map(entry=>({entry,page:pages.get(resolve(entry.title))||pages.get(entry.title)||null}));
  }
  async function commonsMetadata(results){
    const withImage=results.filter(x=>x.page?.pageimage&&x.page?.thumbnail?.source);if(!withImage.length)return new Map();
    const files=[...new Set(withImage.map(x=>x.page.pageimage))];
    const api=new URL('https://commons.wikimedia.org/w/api.php');
    Object.entries({origin:'*',action:'query',format:'json',formatversion:'2',redirects:'1',prop:'imageinfo',iiprop:'url|extmetadata',iiurlwidth:'900',titles:files.map(f=>`File:${f}`).join('|')}).forEach(([k,v])=>api.searchParams.set(k,v));
    try{
      const response=await fetch(api.href,{cache:'force-cache'});if(!response.ok)throw new Error(`Commons: ${response.status}`);
      const payload=await response.json(),map=new Map();
      for(const page of payload.query?.pages||[]){const info=page.imageinfo?.[0];if(!info)continue;const file=page.title.replace(/^File:/,'');map.set(file,{info,page});}
      return map;
    }catch(error){console.warn('[Codex visuals] Commons metadata fallback',error);return new Map();}
  }
  function buildRecord(cardEntry,page,common,candidateIndex){
    if(!page?.thumbnail?.source||!page.pageimage)return null;
    const meta=common?.info?.extmetadata||{};
    const artist=cleanHtml(meta.Artist?.value||meta.Credit?.value||'Wikimedia Commons');
    const license=cleanHtml(meta.LicenseShortName?.value||meta.UsageTerms?.value||'См. страницу файла');
    const description=cleanHtml(meta.ImageDescription?.value||'');
    const source=common?.info?.descriptionurl||`https://commons.wikimedia.org/wiki/File:${encodeURIComponent(page.pageimage.replaceAll(' ','_'))}`;
    return {
      url:common?.info?.thumburl||page.thumbnail.source,
      source_url:source,
      page_url:page.fullurl||'',
      caption:description||`${cardEntry.card.title}: изображение из Wikimedia Commons`,
      credit:artist||'Wikimedia Commons',
      license,
      file:page.pageimage,
      article_title:page.title,
      candidate_index:candidateIndex,
      resolvedAt:new Date().toISOString(),
      kind:'wikimedia-historical'
    };
  }
  function applyRecords(assignments){
    if(!assignments.length)return;
    for(const {id,record} of assignments)stateVisual.records[id]=record;
    stateVisual.resolved=Object.keys(stateVisual.records).length;saveVisualCache();hydrateMountedImages();
    try{window.dispatchEvent(new CustomEvent('codex:visual-progress',{detail:status()}));}catch{}
  }
  async function resolvePass(pending,index,usage){
    const entries=[];
    for(const id of pending){const q=stateVisual.queries?.[id],candidate=q?.candidates?.[index];if(candidate){const currentCard=card(id);entries.push({id,lang:candidate.lang||'ru',title:candidate.title,index,card:currentCard,exact:String(candidate.title).trim().toLocaleLowerCase('ru-RU')===String(currentCard?.title||'').trim().toLocaleLowerCase('ru-RU')});}}
    const resolvedIds=new Set();
    for(const lang of [...new Set(entries.map(x=>x.lang))]){
      const group=entries.filter(x=>x.lang===lang);
      for(const chunk of chunkTitles(group)){
        let results=[];try{results=await wikipediaPages(lang,chunk);}catch(error){stateVisual.error=error.message;console.warn('[Codex visuals]',error);continue;}
        const commons=await commonsMetadata(results);
        const assignments=[];
        for(const {entry,page} of results){if(!page?.pageimage||!page?.thumbnail?.source)continue;
          const uses=usage.get(page.pageimage)||0;
          if(!entry.exact&&uses>=MAX_REUSE)continue;
          const record=buildRecord(entry, page, commons.get(page.pageimage), entry.index);if(!record)continue;
          assignments.push({id:entry.id,record});resolvedIds.add(entry.id);usage.set(page.pageimage,uses+1);
        }
        applyRecords(assignments);
        await new Promise(resolve=>setTimeout(resolve,90));
      }
    }
    return pending.filter(id=>!resolvedIds.has(id));
  }
  async function resolveHistoricalImages({force=false}={}){
    if(stateVisual.running||typeof fetch!=='function')return status();
    if(navigator?.onLine===false){stateVisual.error='Нет подключения к сети';return status();}
    stateVisual.running=true;stateVisual.error=null;stateVisual.failed=0;
    try{
      await loadQueries(force);
      if(force){stateVisual.records={};saveVisualCache();}
      let pending=CARDS.filter(c=>!c.image?.prefer_remote&&!stateVisual.records[c.id]).map(c=>c.id);
      const visible=new Set([...document.querySelectorAll?.('img[data-card-image]')||[]].map(el=>el.dataset.cardImage).filter(Boolean));
      pending.sort((a,b)=>(visible.has(b)?1:0)-(visible.has(a)?1:0));
      const usage=imageUsage();
      for(let pass=0;pass<6&&pending.length;pass++)pending=await resolvePass(pending,pass,usage);
      stateVisual.failed=pending.length;stateVisual.lastRun=new Date().toISOString();saveVisualCache();hydrateMountedImages();
    }catch(error){stateVisual.error=error.message||String(error);console.warn('[Codex visuals]',error);}
    finally{stateVisual.running=false;try{render();}catch{};}
    return status();
  }
  window.refreshHistoricalImages=async function(){
    if(stateVisual.running)return;
    showToast('Исторические изображения','Подбираем источники и лицензии','▧');
    await resolveHistoricalImages({force:true});
    const s=status();showToast('Визуальный архив обновлён',`${s.resolved}/${s.total} карточек · без изображения ${s.failed}`,'✓');
  };
  window.clearHistoricalImageCache=function(){
    if(!confirm('Очистить кэш найденных изображений? Локальные обложки останутся.'))return;
    stateVisual.records={};stateVisual.lastRun=null;stateVisual.failed=0;localStorage.removeItem(CACHE_KEY);render();showToast('Кэш изображений очищен','При следующем запуске источники загрузятся заново','↺');
  };
  window.resolveHistoricalImages=resolveHistoricalImages;

  const previousSettings=settingsScreen;
  settingsScreen=function(){
    let html=previousSettings(),s=status();
    const last=s.lastRun?new Intl.DateTimeFormat('ru-RU',{day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit'}).format(new Date(s.lastRun)):'ещё не запускалось';
    const block=`<article class="settings-card settings-wide visual-archive-settings"><div class="settings-card-head"><span>▧</span><div><h3>Исторические изображения</h3><p>Wikimedia Commons, локальные fallback-обложки и кэш браузера.</p></div></div><div class="visual-archive-meter"><div><b>${s.resolved}/${s.total}</b><span>карточек с историческим изображением</span></div><div class="progress"><span style="width:${Math.round(s.resolved/s.total*100)}%"></span></div><small>${s.running?'Идёт загрузка…':`Последняя проверка: ${last}${s.failed?` · без результата ${s.failed}`:''}`}</small></div><div class="settings-actions"><button class="btn" onclick="refreshHistoricalImages()" ${s.running?'disabled':''}>${s.running?'Загрузка…':'Обновить изображения'}</button><button class="btn ghost" onclick="clearHistoricalImageCache()">Очистить кэш</button></div><p class="settings-note">Файл, автор и лицензия показываются в карточке. При недоступной сети остаётся локальная обложка.</p></article>`;
    const pos=html.lastIndexOf('</section>');return pos>=0?html.slice(0,pos)+block+html.slice(pos):html;
  };
  const previousRender=render;
  render=function(){previousRender();requestAnimationFrame(()=>hydrateMountedImages());};

  if(typeof MutationObserver!=='undefined'){
    const observer=new MutationObserver(()=>hydrateMountedImages());
    const target=document.getElementById?.('app');if(target)observer.observe(target,{childList:true,subtree:true});
  }
  const launch=()=>{
    hydrateMountedImages();
    if(navigator?.connection?.saveData)return;
    setTimeout(()=>resolveHistoricalImages(),700);
  };
  if(typeof window.addEventListener==='function')window.addEventListener('codex:ready',launch,{once:true});
})();
