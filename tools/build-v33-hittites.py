#!/usr/bin/env python3
from __future__ import annotations
import json, html
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
VERSION='3.4.0'
CHECKED='2026-07-13'
SRC_MET={'title':'The Met: The Hittites','url':'https://www.metmuseum.org/essays/the-hittites','type':'museum'}
SRC_UNESCO={'title':'UNESCO: Hattusha, the Hittite Capital','url':'https://whc.unesco.org/en/list/377/','type':'heritage'}
SRC_CONTACT={'title':'The Met: Cultures in Contact','url':'https://www.metmuseum.org/met-publications/cultures-in-contact-from-mesopotamia-to-the-mediterranean-in-the-second-millenium-bc','type':'museum'}
SRC_UGARIT={'title':'The Met: Ugarit','url':'https://www.metmuseum.org/essays/ugarit','type':'museum'}
SRC_BM={'title':'British Museum: Hittite collection context','url':'https://www.britishmuseum.org/collection/term/x13949','type':'museum'}

P={
'HATTUSA':([40.019,34.615],'Хаттуса'), 'YAZILIKAYA':([40.026,34.621],'Язылыкая'),
'ALACA':([40.234,34.695],'Аладжа-Хююк'), 'KANESH':([38.850,35.635],'Каниш / Кюльтепе'),
'ASSUR':([35.456,43.262],'Ашшур'), 'KUSSARA':([38.5,35.0],'Куссара, приблизительное положение'),
'ALEPPO':([36.202,37.134],'Алеппо'), 'BABYLON':([32.536,44.421],'Вавилон'),
'CARCHEMISH':([36.829,38.016],'Каркемиш'), 'UGARIT':([35.602,35.785],'Угарит'),
'KADESH':([34.557,36.519],'Кадеш'), 'AMARNA':([27.644,30.896],'Ахетатон / Амарна'),
'ARINNA':([39.9,34.5],'Аринна, точное место спорно'), 'TARHUNTASSA':([37.2,33.0],'Тархунтасса, приблизительная область'),
'TROY':([39.957,26.239],'Вилуса / Троя'), 'WASHUKANNI':([36.8,40.0],'Вашшуканни, приблизительная область'),
'AMURRU':([34.6,36.1],'Амурру, приблизительная область'), 'MALATYA':([38.355,38.309],'Мелид / Малатья'),
'KIZZUWATNA':([37.0,35.4],'Киццуватна / Киликия'), 'NERIK':([41.1,35.5],'Нерик, приблизительная область'),
'SAPINUWA':([40.17,35.48],'Шапинува'), 'SARISSA':([39.31,36.86],'Шарисса'),
'ALALAKH':([36.236,36.383],'Алалах'), 'TARSUS':([36.918,34.891],'Тарс'),
}

