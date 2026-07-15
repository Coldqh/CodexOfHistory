#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];V='6.6.0';OLD='6.5.0';CHECKED='2026-07-15'
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={'cards':['data/cards/steppe-silk/story.json','data/cards/steppe-silk/archive.json'],'campaigns':['data/campaigns/steppe-silk/campaign.json'],'pools':['data/campaigns/steppe-silk/pools.json'],'quizzes':['data/quizzes/steppe-silk/campaign.json'],'stories':['data/stories/steppe-silk/personal.json'],'lessons':['data/lessons/steppe-silk/campaign.json']}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['STEPPE_SILK']='data/maps/steppe-silk.json';script='js/features/v6-6-steppe-silk.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js') if 'js/features/v3-1-1-hotfix.js' in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));new=load(Path('data/core/relations-660-steppe-silk.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)
world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/steppe-silk/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
for c in world:
 if c['id']=='STEPPE_SILK':
  c.update({'eraId':'ERA_HELLENISTIC_ROMAN','order':24,'title':'Степь и Шёлковые пути','subtitle':'Кочевые державы, оазисы и многозвенные сети','period':'ок. 700 года до н. э. – III век н. э.','chapterCount':11,'releasedChapters':11,'status':'PLAYABLE','region':'Евразийская степь и Центральная Азия','description':'Скифы, саки, Пазырык, сарматы, сюнну, ханьская граница, государства Центральной Азии, Хэси, Тарим и караванные цепи без мифа об одной дороге.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]});break
else:raise SystemExit('STEPPE_SILK placeholder missing')
dump(Path('data/world/campaigns.json'),world)
wt=load(Path('data/world/timeline.json'));events=[
 {'year':-700,'label':'Ранние скифские комплексы','detail':'В степях северного Причерноморья и Предкавказья складываются комплексы раннескифского времени.','campaignId':'STEPPE_SILK','sourcePatch':'v6.6'},
 {'year':-513,'label':'Поход Дария против скифов','detail':'Ахеменидская армия пересекает Дунай; рассказ Геродота остаётся внешним текстом, требующим проверки археологией.','campaignId':'STEPPE_SILK','sourcePatch':'v6.6'},
 {'year':-209,'label':'Модэ объединяет сюнну','detail':'Новая конфедерация превращается в самостоятельную державу северной границы Китая.','campaignId':'STEPPE_SILK','sourcePatch':'v6.6'},
 {'year':-138,'label':'Миссия Чжан Цяня','detail':'Ханьский посланник собирает сведения о государствах Центральной Азии и степных политических связях.','campaignId':'STEPPE_SILK','sourcePatch':'v6.6'},
 {'year':-121,'label':'Хань закрепляется в коридоре Хэси','detail':'Военные победы и новые округа меняют доступ к Дуньхуану и Таримскому бассейну.','campaignId':'STEPPE_SILK','sourcePatch':'v6.6'},
 {'year':-51,'label':'Хуханье признаёт ханьский сюзеренитет','detail':'Часть сюнну вступает в договорные отношения с двором Хань после внутреннего раскола.','campaignId':'STEPPE_SILK','sourcePatch':'v6.6'},
 {'year':73,'label':'Походы Бан Чао в Тариме','detail':'Ханьская дипломатия и военная сила вновь перестраивают систему оазисных союзов.','campaignId':'STEPPE_SILK','sourcePatch':'v6.6'},
 {'year':200,'label':'Плотные евразийские цепи обмена','detail':'Оазисы, степные маршруты и морские ветви связывают товары, тексты и технологии через множество посредников.','campaignId':'STEPPE_SILK','sourcePatch':'v6.6'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)
packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';text=p.read_text(encoding='utf-8');text=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',text,count=1)
if '    "STEPPE_SILK": {' not in text:
 marker='    "HAN": {';i=text.index(marker)
 group='''    "STEPPE_SILK": {\n        "terms": ["скиф", "scythian", "сак", "saka", "сармат", "sarmatian", "сюнну", "xiongnu", "пазырык", "pazyryk", "тарим", "tarim", "дуньхуан", "dunhuang", "бактри", "bactria", "шёлков", "silk road"],\n        "base": [("ru", "Степь и Шёлковые пути"), ("en", "Eurasian Steppe ancient"), ("en", "Silk Roads antiquity")],\n    },\n'''
 text=text[:i]+group+text[i:]
old='("/han/", "HAN"),'
if '("/steppe-silk/", "STEPPE_SILK")' not in text:
 if old not in text:raise SystemExit('image path marker missing')
 text=text.replace(old,old+' ("/steppe-silk/", "STEPPE_SILK"),')
p.write_text(text,encoding='utf-8')

entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg');entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v6.5.0','codex-v6.6.0').replace('codex-v6\\.5\\.0','codex-v6\\.6\\.0');p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v6-6-steppe-silk.js'" not in t:t=t.replace("'./js/features/v6-5-han.js'","'./js/features/v6-5-han.js','./js/features/v6-6-steppe-silk.js'")
if "'./assets/packs/steppe-silk-pack.svg'" not in t:t=t.replace("'./assets/packs/han-pack.svg'","'./assets/packs/han-pack.svg','./assets/packs/steppe-silk-pack.svg'")
p.write_text(t,encoding='utf-8')
for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace("'6.5.0'",f"'{V}'").replace('"6.5.0"',f'"{V}"').replace('3351','3483').replace(r'6\.5\.0',r'6\.6\.0').replace('6.5.0','6.6.0').replace('3309','3441');p.write_text(t,encoding='utf-8')

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v6.6\n\n## v6.7 — Античный мир: сравнительный экзамен\n\n- единая хронология эллинистических царств, Рима, Маурьев, Хань и степных держав;\n- сравнение власти, армий, границ, городов, налогов и статусов населения;\n- маршруты товаров, религий, технологий и текстов;\n- работа с несовместимыми источниками и картами;\n- общий экзамен, завершающий эпоху эллинистического и римского мира.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v6_6.md').write_text('''# Patch v6.6.0 — Степь и Шёлковые пути\n\n- 11 глав, 66 миссий и 132 карточки.\n- Скифы, саки, Пазырык, сарматы и сюнну.\n- Ханьско-сюннуская граница, государства Центральной Азии, Хэси и Тарим.\n- Караваны, товары, религии, технологии и болезни без мифа об одной дороге.\n- Новая карта, 11 архивных пулов и итоговый экзамен.\n''',encoding='utf-8')
(ROOT/'docs/QA_v6_6.md').write_text('''# QA v6.6.0\n\n- Проверены 88 сюжетных и 44 архивных карточки.\n- Проверены 66 миссий, 66 уроков, 11 глав, 11 пулов и 11 личных историй.\n- Проверены карта, пять фаз, архивный пак и четыре модуля итогового экзамена.\n- Проверены связи с Персией, Александром, Маурьями, Римом и Хань.\n- Проверены локальные SVG, источники, версии и runtime-модули.\n''',encoding='utf-8')
p=ROOT/'README.md';t=p.read_text(encoding='utf-8');t=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',t,count=1,flags=re.M);block='''\n## v6.6.0 — Степь и Шёлковые пути\n\n- 11 глав, 66 миссий и 132 карточки.\n- Скифы, саки, сарматы, сюнну, Центральная Азия, Хэси и Тарим.\n- Многозвенные караванные сети без схемы одной постоянной дороги.\n- Patch-only архив.\n\n''';
if '## v6.6.0' not in t:t=t.replace('\n',block,1)
p.write_text(t,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';t=p.read_text(encoding='utf-8');block='''\n\n## v6.6 — Степь и Шёлковые пути\n\nЛокальные SVG-обложки 132 карточек и пака созданы для Codex of History. Фактологическая база сверена по материалам Metropolitan Museum of Art, British Museum и UNESCO World Heritage Centre.\n''';
if '## v6.6 —' not in t:t+=block
p.write_text(t,encoding='utf-8')
pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test:v66']='node tools/smoke-v66-steppe-silk.mjs && node tools/runtime-v66-steppe-silk.mjs'
if 'tools/smoke-v66-steppe-silk.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v66-steppe-silk.mjs && node tools/runtime-v66-steppe-silk.mjs'
dump(Path('package.json'),pkg)
print('integrated v6.6 Steppe and Silk Networks')
