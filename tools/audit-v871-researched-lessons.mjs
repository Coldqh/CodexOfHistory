import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = p => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));
const files = [
  'data/lessons/mesopotamia/chapter_01_05.json',
  'data/lessons/mesopotamia/chapter_06_10.json',
  'data/lessons/egypt/chapter_01_05.json',
  'data/lessons/egypt/chapter_06_10.json',
];
const lessons = Object.assign({}, ...files.map(read));
assert.equal(Object.keys(lessons).length, 60, 'expected 60 consolidated lessons');

const banned = [
  /В теме «/i,
  /данн(?:ый|ом) урок/i,
  /задача урока/i,
  /историческая оговорка/i,
  /понятие «.+» означает следующее/i,
  /факты, последовательность, понятия и границы реконструкции/i,
  /Связать факты с местом и временем/i,
  /Проверить вывод по источникам/i,
  /Разбор темы «/i,
  /Разобрать тему «/i,
  /Проследить изменения от/i,
];
const sentenceSeen = new Map();
const objectiveSeen = new Map();

for (const [id, lesson] of Object.entries(lessons)) {
  assert.equal((lesson.objectives || []).length, 3, `${id}: expected three concrete objectives`);
  for (const objective of lesson.objectives || []) {
    assert(objective.length >= 20, `${id}: objective is too vague`);
    const key = objective.toLowerCase().replace(/\s+/g, ' ').trim();
    const ids = objectiveSeen.get(key) || [];
    ids.push(id);
    objectiveSeen.set(key, ids);
  }

  assert((lesson.sources || []).length >= 1, `${id}: missing source`);
  for (const source of lesson.sources || []) {
    assert(/^https:\/\//.test(source.url || ''), `${id}: invalid source URL`);
    assert((source.title || '').length >= 8, `${id}: source title is too short`);
  }

  const prose = [
    ...(lesson.objectives || []),
    ...(lesson.story || []).map(x => x.text),
    ...(lesson.chronology || []).map(x => x.note),
    ...(lesson.concepts || []).map(x => x.definition),
    ...(lesson.causeEffect?.causes || []),
    ...(lesson.causeEffect?.consequences || []),
    lesson.activity?.prompt,
    lesson.activity?.explanation,
    lesson.activity?.summary,
    lesson.theory?.lead,
    ...(lesson.theory?.paragraphs || []),
    ...(lesson.theory?.historicityNotes || []),
    lesson.theory?.summary,
  ].filter(Boolean);

  const joined = prose.join(' ');
  for (const rule of banned) assert(!rule.test(joined), `${id}: banned generator phrase ${rule}`);

  assert((lesson.theory?.paragraphs || []).length >= 3, `${id}: too few theory paragraphs`);
  const words = (lesson.theory?.paragraphs || []).join(' ').trim().split(/\s+/).length;
  assert(words >= 90, `${id}: theory is too thin (${words})`);
  assert(words <= 520, `${id}: theory is padded (${words})`);
  assert.notEqual(lesson.theory?.lead, lesson.theory?.summary, `${id}: lead and summary repeat verbatim`);

  for (const sentence of joined.split(/(?<=[.!?])\s+/).map(s => s.trim()).filter(s => s.length >= 45)) {
    const key = sentence.toLowerCase()
      .replace(/[«»“”„]/g, '"')
      .replace(/[—–‑]/g, '-')
      .replace(/\s+/g, ' ');
    const ids = sentenceSeen.get(key) || [];
    ids.push(id);
    sentenceSeen.set(key, ids);
  }
}

const duplicateObjectives = [...objectiveSeen.entries()].filter(([, ids]) => new Set(ids).size > 1);
assert.equal(duplicateObjectives.length, 0, `repeated objectives: ${duplicateObjectives.slice(0, 5).map(([s, ids]) => `${ids.join(',')}: ${s}`).join('\n')}`);

const duplicatedSentences = [...sentenceSeen.entries()].filter(([, ids]) => new Set(ids).size > 2);
assert.equal(duplicatedSentences.length, 0, `repeated researched sentences: ${duplicatedSentences.slice(0, 5).map(([s, ids]) => `${ids.join(',')}: ${s}`).join('\n')}`);

console.log(`✓ v8.7.1 researched lesson audit: ${Object.keys(lessons).length} consolidated missions, concrete objectives, sourced theory and no 3+ mission sentence clones`);
