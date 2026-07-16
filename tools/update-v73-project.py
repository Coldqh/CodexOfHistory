#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='7.3.0';OLD='7.2.0';CHECKED='2026-07-16'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={'cards':['data/cards/central-asia-late/story.json','data/cards/central-asia-late/archive.json'],'campaigns':['data/campaigns/central-asia-late/campaign.json'],'pools':['data/campaigns/central-asia-late/pools.json'],'quizzes':['data/quizzes/central-asia-late/campaign.json'],'stories':['data/stories/central-asia-late/personal.json'],'lessons':['data/lessons/central-asia-late/campaign.json']}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['CENTRAL_ASIA_LATE']='data/maps/central-asia-late.json'
script='js/features/v7-3-central-asia.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));new=load(Path('data/core/relations-v73-central-asia.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/central-asia-late/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
entry={'id':'CENTRAL_ASIA_LATE','eraId':'ERA_LATE_ANTIQUITY','order':31,'title':'Центральная Азия после Хань','subtitle':'Согдиана, оазисы, эфталиты и тюркские каганаты','period':'III–VIII века','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Бактрия, Согдиана, Тарим и Семиречье','description':'От распада кушанского мира и бактрийских городов до согдийских диаспор, Таримских оазисов, буддийских сетей, эфталитов, тюркских каганатов и новой борьбы около 700 года.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]}
world=[c for c in world if c['id']!='CENTRAL_ASIA_LATE']
order_map={'LATE_ANTIQUITY':26,'EARLY_CHRISTIANITY':27,'MIGRATION_KINGDOMS':28,'EASTERN_ROMAN':29,'SASANIAN':30,'CENTRAL_ASIA_LATE':31,'GUPTA':32,'CHINA_POST_HAN':33,'ISLAMIC_ORIGINS':34}
world.append(entry)
for c in world:
 if c['id'] in order_map:c['order']=order_map[c['id']]
world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_LATE_ANTIQUITY':
  e['dateLabel']='III–VIII века н. э.';e['endYear']=750
  e['description']='Поздняя Римская и Сасанидская державы перестраивают право, налоги и войну, западные провинции превращаются в королевства, а Центральная Азия сохраняет города, оазисы, согдийские диаспоры, буддийские сети и тюркские каганаты.'
  e['campaignIds']=['LATE_ANTIQUITY','EARLY_CHRISTIANITY','MIGRATION_KINGDOMS','EASTERN_ROMAN','SASANIAN','CENTRAL_ASIA_LATE','GUPTA','CHINA_POST_HAN']
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'));events=[
 {'year':313,'label':'Согдийские древние письма','detail':'Частные послания из района Дуньхуана фиксируют торговую диаспору и кризис связей.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':401,'label':'Кумараджива начинает переводы в Чанъане','detail':'Учёный из Кучи становится одним из главных посредников буддийской литературы.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':420,'label':'Кидаритское влияние в Бактрии','detail':'Новые династические группы используют кушанские и сасанидские монетные формы.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':450,'label':'Эфталиты укрепляются в Тохаристане','detail':'Военное объединение распространяет влияние на Бактрию и соседние регионы.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':484,'label':'Гибель Пероза в войне с эфталитами','detail':'Поражение Сасанидов меняет баланс на востоке Ирана и в Бактрии.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':552,'label':'Основание Первого Тюркского каганата','detail':'Бумын побеждает жужаней и принимает титул кагана.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':560,'label':'Разгром основной эфталитской державы','detail':'Сасаниды и тюрки разделяют влияние в Тохаристане и Согдиане.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':568,'label':'Тюркско-согдийское посольство в Константинополь','detail':'Маниах ведёт переговоры о союзе и продаже шёлка.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':570,'label':'Миссия Земарха к западным тюркам','detail':'Восточноримский посол достигает ставки кагана и описывает дипломатический маршрут.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':603,'label':'Раздел тюркского мира','detail':'Восточная и западная ветви каганата закрепляются как отдельные политические системы.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':630,'label':'Гибель Тун-ябгу','detail':'Династический конфликт ослабляет Западный Тюркский каганат.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':640,'label':'Тан занимает Гаочан','detail':'Восточный Тарим включается в систему танских гарнизонов и протекторатов.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':645,'label':'Сюаньцзан возвращается из путешествия','detail':'Паломник привозит тексты и описание Тарима, Тохаристана и Индии.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':657,'label':'Тан побеждает Ашина Хэлу','detail':'Западнотюркская верховная власть распадается под китайским военным давлением.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':660,'label':'Создаются росписи Зала послов Афрасиаба','detail':'Самаркандский двор изображает посольства и связи с соседними мирами.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':682,'label':'Восстановление Второго Тюркского каганата','detail':'Степная династия возвращает независимую власть в Монголии.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':705,'label':'Начало нового арабского наступления в Мавераннахре','detail':'Военные походы из Хорасана усиливают давление на согдийские княжества.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'},
 {'year':712,'label':'Арабские силы занимают Самарканд','detail':'Местные княжества вступают в новый цикл договоров, восстаний и налоговых изменений.','campaignId':'CENTRAL_ASIA_LATE','sourcePatch':'v7.3'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "CENTRAL_ASIA_LATE": {' not in s:
 marker='    "SASANIAN": {';i=s.index(marker);group='''    "CENTRAL_ASIA_LATE": {\n        "terms": ["Центральная Азия после Хань", "Sogdiana", "Samarkand Afrasiab", "Sogdian merchants", "Tarim Basin", "Kucha", "Khotan", "Bamiyan", "Hephthalites", "First Turkic Khaganate", "Suyab"],\n        "base": [("ru", "Центральная Азия поздняя античность"), ("en", "Sogdiana Late Antiquity"), ("en", "Central Asia Silk Roads 3rd 8th century")],\n    },\n''';s=s[:i]+group+s[i:]
old='("/sasanian/", "SASANIAN"),'
if '("/central-asia-late/", "CENTRAL_ASIA_LATE")' not in s:
 if old not in s:raise SystemExit('image path marker missing')
 s=s.replace(old,old+' ("/central-asia-late/", "CENTRAL_ASIA_LATE"),')
p.write_text(s,encoding='utf-8')

entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg');entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v7.2.0','codex-v7.3.0').replace('codex-v7\\.2\\.0','codex-v7\\.3\\.0');p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v7-3-central-asia.js'" not in t:t=t.replace("'./js/features/v7-2-sasanian.js'","'./js/features/v7-2-sasanian.js','./js/features/v7-3-central-asia.js'")
if "'./assets/packs/central-asia-late-pack.svg'" not in t:t=t.replace("'./assets/packs/sasanian-pack.svg'","'./assets/packs/sasanian-pack.svg','./assets/packs/central-asia-late-pack.svg'")
p.write_text(t,encoding='utf-8')

for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'7\.2\.0',r'7\.3\.0').replace('4239','4371').replace('4197','4329').replace('2017','2083')
 p.write_text(t,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V
newtests='node tools/smoke-v73-central-asia.mjs && node tools/runtime-v73-central-asia.mjs'
if newtests not in pkg['scripts']['test']:pkg['scripts']['test']+=' && '+newtests
pkg['scripts']['test:v73']=newtests;dump(Path('package.json'),pkg)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v7.3\n\n## v7.4 — Индия от Кушанов до Гуптов\n\n- поздние Кушаны, Сатаваханы и региональные государства;\n- Гандхара, буддийские сети и торговля Индийского океана;\n- возникновение Гуптов и устройство державы;\n- санскритская культура, религии, математика и литература;\n- хуна и распад гуптского политического порядка.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v7_3.md').write_text('''# Patch v7.3.0 — Центральная Азия после Хань\n\n- 11 глав, 66 миссий и 132 карточки.\n- Посткушанская Бактрия, Тохаристан и кидаритские владения.\n- Согдийские города, купеческие диаспоры и древние письма.\n- Таримские оазисы, буддийские монастыри и переводчики.\n- Эфталиты, Первый и Западный Тюркские каганаты.\n- Мир около 700 года: Тан, тюрки, Тибет и арабское продвижение.\n''',encoding='utf-8')
(ROOT/'docs/QA_v7_3.md').write_text('''# QA v7.3.0\n\n- `npm test` проверяет старые кампании и новые smoke/runtime-модули.\n- Отдельно проверяются 132 карточки, 66 миссий, 15 квизов, карта, пак, экзамен и связи.\n- Стабильность сохранения и ленивой коллекции остаётся под тестом v6.9.1.\n''',encoding='utf-8')

attr=ROOT/'ATTRIBUTION.md';txt=attr.read_text(encoding='utf-8')
block='''\n\n## v7.3 — Центральная Азия после Хань\n\nЛокальные SVG-обложки 132 карточек и обложка пака созданы для Codex of History. Учебная основа: UNESCO Silk Roads Programme, UNESCO Samarkand и Bamiyan, Metropolitan Museum of Art, British Library, British Museum и справочные исследования по Согдиане, Бактрии, Тариму, эфталитам и тюркским каганатам.\n'''
if '## v7.3 — Центральная Азия после Хань' not in txt:attr.write_text(txt.rstrip()+block,encoding='utf-8')
readme=ROOT/'README.md';txt=readme.read_text(encoding='utf-8')
if '## v7.3.0 — Центральная Азия после Хань' not in txt:readme.write_text(txt.rstrip()+'''\n\n## v7.3.0 — Центральная Азия после Хань\n\nНовая кампания из 11 глав соединяет посткушанскую Бактрию, согдийские города и диаспоры, Таримские оазисы, буддийские сети, эфталитов, тюркские каганаты и новую борьбу за регион около 700 года.\n''',encoding='utf-8')
print('updated project to',V)
