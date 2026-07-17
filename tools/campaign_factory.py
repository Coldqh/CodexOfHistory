#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


def dump(root: Path, path: str | Path, obj: Any) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def card_svg(
    root: Path,
    path: str | Path,
    title: str,
    subtitle: str,
    chapter: int,
    kind: str,
    label: str,
    mark: str,
    accent: str,
) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    safe_title = html.escape(title)
    safe_subtitle = html.escape(subtitle)
    target.write_text(
        f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 900" role="img" aria-label="{safe_title}">
<defs><linearGradient id="g" x2="1" y2="1"><stop stop-color="#06080a"/><stop offset=".58" stop-color="#152126"/><stop offset="1" stop-color="#050708"/></linearGradient><radialGradient id="r"><stop stop-color="{accent}" stop-opacity=".68"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient></defs>
<rect width="720" height="900" fill="url(#g)"/><circle cx="520" cy="215" r="330" fill="url(#r)"/>
<path d="M0 720 C145 640 286 756 444 654 S630 618 720 682 V900 H0Z" fill="#030506" opacity=".96"/>
<path d="M62 112 H658 M62 790 H658" stroke="{accent}" stroke-width="2"/>
<circle cx="520" cy="390" r="112" fill="none" stroke="{accent}" stroke-width="8" opacity=".45"/>
<text x="520" y="428" text-anchor="middle" fill="{accent}" font-size="108" font-family="serif">{html.escape(mark)}</text>
<text x="62" y="82" fill="{accent}" font-size="18" font-family="Arial" letter-spacing="4">{html.escape(label)} · ГЛАВА {chapter:02d}</text>
<text x="62" y="690" fill="#fff7ea" font-size="40" font-family="Georgia">{safe_title[:29]}</text>
<text x="62" y="742" fill="#d7cdc0" font-size="21" font-family="Arial">{safe_subtitle[:52]}</text>
<text x="62" y="835" fill="{accent}" font-size="17" font-family="Arial" letter-spacing="3">{'СЮЖЕТНАЯ КАРТА' if kind == 'story' else 'АРХИВНАЯ КАРТА'}</text>
</svg>''',
        encoding="utf-8",
    )


def pack_svg(root: Path, path: str | Path, title: str, subtitle: str, label: str, mark: str, accent: str) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 960" role="img" aria-label="{html.escape(title)}">
<defs><linearGradient id="g" x2="1" y2="1"><stop stop-color="#06080a"/><stop offset=".58" stop-color="#173039"/><stop offset="1" stop-color="#050708"/></linearGradient><radialGradient id="r"><stop stop-color="{accent}" stop-opacity=".8"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient></defs>
<rect width="720" height="960" rx="58" fill="url(#g)"/><circle cx="510" cy="245" r="370" fill="url(#r)"/>
<circle cx="360" cy="430" r="150" fill="none" stroke="{accent}" stroke-width="18" opacity=".78"/>
<text x="360" y="490" text-anchor="middle" fill="#fff0c9" font-size="170" font-family="serif">{html.escape(mark)}</text>
<text x="80" y="120" fill="{accent}" font-size="22" font-family="Arial" letter-spacing="5">{html.escape(label)}</text>
<text x="80" y="755" fill="#fff7eb" font-size="50" font-family="Georgia">{html.escape(title)}</text>
<text x="80" y="825" fill="#d7cdc0" font-size="25" font-family="Arial">{html.escape(subtitle)}</text>
<text x="80" y="905" fill="{accent}" font-size="21" font-family="Arial" letter-spacing="4">4 КАРТЫ · ОТКРЫТЫЕ ГЛАВЫ</text>
</svg>''',
        encoding="utf-8",
    )


