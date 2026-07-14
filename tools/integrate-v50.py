#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];V='5.0.0'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for key,vals in [('cards',['data/cards/achaemenid-persia/story.json','data/cards/achaemenid-persia/archive.json']),('pools',['data/campaigns/achaemenid-persia/pools.json']),('quizzes',['data/quizzes/achaemenid-persia/campaign.json']),('stories',['data/stories/achaemenid-persia/personal.json']),('lessons',['data/lessons/achaemenid-persia/campaign.json']),('campaigns',['data/campaigns/achaemenid-persia/campaign.json'])]:
 for x in vals:
  if x not in d[key]:d[key].append(x)
d['maps']['PERSIA']='data/maps/achaemenid-persia.json';script='js/features/v5-0-achaemenid-persia.js'
if script not in m['scripts']:m['scripts'].insert(m['scripts'].index('js/features/v3-1-1-hotfix.js'),script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));add=load(Path('data/core/relations-v50-persia.json'));known={x['id'] for x in rels};rels.extend(x for x in add if x['id'] not in known);dump(Path('data/core/relations.json'),rels);(ROOT/'data/core/relations-v50-persia.json').unlink(missing_ok=True)
world=load(Path('data/world/campaigns.json'));camp=load(Path('data/campaigns/achaemenid-persia/campaign.json'))
for c in world:
 if c['id']=='PERSIA':c.update({'title':'Ахеменидская Персия','subtitle':'Царь царей, сатрапии и дороги','period':'ок. 550–330 до н. э.','chapterCount':10,'releasedChapters':10,'status':'PLAYABLE','region':'Иран, Передняя Азия и Восточное Средиземноморье','description':camp['description'],'chapters':[{'number':x['number'],'title':x['title']} for x in camp['chapters']]})
dump(Path('data/world/campaigns.json'),world)

