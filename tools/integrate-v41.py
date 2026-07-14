#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='4.1.0'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for key,vals in [
 ('cards',['data/cards/phoenicians/story.json','data/cards/phoenicians/archive.json']),
 ('pools',['data/campaigns/phoenicians/pools.json']),
 ('quizzes',['data/quizzes/phoenicians/campaign.json']),
 ('stories',['data/stories/phoenicians/personal.json']),
 ('lessons',['data/lessons/phoenicians/campaign.json']),
 ('campaigns',['data/campaigns/phoenicians/campaign.json'])]:
 for x in vals:
  if x not in d[key]:d[key].append(x)
d['maps']['PHOENICIANS']='data/maps/phoenicians.json'
script='js/features/v4-1-phoenicians.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js');m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));add=load(Path('data/core/relations-v41-phoenicians.json'));existing={x['id'] for x in rels};rels.extend(x for x in add if x['id'] not in existing);dump(Path('data/core/relations.json'),rels);(ROOT/'data/core/relations-v41-phoenicians.json').unlink(missing_ok=True)

world=load(Path('data/world/campaigns.json'));camp=load(Path('data/campaigns/phoenicians/campaign.json'))
for c in world:
 if c['id']=='PHOENICIANS':
  c.update({'title':'Финикийцы и западное Средиземноморье','subtitle':'Города, алфавит и морские сети','period':'ок. 1200–539 до н. э.','chapterCount':10,'releasedChapters':10,'status':'PLAYABLE','region':'Левант, Кипр и западное Средиземноморье','description':'От городов Леванта и финикийского алфавита до Кипра, Сардинии, Иберии и раннего Карфагена.','chapters':[{'number':x['number'],'title':x['title']} for x in camp['chapters']]})
dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_IRON' and 'PHOENICIANS' not in e['campaignIds']:e['campaignIds'].insert(1,'PHOENICIANS')
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'))
new=[
 {'year':-1075,'label':'Путешествие Уну-Амона в Библос','detail':'Египетский литературный текст отражает роль Библоса и изменения после бронзового кризиса.','campaignId':'PHOENICIANS','sourcePatch':'v4.1'},
 {'year':-1000,'label':'Формирование стандартного финикийского алфавита','detail':'Порядок двадцати двух согласных знаков распространяется через города и морские контакты.','campaignId':'PHOENICIANS','sourcePatch':'v4.1'},
 {'year':-900,'label':'Рост тирских и сидонских морских сетей','detail':'Города Леванта укрепляют связи с Кипром и центральным Средиземноморьем.','campaignId':'PHOENICIANS','sourcePatch':'v4.1'},
 {'year':-825,'label':'Ранние финикийские поселения на западе','detail':'Археология фиксирует центры на Сардинии, Сицилии, в Северной Африке и Иберии.','campaignId':'PHOENICIANS','sourcePatch':'v4.1'},
 {'year':-814,'label':'Традиционная дата основания Карфагена','detail':'Поздняя традиция связывает город с Элиссой; археологическая фиксация начинается в VIII веке до н. э.','campaignId':'PHOENICIANS','sourcePatch':'v4.1'},
 {'year':-800,'label':'Греческая адаптация финикийского письма','detail':'Грекоязычные сообщества изменяют систему знаков и используют часть букв для гласных.','campaignId':'PHOENICIANS','sourcePatch':'v4.1'},
 {'year':-701,'label':'Финикийские города в ассирийской системе','detail':'Тир, Сидон и другие города платят дань, предоставляют корабли и периодически восстают.','campaignId':'PHOENICIANS','sourcePatch':'v4.1'},
 {'year':-677,'label':'Разрушение Сидона Асархаддоном','detail':'Ассирийский царь подавляет восстание и перестраивает политический порядок города.','campaignId':'PHOENICIANS','sourcePatch':'v4.1'},
 {'year':-585,'label':'Вавилонское давление на Тир','detail':'Поздняя традиция связывает правление Навуходоносора II с длительной осадой островного города.','campaignId':'PHOENICIANS','sourcePatch':'v4.1'},
 {'year':-539,'label':'Финикийские города входят в Ахеменидскую державу','detail':'Города сохраняют морские силы и местные институты при новом имперском верховенстве.','campaignId':'PHOENICIANS','sourcePatch':'v4.1'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

manifest=load(Path('data/image_manifest.json'));existing={x['cardId']:x for x in manifest.get('images',[])}
for c in load(Path('data/cards/phoenicians/story.json'))+load(Path('data/cards/phoenicians/archive.json')):
 existing[c['id']]={'cardId':c['id'],'local':c['image']['local'],'file':c['image']['file'],'kind':'project-cover','prefer_remote':False,'caption':c['image']['caption'],'credit':c['image']['credit'],'source_url':c['image']['source_url'],'license':c['image']['license']}
images=list(existing.values());historical=sum(1 for x in images if x.get('prefer_remote'))
manifest.update({'version':V,'generatedAt':'2026-07-14','count':len(images),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(images)-historical,'dynamicQueryCount':len(images)-historical,'images':images});dump(Path('data/image_manifest.json'),manifest)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v4.1

## v4.2 — Израиль, Иудея и Левант

Следующий патч продолжит железный век через внутренний Левант и развитие региональных царств.

Основные задачи:

- горные поселения раннего железного века;
- Израиль и Иудея как отдельные политические системы;
- Самария, Иерусалим, Лахиш и Мегиддо;
- Моав, Аммон, Эдом и арамейские государства;
- надписи, библейские тексты и археология;
- ассирийское и вавилонское давление;
- отдельная карта, архивные пулы и личные истории.
''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v4_1.md').write_text('''# Patch v4.1.0 — Финикийцы и западное Средиземноморье

- 10 глав, 60 миссий и 120 карточек.
- Тир, Сидон, Библ, Арвад и городская структура побережья.
- Финикийский алфавит, надписи и греческая адаптация письма.
- Корабли, гавани, пурпур, кедр, резная кость и металлические изделия.
- Кипр, Сицилия, Мальта, Сардиния, Иберия и Атлантический выход.
- Ранний Карфаген без перехода к Пуническим войнам.
- Имперское давление Ассирии и Вавилонии и критика источников.
- 10 архивных пулов, 10 личных историй, морская карта и отдельный пак.
''',encoding='utf-8')
(ROOT/'docs/QA_v4_1.md').write_text('''# QA v4.1.0

Проверяется:

- 120 новых карточек: 80 сюжетных и 40 архивных;
- 60 миссий и 60 уроков;
- 14 квизов, 10 пулов и 10 личных историй;
- старт новой игры только с PHO_S_01_01–03;
- пак кампании выдаёт только PHO_A_*;
- карта Леванта, Кипра, Сардинии, Иберии и Карфагена;
- четыре модуля итогового экзамена;
- отсутствие утверждения о единой финикийской империи;
- разделение традиционной даты основания Карфагена и археологической датировки;
- версии manifest, runtime, Service Worker и package metadata.
''',encoding='utf-8')

p=ROOT/'README.md';txt=p.read_text(encoding='utf-8');txt=re.sub(r'^# Codex of History v[^\n]+','# Codex of History v4.1.0',txt,count=1,flags=re.M)
section='''\n## v4.1.0 — Финикийцы и западное Средиземноморье\n\n- 10 глав, 60 миссий и 120 карточек.\n- Города Леванта, алфавит, корабли, пурпур и ремесленные сети.\n- Кипр, Сицилия, Сардиния, Иберия и ранний Карфаген.\n- Ассирийское и вавилонское давление без перехода к Пуническим войнам.\n- Релизный ZIP содержит только изменённые и новые файлы.\n\n'''
if '## v4.1.0' not in txt:txt=txt.replace('\n',section,1)
p.write_text(txt,encoding='utf-8')
attr=ROOT/'ATTRIBUTION.md';at=attr.read_text(encoding='utf-8');section='''\n## v4.1 — Финикийцы и западное Средиземноморье\n\nЛокальные SVG-обложки 120 карточек и вертикальная обложка морского пака созданы для Codex of History. Источники карточек используют материалы UNESCO по Тиру, Библосу, Карфагену и Керкуану, British Museum по финикийским надписям и алфавитным системам, The Metropolitan Museum of Art по левантийским предметам и Smarthistory по ханаанской среде. Динамические исторические изображения загружаются только для видимых карточек и живут до конца текущей сессии.\n'''
if '## v4.1 — Финикийцы' not in at:at+=section
attr.write_text(at,encoding='utf-8')

# Update runtime version surfaces and existing tests to the new content total.
for path in (ROOT/'js').rglob('*.js'):
 text=path.read_text(encoding='utf-8').replace('4.0.0',V)
 path.write_text(text,encoding='utf-8')
for path in (ROOT/'tools').glob('*.mjs'):
 text=path.read_text(encoding='utf-8').replace('4.0.0',V).replace('1715','1835').replace('1673','1793')
 path.write_text(text,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V
if 'node tools/smoke-v41-phoenicians.mjs' not in pkg['scripts']['test']:
 pkg['scripts']['test']+=' && node tools/smoke-v41-phoenicians.mjs && node tools/runtime-v41-phoenicians.mjs'
pkg['scripts']['test:v41']='node tools/smoke-v41-phoenicians.mjs && node tools/runtime-v41-phoenicians.mjs';dump(Path('package.json'),pkg)

for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;text=p.read_text(encoding='utf-8').replace('4.0.0',V).replace('codex-v4.0.0','codex-v4.1.0')
 p.write_text(text,encoding='utf-8')
p=ROOT/'sw.js';text=p.read_text(encoding='utf-8')
if "'./assets/packs/phoenicians-pack.svg'" not in text:text=text.replace("'./assets/packs/assyria-babylon-pack.svg',","'./assets/packs/assyria-babylon-pack.svg','./assets/packs/phoenicians-pack.svg',")
if "'./js/features/v4-1-phoenicians.js'" not in text:text=text.replace("'./js/features/v4-0-assyria-babylon.js',","'./js/features/v4-0-assyria-babylon.js','./js/features/v4-1-phoenicians.js',")
p.write_text(text,encoding='utf-8')
print('integrated v4.1')
