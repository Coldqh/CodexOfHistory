#!/usr/bin/env python3
from __future__ import annotations
import json, html, textwrap
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
VERSION='3.2.0'
CHECKED='2026-07-13'

SRC_MIDDLE={"title":"The Met: Egypt in the Middle Kingdom","url":"https://www.metmuseum.org/essays/egypt-in-the-middle-kingdom-2030-1640-b-c","type":"museum"}
SRC_NEW={"title":"The Met: Egypt in the New Kingdom","url":"https://www.metmuseum.org/essays/egypt-in-the-new-kingdom-ca-1550-1070-b-c","type":"museum"}
SRC_HAT={"title":"The Met: Queen Hatshepsut Restored","url":"https://www.metmuseum.org/essays/queen-hatshepsut-restored","type":"museum"}
SRC_AMARNA={"title":"The Met: Art, Architecture, and the City in the Reign of Akhenaten","url":"https://www.metmuseum.org/essays/art-architecture-and-the-city-in-the-reign-of-amenhotep-iv-akhenaten-ca-13531336-b-c","type":"museum"}
SRC_LETTERS={"title":"The Met: The Amarna Letters","url":"https://www.metmuseum.org/essays/the-amarna-letters","type":"museum"}
SRC_BM={"title":"British Museum: Timeline of ancient Egypt","url":"https://www.britishmuseum.org/learn/schools/ages-7-11/ancient-egypt/timeline-ancient-egypt","type":"museum"}
SRC_THIRD={"title":"The Met: Egypt in the Third Intermediate Period","url":"https://www.metmuseum.org/essays/egypt-in-the-third-intermediate-period-1070-712-b-c","type":"museum"}

P={
'THEBES':([25.7188,32.6573],'Фивы'),
'DEIR_BAHRI':([25.7382,32.6066],'Дейр-эль-Бахри'),
'HERAKLEOPOLIS':([29.086,30.934],'Гераклеополь'),
'ABYDOS':([26.185,31.918],'Абидос'),
'LISHT':([29.570,31.230],'Лишт'),
'ITJTAWY':([29.55,31.15],'Иттауи, приблизительное положение'),
'BENI_HASAN':([27.930,30.877],'Бени-Хасан'),
'LAHUN':([29.238,30.970],'Лахун'),
'FAIYUM':([29.308,30.842],'Файюм'),
'SEMNA':([21.483,30.970],'Семна'),
'BUHEN':([21.917,31.283],'Бухен'),
'ELEPHANTINE':([24.089,32.889],'Элефантина'),
'AVARIS':([30.787,31.821],'Аварис / Телль-эль-Дабъа'),
'THEBES_NORTH':([25.7188,32.6573],'Фивы'),
'SHARUHEN':([31.25,34.3],'Шарухен, приблизительное положение'),
'KARNAK':([25.7188,32.6573],'Карнак'),
'KUMMA':([21.56,30.96],'Кумма'),
'GEBEL_BARKAL':([18.537,31.838],'Джебель-Баркал'),
'DEIR_MEDINA':([25.728,32.601],'Дейр-эль-Медина'),
'PUNT':([13.5,42.5],'Пунт, условная область'),
'MEGIDDO':([32.584,35.184],'Мегиддо'),
'KADESH':([34.557,36.519],'Кадеш'),
'JOPPA':([32.055,34.752],'Яффа'),
'AMARNA':([27.644,30.896],'Ахетатон / Амарна'),
'MEMPHIS':([29.849,31.254],'Мемфис'),
'PI_RAMESSES':([30.80,31.84],'Пер-Рамсес'),
'ABU_SIMBEL':([22.337,31.626],'Абу-Симбел'),
'MEDINET_HABU':([25.719,32.601],'Мединет-Абу'),
}