wt=load(Path('data/world/timeline.json'));new=[
 {'year':-550,'label':'Кир II подчиняет Мидию','detail':'Персидское царство начинает быстрое расширение в Иране.','campaignId':'PERSIA','sourcePatch':'v5.0'},
 {'year':-546,'label':'Падение Лидийского царства','detail':'Сарды и западная Малая Азия входят в державу Кира.','campaignId':'PERSIA','sourcePatch':'v5.0'},
 {'year':-539,'label':'Кир завоёвывает Вавилон','detail':'Ахемениды принимают вавилонские царские титулы и институты.','campaignId':'PERSIA','sourcePatch':'v5.0'},
 {'year':-525,'label':'Камбис II завоёвывает Египет','detail':'Египет становится частью Ахеменидской державы.','campaignId':'PERSIA','sourcePatch':'v5.0'},
 {'year':-522,'label':'Дарий I приходит к власти','detail':'Восстания и Бехистунская надпись формируют новую царскую законность.','campaignId':'PERSIA','sourcePatch':'v5.0'},
 {'year':-518,'label':'Начало строительства Персеполя','detail':'Дворцовый комплекс становится символом многоязычной монархии.','campaignId':'PERSIA','sourcePatch':'v5.0'},
 {'year':-499,'label':'Начало Ионийского восстания','detail':'Конфликт западных сатрапий перерастает в войны с греческими полисами.','campaignId':'PERSIA','sourcePatch':'v5.0'},
 {'year':-480,'label':'Поход Ксеркса и битва при Саламине','detail':'Большая экспедиция не закрепляет власть в материковой Греции.','campaignId':'PERSIA','sourcePatch':'v5.0'},
 {'year':-401,'label':'Битва при Кунаксе','detail':'Династический конфликт показывает силу и напряжение поздней державы.','campaignId':'PERSIA','sourcePatch':'v5.0'},
 {'year':-330,'label':'Конец династии Ахеменидов','detail':'После побед Александра и гибели Дария III начинается эллинистический этап.','campaignId':'PERSIA','sourcePatch':'v5.0'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)
im=load(Path('data/image_manifest.json'));existing={x['cardId']:x for x in im.get('images',[])}
for c in load(Path('data/cards/achaemenid-persia/story.json'))+load(Path('data/cards/achaemenid-persia/archive.json')):existing[c['id']]={'cardId':c['id'],'local':c['image']['local'],'file':c['image']['file'],'kind':'project-cover','prefer_remote':False,'caption':c['image']['caption'],'credit':c['image']['credit'],'source_url':c['image']['source_url'],'license':c['image']['license']}
images=list(existing.values());historical=sum(1 for x in images if x.get('prefer_remote'));im.update({'version':V,'generatedAt':'2026-07-14','count':len(images),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(images)-historical,'dynamicQueryCount':len(images)-historical,'images':images});dump(Path('data/image_manifest.json'),im)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('# Следующий этап после v5.0\n\n## v5.1 — Классическая Греция\n\n- Афины и Спарта после Персидских войн;\n- демократия, империя и Пелопоннесская война;\n- философия, театр, искусство и источники;\n- итоговый экзамен кампании.\n',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v5_0.md').write_text('# Patch v5.0.0 — Ахеменидская Персия\n\n- 10 глав, 60 миссий и 120 карточек.\n- Кир II, Камбис, Дарий I, сатрапии, дороги, Персеполь, Персидские войны и падение династии.\n- 10 пулов, 10 личных историй, карта и отдельный пак.\n',encoding='utf-8')
(ROOT/'docs/QA_v5_0.md').write_text('# QA v5.0.0\n\n- 120 карточек, 60 миссий, 14 квизов;\n- старт только с PER_S_01_01–03;\n- пак выдаёт только PER_A_*;\n- карта, четыре фазы и итоговый экзамен;\n- версии, изображения и runtime-модули.\n',encoding='utf-8')

p=ROOT/'README.md';txt=p.read_text(encoding='utf-8');txt=re.sub(r'^# Codex of History v[^\n]+','# Codex of History v5.0.0',txt,count=1,flags=re.M);sec='\n## v5.0.0 — Ахеменидская Персия\n\n- 10 глав, 60 миссий и 120 карточек.\n- Кир II, Дарий I, сатрапии, дороги, Персеполь и падение династии.\n- Patch-only архив.\n\n';txt=txt if '## v5.0.0' in txt else txt.replace('\n',sec,1);p.write_text(txt,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';txt=p.read_text(encoding='utf-8');sec='\n## v5.0 — Ахеменидская Персия\n\nЛокальные SVG-обложки 120 карточек и обложка пака созданы для Codex of History. Источники: Metropolitan Museum of Art, British Museum, UNESCO и Encyclopaedia Iranica.\n';p.write_text(txt if '## v5.0 —' in txt else txt+sec,encoding='utf-8')

for path in (ROOT/'js').rglob('*.js'):path.write_text(path.read_text(encoding='utf-8').replace('4.6.0',V),encoding='utf-8')
for path in (ROOT/'tools').glob('*.mjs'):
 txt=path.read_text(encoding='utf-8').replace('4.6.0',V).replace('2411','2531').replace('2369','2489')
 path.write_text(txt,encoding='utf-8')
pkg=load(Path('package.json'));pkg['version']=V
if 'smoke-v50-achaemenid-persia.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v50-achaemenid-persia.mjs && node tools/runtime-v50-achaemenid-persia.mjs'
pkg['scripts']['test:v50']='node tools/smoke-v50-achaemenid-persia.mjs && node tools/runtime-v50-achaemenid-persia.mjs';dump(Path('package.json'),pkg)
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;p.write_text(p.read_text(encoding='utf-8').replace('4.6.0',V).replace('codex-v4.6.0','codex-v5.0.0'),encoding='utf-8')
p=ROOT/'sw.js';txt=p.read_text(encoding='utf-8');txt=txt.replace("'./assets/packs/iron-era-pack.svg',","'./assets/packs/iron-era-pack.svg','./assets/packs/achaemenid-persia-pack.svg',").replace("'./js/features/v4-6-iron-world.js',","'./js/features/v4-6-iron-world.js','./js/features/v5-0-achaemenid-persia.js',");p.write_text(txt,encoding='utf-8')
print('integrated v5.0')
