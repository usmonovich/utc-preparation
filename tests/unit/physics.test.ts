// Контрольные примеры по физике: пересчёт примеров из конспекта и проверка согласованности формул.
// Источник значений — конспект (страница указана в названии теста).

import { test } from 'node:test';
import assert from 'node:assert/strict';

const close = (a: number, b: number, rel = 1e-3, msg?: string) =>
  assert.ok(Math.abs(a - b) <= Math.max(Math.abs(b) * rel, 1e-9), msg ?? `${a} ≉ ${b}`);
const g = 10;

test('p21L: атмосферное давление по опыту Торричелли = 101 396,16 Па', () => {
  close(13600 * 9.81 * 0.76, 101396.16, 1e-9);
});

test('p21L: высота столба воды в опыте Торричелли ≈ 10,3 м', () => {
  close(101396.16 / (1000 * 9.81), 10.3, 0.01);
});

test('p17L: первая космическая скорость ≈ 7905 м/с (с корнем — см. замечание E06)', () => {
  const v = Math.sqrt(6.67e-11 * 6e24 / 6.4e6);
  close(v, 7905, 0.001);
  assert.ok(6.67e-11 * 6e24 / 6.4e6 > 1e7, 'без корня получается не скорость — подтверждает описку E06');
});

test('p16R: g₀ = GM/R² ≈ 9,8 м/с²', () => {
  close(6.67e-11 * 6e24 / (6.4e6) ** 2, 9.8, 0.005);
});

test('p37L: вторая космическая = √2 · первая ≈ 11,2 км/с', () => {
  close(Math.SQRT2 * 7.9, 11.2, 0.003);
});

test('p27R: предел силы трения A = μmg = 6 Н', () => {
  close(0.3 * 2 * g, 6);
});

test('p39L: работа против сопротивления = 100 Дж', () => {
  close((2 * 20 ** 2) / 2 - 2 * g * 15, 100);
});

test('p03R: уравнение по графику x(t): x = 20 + 5t', () => {
  const v = (60 - 20) / 8;
  assert.equal(v, 5);
  assert.equal(20 + v * 8, 60);
});

test('p06L: ускорение по графику υ(t) = 4 м/с²', () => {
  assert.equal((60 - 20) / 10, 4);
});

test('p07R: путь по графику = 60 + 90 = 150 м и совпадает с формулой S = (υ+υ₀)t/2', () => {
  assert.equal(10 * 6 + (30 * 6) / 2, 150);
  assert.equal(((10 + 40) / 2) * 6, 150);
});

test('p13R: сумма десяти сил F_рез(3; 0)', () => {
  const F = [[-5, 3], [6, 1], [-4, -3], [4, -3], [0, 3], [6, 0], [3, 2], [-1, -1], [3, -3], [-9, 1]];
  assert.deepEqual(F.reduce(([x, y], [a, b]) => [x + a, y + b], [0, 0]), [3, 0]);
});

test('p24L: тело 2 кг объёмом 1 л — плотность 2000 кг/м³', () => {
  assert.equal(2 / 1e-3, 2000);
});

test('p02R: формулы средней скорости совпадают с определением S_общ / t_общ', () => {
  const [v1, v2, S] = [40, 60, 120];
  close(S / (S / 2 / v1 + S / 2 / v2), (2 * v1 * v2) / (v1 + v2));
  close(S / (S / 3 / v1 + (2 * S) / 3 / v2), (3 * v1 * v2) / (2 * v1 + v2));
  const t = 2;
  close((v1 * t + v2 * t) / (2 * t), (v1 + v2) / 2);
});

test('p06R: путь за n-ю секунду S_n = υ₀ + a(2n−1)/2 совпадает с S(n) − S(n−1)', () => {
  const [v0, a] = [5, 2];
  const S = (t: number) => v0 * t + (a * t * t) / 2;
  for (let n = 1; n <= 10; n++) close(S(n) - S(n - 1), v0 + (a / 2) * (2 * n - 1));
});

test('p07R: скорость в середине пути √((υ₀²+υ²)/2) даёт равные половины пути', () => {
  const [v0, v, a] = [10, 50, 3];
  const vx = Math.sqrt((v0 ** 2 + v ** 2) / 2);
  close((vx ** 2 - v0 ** 2) / (2 * a), (v ** 2 - vx ** 2) / (2 * a));
});

test('p08L: время падения при броске вниз — корень уравнения y(t) = 0', () => {
  const [H, v0] = [40, 10];
  const t = (-v0 + Math.sqrt(v0 ** 2 + 2 * g * H)) / g;
  close(H - v0 * t - (g / 2) * t * t, 0, 1e-9, 'y(t) = 0');
  close(v0 + g * t, Math.sqrt(v0 ** 2 + 2 * g * H));
});

test('p08R: время падения по последнему участку t = Δh/(gΔt) + Δt/2', () => {
  for (const H of [20, 80, 125]) {
    const T = Math.sqrt((2 * H) / g);
    const dt = 0.5;
    const dh = H - (g * (T - dt) ** 2) / 2;
    close(dh / (g * dt) + dt / 2, T);
  }
});

test('p09R: два тела, брошенные вверх с интервалом Δt, встречаются при t = υ₀/g + Δt/2', () => {
  const [v0, dt] = [30, 2];
  const t = v0 / g + dt / 2;
  const y = (s: number) => v0 * s - (g * s * s) / 2;
  close(y(t), y(t - dt));
  close(y(t), v0 ** 2 / (2 * g) - (g * (dt / 2) ** 2) / 2);
  close(v0 - g * t, -g * dt / 2, 1e-9, 'скорость первого тела при встрече');
  close((v0 - g * (t - dt)) - (v0 - g * t), g * dt, 1e-9, 'относительная скорость');
});

test('p11L: Δυ = 2υ·sin(φ/2): ¼ оборота — √2·υ, ½ — 2υ, полный — 0', () => {
  const v = 7;
  close(2 * v * Math.sin(Math.PI / 4), Math.SQRT2 * v);
  close(2 * v * Math.sin(Math.PI / 2), 2 * v);
  close(2 * v * Math.sin(Math.PI), 0, 1e-9);
});

test('p11L: все формы центростремительного ускорения совпадают', () => {
  const [R, T] = [2, 3];
  const w = (2 * Math.PI) / T, v = w * R, nu = 1 / T;
  const forms = [v ** 2 / R, w ** 2 * R, w * v, ((4 * Math.PI ** 2) / T ** 2) * R, 4 * Math.PI ** 2 * nu ** 2 * R];
  for (const f of forms) close(f, forms[0]);
});

test('p26R: блок с двумя грузами — a, T и F согласованы с системой уравнений', () => {
  const [m1, m2] = [3, 1];
  const a = (g * (m1 - m2)) / (m1 + m2);
  const T = ((2 * m1 * m2) / (m1 + m2)) * g;
  close(m1 * a, m1 * g - T);
  close(m2 * a, T - m2 * g);
  close(2 * T, ((4 * m1 * m2) / (m1 + m2)) * g);
});

test('p29R: сила, прижимающая тело к наклонной плоскости, удерживает его', () => {
  const [m, al, mu] = [2, (40 * Math.PI) / 180, 0.5];
  const F = (m * g * Math.sin(al)) / mu - m * g * Math.cos(al);
  close(m * g * Math.sin(al), mu * (m * g * Math.cos(al) + F));
});

test('p34R: импульс сохраняется при неупругом столкновении, теплота ≥ 0', () => {
  for (const [m1, v1, m2, v2] of [[2, 6, 1, 3], [1, 4, 3, -2], [5, 1, 5, 1]]) {
    const u = (m1 * v1 + m2 * v2) / (m1 + m2);
    close((m1 + m2) * u, m1 * v1 + m2 * v2);
    assert.ok((m1 * v1 ** 2) / 2 + (m2 * v2 ** 2) / 2 - ((m1 + m2) * u ** 2) / 2 >= -1e-12);
  }
});

test('p37R–p38L: упругий удар сохраняет импульс и энергию; равные массы меняются скоростями', () => {
  const u1 = (m1: number, v1: number, m2: number, v2: number) => (2 * m2 * v2 + v1 * (m1 - m2)) / (m1 + m2);
  const u2 = (m1: number, v1: number, m2: number, v2: number) => (2 * m1 * v1 + v2 * (m2 - m1)) / (m1 + m2);
  for (const [m1, v1, m2, v2] of [[2, 3, 1, 0], [1, 4, 3, -2], [0.5, -1, 4, 7]]) {
    const a = u1(m1, v1, m2, v2), b = u2(m1, v1, m2, v2);
    close(m1 * a + m2 * b, m1 * v1 + m2 * v2, 1e-9);
    close(m1 * a ** 2 + m2 * b ** 2, m1 * v1 ** 2 + m2 * v2 ** 2, 1e-9);
  }
  assert.equal(u1(2, 5, 2, -3), -3);
  assert.equal(u2(2, 5, 2, -3), 5);
  // формула «навстречу» (p38L) — та же формула с υ₂ → −υ₂
  close((-2 * 3 * 2 + 4 * (1 - 3)) / 4, u1(1, 4, 3, -2));
});

test('p38R: натяжение нити маятника T = mg(3 − 2cos α) = mg + mυ²/l', () => {
  const [m, l, al] = [0.2, 0.9, Math.PI / 3];
  const v = Math.sqrt(2 * g * l * (1 - Math.cos(al)));
  close(m * g + (m * v * v) / l, m * g * (3 - 2 * Math.cos(al)));
});

test('p36R: высота, где W_к = W_п, равна половине максимальной', () => {
  const v0 = 20, hmax = v0 ** 2 / (2 * g), h = hmax / 2;
  const vh2 = v0 ** 2 - 2 * g * h;
  close(vh2 / 2, g * h);
});

