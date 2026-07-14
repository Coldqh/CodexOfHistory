/* Codex v4.1.0 — stable startup without full-catalog image prefetch */
(() => {
  syncDiscovery();
  save();
  render();

  const standalone=window.matchMedia?.('(display-mode: standalone)').matches||navigator.standalone===true;
  const warmVisibleImages=()=>{
    if(typeof navigator==='undefined'||!('serviceWorker' in navigator)||navigator.connection?.saveData||standalone)return;
    const run=async()=>{
      const urls=[...new Set([...document.querySelectorAll('img[data-card-image]')]
        .filter(img=>img.getBoundingClientRect().top<innerHeight*1.5)
        .map(img=>img.currentSrc||img.src)
        .filter(Boolean))].slice(0,8);
      for(const url of urls){
        try{await fetch(url,{cache:'force-cache'});}catch{}
      }
      if(urls.length)console.info(`[Codex] warmed ${urls.length} visible card images`);
    };
    const schedule=()=>('requestIdleCallback'in window?requestIdleCallback(run,{timeout:1800}):setTimeout(run,1200));
    if(navigator.serviceWorker.controller)schedule();
    else navigator.serviceWorker.addEventListener?.('controllerchange',schedule,{once:true});
  };
  warmVisibleImages();
  window.dispatchEvent(new CustomEvent('codex:ready',{detail:{version:CODEX_MANIFEST.version,cards:CARDS.length}}));
  console.info(`[Codex] v${CODEX_MANIFEST.version}: ${CARDS.length} cards, ${RELATIONS.length} relations, ${CAMPAIGN.nodes.length} missions`);
})();
