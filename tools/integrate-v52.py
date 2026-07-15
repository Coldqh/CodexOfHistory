#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];V='5.2.0'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for key,vals in [('cards',['data/cards/alexander/story.json','data/cards/alexander/archive.json']),('pools',['data/campaigns/alexander/pools.json']),('quizzes',['data/quizzes/alexander/campaign.json']),('stories',['data/stories/alexander/personal.json']),('lessons',['data/lessons/alexander/campaign.json']),('campaigns',['data/campaigns/alexander/campaign.json'])]:
 for x in vals:
  if x not in d[key]:d[key].append(x)
d['maps']['ALEXANDER']='data/maps/alexander.json';script='js/features/v5-2-alexander.js'
if script not in m['scripts']:m['scripts'].insert(m['scripts'].index('js/features/v3-1-1-hotfix.js'),script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));add=load(Path('data/core/relations-v52-alexander.json'));rels=[x for x in rels if not str(x.get('id','')).startswith('REL_ALX_')];rels.extend(add);dump(Path('data/core/relations.json'),rels);(ROOT/'data/core/relations-v52-alexander.json').unlink(missing_ok=True)
world=load(Path('data/world/campaigns.json'));camp=load(Path('data/campaigns/alexander/campaign.json'))
for c in world:
 if c['id']=='ALEXANDER':c.update({'title':'Александр Македонский','subtitle':'Поход от Македонии до Инда','period':'336–323 до н. э.','chapterCount':10,'releasedChapters':10,'status':'PLAYABLE','region':'Македония, Ахеменидская Азия и северо-западная Индия','description':camp['description'],'chapters':[{'number':x['number'],'title':x['title']} for x in camp['chapters']]})
dump(Path('data/world/campaigns.json'),world)

