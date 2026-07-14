#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='3.6.0'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for key,val in [
 ('cards',['data/cards/bronze-collapse/story.json','data/cards/bronze-collapse/archive.json']),
 ('pools',['data/campaigns/bronze-collapse/pools.json']),
 ('quizzes',['data/quizzes/bronze-collapse/campaign.json']),
 ('stories',['data/stories/bronze-collapse/personal.json']),
 ('lessons',['data/lessons/bronze-collapse/campaign.json']),
 ('campaigns',['data/campaigns/bronze-collapse/campaign.json'])]:
 for x in val:
  if x not in d[key]:d[key].append(x)
d['maps']['BRONZE_COLLAPSE']='data/maps/bronze-collapse.json'
script='js/features/v3-6-collapse.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js')
 m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));add=load(Path('data/core/relations-v36-collapse.json'))
existing={x['id'] for x in rels};rels.extend(x for x in add if x['id'] not in existing);dump(Path('data/core/relations.json'),rels)
(ROOT/'data/core/relations-v36-collapse.json').unlink(missing_ok=True)

world=load(Path('data/world/campaigns.json'));chapters=load(Path('data/campaigns/bronze-collapse/campaign.json'))['chapters']
for c in world:
 if c['id']=='BRONZE_COLLAPSE':
  c.update({'title':'Катастрофа бронзового века','subtitle':'Кризис, разрушение и переход','period':'ок. 1250–1050 годы до н. э.','chapterCount':10,'releasedChapters':10,'status':'PLAYABLE','region':'Восточное Средиземноморье и Передняя Азия','description':'Разрушение дворцовых систем, засухи, войны, народы моря, выживание регионов и переход к раннему железному веку.','chapters':[{'number':x['number'],'title':x['title']} for x in chapters]})
dump(Path('data/world/campaigns.json'),world)

wt=load(Path('data/world/timeline.json'))
new=[
 {'year':-1250,'label':'Позднебронзовая система под давлением','detail':'Дворцовые государства зависят от дальних поставок, вассалов и сложного перераспределения.','campaignId':'BRONZE_COLLAPSE','sourcePatch':'v3.6'},
 {'year':-1210,'label':'Ослабление Хатти и сирийской системы','detail':'Потеря территорий, военное давление и проблемы снабжения усиливают кризис.','campaignId':'BRONZE_COLLAPSE','sourcePatch':'v3.6'},
 {'year':-1200,'label':'Разрушение многих микенских дворцов','detail':'Пилос, Микены и другие центры переживают разрушения и конец дворцовой письменности.','campaignId':'BRONZE_COLLAPSE','sourcePatch':'v3.6'},
 {'year':-1190,'label':'Гибель Угарита','detail':'Портовый город разрушается, а его последние письма остаются в архивах.','campaignId':'BRONZE_COLLAPSE','sourcePatch':'v3.6'},
 {'year':-1180,'label':'Войны Рамсеса III','detail':'Египетские надписи описывают сухопутные и морские сражения с несколькими группами противников.','campaignId':'BRONZE_COLLAPSE','sourcePatch':'v3.6'},
 {'year':-1150,'label':'Постдворцовая перестройка','detail':'Кипр, Левант, Анатолия и Эгейский мир формируют новые локальные сети.','campaignId':'BRONZE_COLLAPSE','sourcePatch':'v3.6'},
 {'year':-1050,'label':'Переход к раннему железному веку','detail':'Новые государства и письменные системы развиваются на основе разных региональных траекторий.','campaignId':'BRONZE_COLLAPSE','sourcePatch':'v3.6'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt}
wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

bw=load(Path('data/maps/bronze-world.json'))
bw['points'].update({'COLLAPSE_HATTUSA':[40.019,34.615],'COLLAPSE_UGARIT':[35.602,35.785],'COLLAPSE_PYLOS':[37.028,21.696],'COLLAPSE_MEDINET_HABU':[25.72,32.60],'COLLAPSE_CYPRUS':[35.0,33.2]})
dump(Path('data/maps/bronze-world.json'),bw)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v3.6

## v3.7 — Экзамен эпохи бронзового века

Следующий патч объединит все кампании второй эпохи в общий экзамен и сравнительный слой.

Основные задачи:

- параллельная хронология Вавилона, Египта, Хатти, Эгеиды и международного мира;
- карта великих держав, торговых путей, разрушенных и устойчивых центров;
- сравнение дворцовых систем, дипломатии, письма и военной организации;
- итоговые задания по источникам и региональным различиям;
- общий архивный пак эпохи;
- проверка всей второй эпохи на повторяющиеся карточки и изображения.
''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v3_6.md').write_text('''# Patch v3.6.0 — Катастрофа бронзового века

- 10 глав, 60 миссий и 120 карточек.
- Кризис дворцовых систем, засухи, войны и внутренний распад.
- Падение Хатти, последние дни Угарита и войны Рамсеса III.
- Конец микенских дворцов, Кипр, региональная устойчивость и переход к железному веку.
- 10 архивных пулов, 10 личных историй и отдельный пак.
- Карта разрушений и устойчивых центров.
- Четырёхчастный итоговый экзамен.
- Удалён лишний промо-блок эпохи II из экрана выбора кампаний.
''',encoding='utf-8')
(ROOT/'docs/QA_v3_6.md').write_text('''# QA v3.6.0

Проверяется:

- 120 новых карточек и локальные обложки;
- 60 миссий и 60 уроков;
- 14 квизов, 10 пулов и 10 личных историй;
- старт новой игры только с COL_S_01_01–03;
- пак кампании выдаёт только COL_A_*;
- карта Хаттусы, Угарита, Пилоса, Мединет-Абу и Кипра;
- четыре модуля итогового экзамена;
- отсутствие блока «ЭПОХА II / Пять кампаний доступны»;
- версии manifest, runtime, Service Worker и package metadata.
''',encoding='utf-8')

p=ROOT/'README.md';txt=p.read_text(encoding='utf-8');txt=re.sub(r'^# Codex of History v[^\n]+','# Codex of History v3.6.0',txt,count=1,flags=re.M)
section='''\n## v3.6.0 — Катастрофа бронзового века\n\n- 10 глав, 60 миссий и 120 карточек.\n- Падение Хатти, Угарита и микенских дворцов.\n- Египет и народы моря, Кипр и региональная устойчивость.\n- Переход к раннему железному веку и многофакторная реконструкция.\n- Удалён лишний промо-блок эпохи II из выбора кампаний.\n- Релизный ZIP содержит только изменённые и новые файлы.\n\n'''
if '## v3.6.0' not in txt:txt=txt.replace('\n',section,1)
p.write_text(txt,encoding='utf-8')

attr=ROOT/'ATTRIBUTION.md';at=attr.read_text(encoding='utf-8')
section='''\n## v3.6 — Катастрофа бронзового века\n\nЛокальные SVG-обложки 120 карточек и обложка пака созданы для проекта Codex of History. Историческая проверка и ссылки карточек используют материалы The Metropolitan Museum of Art, Institute for the Study of Ancient Cultures, American Journal of Archaeology и World History Encyclopedia. Динамические исторические изображения загружаются только для видимых карточек и живут до конца текущей сессии.\n'''
if '## v3.6 — Катастрофа' not in at:at+=section
attr.write_text(at,encoding='utf-8')
print('integrated v3.6')