test('p41R: бросок под углом — H_max/L = tg α / 4 и три формы H_max совпадают', () => {
  for (const deg of [15, 30, 45, 60, 75]) {
    const a = (deg * Math.PI) / 180, v0 = 20;
    const tUp = (v0 * Math.sin(a)) / g, tFl = 2 * tUp;
    const H = (v0 ** 2 * Math.sin(a) ** 2) / (2 * g);
    const L = (v0 ** 2 * Math.sin(2 * a)) / g;
    close(H / L, Math.tan(a) / 4);
    close(H, (g * tUp ** 2) / 2);
    close(H, (g * tFl ** 2) / 8);
    close(L, v0 * Math.cos(a) * tFl);
  }
});

test('p41R: моменты t₁,₂ с заданным углом β дают tg β = |υ_y| / υ_x', () => {
  const [v0, a, b] = [30, Math.PI / 3, Math.PI / 6];
  for (const sign of [-1, 1]) {
    const t = (v0 * Math.sin(a) + sign * Math.tan(b) * v0 * Math.cos(a)) / g;
    close(Math.abs(v0 * Math.sin(a) - g * t) / (v0 * Math.cos(a)), Math.tan(b));
  }
});

test('p40L: КПД наклонной плоскости — две формы совпадают', () => {
  const [a, mu] = [0.6, 0.3];
  close(Math.tan(a) / (Math.tan(a) + mu), Math.sin(a) / (Math.sin(a) + mu * Math.cos(a)));
});

test('p17R: (T₁/T₂)² = (R₁/R₂)³ следует из T² = 4π²R³/(GM)', () => {
  const GM = 6.67e-11 * 6e24;
  const T = (R: number) => Math.sqrt((4 * Math.PI ** 2 * R ** 3) / GM);
  close((T(7e6) / T(2.8e7)) ** 2, (7e6 / 2.8e7) ** 3);
});

test('p23L: погружённая часть плавающего тела k = ρ_т/ρ_ж из равенства mg = F_A', () => {
  const [rt, rl, V] = [800, 1000, 0.5];
  const Vsub = (rt * V) / rl; // ρ_т V g = ρ_ж V' g
  close(Vsub / V, rt / rl);
});

test('p20R: сила давления на боковую стенку цилиндра = среднее давление × площадь стенки', () => {
  const [rho, h, R] = [1000, 0.5, 0.1];
  const n = 100000;
  let F = 0;
  for (let i = 0; i < n; i++) F += rho * g * ((i + 0.5) * (h / n)) * 2 * Math.PI * R * (h / n);
  close(F, ((rho * g * h) / 2) * 2 * Math.PI * R * h, 1e-6);
});

// ───────────── Молекулярная физика и термодинамика (файл «Молекулярная физика.pdf») ─────────────
const R = 8.31, kB = 1.38e-23, NA = 6e23;

test('m07: задача по графику — T₂ = 1600 К, T₃ = 1200 К при T₁ = 100 К', () => {
  const T = (p: number, V: number) => (100 * p * V) / (1 * 1);
  assert.equal(T(4, 4), 1600);
  assert.equal(T(2, 6), 1200);
});

test('m06: R = N_A·k ≈ 8,31; все пять форм υ_кв совпадают', () => {
  close(6.022e23 * kB, 8.31, 0.002);
  const mu = 32e-3, T = 300, m0 = mu / NA, Rk = NA * kB, p = 1e5;
  const n = p / (kB * T), rho = m0 * n, V = 2, m = rho * V;
  const forms = [Math.sqrt((3 * p) / (m0 * n)), Math.sqrt((3 * p) / rho), Math.sqrt((3 * p * V) / m), Math.sqrt((3 * kB * T) / m0), Math.sqrt((3 * Rk * T) / mu)];
  for (const f of forms) close(f, forms[0], 1e-9);
});

test('m04–m05: основное уравнение МКТ согласуется с p = nkT и p = ⅔nW̄к', () => {
  const T = 300, n = 2.5e25, m0 = 5.3e-26;
  const v2 = (3 * kB * T) / m0;
  close((1 / 3) * m0 * n * v2, n * kB * T);
  close((2 / 3) * n * ((m0 * v2) / 2), n * kB * T);
});

test('m05: замечание M05 — W̄к = 3/2·pV верно только для полной энергии', () => {
  const N = 1e22, V = 1e-3, T = 300, p = (N * kB * T) / V;
  close(1.5 * kB * T * N, 1.5 * p * V, 1e-9); // полная энергия
  assert.ok(Math.abs(1.5 * kB * T - 1.5 * p * V) > 1, 'для одной молекулы формула не выполняется');
});

test('m07: плотность газа ρ = μp/(RT) совпадает с m/V из уравнения состояния', () => {
  const mu = 28e-3, p = 2e5, T = 350, V = 0.5;
  const m = (p * V * mu) / (R * T);
  close(m / V, (mu * p) / (R * T), 1e-12);
});

test('m14–m15: при p = const доли A/Q и ΔU/Q для i = 3, 5, 6', () => {
  for (const [i, a, u] of [[3, 0.4, 0.6], [5, 2 / 7, 5 / 7], [6, 0.25, 0.75]]) {
    const nu = 2, dT = 40, A = nu * R * dT, dU = (i / 2) * nu * R * dT, Q = dU + A;
    close(A / Q, a, 1e-9);
    close(dU / Q, u, 1e-9);
    close(Q, ((i + 2) / 2) * nu * R * dT, 1e-9);
  }
});

test('m13: работа при изотерме — интеграл p dV равен νRT ln(V₂/V₁) = νRT ln(p₁/p₂)', () => {
  const nu = 1, T = 300, V1 = 1e-3, V2 = 3e-3, steps = 200000;
  let A = 0;
  for (let j = 0; j < steps; j++) { const V = V1 + ((j + 0.5) * (V2 - V1)) / steps; A += ((nu * R * T) / V) * ((V2 - V1) / steps); }
  close(A, nu * R * T * Math.log(V2 / V1), 1e-6);
  close(A, nu * R * T * Math.log(((nu * R * T) / V1) / ((nu * R * T) / V2)), 1e-6);
});

test('m15: адиабата — pV^γ = const даёт работу = убыли внутренней энергии', () => {
  const i = 5, g = (i + 2) / i, nu = 1, T1 = 400, V1 = 1e-2, V2 = 2e-2;
  const p1 = (nu * R * T1) / V1, C = p1 * V1 ** g;
  const T2 = (C / V2 ** g) * V2 / (nu * R);
  let A = 0;
  const steps = 200000;
  for (let j = 0; j < steps; j++) { const V = V1 + ((j + 0.5) * (V2 - V1)) / steps; A += (C / V ** g) * ((V2 - V1) / steps); }
  close(A, (i / 2) * nu * R * (T1 - T2), 1e-5);
  assert.ok(T2 < T1, 'при адиабатном расширении температура уменьшается');
});

test('m16: в цикле Карно V₂V₄ = V₁V₃, p₁p₃ = p₂p₄ и КПД = (T_I − T_II)/T_I', () => {
  const g = 5 / 3, nu = 1, TI = 500, TII = 300, V1 = 1e-3, V2 = 3e-3;
  const V3 = V2 * (TI / TII) ** (1 / (g - 1)), V4 = V1 * (TI / TII) ** (1 / (g - 1));
  close(V2 * V4, V1 * V3, 1e-9);
  const p = (T: number, V: number) => (nu * R * T) / V;
  close(p(TI, V1) * p(TII, V3), p(TI, V2) * p(TII, V4), 1e-9);
  const Q1 = nu * R * TI * Math.log(V2 / V1), Q2 = nu * R * TII * Math.log(V3 / V4);
  close((Q1 - Q2) / Q1, (TI - TII) / TI, 1e-9);
});

test('m20: формула температуры смеси совпадает с уравнением теплового баланса', () => {
  const [m1, c1, t1, m2, c2, t2] = [2, 4200, 20, 1, 400, 100];
  const th = (m1 * c1 * t1 + m2 * c2 * t2) / (m1 * c1 + m2 * c2);
  close(m1 * c1 * (th - t1), m2 * c2 * (t2 - th), 1e-9);
  assert.ok(th > t1 && th < t2);
});

test('m18: капиллярное давление 2σ/R уравновешивает столб ρgh', () => {
  const s = 73e-3, R0 = 5e-4, rho = 1000, g0 = 10, h = (2 * s) / (rho * g0 * R0);
  close(rho * g0 * h, (2 * s) / R0, 1e-12);
});

test('h01: относительная влажность через плотности и через давления совпадает (ρ = μp/RT, стр. m07)', () => {
  const mu = 18e-3, T = 293, p = 1170, p0 = 2340;
  const rho = (mu * p) / (R * T), rho0 = (mu * p0) / (R * T);
  close((rho / rho0) * 100, (p / p0) * 100, 1e-12);
});

// ───────────── Конспект по оптике (o01–o20) ─────────────
const c = 3e8, hP = 6.62e-34;

test('o01: формулы контура согласованы — ω = 2πν, λ = c/ν = cT = c·2π√(LC)', () => {
  const L = 0.01, C = 1e-4;
  const nu = 1 / (2 * Math.PI) / Math.sqrt(L * C), T = 2 * Math.PI * Math.sqrt(L * C), w = 1 / Math.sqrt(L * C);
  close(w, 2 * Math.PI * nu, 1e-12);
  close(c / nu, c * T, 1e-12);
  close(c * T, c * 2 * Math.PI * Math.sqrt(L * C), 1e-12);
});

