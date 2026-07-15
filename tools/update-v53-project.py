#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='6.0.0'
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,obj): (ROOT/p).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={
 'cards':['data/cards/classical-world/story.json','data/cards/classical-world/archive.json'],
 'campaigns':['data/campaigns/classical-world/campaign.json'],
 'pools':['data/campaigns/classical-world/pools.json'],
 'quizzes':['data/quizzes/classical-world/campaign.json'],
 'stories':['data/stories/classical-world/personal.json'],
 'lessons':['data/lessons/classical-world/campaign.json'],
}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]: d[key].append(val)
d['maps']['CLASSICAL_ERA_EXAM']='data/maps/classical-world-exam.json'
script='js/features/v5-3-classical-world.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js') if 'js/features/v3-1-1-hotfix.js' in m['scripts'] else len(m['scripts'])
 m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));new=load(Path('data/core/relations-v53-classical-world.json'))
existing={r['id'] for r in rels}
rels.extend(r for r in new if r['id'] not in existing)
dump(Path('data/core/relations.json'),rels)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_CLASSICAL':
  if 'CLASSICAL_ERA_EXAM' not in e['campaignIds']: e['campaignIds'].append('CLASSICAL_ERA_EXAM')
  e['description']='Ахеменидская империя, греческие полисы и Македония рассматриваются отдельно и в общей сравнительной кампании.'
dump(Path('data/world/eras.json'),eras)

world=load(Path('data/world/campaigns.json'))
if not any(c['id']=='CLASSICAL_ERA_EXAM' for c in world):
 world.append({'id':'CLASSICAL_ERA_EXAM','eraId':'ERA_CLASSICAL','order':20,'title':'Классический мир: общий сравнительный слой','subtitle':'Персия, полисы и Македония','period':'ок. 550–323 до н. э.','chapterCount':8,'releasedChapters':8,'status':'PLAYABLE','region':'Восточное Средиземноморье и Ахеменидская Азия','description':'Общая карта, параллельная хронология и экзамен четвёртой эпохи.','chapters':[{'number':i,'title':t} for i,t in enumerate(['Параллельная хронология классического мира','Империя, полис и царская монархия','Армии, флоты и логистика','Граждане, подданные и местные элиты','Налоги, монета и обмен','Религия и законность власти','История, философия и художественный язык','Как историки собирают классический мир'],1)]})
dump(Path('data/world/campaigns.json'),world)

# version fields in JSON data
for p in ROOT.joinpath('data').rglob('*.json'):
 try: obj=json.loads(p.read_text(encoding='utf-8'))
 except Exception: continue
 if isinstance(obj,dict) and 'version' in obj and isinstance(obj['version'],str):
  obj['version']=V;dump(p.relative_to(ROOT),obj)

# image query group and path mapping
p=ROOT/'tools/build-image-queries.py';text=p.read_text(encoding='utf-8')
text=text.replace('VERSION = "6.0.0"',f'VERSION = "{V}"')
needle='''    "ALEXANDER": {\n        "terms": ["александр", "alexander", "македон", "macedon", "дарий", "darius", "перс", "persian", "гавгамел", "gaugamela", "бактр", "bactria", "инд", "india"],\n        "base": [("ru", "Александр Македонский"), ("en", "Alexander the Great"), ("en", "Wars of Alexander the Great")],\n    },\n'''
insert=needle+'''    "CLASSICAL_WORLD": {\n        "terms": ["классическ", "classical world", "ахеменид", "achaemenid", "перс", "persia", "гре", "greek", "полис", "polis", "македон", "macedon", "александр", "alexander", "empire"],\n        "base": [("ru", "Классическая античность"), ("en", "Classical antiquity"), ("en", "Achaemenid Empire")],\n    },\n'''
if '"CLASSICAL_WORLD": {' not in text: text=text.replace(needle,insert)
text=text.replace('(\"/alexander/\", \"ALEXANDER\"),','(\"/alexander/\", \"ALEXANDER\"), (\"/classical-world/\", \"CLASSICAL_WORLD\"),')
p.write_text(text,encoding='utf-8')

# next plan
(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v5.3\n\n## v6.0 — Эллинистический мир\n\n- войны диадохов и раздел державы Александра;\n- Птолемеи, Селевкиды, Антигониды и региональные царства;\n- города, армии, экономика и культурные связи III–I веков до н. э.;\n- переход к эпохе эллинистического и римского мира.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v5_3.md').write_text('''# Patch v6.0.0 — Классический мир: общий сравнительный слой\n\n- 8 глав, 48 миссий и 96 карточек.\n- Общая карта Персии, греческих полисов и Македонии.\n- Параллельная хронология 550–323 годов до н. э.\n- Экзамен эпохи из шести модулей.\n- Общий архивный пак четвёртой эпохи.\n''',encoding='utf-8')
(ROOT/'docs/QA_v5_3.md').write_text('''# QA v6.0.0\n\n- Проверены 96 карточек, 48 миссий, 48 уроков и 8 архивных пулов.\n- Проверены старт новой игры, общий пак, карта, хронология и шесть модулей экзамена.\n- Проверены ссылки между Персией, классической Грецией, Александром и общим слоем.\n- Проверена целостность runtime-модулей и GitHub Pages-ready структура.\n''',encoding='utf-8')

readme=ROOT/'README.md';rt=readme.read_text(encoding='utf-8')
rt=rt.replace('# Codex of History v6.0.0','# Codex of History v6.0.0',1)
block='''## v6.0.0 — Классический мир: общий сравнительный слой\n\n- 8 глав, 48 миссий и 96 карточек.\n- Персия, греческие полисы и Македония на общей карте и временной шкале.\n- Экзамен эпохи из шести модулей.\n- Patch-only архив.\n\n'''
if '## v6.0.0' not in rt: rt=rt.replace('# Codex of History v6.0.0\n','# Codex of History v6.0.0\n'+block,1)
readme.write_text(rt,encoding='utf-8')
attr=ROOT/'ATTRIBUTION.md';at=attr.read_text(encoding='utf-8')
if '## v5.3 — Классический мир' not in at:
 at+='''\n\n## v5.3 — Классический мир: общий сравнительный слой\n\nЛокальные SVG-обложки 96 карточек и обложка общего пака созданы для Codex of History. Источники: Metropolitan Museum of Art, UNESCO и Perseus Digital Library. Динамические исторические изображения загружаются только для видимых карточек и живут до конца текущей сессии.\n'''
attr.write_text(at,encoding='utf-8')
print('updated manifest, world catalog, relations and project metadata')
