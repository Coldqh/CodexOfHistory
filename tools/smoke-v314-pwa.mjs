#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';

const root=path.resolve(new URL('..',import.meta.url).pathname);
const readText=p=>fs.readFileSync(path.join(root,p),'utf8');
const readJson=p=>JSON.parse(readText(p));
const manifest=readJson('data/content-manifest.json');
const webmanifest=readJson('manifest.webmanifest');
const sw=readText('sw.js');
const start=readText('js/core/start.js');
const visuals=readText('js/features/v3-1-3-visual-semantics.js');
const index=readText('index.html');
const styles=readText('styles.css');

assert.equal(manifest.version,'6.9.0');
assert.match(sw,/IMAGE_LIMIT=48/);
assert.match(sw,/TILE_LIMIT=72/);
assert.match(sw,/trim\(cacheName,limit\)/);
assert.match(sw,/API payloads are deliberately not stored/);
assert.doesNotMatch(sw,/cacheFirstExternal/);
assert.doesNotMatch(start,/CARDS\.map\(c=>cardImageSource/);
assert.match(start,/slice\(0,8\)/);
assert.match(start,/standalone/);
assert.match(visuals,/AUTO_BATCH_LIMIT=IS_STANDALONE\?4:10/);
assert.match(visuals,/MANUAL_BATCH_LIMIT=IS_STANDALONE\?12:36/);
assert.match(visuals,/MAX_STORED_RECORDS=IS_STANDALONE\?72:180/);
assert.match(visuals,/IntersectionObserver/);
assert.doesNotMatch(visuals,/setTimeout\(\(\)=>resolveHistoricalImages\(\),700\)/);
assert.match(visuals,/codex_history_visual_archive_v313/);
assert.match(visuals,/codex_history_visual_archive_session_v322/);
assert.match(visuals,/sessionStorage/);
assert.match(index,/apple-touch-icon/);
assert.match(index,/codex_pwa_runtime_build/);
assert.match(index,/pwa-standalone/);
assert.match(styles,/iOS\/standalone safety mode/);
assert.equal(webmanifest.icons.filter(x=>x.type==='image/png').length,3);
for(const size of [180,192,512])assert.ok(fs.existsSync(path.join(root,`assets/ui/codex-icon-${size}.png`)),`missing ${size}px icon`);

console.log('✓ v6.9.0 mobile PWA uses lazy visuals, session cache and PNG icons');
