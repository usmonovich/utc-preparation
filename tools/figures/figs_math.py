"""Иллюстрации к темам математики (книга «Математика. Сборник тестовых заданий для абитуриентов»).
Все числа на рисунках — из примеров темы и посчитаны здесь же по формулам."""
import math
from figlib import *  # noqa: F401,F403
from figs_elec import phase_op  # noqa: F401


def kts(n):
    return ';'.join(f(i / (n - 1)) for i in range(n))


def phases(n, dur, i, extra=''):
    """Группа, видимая только в i-й из n равных фаз (дискретно)."""
    vals = ['0'] * n
    vals[i] = '1'
    # discrete: значение держится до следующего keyTime
    return f'<g opacity="{1 if i == 0 else 0}"{extra}><animate attributeName="opacity" values="{";".join(vals)}" keyTimes="{";".join(f(k / n) for k in range(n))}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>'


# ───────────────────────────── 1.1 Натуральные и целые числа ─────────────────────────────

@fig('division-remainder', 'Деление с остатком: 17 предметов раскладываем по 5 — получается 3 полные группы и 2 предмета остаются; 17 = 5·3 + 2, остаток 2 меньше делителя 5', 360, 210)
def division_remainder():
    dur = 6
    kt = '0;0.15;0.55;0.85;1'
    o = []
    for i in range(17):
        x0, y0 = 22 + i * 19.7, 40
        if i < 15:
            g, k = divmod(i, 5)
            x1, y1 = 50 + g * 70, 78 + k * 22
            cls = 'f-acc'
        else:
            x1, y1 = 290, 78 + (i - 15) * 22
            cls = 'f-red'
        o.append(f'<circle class="{cls}" r="7.5"><animate attributeName="cx" values="{f(x0)};{f(x0)};{f(x1)};{f(x1)};{f(x0)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="cy" values="{y0};{y0};{f(y1)};{f(y1)};{y0}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(text(180, 20, 'a = 17 предметов, делитель b = 5', 't-s'))
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.5;0.9", dur)}')
    for g in range(3):
        o.append(f'<rect class="s-acc" x="{36 + g * 70}" y="66" width="28" height="112" rx="8" fill="none" stroke-width="1.6"/>' + text(50 + g * 70, 196, f'{g + 1}-я', 't-s'))
    o.append(f'<rect class="s-red" x="276" y="66" width="28" height="46" rx="8" fill="none" stroke-width="1.6"/>' + text(290, 130, 'r = 2', 't-red'))
    o.append(text(320, 196, '17 = 5·3 + 2', 't-acc', 'end'))
    o.append('</g>')
    return ''.join(o)


@fig('lcm-jumps', 'НОК на числовой прямой: автобус А отправляется каждые 12 минут, автобус Б — каждые 20 минут; впервые снова вместе через НОК(12, 20) = 60 минут', 360, 190)
def lcm_jumps():
    dur = 8
    x0, sc = 24, 5.2  # 0..60 → 24..336
    o = ['<path class="s-ink" d="M18,100H344" stroke-width="2"/>']
    for t in range(0, 61, 4):
        big = t % 12 == 0 or t % 20 == 0
        o.append(f'<path class="s-mute" d="M{f(x0 + t * sc)},{95 if big else 97}V{105 if big else 103}" stroke-width="1.4"/>')
    for t in (0, 12, 20, 24, 36, 40, 48, 60):
        o.append(text(x0 + t * sc, 136, str(t), 't-s'))
    # прыжки А (над прямой) и Б (под прямой)
    for step, y, cls, lab, ty in ((12, 62, 'acc', 'А: +12', 44), (20, 152, 'red', 'Б: +20', 178)):
        n = 60 // step
        for k in range(n):
            xa, xb = x0 + k * step * sc, x0 + (k + 1) * step * sc
            sweep = 1 if y < 100 else 0
            o.append(f'<path class="s-{cls}" d="M{f(xa)},{100 if y < 100 else 100}A{f((xb - xa) / 2)},{20} 0 0 {sweep} {f(xb)},100" fill="none" stroke-width="1.6" stroke-dasharray="4 3" opacity="0.7"/>')
        xs = [x0 + k * step * sc for k in range(n + 1)]
        vals = ';'.join(f(x) for x in xs) + f';{f(xs[-1])};{f(xs[0])}'
        kt = ';'.join(f(0.8 * k / n) for k in range(n + 1)) + ';0.97;1'
        o.append(f'<circle class="f-{cls}" cy="{y}" r="8"><animate attributeName="cx" values="{vals}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></circle>')
        o.append(text(20, ty, lab, f't-{cls}', 'start'))
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.8;0.97", dur)}<circle class="s-grn" cx="{f(x0 + 60 * sc)}" cy="100" r="14" fill="none" stroke-width="2.4"/>'
             + text(330, 182, 'вместе: НОК(12, 20) = 60', 't-grn', 'end') + '</g>')
    return ''.join(o)


@fig('last-digit-cycle', 'Последние цифры степеней двойки повторяются по кругу 2 → 4 → 8 → 6 → 2: период 4, поэтому у 2^k последняя цифра определяется остатком k при делении на 4', 360, 210)
def last_digit_cycle():
    dur = 8
    cx, cy, R = 110, 110, 62
    digits = [2, 4, 8, 6]
    o = [f'<circle class="s-mute" cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke-width="2" stroke-dasharray="5 4"/>']
    pos = []
    for i, d in enumerate(digits):
        a = -math.pi / 2 + i * math.pi / 2
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        pos.append((x, y))
        o.append(f'<circle class="f-paper" cx="{f(x)}" cy="{f(y)}" r="17"/><circle class="f-soft" cx="{f(x)}" cy="{f(y)}" r="17"/><circle class="s-acc" cx="{f(x)}" cy="{f(y)}" r="17" fill="none" stroke-width="2"/>' + text(x, y + 6, str(d), 't-acc'))
    for i in range(4):
        (x1, y1), (x2, y2) = pos[i], pos[(i + 1) % 4]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ox, oy = mx - cx, my - cy
        L = math.hypot(ox, oy)
        o.append(arrow(mx + oy / L * 8 + ox / L * 6, my - ox / L * 8 + oy / L * 6, mx - oy / L * 8 + ox / L * 6, my + ox / L * 8 + oy / L * 6, 's-mute', 'f-mute', 1.6, 6))
    n = 8
    xs = [pos[k % 4][0] for k in range(n)]
    ys = [pos[k % 4][1] for k in range(n)]
    o.append(f'<circle class="s-red" r="23" fill="none" stroke-width="3"><animate attributeName="cx" values="{nums(xs)}" keyTimes="{";".join(f(k / n) for k in range(n))}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>'
             f'<animate attributeName="cy" values="{nums(ys)}" keyTimes="{";".join(f(k / n) for k in range(n))}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></circle>')
    for k in range(n):
        p = 2 ** (k + 1)
        o.append(phases(n, dur, k) + text(205, 80, f'2^{k + 1} = {p}', 't', 'start') + text(205, 106, f'последняя цифра {p % 10}', 't-red', 'start')
                 + text(205, 132, f'{k + 1} = 4·{(k + 1 - 1) // 4} + {(k % 4) + 1}' if (k + 1) % 4 else f'{k + 1} делится на 4', 't-s', 'start') + '</g>')
    o.append(text(180, 200, 'период 4: 2, 4, 8, 6, 2, 4, 8, 6, …', 't-s'))
    return ''.join(o)


@fig('integer-line', 'Сложение целых чисел на числовой прямой: из точки −3 делаем шаг +5 вправо и попадаем в 2; противоположные числа −5 и 5 стоят на одинаковом расстоянии от нуля, |−5| = |5| = 5', 360, 190)
def integer_line():
    dur = 7
    x0, sc = 180, 19  # -8..8
    X = lambda v: x0 + v * sc  # noqa: E731
    o = [markers('integer-line', ('acc', 'red', 'grn')), '<path class="s-ink" d="M20,110H340" stroke-width="2"/>']
    for v in range(-8, 9):
        o.append(f'<path class="s-mute" d="M{f(X(v))},104V116" stroke-width="1.4"/>' + text(X(v), 134, str(v).replace('-', '−'), 't-s'))
    kt = '0;0.15;0.4;0.55;0.8;1'
    # шаг −3: из 0 влево
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.04;0.98", dur)}' + mline('integer-line', X(0), 66, X(0), 66, 'acc', 3, anims(dur, x2=[X(0), X(-3), X(-3), X(-3), X(-3), X(0)]).replace(times(6), kt)) + '</g>')
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.18;0.98", dur)}' + text(X(-1.5), 56, '−3', 't-acc') + '</g>')
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.42;0.98", dur)}' + mline('integer-line', X(-3), 90, X(-3), 90, 'red', 3, anims(dur, x2=[X(-3), X(-3), X(-3), X(2), X(2), X(-3)]).replace(times(6), kt)) + '</g>')
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.45;0.98", dur)}' + text(X(0.5), 82, '+5', 't-red') + '</g>')
    o.append(f'<circle class="f-grn" cx="{f(X(2))}" cy="110" r="0"><animate attributeName="r" values="0;0;0;0;7;0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.6;0.98", dur)}' + text(180, 28, '−3 + 5 = 2', 't-grn') + '</g>')
    # модуль
    o.append(f'<path class="s-mute" d="M{f(X(-5))},150H{f(X(5))}" stroke-width="1.4" stroke-dasharray="3 3"/>')
    o.append(text(X(-2.5), 168, '|−5| = 5', 't-s') + text(X(2.5), 168, '|5| = 5', 't-s'))
    return ''.join(o)


# ───────────────────────────── 1.2 Дроби ─────────────────────────────

@fig('fraction-add', 'Сложение дробей с разными знаменателями: 1/2 и 1/3 делим на шестые доли (общий знаменатель 6 = НОК(2, 3)): 1/2 = 3/6, 1/3 = 2/6, вместе 5/6', 360, 220)
def fraction_add():
    dur = 9
    W, x0 = 240, 60
    o = []

    def bar(y, parts, filled, cls, lines_cls='s-ink'):
        out = [f'<rect class="f-paper" x="{x0}" y="{y}" width="{W}" height="34" rx="3"/>']
        w = W / parts
        for i in range(filled):
            out.append(f'<rect class="{cls}" x="{f(x0 + i * w)}" y="{y}" width="{f(w)}" height="34"/>')
        for i in range(1, parts):
            out.append(f'<path class="{lines_cls}" d="M{f(x0 + i * w)},{y}V{y + 34}" stroke-width="1.4"/>')
        out.append(f'<rect class="s-ink" x="{x0}" y="{y}" width="{W}" height="34" rx="3" fill="none" stroke-width="2"/>')
        return ''.join(out)

    n = 3
    # фаза 1: 1/2 и 1/3
    o.append(phases(n, dur, 0) + bar(30, 2, 1, 'f-acc') + text(40, 53, '1/2', 't-acc', 'end') + bar(90, 3, 1, 'f-red') + text(40, 113, '1/3', 't-red', 'end')
             + text(180, 160, 'знаменатели разные — складывать нельзя', 't-s') + '</g>')
    # фаза 2: шестые доли
    o.append(phases(n, dur, 1) + bar(30, 6, 3, 'f-acc', 's-mute') + text(40, 53, '3/6', 't-acc', 'end') + bar(90, 6, 2, 'f-red', 's-mute') + text(40, 113, '2/6', 't-red', 'end')
             + text(180, 160, 'общий знаменатель 6 = НОК(2, 3)', 't-s') + '</g>')
    # фаза 3: сумма
    w = W / 6
    sum_bar = [f'<rect class="f-paper" x="{x0}" y="60" width="{W}" height="34" rx="3"/>']
    for i in range(5):
        sum_bar.append(f'<rect class="{"f-acc" if i < 3 else "f-red"}" x="{f(x0 + i * w)}" y="60" width="{f(w)}" height="34"/>')
    for i in range(1, 6):
        sum_bar.append(f'<path class="s-mute" d="M{f(x0 + i * w)},60V94" stroke-width="1.4"/>')
    sum_bar.append(f'<rect class="s-ink" x="{x0}" y="60" width="{W}" height="34" rx="3" fill="none" stroke-width="2"/>')
    o.append(phases(n, dur, 2) + ''.join(sum_bar) + text(40, 83, '5/6', 't-grn', 'end') + text(180, 160, '1/2 + 1/3 = 3/6 + 2/6 = 5/6', 't-grn') + '</g>')
    o.append(text(180, 205, 'a/b + c/d: приводим к общему знаменателю', 't-s'))
    return ''.join(o)


