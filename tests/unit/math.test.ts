// Математика: (1) независимая проверка утверждений теории перебором и точной арифметикой;
// (2) проверка ответов разобранных примеров; (3) целостность учебной базы math/pack.json
// (порядок книги, место в книге, источники с датой проверки, решения у задач).

import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import type { ContentPack } from '../../src/domain/types.ts';

const pack: ContentPack = JSON.parse(fs.readFileSync(new URL('../../content/math/pack.json', import.meta.url), 'utf8'));
const physics: ContentPack = JSON.parse(fs.readFileSync(new URL('../../content/pack.json', import.meta.url), 'utf8'));

const gcd = (a: number, b: number): number => (b ? gcd(b, a % b) : Math.abs(a));
const lcm = (a: number, b: number) => (a / gcd(a, b)) * b;
const digits = (n: number) => String(n).split('').map(Number);
const mod = (a: number, b: number) => ((a % b) + b) % b;
const divisors = (n: number) => Array.from({ length: n }, (_, i) => i + 1).filter((d) => n % d === 0);
const factor = (n: number) => {
  const f = new Map<number, number>();
  for (let p = 2; p * p <= n; p++) while (n % p === 0) { f.set(p, (f.get(p) ?? 0) + 1); n /= p; }
  if (n > 1) f.set(n, (f.get(n) ?? 0) + 1);
  return f;
};

// ───────────── 1.1 Натуральные и целые числа: теория ─────────────

test('1.1.1: свойства действий и тождество n(n+3) − (n+1)(n+2) = −2', () => {
  for (let n = -50; n <= 50; n++) assert.equal(n * (n + 3) - (n + 1) * (n + 2), -2);
  for (const [a, b, c] of [[3, -7, 5], [-2, 4, 9], [0, 1, -1]]) {
    assert.equal(-(a + b - c), -a - b + c);
    assert.equal(a - (b - c), a - b + c);
    assert.equal(a * (b + c), a * b + a * c);
  }
  assert.equal(24 / 4 * 2, 12, 'деление и умножение слева направо');
  assert.equal(-(3 ** 2), -9);
  assert.equal((-3) ** 2, 9);
});

test('1.1.2: признаки делимости на 2, 3, 4, 5, 8, 9, 10, 11, 16, 25, 125 — перебором до 100 000', () => {
  const last = (n: number, k: number) => n % 10 ** k;
  const alt = (n: number) => digits(n).reverse().reduce((s, d, i) => s + (i % 2 ? -d : d), 0);
  const sum = (n: number) => digits(n).reduce((a, b) => a + b, 0);
  for (let n = 1; n <= 100_000; n++) {
    assert.equal(n % 2 === 0, [0, 2, 4, 6, 8].includes(n % 10));
    assert.equal(n % 5 === 0, [0, 5].includes(n % 10));
    assert.equal(n % 10 === 0, n % 10 === 0);
    assert.equal(n % 4 === 0, last(n, 2) % 4 === 0);
    assert.equal(n % 25 === 0, last(n, 2) % 25 === 0);
    assert.equal(n % 8 === 0, last(n, 3) % 8 === 0);
    assert.equal(n % 125 === 0, last(n, 3) % 125 === 0);
    assert.equal(n % 16 === 0, last(n, 4) % 16 === 0);
    assert.equal(n % 3, sum(n) % 3, 'остаток при делении на 3 равен остатку суммы цифр');
    assert.equal(n % 9, sum(n) % 9, 'остаток при делении на 9 равен остатку суммы цифр');
    assert.equal(n % 11 === 0, alt(n) % 11 === 0);
  }
});

test('1.1.2: делимость на произведение — только для взаимно простых множителей', () => {
  for (const [m, k] of [[2, 3], [3, 4], [3, 5], [2, 9], [4, 9], [5, 9], [8, 9]]) {
    assert.equal(gcd(m, k), 1);
    for (let n = 1; n <= 5000; n++) assert.equal(n % m === 0 && n % k === 0, n % (m * k) === 0);
  }
  assert.ok(18 % 2 === 0 && 18 % 6 === 0 && 18 % 12 !== 0, 'контрпример 2 и 6');
  assert.ok(12 % 4 === 0 && 12 % 6 === 0 && 12 % 24 !== 0, 'обязательно делится только на НОК(4, 6) = 12');
});

test('1.1.3: деление с остатком — существование и единственность, отрицательное делимое, арифметика остатков', () => {
  for (let a = -200; a <= 200; a++) for (let b = 1; b <= 13; b++) {
    const q = Math.floor(a / b), r = a - b * q;
    assert.ok(r >= 0 && r < b);
    assert.equal(r, mod(a, b));
  }
  assert.equal(mod(-17, 5), 3);
  assert.equal(mod(-23, 5), 2);
  for (let a = 0; a < 60; a++) for (let c = 0; c < 60; c++) for (const b of [3, 5, 7, 9, 10]) {
    assert.equal((a + c) % b, ((a % b) + (c % b)) % b);
    assert.equal((a * c) % b, ((a % b) * (c % b)) % b);
  }
  // период остатков 2^n при делении на 7: 2, 4, 1
  assert.deepEqual([1, 2, 3, 4, 5, 6].map((k) => 2 ** k % 7), [2, 4, 1, 2, 4, 1]);
});

test('1.1.4: НОД·НОК = ab, число делителей τ(n) = ∏(k+1), общие делители = делители НОД, алгоритм Евклида', () => {
  for (let a = 1; a <= 120; a++) for (let b = 1; b <= 120; b++) assert.equal(gcd(a, b) * lcm(a, b), a * b);
  for (let n = 1; n <= 2000; n++) {
    const t = [...factor(n).values()].reduce((p, k) => p * (k + 1), 1);
    assert.equal(divisors(n).length, t, `τ(${n})`);
  }
  const common = divisors(360).filter((d) => 84 % d === 0);
  assert.deepEqual(common, divisors(gcd(360, 84)));
  assert.equal(common.length, 6);
  // шаги Евклида из примера
  assert.equal(1071 - 462 * 2, 147);
  assert.equal(462 - 147 * 3, 21);
  assert.equal(147 % 21, 0);
  assert.equal(gcd(1071, 462), 21);
});

test('1.1.5: периоды последних цифр степеней (1, 2 или 4) и нули на конце факториала', () => {
  const cycle = (d: number) => {
    const seen: number[] = [];
    let x = d % 10;
    while (!seen.includes(x)) { seen.push(x); x = (x * d) % 10; }
    return seen;
  };
  assert.deepEqual(cycle(2), [2, 4, 8, 6]);
  assert.deepEqual(cycle(3), [3, 9, 7, 1]);
  assert.deepEqual(cycle(7), [7, 9, 3, 1]);
  assert.deepEqual(cycle(8), [8, 4, 2, 6]);
  assert.deepEqual(cycle(4), [4, 6]);
  assert.deepEqual(cycle(9), [9, 1]);
  for (const d of [0, 1, 5, 6]) assert.deepEqual(cycle(d), [d]);
  // правило «k = 4m + s, при s = 0 берём 4» для любой цифры
  for (let d = 0; d <= 9; d++) for (let k = 1; k <= 40; k++) {
    const s = k % 4 === 0 ? 4 : k % 4;
    assert.equal(Number(BigInt(d) ** BigInt(k) % 10n), Number(BigInt(d) ** BigInt(s) % 10n));
  }
  const fact = (n: number) => { let f = 1n; for (let i = 2n; i <= BigInt(n); i++) f *= i; return f; };
  for (let n = 1; n <= 130; n++) {
    const z = Math.floor(n / 5) + Math.floor(n / 25) + Math.floor(n / 125);
    const s = fact(n).toString();
    assert.equal(s.length - s.replace(/0+$/, '').length, z, `${n}!`);
  }
});

test('1.1.6: правила знаков, степени отрицательных чисел', () => {
  for (const a of [-5, -2, 0, 3, 7]) for (const b of [-4, -1, 2, 6]) {
    assert.equal((-a) * (-b), a * b);
    assert.equal((-a) * b, -(a * b));
    assert.equal(a - b, a + (-b));
  }
  for (const a of [-3, -2, 2, 3]) for (let n = 0; n < 5; n++) {
    assert.equal((-a) ** (2 * n), a ** (2 * n));
    assert.equal((-a) ** (2 * n + 1), -(a ** (2 * n + 1)));
  }
});

// ───────────── ответы разобранных примеров 1.1 (пересчёт) ─────────────

test('1.1: ответы разобранных примеров пересчитаны независимо', () => {
  assert.equal(38 * 37 - 37 * 36 + 36 * 35 - 35 * 34, 144);
  assert.equal(3001 * 3004 - 3002 * 3003, -2);
  let fives = 0;
  for (let n = 1; n <= 100; n++) fives += digits(n).filter((d) => d === 5).length;
  assert.equal(fives, 20);
  assert.deepEqual([...Array(10).keys()].filter((x) => (4056 + 100 * x) % 9 === 0), [3]);
  assert.equal(7380 % 36, 0);
  const pairs: [number, number][] = [];
  for (let a = 1; a <= 9; a++) for (const b of [0, 5]) if ((a * 10000 + 2730 + b) % 45 === 0) pairs.push([a, b]);
  assert.deepEqual(pairs, [[1, 5], [6, 0]]);
  assert.equal((395 - 5) / 13, 30);
  assert.equal(Number(2n ** 100n % 7n), 2);
  for (let q = 0; q < 50; q++) assert.equal((6 * q + 5) % 3, 2);
  assert.deepEqual([gcd(84, 90), lcm(84, 90)], [6, 1260]);
  assert.equal(Number(7n ** 2026n % 10n), 9);
  assert.equal(Number((2n ** 50n + 3n ** 50n) % 10n), 3);
  let s = 0n, f = 1n;
  for (let i = 1n; i <= 100n; i++) { f *= i; s += f; }
  assert.equal(Number(s % 10n), 3);
  assert.equal(-12 + 18 / -3 - 4 * -5, 2);
  let sm = 0;
  for (let k = 1; k <= 101; k++) sm += (-1) ** k;
  assert.equal(sm, -1);
  assert.equal(Array.from({ length: 46 }, (_, i) => i - 20).reduce((a, b) => a + b), 115);
});

