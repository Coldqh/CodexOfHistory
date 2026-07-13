/* Codex v1.6 — registries, responsive image URLs and shared helpers */
function card(id){ return CODEX_REGISTRY.cardsById.get(id); }
function isUnlocked(id){ return state.unlocked.includes(id); }
function imgUrl(file){ return 'https://commons.wikimedia.org/wiki/Special:Redirect/file/' + encodeURIComponent(file) + '?width=900'; }
function filePage(file){ return 'https://commons.wikimedia.org/wiki/File:' + String(file||'').replaceAll(' ','_'); }
function cardImageSource(c){
  const image=c?.image||{};
  return image.prefer_remote&&image.file?imgUrl(image.file):(image.local||imgUrl(image.file));
}
function cardImageFallback(c){
  const image=c?.image||{};
  return image.prefer_remote&&image.local?image.local:'assets/ui/fallback-card.svg';
}
function cardImageSourcePage(c){return c?.image?.source_url||filePage(c?.image?.file);}
function fallbackCardImage(el){
  const fallback=el.dataset.fallback;
  if(fallback){delete el.dataset.fallback;el.src=fallback;return;}
  el.onerror=null;el.src='assets/ui/fallback-card.svg';
}
function imgTag(c, cls=''){
  const source=cardImageSource(c),fallback=cardImageFallback(c);
  return `<img class="${cls}" src="${source}" data-fallback="${fallback}" alt="${esc(c.title)}" loading="lazy" decoding="async" style="object-position:${c.image.focus || '50% 50%'}" referrerpolicy="no-referrer" onerror="fallbackCardImage(this)">`;
}
function esc(s){ return String(s ?? '').replace(/[&<>"']/g, m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m])); }
function typeLabel(t){ return TYPE_META[t]?.[1] || t; }
function typeIcon(t){ return TYPE_META[t]?.[0] || '◈'; }
function rarityLabel(r){ return RARITY_META[r] || r; }
function addXp(x){ state.xp += x; state.level = Math.floor(state.xp/500)+1; save(); }
function unlock(ids){ ids.filter(Boolean).forEach(id=>{ if(!state.unlocked.includes(id)) state.unlocked.push(id); }); save(); }
function collectionProgress(){ return Math.round(state.unlocked.length / CARDS.length * 100); }
function levelProgress(){ return Math.round((state.xp % 500) / 500 * 100); }
function quizResult(id){ return state.quizResults?.[id] || null; }
function isQuizPassed(id){ return !!quizResult(id)?.passed; }
function passedQuizCount(){ return Object.values(state.quizResults||{}).filter(r=>r.passed).length; }
function campaignProgress(){ return Math.round(completedMissionCount() / CAMPAIGN.nodes.length * 100); }
function currentNode(){ return currentMission(); }
function averageQuiz(){
  const vals=Object.values(state.quizResults||{}).map(r=>r.bestPercent||0);
  return vals.length ? Math.round(vals.reduce((a,b)=>a+b,0)/vals.length) : 0;
}
function pageTitle(){ return PAGE_META[state.tab] || PAGE_META.home; }
function cardNumber(c){ return String(CARDS.findIndex(x=>x.id===c.id)+1).padStart(2,'0'); }
function currentCard(){ return card(state.currentCard) || CARDS[0]; }
