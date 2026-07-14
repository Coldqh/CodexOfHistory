#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='4.2.0'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for key,vals in [
 ('cards',['data/cards/israel-judah/story.json','data/cards/israel-judah/archive.json']),
 ('pools',['data/campaigns/israel-judah/pools.json']),
 ('quizzes',['data/quizzes/israel-judah/campaign.json']),
 ('stories',['data/stories/israel-judah/personal.json']),
 ('lessons',['data/lessons/israel-judah/campaign.json']),
 ('campaigns',['data/campaigns/israel-judah/campaign.json'])]:
 for x in vals:
  if x not in d[key]:d[key].append(x)
d['maps']['ISRAEL_JUDAH']='data/maps/israel-judah.json'
script='js/features/v4-2-israel-judah.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js');m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));add=load(Path('data/core/relations-v42-israel-judah.json'));existing={x['id'] for x in rels};rels.extend(x for x in add if x['id'] not in existing);dump(Path('data/core/relations.json'),rels);(ROOT/'data/core/relations-v42-israel-judah.json').unlink(missing_ok=True)

world=load(Path('data/world/campaigns.json'));camp=load(Path('data/campaigns/israel-judah/campaign.json'))
for c in world:
 if c['id']=='ISRAEL_JUDAH':
  c.update({'title':'Израиль, Иудея и Левант','subtitle':'Царства, надписи и археология','period':'ок. 1200–539 до н. э.','chapterCount':10,'releasedChapters':10,'status':'PLAYABLE','region':'Южный Левант и Трансиорданье','description':'От нагорных поселений и ранних царств до Самарии, Иерусалима, Ассирии и Вавилона.','chapters':[{'number':x['number'],'title':x['title']} for x in camp['chapters']]})
dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_IRON' and 'ISRAEL_JUDAH' not in e['campaignIds']:e['campaignIds'].insert(2,'ISRAEL_JUDAH')
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'))
new=[
 {'year':-1200,'label':'Рост поселений центрального нагорья','detail':'Археологические разведки фиксируют сеть небольших поселений раннего железного века.','campaignId':'ISRAEL_JUDAH','sourcePatch':'v4.2'},
 {'year':-1000,'label':'Традиционная эпоха Давида и Соломона','detail':'Библейская хронология связывает X век с ранней монархией; масштаб государства остаётся предметом спора.','campaignId':'ISRAEL_JUDAH','sourcePatch':'v4.2'},
 {'year':-880,'label':'Омриды и основание Самарии','detail':'Северное царство превращается в заметную региональную силу.','campaignId':'ISRAEL_JUDAH','sourcePatch':'v4.2'},
 {'year':-853,'label':'Ахав в коалиции при Каркаре','detail':'Ассирийская надпись перечисляет израильское войско среди противников Салманасара III.','campaignId':'ISRAEL_JUDAH','sourcePatch':'v4.2'},
 {'year':-840,'label':'Стела Меши и борьба Моава с Израилем','detail':'Моавитская царская надпись даёт независимую версию регионального конфликта.','campaignId':'ISRAEL_JUDAH','sourcePatch':'v4.2'},
 {'year':-732,'label':'Ассирия уничтожает Арам-Дамаск','detail':'Тиглатпаласар III перестраивает политическую карту северного Леванта.','campaignId':'ISRAEL_JUDAH','sourcePatch':'v4.2'},
 {'year':-722,'label':'Падение Самарии','detail':'Северное царство Израиль прекращает существование и превращается в ассирийские провинции.','campaignId':'ISRAEL_JUDAH','sourcePatch':'v4.2'},
 {'year':-701,'label':'Синаххериб захватывает Лахиш','detail':'Осада известна по археологии, рельефам, ассирийским анналам и библейскому тексту.','campaignId':'ISRAEL_JUDAH','sourcePatch':'v4.2'},
 {'year':-597,'label':'Первое вавилонское взятие Иерусалима','detail':'Навуходоносор II меняет царя Иудеи и депортирует часть элиты.','campaignId':'ISRAEL_JUDAH','sourcePatch':'v4.2'},
 {'year':-586,'label':'Разрушение Иерусалима и конец Иудеи','detail':'Вавилонское завоевание завершает независимую монархию и меняет письменную традицию региона.','campaignId':'ISRAEL_JUDAH','sourcePatch':'v4.2'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

manifest=load(Path('data/image_manifest.json'));existing={x['cardId']:x for x in manifest.get('images',[])}
for c in load(Path('data/cards/israel-judah/story.json'))+load(Path('data/cards/israel-judah/archive.json')):
 existing[c['id']]={'cardId':c['id'],'local':c['image']['local'],'file':c['image']['file'],'kind':'project-cover','prefer_remote':False,'caption':c['image']['caption'],'credit':c['image']['credit'],'source_url':c['image']['source_url'],'license':c['image']['license']}
images=list(existing.values());historical=sum(1 for x in images if x.get('prefer_remote'))
manifest.update({'version':V,'generatedAt':'2026-07-14','count':len(images),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(images)-historical,'dynamicQueryCount':len(images)-historical,'images':images});dump(Path('data/image_manifest.json'),manifest)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v4.2

## v4.3 — Архаическая Греция

Следующий патч продолжит железный век через Эгейский мир после распада микенских дворцов.

Основные задачи:

- ранний железный век и геометрический период;
- полис и гражданская община;
- Великая греческая колонизация;
- Спарта и Афины до классического периода;
- алфавит, Гомер и устная традиция;
- социальные конфликты и ранние законодатели;
- карта Эгейского и Средиземноморского мира;
- отдельные архивные пулы, пак и личные истории.
''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v4_2.md').write_text('''# Patch v4.2.0 — Израиль, Иудея и Левант

- 10 глав, 60 миссий и 120 карточек.
- Нагорные поселения, филистимские города и ранняя монархия.
- Северное царство Израиль, Омриды, Самария и Мегиддо.
- Иудея, Иерусалим, Лахиш и административная система.
- Моав, Аммон, Эдом и Арам-Дамаск.
- Ассирийское завоевание Израиля, поход 701 года и падение Иудеи.
- Библейская традиция отделена от археологии и внешних надписей.
- 10 архивных пулов, 10 личных историй, карта и отдельный пак.
''',encoding='utf-8')
(ROOT/'docs/QA_v4_2.md').write_text('''# QA v4.2.0

Проверяется:

- 120 новых карточек: 80 сюжетных и 40 архивных;
- 60 миссий и 60 уроков;
- 14 квизов, 10 пулов и 10 личных историй;
- старт новой игры только с LEV_S_01_01–03;
- пак кампании выдаёт только LEV_A_*;
- карта Южного Леванта и Трансиорданья;
- четыре модуля итогового экзамена;
- разделение археологии, местных надписей, имперских текстов и библейской традиции;
- версии manifest, runtime, Service Worker и package metadata.
''',encoding='utf-8')

p=ROOT/'README.md';txt=p.read_text(encoding='utf-8');txt=re.sub(r'^# Codex of History v[^\n]+','# Codex of History v4.2.0',txt,count=1,flags=re.M)
section='''\n## v4.2.0 — Израиль, Иудея и Левант\n\n- 10 глав, 60 миссий и 120 карточек.\n- Южный Левант от ранних поселений до ассирийского и вавилонского завоевания.\n- Израиль, Иудея, филистимские, арамейские и трансиорданские царства.\n- Археология, надписи и библейская традиция разделены по типу свидетельства.\n- Релизный ZIP содержит только изменённые и новые файлы.\n\n'''
if '## v4.2.0' not in txt:txt=txt.replace('\n',section,1)
p.write_text(txt,encoding='utf-8')
attr=ROOT/'ATTRIBUTION.md';at=attr.read_text(encoding='utf-8');section='''\n## v4.2 — Израиль, Иудея и Левант\n\nЛокальные SVG-обложки 120 карточек и вертикальная обложка пака созданы для Codex of History. Источники карточек используют материалы The Metropolitan Museum of Art по железному веку Леванта и иудейским предметам, British Museum по Лахишским рельефам, призме Синаххериба и стеле Меши. Динамические исторические изображения загружаются только для видимых карточек и живут до конца текущей сессии.\n'''
if '## v4.2 — Израиль' not in at:at+=section
attr.write_text(at,encoding='utf-8')

# Update runtime version surfaces and existing tests to the new content totals.
for path in (ROOT/'js').rglob('*.js'):
 text=path.read_text(encoding='utf-8').replace('4.1.0',V)
 path.write_text(text,encoding='utf-8')
for path in (ROOT/'tools').glob('*.mjs'):
 text=path.read_text(encoding='utf-8').replace('4.1.0',V).replace('1835','1955').replace('1793','1913')
 path.write_text(text,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V
if 'node tools/smoke-v42-israel-judah.mjs' not in pkg['scripts']['test']:
 pkg['scripts']['test']+=' && node tools/smoke-v42-israel-judah.mjs && node tools/runtime-v42-israel-judah.mjs'
pkg['scripts']['test:v42']='node tools/smoke-v42-israel-judah.mjs && node tools/runtime-v42-israel-judah.mjs';dump(Path('package.json'),pkg)

for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;text=p.read_text(encoding='utf-8').replace('4.1.0',V).replace('codex-v4.1.0','codex-v4.2.0')
 p.write_text(text,encoding='utf-8')
p=ROOT/'sw.js';text=p.read_text(encoding='utf-8')
if "'./assets/packs/israel-judah-pack.svg'" not in text:text=text.replace("'./assets/packs/phoenicians-pack.svg',","'./assets/packs/phoenicians-pack.svg','./assets/packs/israel-judah-pack.svg',")
if "'./js/features/v4-2-israel-judah.js'" not in text:text=text.replace("'./js/features/v4-1-phoenicians.js',","'./js/features/v4-1-phoenicians.js','./js/features/v4-2-israel-judah.js',")
p.write_text(text,encoding='utf-8')
print('integrated v4.2')