@fig('periodic-division', 'Почему дробь 3/11 периодическая: при делении уголком остатки 3 → 8 → 3 → 8 … повторяются, значит, повторяются и цифры частного: 3/11 = 0,(27)', 360, 210)
def periodic_division():
    dur = 8
    steps = []
    r = 3
    digits = ''
    for _ in range(4):
        r10 = r * 10
        d, r2 = divmod(r10, 11)
        steps.append((r, r10, d, r2))
        digits += str(d)
        r = r2
    n = len(steps)
    o = []
    # круг остатков
    o.append('<circle class="s-mute" cx="270" cy="110" r="46" fill="none" stroke-width="2" stroke-dasharray="5 4"/>')
    for (x, y, v) in ((270, 64, 3), (270, 156, 8)):
        o.append(f'<circle class="f-paper" cx="{x}" cy="{y}" r="16"/><circle class="f-soft" cx="{x}" cy="{y}" r="16"/><circle class="s-acc" cx="{x}" cy="{y}" r="16" fill="none" stroke-width="2"/>' + text(x, y + 5, str(v), 't-acc'))
    o.append(text(322, 104, '·10 : 11', 't-s', 'start'))
    o.append(text(270, 28, 'остатки', 't-s'))
    for i, (r0, r10, d, r2) in enumerate(steps):
        o.append(phases(n, dur, i)
                 + text(20, 70, f'{r10} = 11·{d} + {r2}', 't', 'start')
                 + text(20, 100, f'цифра {d}, остаток {r2}', 't-red', 'start')
                 + text(20, 140, '3/11 = 0,' + digits[:i + 1] + '…', 't-acc', 'start')
                 + f'<circle class="s-red" cx="270" cy="{64 if r2 == 3 else 156}" r="22" fill="none" stroke-width="3"/>' + '</g>')
    o.append(text(180, 200, 'остаток повторился → цифры повторяются: 0,(27)', 't-s'))
    return ''.join(o)


# ───────────────────────────── 1.3 Алгебраические выражения ─────────────────────────────

@fig('square-of-sum', 'Квадрат суммы на площадях: квадрат со стороной a + b складывается из квадрата a², квадрата b² и двух прямоугольников ab, поэтому (a + b)² = a² + 2ab + b² (на рисунке a = 3, b = 2: 25 = 9 + 6 + 6 + 4)', 360, 230)
def square_of_sum():
    dur = 8
    u = 30  # 1 единица
    a, b = 3, 2
    x0, y0 = 30, 26
    kt = '0;0.12;0.45;0.75;0.92;1'
    o = []
    pieces = [  # (x, y, w, h, класс, подпись, сдвиг при «раздвигании»)
        (0, 0, a, a, 'f-acc', 'a²', (-6, -6)),
        (a, 0, b, a, 'f-red-soft', 'ab', (6, -6)),
        (0, a, a, b, 'f-red-soft', 'ab', (-6, 6)),
        (a, a, b, b, 'f-grn', 'b²', (6, 6)),
    ]
    for px, py, w, h, cls, lab, (dx, dy) in pieces:
        X, Y, W, H = x0 + px * u, y0 + py * u, w * u, h * u
        tr = f'0 0;0 0;{dx} {dy};{dx} {dy};0 0;0 0'
        o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{tr}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<rect class="{cls}" x="{X}" y="{Y}" width="{W}" height="{H}" opacity="0.85"/><rect class="s-ink" x="{X}" y="{Y}" width="{W}" height="{H}" fill="none" stroke-width="1.6"/>'
                 + text(X + W / 2, Y + H / 2 + 6, lab, 't-w' if cls in ('f-acc', 'f-grn') else 't') + '</g>')
    side = (a + b) * u
    o.append(f'<path class="s-mute" d="M{x0},{y0 + side + 10}H{x0 + a * u}M{x0 + a * u},{y0 + side + 10}H{x0 + side}" stroke-width="1.4"/>'
             + text(x0 + a * u / 2, y0 + side + 24, 'a', 't-acc') + text(x0 + a * u + b * u / 2, y0 + side + 24, 'b', 't-grn'))
    tx = x0 + side + 22
    o.append(text(tx, 46, '(a + b)² =', 't', 'start') + text(tx, 68, '= a² + 2ab + b²', 't', 'start'))
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.4;0.95", dur)}' + text(tx, 100, 'a = 3, b = 2:', 't-s', 'start') + text(tx, 122, '25 = 9 + 6 + 6 + 4', 't-acc', 'start') + '</g>')
    o.append(text(tx, 158, 'два прямоугольника ab —', 't-s', 'start') + text(tx, 176, 'это «удвоенное', 't-s', 'start') + text(tx, 194, 'произведение» 2ab', 't-s', 'start'))
    return ''.join(o)


# ───────────────────────────── 1.4 Корни ─────────────────────────────

@fig('sqrt-two-line', 'Как отложить √2 на числовой прямой: диагональ квадрата со стороной 1 равна √(1² + 1²) = √2; циркулем переносим её на прямую — точка лежит между 1,4 и 1,5 и не совпадает ни с одной дробью', 360, 210)
def sqrt_two_line():
    dur = 7
    x0, y0, u = 60, 160, 110
    o = ['<path class="s-ink" d="M20,160H344" stroke-width="2"/>']
    for v in (0, 1, 2):
        o.append(f'<path class="s-mute" d="M{x0 + v * u},154V166" stroke-width="1.6"/>' + text(x0 + v * u, 184, str(v), 't-s'))
    for k in range(1, 10):
        o.append(f'<path class="s-mute" d="M{f(x0 + u + k * u / 10)},157V163" stroke-width="1"/>')
    o.append(f'<rect class="f-soft" x="{x0}" y="{y0 - u}" width="{u}" height="{u}"/><rect class="s-acc" x="{x0}" y="{y0 - u}" width="{u}" height="{u}" fill="none" stroke-width="2"/>')
    o.append(text(x0 + u / 2, y0 - u - 8, '1', 't-acc') + text(x0 - 10, y0 - u / 2 + 4, '1', 't-acc', 'end'))
    o.append(f'<path class="s-red" d="M{x0},{y0}L{x0 + u},{y0 - u}" stroke-width="3"/>' + text(x0 + u / 2 - 14, y0 - u / 2 - 6, '√2', 't-red', 'end'))
    r = u * math.sqrt(2)
    # дуга: от конца диагонали к прямой; рисуется по ходу анимации (stroke-dashoffset)
    arc_len = r * math.pi / 4
    o.append(f'<path class="s-red" d="M{x0 + u},{y0 - u}A{f(r)},{f(r)} 0 0 1 {f(x0 + r)},{y0}" fill="none" stroke-width="2" stroke-dasharray="{f(arc_len)}" stroke-dashoffset="{f(arc_len)}">'
             f'<animate attributeName="stroke-dashoffset" values="{f(arc_len)};{f(arc_len)};0;0;{f(arc_len)}" keyTimes="0;0.15;0.55;0.92;1" dur="{dur}s" repeatCount="indefinite"/></path>')
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.55;0.95", dur)}<circle class="f-red" cx="{f(x0 + r)}" cy="{y0}" r="6"/>'
             + text(x0 + r + 8, y0 - 14, '√2 ≈ 1,414', 't-red', 'start') + text(300, 40, '1² + 1² = 2', 't-s') + '</g>')
    return ''.join(o)


# ───────────────────────────── 1.5 Уравнения ─────────────────────────────

def show_at(t0, t1, dur):
    """Видимость в интервале долей [t0, t1) периода (дискретно)."""
    if t0 == 0:
        return f'<animate attributeName="opacity" values="1;0" keyTimes="0;{t1}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>'
    return f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;{t0};{t1}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>'


@fig('parabola-discriminant', 'Число корней и знак дискриминанта: парабола y = x² − 2x + c поднимается при росте c; c = −3 — D = 16 > 0, два корня −1 и 3; c = 1 — D = 0, один корень 1 (вершина на оси); c = 3 — D = −8 < 0, пересечений с осью нет', 360, 230)
def parabola_discriminant():
    dur = 9
    ox, oy, sx, sy = 110, 150, 30, 14
    X = lambda x: ox + x * sx
    Y = lambda y: oy - y * sy
    o = [f'<path class="s-mute" d="M30,{oy}H232M{ox},20V222" stroke-width="1.4"/>']
    for v in (-1, 1, 2, 3):
        o.append(f'<path class="s-mute" d="M{X(v)},{oy - 4}V{oy + 4}" stroke-width="1.2"/>' + text(X(v), oy + 16, '−1' if v < 0 else str(v), 't-s'))
    o.append(text(236, oy + 4, 'x', 't-s', 'start') + text(ox + 8, 26, 'y', 't-s', 'start'))
    pts = ' '.join(f'{f(X(x))},{f(Y((x - 1) ** 2 - 4))}' for x in lin(-1.6, 3.6, 41))
    kt = '0;0.28;0.36;0.61;0.69;0.95;1'
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 -{4 * sy};0 -{4 * sy};0 -{6 * sy};0 -{6 * sy};0 0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<polyline class="s-acc" points="{pts}" fill="none" stroke-width="2.6"/></g>')
    ph = [
        (0, 0.28, 'c = −3', 'D = 16 > 0', 'два корня', [-1, 3], 't-grn'),
        (0.36, 0.61, 'c = 1', 'D = 0', 'один корень', [1], 't-acc'),
        (0.69, 0.95, 'c = 3', 'D = −8 < 0', 'корней нет', [], 't-red'),
    ]
    for t0, t1, c, d, n, roots, cls in ph:
        g = f'<g opacity="{1 if t0 == 0 else 0}">{show_at(t0, t1, dur)}'
        for r in roots:
            g += f'<circle class="f-red" cx="{X(r)}" cy="{oy}" r="5.5"/>'
        g += text(248, 70, 'x² − 2x + c = 0', 't-s', 'start') + text(248, 98, c, 't', 'start') + text(248, 124, d, cls, 'start') + text(248, 148, n, cls, 'start')
        o.append(g + '</g>')
    return ''.join(o)


# ───────────────────────────── 1.6 Системы уравнений ─────────────────────────────

