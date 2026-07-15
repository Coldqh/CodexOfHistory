#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];V='6.7.0';OLD='6.6.0';CHECKED='2026-07-15'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets'];adds={'cards':['data/cards/hellenistic-roman-world/story.json','data/cards/hellenistic-roman-world/archive.json'],'campaigns':['data/campaigns/hellenistic-roman-world/campaign.json'],'pools':['data/campaigns/hellenistic-roman-world/pools.json'],'quizzes':['data/quizzes/hellenistic-roman-world/campaign.json'],'stories':['data/stories/hellenistic-roman-world/personal.json'],'lessons':['data/lessons/hellenistic-roman-world/campaign.json']}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['HELLENISTIC_ROMAN_EXAM']='data/maps/hellenistic-roman-world.json';script='js/features/v6-7-hellenistic-roman-world.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js') if 'js/features/v3-1-1-hotfix.js' in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)
rels=load(Path('data/core/relations.json'));new=load(Path('data/core/relations-670-hellenistic-roman-world.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

world=load(Path('data/world/campaigns.json'))
if not any(c['id']=='HELLENISTIC_ROMAN_EXAM' for c in world):
 for c in world:
  if c.get('order',999)>=25:c['order']+=1
 campaign=load(Path('data/campaigns/hellenistic-roman-world/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
 world.append({'id':'HELLENISTIC_ROMAN_EXAM','eraId':'ERA_HELLENISTIC_ROMAN','order':25,'title':'Античный мир: сравнительный экзамен','subtitle':'Эллинистические царства, Рим, Маурьи, Хань и степные державы','period':'323 год до н. э. – 220 год н. э.','chapterCount':8,'releasedChapters':8,'status':'PLAYABLE','region':'Средиземноморье, Южная Азия, Китай и Евразийская степь','description':'Общий слой эпохи: параллельная хронология, формы власти, армии, города, налоги, статусы населения, религии и критика источников.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]})
world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)
eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_HELLENISTIC_ROMAN' and 'HELLENISTIC_ROMAN_EXAM' not in e['campaignIds']:e['campaignIds'].append('HELLENISTIC_ROMAN_EXAM')
dump(Path('data/world/eras.json'),eras)
wt=load(Path('data/world/timeline.json'));events=[
 {'year':-323,'label':'Начало общей шкалы античного мира','detail':'Смерть Александра открывает период, в котором эллинистические царства, Рим, Южная Азия, Китай и степь развиваются параллельно.','campaignId':'HELLENISTIC_ROMAN_EXAM','sourcePatch':'v6.7'},
 {'year':-268,'label':'Ашока и Первая Пуническая война','detail':'Правление Ашоки накладывается на борьбу Рима и Карфагена, но совпадение не означает прямой связи.','campaignId':'HELLENISTIC_ROMAN_EXAM','sourcePatch':'v6.7'},
 {'year':-221,'label':'Объединение Цинь на фоне средиземноморских войн','detail':'Одна шкала позволяет видеть независимые процессы без схемы единого центра.','campaignId':'HELLENISTIC_ROMAN_EXAM','sourcePatch':'v6.7'},
 {'year':-202,'label':'Зама и основание Хань','detail':'Два крупных перелома происходят в одном календарном году в разных политических системах.','campaignId':'HELLENISTIC_ROMAN_EXAM','sourcePatch':'v6.7'},
 {'year':-31,'label':'Акций и Западная Хань','detail':'Рим переходит к принципату, пока ханьская империя решает собственные дворцовые и пограничные задачи.','campaignId':'HELLENISTIC_ROMAN_EXAM','sourcePatch':'v6.7'},
 {'year':220,'label':'Конец Хань без общего конца античного мира','detail':'Распад династии происходит внутри продолжающейся римской императорской эпохи и меняющихся евразийских сетей.','campaignId':'HELLENISTIC_ROMAN_EXAM','sourcePatch':'v6.7'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)
packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';text=p.read_text(encoding='utf-8');text=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',text,count=1)
if '    "HELLENISTIC_ROMAN_EXAM": {' not in text:
 marker='    "STEPPE_SILK": {';i=text.index(marker);group='''    "HELLENISTIC_ROMAN_EXAM": {\n        "terms": ["античный мир", "ancient world", "эллинист", "hellenistic", "рим", "roman", "маур", "maurya", "хань", "han dynasty", "сюнну", "xiongnu", "сравн", "comparison"],\n        "base": [("ru", "Античный мир сравнительная история"), ("en", "connected ancient world"), ("en", "Hellenistic Roman Han Maurya")],\n    },\n''';text=text[:i]+group+text[i:]
old='("/steppe-silk/", "STEPPE_SILK"),'
if '("/hellenistic-roman-world/", "HELLENISTIC_ROMAN_EXAM")' not in text:
 if old not in text:raise SystemExit('image marker missing')
 text=text.replace(old,old+' ("/hellenistic-roman-world/", "HELLENISTIC_ROMAN_EXAM"),')
p.write_text(text,encoding='utf-8')

entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg');entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

for path in (ROOT/'js').rglob('*.js'):
 s=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(s,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;s=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v6.6.0','codex-v6.7.0').replace('codex-v6\\.6\\.0','codex-v6\\.7\\.0');p.write_text(s,encoding='utf-8')
p=ROOT/'sw.js';s=p.read_text(encoding='utf-8')
if "'./js/features/v6-7-hellenistic-roman-world.js'" not in s:s=s.replace("'./js/features/v6-6-steppe-silk.js'","'./js/features/v6-6-steppe-silk.js','./js/features/v6-7-hellenistic-roman-world.js'")
if "'./assets/packs/hellenistic-roman-era-pack.svg'" not in s:s=s.replace("'./assets/packs/steppe-silk-pack.svg'","'./assets/packs/steppe-silk-pack.svg','./assets/packs/hellenistic-roman-era-pack.svg'")
p.write_text(s,encoding='utf-8')
for p in (ROOT/'tools').glob('*.mjs'):
 s=p.read_text(encoding='utf-8').replace("'6.6.0'",f"'{V}'").replace('"6.6.0"',f'"{V}"').replace('6.6.0','6.7.0').replace(r'6\.6\.0',r'6\.7\.0').replace('3483','3579').replace('3441','3537');p.write_text(s,encoding='utf-8')

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v6.7\n\n## v6.8 — Поздняя античность\n\n- кризис III века без схемы мгновенного падения;\n- Диоклетиан, тетрархия и новая администрация;\n- Константин, христианизация и новые столицы;\n- позднеримская армия, налоги, города и сельские элиты;\n- связь с Сасанидами, постханьским Китаем и будущими кампаниями эпохи VI.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v6_7.md').write_text('''# Patch v6.7.0 — Античный мир: сравнительный экзамен\n\n- 8 глав, 48 миссий и 96 карточек.\n- Параллельная хронология эллинистического мира, Рима, Маурьев, Хань и степных держав.\n- Сравнение власти, армий, городов, налогов, статусов, религий и переводов.\n- Общая карта пяти регионов, 8 архивных пулов и шестимодульный экзамен эпохи.\n- Эпоха V завершена; следующий этап — поздняя античность.\n''',encoding='utf-8')
(ROOT/'docs/QA_v6_7.md').write_text('''# QA v6.7.0\n\n- Проверены 72 сюжетные и 24 архивные карточки.\n- Проверены 48 миссий, 48 уроков, 8 глав, 8 пулов и 8 личных историй.\n- Проверены пять региональных кнопок, параллельная хронология и общая карта.\n- Проверены шесть модулей экзамена и завершение пятой эпохи.\n- Проверены связи с Hellenistic, Rome, Maurya, Han и Steppe Silk.\n''',encoding='utf-8')
p=ROOT/'README.md';s=p.read_text(encoding='utf-8');s=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',s,count=1,flags=re.M);block='''\n## v6.7.0 — Античный мир: сравнительный экзамен\n\n- 8 глав, 48 миссий и 96 карточек.\n- Пять регионов на одной шкале времени и одной системе сравнения.\n- Шестимодульный итоговый экзамен завершает пятую эпоху.\n- Patch-only архив.\n\n''';
if '## v6.7.0' not in s:s=s.replace('\n',block,1)
p.write_text(s,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';s=p.read_text(encoding='utf-8');block='''\n\n## v6.7 — Сравнительный слой античного мира\n\nЛокальные SVG-обложки 96 карточек и общего пака созданы для Codex of History. Источниковая рамка опирается на музейные и институциональные материалы Metropolitan Museum of Art, British Museum, UNESCO и Chinese Text Project.\n''';
if '## v6.7 —' not in s:s+=block
p.write_text(s,encoding='utf-8')
pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test:v67']='node tools/smoke-v67-hellenistic-roman-world.mjs && node tools/runtime-v67-hellenistic-roman-world.mjs'
if 'tools/smoke-v67-hellenistic-roman-world.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v67-hellenistic-roman-world.mjs && node tools/runtime-v67-hellenistic-roman-world.mjs'
dump(Path('package.json'),pkg)
print('integrated v6.7 Hellenistic-Roman comparative layer')