# topic: title, original, type, subtitle, date, point
CHAPTERS=[
{
 'title':'Новое объединение Египта','subtitle':'Фиванские правители завершают раскол и создают новую монархию.','description':'Ментухотеп II, борьба с Гераклеополем, Фивы и перестройка царской власти после Первого переходного периода.','period':'ок. 2055–1985 до н. э.','source':SRC_MIDDLE,
 'chronology':[('ок. 2125 до н. э.','Фиванская линия Интефов укрепляется','approximate'),('ок. 2055 до н. э.','Ментухотеп II объединяет Египет','approximate'),('начало XX века до н. э.','Фивы становятся центром новой монархии','mixed'),('ок. 1985 до н. э.','Переход к XII династии','approximate')],
 'locations':['THEBES','HERAKLEOPOLIS','DEIR_BAHRI'],
 'causes':['Ослабление власти Гераклеополя','Рост военных и хозяйственных ресурсов Фив','Контроль путей между Верхним и Нижним Египтом'],
 'consequences':['Возвращение единой царской администрации','Фиванская модель легитимности','Переход к государству XII династии'],
 'story':[
 ('Ментухотеп II','Mentuhotep II','PERSON','фиванский царь, связанный с новым объединением Египта','ок. 2061–2010 до н. э.','DEIR_BAHRI'),
 ('Фивы Среднего царства','Thebes, Egypt','CITY','южный центр, превратившийся в столицу объединения','конец III — начало II тысячелетия до н. э.','THEBES'),
 ('Гераклеопольское царство','Heracleopolis Magna','STATE','северный соперник фиванских правителей','XXII–XXI века до н. э.','HERAKLEOPOLIS'),
 ('Новое объединение Египта','Middle Kingdom of Egypt','EVENT','завершение политического раскола Первого переходного периода','ок. 2055 до н. э.','THEBES'),
 ('XI династия','Eleventh Dynasty of Egypt','DYNASTY','фиванская царская линия, открывшая Среднее царство','ок. 2134–1991 до н. э.','THEBES'),
 ('Комплекс Ментухотепа II','Mortuary Temple of Mentuhotep II','BUILDING','царский памятник у скал Дейр-эль-Бахри','начало XX века до н. э.','DEIR_BAHRI'),
 ('Номархи после раскола','Nomarch','OFFICE','региональные элиты, встроенные в новую систему власти','XXI–XX века до н. э.','BENI_HASAN'),
 ('Среднее царство','Middle Kingdom of Egypt','PERIOD','период нового единства и перестройки институтов','ок. 2055–1650 до н. э.','THEBES')],
 'archive':[
 ('Интеф II','Intef II','PERSON','фиванский правитель, расширявший влияние на север','ок. 2112–2063 до н. э.','THEBES'),
 ('Стела Тжетжи','Stela of Tjetji','ARTIFACT','частный памятник участника фиванского объединения','ок. 2050 до н. э.','THEBES'),
 ('Сафф-гробницы Эль-Тарифа','El-Tarif','SITE','рядовые скальные гробницы ранних фиванских правителей','XI династия','THEBES'),
 ('Модели из гробницы Мекетре','Tomb of Meketre','ARTIFACT','деревянные модели хозяйства и транспорта','ок. 1981–1975 до н. э.','THEBES')]
},
{
 'title':'Государство XII династии','subtitle':'Новая резиденция, чиновники и царская идеология укрепляют монархию.','description':'Аменемхет I, Иттауи, Сенусерт I, провинциальная администрация, литература и дискуссия о соправлении.','period':'ок. 1985–1773 до н. э.','source':SRC_MIDDLE,
 'chronology':[('ок. 1985 до н. э.','Аменемхет I основывает XII династию','approximate'),('начало XX века до н. э.','Царская резиденция переносится в район Иттауи','mixed'),('ок. 1965–1920 до н. э.','Правление Сенусерта I','approximate'),('XIX век до н. э.','Укрепление административной сети XII династии','mixed')],
 'locations':['ITJTAWY','LISHT','BENI_HASAN'],
 'causes':['Необходимость контролировать Верхний и Нижний Египет','Опора на профессиональную администрацию','Перераспределение отношений с провинциальной знатью'],
 'consequences':['Стабильная царская резиденция у Файюма','Развитие письменной бюрократии','Расцвет литературы и частных памятников'],
 'story':[
 ('Аменемхет I','Amenemhat I','PERSON','основатель XII династии и новой царской резиденции','ок. 1985–1955 до н. э.','LISHT'),
 ('Иттауи','Itjtawy','CITY','царская резиденция с неустановленным точным местоположением','XX–XVIII века до н. э.','ITJTAWY'),
 ('Сенусерт I','Senusret I','PERSON','царь, расширивший строительство и административный контроль','ок. 1965–1920 до н. э.','LISHT'),
 ('XII династия','Twelfth Dynasty of Egypt','DYNASTY','главная царская линия Среднего царства','ок. 1985–1773 до н. э.','LISHT'),
 ('Визирь Среднего царства','Vizier (Ancient Egypt)','OFFICE','главный координатор суда, архивов и управления','II тысячелетие до н. э.','ITJTAWY'),
 ('Провинциальная администрация','Nomarch','SYSTEM','связь двора с номами и местными элитами','XX–XIX века до н. э.','BENI_HASAN'),
 ('Повесть о Синухете','Story of Sinuhe','TEXT','литературный текст о бегстве, службе и возвращении','начало II тысячелетия до н. э.','LISHT'),
 ('Соправление царей','Coregency','CONCEPT','спорная модель передачи власти внутри XII династии','XX–XIX века до н. э.','ITJTAWY')],
 'archive':[
 ('Поучение Аменемхета','Instructions of Amenemhat','TEXT','царское наставление, оформленное как речь погибшего правителя','начало II тысячелетия до н. э.','LISHT'),
 ('Белая капелла Сенусерта I','White Chapel','BUILDING','юбилейная капелла с перечнем египетских номов','ок. 1950 до н. э.','KARNAK'),
 ('Гробницы Бени-Хасана','Beni Hasan','SITE','провинциальные гробницы с биографиями и сценами труда','XX–XIX века до н. э.','BENI_HASAN'),
 ('Лахунские папирусы','Kahun Papyri','TEXT','хозяйственные, медицинские и административные документы','ок. 1800 до н. э.','LAHUN')]
},
{
 'title':'Нубия, Файюм и ресурсы','subtitle':'Граница, крепости и хозяйственные проекты расширяют возможности государства.','description':'Сенусерт III, Семна, Бухен, нубийское золото, Файюм, экспедиционные маршруты и пограничные тексты.','period':'XIX–XVIII века до н. э.','source':SRC_MIDDLE,
 'chronology':[('ок. 1878 до н. э.','Начало правления Сенусерта III','approximate'),('XIX век до н. э.','Строительство и усиление крепостей у второго порога','mixed'),('XIX–XVIII века до н. э.','Развитие Файюмского региона','mixed'),('конец XII династии','Расширение хозяйственной и пограничной документации','mixed')],
 'locations':['SEMNA','BUHEN','FAIYUM'],
 'causes':['Потребность в золоте и южных товарах','Необходимость контролировать движение по Нилу','Стремление увеличить земледельческие ресурсы'],
 'consequences':['Сеть крепостей в Нижней Нубии','Рост роли царских экспедиций','Более плотное хозяйственное освоение Файюма'],
 'story':[
 ('Сенусерт III','Senusret III','PERSON','царь, связанный с нубийской границей и административными изменениями','ок. 1878–1840 до н. э.','SEMNA'),
 ('Крепость Семна','Semna (Nubia)','BUILDING','пограничный комплекс у второго порога Нила','XIX век до н. э.','SEMNA'),
 ('Крепость Бухен','Buhen','BUILDING','укреплённый центр Нижней Нубии','Среднее царство','BUHEN'),
 ('Нижняя Нубия','Lower Nubia','REGION','зона крепостей, торговли и египетского военного присутствия','II тысячелетие до н. э.','BUHEN'),
 ('Нубийское золото','Gold mining in ancient Egypt','RESOURCE','важный ресурс царской экономики и внешней политики','Среднее и Новое царства','SEMNA'),
 ('Файюмские проекты','Faiyum Oasis','SYSTEM','земледельческое освоение региона у озера Моэрис','XIX–XVIII века до н. э.','FAIYUM'),
 ('Экспедиционные пути','Wadi Hammamat','ROUTE','дороги к каменоломням, Красному морю и южным землям','II тысячелетие до н. э.','ELEPHANTINE'),
 ('Пограничные стелы Сенусерта III','Semna stelae','TEXT','царские тексты, определявшие режим южной границы','XIX век до н. э.','SEMNA')],
 'archive':[
 ('Семненские донесения','Semna Despatches','TEXT','сообщения о движении людей через нубийскую границу','XII династия','SEMNA'),
 ('Миргисса','Mirgissa','SITE','крепость и поселение в системе Нижней Нубии','Среднее царство','SEMNA'),
 ('Мединет-Мади','Medinet Madi','BUILDING','храмовый комплекс Файюмского региона','XII династия','FAIYUM'),
 ('Надписи Вади-Хаммамат','Wadi Hammamat','TEXT','следы царских экспедиций к камню и Красному морю','Среднее царство','ELEPHANTINE')]
},
{
 'title':'Гиксосы и разделённый Египет','subtitle':'Дельта, Фивы и новые политические силы образуют сложную систему.','description':'Второй переходный период, Аварис, XV династия, западноазиатские связи, колесницы и фиванское сопротивление.','period':'ок. 1650–1550 до н. э.','source':SRC_BM,
 'chronology':[('ок. 1650 до н. э.','Аварис становится центром XV династии','approximate'),('XVII–XVI века до н. э.','Гиксосские правители контролируют значительную часть Дельты','mixed'),('середина XVI века до н. э.','Фиванская XVII династия усиливает сопротивление','approximate'),('ок. 1550 до н. э.','Переход к войне за новое объединение','approximate')],
 'locations':['AVARIS','THEBES','MEMPHIS'],
 'causes':['Ослабление позднего Среднего царства','Рост населения и сетей восточной Дельты','Политическая раздробленность региональных династий'],
 'consequences':['Возникновение гиксосского царства в Аварисе','Военное соперничество Фив и Дельты','Расширение египетских контактов с Левантом'],
 'story':[
 ('Второй переходный период','Second Intermediate Period of Egypt','PERIOD','время нескольких центров власти между Средним и Новым царствами','ок. 1700–1550 до н. э.','AVARIS'),
 ('Аварис','Avaris','CITY','крупный город восточной Дельты и столица XV династии','XVII–XVI века до н. э.','AVARIS'),
 ('Гиксосы','Hyksos','PEOPLE','правящие группы западноазиатского происхождения в северном Египте','ок. 1650–1550 до н. э.','AVARIS'),
 ('XV династия','Fifteenth Dynasty of Egypt','DYNASTY','царская линия гиксосских правителей Авариса','XVII–XVI века до н. э.','AVARIS'),
 ('Колесница и составной лук','Chariotry in ancient Egypt','WAR','военные технологии, ставшие заметными в переходный период','II тысячелетие до н. э.','AVARIS'),
 ('Хиан','Khyan','PERSON','гиксосский царь, известный по находкам в разных регионах','XVII век до н. э.','AVARIS'),
 ('Апопи','Apepi','PERSON','поздний правитель XV династии и противник Фив','XVI век до н. э.','AVARIS'),
 ('XVII династия Фив','Seventeenth Dynasty of Egypt','DYNASTY','южная линия правителей, начавшая войну за объединение','XVI век до н. э.','THEBES')],
 'archive':[
 ('Фрески Телль-эль-Дабъа','Minoan frescoes at Tell el-Dab’a','ARTIFACT','росписи, указывающие на связи Дельты с Эгейским миром','XVIII династия, с более ранним контекстом Авариса','AVARIS'),
 ('Математический папирус Ринда','Rhind Mathematical Papyrus','TEXT','копия математического текста с исторической заметкой','ок. 1550 до н. э.','AVARIS'),
 ('Стелы Камоса','Kamose stelae','TEXT','царские сообщения о войне против Авариса','середина XVI века до н. э.','THEBES'),
 ('Мумия Секененра Таа','Seqenenre Tao','ARTIFACT','останки фиванского царя со следами тяжёлых ранений','XVI век до н. э.','THEBES')]
},
{
 'title':'Изгнание гиксосов','subtitle':'Фиванская династия захватывает Аварис и начинает Новое царство.','description':'Секененра Таа, Камос, Яхмос I, Аварис, Шарухен и военные биографии участников кампаний.','period':'середина XVI века до н. э.','source':SRC_BM,
 'chronology':[('середина XVI века до н. э.','Секененра Таа вступает в конфликт с севером','approximate'),('ок. 1555 до н. э.','Камос ведёт походы к Дельте','approximate'),('ок. 1550 до н. э.','Яхмос I захватывает Аварис','approximate'),('после падения Авариса','Египетские войска осаждают Шарухен','traditional')],
 'locations':['THEBES','AVARIS','SHARUHEN'],
 'causes':['Военное усиление фиванской XVII династии','Контроль речных путей к Дельте','Стремление восстановить единую царскую власть'],
 'consequences':['Падение гиксосской столицы','Основание XVIII династии','Начало долговременной экспансии Египта'],
 'story':[
 ('Секененра Таа','Seqenenre Tao','PERSON','фиванский царь, погибший в период войны с гиксосами','XVI век до н. э.','THEBES'),
 ('Камос','Kamose','PERSON','последний царь XVII династии и участник наступления на север','ок. 1555–1550 до н. э.','THEBES'),
 ('Яхмос I','Ahmose I','PERSON','основатель XVIII династии и победитель Авариса','ок. 1550–1525 до н. э.','THEBES'),
 ('Захват Авариса','Siege of Avaris','EVENT','решающий этап ликвидации гиксосского царства','середина XVI века до н. э.','AVARIS'),
 ('Осада Шарухена','Sharuhen','EVENT','преследование противников в Южном Леванте','XVI век до н. э.','SHARUHEN'),
 ('Автобиография Яхмоса, сына Абаны','Ahmose, son of Ebana','TEXT','военная биография участника кампаний объединения','XVI век до н. э.','THEBES'),
 ('XVIII династия','Eighteenth Dynasty of Egypt','DYNASTY','царская линия, открывшая Новое царство','ок. 1550–1292 до н. э.','THEBES'),
 ('Начало Нового царства','New Kingdom of Egypt','PERIOD','новая политическая система после объединения','ок. 1550 до н. э.','THEBES')],
 'archive':[
 ('Стела Бури Яхмоса','Tempest Stele','TEXT','царская надпись о разрушительном природном явлении и восстановлении','XVI век до н. э.','THEBES'),
 ('Яхмос-Нефертари','Ahmose-Nefertari','PERSON','царица и важная фигура ранней XVIII династии','XVI век до н. э.','THEBES'),
 ('Шабти Яхмоса I','Shabti of Ahmose I','ARTIFACT','один из редких сохранившихся образов основателя XVIII династии','XVI век до н. э.','THEBES'),
 ('Золото доблести','Gold of Honour','ARTIFACT','награда, упоминаемая в военных биографиях Нового царства','XVI–XIII века до н. э.','THEBES')]
},
{
 'title':'Рождение египетской империи','subtitle':'Армия, Нубия и походы в Азию превращают Египет в державу.','description':'Аменхотеп I, Тутмос I, Карнак, Долина царей, наместник Куша, армия и ранняя экспансия XVIII династии.','period':'ок. 1525–1479 до н. э.','source':SRC_NEW,
 'chronology':[('ок. 1525–1504 до н. э.','Правление Аменхотепа I','approximate'),('начало XV века до н. э.','Тутмос I ведёт походы в Нубию и Сирию','mixed'),('XV век до н. э.','Укрепляется администрация Куша','mixed'),('ранняя XVIII династия','Формируется царский некрополь в Долине царей','mixed')],
 'locations':['KARNAK','GEBEL_BARKAL','DEIR_MEDINA'],
 'causes':['Военный опыт войн за объединение','Потребность контролировать Нубию и торговые пути','Ресурсы централизованной царской власти'],
 'consequences':['Появление постоянной военной элиты','Расширение границ до Нубии и Сирии','Рост храмового хозяйства Амона'],
 'story':[
 ('Аменхотеп I','Amenhotep I','PERSON','царь раннего Нового царства и покровитель фиванской некропольной традиции','ок. 1525–1504 до н. э.','THEBES'),
 ('Тутмос I','Thutmose I','PERSON','царь, совершивший походы далеко на юг и север','ок. 1504–1492 до н. э.','KARNAK'),
 ('Карнакский храм','Karnak','BUILDING','главный культовый комплекс Амона и место царских памятников','Новое царство','KARNAK'),
 ('Наместник Куша','Viceroy of Kush','OFFICE','царский чиновник, управлявший египетскими владениями на юге','Новое царство','GEBEL_BARKAL'),
 ('Египетская Нубия','Nubia under Egyptian rule','REGION','территория гарнизонов, храмов и добычи ресурсов','XVI–XI века до н. э.','GEBEL_BARKAL'),
 ('Поход к Евфрату','Thutmose I','EVENT','символ ранней северной экспансии XVIII династии','начало XV века до н. э.','KADESH'),
 ('Долина царей','Valley of the Kings','SITE','царский некрополь Нового царства на западном берегу Фив','XVI–XI века до н. э.','DEIR_MEDINA'),
 ('Армия и колесничие','Military of ancient Egypt','WAR','профессионализирующаяся военная система Нового царства','XVI–XI века до н. э.','KARNAK')],
 'archive':[
 ('Гробница KV38','KV38','SITE','царская гробница, связанная с Тутмосом I','XV век до н. э.','DEIR_MEDINA'),
 ('Надпись Яхмоса, сына Абаны','Ahmose, son of Ebana','TEXT','биография, показывающая карьеру военного служилого человека','XVI век до н. э.','THEBES'),
 ('Стела Тутмоса I у Джебель-Баркала','Jebel Barkal','TEXT','царская надпись о южной экспансии','XV век до н. э.','GEBEL_BARKAL'),
 ('Основание Дейр-эль-Медины','Deir el-Medina','SITE','поселение мастеров царских гробниц','ранняя XVIII династия','DEIR_MEDINA')]
},
{
 'title':'Хатшепсут','subtitle':'Царица принимает полную царскую титулатуру и строит собственную программу власти.','description':'Регентство, коронация Хатшепсут, Дейр-эль-Бахри, Пунт, Сененмут, обелиски и последующее уничтожение части изображений.','period':'ок. 1479–1458 до н. э.','source':SRC_HAT,
 'chronology':[('ок. 1479 до н. э.','Хатшепсут становится регентом при Тутмосе III','approximate'),('первые годы совместного правления','Хатшепсут принимает полную царскую титулатуру','mixed'),('ок. 1470-е годы до н. э.','Экспедиция в Пунт отражается в рельефах','approximate'),('после 1458 до н. э.','Часть изображений и имён Хатшепсут уничтожается','mixed')],
 'locations':['DEIR_BAHRI','KARNAK','PUNT'],
 'causes':['Малолетство Тутмоса III','Высокий статус царской супруги и дочери царя','Поддержка двора и жречества Амона'],
 'consequences':['Уникальная модель совместного царствования','Большая строительная программа','Поздняя переработка памяти о правлении'],
 'story':[
 ('Хатшепсут','Hatshepsut','PERSON','женщина-фараон XVIII династии','ок. 1479–1458 до н. э.','DEIR_BAHRI'),
 ('Регентство при Тутмосе III','Hatshepsut','SYSTEM','переход от опеки над царём к собственному царствованию','XV век до н. э.','THEBES'),
 ('Царская титулатура Хатшепсут','Ancient Egyptian royal titulary','CONCEPT','оформление власти через имена, короны и ритуальные образы','XV век до н. э.','KARNAK'),
 ('Джесер-Джесеру','Mortuary Temple of Hatshepsut','BUILDING','поминальный храм Хатшепсут в Дейр-эль-Бахри','XV век до н. э.','DEIR_BAHRI'),
 ('Экспедиция в Пунт','Land of Punt','EVENT','торговая экспедиция, показанная на храмовых рельефах','XV век до н. э.','PUNT'),
 ('Сененмут','Senenmut','PERSON','высокопоставленный чиновник и управляющий строительными проектами','XV век до н. э.','DEIR_BAHRI'),
 ('Обелиски Хатшепсут','Obelisks of Hatshepsut','BUILDING','монументы в Карнаке, посвящённые Амону','XV век до н. э.','KARNAK'),
 ('Стирание царской памяти','Damnatio memoriae','EVENT','избирательное уничтожение имён и изображений после смерти Хатшепсут','после 1458 до н. э.','DEIR_BAHRI')],
 'archive':[
 ('Рельефы Пунта','Land of Punt','ARTIFACT','изображения людей, товаров и ландшафта Пунта','XV век до н. э.','DEIR_BAHRI'),
 ('Красная капелла','Red Chapel of Hatshepsut','BUILDING','святилище для процессий барки Амона','XV век до н. э.','KARNAK'),
 ('Хатнефер','Hatnefer','PERSON','мать Сененмута, известная по хорошо документированной гробнице','XV век до н. э.','THEBES'),
 ('Фрагменты статуй Хатшепсут','Hatshepsut sculpture','ARTIFACT','разбитые и восстановленные царские статуи из Дейр-эль-Бахри','XV век до н. э.','DEIR_BAHRI')]
},
{
 'title':'Тутмос III и Мегиддо','subtitle':'Военные кампании создают сеть египетского контроля в Сирии и Палестине.','description':'Битва при Мегиддо, Карнакские анналы, осады, дань, Митанни, Яффа и устройство азиатских владений.','period':'ок. 1458–1425 до н. э.','source':SRC_NEW,
 'chronology':[('ок. 1457 до н. э.','Первый поход Тутмоса III и битва при Мегиддо','traditional'),('после Мегиддо','Египет закрепляет контроль над южным Левантом','mixed'),('середина XV века до н. э.','Походы достигают Евфрата и владений Митанни','approximate'),('конец правления','Система дани и заложников связывает азиатские города с двором','mixed')],
 'locations':['MEGIDDO','KADESH','JOPPA'],
 'causes':['Сопротивление коалиции левантийских правителей','Потребность защищать торговые и военные маршруты','Ресурсы армии XVIII династии'],
 'consequences':['Египетское господство в южном Леванте','Регулярные поставки дани и заложников','Долгое соперничество с Митанни'],
 'story':[
 ('Тутмос III','Thutmose III','PERSON','царь и полководец XVIII династии','ок. 1479–1425 до н. э.','KARNAK'),
 ('Битва при Мегиддо','Battle of Megiddo (15th century BC)','BATTLE','первый большой поход самостоятельного правления Тутмоса III','традиционно ок. 1457 до н. э.','MEGIDDO'),
 ('Карнакские анналы','Annals of Thutmose III','TEXT','официальная запись походов и добычи','XV век до н. э.','KARNAK'),
 ('Осада Мегиддо','Battle of Megiddo (15th century BC)','EVENT','длительное завершение победы над коалицией','XV век до н. э.','MEGIDDO'),
 ('Дань азиатских городов','Tribute in ancient Egypt','SYSTEM','поставки товаров и людей в обмен на признание власти','XV век до н. э.','MEGIDDO'),
 ('Митанни','Mitanni','STATE','северный соперник Египта в Сирии','XV–XIV века до н. э.','KADESH'),
 ('Взятие Яффы','The Taking of Joppa','TEXT','литературный рассказ о хитрости египетского военачальника','Новое царство','JOPPA'),
 ('Имперская администрация в Леванте','Egyptian Empire','SYSTEM','сеть вассальных правителей, гарнизонов и царских посланников','XV–XIII века до н. э.','MEGIDDO')],
 'archive':[
 ('Ботанический сад Тутмоса III','Botanical garden of Thutmose III','ARTIFACT','рельефы с растениями и животными чужих земель','XV век до н. э.','KARNAK'),
 ('Стела Джебель-Баркала Тутмоса III','Jebel Barkal Stele of Thutmose III','TEXT','царская надпись о походах и границах','XV век до н. э.','GEBEL_BARKAL'),
 ('Список городов Карнака','Karnak king list','TEXT','перечни покорённых мест в храмовой программе','XV век до н. э.','KARNAK'),
 ('Повесть о взятии Яффы','The Taking of Joppa','TEXT','литературная версия военного эпизода','Новое царство','JOPPA')]
},
{
 'title':'Амарнский перелом','subtitle':'Эхнатон меняет культ, столицу и язык царского изображения.','description':'Аменхотеп III, Эхнатон, Атон, Ахетатон, Нефертити, Амарнские письма, Тутанхамон и восстановление старых культов.','period':'XIV век до н. э.','source':SRC_AMARNA,
 'chronology':[('ок. 1390–1353 до н. э.','Правление Аменхотепа III','approximate'),('ок. 1353 до н. э.','Воцарение Аменхотепа IV','approximate'),('ок. 1348 до н. э.','Основание Ахетатона','approximate'),('ок. 1336–1323 до н. э.','Возвращение двора к прежним культам при Тутанхамоне','mixed')],
 'locations':['AMARNA','KARNAK','MEMPHIS'],
 'causes':['Усиление солнечной теологии царского двора','Политика Аменхотепа IV в отношении храмов','Создание новой столицы и новой придворной среды'],
 'consequences':['Преимущество культа Атона при дворе','Перестройка художественного языка','Быстрое восстановление прежних культов после смерти Эхнатона'],
 'story':[
 ('Аменхотеп III','Amenhotep III','PERSON','царь периода богатой дипломатии и крупного строительства','ок. 1390–1353 до н. э.','THEBES'),
 ('Эхнатон','Akhenaten','PERSON','царь, сделавший Атона центром государственной религиозной программы','ок. 1353–1336 до н. э.','AMARNA'),
 ('Атон','Aten','RELIGION','солнечное божество, получившее исключительное положение при Эхнатоне','XIV век до н. э.','AMARNA'),
 ('Ахетатон','Amarna','CITY','новая столица, построенная на среднем Ниле','ок. 1348–1336 до н. э.','AMARNA'),
 ('Нефертити','Nefertiti','PERSON','великая царская супруга и важная фигура амарнского двора','XIV век до н. э.','AMARNA'),
 ('Амарнское искусство','Amarna art','CULTURE','изменённый язык изображения царской семьи и ритуала','XIV век до н. э.','AMARNA'),
 ('Амарнские письма','Amarna letters','TEXT','дипломатический архив на аккадском языке','XIV век до н. э.','AMARNA'),
 ('Тутанхамон и восстановление культов','Tutankhamun','EVENT','возврат двора к Амону и прежним храмовым центрам','ок. 1336–1323 до н. э.','THEBES')],
 'archive':[
 ('Пограничные стелы Ахетатона','Boundary Stelae of Akhenaten','TEXT','надписи, определявшие пространство новой столицы','XIV век до н. э.','AMARNA'),
 ('Великий гимн Атону','Great Hymn to the Aten','TEXT','религиозный текст амарнского времени','XIV век до н. э.','AMARNA'),
 ('Талататы','Talatat','ARTIFACT','малые каменные блоки амарнских построек','XIV век до н. э.','KARNAK'),
 ('Стела восстановления Тутанхамона','Restoration Stela','TEXT','царская программа возвращения храмов к прежнему порядку','XIV век до н. э.','THEBES')]
},
{
 'title':'Рамессиды и конец Нового царства','subtitle':'Война, дипломатия, храмовые хозяйства и внутренний кризис завершают эпоху.','description':'Сети I, Рамсес II, Кадеш, договор с хеттами, Пер-Рамсес, Дейр-эль-Медина, Рамсес III и распад единой власти.','period':'ок. 1292–1070 до н. э.','source':SRC_NEW,
 'chronology':[('ок. 1290–1279 до н. э.','Правление Сети I','approximate'),('традиционно 1274 до н. э.','Битва при Кадеше','traditional'),('ок. 1259 до н. э.','Египетско-хеттский мирный договор','approximate'),('ок. 1155 до н. э.','Забастовка мастеров Дейр-эль-Медины','approximate'),('ок. 1070 до н. э.','Начало политического разделения Третьего переходного периода','approximate')],
 'locations':['KADESH','PI_RAMESSES','MEDINET_HABU'],
 'causes':['Соперничество Египта и Хеттского царства','Высокая стоимость войн и храмовых программ','Нарушение снабжения и ослабление центрального контроля'],
 'consequences':['Переход от войны к международному договору','Рост влияния храмовых и региональных элит','Разделение власти между севером и Фивами'],
 'story':[
 ('Сети I','Seti I','PERSON','царь XIX династии, восстановивший позиции Египта в Леванте','ок. 1290–1279 до н. э.','KADESH'),
 ('Рамсес II','Ramesses II','PERSON','долгоправящий царь, связанный с Кадешем и крупным строительством','ок. 1279–1213 до н. э.','PI_RAMESSES'),
 ('Битва при Кадеше','Battle of Kadesh','BATTLE','сражение Египта и Хеттского царства у Оронта','традиционно 1274 до н. э.','KADESH'),
 ('Египетско-хеттский договор','Egyptian–Hittite peace treaty','TEXT','договор Рамсеса II и Хаттусили III','ок. 1259 до н. э.','KADESH'),
 ('Пер-Рамсес','Pi-Ramesses','CITY','царская резиденция в восточной Дельте','XIII–XI века до н. э.','PI_RAMESSES'),
 ('Дейр-эль-Медина','Deir el-Medina','SITE','поселение мастеров царских гробниц и источник повседневных документов','Новое царство','DEIR_MEDINA'),
 ('Рамсес III и войны начала XII века','Ramesses III','PERSON','царь XX династии, отражавший вторжения и мятежи','ок. 1184–1153 до н. э.','MEDINET_HABU'),
 ('Конец Нового царства','New Kingdom of Egypt','EVENT','ослабление царской власти и переход к разделённому управлению','ок. 1070 до н. э.','THEBES')],
 'archive':[
 ('Абу-Симбел','Abu Simbel','BUILDING','скальные храмы Рамсеса II в Нубии','XIII век до н. э.','ABU_SIMBEL'),
 ('Большой папирус Харриса','Papyrus Harris I','TEXT','перечень даров и деяний Рамсеса III','XII век до н. э.','MEDINET_HABU'),
 ('Туринский папирус о забастовке','Deir el-Medina strike','TEXT','документ о прекращении работы из-за задержки пайков','ок. 1155 до н. э.','DEIR_MEDINA'),
 ('Рельефы Мединет-Абу','Medinet Habu','ARTIFACT','царские изображения войн Рамсеса III','XII век до н. э.','MEDINET_HABU')]
}
]

