#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];V='4.4.0'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for key,vals in [('cards',['data/cards/zhou-warring/story.json','data/cards/zhou-warring/archive.json']),('pools',['data/campaigns/zhou-warring/pools.json']),('quizzes',['data/quizzes/zhou-warring/campaign.json']),('stories',['data/stories/zhou-warring/personal.json']),('lessons',['data/lessons/zhou-warring/campaign.json']),('campaigns',['data/campaigns/zhou-warring/campaign.json'])]:
 for x in vals:
  if x not in d[key]:d[key].append(x)
d['maps']['ZHOU_WARRING']='data/maps/zhou-warring.json';script='js/features/v4-4-zhou-warring.js'
if script not in m['scripts']:m['scripts'].insert(m['scripts'].index('js/features/v3-1-1-hotfix.js'),script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));add=load(Path('data/core/relations-v44-zhou-warring.json'));known={x['id'] for x in rels};rels.extend(x for x in add if x['id'] not in known);dump(Path('data/core/relations.json'),rels);(ROOT/'data/core/relations-v44-zhou-warring.json').unlink(missing_ok=True)
world=load(Path('data/world/campaigns.json'));camp=load(Path('data/campaigns/zhou-warring/campaign.json'))
for c in world:
 if c['id']=='ZHOU_WARRING':c.update({'title':'Чжоу и Сражающиеся царства','subtitle':'Мандат Неба, царства и философы','period':'1046–221 до н. э.','chapterCount':10,'releasedChapters':10,'status':'PLAYABLE','region':'Северный и Центральный Китай','description':'От завоевания Шан и Мандата Неба до Конфуция, Сражающихся царств, реформ и объединения Цинь.','chapters':[{'number':x['number'],'title':x['title']} for x in camp['chapters']]})
dump(Path('data/world/campaigns.json'),world)