// ───────────── 1.2 Дроби ─────────────
type Q = [number, number]; // несократимая дробь [p, q], q > 0
const fr = (p: number, q: number): Q => { const g = gcd(p, q) || 1; const s = q < 0 ? -1 : 1; return [(s * p) / g, (s * q) / g]; };
const add = (a: Q, b: Q) => fr(a[0] * b[1] + b[0] * a[1], a[1] * b[1]);
const mul = (a: Q, b: Q) => fr(a[0] * b[0], a[1] * b[1]);
const div = (a: Q, b: Q) => fr(a[0] * b[1], a[1] * b[0]);
/** Десятичная запись p/q (0 < p/q < 1): [цифры до периода, период] — делением с запоминанием остатков. */
function decimal(p: number, q: number): [string, string] {
  const seen = new Map<number, number>();
  let r = p % q, s = '';
  while (r && !seen.has(r)) { seen.set(r, s.length); r *= 10; s += Math.floor(r / q); r %= q; }
  return r ? [s.slice(0, seen.get(r)), s.slice(seen.get(r))] : [s, ''];
}

test('1.2.1: действия с дробями и разложение k/(n(n+k)) = 1/n − 1/(n+k)', () => {
  for (let n = 1; n < 60; n++) for (let k = 1; k < 6; k++) assert.deepEqual(fr(k, n * (n + k)), add(fr(1, n), fr(-1, n + k)));
  assert.deepEqual(add(add(fr(5, 12), fr(7, 18)), fr(-1, 4)), [5, 9]);
  let s: Q = [0, 1];
  for (let n = 3; n <= 19; n += 2) s = add(s, fr(2, n * (n + 2)));
  assert.deepEqual(s, [2, 7]);
  assert.deepEqual([60 * 9 / 4, 60 * 7 / 6, 60 * 11 / 10], [135, 70, 66]);
  assert.equal(lcm(lcm(4, 6), 10), 60);
  assert.deepEqual(div(mul(fr(5, 6), fr(9, 10)), fr(3, 8)), [2, 1]);
  // перекрёстное сравнение из задачи
  assert.ok(9 * 11 > 7 * 14 && 7 * 8 > 5 * 11 && 5 * 5 > 3 * 8);
});

test('1.2.2: смешанные числа — примеры пересчитаны', () => {
  assert.deepEqual(add(fr(23, 6), fr(11, 4)), fr(79, 12)); // 6 7/12
  assert.deepEqual(add(fr(21, 4), fr(-8, 3)), fr(31, 12)); // 2 7/12
  assert.deepEqual(mul(mul(fr(-3, 2), fr(-3, 2)), fr(-3, 2)), fr(-27, 8));
  let p: Q = [1, 1];
  for (let n = 2; n <= 9; n++) p = mul(p, fr(n + 1, n));
  assert.deepEqual(p, [5, 1]);
  assert.deepEqual([Math.floor(47 / 6), 47 % 6], [7, 5]);
});

test('1.2.3: десятичные дроби и стандартный вид', () => {
  assert.equal(Math.round((0.48 * 2.5 - 0.6) / 0.15 * 1e9) / 1e9, 4);
  assert.deepEqual(add(fr(1, 8), mul(fr(3, 8), fr(2, 5))), [11, 40]);
  assert.equal(11 / 40, 0.275);
  assert.equal(5.23e4, 52300);
  assert.equal(4.52e-4, 0.000452);
  assert.deepEqual(fr(375, 1000), [3, 8]);
});

test('1.2.4: признак конечности (только 2 и 5) и формулы перевода периодических дробей — перебором', () => {
  for (let q = 2; q <= 200; q++) for (let p = 1; p < q; p++) {
    if (gcd(p, q) !== 1) continue;
    let m = q;
    while (m % 2 === 0) m /= 2;
    while (m % 5 === 0) m /= 5;
    const [pre, per] = decimal(p, q);
    assert.equal(per === '', m === 1, `${p}/${q}`);
    if (per) {
      assert.equal(pre === '', q % 2 !== 0 && q % 5 !== 0, `${p}/${q}: чисто периодическая ⇔ q взаимно просто с 10`);
      // формула перевода: (число до конца периода − число до периода) / (t девяток и s нулей)
      const num = BigInt(pre + per) - BigInt(pre || '0');
      const den = BigInt('9'.repeat(per.length) + '0'.repeat(pre.length));
      assert.equal(num * BigInt(q), BigInt(p) * den, `${p}/${q} = 0,${pre}(${per})`);
    }
  }
  assert.deepEqual(decimal(3, 11), ['', '27']);
  assert.deepEqual(decimal(7, 30), ['2', '3']);
  assert.deepEqual(decimal(5, 24), ['208', '3']);
  assert.deepEqual(fr(45, 99), [5, 11]);
  assert.deepEqual(fr(9, 75), [3, 25]);
  assert.deepEqual(fr(16 - 1, 90), [1, 6]);
  assert.ok(0.34444 > 0.34 && 0.34 > 1 / 3 && 1 / 3 > 0.33);
});

// ───────────── целостность учебной базы математики ─────────────

// ───────────── 1.3 Выражения и 1.4 Корни ─────────────
// Тождества проверяются подстановкой многих точек (численно, с допуском), а не сравнением строк.
const pts = [-3.7, -2, -1.25, -0.5, 0.3, 1, 1.75, 2.5, 4, 7.2];
const pos = [0.04, 0.5, 1.3, 2, 3.61, 5, 7.29, 9, 16, 30.5];
const near = (a: number, b: number, eps = 1e-9) => Math.abs(a - b) <= eps * Math.max(1, Math.abs(a), Math.abs(b));
const ident2 = (l: (a: number, b: number) => number, r: (a: number, b: number) => number, A = pts, B = pts, skip?: (a: number, b: number) => boolean) => {
  for (const a of A) for (const b of B) if (!skip?.(a, b)) assert.ok(near(l(a, b), r(a, b)), `${a}, ${b}: ${l(a, b)} ≠ ${r(a, b)}`);
};

test('1.3.2: формулы сокращённого умножения — подстановкой 100 пар значений', () => {
  ident2((a, b) => (a + b) ** 2, (a, b) => a * a + 2 * a * b + b * b);
  ident2((a, b) => (a - b) ** 2, (a, b) => a * a - 2 * a * b + b * b);
  ident2((a, b) => a * a - b * b, (a, b) => (a - b) * (a + b));
  ident2((a, b) => (a + b) ** 3, (a, b) => a ** 3 + 3 * a * a * b + 3 * a * b * b + b ** 3);
  ident2((a, b) => (a - b) ** 3, (a, b) => a ** 3 - 3 * a * a * b + 3 * a * b * b - b ** 3);
  ident2((a, b) => a ** 3 + b ** 3, (a, b) => (a + b) * (a * a - a * b + b * b));
  ident2((a, b) => a ** 3 - b ** 3, (a, b) => (a - b) * (a * a + a * b + b * b));
  ident2((a, b) => a * a + b * b, (a, b) => (a + b) ** 2 - 2 * a * b);
  ident2((a, b) => a ** 3 + b ** 3, (a, b) => (a + b) ** 3 - 3 * a * b * (a + b));
});

test('1.3: ответы разобранных примеров пересчитаны независимо', () => {
  for (const x of pts) {
    assert.ok(near(3 * x * x * 1.5 * (-2 * x * 1.5 ** 3) * 0.5 * x, -3 * x ** 4 * 1.5 ** 4)); // y = 1,5
    assert.ok(near((2 * x - 3) * (x * x + x - 1), 2 * x ** 3 - x * x - 5 * x + 3));
    assert.ok(near(x ** 3 - 4 * x, x * (x - 2) * (x + 2)));
    assert.ok(near(x ** 3 - 3 * x * x + 2 * x - 6, (x - 3) * (x * x + 2)));
    if (x !== 0 && x !== -3) assert.ok(near((x * x - 9) / (x * x + 3 * x), (x - 3) / x));
    if (x !== 0 && x !== 2) assert.ok(near(x / (x - 2) - 4 / (x * x - 2 * x), (x + 2) / x));
  }
  assert.equal((3 - 2) ** 4, 1); // сумма коэффициентов = P(1)
  assert.equal((3 * 0 - 2) ** 4, 16); // свободный член = P(0)
  assert.equal(49 * 51, 2499);
  assert.equal(101 ** 3, 1030301);
  // a + b = 5, ab = 3: a, b — корни t² − 5t + 3
  const r1 = (5 + Math.sqrt(13)) / 2, r2 = (5 - Math.sqrt(13)) / 2;
  assert.ok(near(r1 * r1 + r2 * r2, 19) && near(r1 ** 3 + r2 ** 3, 80));
  // a + b = 4, ab = −3: a²b + ab² = ab(a + b) = −12
  const s1 = 2 + Math.sqrt(7), s2 = 2 - Math.sqrt(7);
  assert.ok(near(s1 * s1 * s2 + s1 * s2 * s2, -12));
  ident2((a, b) => (a + b) ** 2 - (a - b) ** 2, (a, b) => 4 * a * b);
});

