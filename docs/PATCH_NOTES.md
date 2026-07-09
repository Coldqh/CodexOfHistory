# Codex of History — MVP Patch v0.1

## Что вошло в патч

### 1. Рабочий мобильный web-прототип
Папка: `app/`

Файлы:
- `index.html`
- `styles.css`
- `app.js`

Что умеет:
- Home screen
- Campaign screen
- Collection screen
- Card Detail screen
- Quiz screen
- Map screen
- Profile screen
- локальный прогресс через `localStorage`
- XP и уровни
- открытие карточек
- Daily Pack
- фильтр коллекции
- поиск по карточкам
- связи между карточками
- упрощённая карта

### 2. Data seed
Папка: `data/`

Файлы:
- `cards.json`
- `relations.json`
- `campaigns.json`
- `quizzes.json`
- `sources.json`

Внутри:
- 14 стартовых карточек по Риму
- 14 связей графа
- 1 кампания Rome: From City to Empire
- 5 квизов
- список источников-заглушек для фактчека

### 3. SQL architecture
Папка: `sql/`

Файлы:
- `schema.sql`
- `seed_minimal.sql`

Схема рассчитана не на 50 карточек, а на десятки тысяч:
- cards
- card_attributes JSONB
- card_relations
- campaigns
- campaign_nodes
- missions
- lessons
- story_episodes
- quizzes
- questions
- sources
- citations
- locations
- timeline_entries
- user progress
- review queue
- packs

### 4. CSV-экспорт
Папка: `csv/`

Файлы:
- `cards.csv`
- `relations.csv`
- `campaign_nodes.csv`
- `questions.csv`

Нужно для Google Sheets / ручного редактирования / будущего импорта.

---

## Как открыть прототип

### Вариант 1
Открыть файл:

`app/index.html`

### Вариант 2
Через локальный сервер:

```bash
cd app
python -m http.server 8000
```

Потом открыть:

```text
http://localhost:8000
```

---

## Что важно

Это не финальный продукт. Это первый живой скелет.

Уже заложены правильные рельсы:

- карточки отдельно;
- кампании отдельно;
- связи отдельно;
- квизы отдельно;
- прогресс отдельно;
- источники отдельно;
- миссии можно добавлять данными, а не кодом.

---

## Следующий патч

Лучший следующий шаг:

1. перенести `app.js` на нормальные модули;
2. сделать импорт из `data/*.json`, а не держать данные внутри JS;
3. добавить 50 карточек-скелетов;
4. сделать визуальный Campaign Builder в JSON;
5. добавить экран Timeline;
6. добавить карточные арты/промпты;
7. подключить Supabase.
