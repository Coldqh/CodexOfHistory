# Codex of History v1.1

Статическая историческая игра для GitHub Pages. Версия 1.1 переводит проект на data-first архитектуру.

## Установка

Распакуйте содержимое архива в корень `C:\CodexOfHistory`, затем:

```powershell
git add .
git commit -m "Patch v1.1 content engine refactor"
git push
```

## Локальный запуск

Из-за загрузки JSON через `fetch` нужен HTTP-сервер:

```powershell
cd C:\CodexOfHistory
python -m http.server 8000
```

Открыть `http://localhost:8000`.

## Проверка контента

```powershell
node tools/validate-content.mjs
```

Подробности: `docs/ARCHITECTURE_v1_1.md`.