test('1.4: свойства корней и сопряжённые выражения — подстановкой', () => {
  ident2((a, b) => Math.sqrt(a * b), (a, b) => Math.sqrt(a) * Math.sqrt(b), pos, pos);
  ident2((a, b) => Math.sqrt(a / b), (a, b) => Math.sqrt(a) / Math.sqrt(b), pos, pos);
  ident2((a, b) => a - b, (a, b) => (Math.sqrt(a) - Math.sqrt(b)) * (Math.sqrt(a) + Math.sqrt(b)), pos, pos);
  ident2((a, b) => a + 2 * Math.sqrt(a * b) + b, (a, b) => (Math.sqrt(a) + Math.sqrt(b)) ** 2, pos, pos);
  ident2((a, b) => a * Math.sqrt(a) + b * Math.sqrt(b), (a, b) => (Math.sqrt(a) + Math.sqrt(b)) * (a - Math.sqrt(a * b) + b), pos, pos);
  for (const a of pts) {
    assert.ok(near(Math.sqrt(a * a), Math.abs(a)), '√(a²) = |a|');
    assert.ok(near(Math.pow(a ** 4, 1 / 4), Math.abs(a)), '⁴√(a⁴) = |a|');
    assert.ok(near(Math.cbrt(a ** 3), a), '∛(a³) = a');
  }
  for (const a of pos) for (const [m, n, k] of [[2, 3, 2], [1, 4, 3], [3, 5, 2]]) {
    assert.ok(near(a ** (m / n), Math.pow(Math.pow(a, 1 / n), m)), 'a^(m/n) = (ⁿ√a)^m');
    assert.ok(near(Math.pow(a ** (m * k), 1 / (n * k)), Math.pow(a ** m, 1 / n)), 'сокращение показателей');
    assert.ok(near(Math.pow(Math.pow(a, 1 / m), 1 / n), Math.pow(a, 1 / (m * n))), 'корень из корня');
  }
  // сложный радикал: √(a + b ± 2√(ab)) = √a ± √b (a ≥ b)
  for (const [a, b] of [[6, 5], [5, 4], [5, 1], [3, 2], [10, 3]]) assert.ok(near(Math.sqrt(a + b - 2 * Math.sqrt(a * b)), Math.sqrt(a) - Math.sqrt(b)));
});

test('1.4: ответы разобранных примеров пересчитаны независимо', () => {
  const r = Math.sqrt;
  assert.ok(near(Math.abs(1 - r(3)) + Math.abs(2 - r(3)), 1));
  assert.ok(near(r(18) * r(50), 30) && near(r(75) / r(3), 5));
  assert.ok(5 * r(2) > 3 * r(5) && 50 > 45);
  assert.ok(near(r(9 - 2 * r(20)) + r(9 + 2 * r(20)), 2 * r(5)));
  assert.ok(near(4 / (r(5) - 1) - r(5), 1));
  assert.ok(near(1 / (r(2) + 1) + 1 / (r(3) + r(2)) + 1 / (2 + r(3)), 1));
  for (const x of pos) {
    assert.ok(near((x - 9) / (r(x) + 3), r(x) - 3));
    if (x !== 4) assert.ok(near((x * r(x) + 8) / (r(x) + 2), x - 2 * r(x) + 4));
    for (const b of pos) if (x !== b) assert.ok(near(((r(x) + r(b)) ** 2 - 4 * r(x * b)) / (r(x) - r(b)), r(x) - r(b), 1e-7));
    assert.ok(near(x ** 0.5 * x ** (1 / 3) / x ** (1 / 6), x ** (2 / 3)));
  }
  assert.ok(near((9 * 3 + 8) / (3 + 2), 7));
  assert.ok(near(27 ** (2 / 3) + 16 ** (-3 / 4), 9.125));
  assert.ok(near(Math.cbrt(-125) + 81 ** 0.25 - 64 ** (1 / 6), -4));
  assert.ok(near(8 ** (2 / 3), 4));
});

const lin2 = (a: number, b: number, n: number) => Array.from({ length: n }, (_, i) => a + ((b - a) * i) / (n - 1));
// ───────────── 1.5–1.10: перебор и независимый пересчёт ─────────────
const range = (lo: number, hi: number) => Array.from({ length: hi - lo + 1 }, (_, i) => lo + i);
const ints = (lo: number, hi: number, p: (x: number) => boolean) => range(lo, hi).filter(p);
const sum = (a: number[]) => a.reduce((s, x) => s + x, 0);
const roots2 = (a: number, b: number, c: number): number[] => {
  const D = b * b - 4 * a * c;
  if (D < 0) return [];
  if (D === 0) return [-b / (2 * a)];
  return [(-b - Math.sqrt(D)) / (2 * a), (-b + Math.sqrt(D)) / (2 * a)];
};

test('1.5.2–1.5.3: формула корней, теорема Виета, симметрические выражения, a+b+c=0 — перебор коэффициентов', () => {
  for (let a = -6; a <= 6; a++) for (let b = -8; b <= 8; b++) for (let c = -8; c <= 8; c++) {
    if (a === 0) continue;
    const r = roots2(a, b, c);
    for (const x of r) assert.ok(near(a * x * x + b * x + c, 0, 1e-9), `${a},${b},${c}: корень ${x}`);
    const D = b * b - 4 * a * c;
    assert.equal(r.length, D > 0 ? 2 : D === 0 ? 1 : 0);
    if (r.length === 2) {
      const [x1, x2] = r, s = -b / a, p = c / a;
      assert.ok(near(x1 + x2, s) && near(x1 * x2, p), 'Виет');
      assert.ok(near(x1 * x1 + x2 * x2, s * s - 2 * p) && near(x1 ** 3 + x2 ** 3, s ** 3 - 3 * p * s) && near((x1 - x2) ** 2, s * s - 4 * p), 'симметрические');
      if (a * c < 0) assert.ok(x1 * x2 < 0, 'ac < 0 ⇒ корни разных знаков');
      for (const t of [-2, 0, 1.5, 3]) assert.ok(near(a * t * t + b * t + c, a * (t - x1) * (t - x2), 1e-9), 'разложение');
    }
    if (a + b + c === 0) assert.ok(r.some((x) => near(x, 1)) && r.some((x) => near(x, c / a)), 'a + b + c = 0');
    if (a - b + c === 0) assert.ok(r.some((x) => near(x, -1)) && r.some((x) => near(x, -c / a)), 'a − b + c = 0');
    if (b % 2 === 0 && r.length) { const k = b / 2; assert.ok(near(Math.max(...r), a > 0 ? (-k + Math.sqrt(k * k - a * c)) / a : (-k - Math.sqrt(k * k - a * c)) / a), 'чётный коэффициент'); }
  }
});

test('1.5: ответы примеров и задач пересчитаны', () => {
  assert.equal((22 - 1) / 3 - (22 + 2) / 4, 1);
  assert.equal((2 * 17 + 1) / 5, (17 + 4) / 3);
  assert.deepEqual(roots2(2, -7, 3), [0.5, 3]);
  assert.ok(near(roots2(3, 14, -5)[0], -5) && near(roots2(3, 14, -5)[1], 1 / 3));
  assert.deepEqual(roots2(1, -7, 10), [2, 5]);
  assert.ok(near(-0.5 * 4, -2)); // 1.5.6: (a−2)x² + 4x + 2 при a = 2: x = −1/2
  // рациональные уравнения — перебор корней-кандидатов
  const ok = (f: (x: number) => number, x: number) => Number.isFinite(f(x)) && near(f(x), 0, 1e-9);
  assert.ok(ok((x) => (x * x) / (x - 2) - 4 / (x - 2), -2) && !ok((x) => (x * x) / (x - 2) - 4 / (x - 2), 2));
  assert.ok(ok((x) => 3 / (x - 1) + 1 / (x + 1) - 4 / (x * x - 1), 0.5));
  for (const x of [1, -1, 2, -2]) assert.ok(ok((t) => t ** 4 - 5 * t * t + 4, x));
  const all = [1, -2, 2, -3]; for (const x of all) assert.ok(ok((t) => (t * t + t) ** 2 - 8 * (t * t + t) + 12, x));
  assert.equal(sum(all), -2);
  // параметр: (a − 1)x² + 2x + 1 = 0 ровно один корень при a = 1 и a = 2 (перебор a)
  const one = range(-5, 5).filter((a) => (a === 1 ? 1 : roots2(a - 1, 2, 1).length) === 1);
  assert.deepEqual(one, [1, 2]);
  // x² − 2mx + m + 2 = 0: два корня ⇔ m < −1 или m > 2
  for (const m of range(-6, 6)) assert.equal(roots2(1, -2 * m, m + 2).length === 2, m < -1 || m > 2, `m = ${m}`);
  // x² − 2x + k: два различных положительных ⇔ 0 < k < 1
  for (const k of [-0.5, 0, 0.25, 0.75, 1, 1.5]) { const r = roots2(1, -2, k); assert.equal(r.length === 2 && r.every((x) => x > 0), k > 0 && k < 1); }
});

test('1.6: системы — подстановка решений и перебор', () => {
  const sat = (eqs: ((x: number, y: number) => number)[], x: number, y: number) => eqs.every((e) => near(e(x, y), 0, 1e-9));
  assert.ok(sat([(x, y) => x + 2 * y - 7, (x, y) => 3 * x - y - 7], 3, 2));
  assert.ok(sat([(x, y) => 3 * x + 4 * y - 10, (x, y) => 5 * x - 4 * y - 6], 2, 1));
  for (const [x, y] of [[3, 2], [-2, -3]]) assert.ok(sat([(x, y) => x - y - 1, (x, y) => x * x + y * y - 13], x, y));
  for (const [x, y] of [[1, 2], [2, 1]]) assert.ok(sat([(x, y) => x ** 3 + y ** 3 - 9, (x, y) => x + y - 3], x, y));
  for (const [x, y] of [[3, 3], [4, 2]]) assert.ok(sat([(x, y) => x * x - 3 * x * y + 2 * y * y, (x, y) => x + y - 6], x, y));
  assert.ok(sat([(x, y) => x * x * y - 12, (x, y) => x * y * y - 18], 2, 3));
  for (const [x, y] of [[3, 1], [-1, -3]]) assert.ok(sat([(x, y) => x ** 3 - y ** 3 - 26, (x, y) => x - y - 2], x, y));
  // целочисленный перебор: x⁴ − y⁴ = 15, x² − y² = 3 — ровно 4 решения
  const sols = range(-10, 10).flatMap((x) => range(-10, 10).map((y) => [x, y])).filter(([x, y]) => x ** 4 - y ** 4 === 15 && x * x - y * y === 3);
  assert.equal(sols.length, 4);
  // линейные системы с параметром: Δ = 0 и проверка свободных членов
  const kind = (a1: number, b1: number, c1: number, a2: number, b2: number, c2: number) => {
    const d = a1 * b2 - a2 * b1;
    if (d !== 0) return 'one';
    return a1 * c2 - a2 * c1 === 0 && b1 * c2 - b2 * c1 === 0 ? 'inf' : 'none';
  };
  assert.equal(kind(6, 3, 6, 2, 1, 2), 'inf');
  assert.deepEqual(range(-5, 5).filter((a) => kind(1, a, 1, a, 1, 2) === 'none'), [-1, 1]);
  assert.equal(kind(2, 6, 4, 1, 3, 2), 'inf');
  assert.equal(kind(3, -2, 5, -6, 4, 1), 'none');
  assert.equal(kind(2, 1, 3, 4, 2, 6), 'inf');
  assert.equal(kind(-2, 1, 3, 4, -2, 6), 'none');
  assert.equal(kind(2, -3, 5, 4, -6, 7), 'none');
  // касание: x² + y² = 2, y = x + a — один общий корень при a = ±2
  for (const a of [-2, 2]) assert.equal(roots2(2, 2 * a, a * a - 2).length, 1);
  assert.equal(roots2(2, -8, 16 - 8).length, 1); // x² + y² = 8, x + y = 4
});

