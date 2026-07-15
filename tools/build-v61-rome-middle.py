#!/usr/bin/env python3
from __future__ import annotations
import json, html
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
VERSION='6.1.0'
CHECKED='2026-07-15'

S_MET_ROM={'title':'The Metropolitan Museum of Art: The Art of Ancient Rome','url':'https://www.metmuseum.org/-/media/files/learn/for-educators/publications-for-educators/roman.pdf','type':'museum'}
S_MET_ITALY={'title':'The Metropolitan Museum of Art: Italian Peninsula, 1000 B.C.–1 A.D.','url':'https://www.metmuseum.org/toah/ht/04/eust.html','type':'museum'}
S_BM_ROME={'title':'British Museum: Introduction to ancient Rome','url':'https://www.britishmuseum.org/exhibitions/nero-man-behind-myth/introduction-to-ancient-rome','type':'museum'}
S_BM_PUNIC={'title':'British Museum: Punic culture','url':'https://www.britishmuseum.org/collection/term/x114244','type':'museum'}
S_PERSEUS={'title':'Perseus Digital Library: Polybius and Livy','url':'https://www.perseus.tufts.edu/hopper/','type':'academic'}
S_MET_HEL={'title':'The Metropolitan Museum of Art: Art of the Hellenistic Age','url':'https://www.metmuseum.org/essays/art-of-the-hellenistic-age-and-the-hellenistic-tradition','type':'museum'}

P={
 'ROME':([41.893,12.482],'Рим'),'MESSANA':([38.193,15.554],'Мессана'),'MYLAE':([38.215,15.240],'Милы'),'SICILY':([37.600,14.000],'Сицилия'),'EGATES':([37.950,12.000],'Эгатские острова'),
 'NEW_CARTHAGE':([37.604,-0.986],'Новый Карфаген'),'SAGUNTUM':([39.680,-0.278],'Сагунт'),'ALPS':([45.800,7.500],'Альпы'),'CANNAE':([41.306,16.135],'Канны'),'ZAMA':([36.330,9.450],'Зама'),'CARTHAGE':([36.853,10.323],'Карфаген'),
 'CORCYRA':([39.624,19.922],'Керкира'),'CYNOSCEPHALAE':([39.350,22.450],'Киноскефалы'),'CORINTH':([37.906,22.878],'Коринф'),'MAGNESIA':([38.050,27.350],'Магнесия'),'APAMEA':([38.071,30.166],'Апамея'),'PYDNA':([40.374,22.578],'Пидна'),'MACEDONIA':([40.700,22.500],'Македония'),'AEGEAN':([38.500,25.000],'Эгейское море'),
 'CURIA':([41.893,12.485],'Курия'),'FORUM':([41.892,12.485],'Форум'),'MARS_FIELD':([41.901,12.474],'Марсово поле'),'SICILY_PROVINCE':([37.550,14.100],'провинция Сицилия'),'ITALY':([42.000,13.000],'Италия')
}

