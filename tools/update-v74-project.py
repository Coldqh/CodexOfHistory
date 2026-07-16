#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='7.4.0';OLD='7.3.0';CHECKED='2026-07-16'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={'cards':['data/cards/india-gupta/story.json','data/cards/india-gupta/archive.json'],'campaigns':['data/campaigns/india-gupta/campaign.json'],'pools':['data/campaigns/india-gupta/pools.json'],'quizzes':['data/quizzes/india-gupta/campaign.json'],'stories':['data/stories/india-gupta/personal.json'],'lessons':['data/lessons/india-gupta/campaign.json']}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['GUPTA']='data/maps/india-gupta.json'
script='js/features/v7-4-india-gupta.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));new=load(Path('data/core/relations-v74-india-gupta.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/india-gupta/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
entry={'id':'GUPTA','eraId':'ERA_LATE_ANTIQUITY','order':32,'title':'Индия от Кушанов до Гуптов','subtitle':'Державы, религии, океанские сети и классическая культура','period':'II век до н. э. – VII век н. э.','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Южная Азия и Индийский океан','description':'После Маурьев, индо-греческие и сакские царства, Кушаны, Сатаваханы, порты Индийского океана, возникновение Гуптов, санскритская культура, религии, математика и переход к региональным царствам.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]}
world=[c for c in world if c['id']!='GUPTA'];world.append(entry)
order_map={'LATE_ANTIQUITY':26,'EARLY_CHRISTIANITY':27,'MIGRATION_KINGDOMS':28,'EASTERN_ROMAN':29,'SASANIAN':30,'CENTRAL_ASIA_LATE':31,'GUPTA':32,'CHINA_POST_HAN':33,'ISLAMIC_ORIGINS':34}
for c in world:
 if c['id'] in order_map:c['order']=order_map[c['id']]
world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_LATE_ANTIQUITY':
  e['dateLabel']='II век до н. э. – VIII век н. э.';e['startYear']=-200;e['endYear']=750
  e['description']='Поздняя Античность связывает Рим и Сасанидов, новые западные королевства, Центральную Азию, Кушанскую и гуптскую Индию, религиозные сети, океанскую торговлю и региональные политические порядки.'
  e['campaignIds']=['LATE_ANTIQUITY','EARLY_CHRISTIANITY','MIGRATION_KINGDOMS','EASTERN_ROMAN','SASANIAN','CENTRAL_ASIA_LATE','GUPTA','CHINA_POST_HAN']
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'));events=[
 {'year':-185,'label':'Начало власти Шунгов','detail':'После Маурьев север Индии переходит к нескольким региональным династиям.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':-165,'label':'Индо-греческая власть расширяется в Пенджабе','detail':'Северо-запад соединяет бактрийские и индийские политические традиции.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':-113,'label':'Колонна Гелиодора в Видише','detail':'Посольская надпись показывает дипломатию и ранний бхагаватский культ.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':50,'label':'Ранние Кушаны объединяют Бактрию','detail':'Куджула Кадфиз формирует новую династическую систему.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':78,'label':'Сакские и кшатрапские дома укрепляются на западе','detail':'Региональные правители соединяют иранские титулы и индийские институты.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':127,'label':'Начало правления Канишки в традиционной хронологии','detail':'Кушанская держава достигает высокого политического и культурного влияния.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':150,'label':'Надпись Рудрадамана в Джунагадхе','detail':'Санскритский панегирик связывает власть кшатрапа и ремонт водохранилища.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':170,'label':'Гаутамипутра Шатакарни укрепляет Сатаваханов','detail':'Деканская держава возвращает часть западных территорий.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':250,'label':'Кушанский мир распадается на региональные владения','detail':'Бактрия, Гандхара и север Индии идут разными политическими путями.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':320,'label':'Возвышение Чандрагупты I','detail':'Гуптский дом укрепляет ядро на Гангской равнине.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':350,'label':'Походы Самудрагупты','detail':'Праягский панегирик описывает разные формы подчинения правителей.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':400,'label':'Чандрагупта II расширяет державу на запад','detail':'Победа над кшатрапами усиливает связи с Малвой и портами.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':415,'label':'Удаягирская программа царского культа','detail':'Пещеры и рельеф Варахи связывают миф, ритуал и гуптскую власть.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':455,'label':'Скандрагупта отражает давление хуна','detail':'Имперская система сохраняется, но военные и финансовые трудности растут.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':473,'label':'Надпись шёлкоткачей Мандасора','detail':'Ремесленная корпорация фиксирует миграцию и коллективное храмовое дарение.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':499,'label':'Арьябхата завершает Арьябхатию','detail':'Трактат излагает математические и астрономические методы.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':510,'label':'Торамана контролирует часть Центральной Индии','detail':'Надписи фиксируют власть хуна за пределами северо-запада.','campaignId':'GUPTA','sourcePatch':'v7.4'},
 {'year':528,'label':'Яшодхарман заявляет победу в Малве','detail':'Региональный правитель провозглашает новое верховенство после кризиса Гуптов.','campaignId':'GUPTA','sourcePatch':'v7.4'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "INDIA_GUPTA": {' not in s:
 marker='    "CENTRAL_ASIA_LATE": {';i=s.index(marker);group='''    "INDIA_GUPTA": {\n        "terms": ["India Gupta", "Kushan", "Satavahana", "Gandhara", "Mathura", "Sanchi", "Amaravati", "Gupta Empire", "Ajanta", "Aryabhata", "Sanskrit", "Huna"],\n        "base": [("ru", "Индия эпохи Кушанов и Гуптов"), ("en", "Gupta Empire India"), ("en", "Kushan Satavahana Gupta art")],\n    },\n''';s=s[:i]+group+s[i:]
old='("/central-asia-late/", "CENTRAL_ASIA_LATE"),'
if '("/india-gupta/", "INDIA_GUPTA")' not in s:
 if old not in s:raise SystemExit('image path marker missing')
 s=s.replace(old,old+' ("/india-gupta/", "INDIA_GUPTA"),')
p.write_text(s,encoding='utf-8')

entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg');entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v7.3.0','codex-v7.4.0').replace('codex-v7\\.3\\.0','codex-v7\\.4\\.0');p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v7-4-india-gupta.js'" not in t:t=t.replace("'./js/features/v7-3-central-asia.js'","'./js/features/v7-3-central-asia.js','./js/features/v7-4-india-gupta.js'")
if "'./assets/packs/india-gupta-pack.svg'" not in t:t=t.replace("'./assets/packs/central-asia-late-pack.svg'","'./assets/packs/central-asia-late-pack.svg','./assets/packs/india-gupta-pack.svg'")
p.write_text(t,encoding='utf-8')

for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'7\.3\.0',r'7\.4\.0').replace('4371','4503').replace('4329','4461').replace('2083','2149')
 p.write_text(t,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V
newtests='node tools/smoke-v74-india-gupta.mjs && node tools/runtime-v74-india-gupta.mjs'
if newtests not in pkg['scripts']['test']:pkg['scripts']['test']+=' && '+newtests
pkg['scripts']['test:v74']=newtests;dump(Path('package.json'),pkg)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v7.4\n\n## v7.5 — Китай между Хань и Тан\n\n- Троецарствие и Западная Цзинь;\n- война восьми князей и падение северных столиц;\n- Шестнадцать государств, Восточная Цзинь и Северная Вэй;\n- Северные и Южные династии, буддизм и степные элиты;\n- объединение Суй и возникновение Тан.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v7_4.md').write_text('''# Patch v7.4.0 — Индия от Кушанов до Гуптов\n\n- 11 глав, 66 миссий и 132 карточки.\n- Региональный мир после Маурьев, индо-греки, шаки и индо-парфяне.\n- Кушанская держава, Гандхара, Матхура и буддийские сети.\n- Сатаваханы, Декан и порты Индийского океана.\n- Возникновение Гуптов, управление, земельные грамоты и местные элиты.\n- Санскритская культура, религии, Аджанта, Арьябхата и распад гуптского порядка.\n''',encoding='utf-8')
(ROOT/'docs/QA_v7_4.md').write_text('''# QA v7.4.0\n\n- `npm test` проверяет старые кампании и новые smoke/runtime-модули.\n- Отдельно проверяются 132 карточки, 66 миссий, 15 квизов, карта, пак, экзамен и межкампанийные связи.\n- Стабильность сохранения и ленивой коллекции остаётся под тестом v6.9.1.\n''',encoding='utf-8')

attr=ROOT/'ATTRIBUTION.md';txt=attr.read_text(encoding='utf-8');block='''\n\n## v7.4 — Индия от Кушанов до Гуптов\n\nЛокальные SVG-обложки 132 карточек и обложка пака созданы для Codex of History. Учебная основа: Metropolitan Museum of Art, UNESCO Sanchi, Ajanta и Nalanda, British Museum, Archaeological Survey of India, American Numismatic Society и исследования по Кушанам, Сатаваханам, Гуптам, индийской математике и торговле Индийского океана.\n'''
if '## v7.4 — Индия от Кушанов до Гуптов' not in txt:attr.write_text(txt.rstrip()+block,encoding='utf-8')
readme=ROOT/'README.md';txt=readme.read_text(encoding='utf-8')
if '## v7.4.0 — Индия от Кушанов до Гуптов' not in txt:readme.write_text(txt.rstrip()+'''\n\n## v7.4.0 — Индия от Кушанов до Гуптов\n\nНовая кампания из 11 глав соединяет региональный мир после Маурьев, Кушанскую и Сатаваханскую державы, буддийские сети, торговлю Индийского океана, возникновение Гуптов, санскритскую культуру, религии, математику и переход к региональным царствам VI–VII веков.\n''',encoding='utf-8')
print('updated project to',V)