test('1.7–1.9: целые решения неравенств — перебор', () => {
  const N = (p: (x: number) => boolean) => ints(-50, 50, p);
  assert.deepEqual(N((x) => 3 * (x - 2) - 4 > 5 * x + 2).at(-1), -7);
  assert.equal(N((x) => (x - 1) / 2 - (x + 1) / 3 <= 1).at(-1), 11);
  assert.deepEqual(N((x) => -3 < 2 - 5 * x && 2 - 5 * x <= 7), [-1, 0]);
  assert.equal(N((x) => -1 <= (3 - 2 * x) / 5 && (3 - 2 * x) / 5 < 1).length, 5);
  assert.equal(N((x) => 4 * (x - 1) > 2 * x + 3)[0], 4);
  assert.equal(sum(N((x) => -2 * x < 6 && x / 2 >= -1 && x - 4 < 1)), 7);
  assert.equal(sum(N((x) => 2 * x + 5 >= 1 && 4 - x > 0)), 3);
  assert.equal(N((x) => 5 * x - 2 > 3 * x && 7 - 2 * x >= -3).length, 4);
  // метод интервалов
  assert.equal(N((x) => x * x - 5 * x + 4 <= 0).length, 4);
  assert.equal(sum(N((x) => (x + 3) * (x - 2) < 0)), -2);
  assert.equal(N((x) => x !== -2 && (x - 5) / (x + 2) < 0).length, 6);
  assert.equal(sum(N((x) => x >= -3 && x <= 6 && (x + 1) * (x - 2) * (x - 6) <= 0)), 14);
  assert.equal(N((x) => (x - 3) ** 2 * (x + 4) < 0).at(-1), -5);
  assert.equal(N((x) => x >= -3 && x <= 5 && x !== 1 && (x * x - 9) / (x - 1) >= 0).length, 7);
  assert.deepEqual(N((x) => (x - 2) ** 2 * (x + 1) <= 0).filter((x) => x > -1), [2]);
  // параметрические: x² + mx + 4 > 0 при всех x (проверка на сетке)
  const always = (f: (x: number) => number) => lin2(-20, 20, 4001).every((x) => f(x) > 0);
  assert.deepEqual(range(-6, 6).filter((m) => always((x) => x * x + m * x + 4)), [-3, -2, -1, 0, 1, 2, 3]);
  assert.equal(range(-6, 6).filter((a) => lin2(-20, 20, 4001).every((x) => x * x - a * x + 1 >= -1e-12)).length, 5);
  // модуль
  assert.equal(N((x) => Math.abs(x - 4) < 3).length, 5);
  assert.equal(sum(N((x) => Math.abs(x + 1) <= 2)), -5);
  assert.equal(N((x) => x > 0 && Math.abs(x - 6) > 8)[0], 15);
  assert.equal(N((x) => Math.abs(2 * x - 3) <= 5).length, 6);
  assert.equal(N((x) => Math.abs(x - 1) < Math.abs(x - 5)).at(-1), 2);
  assert.equal(N((x) => Math.abs(x * x - 4) < 5).length, 5);
  // иррациональные (ОДЗ — через проверку под корнем)
  const sq = (v: number) => (v >= 0 ? Math.sqrt(v) : NaN);
  assert.equal(N((x) => sq(x + 4) <= 3).length, 10);
  assert.equal(N((x) => sq(2 * x - 1) > 3)[0], 6);
  assert.equal(N((x) => sq(x - 2) < 4 - x).at(-1), 2);
  assert.equal(N((x) => sq(x + 1) > sq(5 - x)).length, 3);
  assert.equal(N((x) => (x - 3) * sq(x - 1) <= 0).length, 3);
  assert.equal(N((x) => sq(6 - x) > x).at(-1), 1);
  // корни уравнений с модулем и корнями — перебор по сетке с шагом 1/2
  const zeros = (f: (x: number) => number) => lin2(-20, 20, 81).filter((x) => near(f(x), 0, 1e-9));
  assert.deepEqual(zeros((x) => Math.abs(x - 1) + Math.abs(x + 2) - 5), [-3, 2]);
  assert.deepEqual(zeros((x) => Math.abs(x - 2) - (3 * x - 10)), [4]);
  assert.deepEqual(zeros((x) => Math.abs(x) + Math.abs(x - 4) - 6), [-1, 5]);
  assert.equal(zeros((x) => x * x - 5 * Math.abs(x) + 6).reduce((p, x) => p * x, 1), 36);
  assert.deepEqual(zeros((x) => sq(x + 2) - x), [2]);
  assert.deepEqual(zeros((x) => sq(x + 7) - (x + 1)), [2]);
  assert.deepEqual(zeros((x) => sq(x + 5) - sq(x) - 1), [4]);
  assert.deepEqual(zeros((x) => sq(x - 2) * (x - 5)), [2, 5]);
});

test('1.7.5: наименьшие значения и неравенство о средних — на сетке', () => {
  const g = lin2(-10, 10, 2001);
  const min = (f: (x: number) => number, xs = g) => Math.min(...xs.map(f));
  assert.ok(near(min((x) => x * x + 4 * x + 7), 3));
  assert.ok(near(min((x) => x + 16 / x, lin2(0.1, 20, 1991)), 8, 1e-6));
  assert.ok(near(-min((x) => -(6 * x - x * x)), 9));
  assert.ok(near(g.flatMap((a) => lin2(-5, 5, 101).map((b) => a * a - 4 * a * b + 5 * b * b + 2 * b + 3)).reduce((m, v) => Math.min(m, v), Infinity), 2, 1e-6));
  for (const a of pos) for (const b of pos) assert.ok((a + b) / 2 >= Math.sqrt(a * b) - 1e-12, 'AM ≥ GM');
  assert.ok(Math.sqrt(5) + Math.sqrt(7) < 2 * Math.sqrt(6) && Math.sqrt(10) + Math.sqrt(12) < 2 * Math.sqrt(11));
  for (let n = 2; n < 500; n++) assert.ok(Math.sqrt(n - 1) + Math.sqrt(n + 1) < 2 * Math.sqrt(n));
});

test('1.10: прогрессии — формулы сравнены с прямым суммированием', () => {
  for (let a1 = -5; a1 <= 5; a1++) for (let d = -3; d <= 3; d++) {
    const seq = range(1, 30).map((n) => a1 + (n - 1) * d);
    for (let n = 1; n <= 30; n++) {
      const S = sum(seq.slice(0, n));
      assert.equal(S, ((a1 + seq[n - 1]) * n) / 2);
      assert.equal(S, ((2 * a1 + (n - 1) * d) * n) / 2);
    }
  }
  for (const b1 of [1, 2, -3, 0.5]) for (const q of [2, 3, -2, 0.5, -1 / 3]) {
    const seq = range(1, 15).map((n) => b1 * q ** (n - 1));
    for (let n = 1; n <= 15; n++) assert.ok(near(sum(seq.slice(0, n)), (b1 * (q ** n - 1)) / (q - 1), 1e-9));
    for (let n = 2; n < 15; n++) assert.ok(near(seq[n - 1] ** 2, seq[n - 2] * seq[n], 1e-9));
    if (Math.abs(q) < 1) assert.ok(near(sum(range(1, 200).map((n) => b1 * q ** (n - 1))), b1 / (1 - q), 1e-9));
  }
  assert.equal(sum(ints(10, 99, (x) => x % 7 === 0)), 728);
  assert.equal(sum(range(1, 50)), 1275);
  assert.equal(range(0, 40).map((k) => 2 + 3 * k).filter((x) => x <= 98).length, 33);
  const S = (n: number) => n * n + 2 * n; assert.equal(S(5) - S(4), 11);
  assert.ok(near(sum(range(1, 200).map((n) => 9 * (-1 / 3) ** (n - 1))), 6.75));
  assert.ok(near(sum(range(1, 100).map((n) => 12 * (1 / 3) ** (n - 1))), 18));
});

