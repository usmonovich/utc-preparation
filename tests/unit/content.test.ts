// Проверки целостности учебной базы (дополняют валидатор tools/build-content.ts).

import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import katex from 'katex';
import type { ContentPack } from '../../src/domain/types.ts';

const pack: ContentPack = JSON.parse(fs.readFileSync(new URL('../../content/pack.json', import.meta.url), 'utf8'));
const pageRefs = new Set(pack.pages.map((p) => p.ref));

test('страницы: механика 81, молекулярная 21, влажность 1, электричество 40 (лист 41 — дубль), магнетизм 28 (лист 29 — дубль), оптика 20, фото «Дифракция» 2, атом и ядро 8; у каждой есть изображение', () => {
  assert.equal(pack.pages.length, 201);
  const count = (file: string) => pack.pages.filter((p) => p.file === file).length;
  assert.equal(count('konspekt-mech-2024'), 81);
  assert.equal(count('konspekt-mol-2024'), 21);
  assert.equal(count('photo-humidity'), 1);
  assert.equal(count('konspekt-elec-2025'), 40);
  assert.equal(count('konspekt-el-2025'), 28);
  assert.equal(count('konspekt-opt-2025'), 20);
  assert.equal(count('photo-diffraction'), 2);
  assert.equal(count('konspekt-atom-2025'), 8);
  assert.equal(pack.pages[0].ref, 'p01');
  assert.equal(pack.pages[80].ref, 'p41R');
  assert.equal(pack.pages[101].ref, 'm21');
  assert.equal(pack.pages[102].ref, 'h01');
  // электричество стоит перед магнетизмом, магнетизм — перед оптикой
  assert.equal(pack.pages[103].ref, 'c01');
  assert.equal(pack.pages[142].ref, 'c40');
  assert.equal(pack.pages[143].ref, 'e01');
  assert.equal(pack.pages[170].ref, 'e28');
  assert.equal(pack.pages[171].ref, 'o01');
  assert.equal(pack.pages[190].ref, 'o20');
  assert.equal(pack.pages[191].ref, 'd01');
  assert.equal(pack.pages[192].ref, 'd02');
  assert.equal(pack.pages[193].ref, 'a01');
  assert.equal(pack.pages[200].ref, 'a08');
  assert.ok(!pack.pages.some((p) => p.ref === 'c41'), 'лист 41 — та же фотография, что e01, повторно не импортируется');
  assert.ok(!pack.pages.some((p) => p.ref === 'e29'), 'лист 29 — та же фотография, что o01, повторно не импортируется');
  // фото страниц есть только в рабочей копии владельца; в публичном репозитории — только список pages.txt
  const photos = fs.readdirSync(new URL('../../content/pages/', import.meta.url)).filter((f) => f.endsWith('.webp'));
  const listed = fs.readFileSync(new URL('../../content/pages/pages.txt', import.meta.url), 'utf8').split(/\r?\n/).filter(Boolean);
  assert.deepEqual(pack.pages.map((p) => p.image.replace('pages/', '')).sort(), [...listed].sort(), 'pages.txt совпадает со списком страниц');
  if (photos.length) for (const p of pack.pages) assert.ok(fs.existsSync(new URL(`../../content/${p.image}`, import.meta.url)), p.image);
});

test('у каждой записи есть ссылка на существующую страницу источника', () => {
  for (const coll of [pack.theory, pack.formulas, pack.examples, pack.questions])
    for (const e of coll) {
      assert.ok(e.sources.length > 0, e.id);
      for (const s of e.sources) assert.ok(pageRefs.has(s.page), `${e.id} → ${s.page}`);
    }
});

const decisionsUrl = new URL('../../content/review/decisions.json', import.meta.url);
const decisions: Record<string, { status: string; hash: string }> = fs.existsSync(decisionsUrl)
  ? JSON.parse(fs.readFileSync(decisionsUrl, 'utf8')).decisions ?? {}
  : {};

test('у каждого вопроса есть тип, подсказка, объяснение, порядок и пометка «сгенерировано»', () => {
  for (const q of pack.questions) {
    assert.ok(q.hints.length >= 1 && q.hints[0].length > 5, `${q.id}: подсказка`);
    assert.ok(q.explanation.length > 3, `${q.id}: объяснение`);
    assert.equal(typeof q.sourceOrder, 'number');
    assert.equal(q.generated, true, `${q.id}: сгенерированный вопрос должен быть помечен`);
  }
});

