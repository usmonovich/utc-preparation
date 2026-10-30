import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { parseNumber, checkResponse, isComplete } from '../../src/domain/answer-check.ts';
import { applyEvent, emptyAnswer } from '../../src/domain/hint-flow.ts';
import { ContentIndex, emptyOverlay } from '../../src/domain/content-index.ts';
import { selectQuestions, defaultConfig, createAttempt, attemptScore, availableQuestions } from '../../src/domain/test-engine.ts';
import { recordFinal, emptyUserState, overview, dailySeries, ERROR_CLEAR_STREAK } from '../../src/domain/progress.ts';
import { normalizeLatex, splitMath } from '../../src/domain/latex.ts';
import { search } from '../../src/domain/search.ts';
import { pageLabel, labelPageRefs } from '../../src/domain/page-label.ts';
import type { ContentPack, Question } from '../../src/domain/types.ts';

const pack: ContentPack = JSON.parse(fs.readFileSync(new URL('../../content/pack.json', import.meta.url), 'utf8'));

/** Индекс, в котором все вопросы утверждены (как после проверки администратором). */
function approvedIndex() {
  const ov = emptyOverlay();
  for (const q of pack.questions) ov.patches[q.id] = { status: 'approved' };
  return new ContentIndex(pack, ov);
}
const at = '2026-10-16T10:00:00.000Z';

test('parseNumber понимает разные формы записи', () => {
  assert.equal(parseNumber('4,36'), 4.36);
  assert.equal(parseNumber(' 86 400 '), 86400);
  assert.equal(parseNumber('−50'), -50);
  assert.equal(parseNumber('1e-6'), 1e-6);
  assert.equal(parseNumber('1·10^-6'), 1e-6);
  assert.equal(parseNumber('7,2*10^(6)'), 7.2e6);
  assert.equal(parseNumber('3×10⁵'), 3e5);
  assert.equal(parseNumber('10^5'), 1e5);
  assert.ok(Number.isNaN(parseNumber('abc')));
  assert.ok(Number.isNaN(parseNumber('')));
  assert.ok(Number.isNaN(parseNumber('4..3')));
});

const q = (id: string) => pack.questions.find((x) => x.id === id)! as Question;

test('проверка ответа по типам вопросов', () => {
  const single = pack.questions.find((x) => x.type === 'single')!;
  assert.equal(checkResponse(single, { type: 'single', key: single.answer as string }), true);
  assert.equal(checkResponse(single, { type: 'single', key: 'zz' }), false);

  const multi = pack.questions.find((x) => x.type === 'multiple')!;
  const keys = multi.answer as string[];
  assert.equal(checkResponse(multi, { type: 'multiple', keys: [...keys].reverse() }), true);
  assert.equal(checkResponse(multi, { type: 'multiple', keys: keys.slice(1) }), false);
  assert.equal(checkResponse(multi, { type: 'multiple', keys: [...keys, 'e'] }), false);

  const num = q('kin-motion-types-q2'); // 48 км/ч
  assert.equal(checkResponse(num, { type: 'numeric', raw: '48' }), true);
  assert.equal(checkResponse(num, { type: 'numeric', raw: '48,5' }), true); // в пределах допуска 2 %
  assert.equal(checkResponse(num, { type: 'numeric', raw: '50' }), false); // среднее арифметическое — типичная ошибка
  const zero = q('cons-momentum-q4'); // ответ 0
  assert.equal(checkResponse(zero, { type: 'numeric', raw: '0' }), true);
  assert.equal(checkResponse(zero, { type: 'numeric', raw: '0,5' }), false);

  const match = pack.questions.find((x) => x.type === 'matching')!;
  const good: Record<string, string> = {};
  match.pairs!.forEach((_, i) => (good[String(i)] = String(i)));
  assert.equal(checkResponse(match, { type: 'matching', map: good }), true);
  assert.equal(checkResponse(match, { type: 'matching', map: { ...good, '0': '1', '1': '0' } }), false);

  const seq = pack.questions.find((x) => x.type === 'sequence')!;
  assert.equal(checkResponse(seq, { type: 'sequence', order: seq.sequence!.map((_, i) => String(i)) }), true);
  assert.equal(checkResponse(seq, { type: 'sequence', order: seq.sequence!.map((_, i) => String(i)).reverse() }), false);

  const text = pack.questions.find((x) => x.type === 'text')!;
  assert.equal(checkResponse(text, { type: 'text', text: 'любая формулировка' }), null, 'текст не объявляется неверным автоматически');
  assert.equal(checkResponse(text, { type: 'text', text: 'x', selfAssessed: true }), true);
  assert.equal(isComplete(text, { type: 'text', text: '   ' }), false);
});