test('1.11: текстовые задачи — ответы подставлены в условия и найдены перебором', () => {
  assert.deepEqual(range(10, 99).filter((n) => Math.floor(n / 10) + (n % 10) === 11 && (n % 10) * 10 + Math.floor(n / 10) - n === 27), [47]);
  assert.deepEqual(range(10, 99).filter((n) => n === 4 * (Math.floor(n / 10) + (n % 10)) && Math.floor(n / 10) + (n % 10) === 9), [36]);
  assert.deepEqual(range(1, 1000).filter((x) => 10 * x + 5 - x === 293), [32]);
  assert.deepEqual(range(1, 100).filter((n) => n * (n + 1) === 156), [12]);
  assert.ok(near(800 * 1.15 * 0.8, 736) && near(1.2 ** 2, 1.44) && near(5000 * 1.1 ** 2, 6050) && near((22 * 0.1) / 0.88, 2.5));
  assert.equal(360 / (70 + 50), 3);
  assert.equal(36 / 18 + 36 / 12, 5);
  assert.equal((2 * 60 * 40) / 100, 48);
  assert.deepEqual(range(1, 20).filter((v) => near(6 / v - 6 / (v + 1), 0.5)), [3]);
  assert.ok(near(1 / (1 / 6 + 1 / 3), 2) && near(1 / (1 / 12 - 1 / 20), 30) && near(1 / (1 / 4 - 1 / 6), 12) && near(1 / (1 / 3 - 1 / 5), 7.5));
  assert.ok(near(2 + (1 - 2 / 8) / (1 / 8 + 1 / 4), 4));
  assert.ok(near((0.1 * 200 + 0.2 * 300) / 500, 0.16) && near(45 / (300 + 150), 0.1));
  assert.ok(near(0.3 * 10 + 0.5 * 30, 0.45 * 40) && near((0.1 * 2 + 0.25 * 1) / 3, 0.15) && near((2.7 + 2.25) / (6 + 2.25), 0.6));
});

test('1.12: функции — вершины, прямые, композиции и обратные функции', () => {
  const g = lin2(-10, 10, 20001);
  const argmin = (f: (x: number) => number) => g.reduce((b, x) => (f(x) < f(b) ? x : b), g[0]);
  assert.ok(near(argmin((x) => 2 * x * x - 8 * x + 5), 2, 1e-6) && near(argmin((x) => 3 * x * x - 12 * x + 1), 2, 1e-6));
  assert.ok(near(-Math.min(...[-1, 0, 1, 2, 3, 4].map((x) => -(-(x * x) + 4 * x + 5))), 9));
  for (const x of g.filter((_, i) => i % 1000 === 0)) {
    assert.ok(near(x * x + 6 * x + 4, (x + 3) ** 2 - 5));
    assert.ok(near(3 * ((x + 6) / 3) - 6, x), 'f(f⁻¹(x)) = x');
    if (Math.abs(x - 2) > 1e-9 && Math.abs(x - 3) > 1e-9) { const y = (2 * x + 1) / (x - 3); if (Math.abs(y - 2) > 1e-9) assert.ok(near((3 * y + 1) / (y - 2), x, 1e-7), 'дробно-линейная обратная'); }
  }
  assert.ok(near(Math.abs(3 * 3 + 4 * 4 - 5) / 5, 4) && near(10 / 5, 2));
  // x² − 2|x| = a: число решений по сетке значений a
  const cnt = (a: number) => { const t = roots2(1, -2, -a).filter((r) => r >= 0); return t.reduce((s, r) => s + (near(r, 0) ? 1 : 2), 0); };
  assert.equal(cnt(-1), 2); assert.equal(cnt(-0.5), 4); assert.equal(cnt(0), 3); assert.equal(cnt(3), 2); assert.equal(cnt(-2), 0);
  assert.equal(zeros2((x) => x * x - Math.abs(x)).length, 3);
});
const zeros2 = (f: (x: number) => number) => lin2(-20, 20, 81).filter((x) => near(f(x), 0, 1e-9));

test('1.13–1.14: показательные и логарифмические уравнения и неравенства — перебор', () => {
  const N = (p: (x: number) => boolean) => ints(-50, 200, p);
  const lg = Math.log10, log = (a: number, x: number) => Math.log(x) / Math.log(a);
  assert.deepEqual(zeros2((x) => 9 ** x - 4 * 3 ** x + 3), [0, 1]);
  assert.deepEqual(zeros2((x) => 3 ** (x + 2) - 3 ** x - 72), [2]);
  assert.deepEqual(zeros2((x) => 4 ** x - 6 * 2 ** x + 8), [1, 2]);
  assert.deepEqual(zeros2((x) => 2 ** (x * x - x) - 4), [-1, 2]);
  assert.deepEqual(zeros2((x) => 9 ** x - 3 ** x - 6), [1]);
  assert.deepEqual(zeros2((x) => 4 ** x - 8), [1.5]);
  assert.equal(N((x) => 3 ** x > 81)[0], 5);
  assert.equal(N((x) => 0.5 ** x >= 1 / 16).at(-1), 4);
  assert.equal(N((x) => 1 <= 2 ** x && 2 ** x <= 32).length, 6);
  assert.equal(N((x) => 9 ** x - 10 * 3 ** x + 9 <= 0).length, 3);
  assert.equal(N((x) => 0.5 ** (x - 3) > 4).at(-1), 0);
  // логарифмы: допустимость аргумента проверяется явно
  const L = (a: number, x: number) => (x > 0 ? log(a, x) : NaN);
  assert.ok(near(log(6, 4) + log(6, 9), 2) && near(log(3, 8) / log(3, 2), 3) && near(5 ** log(25, 9), 3));
  assert.ok(near(lg(25) + lg(4), 2) && near(log(2, 7) * log(7, 8), 3) && near(9 ** log(3, 5), 25) && near(log(Math.SQRT2, 8), 6));
  assert.deepEqual(N((x) => near(L(3, x) + L(3, x - 8), 2)), [9]);
  assert.deepEqual(N((x) => near(lg(x) ** 2 - 3 * lg(x) + 2, 0) && x > 0), [10, 100]);
  assert.deepEqual(N((x) => near(L(10, x + 2) + L(10, x - 1), 1)), [3]);
  assert.deepEqual(N((x) => near(L(2, x * x - 1), 3)), [-3, 3]);
  assert.deepEqual(N((x) => x > 0 && x !== 1 && near(L(x, 16), 2)), [4]);
  assert.equal(N((x) => L(3, x + 1) <= 2 + 1e-12).length, 9);
  assert.equal(N((x) => L(2, x) > 3)[0], 9);
  assert.equal(N((x) => L(0.5, x - 1) > -2).at(-1), 4);
  assert.deepEqual(N((x) => L(5, x * x - 4) < L(5, 3 * x)), [3]);
  assert.equal(N((x) => x > 0 && lg(x) ** 2 - lg(x) - 2 <= 1e-12).length, 100);
  assert.equal(sum(N((x) => L(2, x) + L(2, x - 2) <= 3 + 1e-12)), 7);
  assert.equal(N((x) => x * x < 9).length, 5);
});

test('1.15: тригонометрические тождества и формулы — на сетке углов', () => {
  const { sin, cos, tan, PI, sqrt, asin, acos, atan } = Math;
  const A = lin2(-7, 7, 141), B = lin2(-3.1, 3.1, 31);
  for (const a of A) {
    assert.ok(near(sin(a) ** 2 + cos(a) ** 2, 1));
    if (Math.abs(cos(a)) > 1e-3) assert.ok(near(1 + tan(a) ** 2, 1 / cos(a) ** 2, 1e-7));
    assert.ok(near(sin(PI - a), sin(a)) && near(cos(PI + a), -cos(a)) && near(sin(PI / 2 + a), cos(a)) && near(cos(1.5 * PI + a), sin(a)) && near(sin(1.5 * PI - a), -cos(a)));
    assert.ok(near(sin(2 * a), 2 * sin(a) * cos(a)) && near(cos(2 * a), 1 - 2 * sin(a) ** 2) && near(cos(2 * a), 2 * cos(a) ** 2 - 1));
    assert.ok(near(sin(3 * a), 3 * sin(a) - 4 * sin(a) ** 3) && near(cos(3 * a), 4 * cos(a) ** 3 - 3 * cos(a)));
    assert.ok(near(sin(a / 2) ** 2, (1 - cos(a)) / 2) && near(cos(a / 2) ** 2, (1 + cos(a)) / 2));
    if (Math.abs(cos(a / 2)) > 1e-3) { const t = tan(a / 2); assert.ok(near(sin(a), (2 * t) / (1 + t * t), 1e-7) && near(cos(a), (1 - t * t) / (1 + t * t), 1e-7)); }
    for (const b of B) {
      assert.ok(near(sin(a + b), sin(a) * cos(b) + cos(a) * sin(b)) && near(cos(a - b), cos(a) * cos(b) + sin(a) * sin(b)));
      assert.ok(near(sin(a) + sin(b), 2 * sin((a + b) / 2) * cos((a - b) / 2)) && near(cos(a) - cos(b), -2 * sin((a + b) / 2) * sin((a - b) / 2)));
      assert.ok(near(sin(a) * sin(b), (cos(a - b) - cos(a + b)) / 2) && near(sin(a) * cos(b), (sin(a + b) + sin(a - b)) / 2));
      assert.ok(near(3 * sin(a) + 4 * cos(a), 5 * sin(a + atan(4 / 3))));
    }
  }
  for (const v of lin2(-1, 1, 41)) {
    assert.ok(near(asin(-v), -asin(v)) && near(acos(-v), PI - acos(v)) && near(asin(v) + acos(v), PI / 2) && near(cos(asin(v)), sqrt(1 - v * v)));
  }
  // ответы примеров и задач
  const d = (x: number) => (x * PI) / 180;
  assert.ok(near(sin(d(75)), (sqrt(6) + sqrt(2)) / 4) && near(tan(atan(2) + atan(3)), -1) && near(sin(asin(0.6) + acos(5 / 13)), 63 / 65));
  assert.ok(near(8 * cos(d(20)) * cos(d(40)) * cos(d(80)), 1) && near(sin(d(75)) * sin(d(15)), 0.25) && near(tan(d(22.5)), sqrt(2) - 1));
  assert.ok(near(Math.min(...lin2(0, 2 * PI, 3601).map((x) => sin(x) ** 4 + cos(x) ** 4)), 0.5, 1e-6));
});

