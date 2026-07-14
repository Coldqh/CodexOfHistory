#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];V='4.5.0'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for key,vals in [('cards',['data/cards/vedic-india/story.json','data/cards/vedic-india/archive.json']),('pools',['data/campaigns/vedic-india/pools.json']),('quizzes',['data/quizzes/vedic-india/campaign.json']),('stories',['data/stories/vedic-india/personal.json']),('lessons',['data/lessons/vedic-india/campaign.json']),('campaigns',['data/campaigns/vedic-india/campaign.json'])]:
 for x in vals:
  if x not in d[key]:d[key].append(x)
d['maps']['INDIA_VEDIC']='data/maps/vedic-india.json';script='js/features/v4-5-vedic-india.js'
if script not in m['scripts']:m['scripts'].insert(m['scripts'].index('js/features/v3-1-1-hotfix.js'),script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));add=load(Path('data/core/relations-v45-vedic-india.json'));known={x['id'] for x in rels};rels.extend(x for x in add if x['id'] not in known);dump(Path('data/core/relations.json'),rels);(ROOT/'data/core/relations-v45-vedic-india.json').unlink(missing_ok=True)
world=load(Path('data/world/campaigns.json'));camp=load(Path('data/campaigns/vedic-india/campaign.json'))
for c in world:
 if c['id']=='INDIA_VEDIC':c.update({'title':'Ведийская Индия и ранние государства','subtitle':'Гимны, ритуал и долина Ганга','period':'ок. 1500–500 до н. э.','chapterCount':10,'releasedChapters':10,'status':'PLAYABLE','region':'Северо-западная и Северная Индия','description':'От ранних гимнов и Сапта-Синдху до Куру-Панчалы, поздних Вед, джанапад и начала второй урбанизации.','chapters':[{'number':x['number'],'title':x['title']} for x in camp['chapters']]})
dump(Path('data/world/campaigns.json'),world)

