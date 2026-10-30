"""Иллюстрации к конспекту «Атомная и ядерная физика» (стр. a01–a08) и к темам, дополненным из интернета
(статика, дифракционная решётка, шкала электромагнитных волн, резонанс в цепи RLC, соединение проводников)."""
import math
import random
from figlib import *  # noqa: F401,F403
from figs_elec import resistor, battery, phase_op  # noqa: F401


def nucleon(x, y, kind, r=6.5, extra=''):
    """Нуклон: протон — красный «p», нейтрон — серый «n»."""
    cls = 'f-red' if kind == 'p' else 'f-mute'
    return f'<g{extra}><circle class="{cls}" cx="{f(x)}" cy="{f(y)}" r="{r}"/>' + text(x, y + 3, kind, 't-ws') + '</g>'


def nucleus(cx, cy, ps, ns, r=6.5, extra=''):
    """Плотная упаковка нуклонов вокруг центра (p и n чередуются)."""
    kinds = []
    p, n = ps, ns
    while p or n:
        if p:
            kinds.append('p'); p -= 1
        if n:
            kinds.append('n'); n -= 1
    out = []
    k = len(kinds)
    pos = [(0, 0)] if k == 1 else []
    if k > 1:
        ring, idx = 0, 0
        while len(pos) < k:
            cnt = 1 if ring == 0 else 6 * ring
            for j in range(cnt):
                if len(pos) >= k:
                    break
                a = 2 * math.pi * j / cnt + ring * 0.4
                pos.append((ring * r * 1.6 * math.cos(a), ring * r * 1.6 * math.sin(a)))
            ring += 1
    for (dx, dy), kind in zip(pos, kinds):
        out.append(nucleon(cx + dx, cy + dy, kind, r))
    return f'<g{extra}>' + ''.join(out) + '</g>'


def wave_path(x1, x2, y, amp, lam, steps=60):
    pts = []
    for i in range(steps + 1):
        x = x1 + (x2 - x1) * i / steps
        pts.append(f'{f(x)},{f(y - amp * math.sin(2 * math.pi * (x - x1) / lam))}')
    return 'M' + 'L'.join(pts)


# ───────────────────────────── атом ─────────────────────────────

@fig('rutherford', 'Опыт Резерфорда: пучок α-частиц направляют на тонкую золотую фольгу; большинство частиц проходит почти без отклонения, немногие отклоняются, а единицы отлетают назад — ядро очень мало', 360, 210)
def rutherford():
    dur = 4
    fx = 205
    o = ['<rect class="f-soft" x="10" y="78" width="34" height="54" rx="4"/>', text(27, 110, 'α', 't-acc')]
    o.append(f'<path class="s-mute" d="M{fx},26V184" stroke-width="5"/>')
    o.append(text(fx, 18, 'золотая фольга', 't-s'))
    for y in range(34, 184, 16):
        o.append(f'<circle class="f-red" cx="{fx}" cy="{y}" r="2"/>')
    paths = [
        ('M44,92H350', 0.0), ('M44,118H350', 0.6), ('M44,104H350', 1.2), ('M44,126H350', 1.8), ('M44,86H350', 2.4),
        (f'M44,99L{fx - 6},100Q{fx + 6},101 {fx + 24},86L350,40', 3.0),
        (f'M44,109L{fx - 10},110Q{fx - 2},111 {fx - 18},122L60,178', 3.4),
    ]
    for k, (d, beg) in enumerate(paths):
        o.append(f'<path id="rutherford-p{k}" d="{d}" fill="none"/>')
        cls = 'f-acc' if k < 5 else 'f-red'
        o.append(f'<circle class="{cls}" r="4.5"><animateMotion dur="{dur}s" begin="-{f(beg)}s" repeatCount="indefinite"><mpath href="#rutherford-p{k}"/></animateMotion></circle>')
    o.append(f'<path class="s-mute" d="M{fx + 24},86L350,40" stroke-width="1" stroke-dasharray="3 4"/>')
    o.append(f'<path class="s-mute" d="M{fx - 18},122L60,178" stroke-width="1" stroke-dasharray="3 4"/>')
    o.append(text(300, 150, 'почти без', 't-s') + text(300, 164, 'отклонения', 't-s'))
    o.append(text(340, 30, 'редко', 't-red', 'end') + text(110, 200, '≈ 1 из 10 000 — назад', 't-red'))
    return ''.join(o)


@fig('bohr-levels', 'Постулаты Бора: атом водорода переходит с уровня 3 на уровень 2 и излучает фотон hν = E₃ − E₂ ≈ 1,89 эВ; поглотив фотон 10,2 эВ, он переходит с уровня 1 на уровень 2', 360, 230)
def bohr_levels():
    dur = 8
    # уровни: y растёт вниз; E_n = −13,6/n² → n = 1 внизу
    ys = {n: 194 - (1 - 1 / n ** 2) * 160 for n in (1, 2, 3)}
    lab = {1: '−13,6 эВ', 2: '−3,4 эВ', 3: '−1,51 эВ'}
    o = []
    for n, y in ys.items():
        o.append(f'<path class="s-ink" d="M110,{f(y)}H300" stroke-width="{2.6 if n == 1 else 1.8}"/>')
        o.append(text(104, y + 4, f'n = {n}', 't-s', 'end'))
        o.append(text(306, y + 4, lab[n], 't-s', 'start'))
    o.append(f'<path class="s-mute" d="M110,{f(194 - 160)}H300" stroke-width="1" stroke-dasharray="4 4"/>' + text(306, 194 - 160 + 4, '0 (n → ∞)', 't-s', 'start'))
    y1, y2, y3 = ys[1], ys[2], ys[3]
    # фаза 1 (0–0,45): излучение 3 → 2
    o.append(f'<circle class="f-acc" cx="160" r="6">'
             f'<animate attributeName="cy" values="{nums([y3, y3, y2, y2, y3])}" keyTimes="0;0.12;0.2;0.46;1" dur="{dur}s" repeatCount="indefinite"/>'
             f'{phase_op("1;0;1", "0;0.47;0.98", dur)}</circle>')
    wy = (y2 + y3) / 2
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.2;0.46", dur)}'
             f'<path class="s-red" d="{wave_path(0, 90, 0, 6, 18)}" stroke-width="2.4">'
             f'<animateTransform attributeName="transform" type="translate" values="168 {f(wy)};240 {f(wy)}" keyTimes="0;1" dur="{f(dur * 0.26)}s" begin="0s" repeatCount="indefinite"/></path></g>')
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.2;0.47", dur)}' + text(180, 20, 'излучение: hν = E_3 − E_2 ≈ 1,89 эВ', 't-red') + '</g>')
    # фаза 2 (0,5–1): поглощение 1 → 2
    o.append(f'<circle class="f-acc" cx="250" r="6" opacity="0">'
             f'<animate attributeName="cy" values="{nums([y1, y1, y1, y2, y2])}" keyTimes="0;0.5;0.74;0.82;1" dur="{dur}s" repeatCount="indefinite"/>'
             f'{phase_op("0;1;0", "0;0.5;0.98", dur)}</circle>')
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.55;0.74", dur)}'
             f'<path class="s-grn" d="{wave_path(0, 70, 0, 6, 14)}" stroke-width="2.4">'
             f'<animateTransform attributeName="transform" type="translate" values="120 {f((y1 + y2) / 2 + 40)};176 {f((y1 + y2) / 2 + 40)}" keyTimes="0;1" dur="{f(dur * 0.19)}s" repeatCount="indefinite"/></path></g>')
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.52;0.98", dur)}' + text(180, 20, 'поглощение: hν = E_2 − E_1 = 10,2 эВ', 't-grn') + '</g>')
    return ''.join(o)


