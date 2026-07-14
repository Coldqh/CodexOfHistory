#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='4.0.0'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for key,vals in [
 ('cards',['data/cards/assyria-babylon/story.json','data/cards/assyria-babylon/archive.json']),
 ('pools',['data/campaigns/assyria-babylon/pools.json']),
 ('quizzes',['data/quizzes/assyria-babylon/campaign.json']),
 ('stories',['data/stories/assyria-babylon/personal.json']),
 ('lessons',['data/lessons/assyria-babylon/campaign.json']),
 ('campaigns',['data/campaigns/assyria-babylon/campaign.json'])]:
 for x in vals:
  if x not in d[key]:d[key].append(x)
d['maps']['ASSYRIA_BABYLON']='data/maps/assyria-babylon.json'
script='js/features/v4-0-assyria-babylon.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js');m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));add=load(Path('data/core/relations-v40-assyria.json'));existing={x['id'] for x in rels};rels.extend(x for x in add if x['id'] not in existing);dump(Path('data/core/relations.json'),rels);(ROOT/'data/core/relations-v40-assyria.json').unlink(missing_ok=True)

world=load(Path('data/world/campaigns.json'));camp=load(Path('data/campaigns/assyria-babylon/campaign.json'))
for c in world:
 if c['id']=='ASSYRIA_BABYLON':
  c.update({'title':'Ассирия и Нововавилонское царство','subtitle':'Имперская машина железного века','period':'ок. 1100–539 до н. э.','chapterCount':10,'releasedChapters':10,'status':'PLAYABLE','region':'Месопотамия, Анатолия и Левант','description':'От восстановления Ассирии до провинциальной империи, Ниневии, падения державы и Нововавилонского царства.','chapters':[{'number':x['number'],'title':x['title']} for x in camp['chapters']]})
dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_IRON' and 'ASSYRIA_BABYLON' not in e['campaignIds']:e['campaignIds'].insert(0,'ASSYRIA_BABYLON')
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'))
new=[
 {'year':-1050,'label':'Ассирия сохраняет ядро после бронзового кризиса','detail':'Города вокруг Ашшура поддерживают царскую и храмовую традицию в раздробленном мире раннего железного века.','campaignId':'ASSYRIA_BABYLON','sourcePatch':'v4.0'},
 {'year':-883,'label':'Ашшурнацирапал II начинает перестройку Кальху','detail':'Новая столица становится административным центром и сценой дворцовой идеологии.','campaignId':'ASSYRIA_BABYLON','sourcePatch':'v4.0'},
 {'year':-744,'label':'Начало правления Тиглатпаласара III','detail':'Реформы усиливают постоянную армию и прямое провинциальное управление.','campaignId':'ASSYRIA_BABYLON','sourcePatch':'v4.0'},
 {'year':-722,'label':'Саргон II и падение Самарии','detail':'Ассирийская власть расширяется в Леванте, а зависимые царства превращаются в провинции.','campaignId':'ASSYRIA_BABYLON','sourcePatch':'v4.0'},
 {'year':-701,'label':'Поход Синаххериба в Иудею','detail':'Осада Лахиша известна по царским надписям, рельефам и другим историческим традициям.','campaignId':'ASSYRIA_BABYLON','sourcePatch':'v4.0'},
 {'year':-671,'label':'Асархаддон захватывает Мемфис','detail':'Ассирия достигает максимального территориального охвата, но удерживает Египет недолго.','campaignId':'ASSYRIA_BABYLON','sourcePatch':'v4.0'},
 {'year':-612,'label':'Падение Ниневии','detail':'Вавилонские и мидийские силы уничтожают главный центр поздней Ассирии.','campaignId':'ASSYRIA_BABYLON','sourcePatch':'v4.0'},
 {'year':-605,'label':'Битва при Каркемише','detail':'Вавилонская победа закрепляет контроль над значительной частью Сирии и Леванта.','campaignId':'ASSYRIA_BABYLON','sourcePatch':'v4.0'},
 {'year':-586,'label':'Вавилонское завоевание Иерусалима','detail':'Навуходоносор II подавляет восстание Иудеи и проводит депортации.','campaignId':'ASSYRIA_BABYLON','sourcePatch':'v4.0'},
 {'year':-539,'label':'Вавилон переходит под власть Кира II','detail':'Нововавилонское царство включается в Ахеменидскую державу.','campaignId':'ASSYRIA_BABYLON','sourcePatch':'v4.0'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

# Rebuild image manifest while preserving the 42 fixed historical images.
manifest=load(Path('data/image_manifest.json'))
existing={x['cardId']:x for x in manifest.get('images',[])}
for c in load(Path('data/cards/assyria-babylon/story.json'))+load(Path('data/cards/assyria-babylon/archive.json')):
 existing[c['id']]={'cardId':c['id'],'local':c['image']['local'],'file':c['image']['file'],'kind':'project-cover','prefer_remote':False,'caption':c['image']['caption'],'credit':c['image']['credit'],'source_url':c['image']['source_url'],'license':c['image']['license']}
images=list(existing.values());historical=sum(1 for x in images if x.get('prefer_remote'))
manifest.update({'version':V,'generatedAt':'2026-07-14','count':len(images),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(images)-historical,'dynamicQueryCount':len(images)-historical,'images':images});dump(Path('data/image_manifest.json'),manifest)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v4.0

## v4.1 — Финикийцы и западное Средиземноморье

Следующий патч продолжит железный век через города Леванта и морские сети.

Основные задачи:

- Тир, Сидон, Библ и Арвад;
- алфавитные письменности железного века;
- торговые маршруты, ремесло и пурпур;
- Кипр, Северная Африка, Сардиния и Иберия;
- ранний Карфаген без перехода к Пуническим войнам;
- взаимодействие с Ассирией и Вавилонией;
- отдельная морская карта, паки и личные истории.
''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v4_0.md').write_text('''# Patch v4.0.0 — Ассирия и Нововавилонское царство

- Открыта Эпоха III — Железный век.
- 10 глав, 60 миссий и 120 карточек.
- Раннее восстановление Ассирии, Кальху, провинции, дороги и депортации.
- Армия, осады, Тиглатпаласар III, Саргон II, Синаххериб и Ниневия.
- Асархаддон, Ашшурбанипал, библиотека и поздние войны.
- Падение Ассирии и Нововавилонское царство до 539 года до н. э.
- 10 архивных пулов, 10 личных историй и отдельный пак.
- Карта Месопотамии, Леванта, Египта и Элама.
- Итоговый экзамен из четырёх модулей.
''',encoding='utf-8')
(ROOT/'docs/QA_v4_0.md').write_text('''# QA v4.0.0

Проверяется:

- 120 новых карточек: 80 сюжетных и 40 архивных;
- 60 миссий и 60 уроков;
- 14 квизов, 10 пулов и 10 личных историй;
- старт новой игры только с ASB_S_01_01–03;
- пак кампании выдаёт только ASB_A_*;
- Эпоха III открыта без отдельного промо-блока;
- карта Ашшура, Кальху, Дур-Шаррукина, Ниневии, Лахиша, Вавилона и Иерусалима;
- четыре модуля итогового экзамена;
- все локальные SVG имеют уникальные пути;
- версии manifest, runtime, Service Worker и package metadata.
''',encoding='utf-8')

p=ROOT/'README.md';txt=p.read_text(encoding='utf-8');txt=re.sub(r'^# Codex of History v[^\n]+','# Codex of History v4.0.0',txt,count=1,flags=re.M)
section='''\n## v4.0.0 — Ассирия и Нововавилонское царство\n\n- Открыта третья эпоха — Железный век.\n- 10 глав, 60 миссий и 120 карточек.\n- Ассирийские столицы, провинции, армия, дороги, депортации и архивы.\n- Падение Ниневии и Нововавилонская держава до 539 года до н. э.\n- Релизный ZIP содержит только изменённые и новые файлы.\n\n'''
if '## v4.0.0' not in txt:txt=txt.replace('\n',section,1)
p.write_text(txt,encoding='utf-8')
attr=ROOT/'ATTRIBUTION.md';at=attr.read_text(encoding='utf-8');section='''\n## v4.0 — Ассирия и Нововавилонское царство\n\nЛокальные SVG-обложки 120 карточек и вертикальная обложка пака созданы для Codex of History. Историческая проверка и ссылки карточек используют материалы The Metropolitan Museum of Art и British Museum по Ассирии, Нимруду, Ниневии, Лахишским рельефам, библиотеке Ашшурбанипала и Вавилону. Динамические исторические изображения загружаются только для видимых карточек и живут до конца текущей сессии.\n'''
if '## v4.0 — Ассирия' not in at:at+=section
attr.write_text(at,encoding='utf-8')

# Core version surfaces.
for path in (ROOT/'js').rglob('*.js'):
 text=path.read_text(encoding='utf-8').replace('3.7.0',V)
 path.write_text(text,encoding='utf-8')
for path in (ROOT/'tools').glob('*.mjs'):
 text=path.read_text(encoding='utf-8').replace('3.7.0',V).replace('1595','1715').replace('1553','1673')
 path.write_text(text,encoding='utf-8')

# Package metadata and browser entry points.
pkg=load(Path('package.json'));pkg['version']=V
if 'node tools/smoke-v40-assyria.mjs' not in pkg['scripts']['test']:
 pkg['scripts']['test']+=' && node tools/smoke-v40-assyria.mjs && node tools/runtime-v40-assyria.mjs'
pkg['scripts']['test:v40']='node tools/smoke-v40-assyria.mjs && node tools/runtime-v40-assyria.mjs';dump(Path('package.json'),pkg)

for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;text=p.read_text(encoding='utf-8').replace('3.7.0',V).replace('codex-v3.7.0','codex-v4.0.0')
 p.write_text(text,encoding='utf-8')
# Ensure new feature and pack are precached.
p=ROOT/'sw.js';text=p.read_text(encoding='utf-8')
if "'./assets/packs/assyria-babylon-pack.svg'" not in text:text=text.replace("'./assets/packs/bronze-era-pack.svg',","'./assets/packs/bronze-era-pack.svg','./assets/packs/assyria-babylon-pack.svg',")
if "'./js/features/v4-0-assyria-babylon.js'" not in text:text=text.replace("'./js/features/v3-7-bronze-world.js',","'./js/features/v3-7-bronze-world.js','./js/features/v4-0-assyria-babylon.js',")
p.write_text(text,encoding='utf-8')
print('integrated v4.0')
