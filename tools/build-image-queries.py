#!/usr/bin/env python3
"""Build semantically constrained Wikimedia image profiles for Codex of History."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "7.0.0"

GROUP_CONTEXT = {
    "ROME": {
        "terms": ["древн", "рим", "roman", "latin", "etrusc", "italy", "итал", "лаци"],
        "base": [("ru", "Древний Рим"), ("en", "Ancient Rome")],
    },
    "MESOPOTAMIA": {
        "terms": ["месопот", "шумер", "аккад", "babylon", "sumer", "mesopot", "iraq", "ассир", "клинопис"],
        "base": [("ru", "Месопотамия"), ("en", "Mesopotamia")],
    },
    "EGYPT": {
        "terms": ["егип", "egypt", "pharaoh", "фараон", "nile", "нил", "додинаст", "династи"],
        "base": [("ru", "Древний Египет"), ("en", "Ancient Egypt")],
    },
    "INDUS": {
        "terms": ["индск", "харап", "indus", "harapp", "pakistan", "пакистан", "south asia", "южн ази", "синд"],
        "base": [("ru", "Индская цивилизация"), ("en", "Indus Valley Civilisation")],
    },
    "CHINA": {
        "terms": ["китай", "china", "chinese", "шан", "shang", "zhou", "чжоу", "henan", "yellow river", "хуанх"],
        "base": [("ru", "История Китая"), ("en", "History of China")],
    },
    "BABYLON": {
        "terms": ["вавилон", "babylon", "месопот", "mesopot", "амор", "old babylon", "сирия", "syria", "клинопис"],
        "base": [("ru", "Старовавилонский период"), ("en", "Old Babylonian period")],
    },
    "HITTITES": {
        "terms": ["хетт", "hittite", "хатт", "hatti", "анатол", "anatolia", "hattusa", "сирия", "syria", "клинопис"],
        "base": [("ru", "Хетты"), ("en", "Hittites")],
    },
    "AEGEAN_BRONZE": {
        "terms": ["миной", "minoan", "микен", "mycenaean", "эгей", "aegean", "crete", "крит", "knossos", "mycenae", "bronze age"],
        "base": [("ru", "Эгейская цивилизация"), ("en", "Aegean civilization")],
    },
    "BRONZE_INTERNATIONAL": {
        "terms": ["бронз", "bronze age", "амарн", "amarna", "угарит", "ugarit", "алаш", "alashiya", "кипр", "cyprus", "хетт", "hittite", "егип", "egypt", "дипломат", "trade"],
        "base": [("ru", "Амарнские письма"), ("en", "Late Bronze Age collapse")],
    },
    "BRONZE_WORLD": {
        "terms": ["бронз", "bronze age", "вавилон", "babylon", "егип", "egypt", "хетт", "hittite", "микен", "mycenaean", "угарит", "ugarit", "кипр", "cyprus", "дворец", "palace"],
        "base": [("ru", "Бронзовый век"), ("en", "Late Bronze Age")],
    },
    "PHOENICIANS": {
        "ARTIFACT": [("en", "Phoenician art"), ("en", "Phoenician metal bowls")],
        "TEXT": [("en", "Phoenician alphabet"), ("en", "Phoenician inscriptions")],
        "LAW": [("en", "Treaty of Esarhaddon with Baal of Tyre"), ("en", "Phoenician inscriptions")],
        "BUILDING": [("en", "Tyre, Lebanon"), ("en", "Byblos")],
        "RELIGION": [("en", "Melqart"), ("en", "Astarte")],
        "STATE": [("en", "Phoenicia"), ("en", "Carthage")],
        "SYSTEM": [("en", "Phoenicia"), ("en", "Phoenician trade")],
        "RESOURCE": [("en", "Tyrian purple"), ("en", "Cedars of Lebanon")],
        "ROUTE": [("en", "Phoenicia"), ("en", "Ancient maritime history")],
        "EVENT": [("en", "Phoenicia under Assyrian rule"), ("en", "Siege of Tyre")],
        "SOURCE": [("en", "Phoenician inscriptions"), ("en", "Phoenician alphabet")],
        "CONCEPT": [("en", "Phoenicia"), ("en", "Punic people")],
    },
    "BRONZE_COLLAPSE": {
        "terms": ["бронз", "bronze age", "collapse", "катастроф", "угарит", "ugarit", "хаттуса", "hattusa", "микен", "mycenaean", "мединет", "sea peoples", "кипр", "cyprus", "iron age"],
        "base": [("ru", "Катастрофа бронзового века"), ("en", "Late Bronze Age collapse")],
    },
    "ASSYRIA_BABYLON": {
        "terms": ["ассир", "assyria", "assyrian", "нинев", "nineveh", "нимруд", "nimrud", "кальху", "вавилон", "babylon", "neo-babylonian", "iron age", "месопот"],
        "base": [("ru", "Новоассирийская держава"), ("en", "Neo-Assyrian Empire"), ("en", "Neo-Babylonian Empire")],
    },
    "PHOENICIANS": {
        "terms": ["финик", "phoen", "тир", "tyre", "сидон", "sidon", "библ", "byblos", "карфаг", "carthage", "пунич", "punic", "кипр", "cyprus", "средизем"],
        "base": [("ru", "Финикия"), ("en", "Phoenicia"), ("en", "Phoenician art")],
    },
    "ISRAEL_JUDAH": {
        "terms": ["израил", "israel", "иуде", "judah", "judaean", "самар", "samaria", "лахиш", "lachish", "левант", "levant", "моав", "moab", "аммон", "edom", "арам", "aramaean", "iron age"],
        "base": [("ru", "Древний Израиль и Иудея"), ("en", "Kingdom of Israel (Samaria)"), ("en", "Kingdom of Judah")],
    },
    "GREECE_ARCHAIC": {
        "terms": ["гре", "greek", "archaic", "архаич", "полис", "polis", "афин", "athens", "спарт", "sparta", "коринф", "corinth", "олимп", "delphi", "колони", "hoplite", "alphabet", "iron age"],
        "base": [("ru", "Архаическая Греция"), ("en", "Archaic Greece"), ("en", "Ancient Greece")],
    },
    "ZHOU_WARRING": {
        "terms": ["чжоу", "zhou", "китай", "china", "warring states", "сражающ", "цинь", "qin", "конфуц", "confuc", "bronze", "бронз", "mandate", "небес"],
        "base": [("ru", "Династия Чжоу"), ("en", "Zhou dynasty"), ("en", "Warring States period")],
    },
    "INDIA_VEDIC": {
        "terms": ["вед", "vedic", "india", "инд", "rigveda", "ригвед", "sanskrit", "санскрит", "ganga", "ганг", "kuru", "куру", "mahajanapada", "джанапад"],
        "base": [("ru", "Ведийский период"), ("en", "Vedic period"), ("en", "History of India")],
    },
    "IRON_WORLD": {
        "terms": ["железн", "iron age", "ассир", "assyria", "финик", "phoen", "левант", "levant", "гре", "greek", "чжоу", "zhou", "вед", "vedic", "полис", "polis", "empire"],
        "base": [("ru", "Железный век"), ("en", "Iron Age"), ("en", "Axial Age")],
    },
    "PERSIA": {
        "terms": ["ахеменид", "achaemenid", "перс", "persia", "persian", "кир", "cyrus", "дарий", "darius", "ксеркс", "xerxes", "персепол", "persepolis", "сатрап", "satrap", "iran"],
        "base": [("ru", "Ахеменидская держава"), ("en", "Achaemenid Empire"), ("en", "Ancient Persia")],
    },
    "GREECE_CLASSICAL": {
        "terms": ["классическ", "classical", "гре", "greek", "афин", "athens", "спарт", "sparta", "полис", "polis", "delian", "пелопоннес", "peloponnesian", "фив", "thebes", "македон", "macedon"],
        "base": [("ru", "Классическая Греция"), ("en", "Classical Greece"), ("en", "Ancient Greece")],
    },
    "ALEXANDER": {
        "terms": ["александр", "alexander", "македон", "macedon", "дарий", "darius", "перс", "persian", "гавгамел", "gaugamela", "бактр", "bactria", "инд", "india"],
        "base": [("ru", "Александр Македонский"), ("en", "Alexander the Great"), ("en", "Wars of Alexander the Great")],
    },
    "CLASSICAL_WORLD": {
        "terms": ["классическ", "classical world", "ахеменид", "achaemenid", "перс", "persia", "гре", "greek", "полис", "polis", "македон", "macedon", "александр", "alexander", "empire"],
        "base": [("ru", "Классическая античность"), ("en", "Classical antiquity"), ("en", "Achaemenid Empire")],
    },
    "HELLENISTIC": {
        "terms": ["эллинист", "hellenistic", "диадох", "diadochi", "птолем", "ptolemaic", "селевкид", "seleucid", "антигонид", "antigonid", "пергам", "pergamon", "александрия", "alexandria", "родос", "rhodes"],
        "base": [("ru", "Эллинистический период"), ("en", "Hellenistic period"), ("en", "Hellenistic kingdoms")],
    },
    "INDIA_MAURYA": {
        "terms": ["маур", "maurya", "ашок", "ashoka", "магадх", "magadha", "будд", "buddha", "джайн", "jain", "паталипутр", "pataliputra", "санчи", "sanchi", "bodh gaya", "ганг", "ganga"],
        "base": [("ru", "Империя Маурьев"), ("en", "Maurya Empire"), ("en", "Ashoka")],
    },
    "MIGRATION_KINGDOMS": {
        "terms": ["переселения народов", "migration period", "готы", "goths", "вандалы", "vandals", "гунны", "huns", "аттила", "attila", "одоакр", "odoacer", "теодорих", "theodoric", "англосаксы", "anglo-saxons"],
        "base": [("ru", "Великое переселение народов"), ("en", "Migration Period"), ("en", "Fall of the Western Roman Empire")],
    },
    "LATE_RELIGIONS": {
        "terms": ["раннее христианство", "early christianity", "late antiquity religion", "иудаизм", "judaism", "никея", "nicaea", "монашество", "monasticism", "манихейство", "manichaeism", "халкидон", "chalcedon"],
        "base": [("ru", "Религии поздней Античности"), ("en", "Early Christianity"), ("en", "Religion in Late Antiquity")],
    },
    "LATE_ROMAN": {
        "terms": ["поздняя римская империя", "late roman empire", "диоклетиан", "diocletian", "константин", "constantine", "тетрарх", "tetrarchy", "аврелиан", "aurelian", "пальмира", "palmyra", "феодосий", "theodosius"],
        "base": [("ru", "Поздняя Римская империя"), ("en", "Late Roman Empire"), ("en", "Late Antiquity Roman Empire")],
    },
    "HELLENISTIC_ROMAN_EXAM": {
        "terms": ["античный мир", "ancient world", "эллинист", "hellenistic", "рим", "roman", "маур", "maurya", "хань", "han dynasty", "сюнну", "xiongnu", "сравн", "comparison"],
        "base": [("ru", "Античный мир сравнительная история"), ("en", "connected ancient world"), ("en", "Hellenistic Roman Han Maurya")],
    },
    "STEPPE_SILK": {
        "terms": ["скиф", "scythian", "сак", "saka", "сармат", "sarmatian", "сюнну", "xiongnu", "пазырык", "pazyryk", "тарим", "tarim", "дуньхуан", "dunhuang", "бактри", "bactria", "шёлков", "silk road"],
        "base": [("ru", "Степь и Шёлковые пути"), ("en", "Eurasian Steppe ancient"), ("en", "Silk Roads antiquity")],
    },
    "HAN": {
        "terms": ["империя хань", "han dynasty", "цинь", "qin dynasty", "у-ди", "wudi", "сюнну", "xiongnu", "чанъань", "chang'an", "лоян", "luoyang", "ван ман", "wang mang", "сыма цянь", "sima qian"],
        "base": [("ru", "Империя Хань"), ("en", "Han dynasty"), ("en", "Qin and Han dynasties")],
    },
    "MIXED": {
        "terms": ["древн", "ancient", "цивилизац", "civilization", "archaeolog", "археолог", "river", "река", "письмен"],
        "base": [("ru", "Древние цивилизации"), ("en", "Cradle of civilization")],
    },
}

TYPE_REQUIRED = {
    "RIVER": ["река", "river", "приток", "водоток", "долин"],
    "CITY": ["город", "city", "settlement", "поселен", "археолог", "ancient", "ruin"],
    "SITE": ["археолог", "site", "settlement", "поселен", "ruin", "город", "древн"],
    "REGION": ["регион", "region", "область", "земл", "долин", "географ", "river", "река"],
    "STATE": ["царств", "kingdom", "state", "empire", "государ", "полит", "династ"],
    "DYNASTY": ["династ", "dynasty", "царств", "kingdom", "правител"],
    "PERSON": ["царь", "king", "ruler", "правител", "фараон", "pharaoh", "полковод", "priest", "жрец", "бог", "goddess", "deity"],
    "PEOPLE": ["народ", "people", "tribe", "этнич", "групп", "семит", "италий"],
    "CULTURE": ["культур", "culture", "археолог", "civilization", "цивилизац"],
    "ARTIFACT": ["артефакт", "artifact", "object", "таблич", "tablet", "сосуд", "vessel", "seal", "печат", "стел", "stela", "bronze", "бронз", "pottery", "керамик", "скульп"],
    "BUILDING": ["сооруж", "building", "architecture", "архитект", "храм", "temple", "дворец", "palace", "пирамид", "стена", "wall"],
    "TEXT": ["текст", "text", "литерат", "literature", "надпис", "inscription", "письм", "writing", "tablet", "таблич"],
    "LAW": ["закон", "law", "кодекс", "code", "право", "legal", "стел", "inscription"],
    "RELIGION": ["бог", "goddess", "deity", "религи", "religion", "культ", "cult", "храм", "temple", "миф"],
    "BATTLE": ["битв", "battle", "сражен", "war", "войн"],
    "WAR": ["войн", "war", "battle", "campaign"],
    "EVENT": ["событ", "event", "паден", "collapse", "основан", "foundation", "завоев", "conquest", "войн"],
    "PERIOD": ["период", "period", "age", "эпох", "era"],
}

TYPE_FORBIDDEN = {
    "RIVER": ["млекопита", "животн", "кошка", "хищник", "panthera", "mammal", "animal", "cat family", "танк", "tank", "самол", "aircraft", "кораб", "ship", "ракета", "missile", "фильм", "film", "песня", "song", "альбом", "album", "футболь", "football"],
    "CITY": ["вид животных", "species", "mammal", "животн", "растение", "plant species", "имя", "given name", "surname", "фильм", "film", "альбом", "album", "группа", "band", "компания", "company", "football club"],
    "SITE": ["вид животных", "species", "mammal", "животн", "имя", "given name", "surname", "фильм", "film", "альбом", "album", "компания", "company"],
    "REGION": ["вид животных", "species", "mammal", "животн", "имя", "given name", "surname", "фильм", "film", "альбом", "album"],
    "PERSON": ["река", "river", "город", "city", "деревня", "village", "район", "district", "провинц", "province", "вид животных", "species", "фильм", "film", "альбом", "album"],
    "PEOPLE": ["фильм", "film", "альбом", "album", "музыкальная группа", "band", "football club", "вид животных", "species"],
    "ARTIFACT": ["животн", "species", "mammal", "фильм", "film", "альбом", "album", "football club"],
    "TEXT": ["фильм", "film", "телесериал", "television series", "альбом", "album", "песня", "song", "группа", "band"],
    "LAW": ["фильм", "film", "телесериал", "television series", "альбом", "album", "песня", "song"],
    "RELIGION": ["фильм", "film", "альбом", "album", "песня", "song", "football club"],
}

GLOBAL_FORBIDDEN = [
    "video game", "видеоигра", "телесериал", "television series", "эпизод сериала", "episode of",
    "football club", "футбольный клуб", "sports team", "музыкальная группа", "rock band",
    "software", "программное обеспечение", "company founded", "компания, основанная",
]

TYPE_FALLBACK = {
    "ROME": {
        "ARTIFACT": [("ru", "Римская скульптура"), ("en", "Roman sculpture")],
        "TEXT": [("ru", "Латинская эпиграфика"), ("en", "Latin epigraphy")],
        "LAW": [("ru", "Римское право"), ("en", "Roman law")],
        "BUILDING": [("ru", "Архитектура Древнего Рима"), ("en", "Ancient Roman architecture")],
        "RELIGION": [("ru", "Римская религия"), ("en", "Religion in ancient Rome")],
        "BATTLE": [("ru", "Римская армия"), ("en", "Roman army")],
        "WAR": [("ru", "Римская армия"), ("en", "Roman army")],
    },
    "MESOPOTAMIA": {
        "ARTIFACT": [("ru", "Глиняная табличка"), ("en", "Cuneiform")],
        "TEXT": [("ru", "Клинопись"), ("en", "Cuneiform")],
        "LAW": [("ru", "Законы Ур-Намму"), ("en", "Code of Ur-Nammu")],
        "BUILDING": [("ru", "Зиккурат"), ("en", "Ziggurat")],
        "RELIGION": [("ru", "Шумеро-аккадская мифология"), ("en", "Mesopotamian mythology")],
    },
    "BABYLON": {
        "ARTIFACT": [("ru", "Глиняная табличка"), ("en", "Cuneiform")],
        "TEXT": [("ru", "Клинопись"), ("en", "Cuneiform")],
        "LAW": [("ru", "Законы Хаммурапи"), ("en", "Code of Hammurabi")],
        "BUILDING": [("ru", "Зиккурат"), ("en", "Ziggurat")],
        "RELIGION": [("ru", "Вавилонская религия"), ("en", "Babylonian religion")],
    },
    "EGYPT": {
        "ARTIFACT": [("ru", "Египетская скульптура"), ("en", "Ancient Egyptian art")],
        "TEXT": [("ru", "Египетские иероглифы"), ("en", "Egyptian hieroglyphs")],
        "LAW": [("ru", "Древний Египет"), ("en", "Ancient Egypt")],
        "BUILDING": [("ru", "Египетские пирамиды"), ("en", "Egyptian pyramids")],
        "RELIGION": [("ru", "Древнеегипетская религия"), ("en", "Ancient Egyptian religion")],
    },
    "INDUS": {
        "ARTIFACT": [("ru", "Печати Индской цивилизации"), ("en", "Indus Valley Civilisation")],
        "TEXT": [("ru", "Хараппское письмо"), ("en", "Indus script")],
        "BUILDING": [("ru", "Мохенджо-Даро"), ("en", "Mohenjo-daro")],
    },
    "CHINA": {
        "ARTIFACT": [("ru", "Китайская бронза"), ("en", "Chinese ritual bronzes")],
        "TEXT": [("ru", "Гадательные кости"), ("en", "Oracle bone")],
        "BUILDING": [("ru", "Эрлитоу"), ("en", "Erlitou culture")],
        "RELIGION": [("ru", "Религия Китая"), ("en", "Chinese folk religion")],
    },
    "HITTITES": {
        "terms": ["хетт", "hittite", "хатт", "hatti", "анатол", "anatolia", "hattusa", "сирия", "syria", "клинопис"],
        "base": [("ru", "Хетты"), ("en", "Hittites")],
    },
    "HITTITES": {
        "ARTIFACT": [("en", "Hittite art"), ("en", "Hittites")],
        "TEXT": [("en", "Hittite texts"), ("en", "Hittite cuneiform")],
        "LAW": [("en", "Hittite laws"), ("en", "Edict of Telipinu")],
        "BUILDING": [("en", "Hattusa"), ("en", "Yazılıkaya")],
        "RELIGION": [("en", "Hittite mythology"), ("en", "Hittite religion")],
        "BATTLE": [("en", "Battle of Kadesh"), ("en", "Hittite military")],
        "WAR": [("en", "Hittite military"), ("en", "Hittite Empire")],
    },
    "AEGEAN_BRONZE": {
        "ARTIFACT": [("en", "Minoan art"), ("en", "Mycenaean art")],
        "TEXT": [("en", "Linear A"), ("en", "Linear B")],
        "BUILDING": [("en", "Minoan palace"), ("en", "Mycenae")],
        "RELIGION": [("en", "Minoan religion"), ("en", "Mycenaean religion")],
        "BATTLE": [("en", "Mycenaean Greece"), ("en", "Trojan War")],
        "WAR": [("en", "Mycenaean Greece"), ("en", "Mycenaean military")],
    },
    "BRONZE_INTERNATIONAL": {
        "ARTIFACT": [("en", "Uluburun shipwreck"), ("en", "Oxhide ingot")],
        "TEXT": [("en", "Amarna letters"), ("en", "Ugaritic texts")],
        "BUILDING": [("en", "Royal Palace of Ugarit"), ("en", "Amarna")],
        "RELIGION": [("en", "Baal Cycle"), ("en", "Ancient Near Eastern religion")],
        "STATE": [("en", "Late Bronze Age"), ("en", "Amarna letters")],
        "SYSTEM": [("en", "Amarna letters"), ("en", "Bronze Age trade")],
        "RESOURCE": [("en", "Oxhide ingot"), ("en", "Uluburun shipwreck")],
        "ROUTE": [("en", "Bronze Age trade"), ("en", "Eastern Mediterranean")],
    },
    "ASSYRIA_BABYLON": {
        "ARTIFACT": [("en", "Assyrian sculpture"), ("en", "Neo-Assyrian Empire")],
        "TEXT": [("en", "Library of Ashurbanipal"), ("en", "Assyrian royal inscriptions")],
        "LAW": [("en", "Succession Treaties of Esarhaddon"), ("en", "Neo-Assyrian Empire")],
        "BUILDING": [("en", "Nineveh"), ("en", "Nimrud"), ("en", "Babylon")],
        "RELIGION": [("en", "Ashur (god)"), ("en", "Marduk")],
        "BATTLE": [("en", "Siege of Lachish"), ("en", "Battle of Carchemish")],
        "WAR": [("en", "Neo-Assyrian Empire"), ("en", "Assyrian army")],
        "STATE": [("en", "Neo-Assyrian Empire"), ("en", "Neo-Babylonian Empire")],
        "SYSTEM": [("en", "Neo-Assyrian Empire"), ("en", "Neo-Assyrian state communications")],
        "EVENT": [("en", "Fall of Nineveh"), ("en", "Fall of Babylon")],
        "SOURCE": [("en", "Assyrian royal inscriptions"), ("en", "Babylonian Chronicles")],
        "CONCEPT": [("en", "Neo-Assyrian Empire"), ("en", "Neo-Babylonian Empire")],
    },
    "BRONZE_COLLAPSE": {
        "ARTIFACT": [("en", "Late Bronze Age collapse"), ("en", "Sea Peoples")],
        "TEXT": [("en", "Medinet Habu inscriptions"), ("en", "Ugarit")],
        "BUILDING": [("en", "Hattusa"), ("en", "Mycenae")],
        "RELIGION": [("en", "Sea Peoples"), ("en", "Ancient Near Eastern religion")],
        "STATE": [("en", "Late Bronze Age collapse"), ("en", "Early Iron Age")],
        "SYSTEM": [("en", "Late Bronze Age collapse"), ("en", "Palace economy")],
        "RESOURCE": [("en", "Oxhide ingot"), ("en", "Bronze Age trade")],
        "ROUTE": [("en", "Eastern Mediterranean"), ("en", "Bronze Age trade")],
        "EVENT": [("en", "Late Bronze Age collapse"), ("en", "Sea Peoples")],
        "SOURCE": [("en", "Late Bronze Age collapse"), ("en", "Archaeology")],
        "CONCEPT": [("en", "Late Bronze Age collapse"), ("en", "Early Iron Age")],
    },
    "ISRAEL_JUDAH": {
        "terms": ["израил", "israel", "иуде", "judah", "judaean", "самар", "samaria", "лахиш", "lachish", "левант", "levant", "моав", "moab", "аммон", "edom", "арам", "aramaean", "iron age"],
        "base": [("ru", "Древний Израиль и Иудея"), ("en", "Kingdom of Israel (Samaria)"), ("en", "Kingdom of Judah")],
    },
    "GREECE_ARCHAIC": {
        "terms": ["гре", "greek", "archaic", "архаич", "полис", "polis", "афин", "athens", "спарт", "sparta", "коринф", "corinth", "олимп", "delphi", "колони", "hoplite", "alphabet", "iron age"],
        "base": [("ru", "Архаическая Греция"), ("en", "Archaic Greece"), ("en", "Ancient Greece")],
    },
    "INDIA_VEDIC": {
        "terms": ["вед", "vedic", "india", "инд", "rigveda", "ригвед", "sanskrit", "санскрит", "ganga", "ганг", "kuru", "куру", "mahajanapada", "джанапад"],
        "base": [("ru", "Ведийский период"), ("en", "Vedic period"), ("en", "History of India")],
    },
    "IRON_WORLD": {
        "terms": ["железн", "iron age", "ассир", "assyria", "финик", "phoen", "левант", "levant", "гре", "greek", "чжоу", "zhou", "вед", "vedic", "полис", "polis", "empire"],
        "base": [("ru", "Железный век"), ("en", "Iron Age"), ("en", "Axial Age")],
    },
    "PERSIA": {
        "terms": ["ахеменид", "achaemenid", "перс", "persia", "persian", "кир", "cyrus", "дарий", "darius", "ксеркс", "xerxes", "персепол", "persepolis", "сатрап", "satrap", "iran"],
        "base": [("ru", "Ахеменидская держава"), ("en", "Achaemenid Empire"), ("en", "Ancient Persia")],
    },
    "GREECE_CLASSICAL": {
        "terms": ["классическ", "classical", "гре", "greek", "афин", "athens", "спарт", "sparta", "полис", "polis", "delian", "пелопоннес", "peloponnesian", "фив", "thebes", "македон", "macedon"],
        "base": [("ru", "Классическая Греция"), ("en", "Classical Greece"), ("en", "Ancient Greece")],
    },
    "MIXED": {
        "ARTIFACT": [("ru", "Археологический артефакт"), ("en", "Archaeological artifact")],
        "TEXT": [("ru", "Письменность"), ("en", "Writing")],
        "BUILDING": [("ru", "Архитектура Древнего мира"), ("en", "Ancient architecture")],
    },
}

# Exact disambiguations for known risky names. These are tried before any bare title.
MANUAL_BY_ID = {
    "PER_S_02_01": [("en", "Cyrus the Great"), ("ru", "Кир II Великий")],
    "PER_S_03_01": [("en", "Cyrus Cylinder"), ("ru", "Цилиндр Кира")],
    "PER_S_05_02": [("en", "Behistun Inscription"), ("ru", "Бехистунская надпись")],
    "PER_S_07_02": [("en", "Persepolis"), ("ru", "Персеполь")],
    "PER_S_09_07": [("en", "Battle of Salamis"), ("ru", "Битва при Саламине")],
    "PER_S_10_08": [("en", "Battle of Gaugamela"), ("ru", "Битва при Гавгамелах")],
    "BAB_S_03_05": [("en", "Yamhad"), ("ru", "Ямхад")],
    "RIV_CHN_002": [("en", "Yangtze"), ("ru", "Янцзы")],
    "PER_CHN_004": [("en", "Fu Hao"), ("ru", "Фу Хао")],
    "CITY_CIV_002": [("en", "Uruk"), ("ru", "Урук")],
    "TERM_EGYA_004": [("en", "Serekh"), ("ru", "Серех")],
    "TERM_EGYA2_001": [("en", "Serekh"), ("ru", "Серех")],
    "TERM_EGY_003": [("en", "Menes"), ("ru", "Менес")],
    "PER_EGY2_002": [("en", "Djer"), ("ru", "Джер")],
    "PER_EGY2_009": [("en", "Khufu"), ("ru", "Хуфу")],
    "PER_EGY2_010": [("en", "Khafre"), ("ru", "Хафра")],
    "PER_EGY2_013": [("en", "Unas"), ("ru", "Унас")],
    "PER_EGY2_014": [("en", "Pepi I Meryre"), ("ru", "Пепи I")],
    "REG_IND_002": [("en", "Sindh"), ("ru", "Синд")],
    "REL_MES_A001": [("en", "Sin (mythology)"), ("ru", "Нанна")],
    "TERM_MES_008": [("en", "Tell (archaeology)"), ("ru", "Телль")],
    "CITY_MES_001": [("en", "Eridu"), ("ru", "Эриду")],
    "CITY_MES_003": [("en", "Uruk"), ("ru", "Урук")],
    "CITY_MES_004": [("en", "Eanna"), ("ru", "Эанна")],
    "PER_MES_001": [("en", "Scribe"), ("ru", "Писец")],
    "CITY_MES_007": [("en", "Lagash"), ("ru", "Лагаш")],
    "TERM_MES_016": [("en", "Ensi (Sumerian)"), ("ru", "Энси")],
    "CITY_MES_011": [("en", "Akkad (city)"), ("ru", "Аккад")],
    "PER_MES_009": [("en", "Rimush"), ("ru", "Римуш")],
    "PER_MES_013": [("en", "Gudea"), ("ru", "Гудеа")],
    "TERM_AREP_002": [("en", "Nexum")],
    "PEO_LOW_007": [("en", "Umbri"), ("ru", "Умбры")],
    "REG_MES_002": [("ru", "Тигр (река)"), ("en", "Tigris")],
    "REG_MES_003": [("ru", "Евфрат"), ("en", "Euphrates")],
    "RIV_CIV_002": [("ru", "Месопотамия"), ("en", "Tigris–Euphrates river system")],
    "RIV_IND_001": [("en", "Indus River"), ("ru", "Инд")],
    "RIV_INDA_001": [("en", "Ravi River"), ("ru", "Рави")],
    "RIV_EGY_001": [("ru", "Нил"), ("en", "Nile")],
    "RIV_CIV_001": [("ru", "Нил"), ("en", "Nile")],
    "REG_ARC_001": [("ru", "Тибр"), ("en", "Tiber")],
    "BAB_S_03_02": [("ru", "Мари (древний город)"), ("en", "Mari, Syria")],
    "CITY_MES_008": [("ru", "Киш (город)"), ("en", "Kish (Sumer)")],
    "CITY_MES_010": [("en", "Umma"), ("ru", "Умма")],
    "CITY_MES_006": [("en", "Ur"), ("ru", "Ур")],
    "CITY_CIV_003": [("ru", "Мемфис (Египет)"), ("en", "Memphis, Egypt")],
    "CITY_EGY_002": [("ru", "Мемфис (Египет)"), ("en", "Memphis, Egypt")],
    "PER_EGY_002": [("en", "Ka (pharaoh)"), ("ru", "Ка (фараон)")],
    "PER_EGY2_003": [("en", "Den (pharaoh)"), ("ru", "Ден (фараон)")],
    "SITE_EGY_005": [("en", "Abydos, Egypt"), ("ru", "Абидос")],
    "SITE_EGY_003": [("en", "Maadi culture"), ("ru", "Маади")],
    "SITE_EGY_004": [("en", "Buto"), ("ru", "Буто")],
    "SITE_EGY_001": [("en", "Naqada"), ("ru", "Накада")],
    "TERM_INDA_010": [("en", "Magan (civilization)"), ("ru", "Маган")],
    "SITE_INDA_005": [("en", "Pirak"), ("ru", "Пирак")],
    "SITE_IND_003": [("en", "Amri culture"), ("ru", "Амри")],
    "SITE_INDA_004": [("en", "Rupnagar"), ("ru", "Рупар")],
    "CITY_MESA_004": [("ru", "Сузы"), ("en", "Susa")],
    "CITY_MES_A007": [("en", "Girsu"), ("ru", "Гирсу")],
    "PEOPLE_MES_A001": [("en", "Gutian people"), ("ru", "Гутии")],
    "STATE_MES_A001": [("ru", "Элам"), ("en", "Elam")],
    "BAB_S_01_04": [("en", "Isin"), ("ru", "Исин")],
    "BAB_S_02_05": [("en", "Larsa"), ("ru", "Ларса")],
    "BAB_S_07_01": [("en", "Assur"), ("ru", "Ашшур")],
    "BAB_S_07_02": [("en", "Kültepe"), ("ru", "Кюльтепе")],
    "BAB_S_07_03": [("en", "Karum"), ("ru", "Карум")],
    "CITY_CHNA_001": [("en", "Yanshi Shang City"), ("ru", "Яньши")],
    "SITE_CHN_001": [("en", "Taosi"), ("ru", "Таоси")],
    "SITE_CHN_002": [("en", "Shimao"), ("ru", "Шимао")],
    "SITE_CHN_003": [("en", "Erlitou culture"), ("ru", "Эрлитоу")],
    "CITY_CIV_005": [("en", "Erlitou culture"), ("ru", "Эрлитоу")],
    "PER_CHN_003": [("en", "Wu Ding"), ("ru", "У Дин")],
    "PER_CHN_006": [("en", "King Wu of Zhou"), ("ru", "У-ван")],
    "CITY_LOW_005": [("en", "Cosa"), ("en", "Cosa (Roman colony)")],
    "LOC_LOW_012": [("en", "Regia"), ("ru", "Регия (Древний Рим)")],
    "LOC_LOW_001": [("en", "Caelian Hill"), ("ru", "Целий")],
    "TERM_LOW_006": [("en", "Fasti"), ("ru", "Фасты")],
    "ORG_LOW_001": [("en", "Curia"), ("ru", "Курия (Древний Рим)")],
    "CITY_LOW_001": [("en", "Cales"), ("ru", "Калес")],
    "PEO_LOW_001": [("en", "Marsi"), ("ru", "Марсы")],
    "PEO_LOW_008": [("en", "Osci"), ("ru", "Оски")],
    "PER_ITA_002": [("en", "Brennus (4th century BC)"), ("ru", "Бренн")],
    "PEO_ITA_002": [("en", "Aequi"), ("ru", "Эквы")],
    "CITY_ITA_004": [("en", "Capua"), ("ru", "Капуя")],
    "REL_LOW_001": [("en", "Lares"), ("ru", "Лары")],
    "CITY_ITA_001": [("en", "Veii"), ("ru", "Вейи")],
    "PER_ROM_005": [("en", "Romulus and Remus"), ("ru", "Ромул и Рем")],
}

MANUAL_BY_TITLE = {
    "Ашшур как город и бог": [("en", "Assur"), ("en", "Ashur (god)")],
    "Кальху": [("en", "Nimrud")],
    "Дур-Шаррукин": [("en", "Dur-Sharrukin")],
    "Ниневия Синаххериба": [("en", "Nineveh")],
    "Дворец без соперника": [("en", "Southwest Palace of Sennacherib")],
    "Осада Лахиша": [("en", "Siege of Lachish")],
    "Лахишские рельефы": [("en", "Lachish reliefs")],
    "Падение Самарии": [("en", "Fall of Samaria")],
    "Падение Ниневии": [("en", "Fall of Nineveh")],
    "Нововавилонское царство": [("en", "Neo-Babylonian Empire")],
    "Навуходоносор II": [("en", "Nebuchadnezzar II")],
    "Ворота Иштар": [("en", "Ishtar Gate")],
    "Этеменанки": [("en", "Etemenanki")],
    "Набонид": [("en", "Nabonidus")],
    "Цилиндр Кира": [("en", "Cyrus Cylinder")],
    "Основание Рима": [("ru", "Основание Рима"), ("en", "Founding of Rome")],
    "Ромул": [("ru", "Ромул и Рем"), ("en", "Romulus")],
    "Рем": [("ru", "Ромул и Рем"), ("en", "Remus")],
    "Плач о разрушении Ура": [("en", "Lament for Ur")],
    "Падение Ура": [("en", "Fall of Ur")],
    "Формула года": [("en", "Year name")],
    "Письма из Мари": [("en", "Mari letters"), ("ru", "Мари (древний город)")],
    "Большая ванна": [("en", "Great Bath, Mohenjo-daro")],
    "Гадательные кости": [("en", "Oracle bone")],
    "Недешифрованная письменность": [("en", "Indus script")],
    "Кодекс Хаммурапи": [("en", "Code of Hammurabi")],
    "Законы Хаммурапи": [("en", "Code of Hammurabi")],
    "Стела Хаммурапи": [("en", "Code of Hammurabi")],
    "Ступенчатая пирамида": [("en", "Pyramid of Djoser")],
    "Фивы Среднего царства": [("en", "Thebes, Egypt"), ("ru", "Фивы")],
    "Иттауи": [("en", "Itjtawy")],
    "Гераклеопольское царство": [("en", "Heracleopolis Magna")],
    "Крепость Семна": [("en", "Semna (Nubia)")],
    "Крепость Бухен": [("en", "Buhen")],
    "Аварис": [("en", "Avaris")],
    "Гиксосы": [("en", "Hyksos")],
    "Хиан": [("en", "Khyan")],
    "Апопи": [("en", "Apepi")],
    "Камос": [("en", "Kamose")],
    "Яхмос I": [("en", "Ahmose I")],
    "Хатшепсут": [("en", "Hatshepsut")],
    "Сененмут": [("en", "Senenmut")],
    "Экспедиция в Пунт": [("en", "Land of Punt")],
    "Мегиддо": [("en", "Tel Megiddo")],
    "Битва при Мегиддо": [("en", "Battle of Megiddo (15th century BC)")],
    "Митанни": [("en", "Mitanni")],
    "Ахетатон": [("en", "Amarna")],
    "Атон": [("en", "Aten")],
    "Пер-Рамсес": [("en", "Pi-Ramesses")],
    "Дейр-эль-Медина": [("en", "Deir el-Medina")],
    "Битва при Кадеше": [("en", "Battle of Kadesh")],
    "Египетско-хеттский договор": [("en", "Egyptian–Hittite peace treaty")],
    "Хаттуса": [("en", "Hattusa")],
    "Каниш": [("en", "Kültepe")],
    "Карум Каниш": [("en", "Karum")],
    "Хатты": [("en", "Hattians")],
    "Земля Хатти": [("en", "Hatti")],
    "Анитта": [("en", "Anitta")],
    "Хаттусили I": [("en", "Hattusili I")],
    "Мурсили I": [("en", "Mursili I")],
    "Телепину": [("en", "Telipinu")],
    "Указ Телепину": [("en", "Edict of Telipinu")],
    "Тавананна": [("en", "Tawananna")],
    "Язылыкая": [("en", "Yazılıkaya")],
    "Суппилулиума I": [("en", "Šuppiluliuma I")],
    "Пудухепа": [("en", "Puduḫepa")],
    "Муваталли II": [("en", "Muwatalli II")],
    "Хаттусили III": [("en", "Hattusili III")],
    "Тудхалия IV": [("en", "Tudḫaliya IV")],
    "Тархунтасса": [("en", "Tarhuntassa")],
    "Курунта": [("en", "Kurunta")],
}

STOPWORDS = {
    "древний", "древняя", "древнее", "ранний", "ранняя", "главный", "главная", "система", "центр",
    "период", "культура", "город", "регион", "царство", "царь", "власть", "государство", "история",
    "первый", "великий", "основной", "южный", "северный", "восточный", "западный", "после", "между",
    "ancient", "early", "history", "kingdom", "city", "culture", "period", "system", "region",
}

GENERIC_SHORT = {"тигр", "инд", "ур", "мари", "ка", "ден", "коза", "киш", "ра", "хор", "ся", "шан", "дин", "цун", "цзюэ", "канал", "глина", "битум", "ячмень", "фаянс", "регия", "фасты", "курии"}


def group_for(path: Path, card: dict) -> str:
    p = path.as_posix()
    for token, group in [
        ("/rome/", "ROME"), ("/mesopotamia/", "MESOPOTAMIA"), ("/egypt/", "EGYPT"),
        ("/indus/", "INDUS"), ("/zhou-warring/", "ZHOU_WARRING"), ("/vedic-india/", "INDIA_VEDIC"), ("/iron-world/", "IRON_WORLD"), ("/china/", "CHINA"), ("/babylon/", "BABYLON"), ("/hittites/", "HITTITES"), ("/aegean/", "AEGEAN_BRONZE"), ("/international-bronze/", "BRONZE_INTERNATIONAL"), ("/bronze-collapse/", "BRONZE_COLLAPSE"), ("/bronze-world/", "BRONZE_WORLD"), ("/assyria-babylon/", "ASSYRIA_BABYLON"), ("/phoenicians/", "PHOENICIANS"), ("/israel-judah/", "ISRAEL_JUDAH"), ("/archaic-greece/", "GREECE_ARCHAIC"), ("/classical-greece/", "GREECE_CLASSICAL"), ("/alexander/", "ALEXANDER"), ("/classical-world/", "CLASSICAL_WORLD"), ("/hellenistic/", "HELLENISTIC"), ("/maurya/", "INDIA_MAURYA"), ("/han/", "HAN"), ("/steppe-silk/", "STEPPE_SILK"), ("/hellenistic-roman-world/", "HELLENISTIC_ROMAN_EXAM"), ("/late-roman/", "LATE_ROMAN"), ("/late-religions/", "LATE_RELIGIONS"), ("/migration-kingdoms/", "MIGRATION_KINGDOMS"),
    ]:
        if token in p:
            return group
    if "/comparison/" in p or "/civilizations/" in p:
        return "MIXED"
    return card.get("campaign") or "MIXED"


def normalize_tokens(text: str) -> list[str]:
    words = re.findall(r"[0-9A-Za-zА-Яа-яЁё]+", (text or "").lower())
    result = []
    for word in words:
        if len(word) < 4 or word in STOPWORDS:
            continue
        stem = word[:7] if len(word) > 7 else word
        if stem not in result:
            result.append(stem)
    return result[:10]


def add_candidate(out: list[dict], lang: str, title: str, *, scope: str, trusted: bool = False, min_score: int | None = None) -> None:
    title = (title or "").strip()
    if not title:
        return
    key = (lang, title.casefold())
    if any((item["lang"], item["title"].casefold()) == key for item in out):
        return
    item = {"lang": lang, "title": title, "scope": scope}
    if trusted:
        item["trusted"] = True
    if min_score is not None:
        item["min_score"] = min_score
    out.append(item)


def candidate_profile(card: dict, group: str) -> dict:
    cid, title = card["id"], card["title"].strip()
    candidates: list[dict] = []

    for lang, page in MANUAL_BY_ID.get(cid, []):
        add_candidate(candidates, lang, page, scope="exact", trusted=True, min_score=2)
    for lang, page in MANUAL_BY_TITLE.get(title, []):
        add_candidate(candidates, lang, page, scope="exact", trusted=True, min_score=2)

    original = (card.get("original") or "").strip()
    if original and original.casefold() != title.casefold() and re.search(r"[A-Za-z]", original):
        add_candidate(candidates, "en", original, scope="exact", min_score=4)

    add_candidate(candidates, "ru", title, scope="exact", min_score=4)

    for lang, page in TYPE_FALLBACK.get(group, {}).get(card.get("type"), []):
        add_candidate(candidates, lang, page, scope="context", trusted=True, min_score=2)

    for lang, page in GROUP_CONTEXT[group]["base"]:
        add_candidate(candidates, lang, page, scope="context", trusted=True, min_score=2)

    # Six candidates is enough, but every one is now tied to the card or its historical context.
    candidates = candidates[:6]

    subject_text = " ".join([title, original, card.get("subtitle", ""), " ".join(card.get("tags") or [])])
    subject_terms = normalize_tokens(subject_text)
    title_norm = re.sub(r"[^0-9a-zа-яё]+", " ", title.lower()).strip()
    strict_context = (
        len(title_norm.replace(" ", "")) <= 5
        or title_norm in GENERIC_SHORT
        or card.get("type") in {"RIVER", "CITY", "SITE", "REGION", "PERSON", "PEOPLE"}
    )

    semantic = {
        "subject_terms": subject_terms,
        "group_terms": GROUP_CONTEXT[group]["terms"],
        "required_any": TYPE_REQUIRED.get(card.get("type"), []),
        "forbidden": sorted(set(GLOBAL_FORBIDDEN + TYPE_FORBIDDEN.get(card.get("type"), []))),
        "strict_context": strict_context,
    }

    return {
        "group": group,
        "type": card.get("type"),
        "query": " ".join(x for x in [title, card.get("subtitle", ""), card.get("region", ""), card.get("era", "")] if x).strip(),
        "semantic": semantic,
        "candidates": candidates,
    }


def main() -> None:
    cards_out: dict[str, dict] = {}
    cards = []
    for path in sorted(ROOT.glob("data/cards/*/*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for card in payload:
            group = group_for(path, card)
            cards_out[card["id"]] = candidate_profile(card, group)
            cards.append(card)

    payload = {
        "version": VERSION,
        "generatedAt": "2026-07-14",
        "strategy": "Semantically validated Wikipedia PageImages + Wikimedia Commons metadata with local fallback",
        "count": len(cards_out),
        "cards": cards_out,
        "notes": [
            "Случайные кандидаты из общего пула удалены.",
            "Неоднозначные названия получают контекстную или англоязычную статью до голого совпадения.",
            "Статья принимается только после проверки описания, вводного текста и категорий.",
            "При низкой уверенности остаётся локальная обложка — неправильное изображение не подставляется.",
        ],
    }
    (ROOT / "data/image_queries.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    old_path = ROOT / "data/image_queries.v312.backup.json"
    if old_path.exists():
        old_path.unlink()

    counts = Counter(profile["type"] for profile in cards_out.values())
    manual = sum(1 for cid in cards_out if cid in MANUAL_BY_ID)
    strict = sum(1 for profile in cards_out.values() if profile["semantic"]["strict_context"])
    candidates = sum(len(profile["candidates"]) for profile in cards_out.values())
    print(f"generated {len(cards_out)} profiles · {candidates} candidates · {manual} manual disambiguations · {strict} strict profiles")
    print("types", dict(counts))


if __name__ == "__main__":
    main()