# ───────────────────────────── ядро ─────────────────────────────

@fig('nucleus-isotopes', 'Изотопы водорода: у ¹H, ²H и ³H по одному протону, а нейтронов 0, 1 и 2; затем изотоны ³H и ⁴He — у обоих по два нейтрона', 360, 200)
def nucleus_isotopes():
    dur = 8
    o = [f'<g>{phase_op("1;0;1", "0;0.5;0.98", dur)}']
    for i, (a, nn) in enumerate([(1, 0), (2, 1), (3, 2)]):
        cx = 70 + i * 110
        o.append(nucleus(cx, 90, 1, nn, 9))
        o.append(text(cx, 148, f'{"¹²³"[a - 1]}H: 1p + {nn}n', 't'))
    o.append(text(180, 184, 'изотопы: протонов поровну (Z = 1), нейтронов разное число', 't-s'))
    o.append(text(180, 30, 'изотопы водорода', 't-red') + '</g>')
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.5;0.98", dur)}')
    o.append(nucleus(110, 90, 1, 2, 9) + text(110, 148, '³H: 1p + 2n', 't'))
    o.append(nucleus(250, 90, 2, 2, 9) + text(250, 148, '⁴He: 2p + 2n', 't'))
    o.append(text(180, 184, 'изотоны: нейтронов поровну (по 2)', 't-s'))
    o.append(text(180, 30, 'изотоны', 't-acc') + '</g>')
    return ''.join(o)


@fig('mass-defect', 'Дефект массы: два протона и два нейтрона по отдельности тяжелее, чем ядро гелия; при соединении нуклонов выделяется энергия связи E = Δmc²', 360, 210)
def mass_defect():
    dur = 6
    kt = '0;0.2;0.45;0.85;1'
    start = [(40, 60), (80, 60), (40, 100), (80, 100)]
    end = [(250 - 6, 74), (250 + 6, 74), (250, 84), (250, 64)]
    kinds = ['p', 'p', 'n', 'n']
    o = []
    for (x0, y0), (x1, y1), kd in zip(start, end, kinds):
        xy = [(0, 0), (0, 0), (x1 - x0, y1 - y0), (x1 - x0, y1 - y0), (0, 0)]
        vs = ';'.join(f'{f(x)} {f(y)}' for x, y in xy)
        o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{vs}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
                 + nucleon(x0, y0, kd, 9) + '</g>')
    o.append(f'<circle class="f-red-soft" cx="250" cy="74" r="10" opacity="0"><animate attributeName="r" values="10;10;10;48;10" keyTimes="0;0.4;0.45;0.6;1" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0;0;0.9;0;0" keyTimes="0;0.43;0.45;0.62;1" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.45;0.85", dur)}' + text(250, 140, 'выделяется E = Δmc²', 't-red') + '</g>')
    # полоски масс
    o.append(text(20, 172, 'm(2p + 2n)', 't-s', 'start') + '<rect class="f-mute" x="110" y="162" width="200" height="12" rx="3"/>')
    o.append(text(20, 194, 'm(ядра)', 't-s', 'start') + '<rect class="f-acc" x="110" y="184" height="12" rx="3" width="200">'
             f'<animate attributeName="width" values="200;200;186;186;200" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></rect>')
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.45;0.85", dur)}<path class="s-red" d="M296,198V160" stroke-width="1.5" stroke-dasharray="3 3"/>' + text(318, 194, 'Δm', 't-red', 'start') + '</g>')
    o.append(text(60, 30, 'нуклоны порознь', 't-s') + text(250, 30, 'ядро ⁴He', 't-s'))
    return ''.join(o)


# ─────────────────────── реакции и распад ───────────────────────

