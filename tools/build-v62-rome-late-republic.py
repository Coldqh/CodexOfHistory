#!/usr/bin/env python3
from __future__ import annotations
import json, html
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
VERSION='6.2.0'
CHECKED='2026-07-15'

S_GRACCHI={'title':'Plutarch: Life of Tiberius Gracchus','url':'https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Plutarch/Lives/Tiberius_Gracchus*.html','type':'primary-source'}
S_APPIAN={'title':'Appian: The Civil Wars, Book I','url':'https://penelope.uchicago.edu/thayer/e/roman/texts/appian/civil_wars/1*.html','type':'primary-source'}
S_MARIUS={'title':'Plutarch: Life of Marius','url':'https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Plutarch/Lives/Marius*.html','type':'primary-source'}
S_CAESAR={'title':'Plutarch: Life of Caesar','url':'https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Plutarch/Lives/Caesar*.html','type':'primary-source'}
S_BM_CAESAR={'title':'British Museum: denarius portraying Julius Caesar, 44 BC','url':'https://www.britishmuseum.org/collection/object/C_1860-0328-106','type':'museum'}
S_BM_ROME={'title':'British Museum: Introduction to ancient Rome','url':'https://www.britishmuseum.org/exhibitions/nero-man-behind-myth/introduction-to-ancient-rome','type':'museum'}

P={
 'ROME':([41.893,12.482],'Рим'),'CAPITOL':([41.893,12.483],'Капитолий'),'AVENTINE':([41.883,12.481],'Авентин'),'ETRURIA':([42.55,11.20],'Этрурия'),'CAMPANIA':([40.83,14.25],'Кампания'),
 'NUMIDIA':([36.45,6.61],'Нумидия'),'AQUAE_SEXTIAE':([43.53,5.45],'Аквы Секстиевы'),'VERCELLAE':([45.32,8.42],'Верцеллы'),'CORFINIUM':([42.12,13.84],'Корфиний'),'COLLINE_GATE':([41.91,12.50],'Коллинские ворота'),
 'GAUL':([46.50,2.50],'Галлия'),'ALESIA':([47.54,4.50],'Алезия'),'RUBICON':([44.16,12.40],'Рубикон'),'PHARSALUS':([39.30,22.38],'Фарсал'),'MUNDA':([37.37,-4.77],'Мунда'),'CURIA_POMPEY':([41.895,12.476],'Курия Помпея')
}

