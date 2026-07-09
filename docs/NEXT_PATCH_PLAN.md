# Next Patch Plan — v0.2

## Цель

Перевести MVP из статичного прототипа в нормальную структуру проекта.

## Патч v0.2

### 1. Data-first app
- вынести данные из `app.js`;
- грузить `cards.json`, `relations.json`, `campaigns.json`, `quizzes.json`;
- сделать простой DataService.

### 2. Timeline screen
- добавить экран таймлайна;
- группировка по векам;
- фильтр по типам карточек.

### 3. 50 card skeletons
Добавить скелеты:
- ранний Рим;
- Республика;
- Пунические войны;
- кризис Республики;
- Цезарь;
- Август;
- ранняя Империя.

### 4. Better campaign unlocks
- узлы открываются по completed quiz;
- награды открывают конкретные карточки;
- завершение кампании даёт pack.

### 5. Review mode
- карточки возвращаются через 1/3/7 дней;
- simple spaced repetition.

### 6. Visual style
- rarity frames;
- card backs;
- portrait slots;
- battle/map slots.

### 7. Supabase start
- поднять БД;
- загрузить schema;
- импортировать первые карточки.
