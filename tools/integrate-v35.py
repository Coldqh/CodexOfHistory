#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='3.5.0'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for key,val in [
 ('cards',['data/cards/international-bronze/story.json','data/cards/international-bronze/archive.json']),
 ('pools',['data/campaigns/international-bronze/pools.json']),
 ('quizzes',['data/quizzes/international-bronze/campaign.json']),
 ('stories',['data/stories/international-bronze/personal.json']),
 ('lessons',['data/lessons/international-bronze/campaign.json']),
 ('campaigns',['data/campaigns/international-bronze/campaign.json'])]:
 for x in val:
  if x not in d[key]:d[key].append(x)
d['maps']['BRONZE_INTERNATIONAL']='data/maps/international-bronze.json'
script='js/features/v3-5-international.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js')
 m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));add=load(Path('data/core/relations-v35-international.json'))
existing={x['id'] for x in rels};rels.extend(x for x in add if x['id'] not in existing);dump(Path('data/core/relations.json'),rels)
(ROOT/'data/core/relations-v35-international.json').unlink(missing_ok=True)

world=load(Path('data/world/campaigns.json'));chapters=load(Path('data/campaigns/international-bronze/campaign.json'))['chapters']
for c in world:
 if c['id']=='BRONZE_INTERNATIONAL':
  c.update({'title':'Международный мир бронзового века','subtitle':'Дипломатия и торговля великих держав','period':'XV–начало XII века до н. э.','chapterCount':10,'releasedChapters':10,'status':'PLAYABLE','region':'Восточное Средиземноморье и Передняя Азия','description':'Великие цари, Амарнский архив, Угарит, Алашия, Кипр, Улубурун и взаимозависимая система позднего бронзового века.','chapters':[{'number':x['number'],'title':x['title']} for x in chapters]})
dump(Path('data/world/campaigns.json'),world)

