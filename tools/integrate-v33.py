#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V='3.3.0'

def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,o):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# manifest
m=load(Path('data/content-manifest.json'));m['version']=V;d=m['datasets']
for key,val in [
 ('cards',['data/cards/hittites/story.json','data/cards/hittites/archive.json']),
 ('pools',['data/campaigns/hittites/pools.json']),('quizzes',['data/quizzes/hittites/campaign.json']),
 ('stories',['data/stories/hittites/personal.json']),('lessons',['data/lessons/hittites/campaign.json']),
 ('campaigns',['data/campaigns/hittites/campaign.json'])]:
 for x in val:
  if x not in d[key]:d[key].append(x)
d['maps']['HITTITES']='data/maps/hittites.json'
script='js/features/v3-3-hittites.js'
if script not in m['scripts']:
 idx=m['scripts'].index('js/features/v3-1-1-hotfix.js')
 m['scripts'].insert(idx,script)
dump(Path('data/content-manifest.json'),m)

# relations
rels=load(Path('data/core/relations.json'));add=load(Path('data/core/relations-v33-hittites.json'))
existing={x['id'] for x in rels};rels.extend(x for x in add if x['id'] not in existing);dump(Path('data/core/relations.json'),rels)
(ROOT/'data/core/relations-v33-hittites.json').unlink(missing_ok=True)

# world campaign
world=load(Path('data/world/campaigns.json'))
chapters=load(Path('data/campaigns/hittites/campaign.json'))['chapters']
for c in world:
 if c['id']=='HITTITES':
  c.update({'title':'Хетты и Анатолия','subtitle':'Империя Хаттусы','period':'ок. 2000–1200 до н. э.','chapterCount':10,'releasedChapters':10,'status':'PLAYABLE','region':'Анатолия, Северная Сирия и Верхняя Месопотамия','description':'От карума Каниш и Старого царства до империи Суппилулиумы I, Кадеша и кризиса около 1200 года до н. э.','chapters':[{'number':x['number'],'title':x['title']} for x in chapters]})
dump(Path('data/world/campaigns.json'),world)

# world timeline
wt=load(Path('data/world/timeline.json'))
new=[
 {'year':-1950,'label':'Расцвет карума Каниш','detail':'Староассирийские купцы ведут торговлю оловом и тканями в центральной Анатолии.','campaignId':'HITTITES','sourcePatch':'v3.3'},
 {'year':-1650,'label':'Хаттусили I укрепляет Хаттусу','detail':'Столица становится центром раннего Хеттского царства.','campaignId':'HITTITES','sourcePatch':'v3.3'},
 {'year':-1595,'label':'Хеттский поход на Вавилон','detail':'Мурсили I завершает первую вавилонскую династию; дата зависит от принятой хронологии.','campaignId':'HITTITES','sourcePatch':'v3.3'},
 {'year':-1500,'label':'Указ Телепину','detail':'Царь пытается упорядочить престолонаследие после дворцовых переворотов.','campaignId':'HITTITES','sourcePatch':'v3.3'},
 {'year':-1340,'label':'Империя Суппилулиумы I','detail':'Хатти устанавливает господство над Каркемишем и рядом сирийских царств.','campaignId':'HITTITES','sourcePatch':'v3.3'},
 {'year':-1274,'label':'Битва при Кадеше','detail':'Хеттская и египетская армии сражаются за контроль над Сирией.','campaignId':'HITTITES','sourcePatch':'v3.3'},
 {'year':-1259,'label':'Египетско-хеттский мирный договор','detail':'Хаттусили III и Рамсес II закрепляют мир и взаимную помощь.','campaignId':'HITTITES','sourcePatch':'v3.3'},
 {'year':-1200,'label':'Распад центральной хеттской державы','detail':'Хаттуса оставлена, но Каркемиш и сиро-хеттские центры продолжают часть традиций.','campaignId':'HITTITES','sourcePatch':'v3.3'}]
keys={(x.get('year'),x.get('label'),x.get('campaignId')) for x in wt}
wt.extend(x for x in new if (x['year'],x['label'],x['campaignId']) not in keys);wt.sort(key=lambda x:x.get('year',0));dump(Path('data/world/timeline.json'),wt)

# bronze world map
bw=load(Path('data/maps/bronze-world.json'));bw['points']['HATTITE_CORE']=[40.019,34.615];bw['points']['HITTITE_SYRIA']=[36.829,38.016];dump(Path('data/maps/bronze-world.json'),bw)

# packs version
packs=load(Path('data/core/packs.json'));packs['version']=V;dump(Path('data/core/packs.json'),packs)

# next plan
(ROOT/'docs/NEXT_PATCH_PLAN.md').write_text('''# Следующий этап после v3.3\n\n## v3.4 — Минойцы и микенцы\n\nСледующий крупный патч открывает эгейскую ветку эпохи бронзового века.\n\nОсновные темы:\n\n- Крит и дворцовые центры;\n- Кносс, Фест и Маллия;\n- минойская морская сеть;\n- линейное письмо А и проблема языка;\n- формирование микенских дворцов;\n- линейное письмо Б;\n- Пилос, Микены и Тиринф;\n- война, обмен и дворцовая администрация;\n- отношения с Хатти и Египтом;\n- кризис эгейских дворцов около 1200 года до н. э.\n\nПлан патча:\n\n- 9–10 глав;\n- 54–60 миссий;\n- 100–120 карточек;\n- карта Крита, Эгейского моря и материковой Греции;\n- отдельный пак, пулы и личные истории;\n- связи с хеттской и египетской кампаниями;\n- экзамен кампании.\n''',encoding='utf-8')

# readme patch section
p=ROOT/'README.md';txt=p.read_text(encoding='utf-8');txt=re.sub(r'^# Codex of History v[^\n]+','# Codex of History v3.3.0',txt,count=1,flags=re.M)
section='''\n## v3.3.0 — Хетты и Анатолия\n\n- 10 глав, 60 миссий и 120 карточек.\n- Каниш, Хаттуса, Старое царство, Суппилулиума I, Кадеш и распад державы.\n- Карта Анатолии и Северной Сирии, 10 архивных пулов и отдельный пак.\n- Четырёхчастный итоговый экзамен и связи с Вавилоном и Египтом.\n- Релизный ZIP содержит только изменённые и новые файлы.\n\n'''
if '## v3.3.0' not in txt:txt=txt.replace('\n',section,1)
p.write_text(txt,encoding='utf-8')

print('integrated v3.3')
