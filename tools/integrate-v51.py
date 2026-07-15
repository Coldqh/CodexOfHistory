#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];V='5.1.0'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for key,vals in [('cards',['data/cards/classical-greece/story.json','data/cards/classical-greece/archive.json']),('pools',['data/campaigns/classical-greece/pools.json']),('quizzes',['data/quizzes/classical-greece/campaign.json']),('stories',['data/stories/classical-greece/personal.json']),('lessons',['data/lessons/classical-greece/campaign.json']),('campaigns',['data/campaigns/classical-greece/campaign.json'])]:
 for x in vals:
  if x not in d[key]:d[key].append(x)
d['maps']['GREECE_CLASSICAL']='data/maps/classical-greece.json';script='js/features/v5-1-classical-greece.js'
if script not in m['scripts']:m['scripts'].insert(m['scripts'].index('js/features/v3-1-1-hotfix.js'),script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));add=load(Path('data/core/relations-v51-classical-greece.json'));rels=[x for x in rels if not str(x.get('id','')).startswith('REL_CLG_')];rels.extend(add);dump(Path('data/core/relations.json'),rels);(ROOT/'data/core/relations-v51-classical-greece.json').unlink(missing_ok=True)
world=load(Path('data/world/campaigns.json'));camp=load(Path('data/campaigns/classical-greece/campaign.json'))
for c in world:
 if c['id']=='GREECE_CLASSICAL':c.update({'title':'Классическая Греция','subtitle':'Полисы, союзы и войны','period':'479–338 до н. э.','chapterCount':10,'releasedChapters':10,'status':'PLAYABLE','region':'Греция, Эгейское море и Сицилия','description':camp['description'],'chapters':[{'number':x['number'],'title':x['title']} for x in camp['chapters']]})
dump(Path('data/world/campaigns.json'),world)