TYPE_LABEL={
'PERSON':'личность','CITY':'город','STATE':'государство','EVENT':'событие','DYNASTY':'династия','BUILDING':'сооружение','OFFICE':'должность','PERIOD':'период','SYSTEM':'система','TEXT':'текст','REGION':'регион','RESOURCE':'ресурс','ROUTE':'маршрут','PEOPLE':'группа','WAR':'военное дело','SITE':'место','RELIGION':'религия','CULTURE':'культура','BATTLE':'битва','CONCEPT':'понятие','ARTIFACT':'артефакт'
}

def dump(path,obj):
    path=ROOT/path; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding='utf-8')

def svg_card(path,title,subtitle,chapter,index,kind):
    path=ROOT/path;path.parent.mkdir(parents=True,exist_ok=True)
    safe_title=html.escape(title);safe_sub=html.escape(subtitle)
    mark=['𓂀','𓋹','𓏏','𓊹','𓆣','𓇳','𓉐','𓎟','𓂋','𓅓'][chapter-1]
    accent=['#b78b55','#c5a86a','#9e7c47','#82674b','#bb9560','#d1b56d','#b88454','#8d724d','#d2a45e','#a77d4b'][chapter-1]
    data=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 900" role="img" aria-label="{safe_title}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#17120d"/><stop offset=".55" stop-color="#302416"/><stop offset="1" stop-color="#080706"/></linearGradient><radialGradient id="r"><stop stop-color="{accent}" stop-opacity=".35"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient></defs>