test('утверждено только то, что утвердил администратор, и только неизменённое после проверки', () => {
  for (const e of [...pack.theory, ...pack.formulas, ...pack.examples, ...pack.questions]) {
    const d = decisions[e.id];
    if (d && d.hash === e.hash) assert.equal(e.status, d.status, e.id);
    else assert.equal(e.status, 'review', `${e.id}: без решения администратора — статус review`);
  }
});

test('все вопросы и записи уникальны (ID и хеш содержимого)', () => {
  const ids = [...pack.theory, ...pack.formulas, ...pack.examples, ...pack.questions].map((e) => e.id);
  assert.equal(new Set(ids).size, ids.length);
  const hashes = pack.questions.map((q) => q.hash);
  assert.equal(new Set(hashes).size, hashes.length);
});

test('ссылки вопросов на формулы указывают на существующие формулы', () => {
  const f = new Set(pack.formulas.map((x) => x.id));
  for (const q of pack.questions) for (const id of q.formulaIds) assert.ok(f.has(id), `${q.id} → ${id}`);
});

test('все формулы рендерятся KaTeX без ошибок', () => {
  for (const f of pack.formulas) katex.renderToString(f.tex, { throwOnError: true, displayMode: true });
});

test('числовые эталоны совпадают с независимым пересчётом', () => {
  for (const q of pack.questions.filter((x) => x.type === 'numeric')) {
    assert.ok(q.numeric?.check, `${q.id}: нет check`);
    const v = Number(new Function(`return (${q.numeric!.check})`)());
    assert.ok(Math.abs(v - q.numeric!.value) <= Math.max(Math.abs(v) * 0.005, q.numeric!.tolAbs ?? 1e-9), `${q.id}: ${q.numeric!.value} vs ${v}`);
  }
});

test('замечания к источнику: к чему, оригинал, что не так и конкретное предложение', () => {
  assert.ok(pack.errata.length >= 20);
  for (const e of pack.errata) {
    assert.ok(e.target && e.original && e.issue && e.suggestion, e.id);
    assert.doesNotMatch(e.suggestion, /^(Проверить|Уточнить)[^.]*\.?$/, `${e.id}: предложение должно говорить, чем заменить или что дописать`);
    assert.ok(pageRefs.has(e.page), e.id);
  }
});

test('отчёты импорта (по файлу) соответствуют фактическим числам', () => {
  assert.equal(pack.reports.length, 8);
  assert.deepEqual(pack.reports.map((r) => r.pagesProcessed), [81, 21, 1, 40, 28, 20, 2, 8]);
  for (const r of pack.reports) assert.equal(r.questionsInSource, 0, 'в конспектах нет готовых тестов — нельзя утверждать обратное');
  const sum = (k: 'questionsGenerated' | 'formulas' | 'theory' | 'examples') => pack.reports.reduce((a, r) => a + r[k], 0);
  assert.equal(sum('questionsGenerated'), pack.questions.length);
  assert.equal(sum('formulas'), pack.formulas.length);
  assert.equal(sum('theory'), pack.theory.length);
});

test('активны только разделы с материалами, пустых разделов и подразделов нет', () => {
  const active = pack.sections.filter((s) => s.status === 'active').map((s) => s.id);
  assert.deepEqual(active, ['mech', 'thermo', 'electro', 'optics', 'quantum']);
  for (const s of pack.sections) {
    const subs = pack.subsections.filter((x) => x.sectionId === s.id);
    const topics = pack.topics.filter((t) => subs.some((x) => x.id === t.subsectionId));
    if (s.status === 'active') assert.ok(topics.length > 0, `раздел ${s.id} без тем`);
    else assert.equal(topics.length, 0, `запланированный раздел ${s.id} не должен иметь тем`);
  }
  for (const sub of pack.subsections) assert.ok(pack.topics.some((t) => t.subsectionId === sub.id), `пустой подраздел ${sub.id}`);
});

