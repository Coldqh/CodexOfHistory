# Codex of History — GitHub Pages MVP v0.1

Чистое статичное веб-приложение под GitHub Pages.

## Что внутри

- `index.html` — главный файл приложения
- `styles.css` — стили
- `app.js` — логика, демо-данные, навигация, квизы, прогресс
- `data/` — JSON seed для будущего подключения к API или импорту
- `csv/` — CSV-таблицы для Google Sheets
- `sql/` — PostgreSQL/Supabase schema
- `docs/` — архитектура и план следующих патчей
- `.nojekyll` — чтобы GitHub Pages не ломал статичные файлы

## Запуск локально

Можно просто открыть `index.html`.

Или через локальный сервер:

```bash
python -m http.server 8000
```

Потом открыть:

```text
http://localhost:8000
```

## Деплой на GitHub Pages

1. Создай репозиторий на GitHub.
2. Загрузи содержимое этой папки в корень репозитория.
3. Открой Settings → Pages.
4. Source: Deploy from a branch.
5. Branch: `main` / root.
6. Сохрани.

После этого GitHub выдаст ссылку вида:

```text
https://username.github.io/repository-name/
```

## Важно

Это static MVP. Backend не нужен. Node, React, сборка и база данных для запуска не требуются.

SQL и JSON лежат как основа для следующих версий.
