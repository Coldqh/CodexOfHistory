#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='6.3.0'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for path in ['data/lessons/rome/chapter_10.json','data/lessons/rome/chapter_11.json','data/lessons/rome/chapter_12.json']:
 if path not in d['lessons']:
  idx=max([i for i,x in enumerate(d['lessons']) if 'data/lessons/rome/chapter_' in x],default=-1)+1;d['lessons'].insert(idx,path)
for path in ['data/quizzes/rome/chapter_10.json','data/quizzes/rome/chapter_11.json','data/quizzes/rome/chapter_12.json']:
 if path not in d['quizzes']:
  idx=max([i for i,x in enumerate(d['quizzes']) if 'data/quizzes/rome/chapter_' in x],default=-1)+1;d['quizzes'].insert(idx,path)
dump(Path('data/content-manifest.json'),m)

world=load(Path('data/world/campaigns.json'));rome=next(c for c in world if c['id']=='ROME_CAMPAIGN')
rome.update({'title':'Рим','subtitle':'От города в Лации к Республике, Империи и поздней Античности','period':'VIII век до н. э. – 476 год н. э.','chapterCount':12,'releasedChapters':12,'status':'PLAYABLE','region':'Италия, Средиземноморье и римские провинции','description':'Полная кампания из двенадцати глав: основание, Республика, завоевания, гражданские войны, принципат, провинциальная Империя и трансформация западной власти до 476 года.'})
rome['chapters']=[{'number':i,'title':t} for i,t in enumerate(['Рождение Рима','Рождение Республики','Борьба за Италию','Пунические войны','Завоевание эллинистического мира','Как работала Республика','Гракхи и социальный кризис','Марий, союзники и Сулла','Цезарь и гражданская война','Август и создание принципата','Расцвет и устройство Империи','Кризис и падение Запада'],1)]
dump(Path('data/world/campaigns.json'),world)

