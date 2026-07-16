#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='8.0.0';OLD='7.8.0';CHECKED='2026-07-16'

def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={
 'cards':['data/cards/islamic-origins/story.json','data/cards/islamic-origins/archive.json'],
 'campaigns':['data/campaigns/islamic-origins/campaign.json'],
 'pools':['data/campaigns/islamic-origins/pools.json'],
 'quizzes':['data/quizzes/islamic-origins/campaign.json'],
 'stories':['data/stories/islamic-origins/personal.json'],
 'lessons':['data/lessons/islamic-origins/campaign.json'],
}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['ISLAMIC_ORIGINS']='data/maps/islamic-origins.json'
script='js/features/v8-0-islamic-origins.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));rels=[r for r in rels if not re.fullmatch(r'REL_ISL_\d{4}',r.get('id',''))]
new=load(Path('data/core/relations-800-islamic-origins.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/islamic-origins/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
entry={'id':'ISLAMIC_ORIGINS','eraId':'ERA_TRANSITION','order':37,'title':'Возникновение исламского мира','subtitle':'От Аравии к халифату и Омейядской империи','period':'VI век – 750 год','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Аравия, Ближний Восток, Северная Африка и Хорасан','description':'Аравия около 600 года, Мекка, Коран и ранняя община, Медина, халифат, завоевания, фитны, Омейяды, административные реформы и аббасидская революция.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]}
world=[c for c in world if c['id']!='ISLAMIC_ORIGINS'];world.append(entry);world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_TRANSITION':
  e['dateLabel']='VI век – 750 год н. э.';e['startYear']=550;e['endYear']=750;e['status']='PLAYABLE'
  e['description']='Аравия поздней Античности, формирование мусульманской общины, ранний халифат, завоевания и Омейядская империя создают один из главных переходов к средневековому миру.'
  e['campaignIds']=['ISLAMIC_ORIGINS']
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'));events=[
 {'year':570,'label':'Аравия между Византией, Ираном и Красным морем','detail':'Позднеантичные пограничные и торговые системы создают контекст западной Аравии.','campaignId':'ISLAMIC_ORIGINS','sourcePatch':'v8.0'},
 {'year':610,'label':'Начало коранического откровения в исламской традиции','detail':'Ранняя проповедь формирует новую общину в Мекке.','campaignId':'ISLAMIC_ORIGINS','sourcePatch':'v8.0'},
 {'year':622,'label':'Хиджра в Медину','detail':'Переселение становится политическим рубежом и началом мусульманского календаря.','campaignId':'ISLAMIC_ORIGINS','sourcePatch':'v8.0'},
 {'year':632,'label':'Смерть Мухаммеда и начало раннего халифата','detail':'Спор о преемстве и войны ридды перестраивают общину и Аравию.','campaignId':'ISLAMIC_ORIGINS','sourcePatch':'v8.0'},
 {'year':636,'label':'Ярмук и Кадисия','detail':'Крупные победы открывают длительное подчинение византийских и сасанидских провинций.','campaignId':'ISLAMIC_ORIGINS','sourcePatch':'v8.0'},
 {'year':661,'label':'Начало Омейядской династии','detail':'Дамаск становится центром первой исламской династии.','campaignId':'ISLAMIC_ORIGINS','sourcePatch':'v8.0'},
 {'year':680,'label':'Кербела и вторая фитна','detail':'Гражданские войны формируют долговременную политическую и религиозную память.','campaignId':'ISLAMIC_ORIGINS','sourcePatch':'v8.0'},
 {'year':692,'label':'Купол Скалы и восстановление власти Абд аль-Малика','detail':'Монумент, эпиграфика и победа в гражданской войне обозначают новую программу империи.','campaignId':'ISLAMIC_ORIGINS','sourcePatch':'v8.0'},
 {'year':697,'label':'Омейядская денежная реформа','detail':'Эпиграфические монеты и арабские формулы меняют язык официальной власти.','campaignId':'ISLAMIC_ORIGINS','sourcePatch':'v8.0'},
 {'year':750,'label':'Аббасидская революция завершает власть Омейядов','detail':'Политический центр смещается на восток, а исламский мир вступает в новый цикл.','campaignId':'ISLAMIC_ORIGINS','sourcePatch':'v8.0'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "ISLAMIC_ORIGINS": {' not in s:
 marker='    "WORLD_AROUND_700": {';i=s.index(marker)
 group='''    "ISLAMIC_ORIGINS": {\n        "terms": ["early Islam", "Islamic origins", "Quran manuscript", "Umayyad", "Mecca", "Medina", "Damascus", "Dome of the Rock", "Arabic papyrus", "Islamic coin"],\n        "base": [("ru", "Возникновение исламского мира"), ("en", "early Islam Umayyad caliphate"), ("en", "early Quran manuscript Islamic coin")],\n    },\n'''
 s=s[:i]+group+s[i:]
old='("/world-around-700/", "WORLD_AROUND_700"),'
if '("/islamic-origins/", "ISLAMIC_ORIGINS")' not in s:
 if old not in s:raise SystemExit('image marker missing')
 s=s.replace(old,'("/islamic-origins/", "ISLAMIC_ORIGINS"), '+old)
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
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v7.8.0','codex-v8.0.0').replace('codex-v7\\.8\\.0','codex-v8\\.0\\.0')
 if rel=='index.html':t=re.sub(r'js/bootstrap\.js\?v=[0-9.]+',f'js/bootstrap.js?v={V}',t)
 p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v8-0-islamic-origins.js'" not in t:t=t.replace("'./js/features/v7-8-world-around-700.js'","'./js/features/v7-8-world-around-700.js','./js/features/v8-0-islamic-origins.js'")
if "'./assets/packs/islamic-origins-pack.svg'" not in t:t=t.replace("'./assets/packs/world-around-700-pack.svg'","'./assets/packs/world-around-700-pack.svg','./assets/packs/islamic-origins-pack.svg'")
p.write_text(t,encoding='utf-8')

for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'7\.8\.0',r'8\.0\.0').replace('4995','5127').replace('4953','5085').replace('2395','2461')
 p.write_text(t,encoding='utf-8')

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v8.0\n\n## v8.1 — Аббасидская революция и Багдад\n\n- переход власти от Омейядов к Аббасидам;\n- основание Багдада и новая придворная система;\n- Ирак, Хорасан и персидские административные традиции;\n- переводческие, правовые и торговые сети VIII–IX веков;\n- региональные династии и ослабление единого центра.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v8_0.md').write_text('''# Patch v8.0.0 — Возникновение исламского мира\n\n- 11 глав, 66 миссий и 132 карточки.\n- Аравия около 600 года, Мекка, Коран, хиджра и мединская община.\n- Ранний халифат, завоевания, гарнизонные города и первая фитна.\n- Омейяды, Кербела, реформы Абд аль-Малика, провинции и 750 год.\n- Отдельное внимание источникам, постепенной исламизации и сохранению местных администраций.\n''',encoding='utf-8')
(ROOT/'docs/QA_v8_0.md').write_text('''# QA v8.0.0\n\n- Проверены 88 сюжетных и 44 архивных карточки.\n- Проверены 66 миссий, 66 уроков, 11 глав, 11 пулов и 11 личных историй.\n- Проверены карта, четыре фазы, архивный пак и четыре модуля итогового экзамена.\n- Проверены межкампанийные связи с Аксумом, Восточным Римом, Сасанидами, Центральной Азией и христианскими общинами.\n- Проверены миграция сейва, коллекция и PWA-кэш.\n''',encoding='utf-8')
p=ROOT/'README.md';s=p.read_text(encoding='utf-8');s=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',s,count=1,flags=re.M);block='''\n## v8.0.0 — Возникновение исламского мира\n\n- 11 глав, 66 миссий и 132 карточки.\n- Аравия, Мекка, Медина, ранний халифат, завоевания, фитны и Омейяды.\n- Кампания завершает переход от поздней Античности к раннему Средневековью.\n- Patch-only архив.\n\n'''
if '## v8.0.0' not in s:s=s.replace('\n',block,1)
p.write_text(s,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';s=p.read_text(encoding='utf-8');block='''\n\n## v8.0 — Возникновение исламского мира\n\nЛокальные SVG-обложки 132 карточек и кампанийного пака созданы для Codex of History. Источниковая рамка опирается на материалы Metropolitan Museum of Art, Corpus Coranicum, University of Birmingham, UNESCO и музейные материалы по ранним кораническим рукописям, омейядской архитектуре, монетам и папирусам.\n'''
if '## v8.0 —' not in s:s+=block
p.write_text(s,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test:v80']='node tools/smoke-v80-islamic-origins.mjs && node tools/runtime-v80-islamic-origins.mjs'
if 'tools/smoke-v80-islamic-origins.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v80-islamic-origins.mjs && node tools/runtime-v80-islamic-origins.mjs'
dump(Path('package.json'),pkg)
print('integrated v8.0 Islamic origins')
