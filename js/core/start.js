/* Codex v1.7 — startup and local image cache warming */
(() => {
  syncDiscovery();
  save();
  render();
  const warmImages=async()=>{
    if(typeof navigator==='undefined'||!('serviceWorker' in navigator)||navigator.connection?.saveData)return;
    const run=async()=>{
      const urls=[...new Set(CARDS.map(c=>imgUrl(c.image.file)))];
      for(let i=0;i<urls.length;i+=4){
        await Promise.allSettled(urls.slice(i,i+4).map(url=>fetch(url,{mode:'no-cors',cache:'force-cache'})));
        await new Promise(resolve=>setTimeout(resolve,80));
      }
      console.info(`[Codex] cached ${urls.length} card images locally`);
    };
    if(navigator.serviceWorker.controller) setTimeout(run,900);
    else if(typeof navigator.serviceWorker.addEventListener==='function') navigator.serviceWorker.addEventListener('controllerchange',()=>setTimeout(run,400),{once:true});
  };
  warmImages();
  window.dispatchEvent(new CustomEvent('codex:ready',{detail:{version:CODEX_MANIFEST.version,cards:CARDS.length}}));
  console.info(`[Codex] v${CODEX_MANIFEST.version}: ${CARDS.length} cards, ${RELATIONS.length} relations, ${CAMPAIGN.nodes.length} missions`);
})();
