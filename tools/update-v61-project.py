#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='6.1.0'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Manifest.
m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for path in ['data/lessons/rome/chapter_04.json','data/lessons/rome/chapter_05.json','data/lessons/rome/chapter_06.json']:
 if path not in d['lessons']:d['lessons'].insert(3,path)
for path in ['data/quizzes/rome/chapter_04.json','data/quizzes/rome/chapter_05.json','data/quizzes/rome/chapter_06.json']:
 if path not in d['quizzes']:d['quizzes'].insert(3,path)
script='js/features/v6-1-rome-middle.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js') if 'js/features/v3-1-1-hotfix.js' in m['scripts'] else len(m['scripts'])
 m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

# World catalog.
world=load(Path('data/world/campaigns.json'))
rome=next(c for c in world if c['id']=='ROME_CAMPAIGN')
rome.update({'title':'Рим','subtitle':'От города в Лации к средиземноморской республике','period':'VIII век до н. э. – V век н. э.','chapterCount':12,'releasedChapters':6,'status':'PLAYABLE','region':'Италия и Средиземноморье','description':'Шесть опубликованных глав: основание, Республика, завоевание Италии, Пунические войны, восточные кампании и устройство средней Республики.'})
rome['chapters']=[{'number':i,'title':t} for i,t in enumerate(['Рождение Рима','Рождение Республики','Борьба за Италию','Пунические войны','Завоевание эллинистического мира','Как работала Республика','Гракхи и социальный кризис','Марий и Сулла','Цезарь и гражданская война','Август и Империя','Расцвет Империи','Кризис и падение Запада'],1)]
dump(Path('data/world/campaigns.json'),world)

# Timeline.
wt=load(Path('data/world/timeline.json'));new=[
 {'year':-264,'label':'Начало Первой Пунической войны','detail':'Конфликт вокруг Мессаны превращается в долгую борьбу Рима и Карфагена за Сицилию.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.1'},
 {'year':-241,'label':'Эгатские острова и первая провинция','detail':'Морская победа завершает войну; Сицилия становится первой устойчивой провинциальной территорией Рима.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.1'},
 {'year':-218,'label':'Ганнибал переходит Альпы','detail':'Вторая Пуническая война переносится в Италию.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.1'},
 {'year':-216,'label':'Катастрофа при Каннах','detail':'Ганнибал уничтожает крупную римскую армию, но союзная система Республики не распадается полностью.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.1'},
 {'year':-202,'label':'Битва при Заме','detail':'Сципион побеждает армию Ганнибала в Африке.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.1'},
 {'year':-197,'label':'Киноскефалы','detail':'Римская армия разбивает Филиппа V; Республика усиливает влияние в греческом мире.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.1'},
 {'year':-188,'label':'Апамейский мир','detail':'Антиох III лишается владений в Малой Азии, а римские союзники получают новые территории.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.1'},
 {'year':-168,'label':'Пидна и конец Антигонидов','detail':'Победа над Персеем ликвидирует македонскую монархию.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.1'},
 {'year':-146,'label':'Коринф и Карфаген','detail':'Рим разрушает два крупных центра сопротивления и оформляет новые провинциальные порядки.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.1'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

# Pack metadata version.
packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

# Rebuild image manifest from all registered cards, preserving remote historical images.
im=load(Path('data/image_manifest.json'));entries=[]
manifest=load(Path('data/content-manifest.json'))
for path in manifest['datasets']['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {}
  entries.append({'cardId':c['id'],'local':image.get('local','assets/ui/fallback-card.svg'),'file':image.get('file',Path(image.get('local','fallback.svg')).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x.get('prefer_remote'))
im.update({'version':V,'generatedAt':'2026-07-15','count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

# Image resolver generator version.
p=ROOT/'tools/build-image-queries.py';txt=p.read_text(encoding='utf-8');txt=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',txt,count=1);p.write_text(txt,encoding='utf-8')

# Documentation.
(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v6.1\n\n## v6.2 — Рим: главы 7–9\n\n- Гракхи и социальный кризис;\n- Марий, союзнический вопрос и Сулла;\n- Цезарь, Помпей и гражданская война;\n- новые карты, теория, архивные пулы и контрольная точка поздней Республики.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v6_1.md').write_text('''# Patch v6.1.0 — Рим: главы 4–6\n\n- Пунические войны, восточные завоевания и устройство средней Республики.\n- 3 главы, 18 миссий и 36 карточек.\n- 3 архивных пула, 3 личные истории и контрольный экзамен из четырёх модулей.\n- Карта расширена от Иберии и Карфагена до Македонии и Малой Азии.\n''',encoding='utf-8')
(ROOT/'docs/QA_v6_1.md').write_text('''# QA v6.1.0\n\n- Проверены 24 сюжетные и 12 архивных карточек.\n- Проверены 18 миссий, 18 уроков, 3 главы и 7 квизов.\n- Проверены старт старого и нового профиля, римские архивные пулы, карта и контрольный экзамен.\n- Проверены связи с финикийской и эллинистической кампаниями.\n''',encoding='utf-8')

# README and attribution.
p=ROOT/'README.md';text=p.read_text(encoding='utf-8');text=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',text,count=1,flags=re.M)
block='''\n## v6.1.0 — Рим: главы 4–6\n\n- Пунические войны, завоевание эллинистического мира и устройство средней Республики.\n- 3 главы, 18 миссий и 36 карточек.\n- Patch-only архив.\n\n'''
if '## v6.1.0' not in text:text=text.replace('\n',block,1)
p.write_text(text,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';text=p.read_text(encoding='utf-8');block='''\n\n## v6.1 — Рим: главы 4–6\n\nЛокальные SVG-обложки новых карточек созданы для Codex of History. Источники: Metropolitan Museum of Art, British Museum и Perseus Digital Library. Пять ранее подготовленных исторических изображений Пунических войн сохранены с исходной атрибуцией Wikimedia Commons.\n'''
if '## v6.1 —' not in text:text+=block
p.write_text(text,encoding='utf-8')

# Package metadata and tests.
pkg=load(Path('package.json'));pkg['version']=V
append='node tools/smoke-v61-rome-middle.mjs && node tools/runtime-v61-rome-middle.mjs'
if 'smoke-v61-rome-middle.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && '+append
pkg['scripts']['test:v61']=append;dump(Path('package.json'),pkg)

# Version consistency in runtime files and current smoke tests.
for path in (ROOT/'js').rglob('*.js'):
 text=path.read_text(encoding='utf-8').replace('6.0.0',V);path.write_text(text,encoding='utf-8')
for path in (ROOT/'tools').glob('*.mjs'):
 text=path.read_text(encoding='utf-8').replace('6.0.0',V).replace('2987','3018').replace('2945','2976')
 path.write_text(text,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;text=p.read_text(encoding='utf-8').replace('6.0.0',V).replace('codex-v6.0.0','codex-v6.1.0');p.write_text(text,encoding='utf-8')
# Ensure the new runtime module is precached.
p=ROOT/'sw.js';text=p.read_text(encoding='utf-8')
if "'./js/features/v6-1-rome-middle.js'" not in text:
 text=text.replace("'./js/features/v6-0-hellenistic.js',","'./js/features/v6-0-hellenistic.js','./js/features/v6-1-rome-middle.js',")
p.write_text(text,encoding='utf-8')
print('integrated v6.1 metadata and runtime')
