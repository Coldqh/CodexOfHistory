/* Codex of History v3.4.0 — semantic historical image resolver with session-only lazy loading */
(() => {
  const CACHE_KEY='codex_history_visual_archive_session_v322';
  const VISUAL_STORAGE=(()=>{try{return sessionStorage;}catch{return null;}})();
  const QUERY_PATH=CODEX_MANIFEST?.datasets?.imageQueries||'data/image_queries.json';
  const STATIC_COUNT=CARDS.filter(c=>c.image?.prefer_remote&&c.image?.file).length;
  const MAX_CONTEXT_REUSE=8;
  const IS_STANDALONE=window.matchMedia?.('(display-mode: standalone)').matches||navigator.standalone===true;
  const AUTO_BATCH_LIMIT=IS_STANDALONE?4:10;
  const MANUAL_BATCH_LIMIT=IS_STANDALONE?12:36;
  const MAX_STORED_RECORDS=IS_STANDALONE?72:180;
  const stateVisual={queries:null,records:{},running:false,resolved:0,failed:0,rejectedCandidates:0,total:CARDS.length,lastRun:null,error:null,storage:'session'};

  // v3.1.2 cached unverified matches (including animal/name collisions) must never be reused.
  try{
    localStorage.removeItem('codex_history_visual_archive_v312');
    localStorage.removeItem('codex_history_visual_archive_v313');
  }catch{}

  try{
    const saved=JSON.parse(VISUAL_STORAGE?.getItem(CACHE_KEY)||'{}');
    if(saved&&saved.version==='3.4.0'&&saved.records&&typeof saved.records==='object'){
      stateVisual.records=saved.records;
      stateVisual.lastRun=saved.lastRun||null;
      stateVisual.rejectedCandidates=Number(saved.rejectedCandidates)||0;
    }
  }catch(error){console.warn('[Codex visuals] cache read failed',error);}

  const cleanHtml=value=>{
    if(!value)return'';
    const text=String(value)
      .replace(/<br\s*\/?>/gi,' ')
      .replace(/<[^>]+>/g,' ')
      .replace(/&nbsp;/gi,' ')
      .replace(/&amp;/gi,'&')
      .replace(/&quot;/gi,'"')
      .replace(/&#39;|&apos;/gi,"'")
      .replace(/\s+/g,' ')
      .trim();
    return text.length>220?`${text.slice(0,217)}…`:text;
  };
  const normalize=value=>String(value||'')
    .toLocaleLowerCase('ru-RU')
    .replace(/ё/g,'е')
    .replace(/[–—−]/g,'-')
    .replace(/[^0-9a-zа-я\-]+/g,' ')
    .replace(/\s+/g,' ')
    .trim();
  const termHit=(text,term)=>{
    const needle=normalize(term);return needle&&text.includes(needle);
  };
  const countHits=(text,terms=[])=>terms.reduce((sum,term)=>sum+(termHit(text,term)?1:0),0);
  const pageSemanticText=page=>normalize([
    page?.title,
    page?.extract,
    ...(page?.terms?.description||[]),
    ...(page?.categories||[]).map(x=>x.title?.replace(/^Category:|^Категория:/i,'')),
  ].filter(Boolean).join(' '));

  const saveVisualCache=()=>{
    try{
      const recent=Object.entries(stateVisual.records)
        .sort((a,b)=>String(b[1]?.resolvedAt||'').localeCompare(String(a[1]?.resolvedAt||'')))
        .slice(0,MAX_STORED_RECORDS);
      stateVisual.records=Object.fromEntries(recent);
      VISUAL_STORAGE?.setItem(CACHE_KEY,JSON.stringify({
        version:'3.4.0',lastRun:stateVisual.lastRun,records:stateVisual.records,rejectedCandidates:stateVisual.rejectedCandidates
      }));
    }catch(error){console.warn('[Codex visuals] cache write failed',error);}
  };
  const visualRecord=c=>stateVisual.records[c?.id]||null;
  const localFallback=c=>c?.image?.local||'assets/ui/fallback-card.svg';
  const staticRecord=c=>c?.image?.prefer_remote&&c.image.file?{
    url:imgUrl(c.image.file),
    source_url:c.image.source_url||filePage(c.image.file),
    caption:c.image.caption,
    credit:c.image.credit,
    license:c.image.license,
    file:c.image.file,
    kind:'static-historical',
    confidence:100,
  }:null;
  const effectiveRecord=c=>visualRecord(c)||staticRecord(c);
  const imageUsage=()=>{
    const usage=new Map();
    for(const rec of Object.values(stateVisual.records))if(rec?.file)usage.set(rec.file,(usage.get(rec.file)||0)+1);
    return usage;
  };
  const status=()=>{
    const dynamic=Object.keys(stateVisual.records).length;
    return {
      static:STATIC_COUNT,dynamic,total:CARDS.length,
      resolved:Math.min(CARDS.length,STATIC_COUNT+dynamic),
      running:stateVisual.running,failed:CARDS.filter(c=>!c.image?.prefer_remote&&!stateVisual.records[c.id]).length,
      rejectedCandidates:stateVisual.rejectedCandidates,
      lastRun:stateVisual.lastRun,error:stateVisual.error,
    };
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
    el.dataset.visualFailed='true';
    el.src=fallback;
    el.onerror=()=>{el.onerror=null;el.src='assets/ui/fallback-card.svg';};
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
      if(el.src!==rec.url&&!el.src.endsWith(encodeURI(rec.url)))el.src=rec.url;
    });
  }
  window.hydrateHistoricalImages=hydrateMountedImages;

  async function loadQueries(force=false){
    if(stateVisual.queries&&!force)return stateVisual.queries;
    if(typeof fetch!=='function')return null;
    const url=new URL(QUERY_PATH,location.href);url.searchParams.set('v',CODEX_MANIFEST?.version||'3.4.0');
    const response=await fetch(url.href,{cache:'no-store'});
    if(!response.ok)throw new Error(`image queries HTTP ${response.status}`);
    const payload=await response.json();
    if(payload.version!==CODEX_MANIFEST?.version)throw new Error(`image queries version ${payload.version||'unknown'}`);
    if(payload.count!==CARDS.length)throw new Error(`image queries ${payload.count}/${CARDS.length}`);
    stateVisual.queries=payload.cards;return stateVisual.queries;
  }
  function chunkTitles(entries,max=28){
    const out=[];let cur=[],size=0;
    for(const entry of entries){
      const add=encodeURIComponent(entry.title).length+3;
      if(cur.length>=max||size+add>6200){out.push(cur);cur=[];size=0;}
      cur.push(entry);size+=add;
    }
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
    Object.entries({
      origin:'*',action:'query',format:'json',formatversion:'2',redirects:'1',
      prop:'pageimages|info|extracts|categories|pageterms',
      piprop:'thumbnail|name',pithumbsize:'900',inprop:'url',
      exintro:'1',explaintext:'1',exsentences:'4',
      cllimit:'30',clshow:'!hidden',wbptterms:'description',
      titles:titles.join('|')
    }).forEach(([k,v])=>api.searchParams.set(k,v));
    const response=await fetch(api.href,{cache:'force-cache'});
    if(!response.ok)throw new Error(`Wikipedia ${lang}: ${response.status}`);
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

  function semanticDecision(entry,page){
    if(!page?.thumbnail?.source||!page.pageimage)return{ok:false,reason:'no-image',score:0};
    const semantic=entry.profile?.semantic||{},candidate=entry.candidate||{},text=pageSemanticText(page);
    if(!text)return{ok:false,reason:'no-context',score:0};
    const forbiddenHits=countHits(text,semantic.forbidden||[]);
    if(forbiddenHits)return{ok:false,reason:'forbidden-context',score:-forbiddenHits};

    const requiredHits=countHits(text,semantic.required_any||[]);
    const groupHits=countHits(text,semantic.group_terms||[]);
    const subjectHits=countHits(text,semantic.subject_terms||[]);
    const candidateTitle=normalize(candidate.title),pageTitle=normalize(page.title);
    const titleMatch=candidateTitle&&pageTitle&&(pageTitle===candidateTitle||pageTitle.includes(candidateTitle)||candidateTitle.includes(pageTitle));

    if(!candidate.trusted){
      if((semantic.required_any||[]).length&&!requiredHits)return{ok:false,reason:'wrong-kind',score:0};
      if(!groupHits)return{ok:false,reason:'wrong-history-context',score:0};
    }

    let score=0;
    if(candidate.trusted)score+=4;
    if(candidate.scope==='exact')score+=2;
    if(candidate.scope==='context')score+=1;
    if(titleMatch)score+=2;
    score+=Math.min(3,requiredHits);
    score+=Math.min(3,groupHits);
    score+=Math.min(2,subjectHits);
    const min=Number(candidate.min_score)||(candidate.scope==='exact'?5:4);
    if(score<min)return{ok:false,reason:'low-confidence',score};
    return{ok:true,reason:'accepted',score,requiredHits,groupHits,subjectHits};
  }
  window.codexVisualSemanticDecision=semanticDecision;

  function buildRecord(cardEntry,page,common,candidateIndex,decision){
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
      confidence:decision.score,
      semantic_reason:decision.reason,
      resolvedAt:new Date().toISOString(),
      kind:'wikimedia-historical-validated'
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
    for(const id of pending){
      const profile=stateVisual.queries?.[id],candidate=profile?.candidates?.[index];
      if(candidate){
        entries.push({id,lang:candidate.lang||'ru',title:candidate.title,index,card:card(id),profile,candidate});
      }
    }
    const resolvedIds=new Set();
    for(const lang of [...new Set(entries.map(x=>x.lang))]){
      const group=entries.filter(x=>x.lang===lang);
      for(const chunk of chunkTitles(group)){
        let results=[];
        try{results=await wikipediaPages(lang,chunk);}catch(error){stateVisual.error=error.message;console.warn('[Codex visuals]',error);continue;}
        const accepted=[];
        for(const result of results){
          const decision=semanticDecision(result.entry,result.page);
          if(decision.ok)accepted.push({...result,decision});
          else if(result.page?.pageimage)stateVisual.rejectedCandidates++;
        }
        const commons=await commonsMetadata(accepted);
        const assignments=[];
        for(const {entry,page,decision} of accepted){
          const uses=usage.get(page.pageimage)||0;
          const contextCandidate=entry.candidate.scope!=='exact';
          if(contextCandidate&&uses>=MAX_CONTEXT_REUSE)continue;
          const record=buildRecord(entry,page,commons.get(page.pageimage),entry.index,decision);if(!record)continue;
          assignments.push({id:entry.id,record});resolvedIds.add(entry.id);usage.set(page.pageimage,uses+1);
        }
        applyRecords(assignments);
        await new Promise(resolve=>setTimeout(resolve,90));
      }
    }
    return pending.filter(id=>!resolvedIds.has(id));
  }
  async function resolveHistoricalImages({force=false,ids=null,limit=null}={}){
    if(stateVisual.running||typeof fetch!=='function')return status();
    if(navigator?.onLine===false){stateVisual.error='Нет подключения к сети';return status();}
    stateVisual.running=true;stateVisual.error=null;
    try{
      await loadQueries(false);
      let pending=(Array.isArray(ids)&&ids.length?ids:CARDS.map(c=>c.id))
        .filter((id,index,list)=>list.indexOf(id)===index)
        .filter(id=>{const c=card(id);return c&&!c.image?.prefer_remote&&(force||!stateVisual.records[id]);});
      if(limit)pending=pending.slice(0,limit);
      if(force)for(const id of pending)delete stateVisual.records[id];
      const visible=new Set([...document.querySelectorAll?.('img[data-card-image]')||[]].map(el=>el.dataset.cardImage).filter(Boolean));
      pending.sort((a,b)=>(visible.has(b)?1:0)-(visible.has(a)?1:0));
      const usage=imageUsage();
      const maxPass=Math.max(1,...Object.values(stateVisual.queries||{}).map(x=>x.candidates?.length||0));
      let unresolved=pending;
      for(let pass=0;pass<maxPass&&unresolved.length;pass++)unresolved=await resolvePass(unresolved,pass,usage);
      stateVisual.failed=CARDS.filter(c=>!c.image?.prefer_remote&&!stateVisual.records[c.id]).length;
      stateVisual.lastRun=new Date().toISOString();saveVisualCache();hydrateMountedImages();
    }catch(error){stateVisual.error=error.message||String(error);console.warn('[Codex visuals]',error);}
    finally{stateVisual.running=false;try{window.dispatchEvent(new CustomEvent('codex:visual-progress',{detail:status()}));}catch{}}
    return status();
  }
  const mountedIds=()=>[...document.querySelectorAll?.('img[data-card-image]')||[]]
    .map(el=>el.dataset.cardImage).filter(Boolean);

  window.refreshHistoricalImages=async function(){
    if(stateVisual.running)return;
    const visible=mountedIds();
    const unresolved=CARDS.filter(c=>!c.image?.prefer_remote&&!stateVisual.records[c.id]).map(c=>c.id);
    const ids=[...new Set([...visible,...unresolved])].slice(0,MANUAL_BATCH_LIMIT);
    if(!ids.length){showToast('Изображения уже загружены','Для открытых карточек есть подтверждённые изображения','✓');return;}
    showToast('Загрузка изображений',`Проверяем до ${ids.length} карточек без перегрузки телефона`,'▧');
    await resolveHistoricalImages({ids,limit:MANUAL_BATCH_LIMIT});
    const s=status();
    showToast('Часть изображений проверена',`${s.resolved}/${s.total} карточек · осталось ${s.failed}`,'✓');
    try{render();}catch{}
  };
  window.clearHistoricalImageCache=function(){
    if(!confirm('Очистить сессию найденных изображений? Локальные обложки останутся.'))return;
    stateVisual.records={};stateVisual.lastRun=null;stateVisual.failed=CARDS.length-STATIC_COUNT;stateVisual.rejectedCandidates=0;
    try{VISUAL_STORAGE?.removeItem(CACHE_KEY);}catch{}
    render();showToast('Кэш текущей сессии очищен','Картинки будут подбираться заново только для видимых карточек','↺');
  };
  window.resolveHistoricalImages=resolveHistoricalImages;

  const previousSettings=settingsScreen;
  settingsScreen=function(){
    let html=previousSettings(),s=status();
    const last=s.lastRun?new Intl.DateTimeFormat('ru-RU',{day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit'}).format(new Date(s.lastRun)):'ещё не запускалось';
    const block=`<article class="settings-card settings-wide visual-archive-settings"><div class="settings-card-head"><span>▧</span><div><h3>Исторические изображения</h3><p>Изображения загружаются только для карточек, которые реально видит игрок. Найденные результаты живут только до конца текущей сессии.</p></div></div><div class="visual-archive-meter"><div><b>${s.resolved}/${s.total}</b><span>карточек подтверждено в этой сессии</span></div><div class="progress"><span style="width:${Math.round(s.resolved/s.total*100)}%"></span></div><small>${s.running?'Идёт проверка…':`Последняя проверка в сессии: ${last}${s.failed?` · ожидают ${s.failed}`:''}${s.rejectedCandidates?` · отклонено ${s.rejectedCandidates}`:''}`}</small></div><div class="settings-actions"><button class="btn" onclick="refreshHistoricalImages()" ${s.running?'disabled':''}>${s.running?'Проверка…':'Загрузить следующую часть'}</button><button class="btn ghost" onclick="clearHistoricalImageCache()">Очистить сессию</button></div><p class="settings-note">При закрытии приложения этот кэш исчезает. Это уменьшает постоянную нагрузку на PWA и память устройства.</p></article>`;
    const pos=html.lastIndexOf('</section>');return pos>=0?html.slice(0,pos)+block+html.slice(pos):html;
  };

  let observer=null,queueTimer=0;
  const queued=new Set();
  const flushQueue=async()=>{
    queueTimer=0;if(!queued.size)return;if(stateVisual.running){queueTimer=setTimeout(flushQueue,900);return;}
    const ids=[...queued].slice(0,AUTO_BATCH_LIMIT);ids.forEach(id=>queued.delete(id));
    await resolveHistoricalImages({ids,limit:AUTO_BATCH_LIMIT});
    if(queued.size)queueTimer=setTimeout(flushQueue,900);
  };
  const queueCard=id=>{
    const c=card(id);if(!c||c.image?.prefer_remote||stateVisual.records[id])return;
    queued.add(id);if(!queueTimer)queueTimer=setTimeout(flushQueue,IS_STANDALONE?900:450);
  };
  if(typeof IntersectionObserver!=='undefined'){
    observer=new IntersectionObserver(entries=>{
      for(const entry of entries)if(entry.isIntersecting){queueCard(entry.target.dataset.cardImage);observer.unobserve(entry.target);}
    },{rootMargin:'240px 0px'});
  }
  const observeImages=(root=document)=>{
    if(!root?.querySelectorAll)return;
    const elements=[...(root.matches?.('img[data-card-image]')?[root]:[]),...root.querySelectorAll('img[data-card-image]')];
    for(const el of elements){
      const id=el.dataset.cardImage,c=card(id);if(!c||effectiveRecord(c))continue;
      if(observer&&!el.dataset.visualObserved){el.dataset.visualObserved='1';observer.observe(el);}
      else if(!observer)queueCard(id);
    }
  };

  const previousRender=render;
  render=function(){previousRender();requestAnimationFrame(()=>{hydrateMountedImages();observeImages();});};

  if(typeof MutationObserver!=='undefined'){
    let scheduled=false;
    const mutationObserver=new MutationObserver(()=>{
      if(scheduled)return;scheduled=true;
      requestAnimationFrame(()=>{scheduled=false;hydrateMountedImages();observeImages();});
    });
    const target=document.getElementById?.('app');if(target)mutationObserver.observe(target,{childList:true,subtree:true});
  }
  const launch=()=>{hydrateMountedImages();observeImages();};
  if(typeof window.addEventListener==='function')window.addEventListener('pagehide',()=>{try{VISUAL_STORAGE?.removeItem(CACHE_KEY);}catch{};},{capture:false});
  if(typeof window.addEventListener==='function')window.addEventListener('codex:ready',launch,{once:true});
})();