# topic = title, original, type, subtitle, date, point
CHAPTERS=[
{
 'title':'Плато, народы и языки Анатолии','subtitle':'Центральная Анатолия складывается из разных языков, культов и локальных центров.','description':'География плато, Хатти, хатты, несийский язык, лувийцы, хурриты и ранние центры показывают сложность региона до единой державы.','period':'III — начало II тысячелетия до н. э.','source':SRC_MET,
 'chronology':[('III тысячелетие до н. э.','Развитие центров раннего бронзового века в центральной Анатолии','archaeological'),('ок. 2300–2000 до н. э.','Богатые погребения Аладжа-Хююка','approximate'),('начало II тысячелетия до н. э.','Расширение контактов с Месопотамией','mixed'),('XVII век до н. э.','Хаттуса становится центром нового царства','approximate')],
 'locations':['HATTUSA','ALACA','KANESH'],'causes':['Положение между Эгейским миром, Кавказом, Сирией и Месопотамией','Доступ к металлам и сухопутным маршрутам','Сосуществование разных языковых и культовых традиций'],'consequences':['Сложная культурная среда будущего Хеттского царства','Заимствование местных названий и богов','Формирование сети укреплённых центров'],
 'story':[
 ('Анатолийское плато','Anatolia','REGION','высокое внутреннее пространство с резкими сезонными условиями','II тысячелетие до н. э.','HATTUSA'),
 ('Река Халис','Kızılırmak','RIVER','дуга реки, окружавшая ядро земли Хатти','II тысячелетие до н. э.','HATTUSA'),
 ('Хатты','Hattians','PEOPLE','неиндоевропейское население центральной Анатолии','III–II тысячелетия до н. э.','ALACA'),
 ('Хеттский язык','Hittite language','TEXT','древнейший письменно засвидетельствованный индоевропейский язык','II тысячелетие до н. э.','HATTUSA'),
 ('Лувийцы','Luwians','PEOPLE','носители родственных анатолийских языков на юге и западе','II тысячелетие до н. э.','TARHUNTASSA'),
 ('Хурриты','Hurrians','PEOPLE','население Верхней Месопотамии и Сирии с сильным культурным влиянием','II тысячелетие до н. э.','WASHUKANNI'),
 ('Аладжа-Хююк','Alaca Höyük','SITE','центр с богатыми погребениями и позднейшими хеттскими памятниками','III–II тысячелетия до н. э.','ALACA'),
 ('Земля Хатти','Hatti','REGION','политико-географическое название ядра хеттского мира','II тысячелетие до н. э.','HATTUSA')],
 'archive':[
 ('Царские гробницы Аладжа-Хююка','Alaca Höyük bronze standards','SITE','богатые погребальные комплексы раннего бронзового века','ок. 2300–2000 до н. э.','ALACA'),
 ('Солнечные диски Аладжа-Хююка','Alaca Höyük bronze standards','ARTIFACT','бронзовые штандарты из элитных погребений','III тысячелетие до н. э.','ALACA'),
 ('Анатолийские металлы','Metallurgy in Anatolia','RESOURCE','медь, серебро и другие материалы торговых сетей','III–II тысячелетия до н. э.','ALACA'),
 ('Многоязычная Анатолия','Languages of the ancient Near East','CONCEPT','сосуществование хаттского, хеттского, лувийского, хурритского и аккадского','II тысячелетие до н. э.','HATTUSA')]
},
{
 'title':'Каниш и староассирийская торговля','subtitle':'Купцы из Ашшура создают сеть карумов, кредитов и семейных предприятий.','description':'Кюльтепе, карум Каниш, архивы купцов, олово, ткани, серебро и караваны показывают раннюю коммерческую систему Анатолии.','period':'ок. 1950–1750 до н. э.','source':SRC_CONTACT,
 'chronology':[('ок. 1950 до н. э.','Расцвет староассирийской торговли в Канише','approximate'),('XIX век до н. э.','Тысячи табличек фиксируют сделки и семейную переписку','archaeological'),('ок. 1836 до н. э.','Разрушение одного из уровней карума Каниш','approximate'),('XVIII век до н. э.','Политическое усиление местных царств и деятельность Анитты','mixed')],
 'locations':['KANESH','ASSUR','KUSSARA'],'causes':['Спрос анатолийских элит на олово и ткани','Доступ купцов Ашшура к дальним торговым маршрутам','Использование кредита, партнёрств и семейных сетей'],'consequences':['Большой корпус письменных источников','Рост Каниша как торгового узла','Связь местных царей с международной торговлей'],
 'story':[
 ('Каниш','Kültepe','CITY','крупный анатолийский центр и место ассирийского карума','XX–XVIII века до н. э.','KANESH'),
 ('Карум Каниш','Karum','SYSTEM','торговый квартал и институт купеческого самоуправления','начало II тысячелетия до н. э.','KANESH'),
 ('Купцы Ашшура','Old Assyrian trade','PEOPLE','семейные торговые дома, работавшие между Месопотамией и Анатолией','XX–XVIII века до н. э.','ASSUR'),
 ('Староассирийские таблички','Kültepe texts','TEXT','деловые письма, контракты, долги и семейная переписка','начало II тысячелетия до н. э.','KANESH'),
 ('Торговля оловом','Tin sources and trade in ancient times','RESOURCE','поставка металла для производства бронзы','начало II тысячелетия до н. э.','KANESH'),
 ('Торговля тканями','Old Assyrian trade','RESOURCE','дорогие ткани из Ашшура в обмен на серебро','начало II тысячелетия до н. э.','ASSUR'),
 ('Караванная сеть','Caravan trade','ROUTE','цепь маршрутов, постоялых дворов и контрольных пунктов','начало II тысячелетия до н. э.','KANESH'),
 ('Анитта','Anitta','PERSON','правитель Куссары и Каниша, известный по раннему хеттскому тексту','XVIII век до н. э.','KUSSARA')],
 'archive':[
 ('Таблички Кюльтепе','Kültepe texts','ARTIFACT','глиняные документы из домов торгового квартала','начало II тысячелетия до н. э.','KANESH'),
 ('Лимму-датировки','Limmu','SYSTEM','годовые эпонимы, связывающие документы в относительную хронологию','начало II тысячелетия до н. э.','ASSUR'),
 ('Купеческие женщины Каниша','Old Assyrian trade','PEOPLE','участницы домашних производств, займов и переписки','начало II тысячелетия до н. э.','KANESH'),
 ('Ослы караванов','Donkey caravan','ARTIFACT','основной транспорт дальних купеческих маршрутов','начало II тысячелетия до н. э.','KANESH')]
},
{
 'title':'Возникновение Старого царства','subtitle':'Хаттусили I создаёт устойчивую династию и ведёт войны в Сирии.','description':'Хаттуса, Лабарна, Хаттусили I, Куссара, Алалах и Алеппо показывают раннюю экспансию и трудности престолонаследия.','period':'XVII век до н. э.','source':SRC_UNESCO,
 'chronology':[('ок. 1650 до н. э.','Хаттусили I делает Хаттусу царской столицей','approximate'),('XVII век до н. э.','Походы в Северную Сирию и нападение на Алалах','mixed'),('конец XVII века до н. э.','Конфликт вокруг наследника отражён в завещании царя','textual'),('ок. 1620 до н. э.','Мурсили I наследует престол','approximate')],
 'locations':['HATTUSA','ALALAKH','ALEPPO'],'causes':['Контроль центральноанатолийского ядра','Стремление к сирийским маршрутам и городам','Династическая консолидация вокруг Хаттусы'],'consequences':['Появление Старого Хеттского царства','Длительное соперничество за Северную Сирию','Фиксация проблем престолонаследия в царских текстах'],
 'story':[
 ('Хаттусили I','Hattusili I','PERSON','ранний великий царь и основатель столицы в Хаттусе','XVII век до н. э.','HATTUSA'),
 ('Хаттуса','Hattusa','CITY','укреплённая столица внутри дуги Халиса','XVII–XIII века до н. э.','HATTUSA'),
 ('Титул Лабарна','Labarna I','CONCEPT','царское имя, ставшее обозначением верховной власти','XVII век до н. э.','HATTUSA'),
 ('Старое Хеттское царство','Hittite Old Kingdom','STATE','ранняя фаза царства до периода внутренних кризисов','ок. 1650–1500 до н. э.','HATTUSA'),
 ('Походы в Северную Сирию','Hattusili I','EVENT','военные кампании против Алалаха и державы Ямхад','XVII век до н. э.','ALALAKH'),
 ('Алалах','Alalakh','CITY','сирийский дворцовый центр на пути к Средиземному морю','II тысячелетие до н. э.','ALALAKH'),
 ('Ямхад и Алеппо','Yamhad','STATE','сильное северосирийское царство с центром в Алеппо','XVIII–XVII века до н. э.','ALEPPO'),
 ('Завещание Хаттусили I','Hattusili I','TEXT','царский текст о предательстве, наследнике и верности двора','XVII век до н. э.','HATTUSA')],
 'archive':[
 ('Куссара','Kussara','CITY','ранний центр династии, точное место которого не установлено','XVIII–XVII века до н. э.','KUSSARA'),
 ('Анналы Хаттусили I','Hattusili I','TEXT','описание военных походов раннего царя','XVII век до н. э.','HATTUSA'),
 ('Городские стены Хаттусы','Hattusa','BUILDING','система укреплений столицы на сложном рельефе','II тысячелетие до н. э.','HATTUSA'),
 ('Старохеттская хронология','Hittite Old Kingdom','CONCEPT','реконструкция порядка ранних царей по поздним копиям','XVII–XVI века до н. э.','HATTUSA')]
},
{
 'title':'Мурсили I, Вавилон и дворцовые кризисы','subtitle':'Дальний поход приносит славу, но убийства царей разрушают устойчивость династии.','description':'Разгром Алеппо, поход к Вавилону, убийство Мурсили I, череда переворотов и указ Телепину показывают цену слабого порядка наследования.','period':'ок. 1620–1500 до н. э.','source':SRC_MET,
 'chronology':[('ок. 1600 до н. э.','Мурсили I завершает разгром Алеппо','approximate'),('традиционно ок. 1595 до н. э.','Хеттское войско захватывает Вавилон','traditional'),('после возвращения','Мурсили I убит в результате дворцового заговора','textual'),('ок. 1500 до н. э.','Телепину издаёт указ о престолонаследии','approximate')],
 'locations':['ALEPPO','BABYLON','HATTUSA'],'causes':['Продолжение сирийской политики Хаттусили I','Уязвимость династии перед дворцовыми группировками','Отсутствие устойчивого порядка передачи власти'],'consequences':['Конец первой династии Вавилона','Серия убийств и переворотов в Хатти','Попытка Телепину упорядочить престолонаследие'],
 'story':[
 ('Мурсили I','Mursili I','PERSON','царь, разгромивший Алеппо и совершивший поход на Вавилон','XVII–XVI века до н. э.','HATTUSA'),
 ('Разгром Алеппо','Yamhad','EVENT','завершение борьбы с главным сирийским соперником','начало XVI века до н. э.','ALEPPO'),
 ('Хеттский поход на Вавилон','Sack of Babylon','EVENT','дальний рейд, завершивший первую вавилонскую династию','традиционно ок. 1595 до н. э.','BABYLON'),
 ('Убийство Мурсили I','Mursili I','EVENT','дворцовый заговор после возвращения царя','XVI век до н. э.','HATTUSA'),
 ('Хантили I','Hantili I','PERSON','участник переворота и преемник Мурсили I','XVI век до н. э.','HATTUSA'),
 ('Дворцовые перевороты','Hittite Old Kingdom','EVENT','серия насильственных смен власти','XVI век до н. э.','HATTUSA'),
 ('Телепину','Telipinu','PERSON','царь, пытавшийся прекратить династические убийства','ок. 1500 до н. э.','HATTUSA'),
 ('Указ Телепину','Edict of Telipinu','LAW','текст о наследовании, преступлениях двора и царском порядке','ок. 1500 до н. э.','HATTUSA')],
 'archive':[
 ('Вавилонская синхронизация','Sack of Babylon','CONCEPT','связь хеттской и месопотамской хронологий через поход Мурсили','XVII–XVI века до н. э.','BABYLON'),
 ('Дворцовая хроника','Hittite texts','TEXT','рассказы о преступлениях и наказаниях при дворе','II тысячелетие до н. э.','HATTUSA'),
 ('Клятва царской семьи','Hittite military oath','TEXT','ритуализированная верность царю и династии','II тысячелетие до н. э.','HATTUSA'),
 ('Проблема средней хронологии','Chronology of the ancient Near East','CONCEPT','спор о точной дате падения Вавилона','II тысячелетие до н. э.','BABYLON')]
},
{
 'title':'Царь, двор и архив Хаттусы','subtitle':'Империя держится на семье царя, чиновниках, писцах, законах и договорах.','description':'Великий царь, тавананна, царевичи, архивы Хаттусы, клинопись, законы, земельные пожалования и наместники раскрывают устройство власти.','period':'XVI–XIII века до н. э.','source':SRC_UNESCO,
 'chronology':[('XVI–XV века до н. э.','Формируется зрелая система царского двора','mixed'),('XV–XIV века до н. э.','Архивы Хаттусы пополняются договорами и ритуалами','archaeological'),('XIV–XIII века до н. э.','Царевичи управляют ключевыми вассальными центрами','textual'),('XIII век до н. э.','Бронзовая табличка фиксирует договор с Курунтой','textual')],
 'locations':['HATTUSA','CARCHEMISH','TARHUNTASSA'],'causes':['Необходимость управлять неоднородными территориями','Опора на царскую семью и писцов','Использование письменных договоров и земельных актов'],'consequences':['Разветвлённая дворцовая администрация','Многоязычный архив международного значения','Сильная, но потенциально опасная роль царевичей'],
 'story':[
 ('Великий царь Хатти','Great King','OFFICE','верховный военный, судебный и ритуальный правитель','II тысячелетие до н. э.','HATTUSA'),
 ('Тавананна','Tawananna','OFFICE','титул главной царицы с самостоятельной культовой ролью','II тысячелетие до н. э.','HATTUSA'),
 ('Царская семья','Hittite monarchy','SYSTEM','династическая сеть правителей, наместников и брачных союзов','II тысячелетие до н. э.','HATTUSA'),
 ('Архив Хаттусы','Hittite texts','TEXT','десятки тысяч фрагментов договоров, ритуалов и писем','II тысячелетие до н. э.','HATTUSA'),
 ('Хеттская клинопись','Hittite cuneiform','TEXT','адаптация месопотамской письменности для нескольких языков','II тысячелетие до н. э.','HATTUSA'),
 ('Хеттские законы','Hittite laws','LAW','сборники правовых положений в копиях разных периодов','II тысячелетие до н. э.','HATTUSA'),
 ('Земельные пожалования','Hittite land donation deeds','SYSTEM','царские акты о владениях, службе и привилегиях','II тысячелетие до н. э.','HATTUSA'),
 ('Царевичи-наместники','Hittite Empire','OFFICE','члены династии во главе Каркемиша и других центров','XIV–XIII века до н. э.','CARCHEMISH')],
 'archive':[
 ('Нишантепский архив печатей','Nişantepe','ARTIFACT','тысячи глиняных оттисков царских и чиновничьих печатей','XIII век до н. э.','HATTUSA'),
 ('Таблички Дома на склоне','Hattusa','ARTIFACT','архивные комплексы столицы','II тысячелетие до н. э.','HATTUSA'),
 ('Панкус','Pankus','CONCEPT','собрание, роль которого в политике остаётся предметом споров','Старое царство','HATTUSA'),
 ('Бронзовая табличка Тудхалии IV','Bronze Tablet of Tudhaliya IV','ARTIFACT','договор с Курунтой и редкий металлический документ','XIII век до н. э.','HATTUSA')]
},
{
 'title':'Тысяча богов Хатти','subtitle':'Хеттская религия соединяет местные, хурритские и сирийские культы.','description':'Бог грозы, богиня Солнца Аринны, хурритские божества, праздники, оракулы, ритуалы очищения и Язылыкая формируют религиозный порядок.','period':'II тысячелетие до н. э.','source':SRC_MET,
 'chronology':[('Старое царство','Хаттские и анатолийские культы входят в царские ритуалы','mixed'),('XIV–XIII века до н. э.','Хурритское влияние усиливается при дворе','textual'),('XIII век до н. э.','Монументальная программа Язылыкая оформляет пантеон','archaeological'),('конец XIII века до н. э.','Цари проводят ритуалы против бедствий и нарушений клятв','textual')],
 'locations':['ARINNA','YAZILIKAYA','KIZZUWATNA'],'causes':['Присоединение разных регионов и культов','Потребность включать местных богов в царский порядок','Сильное хурритское влияние из Киццуватны и Сирии'],'consequences':['Образ «тысячи богов Хатти»','Многоязычные ритуальные тексты','Связь дипломатических клятв с пантеоном'],
 'story':[
 ('Тысяча богов Хатти','Hittite mythology','RELIGION','формула множественного и включающего пантеона','II тысячелетие до н. э.','HATTUSA'),
 ('Бог грозы Хатти','Tarḫunna','RELIGION','главное божество царской власти и погоды','II тысячелетие до н. э.','HATTUSA'),
 ('Богиня Солнца Аринны','Sun goddess of Arinna','RELIGION','верховная богиня, связанная с царской династией','II тысячелетие до н. э.','ARINNA'),
 ('Хурритский Тешуб','Teshub','RELIGION','бог грозы хурритского круга, сближенный с анатолийскими культами','II тысячелетие до н. э.','KIZZUWATNA'),
 ('Государственные праздники','Hittite festivals','SYSTEM','длительные поездки двора по священным центрам','II тысячелетие до н. э.','HATTUSA'),
 ('Ритуалы очищения','Hittite ritual texts','TEXT','тексты против болезни, клятвопреступления и скверны','II тысячелетие до н. э.','HATTUSA'),
 ('Оракулы и гадания','Hittite divination','SYSTEM','процедуры выяснения воли богов','II тысячелетие до н. э.','HATTUSA'),
 ('Язылыкая','Yazılıkaya','SITE','скальное святилище с процессиями богов','XIII век до н. э.','YAZILIKAYA')],
 'archive':[
 ('Серебряный сосуд с оленем','Hittite silver vessel with stag','ARTIFACT','ритуальный сосуд с богом и животным','XIV–XIII века до н. э.','HATTUSA'),
 ('Культовые инвентари','Hittite cult inventory texts','TEXT','перечни храмов, богов и необходимых предметов','II тысячелетие до н. э.','HATTUSA'),
 ('Праздник Пурулли','Puruli','EVENT','весенний ритуал обновления царства','II тысячелетие до н. э.','NERIK'),
 ('Рельефы Язылыкая','Yazılıkaya','ARTIFACT','монументальные изображения хурритизированного пантеона','XIII век до н. э.','YAZILIKAYA')]
},
{
 'title':'Суппилулиума I и хеттская империя','subtitle':'Победы в Сирии превращают Хатти в одну из главных держав позднего бронзового века.','description':'Суппилулиума I, разгром Митанни, Каркемиш, Угарит, Амурру, царевичи и чума показывают расширение и цену империи.','period':'XIV век до н. э.','source':SRC_MET,
 'chronology':[('ок. 1350 до н. э.','Суппилулиума I укрепляет власть в Анатолии','approximate'),('середина XIV века до н. э.','Хеттские походы разрушают систему Митанни в Сирии','mixed'),('XIV век до н. э.','Каркемиш и Угарит входят в хеттскую систему','textual'),('после египетского похода пленных','Эпидемия поражает Хатти','textual')],
 'locations':['HATTUSA','CARCHEMISH','UGARIT'],'causes':['Ослабление Митанни','Военная реорганизация Хеттского царства','Борьба за сирийские города и маршруты'],'consequences':['Создание имперской системы вассалов','Передача Каркемиша царевичу','Эпидемия и династический кризис после завоеваний'],
 'story':[
 ('Суппилулиума I','Šuppiluliuma I','PERSON','царь, создавший хеттскую империю в Сирии','XIV век до н. э.','HATTUSA'),
 ('Война с Митанни','Mitanni','WAR','серия кампаний, сломавших господство Митанни','XIV век до н. э.','WASHUKANNI'),
 ('Каркемишское наместничество','Carchemish','STATE','династический центр хеттского управления Сирией','XIV–XII века до н. э.','CARCHEMISH'),
 ('Угарит как вассал','Ugarit','STATE','богатое портовое царство под верховной властью Хатти','XIV–XIII века до н. э.','UGARIT'),
 ('Амурру','Amurru kingdom','STATE','пограничное царство между Египтом и Хатти','XIV–XIII века до н. э.','AMURRU'),
 ('Шаттиваза','Shattiwaza','PERSON','митаннийский царевич и союзник Суппилулиумы','XIV век до н. э.','WASHUKANNI'),
 ('Чума в Хатти','Hittite plague','EVENT','длительная эпидемия после сирийских войн','XIV век до н. э.','HATTUSA'),
 ('Дело Заннанзы','Zannanza','EVENT','неудачная попытка брака хеттского царевича с египетской царицей','XIV век до н. э.','AMARNA')],
 'archive':[
 ('Деяния Суппилулиумы','Deeds of Suppiluliuma','TEXT','текст Мурсили II о правлении отца','XIV век до н. э.','HATTUSA'),
 ('Договор Шаттивазы','Shattiwaza treaty','TEXT','соглашение о восстановлении зависимого Митанни','XIV век до н. э.','WASHUKANNI'),
 ('Царевич Пияссили','Piyassili','PERSON','сын Суппилулиумы и правитель Каркемиша','XIV век до н. э.','CARCHEMISH'),
 ('Чумные молитвы Мурсили II','Plague prayers of Mursili II','TEXT','царские молитвы о причинах эпидемии','XIV век до н. э.','HATTUSA')]
},
{
 'title':'Договоры и международный порядок','subtitle':'Аккадский язык, вассальные клятвы, браки и подарки связывают дворы великих держав.','description':'Амарнская переписка, договоры, заложники, династические браки, Угарит и Вилуса показывают письменную дипломатию позднего бронзового века.','period':'XIV–XIII века до н. э.','source':SRC_UGARIT,
 'chronology':[('XIV век до н. э.','Хеттские договоры закрепляют сирийских вассалов','textual'),('середина XIV века до н. э.','Амарнская переписка фиксирует конкуренцию великих царей','textual'),('XIII век до н. э.','Договор с Алаксанду связывает Вилусу с Хатти','textual'),('конец XIII века до н. э.','Договор с Шаушкамува отражает новую борьбу с Ассирией','textual')],
 'locations':['HATTUSA','UGARIT','TROY'],'causes':['Невозможность управлять дальними землями только гарнизонами','Потребность закреплять лояльность местных династий','Общий дипломатический язык аккадской клинописи'],'consequences':['Стандартизированные договорные формулы','Сеть вассальных обязанностей и взаимных гарантий','Богатые архивы международной переписки'],
 'story':[
 ('Аккадский язык дипломатии','Akkadian language','TEXT','общий письменный язык международной переписки','II тысячелетие до н. э.','HATTUSA'),
 ('Хеттский вассальный договор','Hittite treaties','TEXT','исторический пролог, обязательства, свидетели-боги и проклятия','XIV–XIII века до н. э.','HATTUSA'),
 ('Великие цари','Great King','CONCEPT','правители, признававшие друг друга равными братьями','XIV–XIII века до н. э.','AMARNA'),
 ('Династические браки','Royal intermarriage','SYSTEM','браки как инструмент союза и статуса','XIV–XIII века до н. э.','HATTUSA'),
 ('Царские дары','Diplomatic gift','SYSTEM','обмен металлами, конями, тканями и престижными предметами','XIV–XIII века до н. э.','UGARIT'),
 ('Амарнские письма о Хатти','Amarna letters','TEXT','переписка, фиксирующая рост хеттской силы','XIV век до н. э.','AMARNA'),
 ('Угаритские архивы','Ugaritic texts','TEXT','договоры, письма и хозяйственные документы вассального царства','XIV–XIII века до н. э.','UGARIT'),
 ('Договор с Алаксанду','Alaksandu treaty','TEXT','соглашение между царём Хатти и правителем Вилусы','XIII век до н. э.','TROY')],
 'archive':[
 ('Договор с Шаушкамува','Treaty of Shaushgamuwa','TEXT','вассальный договор с Амурру и упоминанием Ассирии','XIII век до н. э.','AMURRU'),
 ('Заложники при дворе','Hostage diplomacy','SYSTEM','воспитание родственников вассалов при царском дворе','II тысячелетие до н. э.','HATTUSA'),
 ('Печати Угарита','Ugarit','ARTIFACT','царские и чиновничьи печати международного архива','XIV–XIII века до н. э.','UGARIT'),
 ('Боги-свидетели договора','Hittite treaties','RELIGION','пантеон как гарант клятвы и наказания','II тысячелетие до н. э.','HATTUSA')]
},
{
 'title':'Кадеш и мир с Египтом','subtitle':'Война при Муваталли II сменяется договором Хаттусили III и Рамсеса II.','description':'Перенос двора в Тархунтассу, битва при Кадеше, конкурирующие описания, переворот Хаттусили III, Пудухепа и мирный договор раскрывают зрелую дипломатию.','period':'XIII век до н. э.','source':SRC_BM,
 'chronology':[('ок. 1274 до н. э.','Битва при Кадеше между Муваталли II и Рамсесом II','traditional'),('после смерти Муваталли II','Урхи-Тешуб наследует престол','textual'),('ок. 1267 до н. э.','Хаттусили III захватывает власть','approximate'),('ок. 1259 до н. э.','Египетско-хеттский мирный договор','approximate')],
 'locations':['TARHUNTASSA','KADESH','HATTUSA'],'causes':['Соперничество за Сирию и Амурру','Концентрация армии у южной столицы Муваталли','Потребность Хаттусили III в международном признании'],'consequences':['Неопределённый военный итог Кадеша','Переход к официальному миру и взаимной помощи','Династический брак между Египтом и Хатти'],
 'story':[
 ('Муваталли II','Muwatalli II','PERSON','царь Хатти во время битвы при Кадеше','XIII век до н. э.','TARHUNTASSA'),
 ('Тархунтасса','Tarhuntassa','CITY','южная царская резиденция, точное место которой не найдено','XIII век до н. э.','TARHUNTASSA'),
 ('Битва при Кадеше','Battle of Kadesh','BATTLE','крупное сражение Хатти и Египта у Оронта','традиционно 1274 до н. э.','KADESH'),
 ('Хеттские колесницы','Chariot warfare','WAR','основной ударный компонент армии позднего бронзового века','XIII век до н. э.','KADESH'),
 ('Египетский рассказ о Кадеше','Battle of Kadesh','TEXT','монументальная версия Рамсеса II о сражении','XIII век до н. э.','KADESH'),
 ('Хаттусили III','Hattusili III','PERSON','царь, свергнувший Урхи-Тешуба и заключивший мир с Египтом','XIII век до н. э.','HATTUSA'),
 ('Пудухепа','Puduḫepa','PERSON','тавананна и активная участница международной переписки','XIII век до н. э.','HATTUSA'),
 ('Египетско-хеттский договор','Egyptian–Hittite peace treaty','TEXT','соглашение о мире, границах и взаимной помощи','ок. 1259 до н. э.','HATTUSA')],
 'archive':[
 ('Кадешские рельефы','Battle of Kadesh','ARTIFACT','египетские изображения битвы на храмовых стенах','XIII век до н. э.','KADESH'),
 ('Табличка мирного договора','Egyptian–Hittite peace treaty','ARTIFACT','аккадская версия соглашения из Хаттусы','XIII век до н. э.','HATTUSA'),
 ('Хеттская царевна в Египте','Maathorneferure','PERSON','дочь Хаттусили III, ставшая супругой Рамсеса II','XIII век до н. э.','AMARNA'),
 ('Переписка Пудухепы','Puduḫepa','TEXT','письма царицы египетскому двору','XIII век до н. э.','HATTUSA')]
},
{
 'title':'Последний век и распад державы','subtitle':'Династические расколы, нехватка ресурсов и кризис международной системы разрушают центр.','description':'Тудхалия IV, Курунта, Тархунтасса, поставки зерна, последние письма Угарита, разрушение Хаттусы и продолжение Каркемиша показывают неоднородный конец империи.','period':'конец XIII — начало XII века до н. э.','source':SRC_MET,
 'chronology':[('ок. 1237–1209 до н. э.','Правление Тудхалии IV','approximate'),('XIII век до н. э.','Договоры с Курунтой фиксируют напряжение вокруг Тархунтассы','textual'),('ок. 1200 до н. э.','Угаритские письма сообщают о военной угрозе и нехватке сил','textual'),('начало XII века до н. э.','Столица Хаттуса оставлена и частично разрушена','archaeological')],
 'locations':['HATTUSA','TARHUNTASSA','UGARIT'],'causes':['Конфликт внутри царской династии','Нарушение снабжения и региональных связей','Одновременные кризисы в Сирии, Эгейском мире и Анатолии'],'consequences':['Исчезновение центральной имперской администрации','Разрушение или оставление ряда центров','Продолжение хеттских традиций в Каркемише и сиро-анатолийских царствах'],
 'story':[
 ('Тудхалия IV','Tudḫaliya IV','PERSON','поздний великий царь и участник договоров с Курунтой','XIII век до н. э.','HATTUSA'),
 ('Курунта','Kurunta','PERSON','правитель Тархунтассы и соперник центральной династии','XIII век до н. э.','TARHUNTASSA'),
 ('Тархунтасское царство','Tarhuntassa','STATE','южный центр с особым положением внутри хеттского мира','XIII век до н. э.','TARHUNTASSA'),
 ('Поставки зерна','Late Bronze Age collapse','RESOURCE','срочные перевозки продовольствия в условиях кризиса','конец XIII века до н. э.','UGARIT'),
 ('Последние письма Угарита','Ugarit','TEXT','сообщения о кораблях противника и отсутствии армии','ок. 1200 до н. э.','UGARIT'),
 ('Народы моря','Sea Peoples','PEOPLE','обобщающее название групп, упомянутых в источниках кризиса','конец XIII–XII века до н. э.','UGARIT'),
 ('Оставление Хаттусы','Hattusa','EVENT','уход двора и разрушения в столице','начало XII века до н. э.','HATTUSA'),
 ('Сиро-хеттские государства','Syro-Hittite states','STATE','региональные царства, продолжившие часть лувийских и хеттских традиций','XII–VIII века до н. э.','CARCHEMISH')],
 'archive':[
 ('Бронзовая табличка Курунты','Bronze Tablet of Tudhaliya IV','ARTIFACT','договор о статусе Тархунтассы','XIII век до н. э.','HATTUSA'),
 ('Нишантепские печати последних царей','Nişantepe','ARTIFACT','оттиски династии позднего периода','XIII век до н. э.','HATTUSA'),
 ('Слои разрушения Хаттусы','Hattusa','SITE','археологические следы пожаров, разборки и оставления','начало XII века до н. э.','HATTUSA'),
 ('Каркемиш после империи','Carchemish','STATE','центр династической преемственности после падения Хаттусы','XII век до н. э.','CARCHEMISH')]
}
]

