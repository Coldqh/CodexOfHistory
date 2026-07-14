#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='3.7.0'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for key,vals in [
 ('cards',['data/cards/bronze-world/story.json','data/cards/bronze-world/archive.json']),
 ('pools',['data/campaigns/bronze-world/pools.json']),
 ('quizzes',['data/quizzes/bronze-world/campaign.json']),
 ('stories',['data/stories/bronze-world/personal.json']),
 ('lessons',['data/lessons/bronze-world/campaign.json']),
 ('campaigns',['data/campaigns/bronze-world/campaign.json'])]:
 for x in vals:
  if x not in d[key]:d[key].append(x)
d['maps']['BRONZE_ERA_EXAM']='data/maps/bronze-world-exam.json'
script='js/features/v3-7-bronze-world.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js');m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));add=load(Path('data/core/relations-v37-bronze-world.json'));existing={x['id'] for x in rels};rels.extend(x for x in add if x['id'] not in existing);dump(Path('data/core/relations.json'),rels);(ROOT/'data/core/relations-v37-bronze-world.json').unlink(missing_ok=True)

world=load(Path('data/world/campaigns.json'));camp=load(Path('data/campaigns/bronze-world/campaign.json'))
if not any(x['id']=='BRONZE_ERA_EXAM' for x in world):
 world.append({'id':'BRONZE_ERA_EXAM','eraId':'ERA_BRONZE','order':11,'title':'Царства бронзового века: общий экзамен','subtitle':'Сравнение и итог второй эпохи','period':'ок. 2000–1050 до н. э.','chapterCount':8,'releasedChapters':8,'status':'PLAYABLE','region':'Восточное Средиземноморье и Передняя Азия','description':'Параллельная хронология, державы, дворцы, письмо, обмен, война, кризис и итоговый экзамен эпохи.','chapters':[{'number':x['number'],'title':x['title']} for x in camp['chapters']]})
world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_BRONZE' and 'BRONZE_ERA_EXAM' not in e['campaignIds']:e['campaignIds'].append('BRONZE_ERA_EXAM')
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'))
new=[
 {'year':-2000,'label':'Начало сравнительной шкалы бронзового века','detail':'Старовавилонские государства, Среднее царство Египта и ранние дворцовые системы рассматриваются на одной шкале без уравнивания фаз.','campaignId':'BRONZE_ERA_EXAM','sourcePatch':'v3.7'},
 {'year':-1650,'label':'Формирование нового баланса держав','detail':'Хатти, Египет, Митанни, Вавилония и эгейские центры развиваются разными политическими траекториями.','campaignId':'BRONZE_ERA_EXAM','sourcePatch':'v3.7'},
 {'year':-1400,'label':'Международная система великих царей','detail':'Аккадская переписка, царские дары и вассальные договоры связывают дворцы от Египта до Месопотамии.','campaignId':'BRONZE_ERA_EXAM','sourcePatch':'v3.7'},
 {'year':-1300,'label':'Пик позднебронзовых сетей','detail':'Кипрская медь, Угарит, морские маршруты и дворцовые мастерские поддерживают сложный обмен.','campaignId':'BRONZE_ERA_EXAM','sourcePatch':'v3.7'},
 {'year':-1200,'label':'Региональные кризисы поздней бронзы','detail':'Часть дворцов и царств разрушается, другие государства и общины сохраняют устойчивость.','campaignId':'BRONZE_ERA_EXAM','sourcePatch':'v3.7'},
 {'year':-1050,'label':'Итог перехода к железному веку','detail':'Новые политические формы возникают через сочетание разрыва и непрерывности.','campaignId':'BRONZE_ERA_EXAM','sourcePatch':'v3.7'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v3.7

## v4.0 — Железный век: Ассирия и Нововавилонское царство

Следующий крупный патч откроет третью эпоху и первую полноценную кампанию железного века.

Основные задачи:

- Новоассирийская держава, провинции, армия и депортации;
- столицы Кальху, Дур-Шаррукин и Ниневия;
- архивы, рельефы и царская пропаганда;
- падение Ассирии и возвышение Нововавилонского царства;
- отдельная карта Месопотамии и Леванта железного века;
- новые паки, карточки и личные истории;
- открытие Эпохи III без лишнего промо-блока.
''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v3_7.md').write_text('''# Patch v3.7.0 — Экзамен эпохи бронзового века

- 8 глав, 48 миссий и 96 карточек.
- Параллельная хронология 2000–1050 годов до н. э.
- Сравнение держав, дворцов, письма, торговли, войны и кризиса.
- Глобальная карта шести кампаний второй эпохи.
- 8 архивных пулов, 8 личных историй и общий пак эпохи.
- Итоговый экзамен из шести модулей.
- Межкампанийные связи со всеми ветками бронзового века.
- Аудит точных повторов названий и уникальности локальных изображений.
''',encoding='utf-8')
(ROOT/'docs/QA_v3_7.md').write_text('''# QA v3.7.0

Проверяется:

- 96 новых карточек: 72 сюжетные и 24 архивные;
- 48 миссий и 48 уроков;
- 14 квизов, 8 пулов и 8 личных историй;
- старт новой игры только с BRZ_S_01_01–03;
- общий пак выдаёт только BRZ_A_*;
- шесть регионов и пять строк параллельной хронологии;
- шесть модулей итогового экзамена;
- отсутствие точных дублей названий новых карт с существующим каталогом;
- все локальные SVG имеют уникальные пути;
- версии manifest, runtime, Service Worker и package metadata.
''',encoding='utf-8')

p=ROOT/'README.md';txt=p.read_text(encoding='utf-8');txt=re.sub(r'^# Codex of History v[^\n]+','# Codex of History v3.7.0',txt,count=1,flags=re.M)
section='''\n## v3.7.0 — Экзамен эпохи бронзового века\n\n- 8 глав, 48 миссий и 96 карточек.\n- Общая карта и параллельная хронология шести кампаний второй эпохи.\n- Державы, дворцовые системы, письменность, обмен, война и кризис.\n- Общий архивный пак и итоговый экзамен из шести модулей.\n- Релизный ZIP содержит только изменённые и новые файлы.\n\n'''
if '## v3.7.0' not in txt:txt=txt.replace('\n',section,1)
p.write_text(txt,encoding='utf-8')
attr=ROOT/'ATTRIBUTION.md';at=attr.read_text(encoding='utf-8');section='''\n## v3.7 — Общий слой бронзового века\n\nЛокальные SVG-обложки 96 карточек и вертикальная обложка общего пака созданы для Codex of History. Историческая проверка использует материалы The Metropolitan Museum of Art, UNESCO, British Museum и исследовательские публикации, уже перечисленные в источниках карточек. Динамические исторические изображения загружаются только для видимых карточек и хранятся до конца текущей сессии.\n'''
if '## v3.7 — Общий слой' not in at:at+=section
attr.write_text(at,encoding='utf-8')
print('integrated v3.7')