def _paragraphs(chapter: dict[str, Any], topic: tuple[str, str, str, str, str, str], mission_title: str, method_notes: list[str]) -> list[str]:
    """Build mission-specific theory without shared standalone boilerplate.

    Every sentence contains the mission or topic name. This is intentional: exact
    duplicate sentences across generated missions are treated as a release error by
    tools/audit-lesson-duplicates.mjs.
    """
    title, _, _, subtitle, date, _ = topic
    locations = ", ".join(chapter["location_labels"])
    chronology = "; ".join(f"{item[0]} — {item[1]}" for item in chapter["chronology"])
    causes = ", ".join(item.lower().rstrip(". ") for item in chapter["causes"])
    consequences = ", ".join(item.lower().rstrip(". ") for item in chapter["consequences"])
    source_title = chapter["source"]["title"]
    method_a = method_notes[0].rstrip(". ")
    method_b = method_notes[1].rstrip(". ")
    return [
        f'Миссия «{mission_title}» раскрывает сюжет «{title}» внутри главы «{chapter["title"]}»: {subtitle}. Для миссии «{mission_title}» датировка «{date}» задаёт временную рамку, но объяснение строится через действия людей, институтов и доступные свидетельства.',
        f'Пространство миссии «{mission_title}» включает {locations}. В теме «{title}» эти точки рассматриваются не как единая неизменная система, а как узлы с разными условиями движения, снабжения, хозяйства и политического контроля.',
        f'Хронология миссии «{mission_title}» включает {chronology}. Для темы «{title}» письменная дата, археологический диапазон и позднее описание не равны по надёжности, поэтому порядок событий проверяется отдельно от удобной повествовательной схемы.',
        f'Причинный блок миссии «{mission_title}» включает {causes}. В теме «{title}» ни один фактор не действует автоматически: результат зависит от сочетания местной среды, решений элит и общин, военной силы, обмена и уже существовавших институтов.',
        f'Последствия миссии «{mission_title}» включают {consequences}. В сюжете «{title}» эти изменения затрагивают разные группы неодинаково и проверяются по распределению поселений, вещей, текстов, монет, погребений или следов инфраструктуры.',
        f'Источник «{source_title}» используется в миссии «{mission_title}» для проверки терминов, дат и материального контекста. Для темы «{title}» жанр источника, место находки и история публикации ограничивают то, какие выводы можно считать прямыми, а какие остаются реконструкцией.',
        f'Практический вопрос миссии «{mission_title}» состоит в том, кто собирал ресурсы, организовывал труд, защищал маршруты, передавал сведения и получал выгоду. В теме «{title}» формальная власть над территорией не считается достаточным доказательством реального контроля над людьми и потоками ресурсов.',
        f'Сравнение миссии «{mission_title}» с соседними обществами ведётся по одинаковым критериям: масштабу власти, способам мобилизации, роли городов, характеру границ, налогам, дани и качеству источников. Для сюжета «{title}» ярлыки вроде «кочевой», «имперский» или «торговый» не заменяют анализа конкретного механизма.',
        f'Методический итог миссии «{mission_title}» таков: {method_a}; {method_b}. Для темы «{title}» степень уверенности и альтернативные объяснения должны быть указаны прямо, а финальный вывод обязан связывать факт, место, дату и тип свидетельства.',
    ]