test('o02–o03: цепочка sin α·n = const даёт тот же угол, что и прямой закон Снеллиуса', () => {
  const n = [1.5, 1.8, 1.3, 1.1], sa = 0.4;
  let s = sa;
  for (let i = 1; i < n.length; i++) s = (s * n[i - 1]) / n[i];
  close(s, (sa * n[0]) / n[3], 1e-12);
  // на рисунке φ > γ > α > β ⇔ n₄ < n₃ < n₁ < n₂
  const ang = n.map((ni) => Math.asin((sa * n[0]) / ni));
  assert.ok(ang[3] > ang[2] && ang[2] > ang[0] && ang[0] > ang[1]);
  assert.ok(n[3] < n[2] && n[2] < n[0] && n[0] < n[1]);
});

test('o02: υ₁/υ₂ = λ₁/λ₂ = n₂/n₁ при одинаковой частоте', () => {
  const n1 = 1, n2 = 1.5, nu = 5e14;
  const v1 = c / n1, v2 = c / n2;
  close(v1 / v2, n2 / n1, 1e-12);
  close(v1 / nu / (v2 / nu), n2 / n1, 1e-12);
});

test('o06: sin α₀ = n₂/n₁ — это закон Снеллиуса при β = 90°', () => {
  const n1 = 1.5, n2 = 1;
  close(Math.sin(Math.asin(n2 / n1)) / Math.sin(Math.PI / 2), n2 / n1, 1e-12);
});

test('o04–o05: I_рез в максимуме = (√I₁ + √I₂)²; замечание O05 — нужна A_рез², а не A_рез', () => {
  const A1 = 1, A2 = 2, I = (A: number) => A * A;
  close(I(A1) + I(A2) + 2 * Math.sqrt(I(A1) * I(A2)) * Math.cos(0), (Math.sqrt(I(A1)) + Math.sqrt(I(A2))) ** 2, 1e-12);
  const asWritten = A1 ** 2 + A2 ** 2 + 2 * A1 * A2; // запись конспекта при Δφ = 0
  assert.notEqual(asWritten, A1 + A2, 'A_рез = A₁ + A₂ не получается — подтверждает O05');
  close(Math.sqrt(asWritten), A1 + A2, 1e-12);
  // Δx = kλ ⇔ Δφ = 2πk
  close((2 * Math.PI / 500e-9) * (3 * 500e-9), 2 * Math.PI * 3, 1e-12);
});

test('o14: изображение в плоском зеркале движется со скоростью 2υ, если зеркало движется со скоростью υ', () => {
  const xObj = 0, v = 0.5, img = (t: number) => 2 * (1 + v * t) - xObj; // зеркало в точке 1 + υt
  close((img(2) - img(0)) / 2, 2 * v, 1e-12);
});

test('o16–o17: таблица изображений собирающей линзы согласуется с формулой линзы', () => {
  const F = 10, f = (d: number) => 1 / (1 / F - 1 / d), k = (d: number) => Math.abs(f(d)) / d;
  assert.ok(f(30) > 0 && k(30) < 1, 'd > 2F: действительное, уменьшенное');
  close(k(20), 1, 1e-12); // d = 2F: равное
  assert.ok(f(15) > 0 && k(15) > 1, '2F > d > F: действительное, увеличенное');
  assert.ok(!Number.isFinite(f(F)) || Math.abs(f(F)) > 1e12, 'd = F: изображения нет');
  assert.ok(f(5) < 0 && k(5) > 1, 'F > d > 0: мнимое, увеличенное');
  close(f(1e12), F, 1e-9); // d = ∞: f ≈ F
});

test('o18–o19: частные формулы линзы следуют из общей', () => {
  const D = (nl: number, nc: number, R1: number, R2: number) => ((nl - nc) / nc) * (1 / R1 + 1 / R2);
  close(D(1.5, 1, 0.2, 0.2), (1.5 - 1) * 2 / 0.2, 1e-12);
  close(D(1.6, 1, 0.3, Infinity), (1.6 - 1) / 0.3, 1e-12);
  assert.ok(D(1.5, 1.7, 0.2, 0.2) < 0, 'n_л < n_с: выпуклая линза рассеивающая');
  assert.ok(D(1.5, 1, -0.2, -0.2) < 0, 'вогнутая (R < 0) — рассеивающая');
});

test('o19–o20: система линз — при l = 0 D = D₁ + D₂, при l = F₁ + F₂ D = 0 (пучок выходит параллельным)', () => {
  const Dsys = (D1: number, D2: number, l: number) => D1 + D2 - l * D1 * D2;
  close(Dsys(2, 3, 0), 5, 1e-12);
  assert.ok(Math.abs(Dsys(5, 2, 1 / 5 + 1 / 2)) < 1e-12);
  const F1 = 0.2, F2 = 0.3, l = 0.1;
  close(1 / (1 / F1 + 1 / F2 - l / (F1 * F2)), 1 / Dsys(1 / F1, 1 / F2, l), 1e-12);
});

test('o10–o11: ρ = m/V даёт ρ₀/(1 − υ²/c²); при υ₁ = c относительная скорость равна c', () => {
  const k = Math.sqrt(1 - 0.36), m0 = 2, V0 = 0.5;
  close((m0 / k) / (V0 * k), (m0 / V0) / (1 - 0.36), 1e-12);
  const vrel = (v1: number, v2: number) => (v1 + v2) / (1 + (v1 * v2) / (c * c));
  close(vrel(c, 0.5 * c), c, 1e-12);
  assert.ok(vrel(0.99 * c, 0.99 * c) < c);
});

test('o12: E = E₀/√(1−υ²/c²) совпадает с mc², p = mυ при m = m₀/√(1−υ²/c²)', () => {
  const m0 = 1, v = 0.6 * c, k = Math.sqrt(1 - (v * v) / (c * c)), m = m0 / k;
  close((m0 * c * c) / k, m * c * c, 1e-12);
  close((m0 * v) / k, m * v, 1e-12);
});

test('o12: фотон — p = E/c = h/λ, m = hν/c² = h/(cλ); в среде m_с = hn/(cλ_с), p_с = m_с·υ_с', () => {
  const lam0 = 600e-9, nu = c / lam0, E = hP * nu, n = 1.5;
  close(E / c, hP / lam0, 1e-12);
  close((hP * nu) / (c * c), hP / (c * lam0), 1e-12);
  const lamC = lam0 / n, mC = ((hP * nu) / (c * c)) * n * n;
  close(mC, (hP * n) / (c * lamC), 1e-12);
  close(mC * (c / n), ((hP * nu) / c) * n, 1e-12);
});

test('o14: пример конспекта (8 − 5 = 3 эВ); замечание O15 — уравнение через λ верно только с hc', () => {
  assert.equal(8 - 5, 3);
  assert.ok(5 < 7, 'hν < A — фотоэффекта нет');
  const lam = 400e-9, lamK = 600e-9, Ek = hP * c / lam - hP * c / lamK;
  close(hP * (c / lam), hP * (c / lamK) + Ek, 1e-12); // hν = hν_к + E_к
  const nu = c / lam, nuK = c / lamK;
  const lhs = (hP * nu) / lam, rhs = (hP * nu) / lamK + Ek; // запись конспекта
  assert.ok(Math.abs(lhs - rhs) / lhs > 0.1, 'запись hν/λ = hν/λ_к + E_к не выполняется — подтверждает O15');
  close(hP * nuK, hP * c / lamK, 1e-12); // A = hν_к = hc/λ_к
});

// ───────────── Конспект по магнетизму, колебаниям и переменному току (e01–e28) ─────────────
const mu0 = 4 * Math.PI * 1e-7;
const deriv = (fn: (t: number) => number, t: number, h = 1e-6) => (fn(t + h) - fn(t - h)) / (2 * h);
type V3 = [number, number, number];
const cross = (a: V3, b: V3): V3 => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];

test('e01: схема с диодом — R ∥ 2R = 2R/3, закрытый диод оставляет только 2R', () => {
  const R = 6, par = (a: number, b: number) => (a * b) / (a + b);
  close(par(R, 2 * R), (2 * R) / 3, 1e-12);
  close(par(1e12, 2 * R), 2 * R, 1e-9); // ветвь с R → ∞
});

test('e04: общая формула суперпозиции даёт частные случаи ↑↑, ↑↓ и ⊥', () => {
  const g = (b1: number, b2: number, a: number) => Math.sqrt(b1 ** 2 + b2 ** 2 + 2 * b1 * b2 * Math.cos(a));
  close(g(3, 4, 0), 7, 1e-12);
  close(g(4, 3, Math.PI), 1, 1e-9);
  close(g(3, 4, Math.PI / 2), 5, 1e-12);
});

test('e04–e05: B = μμ₀H выполняется для прямого и кругового тока', () => {
  const I = 5, r = 0.05, R = 0.02, mu = 1;
  close(mu * mu0 * (I / (2 * Math.PI * r)), mu * mu0 * I / (2 * Math.PI * r), 1e-12);
  close(mu * mu0 * (I / (2 * R)), mu * mu0 * I / (2 * R), 1e-12);
  close(mu0 * (5 / (2 * Math.PI * 0.05)), 2e-5, 1e-12);
});

test('e06: все семь рисунков направления силы Ампера совпадают с F = I·l × B (правило левой руки)', () => {
  // x — вправо, y — вверх, z — к нам (⊙)
  const cases: [V3, V3, V3][] = [
    [[1, 0, 0], [0, -1, 0], [0, 0, -1]], // N сверху, I вправо → ⊗
    [[0, 1, 0], [1, 0, 0], [0, 0, -1]], // поле вправо, I вверх → ⊗
    [[0, 0, 1], [-1, 0, 0], [0, -1, 0]], // поле влево, I ⊙ → вниз
    [[-1, 0, 0], [0, 1, 0], [0, 0, -1]], // поле вверх, I влево → ⊗
    [[0, 0, -1], [0, -1, 0], [-1, 0, 0]], // поле вниз, I ⊗ → влево
    [[0, -1, 0], [0, 0, -1], [1, 0, 0]], // поле ⊗, I вниз → вправо
    [[1, 0, 0], [0, 0, 1], [0, -1, 0]], // поле ⊙, I вправо → вниз
  ];
  const sg = (v: number[]) => v.map((x) => Math.sign(x) + 0);
  for (const [I, B, F] of cases) assert.deepEqual(sg(cross(I, B)), sg(F));
  // рамка: слева ток вверх → ⊗, справа ток вниз → ⊙ (стр. e06)
  assert.deepEqual(sg(cross([0, 1, 0], [1, 0, 0])), [0, 0, -1]);
  assert.deepEqual(sg(cross([0, -1, 0], [1, 0, 0])), [0, 0, 1]);
});

