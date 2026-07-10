# Codex of History v1.3

Статическая историческая игра для GitHub Pages. Версия 1.3 делает мобильный интерфейс значительно компактнее и добавляет системный экран настроек, принудительное обновление и отображение версии.

## Установка

Распакуйте содержимое архива в корень `C:\CodexOfHistory`, затем:

```powershell
git add .
git commit -m "Patch v1.3 compact mobile and settings"
git push
```

## Локальный запуск

```powershell
cd C:\CodexOfHistory
python -m http.server 8000
```

Открыть `http://localhost:8000`.

## Проверки

```powershell
npm test
```

Или отдельно:

```powershell
node tools/validate-content.mjs
node tools/smoke-daily.mjs
node tools/smoke-settings.mjs
```

Документация:

- `docs/PATCH_NOTES_v1_3.md`
- `docs/QA_v1_3.md`
