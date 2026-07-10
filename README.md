# Codex of History — GitHub Pages build v0.4

Статическое историческое приложение: карточки, кампания, карта, квизы и локальный прогресс.

## Запуск локально

```powershell
cd C:\CodexOfHistory
python -m http.server 8000
```

Открыть: `http://localhost:8000`

## Публикация

```powershell
git add .
git commit -m "Patch v0.4 premium UI UX"
git push
```

GitHub Pages должен использовать:

- Branch: `main`
- Folder: `/ root`

## Архитектура

- `index.html` — оболочка;
- `styles.css` — дизайн-система и responsive UI;
- `app.js` — данные и логика приложения;
- `assets/` — локальные UI-ассеты;
- `data/` — подготовленные JSON-данные;
- `docs/PATCH_NOTES_v0_4.md` — изменения патча;
- `docs/UI_AUDIT_v0_4.md` — краткий аудит интерфейса.

## Важно

Приложение полностью static. Backend, Node.js и сборщик для GitHub Pages не требуются. Прогресс хранится в `localStorage`.