test('подсказка после первой ошибки, разбор после второй', () => {
  const r = { type: 'single' as const, key: 'b' };
  let a = applyEvent(emptyAnswer(), { type: 'submit', response: r, correct: false, hintsEnabled: true, at });
  assert.equal(a.status, 'hint');
  assert.equal(a.hintShown, true);
  assert.equal(a.correct, null, 'после первой ошибки ответ ещё не закрыт');
  a = applyEvent(a, { type: 'submit', response: r, correct: false, hintsEnabled: true, at });
  assert.equal(a.status, 'wrong');
  assert.equal(a.correct, false);
  assert.equal(a.tries, 2);
  // после финала события игнорируются
  assert.equal(applyEvent(a, { type: 'submit', response: r, correct: true, hintsEnabled: true, at }).status, 'wrong');
});

test('верно со второй попытки после подсказки', () => {
  let a = applyEvent(emptyAnswer(), { type: 'submit', response: { type: 'numeric', raw: '1' }, correct: false, hintsEnabled: true, at });
  a = applyEvent(a, { type: 'submit', response: { type: 'numeric', raw: '2' }, correct: true, hintsEnabled: true, at });
  assert.equal(a.status, 'correct');
  assert.equal(a.responses.length, 2);
});

test('экзамен без подсказок: одна попытка', () => {
  const a = applyEvent(emptyAnswer(), { type: 'submit', response: { type: 'single', key: 'x' }, correct: false, hintsEnabled: false, at });
  assert.equal(a.status, 'wrong');
  assert.equal(a.hintShown, false);
});

test('«Показать решение» сразу открывает разбор', () => {
  const a = applyEvent(emptyAnswer(), { type: 'reveal', at });
  assert.equal(a.status, 'revealed');
  assert.equal(a.solutionShown, true);
  assert.equal(a.correct, false);
});

test('текстовый ответ: сверка с эталоном и самооценка', () => {
  let a = applyEvent(emptyAnswer(), { type: 'submit', response: { type: 'text', text: 'мой ответ' }, correct: null, hintsEnabled: true, at });
  assert.equal(a.status, 'selfcheck');
  a = applyEvent(a, { type: 'selfAssess', correct: true, at });
  assert.equal(a.status, 'correct');
  assert.deepEqual(a.responses[0], { type: 'text', text: 'мой ответ', selfAssessed: true });
});

test('режим A «По порядку» сохраняет порядок источника', () => {
  const idx = approvedIndex();
  const topicIds = idx.allVisibleTopics().map((t) => t.id);
  const cfg = { ...defaultConfig(topicIds), count: 0 };
  const sel = selectQuestions(idx, cfg, 1);
  const keys = sel.ids.map((id) => idx.orderKey(idx.entity(id) as Question));
  for (let i = 1; i < keys.length; i++) assert.ok(ContentIndex.compareKeys(keys[i - 1], keys[i]) <= 0, `нарушен порядок на позиции ${i}`);
  assert.equal(sel.ids.length, pack.questions.length);
  // первый вопрос курса — первый вопрос первой темы кинематики
  assert.equal(sel.ids[0], 'kin-basics-q1');
  // внутри темы порядок совпадает с порядком в источнике, а не с порядком ID
  const inTopic = sel.ids.filter((id) => id.startsWith('kin-throw-up-'));
  assert.deepEqual(inTopic, idx.questionsOf('kin-throw-up', false).map((x) => x.id));
});

test('режим A со случайной выборкой: показ всё равно по порядку', () => {
  const idx = approvedIndex();
  const cfg = { ...defaultConfig(idx.allVisibleTopics().map((t) => t.id)), count: 15, pick: 'random' as const };
  const sel = selectQuestions(idx, cfg, 77);
  assert.equal(sel.ids.length, 15);
  const keys = sel.ids.map((id) => idx.orderKey(idx.entity(id) as Question));
  for (let i = 1; i < keys.length; i++) assert.ok(ContentIndex.compareKeys(keys[i - 1], keys[i]) < 0);
});

test('режим B «Случайный»: перемешивание на уровне попытки, без повторов', () => {
  const idx = approvedIndex();
  const topicIds = idx.topicsOf('kin').map((t) => t.id);
  const cfg = { ...defaultConfig(topicIds), count: 30, order: 'random' as const };
  const a = selectQuestions(idx, cfg, 1).ids;
  const b = selectQuestions(idx, cfg, 2).ids;
  const a2 = selectQuestions(idx, cfg, 1).ids;
  assert.deepEqual(a, a2, 'тот же seed — тот же порядок (восстановление после перезапуска)');
  assert.notDeepEqual(a, b, 'новая попытка — новый порядок');
  assert.equal(new Set(a).size, a.length, 'нет повторов в пределах попытки');
  for (const id of a) assert.ok(topicIds.includes((idx.entity(id) as Question).topicId), 'вопрос из выбранной области');
});