wt=load(Path('data/world/timeline.json'));new=[
 {'year':-336,'label':'Воцарение Александра','detail':'После убийства Филиппа II двадцатилетний царь удерживает Македонию и Коринфский союз.','campaignId':'ALEXANDER','sourcePatch':'v5.2'},
 {'year':-334,'label':'Граник и начало азиатского похода','detail':'Переход через Геллеспонт и победа над сатрапскими силами открывают Малую Азию.','campaignId':'ALEXANDER','sourcePatch':'v5.2'},
 {'year':-333,'label':'Битва при Иссе','detail':'Дарий III терпит поражение в Киликии.','campaignId':'ALEXANDER','sourcePatch':'v5.2'},
 {'year':-332,'label':'Взятие Тира и Египта','detail':'Захват финикийского побережья лишает Персию морских баз.','campaignId':'ALEXANDER','sourcePatch':'v5.2'},
 {'year':-331,'label':'Гавгамелы и вступление в Вавилон','detail':'Главная армия Дария разбита, а царские центры переходят под власть Александра.','campaignId':'ALEXANDER','sourcePatch':'v5.2'},
 {'year':-330,'label':'Пожар Персеполя и смерть Дария','detail':'Ахеменидская центральная власть рушится, но война продолжается на востоке.','campaignId':'ALEXANDER','sourcePatch':'v5.2'},
 {'year':-327,'label':'Согдийская скала и брак с Роксаной','detail':'Александр закрепляет власть в Бактрии и Согдиане.','campaignId':'ALEXANDER','sourcePatch':'v5.2'},
 {'year':-326,'label':'Гидасп и отказ на Гифасисе','detail':'Победа над Пором сменяется отказом армии идти дальше.','campaignId':'ALEXANDER','sourcePatch':'v5.2'},
 {'year':-324,'label':'Свадьбы в Сузах и мятеж в Описе','detail':'Попытка перестроить элиту и армию вызывает сопротивление ветеранов.','campaignId':'ALEXANDER','sourcePatch':'v5.2'},
 {'year':-323,'label':'Смерть Александра в Вавилоне','detail':'Отсутствие взрослого наследника открывает борьбу диадохов.','campaignId':'ALEXANDER','sourcePatch':'v5.2'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)
im=load(Path('data/image_manifest.json'));existing={x['cardId']:x for x in im.get('images',[])}
for c in load(Path('data/cards/alexander/story.json'))+load(Path('data/cards/alexander/archive.json')):existing[c['id']]={'cardId':c['id'],'local':c['image']['local'],'file':c['image']['file'],'kind':'project-cover','prefer_remote':False,'caption':c['image']['caption'],'credit':c['image']['credit'],'source_url':c['image']['source_url'],'license':c['image']['license']}
images=list(existing.values());historical=sum(1 for x in images if x.get('prefer_remote'));im.update({'version':V,'generatedAt':'2026-07-15','count':len(images),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(images)-historical,'dynamicQueryCount':len(images)-historical,'images':images});dump(Path('data/image_manifest.json'),im)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('# Следующий этап после v5.2\n\n## v5.3 — общий слой классического мира\n\n- Персия, полисы и Македония на одной карте;\n- параллельная хронология 550–323 годов до н. э.;\n- сравнение империи, полиса и завоевательной монархии;\n- экзамен эпохи.\n',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v5_2.md').write_text('# Patch v5.2.0 — Александр Македонский\n\n- 10 глав, 60 миссий и 120 карточек.\n- Македония, Персия, Египет, Центральная Азия, Индия и кризис наследования.\n- 10 пулов, 10 личных историй, карта и отдельный пак.\n',encoding='utf-8')
(ROOT/'docs/QA_v5_2.md').write_text('# QA v5.2.0\n\n- 120 карточек, 60 миссий, 14 квизов;\n- старт только с ALX_S_01_01–03;\n- пак выдаёт только ALX_A_*;\n- карта, четыре фазы и итоговый экзамен;\n- версии, изображения и runtime-модули.\n',encoding='utf-8')

p=ROOT/'README.md';txt=p.read_text(encoding='utf-8');txt=re.sub(r'^# Codex of History v[^\n]+','# Codex of History v5.2.0',txt,count=1,flags=re.M);sec='\n## v5.2.0 — Александр Македонский\n\n- 10 глав, 60 миссий и 120 карточек.\n- От Македонии и Граника до Индии, Вавилона и кризиса наследования.\n- Patch-only архив.\n\n';txt=txt if '## v5.2.0' in txt else txt.replace('\n',sec,1);p.write_text(txt,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';txt=p.read_text(encoding='utf-8');sec='\n## v5.2 — Александр Македонский\n\nЛокальные SVG-обложки 120 карточек и обложка пака созданы для Codex of History. Источники: Metropolitan Museum of Art, British Museum, UNESCO и Perseus Digital Library.\n';p.write_text(txt if '## v5.2 —' in txt else txt+sec,encoding='utf-8')

# Image query generator: add campaign context and update version.
p=ROOT/'tools/build-image-queries.py';txt=p.read_text(encoding='utf-8').replace('VERSION = "5.1.0"','VERSION = "5.2.0"')
if '"ALEXANDER": {' not in txt:
 marker='    "MIXED": {'
 block='    "ALEXANDER": {\n        "terms": ["александр", "alexander", "македон", "macedon", "дарий", "darius", "перс", "persian", "гавгамел", "gaugamela", "бактр", "bactria", "инд", "india"],\n        "base": [("ru", "Александр Македонский"), ("en", "Alexander the Great"), ("en", "Wars of Alexander the Great")],\n    },\n'
 txt=txt.replace(marker,block+marker,1)
 txt=txt.replace('("/classical-greece/", "GREECE_CLASSICAL"),','("/classical-greece/", "GREECE_CLASSICAL"), ("/alexander/", "ALEXANDER"),')
p.write_text(txt,encoding='utf-8')

for path in (ROOT/'js').rglob('*.js'):path.write_text(path.read_text(encoding='utf-8').replace('5.1.0',V),encoding='utf-8')
for path in (ROOT/'tools').glob('*.mjs'):
 txt=path.read_text(encoding='utf-8').replace('5.1.0',V).replace('2651','2771').replace('2609','2729')
 path.write_text(txt,encoding='utf-8')
pkg=load(Path('package.json'));pkg['version']=V
if 'smoke-v52-alexander.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v52-alexander.mjs && node tools/runtime-v52-alexander.mjs'
pkg['scripts']['test:v52']='node tools/smoke-v52-alexander.mjs && node tools/runtime-v52-alexander.mjs';dump(Path('package.json'),pkg)
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;p.write_text(p.read_text(encoding='utf-8').replace('5.1.0',V).replace('codex-v5.1.0','codex-v5.2.0'),encoding='utf-8')
p=ROOT/'sw.js';txt=p.read_text(encoding='utf-8');txt=txt.replace("'./assets/packs/alexander-pack.svg',",'').replace("'./assets/packs/alexander-pack.svg'",'').replace("'./js/features/v5-2-alexander.js',",'').replace("'./js/features/v5-2-alexander.js'",'');txt=txt.replace("'./assets/packs/classical-greece-pack.svg',","'./assets/packs/classical-greece-pack.svg','./assets/packs/alexander-pack.svg',").replace("'./js/features/v5-1-classical-greece.js',","'./js/features/v5-1-classical-greece.js','./js/features/v5-2-alexander.js',");p.write_text(txt,encoding='utf-8')
print('integrated v5.2')
