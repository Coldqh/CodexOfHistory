# Codex of History — Settings & Update Architecture v1.3

## Хранение

- Игровой прогресс: `codex_history_v02_ru`.
- Настройки интерфейса: `codex_history_preferences_v13`.
- Принудительный cache-busting token: `sessionStorage.codex_force_refresh`.

Сброс прогресса не удаляет тему, плотность, размер текста и режим анимаций.

## Настройки интерфейса

Параметры применяются через атрибуты `<html>`:

- `data-density="compact|comfortable"`;
- `data-text-size="small|normal|large"`;
- `data-motion="full|reduced"`;
- `data-theme="night|parchment"`.

Это позволяет расширять настройки без изменения разметки экранов.

## Обновление

1. Удаляется Cache Storage.
2. Отменяются старые регистрации Service Worker, если они появятся в будущих версиях.
3. В `sessionStorage` создаётся уникальный refresh token.
4. Страница открывается с query-параметром `refresh`.
5. Bootstrap загружает manifest, JSON и JavaScript с `cache: no-store`, номером версии и refresh token.

Игровой `localStorage` не очищается.

## Версионирование

Единый номер версии хранится в `data/content-manifest.json` и используется:

- в интерфейсе;
- в загрузчике;
- в документации;
- в автоматических тестах;
- для cache-busting ресурсов.