test('e08: сила Лоренца на рисунке ② направлена к центру; формулы R, T, ν, ω и спирали согласованы', () => {
  // ⊖, υ вверх, поле ⊗ → F = qυ × B вправо
  const F = cross([0, 1, 0], [0, 0, -1]).map((v) => -1 * v);
  assert.deepEqual(F.map((x) => Math.sign(x) + 0), [1, 0, 0]);
  const m = 1.6e-27, q = 1.6e-19, B = 0.1, U = 1000;
  const W = U * q, v = Math.sqrt((2 * W) / m), R = (m * v) / (q * B);
  close(R, Math.sqrt(2 * W * m) / (q * B), 1e-12);
  close(R, (1 / B) * Math.sqrt((2 * U * m) / q), 1e-12);
  const T = (2 * Math.PI * R) / v;
  close(T, (2 * Math.PI * m) / (q * B), 1e-12); // период не зависит от скорости
  close((q * B) / m, (2 * Math.PI) / T, 1e-12);
  close(1 / T, (q * B) / (2 * Math.PI * m), 1e-12);
  const a = Math.PI / 3; // спираль: шаг = продольная скорость × период
  close((2 * Math.PI * m * v * Math.cos(a)) / (q * B), v * Math.cos(a) * T, 1e-12);
});

test('e10–e11: υ = x′, a = υ′ и a = −ω²x для всех трёх начальных условий; замечание EM04', () => {
  const A = 0.1, w = 10, ph = 0.5;
  const xs = [(t: number) => A * Math.sin(w * t), (t: number) => A * Math.cos(w * t), (t: number) => A * Math.sin(w * t + ph)];
  for (const x of xs) for (const t of [0.1, 0.37, 1.2]) {
    const v = (s: number) => deriv(x, s);
    close(deriv(v, t, 1e-4), -w * w * x(t), 1e-4);
  }
  close(deriv(xs[0], 0), w * A, 1e-6); // υ_max = ωA
  const aTrue = (t: number) => -A * w * w * Math.cos(w * t), aBox = (t: number) => w * w * A * Math.cos(w * t);
  assert.ok(aTrue(0) < 0 && aBox(0) > 0, 'в рамке на e11 потерян минус — подтверждает EM04');
  close(4 * Math.cos(Math.PI / 3), 2, 1e-12); // пример на e11
  close(4 * Math.sin((Math.PI / 2) * 2), 0, 1e-9); // пример на e10
});

test('e11–e12: формулы маятников согласованы (T·ν = 1, ω = 2πν)', () => {
  const l = 2.5, g0 = 10, k = 40, m = 0.4;
  close(2 * Math.PI * Math.sqrt(l / g0) * (1 / (2 * Math.PI)) * Math.sqrt(g0 / l), 1, 1e-12);
  close(Math.sqrt(g0 / l), 2 * Math.PI * ((1 / (2 * Math.PI)) * Math.sqrt(g0 / l)), 1e-12);
  close(2 * Math.PI * Math.sqrt(m / k) * (1 / (2 * Math.PI)) * Math.sqrt(k / m), 1, 1e-12);
});

test('e12–e13: Eк + Eп = const, формы через cos 2ωt совпадают, энергия колеблется с удвоенной частотой', () => {
  const E = 2, w = 3;
  for (const t of [0, 0.2, 0.9, 1.7]) {
    const ek = E * Math.cos(w * t) ** 2, ep = E * Math.sin(w * t) ** 2;
    close(ek + ep, E, 1e-12);
    close(ek, 0.5 * E * (1 + Math.cos(2 * w * t)), 1e-12);
    close(ep, 0.5 * E * (1 - Math.cos(2 * w * t)), 1e-12);
    close(E * Math.cos(w * (t + Math.PI / w)) ** 2, ek, 1e-9); // период энергии T/2
  }
});

test('e14: пример — между 2-м и 4-м пиком 30 м ⇒ λ = 15 м; λ = υT = υ/ν', () => {
  close(30 / 2, 15, 1e-12);
  close(340 * (1 / 170), 340 / 170, 1e-12);
});

test('e16–e17: три случая ΔΦ совпадают с Φ₂ − Φ₁; Φ = kt + b даёт ε = −k', () => {
  const Phi = (B: number, S: number, a: number) => B * S * Math.cos(a);
  close(Phi(0.5, 0.2, 0.3) - Phi(0.1, 0.2, 0.3), (0.5 - 0.1) * 0.2 * Math.cos(0.3), 1e-12);
  close(Phi(2, 0.3, 1) - Phi(2, 0.1, 1), 2 * 0.2 * Math.cos(1), 1e-12);
  close(Phi(0.5, 0.2, Math.PI / 2) - Phi(0.5, 0.2, 0), 0.5 * 0.2 * (0 - 1), 1e-12);
  const k = 3, b = 2;
  close(-deriv((t) => k * t + b, 1.3), -k, 1e-6);
});

test('e18: L = μμ₀N²S/l₀ согласуется с Φ = LI = NBS и H = NI/l₀; замечание EM09', () => {
  const N = 500, S = 1e-3, l0 = 0.25, I = 3, mu = 1;
  const L = mu * mu0 * (N ** 2 * S) / l0, H = (N * I) / l0, B = mu * mu0 * H;
  close(L * I, N * B * S, 1e-12);
  const W = (L * I ** 2) / 2, Phi = L * I;
  close((Phi * I) / 2, W, 1e-12);
  close(Phi ** 2 / (2 * L), W, 1e-12);
  close(Phi ** 2 / (L * I), Phi, 1e-12); // запись конспекта сводится к самому потоку Φ = LI, а не к энергии — подтверждает EM09
  assert.ok(Math.abs(Phi ** 2 / (L * I) - W) / W > 0.1);
  const I0 = 2, w = 100, Lc = 0.1; // ε = −L·dI/dt при I = I₀cos ωt
  for (const t of [0.01, 0.023]) close(-Lc * deriv((s) => I0 * Math.cos(w * s), t), Lc * I0 * w * Math.sin(w * t), 1e-6);
});

test('e20–e21: в контуре I = q′, I₀ = q₀ω и W_C + W_L = const при ω = 1/√(LC)', () => {
  const L = 0.1, C = 1e-6, U0 = 100, q0 = C * U0, w = 1 / Math.sqrt(L * C), I0 = q0 * w;
  for (const t of [0, 1e-4, 3.3e-4]) {
    close(deriv((s) => q0 * Math.cos(w * s), t, 1e-9), -I0 * Math.sin(w * t), 1e-5);
    const wc = (q0 * Math.cos(w * t)) ** 2 / (2 * C), wl = (L * (I0 * Math.sin(w * t)) ** 2) / 2;
    close(wc + wl, q0 ** 2 / (2 * C), 1e-9);
  }
  close(q0 ** 2 / (2 * C), (L * I0 ** 2) / 2, 1e-9);
});

test('e22–e23: ε = −N·dΦ/dt даёт NBSω sin ωt; U_эф = U₀/√2 — среднеквадратичное; 220·√2 ≈ 310', () => {
  const N = 100, B = 0.2, S = 0.05, w = 100;
  for (const t of [0.003, 0.011]) close(-N * deriv((s) => B * S * Math.cos(w * s), t), N * B * S * w * Math.sin(w * t), 1e-6);
  const U0 = 310, n = 100000;
  let sq = 0, p = 0;
  for (let i = 0; i < n; i++) { const u = U0 * Math.sin((2 * Math.PI * i) / n); sq += u * u; p += Math.sin((2 * Math.PI * i) / n) ** 2; }
  close(Math.sqrt(sq / n), U0 / Math.sqrt(2), 1e-9);
  close(p / n, 0.5, 1e-9); // среднее I₀U₀sin² = I₀U₀/2
  close(220 * Math.SQRT2, 311.1, 1e-3);
});

test('e23–e24: на C ток I = C·U′ (впереди на π/2), на L напряжение U = L·I′ (ток позади); средняя мощность 0', () => {
  const U0 = 100, w = 1000, C = 1e-5, L = 2;
  for (const t of [0.0003, 0.0011]) {
    close(C * deriv((s) => U0 * Math.cos(w * s), t, 1e-8), -U0 * w * C * Math.sin(w * t), 1e-5);
    close(-U0 * w * C * Math.sin(w * t), U0 * w * C * Math.cos(Math.PI / 2 + w * t), 1e-9);
    const I0 = U0 / (w * L);
    close(L * deriv((s) => I0 * Math.sin(w * s), t, 1e-8), U0 * Math.cos(w * t), 1e-5);
  }
  let pc = 0, pl = 0;
  const n = 10000;
  for (let i = 0; i < n; i++) { const ph = (2 * Math.PI * i) / n; pc += Math.cos(ph) * -Math.sin(ph); pl += Math.cos(ph) * Math.sin(ph); }
  assert.ok(Math.abs(pc / n) < 1e-9 && Math.abs(pl / n) < 1e-9);
});