TYPE_LABEL={'PERSON':'личность','CITY':'город','STATE':'государство','EVENT':'событие','DYNASTY':'династия','BUILDING':'сооружение','OFFICE':'должность','PERIOD':'период','SYSTEM':'система','TEXT':'текст','REGION':'регион','RESOURCE':'ресурс','ROUTE':'маршрут','PEOPLE':'народ','WAR':'военное дело','SITE':'место','RELIGION':'религия','CULTURE':'культура','BATTLE':'битва','CONCEPT':'понятие','ARTIFACT':'артефакт','LAW':'правовой текст','RIVER':'река'}

def dump(path,obj):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def svg_card(path,title,subtitle,chapter,index,kind):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
 title=html.escape(title);subtitle=html.escape(subtitle);marks=['⛰','𒀭','♜','⚔','▥','✹','♛','◆','☉','⌁'];acc=['#c58b50','#d2a25c','#b77a43','#ad6745','#c09b65','#ba8f4b','#d0a35f','#b78351','#d5aa6e','#a87149'][chapter-1]
 p.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 900" role="img" aria-label="{title}"><defs><linearGradient id="g" x2="1" y2="1"><stop stop-color="#0a0c0a"/><stop offset=".55" stop-color="#20221a"/><stop offset="1" stop-color="#080806"/></linearGradient><radialGradient id="r"><stop stop-color="{acc}" stop-opacity=".34"/><stop offset="1" stop-color="{acc}" stop-opacity="0"/></radialGradient></defs><rect width="720" height="900" fill="url(#g)"/><circle cx="565" cy="180" r="250" fill="url(#r)"/><path d="M0 670 C140 600 280 720 440 650 S620 600 720 630 V900 H0Z" fill="#070806" opacity=".9"/><path d="M62 112 H658 M62 790 H658" stroke="{acc}" stroke-width="2" opacity=".7"/><text x="62" y="82" fill="{acc}" font-size="21" font-family="Arial" letter-spacing="4">HATTI · ANATOLIA · {chapter:02d}</text><text x="558" y="350" text-anchor="middle" fill="{acc}" font-size="170" font-family="serif" opacity=".82">{marks[chapter-1]}</text><text x="62" y="654" fill="#fff8e9" font-size="43" font-family="Georgia">{title[:30]}</text><text x="62" y="710" fill="#d8cdb8" font-size="23" font-family="Arial">{subtitle[:52]}</text><text x="62" y="832" fill="{acc}" font-size="18" font-family="Arial" letter-spacing="3">{kind.upper()} · CODEX OF HISTORY · {index:02d}</text></svg>''',encoding='utf-8')

