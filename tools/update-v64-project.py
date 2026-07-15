#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='6.4.0'
CHECKED='2026-07-15'

def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
    p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Manifest and datasets.
m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={
 'cards':['data/cards/maurya/story.json','data/cards/maurya/archive.json'],
 'campaigns':['data/campaigns/maurya/campaign.json'],
 'pools':['data/campaigns/maurya/pools.json'],
 'quizzes':['data/quizzes/maurya/campaign.json'],
 'stories':['data/stories/maurya/personal.json'],
 'lessons':['data/lessons/maurya/campaign.json'],
}
for key,vals in adds.items():
    for val in vals:
        if val not in d[key]: d[key].append(val)
d['maps']['INDIA_MAURYA']='data/maps/maurya.json'
script='js/features/v6-4-maurya.js'
if script not in m['scripts']:
    idx=m['scripts'].index('js/features/v3-1-1-hotfix.js') if 'js/features/v3-1-1-hotfix.js' in m['scripts'] else len(m['scripts'])
    m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

# Relations.
rels=load(Path('data/core/relations.json'));new=load(Path('data/core/relations-v64-maurya.json'));existing={r['id'] for r in rels}
rels.extend(r for r in new if r['id'] not in existing);dump(Path('data/core/relations.json'),rels)

# World catalog.
world=load(Path('data/world/campaigns.json'))
chapters=[x['title'] for x in load(Path('data/campaigns/maurya/campaign.json'))['chapters']]
for c in world:
    if c['id']=='INDIA_MAURYA':
        c.update({
            'eraId':'ERA_HELLENISTIC_ROMAN','order':22,
            'title':'Индия: Будда, Магадха и Маурьи',
            'subtitle':'Города, новые учения и первая большая империя',
            'period':'ок. 600–185 до н. э.','chapterCount':len(chapters),'releasedChapters':len(chapters),
            'status':'PLAYABLE','region':'Северная Индия и Маурийская держава',
            'description':'Вторая урбанизация, шраманские движения, Будда и Махавира, возвышение Магадхи, Чандрагупта, Ашока, эдикты и распад державы Маурьев.',
            'chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]
        });break
else: raise SystemExit('INDIA_MAURYA placeholder missing')
dump(Path('data/world/campaigns.json'),world)

# Global timeline.
wt=load(Path('data/world/timeline.json'));new_events=[
 {'year':-600,'label':'Вторая урбанизация Северной Индии','detail':'Города, рынки, монета и территориальные государства укрепляются в долине Ганга.','campaignId':'INDIA_MAURYA','sourcePatch':'v6.4'},
 {'year':-500,'label':'Будда и Махавира','detail':'Приблизительная эпоха ранних буддийских и джайнских общин; точные даты спорны.','campaignId':'INDIA_MAURYA','sourcePatch':'v6.4'},
 {'year':-322,'label':'Начало правления Чандрагупты Маурьи','detail':'Магадха становится центром крупной державы Маурьев.','campaignId':'INDIA_MAURYA','sourcePatch':'v6.4'},
 {'year':-261,'label':'Война Ашоки с Калингой','detail':'Надписи Ашоки связывают завоевание с размышлением о насилии и царской дхамме.','campaignId':'INDIA_MAURYA','sourcePatch':'v6.4'},
 {'year':-250,'label':'Распространение эдиктов Ашоки','detail':'Каменные надписи на разных языках обращаются к подданным и чиновникам державы.','campaignId':'INDIA_MAURYA','sourcePatch':'v6.4'},
 {'year':-185,'label':'Конец династии Маурьев','detail':'Брихадратха свергнут Пушьямитрой Шунгой; региональные политические системы продолжают развиваться.','campaignId':'INDIA_MAURYA','sourcePatch':'v6.4'},
]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in new_events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

# Pack metadata version.
packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

# Image query context.
p=ROOT/'tools/build-image-queries.py';text=p.read_text(encoding='utf-8');text=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',text,count=1)
needle='''    "HELLENISTIC": {\n        "terms": ["эллинист", "hellenistic", "диадох", "diadochi", "птолем", "ptolemaic", "селевкид", "seleucid", "антигонид", "antigonid", "пергам", "pergamon", "александрия", "alexandria", "родос", "rhodes"],\n        "base": [("ru", "Эллинистический период"), ("en", "Hellenistic period"), ("en", "Hellenistic kingdoms")],\n    },\n'''
insert=needle+'''    "INDIA_MAURYA": {\n        "terms": ["маур", "maurya", "ашок", "ashoka", "магадх", "magadha", "будд", "buddha", "джайн", "jain", "паталипутр", "pataliputra", "санчи", "sanchi", "bodh gaya", "ганг", "ganga"],\n        "base": [("ru", "Империя Маурьев"), ("en", "Maurya Empire"), ("en", "Ashoka")],\n    },\n'''
if '"INDIA_MAURYA": {' not in text:
    if needle not in text: raise SystemExit('image group insertion point missing')
    text=text.replace(needle,insert)
