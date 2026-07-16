#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='8.5.0';OLD='8.4.0';CHECKED='2026-07-16'

def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={
 'cards':['data/cards/slavic-bulgaria-rus/story.json','data/cards/slavic-bulgaria-rus/archive.json'],
 'campaigns':['data/campaigns/slavic-bulgaria-rus/campaign.json'],
 'pools':['data/campaigns/slavic-bulgaria-rus/pools.json'],
 'quizzes':['data/quizzes/slavic-bulgaria-rus/campaign.json'],
 'stories':['data/stories/slavic-bulgaria-rus/personal.json'],
 'lessons':['data/lessons/slavic-bulgaria-rus/campaign.json'],
}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['SLAVIC_BULGARIA_RUS']='data/maps/slavic-bulgaria-rus.json'
script='js/features/v8-5-slavic-bulgaria-rus.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));rels=[r for r in rels if not re.fullmatch(r'REL_SLR_\d{4}',r.get('id',''))]
new=load(Path('data/core/relations-850-slavic-bulgaria-rus.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/slavic-bulgaria-rus/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
entry={'id':'SLAVIC_BULGARIA_RUS','eraId':'ERA_EARLY_MEDIEVAL','order':42,'title':'Славяне, Болгария, Великая Моравия и ранняя Русь','subtitle':'Державы, письменность и города от Дуная до Киева','period':'VI–XI века','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Центральная, Юго-Восточная и Восточная Европа','description':'Славянские общества, Аварский каганат, Первое Болгарское царство, Великая Моравия, Преслав и Охрид, Хазария, формирование Руси, крещение Киева и правление Ярослава.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]}
world=[c for c in world if c['id']!='SLAVIC_BULGARIA_RUS'];world.append(entry);world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)
eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_EARLY_MEDIEVAL':
  ids=[x for x in e.get('campaignIds',[]) if x!='SLAVIC_BULGARIA_RUS'];e['campaignIds']=ids+['SLAVIC_BULGARIA_RUS'];e['status']='PLAYABLE'
  e['description']='Аббасидский Багдад, средневековая Византия, северные морские сети и славяноязычные державы показывают раннее Средневековье как мир империй, княжеств, торговых путей, миссий и новых письменных культур VIII–XI веков.'
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'));events=[
 {'year':568,'label':'Авары закрепляются в Карпатском бассейне','detail':'Каганат соединяет степную военную власть, дань и разнообразное население Среднего Дуная.','campaignId':'SLAVIC_BULGARIA_RUS','sourcePatch':'v8.5'},
 {'year':626,'label':'Неудачная аваро-славянская осада Константинополя','detail':'Поражение коалиции ослабляет престиж кагана и меняет дунайское пограничье.','campaignId':'SLAVIC_BULGARIA_RUS','sourcePatch':'v8.5'},
 {'year':681,'label':'Договор закрепляет Болгарию у нижнего Дуная','detail':'Империя признаёт новую политическую силу после победы Аспаруха у Онгала.','campaignId':'SLAVIC_BULGARIA_RUS','sourcePatch':'v8.5'},
 {'year':811,'label':'Гибель императора Никифора I в войне с Крумом','detail':'Разорение Плиски сменяется разгромом имперской армии в горном проходе.','campaignId':'SLAVIC_BULGARIA_RUS','sourcePatch':'v8.5'},
 {'year':815,'label':'Омуртаг заключает длительный мир с Византией','detail':'Договор открывает период строительства и внутреннего укрепления Болгарии.','campaignId':'SLAVIC_BULGARIA_RUS','sourcePatch':'v8.5'},
 {'year':863,'label':'Начинается миссия Кирилла и Мефодия в Моравии','detail':'Глаголица и переводы становятся инструментом церковной самостоятельности.','campaignId':'SLAVIC_BULGARIA_RUS','sourcePatch':'v8.5'},
 {'year':865,'label':'Христианизация болгарского двора','detail':'Крещение Бориса запускает долгую перестройку власти, права и церковной сети.','campaignId':'SLAVIC_BULGARIA_RUS','sourcePatch':'v8.5'},
 {'year':886,'label':'Ученики Мефодия находят покровительство в Болгарии','detail':'Преслав и Охрид превращаются в центры славяноязычной книжности.','campaignId':'SLAVIC_BULGARIA_RUS','sourcePatch':'v8.5'},
 {'year':911,'label':'Договор Руси с Византией','detail':'Правовые нормы и имена участников фиксируют сложившуюся торгово-военную группу.','campaignId':'SLAVIC_BULGARIA_RUS','sourcePatch':'v8.5'},
 {'year':927,'label':'Мир закрепляет болгарский царский и церковный статус','detail':'Договор завершает цикл войн Симеона и оформляет новый баланс на Балканах.','campaignId':'SLAVIC_BULGARIA_RUS','sourcePatch':'v8.5'},
 {'year':965,'label':'Походы Святослава разрушают главные центры Хазарии','detail':'Степные и речные сети перестраиваются, но не исчезают вместе с политическим центром.','campaignId':'SLAVIC_BULGARIA_RUS','sourcePatch':'v8.5'},
 {'year':988,'label':'Крещение Владимира и Киева','detail':'Публичный обряд становится рубежом, за которым следует долгая христианизация земель Руси.','campaignId':'SLAVIC_BULGARIA_RUS','sourcePatch':'v8.5'},
 {'year':1037,'label':'София Киевская и новая программа столицы','detail':'Собор, книжность и церковная иерархия выражают княжескую власть Ярослава.','campaignId':'SLAVIC_BULGARIA_RUS','sourcePatch':'v8.5'},
 {'year':1054,'label':'Смерть Ярослава и новый порядок наследования','detail':'Совместное владение династии сохраняет связи земель, но создаёт будущие конфликты.','campaignId':'SLAVIC_BULGARIA_RUS','sourcePatch':'v8.5'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "SLAVIC_BULGARIA_RUS": {' not in s:
 marker='    "VIKINGS_NORTH_ATLANTIC": {';i=s.index(marker)
 group='''    "SLAVIC_BULGARIA_RUS": {\n        "terms": ["Avar archaeology", "Madara Rider", "Pliska", "Preslav", "Cyril Methodius", "Great Moravia Mikulcice", "Khazar Sarkel", "Staraya Ladoga", "Gnezdovo", "Kievan Rus", "Saint Sophia Kyiv", "Novgorod birch bark"],\n        "base": [("ru", "славяне Болгария Великая Моравия ранняя Русь"), ("en", "early Slavs Bulgaria Great Moravia Kievan Rus archaeology"), ("en", "Avar Khazar Cyril Methodius medieval Eastern Europe")],\n    },\n'''
 s=s[:i]+group+s[i:]
old='("/vikings-north-atlantic/", "VIKINGS_NORTH_ATLANTIC"),'
if '("/slavic-bulgaria-rus/", "SLAVIC_BULGARIA_RUS")' not in s:
 if old not in s:raise SystemExit('image marker missing')
 s=s.replace(old,'("/slavic-bulgaria-rus/", "SLAVIC_BULGARIA_RUS"), '+old)
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
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v8.4.0','codex-v8.5.0').replace('codex-v8\\.4\\.0','codex-v8\\.5\\.0')
 if rel=='index.html':t=re.sub(r'js/bootstrap\.js\?v=[0-9.]+',f'js/bootstrap.js?v={V}',t)
 p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v8-5-slavic-bulgaria-rus.js'" not in t:t=t.replace("'./js/features/v8-4-vikings-north-atlantic.js'","'./js/features/v8-4-vikings-north-atlantic.js','./js/features/v8-5-slavic-bulgaria-rus.js'")
if "'./assets/packs/slavic-bulgaria-rus-pack.svg'" not in t:t=t.replace("'./assets/packs/vikings-north-atlantic-pack.svg'","'./assets/packs/vikings-north-atlantic-pack.svg','./assets/packs/slavic-bulgaria-rus-pack.svg'")
p.write_text(t,encoding='utf-8')

for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'8\.4\.0',r'8\.5\.0').replace('5655','5787').replace('5613','5745').replace('2725','2791')
 p.write_text(t,encoding='utf-8')

p=ROOT/'tools/smoke-v82-franks-transition.mjs';t=p.read_text(encoding='utf-8');t=t.replace("['ABBASID_BAGHDAD','BYZANTIUM_MACEDONIAN','VIKINGS_NORTH_ATLANTIC']","['ABBASID_BAGHDAD','BYZANTIUM_MACEDONIAN','VIKINGS_NORTH_ATLANTIC','SLAVIC_BULGARIA_RUS']");p.write_text(t,encoding='utf-8')

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v8.5\n\n## v8.6 — Аль-Андалус и исламский Запад\n\n- Омейядский эмират и халифат Кордовы;\n- города, ирригация, ремесло и Средиземноморье;\n- христиане, иудеи, мусульмане и меняющиеся правовые статусы;\n- Магриб, берберские государства и торговые сети;\n- распад халифата и возникновение тайф.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v8_5.md').write_text('''# Patch v8.5.0 — Славяне, Болгария, Великая Моравия и ранняя Русь\n\n- 11 глав, 66 миссий и 132 карточки.\n- Ранние славянские общества и ограничения внешних источников.\n- Аварский каганат, Первое Болгарское царство и христианизация.\n- Великая Моравия, глаголица, Преслав и Охрид.\n- Хазария, Ладога, Новгород, Киев и формирование Руси.\n- Ольга, Святослав, Владимир, Ярослав, право и города XI века.\n''',encoding='utf-8')
(ROOT/'docs/QA_v8_5.md').write_text('''# QA v8.5.0\n\n- Проверены 88 сюжетных и 44 архивных карточки.\n- Проверены 66 миссий, 66 уроков, 11 глав, 11 пулов и 11 личных историй.\n- Проверены карта, четыре фазы, архивный пак и четыре модуля итогового экзамена.\n- Проверены уникальность ID и названий во всём проекте.\n- Проверены связи с франками, Византией, викингами и старым модулем Руси.\n- Проверены миграция сейва, коллекция, прямые кнопки этапов урока и PWA-кэш.\n''',encoding='utf-8')
p=ROOT/'README.md';s=p.read_text(encoding='utf-8');s=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',s,count=1,flags=re.M);block='''\n## v8.5.0 — Славяне, Болгария, Великая Моравия и ранняя Русь\n\n- 11 глав, 66 миссий и 132 карточки.\n- Аварское пограничье, Болгария, Моравия, Хазария и Русь VI–XI веков.\n- Письменность, христианизация, торговые пути, право и города.\n- Patch-only архив.\n\n'''
if '## v8.5.0' not in s:s=s.replace('\n',block,1)
p.write_text(s,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';s=p.read_text(encoding='utf-8');block='''\n\n## v8.5 — Славяне, Болгария, Великая Моравия и ранняя Русь\n\nЛокальные SVG-обложки 132 карточек и кампанийного пака созданы для Codex of History. Источниковая рамка опирается на UNESCO Madara Rider, UNESCO Saint-Sophia Kyiv, UNESCO Historic Monuments of Novgorod, маршрут Кирилла и Мефодия Совета Европы, Cambridge University Press и тексты Начальной летописи в Internet Medieval Sourcebook.\n'''
if '## v8.5 —' not in s:s+=block
p.write_text(s,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test:v85']='node tools/smoke-v85-slavic-bulgaria-rus.mjs && node tools/runtime-v85-slavic-bulgaria-rus.mjs'
if 'tools/smoke-v85-slavic-bulgaria-rus.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v85-slavic-bulgaria-rus.mjs && node tools/runtime-v85-slavic-bulgaria-rus.mjs'
dump(Path('package.json'),pkg)
print('integrated v8.5 Slavic, Bulgarian, Moravian and early Rus campaign')