test('e25: U = IZ согласуется с U = √((U_C − U_L)² + U_R²) только при Z с корнем (замечание EM10); P̄ через cos Δφ = I₀²R/2', () => {
  const I = 2, R = 30, XL = 50, XC = 20;
  const U = Math.sqrt((I * XC - I * XL) ** 2 + (I * R) ** 2);
  close(U, I * Math.sqrt((XL - XC) ** 2 + R ** 2), 1e-12);
  assert.notEqual(U, I * ((XL - XC) ** 2 + R ** 2));
  const Z = Math.sqrt((XL - XC) ** 2 + R ** 2), I0 = 2, U0 = I0 * Z;
  close(((I0 * U0) / 2) * (R / Z), (I0 ** 2 * R) / 2, 1e-12);
  close(((U0 ** 2) / (2 * Z ** 2)) * R, (I0 ** 2 * R) / 2, 1e-12);
  close(Math.atan(Math.abs(XL - XC) / R), Math.acos(R / Z), 1e-12);
});

test('e27: трансформатор — k = N₁/N₂ = U₁/U₂ = I₂/I₁ при I₁U₁ = I₂U₂', () => {
  const N1 = 1000, N2 = 50, U1 = 220, U2 = (U1 * N2) / N1, I1 = 0.5, I2 = (I1 * U1) / U2;
  close(N1 / N2, U1 / U2, 1e-12);
  close(U1 / U2, I2 / I1, 1e-12);
  assert.ok(N1 / N2 > 1 && U1 > U2 && I1 < I2, 'понижающий: k > 1');
});

// ——— Конспект «Электричество» (c01–c40) ———

const eps0 = 8.85e-12;
const kC = 9e9;
const e0 = 1.6e-19;

test('c02: |q| = Ne — O: 8p, 5e⁻ → +3e; 8p, 10e⁻ → −2e; закон сохранения заряда для шариков (+7, +9 → по +8; +12, 0, −3 → по +3)', () => {
  const q = (p: number, n: number) => (p - n) * e0;
  close(q(8, 5), 3 * e0, 1e-12);
  close(q(8, 10), -2 * e0, 1e-12);
  assert.equal(q(8, 8), 0);
  close(Math.abs(q(8, 10)) / e0, 2, 1e-12);
  assert.deepEqual([(7 + 9) / 2, (7 + 9) / 2], [8, 8]);
  assert.equal((12 + 0 - 3) / 3, 3);
});

test('c01: m_p ≈ 1836 m_e по массам из конспекта', () => {
  close(1.67e-27 / 9.1e-31, 1836, 0.002);
});

test('c03, c14: k = 1/(4πε₀) ≈ 9·10⁹ (ε₀ — электрическая постоянная, замечание EL01); шар ёмкостью 1 Ф имеет R = k ≈ 9·10⁹ м', () => {
  close(1 / (4 * Math.PI * eps0), kC, 0.002);
  const R = 1 / (4 * Math.PI * eps0 * 1);
  close(R, 9e9, 0.002);
  close(4 * Math.PI * eps0 * R, 1, 1e-12);
});

test('c08: число пар зарядов C²ₙ = n(n−1)/2 — для трёх зарядов 3 слагаемых W; запись n(n+1)/2 даёт 6 (замечание EL04)', () => {
  for (const n of [2, 3, 4, 5, 7]) {
    let pairs = 0;
    for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) pairs++;
    assert.equal(pairs, (n * (n - 1)) / 2, `n = ${n}`);
  }
  assert.equal((3 * (3 + 1)) / 2, 6);
  assert.notEqual((3 * (3 + 1)) / 2, 3);
});

test('c06, c09: заряженная сфера — E₀ = kq/R² = σ/ε₀, E_внеш = E₀(R/(R+l))², φ₀ = kq/R = σR/ε₀, φ_внеш = φ₀·R/(R+l)', () => {
  const q = 4e-9, R = 0.05, l = 0.15;
  const k = 1 / (4 * Math.PI * eps0);
  const S = 4 * Math.PI * R * R, sigma = q / S;
  close((k * q) / R ** 2, sigma / eps0, 1e-12);
  close(((k * q) / R ** 2) * (R / (R + l)) ** 2, (k * q) / (R + l) ** 2, 1e-12);
  close((k * q) / R, (sigma * R) / eps0, 1e-12);
  close(((k * q) / R) * (R / (R + l)), (k * q) / (R + l), 1e-12);
});

test('c07, c22: σ/2ε₀ — поле одной плоскости; между разноимёнными пластинами поля складываются в σ/ε₀, снаружи — 0 (замечание EL03)', () => {
  const sigma = 3e-6, eps = 1;
  const one = sigma / (2 * eps * eps0);
  close(one + one, sigma / (eps * eps0), 1e-12);
  assert.equal(one - one, 0);
  // c21: две одноимённые пластины σ₁ > σ₂ — внутри разность, снаружи сумма
  const s1 = 5e-6, s2 = 2e-6;
  close(s1 / (2 * eps0) - s2 / (2 * eps0), (s1 - s2) / (2 * eps0), 1e-12);
  close(s1 / (2 * eps0) + s2 / (2 * eps0), (s1 + s2) / (2 * eps0), 1e-12);
});

test('c05: суперпозиция — общая формула с cos α даёт сумму (α = 0), разность (α = π) и теорему Пифагора (α = π/2); совпадает с векторным сложением', () => {
  const E1 = 300, E2 = 400;
  const Er = (a: number) => Math.sqrt(E1 ** 2 + E2 ** 2 + 2 * E1 * E2 * Math.cos(a));
  close(Er(0), E1 + E2, 1e-12);
  close(Er(Math.PI), Math.abs(E1 - E2), 1e-9);
  close(Er(Math.PI / 2), 500, 1e-12);
  const a = 1.1;
  close(Er(a), Math.hypot(E1 + E2 * Math.cos(a), E2 * Math.sin(a)), 1e-12);
});

test('c07–c08: знак W = kq₁q₂/R — отталкивание (+ +, − −) даёт W > 0, притяжение — W < 0; φ_об — сумма потенциалов', () => {
  const W = (q1: number, q2: number, R: number) => (kC * q1 * q2) / R;
  assert.ok(W(1e-9, 2e-9, 0.1) > 0 && W(-1e-9, -2e-9, 0.1) > 0);
  assert.ok(W(1e-9, -2e-9, 0.1) < 0);
  const phi = kC * 2e-9 / 0.3 + kC * -1e-9 / 0.2;
  close(phi, 60 - 45, 1e-12);
});

test('c11–c12: A = Eqd = qU = Eql·cos α, U = Ed; закон сохранения энергии φ₁q + mυ₁²/2 = φ₂q + mυ₂²/2', () => {
  const E = 2000, q = 3e-6, d = 0.05, l = 0.08;
  const alpha = Math.acos(d / l);
  close(E * q * l * Math.cos(alpha), E * q * d, 1e-12);
  close(q * (E * d), E * q * d, 1e-12);
  // электрон из покоя проходит разность потенциалов U: υ = √(2eU/m)
  const U = 100, m = 9.1e-31;
  const v2 = Math.sqrt((2 * e0 * U) / m);
  close(0 * e0 + 0, -e0 * U + (m * v2 ** 2) / 2, 1e-9);
  // 1 эВ, 1 кэВ, 1 МэВ
  close(1e3 * e0, 1.6e-16, 1e-12);
  close(1e6 * e0, 1.6e-13, 1e-12);
});

test('c13: контакт шаров — потенциалы равны, q′ᵢ = Rᵢq_об/R_об; φ′ = kq_об/R_об = Σφᵢ Rᵢ/ΣRᵢ (8 нКл, R 1 и 3 см → 2 и 6 нКл)', () => {
  const R1 = 0.01, R2 = 0.03, q1 = 8e-9, q2 = 0;
  const q1n = (R1 * (q1 + q2)) / (R1 + R2), q2n = (R2 * (q1 + q2)) / (R1 + R2);
  close(q1n, 2e-9, 1e-12);
  close(q2n, 6e-9, 1e-12);
  close((kC * q1n) / R1, (kC * q2n) / R2, 1e-12);
  close(q1n + q2n, q1 + q2, 1e-12);
  const phi1 = (kC * q1) / R1, phi2 = (kC * q2) / R2;
  close((phi1 * R1 + phi2 * R2) / (R1 + R2), (kC * (q1 + q2)) / (R1 + R2), 1e-12);
  close((kC * (q1 + q2)) / (R1 + R2), (kC * q1n) / R1, 1e-12);
  // три шара
  const Rs = [0.01, 0.02, 0.05], qs = [3e-9, -1e-9, 4e-9];
  const Rob = Rs.reduce((a, b) => a + b), qob = qs.reduce((a, b) => a + b);
  const after = Rs.map((r) => (r * qob) / Rob);
  for (let i = 1; i < 3; i++) close(after[i] / Rs[i], after[0] / Rs[0], 1e-12);
});

const ser = (...c: number[]) => 1 / c.reduce((a, x) => a + 1 / x, 0);
const par = (...c: number[]) => c.reduce((a, x) => a + x, 0);

test('c18: смешанные соединения конденсаторов — 3C/2, 11C/6, 2C/3 и «ромб» с перемычкой 2C', () => {
  const C = 1;
  close(par(ser(C, C), C), 1.5, 1e-12);
  close(par(ser(C, C, C), ser(C, C), C), 11 / 6, 1e-12);
  close(ser(par(C, C), C), 2 / 3, 1e-12);
  close(par(ser(C, C), C, ser(C, C)), 2, 1e-12);
});

test('c18: «ромб» — независимый расчёт методом узловых потенциалов даёт 2C', () => {
  // узлы: A (φ = 1), B (φ = 0), верх M, низ N; ветви A–M, M–B, A–N, N–B по C и перемычка A–B (C)
  const C = 1;
  // заряд узла M: C(φM − 1) + C(φM − 0) = 0 → φM = 1/2, так же φN
  const phiM = 0.5, phiN = 0.5;
  const qA = C * (1 - phiM) + C * (1 - phiN) + C * (1 - 0);
  close(qA / 1, 2 * C, 1e-12);
});

