/* Codex v1.4 — runtime configuration, state and theme */
const STORE = 'codex_history_v02_ru';
const TYPE_META = {
  PERSON:['♛','Личность'], EVENT:['✦','Событие'], BATTLE:['⚔','Битва'],
  STATE:['◈','Государство'], FACTION:['⌂','Институт'], CITY:['⌖','Место'],
  CULTURE:['◌','Народ / культура'], ARTIFACT:['◇','Артефакт'], RELIGION:['✹','Религия']
};
const RARITY_META = {RARE:'Редкая', EPIC:'Эпическая', LEGENDARY:'Легендарная', MYTHIC:'Мифическая'};
const STAT_LABELS = {influence:'Влияние', complexity:'Сложность', legacy:'Наследие', military:'Война', culture:'Культура', politics:'Политика', religion:'Религия', economy:'Экономика', connections:'Связи'};
const NAV = [
  ['home','⌂','Главная'], ['campaign','♜','Кампания'], ['collection','▦','Коллекция'],
  ['map','⌖','Карта'], ['profile','◉','Профиль']
];
const PAGE_META = {
  home:['Обзор','Твой исторический мир'], campaign:['Кампания','Рождение Рима'], mission:['Миссия','Глава I'],
  collection:['Архив','Коллекция знаний'], detail:['Карточка','Историческое досье'],
  quiz:['Испытание','Проверка знаний'], map:['Атлас','Карта кампании'], profile:['Профиль','Личный прогресс'],
  settings:['Система','Настройки приложения']
};
const PASS_PERCENT = 70;
const initial = {
  tab:'home', xp:0, level:1, theme:'night',
  unlocked:['PER_ROM_001','PER_ROM_005','EVT_ROM_001'],
  read:[], quizDone:[], quizResults:{}, missionsCompleted:[], mapTasks:{}, timelineTasks:{},
  currentCard:'PER_ROM_001', currentQuiz:null, currentMission:'MIS_BIRTH_01', quizMissionId:null,
  quizIndex:0, quizScore:0, selected:null, quizFinished:false, quizLastResult:null,
  filter:'ALL', rarity:'ALL', search:''
};
let state = {...initial, ...(JSON.parse(localStorage.getItem(STORE) || '{}'))};
state.quizResults = state.quizResults || {};
state.quizDone = Array.isArray(state.quizDone) ? state.quizDone : [];
state.missionsCompleted = Array.isArray(state.missionsCompleted) ? state.missionsCompleted : [];
state.mapTasks = state.mapTasks || {};
state.timelineTasks = state.timelineTasks || {};
state.theme = state.theme === 'parchment' ? 'parchment' : 'night';
state.unlocked = Array.isArray(state.unlocked) ? state.unlocked : [...initial.unlocked];
initial.unlocked.forEach(id=>{if(!state.unlocked.includes(id)) state.unlocked.push(id);});
applyTheme();

function save(){ localStorage.setItem(STORE, JSON.stringify(state)); }
function applyTheme(){
  document.documentElement.dataset.theme=state.theme;
  document.documentElement.style.colorScheme=state.theme==='parchment'?'light':'dark';
  const meta=document.querySelector('meta[name="theme-color"]');
  if(meta) meta.content=state.theme==='parchment'?'#ded1b6':'#050505';
}
function toggleTheme(){
  document.documentElement.classList.add('theme-switching');
  state.theme=state.theme==='night'?'parchment':'night'; save(); applyTheme(); render();
  setTimeout(()=>document.documentElement.classList.remove('theme-switching'),520);
  showToast(state.theme==='parchment'?'Пергаментная тема':'Ночная тема',state.theme==='parchment'?'Светлый исторический режим включён':'Тёмный режим включён',state.theme==='parchment'?'☀':'☾');
}