test('порядок разделов: электродинамика стоит перед оптикой, оптика — перед квантовой физикой', () => {
  const order = (id: string) => pack.sections.find((s) => s.id === id)!.order;
  assert.ok(order('thermo') < order('electro'));
  assert.ok(order('electro') < order('optics'));
  assert.ok(order('optics') < order('quantum'));
  // колебательный контур со стр. o01 — в электродинамике, а не в оптике
  const emw = pack.subsections.find((s) => s.id === 'emw')!;
  assert.equal(emw.sectionId, 'electro');
  assert.equal(pack.topics.find((t) => t.id === 'em-circuit')!.subsectionId, 'emw');
  // подразделы конспектов по электричеству и магнетизму стоят перед «Электромагнитными колебаниями и волнами»
  const sub = (id: string) => pack.subsections.find((s) => s.id === id)!;
  for (const id of ['estat', 'capac', 'dc', 'ecur', 'mag', 'induct']) {
    assert.equal(sub(id).sectionId, 'electro');
    assert.ok(sub(id).order < emw.order, id);
  }
  // электростатика → конденсаторы → постоянный ток → ток в средах → магнетизм
  const chain = ['estat', 'capac', 'dc', 'ecur', 'mag'];
  for (let i = 1; i < chain.length; i++) assert.ok(sub(chain[i - 1]).order < sub(chain[i]).order, chain[i]);
  // тема о диоде начинается на последнем листе тетради по электричеству и продолжается в тетради по магнетизму
  assert.deepEqual(pack.topics.find((t) => t.id === 'el-diode')!.pages, ['c40', 'e01']);
  // внутри подраздела темы идут по датам тетрадей: контур 4.03.25 (e20) раньше радиоволн 13.03.25 (o01)
  const topic = (id: string) => pack.topics.find((t) => t.id === id)!;
  assert.ok(topic('em-lc').order < topic('em-waves').order);
  assert.ok(topic('em-waves').order < topic('em-circuit').order);
  // механические колебания — в «Механике» (по классификации ТЗ)
  assert.equal(sub('osc').sectionId, 'mech');
  // статика (дополнена из интернета) — между динамикой и жидкостями; атом и ядро — после фотоэффекта
  assert.equal(sub('stat').sectionId, 'mech');
  assert.ok(sub('dyn').order < sub('stat').order && sub('stat').order < sub('fluids').order);
  for (const [a, b] of [['qphot', 'atom'], ['atom', 'nucl'], ['nucl', 'radio']]) {
    assert.equal(sub(b).sectionId, 'quantum');
    assert.ok(sub(a).order < sub(b).order, b);
  }
});

test('анимированные рисунки безопасны и привязаны к блокам теории', () => {
  const figs = pack.figures ?? {};
  assert.ok(Object.keys(figs).length >= 20);
  const used = new Set(pack.theory.map((t) => t.figure).filter(Boolean));
  for (const [id, f] of Object.entries(figs)) {
    assert.ok(used.has(id), `рисунок ${id} не используется`);
    assert.ok(f.title.length > 10, `${id}: нет описания`);
    assert.doesNotMatch(f.svg, /<script|\son[a-z]+\s*=|javascript:|<foreignObject|<image/i, id);
    assert.match(f.svg, /<animate/, `${id}: нет анимации`);
    for (const m of f.svg.matchAll(/\sid="([^"]+)"/g)) assert.ok(m[1].startsWith(`${id}-`), `${id}: id ${m[1]}`);
  }
  for (const t of pack.theory) if (t.figure) assert.ok(figs[t.figure], `${t.id} → ${t.figure}`);
});

test('анимации есть во всех подразделах, каждый рисунок — в одном блоке теории', () => {
  const topicSub = new Map(pack.topics.map((t) => [t.id, t.subsectionId]));
  const perSub = new Map<string, number>();
  const seen = new Set<string>();
  for (const t of pack.theory) {
    if (!t.figure) continue;
    assert.ok(!seen.has(t.figure), `рисунок ${t.figure} прикреплён дважды`);
    seen.add(t.figure);
    const s = topicSub.get(t.topicId)!;
    perSub.set(s, (perSub.get(s) ?? 0) + 1);
  }
  for (const s of pack.subsections) assert.ok((perSub.get(s.id) ?? 0) > 0, `в подразделе ${s.id} нет анимаций`);
  assert.equal(seen.size, Object.keys(pack.figures ?? {}).length);
});

