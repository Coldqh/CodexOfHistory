#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';

const root=path.resolve(new URL('..',import.meta.url).pathname);
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const manifest=JSON.parse(read('data/content-manifest.json'));
const webmanifest=JSON.parse(read('manifest.webmanifest'));
const index=read('index.html');
const styles=read('styles.css');
const sw=read('sw.js');
const scripts=['js/views/base.js','js/features/mobile-cleanup.js','js/features/v1-5-polish.js','js/features/v2-6-onboarding.js','js/bootstrap.js'].map(read).join('\n');

assert.equal(manifest.version,'6.9.0');
for(const file of ['assets/ui/codex-logo-mark.svg','assets/ui/codex-app-icon.svg','assets/ui/codex-logo-mark.png','assets/ui/codex-icon-180.png','assets/ui/codex-icon-192.png','assets/ui/codex-icon-512.png','assets/ui/codex-icon-maskable-512.png','assets/ui/codex-favicon-32.png','assets/ui/codex-favicon-16.png']){
  const stat=fs.statSync(path.join(root,file));
  assert.ok(stat.size>500,`${file}: file too small`);
}
assert.match(index,/codex-app-icon\.svg/);
assert.match(index,/codex-favicon-32\.png/);
assert.match(index,/apple-touch-icon[^>]+codex-icon-180\.png/);
assert.match(scripts,/codex-logo-mark\.png/);
assert.doesNotMatch(scripts,/<div class="seal">C<\/div>/);
assert.match(styles,/\.brand-logo\{/);
assert.match(styles,/onboarding-codex-mark>img/);
assert.match(sw,/codex-logo-mark\.png/);
assert.match(sw,/codex-app-icon\.svg/);
assert.match(sw,/codex-favicon-32\.png/);
assert.ok(webmanifest.icons.some(x=>x.src==='assets/ui/codex-icon-maskable-512.png'&&x.purpose==='maskable'));
const appIcon=read('assets/ui/codex-app-icon.svg');
const uiMark=read('assets/ui/codex-logo-mark.svg');
assert.match(appIcon,/<rect width="1024" height="1024"/);
assert.doesNotMatch(appIcon,/rx="[0-9]+"/);
assert.doesNotMatch(uiMark,/<rect/);
console.log('✓ v6.9.0 uses a full-bleed PWA icon and a transparent UI mark');
