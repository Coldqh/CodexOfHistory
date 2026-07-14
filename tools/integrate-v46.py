#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];V='4.6.0'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for key,vals in [('cards',['data/cards/iron-world/story.json','data/cards/iron-world/archive.json']),('pools',['data/campaigns/iron-world/pools.json']),('quizzes',['data/quizzes/iron-world/campaign.json']),('stories',['data/stories/iron-world/personal.json']),('lessons',['data/lessons/iron-world/campaign.json']),('campaigns',['data/campaigns/iron-world/campaign.json'])]:
 for x in vals:
  if x not in d[key]:d[key].append(x)
d['maps']['IRON_ERA_EXAM']='data/maps/iron-world-exam.json';script='js/features/v4-6-iron-world.js'
if script not in m['scripts']:m['scripts'].insert(m['scripts'].index('js/features/v3-1-1-hotfix.js'),script)
dump(Path('data/content-manifest.json'),m)
rels=load(Path('data/core/relations.json'));add=load(Path('data/core/relations-v46-iron-world.json'));known={x['id'] for x in rels};rels.extend(x for x in add if x['id'] not in known);dump(Path('data/core/relations.json'),rels);(ROOT/'data/core/relations-v46-iron-world.json').unlink(missing_ok=True)
world=load(Path('data/world/campaigns.json'));camp=load(Path('data/campaigns/iron-world/campaign.json'))
entry={'id':'IRON_ERA_EXAM','eraId':'ERA_IRON','order':17,'title':camp['title'],'subtitle':'Империи, полисы, царства и ранние государства','period':'ок. 1200–500 до н. э.','chapterCount':8,'releasedChapters':8,'status':'PLAYABLE','region':'Средиземноморье, Передняя Азия, Китай и Северная Индия','description':camp['description'],'chapters':[{'number':x['number'],'title':x['title']} for x in camp['chapters']]}
world=[x for x in world if x['id']!='IRON_ERA_EXAM'];idx=next((i for i,x in enumerate(world) if x.get('id')=='PERSIA'),len(world));world.insert(idx,entry);dump(Path('data/world/campaigns.json'),world)
eras=load(Path('data/world/eras.json'));iron=next(e for e in eras if e['id']=='ERA_IRON');
if 'IRON_ERA_EXAM' not in iron['campaignIds']:iron['campaignIds'].append('IRON_ERA_EXAM')
dump(Path('data/world/eras.json'),eras)
wt=load(Path('data/world/timeline.json'));new=[
 {'year':-1200,'label':'Начало сравнительной шкалы железного века','detail':'Постбронзовая перестройка в Средиземноморье, Передней Азии и Азии.','campaignId':'IRON_ERA_EXAM','sourcePatch':'v4.6'},
 {'year':-1000,'label':'Региональные царства и новые сети','detail':'Финикийские города, левантийские царства, Чжоу и поздневедийские центры развиваются параллельно.','campaignId':'IRON_ERA_EXAM','sourcePatch':'v4.6'},
 {'year':-800,'label':'Империи, полисы и алфавиты','detail':'Расширение Ассирии, архаические полисы и рост письменных традиций.','campaignId':'IRON_ERA_EXAM','sourcePatch':'v4.6'},
 {'year':-700,'label':'Урбанизация и военная мобилизация','detail':'Крупные столицы, порты, города Восточной Чжоу и центры долины Ганга.','campaignId':'IRON_ERA_EXAM','sourcePatch':'v4.6'},
 {'year':-612,'label':'Падение Ниневии в общей шкале','detail':'Конец Новоассирийской державы не завершает железный век в других регионах.','campaignId':'IRON_ERA_EXAM','sourcePatch':'v4.6'},
 {'year':-550,'label':'Граница с классическим миром','detail':'Ахеменидская Персия, поздняя архаическая Греция, Восточная Чжоу и махаджанапады открывают следующий блок.','campaignId':'IRON_ERA_EXAM','sourcePatch':'v4.6'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)
packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)
im=load(Path('data/image_manifest.json'));existing={x['cardId']:x for x in im.get('images',[])}
for c in load(Path('data/cards/iron-world/story.json'))+load(Path('data/cards/iron-world/archive.json')):existing[c['id']]={'cardId':c['id'],'local':c['image']['local'],'file':c['image']['file'],'kind':'project-cover','prefer_remote':False,'caption':c['image']['caption'],'credit':c['image']['credit'],'source_url':c['image']['source_url'],'license':c['image']['license']}
images=list(existing.values());historical=sum(1 for x in images if x.get('prefer_remote'));im.update({'version':V,'generatedAt':'2026-07-14','count':len(images),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(images)-historical,'dynamicQueryCount':len(images)-historical,'images':images});dump(Path('data/image_manifest.json'),im)
(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('# Следующий этап после v4.6\n\n## v5.0 — Ахеменидская Персия\n\n- возникновение державы Кира II;\n- провинции, дороги, армии и царская идеология;\n- Вавилон, Египет, Левант и Малая Азия в системе империи;\n- источники и итоговый экзамен кампании.\n',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v4_6.md').write_text('# Patch v4.6.0 — Железный век: общий сравнительный слой\n\n- 8 глав, 48 миссий и 96 карточек.\n- Общая карта, параллельная хронология и экзамен из шести модулей.\n- Ассирия, Финикия, Левант, Греция, Чжоу и Северная Индия.\n',encoding='utf-8')
(ROOT/'docs/QA_v4_6.md').write_text('# QA v4.6.0\n\n- 96 карточек, 48 миссий, 14 квизов;\n- старт только с IRN_S_01_01–03;\n- общий пак выдаёт только IRN_A_*;\n- 6 регионов, 5 периодов и экзамен из 6 модулей;\n- версии, изображения и runtime-модули.\n',encoding='utf-8')
p=ROOT/'README.md';txt=p.read_text(encoding='utf-8');txt=re.sub(r'^# Codex of History v[^\n]+','# Codex of History v4.6.0',txt,count=1,flags=re.M);sec='\n## v4.6.0 — Железный век: общий сравнительный слой\n\n- 8 глав, 48 миссий и 96 карточек.\n- Общая карта, параллельная хронология и экзамен эпохи.\n- Patch-only архив.\n\n';txt=txt if '## v4.6.0' in txt else txt.replace('\n',sec,1);p.write_text(txt,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';txt=p.read_text(encoding='utf-8');sec='\n## v4.6 — Железный век: общий сравнительный слой\n\nЛокальные SVG-обложки 96 карточек и обложка общего пака созданы для Codex of History. Источники: Metropolitan Museum of Art, British Museum, UNESCO и Smarthistory.\n';p.write_text(txt if '## v4.6 —' in txt else txt+sec,encoding='utf-8')
for path in (ROOT/'js').rglob('*.js'):path.write_text(path.read_text(encoding='utf-8').replace('4.5.0',V),encoding='utf-8')
for path in (ROOT/'tools').glob('*.mjs'):path.write_text(path.read_text(encoding='utf-8').replace('4.5.0',V),encoding='utf-8')
pkg=load(Path('package.json'));pkg['version']=V
if 'smoke-v46-iron-world.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v46-iron-world.mjs && node tools/runtime-v46-iron-world.mjs'
pkg['scripts']['test:v46']='node tools/smoke-v46-iron-world.mjs && node tools/runtime-v46-iron-world.mjs';dump(Path('package.json'),pkg)
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;p.write_text(p.read_text(encoding='utf-8').replace('4.5.0',V).replace('codex-v4.5.0','codex-v4.6.0'),encoding='utf-8')
p=ROOT/'sw.js';txt=p.read_text(encoding='utf-8');txt=txt.replace("'./assets/packs/vedic-india-pack.svg',","'./assets/packs/vedic-india-pack.svg','./assets/packs/iron-era-pack.svg',").replace("'./js/features/v4-5-vedic-india.js',","'./js/features/v4-5-vedic-india.js','./js/features/v4-6-iron-world.js',");p.write_text(txt,encoding='utf-8')
print('integrated v4.6')