test('дополнения из интернета: помечены, со ссылками https и местом пробела в конспекте; прежние записи не затронуты', () => {
  const all = [...pack.theory, ...pack.formulas, ...pack.examples, ...pack.questions];
  const web = all.filter((e) => e.web);
  assert.ok(web.length >= 100, `записей из интернета: ${web.length}`);
  for (const e of web) {
    assert.ok(e.web!.length > 0, e.id);
    for (const r of e.web!) {
      assert.match(r.url, /^https:\/\/[^\s]+$/, `${e.id}: ${r.url}`);
      assert.ok(r.title.length > 3, e.id);
    }
    assert.ok(e.sources.length > 0 && e.sources.every((s) => pageRefs.has(s.page)), `${e.id}: место пробела в конспекте`);
    assert.equal(e.status, decisions[e.id]?.status ?? 'review', `${e.id}: без решения владельца — на проверке`);
  }
  // у тем «из интернета» все записи — из интернета
  for (const t of pack.topics.filter((x) => x.web)) {
    const rec = all.filter((e) => e.topicId === t.id);
    assert.ok(rec.length > 0 && rec.every((e) => e.web), t.id);
  }
  // каждый подраздел-дополнение и каждая тема-дополнение описаны в отчёте импорта
  const added = pack.reports.reduce((a, r) => a + (r.addedFromWeb ?? 0), 0);
  assert.equal(added, web.length);
});

test('пробелы, отмеченные раньше, заполнены и связаны с замечаниями', () => {
  const t = (id: string) => pack.theory.filter((x) => x.topicId === id);
  const has = (id: string, re: RegExp) => assert.ok(t(id).some((x) => x.web && re.test(x.title ?? '')), `${id}: ${re}`);
  has('wave-interference', /минимум/i);
  has('wave-diffraction', /белый свет/i);
  has('em-waves', /шкала/i);
  has('ac-resonance', /резонанс напряжений/i);
  has('dc-meters', /шунт/i);
  has('kin-path-accel', /средняя скорость/i);
  has('fl-atmospheric', /керосин/i);
  has('at-bohr', /второй постулат/i);
  has('rad-radiation', /дозы/i);
});

test('дифракция (фото d01–d02): тема записана по конспекту, сомнительные места — в замечаниях DF01–DF06', () => {
  const th = pack.theory.filter((x) => x.topicId === 'wave-diffraction');
  const own = th.filter((x) => !x.web);
  assert.ok(own.length >= 6, 'теория по конспекту');
  for (const x of own) assert.ok(x.sources.every((s) => s.page === 'd01' || s.page === 'd02'), `${x.id}: источник — фото дифракции`);
  assert.ok(th.filter((x) => x.web).length <= 2, 'из интернета — только дополнения');
  const df = pack.errata.filter((e) => e.id.startsWith('DF'));
  assert.equal(df.length, 6);
  for (const e of df) assert.ok(e.page === 'd01' || e.page === 'd02', e.id);
  // оригинал сохранён: «постоянная — количество штрихов в каждом мм» и K = [d/λ]
  assert.ok(th.some((x) => /количество штрихов/i.test(x.body)), 'формулировка конспекта сохранена');
  const tex = pack.formulas.filter((f) => f.topicId === 'wave-diffraction').map((f) => f.tex).join(' ');
  for (const re of [/d\\sin\\varphi\s*=\s*k\\lambda/, /a\s*\+\s*b/, /\\sqrt\{L\^2\s*\+\s*x\^2\}/, /2\\left\[/]) assert.match(tex, re);
});

test('статика: рычаги, блоки, наклонная плоскость, центр тяжести и сложные задачи — из интернета, с разобранными примерами', () => {
  const ids = ['st-kinds', 'st-blocks', 'st-incline', 'st-center', 'st-problems'];
  for (const id of ids) {
    const t = pack.topics.find((x) => x.id === id);
    assert.ok(t && t.web && t.subsectionId === 'stat', id);
    assert.ok(pack.examples.filter((e) => e.topicId === id).length >= 2, `${id}: примеры`);
    assert.ok(pack.questions.filter((q) => q.topicId === id).length >= 5, `${id}: вопросы`);
    assert.ok(pack.formulas.filter((f) => f.topicId === id).length >= 2, `${id}: формулы`);
    for (const q of pack.questions.filter((x) => x.topicId === id)) assert.equal(q.status, decisions[q.id]?.status ?? 'review', q.id);
  }
  const figs = new Set(pack.theory.filter((x) => x.topicId.startsWith('st-') && x.figure).map((x) => x.figure!));
  for (const f of ['lever', 'lever-kinds', 'pulleys', 'incline-golden', 'center-mass', 'equilibrium-types']) assert.ok(figs.has(f), f);
});