wt=load(Path('data/world/timeline.json'));new=[
{'year':-1046,'label':'Традиционная дата завоевания Шан Чжоу','detail':'Победа при Муе и начало Западной Чжоу.','campaignId':'ZHOU_WARRING','sourcePatch':'v4.4'},
{'year':-771,'label':'Кризис Западной Чжоу','detail':'Разрушение западного центра и перенос двора на восток.','campaignId':'ZHOU_WARRING','sourcePatch':'v4.4'},
{'year':-632,'label':'Сражение при Чэнпу','detail':'Победа Цзинь над Чу в эпоху гегемонов.','campaignId':'ZHOU_WARRING','sourcePatch':'v4.4'},
{'year':-551,'label':'Традиционная дата рождения Конфуция','detail':'Начало биографической традиции мыслителя государства Лу.','campaignId':'ZHOU_WARRING','sourcePatch':'v4.4'},
{'year':-453,'label':'Фактический раздел Цзинь','detail':'Рост Хань, Чжао и Вэй.','campaignId':'ZHOU_WARRING','sourcePatch':'v4.4'},
{'year':-356,'label':'Реформы Шан Яна в Цинь','detail':'Регистрация, ранги заслуг и территориальное управление усиливают Цинь.','campaignId':'ZHOU_WARRING','sourcePatch':'v4.4'},
{'year':-316,'label':'Цинь завоёвывает Шу','detail':'Сычуаньские ресурсы усиливают западное царство.','campaignId':'ZHOU_WARRING','sourcePatch':'v4.4'},
{'year':-260,'label':'Битва при Чанпине','detail':'Цинь наносит тяжёлое поражение Чжао.','campaignId':'ZHOU_WARRING','sourcePatch':'v4.4'},
{'year':-256,'label':'Конец царского дома Чжоу','detail':'Последние владения чжоуского царя ликвидированы.','campaignId':'ZHOU_WARRING','sourcePatch':'v4.4'},
{'year':-221,'label':'Объединение царств Цинь','detail':'Завершение эпохи Сражающихся царств.','campaignId':'ZHOU_WARRING','sourcePatch':'v4.4'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)
packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)
im=load(Path('data/image_manifest.json'));existing={x['cardId']:x for x in im.get('images',[])}
for c in load(Path('data/cards/zhou-warring/story.json'))+load(Path('data/cards/zhou-warring/archive.json')):existing[c['id']]={'cardId':c['id'],'local':c['image']['local'],'file':c['image']['file'],'kind':'project-cover','prefer_remote':False,'caption':c['image']['caption'],'credit':c['image']['credit'],'source_url':c['image']['source_url'],'license':c['image']['license']}
images=list(existing.values());historical=sum(1 for x in images if x.get('prefer_remote'));im.update({'version':V,'generatedAt':'2026-07-14','count':len(images),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(images)-historical,'dynamicQueryCount':len(images)-historical,'images':images});dump(Path('data/image_manifest.json'),im)
(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('# Следующий этап после v4.4\n\n## v4.5 — Ведийская Индия и ранние государства\n\n- ведийские тексты и проблема источников;\n- миграции и поселения Северной Индии;\n- варны, ритуал и политические общины;\n- поздневедийский период и ранние государства;\n- карта, архивные пулы, пак и личные истории.\n',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v4_4.md').write_text('# Patch v4.4.0 — Чжоу и Сражающиеся царства\n\n- 10 глав, 60 миссий и 120 карточек.\n- Западная и Восточная Чжоу, Мандат Неба, Конфуций, Сто школ, Сражающиеся царства и Цинь.\n- 10 пулов, 10 личных историй, карта и отдельный пак.\n',encoding='utf-8')
(ROOT/'docs/QA_v4_4.md').write_text('# QA v4.4.0\n\n- 120 карточек, 60 миссий, 14 квизов;\n- старт только с ZHO_S_01_01–03;\n- пак выдаёт только ZHO_A_*;\n- карта, четыре фазы и итоговый экзамен;\n- версии и runtime-модули.\n',encoding='utf-8')
p=ROOT/'README.md';txt=p.read_text(encoding='utf-8');txt=re.sub(r'^# Codex of History v[^\n]+','# Codex of History v4.4.0',txt,count=1,flags=re.M);sec='\n## v4.4.0 — Чжоу и Сражающиеся царства\n\n- 10 глав, 60 миссий и 120 карточек.\n- Мандат Неба, ритуальные бронзы, Конфуций, Сто школ, войны и реформы Цинь.\n- Patch-only архив.\n\n';txt=txt if '## v4.4.0' in txt else txt.replace('\n',sec,1);p.write_text(txt,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';txt=p.read_text(encoding='utf-8');sec='\n## v4.4 — Чжоу и Сражающиеся царства\n\nЛокальные SVG-обложки 120 карточек и обложка пака созданы для Codex of History. Источники: Metropolitan Museum of Art, Smithsonian National Museum of Asian Art, British Museum, Smarthistory и Stanford Encyclopedia of Philosophy.\n';p.write_text(txt if '## v4.4 —' in txt else txt+sec,encoding='utf-8')
for path in (ROOT/'js').rglob('*.js'):path.write_text(path.read_text(encoding='utf-8').replace('4.3.0',V),encoding='utf-8')
for path in (ROOT/'tools').glob('*.mjs'):path.write_text(path.read_text(encoding='utf-8').replace('4.3.0',V).replace('2075','2195').replace('2033','2153'),encoding='utf-8')
pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test']+=' && node tools/smoke-v44-zhou-warring.mjs && node tools/runtime-v44-zhou-warring.mjs' if 'smoke-v44-zhou-warring.mjs' not in pkg['scripts']['test'] else '';pkg['scripts']['test:v44']='node tools/smoke-v44-zhou-warring.mjs && node tools/runtime-v44-zhou-warring.mjs';dump(Path('package.json'),pkg)
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;p.write_text(p.read_text(encoding='utf-8').replace('4.3.0',V).replace('codex-v4.3.0','codex-v4.4.0'),encoding='utf-8')
p=ROOT/'sw.js';txt=p.read_text(encoding='utf-8');txt=txt.replace("'./assets/packs/archaic-greece-pack.svg',","'./assets/packs/archaic-greece-pack.svg','./assets/packs/zhou-warring-pack.svg',").replace("'./js/features/v4-3-archaic-greece.js',","'./js/features/v4-3-archaic-greece.js','./js/features/v4-4-zhou-warring.js',");p.write_text(txt,encoding='utf-8')
print('integrated v4.4')
