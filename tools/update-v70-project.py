#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='7.0.0';OLD='6.9.1';CHECKED='2026-07-16'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={'cards':['data/cards/migration-kingdoms/story.json','data/cards/migration-kingdoms/archive.json'],'campaigns':['data/campaigns/migration-kingdoms/campaign.json'],'pools':['data/campaigns/migration-kingdoms/pools.json'],'quizzes':['data/quizzes/migration-kingdoms/campaign.json'],'stories':['data/stories/migration-kingdoms/personal.json'],'lessons':['data/lessons/migration-kingdoms/campaign.json']}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['MIGRATION_KINGDOMS']='data/maps/migration-kingdoms.json'
script='js/features/v7-0-migration-kingdoms.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else m['scripts'].index('js/features/v3-1-1-hotfix.js');m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));new=load(Path('data/core/relations-v70-migration-kingdoms.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/migration-kingdoms/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
for c in world:
 if c.get('order',0)>=29:c['order']+=1
entry={'id':'MIGRATION_KINGDOMS','eraId':'ERA_LATE_ANTIQUITY','order':29,'title':'Переселения и новые королевства','subtitle':'От дунайского кризиса к постримскому Западу','period':'376–568 годы','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Европа, Северная Африка и западное Средиземноморье','description':'Готы, переход Дуная, Адрианополь, Аларих, Рейн, вандальская Африка, Аттила, 476 год, Британия, франки, вестготы, бургунды и остготская Италия.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]}
world=[c for c in world if c['id']!='MIGRATION_KINGDOMS'];world.append(entry);world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_LATE_ANTIQUITY':
  e['description']='Поздняя Римская империя перестраивается, религиозные общины создают новые институты, а войны, договоры и переселения превращают западные провинции в региональные королевства, сохранившие часть римского права, городов и налогового управления.'
  ids=[x for x in e['campaignIds'] if x!='MIGRATION_KINGDOMS'];pos=ids.index('EARLY_CHRISTIANITY')+1 if 'EARLY_CHRISTIANITY' in ids else 1;ids.insert(pos,'MIGRATION_KINGDOMS');e['campaignIds']=ids
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'));events=[
 {'year':376,'label':'Готские группы переходят Дунай','detail':'Римские власти разрешают переправу части беженцев, но провал снабжения превращает кризис в войну.','campaignId':'MIGRATION_KINGDOMS','sourcePatch':'v7.0'},
 {'year':378,'label':'Битва при Адрианополе','detail':'Армия Валента терпит тяжёлое поражение, а император погибает.','campaignId':'MIGRATION_KINGDOMS','sourcePatch':'v7.0'},
 {'year':406,'label':'Переход Рейна','detail':'Вандальские, аланские и свевские группы входят в Галлию на фоне гражданской войны.','campaignId':'MIGRATION_KINGDOMS','sourcePatch':'v7.0'},
 {'year':410,'label':'Разграбление Рима Аларихом','detail':'Трёхдневное разграбление наносит огромный символический удар, но западный двор остаётся в Равенне.','campaignId':'MIGRATION_KINGDOMS','sourcePatch':'v7.0'},
 {'year':429,'label':'Вандалы переправляются в Африку','detail':'Группа Гейзериха начинает завоевание североафриканских провинций.','campaignId':'MIGRATION_KINGDOMS','sourcePatch':'v7.0'},
 {'year':439,'label':'Захват Карфагена','detail':'Вандальское королевство получает крупнейший порт, налоговый центр и флот.','campaignId':'MIGRATION_KINGDOMS','sourcePatch':'v7.0'},
 {'year':451,'label':'Кампания Аттилы в Галлии','detail':'Гуннская и римско-готская коалиции сталкиваются после осады Орлеана.','campaignId':'MIGRATION_KINGDOMS','sourcePatch':'v7.0'},
 {'year':476,'label':'Одоакр смещает Ромула Августула','detail':'Отдельный западный двор прекращает существование, но администрация Италии продолжает работать.','campaignId':'MIGRATION_KINGDOMS','sourcePatch':'v7.0'},
 {'year':486,'label':'Хлодвиг побеждает Сиагрия','detail':'Франкская власть занимает последний самостоятельный римский центр Северной Галлии.','campaignId':'MIGRATION_KINGDOMS','sourcePatch':'v7.0'},
 {'year':493,'label':'Теодорих занимает Италию','detail':'После войны с Одоакром возникает остготское королевство со столицей в Равенне.','campaignId':'MIGRATION_KINGDOMS','sourcePatch':'v7.0'},
 {'year':507,'label':'Битва при Вуйе','detail':'Франки вытесняют вестготов из большей части Галлии.','campaignId':'MIGRATION_KINGDOMS','sourcePatch':'v7.0'},
 {'year':568,'label':'Лангобарды входят в Италию','detail':'Новый военный союз закрепляет политическую раздробленность полуострова.','campaignId':'MIGRATION_KINGDOMS','sourcePatch':'v7.0'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "MIGRATION_KINGDOMS": {' not in s:
 marker='    "LATE_RELIGIONS": {';i=s.index(marker);group='''    "MIGRATION_KINGDOMS": {\n        "terms": ["переселения народов", "migration period", "готы", "goths", "вандалы", "vandals", "гунны", "huns", "аттила", "attila", "одоакр", "odoacer", "теодорих", "theodoric", "англосаксы", "anglo-saxons"],\n        "base": [("ru", "Великое переселение народов"), ("en", "Migration Period"), ("en", "Fall of the Western Roman Empire")],\n    },\n''';s=s[:i]+group+s[i:]
old='("/late-religions/", "LATE_RELIGIONS"),'
if '("/migration-kingdoms/", "MIGRATION_KINGDOMS")' not in s:
 if old not in s:raise SystemExit('image path marker missing')
 s=s.replace(old,old+' ("/migration-kingdoms/", "MIGRATION_KINGDOMS"),')
p.write_text(s,encoding='utf-8')

entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg');entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v6.9.1','codex-v7.0.0').replace('codex-v6\\.9\\.1','codex-v7\\.0\\.0');p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v7-0-migration-kingdoms.js'" not in t:t=t.replace("'./js/features/v6-9-late-religions.js'","'./js/features/v6-9-late-religions.js','./js/features/v7-0-migration-kingdoms.js'")
if "'./assets/packs/migration-kingdoms-pack.svg'" not in t:t=t.replace("'./assets/packs/maurya-pack.svg'","'./assets/packs/maurya-pack.svg','./assets/packs/migration-kingdoms-pack.svg'")
p.write_text(t,encoding='utf-8')

for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'6\.9\.1',r'7\.0\.0').replace('3843','3975').replace('3801','3933')
 p.write_text(t,encoding='utf-8')

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v7.0\n\n## v7.1 — Восточная Римская империя\n\n- Константинополь и управление восточными провинциями после 395 года;\n- Феодосий II, стены столицы, двор и кодификация права;\n- Юстиниан, восстание «Ника», Святая София и Corpus Juris Civilis;\n- войны в Африке и Италии без схемы простого «восстановления Рима»;\n- Юстинианова чума, Ираклий и последняя война с Сасанидами.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v7_0.md').write_text('''# Patch v7.0.0 — Переселения и новые королевства\n\n- 11 глав, 66 миссий и 132 карточки.\n- Дунайский лимес, гуннское давление, переход 376 года и Адрианополь.\n- Аларих, переход Рейна, вандальская Африка, Аттила и кризис западного двора.\n- 476 год без мифа мгновенного исчезновения римского общества.\n- Британия, вестготы, бургунды, франки и остготская Италия.\n- Право, налоги, церковь, города и местные элиты как механизм перехода к Средневековью.\n''',encoding='utf-8')
(ROOT/'docs/QA_v7_0.md').write_text('''# QA v7.0.0\n\n- Проверены 88 сюжетных и 44 архивных карточки.\n- Проверены 66 миссий, 66 уроков, 11 глав, 11 пулов и 11 архивных дел.\n- Проверены пять фаз кампании, карта переселений и четыре модуля итогового экзамена.\n- Проверено разделение миграции, военной коалиции, этнонима и политического королевства.\n- Проверены связи с позднеримской, религиозной, степной и римской кампаниями.\n- Проверены локальные SVG, обложка пака, PWA-кэш и runtime-модуль.\n''',encoding='utf-8')
p=ROOT/'README.md';t=p.read_text(encoding='utf-8');t=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',t,count=1,flags=re.M);block='''\n## v7.0.0 — Переселения и новые королевства\n\n- 11 глав, 66 миссий и 132 карточки.\n- Дунай, Адрианополь, Аларих, Рейн, вандалы, гунны, 476 год и постримские королевства.\n- Переход к Средневековью показан через армию, землю, право, налоги, церковь и города.\n- Patch-only архив.\n\n'''
if '## v7.0.0' not in t:t=t.replace('\n',block,1)
p.write_text(t,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';t=p.read_text(encoding='utf-8');block='''\n\n## v7.0 — Переселения и новые королевства\n\nЛокальные SVG-обложки 132 карточек и обложка пака созданы для Codex of History. Источниковая рамка использует Ammianus Marcellinus, Encyclopaedia Britannica, Metropolitan Museum of Art, British Museum и UNESCO World Heritage Centre. Этнонимы, археологические культуры и политические союзы не приравниваются автоматически друг к другу.\n'''
if '## v7.0 —' not in t:t+=block
p.write_text(t,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test:v70']='node tools/smoke-v70-migration-kingdoms.mjs && node tools/runtime-v70-migration-kingdoms.mjs'
if 'tools/smoke-v70-migration-kingdoms.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v70-migration-kingdoms.mjs && node tools/runtime-v70-migration-kingdoms.mjs'
dump(Path('package.json'),pkg)
print('integrated v7.0 migration campaign')