test('количество вопросов: предупреждение, если доступно меньше', () => {
  const idx = approvedIndex();
  const cfg = { ...defaultConfig(['kin-basics']), count: 50 };
  const sel = selectQuestions(idx, cfg, 1);
  assert.equal(sel.ids.length, sel.available);
  assert.ok(sel.notice && sel.notice.includes('доступно'));
});

test('непроверенные вопросы не попадают в тест без предпросмотра', () => {
  const idx = new ContentIndex(pack); // всё в статусе review
  const cfg = defaultConfig(idx.allVisibleTopics().map((t) => t.id));
  assert.equal(availableQuestions(idx, cfg).length, 0);
  assert.equal(availableQuestions(idx, { ...cfg, includeReview: true }).length, pack.questions.length);
  const ov = emptyOverlay();
  ov.patches['kin-basics-q1'] = { status: 'approved' };
  ov.patches['kin-basics-q2'] = { status: 'rejected' };
  const idx2 = new ContentIndex(pack, ov);
  assert.deepEqual(availableQuestions(idx2, cfg).map((x) => x.id), ['kin-basics-q1']);
  assert.ok(!availableQuestions(idx2, { ...cfg, includeReview: true }).some((x) => x.id === 'kin-basics-q2'), 'отклонённые не показываются никогда');
});

test('фильтр по типам и категориям', () => {
  const idx = approvedIndex();
  const cfg = { ...defaultConfig(idx.allVisibleTopics().map((t) => t.id)), count: 0, types: ['numeric' as const], categories: ['problem' as const] };
  const list = availableQuestions(idx, cfg);
  assert.ok(list.length > 50);
  assert.ok(list.every((x) => x.type === 'numeric' && x.category === 'problem'));
});

test('попытка с лимитом времени и подсчёт результата', () => {
  const idx = approvedIndex();
  const now = new Date(at);
  const att = createAttempt(idx, { ...defaultConfig(['kin-accel']), count: 3, timeLimitSec: 600 }, { mode: 'exam', title: 't', seed: 5, now });
  assert.equal(att.questionIds.length, 3);
  assert.equal(att.deadlineAt, new Date(now.getTime() + 600000).toISOString());
  const [q1, q2, q3] = att.questionIds;
  att.answers[q1] = { ...emptyAnswer(), status: 'correct', tries: 1, correct: true };
  att.answers[q2] = { ...emptyAnswer(), status: 'correct', tries: 2, correct: true, hintShown: true };
  att.answers[q3] = { ...emptyAnswer(), status: 'revealed', correct: false };
  const s = attemptScore(att);
  assert.deepEqual([s.correct, s.firstTry, s.afterHint, s.revealed, s.percent], [2, 1, 1, 1, 67]);
});

test('очередь ошибок: вопрос уходит после двух верных ответов подряд', () => {
  let st = emptyUserState(new Date(at));
  st = recordFinal(st, 'q', false, new Date(at));
  assert.equal(st.errorQueue.q.wrongCount, 1);
  st = recordFinal(st, 'q', true, new Date(at));
  assert.ok(st.errorQueue.q, 'одного верного ответа мало');
  for (let i = 1; i < ERROR_CLEAR_STREAK; i++) st = recordFinal(st, 'q', true, new Date(at));
  assert.equal(st.errorQueue.q, undefined);
  assert.deepEqual([st.questionStats.q.seen, st.questionStats.q.correct, st.questionStats.q.wrong], [1 + ERROR_CLEAR_STREAK, ERROR_CLEAR_STREAK, 1]);
});

test('сводка прогресса и динамика по дням', () => {
  const idx = approvedIndex();
  let st = emptyUserState(new Date(at));
  st.topicProgress['kin-basics'] = { studiedAt: at };
  const att = createAttempt(idx, { ...defaultConfig(['kin-basics']), count: 2 }, { mode: 'test', title: 't', seed: 1, now: new Date(at) });
  att.answers[att.questionIds[0]] = { ...emptyAnswer(), status: 'correct', tries: 1, correct: true, answeredAt: at };
  att.answers[att.questionIds[1]] = { ...emptyAnswer(), status: 'wrong', tries: 2, correct: false, answeredAt: at };
  att.finishedAt = at;
  st.attempts.push(att);
  st = recordFinal(st, att.questionIds[0], true, new Date(at));
  st = recordFinal(st, att.questionIds[1], false, new Date(at));
  const o = overview(st, idx);
  assert.equal(o.topicsTotal, 164);
  assert.equal(o.topicsStudied, 1);
  assert.equal(o.testsCompleted, 1);
  assert.equal(o.answersCorrect, 1);
  assert.equal(o.answersWrong, 1);
  assert.equal(o.percentCorrect, 50);
  assert.equal(o.mistakes, 1);
  const series = dailySeries(st, 7, new Date(at));
  assert.equal(series.length, 7);
  assert.deepEqual(series[6], { date: '2026-10-16', total: 2, correct: 1, percent: 50 });
});

