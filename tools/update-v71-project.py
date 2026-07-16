#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='7.1.0';OLD='7.0.0';CHECKED='2026-07-16'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={'cards':['data/cards/eastern-roman/story.json','data/cards/eastern-roman/archive.json'],'campaigns':['data/campaigns/eastern-roman/campaign.json'],'pools':['data/campaigns/eastern-roman/pools.json'],'quizzes':['data/quizzes/eastern-roman/campaign.json'],'stories':['data/stories/eastern-roman/personal.json'],'lessons':['data/lessons/eastern-roman/campaign.json']}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['EASTERN_ROMAN']='data/maps/eastern-roman.json'
script='js/features/v7-1-eastern-roman.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));new=load(Path('data/core/relations-v71-eastern-roman.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/eastern-roman/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
entry={'id':'EASTERN_ROMAN','eraId':'ERA_LATE_ANTIQUITY','order':29,'title':'Восточная Римская империя','subtitle':'Константинополь, право и войны 395–641 годов','period':'395–641 годы','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Восточное Средиземноморье, Балканы и Ближний Восток','description':'От отдельного восточного двора и Феодосиевых стен до Юстиниана, кодификации права, войн в Африке и Италии, чумы и последней войны Ираклия с Сасанидами.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]}
world=[c for c in world if c['id']!='EASTERN_ROMAN']
order_map={'LATE_ANTIQUITY':26,'EARLY_CHRISTIANITY':27,'MIGRATION_KINGDOMS':28,'EASTERN_ROMAN':29,'SASANIAN':30,'GUPTA':31,'CHINA_POST_HAN':32,'ISLAMIC_ORIGINS':33}
world.append(entry)
for c in world:
 if c['id'] in order_map:c['order']=order_map[c['id']]
world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_LATE_ANTIQUITY':
  e['description']='Поздняя Римская империя перестраивает право и налоги, религиозные общины создают новые институты, западные провинции превращаются в королевства, а Константинополь сохраняет римскую государственность через войны, кодификации и финансовую мобилизацию.'
  e['campaignIds']=['LATE_ANTIQUITY','EARLY_CHRISTIANITY','MIGRATION_KINGDOMS','EASTERN_ROMAN','SASANIAN','GUPTA','CHINA_POST_HAN']
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'));events=[
 {'year':395,'label':'Отдельный восточный двор после Феодосия I','detail':'Аркадий правит из Константинополя, сохраняя римскую титулатуру и восточную налоговую систему.','campaignId':'EASTERN_ROMAN','sourcePatch':'v7.1'},
 {'year':413,'label':'Строительство Феодосиевых стен','detail':'Новая сухопутная линия закрывает западный подход к Константинополю.','campaignId':'EASTERN_ROMAN','sourcePatch':'v7.1'},
 {'year':438,'label':'Публикация Феодосиева кодекса','detail':'Сборник императорских конституций создаёт общую правовую основу Востока и Запада.','campaignId':'EASTERN_ROMAN','sourcePatch':'v7.1'},
 {'year':447,'label':'Восстановление стен после землетрясения','detail':'Столица срочно ремонтирует укрепления на фоне угрозы Аттилы.','campaignId':'EASTERN_ROMAN','sourcePatch':'v7.1'},
 {'year':498,'label':'Монетная реформа Анастасия','detail':'Крупные медные номиналы меняют повседневное денежное обращение.','campaignId':'EASTERN_ROMAN','sourcePatch':'v7.1'},
 {'year':527,'label':'Юстиниан становится императором','detail':'Начинается масштабная правовая, строительная и военная программа.','campaignId':'EASTERN_ROMAN','sourcePatch':'v7.1'},
 {'year':532,'label':'Восстание «Ника»','detail':'Столичный мятеж подавлен в Ипподроме и меняет политический облик города.','campaignId':'EASTERN_ROMAN','sourcePatch':'v7.1'},
 {'year':537,'label':'Освящение Святой Софии','detail':'Новый купольный храм становится центром императорской церемонии.','campaignId':'EASTERN_ROMAN','sourcePatch':'v7.1'},
 {'year':533,'label':'Дигесты и Институции Юстиниана','detail':'Классическая юриспруденция переработана и получает силу закона.','campaignId':'EASTERN_ROMAN','sourcePatch':'v7.1'},
 {'year':534,'label':'Завершение войны с вандалами','detail':'Карфаген и африканские провинции переходят под прямое восточноримское управление.','campaignId':'EASTERN_ROMAN','sourcePatch':'v7.1'},
 {'year':541,'label':'Начало Юстиниановой чумы','detail':'Эпидемия распространяется по восточному Средиземноморью и достигает столицы.','campaignId':'EASTERN_ROMAN','sourcePatch':'v7.1'},
 {'year':554,'label':'Прагматическая санкция для Италии','detail':'Империя пытается восстановить управление после долгой Готской войны.','campaignId':'EASTERN_ROMAN','sourcePatch':'v7.1'},
 {'year':602,'label':'Свержение Маврикия','detail':'Мятеж дунайской армии приводит к власти Фоку и открывает новую войну с Сасанидами.','campaignId':'EASTERN_ROMAN','sourcePatch':'v7.1'},
 {'year':614,'label':'Сасаниды занимают Иерусалим','detail':'Великая война лишает имперскую власть важнейшего религиозного центра.','campaignId':'EASTERN_ROMAN','sourcePatch':'v7.1'},
 {'year':627,'label':'Битва при Ниневии','detail':'Контрнаступление Ираклия ускоряет крах режима Хосрова II.','campaignId':'EASTERN_ROMAN','sourcePatch':'v7.1'},
 {'year':636,'label':'Битва при Ярмуке','detail':'Истощённая империя теряет контроль над Сирией после поражения от арабской армии.','campaignId':'EASTERN_ROMAN','sourcePatch':'v7.1'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "EASTERN_ROMAN": {' not in s:
 marker='    "MIGRATION_KINGDOMS": {';i=s.index(marker);group='''    "EASTERN_ROMAN": {\n        "terms": ["Восточная Римская империя", "Byzantine Empire", "Константинополь", "Constantinople", "Феодосий II", "Theodosius II", "Юстиниан", "Justinian", "Святая София", "Hagia Sophia", "Велисарий", "Belisarius", "Ираклий", "Heraclius"],\n        "base": [("ru", "Восточная Римская империя"), ("en", "Eastern Roman Empire"), ("en", "Byzantine Empire Late Antiquity")],\n    },\n''';s=s[:i]+group+s[i:]
old='("/migration-kingdoms/", "MIGRATION_KINGDOMS"),'
if '("/eastern-roman/", "EASTERN_ROMAN")' not in s:
 if old not in s:raise SystemExit('image path marker missing')
 s=s.replace(old,old+' ("/eastern-roman/", "EASTERN_ROMAN"),')
p.write_text(s,encoding='utf-8')

entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg');entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v7.0.0','codex-v7.1.0').replace('codex-v7\\.0\\.0','codex-v7\\.1\\.0');p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v7-1-eastern-roman.js'" not in t:t=t.replace("'./js/features/v7-0-migration-kingdoms.js'","'./js/features/v7-0-migration-kingdoms.js','./js/features/v7-1-eastern-roman.js'")
if "'./assets/packs/eastern-roman-pack.svg'" not in t:t=t.replace("'./assets/packs/migration-kingdoms-pack.svg'","'./assets/packs/migration-kingdoms-pack.svg','./assets/packs/eastern-roman-pack.svg'")
p.write_text(t,encoding='utf-8')

for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'7\.0\.0',r'7\.1\.0').replace('3975','4107').replace('3933','4065')
 p.write_text(t,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V
newtests='node tools/smoke-v71-eastern-roman.mjs && node tools/runtime-v71-eastern-roman.mjs'
if newtests not in pkg['scripts']['test']:pkg['scripts']['test']+=' && '+newtests
pkg['scripts']['test:v71']=newtests;dump(Path('package.json'),pkg)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v7.1\n\n## v7.2 — Сасанидский Иран\n\n- падение Парфии, Ардашир и новая династия;\n- Шапур I, зороастрийское жречество и войны с Римом;\n- города, налоги, знать, христиане, иудеи и манихеи;\n- Кавад, Маздак, реформы Хосрова I и восточные границы;\n- последняя римско-персидская война и падение державы в VII веке.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v7_1.md').write_text('''# Patch v7.1.0 — Восточная Римская империя\n\n- 11 глав, 66 миссий и 132 карточки.\n- Восточный двор после 395 года, Феодосий II и стены Константинополя.\n- Бюрократия, Феодосиев кодекс, гуннская дипломатия и реформы Анастасия.\n- Юстиниан, восстание «Ника», Святая София и Corpus Juris Civilis.\n- Вандальская и Готская войны без схемы простого восстановления Рима.\n- Юстинианова чума, Маврикий, Фока, Ираклий и война 602–628 годов.\n''',encoding='utf-8')
(ROOT/'docs/QA_v7_1.md').write_text('''# QA v7.1.0\n\n- Проверены 88 сюжетных и 44 архивных карточки.\n- Проверены 66 миссий, 66 уроков, 11 глав, 11 пулов и 11 архивных дел.\n- Проверены пять фаз кампании, карта, 15 квизов и итоговый экзамен.\n- Проверены связи с позднеримской, религиозной и миграционной кампаниями.\n- Проверены обложка пака, офлайн-кэш, сохранения и пакетная коллекция.\n''',encoding='utf-8')

readme=ROOT/'README.md';txt=readme.read_text(encoding='utf-8');txt=re.sub(r'^# Codex of History v[^\n]+','# Codex of History v7.1.0',txt,count=1,flags=re.M)
section='''\n## v7.1.0 — Восточная Римская империя\n\n- 11 глав, 66 миссий и 132 карточки;\n- Константинополь, Феодосиевы стены, двор и право;\n- Юстиниан, «Ника», Святая София и кодификация;\n- Африка, Италия, чума и последняя война Ираклия.\n'''
if '## v7.1.0 — Восточная Римская империя' not in txt:txt=txt.replace('\n## v7.0.0 — Переселения и новые королевства',section+'\n## v7.0.0 — Переселения и новые королевства',1)
readme.write_text(txt,encoding='utf-8')
attr=ROOT/'ATTRIBUTION.md';at=attr.read_text(encoding='utf-8');sec='''\n\n## v7.1 — Восточная Римская империя\n\nЛокальные SVG-обложки 132 карточек и обложка пака созданы для Codex of History. Источниковая рамка использует Metropolitan Museum of Art, UNESCO World Heritage Centre, Theodosian Code, Procopius, Encyclopaedia Britannica и CDC Emerging Infectious Diseases. Жители государства представлены как римляне; термин «Византия» используется только как позднейшее исследовательское обозначение.\n'''
if '## v7.1 — Восточная Римская империя' not in at:at+=sec
attr.write_text(at,encoding='utf-8')
print('project integrated for',V)