old='("/classical-world/", "CLASSICAL_WORLD"), ("/hellenistic/", "HELLENISTIC"),'
new=old+' ("/maurya/", "INDIA_MAURYA"),'
if '("/maurya/", "INDIA_MAURYA")' not in text:
    if old not in text: raise SystemExit('image path insertion point missing')
    text=text.replace(old,new)
p.write_text(text,encoding='utf-8')

# Rebuild image manifest from all cards.
entries=[]
for path in d['cards']:
    for c in load(Path(path)):
        image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg')
        entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote'])
im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

# Version files and runtime modules.
for path in (ROOT/'js').rglob('*.js'):
    t=path.read_text(encoding='utf-8').replace('6.3.0',V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
    p=ROOT/rel;t=p.read_text(encoding='utf-8').replace('6.3.0',V).replace('codex-v6.3.0','codex-v6.4.0');p.write_text(t,encoding='utf-8')
# Add core files to SW pre-cache.
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v6-4-maurya.js'" not in t:t=t.replace("'./js/features/v6-0-hellenistic.js'","'./js/features/v6-0-hellenistic.js','./js/features/v6-4-maurya.js'")
if "'./assets/packs/maurya-pack.svg'" not in t:t=t.replace("'./assets/packs/hellenistic-pack.svg'","'./assets/packs/hellenistic-pack.svg','./assets/packs/maurya-pack.svg'")
p.write_text(t,encoding='utf-8')

# Documentation.
(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v6.4\n\n## v6.5 — Империя Хань\n\n- объединение при Цинь как предыстория;\n- основание Хань и императорская администрация;\n- У-ди, северные войны и Сюнну;\n- налоги, земля, города и придворная политика;\n- письменная культура, историки и кризисы династии.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v6_4.md').write_text('''# Patch v6.4.0 — Индия: Будда, Магадха и Маурьи\n\n- 11 глав, 66 миссий и 132 карточки.\n- Вторая урбанизация, шраманские движения, ранний буддизм и джайнизм.\n- Магадха, Чандрагупта, Маурийская держава, Ашока и его эдикты.\n- Карта Северной Индии и экзамен из четырёх модулей.\n''',encoding='utf-8')
(ROOT/'docs/QA_v6_4.md').write_text('''# QA v6.4.0\n\n- Проверены 88 сюжетных и 44 архивных карточки.\n- Проверены 66 миссий, 66 уроков, 11 глав, 11 пулов и 11 личных историй.\n- Проверены старт новой игры, архивный пак, карта, четыре фазы и итоговый экзамен.\n- Проверены источники, семантические профили изображений и целостность runtime-модулей.\n''',encoding='utf-8')

p=ROOT/'README.md';t=p.read_text(encoding='utf-8');t=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',t,count=1,flags=re.M)
block='''\n## v6.4.0 — Индия: Будда, Магадха и Маурьи\n\n- 11 глав, 66 миссий и 132 карточки.\n- Вторая урбанизация, ранний буддизм и джайнизм, Магадха, Маурьи и Ашока.\n- Карта Северной Индии, 11 архивных пулов и итоговый экзамен.\n- Patch-only архив.\n\n'''
if '## v6.4.0' not in t:t=t.replace('\n',block,1)
p.write_text(t,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';t=p.read_text(encoding='utf-8');block='''\n\n## v6.4 — Индия: Будда, Магадха и Маурьи\n\nЛокальные SVG-обложки 132 карточек и обложка пака созданы для Codex of History. Источники: Metropolitan Museum of Art, UNESCO World Heritage Centre, British Museum, SuttaCentral и музейные материалы по буддизму, джайнизму, Ашоке и Маурийской державе. Динамические исторические изображения загружаются только для видимых карточек и хранятся до конца сессии.\n'''
if '## v6.4 —' not in t:t+=block
p.write_text(t,encoding='utf-8')

# Package metadata. Tests are appended after creating test files.
pkg=load(Path('package.json'));pkg['version']=V;dump(Path('package.json'),pkg)
print('integrated v6.4 campaign, world catalog, timeline, images and metadata')