CHAPTERS=[
 {
  'number':4,'id':'ROME_CHAPTER_04','title':'Пунические войны','subtitle':'От первого флота до победы при Заме','period':'264–201 годы до н. э.',
  'description':'Рим вышел за пределы Италии, построил большой флот, создал первую провинцию и выдержал вторжение Ганнибала. Победа не была результатом одного сражения: её обеспечили союзная людская база, способность заменять армии, война в нескольких регионах и перенос боевых действий в Африку.',
  'source':S_MET_ROM,
  'chronology':[('264 до н. э.','Начало Первой Пунической войны','textual'),('241 до н. э.','Победа у Эгатских островов и конец войны','archaeological'),('218 до н. э.','Ганнибал переходит Альпы','textual'),('216 до н. э.','Катастрофа Рима при Каннах','textual'),('202 до н. э.','Победа Сципиона при Заме','textual')],
  'locations':['MESSANA','MYLAE','SICILY','CANNAE','ZAMA'],
  'causes':['Соперничество Рима и Карфагена за Сицилию','Вмешательство в конфликт вокруг Мессаны','Рост карфагенской силы в Иберии после Первой войны'],
  'consequences':['Сицилия стала первой римской провинцией','Рим превратился в крупную морскую державу','Карфаген потерял империю и военную самостоятельность'],
  'story':[
   ('WAR_ROM_010','Первая Пуническая война','First Punic War','WAR','долгая борьба Рима и Карфагена за Сицилию и море','264–241 годы до н. э.','MESSANA','COMMON'),
   ('MIL_ROM_010','Римский флот Первой Пунической войны','Roman fleet in the First Punic War','MILITARY','созданный в ходе войны большой флот и новая система морского снабжения','III век до н. э.','MYLAE','UNCOMMON'),
   ('ADM_ROM_010','Сицилия — первая римская провинция','Roman Sicily','ADMINISTRATION','территория за пределами Италии под властью римского магистрата','с 241 года до н. э.','SICILY','RARE'),
   ('PER_CAR_001','Ганнибал Барка','Hannibal Barca','PERSON','карфагенский полководец, перенёсший войну в Италию','ок. 247–183 годы до н. э.','ALPS','LEGENDARY'),
   ('WAR_ROM_001','Вторая Пуническая война','Second Punic War','WAR','война Рима и Карфагена в Иберии, Италии, Сицилии и Африке','218–201 годы до н. э.','SAGUNTUM','EPIC'),
   ('BAT_ROM_001','Битва при Каннах','Battle of Cannae','BATTLE','разгром крупной римской армии Ганнибалом','216 год до н. э.','CANNAE','EPIC'),
   ('PER_ROM_002','Сципион Африканский','Scipio Africanus','PERSON','римский командующий, перенёсший главную войну в Африку','236–183 годы до н. э.','NEW_CARTHAGE','RARE'),
   ('BAT_ROM_002','Битва при Заме','Battle of Zama','BATTLE','решающее поражение армии Ганнибала в Африке','202 год до н. э.','ZAMA','RARE')],
  'archive':[
   ('ROM_A_04_01','Мамертинцы в Мессане','Mamertines in Messana','PEOPLE','наёмники, чей конфликт втянул Рим и Карфаген в Сицилию','III век до н. э.','MESSANA','COMMON'),
   ('ROM_A_04_02','Абордажный мост corvus','Corvus boarding device','TECHNOLOGY','описанное Полибием устройство для абордажа в ранних морских боях','III век до н. э.','MYLAE','UNCOMMON'),
   ('ROM_A_04_03','Эгатские острова: археология морской битвы','Battle of the Egadi Islands archaeology','SOURCE','бронзовые тараны, шлемы и амфоры с места битвы 241 года','241 год до н. э.','EGATES','EPIC'),
   ('ROM_A_04_04','Карфагенская монета с боевым слоном','Carthaginian coin with war elephant','ARTIFACT','серебряная монета из карфагенской Иберии с образом слона','237–209 годы до н. э.','NEW_CARTHAGE','LEGENDARY')]
 },
 {
  'number':5,'id':'ROME_CHAPTER_05','title':'Завоевание эллинистического мира','subtitle':'Союзы, войны и провинции Востока','period':'215–146 годы до н. э.',
  'description':'Рим вошёл в политику Восточного Средиземноморья через войны с Македонией и Селевкидами, союзы с греческими государствами и публичный язык «свободы греков». Военное превосходство не объясняет всё: важны дипломатия, местные коалиции, заложники, договоры и постепенное создание провинциальной власти.',
  'source':S_MET_ITALY,
  'chronology':[('215–205 до н. э.','Первая Македонская война','textual'),('197 до н. э.','Победа при Киноскефалах','textual'),('196 до н. э.','Провозглашение свободы греков','textual'),('188 до н. э.','Апамейский мир','textual'),('168 до н. э.','Победа при Пидне','textual'),('146 до н. э.','Разрушение Коринфа','textual')],
  'locations':['CORCYRA','CYNOSCEPHALAE','CORINTH','MAGNESIA','PYDNA'],
  'causes':['Столкновение Рима с Филиппом V во время войны с Ганнибалом','Просьбы и союзы Пергама, Родоса и греческих государств','Опасение новой большой монархии в Эгейском мире'],
  'consequences':['Македонская монархия была ликвидирована','Селевкидское влияние в Малой Азии резко сократилось','Рим стал главным арбитром и затем прямым правителем части греческого мира'],
  'story':[
   ('ROM_S_05_01','Рим вступает в Первую Македонскую войну','Rome in the First Macedonian War','WAR','первое длительное военное вмешательство Республики в греческий Восток','215–205 годы до н. э.','CORCYRA','COMMON'),
   ('ROM_S_05_02','Фламинин и курс на греческую свободу','Titus Quinctius Flamininus and Greek freedom','PERSON','римский командующий, связавший победу с политическим лозунгом свободы','ок. 228–174 годы до н. э.','CORINTH','UNCOMMON'),
   ('ROM_S_05_03','Манипулярный легион против фаланги','Roman legion against Macedonian phalanx','TACTIC','сопоставление гибкой манипулярной системы и плотного строя сариссофоров','III–II века до н. э.','CYNOSCEPHALAE','RARE'),
   ('ROM_S_05_04','Римская коалиция в Эгейском мире','Roman coalition in the Aegean','DIPLOMACY','союзная сеть Рима, Пергама, Родоса и противников Македонии','III–II века до н. э.','AEGEAN','COMMON'),
   ('ROM_S_05_05','Поход против Антиоха III','Roman–Seleucid campaign','WAR','война Республики и союзников против Селевкидского царя','192–188 годы до н. э.','MAGNESIA','EPIC'),
   ('ROM_S_05_06','Апамейская система после 188 года','Settlement of Apamea','TREATY','договорный порядок, ограничивший Селевкидов к востоку от Тавра','188 год до н. э.','APAMEA','RARE'),
   ('ROM_S_05_07','Македония после Пидны','Macedonia after Pydna','ADMINISTRATION','раздел царства на четыре республики после поражения Персея','168–167 годы до н. э.','PYDNA','UNCOMMON'),
   ('ROM_S_05_08','146 год: Коринф и Карфаген','Rome in 146 BC','EVENT','одновременное уничтожение двух главных противников Республики','146 год до н. э.','CORINTH','LEGENDARY')],
  'archive':[
   ('ROM_A_05_01','Сенатское посольство к Филиппу V','Roman ultimatum to Philip V','DIPLOMACY','дипломатическое давление перед Второй Македонской войной','200 год до н. э.','MACEDONIA','COMMON'),
   ('ROM_A_05_02','Истмийское провозглашение','Flamininus proclamation at the Isthmian Games','SOURCE','публичное объявление свободы греческих общин в 196 году','196 год до н. э.','CORINTH','UNCOMMON'),
   ('ROM_A_05_03','Триумф Луция Эмилия Павла','Triumph of Aemilius Paullus','RITUAL','римское представление победы над Македонией и царём Персеем','167 год до н. э.','ROME','EPIC'),
   ('ROM_A_05_04','Полибий между Ахайей и Римом','Polybius in Rome','PERSON','ахейский политик, заложник и историк римского возвышения','ок. 200–118 годы до н. э.','ROME','MYTHIC')]
 },
 {
  'number':6,'id':'ROME_CHAPTER_06','title':'Как работала Республика','subtitle':'Магистраты, сенат, народ и провинции','period':'III–II века до н. э.',
  'description':'Республика не имела единой писаной конституции. Её порядок складывался из законов, обычаев, ежегодных должностей, сенатского авторитета, народных собраний, трибунской защиты и военного командования. Расширение провинций усилило роль наместников, налоговых подрядчиков и длительных чрезвычайных командований.',
  'source':S_BM_ROME,
  'chronology':[('287 до н. э.','Закон Гортензия завершает основную фазу борьбы сословий','textual'),('242 до н. э.','Появление претора по делам иностранцев','textual'),('227 до н. э.','Дополнительные преторы для Сицилии и Сардинии','textual'),('180 до н. э.','Lex Villia annalis регулирует порядок должностей','textual'),('149 до н. э.','Постоянный суд по делам о вымогательствах','textual')],
  'locations':['CURIA','FORUM','MARS_FIELD','SICILY_PROVINCE','ITALY'],
  'causes':['Необходимость ограничивать единоличную власть','Рост числа войн, судов и провинциальных задач','Конкуренция аристократических семей за должности и славу'],
  'consequences':['Сложилась система коллегиальности и ежегодности','Сенат получил устойчивое влияние на финансы и внешнюю политику','Провинциальные командования создали новые возможности для богатства и злоупотреблений'],
  'story':[
   ('ROM_S_06_01','Сенатское решение','Senatus consultum','POLITICAL','формально совет магистратам, который часто направлял политику Республики','средняя Республика','CURIA','COMMON'),
   ('ROM_S_06_02','Консульская коллегиальность','Roman consular collegiality','OFFICE','два ежегодных консула с высшим гражданским и военным империем','Римская республика','FORUM','UNCOMMON'),
   ('ROM_S_06_03','Претура и юрисдикция','Roman praetorship','OFFICE','магистратура суда и командования, расширявшаяся вместе с государством','с 367 года до н. э.','FORUM','RARE'),
   ('ROM_S_06_04','Народные собрания Республики','Roman assemblies','INSTITUTION','несколько собраний граждан с разным порядком голосования и полномочиями','Римская республика','MARS_FIELD','COMMON'),
   ('ROM_S_06_05','Трибунский запрет','Tribunician veto','LAW','право народного трибуна вмешаться и остановить действие магистрата','Римская республика','FORUM','UNCOMMON'),
   ('ROM_S_06_06','Путь должностей','Cursus honorum','SYSTEM','обычный порядок продвижения через квестуру, претуру и консулат','II–I века до н. э.','ROME','RARE'),
   ('ROM_S_06_07','Провинциальный империй','Provincial imperium','ADMINISTRATION','командная власть магистрата или промагистра за пределами Италии','III–I века до н. э.','SICILY_PROVINCE','EPIC'),
   ('ROM_S_06_08','Союзники, граждане и военный набор','Roman citizens and Italian allies','SOCIAL','неравная система обязанностей, прав и поставки солдат','III–II века до н. э.','ITALY','LEGENDARY')],
  'archive':[
   ('ROM_A_06_01','Полибий о смешанном устройстве','Polybius on the Roman constitution','TEXT','греческое объяснение римского порядка через царский, аристократический и народный элементы','II век до н. э.','ROME','COMMON'),
   ('ROM_A_06_02','Ликторы и знаки магистратской власти','Roman lictors and fasces','ARTIFACT','служители и символы права магистрата приказывать и наказывать','Римская республика','FORUM','UNCOMMON'),
   ('ROM_A_06_03','Публиканы и сбор налогов','Publicani and tax collection','ECONOMY','частные объединения, получавшие государственные подряды и налоговые контракты','II–I века до н. э.','SICILY_PROVINCE','EPIC'),
   ('ROM_A_06_04','Выборы на Марсовом поле','Roman elections on the Campus Martius','RITUAL','пространство голосования, военного сбора и политической конкуренции','Римская республика','MARS_FIELD','MYTHIC')]
 }
]


