#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='7.8.0';OLD='7.7.0';CHECKED='2026-07-16'

def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Content manifest and runtime.
m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={
 'cards':['data/cards/world-around-700/story.json','data/cards/world-around-700/archive.json'],
 'campaigns':['data/campaigns/world-around-700/campaign.json'],
 'pools':['data/campaigns/world-around-700/pools.json'],
 'quizzes':['data/quizzes/world-around-700/campaign.json'],
 'stories':['data/stories/world-around-700/personal.json'],
 'lessons':['data/lessons/world-around-700/campaign.json'],
}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]: d[key].append(val)
d['maps']['WORLD_AROUND_700']='data/maps/world-around-700.json'
script='js/features/v7-8-world-around-700.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

# Relations.
rels=load(Path('data/core/relations.json'));rels=[r for r in rels if not re.fullmatch(r'REL_WAE_\d{4}',r.get('id',''))]
new=load(Path('data/core/relations-780-world-around-700.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

# World catalog and era completion.
world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/world-around-700/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
entry={'id':'WORLD_AROUND_700','eraId':'ERA_LATE_ANTIQUITY','order':36,'title':'Мир около 700 года: сравнительный экзамен','subtitle':'Восемь регионов на одной шкале времени','period':'ок. 550–750 годов','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Европа, Средиземноморье, Африка, Азия и Америки','description':'Итог поздней Античности: синхронная хронология, государства, армии, города, налоги, религии, сети, кризисы и критика источников.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]}
world=[c for c in world if c['id']!='WORLD_AROUND_700'];world.append(entry)
order_map={'LATE_ANTIQUITY':26,'EARLY_CHRISTIANITY':27,'MIGRATION_KINGDOMS':28,'EASTERN_ROMAN':29,'SASANIAN':30,'CENTRAL_ASIA_LATE':31,'GUPTA':32,'CHINA_POST_HAN':33,'AKSUM_NUBIA_ARABIA':34,'AMERICAS_LATE':35,'WORLD_AROUND_700':36,'ISLAMIC_ORIGINS':37}
for c in world:
 if c['id'] in order_map:c['order']=order_map[c['id']]
world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_LATE_ANTIQUITY':
  e['dateLabel']='II век до н. э. – VIII век н. э.';e['startYear']=-200;e['endYear']=750
  e['description']='Поздняя Античность завершена глобальным сравнительным слоем: Рим и западные королевства, Сасаниды, Центральная Азия, Индия, Китай, Красное море и самостоятельные исторические траектории Америк.'
  ids=['LATE_ANTIQUITY','EARLY_CHRISTIANITY','MIGRATION_KINGDOMS','EASTERN_ROMAN','SASANIAN','CENTRAL_ASIA_LATE','GUPTA','CHINA_POST_HAN','AKSUM_NUBIA_ARABIA','AMERICAS_LATE','WORLD_AROUND_700']
  e['campaignIds']=ids
 dump(Path('data/world/eras.json'),eras)

# Timeline summary.
wt=load(Path('data/world/timeline.json'));events=[
 {'year':565,'label':'Смерть Юстиниана на общей шкале мира','detail':'Восточная Римская империя завершает одну программу реставрации, пока другие регионы идут собственными политическими циклами.','campaignId':'WORLD_AROUND_700','sourcePatch':'v7.8'},
 {'year':602,'label':'Начинается последняя римско-сасанидская война','detail':'Долгий конфликт перестраивает налоги, армии и города восточного Средиземноморья и Ирана.','campaignId':'WORLD_AROUND_700','sourcePatch':'v7.8'},
 {'year':618,'label':'Начало Тан','detail':'Китайское объединение создаёт новый центр Восточной Азии без связи с европейским рубежом эпох.','campaignId':'WORLD_AROUND_700','sourcePatch':'v7.8'},
 {'year':628,'label':'Конец последней римско-сасанидской войны','detail':'Победа Ираклия не возвращает прежний мир и предшествует новой политической перестройке региона.','campaignId':'WORLD_AROUND_700','sourcePatch':'v7.8'},
 {'year':651,'label':'Конец сасанидской династии','detail':'Династия исчезает, но часть административных, налоговых и культурных практик продолжает существовать.','campaignId':'WORLD_AROUND_700','sourcePatch':'v7.8'},
 {'year':700,'label':'Мир около 700 года','detail':'Восемь регионов сравниваются на одной шкале без утверждения об одном общем переходе.','campaignId':'WORLD_AROUND_700','sourcePatch':'v7.8'},
 {'year':750,'label':'Поздняя Античность завершена как сравнительный слой','detail':'Следующая эпоха приложения переходит к исламскому миру и нескольким средневековым политическим системам.','campaignId':'WORLD_AROUND_700','sourcePatch':'v7.8'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

# Image query profile.
p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "WORLD_AROUND_700": {' not in s:
 marker='    "AMERICAS_LATE": {';i=s.index(marker)
 group='''    "WORLD_AROUND_700": {\n        "terms": ["world around 700", "late antiquity", "Byzantine", "Sasanian", "Tang", "Sogdian", "Aksum", "Maya", "comparative history"],\n        "base": [("ru", "Мир около 700 года поздняя Античность"), ("en", "world around 700 late antiquity"), ("en", "Byzantine Sasanian Tang Sogdian Aksum Maya")],\n    },\n'''
 s=s[:i]+group+s[i:]
old='("/americas-late/", "AMERICAS_LATE"),'
if '("/world-around-700/", "WORLD_AROUND_700")' not in s:
 if old not in s:raise SystemExit('image marker missing')
 s=s.replace(old,'("/world-around-700/", "WORLD_AROUND_700"), '+old)
p.write_text(s,encoding='utf-8')

# Static image manifest.
entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg')
  entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

# Version runtime and shell.
for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v7.7.0','codex-v7.8.0').replace('codex-v7\\.7\\.0','codex-v7\\.8\\.0')
 if rel=='index.html': t=re.sub(r'js/bootstrap\.js\?v=[0-9.]+',f'js/bootstrap.js?v={V}',t)
 p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v7-8-world-around-700.js'" not in t:t=t.replace("'./js/features/v7-7-americas-late.js'","'./js/features/v7-7-americas-late.js','./js/features/v7-8-world-around-700.js'")
if "'./assets/packs/world-around-700-pack.svg'" not in t:t=t.replace("'./assets/packs/americas-late-pack.svg'","'./assets/packs/americas-late-pack.svg','./assets/packs/world-around-700-pack.svg'")
p.write_text(t,encoding='utf-8')

# Keep all historical tests aligned with the installed application version and totals.
for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'7\.7\.0',r'7\.8\.0').replace('4899','4995').replace('4857','4953').replace('2347','2395')
 p.write_text(t,encoding='utf-8')

# Documentation.
(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v7.8\n\n## v8.0 — Возникновение исламского мира\n\n- Аравия VI–VII веков без образа пустого пространства;\n- Мекка, Медина, Мухаммед и первые общины;\n- объединение Аравии и Праведный халифат;\n- завоевания византийских и сасанидских земель;\n- Омейяды, новые столицы, налоги, языки и религиозные общины.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v7_8.md').write_text('''# Patch v7.8.0 — Мир около 700 года: сравнительный экзамен\n\n- 8 глав, 48 миссий и 96 карточек.\n- Восемь регионов на одной шкале 550–750 годов.\n- Сравнение государств, армий, городов, налогов, религий, сетей и кризисов.\n- Глобальная карта, параллельная хронология и шестимодульный итоговый экзамен.\n- Эпоха поздней Античности завершена; следующий этап — возникновение исламского мира.\n''',encoding='utf-8')
(ROOT/'docs/QA_v7_8.md').write_text('''# QA v7.8.0\n\n- Проверены 64 сюжетные и 32 архивные карточки.\n- Проверены 48 миссий, 48 уроков, 8 глав, 8 пулов и 8 личных историй.\n- Проверены восемь региональных кнопок, параллельная хронология и глобальная карта.\n- Проверены шесть модулей экзамена и завершение эпохи поздней Античности.\n- Проверены связи со всеми региональными кампаниями v7.0–v7.7.\n''',encoding='utf-8')
p=ROOT/'README.md';s=p.read_text(encoding='utf-8');s=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',s,count=1,flags=re.M);block='''\n## v7.8.0 — Мир около 700 года: сравнительный экзамен\n\n- 8 глав, 48 миссий и 96 карточек.\n- Восемь регионов, общая карта и параллельная хронология 550–750 годов.\n- Шестимодульный экзамен завершает эпоху поздней Античности.\n- Patch-only архив.\n\n'''
if '## v7.8.0' not in s:s=s.replace('\n',block,1)
p.write_text(s,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';s=p.read_text(encoding='utf-8');block='''\n\n## v7.8 — Мир около 700 года\n\nЛокальные SVG-обложки 96 карточек и общего пака созданы для Codex of History. Источниковая рамка опирается на материалы Metropolitan Museum of Art, UNESCO World Heritage Centre, Dumbarton Oaks и институциональные архивы предыдущих региональных кампаний.\n'''
if '## v7.8 —' not in s:s+=block
p.write_text(s,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test:v78']='node tools/smoke-v78-world-around-700.mjs && node tools/runtime-v78-world-around-700.mjs'
if 'tools/smoke-v78-world-around-700.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v78-world-around-700.mjs && node tools/runtime-v78-world-around-700.mjs'
dump(Path('package.json'),pkg)
print('integrated v7.8 world around 700 comparative exam')