test('кириллица в формулах оборачивается в \\text', () => {
  assert.equal(normalizeLatex('\\upsilon_{ср}'), '\\upsilon_{{\\text{ср}}}');
  assert.equal(normalizeLatex('V_{в.ж}'), 'V_{{\\text{в.ж}}}');
  assert.equal(normalizeLatex('\\text{мм рт. ст.} + x'), '\\text{мм рт. ст.} + x', 'существующий \\text не трогаем');
  assert.deepEqual(splitMath('a $x$ b \\(y\\) $$z$$').map((s) => s.kind), ['text', 'math', 'text', 'math', 'text', 'math']);
});

test('поиск находит тему, формулу и теорию', () => {
  const idx = new ContentIndex(pack);
  const hits = search(idx, 'архимед', { showReview: true, includeReviewQuestions: false });
  assert.ok(hits.some((h) => h.kind === 'topic' && h.id === 'fl-archimedes'));
  assert.ok(hits.some((h) => h.kind === 'formula'));
  assert.ok(!hits.some((h) => h.kind === 'question'), 'непроверенные вопросы не ищутся');
  assert.ok(search(idx, 'первая космическая', { showReview: true, includeReviewQuestions: false }).length > 0);
});

test('подписи страниц: механика без префикса, остальные файлы — с коротким префиксом', () => {
  assert.equal(pageLabel('p05L'), '5L');
  assert.equal(pageLabel('p10R'), '10R');
  assert.equal(pageLabel('p01'), '1');
  assert.equal(pageLabel('m07'), 'м7');
  assert.equal(pageLabel('m21'), 'м21');
  assert.equal(pageLabel('h01'), 'вл1');
  assert.equal(pageLabel('c05'), 'эл5');
  assert.equal(pageLabel('c40'), 'эл40');
  assert.equal(pageLabel('e05'), 'мг5');
  assert.equal(pageLabel('o12'), 'оп12');
  assert.equal(pageLabel('a05'), 'ат5');
  assert.equal(pageLabel('d01'), 'дф1');
  assert.equal(pageLabel('d02'), 'дф2');
  assert.equal(pageLabel('нечто'), 'нечто');
  // ссылки в текстах подсказок и пояснений показываются теми же подписями
  assert.equal(labelPageRefs('Формула со стр. c03 и замечание EL01'), 'Формула со стр. эл3 и замечание EL01');
  assert.equal(labelPageRefs('Случаи со стр. e10–e11, m07 и o12; стр. 17L'), 'Случаи со стр. мг10–мг11, м7 и оп12; стр. 17L');
  assert.equal(labelPageRefs('1e10 и E05 не трогаем'), '1e10 и E05 не трогаем');
  assert.equal(labelPageRefs('вверху стр. p11L, см. p27R'), 'вверху стр. 11L, см. 27R');
  assert.equal(labelPageRefs('заголовок на стр. a07'), 'заголовок на стр. ат7');
  assert.equal(labelPageRefs('рисунок на стр. d02 и замечание DF02'), 'рисунок на стр. дф2 и замечание DF02');
});

test('режим A «По порядку»: разделы идут в порядке курса — электродинамика, оптика, квантовая физика', () => {
  const idx = approvedIndex();
  const sel = selectQuestions(idx, { ...defaultConfig(pack.topics.map((t) => t.id)), order: 'source', pick: 'first', count: 0 }, 1);
  assert.equal(sel.ids.length, pack.questions.length);
  const ordered = sel.ids.map((id) => idx.entity(id) as Question);
  const sectionOf = (q: Question) => idx.path(q.topicId).section!.id;
  const firstPos = (sec: string) => ordered.findIndex((q) => sectionOf(q) === sec);
  const lastPos = (sec: string) => ordered.map(sectionOf).lastIndexOf(sec);
  assert.ok(lastPos('thermo') < firstPos('electro'));
  assert.ok(lastPos('electro') < firstPos('optics'));
  assert.ok(lastPos('optics') < firstPos('quantum'));
});