def pack_svg():
 p=ROOT/'assets/packs/hittites-pack.svg';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 560"><defs><linearGradient id="g" x2="1" y2="1"><stop stop-color="#070907"/><stop offset=".55" stop-color="#263026"/><stop offset="1" stop-color="#100d08"/></linearGradient><radialGradient id="r"><stop stop-color="#d2a45f" stop-opacity=".55"/><stop offset="1" stop-color="#d2a45f" stop-opacity="0"/></radialGradient></defs><rect width="900" height="560" rx="38" fill="url(#g)"/><circle cx="700" cy="170" r="280" fill="url(#r)"/><path d="M90 410 H810" stroke="#d2a45f" stroke-width="3" opacity=".7"/><text x="90" y="120" fill="#d2a45f" font-size="24" font-family="Arial" letter-spacing="6">ЦАРСТВА БРОНЗОВОГО ВЕКА</text><text x="90" y="215" fill="#fff7e4" font-size="68" font-family="Georgia">Архив Хатти</text><text x="90" y="280" fill="#d9cbb5" font-size="30" font-family="Arial">Хетты и Анатолия</text><text x="700" y="345" text-anchor="middle" fill="#d2a45f" font-size="220" font-family="serif">♜</text><text x="90" y="470" fill="#d2a45f" font-size="22" font-family="Arial" letter-spacing="5">4 КАРТЫ · ОТКРЫТЫЕ ГЛАВЫ</text></svg>''',encoding='utf-8')