CHAPTERS=[
 {
  'number':7,'id':'ROME_CHAPTER_07','title':'Гракхи и социальный кризис','subtitle':'Земля, гражданство и политическое насилие','period':'133–121 годы до н. э.',
  'description':'Завоевания принесли Риму богатство, рабов и провинции, но усилили споры о земле, военной службе, распределении ресурсов и правах италийских союзников. Тиберий и Гай Гракхи пытались проводить реформы через народный трибунат. Их гибель не завершила конфликт, а сделала организованное политическое насилие частью республиканской практики.',
  'source':S_GRACCHI,
  'chronology':[('133 до н. э.','Тиберий Гракх становится трибуном и предлагает аграрный закон','textual'),('133 до н. э.','Убийство Тиберия Гракха и его сторонников','textual'),('123 до н. э.','Первый трибунат Гая Гракха','textual'),('122 до н. э.','Второй трибунат и расширение программы реформ','textual'),('121 до н. э.','Гибель Гая Гракха после senatus consultum ultimum','textual')],
  'locations':['ROME','CAPITOL','AVENTINE','ETRURIA','CAMPANIA'],
  'causes':['Концентрация части общественной земли в руках крупных владельцев','Проблемы набора граждан в армию и имущественного ценза','Неравенство прав между римскими гражданами и италийскими союзниками'],
  'consequences':['Аграрная комиссия перераспределяла часть общественной земли','Трибунат стал центром острой борьбы между народом и сенатской элитой','Убийства 133 и 121 годов расширили допустимые формы политического насилия'],
  'story':[
   ('ROM_S_07_01','Тиберий Семпроний Гракх','Tiberius Sempronius Gracchus','PERSON','народный трибун, связавший земельный вопрос с военной и гражданской устойчивостью Республики','ок. 163–133 годы до н. э.','ROME','RARE'),
   ('ROM_S_07_02','Общественная земля ager publicus','Ager publicus','ECONOMY','земля, считавшаяся собственностью римского народа и ставшая предметом аграрного конфликта','II век до н. э.','ETRURIA','COMMON'),
   ('ROM_S_07_03','Аграрная комиссия Гракхов','Gracchan land commission','INSTITUTION','коллегия трёх уполномоченных, измерявшая и распределявшая часть общественной земли','с 133 года до н. э.','CAMPANIA','UNCOMMON'),
   ('ROM_S_07_04','Смещение трибуна Марка Октавия','Deposition of Marcus Octavius','EVENT','спорный прецедент отстранения трибуна, блокировавшего аграрный закон','133 год до н. э.','FORUM','EPIC'),
   ('ROM_S_07_05','Убийство Тиберия Гракха','Death of Tiberius Gracchus','EVENT','первое крупное кровопролитие внутри римской политики поздней Республики','133 год до н. э.','CAPITOL','LEGENDARY'),
   ('ROM_S_07_06','Гай Семпроний Гракх','Gaius Sempronius Gracchus','PERSON','трибун, соединивший земельную, зерновую, судебную, дорожную и колониальную программы','ок. 154–121 годы до н. э.','ROME','EPIC'),
   ('ROM_S_07_07','Зерновой закон Гая Гракха','Lex frumentaria of Gaius Gracchus','LAW','регулярная продажа зерна гражданам по установленной цене','123 год до н. э.','ROME','UNCOMMON'),
   ('ROM_S_07_08','Чрезвычайное постановление сената','Senatus consultum ultimum','LAW','политическая формула, позволявшая консулам действовать против объявленной внутренней угрозы','121 год до н. э.','AVENTINE','RARE')],
  'archive':[
   ('ROM_A_07_01','Lex Sempronia agraria','Lex Sempronia agraria','LAW','аграрный закон 133 года, ограничивавший использование части общественной земли','133 год до н. э.','ROME','COMMON'),
   ('ROM_A_07_02','Гракханские межевые камни','Gracchan boundary stones','ARTIFACT','надписанные камни, связываемые с работой аграрной комиссии в Италии','конец II века до н. э.','CAMPANIA','UNCOMMON'),
   ('ROM_A_07_03','Консул Луций Опимий','Lucius Opimius','PERSON','консул 121 года, руководивший подавлением сторонников Гая Гракха','II век до н. э.','ROME','EPIC'),
   ('ROM_A_07_04','Авентин в кризисе 121 года','Aventine in 121 BC','SITE','городское пространство последнего противостояния Гая Гракха и сенатской власти','121 год до н. э.','AVENTINE','LEGENDARY')]
 },
 {
  'number':8,'id':'ROME_CHAPTER_08','title':'Марий, союзники и Сулла','subtitle':'Армии, гражданство и первая диктатура гражданской войны','period':'112–79 годы до н. э.',
  'description':'Югуртинская война, вторжение кимвров и тевтонов, Союзническая война и конфликт Мария с Суллой показали, что республиканские должности и армии всё чаще использовались в борьбе внутри гражданского сообщества. Набор бедных граждан не был одномоментной «реформой Мария», а развитие армии нельзя отделять от провинциальных войн, земельных ожиданий ветеранов и личного авторитета командующих.',
  'source':S_MARIUS,
  'chronology':[('112–105 до н. э.','Югуртинская война в Нумидии','textual'),('107 до н. э.','Первое консульство Мария и новое командование в Нумидии','textual'),('102–101 до н. э.','Победы над тевтонами и кимврами','textual'),('91–88 до н. э.','Союзническая война в Италии','textual'),('88 до н. э.','Первый поход Суллы на Рим','textual'),('82–81 до н. э.','Победа Суллы, проскрипции и диктатура','textual')],
  'locations':['NUMIDIA','AQUAE_SEXTIAE','VERCELLAE','CORFINIUM','COLLINE_GATE'],
  'causes':['Коррупционные скандалы и затяжная война с Югуртой','Неравное положение италийских союзников, служивших в римских армиях','Конкуренция за чрезвычайные командования и политический контроль'],
  'consequences':['Гражданство было распространено на большинство свободных италиков','Римские армии впервые были использованы для захвата столицы','Проскрипции и сулланская диктатура сделали насилие инструментом конституционной перестройки'],
  'story':[
   ('ROM_S_08_01','Югуртинская война','Jugurthine War','WAR','затяжная война в Нумидии, обострившая споры о коррупции и командовании','112–105 годы до н. э.','NUMIDIA','COMMON'),
   ('ROM_S_08_02','Гай Марий','Gaius Marius','PERSON','полководец и семикратный консул, чья карьера связала внешние войны с внутренним кризисом','ок. 157–86 годы до н. э.','ROME','LEGENDARY'),
   ('ROM_S_08_03','Набор бедных граждан в легионы','Recruitment of poorer Roman citizens','MILITARY','расширение практики набора граждан без значительного имущества в длительные провинциальные армии','конец II века до н. э.','ROME','RARE'),
   ('ROM_S_08_04','Кимврская угроза','Cimbrian War','WAR','серия войн с кимврами, тевтонами и их союзниками после поражения при Араузионе','113–101 годы до н. э.','AQUAE_SEXTIAE','UNCOMMON'),
   ('ROM_S_08_05','Союзническая война','Social War','WAR','восстание италийских союзников за гражданство и политическое равенство','91–88 годы до н. э.','CORFINIUM','EPIC'),
   ('ROM_S_08_06','Расширение римского гражданства в Италии','Extension of Roman citizenship in Italy','LAW','законы, включившие большинство союзных общин в римское гражданское тело','90–89 годы до н. э.','ITALY','RARE'),
   ('ROM_S_08_07','Первый поход Суллы на Рим','Sulla’s first march on Rome','EVENT','использование консульской армии против столицы в борьбе за восточное командование','88 год до н. э.','ROME','EPIC'),
   ('ROM_S_08_08','Диктатура и проскрипции Суллы','Sulla’s dictatorship and proscriptions','SYSTEM','конфискации, казни и конституционная перестройка после победы в гражданской войне','82–79 годы до н. э.','COLLINE_GATE','MYTHIC')],
  'archive':[
   ('ROM_A_08_01','Царь Югурта','Jugurtha','PERSON','нумидийский царь, противник Рима и центральная фигура войны 112–105 годов','ок. 160–104 годы до н. э.','NUMIDIA','COMMON'),
   ('ROM_A_08_02','Сдача Югурты Бокху','Surrender of Jugurtha to Bocchus','DIPLOMACY','дипломатическая операция, ставшая предметом соперничества Мария и Суллы','105 год до н. э.','NUMIDIA','UNCOMMON'),
   ('ROM_A_08_03','Италика в Корфинии','Italia at Corfinium','STATE','столица и политический образ союзнической конфедерации во время войны с Римом','91–88 годы до н. э.','CORFINIUM','EPIC'),
   ('ROM_A_08_04','Сулланское конституционное устройство','Sullan constitutional settlement','LAW','попытка усилить сенат и ограничить народный трибунат после гражданской войны','81–79 годы до н. э.','ROME','LEGENDARY')]
 },
 {
  'number':9,'id':'ROME_CHAPTER_09','title':'Цезарь и гражданская война','subtitle':'Чрезвычайные командования, коалиции и падение республиканского равновесия','period':'70–44 годы до н. э.',
  'description':'В последние десятилетия Республики Помпей, Красс, Цезарь и их противники использовали выборы, народные законы, провинциальные командования, военные победы и частные политические коалиции. Гражданская война 49–45 годов не была неизбежным итогом одной реформы. Она выросла из конкуренции элит, долговременных командований, проблем возвращения армии в гражданскую политику и отсутствия устойчивого способа разделить власть после победы.',
  'source':S_CAESAR,
  'chronology':[('70 до н. э.','Совместное консульство Помпея и Красса','textual'),('63 до н. э.','Заговор Катилины и консульство Цицерона','textual'),('60 до н. э.','Формирование политического союза Цезаря, Помпея и Красса','textual'),('58–50 до н. э.','Галльские войны Цезаря','textual'),('49 до н. э.','Переход Рубикона','textual'),('48 до н. э.','Победа Цезаря при Фарсале','textual'),('44 до н. э.','Убийство Цезаря в мартовские иды','textual')],
  'locations':['ROME','GAUL','ALESIA','RUBICON','PHARSALUS','CURIA_POMPEY'],
  'causes':['Рост чрезвычайных и многолетних военных командований','Частные коалиции влиятельных политиков обходили обычное сенатское согласование','Невозможность договориться о статусе Цезаря после завершения галльского командования'],
  'consequences':['Римская территория стала полем гражданской войны','Цезарь сосредоточил диктаторскую власть и провёл широкий комплекс решений','Убийство Цезаря не восстановило Республику и открыло новый цикл войн'],
  'story':[
   ('ROM_S_09_01','Гней Помпей Великий','Pompey the Great','PERSON','полководец с чрезвычайными командованиями против пиратов и Митридата','106–48 годы до н. э.','ROME','EPIC'),
   ('ROM_S_09_02','Марк Лициний Красс','Marcus Licinius Crassus','PERSON','богатейший политик Республики, консул и участник частной коалиции с Помпеем и Цезарем','ок. 115–53 годы до н. э.','ROME','RARE'),
   ('ROM_S_09_03','Первый триумвират','First Triumvirate','DIPLOMACY','неформальное политическое соглашение Цезаря, Помпея и Красса','ок. 60–53 годы до н. э.','ROME','UNCOMMON'),
   ('PER_ROM_003','Юлий Цезарь','Julius Caesar','PERSON','полководец, диктатор и центральная фигура последнего кризиса Республики','100–44 годы до н. э.','GAUL','LEGENDARY'),
   ('ROM_S_09_05','Галльские войны Цезаря','Gallic Wars','WAR','серия кампаний, давшая Цезарю армию, богатство и политический престиж','58–50 годы до н. э.','GAUL','EPIC'),
   ('EVT_ROM_003','Переход через Рубикон','Crossing of the Rubicon','EVENT','ввод армии в Италию и открытый разрыв с политическими противниками','49 год до н. э.','RUBICON','EPIC'),
   ('ROM_S_09_07','Битва при Фарсале','Battle of Pharsalus','BATTLE','решающая победа Цезаря над основной армией Помпея','48 год до н. э.','PHARSALUS','RARE'),
   ('ROM_S_09_08','Диктатура и убийство Цезаря','Dictatorship and assassination of Julius Caesar','EVENT','сосредоточение власти и заговор, завершившийся убийством в мартовские иды','46–44 годы до н. э.','CURIA_POMPEY','MYTHIC')],
  'archive':[
   ('ROM_A_09_01','Заговор Катилины','Catilinarian conspiracy','EVENT','политический кризис 63 года, известный прежде всего по речам Цицерона и сочинению Саллюстия','63 год до н. э.','ROME','COMMON'),
   ('ROM_A_09_02','Цицерон и республиканская речь','Cicero and republican oratory','PERSON','консул, оратор и автор, чьи тексты одновременно являются источниками и политическими выступлениями','106–43 годы до н. э.','ROME','UNCOMMON'),
   ('ROM_A_09_03','Денарий с портретом Цезаря','Denarius portraying Julius Caesar','ARTIFACT','монета 44 года с прижизненным портретом диктатора и политической титулатурой','44 год до н. э.','ROME','EPIC'),
   ('ROM_A_09_04','Курия Помпея и мартовские иды','Curia of Pompey and the Ides of March','SITE','место заседания сената, где Цезарь был убит 15 марта 44 года','44 год до н. э.','CURIA_POMPEY','LEGENDARY')]
 }
]