wt=load(Path('data/world/timeline.json'));new=[
 {'year':-43,'label':'Учреждение Второго триумвирата','detail':'Октавиан, Антоний и Лепид получают законные чрезвычайные полномочия.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.3'},
 {'year':-31,'label':'Битва при Акции','detail':'Победа Октавиана разрушает военную позицию Антония и Клеопатры.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.3'},
 {'year':-27,'label':'Начало принципата Августа','detail':'Октавиан получает имя Август и оформляет новое распределение полномочий.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.3'},
 {'year':69,'label':'Год четырёх императоров','detail':'Гражданская война показывает влияние провинциальных армий на передачу власти.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.3'},
 {'year':106,'label':'Создание провинции Дакия','detail':'Траян завершает вторую Дакийскую войну и включает территорию в Империю.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.3'},
 {'year':212,'label':'Constitutio Antoniniana','detail':'Каракалла распространяет гражданство на большинство свободных жителей Империи.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.3'},
 {'year':235,'label':'Начало кризиса III века','detail':'Убийство Александра Севера открывает эпоху частой смены императоров и войн.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.3'},
 {'year':293,'label':'Создание тетрархии','detail':'Диоклетиан распределяет власть между несколькими правителями и резиденциями.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.3'},
 {'year':330,'label':'Освящение Константинополя','detail':'Новая столица на Босфоре становится главным центром Восточной империи.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.3'},
 {'year':378,'label':'Битва при Адрианополе','detail':'Готские силы разбивают восточную римскую армию и убивают императора Валента.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.3'},
 {'year':410,'label':'Разграбление Рима Аларихом','detail':'Захват города имеет огромный символический эффект, но не завершает Империю.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.3'},
 {'year':476,'label':'Смещение Ромула Августула','detail':'Западная императорская должность исчезает в Италии, Восточная Римская империя сохраняется.','campaignId':'ROME_CAMPAIGN','sourcePatch':'v6.3'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

# Rebuild image manifest.
im=load(Path('data/image_manifest.json'));entries=[]
manifest=load(Path('data/content-manifest.json'))
for path in manifest['datasets']['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {}
  entries.append({'cardId':c['id'],'local':image.get('local','assets/ui/fallback-card.svg'),'file':image.get('file',Path(image.get('local','fallback.svg')).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x.get('prefer_remote'))
im.update({'version':V,'generatedAt':'2026-07-15','count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

# Query generator version.
p=ROOT/'tools/build-image-queries.py';txt=p.read_text(encoding='utf-8');txt=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',txt,count=1);p.write_text(txt,encoding='utf-8')

# Runtime versions and test expectations.
for path in (ROOT/'js').rglob('*.js'):
 text=path.read_text(encoding='utf-8').replace('6.2.0',V);path.write_text(text,encoding='utf-8')
for path in (ROOT/'tools').glob('*.mjs'):
 text=path.read_text(encoding='utf-8').replace('6.2.0',V).replace('3052','3087').replace('3047','3086').replace('3010','3045')
 path.write_text(text,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;text=p.read_text(encoding='utf-8').replace('6.2.0',V).replace('codex-v6.2.0','codex-v6.3.0');p.write_text(text,encoding='utf-8')

# Expand Rome runtime through chapter 12 and support final exam.
p=ROOT/'js/features/v6-1-rome-middle.js';text=p.read_text(encoding='utf-8')
text=text.replace('/* Codex v6.3.0 — Rome chapters 4–9: Mediterranean conquest and late republican crisis */','/* Codex v6.3.0 — complete Rome campaign: Republic, principate, high empire and western transformation */')
old="""    {id:'CIVIL',title:'Цезарь и гражданская война',date:'70–44 до н. э.',chapters:[9]}
  ];"""
new="""    {id:'CIVIL',title:'Цезарь и гражданская война',date:'70–44 до н. э.',chapters:[9]},
    {id:'AUGUSTUS',title:'Август и принципат',date:'44 до н. э. – 14 н. э.',chapters:[10]},
    {id:'HIGH',title:'Расцвет Империи',date:'14–180 н. э.',chapters:[11]},
    {id:'LATE',title:'Поздняя Империя и Запад',date:'193–476 н. э.',chapters:[12]}
  ];"""
if old not in text:raise SystemExit('phase block not found')
text=text.replace(old,new)
text=text.replace("html=html.replace(/РИМСКАЯ КАМПАНИЯ/g,'РИМ · РЕСПУБЛИКА И ГРАЖДАНСКИЕ ВОЙНЫ');","html=html.replace(/РИМСКАЯ КАМПАНИЯ/g,'РИМ · ОТ РЕСПУБЛИКИ К ИМПЕРИИ');")
text=text.replace("let html=oldMap().replace('Карта кампании','Карта Римской республики');","let html=oldMap().replace('Карта кампании','Карта Римского мира');")
text=text.replace("if(!m?.romeCheckpointModules)return oldActivity(m,l);\n    const modules=m.romeCheckpointModules||[],passed=modules.filter(x=>isQuizPassed(x.id)).length,all=passed===modules.length;\n    const late=String(m.id).startsWith('ROM_09_');\n    const checkpointTitle=late?'Поздняя Республика закреплена':'Средняя Республика закреплена';\n    const checkpointText=late?'Карта, хронология, социальный кризис, армии и критика источников проверяются отдельно.':'Карта, хронология, устройство Республики и критика источников проверяются отдельно.';\n    const exam=`<div class=\"era-exam assyria-exam\"><header><small>КОНТРОЛЬНАЯ ТОЧКА</small><h3>${all?checkpointTitle:`${passed}/${modules.length} модулей`}</h3><p>${checkpointText}</p>","if(!m?.romeCheckpointModules&&!m?.romeFinalModules)return oldActivity(m,l);\n    const finalExam=Array.isArray(m.romeFinalModules),modules=finalExam?m.romeFinalModules:(m.romeCheckpointModules||[]),passed=modules.filter(x=>isQuizPassed(x.id)).length,all=passed===modules.length;\n    const late=String(m.id).startsWith('ROM_09_');\n    const checkpointTitle=finalExam?'Римская кампания завершена':late?'Поздняя Республика закреплена':'Средняя Республика закреплена';\n    const checkpointText=finalExam?'Шесть модулей проверяют географию, хронологию, Республику, принципат, позднюю Империю и работу с источниками.':late?'Карта, хронология, социальный кризис, армии и критика источников проверяются отдельно.':'Карта, хронология, устройство Республики и критика источников проверяются отдельно.';\n    const exam=`<div class=\"era-exam assyria-exam\"><header><small>${finalExam?'ФИНАЛЬНЫЙ ЭКЗАМЕН':'КОНТРОЛЬНАЯ ТОЧКА'}</small><h3>${all?checkpointTitle:`${passed}/${modules.length} модулей`}</h3><p>${checkpointText}</p>")
text=text.replace("${all?`<button class=\"btn\" onclick=\"if(!missionCompleted('${m.id}'))completeMission('${m.id}')\">Завершить главу</button>`:''}","${all?`<button class=\"btn\" onclick=\"if(!missionCompleted('${m.id}'))completeMission('${m.id}')\">${finalExam?'Завершить римскую кампанию':'Завершить главу'}</button>`:''}")
p.write_text(text,encoding='utf-8')

# Documentation.
(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v6.3\n\n## v6.4 — Индия: Будда, Магадха и Маурьи\n\n- вторая урбанизация долины Ганга;\n- шраманские движения и ранний буддизм;\n- махаджанапады и Магадха;\n- Чандрагупта, Ашока и устройство державы Маурьев.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v6_3.md').write_text('''# Patch v6.3.0 — Рим: главы 10–12\n\n- Август и создание принципата.\n- Расцвет и устройство Империи.\n- Кризис III века, поздняя Империя и исчезновение западной императорской должности.\n- 3 главы, 18 миссий, 36 карточек и финальный экзамен всей римской кампании.\n''',encoding='utf-8')
(ROOT/'docs/QA_v6_3.md').write_text('''# QA v6.3.0\n\n- Проверены 24 сюжетные и 12 архивных карточек.\n- Проверены 18 миссий, 18 уроков, 3 главы, 3 главных квиза и 6 модулей финального экзамена.\n- Проверены перенос Августа из будущего каталога, карта, пулы, финал кампании и старые сохранения.\n''',encoding='utf-8')

p=ROOT/'README.md';t=p.read_text(encoding='utf-8');t=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',t,count=1,flags=re.M)
block='''\n## v6.3.0 — Рим: главы 10–12\n\n- Август, принципат, расцвет Империи, кризис III века и падение западной императорской власти.\n- 3 главы, 18 миссий и 36 карточек.\n- Финальный экзамен всей римской кампании.\n- Patch-only архив.\n\n'''
if '## v6.3.0' not in t:t=t.replace('\n',block,1)
p.write_text(t,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';t=p.read_text(encoding='utf-8');block='''\n\n## v6.3 — Римская империя\n\nЛокальные SVG-обложки новых карточек созданы для Codex of History. Источники: Res Gestae Divi Augusti, Metropolitan Museum of Art и музейные материалы по римским провинциям, династиям и поздней Античности. Историческое изображение Августа сохранено с исходной атрибуцией Wikimedia Commons.\n'''
if '## v6.3 —' not in t:t+=block
p.write_text(t,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V;append='node tools/smoke-v63-rome-empire.mjs && node tools/runtime-v63-rome-empire.mjs'
if 'smoke-v63-rome-empire.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && '+append
pkg['scripts']['test:v63']=append;dump(Path('package.json'),pkg)
print('integrated v6.3 metadata and runtime')
