#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='4.3.0'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for key,vals in [
 ('cards',['data/cards/archaic-greece/story.json','data/cards/archaic-greece/archive.json']),
 ('pools',['data/campaigns/archaic-greece/pools.json']),
 ('quizzes',['data/quizzes/archaic-greece/campaign.json']),
 ('stories',['data/stories/archaic-greece/personal.json']),
 ('lessons',['data/lessons/archaic-greece/campaign.json']),
 ('campaigns',['data/campaigns/archaic-greece/campaign.json'])]:
 for x in vals:
  if x not in d[key]:d[key].append(x)
d['maps']['GREECE_ARCHAIC']='data/maps/archaic-greece.json'
script='js/features/v4-3-archaic-greece.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js');m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));add=load(Path('data/core/relations-v43-archaic-greece.json'));existing={x['id'] for x in rels};rels.extend(x for x in add if x['id'] not in existing);dump(Path('data/core/relations.json'),rels);(ROOT/'data/core/relations-v43-archaic-greece.json').unlink(missing_ok=True)

world=load(Path('data/world/campaigns.json'));camp=load(Path('data/campaigns/archaic-greece/campaign.json'))
for c in world:
 if c['id']=='GREECE_ARCHAIC':
  c.update({'title':'Архаическая Греция','subtitle':'Полисы, колонии и реформы','period':'ок. 1100–480 до н. э.','chapterCount':10,'releasedChapters':10,'status':'PLAYABLE','region':'Эгейский и Средиземноморский мир','description':'От раннего железного века и рождения полисов до колонизации, Спарты, Афин, реформ и архаического искусства.','chapters':[{'number':x['number'],'title':x['title']} for x in camp['chapters']]})
dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_IRON' and 'GREECE_ARCHAIC' not in e['campaignIds']:e['campaignIds'].append('GREECE_ARCHAIC')
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'))
new=[
 {'year':-1050,'label':'Протогеометрический период в Греции','detail':'Новые керамические стили и дальние контакты показывают перестройку постдворцового мира.','campaignId':'GREECE_ARCHAIC','sourcePatch':'v4.3'},
 {'year':-900,'label':'Начало геометрического периода','detail':'Поселения, погребения и святилища становятся крупнее и заметнее.','campaignId':'GREECE_ARCHAIC','sourcePatch':'v4.3'},
 {'year':-800,'label':'Ранние полисы и греческий алфавит','detail':'Гражданские общины и алфавитные надписи развиваются в разных регионах.','campaignId':'GREECE_ARCHAIC','sourcePatch':'v4.3'},
 {'year':-776,'label':'Традиционная дата первой Олимпиады','detail':'Поздняя хронография использовала Олимпиады как систему датировки.','campaignId':'GREECE_ARCHAIC','sourcePatch':'v4.3'},
 {'year':-734,'label':'Традиционное основание Сиракуз','detail':'Коринфские переселенцы создают крупный полис на Сицилии.','campaignId':'GREECE_ARCHAIC','sourcePatch':'v4.3'},
 {'year':-650,'label':'Распространение тираний и письменных законов','detail':'Полисы отвечают на социальные конфликты разными политическими формами.','campaignId':'GREECE_ARCHAIC','sourcePatch':'v4.3'},
 {'year':-600,'label':'Основание Массалии и расширение западных сетей','detail':'Греческие поселения укрепляются на западном Средиземноморье.','campaignId':'GREECE_ARCHAIC','sourcePatch':'v4.3'},
 {'year':-594,'label':'Традиционная дата реформ Солона','detail':'Долговые и политические конфликты Аттики получают новый правовой ответ.','campaignId':'GREECE_ARCHAIC','sourcePatch':'v4.3'},
 {'year':-546,'label':'Укрепление власти Писистрата в Афинах','detail':'Тирания сочетает единоличную власть с развитием культов и города.','campaignId':'GREECE_ARCHAIC','sourcePatch':'v4.3'},
 {'year':-508,'label':'Реформы Клисфена','detail':'Демы и новые филы перестраивают афинскую гражданскую общину.','campaignId':'GREECE_ARCHAIC','sourcePatch':'v4.3'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

manifest=load(Path('data/image_manifest.json'));existing={x['cardId']:x for x in manifest.get('images',[])}
for c in load(Path('data/cards/archaic-greece/story.json'))+load(Path('data/cards/archaic-greece/archive.json')):
 existing[c['id']]={'cardId':c['id'],'local':c['image']['local'],'file':c['image']['file'],'kind':'project-cover','prefer_remote':False,'caption':c['image']['caption'],'credit':c['image']['credit'],'source_url':c['image']['source_url'],'license':c['image']['license']}
images=list(existing.values());historical=sum(1 for x in images if x.get('prefer_remote'))
manifest.update({'version':V,'generatedAt':'2026-07-14','count':len(images),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(images)-historical,'dynamicQueryCount':len(images)-historical,'images':images});dump(Path('data/image_manifest.json'),manifest)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v4.3

## v4.4 — Чжоу и Сражающиеся царства

Следующий патч продолжит железный век в Китае.

Основные задачи:

- завоевание Шан и Западная Чжоу;
- мандат Неба и ритуальная власть;
- ослабление царского центра;
- эпоха Вёсен и Осеней;
- Конфуций и конкурирующие интеллектуальные традиции;
- Сражающиеся царства, реформы и бюрократия;
- карта царств, архивные пулы, пак и личные истории.
''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v4_3.md').write_text('''# Patch v4.3.0 — Архаическая Греция

- 10 глав, 60 миссий и 120 карточек.
- Ранний железный век, геометрический период и формирование полисов.
- Греческий алфавит, эпическая и лирическая традиция.
- Олимпия, Дельфы и общегреческие связи.
- Колонизация Средиземноморья и Чёрного моря.
- Законы, тирании, гоплиты, Спарта и Афины.
- Архаическое искусство и переход к классической эпохе.
- 10 архивных пулов, 10 личных историй, карта и отдельный пак.
''',encoding='utf-8')
(ROOT/'docs/QA_v4_3.md').write_text('''# QA v4.3.0

Проверяется:

- 120 новых карточек: 80 сюжетных и 40 архивных;
- 60 миссий и 60 уроков;
- 14 квизов, 10 пулов и 10 личных историй;
- старт новой игры только с ARC_S_01_01–03;
- пак кампании выдаёт только ARC_A_*;
- карта Эгейского и Средиземноморского мира;
- четыре модуля итогового экзамена;
- разделение археологии, надписей, изображений и поздней традиции;
- версии manifest, runtime, Service Worker и package metadata.
''',encoding='utf-8')

p=ROOT/'README.md';txt=p.read_text(encoding='utf-8');txt=re.sub(r'^# Codex of History v[^\n]+','# Codex of History v4.3.0',txt,count=1,flags=re.M)
section='''\n## v4.3.0 — Архаическая Греция\n\n- 10 глав, 60 миссий и 120 карточек.\n- Полисы, алфавит, святилища, колонизация, законы, Спарта и Афины.\n- Археология, надписи, изображения и поздняя традиция разделены по типу свидетельства.\n- Релизный ZIP содержит только изменённые и новые файлы.\n\n'''
if '## v4.3.0' not in txt:txt=txt.replace('\n',section,1)
p.write_text(txt,encoding='utf-8')
attr=ROOT/'ATTRIBUTION.md';at=attr.read_text(encoding='utf-8');section='''\n## v4.3 — Архаическая Греция\n\nЛокальные SVG-обложки 120 карточек и вертикальная обложка пака созданы для Codex of History. Источники карточек используют материалы The Metropolitan Museum of Art по геометрическому и архаическому искусству, колонизации, архитектуре, религии, вазописи и Спарте. Динамические исторические изображения загружаются только для видимых карточек и живут до конца текущей сессии.\n'''
if '## v4.3 — Архаическая Греция' not in at:at+=section
attr.write_text(at,encoding='utf-8')

for path in (ROOT/'js').rglob('*.js'):
 text=path.read_text(encoding='utf-8').replace('4.2.0',V)
 path.write_text(text,encoding='utf-8')
for path in (ROOT/'tools').glob('*.mjs'):
 text=path.read_text(encoding='utf-8').replace('4.2.0',V).replace('1955','2075').replace('1913','2033')
 path.write_text(text,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V
if 'node tools/smoke-v43-archaic-greece.mjs' not in pkg['scripts']['test']:
 pkg['scripts']['test']+=' && node tools/smoke-v43-archaic-greece.mjs && node tools/runtime-v43-archaic-greece.mjs'
pkg['scripts']['test:v43']='node tools/smoke-v43-archaic-greece.mjs && node tools/runtime-v43-archaic-greece.mjs';dump(Path('package.json'),pkg)

for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;text=p.read_text(encoding='utf-8').replace('4.2.0',V).replace('codex-v4.2.0','codex-v4.3.0')
 p.write_text(text,encoding='utf-8')
p=ROOT/'sw.js';text=p.read_text(encoding='utf-8')
if "'./assets/packs/archaic-greece-pack.svg'" not in text:text=text.replace("'./assets/packs/israel-judah-pack.svg',","'./assets/packs/israel-judah-pack.svg','./assets/packs/archaic-greece-pack.svg',")
if "'./js/features/v4-3-archaic-greece.js'" not in text:text=text.replace("'./js/features/v4-2-israel-judah.js',","'./js/features/v4-2-israel-judah.js','./js/features/v4-3-archaic-greece.js',")
p.write_text(text,encoding='utf-8')
print('integrated v4.3')
