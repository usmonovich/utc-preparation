// Релизная учебная база для магазинов: в неё попадают только утверждённые записи.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildReleasePack, readOverlay } from '../../tools/release-pack.ts';
import { emptyOverlay } from '../../src/domain/content-index.ts';
import type { AdminOverlay, ContentPack } from '../../src/domain/types.ts';

const read = (p: string) => fs.readFileSync(new URL(`../../${p}`, import.meta.url));
const physics: ContentPack = JSON.parse(read('content/pack.json').toString('utf8'));
const math: ContentPack = JSON.parse(read('content/math/pack.json').toString('utf8'));

test('релиз: без решений администратора в пакет не попадает ни одной записи, пункты математики остаются в плане', () => {
  const { pack, stats } = buildReleasePack(math, emptyOverlay());
  for (const k of ['theory', 'formulas', 'examples', 'questions'] as const) assert.equal(pack[k].length, 0, k);
  assert.equal(pack.topics.length, 0);
  assert.equal(pack.plan!.length, 131, 'все пункты книги видны в плане курса');
  assert.deepEqual(pack.plan!.map((p) => p.num), math.topics.map((t) => t.num), 'порядок книги сохранён');
  assert.equal(stats.dropped.questions.review, math.questions.length);
});

test('релиз: утверждённое входит, на проверке / отклонённое / устаревшее решение — нет; ссылки на неутверждённые формулы убираются', () => {
  const q = physics.questions.find((x) => x.formulaIds.length >= 1)!;
  const [q2, q3, q4] = physics.questions.filter((x) => x.id !== q.id && x.topicId !== q.topicId).slice(0, 3);
  const ov: AdminOverlay = {
    ...emptyOverlay(),
    patches: {
      [q.id]: { status: 'approved', baseHash: q.hash },
      [q2.id]: { status: 'approved', baseHash: q2.hash },
      [q3.id]: { status: 'rejected', baseHash: q3.hash },
      [q4.id]: { status: 'approved', baseHash: 'устаревший-хеш' }, // запись изменилась после проверки
    },
  };
  const { pack, stats } = buildReleasePack(physics, ov);
  assert.deepEqual(pack.questions.map((x) => x.id).sort(), [q.id, q2.id].sort());
  assert.ok(pack.questions.every((x) => x.status === 'approved'));
  assert.deepEqual(pack.questions.find((x) => x.id === q.id)!.formulaIds, [], 'формулы темы не утверждены — ссылки убраны');
  assert.equal(stats.danglingFormulaRefs, q.formulaIds.length);
  assert.deepEqual(stats.stale, [q4.id]);
  assert.deepEqual(new Set(pack.topics.map((t) => t.id)), new Set([q.topicId, q2.topicId]), 'только темы с утверждёнными записями');
  assert.equal(pack.theory.length + pack.formulas.length + pack.examples.length, 0);
});

test('релиз: оверлей читается из частей базы артефакта, из резервной копии и из файла оверлея', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'release-ov-'));
  const ov = { ...emptyOverlay(), patches: { x: { status: 'approved' } } };
  const s = JSON.stringify(ov);
  fs.mkdirSync(`${dir}/chunks`);
  fs.writeFileSync(`${dir}/chunks/c0.json`, JSON.stringify({ s: s.slice(0, 10) }));
  fs.writeFileSync(`${dir}/chunks/c1.json`, JSON.stringify({ s: s.slice(10) }));
  fs.writeFileSync(`${dir}/backup.json`, JSON.stringify({ kind: 'fpk-admin-backup', overlay: ov }));
  fs.writeFileSync(`${dir}/overlay.json`, s);
  for (const p of [`${dir}/chunks`, `${dir}/backup.json`, `${dir}/overlay.json`]) assert.deepEqual(readOverlay(p).patches, ov.patches, p);
  fs.writeFileSync(`${dir}/bad.json`, '{"a":1}');
  assert.throws(() => readOverlay(`${dir}/bad.json`), /не решения администратора/);
  fs.rmSync(`${dir}/chunks/c0.json`);
  assert.throws(() => readOverlay(`${dir}/chunks`), /пропущена часть c0/);
  fs.rmSync(dir, { recursive: true, force: true });
});

test('релиз: сохранённые релизные пакеты сделаны из текущей учебной базы и содержат только утверждённое', () => {
  for (const [subject, src, full] of [['physics', 'content/pack.json', physics], ['math', 'content/math/pack.json', math]] as const) {
    const metaUrl = new URL(`../../content/release/${subject}.meta.json`, import.meta.url);
    if (!fs.existsSync(metaUrl)) continue; // релизная база ещё не создавалась
    const meta = JSON.parse(fs.readFileSync(metaUrl, 'utf8'));
    assert.equal(meta.sourceSha256, crypto.createHash('sha256').update(read(src)).digest('hex'), `${subject}: учебная база изменилась — npm run release:pack`);
    const rel: ContentPack = JSON.parse(read(`content/release/${subject}.json`).toString('utf8'));
    for (const k of ['theory', 'formulas', 'examples', 'questions'] as const) {
      assert.ok(rel[k].every((r) => r.status === 'approved'), `${subject}.${k}: только утверждённое`);
      const ids = new Set(full[k].map((r) => r.id));
      assert.ok(rel[k].every((r) => ids.has(r.id)), `${subject}.${k}: нет посторонних записей`);
    }
    // пересборка из сохранённых решений даёт тот же пакет
    const again = buildReleasePack(full, readOverlay(fileURLToPath(new URL(`../../content/release/overlays/${subject}`, import.meta.url)))).pack;
    for (const k of ['topics', 'theory', 'formulas', 'examples', 'questions'] as const) assert.deepEqual(again[k].map((r) => r.id), rel[k].map((r) => r.id), `${subject}.${k}`);
  }
});
