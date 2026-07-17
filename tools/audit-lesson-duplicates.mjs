#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const baselinePath = path.join(root, 'data', 'quality', 'lesson-duplicate-baseline.json');
const strictCampaigns = new Set([
  'mesopotamia',
  'egypt',
  'comparison',
  'indus',
  'china',
  'civilizations',
]);
const prosePaths = new Set([
  'story[].text',
  'chronology[].note',
  'concepts[].definition',
  'activity.prompt',
  'activity.explanation',
  'activity.summary',
  'theory.lead',
  'theory.paragraphs[]',
  'theory.historicityNotes[]',
  'theory.summary',
]);
const bannedFragments = [
  'Вода, глина и тростник были местными ресурсами, тогда как камень, металл и качественную древесину приходилось получать через обмен.',
  'Поэтому ранняя история региона — это не простая история «даров рек», а история приспособления к нестабильному ландшафту.',
  'Связь проверяется по месту, датировке, жанру и задаче источника.',
];
const abbreviations = new Map([
  ['до н. э.', 'до§н§э§'],
  ['н. э.', 'н§э§'],
  ['ок.', 'ок§'],
  ['г.', 'г§'],
  ['т. е.', 'т§е§'],
]);

const readJson = async relative => JSON.parse(await fs.readFile(path.join(root, relative), 'utf8'));
const canonicalPath = value => value.replace(/\[\d+\]/g, '[]');
const normalize = value => String(value || '')
  .normalize('NFKC')
  .replace(/\u00a0/g, ' ')
  .replace(/[«»“”„]/g, '"')
  .replace(/[—–‑]/g, '-')
  .replace(/\s+/g, ' ')
  .trim()
  .toLocaleLowerCase('ru-RU');