test('1.15.10–1.15.11: число корней и решения неравенств — перебор по градусам', () => {
  const deg = (lo: number, hi: number) => range(lo * 10, hi * 10).map((k) => k / 10);
  const s = (x: number) => Math.sin((x * Math.PI) / 180), c = (x: number) => Math.cos((x * Math.PI) / 180), t = (x: number) => Math.tan((x * Math.PI) / 180);
  const roots = (f: (x: number) => number, lo: number, hi: number) => deg(lo, hi).filter((x) => near(f(x), 0, 1e-9));
  assert.deepEqual(roots((x) => s(x) - 0.5, 0, 360), [30, 150]);
  assert.deepEqual(roots((x) => 2 * s(x) ** 2 - s(x) - 1, 0, 359.9), [90, 210, 330]);
  assert.deepEqual(roots((x) => s(2 * x) - c(x), 0, 180), [30, 90, 150]);
  assert.deepEqual(roots((x) => s(x) + c(x) - 1, 0.1, 720), [90, 360, 450, 720]);
  assert.equal(sum(roots((x) => t(x) - 1, 0, 360)), 270);
  assert.equal(roots((x) => c(x) + 0.5, 0.1, 360)[0], 120);
  // неравенства: длины множеств решений (шаг 0,1°)
  const len = (p: (x: number) => boolean, lo: number, hi: number) => deg(lo, hi).filter(p).length / 10;
  assert.ok(Math.abs(len((x) => s(x) >= 0.5 - 1e-12, 0, 360) - 120) <= 0.2);
  assert.ok(Math.abs(len((x) => c(x) > 1e-12, 0, 360) - 180) <= 0.2);
  assert.ok(Math.abs(len((x) => t(x) > 1, 0.1, 89.9) - 45) <= 0.2);
  assert.equal(range(1, 10).find((x) => Math.sin(x) < 0), 4);
  assert.equal(range(0, 6).filter((x) => Math.cos(x) > 0).length, 4);
});

test('1.16–1.17: производные и интегралы — численная проверка ответов', () => {
  const { sin, cos, exp, log, sqrt, PI, E } = Math;
  const d = (f: (x: number) => number, x: number, h = 1e-5) => (f(x + h) - f(x - h)) / (2 * h);
  const close = (a: number, b: number, eps = 1e-5) => Math.abs(a - b) <= eps * Math.max(1, Math.abs(b));
  const D: [(x: number) => number, number, number][] = [
    [(x) => x ** 3 - 4 * x * x + 5, 2, -4], [(x) => 2 * sqrt(x) + 3 / x, 1, -2], [(x) => 3 * sin(x) - 2 * cos(x) + exp(x), 0, 4],
    [(x) => x ** 4 - 2 * x, 1, 2], [(x) => 5 * x ** 3 + x, -1, 16], [sqrt, 4, 0.25], [(x) => log(x) + x * x, 1, 3], [(x) => exp(x) - 3 * x, 0, -2],
    [(x) => (x + 1) * (x * x - 3), 1, 2], [(x) => x * exp(x), 0, 1], [(x) => x * log(x), 1, 1], [(x) => (2 * x - 1) * (x + 3), 0, 5],
    [(x) => x * x * exp(x), 1, 3 * E], [(x) => x * sin(x), PI / 2, 1], [(x) => x * sqrt(x), 4, 3], [(x) => (x * x + 1) * (x - 1), 2, 9],
    [(x) => (x + 1) / (x - 1), 2, -2], [(x) => (x * x) / (x + 1), 1, 0.75], [(x) => 1 / (x * x + 1), 1, -0.5], [(x) => (2 * x + 3) / x, 1, -3],
    [(x) => x / (x + 2), 0, 0.5], [(x) => sin(x) / x, PI, -1 / PI], [(x) => exp(x) / x, 1, 0], [(x) => (x - 1) / (x + 1), 0, 2],
    [(x) => (3 * x - 1) ** 4, 1, 96], [(x) => exp(2 * x), 0, 2], [(x) => log(x * x + 1), 1, 1], [(x) => cos(2 * x), PI / 4, -2],
    [(x) => sqrt(2 * x + 1), 4, 1 / 3], [(x) => sin(x) ** 2, PI / 4, 1], [(x) => sqrt(x * x + 9), 4, 0.8],
    [(x) => x ** 3 - 2 * x, 1, 1], [(x) => sqrt(3) * log(x), 1, sqrt(3)], [log, 0.5, 2],
  ];
  for (const [f, x, v] of D) assert.ok(close(d(f, x), v), `f′(${x}) = ${d(f, x)} ≠ ${v}`);
  // экстремумы и наибольшие/наименьшие значения — по сетке
  const g = (a: number, b: number) => lin2(a, b, 20001);
  const mx = (f: (x: number) => number, a: number, b: number) => g(a, b).reduce((m, x) => Math.max(m, f(x)), -Infinity);
  const mn = (f: (x: number) => number, a: number, b: number) => g(a, b).reduce((m, x) => Math.min(m, f(x)), Infinity);
  assert.ok(close(mx((x) => x ** 3 - 3 * x, 0, 2), 2) && close(mn((x) => x ** 3 - 3 * x, 0, 2), -2));
  assert.ok(close(mx((x) => 2 * x ** 3 - 3 * x * x - 12 * x + 1, -2, 3), 8) && close(mn((x) => 2 * x ** 3 - 3 * x * x - 12 * x + 1, -2, 3), -19));
  assert.ok(close(mx((x) => x ** 4 - 2 * x * x, -2, 1), 8) && close(mn((x) => exp(x) - x, -1, 1), 1) && close(mx((x) => sin(x) + cos(x), 0, PI / 2), sqrt(2), 1e-6));
  assert.ok(close(mn((x) => x + 4 / x, 0.1, 10), 4, 1e-6) && close(mx((x) => x * exp(-x), 0, 5), 1 / E, 1e-6));
  // касательные: точка касания на прямой и наклон
  const tan = (f: (x: number) => number, x0: number) => ({ k: d(f, x0), b: f(x0) - d(f, x0) * x0 });
  const T = [tan((x) => x * x + 3 * x, 1), tan((x) => x ** 3 - x, 2), tan(sqrt, 4), tan((x) => 1 / x, 1)];
  assert.ok(close(T[0].b, -1) && close(T[1].b, -16) && close(T[2].b, 1) && close(T[3].k, -1) && close(T[3].b, 2));
  // интегралы — методом трапеций
  const I = (f: (x: number) => number, a: number, b: number, n = 20000) => { const h = (b - a) / n; let s = (f(a) + f(b)) / 2; for (let i = 1; i < n; i++) s += f(a + i * h); return s * h; };
  const J: [(x: number) => number, number, number, number][] = [
    [(x) => x * x, 0, 2, 8 / 3], [sin, 0, PI, 2], [(x) => 1 / x, 1, E, 1], [(x) => 3 * x * x + 2 * x, 0, 1, 2], [sqrt, 1, 4, 14 / 3],
    [cos, 0, PI / 2, 1], [exp, 0, 1, E - 1], [(x) => x ** 3, -1, 1, 0], [(x) => 2 * x - 1, 0, 2, 2], [(x) => x * x, 0, 3, 9],
    [(x) => x - x * x, 0, 1, 1 / 6], [(x) => x * x + 1, 0, 3, 12], [(x) => 4 - x * x, -2, 2, 32 / 3], [(x) => 2 * x - x * x, 0, 2, 4 / 3],
    [(x) => 1 / x, 1, E * E, 2], [sqrt, 0, 4, 16 / 3], [exp, 0, log(3), 2],
  ];
  for (const [f, a, b, v] of J) assert.ok(Math.abs(I(f, a, b) - v) < 1e-4, `∫ = ${I(f, a, b)} ≠ ${v}`);
  // первообразные: F′ = f и условие в точке
  const F: [(x: number) => number, (x: number) => number, number, number][] = [
    [(x) => x ** 3 + 2, (x) => 3 * x * x, 2, 10], [(x) => exp(x) + 2, exp, 1, E + 2], [(x) => x ** 4 + x - 2, (x) => 4 * x ** 3 + 1, 2, 16],
    [(x) => 1 - cos(x), sin, PI, 2], [(x) => (2 * x + 1) ** 3 / 6, (x) => (2 * x + 1) ** 2, 1, 4.5], [(x) => 2 * sqrt(x), (x) => 1 / sqrt(x), 4, 4],
  ];
  for (const [Fn, f, x, v] of F) { assert.ok(close(d(Fn, x * 0.7 + 0.3), f(x * 0.7 + 0.3), 1e-5)); assert.ok(close(Fn(x), v)); }
  // механический смысл
  assert.ok(close(d((t) => t ** 3 - 2 * t * t + 3, 2), 4) && close(d((t) => d((s) => s ** 3 - 2 * s * s + 3, t, 1e-4), 2, 1e-3), 8, 1e-3));
  assert.ok(close(d((t) => t ** 3 - 6 * t * t + 10 * t, 2), -2));
});

// ───────────── 3. Геометрия: формулы теории на случайных фигурах ─────────────

type P = [number, number];
const rnd = (seed: number) => () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
const dist = (a: P, b: P) => Math.hypot(a[0] - b[0], a[1] - b[1]);
const shoelace = (ps: P[]) => Math.abs(ps.reduce((s, p, i) => { const q = ps[(i + 1) % ps.length]; return s + p[0] * q[1] - q[0] * p[1]; }, 0)) / 2;
const angAt = (a: P, b: P, c: P) => { // угол ABC
  const u = [a[0] - b[0], a[1] - b[1]], v = [c[0] - b[0], c[1] - b[1]];
  return Math.acos((u[0] * v[0] + u[1] * v[1]) / (Math.hypot(u[0], u[1]) * Math.hypot(v[0], v[1])));
};
const close = (x: number, y: number, msg = '') => assert.ok(Math.abs(x - y) < 1e-6 * Math.max(1, Math.abs(y)), `${msg}: ${x} ≠ ${y}`);