<rect width="720" height="900" fill="url(#g)"/><circle cx="565" cy="180" r="250" fill="url(#r)"/><path d="M0 675 C150 610 278 720 430 650 S620 600 720 635 V900 H0Z" fill="#090807" opacity=".88"/>
<path d="M62 112 H658 M62 790 H658" stroke="{accent}" stroke-width="2" opacity=".65"/><text x="62" y="82" fill="{accent}" font-size="22" font-family="serif" letter-spacing="4">EGYPT · BRONZE AGE · {chapter:02d}</text>
<text x="560" y="340" text-anchor="middle" fill="{accent}" font-size="190" font-family="serif" opacity=".75">{mark}</text>
<text x="62" y="660" fill="#fff8e8" font-size="46" font-family="Georgia,serif">{safe_title[:28]}</text>
<text x="62" y="713" fill="#d8cbb4" font-size="24" font-family="Arial,sans-serif">{safe_sub[:48]}</text>
<text x="62" y="832" fill="{accent}" font-size="18" font-family="Arial,sans-serif" letter-spacing="3">{kind.upper()} · CODEX OF HISTORY · {index:02d}</text></svg>'''
    path.write_text(data,encoding='utf-8')

def pack_svg():
    p=ROOT/'assets/packs/egypt-bronze-pack.svg';p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 560"><defs><linearGradient id="g" x2="1" y2="1"><stop stop-color="#090807"/><stop offset=".55" stop-color="#3b2917"/><stop offset="1" stop-color="#110d08"/></linearGradient><radialGradient id="r"><stop stop-color="#d8ad66" stop-opacity=".55"/><stop offset="1" stop-color="#d8ad66" stop-opacity="0"/></radialGradient></defs><rect width="900" height="560" rx="38" fill="url(#g)"/><circle cx="700" cy="170" r="280" fill="url(#r)"/><path d="M90 410 H810" stroke="#d8ad66" stroke-width="3" opacity=".7"/><text x="90" y="120" fill="#d8ad66" font-size="24" font-family="Arial" letter-spacing="6">ЦАРСТВА БРОНЗОВОГО ВЕКА</text><text x="90" y="215" fill="#fff7e4" font-size="68" font-family="Georgia">Египетский архив</text><text x="90" y="280" fill="#d9cbb5" font-size="30" font-family="Arial">Среднее и Новое царства</text><text x="700" y="345" text-anchor="middle" fill="#d8ad66" font-size="230" font-family="serif">𓂀</text><text x="90" y="470" fill="#d8ad66" font-size="22" font-family="Arial" letter-spacing="5">4 КАРТЫ · ОТКРЫТЫЕ ГЛАВЫ</text></svg>''',encoding='utf-8')

