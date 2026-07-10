/* Codex v1.3 — settings, compact mobile preferences and update controls */
const PREF_STORE='codex_history_preferences_v13';
const DEFAULT_PREFERENCES={density:'compact',textSize:'normal',motion:'full',confirmReset:true,lastForcedRefresh:null};
let storedPreferences={};
try{storedPreferences=JSON.parse(localStorage.getItem(PREF_STORE)||'{}')||{};}catch{storedPreferences={};}
let preferences={...DEFAULT_PREFERENCES,...storedPreferences};

function appVersion(){return CODEX_MANIFEST?.version||'1.3.0';}
function savePreferences(){localStorage.setItem(PREF_STORE,JSON.stringify(preferences));}
function applyPreferences(){
  const root=document.documentElement;
  root.dataset.density=preferences.density==='comfortable'?'comfortable':'compact';
  root.dataset.textSize=['small','normal','large'].includes(preferences.textSize)?preferences.textSize:'normal';
  root.dataset.motion=preferences.motion==='reduced'?'reduced':'full';
}
function setPreference(key,value){preferences[key]=value;savePreferences();applyPreferences();render();showToast('Настройки сохранены','Интерфейс обновлён','⚙');}
function selectClass(key,value){return preferences[key]===value?'selected':'';}
function preferenceButton(key,value,label,sub=''){
  return `<button class="preference-option ${selectClass(key,value)}" onclick="setPreference('${key}','${value}')"><b>${label}</b>${sub?`<span>${sub}</span>`:''}</button>`;
}
async function forceRefresh(ask=true){
  if(ask&&!confirm('Принудительно загрузить свежую версию Codex? Прогресс останется на месте.'))return;
  preferences.lastForcedRefresh=new Date().toISOString();savePreferences();
  showToast('Обновляем Codex','Очищаем кэш и загружаем свежие файлы','↻');
  try{
    if('caches'in window){const keys=await caches.keys();await Promise.all(keys.map(k=>caches.delete(k)));}
    if('serviceWorker'in navigator){const regs=await navigator.serviceWorker.getRegistrations();await Promise.all(regs.map(r=>r.unregister()));}
  }catch(error){console.warn('[Codex refresh]',error);}
  sessionStorage.setItem('codex_force_refresh',String(Date.now()));
  const url=new URL(location.href);url.searchParams.set('refresh',String(Date.now()));
  setTimeout(()=>location.replace(url.href),220);
}
function exportSave(){
  const payload={product:'Codex of History',version:appVersion(),exportedAt:new Date().toISOString(),progress:state,preferences};
  const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});
  const url=URL.createObjectURL(blob);const a=document.createElement('a');
  a.href=url;a.download=`codex-save-v${appVersion()}-${new Date().toISOString().slice(0,10)}.json`;a.click();URL.revokeObjectURL(url);
  showToast('Сохранение экспортировано','Файл можно перенести на другое устройство','⇩');
}
function requestImport(){document.getElementById('settings-import')?.click();}
async function importSave(event){
  const file=event.target.files?.[0];if(!file)return;
  try{
    const payload=JSON.parse(await file.text());const progress=payload.progress||payload;
    if(!progress||typeof progress!=='object'||!Array.isArray(progress.unlocked))throw new Error('Не найдено корректное сохранение');
    if(!confirm('Заменить текущий прогресс данными из файла?'))return;
    localStorage.setItem(STORE,JSON.stringify(progress));
    if(payload.preferences&&typeof payload.preferences==='object')localStorage.setItem(PREF_STORE,JSON.stringify({...DEFAULT_PREFERENCES,...payload.preferences}));
    sessionStorage.setItem('codex_force_refresh',String(Date.now()));location.reload();
  }catch(error){showToast('Импорт не выполнен',error.message||'Файл повреждён','!');}
  finally{event.target.value='';}
}
function clearInterfacePreferences(){
  if(!confirm('Вернуть стандартные настройки интерфейса? Прогресс игры не изменится.'))return;
  preferences={...DEFAULT_PREFERENCES};savePreferences();applyPreferences();render();showToast('Настройки сброшены','Включён компактный мобильный режим','↺');
}
function formatSettingDate(value){
  if(!value)return 'ещё не запускалось';
  try{return new Intl.DateTimeFormat('ru-RU',{day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit'}).format(new Date(value));}catch{return 'неизвестно';}
}
function settingsScreen(){
  const light=state.theme==='parchment';
  return shell(`<section class="settings-hero reveal"><div><div class="eyebrow">Система Codex</div><h2>Настройки</h2><p>Компактность, тема, анимации, резервные копии и ручное обновление приложения.</p></div><div class="version-medallion"><small>ТЕКУЩАЯ ВЕРСИЯ</small><b>v${appVersion()}</b><span>Content Engine</span></div></section>
  <section class="settings-grid reveal">
    <article class="settings-card settings-wide"><div class="settings-card-head"><span>◐</span><div><h3>Внешний вид</h3><p>Параметры применяются сразу и хранятся отдельно от игрового прогресса.</p></div></div>
      <div class="setting-row"><div><b>Тема</b><span>Чёрная или историческая пергаментная</span></div><button class="settings-theme-preview ${light?'light':''}" onclick="toggleTheme()"><i>☾</i><b></b><i>☀</i></button></div>
      <div class="setting-block"><label>Плотность мобильного интерфейса</label><div class="preference-grid">${preferenceButton('density','compact','Компактная','Больше контента на экране')}${preferenceButton('density','comfortable','Комфортная','Крупнее карточки и отступы')}</div></div>
      <div class="setting-block"><label>Размер текста</label><div class="preference-grid three">${preferenceButton('textSize','small','Мелкий')}${preferenceButton('textSize','normal','Обычный')}${preferenceButton('textSize','large','Крупный')}</div></div>
      <div class="setting-block"><label>Анимации</label><div class="preference-grid">${preferenceButton('motion','full','Полные','Переходы и эффекты')}${preferenceButton('motion','reduced','Минимальные','Меньше движения и нагрузки')}</div></div>
    </article>
    <article class="settings-card"><div class="settings-card-head"><span>↻</span><div><h3>Обновление</h3><p>Для GitHub Pages и кэшированных файлов.</p></div></div><div class="version-table"><span>Версия приложения</span><b>v${appVersion()}</b><span>Контент</span><b>${CARDS.length} карт · ${CAMPAIGN.nodes.length} миссий</b><span>Последнее ручное обновление</span><b>${formatSettingDate(preferences.lastForcedRefresh)}</b></div><button class="btn settings-main-btn" onclick="forceRefresh()">↻ Загрузить свежую версию</button><p class="settings-note">Кэш будет очищен. Карточки, XP и прохождение сохранятся.</p></article>
    <article class="settings-card"><div class="settings-card-head"><span>▣</span><div><h3>Сохранение</h3><p>Перенос прогресса между браузерами и устройствами.</p></div></div><div class="settings-actions"><button class="btn secondary" onclick="exportSave()">⇩ Экспортировать</button><button class="btn secondary" onclick="requestImport()">⇧ Импортировать</button><input id="settings-import" type="file" accept="application/json,.json" hidden onchange="importSave(event)"></div><p class="settings-note">Экспорт включает игровой прогресс и настройки интерфейса.</p></article>
    <article class="settings-card"><div class="settings-card-head"><span>⌁</span><div><h3>Управление данными</h3><p>Опасные действия вынесены отдельно.</p></div></div><div class="settings-actions vertical"><button class="btn ghost" onclick="clearInterfacePreferences()">↺ Сбросить только настройки</button><button class="btn danger" onclick="resetProgress()">Удалить игровой прогресс</button></div></article>
    <article class="settings-card settings-wide settings-about"><div class="settings-card-head"><span>i</span><div><h3>О приложении</h3><p>Codex of History работает как статическое приложение на GitHub Pages. Сервер и аккаунт не требуются.</p></div></div><div class="about-pills"><span>Static PWA-ready</span><span>LocalStorage</span><span>GitHub Pages</span><span>Русский интерфейс</span><span>v${appVersion()}</span></div></article>
  </section>`);
}

applyPreferences();