test('3.1–3.3: треугольник — сумма углов, Герон, ½ab·sinC, теоремы синусов и косинусов, медиана, r = S/p, R = abc/4S', () => {
  const r = rnd(7);
  for (let k = 0; k < 300; k++) {
    const A: P = [r() * 20, r() * 20], B: P = [r() * 20, r() * 20], C: P = [r() * 20, r() * 20];
    const S = shoelace([A, B, C]);
    if (S < 1) continue;
    const a = dist(B, C), b = dist(A, C), c = dist(A, B);
    const al = angAt(B, A, C), be = angAt(A, B, C), ga = angAt(A, C, B);
    close(al + be + ga, Math.PI, 'сумма углов');
    const p = (a + b + c) / 2;
    close(Math.sqrt(p * (p - a) * (p - b) * (p - c)), S, 'Герон');
    close(0.5 * a * b * Math.sin(ga), S, '½ab·sinC');
    close(c * c, a * a + b * b - 2 * a * b * Math.cos(ga), 'теорема косинусов');
    const R = (a * b * c) / (4 * S);
    close(a / Math.sin(al), 2 * R, 'теорема синусов');
    // центр описанной окружности равноудалён от вершин
    const d = 2 * (A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1]));
    const sq = (P0: P) => P0[0] ** 2 + P0[1] ** 2;
    const O: P = [(sq(A) * (B[1] - C[1]) + sq(B) * (C[1] - A[1]) + sq(C) * (A[1] - B[1])) / d, (sq(A) * (C[0] - B[0]) + sq(B) * (A[0] - C[0]) + sq(C) * (B[0] - A[0])) / d];
    close(dist(O, A), R, 'R = abc/4S');
    // центр вписанной окружности: расстояние до стороны = S/p
    const I: P = [(a * A[0] + b * B[0] + c * C[0]) / (2 * p), (a * A[1] + b * B[1] + c * C[1]) / (2 * p)];
    close((2 * shoelace([I, B, C])) / a, S / p, 'r = S/p');
    // медиана к стороне c
    const M: P = [(A[0] + B[0]) / 2, (A[1] + B[1]) / 2];
    close(dist(C, M), 0.5 * Math.sqrt(2 * a * a + 2 * b * b - c * c), 'медиана');
    // биссектриса делит сторону в отношении прилежащих сторон
    const L: P = [(b * B[0] + a * A[0]) / (a + b), (b * B[1] + a * A[1]) / (a + b)];
    close(angAt(A, C, L), angAt(L, C, B), 'биссектриса');
  }
});

test('3.3.6–3.5: многоугольники и четырёхугольники — сумма углов, диагонали, правильные многоугольники, параллелограмм, ½d₁d₂·sinφ', () => {
  for (let n = 3; n <= 20; n++) {
    let diag = 0;
    for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) if (j - i !== 1 && !(i === 0 && j === n - 1)) diag++;
    assert.equal(diag, (n * (n - 3)) / 2, `диагоналей у ${n}-угольника`);
    const ps: P[] = Array.from({ length: n }, (_, i) => [Math.cos((2 * Math.PI * i) / n), Math.sin((2 * Math.PI * i) / n)]);
    let angSum = 0;
    for (let i = 0; i < n; i++) angSum += angAt(ps[(i + n - 1) % n], ps[i], ps[(i + 1) % n]);
    close(angSum, (n - 2) * Math.PI, 'сумма углов');
    const a = dist(ps[0], ps[1]);
    close(shoelace(ps), (n * a * a) / (4 * Math.tan(Math.PI / n)), 'площадь правильного многоугольника');
    close(a / (2 * Math.tan(Math.PI / n)), Math.cos(Math.PI / n), 'радиус вписанной окружности');
  }
  const r = rnd(11);
  for (let k = 0; k < 200; k++) {
    const A: P = [r() * 10, r() * 10], B: P = [r() * 10, r() * 10], D: P = [r() * 10, r() * 10];
    const C: P = [B[0] + D[0] - A[0], B[1] + D[1] - A[1]];
    const d1 = dist(A, C), d2 = dist(B, D);
    close(d1 * d1 + d2 * d2, 2 * (dist(A, B) ** 2 + dist(A, D) ** 2), 'диагонали параллелограмма');
    // выпуклый четырёхугольник: S = ½ d₁ d₂ sin φ
    const Q: P[] = [[0, 0], [4 + r() * 6, -r() * 3], [5 + r() * 5, 4 + r() * 5], [-r() * 3, 3 + r() * 6]];
    const u = [Q[2][0] - Q[0][0], Q[2][1] - Q[0][1]], v = [Q[3][0] - Q[1][0], Q[3][1] - Q[1][1]];
    close(shoelace(Q), 0.5 * Math.abs(u[0] * v[1] - u[1] * v[0]), '½d₁d₂ sinφ');
  }
});

test('3.6–3.7: окружность — вписанный угол, хорды, касательная и секущая, вписанный четырёхугольник', () => {
  const r = rnd(13);
  const onC = (t: number): P => [5 * Math.cos(t), 5 * Math.sin(t)];
  for (let k = 0; k < 300; k++) {
    const t = Array.from({ length: 4 }, () => r() * 2 * Math.PI).sort((x, y) => x - y);
    const [A, B, C, D] = t.map(onC);
    // вписанный угол ADB... угол ACB опирается на дугу AB, не содержащую C → половина центрального
    const central = t[1] - t[0];
    close(angAt(A, C, B), central / 2, 'вписанный угол');
    close(angAt(A, D, B), angAt(A, C, B), 'углы, опирающиеся на одну дугу');
    // вписанный четырёхугольник ABCD
    close(angAt(D, A, B) + angAt(B, C, D), Math.PI, 'сумма противоположных углов');
    close(dist(A, C) * dist(B, D), dist(A, B) * dist(C, D) + dist(B, C) * dist(A, D), 'Птолемей');
    // пересекающиеся хорды AC и BD
    const den = (A[0] - C[0]) * (B[1] - D[1]) - (A[1] - C[1]) * (B[0] - D[0]);
    const s = ((A[0] - B[0]) * (B[1] - D[1]) - (A[1] - B[1]) * (B[0] - D[0])) / den;
    const X: P = [A[0] + s * (C[0] - A[0]), A[1] + s * (C[1] - A[1])];
    close(dist(A, X) * dist(X, C), dist(B, X) * dist(X, D), 'хорды');
    // касательная из внешней точки: t² = (R… степень точки)
    const M: P = [8 + r() * 10, r() * 4 - 2];
    const tangent2 = M[0] ** 2 + M[1] ** 2 - 25;
    const dir = [A[0] - M[0], A[1] - M[1]]; // секущая через A
    const qa = dir[0] ** 2 + dir[1] ** 2, qb = 2 * (M[0] * dir[0] + M[1] * dir[1]);
    // точки пересечения M + t·dir с окружностью: qa·t² + qb·t + tangent2 = 0 — решаем формулой корней
    const disc = qb * qb - 4 * qa * tangent2;
    assert.ok(disc >= -1e-9);
    const t1 = (-qb - Math.sqrt(Math.max(disc, 0))) / (2 * qa), t2 = (-qb + Math.sqrt(Math.max(disc, 0))) / (2 * qa);
    assert.ok(Math.abs(t1 - 1) < 1e-6 || Math.abs(t2 - 1) < 1e-6, 'секущая проходит через A');
    const P1: P = [M[0] + t1 * dir[0], M[1] + t1 * dir[1]], P2: P = [M[0] + t2 * dir[0], M[1] + t2 * dir[1]];
    // касательная: точка касания T, где OT ⟂ MT
    const dM = Math.hypot(M[0], M[1]), th = Math.atan2(M[1], M[0]) + Math.acos(5 / dM);
    const T = onC(th);
    close(T[0] * (M[0] - T[0]) + T[1] * (M[1] - T[1]), 0, 'радиус ⟂ касательной');
    close(dist(M, T) ** 2, dist(M, P1) * dist(M, P2), 'касательная² = секущая·внешняя часть');
  }
});

test('3.8–3.9: координаты и векторы — расстояние, середина, скалярное произведение через угол, коллинеарность', () => {
  const r = rnd(17);
  for (let k = 0; k < 300; k++) {
    const a: P = [r() * 20 - 10, r() * 20 - 10], b: P = [r() * 20 - 10, r() * 20 - 10];
    const la = Math.hypot(...a), lb = Math.hypot(...b);
    const phi = Math.abs(Math.atan2(a[1], a[0]) - Math.atan2(b[1], b[0]));
    close(a[0] * b[0] + a[1] * b[1], la * lb * Math.cos(phi), 'a·b = |a||b|cos φ');
    const M: P = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
    close(dist(a, M), dist(M, b), 'середина');
    close(dist(a, M) * 2, dist(a, b), 'середина');
    const kk = r() * 6 - 3;
    close(a[0] * (kk * a[1]) - a[1] * (kk * a[0]), 0, 'коллинеарность');
    // правило параллелограмма: |a+b|² + |a−b|² = 2(|a|² + |b|²)
    close(Math.hypot(a[0] + b[0], a[1] + b[1]) ** 2 + Math.hypot(a[0] - b[0], a[1] - b[1]) ** 2, 2 * (la * la + lb * lb), 'параллелограмм');
  }
  // окружность x² + y² − 6x + 8y = 0: центр (3; −4), R = 5 — точки на ней
  for (let t = 0; t < 2 * Math.PI; t += 0.3) { const x = 3 + 5 * Math.cos(t), y = -4 + 5 * Math.sin(t); close(x * x + y * y - 6 * x + 8 * y, 0, 'окружность'); }
});

