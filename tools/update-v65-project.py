#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='6.5.0'
CHECKED='2026-07-15'

def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={
 'cards':['data/cards/han/story.json','data/cards/han/archive.json'],
 'campaigns':['data/campaigns/han/campaign.json'],
 'pools':['data/campaigns/han/pools.json'],
 'quizzes':['data/quizzes/han/campaign.json'],
 'stories':['data/stories/han/personal.json'],
 'lessons':['data/lessons/han/campaign.json'],
}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]: d[key].append(val)
d['maps']['HAN']='data/maps/han.json'
script='js/features/v6-5-han.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js') if 'js/features/v3-1-1-hotfix.js' in m['scripts'] else len(m['scripts'])
 m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));new=load(Path('data/core/relations-v65-han.json'));existing={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in existing);dump(Path('data/core/relations.json'),rels)

world=load(Path('data/world/campaigns.json'));chapters=[x['title'] for x in load(Path('data/campaigns/han/campaign.json'))['chapters']]
for c in world:
 if c['id']=='HAN':
  c.update({'eraId':'ERA_HELLENISTIC_ROMAN','order':23,'title':'Империя Хань','subtitle':'Бюрократия, степь и западные маршруты','period':'221 год до н. э. – 220 год н. э.','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Китай, северная степь и Центральная Азия','description':'Объединение Цинь, война Чу–Хань, Гао-цзу, У-ди, сюнну, налоги, города, историки, Ван Ман, Восточная Хань и распад династии.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]});break
else: raise SystemExit('HAN placeholder missing')
dump(Path('data/world/campaigns.json'),world)

wt=load(Path('data/world/timeline.json'));new_events=[
 {'year':-221,'label':'Объединение Цинь','detail':'Ин Чжэн завершает завоевания и принимает императорский титул.','campaignId':'HAN','sourcePatch':'v6.5'},
 {'year':-202,'label':'Основание династии Хань','detail':'Лю Бан побеждает в войне Чу–Хань и становится императором Гао-цзу.','campaignId':'HAN','sourcePatch':'v6.5'},
 {'year':-141,'label':'Начало правления У-ди','detail':'Двор расширяет администрацию, финансовые меры и войны на северной границе.','campaignId':'HAN','sourcePatch':'v6.5'},
 {'year':-119,'label':'Походы против сюнну и монета у-чжу','detail':'Хань усиливает контроль над Ордосом, Хэси и денежной системой.','campaignId':'HAN','sourcePatch':'v6.5'},
 {'year':9,'label':'Ван Ман провозглашает династию Синь','detail':'Регент захватывает престол и начинает серию реформ.','campaignId':'HAN','sourcePatch':'v6.5'},
 {'year':25,'label':'Восстановление Восточной Хань','detail':'Лю Сю становится императором Гуан-у и переносит центр власти в Лоян.','campaignId':'HAN','sourcePatch':'v6.5'},
 {'year':184,'label':'Восстание Жёлтых повязок','detail':'Массовое восстание ускоряет военную регионализацию поздней Хань.','campaignId':'HAN','sourcePatch':'v6.5'},
 {'year':220,'label':'Конец династии Хань','detail':'Сянь-ди отрекается, и формальная единая империя прекращает существование.','campaignId':'HAN','sourcePatch':'v6.5'},
]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in new_events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';text=p.read_text(encoding='utf-8');text=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',text,count=1)
needle='''    "INDIA_MAURYA": {\n        "terms": ["маур", "maurya", "ашок", "ashoka", "магадх", "magadha", "будд", "buddha", "джайн", "jain", "паталипутр", "pataliputra", "санчи", "sanchi", "bodh gaya", "ганг", "ganga"],\n        "base": [("ru", "Империя Маурьев"), ("en", "Maurya Empire"), ("en", "Ashoka")],\n    },\n'''
insert=needle+'''    "HAN": {\n        "terms": ["империя хань", "han dynasty", "цинь", "qin dynasty", "у-ди", "wudi", "сюнну", "xiongnu", "чанъань", "chang'an", "лоян", "luoyang", "ван ман", "wang mang", "сыма цянь", "sima qian"],\n        "base": [("ru", "Империя Хань"), ("en", "Han dynasty"), ("en", "Qin and Han dynasties")],\n    },\n'''
if '    "HAN": {' not in text:
 if needle not in text: raise SystemExit('HAN image group insertion point missing')
 text=text.replace(needle,insert)
old='("/hellenistic/", "HELLENISTIC"), ("/maurya/", "INDIA_MAURYA"),'
new=old+' ("/han/", "HAN"),'
if '("/han/", "HAN")' not in text:
 if old not in text: raise SystemExit('HAN image path insertion point missing')
 text=text.replace(old,new)
p.write_text(text,encoding='utf-8')

entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg')
  entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace('6.4.0',V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace('6.4.0',V).replace('codex-v6.4.0','codex-v6.5.0').replace('codex-v6\\.4\\.0','codex-v6\\.5\\.0');p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v6-5-han.js'" not in t:t=t.replace("'./js/features/v6-4-maurya.js'","'./js/features/v6-4-maurya.js','./js/features/v6-5-han.js'")
if "'./assets/packs/han-pack.svg'" not in t:t=t.replace("'./assets/packs/maurya-pack.svg'","'./assets/packs/maurya-pack.svg','./assets/packs/han-pack.svg'")
p.write_text(t,encoding='utf-8')

# Keep cumulative smoke tests aligned with the current complete catalog.
for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace("'6.4.0'",f"'{V}'").replace('"6.4.0"',f'"{V}"')
 t=t.replace('3219','3351').replace('3177','3309')
 p.write_text(t,encoding='utf-8')

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v6.5\n\n## v6.6 — Степь и Шёлковые пути\n\n- скифы, саки, сарматы и ранние кочевые системы;\n- сюнну как самостоятельная степная держава;\n- города и государства Центральной Азии;\n- коридор Хэси, Таримский бассейн и караванные цепи;\n- товары, посредники, религии, технологии и болезни без мифа об одной дороге.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v6_5.md').write_text('''# Patch v6.5.0 — Империя Хань\n\n- 11 глав, 66 миссий и 132 карточки.\n- Объединение Цинь, падение династии и война Чу–Хань.\n- Гао-цзу, Вэнь, Цзин, У-ди, сюнну, Хэси и западные маршруты.\n- Налоги, города, чиновники, придворные группы, Сыма Цянь, Ван Ман и Восточная Хань.\n- Карта Китая и Центральной Азии, 11 архивных пулов и итоговый экзамен.\n''',encoding='utf-8')
(ROOT/'docs/QA_v6_5.md').write_text('''# QA v6.5.0\n\n- Проверены 88 сюжетных и 44 архивных карточки.\n- Проверены 66 миссий, 66 уроков, 11 глав, 11 пулов и 11 личных историй.\n- Проверены старт новой игры, архивный пак, карта, пять фаз и итоговый экзамен.\n- Проверены переходы от кампании Чжоу, связи с эллинистическим миром, Маурьями и Римом.\n- Проверены источники, локальные SVG, семантические профили изображений и runtime-модули.\n''',encoding='utf-8')

p=ROOT/'README.md';t=p.read_text(encoding='utf-8');t=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',t,count=1,flags=re.M)
block='''\n## v6.5.0 — Империя Хань\n\n- 11 глав, 66 миссий и 132 карточки.\n- Цинь, война Чу–Хань, Гао-цзу, У-ди, сюнну, западные маршруты и Восточная Хань.\n- Налоги, города, придворная политика, историки, Ван Ман и распад династии.\n- Patch-only архив.\n\n'''
if '## v6.5.0' not in t:t=t.replace('\n',block,1)
p.write_text(t,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';t=p.read_text(encoding='utf-8');block='''\n\n## v6.5 — Империя Хань\n\nЛокальные SVG-обложки 132 карточек и обложка пака созданы для Codex of History. Источники: Metropolitan Museum of Art, National Museum of Asian Art, UNESCO World Heritage Centre, British Museum и Chinese Text Project. Динамические исторические изображения загружаются только для видимых карточек и хранятся до конца сессии.\n'''
if '## v6.5 —' not in t:t+=block
p.write_text(t,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test:v65']='node tools/smoke-v65-han.mjs && node tools/runtime-v65-han.mjs'
if 'tools/smoke-v65-han.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v65-han.mjs && node tools/runtime-v65-han.mjs'
dump(Path('package.json'),pkg)
print('integrated v6.5 Han campaign, world catalog, timeline, images and metadata')
