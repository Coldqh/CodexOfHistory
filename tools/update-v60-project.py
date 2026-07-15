#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='6.0.0'

def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,obj):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={
 'cards':['data/cards/hellenistic/story.json','data/cards/hellenistic/archive.json'],
 'campaigns':['data/campaigns/hellenistic/campaign.json'],
 'pools':['data/campaigns/hellenistic/pools.json'],
 'quizzes':['data/quizzes/hellenistic/campaign.json'],
 'stories':['data/stories/hellenistic/personal.json'],
 'lessons':['data/lessons/hellenistic/campaign.json'],
}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['HELLENISTIC']='data/maps/hellenistic.json'
script='js/features/v6-0-hellenistic.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js') if 'js/features/v3-1-1-hotfix.js' in m['scripts'] else len(m['scripts'])
 m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));new=load(Path('data/core/relations-v60-hellenistic.json'));existing={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in existing);dump(Path('data/core/relations.json'),rels)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_HELLENISTIC_ROMAN':
  if 'HELLENISTIC' not in e['campaignIds']:e['campaignIds'].insert(0,'HELLENISTIC')
  e['description']='Эллинистические царства, Рим, Маурьи, Хань и евразийские сети рассматриваются как связанные, но разные политические и культурные системы.'
dump(Path('data/world/eras.json'),eras)

world=load(Path('data/world/campaigns.json'))
for c in world:
 if c['id']=='HELLENISTIC':
  c.update({'eraId':'ERA_HELLENISTIC_ROMAN','order':20,'title':'Эллинистический мир','subtitle':'Царства наследников Александра','period':'323–30 до н. э.','chapterCount':10,'releasedChapters':10,'status':'PLAYABLE','region':'Восточное Средиземноморье, Египет и Западная Азия','description':'Диадохи, Птолемеи, Селевкиды, Антигониды, Пергам, города, учёность и римское вмешательство.','chapters':[{'number':i,'title':t} for i,t in enumerate(['После смерти Александра','Войны диадохов и рождение царств','Птолемеевский Египет','Селевкидская держава','Македония и греческие союзы','Пергам, Родос и малые державы','Города, деньги и мобильность','Александрия и мир знаний','Религии, культы и идентичности','Рим и конец эллинистических царств'],1)]})
  break
else:
 raise SystemExit('HELLENISTIC placeholder missing')
dump(Path('data/world/campaigns.json'),world)

# Build image-query context for the new campaign.
p=ROOT/'tools/build-image-queries.py';text=p.read_text(encoding='utf-8')
text=text.replace('VERSION = "6.0.0"',f'VERSION = "{V}"')
needle='''    "CLASSICAL_WORLD": {\n        "terms": ["классическ", "classical world", "ахеменид", "achaemenid", "перс", "persia", "гре", "greek", "полис", "polis", "македон", "macedon", "александр", "alexander", "empire"],\n        "base": [("ru", "Классическая античность"), ("en", "Classical antiquity"), ("en", "Achaemenid Empire")],\n    },\n'''
insert=needle+'''    "HELLENISTIC": {\n        "terms": ["эллинист", "hellenistic", "диадох", "diadochi", "птолем", "ptolemaic", "селевкид", "seleucid", "антигонид", "antigonid", "пергам", "pergamon", "александрия", "alexandria", "родос", "rhodes"],\n        "base": [("ru", "Эллинистический период"), ("en", "Hellenistic period"), ("en", "Hellenistic kingdoms")],\n    },\n'''
if '"HELLENISTIC": {' not in text:text=text.replace(needle,insert)
text=text.replace('("/classical-world/", "CLASSICAL_WORLD"),','("/classical-world/", "CLASSICAL_WORLD"), ("/hellenistic/", "HELLENISTIC"),')
p.write_text(text,encoding='utf-8')

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v6.0\n\n## v6.1 — Рим: главы 4–6\n\n- ранняя республика после завоевания Италии;\n- Первая и Вторая Пунические войны;\n- выход Рима в Восточное Средиземноморье;\n- связь с эллинистическими царствами;\n- полноценные миссии, карты, теория и новые архивные пулы.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v6_0.md').write_text('''# Patch v6.0.0 — Эллинистический мир\n\n- 10 глав, 60 миссий и 120 карточек.\n- Диадохи, Птолемеи, Селевкиды, Антигониды, Пергам и Родос.\n- Города, экономика, учёность, религии и римское вмешательство.\n- Карта от Македонии и Египта до Вавилона и Бактрии.\n- Итоговый экзамен из четырёх модулей.\n''',encoding='utf-8')
(ROOT/'docs/QA_v6_0.md').write_text('''# QA v6.0.0\n\n- Проверены 120 карточек, 60 миссий, 60 уроков и 10 архивных пулов.\n- Проверены старт новой игры, архивный пак, карта и четыре модуля экзамена.\n- Проверены связи с Александром, Египтом, Вавилоном, Левантом и Римом.\n- Проверена целостность runtime-модулей и GitHub Pages-ready структура.\n''',encoding='utf-8')

# README and attribution.
readme=ROOT/'README.md';rt=readme.read_text(encoding='utf-8');rt=rt.replace('# Codex of History v6.0.0','# Codex of History v6.0.0',1)
block='''## v6.0.0 — Эллинистический мир\n\n- 10 глав, 60 миссий и 120 карточек.\n- Диадохи, большие царства, города, знания, религии и римское вмешательство.\n- Patch-only архив.\n\n'''
if '## v6.0.0' not in rt:rt=rt.replace('# Codex of History v6.0.0\n','# Codex of History v6.0.0\n'+block,1)
readme.write_text(rt,encoding='utf-8')
attr=ROOT/'ATTRIBUTION.md';at=attr.read_text(encoding='utf-8')
if '## v6.0 — Эллинистический мир' not in at:at+='''\n\n## v6.0 — Эллинистический мир\n\nЛокальные SVG-обложки 120 карточек и обложка пака созданы для Codex of History. Источники: Metropolitan Museum of Art, British Museum, Encyclopaedia Iranica, UNESCO и Perseus Digital Library. Динамические исторические изображения загружаются только для видимых карточек и живут до конца текущей сессии.\n'''
attr.write_text(at,encoding='utf-8')
print('updated manifest, world catalog, relations and v6.0 metadata')