function splitSentences(value) {
  let text = String(value || '').normalize('NFKC').replace(/\u00a0/g, ' ').replace(/\s+/g, ' ').trim();
  for (const [source, token] of abbreviations) text = text.replaceAll(source, token);
  const pieces = text.split(/(?<=[.!?])\s+(?=[А-ЯЁA-Z«"])/u);
  return pieces.map(piece => {
    let restored = piece;
    for (const [source, token] of abbreviations) restored = restored.replaceAll(token, source);
    return restored.trim();
  }).filter(piece => piece.length >= 25);
}

function collectStrings(node, currentPath, output) {
  if (typeof node === 'string') {
    if (prosePaths.has(canonicalPath(currentPath))) output.push(...splitSentences(node));
    return;
  }
  if (Array.isArray(node)) {
    node.forEach((value, index) => collectStrings(value, `${currentPath}[${index}]`, output));
    return;
  }
  if (node && typeof node === 'object') {
    for (const [key, value] of Object.entries(node)) {
      collectStrings(value, currentPath ? `${currentPath}.${key}` : key, output);
    }
  }
}

async function measure() {
  const manifest = await readJson('data/content-manifest.json');
  const lessonPaths = manifest.datasets.lessons;
  const records = [];
  for (const relative of lessonPaths) {
    const campaign = relative.split('/')[2];
    const bundle = await readJson(relative);
    for (const [missionId, mission] of Object.entries(bundle)) {
      const strings = [];
      collectStrings(mission, '', strings);
      for (const sentence of strings) {
        records.push({ campaign, missionId, sentence, normalized: normalize(sentence), file: relative });
      }
    }
  }

  const groups = new Map();
  for (const record of records) {
    if (!groups.has(record.normalized)) groups.set(record.normalized, []);
    groups.get(record.normalized).push(record);
  }
  const duplicates = [...groups.entries()].filter(([, values]) => {
    const missions = new Set(values.map(value => `${value.campaign}:${value.missionId}`));
    return missions.size >= 2;
  });
  const strictRecords = records.filter(record => strictCampaigns.has(record.campaign));
  const strictPairs = new Set(strictRecords.map(record => `${record.campaign}:${record.missionId}:${record.normalized}`));
  const duplicateKeys = new Set(duplicates.map(([key]) => key));
  const strictDuplicatePairs = new Set(
    strictRecords
      .filter(record => duplicateKeys.has(record.normalized))
      .map(record => `${record.campaign}:${record.missionId}:${record.normalized}`),
  );
  const maxStrictMissionCount = duplicates.reduce((max, [, values]) => {
    const missions = new Set(values
      .filter(value => strictCampaigns.has(value.campaign))
      .map(value => `${value.campaign}:${value.missionId}`));
    return Math.max(max, missions.size);
  }, 0);
  const bannedHits = [];
  for (const fragment of bannedFragments) {
    for (const record of records) {
      if (strictCampaigns.has(record.campaign) && record.sentence.includes(fragment)) bannedHits.push({ fragment, ...record });
    }
  }

  const top = duplicates
    .map(([, values]) => ({
      sentence: values[0].sentence,
      missions: new Set(values.map(value => `${value.campaign}:${value.missionId}`)).size,
      occurrences: values.length,
      campaigns: new Set(values.map(value => value.campaign)).size,
    }))
    .sort((a, b) => b.missions - a.missions || b.occurrences - a.occurrences)
    .slice(0, 20);

  return {
    version: manifest.version,
    lessonFiles: lessonPaths.length,
    missions: new Set(records.map(record => `${record.campaign}:${record.missionId}`)).size,
    sentences: records.length,
    duplicateSentenceTypes: duplicates.length,
    duplicateExtraOccurrences: duplicates.reduce((sum, [, values]) => sum + values.length - 1, 0),
    strictMissionSentencePairs: strictPairs.size,
    strictDuplicatePairs: strictDuplicatePairs.size,
    strictDuplicateRatePercent: Number((strictDuplicatePairs.size / Math.max(1, strictPairs.size) * 100).toFixed(3)),
    maxStrictMissionCount,
    bannedHits,
    top,
  };
}

const metrics = await measure();
if (process.argv.includes('--write-baseline')) {
  await fs.mkdir(path.dirname(baselinePath), { recursive: true });
  const baseline = {
    version: metrics.version,
    generatedAt: new Date().toISOString(),
    duplicateSentenceTypes: metrics.duplicateSentenceTypes,
    duplicateExtraOccurrences: metrics.duplicateExtraOccurrences,
    strictDuplicateRatePercentMax: 2,
    maxStrictMissionCountMax: 2,
  };
  await fs.writeFile(baselinePath, `${JSON.stringify(baseline, null, 2)}\n`, 'utf8');
  console.log(`Duplicate baseline written: ${path.relative(root, baselinePath)}`);
  console.log(JSON.stringify(metrics, null, 2));
  process.exit(0);
}

const baseline = await readJson('data/quality/lesson-duplicate-baseline.json');
const errors = [];
if (metrics.duplicateSentenceTypes > baseline.duplicateSentenceTypes) {
  errors.push(`Глобальное число типов дублей выросло: ${metrics.duplicateSentenceTypes} > ${baseline.duplicateSentenceTypes}`);
}
if (metrics.duplicateExtraOccurrences > baseline.duplicateExtraOccurrences) {
  errors.push(`Глобальное число лишних повторов выросло: ${metrics.duplicateExtraOccurrences} > ${baseline.duplicateExtraOccurrences}`);
}
if (metrics.strictDuplicateRatePercent > baseline.strictDuplicateRatePercentMax) {
  errors.push(`В очищенных кампаниях доля дублей ${metrics.strictDuplicateRatePercent}% > ${baseline.strictDuplicateRatePercentMax}%`);
}
if (metrics.maxStrictMissionCount > baseline.maxStrictMissionCountMax) {
  errors.push(`Одна строка повторяется в ${metrics.maxStrictMissionCount} очищенных миссиях; максимум ${baseline.maxStrictMissionCountMax}`);
}
if (metrics.bannedHits.length) {
  errors.push(`Найдены запрещённые массовые фразы: ${metrics.bannedHits.length}`);
}

console.log(`Lesson Duplicate Audit v${metrics.version}`);
console.log(`Уроки: ${metrics.lessonFiles}; миссии: ${metrics.missions}; предложения: ${metrics.sentences}`);
console.log(`Глобальные дубли: ${metrics.duplicateSentenceTypes} типов / ${metrics.duplicateExtraOccurrences} лишних вхождений`);
console.log(`Очищенная Эпоха I: ${metrics.strictDuplicateRatePercent}% повторяющихся mission–sentence пар; максимум ${metrics.maxStrictMissionCount} миссии на строку`);
if (errors.length) {
  for (const error of errors) console.error(`ERROR ${error}`);
  console.error('Самые массовые повторы:');
  for (const item of metrics.top.slice(0, 10)) console.error(`${item.missions} миссий — ${item.sentence}`);
  process.exit(1);
}
console.log('✓ Дубликаты не превышают зафиксированный бюджет; очищенные кампании проходят строгий порог');
