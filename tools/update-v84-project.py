#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='8.4.0';OLD='8.3.0';CHECKED='2026-07-16'

def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Content registry.
m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={
 'cards':['data/cards/vikings-north-atlantic/story.json','data/cards/vikings-north-atlantic/archive.json'],
 'campaigns':['data/campaigns/vikings-north-atlantic/campaign.json'],
 'pools':['data/campaigns/vikings-north-atlantic/pools.json'],
 'quizzes':['data/quizzes/vikings-north-atlantic/campaign.json'],
 'stories':['data/stories/vikings-north-atlantic/personal.json'],
 'lessons':['data/lessons/vikings-north-atlantic/campaign.json'],
}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['VIKINGS_NORTH_ATLANTIC']='data/maps/vikings-north-atlantic.json'
script='js/features/v8-4-vikings-north-atlantic.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

# Relations.
rels=load(Path('data/core/relations.json'));rels=[r for r in rels if not re.fullmatch(r'REL_VIK_\d{4}',r.get('id',''))]
new=load(Path('data/core/relations-840-vikings-north-atlantic.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

# Campaign catalogue and era membership.
world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/vikings-north-atlantic/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
entry={'id':'VIKINGS_NORTH_ATLANTIC','eraId':'ERA_EARLY_MEDIEVAL','order':41,'title':'Викинги и Северная Атлантика','subtitle':'Корабли, торговля, походы и океанские поселения','period':'VIII–XI века','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Скандинавия, Британские острова, Восточная Европа и Северная Атлантика','description':'Скандинавские общества, корабли, набеги, торговые города, Британия и Ирландия, Нормандия, Русь, Исландия, Гренландия, Винланд, королевская власть и христианизация.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]}
world=[c for c in world if c['id']!='VIKINGS_NORTH_ATLANTIC'];world.append(entry);world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)
eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_EARLY_MEDIEVAL':
  ids=[x for x in e.get('campaignIds',[]) if x!='VIKINGS_NORTH_ATLANTIC'];e['campaignIds']=ids+['VIKINGS_NORTH_ATLANTIC'];e['status']='PLAYABLE'
  e['description']='Аббасидский Багдад, средневековая Византия и северные морские сети показывают раннее Средневековье как мир региональных империй, портов, переводов, миграций и новых королевств VIII–XI веков.'
dump(Path('data/world/eras.json'),eras)

# Timeline.
wt=load(Path('data/world/timeline.json'));events=[
 {'year':750,'label':'Рибе и ранние торговые центры Скандинавии','detail':'Ремесленные и рыночные узлы расширяют дальние контакты до начала знаменитых западных набегов.','campaignId':'VIKINGS_NORTH_ATLANTIC','sourcePatch':'v8.4'},
 {'year':793,'label':'Нападение на Линдисфарн','detail':'Монастырский центр становится символом новой видимости скандинавских морских походов в западных хрониках.','campaignId':'VIKINGS_NORTH_ATLANTIC','sourcePatch':'v8.4'},
 {'year':841,'label':'Скандинавская база у Дублина','detail':'Военная стоянка постепенно превращается в городской и торговый центр Ирландского моря.','campaignId':'VIKINGS_NORTH_ATLANTIC','sourcePatch':'v8.4'},
 {'year':865,'label':'Большая языческая армия в Англии','detail':'Крупная коалиция переходит от сезонных набегов к зимовкам, завоеванию и разделу земель.','campaignId':'VIKINGS_NORTH_ATLANTIC','sourcePatch':'v8.4'},
 {'year':878,'label':'Соглашение Альфреда и Гутрума','detail':'Военный конфликт завершается крещением, договором и новым политическим разграничением.','campaignId':'VIKINGS_NORTH_ATLANTIC','sourcePatch':'v8.4'},
 {'year':911,'label':'Соглашение с Роллоном','detail':'Признанное поселение у нижней Сены становится ядром будущей Нормандии.','campaignId':'VIKINGS_NORTH_ATLANTIC','sourcePatch':'v8.4'},
 {'year':922,'label':'Ибн Фадлан встречает русов на Волге','detail':'Арабский дипломат оставляет внешнее описание конкретной торгово-военной группы.','campaignId':'VIKINGS_NORTH_ATLANTIC','sourcePatch':'v8.4'},
 {'year':930,'label':'Учреждение Альтинга','detail':'Общее собрание Исландии координирует право и союзы общества без местного короля.','campaignId':'VIKINGS_NORTH_ATLANTIC','sourcePatch':'v8.4'},
 {'year':965,'label':'Йеллингский камень Харальда','detail':'Надпись связывает династическую власть, объединение Дании и христианскую идентичность.','campaignId':'VIKINGS_NORTH_ATLANTIC','sourcePatch':'v8.4'},
 {'year':985,'label':'Основание норвежских поселений Гренландии','detail':'Переселенцы создают фермерские общины, зависимые от Атлантики и европейского рынка.','campaignId':'VIKINGS_NORTH_ATLANTIC','sourcePatch':'v8.4'},
 {'year':1000,'label':'Норвежские экспедиции к Северной Америке','detail':'Л’Анс-о-Медоус подтверждает кратковременную базу на Ньюфаундленде.','campaignId':'VIKINGS_NORTH_ATLANTIC','sourcePatch':'v8.4'},
 {'year':1016,'label':'Кнуд становится королём Англии','detail':'Североморская держава соединяет несколько королевств через разные элиты, налоги и военные системы.','campaignId':'VIKINGS_NORTH_ATLANTIC','sourcePatch':'v8.4'},
 {'year':1066,'label':'Стамфорд-Бридж как условный конец эпохи','detail':'Гибель Харальда Сурового стала удобным рубежом, хотя северная морская история продолжилась.','campaignId':'VIKINGS_NORTH_ATLANTIC','sourcePatch':'v8.4'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

# Image query group.
p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "VIKINGS_NORTH_ATLANTIC": {' not in s:
 marker='    "BYZANTIUM_MACEDONIAN": {';i=s.index(marker)
 group='''    "VIKINGS_NORTH_ATLANTIC": {\n        "terms": ["Viking ship", "Hedeby", "Birka", "Lindisfarne Vikings", "Danelaw York", "Viking Dublin", "Normandy Rollo", "Varangians Rus", "Thingvellir", "Norse Greenland", "L Anse aux Meadows", "Jelling stone"],\n        "base": [("ru", "викинги корабли Бирка Хедебю Исландия"), ("en", "Viking Age ships trade settlements North Atlantic"), ("en", "Viking archaeology runestone hoard longhouse")],\n    },\n'''
 s=s[:i]+group+s[i:]
old='("/byzantium-macedonian/", "BYZANTIUM_MACEDONIAN"),'
if '("/vikings-north-atlantic/", "VIKINGS_NORTH_ATLANTIC")' not in s:
 if old not in s:raise SystemExit('image marker missing')
 s=s.replace(old,'("/vikings-north-atlantic/", "VIKINGS_NORTH_ATLANTIC"), '+old)
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
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v8.3.0','codex-v8.4.0').replace('codex-v8\\.3\\.0','codex-v8\\.4\\.0')
 if rel=='index.html':t=re.sub(r'js/bootstrap\.js\?v=[0-9.]+',f'js/bootstrap.js?v={V}',t)
 p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v8-4-vikings-north-atlantic.js'" not in t:t=t.replace("'./js/features/v8-3-byzantium-macedonian.js'","'./js/features/v8-3-byzantium-macedonian.js','./js/features/v8-4-vikings-north-atlantic.js'")
if "'./assets/packs/vikings-north-atlantic-pack.svg'" not in t:t=t.replace("'./assets/packs/byzantium-macedonian-pack.svg'","'./assets/packs/byzantium-macedonian-pack.svg','./assets/packs/vikings-north-atlantic-pack.svg'")
p.write_text(t,encoding='utf-8')

# Bring old test expectations to current totals/version.
for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'8\.3\.0',r'8\.4\.0').replace('5523','5655').replace('5481','5613').replace('2659','2725')
 p.write_text(t,encoding='utf-8')

# Update earlier era membership expectations.
for name in ['smoke-v82-franks-transition.mjs','smoke-v83-byzantium-macedonian.mjs']:
 p=ROOT/'tools'/name;t=p.read_text(encoding='utf-8')
 t=t.replace("['ABBASID_BAGHDAD','BYZANTIUM_MACEDONIAN']","['ABBASID_BAGHDAD','BYZANTIUM_MACEDONIAN','VIKINGS_NORTH_ATLANTIC']")
 p.write_text(t,encoding='utf-8')

# Documentation.
(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v8.4\n\n## v8.5 — Славяне, Болгария, Великая Моравия и ранняя Русь\n\n- расселение славян и аварское пограничье;\n- Первое Болгарское царство и христианизация;\n- Великая Моравия, Кирилл и Мефодий;\n- Хазарский каганат, Новгород и Киев;\n- Владимир, крещение Руси и правление Ярослава.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v8_4.md').write_text('''# Patch v8.4.0 — Викинги и Северная Атлантика\n\n- 11 глав, 66 миссий и 132 карточки.\n- Скандинавское общество без отождествления всех жителей с участниками походов.\n- Разные типы кораблей, морская технология и навигация.\n- Линдисфарн, торговые города, Денло, Дублин, Нормандия и восточные маршруты.\n- Исландия, Гренландия, Винланд и археология Л’Анс-о-Медоус.\n- Королевская власть, христианизация и условный рубеж 1066 года.\n''',encoding='utf-8')
(ROOT/'docs/QA_v8_4.md').write_text('''# QA v8.4.0\n\n- Проверены 88 сюжетных и 44 архивных карточки.\n- Проверены 66 миссий, 66 уроков, 11 глав, 11 пулов и 11 личных историй.\n- Проверены карта, четыре фазы, архивный пак и четыре модуля итогового экзамена.\n- Проверены уникальность ID и названий во всём проекте.\n- Проверены связи с франками, Аббасидами, Византией, Русью и Америками.\n- Проверены миграция сейва, коллекция, прямые кнопки этапов урока и PWA-кэш.\n''',encoding='utf-8')
p=ROOT/'README.md';s=p.read_text(encoding='utf-8');s=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',s,count=1,flags=re.M);block='''\n## v8.4.0 — Викинги и Северная Атлантика\n\n- 11 глав, 66 миссий и 132 карточки.\n- Корабли, набеги, рынки, Британия, Нормандия, Русь и Северная Атлантика.\n- Исландия, Гренландия, Винланд, королевства и христианизация.\n- Patch-only архив.\n\n'''
if '## v8.4.0' not in s:s=s.replace('\n',block,1)
p.write_text(s,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';s=p.read_text(encoding='utf-8');block='''\n\n## v8.4 — Викинги и Северная Атлантика\n\nЛокальные SVG-обложки 132 карточек и кампанийного пака созданы для Codex of History. Источниковая рамка опирается на National Museum of Denmark, Viking Ship Museum Roskilde, Metropolitan Museum of Art, UNESCO Þingvellir и UNESCO L’Anse aux Meadows.\n'''
if '## v8.4 —' not in s:s+=block
p.write_text(s,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test:v84']='node tools/smoke-v84-vikings.mjs && node tools/runtime-v84-vikings.mjs'
if 'tools/smoke-v84-vikings.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v84-vikings.mjs && node tools/runtime-v84-vikings.mjs'
dump(Path('package.json'),pkg)
print('integrated v8.4 Viking campaign')
