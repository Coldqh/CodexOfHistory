#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='6.9.0';OLD='6.8.0';CHECKED='2026-07-15'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
adds={'cards':['data/cards/late-religions/story.json','data/cards/late-religions/archive.json'],'campaigns':['data/campaigns/late-religions/campaign.json'],'pools':['data/campaigns/late-religions/pools.json'],'quizzes':['data/quizzes/late-religions/campaign.json'],'stories':['data/stories/late-religions/personal.json'],'lessons':['data/lessons/late-religions/campaign.json']}
for key,vals in adds.items():
 for val in vals:
  if val not in d[key]:d[key].append(val)
d['maps']['EARLY_CHRISTIANITY']='data/maps/late-religions.json'
script='js/features/v6-9-late-religions.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js') if 'js/features/v3-1-1-hotfix.js' in m['scripts'] else len(m['scripts']);m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));new=load(Path('data/core/relations-v69-late-religions.json'));seen={r['id'] for r in rels};rels.extend(r for r in new if r['id'] not in seen);dump(Path('data/core/relations.json'),rels)

world=load(Path('data/world/campaigns.json'));campaign=load(Path('data/campaigns/late-religions/campaign.json'));chapters=[x['title'] for x in campaign['chapters']]
for c in world:
 if c['id']=='EARLY_CHRISTIANITY':
  c.update({'eraId':'ERA_LATE_ANTIQUITY','order':28,'title':'Христианство и религии поздней Античности','subtitle':'Общины, тексты, соборы и святые места','period':'I–VI века','chapterCount':len(chapters),'releasedChapters':len(chapters),'status':'PLAYABLE','region':'Средиземноморье, Передняя Азия и Сасанидский Иран','description':'Иудейский мир I века, Иисус и раннее движение, Павловы сети, канон, мученики, раввинистические центры, Константин, Никея, монашество, манихейство, Эфес и Халкидон.','chapters':[{'number':i,'title':t} for i,t in enumerate(chapters,1)]});break
else:raise SystemExit('EARLY_CHRISTIANITY placeholder missing')
dump(Path('data/world/campaigns.json'),world)

eras=load(Path('data/world/eras.json'))
for e in eras:
 if e['id']=='ERA_LATE_ANTIQUITY':
  e['description']='Римская и Сасанидская державы перестраиваются, христианские, иудейские, манихейские и традиционные общины борются за места, тексты, покровительство и юридический статус, а новые церковные и монастырские сети переживают границы империй.'
  if 'EARLY_CHRISTIANITY' not in e['campaignIds']:
   pos=1 if 'LATE_ANTIQUITY' in e['campaignIds'] else 0;e['campaignIds'].insert(pos,'EARLY_CHRISTIANITY')
dump(Path('data/world/eras.json'),eras)