@fig('lines-intersection', 'Сколько решений у системы двух линейных уравнений: прямые x + 2y = 7 и 3x − y = 7 пересекаются в одной точке (3; 2) — одно решение; параллельные прямые x + 2y = 7 и x + 2y = 3 — решений нет; совпадающие x + 2y = 7 и 2x + 4y = 14 — бесконечно много решений', 360, 220)
def lines_intersection():
    dur = 9
    ox, oy, u = 40, 176, 22
    X = lambda x: ox + x * u
    Y = lambda y: oy - y * u
    seg = lambda fn, x1, x2: f'M{f(X(x1))},{f(Y(fn(x1)))}L{f(X(x2))},{f(Y(fn(x2)))}'
    o = [f'<path class="s-mute" d="M14,{oy}H214M{ox},16V208" stroke-width="1.4"/>']
    for v in range(1, 8):
        o.append(f'<path class="s-mute" d="M{X(v)},{oy - 3}V{oy + 3}" stroke-width="1"/>')
    for v in range(1, 7):
        o.append(f'<path class="s-mute" d="M{ox - 3},{Y(v)}H{ox + 3}" stroke-width="1"/>')
    o.append(text(X(3), oy + 16, '3', 't-s') + text(ox - 8, Y(2) + 4, '2', 't-s', 'end'))
    l1 = lambda x: (7 - x) / 2
    o.append(f'<path class="s-acc" d="{seg(l1, -1, 7.6)}" stroke-width="2.6"/>')
    ph = [
        (0, 0.33, f'<path class="s-red" d="{seg(lambda x: 3 * x - 7, 1.6, 4.25)}" stroke-width="2.6"/>'
         f'<path class="s-mute" d="M{X(3)},{oy}V{Y(2)}H{ox}" stroke-width="1.2" stroke-dasharray="4 3"/><circle class="f-red" cx="{X(3)}" cy="{Y(2)}" r="5.5"/>',
         ['x + 2y = 7', '3x − y = 7'], ['одно решение'], '(3; 2)', 't-grn'),
        (0.33, 0.66, f'<path class="s-red" d="{seg(lambda x: (3 - x) / 2, -1, 6)}" stroke-width="2.6"/>',
         ['x + 2y = 7', 'x + 2y = 3'], ['решений нет'], 'прямые параллельны', 't-red'),
        (0.66, 1, f'<path class="s-red" d="{seg(l1, -1, 7.6)}" stroke-width="2.6" stroke-dasharray="9 7"/>',
         ['x + 2y = 7', '2x + 4y = 14'], ['бесконечно', 'много решений'], 'прямые совпадают', 't-acc'),
    ]
    for t0, t1, art, eqs, n1, n2, cls in ph:
        g = f'<g opacity="{1 if t0 == 0 else 0}">{show_at(t0, t1, dur) if t1 < 1 else show_at(t0, 0.999, dur)}{art}'
        g += text(224, 48, eqs[0], 't-acc', 'start') + text(224, 70, eqs[1], 't-red', 'start') + ''.join(text(224, 110 + 20 * i, s, cls, 'start') for i, s in enumerate(n1)) + text(224, 114 + 20 * len(n1), n2, 't-s', 'start')
        o.append(g + '</g>')
    return ''.join(o)


@fig('circle-line', 'Система «окружность и прямая»: x² + y² = 25, y = x + b. При b = 1 прямая пересекает окружность в двух точках (3; 4) и (−4; −3) — два решения; при b = 5√2 ≈ 7,07 касается — одно решение; при b = 9 проходит мимо — решений нет', 360, 230)
def circle_line():
    dur = 9
    cx, cy, u = 112, 128, 13
    X = lambda x: cx + x * u
    Y = lambda y: cy - y * u
    o = [f'<defs><clipPath id="circle-line-clip"><rect x="14" y="12" width="210" height="210"/></clipPath></defs>']
    o.append(f'<path class="s-mute" d="M24,{cy}H218M{cx},16V222" stroke-width="1.3"/>')
    o.append(f'<circle class="s-acc" cx="{cx}" cy="{cy}" r="{5 * u}" fill="none" stroke-width="2.6"/>')
    o.append(text(X(5) + 4, cy + 14, '5', 't-s', 'start'))
    t = 5 * math.sqrt(2)
    kt = '0;0.28;0.36;0.61;0.69;0.95;1'
    d1, d2 = f((t - 1) * u), f((9 - 1) * u)
    o.append(f'<g clip-path="url(#circle-line-clip)"><g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 -{d1};0 -{d1};0 -{d2};0 -{d2};0 0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<path class="s-red" d="M{f(X(-16))},{f(Y(-15))}L{f(X(8))},{f(Y(9))}" stroke-width="2.4"/></g></g>')
    ph = [
        (0, 0.28, 'b = 1', 'два решения', [(3, 4), (-4, -3)], 't-grn'),
        (0.36, 0.61, 'b = 5√2 ≈ 7,07', 'одно (касание)', [(-t / 2, t / 2)], 't-acc'),
        (0.69, 0.95, 'b = 9', 'решений нет', [], 't-red'),
    ]
    for t0, t1, b, n, pts, cls in ph:
        g = f'<g opacity="{1 if t0 == 0 else 0}">{show_at(t0, t1, dur)}'
        for px, py in pts:
            g += f'<circle class="f-red" cx="{f(X(px))}" cy="{f(Y(py))}" r="5.5"/>'
        g += text(234, 46, 'x² + y² = 25', 't-acc', 'start') + text(234, 68, 'y = x + b', 't-red', 'start') + text(234, 108, b, 't', 'start') + text(234, 132, n, cls, 'start')
        o.append(g + '</g>')
    return ''.join(o)


# ───────────────────────────── 1.7 Неравенства ─────────────────────────────

@fig('sign-chart', 'Метод интервалов для (x + 2)(x − 1)(x − 3) > 0: отмечаем корни −2, 1, 3 выколотыми точками, справа от большего корня знак «+», при переходе через каждый простой корень знак меняется; ответ — промежутки со знаком «+»: (−2; 1) ∪ (3; +∞)', 360, 220)
def sign_chart():
    dur = 9
    P = lambda x: 20 + (x + 3.5) * 40
    y0 = 124
    o = [text(180, 26, '(x + 2)(x − 1)(x − 3) > 0', 't')]
    o.append(f'<path class="s-ink" d="M14,{y0}H346" stroke-width="2"/>')
    # решение — промежутки со знаком «+»
    o.append(f'<g opacity="0">{phase_op("0;0;1;1;0", "0;0.62;0.68;0.95;1", dur)}'
             f'<path class="s-grn" d="M{P(-2)},{y0}H{P(1)}M{P(3)},{y0}H346" stroke-width="7" stroke-linecap="round" opacity="0.55"/>'
             + text(180, 206, 'x ∈ (−2; 1) ∪ (3; +∞)', 't-grn') + '</g>')
    # «змейка» справа налево
    d = (f'M346,{y0 - 50}Q{P(3) + 30},{y0 - 52} {P(3)},{y0}Q{(P(1) + P(3)) / 2},{y0 + 80} {P(1)},{y0}'
         f'Q{(P(-2) + P(1)) / 2},{y0 - 90} {P(-2)},{y0}Q{P(-2) - 30},{y0 + 52} 14,{y0 + 54}')
    o.append(f'<path class="s-red" d="{d}" fill="none" stroke-width="2.4" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">'
             f'<animate attributeName="stroke-dashoffset" values="1;1;0;0;1" keyTimes="0;0.14;0.5;0.95;1" dur="{dur}s" repeatCount="indefinite"/></path>')
    for x, y, s, t in ((P(3) + 34, y0 - 50, '+', 0.2), ((P(1) + P(3)) / 2, y0 + 48, '−', 0.3), ((P(-2) + P(1)) / 2, y0 - 50, '+', 0.4), (P(-2) - 34, y0 + 50, '−', 0.48)):
        o.append(f'<g opacity="0">{phase_op("0;0;1;1;0", f"0;{t};{t + 0.04};0.95;1", dur)}' + text(x, y + 7, s, 't-red' if s == '−' else 't-grn', 'middle', ' style="font-size:24px;font-weight:700"') + '</g>')
    for r in (-2, 1, 3):
        o.append(f'<circle class="f-paper s-ink" cx="{P(r)}" cy="{y0}" r="5.5" stroke-width="2"/>' + text(P(r), y0 + 22, '−2' if r < 0 else str(r), 't-s'))
    return ''.join(o)


