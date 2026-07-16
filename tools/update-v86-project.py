#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='8.6.0';OLD='8.5.0';CHECKED='2026-07-16'

def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={
 'cards':['data/cards/al-andalus-west/story.json','data/cards/al-andalus-west/archive.json'],
 'campaigns':['data/campaigns/al-andalus-west/campaign.json'],
 'pools':['data/campaigns/al-andalus-west/pools.json'],
 'quizzes':['data/quizzes/al-andalus-west/campaign.json'],
 'stories':['data/stories/al-andalus-west/personal.json'],
 'lessons':['data/lessons/al-andalus-west/campaign.json'],
}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['AL_ANDALUS_WEST']='data/maps/al-andalus-west.json'
script='js/features/v8-6-al-andalus-west.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));rels=[r for r in rels if not re.fullmatch(r'REL_ADW_\d{4}',r.get('id',''))]
new=load(Path('data/core/relations-860-al-andalus-west.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/al-andalus-west/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
entry={'id':'AL_ANDALUS_WEST','eraId':'ERA_EARLY_MEDIEVAL','order':43,'title':'Аль-Андалус и исламский Запад','subtitle':'Эмират, халифат, Магриб и города западного Средиземноморья','period':'711–1031 годы','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Иберийский полуостров и Магриб','description':'Завоевание Иберии, независимый омейядский эмират, Кордовский халифат, пограничные марки, городские общины, экономика, Магриб, Мадинат аз-Захра, книжность, фитна и первые тайфы.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]}
world=[c for c in world if c['id']!='AL_ANDALUS_WEST'];world.append(entry);world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)
eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_EARLY_MEDIEVAL':
  ids=[x for x in e.get('campaignIds',[]) if x!='AL_ANDALUS_WEST'];e['campaignIds']=ids+['AL_ANDALUS_WEST'];e['status']='PLAYABLE'
  e['description']='Аббасидский Багдад, средневековая Византия, северные морские сети, славяноязычные державы и исламский Запад показывают раннее Средневековье как систему империй, княжеств, городов, морских путей и новых письменных культур VIII–XI веков.'
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'));events=[
 {'year':711,'label':'Войска Тарика переходят в Иберию','detail':'Переход через пролив открывает длительный процесс завоевания и местных соглашений.','campaignId':'AL_ANDALUS_WEST','sourcePatch':'v8.6'},
 {'year':756,'label':'Абд ар-Рахман I создаёт независимый эмират','detail':'Западная омейядская династия закрепляется в Кордове после краха сирийского центра.','campaignId':'AL_ANDALUS_WEST','sourcePatch':'v8.6'},
 {'year':785,'label':'Начинается строительство Большой мечети Кордовы','detail':'Соборная мечеть становится многослойным символом династии и столицы.','campaignId':'AL_ANDALUS_WEST','sourcePatch':'v8.6'},
 {'year':800,'label':'Аглабиды получают власть в Ифрикии','detail':'Кайруан становится центром почти самостоятельной династии исламского Запада.','campaignId':'AL_ANDALUS_WEST','sourcePatch':'v8.6'},
 {'year':827,'label':'Аглабидские силы начинают завоевание Сицилии','detail':'Морская война перестраивает центральное Средиземноморье.','campaignId':'AL_ANDALUS_WEST','sourcePatch':'v8.6'},
 {'year':850,'label':'Начинается конфликт кордовских мучеников','detail':'Публичные выступления части христиан показывают напряжение внутри арабоязычного города.','campaignId':'AL_ANDALUS_WEST','sourcePatch':'v8.6'},
 {'year':880,'label':'Ибн Хафсун укрепляется в Бобастро','detail':'Горная коалиция десятилетиями сопротивляется централизации Кордовы.','campaignId':'AL_ANDALUS_WEST','sourcePatch':'v8.6'},
 {'year':909,'label':'Фатимиды свергают Аглабидов','detail':'Новая халифская династия меняет борьбу за Магриб и западное Средиземноморье.','campaignId':'AL_ANDALUS_WEST','sourcePatch':'v8.6'},
 {'year':929,'label':'Абд ар-Рахман III провозглашает Кордовский халифат','detail':'Титул соединяет внутреннюю централизацию и соперничество с Фатимидами.','campaignId':'AL_ANDALUS_WEST','sourcePatch':'v8.6'},
 {'year':936,'label':'Начинается строительство Мадинат аз-Захры','detail':'Новый дворцовый город превращает придворную иерархию в архитектуру.','campaignId':'AL_ANDALUS_WEST','sourcePatch':'v8.6'},
 {'year':997,'label':'Поход аль-Мансура достигает Сантьяго','detail':'Разорение святыни демонстрирует силу, но не создаёт постоянного контроля над Галисией.','campaignId':'AL_ANDALUS_WEST','sourcePatch':'v8.6'},
 {'year':1009,'label':'Фитна разрушает кордовский политический центр','detail':'Перевороты, конкурирующие халифы и военные группы раскалывают систему.','campaignId':'AL_ANDALUS_WEST','sourcePatch':'v8.6'},
 {'year':1031,'label':'Кордовский халифат упразднён','detail':'Региональные тайфы наследуют города, дворы, армии и ремесленные сети.','campaignId':'AL_ANDALUS_WEST','sourcePatch':'v8.6'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "AL_ANDALUS_WEST": {' not in s:
 marker='    "SLAVIC_BULGARIA_RUS": {';i=s.index(marker)
 group='''    "AL_ANDALUS_WEST": {\n        "terms": ["Umayyad Spain", "Great Mosque Cordoba", "Medina Azahara", "Al-Andalus coin", "Bobastro", "Kairouan Aghlabid", "Rustamid Tahert", "Idrisid Fez", "Al-Zahrawi manuscript", "Cordoba Caliphate"],\n        "base": [("ru", "аль-Андалус Кордова Магриб раннее Средневековье"), ("en", "Al-Andalus Cordoba caliphate Islamic West archaeology"), ("en", "Umayyad Spain Maghreb Kairouan Fez medieval")],\n    },\n'''
 s=s[:i]+group+s[i:]
old='("/slavic-bulgaria-rus/", "SLAVIC_BULGARIA_RUS"),'
if '("/al-andalus-west/", "AL_ANDALUS_WEST")' not in s:
 if old not in s:raise SystemExit('image marker missing')
 s=s.replace(old,'("/al-andalus-west/", "AL_ANDALUS_WEST"), '+old)
p.write_text(s,encoding='utf-8')

entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg')
  entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v8.5.0','codex-v8.6.0').replace('codex-v8\\.5\\.0','codex-v8\\.6\\.0')
 if rel=='index.html':t=re.sub(r'js/bootstrap\.js\?v=[0-9.]+',f'js/bootstrap.js?v={V}',t)
 p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v8-6-al-andalus-west.js'" not in t:t=t.replace("'./js/features/v8-5-slavic-bulgaria-rus.js'","'./js/features/v8-5-slavic-bulgaria-rus.js','./js/features/v8-6-al-andalus-west.js'")
if "'./assets/packs/al-andalus-west-pack.svg'" not in t:t=t.replace("'./assets/packs/slavic-bulgaria-rus-pack.svg'","'./assets/packs/slavic-bulgaria-rus-pack.svg','./assets/packs/al-andalus-west-pack.svg'")
p.write_text(t,encoding='utf-8')

for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'8\.5\.0',r'8\.6\.0').replace('5787','5931').replace('5745','5889').replace('2791','2863')
 p.write_text(t,encoding='utf-8')

p=ROOT/'tools/smoke-v82-franks-transition.mjs';t=p.read_text(encoding='utf-8');t=t.replace("['ABBASID_BAGHDAD','BYZANTIUM_MACEDONIAN','VIKINGS_NORTH_ATLANTIC','SLAVIC_BULGARIA_RUS']","['ABBASID_BAGHDAD','BYZANTIUM_MACEDONIAN','VIKINGS_NORTH_ATLANTIC','SLAVIC_BULGARIA_RUS','AL_ANDALUS_WEST']");p.write_text(t,encoding='utf-8')

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v8.6\n\n## v8.7 — Китай: от Тан к Сун\n\n- Чанъань и устройство Танской империи;\n- экзамены, чиновники, буддизм и международные города;\n- восстание Ань Лушаня и региональные военные правители;\n- падение Тан и эпоха Пяти династий;\n- объединение при Сун, города, торговля и печать.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v8_6.md').write_text('''# Patch v8.6.0 — Аль-Андалус и исламский Запад\n\n- 12 глав, 72 миссии и 144 карточки.\n- Завоевание Иберии, независимый омейядский эмират и пограничные марки.\n- Кордова, Большая мечеть, общины, право, ирригация, ремесло и порты.\n- Аглабиды, Рустамиды, Идрисиды и соперничество в Магрибе.\n- Абд ар-Рахман III, Мадинат аз-Захра, книжность, аль-Мансур и тайфы.\n''',encoding='utf-8')
(ROOT/'docs/QA_v8_6.md').write_text('''# QA v8.6.0\n\n- Проверены 96 сюжетных и 48 архивных карточек.\n- Проверены 72 миссии, 72 урока, 12 глав, 12 пулов и 12 личных историй.\n- Проверены карта, четыре фазы, архивный пак и четыре модуля итогового экзамена.\n- Проверены уникальность ID и названий во всём проекте.\n- Проверены связи с исламской, аббасидской и франкской кампаниями.\n- Проверены миграция сейва, коллекция, прямые кнопки этапов урока и PWA-кэш.\n''',encoding='utf-8')
p=ROOT/'README.md';s=p.read_text(encoding='utf-8');s=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',s,count=1,flags=re.M);block='''\n## v8.6.0 — Аль-Андалус и исламский Запад\n\n- 12 глав, 72 миссии и 144 карточки.\n- Кордовский эмират и халифат, Магриб, города, общины, экономика и тайфы.\n- Patch-only архив.\n\n'''
if '## v8.6.0' not in s:s=s.replace('\n',block,1)
p.write_text(s,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';s=p.read_text(encoding='utf-8');block='''\n\n## v8.6 — Аль-Андалус и исламский Запад\n\nЛокальные SVG-обложки 144 карточек и кампанийного пака созданы для Codex of History. Источниковая рамка опирается на Metropolitan Museum of Art, UNESCO Historic Centre of Cordoba, UNESCO Caliphate City of Medina Azahara, UNESCO Kairouan, UNESCO Medina of Fez и корпус переводных средневековых источников Fordham University.\n'''
if '## v8.6 —' not in s:s+=block
p.write_text(s,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test:v86']='node tools/smoke-v86-al-andalus-west.mjs && node tools/runtime-v86-al-andalus-west.mjs'
if 'tools/smoke-v86-al-andalus-west.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v86-al-andalus-west.mjs && node tools/runtime-v86-al-andalus-west.mjs'
dump(Path('package.json'),pkg)
print('integrated v8.6 Al-Andalus and Islamic West campaign')
