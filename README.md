# Codex of History v1.2

Статическая историческая игра для GitHub Pages. Версия 1.2 добавляет ежедневное обучение и интервальные повторения поверх data-first архитектуры v1.1.

## Установка

Распакуйте содержимое архива в корень `C:\CodexOfHistory`, затем:

```powershell
git add .
git commit -m "Patch v1.2 daily learning"
git push
```

## Локальный запуск

Данные загружаются через `fetch`, поэтому нужен HTTP-сервер:

```powershell
cd C:\CodexOfHistory
python -m http.server 8000
```

Открыть `http://localhost:8000`.

## Проверка контента

```powershell
node tools/validate-content.mjs
```

Документация:

- `docs/PATCH_NOTES_v1_2.md`
- `docs/ARCHITECTURE_v1_2.md`
- `docs/QA_v1_2.md`
