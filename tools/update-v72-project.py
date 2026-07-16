#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='7.2.0';OLD='7.1.0';CHECKED='2026-07-16'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={'cards':['data/cards/sasanian/story.json','data/cards/sasanian/archive.json'],'campaigns':['data/campaigns/sasanian/campaign.json'],'pools':['data/campaigns/sasanian/pools.json'],'quizzes':['data/quizzes/sasanian/campaign.json'],'stories':['data/stories/sasanian/personal.json'],'lessons':['data/lessons/sasanian/campaign.json']}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['SASANIAN']='data/maps/sasanian.json'
script='js/features/v7-2-sasanian.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));new=load(Path('data/core/relations-v72-sasanian.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/sasanian/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
entry={'id':'SASANIAN','eraId':'ERA_LATE_ANTIQUITY','order':30,'title':'Сасанидский Иран','subtitle':'Шахиншах, знать, религии и границы','period':'224–651 годы','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Иран, Месопотамия, Кавказ и Центральная Азия','description':'От Ардашира и Шапура I до религиозных общин, налогов, пограничных царств, эфталитов, реформ Хосрова I и конца династии после последней войны с Восточным Римом.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]}
world=[c for c in world if c['id']!='SASANIAN']
order_map={'LATE_ANTIQUITY':26,'EARLY_CHRISTIANITY':27,'MIGRATION_KINGDOMS':28,'EASTERN_ROMAN':29,'SASANIAN':30,'GUPTA':31,'CHINA_POST_HAN':32,'ISLAMIC_ORIGINS':33}
world.append(entry)
for c in world:
 if c['id'] in order_map:c['order']=order_map[c['id']]
world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_LATE_ANTIQUITY':
  e['description']='Поздняя Римская империя перестраивает право и налоги, западные провинции превращаются в королевства, Константинополь сохраняет римскую государственность, а Сасанидский Иран соединяет шахиншаха, знать, жречество, города и несколько военных границ.'
  e['campaignIds']=['LATE_ANTIQUITY','EARLY_CHRISTIANITY','MIGRATION_KINGDOMS','EASTERN_ROMAN','SASANIAN','GUPTA','CHINA_POST_HAN']
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'));events=[
 {'year':224,'label':'Ардашир побеждает Артабана IV','detail':'Битва при Хормоздгане открывает переход от Аршакидов к Сасанидам.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':226,'label':'Коронация Ардашира как шахиншаха','detail':'Новая династия формирует царскую титулатуру и символику.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':260,'label':'Шапур I пленяет Валериана','detail':'Римский император попадает в плен после кампании в Месопотамии.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':276,'label':'Картир усиливает жреческую власть','detail':'Надписи фиксируют карьеру жреца и борьбу религиозных общин.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':359,'label':'Сасаниды берут Амиду','detail':'Шапур II выигрывает тяжёлую осаду на римской границе.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':363,'label':'Мир Иовиана','detail':'Рим уступает города и политические позиции после гибели Юлиана.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':387,'label':'Раздел Армении','detail':'Рим и Иран закрепляют разные сферы влияния при сохранении местной знати.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':410,'label':'Собор церкви Востока','detail':'Епископы собираются в Селевкии-Ктесифоне и укрепляют общую организацию.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':484,'label':'Гибель Пероза в войне с эфталитами','detail':'Восточное поражение вызывает дань и династический кризис.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':496,'label':'Свержение Кавада I','detail':'Знать и жречество временно лишают шаха престола.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':531,'label':'Хосров I становится шахиншахом','detail':'Начинается этап налоговых, военных и придворных реформ.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':540,'label':'Хосров I берёт Антиохию','detail':'Жители переселяются в новый город рядом с Ктесифоном.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':570,'label':'Сасанидское вмешательство в Йемене','detail':'Иранские силы вытесняют аксумское влияние и закрепляются в Южной Аравии.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':602,'label':'Начало последней римско-сасанидской войны','detail':'Хосров II использует переворот Фоки как повод для масштабного наступления.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':614,'label':'Сасаниды занимают Иерусалим','detail':'Армия Ирана захватывает город и важнейшие христианские святыни.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':628,'label':'Свержение Хосрова II','detail':'Поражение в войне открывает серию кратких правлений и гражданский кризис.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':637,'label':'Падение Ктесифона','detail':'Арабские армии занимают столичную агломерацию и царскую казну.','campaignId':'SASANIAN','sourcePatch':'v7.2'},
 {'year':651,'label':'Смерть Яздигерда III','detail':'Гибель последнего шахиншаха завершает сасанидскую династию.','campaignId':'SASANIAN','sourcePatch':'v7.2'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "SASANIAN": {' not in s:
 marker='    "EASTERN_ROMAN": {';i=s.index(marker);group='''    "SASANIAN": {\n        "terms": ["Сасанидский Иран", "Sasanian Empire", "Ардашир", "Ardashir", "Шапур I", "Shapur I", "Ктесифон", "Ctesiphon", "Картир", "Kartir", "Хосров I", "Khosrow I", "Так-е Бостан", "Taq-e Bostan"],\n        "base": [("ru", "Сасанидский Иран"), ("en", "Sasanian Empire"), ("en", "Sasanian Iran Late Antiquity")],\n    },\n''';s=s[:i]+group+s[i:]
old='("/eastern-roman/", "EASTERN_ROMAN"),'
if '("/sasanian/", "SASANIAN")' not in s:
 if old not in s:raise SystemExit('image path marker missing')
 s=s.replace(old,old+' ("/sasanian/", "SASANIAN"),')
p.write_text(s,encoding='utf-8')

entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg');entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v7.1.0','codex-v7.2.0').replace('codex-v7\\.1\\.0','codex-v7\\.2\\.0');p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v7-2-sasanian.js'" not in t:t=t.replace("'./js/features/v7-1-eastern-roman.js'","'./js/features/v7-1-eastern-roman.js','./js/features/v7-2-sasanian.js'")
if "'./assets/packs/sasanian-pack.svg'" not in t:t=t.replace("'./assets/packs/eastern-roman-pack.svg'","'./assets/packs/eastern-roman-pack.svg','./assets/packs/sasanian-pack.svg'")
p.write_text(t,encoding='utf-8')

for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'7\.1\.0',r'7\.2\.0').replace('4107','4239').replace('4065','4197').replace('1951','2017')
 p.write_text(t,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V
newtests='node tools/smoke-v72-sasanian.mjs && node tools/runtime-v72-sasanian.mjs'
if newtests not in pkg['scripts']['test']:pkg['scripts']['test']+=' && '+newtests
pkg['scripts']['test:v72']=newtests;dump(Path('package.json'),pkg)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v7.2\n\n## v7.3 — Центральная Азия после Хань\n\n- распад кушанского мира и новые региональные центры;\n- Согдиана, Самарканд и торговые диаспоры;\n- эфталиты, Таримские оазисы и буддийские сети;\n- ранние тюркские каганаты и дипломатия VI–VII веков;\n- связь Китая, Ирана, Индии и Восточного Средиземноморья.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v7_2.md').write_text('''# Patch v7.2.0 — Сасанидский Иран\n\n- 11 глав, 66 миссий и 132 карточки.\n- Ардашир, Шапур I, Шапур II, Кавад, Хосров I, Хосров II и Яздигерд III.\n- Двор, великие дома, дихканы, жречество и религиозные общины.\n- Города, ирригация, налоги, серебряная драхма и Персидский залив.\n- Армения, Кавказ, Лахмиды, Йемен, эфталиты и центральноазиатские границы.\n- Последняя война с Восточным Римом и конец династии в 651 году.\n''',encoding='utf-8')
(ROOT/'docs/QA_v7_2.md').write_text('''# QA v7.2.0\n\n- `npm test` проверяет старые кампании и новые smoke/runtime-модули.\n- Отдельно проверяются 132 карточки, 66 миссий, 15 квизов, карта, пак, экзамен и связи.\n- Стабильность сохранения и ленивой коллекции остаётся под тестом v6.9.1.\n''',encoding='utf-8')

attr=ROOT/'ATTRIBUTION.md';txt=attr.read_text(encoding='utf-8')
block='''\n\n## v7.2 — Сасанидский Иран\n\nЛокальные SVG-обложки 132 карточек и обложка пака созданы для Codex of History. Учебная основа: Metropolitan Museum of Art, Encyclopaedia Iranica, Encyclopaedia Britannica, надпись Шапура I и исследования по сасанидским монетам, печатям, религиозным общинам и пограничным системам.\n'''
if '## v7.2 — Сасанидский Иран' not in txt:attr.write_text(txt.rstrip()+block,encoding='utf-8')
readme=ROOT/'README.md';txt=readme.read_text(encoding='utf-8')
if '## v7.2.0 — Сасанидский Иран' not in txt:readme.write_text(txt.rstrip()+'''\n\n## v7.2.0 — Сасанидский Иран\n\nНовая кампания из 11 глав соединяет основание династии, войны с Римом, двор и знать, жречество и религиозные общины, города и налоги, Армению и арабские границы, эфталитский кризис, реформы Хосрова I и конец державы в 651 году.\n''',encoding='utf-8')
print('updated project to',V)