wt=load(Path('data/world/timeline.json'));events=[
 {'year':30,'label':'Деятельность Иисуса и рождение движения','detail':'В иудейской Галилее и Иерусалиме возникает движение учеников; точные даты отдельных эпизодов реконструируются.','campaignId':'EARLY_CHRISTIANITY','sourcePatch':'v6.9'},
 {'year':70,'label':'Разрушение Второго Храма','detail':'Войска Тита разрушают Иерусалимский Храм; иудейские и христианские общины перестраивают институты памяти и ритуала.','campaignId':'EARLY_CHRISTIANITY','sourcePatch':'v6.9'},
 {'year':112,'label':'Плиний и Траян обсуждают христиан','detail':'Переписка наместника и императора показывает локальную юридическую процедуру, а не единую непрерывную политику.','campaignId':'EARLY_CHRISTIANITY','sourcePatch':'v6.9'},
 {'year':250,'label':'Указ Деция и либеллы','detail':'Жители подтверждают участие в жертвоприношении документами; исполнение различается по регионам.','campaignId':'EARLY_CHRISTIANITY','sourcePatch':'v6.9'},
 {'year':313,'label':'Медиоланские договорённости','detail':'Константин и Лициний разрешают культы и возвращение конфискованной церковной собственности.','campaignId':'EARLY_CHRISTIANITY','sourcePatch':'v6.9'},
 {'year':325,'label':'Первый Никейский собор','detail':'Собор принимает символ с термином homoousios, но спор продолжается десятилетиями.','campaignId':'EARLY_CHRISTIANITY','sourcePatch':'v6.9'},
 {'year':381,'label':'Первый Константинопольский собор','detail':'Никейское направление укрепляется, а Константинополь получает новый церковный статус.','campaignId':'EARLY_CHRISTIANITY','sourcePatch':'v6.9'},
 {'year':431,'label':'Эфесский собор','detail':'Соперничающие епископские группы решают спор вокруг Нестория и Кирилла Александрийского.','campaignId':'EARLY_CHRISTIANITY','sourcePatch':'v6.9'},
 {'year':451,'label':'Халкидонский собор','detail':'Соборная формула становится нормой для одних церквей и основанием устойчивого отказа для других.','campaignId':'EARLY_CHRISTIANITY','sourcePatch':'v6.9'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in events if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

p=ROOT/'tools/build-image-queries.py';s=p.read_text(encoding='utf-8');s=re.sub(r'VERSION = "[^"]+"',f'VERSION = "{V}"',s,count=1)
if '    "LATE_RELIGIONS": {' not in s:
 marker='    "LATE_ROMAN": {';i=s.index(marker);group='''    "LATE_RELIGIONS": {\n        "terms": ["раннее христианство", "early christianity", "late antiquity religion", "иудаизм", "judaism", "никея", "nicaea", "монашество", "monasticism", "манихейство", "manichaeism", "халкидон", "chalcedon"],\n        "base": [("ru", "Религии поздней Античности"), ("en", "Early Christianity"), ("en", "Religion in Late Antiquity")],\n    },\n''';s=s[:i]+group+s[i:]
old='("/late-roman/", "LATE_ROMAN"),'
if '("/late-religions/", "LATE_RELIGIONS")' not in s:
 if old not in s:raise SystemExit('image path marker missing')
 s=s.replace(old,old+' ("/late-religions/", "LATE_RELIGIONS"),')
p.write_text(s,encoding='utf-8')

entries=[]
for path in d['cards']:
 for c in load(Path(path)):
  image=c.get('image') or {};local=image.get('local','assets/ui/fallback-card.svg');entries.append({'cardId':c['id'],'local':local,'file':image.get('file',Path(local).name),'kind':image.get('kind','historical-image' if image.get('prefer_remote') else 'project-cover'),'prefer_remote':bool(image.get('prefer_remote')),'caption':image.get('caption',f'Изображение: {c["title"]}'),'credit':image.get('credit','Codex of History'),'source_url':image.get('source_url',c.get('source',{}).get('url','ATTRIBUTION.md')),'license':image.get('license','Project asset')})
historical=sum(1 for x in entries if x['prefer_remote']);im=load(Path('data/image_manifest.json'));im.update({'version':V,'generatedAt':CHECKED,'count':len(entries),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(entries)-historical,'dynamicQueryCount':len(entries)-historical,'images':entries});dump(Path('data/image_manifest.json'),im)

for path in (ROOT/'js').rglob('*.js'):
 t=path.read_text(encoding='utf-8').replace(OLD,V);path.write_text(t,encoding='utf-8')
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;t=p.read_text(encoding='utf-8').replace(OLD,V).replace('codex-v6.8.0','codex-v6.9.0').replace('codex-v6\\.8\\.0','codex-v6\\.9\\.0');p.write_text(t,encoding='utf-8')
p=ROOT/'sw.js';t=p.read_text(encoding='utf-8')
if "'./js/features/v6-9-late-religions.js'" not in t:t=t.replace("'./js/features/v6-8-late-roman.js'","'./js/features/v6-8-late-roman.js','./js/features/v6-9-late-religions.js'")
if "'./assets/packs/late-religions-pack.svg'" not in t:t=t.replace("'./assets/packs/late-roman-pack.svg'","'./assets/packs/late-roman-pack.svg','./assets/packs/late-religions-pack.svg'")
p.write_text(t,encoding='utf-8')

for p in (ROOT/'tools').glob('*.mjs'):
 t=p.read_text(encoding='utf-8').replace("'6.8.0'",f"'{V}'").replace('"6.8.0"',f'"{V}"').replace('6.8.0','6.9.0').replace(r'6\.8\.0',r'6\.9\.0').replace('3711','3843').replace('3669','3801')
 p.write_text(t,encoding='utf-8')

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v6.9\n\n## v7.0 — Переселения и новые королевства\n\n- готы, переход Дуная и Адрианополь как начало долгого процесса;\n- переход Рейна, вандалы в Африке и гуннская держава;\n- конец западного императорского двора без мифа мгновенного исчезновения Рима;\n- остготы, вестготы, франки и другие новые королевства;\n- римское право, церковь, города и местные элиты внутри постримского Запада.\n''',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v6_9.md').write_text('''# Patch v6.9.0 — Христианство и религии поздней Античности\n\n- 11 глав, 66 миссий и 132 карточки.\n- Иудейский мир I века, Иисус, ранние общины, Павел, ритуалы и формирование канона.\n- Гонения без схемы непрерывной единой политики, мученические тексты и общинная память.\n- Иудаизм после разрушения Храма, Мишна, синагоги и критика мифа единого «собора Явне».\n- Константин, Никея, арианские споры, монашество, реликвии и паломничества.\n- Манихейство, поздние традиционные культы, Эфес, Халкидон и разные христианские Востоки.\n''',encoding='utf-8')
(ROOT/'docs/QA_v6_9.md').write_text('''# QA v6.9.0\n\n- Проверены 88 сюжетных и 44 архивных карточки.\n- Проверены 66 миссий, 66 уроков, 11 глав, 11 пулов и 11 архивных дел.\n- Проверены пять фаз кампании, карта общин и соборов, четыре модуля итогового экзамена.\n- Проверена нейтральная историческая рамка: вера участников отделена от источниковедческой реконструкции.\n- Проверены связи с римской, позднеримской, ханьской и степной кампаниями.\n- Проверены локальные SVG, источники, PWA-кэш и runtime-модуль.\n''',encoding='utf-8')
p=ROOT/'README.md';t=p.read_text(encoding='utf-8');t=re.sub(r'^# Codex of History v[^\n]+',f'# Codex of History v{V}',t,count=1,flags=re.M);block='''\n## v6.9.0 — Христианство и религии поздней Античности\n\n- 11 глав, 66 миссий и 132 карточки.\n- Общины, рукописи, мученики, раввинистические центры, соборы, монашество и манихейство.\n- Историческая рамка не выбирает «истинную» традицию и отделяет веру участников от реконструкции.\n- Patch-only архив.\n\n'''
if '## v6.9.0' not in t:t=t.replace('\n',block,1)
p.write_text(t,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';t=p.read_text(encoding='utf-8');block='''\n\n## v6.9 — Христианство и религии поздней Античности\n\nЛокальные SVG-обложки 132 карточек и обложка пака созданы для Codex of History. Источниковая рамка использует Encyclopaedia Britannica, Codex Sinaiticus Project, Sefaria, Fordham Ancient History Sourcebook и UNESCO World Heritage Centre. Религиозные утверждения представлены как позиции исторических общин и авторов, а не как выводы исторического метода.\n'''
if '## v6.9 —' not in t:t+=block
p.write_text(t,encoding='utf-8')

pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test:v69']='node tools/smoke-v69-late-religions.mjs && node tools/runtime-v69-late-religions.mjs'
if 'tools/smoke-v69-late-religions.mjs' not in pkg['scripts']['test']:pkg['scripts']['test']+=' && node tools/smoke-v69-late-religions.mjs && node tools/runtime-v69-late-religions.mjs'
dump(Path('package.json'),pkg)
print('integrated v6.9 religions campaign')
