# Codex of History — Architecture v1.1

## Цель рефакторинга

Версия 1.1 отделяет контент от игрового движка. Новые карточки, кампании, пулы и личные истории добавляются через JSON, а не через правки монолитного `app.js`.

## Загрузка

1. `index.html` запускает `js/bootstrap.js`.
2. Bootstrap читает `data/content-manifest.json`.
3. JSON загружаются параллельно и объединяются в реестры.
4. JS-модули загружаются последовательно, чтобы сохранить совместимость с текущим UI и inline-событиями.
5. `js/core/start.js` запускает приложение.

## Структура

```text
js/
├─ bootstrap.js
├─ core/       # состояние, хранение, общие функции, запуск
├─ maps/       # Leaflet и географические слои
├─ features/   # кампании, квизы, mastery, паки, пулы, истории
└─ views/      # базовые экраны

data/
├─ cards/rome/
├─ campaigns/rome/
├─ quizzes/rome/
├─ stories/rome/
├─ maps/
├─ core/
└─ schemas/
```

## Добавление кампании

Новая кампания получает собственные папки в `cards`, `campaigns`, `quizzes`, `stories` и `maps`. Затем пути добавляются в `data/content-manifest.json`. Основной движок менять не требуется.

## Реестры

Bootstrap создаёт `CODEX_REGISTRY`: карточки, миссии, пулы и связи доступны по ID без постоянного полного перебора массивов.

## Проверка

```bash
node tools/validate-content.mjs
```

GitHub Action запускает эту проверку автоматически.