story_r=['COMMON','COMMON','UNCOMMON','COMMON','UNCOMMON','RARE','RARE','EPIC']
archive_r=[]
for i in range(10):archive_r.append(['UNCOMMON','RARE','RARE' if i<5 else 'EPIC','MYTHIC' if i in (2,6,9) else 'LEGENDARY'])
story_cards=[];archive_cards=[];nodes=[];lessons={};quizzes={};pools=[];acquisition={};stories={};relations=[];card_points={};map_chapters={};rel_i=1

for ci,ch in enumerate(CHAPTERS,1):
 ch_id=f'HIT_CHAPTER_{ci:02d}';story_ids=[];arch_ids=[]
 for ti,t in enumerate(ch['story'],1):
  cid=f'HIT_S_{ci:02d}_{ti:02d}';story_ids.append(cid);title,original,typ,subtitle,date,point=t;coord,label=P[point]
  card={'id':cid,'type':typ,'title':title,'original':original,'subtitle':subtitle,'era':'Царства бронзового века','region':'Анатолия, Северная Сирия и Верхняя Месопотамия','date':date,'rarity':story_r[ti-1],'difficulty':5+min(4,ci//3),'summary':f'{title} — {subtitle}.','importance':f'Карточка раскрывает главу «{ch["title"]}» через конкретный {TYPE_LABEL.get(typ,"материал")} и связывает его с географией, источниками и институтами Хатти.','facts':[f'Датировка: {date}.',f'Основной смысл: {subtitle}.',f'Выводы проверяются по жанру текста, месту находки и археологическому контексту главы «{ch["title"]}».'],'tags':['Хетты','Анатолия',ch['title'],typ.lower()],'stats':{'influence':5+(ci+ti)%5,'complexity':5+(ti%4),'legacy':4+(ci%6),'military':2+((ci+ti*2)%7),'culture':4+((ci+ti)%6),'politics':4+((ci*2+ti)%6),'religion':2+((ci+ti*3)%7),'economy':3+((ci+ti)%6),'connections':5+((ci+ti)%5)},'loc':{'label':label,'lat':coord[0],'lon':coord[1]},'image':{'local':f'assets/cards/hittites/chapter-{ci:02d}/{cid.lower()}.svg','caption':f'Локальная учебная обложка: {title}','credit':'Codex of History · локальная учебная обложка','source_url':ch['source']['url'],'license':'Project asset','focus':'50% 50%','file':f'{cid.lower()}.svg','kind':'project-cover'},'source':ch['source'],'acquisition':'STORY','campaign':'HITTITES','chapter':ch_id}
  story_cards.append(card);card_points[cid]=point;svg_card(Path(card['image']['local']),title,subtitle,ci,ti,'story')
 for ti,t in enumerate(ch['archive'],1):
  cid=f'HIT_A_{ci:02d}_{ti:02d}';arch_ids.append(cid);title,original,typ,subtitle,date,point=t;coord,label=P[point]
  card={'id':cid,'type':typ,'title':title,'original':original,'subtitle':subtitle,'era':'Царства бронзового века','region':'Анатолия, Северная Сирия и Верхняя Месопотамия','date':date,'rarity':archive_r[ci-1][ti-1],'difficulty':5+min(4,ci//3),'summary':f'{title} — {subtitle}.','importance':f'Архивная карточка дополняет главу «{ch["title"]}» отдельным документом, памятником или спорной проблемой.','facts':[f'Датировка: {date}.',f'Связь с темой: {subtitle}.','Надёжность вывода зависит от происхождения, сохранности и назначения материала.'],'tags':['Хетты','архив',ch['title'],typ.lower()],'stats':{'influence':4+(ci+ti)%6,'complexity':6+(ti%3),'legacy':5+(ci%5),'military':2+((ci+ti)%6),'culture':5+((ci+ti*2)%5),'politics':4+((ci*2+ti)%6),'religion':2+((ci+ti)%7),'economy':3+((ci+ti)%5),'connections':5+((ci+ti)%5)},'loc':{'label':label,'lat':coord[0],'lon':coord[1]},'image':{'local':f'assets/cards/hittites/chapter-{ci:02d}/{cid.lower()}.svg','caption':f'Локальная учебная обложка: {title}','credit':'Codex of History · локальная учебная обложка','source_url':ch['source']['url'],'license':'Project asset','focus':'50% 50%','file':f'{cid.lower()}.svg','kind':'project-cover'},'source':ch['source'],'acquisition':'ARCHIVE','campaign':'HITTITES','chapter':ch_id}
  archive_cards.append(card);card_points[cid]=point;svg_card(Path(card['image']['local']),title,subtitle,ci,ti,'archive');acquisition[cid]={'kind':'ARCHIVE','pool':f'HIT_POOL_{ci:02d}','campaign':'HITTITES'}
 pools.append({'id':f'HIT_POOL_{ci:02d}','campaign':'HITTITES','title':ch['title'],'unlockMission':f'HIT_{ci:02d}_02','cardIds':arch_ids})
 target=arch_ids[-1]
 stories[f'STORY_HIT_{ci:02d}']={'id':f'STORY_HIT_{ci:02d}','cardId':target,'title':f'Архивное дело: {ch["archive"][-1][0]}','subtitle':ch['title'],'rewardXp':125+ci*5,'rewardFragments':13+ci,'steps':[{'type':'SCENE','title':'Материал архива','text':f'Материал «{ch["archive"][-1][0]}» рассматривается отдельно от общего рассказа. Сначала фиксируются происхождение, дата, язык, место находки и назначение.'},{'type':'QUESTION','title':'Проверка источника','question':'Какой шаг должен быть первым?','options':['Определить происхождение и жанр','Сразу восстановить скрытые намерения всех участников','Принять царскую формулу за нейтральный отчёт','Игнорировать археологический слой'],'correct':0,'explanation':'Происхождение и жанр задают границы допустимого вывода.'},{'type':'QUESTION','title':'Граница вывода','question':'Как оформить итог исследования?','options':['Разделить наблюдение, реконструкцию и уверенность','Назвать гипотезу прямым фактом','Считать один документ полной картиной государства','Убрать все оговорки о датировке'],'correct':0,'explanation':'Исторический ответ показывает, на чём держится каждый вывод.'}]}
 for i in range(7):
  relations.append({'id':f'REL_HIT_{rel_i:04d}','source':story_ids[i],'target':story_ids[i+1],'type':'СВЯЗАНО_В_ГЛАВЕ','description':f'{ch["story"][i][0]} связан с темой «{ch["story"][i+1][0]}» внутри главы «{ch["title"]}».','strength':7});rel_i+=1
 for i,a in enumerate(arch_ids):
  relations.append({'id':f'REL_HIT_{rel_i:04d}','source':a,'target':story_ids[min(i*2,7)],'type':'АРХИВНЫЙ_КОНТЕКСТ','description':f'{ch["archive"][i][0]} дополняет сюжетную тему «{ch["story"][min(i*2,7)][0]}».','strength':6});rel_i+=1
 mission_titles=[f'Рассказ: {ch["title"]}',f'Хронология: {ch["period"]}',f'Источник: {ch["archive"][0][0]}',f'Карта: {P[ch["locations"][0]][1]}, {P[ch["locations"][1]][1]} и {P[ch["locations"][2]][1]}','Разбор: причины и последствия',('Экзамен: Хетты и Анатолия' if ci==10 else f'Итог главы: {ch["title"]}')]
 mtypes=['LESSON','TIMELINE','SOURCE','MAP','CAUSE_EFFECT','FINAL'];emojis=['▤','◷','▥','⌖','◆','◎'];card_plan=[[0,1,2],[2,3,4],[3,4,5],[1,5,6],[0,6,7],[7,0,3]];unlock_plan=[[0,1],[2],[3,4],[5],[6],[7]]
 for mi in range(1,7):
  mid=f'HIT_{ci:02d}_{mi:02d}';topic=ch['story'][min(mi-1,7)];node={'id':mid,'type':mtypes[mi-1],'title':mission_titles[mi-1],'description':f'{ch["description"]} Фокус миссии: {mission_titles[mi-1]}.','cards':[story_ids[x] for x in card_plan[mi-1]],'unlockCards':[story_ids[x] for x in unlock_plan[mi-1]],'xp':175+ci*7+mi*5,'emoji':emojis[mi-1],'chapterId':ch_id,'lessonId':mid}
  if mi==2:node['timeline']=[{'id':f't{x}','date':d,'title':t} for x,(d,t,_) in enumerate(ch['chronology'])]
  if mi==4:node['mapTargets']=[{'key':key.lower(),'label':P[key][1],'point':key,'zoom':6 if key not in ('HATTUSA','KANESH','YAZILIKAYA') else 8,'radius':100000} for key in ch['locations']]
  if mi==6:
   node['quiz']=f'QUIZ_HIT_CH{ci}'
   if ci==10:node['campaignExamModules']=[{'id':'QUIZ_HIT_EXAM_MAP','title':'Карта Анатолии и Сирии','icon':'⌖'},{'id':'QUIZ_HIT_EXAM_TIME','title':'Хронология 2000–1200','icon':'◷'},{'id':'QUIZ_HIT_EXAM_SOURCE','title':'Таблички, договоры и рельефы','icon':'▥'},{'id':'QUIZ_HIT_EXAM_SYSTEM','title':'Царь, вассалы и пантеон','icon':'◆'}]
  nodes.append(node)
  activity={'type':'choice','prompt':f'Какой вывод точнее описывает миссию «{mission_titles[mi-1]}»?','options':[ch['subtitle'],'Все изменения объясняются только одним царём','Царские тексты всегда являются нейтральными отчётами','Датировки бронзового века известны до точного дня'],'correct':0,'explanation':ch['description']}
  if mi==2:activity={'type':'timeline'}
  if mi==3:activity={'type':'source','prompt':f'Как нужно работать с материалом «{ch["archive"][0][0]}»?','options':['Определить жанр, дату и происхождение','Считать его полной картиной общества','Игнорировать место находки','Заменить анализ поздней легендой'],'correct':0,'explanation':'Источник сначала помещается в собственный контекст.'}
  if mi==4:activity={'type':'map'}
  if mi==5:activity={'type':'cause-effect'}
  if mi==6:activity={'type':'quiz','quizId':f'QUIZ_HIT_CH{ci}'}
  paras=[
   f'Глава «{ch["title"]}» рассматривает не отдельный эпизод, а связку географии, институтов и источников. {ch["description"]} Для темы «{topic[0]}» важно установить хронологический диапазон, место действия и то, какой материал позволяет делать вывод. Абсолютные даты для хеттской истории часто приблизительны, а порядок событий восстанавливается через сопоставление царских списков, договоров, писем и археологических слоёв.',
   f'Основной материал миссии — {topic[0].lower()}: {topic[3]}. Тексты Хаттусы создавались при дворце и храмах, поэтому отражают задачи администрации, ритуала и царской легитимации. Они содержат конкретные имена и обязанности, но не обязаны передавать позицию подчинённых общин или побеждённых противников. Археологические данные дополняют тексты планировкой городов, хозяйственными комплексами, печатями, оружием и слоями разрушения.',
   f'Политическая система Хатти не была однородной территориальной машиной. Царский двор управлял ядром вокруг Хаттусы, но дальние регионы часто контролировались через вассальные договоры, родственников царя и местные династии. Для миссии «{mission_titles[mi-1]}» нужно определить, кто приносил клятву, кто поставлял войско и дань, кто сохранял местный престол и какие гарантии поддерживали соглашение.',
   f'География объясняет границы власти. В этой главе важны {P[ch["locations"][0]][1]}, {P[ch["locations"][1]][1]} и {P[ch["locations"][2]][1]}. Горные дороги, зимние условия, речные долины и удалённость сирийских владений делали снабжение постоянной задачей. Карта показывает не декоративные точки, а расстояния между столицей, торговыми узлами, вассалами и зонами военной конкуренции.',
   f'Причины процесса нельзя свести к одному приказу. Нужно сопоставить: {ch["causes"][0].lower()}, {ch["causes"][1].lower()} и {ch["causes"][2].lower()}. Следствия также проявлялись не одновременно: {ch["consequences"][0].lower()}, {ch["consequences"][1].lower()} и {ch["consequences"][2].lower()}. Между военной победой и устойчивым административным контролем могли пройти годы.',
   'Особое значение имеет язык источника. В архивах Хаттусы использовались хеттский, аккадский, хурритский, хаттский и лувийский. Выбор языка зависел от жанра и аудитории: международный договор мог быть записан по-аккадски, местный ритуал сохранял чужие формулы, а царские анналы создавали официальную версию прошлого. Поэтому перевод термина всегда требует проверки контекста.',
   f'Итог миссии должен разделять подтверждённое наблюдение и реконструкцию. Опорный материал «{ch["source"]["title"]}» задаёт общую рамку. Корректный ответ называет источник, место, дату или диапазон, затем объясняет связь темы «{topic[0]}» с главой и отдельно отмечает спорные места. Так сохраняется разница между археологическим фактом, царской программой и современной интерпретацией.'
  ]
  lessons[mid]={'id':mid,'title':mission_titles[mi-1],'duration':10+mi,'objectives':[f'объяснить роль темы «{topic[0]}» в главе «{ch["title"]}»','различить археологический факт, официальный текст и реконструкцию','связать дату, географию, институт и последствия'],'story':[{'title':ch['title'],'text':ch['description']},{'title':'Фокус миссии','text':f'{mission_titles[mi-1]}. Главный материал: {topic[0]} — {topic[3]}.'},{'title':'Граница знания','text':'Тексты, археологические слои и позднейшие копии имеют разную доказательную силу.'}],'chronology':[{'date':d,'title':t,'note':f'{t}. Связь с миссией проверяется по жанру и контексту источника.','certainty':c} for d,t,c in ch['chronology']],'concepts':[{'term':x[0],'definition':x[3]} for x in ch['story'][:3]],'causeEffect':{'causes':ch['causes'],'consequences':ch['consequences']},'activity':activity,'sources':[ch['source']],'theory':{'title':mission_titles[mi-1],'readingMinutes':7,'lead':f'{ch["description"]} Основной вопрос миссии — {topic[0].lower()}.','paragraphs':paras,'historicityNotes':['Даты правлений и походов приблизительны и зависят от принятой хронологии.','Царские анналы и договоры выражают интересы двора.','Археологический слой не всегда позволяет назвать конкретного виновника разрушения.'],'sources':[ch['source']],'license':'Авторский учебный текст Codex of History.','checkedAt':CHECKED}}
 map_chapters[ch_id]={'title':ch['title'],'center':P[ch['locations'][0]][0],'zoom':5}
 qs=[]
 for qi in range(4):
  correct=ch['story'][qi][0];distr=[ch['story'][(qi+j+1)%8][0] for j in range(3)];pos=(ci+qi)%4;opts=distr[:];opts.insert(pos,correct);qs.append({'text':f'Какой термин соответствует описанию: «{ch["story"][qi][3]}»?','options':opts,'correct':pos,'explanation':f'{correct}: {ch["story"][qi][3]}.'})
 pos=(ci+4)%4;opts=['Считать царский текст полной картиной общества','Игнорировать язык документа','Выбрать дату без диапазона'];opts.insert(pos,'Определить происхождение, жанр и дату источника');qs.append({'text':f'Какой способ работы нужен в главе «{ch["title"]}»?','options':opts,'correct':pos,'explanation':'Происхождение и жанр определяют предел вывода.'})
 pos=(ci+5)%4;opts=['Все процессы вызваны одним походом','Археология полностью заменяет тексты','Все регионы управлялись одинаково'];opts.insert(pos,ch['subtitle']);qs.append({'text':f'Какой итог главы «{ch["title"]}» наиболее точен?','options':opts,'correct':pos,'explanation':ch['description']})
 quizzes[f'QUIZ_HIT_CH{ci}']={'id':f'QUIZ_HIT_CH{ci}','title':f'Глава {ci}: {ch["title"]}','passPercent':70,'questions':qs}

chapters=[{'id':f'HIT_CHAPTER_{i:02d}','number':i,'title':ch['title'],'subtitle':ch['subtitle'],'description':ch['description'],'missionIds':[f'HIT_{i:02d}_{x:02d}' for x in range(1,7)]} for i,ch in enumerate(CHAPTERS,1)]
for source,target,desc in [
 ('BAB_S_07_02','HIT_S_02_01','Каниш из вавилонской кампании становится центром отдельного разбора староассирийской торговли.'),
 ('BAB_S_08_08','HIT_S_04_03','Хеттский поход завершает историю первой вавилонской династии.'),
 ('EMN_S_08_06','HIT_S_07_02','Митанни оказывается между египетской и хеттской экспансией.'),
 ('EMN_S_09_07','HIT_S_08_06','Амарнские письма фиксируют рост Хатти как великой державы.'),
 ('EMN_S_10_03','HIT_S_09_03','Кадеш изучается с египетской и хеттской стороны.'),
 ('EMN_S_10_04','HIT_S_09_08','Один мирный договор связывает две региональные кампании.'),
 ('BAB_S_03_05','HIT_S_03_07','Ямхад становится целью ранней хеттской экспансии.'),
 ('SYS_CIV_002','HIT_S_08_01','Письменная дипломатия бронзового века работает через аккадский язык.')]:
 relations.append({'id':f'REL_HIT_{rel_i:04d}','source':source,'target':target,'type':'МЕЖКАМПАНИЙНАЯ_СВЯЗЬ','description':desc,'strength':8});rel_i+=1

exam_specs={
'QUIZ_HIT_EXAM_MAP':('Карта Анатолии и Сирии',[
 ('Где находилась столица Хеттского царства?',['Хаттуса','Угарит','Кадеш','Ашшур'],0,'Хаттуса находилась в центральной Анатолии.'),
 ('Какой центр связан со староассирийским карумом?',['Алеппо','Каниш','Вавилон','Каркемиш'],1,'Карум Каниш раскопан в Кюльтепе.'),
 ('Какой город был главным хеттским центром управления Сирией?',['Аладжа-Хююк','Аринна','Каркемиш','Троя'],2,'Каркемиш управлялся царевичами хеттской династии.'),
 ('Где произошло сражение с армией Рамсеса II?',['Куссара','Язылыкая','Тархунтасса','Кадеш'],3,'Кадеш находился на Оронте.'),
 ('Какой маршрут соединял ядро Хатти с сирийскими вассалами?',['Дороги через Киликийские ворота и Северную Сирию','Только путь по Нилу','Тигр без сухопутных переходов','Морской путь вокруг Африки'],0,'Снабжение шло через горные и сирийские маршруты.')]),
'QUIZ_HIT_EXAM_TIME':('Хронология 2000–1200',[
 ('Какое явление было раньше остальных?',['Староассирийский карум Каниш','Битва при Кадеше','Договор Хаттусили III','Разрушение Угарита'],0,'Карум Каниш относится к началу II тысячелетия до н. э.'),
 ('Что произошло после похода Мурсили I на Вавилон?',['Расцвет карума Каниш','Дворцовые кризисы Старого царства','Создание Амарнского архива','Битва при Кадеше'],1,'После убийства Мурсили последовала серия переворотов.'),
 ('Какое событие относится к XIV веку до н. э.?',['Указ Телепину','Падение Хаттусы','Империя Суппилулиумы I','Карум Каниш'],2,'Суппилулиума I правил в XIV веке до н. э.'),
 ('Что ближе всего к концу империи?',['Хаттусили I','Мурсили I','Суппилулиума I','Последние письма Угарита'],3,'Письма относятся к кризису около 1200 года до н. э.'),
 ('Какой порядок верен?',['Каниш → Хаттусили I → Суппилулиума I → Кадеш','Кадеш → Каниш → Хаттусили I → Суппилулиума I','Суппилулиума I → Мурсили I → Каниш → Кадеш','Хаттусили III → Каниш → Хаттусили I → Кадеш'],0,'Это общий порядок кампании.')]),
'QUIZ_HIT_EXAM_SOURCE':('Таблички, договоры и рельефы',[
 ('Что прежде всего показывает царская аннала?',['Официальную версию царских деяний','Полную позицию всех вассалов','Нейтральную статистику населения','Точный календарь каждого марша'],0,'Анналы создавались при дворе.'),
 ('Почему таблички Каниша особенно важны?',['Они написаны по-латыни','Они фиксируют сделки и семейную переписку купцов','Они являются поздними легендами','Они описывают только храмовые ритуалы'],1,'Это повседневный коммерческий архив.'),
 ('Какой материал закрепляет обязанности вассала?',['Погребальный штандарт','Слой пожара','Письменный договор','Случайная находка оружия'],2,'Договор перечисляет обязательства и санкции.'),
 ('Что нельзя автоматически вывести из разрушения Хаттусы?',['Факт пожара в части города','Изменение использования квартала','Примерное время оставления','Имя конкретной группы, уничтожившей столицу'],3,'Имя виновника требует независимых данных.'),
 ('Как оформить спорную локализацию Тархунтассы?',['Указать приблизительную область и степень уверенности','Поставить точную точку без оговорки','Заменить карту легендой','Игнорировать спор'],0,'Неопределённость должна быть видна.')]),
'QUIZ_HIT_EXAM_SYSTEM':('Царь, вассалы и пантеон',[
 ('Как Хатти управляла Сирией?',['Через договоры, местных царей и династических наместников','Только прямыми поселениями из Хаттусы','Без письменных обязательств','Только ежегодным грабежом'],0,'Империя сочетала вассалов и царевичей.'),
 ('Какую роль играла тавананна?',['Не имела публичных функций','Сохраняла высокий культовый и династический статус','Была только названием города','Командовала каждым гарнизоном'],1,'Титул царицы имел самостоятельное значение.'),
 ('Почему пантеон называли «тысячей богов»?',['В царстве запрещали местные культы','Все боги были одним божеством','Система включала культы разных регионов','Число было точной переписью храмов'],2,'Хеттская религия включала местные и заимствованные культы.'),
 ('Что показывает поздний кризис?',['Центр контролировал всё без перебоев','Одно сражение уничтожило все города одновременно','Архивы перестали существовать за век до кризиса','Династические, снабженческие и внешние проблемы усиливали друг друга'],3,'Распад имел несколько причин.'),
 ('Какой общий вывод точнее?',['Хеттская держава держалась на географии, письме, династии, договорах и ритуале','Историю определяли только колесницы','Все тексты одинаково надёжны','Анатолия была культурно однородной'],0,'Кампания требует многопричинного объяснения.')])}
for qid,(title,raw) in exam_specs.items():quizzes[qid]={'id':qid,'title':title,'passPercent':70,'questions':[{'text':a,'options':b,'correct':c,'explanation':d} for a,b,c,d in raw]}

campaign={'id':'HITTITES','title':'Хетты и Анатолия','description':'От многоязычной Анатолии и карума Каниш до империи Хаттусы, Кадеша и кризиса около 1200 года до н. э.','difficulty':7,'chapters':chapters,'nodes':nodes,'eraLayer':{'period':'ок. 2000–1200 до н. э.','summary':'Кампания связывает торговые колонии, становление царства, имперскую дипломатию и распад позднего бронзового века.','phases':[{'id':'ORIGINS','title':'Торговля и раннее царство','date':'ок. 2000–1500 до н. э.','chapters':[1,2,3,4]},{'id':'EMPIRE','title':'Империя Хаттусы','date':'ок. 1500–1270 до н. э.','chapters':[5,6,7,8]},{'id':'LATE','title':'Кадеш и последний век','date':'ок. 1270–1200 до н. э.','chapters':[9,10]}]}}
pools_payload={'campaignId':'HITTITES','campaigns':{'HITTITES':{'id':'HITTITES','title':'Хетты и Анатолия','active':True,'status':'STARTED'}},'pools':pools,'acquisition':acquisition}
map_payload={'points':{k:v[0] for k,v in P.items()},'regions':{},'cardPoints':card_points,'chapters':map_chapters,'missionCenter':[38.7,35.2],'missionZoom':5}

dump(Path('data/cards/hittites/story.json'),story_cards);dump(Path('data/cards/hittites/archive.json'),archive_cards);dump(Path('data/campaigns/hittites/campaign.json'),campaign);dump(Path('data/campaigns/hittites/pools.json'),pools_payload);dump(Path('data/lessons/hittites/campaign.json'),lessons);dump(Path('data/quizzes/hittites/campaign.json'),quizzes);dump(Path('data/stories/hittites/personal.json'),stories);dump(Path('data/maps/hittites.json'),map_payload);dump(Path('data/core/relations-v33-hittites.json'),relations);pack_svg()
print(f'generated {len(story_cards)+len(archive_cards)} cards, {len(nodes)} missions, {len(lessons)} lessons, {len(quizzes)} quizzes, {len(relations)} relations')