# Existing map keys used above but defined in old map.

def load(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))
def dump(path,obj):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def point_data(point, old_map):
 if point in P:return P[point]
 coord=old_map['points'][point];return (coord, point.replace('_',' ').title())

def svg_card(path,title,subtitle,chapter,index,kind):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);title=html.escape(title);subtitle=html.escape(subtitle)
 accents={7:'#a66b4f',8:'#826b88',9:'#a64236'};marks={7:'VII',8:'VIII',9:'IX'};acc=accents[chapter]
 p.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 900" role="img" aria-label="{title}"><defs><linearGradient id="g" x2="1" y2="1"><stop stop-color="#050505"/><stop offset=".58" stop-color="#241f1f"/><stop offset="1" stop-color="#090909"/></linearGradient><radialGradient id="r"><stop stop-color="{acc}" stop-opacity=".66"/><stop offset="1" stop-color="{acc}" stop-opacity="0"/></radialGradient></defs><rect width="720" height="900" fill="url(#g)"/><circle cx="540" cy="220" r="330" fill="url(#r)"/><path d="M80 116 H640 M80 786 H640" stroke="{acc}" stroke-width="2"/><path d="M92 520 C190 420 300 590 402 446 S566 420 638 530" fill="none" stroke="{acc}" stroke-width="9" opacity=".3"/><text x="526" y="390" text-anchor="middle" fill="{acc}" font-size="104" font-family="Georgia">{marks[chapter]}</text><text x="62" y="82" fill="{acc}" font-size="18" font-family="Arial" letter-spacing="4">ROME · CHAPTER {chapter:02d}</text><text x="62" y="650" fill="#fff8e9" font-size="37" font-family="Georgia">{title[:31]}</text><text x="62" y="708" fill="#d8d0c2" font-size="21" font-family="Arial">{subtitle[:58]}</text><text x="62" y="832" fill="{acc}" font-size="18" font-family="Arial" letter-spacing="3">{kind.upper()} · CODEX OF HISTORY · {index:02d}</text></svg>''',encoding='utf-8')