test('3.10–3.12: объёмы тел — численное интегрирование по сечениям; наклонная и проекция', () => {
  const vol = (area: (z: number) => number, h: number, n = 20000) => { let s = 0; for (let i = 0; i < n; i++) s += area(((i + 0.5) * h) / n); return (s * h) / n; };
  const near1 = (x: number, y: number, msg: string) => assert.ok(Math.abs(x - y) < 1e-4 * y, `${msg}: ${x} ≠ ${y}`);
  for (const [R, h] of [[3, 5], [2, 7], [6, 8], [5, 12]]) {
    near1(vol(() => Math.PI * R * R, h), Math.PI * R * R * h, 'цилиндр');
    near1(vol((z) => Math.PI * (R * (1 - z / h)) ** 2, h), (Math.PI * R * R * h) / 3, 'конус');
    near1(vol((z) => (2 * R * (1 - z / h)) ** 2, h), (4 * R * R * h) / 3, 'пирамида ⅓Sh');
    near1(vol((z) => Math.PI * (R * R - (z - R) ** 2), 2 * R), (4 / 3) * Math.PI * R ** 3, 'шар');
    // боковая поверхность конуса: πRl = площадь сектора развёртки
    const l = Math.hypot(R, h), alpha = (2 * Math.PI * R) / l;
    close(0.5 * l * l * alpha, Math.PI * R * l, 'развёртка конуса');
    // площадь сферы — производная объёма по радиусу
    close(((4 / 3) * Math.PI * ((R + 1e-6) ** 3 - (R - 1e-6) ** 3)) / 2e-6, 4 * Math.PI * R * R, 'S = dV/dR');
  }
  // перпендикуляр, наклонная, проекция в координатах: точка (0,0,d), плоскость z = 0
  for (const [d, p] of [[6, 8], [12, 5], [8, 15]]) {
    const l = Math.hypot(d, p);
    close(Math.asin(d / l), Math.atan2(d, p), 'угол наклонной');
  }
});

test('3.13: комбинации тел — вписанные и описанные шары проверены по координатам', () => {
  // правильная четырёхугольная пирамида: r = 3V/S совпадает с расстоянием от центра шара до боковой грани
  for (const [half, h] of [[3, 4], [6, 8], [4, 3], [5, 12]]) {
    const a = 2 * half, m = Math.hypot(h, half);
    const V = (a * a * h) / 3, S = 2 * a * m + a * a;
    const r = (3 * V) / S;
    // боковая грань — плоскость через (half,±half,0) и (0,0,h): h·x + half·z − half·h = 0
    const distToFace = Math.abs(h * 0 + half * r - half * h) / Math.hypot(h, half);
    close(distToFace, r, 'r = 3V/S касается грани');
    // описанный шар: R = (h² + ρ²)/2h равноудалён от вершины и вершин основания
    const rho = half * Math.SQRT2, R = (h * h + rho * rho) / (2 * h);
    close(Math.hypot(rho, R - h), R, 'описанный шар пирамиды');
  }
  // конус: r = Rh/(R+l) — центр (0, r) на оси касается образующей; Rш = l²/2h
  for (const [R, h] of [[3, 4], [6, 8], [5, 12], [9, 12]]) {
    const l = Math.hypot(R, h);
    const r = (R * h) / (R + l);
    // образующая: прямая через (R,0) и (0,h): h·x + R·y − R·h = 0
    close(Math.abs(R * r - R * h) / Math.hypot(h, R), r, 'вписанный шар конуса');
    const Rs = (l * l) / (2 * h);
    close(Math.hypot(R, h - Rs), Rs, 'описанный шар конуса');
  }
  // Архимед: конус : шар : цилиндр = 1 : 2 : 3
  for (const R of [1, 2, 3.5]) {
    const cyl = Math.PI * R * R * 2 * R, ball = (4 / 3) * Math.PI * R ** 3, cone = cyl / 3;
    close(ball / cone, 2, 'шар : конус');
    close(cyl / cone, 3, 'цилиндр : конус');
    close(4 * Math.PI * R * R, 2 * Math.PI * R * 2 * R, 'сфера = боковая поверхность цилиндра');
  }
  // куб: вписанный a/2, описанный a√3/2; параллелепипед — половина диагонали
  for (const [x, y, z] of [[2, 3, 6], [1, 4, 8], [4, 4, 4]]) {
    const R = Math.hypot(x, y, z) / 2;
    for (const sx of [0, x]) for (const sy of [0, y]) for (const sz of [0, z]) close(Math.hypot(sx - x / 2, sy - y / 2, sz - z / 2), R, 'описанный шар параллелепипеда');
  }
});

test('математика: заголовки теории, формул и примеров — без TeX (отображаются как обычный текст)', () => {
  for (const x of [...pack.theory, ...pack.formulas, ...pack.examples]) assert.ok(!String((x as { title?: string }).title ?? '').includes('$'), `${x.id}: «$» в заголовке`);
});

test('математика: план курса — все пункты оглавления обеих частей книги по порядку, без пропусков', () => {
  const plan = pack.plan ?? [];
  const nums = [...pack.topics.map((t) => t.num!), ...plan.map((p) => p.num)];
  assert.equal(nums.length, 131, 'пунктов оглавления');
  assert.equal(new Set(nums).size, nums.length, 'пункты не повторяются');
  // главы 1.1–1.18 и 3.1–3.13
  assert.equal(pack.subsections.length, 31);
  assert.deepEqual(pack.subsections.slice(0, 2).map((s) => s.title), ['1.1 Натуральные и целые числа', '1.2 Дроби']);
  assert.equal(pack.subsections.at(-1)!.title, '3.13 Комбинации тел');
  // порядок: темы и пункты плана идут по возрастанию номеров внутри глав, страницы не убывают
  const key = (n: string) => n.split('.').map(Number);
  const all = [...pack.topics.map((t) => ({ num: t.num!, sub: t.subsectionId, page: t.pages[0] })), ...plan.map((p) => ({ num: p.num, sub: p.subsectionId, page: p.pages[0] }))];
  all.sort((a, b) => { const x = key(a.num), y = key(b.num); for (let i = 0; i < 3; i++) if ((x[i] ?? 0) !== (y[i] ?? 0)) return (x[i] ?? 0) - (y[i] ?? 0); return 0; });
  const pageIdx = new Map(pack.pages.map((p) => [p.ref, p.index]));
  for (let i = 1; i < all.length; i++) assert.ok(pageIdx.get(all[i].page)! >= pageIdx.get(all[i - 1].page)!, `${all[i - 1].num} → ${all[i].num}: страницы идут по порядку`);
  // тема 1.15 «Тригонометрия» начинается в части 1 и продолжается в части 2
  const trig = [...pack.topics, ...plan].filter((p) => p.num!.startsWith('1.15.'));
  assert.ok(trig.some((p) => p.pages.some((r) => Number(r.slice(1)) <= 156)) && trig.some((p) => p.pages.some((r) => Number(r.slice(1)) >= 157)));
  // пункты без новой теории помечены, а не удалены
  for (const n of ['1.12.4', '1.15.12', '1.18', '3.3.8', '3.13.5']) assert.ok(plan.find((p) => p.num === n)?.note || pack.topics.find((t) => t.num === n), n);
});

test('математика: страницы книги без изображений, две части, нумерация сквозная', () => {
  assert.equal(pack.sourceFiles.length, 2);
  assert.equal(pack.pages.length, 152 + 159);
  for (const p of pack.pages) assert.equal(p.image, '', 'страницы книги в приложение не встраиваются');
  assert.equal(pack.pages[0].ref, 'b005');
  assert.equal(pack.pages.at(-1)!.ref, 'b315');
  assert.equal(pack.pages.find((p) => p.ref === 'b157')!.file, 'book-2');
  assert.equal(pack.pages.find((p) => p.ref === 'b156')!.file, 'book-1');
});

test('математика: у каждой темы место в книге, этап, дата проверки источников; у записей — источники и ID «ma-»', () => {
  const recs = [...pack.theory, ...pack.formulas, ...pack.examples, ...pack.questions];
  for (const t of pack.topics) {
    assert.match(t.id, /^ma-/);
    assert.ok(t.book?.place && t.num && t.stage && t.sourcesChecked, t.id);
    const own = recs.filter((r) => r.topicId === t.id);
    for (const kind of ['theory', 'formulas', 'examples', 'questions'] as const) assert.ok(pack[kind].some((r) => r.topicId === t.id), `${t.id}: ${kind}`);
    for (const r of own) {
      assert.match(r.id, /^ma-/);
      assert.ok(r.web?.length, `${r.id}: дополнительные источники`);
      for (const w of r.web!) { assert.match(w.url, /^https:\/\//); assert.match(w.checked ?? '', /^\d{4}-\d{2}-\d{2}$/); }
      assert.ok(r.sources.length && r.sources.every((s) => s.page.startsWith('b')), `${r.id}: место в книге`);
      assert.equal(r.status, 'review', `${r.id}: до утверждения — на проверке`);
    }
  }
  // ID математики и физики не пересекаются (прогресс в общих таблицах сервера не смешивается)
  const phys = new Set([...physics.topics, ...physics.theory, ...physics.formulas, ...physics.examples, ...physics.questions].map((x) => x.id));
  for (const r of [...pack.topics, ...recs]) assert.ok(!phys.has(r.id), r.id);
  for (const id of phys) assert.ok(!id.startsWith('ma-'), id);
});

test('математика: задачи с пошаговым решением, примеры с методом и проверкой, формулы с обозначениями и применением', () => {
  for (const q of pack.questions) {
    assert.ok(q.generated, `${q.id}: задания составлены по материалам темы, не из книги`);
    assert.ok(q.hints.length && q.explanation, q.id);
    if (q.category === 'problem') assert.ok(q.solution?.steps?.length || q.solution?.calc, `${q.id}: пошаговое решение`);
    if (q.type === 'numeric') assert.ok(q.numeric?.check, `${q.id}: независимый пересчёт ответа`);
  }
  for (const e of pack.examples) assert.ok(e.given && e.find && e.method && e.steps.length >= 2 && e.check && e.answer, e.id);
  for (const f of pack.formulas) assert.ok(f.meaning && f.use, f.id);
  const byTopic = (id: string) => pack.examples.filter((e) => e.topicId === id).length;
  for (const t of pack.topics) assert.ok(byTopic(t.id) >= 3, `${t.id}: не меньше трёх разобранных примеров`);
});
