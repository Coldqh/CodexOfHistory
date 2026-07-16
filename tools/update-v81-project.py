#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='8.1.0';OLD='8.0.0';CHECKED='2026-07-16'

def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={
 'cards':['data/cards/abbasid-baghdad/story.json','data/cards/abbasid-baghdad/archive.json'],
 'campaigns':['data/campaigns/abbasid-baghdad/campaign.json'],
 'pools':['data/campaigns/abbasid-baghdad/pools.json'],
 'quizzes':['data/quizzes/abbasid-baghdad/campaign.json'],
 'stories':['data/stories/abbasid-baghdad/personal.json'],
 'lessons':['data/lessons/abbasid-baghdad/campaign.json'],
}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['ABBASID_BAGHDAD']='data/maps/abbasid-baghdad.json'
script='js/features/v8-1-abbasid-baghdad.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));rels=[r for r in rels if not re.fullmatch(r'REL_ABB_\d{4}',r.get('id',''))]
new=load(Path('data/core/relations-810-abbasid-baghdad.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/abbasid-baghdad/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
entry={'id':'ABBASID_BAGHDAD','eraId':'ERA_TRANSITION','order':38,'title':'Аббасидская революция и Багдад','subtitle':'От Хорасана к столице, знанию и региональным державам','period':'ок. 718–945 годы','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Ирак, Хорасан, Египет, Центральная Азия и Магриб','description':'Хорасанская революция, ранние Аббасиды, основание Багдада, визири, торговля, гражданская война, переводы, право, Самарра и региональные династии.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]}
world=[c for c in world if c['id']!='ABBASID_BAGHDAD'];world.append(entry);world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_TRANSITION':
  e['title']='Переход к Средневековью';e['dateLabel']='VI–X века н. э.';e['startYear']=550;e['endYear']=945;e['status']='PLAYABLE'
  e['description']='Возникновение исламского мира, Омейяды, Аббасидская революция, Багдад и региональные державы показывают переход от поздней Античности к раннему Средневековью.'
  ids=e.setdefault('campaignIds',[])
  for cid in ['ISLAMIC_ORIGINS','ABBASID_BAGHDAD']:
   if cid not in ids:ids.append(cid)
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'));events=[
 {'year':747,'label':'Начало аббасидского выступления в Хорасане','detail':'Армия Абу Муслима занимает Мерв и превращает восточную даʿву в революцию.','campaignId':'ABBASID_BAGHDAD','sourcePatch':'v8.1'},
 {'year':750,'label':'Победа Аббасидов при Большом Забе','detail':'Омейядский центр рушится, а власть переходит к новой династии.','campaignId':'ABBASID_BAGHDAD','sourcePatch':'v8.1'},
 {'year':755,'label':'Аль-Мансур устраняет Абу Муслима','detail':'Династия ограничивает самостоятельность революционной военной сети.','campaignId':'ABBASID_BAGHDAD','sourcePatch':'v8.1'},
 {'year':762,'label':'Основание Мадинат ас-Салам — Багдада','detail':'Новая столица создаётся на Тигре рядом со старыми иракскими и сасанидскими центрами.','campaignId':'ABBASID_BAGHDAD','sourcePatch':'v8.1'},
 {'year':803,'label':'Падение Бармакидов','detail':'Харун ар-Рашид уничтожает влиятельную визирскую сеть.','campaignId':'ABBASID_BAGHDAD','sourcePatch':'v8.1'},
 {'year':813,'label':'Завершение осады Багдада','detail':'Аль-Мамун побеждает аль-Амина после разрушительной гражданской войны.','campaignId':'ABBASID_BAGHDAD','sourcePatch':'v8.1'},
 {'year':833,'label':'Начало михны','detail':'Халифская власть пытается контролировать богословскую позицию судей и учёных.','campaignId':'ABBASID_BAGHDAD','sourcePatch':'v8.1'},
 {'year':836,'label':'Основание Самарры как столицы двора и гвардии','detail':'Новый дворцовый город отделяет армию от населения Багдада.','campaignId':'ABBASID_BAGHDAD','sourcePatch':'v8.1'},
 {'year':861,'label':'Убийство аль-Мутаваккиля','detail':'Военные командиры становятся открытыми участниками смены халифов.','campaignId':'ABBASID_BAGHDAD','sourcePatch':'v8.1'},
 {'year':892,'label':'Возвращение аббасидского двора в Багдад','detail':'Самарра теряет столичную функцию, но региональные центры продолжают усиливаться.','campaignId':'ABBASID_BAGHDAD','sourcePatch':'v8.1'},
 {'year':945,'label':'Буиды занимают Багдад','detail':'Военная власть переходит к региональной династии, сохраняющей аббасидского халифа.','campaignId':'ABBASID_BAGHDAD','sourcePatch':'v8.1'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "ABBASID_BAGHDAD": {' not in s:
 marker='    "ISLAMIC_ORIGINS": {';i=s.index(marker)
 group='''    "ABBASID_BAGHDAD": {\n        "terms": ["Abbasid", "Baghdad", "Samarra", "Abbasid coin", "Arabic manuscript", "translation movement", "House of Wisdom", "Barmakids", "Islamic papyrus", "Samanid"],\n        "base": [("ru", "Аббасиды Багдад Самарра"), ("en", "Abbasid Baghdad Samarra"), ("en", "Abbasid manuscript coin papyrus")],\n    },\n'''
 s=s[:i]+group+s[i:]
old='("/islamic-origins/", "ISLAMIC_ORIGINS"),'
if '("/abbasid-baghdad/", "ABBASID_BAGHDAD")' not in s:
 if old not in s:raise SystemExit('image marker missing')
 s=s.replace(old,'("/abbasid-baghdad/", "ABBASID_BAGHDAD"), '+old)
p.write_text(s,encoding='utf-8')

entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg')
  entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v8.0.0','codex-v8.1.0').replace('codex-v8\\.0\\.0','codex-v8\\.1\\.0')
 if rel=='index.html':t=re.sub(r'js/bootstrap\.js\?v=[0-9.]+',f'js/bootstrap.js?v={V}',t)
 p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v8-1-abbasid-baghdad.js'" not in t:t=t.replace("'./js/features/v8-0-islamic-origins.js'","'./js/features/v8-0-islamic-origins.js','./js/features/v8-1-abbasid-baghdad.js'")
if "'./assets/packs/abbasid-baghdad-pack.svg'" not in t:t=t.replace("'./assets/packs/islamic-origins-pack.svg'","'./assets/packs/islamic-origins-pack.svg','./assets/packs/abbasid-baghdad-pack.svg'")
p.write_text(t,encoding='utf-8')

for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'8\.0\.0',r'8\.1\.0').replace('5127','5259').replace('5085','5217').replace('2461','2527')
 p.write_text(t,encoding='utf-8')

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v8.1\n\n## v8.2 — Каролингская Европа\n\n- франкские королевства после Меровингов;\n- Пипин Короткий, папство и новая династия;\n- Карл Великий, войны и императорская коронация;\n- графства, капитулярии, монастыри и письменная реформа;\n- раздел империи и формирование новых западноевропейских королевств.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v8_1.md').write_text('''# Patch v8.1.0 — Аббасидская революция и Багдад\n\n- 11 глав, 66 миссий и 132 карточки.\n- Хорасанская революция, битва при Забе, ас-Саффах и аль-Мансур.\n- Основание Багдада, визири, Бармакиды, Харун ар-Рашид и имперская экономика.\n- Гражданская война, переводческое движение, право, михна и Самарра.\n- Региональные династии и занятие Багдада Буидами в 945 году.\n- Все значки этапов урока стали прямыми кнопками навигации.\n''',encoding='utf-8')
(ROOT/'docs/QA_v8_1.md').write_text('''# QA v8.1.0\n\n- Проверены 88 сюжетных и 44 архивных карточки.\n- Проверены 66 миссий, 66 уроков, 11 глав, 11 пулов и 11 личных историй.\n- Проверены карта, четыре фазы, архивный пак и четыре модуля итогового экзамена.\n- Проверены межкампанийные связи с ранним исламом, Центральной Азией, Сасанидами, Аксумом и Китаем.\n- Проверен прямой переход по всем пяти значкам этапов урока.\n- Проверены миграция сейва, коллекция и PWA-кэш.\n''',encoding='utf-8')
p=ROOT/'README.md';s=p.read_text(encoding='utf-8');s=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',s,count=1,flags=re.M);block='''\n## v8.1.0 — Аббасидская революция и Багдад\n\n- 11 глав, 66 миссий и 132 карточки.\n- Революция, Багдад, переводческое движение, Самарра и региональные династии.\n- Значки этапов урока открывают рассказ, хронологию, разбор, теорию и практику напрямую.\n- Patch-only архив.\n\n'''
if '## v8.1.0' not in s:s=s.replace('\n',block,1)
p.write_text(s,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';s=p.read_text(encoding='utf-8');block='''\n\n## v8.1 — Аббасидская революция и Багдад\n\nЛокальные SVG-обложки 132 карточек и кампанийного пака созданы для Codex of History. Источниковая рамка опирается на материалы Metropolitan Museum of Art, UNESCO Samarra Archaeological City, Encyclopaedia Iranica, Encyclopaedia Britannica и исследования аббасидской монеты, папирусов, рукописей и городской археологии.\n'''
if '## v8.1 —' not in s:s+=block
p.write_text(s,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test:v81']='node tools/smoke-v81-abbasid-baghdad.mjs && node tools/runtime-v81-abbasid-baghdad.mjs'
if 'tools/smoke-v81-abbasid-baghdad.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v81-abbasid-baghdad.mjs && node tools/runtime-v81-abbasid-baghdad.mjs'
dump(Path('package.json'),pkg)
print('integrated v8.1 Abbasid Baghdad and interactive lesson stages')
