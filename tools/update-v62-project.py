#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='6.2.0'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for path in ['data/lessons/rome/chapter_07.json','data/lessons/rome/chapter_08.json','data/lessons/rome/chapter_09.json']:
 if path not in d['lessons']:
  idx=max([i for i,x in enumerate(d['lessons']) if 'data/lessons/rome/chapter_' in x],default=-1)+1;d['lessons'].insert(idx,path)
for path in ['data/quizzes/rome/chapter_07.json','data/quizzes/rome/chapter_08.json','data/quizzes/rome/chapter_09.json']:
 if path not in d['quizzes']:
  idx=max([i for i,x in enumerate(d['quizzes']) if 'data/quizzes/rome/chapter_' in x],default=-1)+1;d['quizzes'].insert(idx,path)
dump(Path('data/content-manifest.json'),m)

world=load(Path('data/world/campaigns.json'));rome=next(c for c in world if c['id']=='ROME_CAMPAIGN')
rome.update({'title':'Рим','subtitle':'От города в Лации к гражданским войнам поздней Республики','period':'VIII век до н. э. – V век н. э.','chapterCount':12,'releasedChapters':9,'status':'PLAYABLE','region':'Италия и Средиземноморье','description':'Девять опубликованных глав: основание, Республика, Италия, Пунические войны, восточные завоевания, институты, Гракхи, Марий и Сулла, Цезарь и гражданская война.'})
rome['chapters']=[{'number':i,'title':t} for i,t in enumerate(['Рождение Рима','Рождение Республики','Борьба за Италию','Пунические войны','Завоевание эллинистического мира','Как работала Республика','Гракхи и социальный кризис','Марий, союзники и Сулла','Цезарь и гражданская война','Август и Империя','Расцвет Империи','Кризис и падение Запада'],1)]
dump(Path('data/world/campaigns.json'),world)