# rarity allocation
story_r=['COMMON','COMMON','UNCOMMON','COMMON','UNCOMMON','RARE','RARE','EPIC']
archive_r_by_ch=[]
for i in range(10):
    archive_r_by_ch.append(['COMMON','UNCOMMON','RARE' if i<5 else 'EPIC','MYTHIC' if i in (2,6,9) else 'LEGENDARY'])

story_cards=[];archive_cards=[];nodes=[];lessons={};quizzes={};pools=[];acquisition={};stories={};relations=[]
map_points={k:v[0] for k,v in P.items()};card_points={};map_chapters={}
rel_i=1

# precollect distractors per chapter
for ci,ch in enumerate(CHAPTERS,1):
    ch_id=f'EMN_CHAPTER_{ci:02d}'
    story_ids=[];arch_ids=[]
    all_topics=ch['story']+ch['archive']
    for ti,t in enumerate(ch['story'],1):
        cid=f'EMN_S_{ci:02d}_{ti:02d}';story_ids.append(cid)
        title,original,typ,subtitle,date,point=t
        loc=P[point]
        card={
          'id':cid,'type':typ,'title':title,'original':original,'subtitle':subtitle,'era':'Царства бронзового века','region':'Египет и соседние регионы','date':date,
          'rarity':story_r[ti-1],'difficulty':5+min(4,ci//3),'summary':f'{title}: {subtitle}.','importance':f'Тема помогает понять главу «{ch["title"]}» через конкретный {TYPE_LABEL.get(typ,"источник")}, его дату и исторический контекст.',
          'facts':[f'Датировка: {date}.',f'Главный смысл: {subtitle}.',f'Материал нужно сопоставлять с другими текстами, памятниками и археологическим контекстом главы «{ch["title"]}».'],
          'tags':['Египет','бронзовый век',ch['title'],typ.lower()],'stats':{'context':5+ci%4,'sources':4+(ti%4),'connections':5+((ci+ti)%4)},
          'loc':{'label':loc[1],'lat':loc[0][0],'lon':loc[0][1]},
          'image':{'local':f'assets/cards/egypt-middle-new/chapter-{ci:02d}/{cid.lower()}.svg','caption':f'Локальная учебная обложка: {title}','credit':'Codex of History · локальная учебная обложка','source_url':ch['source']['url'],'license':'Project asset','focus':'50% 50%','file':f'{cid.lower()}.svg','kind':'project-cover'},
          'source':ch['source'],'acquisition':'STORY','campaign':'EGYPT_BRONZE','chapter':ch_id
        }
        story_cards.append(card);card_points[cid]=point;svg_card(Path(card['image']['local']),title,subtitle,ci,ti,'story')
    for ti,t in enumerate(ch['archive'],1):
        cid=f'EMN_A_{ci:02d}_{ti:02d}';arch_ids.append(cid)
        title,original,typ,subtitle,date,point=t;loc=P[point]
        card={
          'id':cid,'type':typ,'title':title,'original':original,'subtitle':subtitle,'era':'Царства бронзового века','region':'Египет и соседние регионы','date':date,
          'rarity':archive_r_by_ch[ci-1][ti-1],'difficulty':5+min(4,ci//3),'summary':f'{title}: {subtitle}.','importance':f'Архивная карточка дополняет главу «{ch["title"]}» отдельным памятником, документом или человеком.',
          'facts':[f'Датировка: {date}.',f'Связь с темой: {subtitle}.',f'Надёжный вывод зависит от происхождения, жанра и состояния материала.'],
          'tags':['Египет','архив',ch['title'],typ.lower()],'stats':{'context':5+ci%4,'sources':5+(ti%3),'connections':4+((ci+ti)%5)},
          'loc':{'label':loc[1],'lat':loc[0][0],'lon':loc[0][1]},
          'image':{'local':f'assets/cards/egypt-middle-new/chapter-{ci:02d}/{cid.lower()}.svg','caption':f'Локальная учебная обложка: {title}','credit':'Codex of History · локальная учебная обложка','source_url':ch['source']['url'],'license':'Project asset','focus':'50% 50%','file':f'{cid.lower()}.svg','kind':'project-cover'},
          'source':ch['source'],'acquisition':'ARCHIVE','campaign':'EGYPT_BRONZE','chapter':ch_id
        }
        archive_cards.append(card);card_points[cid]=point;svg_card(Path(card['image']['local']),title,subtitle,ci,ti,'archive')
        acquisition[cid]={'kind':'ARCHIVE','pool':f'EMN_POOL_{ci:02d}','campaign':'EGYPT_BRONZE'}
    pools.append({'id':f'EMN_POOL_{ci:02d}','campaign':'EGYPT_BRONZE','title':ch['title'],'unlockMission':f'EMN_{ci:02d}_02','cardIds':arch_ids})
    # personal story anchored to most prestigious archive card
    target=arch_ids[-1]
    stories[f'STORY_EMN_{ci:02d}']={
      'id':f'STORY_EMN_{ci:02d}','cardId':target,'title':f'Архивное дело: {ch["archive"][-1][0]}','subtitle':ch['title'],'rewardXp':120+ci*5,'rewardFragments':12+ci,
      'steps':[{'type':'SCENE','title':'Материал архива','text':f'Карточка «{ch["archive"][-1][0]}» рассматривается как отдельный материал главы «{ch["title"]}». Сначала фиксируются дата, место, жанр и состояние источника.'},
               {'type':'QUESTION','title':'Проверка источника','question':f'Какой первый шаг нужен при работе с материалом «{ch["archive"][-1][0]}»?','options':['Определить происхождение и жанр','Сразу восстановить мысли всех участников','Принять позднее толкование за факт','Игнорировать место находки'],'correct':0,'explanation':'Происхождение и жанр задают предел допустимого вывода.'},
               {'type':'QUESTION','title':'Граница вывода','question':'Как правильно оформить итог?','options':['Разделить наблюдение, реконструкцию и степень уверенности','Назвать гипотезу прямым свидетельством','Считать один предмет полной картиной эпохи','Убрать все оговорки о датировке'],'correct':0,'explanation':'Историческая реконструкция должна показывать опору и ограничения.'}]}
    # relations in chapter
    for i in range(7):
        relations.append({'id':f'REL_EMN_{rel_i:04d}','source':story_ids[i],'target':story_ids[i+1],'type':'СВЯЗАНО_В_ГЛАВЕ','description':f'{ch["story"][i][0]} связан с темой «{ch["story"][i+1][0]}» внутри главы «{ch["title"]}».','strength':7});rel_i+=1
    for i,a in enumerate(arch_ids):
        relations.append({'id':f'REL_EMN_{rel_i:04d}','source':a,'target':story_ids[min(i*2,7)],'type':'АРХИВНЫЙ_КОНТЕКСТ','description':f'{ch["archive"][i][0]} дополняет сюжетную тему «{ch["story"][min(i*2,7)][0]}».','strength':6});rel_i+=1
    # mission and lessons
    mission_titles=[
      f'Рассказ: {ch["title"]}',
      f'Хронология: {ch["period"]}',
      f'Источник: {ch["archive"][0][0]}',
      f'Карта: {P[ch["locations"][0]][1]}, {P[ch["locations"][1]][1]} и {P[ch["locations"][2]][1]}',
      f'Разбор: причины и последствия',
      ('Экзамен: Египет Среднего и Нового царства' if ci==10 else f'Итог главы: {ch["title"]}')
    ]
    mtypes=['LESSON','TIMELINE','SOURCE','MAP','CAUSE_EFFECT','FINAL']; emojis=['▤','◷','▥','⌖','◆','◎']
    unlock_plan=[[0,1],[2],[3,4],[5],[6],[7]]
    card_plan=[[0,1,2],[2,3,4],[3,4,5],[1,5,6],[0,6,7],[7,0,3]]
    chapter_mission_ids=[]
    concepts=[{'term':x[0],'definition':x[3]} for x in ch['story'][:3]]
    for mi in range(1,7):
        mid=f'EMN_{ci:02d}_{mi:02d}';chapter_mission_ids.append(mid)
        n={'id':mid,'type':mtypes[mi-1],'title':mission_titles[mi-1],'description':f'{ch["description"]} Фокус миссии: {mission_titles[mi-1]}.','cards':[story_ids[i] for i in card_plan[mi-1]],'unlockCards':[story_ids[i] for i in unlock_plan[mi-1]],'xp':160+ci*8+mi*5,'emoji':emojis[mi-1],'chapterId':ch_id,'lessonId':mid}
        if mi==2:
            n['timeline']=[{'id':f't{i}','date':e[0],'title':e[1]} for i,e in enumerate(ch['chronology'])]
        if mi==4:
            n['mapTargets']=[{'key':k.lower(),'label':P[k][1],'point':k,'zoom':7 if k not in ('PUNT','SHARUHEN','KADESH') else 5,'radius':90000} for k in ch['locations']]
        if mi==6:
            n['quiz']=f'QUIZ_EMN_CH{ci}'
            if ci==10:
                n['campaignExamModules']=[
                  {'id':'QUIZ_EMN_EXAM_MAP','title':'Карта Нила, Нубии и Леванта','icon':'⌖'},
                  {'id':'QUIZ_EMN_EXAM_TIME','title':'Хронология 2055–1070','icon':'◷'},
                  {'id':'QUIZ_EMN_EXAM_SOURCE','title':'Надписи, рельефы и письма','icon':'▥'},
                  {'id':'QUIZ_EMN_EXAM_SYSTEM','title':'Царская власть, храмы и империя','icon':'◆'}]
        nodes.append(n)
        # lesson activity
        if mi in (1,5):
            activity={'type':'choice','prompt':f'Какой вывод точнее всего описывает миссию «{mission_titles[mi-1]}»?','options':[ch['subtitle'],'Все изменения объясняются одним правителем','Письменные источники дают полную и нейтральную картину','Датировки древнего Египта всегда точны до года'],'correct':0,'explanation':ch['description']}
        elif mi==2: activity={'type':'timeline'}
        elif mi==3:
            activity={'type':'match','prompt':'Сопоставь материал и тип вывода.','pairs':[{'left':ch['archive'][0][0],'right':'конкретный источник или памятник'},{'left':ch['story'][0][0],'right':'исторический участник или институт'},{'left':ch['chronology'][1][1],'right':'событие в последовательности'}]}
        elif mi==4: activity={'type':'map'}
        else: activity={'type':'final_quiz'}
        topic=ch['story'][(mi-1)%8]
        title=mission_titles[mi-1]
        paras=[
          f'Миссия «{title}» относится к главе «{ch["title"]}» и рассматривает тему «{topic[0]}». {ch["description"]} Для древнеегипетской истории важно различать относительную последовательность царей, приблизительную абсолютную датировку и дату создания конкретного памятника. Даже хорошо известное правление редко позволяет восстановить каждое событие по современному календарю.',
          f'Основной материал миссии — {topic[0].lower()}: {topic[3]}. Свидетельства могут включать царские надписи, частные биографии, храмовые рельефы, папирусы, археологические слои и поздние списки царей. Каждый тип материала создан с собственной целью. Официальный текст показывает программу власти, но не обязан перечислять неудачи; частный документ точнее в деталях, но уже по охвату.',
          f'В рамках миссии «{title}» институциональный разбор требует проверить, кто принимал решения, кто собирал и распределял ресурсы и какие местные группы сохраняли собственное влияние. Политическая система главы «{ch["title"]}» связывала царский двор, храмы, провинциальные администрации, войско и хозяйственные службы. Эта связь не была одинаковой во все десятилетия. Центр мог контролировать назначения и крупные ресурсы, а местные элиты сохраняли влияние на землю, людей и культ. Поэтому термин «единое государство» не означает одинаковое управление в каждой области.',
          f'Пространственный разбор миссии «{title}» связывает политические решения с конкретными маршрутами, поселениями и зонами контроля. География задаёт пределы решений. В этой миссии важны {P[ch["locations"][0]][1]}, {P[ch["locations"][1]][1]} и {P[ch["locations"][2]][1]}. Нил облегчал перевозку людей и грузов, но пороги, пустыни, Дельта и дальние маршруты требовали крепостей, складов, кораблей и договорённостей с местными группами. Карта используется как часть объяснения, а не как декоративный фон.',
          f'Причины процесса нельзя свести к одному приказу. Для темы «{title}» нужно сопоставить: {ch["causes"][0].lower()}, {ch["causes"][1].lower()} и {ch["causes"][2].lower()}. Следствия также шли с разной скоростью: {ch["consequences"][0].lower()}, {ch["consequences"][1].lower()} и {ch["consequences"][2].lower()}. Между событием и устойчивым изменением могли пройти годы или поколения.',
          f'Итог миссии «{title}» должен отделять подтверждённое наблюдение от реконструкции. Опорный материал «{ch["source"]["title"]}» задаёт общую рамку, но отдельные даты и интерпретации проверяются по специализированным публикациям. Корректный ответ называет источник, место, хронологический диапазон и степень уверенности, а затем объясняет, как тема «{topic[0]}» меняет понимание всей главы.'
        ]
        lessons[mid]={
          'id':mid,'title':title,'duration':9+mi,'objectives':[f'объяснить роль темы «{topic[0]}» в главе «{ch["title"]}»','различить археологический факт, официальный текст и современную реконструкцию','связать дату, географию, институт и последствия'],
          'story':[{'title':ch['title'],'text':ch['description']},{'title':'Фокус миссии','text':f'{title}. Главный материал: {topic[0]} — {topic[3]}.'},{'title':'Граница знания','text':'Датировки и политические выводы зависят от характера источника. Царская надпись, археологический слой и поздний список не имеют одинаковой доказательной силы.'}],
          'chronology':[{'date':e[0],'title':e[1],'note':f'{e[1]}. Связь с миссией «{title}» проверяется по жанру и контексту источника.','certainty':e[2]} for e in ch['chronology']],
          'concepts':concepts,'causeEffect':{'causes':ch['causes'],'consequences':ch['consequences']},'activity':activity,'sources':[ch['source']],
          'theory':{'title':title,'readingMinutes':6,'lead':f'{ch["description"]} В этой миссии основной вопрос — {topic[0].lower()}.','paragraphs':paras,'historicityNotes':['Даты правлений и событий приблизительны и зависят от принятой хронологии.','Царские изображения и надписи выражают официальную программу власти.','Археологический контекст может уточнять или ограничивать текстовую традицию.'],'sources':[ch['source']],'license':'Авторский учебный текст Codex of History.','checkedAt':CHECKED}
        }
    map_chapters[ch_id]={'title':ch['title'],'center':P[ch['locations'][0]][0],'zoom':5}
    # chapter quiz: 6 unique questions with rotated correct positions
    qs=[]
    for qi in range(4):
        correct_title=ch['story'][qi][0]
        distract=[ch['story'][(qi+j+1)%8][0] for j in range(3)]
        pos=(ci+qi)%4;opts=distract[:];opts.insert(pos,correct_title)
        qs.append({'text':f'Какой термин или участник соответствует описанию: «{ch["story"][qi][3]}»?','options':opts,'correct':pos,'explanation':f'{correct_title}: {ch["story"][qi][3]}.'})
    pos=(ci+4)%4;opts=['Сначала определить жанр, дату и место документа','Считать царскую надпись полной картиной общества','Выбрать одну причину без сопоставления','Принять поздний список за запись очевидца'];right=opts.pop(0);opts.insert(pos,right)
    qs.append({'text':f'Какой способ работы с источником нужен в главе «{ch["title"]}»?','options':opts,'correct':pos,'explanation':'Жанр, дата и происхождение задают предел допустимого вывода.'})
    pos=(ci+5)%4;opts=['Все процессы объясняются одним походом','Письменная администрация исчезла полностью','Все регионы имели одинаковые институты'];opts.insert(pos,ch['subtitle'])
    qs.append({'text':f'Какой итог по главе «{ch["title"]}» наиболее точен?','options':opts,'correct':pos,'explanation':ch['description']})
    quizzes[f'QUIZ_EMN_CH{ci}']={'id':f'QUIZ_EMN_CH{ci}','title':f'Глава {ci}: {ch["title"]}','passPercent':70,'questions':qs}

# campaign chapters list
campaign_chapters=[]
for ci,ch in enumerate(CHAPTERS,1):
    campaign_chapters.append({'id':f'EMN_CHAPTER_{ci:02d}','number':ci,'title':ch['title'],'subtitle':ch['subtitle'],'description':ch['description'],'missionIds':[f'EMN_{ci:02d}_{i:02d}' for i in range(1,7)]})

# Cross-campaign continuity relations
for source,target,desc in [
 ('PERIOD_EGY2_003','EMN_S_01_04','Первый переходный период предшествует новому объединению при Ментухотепе II.'),
 ('STATE_EGY2_002','EMN_S_01_02','Раннее Фиванское царство становится основой Среднего царства.'),
 ('RIV_EGY_001','EMN_S_03_04','Нил связывает Египет с крепостной системой Нижней Нубии.'),
 ('REG_EGY_005','EMN_S_04_02','Восточная Дельта становится пространством Авариса.'),
 ('BAB_S_07_02','EMN_S_04_02','Торговые сети бронзового века связывали Анатолию, Сирию и Египет.'),
 ('BAB_S_03_05','EMN_S_08_06','Ямхад и позднее Митанни входят в меняющуюся систему сирийских держав.'),
 ('SYS_CIV_002','EMN_S_09_07','Письменная дипломатия бронзового века проявляется в Амарнском архиве.'),
 ('EMN_S_10_04','BAB_S_08_08','Египетско-хеттский договор относится к миру держав после старовавилонского периода.')]:
    relations.append({'id':f'REL_EMN_{rel_i:04d}','source':source,'target':target,'type':'МЕЖКАМПАНИЙНАЯ_СВЯЗЬ','description':desc,'strength':8});rel_i+=1

# Exam modules: 5 questions each
exam_specs={
'QUIZ_EMN_EXAM_MAP':('Карта Нила, Нубии и Леванта',[
 ('Где находилась столица гиксосской XV династии?',['Аварис','Карнак','Мегиддо','Абу-Симбел'],0,'Аварис располагался в восточной Дельте.'),
 ('Какой пункт относится к системе крепостей Среднего царства в Нубии?',['Ахетатон','Семна','Яффа','Пер-Рамсес'],1,'Семна контролировала район второго порога.'),
 ('Где была построена столица Эхнатона?',['Лишт','Бени-Хасан','Ахетатон','Шарухен'],2,'Ахетатон расположен в районе современной Амарны.'),
 ('Какое место связано с битвой Тутмоса III против левантийской коалиции?',['Файюм','Фивы','Бухен','Мегиддо'],3,'Битва при Мегиддо открыла серию походов Тутмоса III.'),
 ('Какой маршрут связывает Египет с Нубией прежде всего?',['Долина Нила','Средиземное море','Тигр','Эгейские острова'],0,'Нил был главным путём движения на юг.')]),
'QUIZ_EMN_EXAM_TIME':('Хронология 2055–1070',[
 ('Какое событие произошло раньше остальных?',['Новое объединение при Ментухотепе II','Битва при Кадеше','Основание Ахетатона','Изгнание гиксосов'],0,'Объединение относится к началу Среднего царства.'),
 ('Что следует после Второго переходного периода?',['XII династия','Новое царство','Первый переходный период','Древнее царство'],1,'Победа Яхмоса I открывает Новое царство.'),
 ('Какое событие относится к XIV веку до н. э.?',['Поход Камоса','Строительство Семны','Основание Ахетатона','Новое объединение Ментухотепа II'],2,'Амарнский период приходится на XIV век до н. э.'),
 ('Что ближе всего к концу Нового царства?',['Правление Сенусерта I','Битва при Мегиддо','Экспедиция Хатшепсут в Пунт','Забастовка в Дейр-эль-Медине'],3,'Забастовка относится к позднему XX династическому периоду.'),
 ('Какой порядок верен?',['Ментухотеп II → гиксосы → Хатшепсут → Рамсес II','Гиксосы → Ментухотеп II → Рамсес II → Хатшепсут','Хатшепсут → гиксосы → Ментухотеп II → Рамсес II','Рамсес II → Хатшепсут → гиксосы → Ментухотеп II'],0,'Так выглядит общий порядок эпох.')]),
'QUIZ_EMN_EXAM_SOURCE':('Надписи, рельефы и письма',[
 ('Что прежде всего показывает царская надпись?',['Официальную программу власти','Полную статистику населения','Нейтральный отчёт противника','Точный календарь каждого события'],0,'Царская надпись создавалась в интересах власти.'),
 ('Почему Амарнские письма особенно важны?',['Они написаны на латыни','Они фиксируют международную переписку на аккадском','Они являются поздней греческой легендой','Они описывают только строительство пирамид'],1,'Архив показывает дипломатическую систему позднего бронзового века.'),
 ('Какой материал связан с трудовым конфликтом позднего Нового царства?',['Палетка Нармера','Стела Хаммурапи','Туринский папирус о забастовке','Гимн Атону'],2,'Документ связан с задержкой пайков мастерам.'),
 ('Что нельзя автоматически вывести из слоя разрушения?',['Факт сильного повреждения','Примерный период пожара','Связь с изменением поселения','Имя конкретного нападавшего'],3,'Имя виновника требует независимого подтверждения.'),
 ('Как оформить спорную датировку?',['Указать диапазон и степень уверенности','Скрыть разногласия','Выбрать самую красивую дату','Заменить датировку легендой'],0,'Оговорка о точности является частью ответа.')]),
'QUIZ_EMN_EXAM_SYSTEM':('Царская власть, храмы и империя',[
 ('Что помогало царю контролировать Нубию?',['Крепости и наместник Куша','Только храмовые праздники','Отказ от речного транспорта','Ликвидация всех местных элит'],0,'Контроль строился на администрации, гарнизонах и путях снабжения.'),
 ('Как работало египетское господство в Леванте?',['Через полное переселение населения','Через вассалов, гарнизоны, дань и заложников','Без дипломатии и писем','Только через один ежегодный поход'],1,'Система сочетала местных правителей и египетский надзор.'),
 ('Почему храмы были политически важны?',['Они не владели ресурсами','Они существовали только как гробницы','Они управляли землями, людьми и перераспределением','Они полностью заменяли царя'],2,'Храмовые хозяйства были крупными институциональными центрами.'),
 ('Что показывает конец Нового царства?',['Империя росла без затрат','Все регионы управлялись одинаково','Царская власть только усиливалась','Снабжение, война и региональные элиты могли ослабить центр'],3,'Кризис был связан с несколькими взаимными процессами.'),
 ('Какой общий вывод наиболее точен?',['Египет менялся через сочетание географии, институтов, войн и религиозной политики','Историю определял один фараон','Тексты всегда точнее археологии','Все перемены происходили одновременно'],0,'Кампания требует многопричинного объяснения.')])
}
for qid,(title,qraw) in exam_specs.items():
    quizzes[qid]={'id':qid,'title':title,'passPercent':70,'questions':[{'text':a,'options':b,'correct':c,'explanation':d} for a,b,c,d in qraw]}

campaign={
'id':'EGYPT_MIDDLE_NEW','title':'Египет: от Среднего к Новому царству','description':'От объединения при Ментухотепе II до распада единой власти в конце Нового царства.','difficulty':7,'chapters':campaign_chapters,'nodes':nodes,
'eraLayer':{
 'period':'ок. 2055–1070 до н. э.','summary':'Среднее царство, Второй переходный период и Новое царство рассматриваются как единая длинная линия с разрывами и перестройками.',
 'phases':[{'id':'MIDDLE','title':'Среднее царство','date':'ок. 2055–1650 до н. э.','chapters':[1,2,3]},{'id':'INTERMEDIATE','title':'Второй переходный период','date':'ок. 1650–1550 до н. э.','chapters':[4,5]},{'id':'NEW','title':'Новое царство','date':'ок. 1550–1070 до н. э.','chapters':[6,7,8,9,10]}]
}}

pools_payload={'campaignId':'EGYPT_MIDDLE_NEW','campaigns':{'EGYPT_BRONZE':{'id':'EGYPT_BRONZE','title':'Египет: от Среднего к Новому царству','active':True,'status':'STARTED'}},'pools':pools,'acquisition':acquisition}
map_payload={'points':map_points,'regions':{},'cardPoints':card_points,'chapters':map_chapters,'missionCenter':[26.8,31.0],'missionZoom':5}

dump(Path('data/cards/egypt/middle-new-story.json'),story_cards)
dump(Path('data/cards/egypt/middle-new-archive.json'),archive_cards)
dump(Path('data/campaigns/egypt-middle-new/campaign.json'),campaign)
dump(Path('data/campaigns/egypt-middle-new/pools.json'),pools_payload)
dump(Path('data/lessons/egypt-middle-new/campaign.json'),lessons)
dump(Path('data/quizzes/egypt-middle-new/campaign.json'),quizzes)
dump(Path('data/stories/egypt-middle-new/personal.json'),stories)
dump(Path('data/maps/egypt-middle-new.json'),map_payload)
pack_svg()
print(f'generated {len(story_cards)+len(archive_cards)} cards, {len(nodes)} missions, {len(lessons)} lessons, {len(quizzes)} quizzes, {len(relations)} relations')
# write relations addition for caller to merge
dump(Path('data/core/relations-v32-egypt.json'),relations)