test('c20: ключ в мостике C–2C / 2C–C: разомкнут 4C/3, замкнут 3C/2, «увеличилось в 9/8 раз»', () => {
  const C = 1;
  const open = par(ser(C, 2 * C), ser(2 * C, C));
  const closed = ser(par(C, 2 * C), par(2 * C, C));
  close(open, 4 / 3, 1e-12);
  close(closed, 3 / 2, 1e-12);
  close(closed / open, 9 / 8, 1e-12);
});

test('c17: n одинаковых последовательно — C/n; C_об меньше наименьшей ёмкости, а как произведение запись неверна (замечание EL05)', () => {
  const C = 4e-6;
  close(ser(C, C, C, C, C), C / 5, 1e-12);
  const cs = [1e-6, 2e-6, 5e-6];
  const cob = ser(...cs);
  assert.ok(cob < Math.min(...cs));
  const product = cs.reduce((a, b) => a * b, 1);
  assert.ok(!(cob < product), 'при C < 1 Ф произведение много меньше C_об');
});

test('c21: распределение напряжения на последовательных конденсаторах Uᵢ = U·C_об/Cᵢ (2 и 3 мкФ при 10 В → 6 и 4 В, q = 12 мкКл)', () => {
  const U = 10, cs = [2e-6, 3e-6];
  const cob = ser(...cs);
  const Ui = cs.map((c) => (U * cob) / c);
  close(Ui[0], 6, 1e-12);
  close(Ui[1], 4, 1e-12);
  close(Ui[0] + Ui[1], U, 1e-12);
  close(cob * U, 12e-6, 1e-12);
  close(cs[0] * Ui[0], cs[1] * Ui[1], 1e-12);
});

test('c15, c22–c23: C = εε₀S/d; W = q²/2C = CU²/2 = qU/2; w = W/V = εε₀E²/2 = σ²/2εε₀', () => {
  const eps = 2, S = 0.02, d = 0.001, U = 200;
  const C = (eps * eps0 * S) / d, q = C * U;
  const W = (C * U ** 2) / 2;
  close(q ** 2 / (2 * C), W, 1e-12);
  close((q * U) / 2, W, 1e-12);
  const E = U / d, sigma = q / S;
  close(W / (S * d), (eps * eps0 * E ** 2) / 2, 1e-12);
  close(W / (S * d), sigma ** 2 / (2 * eps * eps0), 1e-12);
  close(E, sigma / (eps * eps0), 1e-12);
});

test('c23: раздвигаем пластины вдвое — при U = const энергия уменьшается вдвое, при q = const — растёт вдвое', () => {
  const S = 0.01, d = 0.002, U = 100;
  const C1 = (eps0 * S) / d, C2 = (eps0 * S) / (2 * d);
  close((C2 * U ** 2) / 2 / ((C1 * U ** 2) / 2), 0.5, 1e-12);
  const q = C1 * U;
  close((q ** 2 / (2 * C2)) / (q ** 2 / (2 * C1)), 2, 1e-12);
});

test('c14: в среде с ε сила, напряжённость, энергия и потенциал уменьшаются в ε раз; C шара = 4πεε₀R', () => {
  const eps = 81, q = 1e-9, R = 0.1;
  const k = 1 / (4 * Math.PI * eps0);
  close((k * q) / (eps * R), q / (4 * Math.PI * eps0 * eps * R), 1e-12);
  close(q / ((k * q) / (eps * R)), 4 * Math.PI * eps0 * eps * R, 1e-12);
});

test('c19, c24: I = q/t = Ne/t = neυS — одно и то же для N электронов в объёме Sl, проходящих сечение за t = l/υ; j = I/S = neυ', () => {
  const n = 8.5e28, S = 1e-6, l = 2, v = 1e-4;
  const N = n * S * l, t = l / v;
  close((N * e0) / t, n * e0 * v * S, 1e-12);
  close((n * e0 * v * S) / S, n * e0 * v, 1e-12);
});

test('c25: при I(t) = kt + b заряд q = ∫I dt = Ī·Δt, Ī = (I₁ + I₂)/2', () => {
  const k = 0.4, b = 1, t1 = 2, t2 = 7, n = 100000;
  let q = 0;
  for (let i = 0; i < n; i++) { const t = t1 + ((i + 0.5) * (t2 - t1)) / n; q += (k * t + b) * ((t2 - t1) / n); }
  close(q, (((k * t1 + b) + (k * t2 + b)) / 2) * (t2 - t1), 1e-9);
});

test('c19: R = ρl/S и ρ = RS/l — взаимно обратные; удвоение длины удваивает R, удвоение сечения — уменьшает вдвое', () => {
  const rho = 1.7e-8, l = 10, S = 2e-6;
  const R = (rho * l) / S;
  close((R * S) / l, rho, 1e-12);
  close((rho * 2 * l) / S, 2 * R, 1e-12);
  close((rho * l) / (2 * S), R / 2, 1e-12);
});

// мост: узлы A (φ = U), B (0), M (между R1 и R2), N (между R3 и R4), R5 между M и N
const bridge = (R1: number, R2: number, R3: number, R4: number, R5: number, U = 10) => {
  // уравнения Кирхгофа для узлов M и N
  const a11 = 1 / R1 + 1 / R2 + 1 / R5, a12 = -1 / R5, b1 = U / R1;
  const a21 = -1 / R5, a22 = 1 / R3 + 1 / R4 + 1 / R5, b2 = U / R3;
  const det = a11 * a22 - a12 * a21;
  const phiM = (b1 * a22 - a12 * b2) / det, phiN = (a11 * b2 - a21 * b1) / det;
  return { I5: (phiM - phiN) / R5, phiM, phiN };
};

test('c26: мост Уитстона (замечание EL07) — при R₁R₄ = R₂R₃ ток через R₅ равен нулю при любом R₅, иначе не равен', () => {
  for (const R5 of [1, 10, 1000]) {
    assert.ok(Math.abs(bridge(2, 4, 3, 6, R5).I5) < 1e-12, `R5 = ${R5}`);
    assert.ok(Math.abs(bridge(5, 10, 1, 2, R5).I5) < 1e-12);
  }
  assert.ok(Math.abs(bridge(2, 4, 3, 5, 10).I5) > 1e-4);
});

test('c27: последовательные резисторы — Uᵢ = U·Rᵢ/R_об, сумма равна U', () => {
  const U = 12, rs = [2, 4, 6];
  const Rob = rs.reduce((a, b) => a + b);
  const Ui = rs.map((r) => (U * r) / Rob);
  close(Ui.reduce((a, b) => a + b), U, 1e-12);
  close(Ui[1], 4, 1e-12);
});

test('c29–c30: Q = UIt = I²Rt = U²t/R; последовательно P₁/P₂ = R₁/R₂, параллельно — R₂/R₁; 1 кВт·ч = 3,6·10⁶ Дж', () => {
  const R = 20, I = 3, t = 60, U = I * R;
  close(U * I * t, I ** 2 * R * t, 1e-12);
  close(U * I * t, (U ** 2 / R) * t, 1e-12);
  const R1 = 10, R2 = 30, Iser = 2;
  close((Iser ** 2 * R1) / (Iser ** 2 * R2), R1 / R2, 1e-12);
  const Up = 120;
  close((Up ** 2 / R1) / (Up ** 2 / R2), R2 / R1, 1e-12);
  close(1000 * 3600, 3.6e6, 1e-12);
  // c29: n одинаковых лампочек последовательно — P = U²/(nR)
  close(220 ** 2 / (8 * 100), (220 ** 2 / 100) / 8, 1e-12);
});

test('c30: электрочайники — при неизменном U параллельно t = (1/t₁ + 1/t₂)⁻¹, последовательно t = t₁ + t₂ (из Q = U²t/R)', () => {
  const U = 220, Q = 5e5, t1 = 300, t2 = 600;
  const R1 = (U ** 2 * t1) / Q, R2 = (U ** 2 * t2) / Q;
  const tPar = (Q * ((R1 * R2) / (R1 + R2))) / U ** 2;
  const tSer = (Q * (R1 + R2)) / U ** 2;
  close(tPar, 1 / (1 / t1 + 1 / t2), 1e-12);
  close(tSer, t1 + t2, 1e-12);
});

test('c31: лампы 100 и 25 Вт (220 В) последовательно — формулы конспекта совпадают с I²R: 4 и 16 Вт, P_об = 20 Вт', () => {
  const U0 = 220, P01 = 100, P02 = 25;
  const R1 = U0 ** 2 / P01, R2 = U0 ** 2 / P02, I = U0 / (R1 + R2);
  const P1 = P01 * (P02 / (P01 + P02)) ** 2, P2 = P02 * (P01 / (P01 + P02)) ** 2;
  close(P1, I ** 2 * R1, 1e-12);
  close(P2, I ** 2 * R2, 1e-12);
  close(P1, 4, 1e-12);
  close(P2, 16, 1e-12);
  close(1 / (1 / P01 + 1 / P02), P1 + P2, 1e-12);
  assert.ok(P1 < P01 && P2 < P02);
});

test('c31–c32: закон Ома для полной цепи — ε = U_внеш + U_внутр, U_внеш = εR/(R+r), η = R/(R+r), I_кз = ε/r', () => {
  const eps = 12, r = 0.5, R = 5.5;
  const I = eps / (R + r);
  close(I * R + I * r, eps, 1e-12);
  close(I * R, (eps * R) / (R + r), 1e-12);
  close((I * R) / eps, R / (R + r), 1e-12);
  close(eps / (1e-12 + r), eps / r, 1e-9);
  // c35: зарядка и разрядка источника
  const Iq = 2;
  close(eps - Iq * r, 11, 1e-12);
  close(eps + Iq * r, 13, 1e-12);
});