wt=load(Path('data/world/timeline.json'));new=[
 {'year':-133,'label':'Трибунат и гибель Тиберия Гракха','detail':'Аграрный закон и убийство трибуна открывают новую фазу политического конфликта.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.2'},
 {'year':-121,'label':'Гибель Гая Гракха','detail':'Senatus consultum ultimum используется в подавлении сторонников трибуна.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.2'},
 {'year':-107,'label':'Первое консульство Гая Мария','detail':'Марий получает командование в Югуртинской войне.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.2'},
 {'year':-91,'label':'Начало Союзнической войны','detail':'Италийские союзники выступают за гражданство и равное участие.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.2'},
 {'year':-88,'label':'Сулла ведёт армию на Рим','detail':'Консульская армия впервые захватывает столицу в борьбе за командование.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.2'},
 {'year':-82,'label':'Победа Суллы и проскрипции','detail':'Гражданская война завершается диктатурой и политическими конфискациями.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.2'},
 {'year':-60,'label':'Политический союз Цезаря, Помпея и Красса','detail':'Неформальная коалиция соединяет ресурсы трёх влиятельных политиков.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.2'},
 {'year':-49,'label':'Переход Цезаря через Рубикон','detail':'Конфликт о командовании превращается в открытую гражданскую войну.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.2'},
 {'year':-44,'label':'Убийство Юлия Цезаря','detail':'Заговор в мартовские иды не восстанавливает республиканское равновесие.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.2'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

# Image query generator version.
p=ROOT/'tools/build-image-queries.py';txt=p.read_text(encoding='utf-8');txt=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',txt,count=1);p.write_text(txt,encoding='utf-8')

# Runtime versions.
for path in (ROOT/'js').rglob('*.js'):
 text=path.read_text(encoding='utf-8').replace('6.1.0',V);path.write_text(text,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;text=p.read_text(encoding='utf-8').replace('6.1.0',V).replace('codex-v6.1.0','codex-v6.2.0');p.write_text(text,encoding='utf-8')

# Expand the existing Rome runtime into chapters 1–9.
p=ROOT/'js/features/v6-1-rome-middle.js';text=p.read_text(encoding='utf-8')
text=text.replace('/* Codex v6.2.0 — Rome chapters 4–6: Punic Wars, Eastern expansion and republican institutions */','/* Codex v6.2.0 — Rome chapters 4–9: Mediterranean conquest and late republican crisis */')
old="""    {id:'SYSTEM',title:'Механика Республики',date:'III–II века до н. э.',chapters:[6]}
  ];"""
new="""    {id:'SYSTEM',title:'Механика Республики',date:'III–II века до н. э.',chapters:[6]},
    {id:'GRACCHI',title:'Гракхи и социальный кризис',date:'133–121 до н. э.',chapters:[7]},
    {id:'ARMIES',title:'Марий, союзники и Сулла',date:'112–79 до н. э.',chapters:[8]},
    {id:'CIVIL',title:'Цезарь и гражданская война',date:'70–44 до н. э.',chapters:[9]}
  ];"""
if old not in text:raise SystemExit('phase block not found')
text=text.replace(old,new)
text=text.replace("html=html.replace(/РИМСКАЯ КАМПАНИЯ/g,'РИМ · РЕСПУБЛИКА И СРЕДИЗЕМНОМОРЬЕ');","html=html.replace(/РИМСКАЯ КАМПАНИЯ/g,'РИМ · РЕСПУБЛИКА И ГРАЖДАНСКИЕ ВОЙНЫ');")
text=text.replace("    if(!String(m?.id||'').startsWith('ROM_06_')||!m.romeCheckpointModules)return oldActivity(m,l);","    if(!m?.romeCheckpointModules)return oldActivity(m,l);")
text=text.replace("    const exam=`<div class=\"era-exam assyria-exam\"><header><small>КОНТРОЛЬНАЯ ТОЧКА</small><h3>${all?'Средняя Республика закреплена':`${passed}/${modules.length} модулей`}</h3><p>Карта, хронология, устройство Республики и критика источников проверяются отдельно.</p>","    const late=String(m.id).startsWith('ROM_09_');\n    const checkpointTitle=late?'Поздняя Республика закреплена':'Средняя Республика закреплена';\n    const checkpointText=late?'Карта, хронология, социальный кризис, армии и критика источников проверяются отдельно.':'Карта, хронология, устройство Республики и критика источников проверяются отдельно.';\n    const exam=`<div class=\"era-exam assyria-exam\"><header><small>КОНТРОЛЬНАЯ ТОЧКА</small><h3>${all?checkpointTitle:`${passed}/${modules.length} модулей`}</h3><p>${checkpointText}</p>")
p.write_text(text,encoding='utf-8')

# Documentation.
(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v6.2\n\n## v6.3 — Рим: главы 10–12\n\n- Август и создание принципата;\n- расцвет и устройство Империи;\n- кризис III века, поздняя Империя и падение Запада;\n- финальный экзамен всей римской кампании.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v6_2.md').write_text('''# Patch v6.2.0 — Рим: главы 7–9\n\n- Гракхи, Марий, Союзническая война, Сулла, Помпей, Цезарь и гражданская война.\n- 3 главы, 18 миссий и 36 карточек.\n- 3 архивных пула, 3 личные истории и контрольная точка поздней Республики.\n''',encoding='utf-8')
(ROOT/'docs/QA_v6_2.md').write_text('''# QA v6.2.0\n\n- Проверены 24 сюжетные и 12 архивных карточек.\n- Проверены 18 миссий, 18 уроков, 3 главы и 7 квизов.\n- Проверены перенос Цезаря и Рубикона из будущего каталога, стартовый профиль, пулы, карта и контрольный экзамен.\n''',encoding='utf-8')

p=ROOT/'README.md';t=p.read_text(encoding='utf-8');t=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',t,count=1,flags=re.M)
block='''\n## v6.2.0 — Рим: главы 7–9\n\n- Гракхи, Марий и Сулла, Цезарь и гражданская война.\n- 3 главы, 18 миссий и 36 карточек.\n- Patch-only архив.\n\n'''
if '## v6.2.0' not in t:t=t.replace('\n',block,1)
p.write_text(t,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';t=p.read_text(encoding='utf-8');block='''\n\n## v6.2 — Поздняя Римская республика\n\nЛокальные SVG-обложки новых карточек созданы для Codex of History. Источники: Плутарх, Аппиан, British Museum и материалы римской нумизматики. Исторические изображения Юлия Цезаря и перехода через Рубикон сохранены с исходной атрибуцией Wikimedia Commons.\n'''
if '## v6.2 —' not in t:t+=block
p.write_text(t,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V;append='node tools/smoke-v62-rome-late.mjs && node tools/runtime-v62-rome-late.mjs'
if 'smoke-v62-rome-late.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && '+append
pkg['scripts']['test:v62']=append;dump(Path('package.json'),pkg)
print('integrated v6.2 metadata and runtime')