@fig('decay-shift', 'Виды распада и сдвиг в таблице Менделеева: α-распад — на 2 клетки к началу, β⁻ — на 1 клетку к концу, β⁺ — на 1 клетку к началу, γ — элемент остаётся на месте', 360, 210)
def decay_shift():
    dur = 12
    cw, y0, x0 = 40, 150, 40
    o = []
    for i in range(7):
        o.append(f'<rect class="f-paper s-ink" x="{x0 + i * cw}" y="{y0}" width="{cw}" height="34" stroke-width="1.4"/>')
        o.append(text(x0 + i * cw + cw / 2, y0 + 50, f'Z{["−3", "−2", "−1", "", "+1", "+2", "+3"][i]}', 't-s'))
    home = x0 + 3 * cw + cw / 2
    # фазы по 0,25: α, β⁻, β⁺, γ
    shifts = [-2, 1, -1, 0]
    names = [('α-распад: A − 4, Z − 2', 't-red'), ('β⁻-распад: Z + 1, вылетают e⁻ и антинейтрино', 't-acc'),
             ('β⁺-распад: Z − 1, вылетают e⁺ и нейтрино', 't-grn'), ('γ-распад: A и Z не меняются', 't')]
    xs, kts = [], []
    for k, s in enumerate(shifts):
        a = k * 0.25
        xs += [home, home, home + s * cw, home + s * cw]
        kts += [a, a + 0.08, a + 0.14, a + 0.24]
    xs.append(home); kts.append(1)
    o.append(f'<rect class="f-red-soft" y="{y0 + 2}" width="{cw - 4}" height="30" rx="4">'
             f'<animate attributeName="x" values="{nums([x - cw / 2 + 2 for x in xs])}" keyTimes="{";".join(f(t) for t in kts)}" dur="{dur}s" repeatCount="indefinite"/></rect>')
    o.append(f'<text class="t" y="{y0 + 22}" text-anchor="middle">X<animate attributeName="x" values="{nums(xs)}" keyTimes="{";".join(f(t) for t in kts)}" dur="{dur}s" repeatCount="indefinite"/></text>')
    # ядро и вылетающая частица
    o.append(nucleus(180, 74, 5, 6, 6))
    emit = [('α', 'f-red'), ('e⁻', 'f-acc'), ('e⁺', 'f-grn')]
    for k, (lab, cls) in enumerate(emit):
        a = k * 0.25
        o.append(f'<g opacity="0">{phase_op("0;1;0", f"0;{f(a + 0.02)};{f(a + 0.24)}", dur)}'
                 f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;120 6;120 6" keyTimes="0;{f(a + 0.03)};{f(a + 0.14)};1" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<circle class="{cls}" cx="200" cy="70" r="9"/>' + text(200, 74, lab, 't-ws') + '</g></g>')
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.77;0.99", dur)}<path class="s-red" d="{wave_path(200, 320, 60, 6, 14)}" stroke-width="2.4"/>' + text(330, 52, 'γ', 't-red') + '</g>')
    for k, (t, cls) in enumerate(names):
        a = k * 0.25
        o.append(f'<g opacity="0">{phase_op("0;1;0", f"0;{f(a)};{f(a + 0.25)}", dur)}' + text(180, 24, t, cls) + '</g>')
    return ''.join(o)


@fig('half-life', 'Закон радиоактивного распада: за каждый период полураспада T остаётся половина ядер — N₀, N₀/2, N₀/4, N₀/8 …; точки-ядра гаснут в случайном порядке, а их число следует кривой N = N₀·2^(−t/T)', 360, 220)
def half_life():
    dur = 10
    gx, gy, w, hgt = 40, 186, 190, 150
    Tpx = w / 4
    o = [arrow(gx, gy, gx + w + 14, gy, 's-ink', 'f-ink', 1.4, 6), arrow(gx, gy, gx, gy - hgt - 14, 's-ink', 'f-ink', 1.4, 6),
         text(gx - 6, gy - hgt + 4, 'N₀', 't-s', 'end'), text(gx + w + 10, gy + 16, 't', 't', 'end'), text(gx + 8, gy - hgt - 16, 'N', 't', 'start')]
    pts = 'L'.join(f'{f(gx + w * u)},{f(gy - hgt * 2 ** (-4 * u))}' for u in lin(0, 1, 60))
    o.append(f'<path class="s-acc" d="M{pts}" stroke-width="2.4" fill="none"/>')
    for k in (1, 2, 3):
        x = gx + Tpx * k
        y = gy - hgt * 2 ** (-k)
        o.append(f'<path class="s-mute" d="M{f(x)},{gy}V{f(y)}H{gx}" stroke-width="1" stroke-dasharray="3 4"/>')
        o.append(text(x, gy + 14, f'{k}T' if k > 1 else 'T', 't-s'))
        o.append(text(gx - 6, y + 4, f'N₀/{2 ** k}', 't-s', 'end'))
    us = lin(0, 1, 41)
    o.append(f'<circle class="f-red" r="5">{anims(dur, cx=[gx + w * u for u in us], cy=[gy - hgt * 2 ** (-4 * u) for u in us])}</circle>')
    # 16 «ядер»: гаснут по закону — к T осталось 8, к 2T — 4, к 3T — 2, к 4T — 1
    rnd = random.Random(7)
    order = list(range(16)); rnd.shuffle(order)
    decay_t = []
    for j in range(16):
        remain_after = 16 - (j + 1)  # после распада j-го ядра
        t = -math.log2(max(remain_after, 0.5) / 16) / 4  # доля полного времени (4T)
        decay_t.append(min(t, 0.98))
    for j, idx in enumerate(order):
        x = 262 + (idx % 4) * 22
        y = 60 + (idx // 4) * 22
        t = decay_t[j]
        o.append(f'<circle class="f-acc" cx="{x}" cy="{y}" r="7"><animate attributeName="opacity" values="1;1;0.15;0.15" keyTimes="0;{f(max(t - 0.005, 0.001))};{f(t)};1" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(text(295, 160, 'нераспавшиеся', 't-s') + text(295, 174, 'ядра', 't-s'))
    return ''.join(o)


@fig('penetration', 'Проникающая способность: α-частицы задерживает лист бумаги, β-частицы — несколько миллиметров алюминия, γ-излучение ослабляет только толстый слой свинца', 360, 200)
def penetration():
    dur = 1.2
    o = ['<rect class="f-soft" x="8" y="50" width="30" height="110" rx="4"/>', text(23, 110, '☢', 't')]
    walls = [(110, 4, 'f-mute', 'бумага'), (190, 12, 'f-acc', 'алюминий'), (270, 34, 'f-ink', 'свинец')]
    for x, wd, cls, lab in walls:
        o.append(f'<rect class="{cls}" x="{x}" y="34" width="{wd}" height="136" rx="2" opacity="0.75"/>' + text(x + wd / 2, 188, lab, 't-s'))
    rays = [(70, 110, 'red', 'α'), (105, 190, 'acc', 'β'), (140, 352, 'grn', 'γ')]
    for y, xend, c, lab in rays:
        if c == 'grn':
            o.append(f'<path class="s-grn" d="M38,{y}H270" stroke-width="3" stroke-dasharray="8 6">{flow(dur, 14, True)}</path>')
            o.append(f'<path class="s-grn" d="M304,{y}H352" stroke-width="3" stroke-dasharray="8 6" opacity="0.35">{flow(dur, 14, True)}</path>')
        else:
            o.append(f'<path class="s-{c}" d="M38,{y}H{xend}" stroke-width="3" stroke-dasharray="8 6">{flow(dur, 14, True)}</path>')
        o.append(text(52, y - 8, lab, f't-{c}'))
    o.append(text(352, 128, 'слабее', 't-s', 'end'))
    return ''.join(o)


# ───────────────────────────── статика ─────────────────────────────

@fig('lever', 'Правило моментов: груз F₂ = 10 Н двигают вдоль рычага; рычаг встаёт горизонтально, когда F₁d₁ = F₂d₂ (30 Н · 0,2 м = 10 Н · 0,6 м)', 360, 210)
def lever():
    dur = 8
    px, py = 150, 120
    scale = 240  # 1 м = 240 px
    d1 = 0.2
    F1, F2 = 30, 10
    ds = [0.3, 0.45, 0.6, 0.6, 0.75, 0.6, 0.6, 0.3]
    kt = '0;0.18;0.34;0.5;0.66;0.8;0.92;1'
    angs = [max(-12, min(12, -(F2 * d - F1 * d1) * 6)) for d in ds]  # наклон: + — по часовой
    o = [f'<path class="f-mute" d="M{px - 14},{py + 32}L{px},{py}L{px + 14},{py + 32}Z"/>', '<path class="s-mute" d="M60,152H300" stroke-width="2"/>']
    rv = ';'.join(f'{f(-a)} {px} {py}' for a in angs)
    o.append(f'<g><animateTransform attributeName="transform" type="rotate" values="{rv}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>')
    o.append(f'<rect class="f-ink" x="{px - d1 * scale - 20}" y="{py - 4}" width="{d1 * scale + 0.8 * scale + 20}" height="8" rx="3"/>')
    x1 = px - d1 * scale
    o.append(f'<rect class="f-red" x="{x1 - 14}" y="{py - 32}" width="28" height="28" rx="3"/>' + text(x1, py - 13, 'F_1', 't-w'))
    xs = [px + d * scale for d in ds]
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(f"{f(x - px)} 0" for x in xs)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<rect class="f-acc" x="{px - 11}" y="{py - 26}" width="22" height="22" rx="3"/>' + text(px, py - 10, 'F_2', 't-ws') + '</g>')
    o.append('</g>')
    o.append(text(x1, py + 30, 'd₁ = 0,2 м', 't-s'))
    o.append(text(60, 30, 'F₁ = 30 Н', 't-red', 'start') + text(60, 50, 'F₂ = 10 Н', 't-acc', 'start'))
    o.append(f'<g opacity="0">{phase_op("0;1;0;1;0", "0;0.34;0.66;0.8;0.95", dur)}' + text(250, 30, 'равновесие: d₂ = 0,6 м', 't-grn') + text(250, 50, 'F₁d₁ = F₂d₂', 't-grn') + '</g>')
    o.append(text(180, 196, 'M = F·d; рычаг в равновесии, когда моменты равны', 't-s'))
    return ''.join(o)


@fig('equilibrium-types', 'Виды равновесия: шар в ямке после толчка возвращается (устойчивое), с вершины горки скатывается (неустойчивое), на плоскости остаётся там, где его оставили (безразличное)', 360, 200)
def equilibrium_types():
    dur = 6
    o = []
    # ямка
    o.append('<path class="s-ink" d="M10,80Q60,170 110,80" stroke-width="2.4" fill="none"/>')
    xs = [60, 60, 40, 76, 50, 66, 57, 60, 60]
    ys = [(x - 60) ** 2 / 200 + 116 for x in xs]
    o.append(f'<circle class="f-red" r="9">{anims(dur, cx=xs, cy=[y - 9 for y in ys])}</circle>')
    o.append(text(60, 180, 'устойчивое', 't-red'))
    # горка
    o.append('<path class="s-ink" d="M130,150Q180,40 230,150" stroke-width="2.4" fill="none"/>')
    def hill(x):
        t = (x - 130) / 100
        return (1 - t) ** 2 * 150 + 2 * (1 - t) * t * 40 + t * t * 150
    hx = [180, 180, 186, 200, 222, 230, 230]
    ky = '0;0.25;0.35;0.5;0.62;0.7;1'
    o.append(f'<circle class="f-acc" r="9"><animate attributeName="cx" values="{nums(hx)}" keyTimes="{ky}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="cy" values="{nums([hill(x) - 9 for x in hx])}" keyTimes="{ky}" dur="{dur}s" repeatCount="indefinite"/>'
             f'{phase_op("1;0;1", "0;0.72;0.98", dur)}</circle>')
    o.append(text(180, 180, 'неустойчивое', 't-acc'))
    # плоскость
    o.append('<path class="s-ink" d="M250,130H350" stroke-width="2.4"/>')
    px = [280, 280, 320, 320, 280]
    o.append(f'<circle class="f-grn" cy="121" r="9"><animate attributeName="cx" values="{nums(px)}" keyTimes="0;0.3;0.5;0.8;1" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(text(300, 180, 'безразличное', 't-grn'))
    return ''.join(o)


# ───────────────────────────── волны ─────────────────────────────

@fig('grating', 'Дифракционная решётка: свет проходит через щели, и за решёткой максимумы видны под углами, где d·sinφ = kλ; белый свет раскладывается в спектры, красные лучи отклоняются сильнее фиолетовых', 360, 220)
def grating():
    dur = 1.4
    gx, cy = 120, 110
    o = []
    for x in (40, 60, 80, 100):
        o.append(f'<path class="s-mute" d="M{x},40V180" stroke-width="1.5" opacity="0.6"/>')
    o.append(f'<path class="s-ink" d="M30,{cy}H{gx}" stroke-width="3" stroke-dasharray="10 6">{flow(dur, 16, True)}</path>')
    o.append(text(60, 30, 'белый свет', 't-s'))
    for y in range(30, 191, 8):
        o.append(f'<rect class="f-ink" x="{gx - 2}" y="{y}" width="4" height="5"/>')
    o.append(text(gx, 208, 'решётка, период d', 't-s'))
    o.append(f'<path class="s-ink" d="M{gx},{cy}H340" stroke-width="2.4" stroke-dasharray="10 6">{flow(dur, 16, True)}</path>')
    o.append(text(338, cy - 6, 'k = 0', 't-s', 'end'))
    cols = [('s-sp-v', 400e-9), ('s-sp-b', 470e-9), ('s-sp-g', 530e-9), ('s-sp-y', 580e-9), ('s-sp-o', 610e-9), ('s-sp-r', 680e-9)]
    d = 2.6e-6
    L = 220
    for sign in (1, -1):
        for cls, lam in cols:
            phi = math.asin(lam / d)
            x2 = gx + L * math.cos(phi)
            y2 = cy - sign * L * math.sin(phi)
            o.append(f'<path class="{cls}" d="M{gx},{cy}L{f(x2)},{f(y2)}" stroke-width="2" stroke-dasharray="10 6">{flow(dur, 16, True)}</path>')
    o.append(text(330, 40, 'k = 1: красный дальше', 't-red', 'end'))
    o.append(text(340, 186, 'k = −1', 't-s', 'end'))
    o.append(text(262, 210, 'd sin φ = kλ', 't-acc'))
    return ''.join(o)


@fig('em-scale', 'Шкала электромагнитных волн: от радиоволн (больше 1 мм) через инфракрасное, видимый свет (380–780 нм), ультрафиолет и рентген к гамма-излучению (меньше 5 пм) — длина волны уменьшается, частота и энергия фотона растут', 360, 200)
def em_scale():
    dur = 2
    x0, x1 = 20, 340
    # волна с уменьшающейся длиной волны (чирп)
    pts = []
    ph = 0
    n = 400
    for i in range(n + 1):
        u = i / n
        x = x0 + (x1 - x0) * u
        lam = 60 * math.exp(math.log(0.07) * u)  # длина волны на рисунке: от 60 px до ≈ 4 px
        if i:
            ph += 2 * math.pi * ((x1 - x0) / n) / max(lam, 3.2)
        pts.append(f'{f(x)},{f(64 - 22 * math.sin(ph))}')
    o = [f'<path class="s-acc" d="M{"L".join(pts)}" stroke-width="2" fill="none" stroke-dasharray="400 0"/>']
    bands = [(20, 110, 'радио', 'f-soft'), (110, 160, 'ИК', 'f-red-soft'), (160, 186, '', None), (186, 236, 'УФ', 'f-soft'), (236, 286, 'рентген', 'f-red-soft'), (286, 340, 'гамма', 'f-soft')]
    for a, b, lab, cls in bands:
        if cls:
            o.append(f'<rect class="{cls}" x="{a}" y="104" width="{b - a}" height="30" stroke="none"/>')
            o.append(text((a + b) / 2, 124, lab, 't-s'))
    for k, c in enumerate(['s-sp-r', 's-sp-o', 's-sp-y', 's-sp-g', 's-sp-b', 's-sp-v']):
        x = 162 + k * 4.4
        o.append(f'<path class="{c}" d="M{f(x)},104V134" stroke-width="4.6"/>')
    o.append(text(173, 150, 'видимый', 't-s'))
    o.append(text(173, 164, '380–780 нм', 't-s'))
    o.append(text(65, 150, '> 1 мм', 't-s') + text(313, 150, '< 5 пм', 't-s'))
    o.append(arrow(40, 186, 320, 186, 's-red', 'f-red', 2, 7) + text(180, 180, 'λ ↓   ν и энергия фотона ↑', 't-red'))
    o.append(f'<circle class="f-red" r="6" cy="119"><animate attributeName="cx" values="30;330;30" keyTimes="0;0.5;1" dur="{dur * 4}s" repeatCount="indefinite"/></circle>')
    o.append(text(180, 20, 'шкала электромагнитных волн (границы условны)', 't-s'))
    return ''.join(o)


@fig('rlc-resonance', 'Резонанс напряжений в цепи RLC: ток наибольший, когда X_L = X_C, то есть при ω₀ = 1/√(LC) (L = 0,1 Гн, C = 10 мкФ → ω₀ = 1000 рад/с, R = 20 Ом, U = 100 В → I = 5 А)', 360, 220)
def rlc_resonance():
    dur = 8
    gx, gy, w, hgt = 40, 186, 290, 150
    L, C, R, U = 0.1, 1e-5, 20, 100
    wmin, wmax = 200, 2400
    def X(w_):
        return gx + (w_ - wmin) / (wmax - wmin) * w
    def I(w_):
        return U / math.sqrt(R ** 2 + (w_ * L - 1 / (w_ * C)) ** 2)
    def Y(i):
        return gy - i / 5 * (hgt - 10)
    o = [arrow(gx, gy, gx + w + 14, gy, 's-ink', 'f-ink', 1.4, 6), arrow(gx, gy, gx, gy - hgt - 10, 's-ink', 'f-ink', 1.4, 6),
         text(gx + 8, gy - hgt - 8, 'I', 't', 'start'), text(gx + w + 10, gy + 16, 'ω', 't', 'end')]
    ws = lin(wmin, wmax, 120)
    o.append(f'<path class="s-red" d="M{"L".join(f"{f(X(v))},{f(Y(I(v)))}" for v in ws)}" stroke-width="2.6" fill="none"/>')
    # X_L и X_C (масштаб 1 Ом = 0,6 px)
    def YX(x_):
        return gy - min(x_, 260) * 0.55
    o.append(f'<path class="s-acc" d="M{"L".join(f"{f(X(v))},{f(YX(v * L))}" for v in ws)}" stroke-width="1.4" stroke-dasharray="5 4" fill="none"/>')
    o.append(f'<path class="s-grn" d="M{"L".join(f"{f(X(v))},{f(YX(1 / (v * C)))}" for v in ws)}" stroke-width="1.4" stroke-dasharray="5 4" fill="none"/>')
    o.append(text(X(2300), YX(230) - 6, 'X_L', 't-acc', 'end') + text(X(300) + 4, YX(255) + 4, 'X_C', 't-grn', 'start'))
    x0 = X(1000)
    o.append(f'<path class="s-mute" d="M{f(x0)},{gy}V{f(Y(5) - 6)}" stroke-width="1" stroke-dasharray="3 4"/>' + text(x0, gy + 14, 'ω₀ = 1/√(LC)', 't-s'))
    o.append(text(x0 + 8, Y(5) - 4, 'X_L = X_C, I = U/R = 5 А', 't-red', 'start'))
    path = [wmin + (wmax - wmin) * (0.5 - 0.5 * math.cos(2 * math.pi * u)) for u in lin(0, 1, 41)]
    o.append(f'<circle class="f-red" r="5">{anims(dur, cx=[X(v) for v in path], cy=[Y(I(v)) for v in path])}</circle>')
    return ''.join(o)


@fig('resistors-connect', 'Соединение проводников: последовательно ток один и тот же через оба резистора, а напряжения складываются; параллельно ток разделяется — через меньшее сопротивление идёт больший ток', 360, 210)
def resistors_connect():
    dur = 3
    o = [text(90, 20, 'последовательно', 't'), text(270, 20, 'параллельно', 't')]
    # последовательно
    o.append('<path class="s-ink" d="M20,60H160V170H20Z" stroke-width="2" fill="none"/>')
    o.append(resistor(40, 76, 60, 'R₁') + resistor(104, 140, 60, 'R₂'))
    o.append(battery(20, 115, True, ''))
    o.append('<path id="resistors-connect-s" d="M20,60H160V170H20Z" fill="none"/>')
    for k in range(6):
        o.append(f'<circle class="f-acc" r="3.5"><animateMotion dur="{dur * 2}s" begin="-{f(k * dur * 2 / 6)}s" repeatCount="indefinite"><mpath href="#resistors-connect-s"/></animateMotion></circle>')
    o.append(text(90, 196, 'I одинаков, U = U₁ + U₂', 't-s'))
    # параллельно: R₁ = 1 (сверху), R₂ = 3 (снизу) — ток сверху в 3 раза больше
    o.append('<path class="s-ink" d="M200,170V60H340V170Z M220,60V140H320V60" stroke-width="2" fill="none"/>')
    o.append(resistor(250, 290, 60, 'R₁ (малое)') + resistor(250, 290, 140, 'R₂ (большое)'))
    o.append(battery(200, 115, True, ''))
    o.append('<path id="resistors-connect-a" d="M200,170V60H340V170H200" fill="none"/>')
    o.append('<path id="resistors-connect-b" d="M200,170V60H220V140H320V60H340V170H200" fill="none"/>')
    for k in range(6):
        o.append(f'<circle class="f-red" r="3.5"><animateMotion dur="{dur * 2}s" begin="-{f(k * dur * 2 / 6)}s" repeatCount="indefinite"><mpath href="#resistors-connect-a"/></animateMotion></circle>')
    for k in range(2):
        o.append(f'<circle class="f-acc" r="3.5"><animateMotion dur="{dur * 2.4}s" begin="-{f(k * dur * 1.2)}s" repeatCount="indefinite"><mpath href="#resistors-connect-b"/></animateMotion></circle>')
    o.append(text(270, 196, 'U одинаково, I = I₁ + I₂', 't-s'))
    return ''.join(o)


# ──────────────── дифракция по конспекту (d02) и статика, дополнение 22.10.2026 ────────────────

@fig('grating-screen', 'Решётка и экран, как на рисунке в конспекте (стр. дф2): максимум номер k виден под углом φ к центральному (0-max), на экране он на расстоянии x от него; sin φ = x/√(L² + x²) и d·sin φ = kλ. Для d = 2,5λ видны максимумы k = 0, 1, 2', 360, 250)
def grating_screen():
    dur = 6
    gx, ay, sx = 100, 190, 220
    L = sx - gx
    o = ['<defs><clipPath id="grating-screen-clip"><rect x="12" y="170" width="86" height="40"/></clipPath></defs>']
    o.append(f'<g clip-path="url(#grating-screen-clip)"><path class="s-acc" d="{wave_path(-8, 98, ay, 6, 20)}" stroke-width="2" fill="none">'
             f'<animateTransform attributeName="transform" type="translate" values="0 0;20 0" dur="1s" repeatCount="indefinite"/></path></g>')
    o.append(text(40, 174, 'λ', 't-acc'))
    o.append(f'<path class="s-ink" d="M{gx},20V200" stroke-width="3" stroke-dasharray="6 4"/>')
    o.append(text(gx, 14, 'решётка, d', 't-s'))
    o.append(f'<path class="s-mute" d="M{sx},20V200" stroke-width="4"/>')
    o.append(text(sx, 14, 'экран', 't-s'))
    ks = []
    for k, cls in ((0, 's-acc'), (1, 's-grn'), (2, 's-red')):
        phi = math.asin(k / 2.5)
        x = L * math.tan(phi)
        ks.append((phi, x))
        o.append(f'<path class="{cls}" d="M{gx},{ay}L{sx},{f(ay - x)}" stroke-width="2" stroke-dasharray="8 5">{flow(1, 13, True)}</path>')
        o.append(f'<circle class="f-{cls[2:]}" cx="{sx}" cy="{f(ay - x)}" r="4"/>')
        o.append(text(sx + 8, ay - x + 4, f'{k}-max', 't-s', 'start'))
    o.append(f'<path class="s-mute" d="M{gx},212H{sx}M{gx},207V217M{sx},207V217" stroke-width="1.4"/>' + text((gx + sx) / 2, 208, 'L', 't-s'))
    for i, (k, kt) in enumerate(((1, '1;0'), (2, '0;1'))):
        phi, x = ks[k]
        r = 34
        ex, ey = gx + r * math.cos(phi), ay - r * math.sin(phi)
        hx, hy = gx + (r + 12) * math.cos(phi / 2), ay - (r + 12) * math.sin(phi / 2)
        g = [f'<g opacity="{1 if i == 0 else 0}">{phase_op(kt, "0;0.5", dur)}']
        g.append(f'<path class="s-ink" d="M{gx},{ay}L{sx},{f(ay - x)}" stroke-width="3"/>')
        g.append(f'<path class="s-ink" d="M{gx + r},{ay}A{r},{r} 0 0 0 {f(ex)},{f(ey)}" stroke-width="1.6" fill="none"/>' + text(hx, hy + 4, 'φ', 't'))
        g.append(f'<path class="s-acc" d="M270,{ay}V{f(ay - x)}M264,{ay}H276M264,{f(ay - x)}H276" stroke-width="1.8"/>')
        g.append(text(280, ay - x / 2 + 2, 'x', 't-acc', 'start') + text(280, ay - x / 2 + 18, f'k = {k}', 't-s', 'start'))
        g.append('</g>')
        o.append(''.join(g))
    o.append(text(180, 240, 'd·sin φ = kλ,   sin φ = x / √(L² + x²)', 't-acc'))
    return ''.join(o)


@fig('lever-kinds', 'Рода рычагов: у рычага I рода опора между силами (ножницы, качели, лом), у рычага II рода обе силы по одну сторону от опоры (тачка, щипцы для орехов); выигрыш в силе k = d / d_гр', 360, 214)
def lever_kinds():
    dur = 4
    py = 104
    o = []
    # I род: опора между силами
    p1, a1, b1 = 86, 28, 172
    o.append(text(100, 22, 'I род: опора между силами', 't-s'))
    o.append(f'<path class="f-mute" d="M{p1 - 12},{py + 28}L{p1},{py + 4}L{p1 + 12},{py + 28}Z"/>')
    o.append(f'<g>{rot([0, 0, 9, 9, 0], p1, py, dur)}')
    o.append(f'<rect class="f-ink" x="{a1}" y="{py - 4}" width="{b1 - a1}" height="8" rx="3"/>')
    o.append(f'<rect class="f-red" x="{a1}" y="{py - 30}" width="26" height="26" rx="3"/>' + text(a1 + 13, py - 12, 'P', 't-w'))
    o.append(arrow(b1 - 6, py - 46, b1 - 6, py - 6, 's-acc', 'f-acc', 2.6) + text(b1 - 14, py - 34, 'F', 't-acc', 'end'))
    o.append('</g>')
    o.append(f'<path class="s-mute" d="M{a1 + 13},{py + 40}H{p1}M{p1},{py + 54}H{b1 - 6}M{a1 + 13},{py + 35}V{py + 45}M{p1},{py + 35}V{py + 59}M{b1 - 6},{py + 49}V{py + 59}" stroke-width="1.4"/>')
    o.append(text((a1 + 13 + p1) / 2, py + 34, 'd_гр', 't-s') + text((p1 + b1 - 6) / 2, py + 50, 'd', 't-s'))
    o.append(text(100, 186, 'ножницы, качели, лом', 't-s'))
    # II род: обе силы по одну сторону от опоры
    p2, b2, lx = 204, 346, 250
    o.append(text(272, 22, 'II род: силы по одну сторону', 't-s'))
    o.append(f'<path class="f-mute" d="M{p2 - 12},{py + 28}L{p2},{py + 4}L{p2 + 12},{py + 28}Z"/>')
    o.append(f'<g>{rot([0, 0, -9, -9, 0], p2, py, dur)}')
    o.append(f'<rect class="f-ink" x="{p2 - 6}" y="{py - 4}" width="{b2 - p2 + 6}" height="8" rx="3"/>')
    o.append(f'<rect class="f-red" x="{lx - 13}" y="{py - 30}" width="26" height="26" rx="3"/>' + text(lx, py - 12, 'P', 't-w'))
    o.append(arrow(b2 - 6, py + 42, b2 - 6, py + 6, 's-acc', 'f-acc', 2.6) + text(b2 - 14, py + 34, 'F', 't-acc', 'end'))
    o.append('</g>')
    o.append(f'<path class="s-mute" d="M{p2},{py + 40}H{lx}M{p2},{py + 58}H{b2 - 6}M{lx},{py + 35}V{py + 45}M{p2},{py + 35}V{py + 63}M{b2 - 6},{py + 53}V{py + 63}" stroke-width="1.4"/>')
    o.append(text((p2 + lx) / 2, py + 34, 'd_гр', 't-s') + text((lx + b2) / 2, py + 54, 'd', 't-s'))
    o.append(text(272, 186, 'тачка, щипцы для орехов', 't-s'))
    o.append(text(180, 206, 'выигрыш в силе k = d / d_гр', 't-acc'))
    return ''.join(o)


@fig('pulleys', 'Блоки: неподвижный блок только меняет направление силы (F = P, конец верёвки проходит s = h); подвижный даёт выигрыш в силе в 2 раза (F = P/2), но s = 2h; полиспаст, у которого груз держат n = 4 ветви, — F = P/4, s = 4h', 360, 222)
def pulleys():
    dur = 5
    kt = '0;0.15;0.55;0.7;1'

    def sv(a, b):
        return f'{f(a)};{f(a)};{f(b)};{f(b)};{f(a)}'

    def an(attr, a, b):
        return f'<animate attributeName="{attr}" values="{sv(a, b)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'

    def tr(dy):
        return f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 {f(dy)};0 {f(dy)};0 0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'

    o = []
    for x1, x2 in ((24, 96), (140, 170), (252, 340)):
        o.append(f'<path class="s-mute" d="M{x1},22H{x2}" stroke-width="5"/>')
    # неподвижный блок
    h = 30
    o.append('<path class="s-ink" d="M60,22V50" stroke-width="2"/>')
    o.append('<path class="s-ink" d="M44,50A16,16 0 0 1 76,50" stroke-width="2" fill="none"/>')
    o.append('<circle class="f-soft" cx="60" cy="50" r="13"/><circle class="s-ink" cx="60" cy="50" r="13" stroke-width="2" fill="none"/><circle class="f-ink" cx="60" cy="50" r="2.5"/>')
    o.append(f'<line class="s-ink" x1="44" y1="50" x2="44" y2="150" stroke-width="2">{an("y2", 150, 150 - h)}</line>')
    o.append(f'<g>{tr(-h)}<rect class="f-red" x="32" y="150" width="24" height="24" rx="3"/>' + text(44, 166, 'P', 't-w') + '</g>')
    o.append(f'<line class="s-ink" x1="76" y1="50" x2="76" y2="120" stroke-width="2">{an("y2", 120, 120 + h)}</line>')
    o.append(f'<g>{tr(h)}' + arrow(76, 120, 76, 146, 's-acc', 'f-acc', 2.6) + text(84, 140, 'F', 't-acc', 'start') + '</g>')
    o.append(text(60, 196, 'неподвижный', 't-s') + text(60, 214, 'F = P,  s = h', 't-acc'))
    # подвижный блок
    h = 25
    o.append(f'<line class="s-ink" x1="154" y1="22" x2="154" y2="120" stroke-width="2">{an("y2", 120, 120 - h)}</line>')
    o.append(f'<line class="s-ink" x1="190" y1="120" x2="190" y2="86" stroke-width="2">{an("y1", 120, 120 - h)}{an("y2", 86, 86 - 2 * h)}</line>')
    o.append(f'<g>{tr(-2 * h)}' + arrow(190, 86, 190, 60, 's-acc', 'f-acc', 2.6) + text(198, 72, 'F', 't-acc', 'start') + '</g>')
    o.append(f'<g>{tr(-h)}<path class="s-ink" d="M154,120A18,18 0 0 0 190,120" stroke-width="2" fill="none"/>'
             '<circle class="f-soft" cx="172" cy="120" r="15"/><circle class="s-ink" cx="172" cy="120" r="15" stroke-width="2" fill="none"/><circle class="f-ink" cx="172" cy="120" r="2.5"/>'
             '<path class="s-ink" d="M172,120V146" stroke-width="2"/><rect class="f-red" x="160" y="146" width="24" height="24" rx="3"/>' + text(172, 162, 'P', 't-w') + '</g>')
    o.append(text(172, 196, 'подвижный', 't-s') + text(172, 214, 'F = P/2,  s = 2h', 't-acc'))
    # полиспаст на 4 ветвях
    h = 15
    bx = [268, 282, 296, 310]
    o.append('<path class="s-ink" d="M289,22V30" stroke-width="2"/><rect class="f-soft" x="262" y="30" width="54" height="16" rx="4"/>')
    o.append('<circle class="s-ink" cx="275" cy="38" r="7" stroke-width="2" fill="none"/><circle class="s-ink" cx="303" cy="38" r="7" stroke-width="2" fill="none"/>')
    for x in bx:
        o.append(f'<line class="s-ink" x1="{x}" y1="38" x2="{x}" y2="130" stroke-width="1.8">{an("y2", 130, 130 - h)}</line>')
    o.append('<path class="s-ink" d="M310,38H330" stroke-width="1.8"/>')
    o.append(f'<line class="s-ink" x1="330" y1="38" x2="330" y2="78" stroke-width="1.8">{an("y2", 78, 78 + 4 * h)}</line>')
    o.append(f'<g>{tr(4 * h)}' + arrow(330, 78, 330, 102, 's-acc', 'f-acc', 2.6) + text(336, 96, 'F', 't-acc', 'start') + '</g>')
    o.append(f'<g>{tr(-h)}<rect class="f-soft" x="262" y="124" width="54" height="16" rx="4"/>'
             '<circle class="s-ink" cx="275" cy="130" r="7" stroke-width="2" fill="none"/><circle class="s-ink" cx="303" cy="130" r="7" stroke-width="2" fill="none"/>'
             '<path class="s-ink" d="M289,140V148" stroke-width="2"/><rect class="f-red" x="275" y="148" width="28" height="26" rx="3"/>' + text(289, 165, 'P', 't-w') + '</g>')
    o.append(text(296, 196, 'полиспаст, n = 4', 't-s') + text(296, 214, 'F = P/4,  s = 4h', 't-acc'))
    return ''.join(o)


@fig('incline-golden', 'Золотое правило механики: по наклонной плоскости груз втаскивают силой F = mg·h/l, меньшей веса, но проходят путь l, больший высоты h; работа F·l равна работе mg·h при подъёме по вертикали — выигрыша в работе нет', 360, 214)
def incline_golden():
    dur = 5
    x0, y0, x1, y1 = 24, 170, 214, 95
    L = math.hypot(x1 - x0, y0 - y1)
    a = math.atan2(y0 - y1, x1 - x0)
    deg = math.degrees(a)
    kt = '0;0.12;0.62;0.78;1'
    o = [f'<path class="f-soft" d="M{x0},{y0}L{x1},{y0}L{x1},{y1}Z"/>',
         f'<path class="s-ink" d="M{x0},{y0}L{x1},{y1}V{y0}H{x0}" stroke-width="2" fill="none"/>']
    o.append(f'<path class="s-ink" d="M{x0 + 34},{y0}A34,34 0 0 0 {f(x0 + 34 * math.cos(a))},{f(y0 - 34 * math.sin(a))}" stroke-width="1.4" fill="none"/>' + text(x0 + 46, y0 - 5, 'α', 't'))
    o.append(text(x1 + 10, (y0 + y1) / 2 + 4, 'h', 't-red', 'start'))
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    o.append(text(mx - 14 * math.sin(a) - 4, my - 14 * math.cos(a) - 14, 'l', 't-acc'))
    s0, s1 = 6, L - 34
    dx, dy = (s1 - s0) * math.cos(a), -(s1 - s0) * math.sin(a)
    mg = 60
    Fl = mg * math.sin(a)
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;{f(dx)} {f(dy)};{f(dx)} {f(dy)};0 0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<g transform="translate({f(x0 + s0 * math.cos(a))} {f(y0 - s0 * math.sin(a))}) rotate({f(-deg)})">'
             '<rect class="f-red" x="0" y="-22" width="22" height="22" rx="3"/>'
             + arrow(22, -11, 22 + Fl, -11, 's-acc', 'f-acc', 2.6) + text(24 + Fl / 2, -16, 'F', 't-acc') + '</g></g>')
    # подъём по вертикали
    vx = 296
    o.append(f'<path class="s-mute" d="M{vx - 30},{y0}H{vx + 30}M{vx + 22},{y0}V{y1}" stroke-width="1.6" stroke-dasharray="4 3"/>' + text(vx + 28, (y0 + y1) / 2 + 4, 'h', 't-red', 'start'))
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 {f(y1 - y0)};0 {f(y1 - y0)};0 0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<rect class="f-red" x="{vx - 11}" y="{y0 - 22}" width="22" height="22" rx="3"/>'
             + arrow(vx, y0 - 22, vx, y0 - 22 - mg, 's-red', 'f-red', 2.6) + text(vx - 8, y0 - 22 - mg + 12, 'mg', 't-red', 'end') + '</g>')
    o.append(text(118, 192, 'F = mg·h/l, путь l', 't-acc') + text(296, 192, 'F = mg, путь h', 't-red'))
    o.append(text(180, 208, 'F·l = mg·h — выигрыша в работе нет', 't-s'))
    return ''.join(o)


@fig('center-mass', 'Центр масс двух грузов: опору двигают вдоль лёгкого стержня с грузами 2 кг и 6 кг; стержень уравновешен, только когда опора под центром масс — в 0,6 м от лёгкого груза, ближе к тяжёлому (l₁/l₂ = m₂/m₁ = 3)', 360, 214)
def center_mass():
    dur = 8
    py = 104
    xa, xb = 40, 320  # 0,8 м = 280 px
    m1, m2 = 2, 6
    xc = (m1 * xa + m2 * xb) / (m1 + m2)
    ss = [150, 150, 205, 250, 250, 300, 250, 250, 150]
    kt = '0;0.08;0.25;0.38;0.55;0.68;0.8;0.94;1'
    angs = [max(-9, min(9, (m2 * (xb - s) - m1 * (s - xa)) / 60)) for s in ss]
    o = [f'<path class="s-mute" d="M16,{py + 34}H344" stroke-width="2"/>']
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(f"{f(s - 150)} 0" for s in ss)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<path class="f-mute" d="M138,{py + 34}L150,{py + 4}L162,{py + 34}Z"/></g>')
    rv = ';'.join(f'{f(a)} {f(s)} {py}' for a, s in zip(angs, ss))
    o.append(f'<g><animateTransform attributeName="transform" type="rotate" values="{rv}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>')
    o.append(f'<rect class="f-ink" x="{xa - 8}" y="{py - 4}" width="{xb - xa + 16}" height="8" rx="3"/>')
    o.append(f'<rect class="f-acc" x="{xa - 13}" y="{py - 30}" width="26" height="26" rx="3"/>' + text(xa, py - 12, '2 кг', 't-ws'))
    o.append(f'<rect class="f-red" x="{xb - 20}" y="{py - 44}" width="40" height="40" rx="3"/>' + text(xb, py - 19, '6 кг', 't-w'))
    o.append(f'<circle class="f-paper" cx="{f(xc)}" cy="{py}" r="6"/><circle class="s-grn" cx="{f(xc)}" cy="{py}" r="6" stroke-width="2" fill="none"/>'
             f'<path class="f-grn" d="M{f(xc)},{py}V{py - 6}A6,6 0 0 1 {f(xc + 6)},{py}ZM{f(xc)},{py}V{py + 6}A6,6 0 0 1 {f(xc - 6)},{py}Z"/>')
    o.append('</g>')
    o.append(f'<path class="s-mute" d="M{xa},{py + 50}H{f(xc)}M{f(xc)},{py + 50}H{xb}M{xa},{py + 44}V{py + 56}M{f(xc)},{py + 44}V{py + 56}M{xb},{py + 44}V{py + 56}" stroke-width="1.4"/>')
    o.append(text((xa + xc) / 2, py + 46, 'l₁ = 0,6 м', 't-s') + text((xc + xb) / 2, py + 46, 'l₂ = 0,2 м', 't-s'))
    o.append(text(xc, py + 72, 'центр масс', 't-grn'))
    o.append(f'<g opacity="0">{phase_op("0;1;0;1;0", "0;0.38;0.55;0.8;0.94", dur)}' + text(180, 24, 'равновесие: опора под центром масс', 't-grn') + '</g>')
    o.append(text(180, 204, 'x_c = (m₁x₁ + m₂x₂) / (m₁ + m₂) = (2·0 + 6·0,8) / 8 = 0,6 м', 't-s'))
    return ''.join(o)
