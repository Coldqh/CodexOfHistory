#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const root=path.resolve(new URL('..',import.meta.url).pathname);
const manifestPath=path.join(root,'data/content-manifest.json');
const failures=[];

function exists(rel){
  const clean=String(rel||'').replace(/^\.\//,'');
  if(!clean||/^https?:\/\//i.test(clean))return;
  if(!fs.existsSync(path.join(root,clean)))failures.push(clean);
}
function walk(value){
  if(typeof value==='string'){exists(value);return;}
  if(Array.isArray(value)){for(const item of value)walk(item);return;}
  if(value&&typeof value==='object')for(const item of Object.values(value))walk(item);
}

for(const rel of ['index.html','styles.css','manifest.webmanifest','sw.js','js/bootstrap.js','data/content-manifest.json'])exists(rel);
if(!fs.existsSync(manifestPath)){
  console.error('ERROR: отсутствует data/content-manifest.json');
  process.exit(1);
}
const manifest=JSON.parse(fs.readFileSync(manifestPath,'utf8'));
walk(manifest.scripts);
walk(manifest.datasets);

const unique=[...new Set(failures)].sort();
if(unique.length){
  console.error(`ERROR: не хватает ${unique.length} файлов проекта:`);
  for(const rel of unique)console.error(`- ${rel}`);
  console.error('\nРаспакуй patch-only архив поверх корня репозитория C:\\CodexOfHistory с заменой файлов.');
  process.exit(1);
}
console.log(`✓ Установка целая: ${manifest.scripts?.length||0} runtime-модулей и все manifest-данные найдены`);