wt=load(Path('data/world/timeline.json'))
new=[
 {'year':-1450,'label':'Формирование круга великих держав','detail':'Египет, Митанни, Вавилония и Хатти ведут регулярную междворцовую дипломатию.','campaignId':'BRONZE_INTERNATIONAL','sourcePatch':'v3.5'},
 {'year':-1400,'label':'Переписка Аменхотепа III и Тушратты','detail':'Письма обсуждают браки, золото, дары и взаимные обязательства царских домов.','campaignId':'BRONZE_INTERNATIONAL','sourcePatch':'v3.5'},
 {'year':-1350,'label':'Амарнский дипломатический архив','detail':'Клинописные письма великих царей и вассалов поступают в канцелярию Ахетатона.','campaignId':'BRONZE_INTERNATIONAL','sourcePatch':'v3.5'},
 {'year':-1325,'label':'Алашия поставляет медь Египту','detail':'Письма связывают царя Алашии с медным экспортом Кипра и обменом дарами.','campaignId':'BRONZE_INTERNATIONAL','sourcePatch':'v3.5'},
 {'year':-1300,'label':'Кораблекрушение Улубурун','detail':'Международный груз меди, олова, стекла, смолы, древесины и престижных предметов тонет у Анатолии.','campaignId':'BRONZE_INTERNATIONAL','sourcePatch':'v3.5'},
 {'year':-1270,'label':'Расцвет Угарита как международного порта','detail':'Многоязычные архивы и купеческие дома связывают Сирию, Кипр, Анатолию и Эгейский мир.','campaignId':'BRONZE_INTERNATIONAL','sourcePatch':'v3.5'},
 {'year':-1210,'label':'Позднебронзовая система под давлением','detail':'Войны, перебои поставок и внутренние кризисы усиливают уязвимость дворцовых сетей.','campaignId':'BRONZE_INTERNATIONAL','sourcePatch':'v3.5'},
 {'year':-1190,'label':'Гибель Угарита','detail':'Портовый город и его архивы прекращают работу в начале XII века до н. э.','campaignId':'BRONZE_INTERNATIONAL','sourcePatch':'v3.5'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt}
wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

bw=load(Path('data/maps/bronze-world.json'))
bw['points']['AMARNA_DIPLOMACY']=[27.645,30.897]
bw['points']['UGARIT_PORT']=[35.602,35.785]
bw['points']['ALASHIYA_CYPRUS']=[35.0,33.2]
bw['points']['ULUBURUN_WRECK']=[36.13,29.69]
dump(Path('data/maps/bronze-world.json'),bw)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v3.5

## v3.6 — Катастрофа бронзового века

Следующий патч отдельно разберёт кризис около 1200 года до н. э., не сводя его к одной причине или одному народу.

Основные темы:

- разрушение Хаттусы, Угарита и микенских дворцов;
- кризис Египта конца Нового царства;
- народы моря в египетских текстах;
- засухи, голод и перебои поставок;
- внутренние восстания и дворцовая уязвимость;
- войны, миграции и морское насилие;
- региональные различия и продолжение жизни после кризиса;
- переход от позднего бронзового века к раннему железному.

План патча:

- 10 глав;
- 60 миссий;
- 120 карточек;
- карта разрушений и устойчивых центров;
- параллельная хронология около 1250–1050 годов до н. э.;
- итоговый экзамен эпохи бронзового века.
''',encoding='utf-8')

(ROOT/'docs/PATCH_NOTES_v3_5.md').write_text('''# Patch v3.5.0 — Международный мир бронзового века

- 10 глав, 60 миссий и 120 карточек.
- Великие цари, Амарнский архив, писцы, послы, дары, браки и вассалы.
- Угарит, Алашия, Кипр, медь и кораблекрушение Улубурун.
- Международная карта Восточного Средиземноморья.
- 10 архивных пулов, 10 личных историй и отдельный пак.
- Четырёхчастный итоговый экзамен.
- Связи с Египтом, Хатти, Вавилоном и Эгейским миром.
''',encoding='utf-8')
(ROOT/'docs/QA_v3_5.md').write_text('''# QA v3.5.0

Проверяется:

- 120 новых карточек и локальные обложки;
- 60 миссий и 60 уроков;
- 14 квизов, 10 пулов и 10 личных историй;
- старт новой игры только с INT_S_01_01–03;
- пак кампании выдаёт только INT_A_*;
- карта Амарны, Угарита, Кипра и Улубуруна;
- четыре модуля итогового экзамена;
- версии manifest, runtime, Service Worker и package metadata.
''',encoding='utf-8')

p=ROOT/'README.md';txt=p.read_text(encoding='utf-8');txt=re.sub(r'^# Codex of History v[^\n]+','# Codex of History v3.5.0',txt,count=1,flags=re.M)
section='''\n## v3.5.0 — Международный мир бронзового века\n\n- 10 глав, 60 миссий и 120 карточек.\n- Амарнский архив, великие цари, послы, дары, браки и вассальные города.\n- Угарит, Алашия, Кипр, медь и кораблекрушение Улубурун.\n- Международная карта, 10 архивных пулов и отдельный пак.\n- Четырёхчастный экзамен и межкампанийные связи.\n- Релизный ZIP содержит только изменённые и новые файлы.\n\n'''
if '## v3.5.0' not in txt:txt=txt.replace('\n',section,1)
p.write_text(txt,encoding='utf-8')

attr=ROOT/'ATTRIBUTION.md';at=attr.read_text(encoding='utf-8')
section='''\n## v3.5 — Международный мир бронзового века\n\nЛокальные SVG-обложки 120 карточек и обложка пака созданы для проекта Codex of History. Историческая проверка и ссылки карточек используют материалы The Metropolitan Museum of Art, British Museum, Institute of Nautical Archaeology и UCL Archaeology. Динамические исторические изображения по-прежнему подбираются через Wikimedia только для видимых карточек и не сохраняются после завершения сессии.\n'''
if '## v3.5 — Международный мир' not in at:at+=section
attr.write_text(at,encoding='utf-8')
print('integrated v3.5')