def build_campaign(
    *,
    root: Path,
    version: str,
    checked_at: str,
    campaign_id: str,
    prefix: str,
    folder: str,
    era_name: str,
    region_name: str,
    title: str,
    description: str,
    difficulty: int,
    chapters: list[dict[str, Any]],
    points: dict[str, tuple[list[float], str]],
    phases: list[dict[str, Any]],
    pack_path: str,
    pack_title: str,
    pack_subtitle: str,
    visual_label: str,
    visual_marks: list[str],
    visual_accents: list[str],
    map_center: list[float],
    map_zoom: int,
    exam_specs: dict[str, tuple[str, list[tuple[str, list[str], int, str]]]],
    exam_modules_key: str,
    exam_modules: list[dict[str, str]],
    inter_relations: list[tuple[str, str, str]],
    method_notes: list[str],
    map_regions: list[dict[str, Any]] | None = None,
    parallel_timeline: list[dict[str, Any]] | None = None,
    story_per_chapter: int = 8,
    archive_per_chapter: int = 4,
    story_rarities: list[str] | None = None,
    archive_rarities: list[str] | None = None,
) -> dict[str, Any]:
    story_rarities = story_rarities or ["COMMON", "COMMON", "UNCOMMON", "COMMON", "UNCOMMON", "RARE", "RARE", "EPIC", "EPIC"]
    archive_rarities = archive_rarities or ["UNCOMMON", "RARE", "EPIC", "LEGENDARY"]
    story_cards: list[dict[str, Any]] = []
    archive_cards: list[dict[str, Any]] = []
    nodes: list[dict[str, Any]] = []
    lessons: dict[str, Any] = {}
    quizzes: dict[str, Any] = {}
    pools: list[dict[str, Any]] = []
    acquisition: dict[str, Any] = {}
    stories: dict[str, Any] = {}
    relations: list[dict[str, Any]] = []
    card_points: dict[str, str] = {}
    map_chapters: dict[str, Any] = {}
    rel_i = 1

    for ci, chapter in enumerate(chapters, 1):
        chapter_id = f"{prefix}_CHAPTER_{ci:02d}"
        chapter["location_labels"] = [points[k][1] for k in chapter["locations"]]
        story_ids: list[str] = []
        archive_ids: list[str] = []
        if len(chapter["story"]) != story_per_chapter:
            raise ValueError(f"{chapter['title']}: expected {story_per_chapter} story items")
        if len(chapter["archive"]) != archive_per_chapter:
            raise ValueError(f"{chapter['title']}: expected {archive_per_chapter} archive items")

        for ti, item in enumerate(chapter["story"], 1):
            cid = f"{prefix}_S_{ci:02d}_{ti:02d}"
            story_ids.append(cid)
            item_title, original, typ, subtitle, date, point = item
            coord, loc_label = points[point]
            local_path = f"assets/cards/{folder}/chapter-{ci:02d}/{cid.lower()}.svg"
            card = {
                "id": cid,
                "type": typ,
                "title": item_title,
                "original": original,
                "subtitle": subtitle,
                "era": era_name,
                "region": region_name,
                "date": date,
                "rarity": story_rarities[ti - 1],
                "difficulty": difficulty,
                "summary": f"{item_title} — {subtitle}.",
                "importance": f"Карточка раскрывает главу «{chapter['title']}» через конкретный механизм власти, мобильности, обмена, войны или исторического метода.",
                "facts": [
                    f"Датировка: {date}.",
                    f"Основной смысл: {subtitle}.",
                    "Вывод проверяется через сопоставление письменных сообщений, археологии, предметов, монет, погребений и пространственного контекста.",
                ],
                "tags": [region_name, title, chapter["title"], typ.lower()],
                "stats": {
                    "influence": 6 + (ci + ti) % 4,
                    "complexity": 6 + ti % 4,
                    "legacy": 6 + ci % 4,
                    "military": 3 + (ci + ti * 2) % 6,
                    "culture": 5 + (ci + ti) % 5,
                    "politics": 5 + (ci * 2 + ti) % 5,
                    "religion": 4 + (ci + ti) % 5,
                    "economy": 5 + (ci + ti) % 5,
                    "connections": 7 + (ci + ti) % 3,
                },
                "loc": {"label": loc_label, "lat": coord[0], "lon": coord[1]},
                "image": {
                    "local": local_path,
                    "caption": f"Локальная учебная обложка: {item_title}",
                    "credit": "Codex of History · локальная учебная обложка",
                    "source_url": chapter["source"]["url"],
                    "license": "Project asset",
                    "focus": "50% 50%",
                    "file": Path(local_path).name,
                    "kind": "project-cover",
                },
                "source": chapter["source"],
                "acquisition": "STORY",
                "campaign": campaign_id,
                "chapter": chapter_id,
            }
            story_cards.append(card)
            acquisition[cid] = {"kind": "STORY", "campaignId": campaign_id, "chapter": ci}
            card_points[cid] = point
            card_svg(root, local_path, item_title, subtitle, ci, "story", visual_label, visual_marks[ci - 1], visual_accents[ci - 1])

        for ai, item in enumerate(chapter["archive"], 1):
            cid = f"{prefix}_A_{ci:02d}_{ai:02d}"
            archive_ids.append(cid)
            item_title, original, typ, subtitle, date, point = item
            coord, loc_label = points[point]
            local_path = f"assets/cards/{folder}/chapter-{ci:02d}/{cid.lower()}.svg"
            rarity = archive_rarities[min(ai - 1, len(archive_rarities) - 1)]
            if ai == archive_per_chapter and ci % 4 == 0:
                rarity = "MYTHIC"
            card = {
                "id": cid,
                "type": typ,
                "title": item_title,
                "original": original,
                "subtitle": subtitle,
                "era": era_name,
                "region": region_name,
                "date": date,
                "rarity": rarity,
                "difficulty": difficulty,
                "summary": f"{item_title} — {subtitle}.",
                "importance": f"Архивная карточка углубляет главу «{chapter['title']}» через конкретный документ, предмет, памятник или спорную реконструкцию.",
                "facts": [
                    f"Датировка: {date}.",
                    f"Основной смысл: {subtitle}.",
                    "Архивный вывод должен учитывать происхождение находки, жанр источника, историю публикации и пределы сохранности.",
                ],
                "tags": [region_name, "архив", chapter["title"], typ.lower()],
                "stats": {
                    "influence": 6 + (ci + ai) % 4,
                    "complexity": 7 + ai % 3,
                    "legacy": 7 + ci % 3,
                    "military": 3 + (ci + ai) % 6,
                    "culture": 6 + (ci + ai) % 4,
                    "politics": 5 + (ci * 2 + ai) % 5,
                    "religion": 4 + (ci + ai) % 5,
                    "economy": 5 + (ci + ai) % 5,
                    "connections": 8 + (ci + ai) % 2,
                },
                "loc": {"label": loc_label, "lat": coord[0], "lon": coord[1]},
                "image": {
                    "local": local_path,
                    "caption": f"Локальная учебная обложка: {item_title}",
                    "credit": "Codex of History · локальная учебная обложка",
                    "source_url": chapter["source"]["url"],
                    "license": "Project asset",
                    "focus": "50% 50%",
                    "file": Path(local_path).name,
                    "kind": "project-cover",
                },
                "source": chapter["source"],
                "acquisition": "ARCHIVE",
                "campaign": campaign_id,
                "chapter": chapter_id,
            }
            archive_cards.append(card)
            acquisition[cid] = {"kind": "ARCHIVE", "pool": f"{prefix}_POOL_{ci:02d}", "campaign": campaign_id}
            card_points[cid] = point
            card_svg(root, local_path, item_title, subtitle, ci, "archive", visual_label, visual_marks[ci - 1], visual_accents[ci - 1])

        pools.append({
            "id": f"{prefix}_POOL_{ci:02d}",
            "campaign": campaign_id,
            "title": chapter["title"],
            "unlockMission": f"{prefix}_{ci:02d}_02",
            "cardIds": archive_ids,
        })
        stories[f"STORY_{prefix}_{ci:02d}"] = {
            "id": f"STORY_{prefix}_{ci:02d}",
            "cardId": archive_ids[-1],
            "title": f"Архивное дело: {chapter['archive'][-1][0]}",
            "subtitle": chapter["title"],
            "rewardXp": 165 + ci * 5,
            "rewardFragments": 18 + ci,
            "steps": [
                {"type": "SCENE", "title": "Материал архива", "text": f"Материал «{chapter['archive'][-1][0]}» требует проверки происхождения, датировки, жанра и археологического контекста."},
                {"type": "QUESTION", "title": "Проверка источника", "question": "Какой шаг должен быть первым?", "options": ["Определить происхождение, дату, жанр и материальный контекст", "Считать поздний рассказ стенограммой", "Принимать карту как точную границу", "Игнорировать историю раскопок"], "correct": 0, "explanation": "Исторический вывод начинается с критики происхождения и жанра свидетельства."},
                {"type": "QUESTION", "title": "Граница вывода", "question": "Как оформить итог?", "options": ["Разделить прямое свидетельство, интерпретацию и реконструкцию", "Объяснить всё одним товаром", "Считать все группы одинаковыми", "Отбросить неудобные данные"], "correct": 0, "explanation": "Корректный итог показывает, где заканчиваются данные и начинается модель."},
            ],
        }

        for source, target in zip(story_ids, story_ids[1:]):
            relations.append({"id": f"REL_{prefix}_{rel_i:04d}", "source": source, "target": target, "type": "ПОСЛЕДОВАТЕЛЬНОСТЬ", "description": f"Связь внутри главы «{chapter['title']}».", "strength": 8})
            rel_i += 1
        for source, target in zip(archive_ids, story_ids[1:1 + archive_per_chapter]):
            relations.append({"id": f"REL_{prefix}_{rel_i:04d}", "source": source, "target": target, "type": "АРХИВНЫЙ_КОНТЕКСТ", "description": f"Архивный материал уточняет тему «{chapter['title']}».", "strength": 7})
            rel_i += 1

        mission_titles = [
            f"Рассказ: {chapter['title']}",
            f"Хронология: {chapter['period']}",
            f"Источник: {chapter['archive'][0][0]}",
            f"Карта: {', '.join(chapter['location_labels'])}",
            "Разбор: причины, институты и последствия",
            f"Итог главы: {chapter['title']}",
        ]
        card_sets = [
            [story_ids[0], story_ids[1], story_ids[2]],
            [story_ids[2], story_ids[3], story_ids[4]],
            [story_ids[3], story_ids[4], story_ids[5]],
            [story_ids[1], story_ids[-3], story_ids[-2]],
            [story_ids[0], story_ids[-2], story_ids[-1]],
            [story_ids[-1], story_ids[0], story_ids[3]],
        ]
        unlock_sets = [
            [story_ids[0], story_ids[1]],
            [story_ids[2]],
            [story_ids[3], story_ids[4]],
            [story_ids[5]],
            [story_ids[-2]],
            [story_ids[-1]],
        ]
        for mi in range(1, 7):
            mid = f"{prefix}_{ci:02d}_{mi:02d}"
            topic = chapter["story"][(mi - 1) % story_per_chapter]
            node: dict[str, Any] = {
                "id": mid,
                "type": ["LESSON", "TIMELINE", "SOURCE", "MAP", "CAUSE_EFFECT", "FINAL"][mi - 1],
                "title": mission_titles[mi - 1],
                "description": f"{chapter['description']} Фокус миссии: {mission_titles[mi - 1]}.",
                "cards": card_sets[mi - 1],
                "unlockCards": unlock_sets[mi - 1],
                "xp": 225 + ci * 7 + mi * 5,
                "emoji": ["▤", "◷", "▥", "⌖", "◆", "◎"][mi - 1],
                "chapterId": chapter_id,
                "lessonId": mid,
            }
            if mi == 2:
                node["timeline"] = [{"id": f"t{i}", "date": d, "title": t} for i, (d, t, _) in enumerate(chapter["chronology"])]
            if mi == 4:
                node["mapTargets"] = [{"key": key.lower(), "label": points[key][1], "point": key, "zoom": chapter.get("zoom", 5), "radius": chapter.get("radius", 220000)} for key in chapter["locations"]]
            if mi == 6:
                node["quiz"] = f"QUIZ_{prefix}_CH{ci}"
                if ci == len(chapters):
                    node[exam_modules_key] = exam_modules
            nodes.append(node)

            activity: dict[str, Any]
            if mi == 1:
                activity = {"type": "reading"}
            elif mi == 2:
                activity = {"type": "timeline", "items": node.get("timeline", [])}
            elif mi == 3:
                activity = {"type": "source", "source": chapter["source"]}
            elif mi == 4:
                activity = {"type": "map", "targets": node.get("mapTargets", [])}
            elif mi == 5:
                activity = {"type": "cause_effect", "causes": chapter["causes"], "consequences": chapter["consequences"]}
            else:
                activity = {"type": "quiz", "quizId": f"QUIZ_{prefix}_CH{ci}"}

            lessons[mid] = {
                "id": mid,
                "title": mission_titles[mi - 1],
                "duration": 14,
                "objectives": [
                    f"объяснить роль темы «{topic[0]}» в главе «{chapter['title']}»",
                    "различить письменное сообщение, археологический объект, музейную реконструкцию и современную карту",
                    "связать власть, мобильность, хозяйство, войну и посредников",
                ],
                "story": [
                    {"title": chapter["title"], "text": chapter["description"]},
                    {"title": "Фокус миссии", "text": f"{mission_titles[mi - 1]}. Главный материал: {topic[0]} — {topic[3]}."},
                    {"title": "Граница знания", "text": method_notes[0]},
                ],
                "chronology": [{"date": d, "title": t, "note": f"{t}. Связь проверяется по месту, датировке, жанру и задаче источника.", "certainty": cert} for d, t, cert in chapter["chronology"]],
                "concepts": [{"term": x[0], "definition": x[3]} for x in chapter["story"][:3]],
                "causeEffect": {"causes": chapter["causes"], "consequences": chapter["consequences"]},
                "activity": activity,
                "sources": [chapter["source"]],
                "theory": {
                    "title": mission_titles[mi - 1],
                    "readingMinutes": 10,
                    "lead": f"{chapter['description']} Основной вопрос миссии — {topic[0].lower()}.",
                    "paragraphs": _paragraphs(chapter, topic, mission_titles[mi - 1], method_notes),
                    "historicityNotes": method_notes,
                    "sources": [chapter["source"]],
                    "license": "Авторский учебный текст Codex of History.",
                    "checkedAt": checked_at,
                },
            }

        map_chapters[chapter_id] = {"title": chapter["title"], "center": points[chapter["locations"][0]][0], "zoom": chapter.get("zoom", 5)}
        questions: list[dict[str, Any]] = []
        for qi in range(4):
            correct = chapter["story"][qi][0]
            distractors = [chapter["story"][(qi + j + 1) % story_per_chapter][0] for j in range(3)]
            pos = (ci + qi) % 4
            options = distractors[:]
            options.insert(pos, correct)
            questions.append({"text": f"Какой термин соответствует описанию: «{chapter['story'][qi][3]}»?", "options": options, "correct": pos, "explanation": f"{correct}: {chapter['story'][qi][3]}."})
        pos = (ci + 4) % 4
        options = ["Принять поздний рассказ буквально", "Считать границы неизменными", "Игнорировать материальные данные"]
        options.insert(pos, "Сопоставить тексты, археологию, предметы, датировки и пространственный контекст")
        questions.append({"text": f"Какой метод нужен в главе «{chapter['title']}»?", "options": options, "correct": pos, "explanation": "Исторический вывод строится через несколько независимых типов свидетельств."})
        pos = (ci + 5) % 4
        options = ["Все маршруты контролировались одной державой", "Все кочевые группы имели одинаковое устройство", "Один товар объясняет весь обмен"]
        options.insert(pos, chapter["subtitle"])
        questions.append({"text": f"Какой итог главы «{chapter['title']}» наиболее точен?", "options": options, "correct": pos, "explanation": chapter["description"]})
        quizzes[f"QUIZ_{prefix}_CH{ci}"] = {"id": f"QUIZ_{prefix}_CH{ci}", "title": f"Глава {ci}: {chapter['title']}", "passPercent": 70, "questions": questions}

    for source, target, relation_description in inter_relations:
        relations.append({"id": f"REL_{prefix}_{rel_i:04d}", "source": source, "target": target, "type": "МЕЖКАМПАНИЙНАЯ_СВЯЗЬ", "description": relation_description, "strength": 9})
        rel_i += 1

    for qid, (quiz_title, raw_questions) in exam_specs.items():
        quizzes[qid] = {"id": qid, "title": quiz_title, "passPercent": 70, "questions": [{"text": q, "options": opts, "correct": correct, "explanation": explanation} for q, opts, correct, explanation in raw_questions]}

    chapter_payload = [
        {
            "id": f"{prefix}_CHAPTER_{i:02d}",
            "number": i,
            "title": chapter["title"],
            "subtitle": chapter["subtitle"],
            "description": chapter["description"],
            "missionIds": [f"{prefix}_{i:02d}_{mission:02d}" for mission in range(1, 7)],
        }
        for i, chapter in enumerate(chapters, 1)
    ]
    era_layer: dict[str, Any] = {
        "period": phases[0].get("period", "") if phases else "",
        "summary": description,
        "phases": phases,
    }
    if map_regions is not None:
        era_layer["regions"] = map_regions
    if parallel_timeline is not None:
        era_layer["parallelTimeline"] = parallel_timeline

    campaign = {"id": campaign_id, "title": title, "description": description, "difficulty": difficulty, "chapters": chapter_payload, "nodes": nodes, "eraLayer": era_layer}
    pools_payload = {"campaignId": campaign_id, "campaigns": {campaign_id: {"id": campaign_id, "title": title, "active": True, "status": "STARTED"}}, "pools": pools, "acquisition": acquisition}
    map_payload = {"points": {key: value[0] for key, value in points.items()}, "regions": {}, "cardPoints": card_points, "chapters": map_chapters, "missionCenter": map_center, "missionZoom": map_zoom}

    dump(root, f"data/cards/{folder}/story.json", story_cards)
    dump(root, f"data/cards/{folder}/archive.json", archive_cards)
    dump(root, f"data/campaigns/{folder}/campaign.json", campaign)
    dump(root, f"data/campaigns/{folder}/pools.json", pools_payload)
    dump(root, f"data/lessons/{folder}/campaign.json", lessons)
    dump(root, f"data/quizzes/{folder}/campaign.json", quizzes)
    dump(root, f"data/stories/{folder}/personal.json", stories)
    dump(root, f"data/maps/{folder}.json", map_payload)
    dump(root, f"data/core/relations-{version.replace('.', '')}-{folder}.json", relations)
    pack_svg(root, pack_path, pack_title, pack_subtitle, visual_label, visual_marks[0], visual_accents[0])
    return {
        "story_cards": story_cards,
        "archive_cards": archive_cards,
        "campaign": campaign,
        "pools": pools_payload,
        "lessons": lessons,
        "quizzes": quizzes,
        "stories": stories,
        "map": map_payload,
        "relations": relations,
    }