test('c33: P_полн = P_внеш + P_внутр; полезная мощность максимальна при R = r и равна ε²/4r (при этом η = 50 %)', () => {
  const eps = 9, r = 1.5;
  const P = (R: number) => (eps ** 2 / (R + r) ** 2) * R;
  for (const R of [0.5, 3, 10]) close(eps ** 2 / (R + r), P(R) + (eps ** 2 / (R + r) ** 2) * r, 1e-12);
  let best = 0, bestR = 0;
  for (let R = 0.001; R < 20; R += 0.001) if (P(R) > best) { best = P(R); bestR = R; }
  close(bestR, r, 1e-3);
  close(best, eps ** 2 / (4 * r), 1e-6);
  close(r / (r + r), 0.5, 1e-12);
});

test('c33: последовательные источники — ε_об = Σεᵢ (обратный — со знаком «−»), r_об = Σrᵢ; N одинаковых — Nε и Nr', () => {
  close(1.5 + 1.5 + 1.5, 4.5, 1e-12);
  close(1.5 + 1.5 - 1.5, 1.5, 1e-12);
  const N = 4, eps = 2, r = 0.3;
  close(Array(N).fill(eps).reduce((a, b) => a + b), N * eps, 1e-12);
  close(Array(N).fill(r).reduce((a, b) => a + b), N * r, 1e-12);
});

test('c34: параллельные источники — ε_об = (Σεᵢ/rᵢ)·r_об совпадает с узловым расчётом; без степени −1 r_об — не сопротивление (замечание EL09)', () => {
  const eps = [6, 4, 5], r = [1, 2, 0.5], R = 3;
  const rob = 1 / r.reduce((a, x) => a + 1 / x, 0);
  const eob = eps.reduce((a, e, i) => a + e / r[i], 0) * rob;
  // узловой потенциал V на нагрузке R: Σ(εᵢ − V)/rᵢ = V/R
  const V = eps.reduce((a, e, i) => a + e / r[i], 0) / (r.reduce((a, x) => a + 1 / x, 0) + 1 / R);
  close(V / R, eob / (R + rob), 1e-12);
  close(eob / rob, eps.reduce((a, e, i) => a + e / r[i], 0), 1e-12);
  // I_max об = Σ I_max i
  close(eob / rob, eps.reduce((a, e, i) => a + e / r[i], 0), 1e-12);
  // N одинаковых: r/N и ε
  const Nr = 1 / (1 / 0.6 + 1 / 0.6 + 1 / 0.6);
  close(Nr, 0.6 / 3, 1e-12);
  close(((2 / 0.6) * 3) * Nr, 2, 1e-12);
  // неправильное включение второго источника
  const eobWrong = (eps[0] / r[0] - eps[1] / r[1] + eps[2] / r[2]) * rob;
  const Vw = (eps[0] / r[0] - eps[1] / r[1] + eps[2] / r[2]) / (r.reduce((a, x) => a + 1 / x, 0) + 1 / R);
  close(Vw / R, eobWrong / (R + rob), 1e-12);
  // запись без −1 даёт Σ1/rᵢ = 3,5 См вместо 1/3,5 Ом
  assert.notEqual(r.reduce((a, x) => a + 1 / x, 0), rob);
});

test('c35: конденсатор не пропускает постоянный ток; параллельно R: U_c = εR/(R+r), q = CεR/(R+r)', () => {
  const eps = 10, r = 1, R = 4, C = 2e-6;
  const I = eps / (R + r);
  close(C * I * R, (C * eps * R) / (R + r), 1e-12);
  close(C * eps, 2e-5, 1e-12); // без нагрузки: I = 0, U_c = ε
});

test('c36, c38: R(t) = R₀(1 + αt) у металла растёт, R₀(1 − αt) у электролита убывает — линейно', () => {
  const R0 = 50, a = 0.004;
  const met = (t: number) => R0 * (1 + a * t), el = (t: number) => R0 * (1 - a * 0.5 * t);
  close(met(100) - met(50), met(50) - met(0), 1e-12);
  assert.ok(met(100) > met(0) && el(100) < el(0));
});

test('c37–c38: законы Фарадея — m = kIt, k = A/(Fz); A подставляется в кг/моль, иначе k завышен в 1000 раз (замечание EL12)', () => {
  const A_gmol = 27, z = 3, F = 96500, I = 2, t = 3600;
  const k = A_gmol / 1000 / (F * z);
  const m = k * I * t;
  close(m, ((A_gmol / 1000) * I * t) / (F * z), 1e-12);
  close((A_gmol / (F * z)) / k, 1000, 1e-12);
  close(k * (2 * I) * t, 2 * m, 1e-12);
});

test('c39–c40: соотношение примесей 10⁹ : 1 = 10²³ : 10¹⁴', () => {
  close(1e23 / 1e14, 1e9, 1e-12);
});

// ——— Конспект «Атомная и ядерная физика» (a01–a08) и дополнения из интернета ———

test('a03: состав ядра — ³⁹₁₉K: 20 нейтронов; ядро из 3p + 4n: A = 7, q = 3e; m_p ≈ m_n ≈ 1 а.е.м.', () => {
  assert.equal(39 - 19, 20);
  assert.equal(3 + 4, 7);
  close(1.68e-27 / 1.67e-27, 1, 0.01);
});

test('a04: изотопы — Z одинаково, изобары — A, изотоны — A − Z (³H и ⁴He по 2 нейтрона); бор с q = −2e — 7 электронов (AT05)', () => {
  const nuc = { H1: [1, 1], H2: [2, 1], H3: [3, 1], He4: [4, 2], Co59: [59, 27], Ni59: [59, 28] } as Record<string, [number, number]>;
  assert.equal(nuc.H1[1], nuc.H3[1]);
  assert.equal(nuc.Co59[0], nuc.Ni59[0]);
  assert.equal(nuc.H3[0] - nuc.H3[1], nuc.He4[0] - nuc.He4[1]);
  assert.equal(5 - -2, 7);
});

test('a05: дефект массы Δm = Zm_p + (A − Z)m_n − m_я и энергия связи E = Δmc²; ε = E/A', () => {
  const dm = 2 * 1.67e-27 + 2 * 1.68e-27 - 6.64e-27;
  close(dm, 6e-29, 1e-6);
  close(5e-29 * (3e8) ** 2, 4.5e-12, 1e-12);
  close(28 / 4, 7, 1e-12);
});

test('a06: в реакции с торием сохраняются A и Z (233 = 233, 90 = 90); найденное ядро — Z = 8, A = 47 (AT10)', () => {
  const left = { A: 232 + 1, Z: 90 + 0 };
  const right = [[108, 47], [73, 32], [1, 1], [4, 2]];
  const A = left.A - right.reduce((a, r) => a + r[0], 0);
  const Z = left.Z - right.reduce((a, r) => a + r[1], 0);
  assert.deepEqual([A, Z], [47, 8]);
});

test('a07: α-распад (A − 4, Z − 2), β⁻ (Z + 1), β⁺ (Z − 1), γ (без изменений); U-238 → α → 2β⁻ → U-234', () => {
  const alpha = ([A, Z]: number[]) => [A - 4, Z - 2];
  const betaM = ([A, Z]: number[]) => [A, Z + 1];
  const betaP = ([A, Z]: number[]) => [A, Z - 1];
  assert.deepEqual(alpha([226, 88]), [222, 86]);
  assert.deepEqual(betaM([14, 6]), [14, 7]);
  assert.deepEqual(betaP(betaM([14, 6])), [14, 6]);
  assert.deepEqual(betaM(betaM(alpha([238, 92]))), [234, 92]);
});

test('a08: N = N₀·2^(−t/T) = N₀e^(−λt) при λ = ln2/T; A = −dN/dt = λN = (N₀/T)·2^(−t/T)·ln2; τ = T/ln2 = 1/λ; ΔN = N₀(1 − 2^(−t/T))', () => {
  const N0 = 8000, T = 2;
  const N = (t: number) => N0 * 2 ** (-t / T);
  const lam = Math.LN2 / T;
  for (const t of [0, 1.3, 6]) close(N(t), N0 * Math.exp(-lam * t), 1e-12);
  for (const t of [0.5, 3]) {
    const h = 1e-6;
    const act = -(N(t + h) - N(t - h)) / (2 * h);
    close(act, lam * N(t), 1e-6);
    close(act, (N0 / T) * 2 ** (-t / T) * Math.LN2, 1e-6);
  }
  close(T / Math.LN2, 1 / lam, 1e-12);
  close(N(6), 1000, 1e-12);
  close(N0 - N(6), N0 * (1 - 2 ** (-3)), 1e-12);
  close(1600 * 2 ** (-12 / 3), 100, 1e-12);
});

test('a02 (из интернета): уровни водорода E_n = −13,6/n² эВ согласуются с формулой Ридберга (hR = 13,6 эВ); переход 3 → 2 — 1,89 эВ, λ ≈ 656 нм', () => {
  const h = 6.62e-34, R = 3.29e15, e = 1.6e-19, c = 3e8;
  close((h * R) / e, 13.6, 0.003);
  const E32 = 13.6 * (1 / 4 - 1 / 9);
  close(E32, 1.889, 1e-3);
  close((h * R * (1 / 4 - 1 / 9)) / e, E32, 0.003);
  close((h * c) / (E32 * e), 657e-9, 0.005);
  close(13.6 * (1 - 1 / 4), 10.2, 1e-12);
  assert.equal(3 ** 2, 9);
});

test('a07 (из интернета): эквивалентная доза H = W_R·D; D = E/m', () => {
  close(0.1 / 50, 0.002, 1e-12);
  close(20 * 1e-3, 0.02, 1e-12);
  close(2.58e-4 * 1, 2.58e-4, 1e-12);
});