wt=load(Path('data/world/timeline.json'));new=[
 {'year':-479,'label':'Платеи и Микале','detail':'Победы союзников завершают вторжение Ксеркса и меняют баланс в Эгейском мире.','campaignId':'GREECE_CLASSICAL','sourcePatch':'v5.1'},
 {'year':-478,'label':'Создание Делосского союза','detail':'Морские полисы объединяются под руководством Афин.','campaignId':'GREECE_CLASSICAL','sourcePatch':'v5.1'},
 {'year':-454,'label':'Казна союза перенесена в Афины','detail':'Афинский контроль над союзной системой становится заметнее.','campaignId':'GREECE_CLASSICAL','sourcePatch':'v5.1'},
 {'year':-447,'label':'Начало строительства Парфенона','detail':'Акрополь становится центром монументальной программы Афин.','campaignId':'GREECE_CLASSICAL','sourcePatch':'v5.1'},
 {'year':-431,'label':'Начало Пелопоннесской войны','detail':'Конфликт Афинского и Пелопоннесского союзов охватывает греческий мир.','campaignId':'GREECE_CLASSICAL','sourcePatch':'v5.1'},
 {'year':-415,'label':'Сицилийская экспедиция','detail':'Афины отправляют крупные силы против Сиракуз.','campaignId':'GREECE_CLASSICAL','sourcePatch':'v5.1'},
 {'year':-404,'label':'Капитуляция Афин','detail':'Победа Спарты завершает Пелопоннесскую войну.','campaignId':'GREECE_CLASSICAL','sourcePatch':'v5.1'},
 {'year':-371,'label':'Битва при Левктрах','detail':'Фиванцы разрушают спартанскую сухопутную гегемонию.','campaignId':'GREECE_CLASSICAL','sourcePatch':'v5.1'},
 {'year':-362,'label':'Битва при Мантинее','detail':'Фиванское лидерство не превращается в устойчивый общий порядок.','campaignId':'GREECE_CLASSICAL','sourcePatch':'v5.1'},
 {'year':-338,'label':'Битва при Херонее','detail':'Филипп II подчиняет ключевые полисы македонской гегемонии.','campaignId':'GREECE_CLASSICAL','sourcePatch':'v5.1'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)
im=load(Path('data/image_manifest.json'));existing={x['cardId']:x for x in im.get('images',[])}
for c in load(Path('data/cards/classical-greece/story.json'))+load(Path('data/cards/classical-greece/archive.json')):existing[c['id']]={'cardId':c['id'],'local':c['image']['local'],'file':c['image']['file'],'kind':'project-cover','prefer_remote':False,'caption':c['image']['caption'],'credit':c['image']['credit'],'source_url':c['image']['source_url'],'license':c['image']['license']}
images=list(existing.values());historical=sum(1 for x in images if x.get('prefer_remote'));im.update({'version':V,'generatedAt':'2026-07-15','count':len(images),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(images)-historical,'dynamicQueryCount':len(images)-historical,'images':images});dump(Path('data/image_manifest.json'),im)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('# Следующий этап после v5.1\n\n## v5.2 — Александр Македонский\n\n- Филипп II и подготовка похода;\n- Граник, Исс, Тир и Египет;\n- Гавгамелы, Центральная Азия и Индия;\n- смерть Александра и проблема наследия.\n',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v5_1.md').write_text('# Patch v5.1.0 — Классическая Греция\n\n- 10 глав, 60 миссий и 120 карточек.\n- Афинская демократия, Делосский союз, Спарта, Пелопоннесская война, IV век и Македония.\n- 10 пулов, 10 личных историй, карта и отдельный пак.\n',encoding='utf-8')
(ROOT/'docs/QA_v5_1.md').write_text('# QA v5.1.0\n\n- 120 карточек, 60 миссий, 14 квизов;\n- старт только с CLG_S_01_01–03;\n- пак выдаёт только CLG_A_*;\n- карта, четыре фазы и итоговый экзамен;\n- версии, изображения и runtime-модули.\n',encoding='utf-8')

p=ROOT/'README.md';txt=p.read_text(encoding='utf-8');txt=re.sub(r'^# Codex of History v[^\n]+','# Codex of History v5.1.0',txt,count=1,flags=re.M);sec='\n## v5.1.0 — Классическая Греция\n\n- 10 глав, 60 миссий и 120 карточек.\n- Афины, Спарта, союзы, Пелопоннесская война и подъём Македонии.\n- Patch-only архив.\n\n';txt=txt if '## v5.1.0' in txt else txt.replace('\n',sec,1);p.write_text(txt,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';txt=p.read_text(encoding='utf-8');sec='\n## v5.1 — Классическая Греция\n\nЛокальные SVG-обложки 120 карточек и обложка пака созданы для Codex of History. Источники: Metropolitan Museum of Art, British Museum, UNESCO и Perseus Digital Library.\n';p.write_text(txt if '## v5.1 —' in txt else txt+sec,encoding='utf-8')

for path in (ROOT/'js').rglob('*.js'):path.write_text(path.read_text(encoding='utf-8').replace('5.0.0',V),encoding='utf-8')
for path in (ROOT/'tools').glob('*.mjs'):
 txt=path.read_text(encoding='utf-8').replace('5.0.0',V).replace('2531','2651').replace('2489','2609')
 path.write_text(txt,encoding='utf-8')
pkg=load(Path('package.json'));pkg['version']=V
if 'smoke-v51-classical-greece.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v51-classical-greece.mjs && node tools/runtime-v51-classical-greece.mjs'
pkg['scripts']['test:v51']='node tools/smoke-v51-classical-greece.mjs && node tools/runtime-v51-classical-greece.mjs';dump(Path('package.json'),pkg)
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;p.write_text(p.read_text(encoding='utf-8').replace('5.0.0',V).replace('codex-v5.0.0','codex-v5.1.0'),encoding='utf-8')
p=ROOT/'sw.js';txt=p.read_text(encoding='utf-8');txt=txt.replace("'./assets/packs/classical-greece-pack.svg',",'').replace("'./assets/packs/classical-greece-pack.svg'",'').replace("'./js/features/v5-1-classical-greece.js',",'').replace("'./js/features/v5-1-classical-greece.js'",'');txt=txt.replace("'./assets/packs/achaemenid-persia-pack.svg',","'./assets/packs/achaemenid-persia-pack.svg','./assets/packs/classical-greece-pack.svg',").replace("'./js/features/v5-0-achaemenid-persia.js',","'./js/features/v5-0-achaemenid-persia.js','./js/features/v5-1-classical-greece.js',");p.write_text(txt,encoding='utf-8')
print('integrated v5.1')
