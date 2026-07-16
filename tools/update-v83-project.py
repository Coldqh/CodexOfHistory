#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='8.3.0';OLD='8.2.0';CHECKED='2026-07-16'

def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Content registry.
m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={
 'cards':['data/cards/byzantium-macedonian/story.json','data/cards/byzantium-macedonian/archive.json'],
 'campaigns':['data/campaigns/byzantium-macedonian/campaign.json'],
 'pools':['data/campaigns/byzantium-macedonian/pools.json'],
 'quizzes':['data/quizzes/byzantium-macedonian/campaign.json'],
 'stories':['data/stories/byzantium-macedonian/personal.json'],
 'lessons':['data/lessons/byzantium-macedonian/campaign.json'],
}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['BYZANTIUM_MACEDONIAN']='data/maps/byzantium-macedonian.json'
script='js/features/v8-3-byzantium-macedonian.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

# Relations.
rels=load(Path('data/core/relations.json'));rels=[r for r in rels if not re.fullmatch(r'REL_BYM_\d{4}',r.get('id',''))]
new=load(Path('data/core/relations-830-byzantium-macedonian.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

# Campaign catalogue and era membership.
world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/byzantium-macedonian/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
entry={'id':'BYZANTIUM_MACEDONIAN','eraId':'ERA_EARLY_MEDIEVAL','order':40,'title':'Византия: от иконоборчества до Василия II','subtitle':'Фемы, изображения, миссии и имперское расширение','period':'641–1025 годы','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Восточная Римская империя, Балканы и Анатолия','description':'Территориальный кризис VII века, фемная перестройка, две эпохи иконоборчества, славянские миссии, Македонская династия, возвращение Крита и Антиохии и правление Василия II.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]}
world=[c for c in world if c['id']!='BYZANTIUM_MACEDONIAN'];world.append(entry);world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)
eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_EARLY_MEDIEVAL':
  ids=[x for x in e.get('campaignIds',[]) if x!='BYZANTIUM_MACEDONIAN'];e['campaignIds']=ids+['BYZANTIUM_MACEDONIAN'];e['status']='PLAYABLE'
  e['description']='Аббасидский Багдад и средневековая Восточная Римская империя открывают эпоху региональных империй, религиозных институтов, письменных культур, морских и сухопутных сетей VIII–XI веков.'
dump(Path('data/world/eras.json'),eras)

# Timeline.
wt=load(Path('data/world/timeline.json'));events=[
 {'year':641,'label':'Начало эпохи Восточной Римской империи меньшего масштаба','detail':'После смерти Ираклия и арабских завоеваний Анатолия становится главным ядром государства.','campaignId':'BYZANTIUM_MACEDONIAN','sourcePatch':'v8.3'},
 {'year':718,'label':'Конец осады Константинополя','detail':'Стены, флот, снабжение, погода и болгарское давление срывают омейядскую операцию.','campaignId':'BYZANTIUM_MACEDONIAN','sourcePatch':'v8.3'},
 {'year':754,'label':'Иконоборческий собор в Иерии','detail':'Императорская церковная политика получает соборную формулировку.','campaignId':'BYZANTIUM_MACEDONIAN','sourcePatch':'v8.3'},
 {'year':787,'label':'Второй Никейский собор','detail':'Собор восстанавливает почитание икон и различает почитание образа и поклонение Богу.','campaignId':'BYZANTIUM_MACEDONIAN','sourcePatch':'v8.3'},
 {'year':843,'label':'Восстановление почитания икон','detail':'Регентство Феодоры завершает вторую эпоху иконоборчества.','campaignId':'BYZANTIUM_MACEDONIAN','sourcePatch':'v8.3'},
 {'year':863,'label':'Миссия Кирилла и Мефодия в Моравию','detail':'Славянская письменность и литургический перевод становятся частью международной церковной политики.','campaignId':'BYZANTIUM_MACEDONIAN','sourcePatch':'v8.3'},
 {'year':867,'label':'Начало Македонской династии','detail':'Василий I захватывает престол после убийства Михаила III.','campaignId':'BYZANTIUM_MACEDONIAN','sourcePatch':'v8.3'},
 {'year':961,'label':'Возвращение Крита','detail':'Экспедиция Никифора Фоки ликвидирует Критский эмират и меняет безопасность Эгейского моря.','campaignId':'BYZANTIUM_MACEDONIAN','sourcePatch':'v8.3'},
 {'year':969,'label':'Возвращение Антиохии','detail':'Восточное наступление достигает одного из крупнейших городов Сирии.','campaignId':'BYZANTIUM_MACEDONIAN','sourcePatch':'v8.3'},
 {'year':1014,'label':'Битва при Клидионе','detail':'Важная победа Василия II ускоряет завершение долгой войны с державой Самуила.','campaignId':'BYZANTIUM_MACEDONIAN','sourcePatch':'v8.3'},
 {'year':1018,'label':'Присоединение Болгарии','detail':'Империя включает болгарские земли, сохраняя часть местных церковных и налоговых порядков.','campaignId':'BYZANTIUM_MACEDONIAN','sourcePatch':'v8.3'},
 {'year':1025,'label':'Смерть Василия II','detail':'Империя достигает широких границ, но остаётся без устойчивого наследника.','campaignId':'BYZANTIUM_MACEDONIAN','sourcePatch':'v8.3'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

# Image query group.
p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "BYZANTIUM_MACEDONIAN": {' not in s:
 marker='    "FRANKS_TRANSITION": {';i=s.index(marker)
 group='''    "BYZANTIUM_MACEDONIAN": {\n        "terms": ["Byzantine Iconoclasm", "Leo III", "Constantine V", "Nicaea 787", "Empress Theodora", "Photios", "Cyril Methodius", "Macedonian dynasty", "Nikephoros Phokas", "Basil II", "Byzantine seal manuscript"],\n        "base": [("ru", "Византия иконоборчество Василий II"), ("en", "Byzantine Iconoclasm Macedonian dynasty Basil II"), ("en", "Byzantine manuscript seal icon 8th 11th century")],\n    },\n'''
 s=s[:i]+group+s[i:]
old='("/franks-transition/", "FRANKS_TRANSITION"),'
if '("/byzantium-macedonian/", "BYZANTIUM_MACEDONIAN")' not in s:
 if old not in s:raise SystemExit('image marker missing')
 s=s.replace(old,'("/byzantium-macedonian/", "BYZANTIUM_MACEDONIAN"), '+old)
p.write_text(s,encoding='utf-8')

# Rebuild image manifest from content registry.
entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg')
  entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

# Runtime versions and PWA.
for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v8.2.0','codex-v8.3.0').replace('codex-v8\\.2\\.0','codex-v8\\.3\\.0')
 if rel=='index.html':t=re.sub(r'js/bootstrap\.js\?v=[0-9.]+',f'js/bootstrap.js?v={V}',t)
 p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v8-3-byzantium-macedonian.js'" not in t:t=t.replace("'./js/features/v8-2-franks-transition.js'","'./js/features/v8-2-franks-transition.js','./js/features/v8-3-byzantium-macedonian.js'")
if "'./assets/packs/byzantium-macedonian-pack.svg'" not in t:t=t.replace("'./assets/packs/franks-transition-pack.svg'","'./assets/packs/franks-transition-pack.svg','./assets/packs/byzantium-macedonian-pack.svg'")
p.write_text(t,encoding='utf-8')

# Bring old test expectations to current totals/version.
for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'8\.2\.0',r'8\.3\.0').replace('5391','5523').replace('5349','5481').replace('2593','2659')
 p.write_text(t,encoding='utf-8')

# Update the previous era-reorganisation smoke expectation after adding a second Early Medieval campaign.
p=ROOT/'tools/smoke-v82-franks-transition.mjs'
t=p.read_text(encoding='utf-8').replace("assert.deepEqual(early.campaignIds,['ABBASID_BAGHDAD'])","assert.deepEqual(early.campaignIds,['ABBASID_BAGHDAD','BYZANTIUM_MACEDONIAN'])")
p.write_text(t,encoding='utf-8')

# Documentation.
(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v8.3\n\n## v8.4 — Викинги и Северная Атлантика\n\n- Скандинавия VIII века и устройство обществ;\n- корабли, навигация, торговля и набеги;\n- Англия, Ирландия, Нормандия и восточные маршруты;\n- Исландия, Гренландия и Винланд;\n- королевская власть и христианизация Скандинавии.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v8_3.md').write_text('''# Patch v8.3.0 — Византия: от иконоборчества до Василия II\n\n- 11 глав, 66 миссий и 132 карточки.\n- Территориальная перестройка после 641 года и формирование фем.\n- Осада 717–718 годов и правление Льва III.\n- Две эпохи иконоборчества, Никея II и восстановление икон в 843 году.\n- Фотий, Кирилл и Мефодий, христианизация Болгарии и славянская книжность.\n- Македонская династия, право, двор, возвращение Крита и Антиохии.\n- Василий II, Болгария и империя 1025 года без мифа о безусловной вершине.\n''',encoding='utf-8')
(ROOT/'docs/QA_v8_3.md').write_text('''# QA v8.3.0\n\n- Проверены 88 сюжетных и 44 архивных карточки.\n- Проверены 66 миссий, 66 уроков, 11 глав, 11 пулов и 11 личных историй.\n- Проверены карта, четыре фазы, архивный пак и четыре модуля итогового экзамена.\n- Проверены уникальность ID и названий относительно кампании Восточной Римской империи v7.1.\n- Проверены межкампанийные связи с ранним исламом, Аббасидами, франками, Китаем и Центральной Азией.\n- Проверены миграция сейва, коллекция, прямые кнопки этапов урока и PWA-кэш.\n''',encoding='utf-8')
p=ROOT/'README.md';s=p.read_text(encoding='utf-8');s=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',s,count=1,flags=re.M);block='''\n## v8.3.0 — Византия: от иконоборчества до Василия II\n\n- 11 глав, 66 миссий и 132 карточки.\n- Полная линия Восточной Римской империи от кризиса VII века до 1025 года.\n- Фемы, иконоборчество, славянские миссии, Македонская династия и Василий II.\n- Patch-only архив.\n\n'''
if '## v8.3.0' not in s:s=s.replace('\n',block,1)
p.write_text(s,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';s=p.read_text(encoding='utf-8');block='''\n\n## v8.3 — Византия: от иконоборчества до Василия II\n\nЛокальные SVG-обложки 132 карточек и кампанийного пака созданы для Codex of History. Источниковая рамка опирается на Encyclopaedia Britannica, UNESCO Paleochristian and Byzantine Monuments of Thessalonika, Metropolitan Museum of Art и исследовательские материалы Dumbarton Oaks по византийским печатям, рукописям и праву.\n'''
if '## v8.3 —' not in s:s+=block
p.write_text(s,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test:v83']='node tools/smoke-v83-byzantium-macedonian.mjs && node tools/runtime-v83-byzantium-macedonian.mjs'
if 'tools/smoke-v83-byzantium-macedonian.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v83-byzantium-macedonian.mjs && node tools/runtime-v83-byzantium-macedonian.mjs'
dump(Path('package.json'),pkg)
print('integrated v8.3 Byzantine campaign')
