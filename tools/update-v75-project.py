#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='7.5.0';OLD='7.4.0';CHECKED='2026-07-16'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={'cards':['data/cards/china-post-han/story.json','data/cards/china-post-han/archive.json'],'campaigns':['data/campaigns/china-post-han/campaign.json'],'pools':['data/campaigns/china-post-han/pools.json'],'quizzes':['data/quizzes/china-post-han/campaign.json'],'stories':['data/stories/china-post-han/personal.json'],'lessons':['data/lessons/china-post-han/campaign.json']}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['CHINA_POST_HAN']='data/maps/china-post-han.json'
script='js/features/v7-5-china-post-han.js'
if script not in m['scripts']:
 marker='js/features/v6-9-1-stability.js';idx=m['scripts'].index(marker) if marker in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));rels=[r for r in rels if not re.fullmatch(r'REL_CHN_\d{4}',r.get('id',''))];new=load(Path('data/core/relations-v75-china-post-han.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/china-post-han/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
entry={'id':'CHINA_POST_HAN','eraId':'ERA_LATE_ANTIQUITY','order':33,'title':'Китай между Хань и Тан','subtitle':'Раздробленность, буддизм и новое объединение','period':'220–649 годы','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Китай и Восточная Азия','description':'Троецарствие, Западная и Восточная Цзинь, Шестнадцать государств, Северная Вэй, буддизм, Северные и Южные династии, объединение Суй и возникновение Тан.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]}
world=[c for c in world if c['id']!='CHINA_POST_HAN'];world.append(entry)
order_map={'LATE_ANTIQUITY':26,'EARLY_CHRISTIANITY':27,'MIGRATION_KINGDOMS':28,'EASTERN_ROMAN':29,'SASANIAN':30,'CENTRAL_ASIA_LATE':31,'GUPTA':32,'CHINA_POST_HAN':33,'ISLAMIC_ORIGINS':34}
for c in world:
 if c['id'] in order_map:c['order']=order_map[c['id']]
world.sort(key=lambda x:x.get('order',999));dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_LATE_ANTIQUITY':
  e['dateLabel']='II век до н. э. – VIII век н. э.';e['startYear']=-200;e['endYear']=750
  e['description']='Поздняя Античность связывает Рим, Сасанидов, новые западные королевства, Центральную Азию, Индию и Китай между Хань и Тан через войны, религиозные сети, миграции, торговлю и новые государственные системы.'
  ids=['LATE_ANTIQUITY','EARLY_CHRISTIANITY','MIGRATION_KINGDOMS','EASTERN_ROMAN','SASANIAN','CENTRAL_ASIA_LATE','GUPTA','CHINA_POST_HAN']
  e['campaignIds']=ids
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'));events=[
 {'year':220,'label':'Оформление государства Цао Вэй','detail':'Формальный конец Хань открывает период Троецарствия.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':280,'label':'Западная Цзинь покоряет Восточное У','detail':'Китай кратко объединяется под домом Сыма.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':291,'label':'Начинается война восьми князей','detail':'Борьба регентов разрушает столичное управление Западной Цзинь.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':311,'label':'Падение Лояна','detail':'Армии Хань-Чжао захватывают северную столицу.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':317,'label':'Основание Восточной Цзинь','detail':'Двор Сыма закрепляется в Цзянькане на Янцзы.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':383,'label':'Битва на реке Фэй','detail':'Южная армия останавливает попытку Ранней Цинь объединить Китай.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':386,'label':'Основание Северной Вэй','detail':'Тоба Гуй восстанавливает государство тоба.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':439,'label':'Северная Вэй объединяет север','detail':'Покорение Северной Лян завершает крупный цикл завоеваний.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':460,'label':'Начало главного строительства Юньгана','detail':'Императорское покровительство создаёт крупнейший пещерный комплекс.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':485,'label':'Введение системы равных полей','detail':'Северная Вэй связывает земельный учёт и налоговые повинности.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':494,'label':'Северная Вэй переносит столицу в Лоян','detail':'Двор перестраивает столичную и аристократическую систему.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':523,'label':'Восстание шести гарнизонов','detail':'Кризис пограничной армии разрушает позднюю Северную Вэй.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':534,'label':'Раздел Северной Вэй','detail':'Возникают Восточная и Западная Вэй.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':581,'label':'Основание династии Суй','detail':'Ян Цзянь захватывает власть у Северной Чжоу.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':589,'label':'Суй объединяет Китай','detail':'Покорение Чэнь завершает длительное политическое разделение.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':605,'label':'Расширение Великого канала','detail':'Транспортная система связывает северные столицы и зерновой юг.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':618,'label':'Основание династии Тан','detail':'Ли Юань провозглашает новую династию в Чанъане.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':626,'label':'Инцидент у ворот Сюаньу','detail':'Ли Шимин получает контроль над наследованием и становится Тай-цзуном.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'},
 {'year':645,'label':'Сюаньцзан возвращается в Чанъань','detail':'Паломник привозит тексты из Индии через Центральную Азию.','campaignId':'CHINA_POST_HAN','sourcePatch':'v7.5'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "CHINA_POST_HAN": {' not in s:
 marker='    "INDIA_GUPTA": {';i=s.index(marker);group='''    "CHINA_POST_HAN": {\n        "terms": ["Three Kingdoms China", "Western Jin", "Northern Wei", "Yungang", "Longmen", "Six Dynasties", "Sui dynasty", "early Tang", "Chang'an"],\n        "base": [("ru", "Китай между Хань и Тан"), ("en", "China Six Dynasties Northern Wei Sui Tang"), ("en", "Three Kingdoms Northern Wei Buddhist art")],\n    },\n''';s=s[:i]+group+s[i:]
old='("/india-gupta/", "INDIA_GUPTA"),'
if '("/china-post-han/", "CHINA_POST_HAN")' not in s:
 if old not in s:raise SystemExit('image path marker missing')
 s=s.replace(old,'("/china-post-han/", "CHINA_POST_HAN"), '+old)
p.write_text(s,encoding='utf-8')

entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg');entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v7.4.0','codex-v7.5.0').replace('codex-v7\\.4\\.0','codex-v7\\.5\\.0');p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v7-5-china-post-han.js'" not in t:t=t.replace("'./js/features/v7-4-india-gupta.js'","'./js/features/v7-4-india-gupta.js','./js/features/v7-5-china-post-han.js'")
if "'./assets/packs/china-post-han-pack.svg'" not in t:t=t.replace("'./assets/packs/india-gupta-pack.svg'","'./assets/packs/india-gupta-pack.svg','./assets/packs/china-post-han-pack.svg'")
p.write_text(t,encoding='utf-8')

for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace(OLD,V).replace(r'7\.4\.0',r'7\.5\.0').replace('4503','4635').replace('4461','4593').replace('2149','2215')
 p.write_text(t,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V
newtests='node tools/smoke-v75-china-post-han.mjs && node tools/runtime-v75-china-post-han.mjs'
if newtests not in pkg['scripts']['test']:pkg['scripts']['test']+=' && '+newtests
pkg['scripts']['test:v75']=newtests;dump(Path('package.json'),pkg)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v7.5\n\n## v7.6 — Аксум, Нубия и Южная Аравия\n\n- Аксум и порт Адулис;\n- Эзана, монеты и принятие христианства;\n- поздний Мероэ и нубийские царства;\n- Химьяр, иудаизм и христианство Южной Аравии;\n- Красное море перед возникновением ислама.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v7_5.md').write_text('''# Patch v7.5.0 — Китай между Хань и Тан\n\n- 11 глав, 66 миссий и 132 карточки.\n- Троецарствие, Западная Цзинь, война восьми князей и Шестнадцать государств.\n- Восточная Цзинь, Северная Вэй, Юньган, Лунмэнь и реформы Сяовэня.\n- Северные и Южные династии, гарнизонные восстания и новые военные системы.\n- Объединение Суй, Великий канал и возникновение Тан.\n''',encoding='utf-8')
(ROOT/'docs/QA_v7_5.md').write_text('''# QA v7.5.0\n\n- `npm test` проверяет старые кампании и новые smoke/runtime-модули.\n- Отдельно проверяются 132 карточки, 66 миссий, 15 квизов, карта, пак, экзамен и межкампанийные связи.\n- Стабильность сохранения и ленивой коллекции остаётся под тестом v6.9.1.\n''',encoding='utf-8')

attr=ROOT/'ATTRIBUTION.md';txt=attr.read_text(encoding='utf-8');block='''\n\n## v7.5 — Китай между Хань и Тан\n\nЛокальные SVG-обложки 132 карточек и обложка пака созданы для Codex of History. Учебная основа: UNESCO Yungang и Longmen, Metropolitan Museum of Art, British Museum, Smithsonian National Museum of Asian Art, International Dunhuang Programme, Chinese Text Project и исследования по Троецарствию, Северной Вэй, династиям Суй и ранней Тан.\n'''
if '## v7.5 — Китай между Хань и Тан' not in txt:attr.write_text(txt.rstrip()+block,encoding='utf-8')
readme=ROOT/'README.md';txt=readme.read_text(encoding='utf-8')
if '## v7.5.0 — Китай между Хань и Тан' not in txt:readme.write_text(txt.rstrip()+'''\n\n## v7.5.0 — Китай между Хань и Тан\n\nНовая кампания из 11 глав соединяет падение Хань, Троецарствие, кризис Цзинь, северные и южные династии, буддийские сети, реформы Северной Вэй, объединение Суй и возникновение ранней Тан.\n''',encoding='utf-8')
print('updated project to',V)
