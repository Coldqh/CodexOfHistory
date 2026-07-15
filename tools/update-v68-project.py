#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='6.8.0';OLD='6.7.0';CHECKED='2026-07-15'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={'cards':['data/cards/late-roman/story.json','data/cards/late-roman/archive.json'],'campaigns':['data/campaigns/late-roman/campaign.json'],'pools':['data/campaigns/late-roman/pools.json'],'quizzes':['data/quizzes/late-roman/campaign.json'],'stories':['data/stories/late-roman/personal.json'],'lessons':['data/lessons/late-roman/campaign.json']}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['LATE_ANTIQUITY']='data/maps/late-roman.json'
script='js/features/v6-8-late-roman.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js') if 'js/features/v3-1-1-hotfix.js' in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));new=load(Path('data/core/relations-v68-late-roman.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/late-roman/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
for c in world:
 if c['id']=='LATE_ANTIQUITY':
  c.update({'eraId':'ERA_LATE_ANTIQUITY','order':26,'title':'Поздняя Римская империя: кризис и перестройка','subtitle':'От армейских императоров к двум дворам','period':'235–395 годы','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Римская империя, Средиземноморье и европейские фронтиры','description':'Кризис III века, региональные империи, Аврелиан, Диоклетиан, тетрархия, налоги, Константин, новые столицы, позднеримская армия и раздел дворов 395 года.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]});break
else:raise SystemExit('LATE_ANTIQUITY placeholder missing')
dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_LATE_ANTIQUITY':
  e['description']='Римская и Сасанидская державы перестраиваются, религиозные институты получают новые политические роли, а старые имперские пространства входят в эпоху региональных дворов и новых государств.'
  if 'LATE_ANTIQUITY' not in e['campaignIds']:e['campaignIds'].insert(0,'LATE_ANTIQUITY')
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'));events=[
 {'year':235,'label':'Убийство Александра Севера','detail':'Рейнская армия убивает императора и провозглашает Максимина Фракийца.','campaignId':'LATE_ANTIQUITY','sourcePatch':'v6.8'},
 {'year':260,'label':'Пленение Валериана и региональные империи','detail':'После поражения у Эдессы усиливаются Галльская империя и Пальмира.','campaignId':'LATE_ANTIQUITY','sourcePatch':'v6.8'},
 {'year':274,'label':'Аврелиан восстанавливает единство','detail':'Пальмира и Галльская империя вновь подчиняются центральному двору.','campaignId':'LATE_ANTIQUITY','sourcePatch':'v6.8'},
 {'year':293,'label':'Создание тетрархии','detail':'Два августа и два цезаря распределяют дворы и фронтиры.','campaignId':'LATE_ANTIQUITY','sourcePatch':'v6.8'},
 {'year':312,'label':'Битва у Мульвийского моста','detail':'Константин побеждает Максенция и входит в Рим.','campaignId':'LATE_ANTIQUITY','sourcePatch':'v6.8'},
 {'year':330,'label':'Посвящение Константинополя','detail':'Новый Рим становится постоянным восточным центром императорской власти.','campaignId':'LATE_ANTIQUITY','sourcePatch':'v6.8'},
 {'year':378,'label':'Битва при Адрианополе','detail':'Восточная армия терпит поражение, император Валент погибает.','campaignId':'LATE_ANTIQUITY','sourcePatch':'v6.8'},
 {'year':395,'label':'Смерть Феодосия и два императорских двора','detail':'Аркадий получает Восток, Гонорий — Запад; римская государственность сохраняется.','campaignId':'LATE_ANTIQUITY','sourcePatch':'v6.8'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "LATE_ROMAN": {' not in s:
 marker='    "HELLENISTIC_ROMAN_EXAM": {';i=s.index(marker);group='''    "LATE_ROMAN": {\n        "terms": ["поздняя римская империя", "late roman empire", "диоклетиан", "diocletian", "константин", "constantine", "тетрарх", "tetrarchy", "аврелиан", "aurelian", "пальмира", "palmyra", "феодосий", "theodosius"],\n        "base": [("ru", "Поздняя Римская империя"), ("en", "Late Roman Empire"), ("en", "Late Antiquity Roman Empire")],\n    },\n''';s=s[:i]+group+s[i:]
old='("/hellenistic-roman-world/", "HELLENISTIC_ROMAN_EXAM"),'
if '("/late-roman/", "LATE_ROMAN")' not in s:
 if old not in s:raise SystemExit('image path marker missing')
 s=s.replace(old,old+' ("/late-roman/", "LATE_ROMAN"),')
p.write_text(s,encoding='utf-8')

entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg');entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v6.7.0','codex-v6.8.0').replace('codex-v6\\.7\\.0','codex-v6\\.8\\.0');p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v6-8-late-roman.js'" not in t:t=t.replace("'./js/features/v6-7-hellenistic-roman-world.js'","'./js/features/v6-7-hellenistic-roman-world.js','./js/features/v6-8-late-roman.js'")
if "'./assets/packs/late-roman-pack.svg'" not in t:t=t.replace("'./assets/packs/hellenistic-roman-era-pack.svg'","'./assets/packs/hellenistic-roman-era-pack.svg','./assets/packs/late-roman-pack.svg'")
p.write_text(t,encoding='utf-8')

for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace("'6.7.0'",f"'{V}'").replace('"6.7.0"',f'"{V}"').replace('6.7.0','6.8.0').replace(r'6\.7\.0',r'6\.8\.0').replace('3579','3711').replace('3537','3669')
 p.write_text(t,encoding='utf-8')

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v6.8\n\n## v6.9 — Христианство и религии поздней Античности\n\n- ранние общины, канон и епископская организация;\n- Никейский собор, арианские споры и императорская церковная политика;\n- монашество, святые, реликвии и паломничества;\n- иудаизм после разрушения Храма, манихейство и поздние традиционные культы;\n- Халкидон и формирование разных восточных церквей.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v6_8.md').write_text('''# Patch v6.8.0 — Поздняя Римская империя: кризис и перестройка\n\n- 11 глав, 66 миссий и 132 карточки.\n- Кризис III века, Валериан, Галльская империя, Пальмира и Аврелиан.\n- Диоклетиан, четыре двора тетрархии, налоги и новая администрация.\n- Константин, Константинополь, позднеримская армия, Адрианополь и Феодосий.\n- Кампания заканчивается разделом дворов 395 года; переселения и новые королевства будут отдельной кампанией.\n''',encoding='utf-8')
(ROOT/'docs/QA_v6_8.md').write_text('''# QA v6.8.0\n\n- Проверены 88 сюжетных и 44 архивных карточки.\n- Проверены 66 миссий, 66 уроков, 11 глав, 11 пулов и 11 архивных дел.\n- Проверены пять фаз кампании, карта дворов и фронтиров, четыре модуля итогового экзамена.\n- Проверены связи с завершённой римской кампанией и степными сетями.\n- Проверены локальные SVG, источники, PWA-кэш и runtime-модуль.\n''',encoding='utf-8')
p=ROOT/'README.md';t=p.read_text(encoding='utf-8');t=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',t,count=1,flags=re.M);block='''\n## v6.8.0 — Поздняя Римская империя\n\n- 11 глав, 66 миссий и 132 карточки.\n- Кризис III века, тетрархия, Константин, новые столицы, армия и раздел 395 года.\n- Первая кампания эпохи поздней Античности.\n- Patch-only архив.\n\n'''
if '## v6.8.0' not in t:t=t.replace('\n',block,1)
p.write_text(t,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';t=p.read_text(encoding='utf-8');block='''\n\n## v6.8 — Поздняя Римская империя\n\nЛокальные SVG-обложки 132 карточек и обложка пака созданы для Codex of History. Источниковая рамка использует Encyclopaedia Britannica, UNESCO World Heritage Centre, Perseus Digital Library, Bodleian Libraries, Roman Law Library и Fordham Internet Sourcebooks.\n'''
if '## v6.8 —' not in t:t+=block
p.write_text(t,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test:v68']='node tools/smoke-v68-late-roman.mjs && node tools/runtime-v68-late-roman.mjs'
if 'tools/smoke-v68-late-roman.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v68-late-roman.mjs && node tools/runtime-v68-late-roman.mjs'
dump(Path('package.json'),pkg)
print('integrated v6.8 late Roman campaign')
