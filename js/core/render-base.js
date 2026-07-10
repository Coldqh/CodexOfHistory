/* Codex v1.1 — enhancement and base render loop */
function initEnhancements(){
  const prefersReduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(!prefersReduced){
    document.querySelectorAll('.tilt:not(.lock)').forEach(el=>{
      el.addEventListener('pointermove',e=>{
        if(window.innerWidth<901) return;
        const r=el.getBoundingClientRect(); const x=(e.clientX-r.left)/r.width; const y=(e.clientY-r.top)/r.height;
        el.style.setProperty('--ry',`${(x-.5)*8}deg`); el.style.setProperty('--rx',`${(.5-y)*8}deg`);
        el.style.setProperty('--hx',`${x*100}%`); el.style.setProperty('--hy',`${y*100}%`);
      });
      el.addEventListener('pointerleave',()=>{el.style.setProperty('--ry','0deg');el.style.setProperty('--rx','0deg');});
    });
  }
  const items=document.querySelectorAll('.reveal');
  if(!('IntersectionObserver' in window) || prefersReduced){items.forEach(x=>x.classList.add('visible'));return;}
  const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target);}}),{threshold:.08});
  items.forEach((x,i)=>{x.style.transitionDelay=`${Math.min(i*55,220)}ms`;io.observe(x);});
}
function render(){
  applyTheme();
  destroyMaps();
  document.getElementById('app').innerHTML=({home,campaign,mission:missionScreen,collection,detail,quiz,map:mapScreen,profile}[state.tab]||home)();
  requestAnimationFrame(()=>{initEnhancements();initMapsForView();});
}

document.addEventListener('pointermove',e=>{
  document.documentElement.style.setProperty('--mx',`${e.clientX}px`);
  document.documentElement.style.setProperty('--my',`${e.clientY}px`);
},{passive:true});
document.addEventListener('keydown',e=>{
  if(e.altKey && /^[1-5]$/.test(e.key)) go(NAV[Number(e.key)-1][0]);
  if(e.key==='Escape' && state.tab==='detail') go('collection');
});


