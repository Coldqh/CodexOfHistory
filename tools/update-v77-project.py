#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='7.7.0';OLD='7.6.0';CHECKED='2026-07-16'

def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Content manifest.
m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={
 'cards':['data/cards/americas-late/story.json','data/cards/americas-late/archive.json'],
 'campaigns':['data/campaigns/americas-late/campaign.json'],
 'pools':['data/campaigns/americas-late/pools.json'],
 'quizzes':['data/quizzes/americas-late/campaign.json'],
 'stories':['data/stories/americas-late/personal.json'],
 'lessons':['data/lessons/americas-late/campaign.json'],
}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]: d[key].append(val)
d['maps']['AMERICAS_LATE']='data/maps/americas-late.json'
script='js/features/v7-7-americas-late.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

# Merge campaign relationships.
rels=load(Path('data/core/relations.json'))
rels=[r for r in rels if not re.fullmatch(r'REL_AME_\d{4}',r.get('id',''))]
new=load(Path('data/core/relations-770-americas-late.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen)
dump(Path('data/core/relations.json'),rels)

# World catalog.
world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/americas-late/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
entry={
 'id':'AMERICAS_LATE','eraId':'ERA_LATE_ANTIQUITY','order':35,
 'title':'Америки в эпоху поздней Античности','subtitle':'Города, царства и ландшафты III–VIII веков',
 'period':'III–VIII века','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE',
 'region':'Мезоамерика и Центральные Анды',
 'description':'Параллельная история Теотиуакана, классических государств майя, Моче, Наска, Тиуанако и Уари без механического переноса европейской периодизации.',
 'chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]
}
world=[c for c in world if c['id']!='AMERICAS_LATE'];world.append(entry)
order_map={'LATE_ANTIQUITY':26,'EARLY_CHRISTIANITY':27,'MIGRATION_KINGDOMS':28,'EASTERN_ROMAN':29,'SASANIAN':30,'CENTRAL_ASIA_LATE':31,'GUPTA':32,'CHINA_POST_HAN':33,'AKSUM_NUBIA_ARABIA':34,'AMERICAS_LATE':35,'ISLAMIC_ORIGINS':36}
for c in world:
 if c['id'] in order_map:c['order']=order_map[c['id']]
world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)

# Era layer.
eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_LATE_ANTIQUITY':
  e['dateLabel']='II век до н. э. – VIII век н. э.';e['startYear']=-200;e['endYear']=750
  e['description']='Поздняя Античность показана как глобальный временной слой: Рим и новые западные королевства, Сасаниды, Центральная Азия, Индия, Китай, Красное море и самостоятельные исторические траектории Америк.'
  e['campaignIds']=['LATE_ANTIQUITY','EARLY_CHRISTIANITY','MIGRATION_KINGDOMS','EASTERN_ROMAN','SASANIAN','CENTRAL_ASIA_LATE','GUPTA','CHINA_POST_HAN','AKSUM_NUBIA_ARABIA','AMERICAS_LATE']
dump(Path('data/world/eras.json'),eras)

# Shared timeline.
wt=load(Path('data/world/timeline.json'));events=[
 {'year':250,'label':'Начинается зрелый городской цикл Теотиуакана','detail':'Монументальный центр и сетка кварталов связывают ритуальную ось с огромным жилым городом.','campaignId':'AMERICAS_LATE','sourcePatch':'v7.7'},
 {'year':300,'label':'Классические царства майя расширяют династические сети','detail':'Надписи фиксируют царей, войны, союзы и ритуальные календари множества городов.','campaignId':'AMERICAS_LATE','sourcePatch':'v7.7'},
 {'year':350,'label':'Моче укрепляют долинные политические центры','detail':'Каналы, храмовые комплексы, ремесло и трудовые повинности связывают побережье северных Анд.','campaignId':'AMERICAS_LATE','sourcePatch':'v7.7'},
 {'year':378,'label':'Теотиуаканское вмешательство меняет династию Тикаля','detail':'Монументы Тикаля связывают приход нового правителя с людьми и символами центральной Мексики.','campaignId':'AMERICAS_LATE','sourcePatch':'v7.7'},
 {'year':400,'label':'Теотиуакан достигает крупнейшего городского масштаба','detail':'Многоэтничные жилые комплексы, рынки и ремесленные зоны обслуживают один из крупнейших городов своего времени.','campaignId':'AMERICAS_LATE','sourcePatch':'v7.7'},
 {'year':426,'label':'В Копане утверждается новая царская линия','detail':'Династическая память связывает основателя с центральномексиканскими образами и региональными союзами.','campaignId':'AMERICAS_LATE','sourcePatch':'v7.7'},
 {'year':450,'label':'Кауачи теряет роль главного центра Наска','detail':'Ритуальная география сохраняется, но население и политические центры перестраиваются.','campaignId':'AMERICAS_LATE','sourcePatch':'v7.7'},
 {'year':500,'label':'Тиуанако усиливает влияние вокруг озера Титикака','detail':'Монументы, земледельческие системы и колонии связывают высокогорье с дальними экологическими зонами.','campaignId':'AMERICAS_LATE','sourcePatch':'v7.7'},
 {'year':562,'label':'Калакмульская сеть наносит поражение Тикалю','detail':'Соперничество двух династических блоков перестраивает политику низменностей майя.','campaignId':'AMERICAS_LATE','sourcePatch':'v7.7'},
 {'year':600,'label':'Моче входят в период региональной перестройки','detail':'Разные долины реагируют на климатические и политические изменения неодинаково.','campaignId':'AMERICAS_LATE','sourcePatch':'v7.7'},
 {'year':650,'label':'Монументальный центр Теотиуакана переживает разрушения','detail':'Пожары и политическая дезинтеграция не означают мгновенного исчезновения населения долины.','campaignId':'AMERICAS_LATE','sourcePatch':'v7.7'},
 {'year':680,'label':'Уари формирует сеть административных центров','detail':'Планировка, дороги и провинциальные комплексы связывают центральные Анды новым способом.','campaignId':'AMERICAS_LATE','sourcePatch':'v7.7'},
 {'year':695,'label':'Тикаль побеждает Калакмуль','detail':'Династический баланс низменностей майя снова меняется после долгого соперничества.','campaignId':'AMERICAS_LATE','sourcePatch':'v7.7'},
 {'year':700,'label':'Тиуанако и Уари становятся главными андскими системами','detail':'Их зоны влияния пересекаются через колонии, обмен, ритуальные стили и пограничные центры.','campaignId':'AMERICAS_LATE','sourcePatch':'v7.7'},
 {'year':750,'label':'Америки сохраняют несколько самостоятельных политических миров','detail':'Майя, посттеотиуаканская Мезоамерика и андские системы входят в новые циклы без единого общего падения.','campaignId':'AMERICAS_LATE','sourcePatch':'v7.7'},
]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

# Image query profiles.
p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "AMERICAS_LATE": {' not in s:
 marker='    "AKSUM_NUBIA_ARABIA": {';i=s.index(marker)
 group='''    "AMERICAS_LATE": {\n        "terms": ["Teotihuacan", "Tikal", "Calakmul", "Maya", "Moche", "Nasca", "Nazca", "Tiwanaku", "Tiahuanaco", "Wari", "Huari", "Mesoamerica", "Andes"],\n        "base": [("ru", "Древние цивилизации Америки"), ("en", "Teotihuacan Maya Moche Nasca Tiwanaku Wari"), ("en", "Ancient Americas 3rd 8th century")],\n    },\n'''
 s=s[:i]+group+s[i:]
old='("/aksum-nubia-arabia/", "AKSUM_NUBIA_ARABIA"),'
if '("/americas-late/", "AMERICAS_LATE")' not in s:
 if old not in s:raise SystemExit('image path marker missing')
 s=s.replace(old,'("/americas-late/", "AMERICAS_LATE"), '+old)
p.write_text(s,encoding='utf-8')

# Rebuild static image manifest from all card datasets.
entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg')
  entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

# Version all runtime files and application shell.
for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v7.6.0','codex-v7.7.0').replace('codex-v7\\.6\\.0','codex-v7\\.7\\.0');p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v7-7-americas-late.js'" not in t:t=t.replace("'./js/features/v7-6-aksum-nubia-arabia.js'","'./js/features/v7-6-aksum-nubia-arabia.js','./js/features/v7-7-americas-late.js'")
if "'./assets/packs/americas-late-pack.svg'" not in t:t=t.replace("'./assets/packs/aksum-nubia-arabia-pack.svg'","'./assets/packs/aksum-nubia-arabia-pack.svg','./assets/packs/americas-late-pack.svg'")
p.write_text(t,encoding='utf-8')

# Update inherited test expectations.
for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'7\.6\.0',r'7\.7\.0').replace('4767','4899').replace('4725','4857').replace('2281','2347')
 p.write_text(t,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V
newtests='node tools/smoke-v77-americas-late.mjs && node tools/runtime-v77-americas-late.mjs'
if newtests not in pkg['scripts']['test']:pkg['scripts']['test']+=' && '+newtests
pkg['scripts']['test:v77']=newtests;dump(Path('package.json'),pkg)

# Documentation.
(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v7.7\n\n## v7.8 — Мир около 700 года: сравнительный экзамен\n\n- позднеримский и постримский Запад;\n- Восточная Римская империя и Сасаниды;\n- Центральная Азия, Индия и Китай;\n- Красное море и древние Америки;\n- власть, города, религии, обмен, экология и работа с разными типами источников.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v7_7.md').write_text('''# Patch v7.7.0 — Америки в эпоху поздней Античности\n\n- 11 глав, 66 миссий и 132 карточки.\n- Теотиуакан: монументальный центр, жилые кварталы и дальние связи.\n- Классические государства майя, Тикаль, Калакмуль, письмо и династическая политика.\n- Моче, Наска, Тиуанако и Уари.\n- Сравнение городов, власти, ландшафтов и источников без переноса европейской периодизации.\n''',encoding='utf-8')
(ROOT/'docs/QA_v7_7.md').write_text('''# QA v7.7.0\n\n- `npm test` проверяет старые кампании и новые smoke/runtime-модули.\n- Отдельно проверяются 132 карточки, 66 миссий, 15 квизов, карта, пак, экзамен и межкампанийные связи.\n- Проверяются уникальность ID и названий, длина уроков, изображения, PWA-кэш, сохранения и ленивая коллекция.\n''',encoding='utf-8')

attr=ROOT/'ATTRIBUTION.md';txt=attr.read_text(encoding='utf-8');block='''\n\n## v7.7 — Америки в эпоху поздней Античности\n\nЛокальные SVG-обложки 132 карточек и обложка пака созданы для Codex of History. Учебная основа: UNESCO Teotihuacan, Tikal, Calakmul, Lines and Geoglyphs of Nasca and Palpa и Tiwanaku; Metropolitan Museum of Art; Dumbarton Oaks и археологические исследования Теотиуакана, классических майя, Моче, Наска, Тиуанако и Уари.\n'''
if '## v7.7 — Америки в эпоху поздней Античности' not in txt:attr.write_text(txt.rstrip()+block,encoding='utf-8')
readme=ROOT/'README.md';txt=readme.read_text(encoding='utf-8')
if '## v7.7.0 — Америки в эпоху поздней Античности' not in txt:readme.write_text(txt.rstrip()+'''\n\n## v7.7.0 — Америки в эпоху поздней Античности\n\nНовая кампания из 11 глав показывает самостоятельные траектории Теотиуакана, классических царств майя, Моче, Наска, Тиуанако и Уари и завершает глобальное наполнение эпохи перед сравнительным экзаменом.\n''',encoding='utf-8')
print('updated project to',V)