test('статика (из интернета): правило моментов F₁d₁ = F₂d₂ — сумма моментов с учётом знака равна нулю', () => {
  const F1 = 30, d1 = 0.2, F2 = 10;
  const d2 = (F1 * d1) / F2;
  close(d2, 0.6, 1e-12);
  close(F1 * d1 - F2 * d2, 0, 1e-12);
  close((600 * 0.3) / 1.5, 120, 1e-12);
  close(20 * 0.25, 5, 1e-12);
});

test('o07 (из интернета): решётка d·sinφ = kλ — красный отклоняется сильнее фиолетового; k_max = ⌊d/λ⌋', () => {
  const d = 2e-6;
  const ang = (lam: number, k = 1) => Math.asin((k * lam) / d);
  assert.ok(ang(700e-9) > ang(400e-9));
  close((ang(500e-9) * 180) / Math.PI, 14.4775, 1e-4);
  assert.equal(Math.floor(d / 600e-9), 3);
  assert.ok((4 * 600e-9) / d > 1, 'четвёртого порядка нет: sinφ > 1');
  close(1e-3 / 500, 2e-6, 1e-12);
});

test('o05 (из интернета): при разности хода (2k + 1)λ/2 волны гасят друг друга — результирующая амплитуда |A₁ − A₂|', () => {
  const lam = 600e-9, A1 = 3, A2 = 2;
  for (const k of [0, 1, 4]) {
    const dx = ((2 * k + 1) * lam) / 2;
    let mx = 0;
    for (let i = 0; i < 2000; i++) {
      const t = (i / 2000) * 2 * Math.PI;
      mx = Math.max(mx, Math.abs(A1 * Math.sin(t) + A2 * Math.sin(t - (2 * Math.PI * dx) / lam)));
    }
    close(mx, Math.abs(A1 - A2), 1e-4);
  }
});

test('e26 (из интернета): резонанс напряжений — ток наибольший при ω₀ = 1/√(LC), где X_L = X_C и Z = R', () => {
  const L = 0.1, C = 1e-5, R = 20, U = 100;
  const I = (w: number) => U / Math.sqrt(R ** 2 + (w * L - 1 / (w * C)) ** 2);
  let best = 0, bw = 0;
  for (let w = 100; w < 5000; w += 0.5) if (I(w) > best) { best = I(w); bw = w; }
  close(bw, 1 / Math.sqrt(L * C), 1e-3);
  close(best, U / R, 1e-6);
  close(bw * L, 1 / (bw * C), 1e-3);
});

test('c28 (из интернета): шунт R_ш = R_A/(n − 1) пропускает через амперметр I/n; добавочное R_д = R_V(n − 1) оставляет на вольтметре U/n', () => {
  const RA = 0.9, n = 10, I = 10;
  const Rsh = RA / (n - 1);
  close(I * (Rsh / (RA + Rsh)), I / n, 1e-12);
  const RV = 2000, m = 5, U = 50;
  const Rd = RV * (m - 1);
  close(U * (RV / (RV + Rd)), U / m, 1e-12);
});

test('c27 (из интернета): соединение проводников — последовательно R₁ + R₂, параллельно R₁R₂/(R₁ + R₂); токи обратно пропорциональны R', () => {
  close(4 * 6 / (4 + 6), 1 / (1 / 4 + 1 / 6), 1e-12);
  const U = 10, R1 = 2, R2 = 8;
  close(U / R1 / (U / R2), R2 / R1, 1e-12);
  close(5 * R2 / (R1 + R2), 4, 1e-12);
  close(100 / 5, 1 / (5 / 100), 1e-12);
});

test('p06R: средняя скорость равноускоренного движения (υ₀ + υ)/2 совпадает с S/t из S = υ₀t + at²/2', () => {
  const v0 = 4, a = 1.5, t = 4;
  const v = v0 + a * t;
  close((v0 * t + (a * t * t) / 2) / t, (v0 + v) / 2, 1e-12);
});

test('p21L (из интернета): с ρ_кер ≈ 800 кг/м³ столб керосина ≈ 12,9 м — согласуется с 12,8 м конспекта; из 12,8 м ρ ≈ 808 кг/м³', () => {
  close(101396 / (800 * 9.81), 12.92, 1e-3);
  close(101396 / (9.81 * 12.8), 808, 1e-3);
});

// ——— Фото «Дифракция» (d01–d02) и дополнение статики из интернета (22.10.2026) ———

test('d02: sin φ = x/√(L² + x²) — тот же угол, что tg φ = x/L; d·x/√(L² + x²) = kλ даёт x для данного k', () => {
  const L = 1.2, x = 0.3;
  close(x / Math.sqrt(L * L + x * x), Math.sin(Math.atan(x / L)), 1e-12);
  const d = 1e-3 / 500, lam = 600e-9, k = 1;
  const s = (k * lam) / d;
  const xk = L * Math.tan(Math.asin(s));
  close((d * xk) / Math.sqrt(L * L + xk * xk), k * lam, 1e-9);
});

test('d01–d02: d = l₀/N, K = [d/λ], N = 2[d/λ] + 1 — пока d/λ не целое; при целом d/λ максимум K шёл бы под 90° (замечание DF03)', () => {
  const d = 1e-3 / 400, lam = 600e-9; // d/λ ≈ 4,17
  const K = Math.floor(d / lam);
  assert.equal(K, 4);
  assert.ok((K * lam) / d < 1 && ((K + 1) * lam) / d > 1);
  assert.equal(2 * K + 1, 9);
  // d/λ = 5 ровно: sin φ = 1 для k = 5 — такого максимума на экране нет
  const d2 = 5 * lam;
  assert.equal((5 * lam) / d2, 1);
  const visible = [...Array(11).keys()].map((i) => i - 5).filter((k) => Math.abs((k * lam) / d2) < 1).length;
  assert.equal(visible, 9);
  assert.equal(2 * Math.floor(d2 / lam) + 1, 11);
});

test('статика (из интернета): рычаг с собственным весом и система рычагов — выигрыш перемножается', () => {
  // стержень 1 м, 2 кг, опора в 0,3 м от левого конца: m₁g·0,3 = mg·0,2
  close((2 * g * 0.2) / (g * 0.3), 4 / 3, 1e-12);
  // два рычага: выигрыши 5 и 3, груз 900 Н
  const F2 = 900 * 0.2 / 0.6; // сила, которую передаёт второй рычаг первому
  close(F2 * 0.1 / 0.5, 60, 1e-12);
  close(900 / (5 * 3), 60, 1e-12);
});

test('блоки (из интернета): подвижный блок — F = P/2, s = 2h; полиспаст на n ветвях — F = P/n, s = nh; золотое правило F·s = P·h', () => {
  const P = 600, h = 1.5;
  for (const n of [1, 2, 4, 6]) {
    const F = P / n, s = n * h;
    close(F * s, P * h, 1e-12);
  }
  // подвижный блок с весом P₀ — две ветви держат P + P₀
  close((400 + 20) / 2, 210, 1e-12);
  // подвижный блок как рычаг: плечи 2r и r
  const r = 0.1;
  close((P * r) / (2 * r), P / 2, 1e-12);
});

test('наклонная плоскость (из интернета): F = mg sin α; с трением η = 1/(1 + μ ctg α) = A_пол/A_полн', () => {
  const m = 50, l = 5, h = 1;
  close(m * g * h / l, 100, 1e-12);
  close((m * g * h) / (125 * l) * 100, 80, 1e-12);
  const a = Math.PI / 6, mu = 0.2;
  const F = m * g * (Math.sin(a) + mu * Math.cos(a));
  const len = h / Math.sin(a);
  close((m * g * h) / (F * len), 1 / (1 + mu / Math.tan(a)), 1e-12);
  close(1 / (1 + 0.2 * Math.sqrt(3)), 0.743, 1e-3);
});

test('центр масс (из интернета): x_c = Σmᵢxᵢ/Σmᵢ; для двух грузов l₁/l₂ = m₂/m₁; брусок опрокидывается при tg α > a/(2h_c)', () => {
  const xc = (2 * 0 + 6 * 0.8) / 8;
  close(xc, 0.6, 1e-12);
  close(xc / (0.8 - xc), 6 / 2, 1e-12);
  // момент сил тяжести относительно центра масс равен нулю
  close(2 * g * xc, 6 * g * (0.8 - xc), 1e-12);
  close((1 * 0 + 2 * 4 + 1 * 0) / 4, 2, 1e-12);
  close((1 * 0 + 2 * 0 + 1 * 4) / 4, 1, 1e-12);
  // опрокидывание: вертикаль через центр тяжести проходит через край основания
  const a = 0.2, hc = 0.3;
  const alpha = Math.atan(a / (2 * hc));
  close(hc * Math.sin(alpha), (a / 2) * Math.cos(alpha), 1e-12);
  close((alpha * 180) / Math.PI, 18.43, 1e-3);
});

test('сложные задачи на равновесие (из интернета): балка на двух опорах, стержень на шарнире с тросом, лестница у гладкой стены', () => {
  // балка 4 м, 100 кг, груз 200 кг в 1 м от A
  const NB = (1000 * 2 + 2000 * 1) / 4;
  close(NB, 1000, 1e-12);
  close(3000 - NB, 2000, 1e-12);
  // стержень 10 кг, трос под 30°: T·L·sin30° = mg·L/2
  close((10 * g) / (2 * Math.sin(Math.PI / 6)), 100, 1e-9);
  // лестница: моменты относительно нижнего конца, μ_min = 1/(2 tg α)
  const m = 20, L = 4, a = Math.PI / 3;
  const Nw = (m * g * (L / 2) * Math.cos(a)) / (L * Math.sin(a));
  close(Nw / (m * g), 1 / (2 * Math.tan(a)), 1e-12);
  close(1 / (2 * Math.tan(a)), 0.2887, 1e-3);
  close(1 / (2 * Math.tan(Math.PI / 4)), 0.5, 1e-12);
});