wt=load(Path('data/world/timeline.json'));new=[
{'year':-1500,'label':'Ранний ведийский мир северо-запада','detail':'Условная граница ранних слоёв ригведийской традиции.','campaignId':'INDIA_VEDIC','sourcePatch':'v4.5'},
{'year':-1200,'label':'Рост поздневедийских центров в Доабе','detail':'Куру-Панчала и распространение расписной серой керамики.','campaignId':'INDIA_VEDIC','sourcePatch':'v4.5'},
{'year':-1000,'label':'Усложнение ведийского ритуального корпуса','detail':'Самаведа, Яджурведа и ранние брахманы формируют специализированные традиции.','campaignId':'INDIA_VEDIC','sourcePatch':'v4.5'},
{'year':-900,'label':'Расширение железных технологий в Северной Индии','detail':'Рост поселений, земледелия и ремесла в Ганга-Ямунском Доабе.','campaignId':'INDIA_VEDIC','sourcePatch':'v4.5'},
{'year':-800,'label':'Поздние брахманы и араньяки','detail':'Ритуальное толкование переходит к новым вопросам о знании и космосе.','campaignId':'INDIA_VEDIC','sourcePatch':'v4.5'},
{'year':-700,'label':'Рост городских центров долины Ганга','detail':'Каушамби, Раджагриха и другие центры входят в период второй урбанизации.','campaignId':'INDIA_VEDIC','sourcePatch':'v4.5'},
{'year':-650,'label':'Ранние упанишады','detail':'Тексты Видехи и Куру-Панчалы обсуждают атман, брахман и знание.','campaignId':'INDIA_VEDIC','sourcePatch':'v4.5'},
{'year':-600,'label':'Оформление джанапад и крупных царств','detail':'Кошала, Ватса, Аванти и Магадха усиливаются в Северной Индии.','campaignId':'INDIA_VEDIC','sourcePatch':'v4.5'},
{'year':-550,'label':'Махаджанапады и шраманские движения','detail':'Политическая и интеллектуальная среда выходит за пределы классической ведийской эпохи.','campaignId':'INDIA_VEDIC','sourcePatch':'v4.5'},
{'year':-500,'label':'Переход к раннеисторической Северной Индии','detail':'Города, монета, государства и новые религиозные движения создают новый этап.','campaignId':'INDIA_VEDIC','sourcePatch':'v4.5'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt};wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)
packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)
im=load(Path('data/image_manifest.json'));existing={x['cardId']:x for x in im.get('images',[])}
for c in load(Path('data/cards/vedic-india/story.json'))+load(Path('data/cards/vedic-india/archive.json')):existing[c['id']]={'cardId':c['id'],'local':c['image']['local'],'file':c['image']['file'],'kind':'project-cover','prefer_remote':False,'caption':c['image']['caption'],'credit':c['image']['credit'],'source_url':c['image']['source_url'],'license':c['image']['license']}
images=list(existing.values());historical=sum(1 for x in images if x.get('prefer_remote'));im.update({'version':V,'generatedAt':'2026-07-14','count':len(images),'historicalImageCount':historical,'staticHistoricalImageCount':historical,'projectCoverCount':len(images)-historical,'dynamicQueryCount':len(images)-historical,'images':images});dump(Path('data/image_manifest.json'),im)
(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('# Следующий этап после v4.5\n\n## v4.6 — Железный век: общий сравнительный слой\n\n- Ассирия, Финикия, Левант, Греция, Чжоу и Северная Индия на одной шкале;\n- глобальная карта и параллельная хронология;\n- сравнение письма, государства, войны, религии и урбанизации;\n- итоговый экзамен эпохи.\n',encoding='utf-8')
(ROOT/'docs/PATCH_NOTES_v4_5.md').write_text('# Patch v4.5.0 — Ведийская Индия и ранние государства\n\n- 10 глав, 60 миссий и 120 карточек.\n- Ригведа, устная передача, хозяйство, ритуал, Куру-Панчала, поздние Веды, варны, джанапады и махаджанапады.\n- 10 пулов, 10 личных историй, карта и отдельный пак.\n',encoding='utf-8')
(ROOT/'docs/QA_v4_5.md').write_text('# QA v4.5.0\n\n- 120 карточек, 60 миссий, 14 квизов;\n- старт только с VED_S_01_01–03;\n- пак выдаёт только VED_A_*;\n- карта, четыре фазы и итоговый экзамен;\n- версии, изображения и runtime-модули.\n',encoding='utf-8')
p=ROOT/'README.md';txt=p.read_text(encoding='utf-8');txt=re.sub(r'^# Codex of History v[^\n]+','# Codex of History v4.5.0',txt,count=1,flags=re.M);sec='\n## v4.5.0 — Ведийская Индия и ранние государства\n\n- 10 глав, 60 миссий и 120 карточек.\n- Ригведа, устная традиция, ритуал, общество, Куру-Панчала и ранние государства.\n- Patch-only архив.\n\n';txt=txt if '## v4.5.0' in txt else txt.replace('\n',sec,1);p.write_text(txt,encoding='utf-8')
p=ROOT/'ATTRIBUTION.md';txt=p.read_text(encoding='utf-8');sec='\n## v4.5 — Ведийская Индия и ранние государства\n\nЛокальные SVG-обложки 120 карточек и обложка пака созданы для Codex of History. Источники: Metropolitan Museum of Art, Smarthistory и Vedic Heritage Portal.\n';p.write_text(txt if '## v4.5 —' in txt else txt+sec,encoding='utf-8')
for path in (ROOT/'js').rglob('*.js'):path.write_text(path.read_text(encoding='utf-8').replace('4.4.0',V),encoding='utf-8')
for path in (ROOT/'tools').glob('*.mjs'):path.write_text(path.read_text(encoding='utf-8').replace('4.4.0',V).replace('2195','2315').replace('2153','2273'),encoding='utf-8')
pkg=load(Path('package.json'));pkg['version']=V;pkg['scripts']['test']+=' && node tools/smoke-v45-vedic-india.mjs && node tools/runtime-v45-vedic-india.mjs' if 'smoke-v45-vedic-india.mjs' not in pkg['scripts']['test'] else '';pkg['scripts']['test:v45']='node tools/smoke-v45-vedic-india.mjs && node tools/runtime-v45-vedic-india.mjs';dump(Path('package.json'),pkg)
for rel in ['index.html','manifest.webmanifest','js/bootstrap.js','sw.js']:
 p=ROOT/rel;p.write_text(p.read_text(encoding='utf-8').replace('4.4.0',V).replace('codex-v4.4.0','codex-v4.5.0'),encoding='utf-8')
p=ROOT/'sw.js';txt=p.read_text(encoding='utf-8');txt=txt.replace("'./assets/packs/zhou-warring-pack.svg',","'./assets/packs/zhou-warring-pack.svg','./assets/packs/vedic-india-pack.svg',").replace("'./js/features/v4-4-zhou-warring.js',","'./js/features/v4-4-zhou-warring.js','./js/features/v4-5-vedic-india.js',");p.write_text(txt,encoding='utf-8')
print('integrated v4.5')
