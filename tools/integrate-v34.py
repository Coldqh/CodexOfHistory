#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='3.4.0'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for key,val in [
 ('cards',['data/cards/aegean/story.json','data/cards/aegean/archive.json']),
 ('pools',['data/campaigns/aegean/pools.json']),('quizzes',['data/quizzes/aegean/campaign.json']),
 ('stories',['data/stories/aegean/personal.json']),('lessons',['data/lessons/aegean/campaign.json']),
 ('campaigns',['data/campaigns/aegean/campaign.json'])]:
 for x in val:
  if x not in d[key]:d[key].append(x)
d['maps']['AEGEAN_BRONZE']='data/maps/aegean.json'
script='js/features/v3-4-aegean.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js')
 m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

rels=load(Path('data/core/relations.json'));add=load(Path('data/core/relations-v34-aegean.json'))
existing={x['id'] for x in rels};rels.extend(x for x in add if x['id'] not in existing);dump(Path('data/core/relations.json'),rels)
(ROOT/'data/core/relations-v34-aegean.json').unlink(missing_ok=True)

world=load(Path('data/world/campaigns.json'));chapters=load(Path('data/campaigns/aegean/campaign.json'))['chapters']
for c in world:
 if c['id']=='AEGEAN_BRONZE':
  c.update({'title':'Минойцы и микенцы','subtitle':'Дворцы Эгейского мира','period':'ок. 3200–1050 до н. э.','chapterCount':10,'releasedChapters':10,'status':'PLAYABLE','region':'Крит, Эгейское море и материковая Греция','description':'От островных сетей и дворцов Крита до микенских цитаделей, письма Б и кризиса около 1200 года до н. э.','chapters':[{'number':x['number'],'title':x['title']} for x in chapters]})
dump(Path('data/world/campaigns.json'),world)

wt=load(Path('data/world/timeline.json'))
new=[
 {'year':-3200,'label':'Раннекикладские культуры','detail':'Островные общества развивают морские сети, металлургию и характерную мраморную пластику.','campaignId':'AEGEAN_BRONZE','sourcePatch':'v3.4'},
 {'year':-1900,'label':'Первые дворцовые центры Крита','detail':'Кносс, Фест и Маллия становятся крупными административными и ритуальными узлами.','campaignId':'AEGEAN_BRONZE','sourcePatch':'v3.4'},
 {'year':-1625,'label':'Извержение Феры','detail':'Точная дата спорна; извержение погребает Акротири под вулканическим пеплом.','campaignId':'AEGEAN_BRONZE','sourcePatch':'v3.4'},
 {'year':-1600,'label':'Шахтовые гробницы Микен','detail':'Богатые погребения показывают рост материковых воинских элит.','campaignId':'AEGEAN_BRONZE','sourcePatch':'v3.4'},
 {'year':-1450,'label':'Разрушение большинства минойских дворцов','detail':'Большинство критских центров гибнет; Кносс продолжает работу при использовании письма Б.','campaignId':'AEGEAN_BRONZE','sourcePatch':'v3.4'},
 {'year':-1375,'label':'Архивы линейного письма Б в Кноссе','detail':'Административные таблички фиксируют раннюю форму греческого языка.','campaignId':'AEGEAN_BRONZE','sourcePatch':'v3.4'},
 {'year':-1250,'label':'Львиные ворота Микен','detail':'Монументальный вход и расширенные укрепления отражают зрелый дворцовый период.','campaignId':'AEGEAN_BRONZE','sourcePatch':'v3.4'},
 {'year':-1200,'label':'Кризис микенских дворцов','detail':'Пилос и другие центры разрушены; дворцовая письменность и администрация исчезают.','campaignId':'AEGEAN_BRONZE','sourcePatch':'v3.4'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt}
wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

bw=load(Path('data/maps/bronze-world.json'));bw['points']['MINOAN_CRETE']=[35.24,24.81];bw['points']['MYCENAEAN_GREECE']=[37.73,22.76];dump(Path('data/maps/bronze-world.json'),bw)

packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v3.4

## v3.5 — Международный мир бронзового века

Следующий патч свяжет уже готовые региональные кампании в общую систему позднего бронзового века.

Основные темы:

- дипломатия великих держав;
- Амарнский архив;
- торговля медью, оловом, стеклом и престижными товарами;
- Угарит, Алашия и Кипр;
- кораблекрушение Улубурун;
- вассальные договоры и династические браки;
- движение ремесленников, послов и военных;
- параллельная хронология Египта, Хатти, Вавилонии и Эгейского мира;
- системный кризис около 1200 года до н. э.

План патча:

- 8–10 глав;
- 48–60 миссий;
- 90–120 карточек;
- международная карта Восточного Средиземноморья;
- общий пак эпохи;
- межкампанийные задания и итоговый экзамен.
''',encoding='utf-8')

p=ROOT/'README.md';txt=p.read_text(encoding='utf-8');txt=re.sub(r'^# Codex of History v[^\n]+','# Codex of History v3.4.0',txt,count=1,flags=re.M)
section='''\n## v3.4.0 — Минойцы и микенцы\n\n- 10 глав, 60 миссий и 120 карточек.\n- Крит, минойские дворцы, Фера, микенские цитадели, линейное письмо Б и кризис около 1200 года до н. э.\n- Карта Эгейского мира, 10 архивных пулов и отдельный пак.\n- Четырёхчастный экзамен и связи с Хатти, Египтом и Вавилонией.\n- Релизный ZIP содержит только изменённые и новые файлы.\n\n'''
if '## v3.4.0' not in txt:txt=txt.replace('\n',section,1)
p.write_text(txt,encoding='utf-8')
print('integrated v3.4')