def load(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))
def dump(path,obj):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def svg_card(path,title,subtitle,chapter,index,kind):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);title=html.escape(title);subtitle=html.escape(subtitle)
 accents={4:'#b18b5a',5:'#837f99',6:'#9c745b'};marks={4:'IV',5:'V',6:'VI'};acc=accents[chapter]
 p.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 900" role="img" aria-label="{title}"><defs><linearGradient id="g" x2="1" y2="1"><stop stop-color="#050505"/><stop offset=".55" stop-color="#27231f"/><stop offset="1" stop-color="#090909"/></linearGradient><radialGradient id="r"><stop stop-color="{acc}" stop-opacity=".62"/><stop offset="1" stop-color="{acc}" stop-opacity="0"/></radialGradient></defs><rect width="720" height="900" fill="url(#g)"/><circle cx="540" cy="210" r="330" fill="url(#r)"/><path d="M80 116 H640 M80 786 H640" stroke="{acc}" stroke-width="2"/><path d="M90 520 C185 432 290 590 395 450 S560 420 635 530" fill="none" stroke="{acc}" stroke-width="9" opacity=".28"/><text x="530" y="390" text-anchor="middle" fill="{acc}" font-size="112" font-family="Georgia">{marks[chapter]}</text><text x="62" y="82" fill="{acc}" font-size="18" font-family="Arial" letter-spacing="4">ROME · CHAPTER {chapter:02d}</text><text x="62" y="650" fill="#fff8e9" font-size="38" font-family="Georgia">{title[:31]}</text><text x="62" y="708" fill="#d8d0c2" font-size="21" font-family="Arial">{subtitle[:58]}</text><text x="62" y="832" fill="{acc}" font-size="18" font-family="Arial" letter-spacing="3">{kind.upper()} · CODEX OF HISTORY · {index:02d}</text></svg>''',encoding='utf-8')