def make_card(item,chapter,source,acquisition,old_map):
 cid,title,original,typ,subtitle,date,point,rarity=item
 coord,label=point_data(point,old_map);local=f'assets/cards/rome/chapter_{chapter:02d}/{cid.lower()}.svg'
 ch=next(c for c in CHAPTERS if c['number']==chapter)
 return {'id':cid,'type':typ,'title':title,'original':original,'subtitle':subtitle,'era':'Поздняя Римская республика','region':'Италия и Средиземноморье','date':date,'rarity':rarity,'difficulty':6+chapter//3,'summary':f'{title} — {subtitle}.','importance':f'Карточка раскрывает главу «{ch["title"]}» и показывает, как социальные конфликты, армии и личные коалиции изменяли республиканские институты.','facts':[f'Датировка: {date}.',f'Основной смысл: {subtitle}.','Литературные рассказы нужно сопоставлять с законами, монетами, надписями, археологией и политической задачей автора.'],'tags':['Поздняя Республика',ch['title'],typ.lower()],'stats':{'influence':7+(chapter%3),'complexity':6+(len(title)%4),'legacy':7+(len(subtitle)%3),'military':5+(1 if typ in {'WAR','BATTLE','MILITARY'} else 0),'culture':5+(len(original)%4),'politics':7+(1 if typ in {'LAW','INSTITUTION','DIPLOMACY','SYSTEM','EVENT'} else 0),'religion':3+(len(title)%4),'economy':5+(1 if typ in {'ECONOMY'} else 0),'connections':8},'loc':{'label':label,'lat':coord[0],'lon':coord[1]},'image':{'local':local,'caption':f'Локальная учебная обложка: {title}','credit':'Codex of History · локальная учебная обложка','source_url':source['url'],'license':'Project asset','focus':'50% 50%','file':f'{cid.lower()}.svg','kind':'project-cover'},'source':source,'acquisition':acquisition,'campaign':'ROME','chapter':f'ROME_CHAPTER_{chapter:02d}'}

old_map=load(Path('data/maps/rome.json'))
story=load(Path('data/cards/rome/story.json'));archive=load(Path('data/cards/rome/archive.json'));future=load(Path('data/cards/rome/future.json'))
move_ids={'PER_ROM_003','EVT_ROM_003'};legacy={c['id']:c for c in future if c['id'] in move_ids};future=[c for c in future if c['id'] not in move_ids]
all_new_ids={x[0] for ch in CHAPTERS for x in ch['story']+ch['archive']}
story=[c for c in story if c['id'] not in all_new_ids];archive=[c for c in archive if c['id'] not in all_new_ids]
new_story=[];new_archive=[];new_nodes=[];new_chapters=[];new_lessons={};new_quizzes={};new_stories={};new_rel=[];card_points={};rel_i=1

for ch in CHAPTERS:
 ci=ch['number'];story_ids=[];arch_ids=[]
 for idx,item in enumerate(ch['story'],1):
  cid,title,original,typ,subtitle,date,point,rarity=item
  if cid in legacy:
   c=legacy[cid];coord,label=point_data(point,old_map)
   c.update({'type':typ,'title':title,'original':original,'subtitle':subtitle,'era':'Поздняя Римская республика','region':'Италия и Средиземноморье','date':date,'rarity':rarity,'difficulty':7,'summary':f'{title} — {subtitle}.','importance':f'Карточка входит в главу «{ch["title"]}» и показывает последний кризис Республики.','facts':[f'Датировка: {date}.',f'Основной смысл: {subtitle}.','Событие известно через политически заинтересованные и часто более поздние литературные традиции.'],'tags':['Поздняя Республика',ch['title'],typ.lower()],'loc':{'label':label,'lat':coord[0],'lon':coord[1]},'source':ch['source'],'acquisition':'STORY','campaign':'ROME','chapter':ch['id']})
  else:
   c=make_card(item,ci,ch['source'],'STORY',old_map);svg_card(Path(c['image']['local']),title,subtitle,ci,idx,'story')
  new_story.append(c);story_ids.append(cid);card_points[cid]=point
 for idx,item in enumerate(ch['archive'],1):
  c=make_card(item,ci,S_BM_CAESAR if item[0]=='ROM_A_09_03' else ch['source'],'ARCHIVE',old_map);svg_card(Path(c['image']['local']),item[1],item[4],ci,idx,'archive');new_archive.append(c);arch_ids.append(c['id']);card_points[c['id']]=item[6]
 for a,b in zip(story_ids,story_ids[1:]):
  new_rel.append({'id':f'REL_ROM62_{rel_i:04d}','source':a,'target':b,'type':'ПОСЛЕДОВАТЕЛЬНОСТЬ','description':f'Связь внутри главы «{ch["title"]}».','strength':8});rel_i+=1
 for a,b in zip(arch_ids,story_ids[1:5]):
  new_rel.append({'id':f'REL_ROM62_{rel_i:04d}','source':a,'target':b,'type':'АРХИВНЫЙ_КОНТЕКСТ','description':f'Архивный материал уточняет тему главы «{ch["title"]}».','strength':7});rel_i+=1
 sid=f'STORY_ROM_{ci:02d}';new_stories[sid]={'id':sid,'cardId':arch_ids[-1],'title':f'Архивное дело: {ch["archive"][-1][1]}','subtitle':ch['title'],'rewardXp':180+ci*10,'rewardFragments':20+ci,'steps':[{'type':'SCENE','title':'Материал архива','text':f'Карточка «{ch["archive"][-1][1]}» требует отделить прямое свидетельство от позднего политического рассказа.'},{'type':'QUESTION','title':'Проверка источника','question':'Как начать анализ?','options':['Определить автора, дату, жанр, аудиторию и политическую задачу','Считать биографию точной стенограммой','Выбрать самую драматичную версию','Игнорировать монеты и надписи'],'correct':0,'explanation':'Источники поздней Республики создавались участниками борьбы или более поздними авторами.'},{'type':'QUESTION','title':'Форма вывода','question':'Какой вывод корректнее?','options':['Разделить подтверждённые данные, вероятную реконструкцию и спорные мотивы','Объяснить кризис характером одного человека','Считать насилие неизбежным','Игнорировать союзников и провинции'],'correct':0,'explanation':'Кризис Республики имел институциональные, социальные и военные причины.'}]}
 mission_titles=[f'Рассказ: {ch["title"]}',f'Хронология: {ch["period"]}',f'Источник: {ch["archive"][0][1]}',f'Карта: {", ".join(point_data(x,old_map)[1] for x in ch["locations"][:4])}','Разбор: причины, механизмы и последствия',f'Итог главы: {ch["title"]}']
 mission_ids=[]
 for mi in range(1,7):
  mid=f'ROM_{ci:02d}_{mi:02d}';mission_ids.append(mid);topic=ch['story'][(mi-1)%8]
  patterns=[[0,1,2],[2,3,4],[3,4,5],[1,5,6],[0,6,7],[7,0,3]];unlock_patterns=[[0,1],[2],[3,4],[5],[6],[7]]
  node={'id':mid,'type':['LESSON','TIMELINE','SOURCE','MAP','CAUSE_EFFECT','FINAL'][mi-1],'title':mission_titles[mi-1],'description':f'{ch["description"]} Фокус миссии: {mission_titles[mi-1]}.','cards':[story_ids[i] for i in patterns[mi-1]],'unlockCards':[story_ids[i] for i in unlock_patterns[mi-1]],'xp':210+ci*12+mi*6,'emoji':['▤','◷','▥','⌖','◆','◎'][mi-1],'chapterId':ch['id'],'lessonId':mid}
  if mi==2:node['timeline']=[{'id':f't{i}','date':d,'title':t} for i,(d,t,_) in enumerate(ch['chronology'])]
  if mi==4:node['mapTargets']=[{'key':x.lower(),'label':point_data(x,old_map)[1],'point':x,'zoom':5 if x not in {'ROME','CAPITOL','AVENTINE','CURIA_POMPEY'} else 8,'radius':180000 if x not in {'ROME','CAPITOL','AVENTINE','CURIA_POMPEY'} else 50000} for x in ch['locations'][:4]]
  if mi==6:node['quiz']=f'QUIZ_ROM_CH{ci}'
  if ci==9 and mi==6:
   node['title']='Контрольный экзамен: Поздняя Республика';node['romeCheckpointModules']=[{'id':'QUIZ_ROM_LATE_MAP','title':'Карта кризиса Республики'},{'id':'QUIZ_ROM_LATE_TIME','title':'Хронология 133–44 годов'},{'id':'QUIZ_ROM_LATE_CRISIS','title':'Институты, армии и насилие'},{'id':'QUIZ_ROM_LATE_SOURCE','title':'Источники и политическая память'}]
  new_nodes.append(node)
  activity={'type':['reading','timeline','source','map','cause-effect','quiz'][mi-1]}
  if mi==3:activity.update({'prompt':f'Как работать с темой «{topic[1]}»?','options':['Сопоставить дату, жанр, аудиторию, материальные данные и политический контекст','Принять биографический рассказ буквально','Считать речь точной стенограммой','Объяснить всё личной амбицией'],'correct':0,'explanation':'Поздняя Республика известна по конфликтующим литературным традициям, законам, монетам, надписям и археологии.'})
  if mi==6:activity['quizId']=f'QUIZ_ROM_CH{ci}'
  focus=topic[1];definition=topic[4];locs=', '.join(point_data(x,old_map)[1] for x in ch['locations'])
  paras=[
   f'Глава «{ch["title"]}» рассматривает позднюю Республику через социальные конфликты, военные командования и конкуренцию элит. {ch["description"]} Тема «{focus}» показывает один механизм кризиса, а не самостоятельную причину всех последующих событий.',
   f'Основной материал миссии — {focus.lower()}: {definition}. Его необходимо связать с конкретной датой, должностью, территорией и процедурой принятия решения. Поздняя биография или речь может сохранять важные сведения, но одновременно строит образ героя, врага или защитника Республики.',
   f'Хронология главы включает {", ".join(x[0] for x in ch["chronology"])}. Даты должностей и сражений обычно устанавливаются увереннее, чем мотивы политиков, численность сторонников и точный ход уличного насилия.',
   f'География главы включает {locs}. Войны в Нумидии, Галлии, Греции и самой Италии меняли политический вес полководцев, длительность командований и ожидания солдат после завершения службы.',
   f'К основным причинам относятся {", ".join(x.lower() for x in ch["causes"])}. Главные последствия — {", ".join(x.lower() for x in ch["consequences"])}.',
   'Народный трибунат, сенат, консулы и собрания не исчезли во время кризиса. Конфликт разворачивался через существующие должности и законы, но участники всё чаще применяли чрезвычайные постановления, давление толпы, вооружённые отряды и провинциальные армии.',
   'Выражение «мариевы реформы» удобно, но создаёт ложное впечатление единого закона, который сразу превратил армию в профессиональную. Изменения набора, снаряжения, срока службы и отношений между солдатами и полководцем растянулись на десятилетия и зависели от конкретной войны.',
   'Союзническая война показывает, что расширение Рима не означало равенства италийских общин. Союзники несли военные обязанности, но не участвовали в римских выборах. Распространение гражданства стало крупной перестройкой государства, а не простым завершением восстания.',
   'Походы Суллы и Цезаря на Италию сделали армию участником внутренней политики. Однако солдаты действовали не только из личной верности. На решение влияли законность командования, добыча, земля, задолженность службы и страх перед противниками.',
   'Плутарх и Аппиан писали спустя много поколений и использовали утраченные источники. Их рассказы нельзя отбросить, но следует сравнивать между собой, с Цицероном, Саллюстием, Цезарем, монетами, надписями и археологией конкретных мест.',
   f'Итог миссии должен показать, как тема «{focus}» связана с гражданством, командованием, общественными ресурсами и политическим насилием. Нельзя объяснять падение республиканского равновесия только моральным упадком или характером одного человека.'
  ]
  new_lessons[mid]={'id':mid,'title':mission_titles[mi-1],'duration':15,'objectives':[f'объяснить роль темы «{focus}» в главе «{ch["title"]}»','различить первичный политический текст, позднюю биографию, монету и археологический материал','связать гражданство, военное командование и политическое насилие'],'story':[{'title':ch['title'],'text':ch['description']},{'title':'Фокус миссии','text':f'{mission_titles[mi-1]}. Главный материал: {focus} — {definition}.'},{'title':'Граница знания','text':'Политические речи, мемуары и поздние биографии сохраняют конфликтующие версии поздней Республики.'}],'chronology':[{'date':d,'title':t,'note':f'{t}. Событие нужно связать с должностью, территорией, типом источника и политическими последствиями.','certainty':cert} for d,t,cert in ch['chronology']],'concepts':[{'term':x[1],'definition':x[4]} for x in ch['story'][:3]],'causeEffect':{'causes':ch['causes'],'consequences':ch['consequences']},'activity':activity,'sources':[ch['source'],S_APPIAN,S_BM_ROME],'theory':{'title':mission_titles[mi-1],'readingMinutes':12,'lead':f'{ch["description"]} Основной вопрос миссии — {focus.lower()}.','paragraphs':paras,'historicityNotes':['Плутарх и Аппиан писали после событий и строили моральные и политические объяснения.','Понятие «мариевы реформы» не следует понимать как один точно датированный пакет законов.','Численность жертв, сторонников и армий в литературной традиции часто приблизительна.','Современные термины «партия», «профессиональная армия» и «конституция» требуют пояснения.'],'sources':[ch['source'],S_APPIAN,S_BM_ROME],'license':'Авторский учебный текст Codex of History.','checkedAt':CHECKED}}
 new_chapters.append({'id':ch['id'],'number':ci,'title':ch['title'],'subtitle':ch['subtitle'],'description':ch['description'],'missionIds':mission_ids})
 qs=[]
 for qi in range(4):
  correct=ch['story'][qi][1];distr=[ch['story'][(qi+j+1)%8][1] for j in range(3)];pos=(ci+qi)%4;opts=distr[:];opts.insert(pos,correct);qs.append({'text':f'Какой термин соответствует описанию: «{ch["story"][qi][4]}»?','options':opts,'correct':pos,'explanation':f'{correct}: {ch["story"][qi][4]}.'})
 pos=(ci+4)%4;opts=['Принять позднюю биографию буквально','Игнорировать монеты и законы','Объяснить кризис одним полководцем'];opts.insert(pos,'Сопоставить тексты, законы, монеты, археологию и институциональный контекст');qs.append({'text':f'Какой метод нужен в главе «{ch["title"]}»?','options':opts,'correct':pos,'explanation':'Поздняя Республика требует сопоставления конфликтующих свидетельств.'})
 pos=(ci+5)%4;opts=['Республика перестала существовать сразу после Гракхов','Все италийские союзники имели гражданство до 91 года','Армии действовали только ради добычи'];opts.insert(pos,ch['subtitle']);qs.append({'text':f'Какой итог главы «{ch["title"]}» наиболее точен?','options':opts,'correct':pos,'explanation':ch['description']})
 new_quizzes[f'QUIZ_ROM_CH{ci}']={'id':f'QUIZ_ROM_CH{ci}','title':f'Глава {ci}: {ch["title"]}','passPercent':70,'questions':qs}

exam={
 'QUIZ_ROM_LATE_MAP':('Карта кризиса Республики',[
  ('Где происходило последнее противостояние Гая Гракха?',['На Авентине','В Нумидии','У Фарсала','В Галлии'],0,'Кризис 121 года завершился на Авентине.'),('Какой город союзники сделали столицей Италики?',['Рим','Корфиний','Капуя','Фарсал'],1,'Корфиний получил новое политическое значение во время Союзнической войны.'),('Какую границу перешёл Цезарь в 49 году?',['Альпы','Дунай','Рубикон','Евфрат'],2,'Рубикон отделял провинциальное командование от Италии.'),('Где Цезарь победил основную армию Помпея?',['При Каннах','У Зама','При Пидне','При Фарсале'],3,'Фарсал стал решающей победой 48 года.'),('Где Сулла победил противников перед установлением диктатуры?',['У Коллинских ворот','В Алезии','В Нумидии','У Верцелл'],0,'Битва у Коллинских ворот произошла в 82 году.')]),
 'QUIZ_ROM_LATE_TIME':('Хронология 133–44 годов',[
  ('Что произошло первым?',['Трибунат Тиберия Гракха','Союзническая война','Переход Рубикона','Убийство Цезаря'],0,'Тиберий был трибуном в 133 году.'),('Какое событие относится к 91–88 годам?',['Галльские войны','Союзническая война','Югуртинская война','Битва при Фарсале'],1,'Союзническая война началась в 91 году.'),('Что произошло в 88 году до н. э.?',['Убийство Гая Гракха','Фарсал','Первый поход Суллы на Рим','Заговор Катилины'],2,'Сулла впервые ввёл консульскую армию в Рим.'),('Какое событие позже всего?',['Заговор Катилины','Переход Рубикона','Фарсал','Убийство Цезаря'],3,'Цезарь был убит в 44 году.'),('Какой порядок верен?',['Гракхи → Марий → Союзническая война → Сулла → Цезарь','Сулла → Гракхи → Цезарь → Марий','Цезарь → Марий → Союзническая война','Марий → Гракхи → Сулла → Югурта'],0,'Это базовая последовательность трёх глав.')]),
 'QUIZ_ROM_LATE_CRISIS':('Институты, армии и насилие',[
  ('Почему аграрный вопрос был политическим?',['Он связывал землю, военную службу, гражданский статус и власть собраний','Он касался только рабов','Он решался иностранными царями','Он не затрагивал Италию'],0,'Земля была связана с имущественным положением граждан и общественными ресурсами.'),('Что точнее о «мариевых реформах»?',['Это один закон 107 года','Это длительный комплекс изменений, а не единый мгновенный пакет','Марий отменил гражданство','Марий создал постоянную императорскую армию'],1,'Историки не сводят все изменения армии к одному акту.'),('Что изменила Союзническая война?',['Отменила сенат','Уничтожила провинции','Резко расширила римское гражданство в Италии','Передала власть Карфагену'],2,'После войны большинство италиков получили гражданство.'),('Почему походы Суллы и Цезаря были переломом?',['Они запретили выборы','Они уничтожили все легионы','Они отменили провинции','Провинциальные армии были использованы в борьбе за власть в Италии'],3,'Армия стала прямым инструментом гражданской войны.'),('Что было первым триумвиратом?',['Неформальная коалиция Цезаря, Помпея и Красса','Законный орган из трёх царей','Постоянная магистратура','Союз Рима, Карфагена и Египта'],0,'Это современное название частного политического соглашения.')]),
 'QUIZ_ROM_LATE_SOURCE':('Источники и политическая память',[
  ('Как читать Плутарха о Гракхах?',['Как позднюю биографию с ценными данными и моральной композицией','Как протокол заседания','Как современную надпись','Как археологический отчёт'],0,'Плутарх писал через два века после событий.'),('Что дают монеты Цезаря 44 года?',['Точный план убийства','Изображение, титулатуру и политическую коммуникацию','Полную биографию','Список всех сенаторов'],1,'Монеты являются прямым политическим и материальным источником.'),('Почему речи Цицерона требуют критики?',['Они написаны на греческом','Они не имеют дат','Они были частью политической борьбы и литературно отредактированы','Они созданы археологами'],2,'Речь одновременно сообщает и убеждает аудиторию.'),('Как использовать «Записки о Галльской войне»?',['Как нейтральную хронику','Как поздний средневековый роман','Как археологическую карту','Как рассказ самого командующего, требующий сравнения с другими данными'],3,'Цезарь формировал публичное объяснение собственных действий.'),('Какой вывод корректнее?',['Разделять прямые данные, авторскую позицию и современную реконструкцию','Выбирать самого известного автора','Принимать цифры жертв буквально','Игнорировать монеты и надписи'],0,'Исторический метод должен показывать степень уверенности.')])
}
for qid,(title,raw) in exam.items():new_quizzes[qid]={'id':qid,'title':title,'passPercent':70,'questions':[{'text':q,'options':opts,'correct':cor,'explanation':exp} for q,opts,cor,exp in raw]}

story.extend(new_story);archive.extend(new_archive);dump(Path('data/cards/rome/story.json'),story);dump(Path('data/cards/rome/archive.json'),archive);dump(Path('data/cards/rome/future.json'),future)
campaign=load(Path('data/campaigns/rome/campaign.json'));campaign['title']='Рим: Республика и гражданские войны';campaign['description']='Девять опубликованных глав: от основания и завоевания Средиземноморья до Гракхов, Союзнической войны, Суллы, Цезаря и падения республиканского равновесия.';campaign['difficulty']=7
campaign['chapters']=[c for c in campaign['chapters'] if c['number']<7]+new_chapters+[c for c in campaign['chapters'] if c['number']>9]
campaign['nodes']=[n for n in campaign['nodes'] if not str(n['id']).startswith(('ROM_07_','ROM_08_','ROM_09_'))]+new_nodes
dump(Path('data/campaigns/rome/campaign.json'),campaign)
for ch in new_chapters:dump(Path(f'data/campaigns/rome/chapter_{ch["number"]:02d}.json'),ch)
for ci in (7,8,9):
 dump(Path(f'data/lessons/rome/chapter_{ci:02d}.json'),{k:v for k,v in new_lessons.items() if k.startswith(f'ROM_{ci:02d}_')})
 dump(Path(f'data/quizzes/rome/chapter_{ci:02d}.json'),{k:v for k,v in new_quizzes.items() if k.startswith(f'QUIZ_ROM_CH{ci}') or (ci==9 and k.startswith('QUIZ_ROM_LATE_'))})
stories=load(Path('data/stories/rome/personal.json'));stories.update(new_stories);dump(Path('data/stories/rome/personal.json'),stories)
rels=load(Path('data/core/relations.json'));rels=[r for r in rels if not str(r.get('id','')).startswith('REL_ROM62_')]
for source,target,desc in [
 ('ROM_S_06_08','ROM_S_07_01','Система граждан и союзников ведёт к земельному и военному спору Гракхов.'),('ASB_S_10_08','ROM_S_08_01','Нумидийская война разворачивается в мире, ранее затронутом карфагенскими и римскими сетями.'),('CLG_S_10_08','ROM_S_09_01','Позднереспубликанские командования на Востоке связаны с греко-македонским пространством.'),('ALX_S_09_06','ROM_S_09_05','Римские полководцы использовали модель личного военного престижа, но действовали в иной политической системе.'),('HEL_S_10_08','ROM_S_09_07','Фарсал проходит в эллинистическом Восточном Средиземноморье.')]:
 new_rel.append({'id':f'REL_ROM62_{rel_i:04d}','source':source,'target':target,'type':'МЕЖКАМПАНИЙНАЯ_СВЯЗЬ','description':desc,'strength':8});rel_i+=1
rels.extend(new_rel);dump(Path('data/core/relations.json'),rels)
pools=load(Path('data/campaigns/rome/pools.json'));specs={'ROME_GRACCHI':('Гракхи и социальный кризис','ROM_07_02',[x[0] for x in CHAPTERS[0]['archive']]),'ROME_MARIUS_SULLA':('Марий, союзники и Сулла','ROM_08_02',[x[0] for x in CHAPTERS[1]['archive']]),'ROME_CAESAR_CIVIL':('Цезарь и гражданская война','ROM_09_02',[x[0] for x in CHAPTERS[2]['archive']])};by={p['id']:p for p in pools['pools']}
for pid,(title,unlock,ids) in specs.items():by[pid]={'id':pid,'campaign':'ROME','title':title,'unlockMission':unlock,'cardIds':ids}
pools['pools']=list(by.values())
for c in new_story:pools['acquisition'][c['id']]={'kind':'STORY','campaign':'ROME','chapter':c['chapter']}
for ci,pid in [(7,'ROME_GRACCHI'),(8,'ROME_MARIUS_SULLA'),(9,'ROME_CAESAR_CIVIL')]:
 for c in [x for x in new_archive if x['chapter']==f'ROME_CHAPTER_{ci:02d}']:pools['acquisition'][c['id']]={'kind':'ARCHIVE','pool':pid,'campaign':'ROME'}
dump(Path('data/campaigns/rome/pools.json'),pools)
mp=old_map
for key,(coord,label) in P.items():mp['points'][key]=coord
mp.setdefault('cardPoints',{}).update(card_points)
for ch in new_chapters:
 loc=CHAPTERS[ch['number']-7]['locations'][0];mp.setdefault('chapters',{})[ch['id']]={'title':ch['title'],'center':point_data(loc,old_map)[0],'zoom':5 if ch['number'] in (8,9) else 7,'missionIds':ch['missionIds']}
mp['missionCenter']=[42.0,12.0];mp['missionZoom']=4;dump(Path('data/maps/rome.json'),mp)
print(f'generated Rome chapters 7–9: {len(new_story)} story, {len(new_archive)} archive, {len(new_nodes)} missions')
