#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='7.6.0';OLD='7.5.0';CHECKED='2026-07-16'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={'cards':['data/cards/aksum-nubia-arabia/story.json','data/cards/aksum-nubia-arabia/archive.json'],'campaigns':['data/campaigns/aksum-nubia-arabia/campaign.json'],'pools':['data/campaigns/aksum-nubia-arabia/pools.json'],'quizzes':['data/quizzes/aksum-nubia-arabia/campaign.json'],'stories':['data/stories/aksum-nubia-arabia/personal.json'],'lessons':['data/lessons/aksum-nubia-arabia/campaign.json']}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['AKSUM_NUBIA_ARABIA']='data/maps/aksum-nubia-arabia.json'
script='js/features/v7-6-aksum-nubia-arabia.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));rels=[r for r in rels if not re.fullmatch(r'REL_ANA_\d{4}',r.get('id',''))];new=load(Path('data/core/relations-760-aksum-nubia-arabia.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/aksum-nubia-arabia/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
entry={'id':'AKSUM_NUBIA_ARABIA','eraId':'ERA_LATE_ANTIQUITY','order':34,'title':'Аксум, Нубия и Южная Аравия','subtitle':'Красное море между Африкой и Аравией','period':'I–VII века','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Африканский Рог, Нубия и Южная Аравия','description':'Аксум, Адулис, монета и христианизация; конец Мероэ и нубийские царства; Химьяр, Наджран, Абраха и мир Красного моря около 600 года.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]}
world=[c for c in world if c['id']!='AKSUM_NUBIA_ARABIA'];world.append(entry)
order_map={'LATE_ANTIQUITY':26,'EARLY_CHRISTIANITY':27,'MIGRATION_KINGDOMS':28,'EASTERN_ROMAN':29,'SASANIAN':30,'CENTRAL_ASIA_LATE':31,'GUPTA':32,'CHINA_POST_HAN':33,'AKSUM_NUBIA_ARABIA':34,'ISLAMIC_ORIGINS':35}
for c in world:
 if c['id'] in order_map:c['order']=order_map[c['id']]
world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_LATE_ANTIQUITY':
  e['dateLabel']='II век до н. э. – VIII век н. э.';e['startYear']=-200;e['endYear']=750
  e['description']='Поздняя Античность связывает Рим, Сасанидов, новые западные королевства, Центральную Азию, Индию, Китай и Красное море через войны, религиозные сети, миграции, торговлю и новые государственные системы.'
  e['campaignIds']=['LATE_ANTIQUITY','EARLY_CHRISTIANITY','MIGRATION_KINGDOMS','EASTERN_ROMAN','SASANIAN','CENTRAL_ASIA_LATE','GUPTA','CHINA_POST_HAN','AKSUM_NUBIA_ARABIA']
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'));events=[
 {'year':50,'label':'Адулис становится главным портом Аксумского мира','detail':'Морской узел связывает нагорье, Египет, Аравию и Индийский океан.','campaignId':'AKSUM_NUBIA_ARABIA','sourcePatch':'v7.6'},
 {'year':270,'label':'Аксум начинает регулярную чеканку монеты','detail':'Золотые, серебряные и медные выпуски превращают царский образ в международный язык.','campaignId':'AKSUM_NUBIA_ARABIA','sourcePatch':'v7.6'},
 {'year':300,'label':'Химьяр объединяет большую часть Южной Аравии','detail':'Зафар становится центром нового южноаравийского царства.','campaignId':'AKSUM_NUBIA_ARABIA','sourcePatch':'v7.6'},
 {'year':330,'label':'Аксум возводит крупнейшие монументальные стелы','detail':'Царские гробницы и монолиты формируют центральный памятный ландшафт.','campaignId':'AKSUM_NUBIA_ARABIA','sourcePatch':'v7.6'},
 {'year':340,'label':'Эзана утверждает христианскую символику','detail':'Крест появляется на монетах, а двор связывается с Александрийской церковью.','campaignId':'AKSUM_NUBIA_ARABIA','sourcePatch':'v7.6'},
 {'year':350,'label':'Завершается царская эпоха Мероэ','detail':'Единый кушитский центр уступает место постмероитским региональным обществам.','campaignId':'AKSUM_NUBIA_ARABIA','sourcePatch':'v7.6'},
 {'year':450,'label':'Химьяритские надписи закрепляют культ Рахманана','detail':'Монотеистический язык становится частью царской идеологии Южной Аравии.','campaignId':'AKSUM_NUBIA_ARABIA','sourcePatch':'v7.6'},
 {'year':523,'label':'Трагедия христиан Наджрана','detail':'Конфликт Юсуфа Асара с противниками становится международным религиозным кризисом.','campaignId':'AKSUM_NUBIA_ARABIA','sourcePatch':'v7.6'},
 {'year':525,'label':'Поход царя Калеба в Южную Аравию','detail':'Аксумская морская экспедиция свергает власть Юсуфа Асара.','campaignId':'AKSUM_NUBIA_ARABIA','sourcePatch':'v7.6'},
 {'year':543,'label':'Христианизация Нобатии','detail':'Северная Нубия входит в новую церковную и царскую систему.','campaignId':'AKSUM_NUBIA_ARABIA','sourcePatch':'v7.6'},
 {'year':547,'label':'Абраха ремонтирует Марибскую плотину','detail':'Надпись связывает водное хозяйство, мятежи и международную дипломатию.','campaignId':'AKSUM_NUBIA_ARABIA','sourcePatch':'v7.6'},
 {'year':570,'label':'Сасанидское вмешательство в Йемене','detail':'Персидская экспедиция вытесняет аксумско-химьяритский режим.','campaignId':'AKSUM_NUBIA_ARABIA','sourcePatch':'v7.6'},
 {'year':580,'label':'Алодия принимает христианство','detail':'Южное нубийское царство укрепляет церковный центр в Собе.','campaignId':'AKSUM_NUBIA_ARABIA','sourcePatch':'v7.6'},
 {'year':600,'label':'Красное море входит в новый политический цикл','detail':'Аксум, нубийские царства, Йемен и Хиджаз сохраняют разные системы перед завоеваниями VII века.','campaignId':'AKSUM_NUBIA_ARABIA','sourcePatch':'v7.6'},
 {'year':642,'label':'Новые арабские армии выходят к Нубии и Красному морю','detail':'Позднеантичные государства сталкиваются с новой региональной силой.','campaignId':'AKSUM_NUBIA_ARABIA','sourcePatch':'v7.6'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "AKSUM_NUBIA_ARABIA": {' not in s:
 marker='    "CHINA_POST_HAN": {';i=s.index(marker);group='''    "AKSUM_NUBIA_ARABIA": {\n        "terms": ["Aksum", "Adulis", "Ezana", "Meroe", "Nubia", "Makuria", "Himyar", "Najran", "South Arabia", "Red Sea"],\n        "base": [("ru", "Аксум Нубия Южная Аравия"), ("en", "Aksum Nubia Himyar Red Sea late antiquity"), ("en", "Ezana Meroe Makuria Najran")],\n    },\n''';s=s[:i]+group+s[i:]
old='("/china-post-han/", "CHINA_POST_HAN"),'
if '("/aksum-nubia-arabia/", "AKSUM_NUBIA_ARABIA")' not in s:
 if old not in s:raise SystemExit('image path marker missing')
 s=s.replace(old,'("/aksum-nubia-arabia/", "AKSUM_NUBIA_ARABIA"), '+old)
p.write_text(s,encoding='utf-8')

entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg');entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v7.5.0','codex-v7.6.0').replace('codex-v7\\.5\\.0','codex-v7\\.6\\.0');p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v7-6-aksum-nubia-arabia.js'" not in t:t=t.replace("'./js/features/v7-5-china-post-han.js'","'./js/features/v7-5-china-post-han.js','./js/features/v7-6-aksum-nubia-arabia.js'")
if "'./assets/packs/aksum-nubia-arabia-pack.svg'" not in t:t=t.replace("'./assets/packs/china-post-han-pack.svg'","'./assets/packs/china-post-han-pack.svg','./assets/packs/aksum-nubia-arabia-pack.svg'")
p.write_text(t,encoding='utf-8')

for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'7\.5\.0',r'7\.6\.0').replace('4635','4767').replace('4593','4725').replace('2215','2281')
 p.write_text(t,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V
newtests='node tools/smoke-v76-aksum-nubia-arabia.mjs && node tools/runtime-v76-aksum-nubia-arabia.mjs'
if newtests not in pkg['scripts']['test']:pkg['scripts']['test']+=' && '+newtests
pkg['scripts']['test:v76']=newtests;dump(Path('package.json'),pkg)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v7.6\n\n## v7.7 — Америки в эпоху поздней Античности\n\n- Теотиуакан и его кварталы;\n- классические государства майя;\n- Тикаль, Калакмуль и династическая политика;\n- Моче, Наска и Тиуанако;\n- сравнительный взгляд на города, царскую власть и источники Америк.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v7_6.md').write_text('''# Patch v7.6.0 — Аксум, Нубия и Южная Аравия\n\n- 11 глав, 66 миссий и 132 карточки.\n- Красное море, Аксум, Адулис, монета, стелы и христианизация при Эзане.\n- Конец Мероэ, постмероитская Нубия, Нобатия, Макурия и Алодия.\n- Химьяр, Зафар, Наджран, Калеб, Абраха и сасанидское вмешательство в Йемене.\n- Переход к миру Красного моря около 600 года.\n''',encoding='utf-8')
(ROOT/'docs/QA_v7_6.md').write_text('''# QA v7.6.0\n\n- `npm test` проверяет старые кампании и новые smoke/runtime-модули.\n- Отдельно проверяются 132 карточки, 66 миссий, 15 квизов, карта, пак, экзамен и межкампанийные связи.\n- Стабильность сохранения и ленивой коллекции остаётся под тестом v6.9.1.\n''',encoding='utf-8')

attr=ROOT/'ATTRIBUTION.md';txt=attr.read_text(encoding='utf-8');block='''\n\n## v7.6 — Аксум, Нубия и Южная Аравия\n\nЛокальные SVG-обложки 132 карточек и обложка пака созданы для Codex of History. Учебная основа: UNESCO Aksum, Archaeological Sites of the Island of Meroe и Gebel Barkal, British Museum, Metropolitan Museum of Art, Digital Archive for the Study of pre-Islamic Arabian Inscriptions и исследования по Адулису, Эзане, нубийским царствам, Химьяру и Наджрану.\n'''
if '## v7.6 — Аксум, Нубия и Южная Аравия' not in txt:attr.write_text(txt.rstrip()+block,encoding='utf-8')
readme=ROOT/'README.md';txt=readme.read_text(encoding='utf-8')
if '## v7.6.0 — Аксум, Нубия и Южная Аравия' not in txt:readme.write_text(txt.rstrip()+'''\n\n## v7.6.0 — Аксум, Нубия и Южная Аравия\n\nНовая кампания из 11 глав соединяет Аксум и Адулис, конец Мероэ и христианские царства Нубии, Химьяр и Наджран, поход Калеба, правление Абрахи и перестройку Красного моря перед исламскими завоеваниями.\n''',encoding='utf-8')
print('updated project to',V)