@fig('am-gm', 'Среднее арифметическое и среднее геометрическое: на диаметре a + b строим полуокружность; перпендикуляр из точки деления равен √(ab), радиус равен (a + b)/2; перпендикуляр никогда не длиннее радиуса и равен ему только при a = b', 360, 210)
def am_gm():
    dur = 8
    cx, cy, R = 112, 176, 88
    o = [f'<path class="s-acc" d="M{cx - R},{cy}A{R},{R} 0 0 1 {cx + R},{cy}" fill="none" stroke-width="2.4"/>']
    o.append(f'<path class="s-mute" d="M{cx},{cy}V{cy - R}" stroke-width="1.6" stroke-dasharray="5 4"/>' + text(cx + 6, cy - R - 6, '(a + b)/2', 't-s', 'start'))
    ds = [R * 0.8 * math.sin(2 * math.pi * k / 24) for k in range(25)]
    kt = kts(25)
    xs = ';'.join(f(cx + d) for d in ds)
    hs = ';'.join(f(cy - math.sqrt(R * R - d * d)) for d in ds)
    o.append(f'<line class="s-acc" x1="{cx - R}" y1="{cy}" y2="{cy}" stroke-width="6"><animate attributeName="x2" values="{xs}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></line>')
    o.append(f'<line class="s-grn" x2="{cx + R}" y1="{cy}" y2="{cy}" stroke-width="6"><animate attributeName="x1" values="{xs}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></line>')
    o.append(f'<line class="s-red" y1="{cy}" stroke-width="3"><animate attributeName="x1" values="{xs}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="x2" values="{xs}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/><animate attributeName="y2" values="{hs}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></line>')
    o.append(f'<circle class="f-red" r="5"><animate attributeName="cx" values="{xs}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/><animate attributeName="cy" values="{hs}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(text(cx - R + 14, cy + 22, 'a', 't-acc') + text(cx + R - 14, cy + 22, 'b', 't-grn'))
    o.append(text(214, 56, '√(ab) ≤ (a + b)/2', 't', 'start') + text(214, 82, 'красный = √(ab)', 't-red', 'start') + text(214, 100, 'не длиннее радиуса', 't-s', 'start') + text(214, 124, 'равенство при a = b', 't-s', 'start'))
    return ''.join(o)


# ───────────────────────────── 1.8 Модуль ─────────────────────────────

@fig('abs-distance', 'Модуль как расстояние: |x − 2| — расстояние от точки x до точки 2. Точка x = 6 удалена на 4, x = 0 — на 2, x = 5 — ровно на 3; поэтому |x − 2| ≤ 3 — это все точки на расстоянии не больше 3 от 2, отрезок [−1; 5]', 360, 200)
def abs_distance():
    dur = 10
    P = lambda x: 40 + (x + 2) * 30
    y0 = 120
    o = [f'<path class="s-ink" d="M16,{y0}H344" stroke-width="2"/>']
    for v in range(-2, 9):
        o.append(f'<path class="s-mute" d="M{P(v)},{y0 - 4}V{y0 + 4}" stroke-width="1.2"/>' + text(P(v), y0 + 20, ('−' + str(-v)) if v < 0 else str(v), 't-s'))
    o.append(f'<g opacity="0">{phase_op("0;0;1;1;0", "0;0.72;0.76;0.96;1", dur)}<path class="s-grn" d="M{P(-1)},{y0}H{P(5)}" stroke-width="8" stroke-linecap="round" opacity="0.5"/>'
             f'<circle class="f-grn" cx="{P(-1)}" cy="{y0}" r="5.5"/><circle class="f-grn" cx="{P(5)}" cy="{y0}" r="5.5"/>' + text(180, 176, '|x − 2| ≤ 3  ⇔  −1 ≤ x ≤ 5', 't-grn') + '</g>')
    xs = [6, 6, 0, 0, 5, 5, 5, 6]
    kt = '0;0.2;0.28;0.46;0.54;0.72;0.96;1'
    cx = ';'.join(f(P(x)) for x in xs)
    o.append(f'<line class="s-red" x1="{P(2)}" y1="{y0 - 26}" y2="{y0 - 26}" stroke-width="3"><animate attributeName="x2" values="{cx}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></line>')
    o.append(f'<circle class="f-red" cy="{y0}" r="6"><animate attributeName="cx" values="{cx}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(f'<circle class="f-acc" cx="{P(2)}" cy="{y0}" r="6"/>')
    for t0, t1, x, d in ((0, 0.2, 6, 4), (0.28, 0.46, 0, 2), (0.54, 0.72, 5, 3)):
        o.append(f'<g opacity="{1 if t0 == 0 else 0}">{show_at(t0, t1, dur)}' + text(P(x), y0 + 40, 'x', 't-red')
                 + text(180, 36, f'x = {x}:  |{x} − 2| = {d}', 't', 'middle') + text(180, 58, 'дальше 3 — вне' if d > 3 else ('ровно 3 — граница' if d == 3 else 'ближе 3 — внутри'), 't-s') + '</g>')
    return ''.join(o)


# ───────────────────────────── 1.9 Иррациональные уравнения ─────────────────────────────

@fig('extraneous-root', 'Откуда берётся посторонний корень: √(x + 2) = x — это пересечение верхней ветви y = √(x + 2) с прямой y = x, точка (2; 2). После возведения в квадрат уравнение x + 2 = x² описывает обе ветви y = ±√(x + 2), и появляется лишняя точка (−1; −1) на нижней ветви — посторонний корень x = −1', 360, 230)
def extraneous_root():
    dur = 9
    ox, oy, u = 120, 118, 30
    X = lambda x: ox + x * u
    Y = lambda y: oy - y * u
    o = [f'<path class="s-mute" d="M24,{oy}H262M{ox},12V224" stroke-width="1.3"/>']
    for v in (-2, -1, 1, 2, 3):
        o.append(f'<path class="s-mute" d="M{X(v)},{oy - 3}V{oy + 3}" stroke-width="1"/>' + text(X(v), oy + 16, ('−' + str(-v)) if v < 0 else str(v), 't-s'))
    o.append(f'<path class="s-ink" d="M{X(-2.8)},{Y(-2.8)}L{X(3.4)},{Y(3.4)}" stroke-width="2"/>' + text(X(3.3) + 6, Y(3.3) + 4, 'y = x', 't-s', 'start'))
    up = ' '.join(f'{f(X(y * y - 2))},{f(Y(y))}' for y in lin(0, 2.35, 30))
    dn = ' '.join(f'{f(X(y * y - 2))},{f(Y(y))}' for y in lin(0, -2.35, 30))
    o.append(f'<polyline class="s-acc" points="{up}" fill="none" stroke-width="2.8"/>' + text(X(-0.25), Y(1.55), 'y = √(x + 2)', 't-acc', 'end'))
    o.append(f'<circle class="f-grn" cx="{X(2)}" cy="{Y(2)}" r="6"/>')
    o.append(f'<g opacity="0">{phase_op("0;0;1;1;0", "0;0.4;0.48;0.95;1", dur)}<polyline class="s-red" points="{dn}" fill="none" stroke-width="2.4" stroke-dasharray="7 5"/>'
             f'<circle class="f-red" cx="{X(-1)}" cy="{Y(-1)}" r="6"/>' + text(X(3.5), Y(-2.3) + 16, 'y = −√(x + 2)', 't-red', 'end') + '</g>')
    o.append(f'<g>{show_at(0, 0.44, dur)}' + text(272, 50, '√(x + 2) = x', 't', 'start') + text(272, 76, 'одна точка', 't-s', 'start') + text(272, 98, 'x = 2', 't-grn', 'start') + '</g>')
    o.append(f'<g opacity="0">{show_at(0.44, 0.96, dur)}' + text(272, 50, 'x + 2 = x²', 't', 'start') + text(272, 76, 'корни 2 и −1', 't-s', 'start') + text(272, 98, 'x = 2 ✓', 't-grn', 'start')
             + text(272, 120, 'x = −1', 't-red', 'start') + text(272, 140, 'посторонний', 't-s', 'start') + '</g>')
    return ''.join(o)


# ───────────────────────────── 1.10 Прогрессии ─────────────────────────────

@fig('gauss-sum', 'Сумма арифметической прогрессии: две одинаковые «лесенки» 1, 2, …, 6 (вторая перевёрнута) складываются в прямоугольник 6 × 7, поэтому 1 + 2 + … + 6 = 6·7/2 = 21; в общем виде Sₙ = (a₁ + aₙ)·n/2', 360, 220)
def gauss_sum():
    dur = 8
    n, c = 6, 20
    x0, y0 = 40, 190
    o = []
    for i in range(n):
        h = i + 1
        o.append(f'<rect class="f-acc" x="{x0 + i * c}" y="{y0 - h * c}" width="{c}" height="{h * c}" opacity="0.85"/><rect class="s-ink" x="{x0 + i * c}" y="{y0 - h * c}" width="{c}" height="{h * c}" fill="none" stroke-width="1"/>'
                 + text(x0 + i * c + c / 2, y0 + 16, str(h), 't-s'))
    g = []
    for i in range(n):
        h = n - i
        top = y0 - (n + 1) * c
        g.append(f'<rect class="f-grn" x="{x0 + i * c}" y="{top}" width="{c}" height="{h * c}" opacity="0.8"/><rect class="s-ink" x="{x0 + i * c}" y="{top}" width="{c}" height="{h * c}" fill="none" stroke-width="1"/>')
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="150 0;150 0;0 0;0 0;150 0" keyTimes="0;0.2;0.5;0.92;1" dur="{dur}s" repeatCount="indefinite"/>{"".join(g)}</g>')
    o.append(f'<g opacity="0">{phase_op("0;0;1;1;0", "0;0.5;0.56;0.92;1", dur)}<rect class="s-red" x="{x0}" y="{y0 - (n + 1) * c}" width="{n * c}" height="{(n + 1) * c}" fill="none" stroke-width="2.6"/>'
             + text(x0 + n * c + 14, y0 - (n + 1) * c / 2, '7', 't-red', 'start') + text(220, 80, '2S = 6 · 7 = 42', 't', 'start') + text(220, 106, 'S = 21', 't-red', 'start')
             + text(220, 140, 'Sₙ = (a₁ + aₙ)·n/2', 't-s', 'start') + '</g>')
    o.append(text(x0, 30, '1 + 2 + … + 6 = ?', 't-acc', 'start'))
    return ''.join(o)


@fig('geo-series', 'Бесконечно убывающая геометрическая прогрессия: 1/2 + 1/4 + 1/8 + … — каждый новый кусок закрывает половину оставшейся части квадрата, поэтому сумма равна 1 = b₁/(1 − q) = (1/2)/(1 − 1/2)', 360, 220)
def geo_series():
    dur = 9
    x0, y0, s = 40, 20, 180
    o = [f'<rect class="s-ink" x="{x0}" y="{y0}" width="{s}" height="{s}" fill="none" stroke-width="2"/>']
    x, y, w, h = x0, y0, s, s
    labels = ['1/2', '1/4', '1/8', '1/16', '1/32', '1/64', '', '']
    for k in range(8):
        if k % 2 == 0:
            rx, ry, rw, rh = x, y, w / 2, h
            x, w = x + w / 2, w / 2
        else:
            rx, ry, rw, rh = x, y, w, h / 2
            y, h = y + h / 2, h / 2
        t = 0.08 + k * 0.09
        cls = 'f-acc' if k % 2 == 0 else 'f-grn'
        o.append(f'<g opacity="0">{phase_op("0;0;1;1;0", f"0;{f(t)};{f(t + 0.05)};0.95;1", dur)}<rect class="{cls}" x="{f(rx)}" y="{f(ry)}" width="{f(rw)}" height="{f(rh)}" opacity="{0.9 - k * 0.07:.2f}"/>'
                 f'<rect class="s-ink" x="{f(rx)}" y="{f(ry)}" width="{f(rw)}" height="{f(rh)}" fill="none" stroke-width="1"/>'
                 + (text(rx + rw / 2, ry + rh / 2 + 5, labels[k], 't-w' if k < 4 else 't-s') if labels[k] and k < 5 else '') + '</g>')
    o.append(text(238, 44, '1/2 + 1/4 + 1/8 + … = 1', 't', 'start'))
    o.append(f'<g opacity="0">{phase_op("0;0;1;1;0", "0;0.8;0.85;0.95;1", dur)}' + text(238, 80, 'S = b₁/(1 − q)', 't-acc', 'start') + text(238, 104, '= (1/2)/(1/2) = 1', 't-acc', 'start') + '</g>')
    o.append(text(238, 140, 'q = 1/2, |q| < 1', 't-s', 'start'))
    return ''.join(o)


# ───────────────────────────── 1.11 Текстовые задачи ─────────────────────────────

@fig('meeting-motion', 'Движение навстречу: расстояние 360 км, автомобили едут навстречу со скоростями 70 и 50 км/ч; расстояние между ними уменьшается на 70 + 50 = 120 км каждый час, поэтому встреча через 360 : 120 = 3 ч; первый проедет 210 км, второй 150 км', 360, 200)
def meeting_motion():
    dur = 8
    x0, x1, y = 30, 330, 110
    k = (x1 - x0) / 360
    xm = x0 + 210 * k
    o = [f'<path class="s-ink" d="M{x0},{y + 14}H{x1}" stroke-width="2"/>']
    for km in range(0, 361, 60):
        o.append(f'<path class="s-mute" d="M{f(x0 + km * k)},{y + 10}V{y + 18}" stroke-width="1.2"/>' + text(x0 + km * k, y + 34, str(km), 't-s'))
    o.append(text(x1, y + 52, 'км', 't-s', 'end'))
    kt = '0;0.1;0.7;0.95;1'
    a = f'0 0;0 0;{f(xm - x0)} 0;{f(xm - x0)} 0;0 0'
    b = f'0 0;0 0;{f(xm - x1)} 0;{f(xm - x1)} 0;0 0'
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{a}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<rect class="f-acc" x="{x0 - 14}" y="{y - 6}" width="28" height="14" rx="4"/>' + text(x0, y - 14, '70 км/ч', 't-acc') + '</g>')
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{b}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<rect class="f-red" x="{x1 - 14}" y="{y - 6}" width="28" height="14" rx="4"/>' + text(x1, y - 32, '50 км/ч', 't-red') + '</g>')
    o.append(text(180, 30, 'сближение: 70 + 50 = 120 км/ч', 't'))
    o.append(f'<g opacity="0">{phase_op("0;0;1;1;0", "0;0.7;0.74;0.95;1", dur)}<path class="s-grn" d="M{f(xm)},{y - 40}V{y + 14}" stroke-width="2" stroke-dasharray="4 3"/>'
             + text(180, 56, 't = 360 : 120 = 3 ч', 't-grn') + text(xm - 6, y + 70, '210 км', 't-acc', 'end') + text(xm + 6, y + 70, '150 км', 't-red', 'start') + '</g>')
    return ''.join(o)


@fig('work-rates', 'Совместная работа: первая труба наполняет бак за 6 ч (1/6 бака в час), вторая — за 3 ч (1/3 бака в час); вместе 1/6 + 1/3 = 1/2 бака в час, поэтому бак наполнится за 2 ч', 360, 220)
def work_rates():
    dur = 9
    T = 0.8  # доля периода на 6 часов
    H, y0, w = 116, 158, 56
    o = []
    for i, (t, cls, lab) in enumerate(((6, 'f-acc', 'первая: 6 ч'), (3, 'f-grn', 'вторая: 3 ч'), (2, 'f-red', 'вместе: 2 ч'))):
        x = 34 + i * 100
        o.append(f'<rect class="s-ink" x="{x}" y="{y0 - H}" width="{w}" height="{H}" fill="none" stroke-width="2"/>')
        te = t / 6 * T
        o.append(f'<rect class="{cls}" x="{x + 2}" width="{w - 4}" opacity="0.85">'
                 f'<animate attributeName="height" values="0;{H - 2};{H - 2};0" keyTimes="0;{f(te)};0.96;1" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y" values="{y0};{y0 - H + 2};{y0 - H + 2};{y0}" keyTimes="0;{f(te)};0.96;1" dur="{dur}s" repeatCount="indefinite"/></rect>')
        o.append(text(x + w / 2, y0 + 20, lab, 't-s'))
        o.append(text(x + w / 2, y0 - H - 10, ['1/6 в час', '1/3 в час', '1/6 + 1/3 = 1/2'][i], 't-s'))
    o.append(f'<path class="s-mute" d="M30,{y0 + 34}H330" stroke-width="1.2"/>')
    for h in range(7):
        o.append(f'<path class="s-mute" d="M{30 + h * 50},{y0 + 30}V{y0 + 38}" stroke-width="1"/>')
    o.append(f'<circle class="f-ink" cy="{y0 + 34}" r="4.5"><animate attributeName="cx" values="30;330;330;30" keyTimes="0;{T};0.96;1" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(text(334, y0 + 30, '6 ч', 't-s', 'end') + text(30, y0 + 52, '0', 't-s') + text(130, y0 + 52, '2 ч', 't-s') + text(180, y0 + 52, '3 ч', 't-s'))
    return ''.join(o)


# ───────────────────────────── 1.12 Функции ─────────────────────────────

@fig('line-slope', 'Угловой коэффициент прямой y = kx + 1: прямая поворачивается вокруг точки (0; 1); при k > 0 функция возрастает, при k = 0 прямая горизонтальна, при k < 0 функция убывает; b = 1 — точка пересечения с осью Oy', 360, 220)
def line_slope():
    dur = 9
    ox, oy, u = 120, 130, 30
    py = oy - u
    o = [f'<path class="s-mute" d="M20,{oy}H236M{ox},16V214" stroke-width="1.3"/>']
    for v in (-3, -2, -1, 1, 2, 3):
        o.append(f'<path class="s-mute" d="M{ox + v * u},{oy - 3}V{oy + 3}" stroke-width="1"/>')
    o.append(text(240, oy + 4, 'x', 't-s', 'start') + text(ox + 8, 24, 'y', 't-s', 'start'))
    kt = '0;0.28;0.36;0.61;0.69;0.95;1'
    o.append(f'<g><animateTransform attributeName="transform" type="rotate" values="-45 {ox} {py};-45 {ox} {py};0 {ox} {py};0 {ox} {py};45 {ox} {py};45 {ox} {py};-45 {ox} {py}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<path class="s-acc" d="M{ox - 108},{py}H{ox + 108}" stroke-width="2.8"/></g>')
    o.append(f'<circle class="f-red" cx="{ox}" cy="{py}" r="5.5"/>' + text(ox - 36, py - 8, 'b = 1', 't-red', 'end'))
    for t0, t1, k, n, cls in ((0, 0.28, 'k = 1 > 0', 'возрастает', 't-grn'), (0.36, 0.61, 'k = 0', 'постоянна', 't-acc'), (0.69, 0.95, 'k = −1 < 0', 'убывает', 't-red')):
        o.append(f'<g opacity="{1 if t0 == 0 else 0}">{show_at(t0, t1, dur)}' + text(250, 60, 'y = kx + 1', 't', 'start') + text(250, 90, k, cls, 'start') + text(250, 114, n, cls, 'start') + '</g>')
    o.append(text(250, 150, 'k = tg α', 't-s', 'start'))
    return ''.join(o)


@fig('parabola-vertex', 'Сдвиги параболы: график y = (x − 2)² − 3 получается из y = x² сдвигом на 2 вправо и на 3 вниз; вершина (2; −3), ось симметрии x = 2. Так же y = ax² + bx + c приводится к виду a(x − x₀)² + y₀, где x₀ = −b/(2a)', 360, 230)
def parabola_vertex():
    dur = 9
    ox, oy, u = 100, 120, 22
    X = lambda x: ox + x * u
    Y = lambda y: oy - y * u
    o = [f'<path class="s-mute" d="M16,{oy}H250M{ox},10V226" stroke-width="1.3"/>']
    for v in (-3, -2, -1, 1, 2, 3, 4, 5):
        o.append(f'<path class="s-mute" d="M{X(v)},{oy - 3}V{oy + 3}" stroke-width="1"/>')
    o.append(text(X(2), oy + 16, '2', 't-s'))
    pts = ' '.join(f'{f(X(x))},{f(Y(x * x))}' for x in lin(-2.3, 2.3, 31))
    o.append(f'<polyline class="s-mute" points="{pts}" fill="none" stroke-width="1.6" stroke-dasharray="5 4"/>')
    kt = '0;0.2;0.35;0.5;0.65;0.95;1'
    tr = f'0 0;0 0;{2 * u} 0;{2 * u} 0;{2 * u} {3 * u};{2 * u} {3 * u};0 0'
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{tr}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<polyline class="s-acc" points="{pts}" fill="none" stroke-width="2.8"/><circle class="f-red" cx="{X(0)}" cy="{Y(0)}" r="5.5"/></g>')
    o.append(f'<g opacity="0">{phase_op("0;0;1;1;0", "0;0.65;0.7;0.95;1", dur)}<path class="s-red" d="M{X(2)},14V222" stroke-width="1.4" stroke-dasharray="4 3"/>'
             + text(X(2) + 8, Y(-3) + 18, '(2; −3)', 't-red', 'start') + '</g>')
    for t0, t1, s in ((0, 0.2, 'y = x²'), (0.35, 0.5, 'y = (x − 2)²'), (0.65, 0.95, 'y = (x − 2)² − 3')):
        o.append(f'<g opacity="{1 if t0 == 0 else 0}">{show_at(t0, t1, dur)}' + text(256, 50, s, 't-acc', 'start') + '</g>')
    o.append(text(256, 90, 'вправо на 2,', 't-s', 'start') + text(256, 108, 'вниз на 3', 't-s', 'start') + text(256, 140, 'x₀ = −b/(2a)', 't-s', 'start'))
    return ''.join(o)


@fig('inverse-mirror', 'График обратной функции симметричен графику исходной относительно прямой y = x: точка (a; b) графика y = x²/4 (x ≥ 0) переходит в точку (b; a) графика обратной функции y = 2√x', 360, 230)
def inverse_mirror():
    dur = 8
    ox, oy, u = 40, 200, 34
    X = lambda x: ox + x * u
    Y = lambda y: oy - y * u
    o = [f'<path class="s-mute" d="M{ox - 20},{oy}H{X(5.6)}M{ox},{oy + 20}V{Y(5.6)}" stroke-width="1.3"/>']
    o.append(f'<path class="s-ink" d="M{X(-0.3)},{Y(-0.3)}L{X(5.4)},{Y(5.4)}" stroke-width="1.6" stroke-dasharray="6 4"/>' + text(X(5.4), Y(5.4) - 6, 'y = x', 't-s', 'end'))
    f1 = ' '.join(f'{f(X(x))},{f(Y(x * x / 4))}' for x in lin(0, 3.8, 30))
    f2 = ' '.join(f'{f(X(x * x / 4))},{f(Y(x))}' for x in lin(0, 3.8, 30))
    o.append(f'<polyline class="s-acc" points="{f1}" fill="none" stroke-width="2.8"/>' + text(X(3.8) + 6, Y(3.61) + 4, 'y = x²/4', 't-acc', 'start'))
    o.append(f'<polyline class="s-red" points="{f2}" fill="none" stroke-width="2.8"/>' + text(X(3.61) - 8, Y(3.8) - 2, 'y = 2√x', 't-red', 'end'))
    ts = [0.7 + 2.6 * (0.5 - 0.5 * math.cos(2 * math.pi * k / 24)) for k in range(25)]
    kt = kts(25)
    ax = ';'.join(f(X(t)) for t in ts); ay = ';'.join(f(Y(t * t / 4)) for t in ts)
    bx = ';'.join(f(X(t * t / 4)) for t in ts); by = ';'.join(f(Y(t)) for t in ts)
    an = lambda attr, v: f'<animate attributeName="{attr}" values="{v}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
    o.append(f'<line class="s-mute" stroke-width="1.4" stroke-dasharray="3 3">{an("x1", ax)}{an("y1", ay)}{an("x2", bx)}{an("y2", by)}</line>')
    o.append(f'<circle class="f-acc" r="5.5">{an("cx", ax)}{an("cy", ay)}</circle><circle class="f-red" r="5.5">{an("cx", bx)}{an("cy", by)}</circle>')
    o.append(text(250, 50, '(a; b) → (b; a)', 't', 'start') + text(250, 76, 'зеркало — y = x', 't-s', 'start'))
    return ''.join(o)


# ───────────────────────────── 1.13–1.14 Показательная и логарифмическая функции ─────────────────────────────

@fig('exp-graphs', 'Показательная функция y = aˣ: при a > 1 (здесь 2ˣ) она возрастает, при 0 < a < 1 (здесь (1/2)ˣ) убывает; все графики проходят через точку (0; 1) и лежат выше оси Ox — значения всегда положительны', 360, 230)
def exp_graphs():
    dur = 8
    ox, oy, u = 132, 200, 28
    X = lambda x: ox + x * u
    Y = lambda y: oy - y * u
    o = [f'<path class="s-mute" d="M12,{oy}H262M{ox},14V214" stroke-width="1.3"/>']
    for v in (-4, -3, -2, -1, 1, 2, 3, 4):
        o.append(f'<path class="s-mute" d="M{X(v)},{oy - 3}V{oy + 3}" stroke-width="1"/>')
    for v in (1, 2, 3, 4, 5, 6):
        o.append(f'<path class="s-mute" d="M{ox - 3},{Y(v)}H{ox + 3}" stroke-width="1"/>')
    o.append(text(ox - 6, Y(1) + 4, '1', 't-s', 'end') + text(ox - 6, Y(4) + 4, '4', 't-s', 'end'))
    up = ' '.join(f'{f(X(x))},{f(Y(2 ** x))}' for x in lin(-4.5, 2.6, 40))
    dn = ' '.join(f'{f(X(x))},{f(Y(0.5 ** x))}' for x in lin(-2.6, 4.5, 40))
    o.append(f'<polyline class="s-acc" points="{up}" fill="none" stroke-width="2.8"/>' + text(X(2.6) + 4, Y(6) + 4, 'y = 2ˣ', 't-acc', 'start'))
    o.append(f'<polyline class="s-red" points="{dn}" fill="none" stroke-width="2.8"/>' + text(X(-2.6) - 4, Y(6) + 4, '(1/2)ˣ', 't-red', 'end'))
    o.append(f'<circle class="f-ink" cx="{ox}" cy="{Y(1)}" r="4.5"/>')
    xs = [-3 + 5.5 * (0.5 - 0.5 * math.cos(2 * math.pi * k / 24)) for k in range(25)]
    kt = kts(25)
    an = lambda attr, v: f'<animate attributeName="{attr}" values="{v}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
    cx = ';'.join(f(X(x)) for x in xs)
    o.append(f'<circle class="f-acc" r="5.5">{an("cx", cx)}{an("cy", ";".join(f(Y(2 ** x)) for x in xs))}</circle>')
    o.append(f'<circle class="f-red" r="5.5">{an("cx", ";".join(f(X(-x)) for x in xs))}{an("cy", ";".join(f(Y(2 ** x)) for x in xs))}</circle>')
    o.append(text(274, 60, 'a > 1:', 't-acc', 'start') + text(274, 80, 'возрастает', 't-s', 'start') + text(274, 112, '0 < a < 1:', 't-red', 'start') + text(274, 132, 'убывает', 't-s', 'start') + text(274, 166, 'aˣ > 0', 't', 'start'))
    return ''.join(o)


@fig('log-exp-mirror', 'Логарифмическая функция y = log₂x — обратная к y = 2ˣ: её график симметричен графику 2ˣ относительно прямой y = x. Точка (3; 8) графика 2ˣ переходит в точку (8; 3) графика log₂x; логарифм определён только при x > 0 и проходит через (1; 0)', 360, 230)
def log_exp_mirror():
    dur = 8
    ox, oy, u = 70, 170, 19
    X = lambda x: ox + x * u
    Y = lambda y: oy - y * u
    o = [f'<path class="s-mute" d="M14,{oy}H{X(9.6)}M{ox},10V224" stroke-width="1.3"/>']
    for v in range(1, 10):
        o.append(f'<path class="s-mute" d="M{X(v)},{oy - 3}V{oy + 3}" stroke-width="1"/>')
    for v in range(-2, 9):
        if v:
            o.append(f'<path class="s-mute" d="M{ox - 3},{Y(v)}H{ox + 3}" stroke-width="1"/>')
    o.append(text(X(1), oy + 16, '1', 't-s') + text(X(8), oy + 16, '8', 't-s') + text(ox - 6, Y(1) + 4, '1', 't-s', 'end') + text(ox - 6, Y(8) + 4, '8', 't-s', 'end'))
    o.append(f'<path class="s-ink" d="M{X(-2.5)},{Y(-2.5)}L{X(8.2)},{Y(8.2)}" stroke-width="1.5" stroke-dasharray="6 4"/>' + text(X(8.2) + 4, Y(8.2) + 4, 'y = x', 't-s', 'start'))
    e = ' '.join(f'{f(X(x))},{f(Y(2 ** x))}' for x in lin(-3, 3.1, 40))
    l = ' '.join(f'{f(X(2 ** x))},{f(Y(x))}' for x in lin(-3, 3.1, 40))
    o.append(f'<polyline class="s-acc" points="{e}" fill="none" stroke-width="2.8"/>' + text(X(2.6) - 10, Y(6.5), 'y = 2ˣ', 't-acc', 'end'))
    o.append(f'<polyline class="s-red" points="{l}" fill="none" stroke-width="2.8"/>' + text(X(8.6), Y(3.1) + 26, 'y = log₂x', 't-red', 'end'))
    ts = [-1 + 4 * (0.5 - 0.5 * math.cos(2 * math.pi * k / 24)) for k in range(25)]
    kt = kts(25)
    an = lambda attr, v: f'<animate attributeName="{attr}" values="{v}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
    ax = ';'.join(f(X(t)) for t in ts); ay = ';'.join(f(Y(2 ** t)) for t in ts)
    bx = ';'.join(f(X(2 ** t)) for t in ts); by = ';'.join(f(Y(t)) for t in ts)
    o.append(f'<line class="s-mute" stroke-width="1.3" stroke-dasharray="3 3">{an("x1", ax)}{an("y1", ay)}{an("x2", bx)}{an("y2", by)}</line>')
    o.append(f'<circle class="f-acc" r="5">{an("cx", ax)}{an("cy", ay)}</circle><circle class="f-red" r="5">{an("cx", bx)}{an("cy", by)}</circle>')
    o.append(f'<circle class="f-ink" cx="{X(1)}" cy="{oy}" r="4"/><circle class="f-ink" cx="{ox}" cy="{Y(1)}" r="4"/>')
    o.append(text(262, 44, '2³ = 8', 't-acc', 'start') + text(262, 66, 'log₂8 = 3', 't-red', 'start') + text(262, 100, 'x > 0', 't-s', 'start'))
    return ''.join(o)


# ───────────────────────────── 1.15 Тригонометрия ─────────────────────────────

@fig('unit-circle', 'Единичная окружность: точка поворачивается на угол α от положительного направления оси Ox; её абсцисса — cos α, ордината — sin α. Поэтому sin²α + cos²α = 1, а знаки синуса и косинуса зависят от четверти', 360, 230)
def unit_circle():
    dur = 12
    cx, cy, R = 120, 118, 92
    o = [f'<path class="s-mute" d="M{cx - R - 18},{cy}H{cx + R + 18}M{cx},{cy - R - 16}V{cy + R + 14}" stroke-width="1.3"/>']
    o.append(f'<circle class="s-ink" cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke-width="2"/>')
    o.append(text(cx + R + 6, cy + 16, '1', 't-s', 'start') + text(cx - R - 6, cy + 16, '−1', 't-s', 'end') + text(cx + 8, cy - R - 4, '1', 't-s', 'start'))
    for q, (x, y) in (('I', (1, -1)), ('II', (-1, -1)), ('III', (-1, 1)), ('IV', (1, 1))):
        o.append(text(cx + x * 62, cy + y * 62 + 4, q, 't-s'))
    n = 49
    ang = [2 * math.pi * k / (n - 1) for k in range(n)]
    kt = kts(n)
    px = ';'.join(f(cx + R * math.cos(a)) for a in ang)
    py = ';'.join(f(cy - R * math.sin(a)) for a in ang)
    an = lambda attr, v: f'<animate attributeName="{attr}" values="{v}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
    # дуга угла: рисуется по ходу вращения (pathLength)
    o.append(f'<circle class="s-acc" cx="{cx}" cy="{cy}" r="22" fill="none" stroke-width="2" pathLength="1" stroke-dasharray="1" transform="rotate(0 {cx} {cy}) scale(1 -1) translate(0 {-2 * cy})">'
             f'<animate attributeName="stroke-dashoffset" values="1;0" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(f'<line class="s-ink" x1="{cx}" y1="{cy}" stroke-width="2">{an("x2", px)}{an("y2", py)}</line>')
    o.append(f'<line class="s-acc" y1="{cy}" y2="{cy}" x1="{cx}" stroke-width="5">{an("x2", px)}</line>')
    o.append(f'<line class="s-red" stroke-width="5">{an("x1", px)}{an("x2", px)}<set attributeName="y1" to="{cy}"/>{an("y2", py)}</line>')
    o.append(f'<circle class="f-red" r="6">{an("cx", px)}{an("cy", py)}</circle>')
    o.append(text(240, 50, 'cos α = x', 't-acc', 'start') + text(240, 74, 'sin α = y', 't-red', 'start') + text(240, 110, 'sin²α + cos²α = 1', 't-s', 'start'))
    o.append(text(240, 146, 'знаки:', 't-s', 'start') + text(240, 166, 'I: sin +, cos +', 't-s', 'start') + text(240, 184, 'II: sin +, cos −', 't-s', 'start') + text(240, 202, 'III: −, −; IV: −, +', 't-s', 'start'))
    return ''.join(o)


@fig('sin-equation', 'Уравнение sin x = a на графике: прямая y = a пересекает синусоиду на отрезке [0; 2π] в двух точках при |a| < 1 (для a = 1/2 это π/6 и 5π/6), в одной — при a = 1 (x = π/2) и ни в одной — при |a| > 1; с периодом 2π корни повторяются', 360, 220)
def sin_equation():
    dur = 12
    ox, oy, sx, sy = 30, 110, 40, 60
    X = lambda x: ox + x * sx
    Y = lambda y: oy - y * sy
    o = [f'<path class="s-mute" d="M14,{oy}H{X(2 * math.pi) + 14}M{ox},28V196" stroke-width="1.3"/>']
    for k, lab in ((1, 'π/2'), (2, 'π'), (3, '3π/2'), (4, '2π')):
        o.append(f'<path class="s-mute" d="M{f(X(k * math.pi / 2))},{oy - 3}V{oy + 3}" stroke-width="1"/>' + text(X(k * math.pi / 2), oy + 16, lab, 't-s'))
    o.append(text(ox - 6, Y(1) + 4, '1', 't-s', 'end') + text(ox - 6, Y(-1) + 4, '−1', 't-s', 'end'))
    pts = ' '.join(f'{f(X(x))},{f(Y(math.sin(x)))}' for x in lin(0, 2 * math.pi, 60))
    o.append(f'<polyline class="s-acc" points="{pts}" fill="none" stroke-width="2.6"/>')
    ph = [(0, 0.24, 0.5, 'a = 1/2', 'два корня: π/6, 5π/6', 't-grn'), (0.25, 0.49, 1, 'a = 1', 'один корень: π/2', 't-acc'),
          (0.5, 0.74, -0.5, 'a = −1/2', 'два корня: 7π/6, 11π/6', 't-grn'), (0.75, 0.99, 1.3, 'a = 1,3', 'корней нет: |a| > 1', 't-red')]
    for t0, t1, a, la, lb, cls in ph:
        g = f'<g opacity="{1 if t0 == 0 else 0}">{show_at(t0, t1, dur)}<path class="s-red" d="M14,{f(Y(a))}H{X(2 * math.pi) + 14}" stroke-width="2" stroke-dasharray="6 4"/>'
        if abs(a) <= 1:
            r = math.asin(a)
            xs = sorted({(r) % (2 * math.pi), (math.pi - r) % (2 * math.pi)})
            for x in xs:
                g += f'<circle class="f-red" cx="{f(X(x))}" cy="{f(Y(a))}" r="5.5"/>'
        g += text(300, 50, la, 't-red', 'start') + text(300, 74, '', 't-s', 'start') + text(180, 214, lb, cls)
        o.append(g + '</g>')
    o.append(text(300, 100, 'y = sin x', 't-acc', 'start'))
    return ''.join(o)


@fig('sine-period', 'Период функции y = sin(kx) равен 2π/k: при k = 1 — 2π, при k = 2 график сжимается вдвое (период π), при k = 1/2 растягивается вдвое (период 4π); амплитуда 1 не меняется', 360, 200)
def sine_period():
    dur = 9
    ox, oy, sx, sy = 20, 100, 20, 52
    X = lambda x: ox + x * sx
    Y = lambda y: oy - y * sy
    o = [f'<path class="s-mute" d="M10,{oy}H{X(4 * math.pi) + 8}M{ox},36V164" stroke-width="1.3"/>']
    for k, lab in ((1, 'π'), (2, '2π'), (4, '4π')):
        o.append(f'<path class="s-mute" d="M{f(X(k * math.pi))},{oy - 3}V{oy + 3}" stroke-width="1"/>' + text(X(k * math.pi), oy + 16, lab, 't-s'))
    for t0, t1, k, lab, T, cls in ((0, 0.33, 1, 'y = sin x', 'T = 2π', 's-acc'), (0.33, 0.66, 2, 'y = sin 2x', 'T = π', 's-red'), (0.66, 0.999, 0.5, 'y = sin(x/2)', 'T = 4π', 's-grn')):
        pts = ' '.join(f'{f(X(x))},{f(Y(math.sin(k * x)))}' for x in lin(0, 4 * math.pi, 120))
        tcls = {'s-acc': 't-acc', 's-red': 't-red', 's-grn': 't-grn'}[cls]
        per = 2 * math.pi / k
        o.append(f'<g opacity="{1 if t0 == 0 else 0}">{show_at(t0, t1, dur)}<polyline class="{cls}" points="{pts}" fill="none" stroke-width="2.6"/>'
                 f'<path class="{cls}" d="M{ox},{Y(-1) + 22}H{f(X(per))}" stroke-width="2"/><path class="{cls}" d="M{ox},{Y(-1) + 16}V{Y(-1) + 28}M{f(X(per))},{Y(-1) + 16}V{Y(-1) + 28}" stroke-width="2"/>'
                 + text((ox + X(per)) / 2, Y(-1) + 40, T, tcls) + text(40, 24, lab, tcls, 'start') + '</g>')
    o.append(text(220, 24, 'T = 2π / k', 't-s', 'start'))
    return ''.join(o)


# ───────────────────────────── 1.16–1.17 Производная и интеграл ─────────────────────────────

@fig('tangent-slope', 'Касательная как предел секущих: точка Q приближается к точке P(1; 1) параболы y = x²; угловой коэффициент секущей PQ равен 1 + x_Q и стремится к 2 = f′(1) — это угловой коэффициент касательной', 360, 230)
def tangent_slope():
    dur = 9
    ox, oy, u = 80, 200, 50
    X = lambda x: ox + x * u
    Y = lambda y: oy - y * u
    o = [f'<path class="s-mute" d="M16,{oy}H250M{ox},10V222" stroke-width="1.3"/>']
    for v in (1, 2):
        o.append(f'<path class="s-mute" d="M{X(v)},{oy - 3}V{oy + 3}" stroke-width="1"/>' + text(X(v), oy + 16, str(v), 't-s'))
    pts = ' '.join(f'{f(X(x))},{f(Y(x * x))}' for x in lin(-1.2, 1.9, 40))
    o.append(f'<polyline class="s-acc" points="{pts}" fill="none" stroke-width="2.6"/>')
    o.append(f'<path class="s-grn" d="M{X(-0.3)},{Y(2 * -0.3 - 1)}L{X(2.2)},{Y(2 * 2.2 - 1)}" stroke-width="1.8" stroke-dasharray="6 4"/>')
    n = 25
    qs = [1.8 - 0.78 * (0.5 - 0.5 * math.cos(2 * math.pi * k / (n - 1))) for k in range(n)]
    kt = kts(n)
    an = lambda attr, v: f'<animate attributeName="{attr}" values="{v}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
    x1, x2 = -0.4, 2.2
    y1 = ';'.join(f(Y(1 + (1 + q) * (x1 - 1))) for q in qs)
    y2 = ';'.join(f(Y(1 + (1 + q) * (x2 - 1))) for q in qs)
    o.append(f'<line class="s-red" x1="{X(x1)}" x2="{X(x2)}" stroke-width="2.2">{an("y1", y1)}{an("y2", y2)}</line>')
    o.append(f'<circle class="f-ink" cx="{X(1)}" cy="{Y(1)}" r="5"/>' + text(X(1) - 8, Y(1) + 4, 'P', 't', 'end'))
    o.append(f'<circle class="f-red" r="5.5">{an("cx", ";".join(f(X(q)) for q in qs))}{an("cy", ";".join(f(Y(q * q)) for q in qs))}</circle>')
    o.append(text(262, 50, 'k(PQ) = 1 + x_Q', 't-red', 'start') + text(262, 78, 'Q → P:', 't-s', 'start') + text(262, 100, 'k → 2 = f′(1)', 't-grn', 'start') + text(262, 140, 'y = x²', 't-acc', 'start'))
    return ''.join(o)


@fig('extremum-sign', 'Экстремумы и знак производной: точка движется по графику y = x³ − 3x, вместе с ней — касательная. Где f′(x) > 0, функция растёт; в точке x = −1 производная меняет знак с «+» на «−» — максимум (2), в точке x = 1 — с «−» на «+» — минимум (−2); там касательная горизонтальна', 360, 230)
def extremum_sign():
    dur = 10
    ox, oy, sx, sy = 130, 115, 48, 34
    X = lambda x: ox + x * sx
    Y = lambda y: oy - y * sy
    F = lambda x: x ** 3 - 3 * x
    D = lambda x: 3 * x * x - 3
    o = [f'<path class="s-mute" d="M20,{oy}H246M{ox},12V222" stroke-width="1.3"/>']
    for v in (-2, -1, 1, 2):
        o.append(f'<path class="s-mute" d="M{X(v)},{oy - 3}V{oy + 3}" stroke-width="1"/>' + text(X(v), oy + 16, ('−' + str(-v)) if v < 0 else str(v), 't-s'))
    pts = ' '.join(f'{f(X(x))},{f(Y(F(x)))}' for x in lin(-2.15, 2.15, 60))
    o.append(f'<polyline class="s-acc" points="{pts}" fill="none" stroke-width="2.6"/>')
    o.append(f'<circle class="f-grn" cx="{X(-1)}" cy="{Y(2)}" r="5"/><circle class="f-grn" cx="{X(1)}" cy="{Y(-2)}" r="5"/>' + text(X(-1), Y(2) - 10, 'max', 't-grn') + text(X(1), Y(-2) + 20, 'min', 't-grn'))
    n = 41
    xs = [-2 + 4 * (0.5 - 0.5 * math.cos(2 * math.pi * k / (n - 1))) for k in range(n)]
    kt = kts(n)
    an = lambda attr, v: f'<animate attributeName="{attr}" values="{v}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
    L = 0.5
    def ends(x):
        k = D(x)
        dx = L / math.sqrt(1 + (k * sy / sx) ** 2)
        return X(x - dx), Y(F(x) - k * dx), X(x + dx), Y(F(x) + k * dx)
    e = [ends(x) for x in xs]
    o.append(f'<line class="s-red" stroke-width="2.4">{an("x1", ";".join(f(a[0]) for a in e))}{an("y1", ";".join(f(a[1]) for a in e))}{an("x2", ";".join(f(a[2]) for a in e))}{an("y2", ";".join(f(a[3]) for a in e))}</line>')
    o.append(f'<circle class="f-red" r="5.5">{an("cx", ";".join(f(X(x)) for x in xs))}{an("cy", ";".join(f(Y(F(x))) for x in xs))}</circle>')
    o.append(text(256, 40, 'f′(x) = 3x² − 3', 't', 'start'))
    o.append(text(256, 72, 'x < −1: f′ > 0 ↗', 't-s', 'start') + text(256, 92, '−1 < x < 1: f′ < 0 ↘', 't-s', 'start') + text(256, 112, 'x > 1: f′ > 0 ↗', 't-s', 'start'))
    o.append(text(256, 146, 'f′ = 0:', 't-red', 'start') + text(256, 166, 'касательная', 't-red', 'start') + text(256, 186, 'горизонтальна', 't-red', 'start'))
    return ''.join(o)


@fig('riemann-area', 'Площадь криволинейной трапеции под y = x² на [0; 2] как предел сумм площадей прямоугольников: при 2, 4, 8, 16 прямоугольниках сумма 1, 1,75, 2,1875, 2,4219 приближается к ∫₀² x² dx = 8/3 ≈ 2,667', 360, 220)
def riemann_area():
    dur = 10
    ox, oy, sx, sy = 40, 200, 90, 42
    X = lambda x: ox + x * sx
    Y = lambda y: oy - y * sy
    o = [f'<path class="s-mute" d="M20,{oy}H{X(2) + 20}M{ox},20V{oy + 10}" stroke-width="1.3"/>']
    o.append(text(X(1), oy + 16, '1', 't-s') + text(X(2), oy + 16, '2', 't-s') + text(ox - 6, Y(4) + 4, '4', 't-s', 'end'))
    for i, n in enumerate((2, 4, 8, 16)):
        t0, t1 = i * 0.24, (i + 1) * 0.24 - 0.01
        h = 2 / n
        g = f'<g opacity="{1 if i == 0 else 0}">{show_at(t0, t1, dur)}'
        s = 0
        for k in range(n):
            x = k * h
            y = x * x
            s += y * h
            g += f'<rect class="f-grn" x="{f(X(x))}" y="{f(Y(y))}" width="{f(h * sx)}" height="{f(y * sy)}" opacity="0.55"/><rect class="s-ink" x="{f(X(x))}" y="{f(Y(y))}" width="{f(h * sx)}" height="{f(y * sy)}" fill="none" stroke-width="0.8"/>'
        g += text(250, 92, f'n = {n}', 't', 'start') + text(250, 116, f'S ≈ {s:.4f}'.replace('.', ','), 't-grn', 'start')
        o.append(g + '</g>')
    pts = ' '.join(f'{f(X(x))},{f(Y(x * x))}' for x in lin(0, 2.1, 40))
    o.append(f'<polyline class="s-acc" points="{pts}" fill="none" stroke-width="2.6"/>')
    o.append(text(250, 50, 'y = x²', 't-acc', 'start') + text(250, 156, '∫₀² x² dx = 8/3', 't-red', 'start') + text(250, 176, '≈ 2,667', 't-red', 'start'))
    return ''.join(o)


# ───────────────────────────── 3. Геометрия ─────────────────────────────

@fig('triangle-sum', 'Сумма углов треугольника: через вершину B проведена прямая, параллельная AC; углы при A и C «переезжают» к вершине B как накрест лежащие и вместе с углом B составляют развёрнутый угол 180°', 360, 210)
def triangle_sum():
    dur = 9
    A, B, C = (40, 180), (150, 50), (300, 180)
    o = [f'<path class="s-mute" d="M20,{B[1]}H340" stroke-width="1.5" stroke-dasharray="6 4"/>']
    o.append(f'<path class="s-ink" d="M{A[0]},{A[1]}L{B[0]},{B[1]}L{C[0]},{C[1]}Z" fill="none" stroke-width="2.4"/>')
    o.append(text(A[0] - 8, A[1] + 16, 'A', 't') + text(B[0], B[1] - 12, 'B', 't') + text(C[0] + 8, C[1] + 16, 'C', 't'))
    def ang(p, q):
        return math.degrees(math.atan2(-(q[1] - p[1]), q[0] - p[0]))
    def sector(cx, cy, r, a1, a2, cls):
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
        x2, y2 = cx + r * math.cos(math.radians(a2)), cy - r * math.sin(math.radians(a2))
        large = 1 if (a2 - a1) % 360 > 180 else 0
        return f'<path class="{cls}" d="M{cx},{cy}L{f(x1)},{f(y1)}A{r},{r} 0 {large} 0 {f(x2)},{f(y2)}Z" opacity="0.75"/>'
    aA = ang(A, B)                  # угол A между AC (0°) и AB
    aC = 180 - ang(C, B)            # угол C между CA (180°) и CB
    o.append(sector(A[0], A[1], 30, 0, aA, 'f-red') + sector(C[0], C[1], 30, 180 - aC, 180, 'f-grn') + sector(B[0], B[1], 26, ang(B, A) % 360, ang(B, C) % 360, 'f-acc'))
    # копии углов A и C переезжают к вершине B
    kt = '0;0.15;0.5;0.92;1'
    tA = f'0 0;0 0;{B[0] - A[0]} {B[1] - A[1]};{B[0] - A[0]} {B[1] - A[1]};0 0'
    tC = f'0 0;0 0;{B[0] - C[0]} {B[1] - C[1]};{B[0] - C[0]} {B[1] - C[1]};0 0'
    # у вершины B угол A должен стоять справа (накрест с AC→AB), угол C — слева: поворот на 180° вокруг вершины
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{tA}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<g transform="rotate(180 {A[0]} {A[1]})">{sector(A[0], A[1], 30, 0, aA, "f-red")}</g></g>')
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{tC}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<g transform="rotate(180 {C[0]} {C[1]})">{sector(C[0], C[1], 30, 180 - aC, 180, "f-grn")}</g></g>')
    o.append(f'<g opacity="0">{phase_op("0;0;1;1;0", "0;0.5;0.56;0.92;1", dur)}' + text(180, 24, '∠A + ∠B + ∠C = 180°', 't-red') + '</g>')
    return ''.join(o)


@fig('inscribed-angle', 'Вписанный угол равен половине центрального, опирающегося на ту же дугу: вершина M движется по окружности, а угол AMB остаётся равным 40° — половине центрального угла AOB = 80°', 360, 230)
def inscribed_angle():
    dur = 9
    cx, cy, R = 130, 118, 92
    P = lambda a: (cx + R * math.cos(math.radians(a)), cy - R * math.sin(math.radians(a)))
    A, B = P(-130), P(-50)  # дуга AB снизу: центральный угол 80°
    o = [f'<circle class="s-ink" cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke-width="2"/>']
    o.append(f'<path class="f-acc" d="M{cx},{cy}L{f(A[0])},{f(A[1])}A{R},{R} 0 0 0 {f(B[0])},{f(B[1])}Z" opacity="0.18"/>')
    o.append(f'<path class="s-acc" d="M{f(A[0])},{f(A[1])}L{cx},{cy}L{f(B[0])},{f(B[1])}" fill="none" stroke-width="2.2"/>')
    o.append(f'<circle class="f-ink" cx="{cx}" cy="{cy}" r="3.5"/>' + text(cx + 8, cy + 4, 'O', 't-s', 'start'))
    o.append(text(A[0] - 8, A[1] + 14, 'A', 't', 'end') + text(B[0] + 8, B[1] + 14, 'B', 't', 'start'))
    n = 25
    angs = [40 + 100 * (0.5 - 0.5 * math.cos(2 * math.pi * k / (n - 1))) for k in range(n)]
    kt = kts(n)
    an = lambda attr, v: f'<animate attributeName="{attr}" values="{v}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
    mx = ';'.join(f(P(a)[0]) for a in angs); my = ';'.join(f(P(a)[1]) for a in angs)
    o.append(f'<line class="s-red" x1="{f(A[0])}" y1="{f(A[1])}" stroke-width="2.2">{an("x2", mx)}{an("y2", my)}</line>')
    o.append(f'<line class="s-red" x1="{f(B[0])}" y1="{f(B[1])}" stroke-width="2.2">{an("x2", mx)}{an("y2", my)}</line>')
    o.append(f'<circle class="f-red" r="5.5">{an("cx", mx)}{an("cy", my)}</circle>')
    o.append(text(250, 60, '∠AOB = 80°', 't-acc', 'start') + text(250, 86, '∠AMB = 40°', 't-red', 'start') + text(250, 120, 'вписанный угол =', 't-s', 'start') + text(250, 138, '½ центрального', 't-s', 'start'))
    return ''.join(o)


@fig('vector-sum', 'Сложение векторов по правилу параллелограмма и в координатах: a = (3; 1), b = (1; 2); их сумма a + b = (4; 3) — диагональ параллелограмма, построенного на a и b; координаты складываются, длина |a + b| = 5', 360, 220)
def vector_sum():
    dur = 8
    ox, oy, u = 50, 190, 40
    X = lambda x: ox + x * u
    Y = lambda y: oy - y * u
    o = [markers('vector-sum', ('acc', 'red', 'grn', 'mute'))]
    o.append(f'<path class="s-mute" d="M20,{oy}H{X(5)}M{ox},{Y(4)}V{oy + 14}" stroke-width="1.2"/>')
    for v in range(1, 5):
        o.append(f'<path class="s-mute" d="M{X(v)},{oy - 3}V{oy + 3}M{ox - 3},{Y(v)}H{ox + 3}" stroke-width="1"/>' + text(X(v), oy + 16, str(v), 't-s'))
    o.append(mline('vector-sum', X(0), Y(0), X(3), Y(1), 'acc', 2.8) + text(X(1.8), Y(0.45) + 18, 'a', 't-acc'))
    o.append(mline('vector-sum', X(0), Y(0), X(1), Y(2), 'red', 2.8) + text(X(0.3), Y(1.2), 'b', 't-red', 'end'))
    # перенос b в конец a и a в конец b
    o.append(f'<g opacity="0">{phase_op("0;0;1;1;0", "0;0.15;0.3;0.95;1", dur)}' + mline('vector-sum', X(3), Y(1), X(4), Y(3), 'red', 2, extra=' stroke-dasharray="5 4"')
             + mline('vector-sum', X(1), Y(2), X(4), Y(3), 'acc', 2, extra=' stroke-dasharray="5 4"') + '</g>')
    o.append(f'<g opacity="0">{phase_op("0;0;1;1;0", "0;0.45;0.55;0.95;1", dur)}' + mline('vector-sum', X(0), Y(0), X(4), Y(3), 'grn', 3.2)
             + text(X(2.3), Y(1.9), 'a + b', 't-grn', 'end') + text(250, 120, 'a + b = (4; 3)', 't-grn', 'start') + text(250, 144, '|a + b| = 5', 't-grn', 'start') + '</g>')
    o.append(text(250, 50, 'a = (3; 1)', 't-acc', 'start') + text(250, 74, 'b = (1; 2)', 't-red', 'start'))
    return ''.join(o)


@fig('archimedes', 'Конус, шар и цилиндр одного радиуса R и высоты 2R: их объёмы относятся как 1 : 2 : 3 (Архимед). Вода из конуса заполняет треть цилиндра, вода из шара — ещё две трети', 360, 220)
def archimedes():
    dur = 9
    R, base = 40, 190
    H = 2 * R
    o = []
    # конус
    cx1 = 55
    o.append(f'<path class="f-acc" d="M{cx1 - R},{base - H}H{cx1 + R}L{cx1},{base}Z" opacity="0.25"/><path class="s-ink" d="M{cx1 - R},{base - H}H{cx1 + R}L{cx1},{base}Z" fill="none" stroke-width="2"/>')
    o.append(text(cx1, base + 18, 'конус: 1', 't-s'))
    # шар
    cx2 = 155
    o.append(f'<circle class="f-red" cx="{cx2}" cy="{base - R}" r="{R}" opacity="0.25"/><circle class="s-ink" cx="{cx2}" cy="{base - R}" r="{R}" fill="none" stroke-width="2"/>')
    o.append(text(cx2, base + 18, 'шар: 2', 't-s'))
    # цилиндр, заполняемый
    cx3 = 270
    lv1, lv2 = H / 3, H
    o.append(f'<rect class="f-acc" x="{cx3 - R}" width="{2 * R}" opacity="0.55"><animate attributeName="height" values="0;0;{f(lv1)};{f(lv1)};{f(lv1)};{f(lv1)};0" keyTimes="0;0.1;0.35;0.45;0.92;0.98;1" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="{base};{base};{f(base - lv1)};{f(base - lv1)};{f(base - lv1)};{f(base - lv1)};{base}" keyTimes="0;0.1;0.35;0.45;0.92;0.98;1" dur="{dur}s" repeatCount="indefinite"/></rect>')
    o.append(f'<rect class="f-red" x="{cx3 - R}" width="{2 * R}" opacity="0.55"><animate attributeName="height" values="0;0;{f(lv2 - lv1)};{f(lv2 - lv1)};0" keyTimes="0;0.5;0.8;0.95;1" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="{f(base - lv1)};{f(base - lv1)};{base - lv2};{base - lv2};{f(base - lv1)}" keyTimes="0;0.5;0.8;0.95;1" dur="{dur}s" repeatCount="indefinite"/></rect>')
    o.append(f'<rect class="s-ink" x="{cx3 - R}" y="{base - H}" width="{2 * R}" height="{H}" fill="none" stroke-width="2"/>')
    o.append(text(cx3, base + 18, 'цилиндр: 3', 't-s'))
    o.append(text(180, 26, 'V = ⅓πR²·2R : ⁴⁄₃πR³ : πR²·2R = 1 : 2 : 3', 't-s'))
    return ''.join(o)


# ───────────────────────────── 3.12 Тела вращения ─────────────────────────────

@fig('cylinder-unfold', 'Развёртка боковой поверхности цилиндра: если разрезать боковую поверхность по образующей и развернуть, получится прямоугольник; одна его сторона равна высоте h, другая — длине окружности основания 2πR, поэтому S бок = 2πR·h', 360, 220)
def cylinder_unfold():
    dur = 8
    R, h, ry = 30, 110, 9
    cx, top = 60, 62
    bot = top + h
    o = []
    o.append(f'<rect class="f-acc" x="{cx - R}" y="{top}" width="{2 * R}" height="{h}" opacity="0.18"/>')
    o.append(f'<ellipse class="s-ink" cx="{cx}" cy="{top}" rx="{R}" ry="{ry}" fill="none" stroke-width="2"/>')
    o.append(f'<path class="s-ink" d="M{cx - R},{bot}A{R},{ry} 0 0 0 {cx + R},{bot}" fill="none" stroke-width="2"/>')
    o.append(f'<path class="s-mute" d="M{cx - R},{bot}A{R},{ry} 0 0 1 {cx + R},{bot}" fill="none" stroke-width="1.4" stroke-dasharray="4 3"/>')
    o.append(f'<line class="s-ink" x1="{cx - R}" y1="{top}" x2="{cx - R}" y2="{bot}" stroke-width="2"/><line class="s-ink" x1="{cx + R}" y1="{top}" x2="{cx + R}" y2="{bot}" stroke-width="2"/>')
    o.append(f'<line class="s-red" x1="{cx}" y1="{top}" x2="{cx + R}" y2="{top}" stroke-width="1.6"/>')
    o.append(text(cx + R / 2, top - 14, 'R', 't-s'))
    o.append(f'<line class="s-red" x1="{cx + R}" y1="{top}" x2="{cx + R}" y2="{bot}" stroke-width="3"/>')
    o.append(text(cx - R - 10, (top + bot) / 2 + 5, 'h', 't-s', 'end'))
    # развёртка: прямоугольник растёт по ширине
    x0, W = 130, 2 * math.pi * R
    kt = '0;0.15;0.6;0.9;1'
    o.append(f'<rect class="f-acc" x="{x0}" y="{top}" height="{h}" opacity="0.3"><animate attributeName="width" values="0;0;{f(W)};{f(W)};0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></rect>')
    o.append(f'<rect class="s-acc" x="{x0}" y="{top}" height="{h}" fill="none" stroke-width="2"><animate attributeName="width" values="0;0;{f(W)};{f(W)};0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></rect>')
    o.append(f'<line class="s-red" x1="{x0}" y1="{top}" x2="{x0}" y2="{bot}" stroke-width="3"/>')
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.6;0.95", dur)}'
             + text(x0 + W / 2, bot + 20, 'длина 2πR', 't-s')
             + text(x0 + W + 8, (top + bot) / 2 + 5, 'h', 't-s', 'start')
             + text(x0 + W / 2, (top + bot) / 2 + 5, 'S = 2πR·h', 't-s') + '</g>')
    o.append(text(180, 24, 'разрезаем по образующей и разворачиваем', 't-s'))
    return ''.join(o)


@fig('sphere-section', 'Сечение шара плоскостью — круг: если плоскость удалена от центра на d, радиус сечения r = √(R² − d²). Для R = 5: при d = 0 — большой круг r = 5, при d = 3 — r = 4, при d = 4 — r = 3, при d = 5 плоскость только касается шара', 360, 220)
def sphere_section():
    dur = 10
    R = 75
    cx, cy = 120, 115
    o = []
    o.append(f'<circle class="f-acc" cx="{cx}" cy="{cy}" r="{R}" opacity="0.15"/><circle class="s-ink" cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke-width="2"/>')
    o.append(f'<ellipse class="s-mute" cx="{cx}" cy="{cy}" rx="{R}" ry="14" fill="none" stroke-width="1.2" stroke-dasharray="4 3"/>')
    o.append(f'<circle class="f-ink" cx="{cx}" cy="{cy}" r="3"/>')
    ds = [0, 3, 4, 5]
    n = len(ds)
    for i, d in enumerate(ds):
        r = math.sqrt(25 - d * d)
        yy = cy - d * R / 5
        rr = r * R / 5
        g = [f'<ellipse class="f-red" cx="{cx}" cy="{f(yy)}" rx="{f(max(rr, 1))}" ry="{f(max(rr * 0.19, 1))}" opacity="0.45"/>']
        g.append(f'<line class="s-red" x1="{cx}" y1="{f(yy)}" x2="{f(cx + rr)}" y2="{f(yy)}" stroke-width="2.4"/>')
        if d:
            g.append(f'<line class="s-grn" x1="{cx}" y1="{cy}" x2="{cx}" y2="{f(yy)}" stroke-width="2.4"/>')
            g.append(f'<line class="s-mute" x1="{cx}" y1="{cy}" x2="{f(cx + rr)}" y2="{f(yy)}" stroke-width="1.4"/>')
        g.append(text(222, 90, 'R = 5', 't-s', 'start'))
        g.append(text(222, 116, f'd = {d}', 't-s', 'start'))
        g.append(text(222, 142, 'r = ' + ('5' if d == 0 else ('0' if d == 5 else f'√(25 − {d * d}) = {f(r)}')), 't-s', 'start'))
        o.append(f'<g opacity="{1 if i == 0 else 0}">{show_at(round(i / n, 4), round((i + 1) / n, 4), dur)}' + ''.join(g) + '</g>')
    o.append(text(180, 24, 'r² = R² − d²', 't-s'))
    return ''.join(o)
