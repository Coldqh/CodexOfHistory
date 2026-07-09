# Codex of History — MVP v0.2 RU/UI

Статичное приложение под GitHub Pages.

## Что внутри

- русский UI и русский контент первого модуля;
- отдельное поведение под ПК и телефон;
- новый исторический UI: codex / карта / коллекция;
- изображения карточек через Wikimedia Commons Special:FilePath;
- fallback SVG, если картинка не загрузилась;
- 14 карточек Рима, кампания, квизы, связи;
- JSON и CSV экспорт данных.

## Запуск локально

```bash
python -m http.server 8000
```

Открыть:

```text
http://localhost:8000
```

Можно также открыть `index.html`, но для GitHub Pages лучше пушить как обычный static root.

## GitHub Pages

Файлы должны лежать в корне репозитория:

```text
index.html
styles.css
app.js
.nojekyll
data/
assets/
docs/
csv/
sql/
```
