#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='8.2.0';OLD='8.1.0';CHECKED='2026-07-16'

def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Content registry.
m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={
 'cards':['data/cards/franks-transition/story.json','data/cards/franks-transition/archive.json'],
 'campaigns':['data/campaigns/franks-transition/campaign.json'],
 'pools':['data/campaigns/franks-transition/pools.json'],
 'quizzes':['data/quizzes/franks-transition/campaign.json'],
 'stories':['data/stories/franks-transition/personal.json'],
 'lessons':['data/lessons/franks-transition/campaign.json'],
}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['FRANKS_TRANSITION']='data/maps/franks-transition.json'
script='js/features/v8-2-franks-transition.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

# Relations.
rels=load(Path('data/core/relations.json'));rels=[r for r in rels if not re.fullmatch(r'REL_FRC_\d{4}',r.get('id',''))]
new=load(Path('data/core/relations-820-franks-transition.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

# Campaign catalogue and era reorganisation.
world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/franks-transition/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
for c in world:
 if c['id']=='WORLD_AROUND_700':c['eraId']='ERA_TRANSITION'
 if c['id']=='ABBASID_BAGHDAD':c['eraId']='ERA_EARLY_MEDIEVAL'
entry={'id':'FRANKS_TRANSITION','eraId':'ERA_TRANSITION','order':39,'title':'Франки: от Меровингов к Каролингам','subtitle':'Дворы, майордомы, Карл Великий и Верден','period':'511–843 годы','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Галлия, Рейн, Германия и Италия','description':'Меровингские королевства, майордомы, Карл Мартелл, Пипин Короткий, Карл Великий, управление империей, Ахен, письменная реформа и Верденский договор.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]}
world=[c for c in world if c['id']!='FRANKS_TRANSITION'];world.append(entry);world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)

# Move the comparative 700 campaign into the transition era at card level as well.
for rel in ['data/cards/world-around-700/story.json','data/cards/world-around-700/archive.json']:
 cards=load(Path(rel))
 for card in cards: card['era']='Переход к Средневековью'
 dump(Path(rel),cards)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_LATE_ANTIQUITY':
  e['campaignIds']=[x for x in e.get('campaignIds',[]) if x!='WORLD_AROUND_700']
  e['dateLabel']='II век до н. э. – VII век н. э.';e['endYear']=650
  e['description']='Поздняя Античность охватывает перестройку Рима, новые религиозные системы, Сасанидский Иран, постханьскую Азию, Красное море и самостоятельные траектории Америк до мира VII века.'
 if e['id']=='ERA_TRANSITION':
  e['title']='Переход к Средневековью';e['subtitle']='Новые державы и политические миры VI–IX веков';e['dateLabel']='VI–IX века н. э.';e['startYear']=500;e['endYear']=843;e['status']='PLAYABLE'
  e['description']='Сравнительный мир около 700 года, возникновение исламского мира и франкская линия от Меровингов до Вердена показывают несколько разных переходов к Средневековью.'
  e['campaignIds']=['WORLD_AROUND_700','ISLAMIC_ORIGINS','FRANKS_TRANSITION']
# Create the full early medieval era and move Abbasids into it.
if not any(e['id']=='ERA_EARLY_MEDIEVAL' for e in eras):
 eras.append({'id':'ERA_EARLY_MEDIEVAL','order':8,'title':'Раннее Средневековье','subtitle':'Империи, королевства и торговые миры','dateLabel':'750–1050 годы н. э.','startYear':750,'endYear':1050,'accent':'#6f7f93','icon':'♜','cover':'assets/eras/early-medieval.svg','description':'Аббасидский Багдад открывает эпоху региональных империй, морских и сухопутных сетей, новых королевств, письменных культур и религиозных институтов VIII–XI веков.','campaignIds':['ABBASID_BAGHDAD'],'status':'PLAYABLE'})
else:
 for e in eras:
  if e['id']=='ERA_EARLY_MEDIEVAL':
   e['campaignIds']=['ABBASID_BAGHDAD'];e['status']='PLAYABLE'
eras.sort(key=lambda x:x.get('order',999));dump(Path('data/world/eras.json'),eras)

# Timeline.
wt=load(Path('data/world/timeline.json'));events=[
 {'year':511,'label':'Раздел Франкского королевства после смерти Хлодвига','detail':'Сыновья правителя создают несколько дворов внутри общего династического пространства.','campaignId':'FRANKS_TRANSITION','sourcePatch':'v8.2'},
 {'year':614,'label':'Парижский эдикт Хлотаря II','detail':'Корона, церковь и региональная знать закрепляют политический компромисс.','campaignId':'FRANKS_TRANSITION','sourcePatch':'v8.2'},
 {'year':687,'label':'Победа Пипина Геристальского при Тертри','detail':'Австразийская коалиция получает превосходство над Нейстрией.','campaignId':'FRANKS_TRANSITION','sourcePatch':'v8.2'},
 {'year':732,'label':'Сражение между Туром и Пуатье','detail':'Карл Мартелл останавливает конкретный омейядский поход в ходе долгой борьбы за Аквитанию.','campaignId':'FRANKS_TRANSITION','sourcePatch':'v8.2'},
 {'year':751,'label':'Пипин Короткий становится королём франков','detail':'Меровингская династия сменяется Каролингами через решение элит и церковную легитимацию.','campaignId':'FRANKS_TRANSITION','sourcePatch':'v8.2'},
 {'year':774,'label':'Карл Великий завоёвывает Лангобардское королевство','detail':'Взятие Павии даёт франкскому королю новый итальянский титул.','campaignId':'FRANKS_TRANSITION','sourcePatch':'v8.2'},
 {'year':789,'label':'Admonitio generalis','detail':'Каролингский двор связывает церковную дисциплину, школы и исправление книг.','campaignId':'FRANKS_TRANSITION','sourcePatch':'v8.2'},
 {'year':800,'label':'Императорская коронация Карла Великого','detail':'Папа Лев III коронует франкского правителя в Риме.','campaignId':'FRANKS_TRANSITION','sourcePatch':'v8.2'},
 {'year':817,'label':'Ordinatio Imperii Людовика Благочестивого','detail':'План наследования пытается сохранить единство императорского титула.','campaignId':'FRANKS_TRANSITION','sourcePatch':'v8.2'},
 {'year':842,'label':'Страсбургские клятвы','detail':'Карл Лысый и Людовик Немецкий публично закрепляют союз против Лотаря.','campaignId':'FRANKS_TRANSITION','sourcePatch':'v8.2'},
 {'year':843,'label':'Верденский договор','detail':'Каролингские владения разделены между тремя наследниками без появления современных национальных границ.','campaignId':'FRANKS_TRANSITION','sourcePatch':'v8.2'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

# Image query groups.
p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "FRANKS_TRANSITION": {' not in s:
 marker='    "ABBASID_BAGHDAD": {';i=s.index(marker)
 group='''    "FRANKS_TRANSITION": {\n        "terms": ["Merovingian", "Carolingian", "Charlemagne", "Aachen", "Pepin", "Charles Martel", "Carolingian manuscript", "capitulary", "Treaty of Verdun", "Frankish coin"],\n        "base": [("ru", "Меровинги Каролинги Карл Великий"), ("en", "Merovingian Carolingian Charlemagne Aachen"), ("en", "Carolingian manuscript coin capitulary")],\n    },\n'''
 s=s[:i]+group+s[i:]
old='("/abbasid-baghdad/", "ABBASID_BAGHDAD"),'
if '("/franks-transition/", "FRANKS_TRANSITION")' not in s:
 if old not in s:raise SystemExit('image marker missing')
 s=s.replace(old,'("/franks-transition/", "FRANKS_TRANSITION"), '+old)
p.write_text(s,encoding='utf-8')

# Rebuild the image manifest from content registry.
entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg')
  entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

# Runtime versions and PWA.
for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v8.1.0','codex-v8.2.0').replace('codex-v8\\.1\\.0','codex-v8\\.2\\.0')
 if rel=='index.html':t=re.sub(r'js/bootstrap\.js\?v=[0-9.]+',f'js/bootstrap.js?v={V}',t)
 p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v8-2-franks-transition.js'" not in t:t=t.replace("'./js/features/v8-1-abbasid-baghdad.js'","'./js/features/v8-1-abbasid-baghdad.js','./js/features/v8-2-franks-transition.js'")
if "'./assets/packs/franks-transition-pack.svg'" not in t:t=t.replace("'./assets/packs/abbasid-baghdad-pack.svg'","'./assets/packs/abbasid-baghdad-pack.svg','./assets/packs/franks-transition-pack.svg'")
if "'./assets/eras/early-medieval.svg'" not in t:t=t.replace("'./assets/ui/fallback-card.svg',","'./assets/ui/fallback-card.svg','./assets/eras/early-medieval.svg',")
p.write_text(t,encoding='utf-8')

# Bring old test expectations to current totals/version.
for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'8\.1\.0',r'8\.2\.0').replace('5259','5391').replace('5217','5349').replace('2527','2593')
 p.write_text(t,encoding='utf-8')

# Documentation.
(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v8.2\n\n## v8.3 — Византия: от иконоборчества до Василия II\n\n- кризис VII–VIII веков и фемная система;\n- иконоборчество и борьба за религиозный образ;\n- Македонская династия, право и придворная культура;\n- миссии Кирилла и Мефодия;\n- войны с Болгарией и правление Василия II.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v8_2.md').write_text('''# Patch v8.2.0 — Франки: от Меровингов к Каролингам\n\n- 11 глав, 66 миссий и 132 карточки.\n- Меровингские разделы, королевы и дворы, майордомы и Пипиниды.\n- Карл Мартелл, Пипин Короткий, смена династии и союз с папством.\n- Карл Великий, войны, управление, Ахен, письменная реформа и коронация 800 года.\n- Людовик Благочестивый, Страсбургские клятвы и Верденский договор.\n- Эпоха VII расширена: в неё перенесён сравнительный мир около 700 года и добавлена франкская кампания.\n- Создана Эпоха VIII «Раннее Средневековье», куда перенесена кампания Аббасидов.\n''',encoding='utf-8')
(ROOT/'docs/QA_v8_2.md').write_text('''# QA v8.2.0\n\n- Проверены 88 сюжетных и 44 архивных карточки.\n- Проверены 66 миссий, 66 уроков, 11 глав, 11 пулов и 11 личных историй.\n- Проверены карта, четыре фазы, архивный пак и четыре модуля итогового экзамена.\n- Проверена реорганизация Эпох VII и VIII без дублирования кампаний.\n- Проверены межкампанийные связи с переселениями, ранним исламом, Аббасидами и Восточной Римской империей.\n- Проверены миграция сейва, коллекция, прямые кнопки этапов урока и PWA-кэш.\n''',encoding='utf-8')
p=ROOT/'README.md';s=p.read_text(encoding='utf-8');s=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',s,count=1,flags=re.M);block='''\n## v8.2.0 — Франки: от Меровингов к Каролингам\n\n- 11 глав, 66 миссий и 132 карточки.\n- Полная франкская линия от 511 до 843 года.\n- Эпоха VII расширена, а Аббасиды перенесены в новую Эпоху VIII «Раннее Средневековье».\n- Patch-only архив.\n\n'''
if '## v8.2.0' not in s:s=s.replace('\n',block,1)
p.write_text(s,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';s=p.read_text(encoding='utf-8');block='''\n\n## v8.2 — Франки: от Меровингов к Каролингам\n\nЛокальные SVG-обложки 132 карточек, кампанийного пака и обложка эпохи созданы для Codex of History. Источниковая рамка опирается на Encyclopaedia Britannica, UNESCO Aachen Cathedral, материалы Metropolitan Museum of Art и цифровые коллекции средневековых грамот, монет и рукописей.\n'''
if '## v8.2 —' not in s:s+=block
p.write_text(s,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test:v82']='node tools/smoke-v82-franks-transition.mjs && node tools/runtime-v82-franks-transition.mjs'
if 'tools/smoke-v82-franks-transition.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v82-franks-transition.mjs && node tools/runtime-v82-franks-transition.mjs'
dump(Path('package.json'),pkg)
print('integrated v8.2 Franks transition and reorganised eras VII–VIII')
