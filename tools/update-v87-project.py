#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='8.7.0';OLD='8.6.0';CHECKED='2026-07-16'

def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={
 'cards':['data/cards/tang-song/story.json','data/cards/tang-song/archive.json'],
 'campaigns':['data/campaigns/tang-song/campaign.json'],
 'pools':['data/campaigns/tang-song/pools.json'],
 'quizzes':['data/quizzes/tang-song/campaign.json'],
 'stories':['data/stories/tang-song/personal.json'],
 'lessons':['data/lessons/tang-song/campaign.json'],
}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['TANG_SONG']='data/maps/tang-song.json'
script='js/features/v8-7-tang-song.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));rels=[r for r in rels if not re.fullmatch(r'REL_TSG_\d{4}',r.get('id',''))]
new=load(Path('data/core/relations-870-tang-song.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/tang-song/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
entry={'id':'TANG_SONG','eraId':'ERA_EARLY_MEDIEVAL','order':44,'title':'Китай: от Тан к Сун','subtitle':'Имперские столицы, кризис Тан и новое объединение','period':'649–1067 годы','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Китай, Внутренняя Азия и морские пути','description':'У Цзэтянь, экзамены, Чанъань и Лоян, буддизм, фронтиры, восстание Ань Лушаня, поздняя Тан, Пять династий, основание Сун, города, печать, бумажные деньги и торговля.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]}
world=[c for c in world if c['id']!='TANG_SONG'];world.append(entry);world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)
eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_EARLY_MEDIEVAL':
  ids=[x for x in e.get('campaignIds',[]) if x!='TANG_SONG'];e['campaignIds']=ids+['TANG_SONG'];e['status']='PLAYABLE'
  e['description']='Аббасидский Багдад, Византия, викингские сети, славяноязычные державы, исламский Запад и Китай от Тан к Сун показывают раннее Средневековье как систему империй, королевств, городов, морских путей и новых письменных культур VIII–XI веков.'
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'));events=[
 {'year':657,'label':'Тан разбивает Западно-Тюркский каганат','detail':'Победа расширяет систему протекторатов, но не создаёт одинакового контроля над всеми оазисами.','campaignId':'TANG_SONG','sourcePatch':'v8.7'},
 {'year':690,'label':'У Цзэтянь провозглашает династию Чжоу','detail':'Правительница принимает императорский титул и переносит центр легитимности в Лоян.','campaignId':'TANG_SONG','sourcePatch':'v8.7'},
 {'year':751,'label':'Битва при Таласе','detail':'Танские, аббасидские и местные силы сталкиваются в Центральной Азии.','campaignId':'TANG_SONG','sourcePatch':'v8.7'},
 {'year':755,'label':'Начинается восстание Ань Лушаня','detail':'Пограничная армия превращается в гражданскую войну за столицы и престол.','campaignId':'TANG_SONG','sourcePatch':'v8.7'},
 {'year':780,'label':'Тан вводит двухразовый налог','detail':'Новая система отвечает на распад старых земельных и податных реестров.','campaignId':'TANG_SONG','sourcePatch':'v8.7'},
 {'year':845,'label':'Антимонастырская кампания У-цзуна','detail':'Закрытие монастырей соединяет религиозную политику и конфискацию ресурсов.','campaignId':'TANG_SONG','sourcePatch':'v8.7'},
 {'year':868,'label':'Создан датированный печатный свиток Алмазной сутры','detail':'Дуньхуанский памятник показывает зрелость ксилографии в IX веке.','campaignId':'TANG_SONG','sourcePatch':'v8.7'},
 {'year':907,'label':'Династия Тан прекращает существование','detail':'Чжу Вэнь основывает Позднюю Лян, а Китай входит в период нескольких государств.','campaignId':'TANG_SONG','sourcePatch':'v8.7'},
 {'year':936,'label':'Шестнадцать округов переданы киданям','detail':'Северная граница будущей Сун формируется в отношениях с империей Ляо.','campaignId':'TANG_SONG','sourcePatch':'v8.7'},
 {'year':960,'label':'Основана династия Сун','detail':'Чжао Куанъинь начинает объединение и ограничение власти военных командиров.','campaignId':'TANG_SONG','sourcePatch':'v8.7'},
 {'year':1005,'label':'Шаньюаньский договор Сун и Ляо','detail':'Две державы закрепляют устойчивую границу и обмен ежегодными дарами.','campaignId':'TANG_SONG','sourcePatch':'v8.7'},
 {'year':1044,'label':'Военный трактат фиксирует пороховые формулы','detail':'Техническое описание показывает раннее военное применение смесей без мгновенной революции.','campaignId':'TANG_SONG','sourcePatch':'v8.7'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "TANG_SONG": {' not in s:
 marker='    "AL_ANDALUS_WEST": {';i=s.index(marker)
 group='''    "TANG_SONG": {\n        "terms": ["Tang dynasty Chang'an", "Wu Zetian Longmen", "An Lushan rebellion", "Dunhuang Diamond Sutra", "Tang sancai camel", "Five Dynasties China", "Northern Song Kaifeng", "Song dynasty printing", "jiaozi paper money", "Song ceramics"],\n        "base": [("ru", "Тан Сун Чанъань Лоян раннее Средневековье"), ("en", "Tang Song China Chang'an Kaifeng archaeology"), ("en", "Tang dynasty Song dynasty printing trade Buddhist art")],\n    },\n'''
 s=s[:i]+group+s[i:]
old='("/al-andalus-west/", "AL_ANDALUS_WEST"),'
if '("/tang-song/", "TANG_SONG")' not in s:
 if old not in s:raise SystemExit('image marker missing')
 s=s.replace(old,'("/tang-song/", "TANG_SONG"), '+old)
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
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v8.6.0','codex-v8.7.0').replace('codex-v8\\.6\\.0','codex-v8\\.7\\.0')
 if rel=='index.html':t=re.sub(r'js/bootstrap\.js\?v=[0-9.]+',f'js/bootstrap.js?v={V}',t)
 p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v8-7-tang-song.js'" not in t:t=t.replace("'./js/features/v8-6-al-andalus-west.js'","'./js/features/v8-6-al-andalus-west.js','./js/features/v8-7-tang-song.js'")
if "'./assets/packs/tang-song-pack.svg'" not in t:t=t.replace("'./assets/packs/al-andalus-west-pack.svg'","'./assets/packs/al-andalus-west-pack.svg','./assets/packs/tang-song-pack.svg'")
p.write_text(t,encoding='utf-8')

for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'8\.6\.0',r'8\.7\.0').replace('5931','6063').replace('5889','6021').replace('2863','2929')
 p.write_text(t,encoding='utf-8')

p=ROOT/'tools/smoke-v82-franks-transition.mjs';t=p.read_text(encoding='utf-8');t=t.replace("['ABBASID_BAGHDAD','BYZANTIUM_MACEDONIAN','VIKINGS_NORTH_ATLANTIC','SLAVIC_BULGARIA_RUS','AL_ANDALUS_WEST']","['ABBASID_BAGHDAD','BYZANTIUM_MACEDONIAN','VIKINGS_NORTH_ATLANTIC','SLAVIC_BULGARIA_RUS','AL_ANDALUS_WEST','TANG_SONG']");p.write_text(t,encoding='utf-8')

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v8.7\n\n## v8.8 — Индия и Индийский океан\n\n- Палы, Гурджара-Пратихары и Раштракуты;\n- Чолы и морские походы;\n- Наланда, храмовые центры и санскритская культура;\n- порты, купеческие корпорации и связи с Юго-Восточной Азией;\n- региональные государства без мифа о единой «классической Индии».\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v8_7.md').write_text('''# Patch v8.7.0 — Китай: от Тан к Сун\n\n- 11 глав, 66 миссий и 132 карточки.\n- У Цзэтянь, столицы, чиновники, экзамены и религиозные сети Тан.\n- Фронтиры, восстание Ань Лушаня, позднетанские налоги и региональные армии.\n- Пять династий, основание Сун, Кайфэн, печать, бумажные деньги и торговля.\n''',encoding='utf-8')
(ROOT/'docs/QA_v8_7.md').write_text('''# QA v8.7.0\n\n- Проверены 88 сюжетных и 44 архивных карточки.\n- Проверены 66 миссий, 66 уроков, 11 глав, 11 пулов и 11 личных историй.\n- Проверены карта, четыре фазы, архивный пак и четыре модуля итогового экзамена.\n- Проверены уникальность ID и названий во всём проекте.\n- Проверены связи с постханьским Китаем, Центральной Азией, Аббасидами, викингскими и андалусскими сетями.\n- Проверены миграция сейва, коллекция, прямые кнопки этапов урока и PWA-кэш.\n''',encoding='utf-8')
p=ROOT/'README.md';s=p.read_text(encoding='utf-8');s=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',s,count=1,flags=re.M);block='''\n## v8.7.0 — Китай: от Тан к Сун\n\n- 11 глав, 66 миссий и 132 карточки.\n- Танские столицы, кризис VIII–IX веков, Пять династий и ранняя Сун.\n- Patch-only архив.\n\n'''
if '## v8.7.0' not in s:s=s.replace('\n',block,1)
p.write_text(s,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';s=p.read_text(encoding='utf-8');block='''\n\n## v8.7 — Китай: от Тан к Сун\n\nЛокальные SVG-обложки 132 карточек и кампанийного пака созданы для Codex of History. Источниковая рамка опирается на Metropolitan Museum of Art, UNESCO Longmen Grottoes, UNESCO Mogao Caves, UNESCO Silk Roads: Chang’an–Tianshan Corridor, UNESCO Grand Canal и International Dunhuang Project.\n'''
if '## v8.7 —' not in s:s+=block
p.write_text(s,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test:v87']='node tools/smoke-v87-tang-song.mjs && node tools/runtime-v87-tang-song.mjs'
if 'tools/smoke-v87-tang-song.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v87-tang-song.mjs && node tools/runtime-v87-tang-song.mjs'
dump(Path('package.json'),pkg)
print('integrated v8.7 Tang-to-Song campaign')