def make_card(cid,title,original,typ,subtitle,date,point,rarity,chapter,source,acquisition):
 coord,label=P[point]
 local=f'assets/cards/rome/chapter_{chapter:02d}/{cid.lower()}.svg'
 return {'id':cid,'type':typ,'title':title,'original':original,'subtitle':subtitle,'era':'Средняя Римская республика','region':'Италия и Средиземноморье','date':date,'rarity':rarity,'difficulty':5+chapter//2,'summary':f'{title} — {subtitle}.','importance':f'Карточка раскрывает главу «{next(c["title"] for c in CHAPTERS if c["number"]==chapter)}» и связывает войну, институты, общество и источники Республики.','facts':[f'Датировка: {date}.',f'Основной смысл: {subtitle}.','Вывод нужно проверять по литературным текстам, монетам, надписям, археологии и устройству конкретного региона.'],'tags':['Римская республика',next(c['title'] for c in CHAPTERS if c['number']==chapter),typ.lower()],'stats':{'influence':7+(chapter%3),'complexity':6+(len(title)%4),'legacy':7+(len(subtitle)%3),'military':4+(1 if typ in {'WAR','BATTLE','MILITARY','TACTIC'} else 0)+chapter%3,'culture':5+(len(original)%4),'politics':6+(1 if typ in {'POLITICAL','DIPLOMACY','OFFICE','INSTITUTION','ADMINISTRATION','LAW','SYSTEM'} else 0)+chapter%3,'religion':3+(len(title)%4),'economy':5+(1 if typ in {'ECONOMY','ADMINISTRATION'} else 0)+chapter%3,'connections':8},'loc':{'label':label,'lat':coord[0],'lon':coord[1]},'image':{'local':local,'caption':f'Локальная учебная обложка: {title}','credit':'Codex of History · локальная учебная обложка','source_url':source['url'],'license':'Project asset','focus':'50% 50%','file':f'{cid.lower()}.svg','kind':'project-cover'},'source':source,'acquisition':acquisition,'campaign':'ROME','chapter':f'ROME_CHAPTER_{chapter:02d}'}

# Existing Rome data.
story=load(Path('data/cards/rome/story.json'));archive=load(Path('data/cards/rome/archive.json'));future=load(Path('data/cards/rome/future.json'))
move_ids={'PER_CAR_001','WAR_ROM_001','BAT_ROM_001','PER_ROM_002','BAT_ROM_002'}
legacy={c['id']:c for c in future if c['id'] in move_ids};future=[c for c in future if c['id'] not in move_ids]
story=[c for c in story if c['id'] not in {x[0] for ch in CHAPTERS for x in ch['story']}]
archive=[c for c in archive if c['id'] not in {x[0] for ch in CHAPTERS for x in ch['archive']}]

new_story=[];new_archive=[];new_rel=[];new_lessons={};new_quizzes={};new_stories={};card_points={};new_nodes=[];new_chapters=[]
rel_i=1
for ch in CHAPTERS:
 ci=ch['number'];ch_id=ch['id'];story_ids=[];arch_ids=[]
 for idx,item in enumerate(ch['story'],1):
  cid,title,original,typ,subtitle,date,point,rarity=item
  if cid in legacy:
   c=legacy[cid]
   c.update({'type':typ,'title':title,'original':original,'subtitle':subtitle,'era':'Средняя Римская республика','region':'Западное Средиземноморье' if ci==4 else 'Средиземноморье','date':date,'rarity':rarity,'difficulty':6,'summary':f'{title} — {subtitle}.','importance':f'Карточка входит в главу «{ch["title"]}» и показывает, как республика превратилась из италийской силы в средиземноморскую державу.','facts':[f'Датировка: {date}.',f'Основной смысл: {subtitle}.','Литературные рассказы нужно сопоставлять с монетами, археологией, географией и политическими интересами авторов.'],'tags':['Римская республика',ch['title'],typ.lower()],'loc':{'label':P[point][1],'lat':P[point][0][0],'lon':P[point][0][1]},'source':ch['source'],'acquisition':'STORY','campaign':'ROME','chapter':ch_id})
   # Keep the historical image and local fallback already attached.
  else:
   c=make_card(cid,title,original,typ,subtitle,date,point,rarity,ci,ch['source'],'STORY');svg_card(Path(c['image']['local']),title,subtitle,ci,idx,'story')
  new_story.append(c);story_ids.append(cid);card_points[cid]=point
 for idx,item in enumerate(ch['archive'],1):
  cid,title,original,typ,subtitle,date,point,rarity=item;c=make_card(cid,title,original,typ,subtitle,date,point,rarity,ci,ch['source'],'ARCHIVE');new_archive.append(c);arch_ids.append(cid);card_points[cid]=point;svg_card(Path(c['image']['local']),title,subtitle,ci,idx,'archive')
 for a,b in zip(story_ids,story_ids[1:]):
  new_rel.append({'id':f'REL_ROM61_{rel_i:04d}','source':a,'target':b,'type':'ПОСЛЕДОВАТЕЛЬНОСТЬ','description':f'Связь внутри главы «{ch["title"]}».','strength':8});rel_i+=1
 for a,b in zip(arch_ids,story_ids[1:5]):
  new_rel.append({'id':f'REL_ROM61_{rel_i:04d}','source':a,'target':b,'type':'АРХИВНЫЙ_КОНТЕКСТ','description':f'Архивный материал уточняет тему главы «{ch["title"]}».','strength':7});rel_i+=1
 # One personal story per new archive pool.
 sid=f'STORY_ROM_{ci:02d}';new_stories[sid]={'id':sid,'cardId':arch_ids[-1],'title':f'Архивное дело: {ch["archive"][-1][1]}','subtitle':ch['title'],'rewardXp':160+ci*10,'rewardFragments':18+ci,'steps':[{'type':'SCENE','title':'Материал архива','text':f'Карточка «{ch["archive"][-1][1]}» требует проверить происхождение, датировку, политический контекст и границу между свидетельством и поздней реконструкцией.'},{'type':'QUESTION','title':'Работа с источником','question':'Какой шаг должен быть первым?','options':['Определить автора или происхождение, дату, аудиторию и жанр','Считать поздний рассказ точной стенограммой','Выбрать самый известный образ','Игнорировать археологический контекст'],'correct':0,'explanation':'История средней Республики восстанавливается по разным типам свидетельств, созданным с разными задачами.'},{'type':'QUESTION','title':'Форма вывода','question':'Как сформулировать итог?','options':['Разделить прямые данные, вероятную реконструкцию и степень уверенности','Объяснить всё одним полководцем','Считать победу доказательством идеального устройства','Не учитывать побеждённые общества'],'correct':0,'explanation':'Корректный вывод показывает ограничения текста и сопоставляет его с другими данными.'}]}
 pool_id={4:'ROME_PUNIC',5:'ROME_EASTERN_WARS',6:'ROME_REPUBLIC_SYSTEM'}[ci]
 mission_titles=[f'Рассказ: {ch["title"]}',f'Хронология: {ch["period"]}',f'Источник: {ch["archive"][0][1]}',f'Карта: {", ".join(P[x][1] for x in ch["locations"][:4])}','Разбор: причины, механизмы и последствия',f'Итог главы: {ch["title"]}']
 mission_ids=[]
 for mi in range(1,7):
  mid=f'ROM_{ci:02d}_{mi:02d}';mission_ids.append(mid);topic=ch['story'][(mi-1)%8]
  cards_pattern=[[story_ids[0],story_ids[1],story_ids[2]],[story_ids[2],story_ids[3],story_ids[4]],[story_ids[3],story_ids[4],story_ids[5]],[story_ids[1],story_ids[5],story_ids[6]],[story_ids[0],story_ids[6],story_ids[7]],[story_ids[7],story_ids[0],story_ids[3]]][mi-1]
  unlock_pattern=[[story_ids[0],story_ids[1]],[story_ids[2]],[story_ids[3],story_ids[4]],[story_ids[5]],[story_ids[6]],[story_ids[7]]][mi-1]
  node={'id':mid,'type':['LESSON','TIMELINE','SOURCE','MAP','CAUSE_EFFECT','FINAL'][mi-1],'title':mission_titles[mi-1],'description':f'{ch["description"]} Фокус миссии: {mission_titles[mi-1]}.','cards':cards_pattern,'unlockCards':unlock_pattern,'xp':180+ci*12+mi*6,'emoji':['▤','◷','▥','⌖','◆','◎'][mi-1],'chapterId':ch_id,'lessonId':mid}
  if mi==2:node['timeline']=[{'id':f't{i}','date':d,'title':t} for i,(d,t,_) in enumerate(ch['chronology'])]
  if mi==4:node['mapTargets']=[{'key':x.lower(),'label':P[x][1],'point':x,'zoom':5 if ci in (4,5) else 8,'radius':180000 if ci in (4,5) else 50000} for x in ch['locations'][:4]]
  if mi==6:node['quiz']=f'QUIZ_ROM_CH{ci}'
  if ci==6 and mi==6:
   node['title']='Контрольный экзамен: Средняя Республика';node['romeCheckpointModules']=[{'id':'QUIZ_ROM_MID_MAP','title':'Карта Средиземноморья'},{'id':'QUIZ_ROM_MID_TIME','title':'Хронология 264–146 годов'},{'id':'QUIZ_ROM_MID_RULE','title':'Устройство Республики'},{'id':'QUIZ_ROM_MID_SOURCE','title':'Источники и границы знания'}]
  new_nodes.append(node)
  activity={'type':['reading','timeline','source','map','cause-effect','quiz'][mi-1]}
  if mi==3:activity.update({'prompt':f'Как работать с темой «{topic[1]}»?','options':['Проверить происхождение, дату, жанр, географию и политическую задачу источника','Считать рассказ победителя нейтральным','Игнорировать материальные данные','Объяснить всё личными качествами полководца'],'correct':0,'explanation':'Римская история требует сопоставлять литературную традицию, археологию, монеты, надписи и институциональный контекст.'})
  if mi==6:activity['quizId']=f'QUIZ_ROM_CH{ci}'
  focus=topic[1];definition=topic[4]
  paras=[
   f'Глава «{ch["title"]}» рассматривает среднюю Республику через войну, дипломатию, управление и участие граждан. {ch["description"]} Тема «{focus}» показывает один из механизмов этой системы, а не отдельный эпизод без последствий.',
   f'Основной материал миссии — {focus.lower()}: {definition}. Его нужно связать с датой, местом, участниками и политическим языком источника. Поздний литературный рассказ не заменяет современную событию надпись, монету или археологический слой.',
   f'Хронология главы включает {", ".join(x[0] for x in ch["chronology"])}. Точные даты крупных сражений известны лучше, чем численность армий, повседневная реакция населения и мотивы всех участников.',
   f'География главы включает {", ".join(P[x][1] for x in ch["locations"])}. Морские расстояния, перевалы, союзные гавани и дороги определяли снабжение и пределы римского командования.',
   f'К основным причинам относятся {", ".join(x.lower() for x in ch["causes"])}. Главные последствия — {", ".join(x.lower() for x in ch["consequences"])}.',
   'Римская победа зависела от сети италийских союзников, ежегодного набора, способности создавать новые армии и распределять командование между магистратами. Это не делает систему бесконечно устойчивой и не отменяет тяжёлых потерь союзных общин.',
   'Сенат не был современным правительством и формально часто давал советы действующим магистратам. Его устойчивое влияние опиралось на опыт бывших должностных лиц, контроль обсуждения финансов и внешней политики, а также на социальный вес аристократии.',
   'Народные собрания принимали законы и избирали магистратов, но порядок голосования был неравным. Богатство, возраст, место жительства, клиентские связи и способность присутствовать в Риме влияли на реальное участие граждан.',
   'Провинция сначала означала сферу поручения магистрата, а затем стала обозначать устойчивую территорию. Управление Сицилией и другими землями потребовало продления полномочий, новых судов, налоговых схем и местных посредников.',
   'Литературная традиция дошла главным образом через римских и греческих авторов, писавших после многих событий. Полибий был близок к элите победителей, Ливий использовал более ранние материалы, а карфагенские и многие местные голоса сохранились хуже.',
   f'Итог миссии должен показать, как тема «{focus}» связана с устройством Республики, ресурсами союзов, географией войны и ограничениями источников. Военная победа не объясняет автоматически, кому принадлежала власть и кто нёс основные расходы.'
  ]
  new_lessons[mid]={'id':mid,'title':mission_titles[mi-1],'duration':14,'objectives':[f'объяснить роль темы «{focus}» в главе «{ch["title"]}»','различить литературный текст, монету, надпись и археологический материал','связать войну, магистратуры, союзников и провинциальное управление'],'story':[{'title':ch['title'],'text':ch['description']},{'title':'Фокус миссии','text':f'{mission_titles[mi-1]}. Главный материал: {focus} — {definition}.'},{'title':'Граница знания','text':'Победившая римская традиция сохранилась лучше карфагенских и многих местных свидетельств.'}],'chronology':[{'date':d,'title':t,'note':f'{t}. Событие нужно связывать с типом источника, географией и политическими последствиями.','certainty':cert} for d,t,cert in ch['chronology']],'concepts':[{'term':x[1],'definition':x[4]} for x in ch['story'][:3]],'causeEffect':{'causes':ch['causes'],'consequences':ch['consequences']},'activity':activity,'sources':[ch['source'],S_PERSEUS],'theory':{'title':mission_titles[mi-1],'readingMinutes':11,'lead':f'{ch["description"]} Основной вопрос миссии — {focus.lower()}.','paragraphs':paras,'historicityNotes':['Численность армий и потерь у древних авторов часто приблизительна и риторически обработана.','Победители определили значительную часть сохранившегося рассказа о Карфагене, Македонии и Селевкидах.','Республиканские институты не образовывали единую писаную конституцию и менялись со временем.','Термины «провинция», «империя» и «демократия» нужно использовать в античном контексте.'],'sources':[ch['source'],S_PERSEUS],'license':'Авторский учебный текст Codex of History.','checkedAt':CHECKED}}
 new_chapters.append({'id':ch_id,'number':ci,'title':ch['title'],'subtitle':ch['subtitle'],'description':ch['description'],'missionIds':mission_ids})
 # Six chapter questions.
 qs=[]
 for qi in range(4):
  correct=ch['story'][qi][1];distr=[ch['story'][(qi+j+1)%8][1] for j in range(3)];pos=(ci+qi)%4;opts=distr[:];opts.insert(pos,correct);qs.append({'text':f'Какой термин соответствует описанию: «{ch["story"][qi][4]}»?','options':opts,'correct':pos,'explanation':f'{correct}: {ch["story"][qi][4]}.'})
 pos=(ci+4)%4;opts=['Принять поздний рассказ буквально','Игнорировать археологию и монеты','Считать войну результатом одного человека'];opts.insert(pos,'Сопоставить тексты, археологию, монеты, географию и институты');qs.append({'text':f'Какой метод нужен в главе «{ch["title"]}»?','options':opts,'correct':pos,'explanation':'История средней Республики строится через несколько независимых типов свидетельств.'})
 pos=(ci+5)%4;opts=['Рим всегда побеждал без тяжёлых потерь','Сенат был современным парламентом','Все союзники имели одинаковые права'];opts.insert(pos,ch['subtitle']);qs.append({'text':f'Какой итог главы «{ch["title"]}» наиболее точен?','options':opts,'correct':pos,'explanation':ch['description']})
 new_quizzes[f'QUIZ_ROM_CH{ci}']={'id':f'QUIZ_ROM_CH{ci}','title':f'Глава {ci}: {ch["title"]}','passPercent':70,'questions':qs}

# Checkpoint exam.
exam={
 'QUIZ_ROM_MID_MAP':('Карта Средиземноморья',[
  ('Где началась Первая Пуническая война?',['В Мессане','В Риме','В Пидне','В Апамее'],0,'Конфликт вокруг Мессаны втянул обе державы в войну.'),('Какой остров стал первой римской провинцией?',['Сардиния','Сицилия','Кипр','Крит'],1,'Основная часть Сицилии стала провинцией после 241 года.'),('Где Ганнибал нанёс крупнейшее поражение Риму?',['При Заме','При Киноскефалах','При Каннах','При Пидне'],2,'Канны стали катастрофой 216 года.'),('Где Рим разгромил Антиоха III?',['При Мессане','При Заме','При Коринфе','При Магнесии'],3,'Магнесия открыла путь к Апамейскому миру.'),('Где проходили важные выборы граждан?',['На Марсовом поле','В Карфагене','В Апамее','На Эгатских островах'],0,'Марсово поле было пространством собраний и военного сбора.')]),
 'QUIZ_ROM_MID_TIME':('Хронология 264–146 годов',[
  ('Что произошло первым?',['Начало Первой Пунической войны','Канны','Пидна','Разрушение Коринфа'],0,'Первая война началась в 264 году.'),('Какое событие относится к 241 году до н. э.?',['Зама','Победа у Эгатских островов','Киноскефалы','Апамейский мир'],1,'Морская победа завершила Первую Пуническую войну.'),('Что произошло в 216 году до н. э.?',['Зама','Пидна','Канны','Коринф'],2,'Канны произошли в 216 году.'),('Какое событие позже всего?',['Магнесия','Пидна','Зама','Разрушение Коринфа'],3,'Коринф был разрушен в 146 году.'),('Какой порядок верен?',['Эгатские острова → Канны → Зама → Киноскефалы → Пидна','Канны → Эгатские острова → Пидна → Зама','Пидна → Зама → Канны → Коринф','Коринф → Пидна → Зама → Канны'],0,'Это базовая последовательность трёх глав.')]),
 'QUIZ_ROM_MID_RULE':('Устройство Республики',[
  ('Что ограничивало власть консулов?',['Коллегиальность, ежегодность и возможность сопротивления других органов','Наследственная монархия','Отсутствие армии','Право провинций выбирать царя'],0,'Консулы делили должность и служили ограниченный срок.'),('Что точнее описывает сенат?',['Современный парламент','Совет аристократов с огромным устойчивым влиянием','Собрание всех жителей Италии','Профессиональная армия'],1,'Сенат формально советовал, но реально направлял многие сферы.'),('Что делали народные собрания?',['Только проводили религиозные игры','Только судили рабов','Избирали магистратов и принимали решения по установленным процедурам','Назначали царей'],2,'Существовало несколько собраний с разным порядком голосования.'),('Что такое провинциальный империй?',['Налог без командования','Право иностранного царя','Частный договор купца','Командная власть римского магистрата вне обычной городской сферы'],3,'Империй позволял командовать армией и управлять порученной областью.'),('Почему союзники были важны?',['Они давали значительную часть войск и ресурсов','Они не участвовали в войнах','Они имели полное гражданство','Они управляли сенатом'],0,'Италийская союзная система давала Риму огромную людскую базу.')]),
 'QUIZ_ROM_MID_SOURCE':('Источники и границы знания',[
  ('Почему Полибий особенно важен?',['Он анализировал возвышение Рима и знал средиземноморскую политику II века','Он был карфагенским царём','Он написал законы Двенадцати таблиц','Он лично видел Первую Пуническую войну'],0,'Полибий был близок к элите, но его взгляд тоже требует критики.'),('Что дают находки у Эгатских островов?',['Точный текст мирного договора','Материальные данные о морской битве','Полный список экипажей','Речь римского консула'],1,'Тараны, шлемы и амфоры связывают рассказ с материальным полем боя.'),('Что показывает монета с боевым слоном?',['Полную программу Ганнибала','Мнение всех карфагенян','Политическую и военную символику карфагенской Иберии','Точную численность слонов'],2,'Монета является источником власти и денежного обращения, а не хроникой.'),('Как читать лозунг «свобода греков»?',['Как доказательство полного ухода Рима','Как современную декларацию прав','Как отказ Рима от союзов','Как политический язык, который нужно сравнить с реальным вмешательством'],3,'Лозунг был действенным, но не означал отсутствия римского давления.'),('Какой вывод корректнее?',['Разделять событие, поздний рассказ, материальные данные и реконструкцию','Принимать цифры потерь буквально','Изучать только победителей','Считать институты неизменными'],0,'Исторический метод требует указать степень уверенности.')])
}
for qid,(title,raw) in exam.items():new_quizzes[qid]={'id':qid,'title':title,'passPercent':70,'questions':[{'text':q,'options':opts,'correct':cor,'explanation':exp} for q,opts,cor,exp in raw]}

# Append cards and save future list.
story.extend(new_story);archive.extend(new_archive);dump(Path('data/cards/rome/story.json'),story);dump(Path('data/cards/rome/archive.json'),archive);dump(Path('data/cards/rome/future.json'),future)

# Campaign chapters and nodes.
campaign=load(Path('data/campaigns/rome/campaign.json'))
campaign['title']='Рим: Республика и Средиземноморье';campaign['description']='Шесть опубликованных глав: от мифов основания и республиканских институтов до завоевания Италии, Пунических войн, восточных кампаний и устройства средней Республики.';campaign['difficulty']=6
campaign['chapters']=[c for c in campaign['chapters'] if c['number']<4]+new_chapters+[{**c} for c in campaign['chapters'] if c['number']>6]
campaign['nodes']=[n for n in campaign['nodes'] if not str(n['id']).startswith(('ROM_04_','ROM_05_','ROM_06_'))]+new_nodes
dump(Path('data/campaigns/rome/campaign.json'),campaign)
for ch in new_chapters:dump(Path(f'data/campaigns/rome/chapter_{ch["number"]:02d}.json'),ch)
# Lessons and quizzes in three files.
for ci in (4,5,6):
 dump(Path(f'data/lessons/rome/chapter_{ci:02d}.json'),{k:v for k,v in new_lessons.items() if k.startswith(f'ROM_{ci:02d}_')})
 dump(Path(f'data/quizzes/rome/chapter_{ci:02d}.json'),{k:v for k,v in new_quizzes.items() if k.startswith(f'QUIZ_ROM_CH{ci}') or (ci==6 and k.startswith('QUIZ_ROM_MID_'))})
# Stories.
stories=load(Path('data/stories/rome/personal.json'));stories.update(new_stories);dump(Path('data/stories/rome/personal.json'),stories)
# Relations.
rels=load(Path('data/core/relations.json'));rels=[r for r in rels if not str(r.get('id','')).startswith('REL_ROM61_')]
# Cross-campaign links to existing Hellenistic and Phoenician cards.
for source,target,desc in [
 ('PHO_S_09_08','WAR_ROM_010','Ранний Карфаген из финикийской кампании становится главным западным противником Рима.'),('HEL_S_10_01','ROM_S_05_02','Римская война с Македонией связывает римскую и эллинистическую перспективы.'),('HEL_S_10_02','ROM_S_05_03','Киноскефалы позволяют сравнить фалангу и манипулярный легион.'),('HEL_S_10_04','ROM_S_05_05','Война с Антиохом III показана с двух сторон.'),('STATE_ROM_002','ROM_S_06_01','Общая карточка Республики связана с конкретным механизмом сенатского решения.'),('ORG_ROM_001','ROM_A_06_01','Римский сенат сопоставляется с анализом Полибия.')]:
 new_rel.append({'id':f'REL_ROM61_{rel_i:04d}','source':source,'target':target,'type':'МЕЖКАМПАНИЙНАЯ_СВЯЗЬ','description':desc,'strength':9});rel_i+=1
rels.extend(new_rel);dump(Path('data/core/relations.json'),rels)
# Pools and acquisition.
pools=load(Path('data/campaigns/rome/pools.json'))
new_pool_specs={
 'ROME_PUNIC':('Пунические войны','ROM_04_02',[x[0] for x in CHAPTERS[0]['archive']]),
 'ROME_EASTERN_WARS':('Рим и эллинистический Восток','ROM_05_02',[x[0] for x in CHAPTERS[1]['archive']]),
 'ROME_REPUBLIC_SYSTEM':('Механика средней Республики','ROM_06_02',[x[0] for x in CHAPTERS[2]['archive']])}
by={p['id']:p for p in pools['pools']}
for pid,(title,unlock,ids) in new_pool_specs.items():
 by[pid]={'id':pid,'campaign':'ROME','title':title,'unlockMission':unlock,'cardIds':ids}
pools['pools']=list(by.values())
for c in new_story:pools['acquisition'][c['id']]={'kind':'STORY','campaign':'ROME','chapter':c['chapter']}
for ci,ch in enumerate(CHAPTERS,4):
 pid={4:'ROME_PUNIC',5:'ROME_EASTERN_WARS',6:'ROME_REPUBLIC_SYSTEM'}[ci]
 for c in [x for x in new_archive if x['chapter']==ch['id']]:pools['acquisition'][c['id']]={'kind':'ARCHIVE','pool':pid,'campaign':'ROME'}
dump(Path('data/campaigns/rome/pools.json'),pools)
# Map.
mp=load(Path('data/maps/rome.json'))
for key,(coord,label) in P.items():mp['points'][key]=coord
mp.setdefault('cardPoints',{}).update(card_points)
for ch in new_chapters:mp.setdefault('chapters',{})[ch['id']]={'title':ch['title'],'center':P[CHAPTERS[ch['number']-4]['locations'][0]][0],'zoom':5 if ch['number'] in (4,5) else 8,'missionIds':ch['missionIds']}
mp['missionCenter']=[39.5,15.0];mp['missionZoom']=4
dump(Path('data/maps/rome.json'),mp)
print(f'generated Rome chapters 4–6: {len(new_story)} story, {len(new_archive)} archive, {len(new_nodes)} missions')
