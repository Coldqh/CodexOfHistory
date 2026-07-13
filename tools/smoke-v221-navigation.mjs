#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const manifest=JSON.parse(fs.readFileSync(path.join(root,'data/content-manifest.json'),'utf8'));
assert.ok(['2.2.1','2.3.0','2.4.0'].includes(manifest.version));
assert(manifest.scripts.includes('js/features/v2-2-1-navigation-cleanup.js'));
const js=fs.readFileSync(path.join(root,'js/features/v2-2-1-navigation-cleanup.js'),'utf8');
for(const token of ["state.activeCampaign='MESOPOTAMIA_DAWN'",'Доступные кампании','Хронология','Выбери эпоху','worldDepth'])assert(js.includes(token));
for(const forbidden of ['Продолжить Рим','Открыть мир','Глобальная хронология начинается','Твой прогресс Рима'])assert(!js.includes(forbidden));
console.log('✓ v2.2.1 navigation cleanup smoke');
