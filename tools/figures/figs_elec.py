"""Иллюстрации к конспекту «Электричество» (стр. c01–c40): электростатика, конденсаторы, постоянный ток, ток в средах."""
import math
import random
from figlib import *  # noqa: F401,F403


def chg(x, y, sign, r=12, extra=''):
    """Заряд: «+» красный, «−» синий."""
    cls = 'f-red' if sign > 0 else 'f-acc'
    return f'<circle class="{cls}" cx="{f(x)}" cy="{f(y)}" r="{r}"{extra}/>' + text(x, y + r * 0.42, '+' if sign > 0 else '−', 't-w')


def resistor(x1, x2, y, label='', vertical=False, cls='s-ink'):
    if vertical:
        h = x2 - x1
        return (f'<rect class="f-paper {cls}" x="{f(y - 7)}" y="{f(x1)}" width="14" height="{f(h)}" rx="2" stroke-width="2"/>'
                + (text(y + 12, (x1 + x2) / 2 + 4, label, 't-s', 'start') if label else ''))
    return (f'<rect class="f-paper {cls}" x="{f(x1)}" y="{f(y - 7)}" width="{f(x2 - x1)}" height="14" rx="2" stroke-width="2"/>'
            + (text((x1 + x2) / 2, y - 12, label, 't-s') if label else ''))


def battery(x, y, vertical=True, label='', flip=False):
    """Источник: длинная черта «+», короткая «−»."""
    s = -1 if flip else 1
    if vertical:
        return (f'<rect class="f-paper" x="{x - 12}" y="{y - 6}" width="24" height="12"/>'
                f'<path class="s-ink" d="M{x - 12},{f(y - 4 * s)}H{x + 12}" stroke-width="2.4"/><path class="s-ink" d="M{x - 6},{f(y + 4 * s)}H{x + 6}" stroke-width="4"/>'
                + (text(x + 16, y + 4, label, 't-s', 'start') if label else ''))
    return (f'<rect class="f-paper" x="{x - 6}" y="{y - 12}" width="12" height="24"/>'
            f'<path class="s-ink" d="M{f(x - 4 * s)},{y - 12}V{y + 12}" stroke-width="2.4"/><path class="s-ink" d="M{f(x + 4 * s)},{y - 6}V{y + 6}" stroke-width="4"/>'
            + (text(x, y - 16, label, 't-s') if label else ''))


def cap_sym(x, y, vertical=False, gap=8, w=26, label=''):
    if vertical:  # обкладки горизонтальные (ток вертикально)
        return (f'<rect class="f-paper" x="{x - w / 2}" y="{y - gap / 2}" width="{w}" height="{gap}"/>'
                f'<path class="s-ink" d="M{x - w / 2},{y - gap / 2}H{x + w / 2}M{x - w / 2},{y + gap / 2}H{x + w / 2}" stroke-width="3"/>'
                + (text(x + w / 2 + 4, y + 4, label, 't-s', 'start') if label else ''))
    return (f'<rect class="f-paper" x="{x - gap / 2}" y="{y - w / 2}" width="{gap}" height="{w}"/>'
            f'<path class="s-ink" d="M{x - gap / 2},{y - w / 2}V{y + w / 2}M{x + gap / 2},{y - w / 2}V{y + w / 2}" stroke-width="3"/>'
            + (text(x, y - w / 2 - 5, label, 't-s') if label else ''))


def lamp(x, y, glow_vals=None, dur=1, r=10, kt=None, label=''):
    g = ''
    if glow_vals is not None:
        k = kt or times(len(glow_vals))
        g = (f'<circle class="f-red-soft" cx="{x}" cy="{y}" r="{r * 2.2}"><animate attributeName="opacity" values="{nums(glow_vals)}" keyTimes="{k}" dur="{dur}s" repeatCount="indefinite"/></circle>'
             f'<circle class="f-red" cx="{x}" cy="{y}" r="{r - 2}"><animate attributeName="opacity" values="{nums([0.85 * v for v in glow_vals])}" keyTimes="{k}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    d = r * 0.7
    return (g + f'<circle class="s-ink" cx="{x}" cy="{y}" r="{r}" stroke-width="2" fill="none"/>'
            f'<path class="s-ink" d="M{f(x - d)},{f(y - d)}L{f(x + d)},{f(y + d)}M{f(x + d)},{f(y - d)}L{f(x - d)},{f(y + d)}" stroke-width="1.6"/>'
            + (text(x, y + r + 14, label, 't-s') if label else ''))


def dial(x, y, angs, dur, letter, r=15, kt=None):
    """Стрелочный прибор (амперметр/вольтметр) со стрелкой, поворачивающейся на углы angs (° от вертикали)."""
    k = kt or times(len(angs))
    vs = ';'.join(f'{f(a)} {x} {y}' for a in angs)
    return (f'<circle class="f-paper s-ink" cx="{x}" cy="{y}" r="{r}" stroke-width="2"/>'
            f'<g><animateTransform attributeName="transform" type="rotate" values="{vs}" keyTimes="{k}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<path class="s-red" d="M{x},{y + 4}V{y - r + 3}" stroke-width="2"/></g>'
            + text(x, y + r - 3, letter, 't-s'))


def phase_op(values, kt, dur, discrete=True):
    return f'<animate attributeName="opacity" values="{values}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"{" calcMode=\"discrete\"" if discrete else ""}/>'


# ───────────────────────────── заряд ─────────────────────────────

@fig('charge-atom', 'Атом: в ядре протоны (+e), по орбитам движутся электроны (−e); если атом теряет электрон, у него недостаток электронов и заряд становится положительным', 360, 210)
def charge_atom():
    dur = 10
    cx, cy = 115, 105
    o = []
    for i in range(8):
        a = i / 7 * 2 * math.pi
        x, y = (cx + 9 * math.cos(a), cy + 9 * math.sin(a)) if i < 7 else (cx, cy)
        o.append(f'<circle class="f-red" cx="{f(x)}" cy="{f(y)}" r="5.5"/>' + text(x, y + 3, '+', 't-ws'))
    for R, n, T in [(40, 2, 4), (78, 6, 9)]:
        o.append(f'<circle class="s-mute" cx="{cx}" cy="{cy}" r="{R}" stroke-width="1.2" stroke-dasharray="3 4"/>')
        path = f'M{cx + R},{cy}A{R},{R} 0 1 1 {cx - R},{cy}A{R},{R} 0 1 1 {cx + R},{cy}'
        for k in range(n):
            fade = phase_op('1;0', '0;0.5', dur) if (R == 78 and k == 0) else ''
            o.append(f'<g>{fade}<g><animateMotion dur="{T}s" begin="{f(-T * k / n)}s" repeatCount="indefinite" path="{path}"/>'
                     f'<circle class="f-acc" cx="0" cy="0" r="7"/>{text(0, 3, "−", "t-ws")}</g></g>')
    o.append(text(cx, cy - 18, 'ядро', 't-s'))
    o.append(f'<g>{phase_op("1;0", "0;0.5", dur)}' + text(212, 62, 'q = 0', 't', 'start') + text(212, 82, '8 протонов, 8 электронов', 't-s', 'start') + text(212, 98, 'атом нейтрален', 't-s', 'start') + '</g>')
    o.append(f'<g opacity="0">{phase_op("0;1", "0;0.5", dur)}' + text(212, 62, 'q = +e', 't-red', 'start') + text(212, 82, '8 протонов, 7 электронов', 't-s', 'start') + text(212, 98, 'недостаток электрона', 't-s', 'start') + '</g>')
    o.append(text(212, 140, 'протон: +e, m_p = 1836 m_e', 't-s', 'start') + text(212, 158, 'электрон: −e', 't-s', 'start'))
    o.append(text(212, 184, 'e = 1,6·10⁻¹⁹ Кл', 't-s', 'start'))
    return ''.join(o)


@fig('charge-contact', 'Закон сохранения заряда: одинаковые шарики +7 и +9 после соприкосновения получают по +8; шарики +12, 0 и −3 — по +3', 360, 210)
def charge_contact():
    dur = 6
    kt = '0;0.3;0.45;0.6;0.9;1'
    o = []
    # верхний ряд: два шарика
    for x0, xc, q0, q1 in [(70, 160, '+7', '+8'), (290, 200, '+9', '+8')]:
        xs = [x0, x0, xc, xc, x0, x0]
        tr = ';'.join(f'{f(x - x0)} 0' for x in xs)
        o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{tr}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<circle class="f-soft s-red" cx="{x0}" cy="60" r="20" stroke-width="2"/>'
                 f'<text class="t" x="{x0}" y="65" text-anchor="middle">{q0}{phase_op("1;0;1", "0;0.45;0.95", dur)}</text>'
                 f'<text class="t-red" x="{x0}" y="65" text-anchor="middle" opacity="0">{q1}{phase_op("0;1;0", "0;0.45;0.95", dur)}</text></g>')
    o.append(text(180, 106, '+7 + 9 = +16 → по +8', 't-s'))
    # нижний ряд: три шарика
    for x0, xc, q0 in [(50, 140, '+12'), (180, 180, '0'), (310, 220, '−3')]:
        xs = [x0, x0, xc, xc, x0, x0]
        tr = ';'.join(f'{f(x - x0)} 0' for x in xs)
        o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{tr}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<circle class="f-soft s-red" cx="{x0}" cy="150" r="20" stroke-width="2"/>'
                 f'<text class="t" x="{x0}" y="155" text-anchor="middle">{q0}{phase_op("1;0;1", "0;0.45;0.95", dur)}</text>'
                 f'<text class="t-red" x="{x0}" y="155" text-anchor="middle" opacity="0">+3{phase_op("0;1;0", "0;0.45;0.95", dur)}</text></g>')
    o.append(text(180, 198, '+12 + 0 − 3 = +9 → по +3', 't-s'))
    return ''.join(o)


# ───────────────────────────── Кулон, поле ─────────────────────────────

@fig('coulomb', 'Закон Кулона: разноимённые заряды притягиваются, одноимённые отталкиваются; при уменьшении расстояния сила растёт как 1/r²', 360, 200)
def coulomb():
    dur, n = 10, 61
    us = lin(0, 1, n)
    rs = [80 + 50 * (0.5 + 0.5 * math.cos(4 * math.pi * u)) for u in us]   # 80…130, дважды за цикл
    attract = [u < 0.5 for u in us]
    c = 180
    x1 = [c - r / 2 for r in rs]
    x2 = [c + r / 2 for r in rs]
    F = [min(60, 40 * (80 / r) ** 2) for r in rs]
    o = [markers('coulomb', ('red', 'acc'))]
    o.append(f'<g>{move([(x - x1[0], 0) for x in x1], dur)}{chg(x1[0], 100, 1, 16)}</g>')
    o.append(f'<g>{move([(x - x2[0], 0) for x in x2], dur)}'
             f'<g>{phase_op("1;0", "0;0.5", dur)}{chg(x2[0], 100, -1, 16)}</g><g opacity="0">{phase_op("0;1", "0;0.5", dur)}{chg(x2[0], 100, 1, 16)}</g></g>')
    # стрелки сил
    a1x1 = [x + (18 if a else -18) for x, a in zip(x1, attract)]
    a1x2 = [x + (18 + Fv if a else -18 - Fv) for x, a, Fv in zip(x1, attract, F)]
    a2x1 = [x + (-18 if a else 18) for x, a in zip(x2, attract)]
    a2x2 = [x + (-18 - Fv if a else 18 + Fv) for x, a, Fv in zip(x2, attract, F)]
    o.append(f'<line class="s-red" y1="60" y2="60" stroke-width="2.6" marker-end="url(#coulomb-m-red)">{anims(dur, x1=a1x1, x2=a1x2)}</line>')
    o.append(f'<line class="s-red" y1="60" y2="60" stroke-width="2.6" marker-end="url(#coulomb-m-red)">{anims(dur, x1=a2x1, x2=a2x2)}</line>')
    o.append(f'<line class="s-mute" y1="140" y2="140" stroke-width="1.2">{anims(dur, x1=x1, x2=x2)}</line><text class="t" x="180" y="158" text-anchor="middle">r</text>')
    o.append(f'<text class="t" x="180" y="24" text-anchor="middle">разноимённые — притягиваются{phase_op("1;0", "0;0.5", dur)}</text>')
    o.append(f'<text class="t" x="180" y="24" text-anchor="middle" opacity="0">одноимённые — отталкиваются{phase_op("0;1", "0;0.5", dur)}</text>')
    o.append(text(180, 190, 'F = k|q₁||q₂| / εr²', 't-s'))
    return ''.join(o)


def radial(cx, cy, sign, n=12, r0=14, r1=78, cls='s-red', fid=''):
    out = []
    for k in range(n):
        a = k / n * 2 * math.pi
        xa, ya = cx + r0 * math.cos(a), cy + r0 * math.sin(a)
        xb, yb = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
        d = f'M{f(xa)},{f(ya)}L{f(xb)},{f(yb)}' if sign > 0 else f'M{f(xb)},{f(yb)}L{f(xa)},{f(ya)}'
        out.append(f'<path class="{cls}" d="{d}" stroke-width="1.6" opacity="0.5"/>')
        out.append(f'<path class="{cls}" d="{d}" stroke-width="2.4" stroke-dasharray="6 10">{flow(1.2, 16)}</path>')
        # наконечник у внешнего конца
        ang = math.degrees(a) if sign > 0 else math.degrees(a) + 180
        hx, hy = (xb, yb) if sign > 0 else (cx + (r0 + 6) * math.cos(a), cy + (r0 + 6) * math.sin(a))
        out.append(head(hx, hy, ang, cls.replace('s-', 'f-'), 6))
    return ''.join(out)


@fig('field-radial', 'Силовые линии электрического поля перпендикулярны поверхности заряда: из положительного заряда они исходят, в отрицательный входят', 360, 200)
def field_radial():
    o = [radial(95, 100, 1, cls='s-red'), chg(95, 100, 1, 13), radial(265, 100, -1, cls='s-acc'), chg(265, 100, -1, 13)]
    o.append(text(95, 196, 'линии исходят', 't-s') + text(265, 196, 'линии входят', 't-s'))
    return ''.join(o)


@fig('field-pair', 'Причина притяжения и отталкивания: у разноимённых зарядов линии идут от «+» к «−» и стягивают заряды, у одноимённых линии расходятся и расталкивают их', 360, 220)
def field_pair():
    dur = 4
    o = []
    # разноимённые
    ax, bx, y = 40, 140, 100
    wig = '0 0;6 0;0 0'
    lines = []
    for h in (-70, -40, -16, 0, 16, 40, 70):
        lines.append(f'<path class="s-red" d="M{ax + 10},{y}Q{(ax + bx) / 2},{y + h * 1.6} {bx - 10},{y}" stroke-width="1.8" fill="none" stroke-dasharray="6 8">{flow(1.4, 14)}</path>')
    o.append(''.join(lines))
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{wig}" dur="{dur}s" repeatCount="indefinite"/>{chg(ax, y, 1, 12)}</g>')
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;-6 0;0 0" dur="{dur}s" repeatCount="indefinite"/>{chg(bx, y, -1, 12)}</g>')
    o.append(text(90, 206, 'притягиваются', 't'))
    # одноимённые
    ax, bx = 225, 315
    lines = []
    for c, sgn in ((ax, -1), (bx, 1)):
        for k in range(9):
            a = math.radians(-120 + k * 30) if sgn > 0 else math.radians(60 + k * 30)
            x0, y0 = c + 12 * math.cos(a), y + 12 * math.sin(a)
            x1, y1 = c + 70 * math.cos(a), y + 70 * math.sin(a)
            # линии отклоняются от соседнего заряда
            mx, my = c + 40 * math.cos(a) + sgn * 6, y + 40 * math.sin(a) * 1.15
            lines.append(f'<path class="s-red" d="M{f(x0)},{f(y0)}Q{f(mx)},{f(my)} {f(x1)},{f(y1)}" stroke-width="1.8" fill="none" stroke-dasharray="6 8">{flow(1.4, 14)}</path>')
    o.append(''.join(lines))
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;-6 0;0 0" dur="{dur}s" repeatCount="indefinite"/>{chg(ax, y, 1, 12)}</g>')
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{wig}" dur="{dur}s" repeatCount="indefinite"/>{chg(bx, y, 1, 12)}</g>')
    o.append(text(270, 206, 'отталкиваются', 't'))
    return ''.join(o)


@fig('superposition', 'Принцип суперпозиции: напряжённости полей двух зарядов в точке складываются как векторы', 360, 220)
def superposition():
    dur, n = 10, 61
    q1, q2 = (110, 170), (250, 170)
    us = lin(0, 1, n)
    P = [(180 + 120 * math.cos(math.pi * (1 - 0.5 + 0.5 * math.cos(2 * math.pi * u))) * 0.9, 150 - 95 * math.sin(math.pi * (0.5 - 0.5 * math.cos(2 * math.pi * u)))) for u in us]
    # точка ходит по дуге над зарядами
    P = []
    for u in us:
        th = math.pi * (0.15 + 0.7 * (0.5 - 0.5 * math.cos(2 * math.pi * u)))
        P.append((180 - 130 * math.cos(th), 175 - 120 * math.sin(th)))
    K = 6e5
    E1, E2, ER = [], [], []
    for x, y in P:
        vs = []
        for qx, qy in (q1, q2):
            dx, dy = x - qx, y - qy
            r = math.hypot(dx, dy)
            e = min(K / r ** 2, 80)
            vs.append((e * dx / r, e * dy / r))
        E1.append(vs[0]); E2.append(vs[1]); ER.append((vs[0][0] + vs[1][0], vs[0][1] + vs[1][1]))
    o = [markers('superposition', ('acc', 'grn', 'red'))]
    o.append(chg(*q1, 1, 13) + chg(*q2, 1, 13) + text(q1[0], q1[1] + 30, 'q₁', 't-s') + text(q2[0], q2[1] + 30, 'q₂', 't-s'))
    px = [p[0] for p in P]
    py = [p[1] for p in P]
    for vec, color in [(E1, 'acc'), (E2, 'grn'), (ER, 'red')]:
        o.append(f'<line class="s-{color}" stroke-width="{2.8 if color == "red" else 2.2}" marker-end="url(#superposition-m-{color})">'
                 f'{anims(dur, x1=px, y1=py, x2=[x + v[0] for x, v in zip(px, vec)], y2=[y + v[1] for y, v in zip(py, vec)])}</line>')
    o.append(f'<line class="s-mute" stroke-width="1" stroke-dasharray="3 3">{anims(dur, x1=[x + v[0] for x, v in zip(px, E1)], y1=[y + v[1] for y, v in zip(py, E1)], x2=[x + v[0] for x, v in zip(px, ER)], y2=[y + v[1] for y, v in zip(py, ER)])}</line>')
    o.append(f'<circle class="f-ink" r="4">{anims(dur, cx=px, cy=py)}</circle>')
    o.append('<g transform="translate(270,24)"><line class="s-acc" x1="0" y1="0" x2="14" y2="0" stroke-width="2.4"/>' + text(18, 4, 'E_1', 't-acc', 'start')
             + '<line class="s-grn" x1="0" y1="20" x2="14" y2="20" stroke-width="2.4"/>' + text(18, 24, 'E_2', 't-grn', 'start')
             + '<line class="s-red" x1="0" y1="40" x2="14" y2="40" stroke-width="2.4"/>' + text(18, 44, 'E_рез', 't-red', 'start') + '</g>')
    return ''.join(o)


@fig('sphere-field', 'Заряженная металлическая сфера: внутри поле равно нулю, а потенциал такой же, как на поверхности; снаружи E убывает как 1/r², потенциал — как 1/r', 360, 220)
def sphere_field():
    dur, n = 8, 61
    cx, cy, R = 70, 110, 40
    o = []
    o.append(f'<circle class="f-soft s-ink" cx="{cx}" cy="{cy}" r="{R}" stroke-width="2"/>')
    for k in range(14):
        a = k / 14 * 2 * math.pi
        o.append(text(cx + (R - 7) * math.cos(a), cy + (R - 7) * math.sin(a) + 4, '+', 't-red'))
    us = lin(0, 1, n)
    rr = [2.8 * R * (0.5 - 0.5 * math.cos(2 * math.pi * u)) for u in us]     # 0 … 2,8R
    o.append(f'<line class="s-mute" x1="{cx}" y1="{cy}" y2="{cy}" stroke-width="1.2" stroke-dasharray="3 3">{anim("x2", nums([cx + r for r in rr]), dur)}</line>')
    o.append(f'<circle class="f-ink" cy="{cy}" r="4">{anim("cx", nums([cx + r for r in rr]), dur)}</circle>')
    # графики
    gx, gy, sx = 170, 196, 60   # 1R = 60 px по оси r
    o.append(arrow(gx, gy, 352, gy, 's-ink', 'f-ink', 1.4, 6) + arrow(gx, gy, gx, 24, 's-ink', 'f-ink', 1.4, 6) + text(348, gy + 16, 'r', 't', 'end'))
    o.append(f'<path class="s-mute" d="M{gx + sx},{gy}V30" stroke-width="1" stroke-dasharray="3 4"/>' + text(gx + sx, gy + 16, 'R', 't-s'))
    E0, P0 = 140, 90
    Ec = f'M{gx},{gy}H{gx + sx}V{gy - E0}' + ''.join(f'L{f(gx + sx * x)},{f(gy - E0 / x ** 2)}' for x in lin(1, 3, 30))
    Pc = f'M{gx},{gy - P0}H{gx + sx}' + ''.join(f'L{f(gx + sx * x)},{f(gy - P0 / x)}' for x in lin(1, 3, 30))
    o.append(f'<path class="s-red" d="{Ec}" stroke-width="2.4" fill="none"/>' + f'<path class="s-acc" d="{Pc}" stroke-width="2.4" fill="none" stroke-dasharray="6 4"/>')
    x_r = [r / R for r in rr]
    ey = [gy if x < 1 else gy - E0 / x ** 2 for x in x_r]
    py = [gy - P0 if x < 1 else gy - P0 / x for x in x_r]
    gxs = [gx + sx * min(x, 3) for x in x_r]
    o.append(f'<circle class="f-red" r="5">{anims(dur, cx=gxs, cy=ey)}</circle><circle class="f-acc" r="5">{anims(dur, cx=gxs, cy=py)}</circle>')
    o.append(text(gx + sx + 6, gy - E0 + 4, 'E₀', 't-red', 'start') + text(300, 120, 'E ~ 1/r²', 't-red', 'start') + text(300, 70, 'φ ~ 1/r', 't-acc', 'start'))
    o.append(text(gx + 10, 40, 'E, φ', 't', 'start'))
    o.append(text(cx, 196, 'внутри E = 0', 't-s'))
    return ''.join(o)


@fig('uniform-field', 'Однородное поле между пластинами: напряжённость одинакова во всех точках, на +q сила действует вдоль линий, на −q — против', 360, 210)
def uniform_field():
    dur, n = 4, 31
    o = [markers('uniform-field', ('red', 'acc'))]
    o.append('<rect class="f-acc" x="40" y="24" width="280" height="8" rx="2"/><rect class="f-red" x="40" y="178" width="280" height="8" rx="2"/>')
    o.append(''.join(text(60 + 30 * k, 21, '−', 't-acc') for k in range(9)) + ''.join(text(60 + 30 * k, 202, '+', 't-red') for k in range(9)))
    for x in range(70, 320, 40):
        o.append(f'<path class="s-mute" d="M{x},176V36" stroke-width="1.4"/><path class="s-red" d="M{x},176V36" stroke-width="2" stroke-dasharray="5 9">{flow(1.0, 14)}</path>' + head(x, 36, -90, 'f-mute', 6))
    us = lin(0, 1, n)
    yp = [160 - 110 * u * u for u in us]
    yn = [50 + 110 * u * u for u in us]
    kt = ';'.join(f(0.85 * u) for u in us) + ';1'
    def mv(vals):
        return ';'.join(f(v) for v in vals) + ';' + f(vals[-1])
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(f"0 {f(y - 160)}" for y in yp)};0 {f(yp[-1] - 160)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'{chg(110, 160, 1, 10)}' + mline('uniform-field', 124, 160, 124, 128, 'red', 2.6) + text(130, 148, 'F', 't-red', 'start') + '</g>')
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(f"0 {f(y - 50)}" for y in yn)};0 {f(yn[-1] - 50)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'{chg(250, 50, -1, 10)}' + mline('uniform-field', 264, 50, 264, 82, 'acc', 2.6) + text(270, 72, 'F', 't-acc', 'start') + '</g>')
    o.append(text(352, 110, 'E', 't', 'end') + text(352, 128, 'F = Eq', 't-s', 'end'))
    return ''.join(o)


@fig('equipotential', 'Эквипотенциали точечного заряда — концентрические сферы: вдоль них работа поля равна нулю, а по направлению силовых линий потенциал уменьшается', 360, 230)
def equipotential():
    dur = 10
    cx, cy = 110, 118
    o = []
    for k in range(12):
        a = k / 12 * 2 * math.pi
        o.append(f'<path class="s-red" d="M{f(cx + 14 * math.cos(a))},{f(cy + 14 * math.sin(a))}L{f(cx + 112 * math.cos(a))},{f(cy + 112 * math.sin(a))}" stroke-width="1.2" opacity="0.45"/>')
    rads = [(24, '500 В'), (40, '300 В'), (100, '100 В')]
    for (r, lab), ang in zip(rads, (-150, -35, 35)):
        o.append(f'<circle class="s-acc" cx="{cx}" cy="{cy}" r="{r}" stroke-width="1.8" stroke-dasharray="5 4" fill="none"/>')
        a = math.radians(ang)
        lx, ly = cx + (r + 4) * math.cos(a), cy + (r + 4) * math.sin(a)
        o.append(f'<rect class="f-paper" x="{f(lx - (34 if ang < -90 else 0))}" y="{f(ly - 10)}" width="34" height="13" rx="2"/>' + text(lx, ly, lab, 't-s', 'end' if ang < -90 else 'start'))
    o.append(chg(cx, cy, 1, 12))
    o.append(f'<path id="equipotential-orb" d="M{cx + 40},{cy}A40,40 0 1 1 {cx - 40},{cy}A40,40 0 1 1 {cx + 40},{cy}" fill="none"/>')
    o.append(f'<circle class="f-ink" r="6" opacity="0">{phase_op("1;0", "0;0.5", dur)}<animateMotion dur="{dur}s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.5;1" calcMode="linear"><mpath href="#equipotential-orb"/></animateMotion></circle>')
    o.append(f'<circle class="f-ink" r="6" opacity="0">{phase_op("0;1;0", "0;0.5;0.98", dur)}<animate attributeName="cx" values="{cx + 20};{cx + 20};{cx + 210};{cx + 210}" keyTimes="0;0.5;0.95;1" dur="{dur}s" repeatCount="indefinite"/><animate attributeName="cy" values="{cy}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append('<rect class="f-paper" x="196" y="16" width="160" height="40" rx="4" opacity="0.9"/>')
    o.append(f'<g>{phase_op("1;0", "0;0.5", dur)}' + text(352, 30, 'вдоль эквипотенциали', 't', 'end') + text(352, 50, 'φ = const, A = 0', 't-s', 'end') + '</g>')
    o.append(f'<g opacity="0">{phase_op("0;1", "0;0.5", dur)}' + text(352, 30, 'вдоль силовой линии', 't', 'end') + text(352, 50, 'φ падает: 500→300→100 В', 't-s', 'end') + '</g>')
    return ''.join(o)


@fig('work-paths', 'Работа однородного поля не зависит от формы пути: между двумя эквипотенциалями A₁ = A₂ = A₃ = A₄ = Eqd', 360, 230)
def work_paths():
    dur = 12
    x1, x2 = 90, 270
    o = [text(180, 18, 'A₁ = A₂ = A₃ = A₄ = Eqd', 't')]
    for y in range(60, 211, 30):
        o.append(f'<path class="s-mute" d="M20,{y}H340" stroke-width="1.2"/>' + head(340, y, 0, 'f-mute', 6))
    o.append(f'<path class="s-acc" d="M{x1},40V214M{x2},40V214" stroke-width="2" stroke-dasharray="6 5"/>')
    o.append(text(x1 - 6, 228, 'φ₁', 't-acc', 'end') + text(x2 + 6, 228, 'φ₂', 't-acc', 'start'))
    o.append(f'<path class="s-ink" d="M{x1},34H{x2}M{x1},28V40M{x2},28V40" stroke-width="1.2"/>' + text((x1 + x2) / 2, 48, 'd', 't-s'))
    paths = [f'M{x1},75L{x2},75', f'M{x1},185L{x2},105', f'M{x1},135C150,60 200,220 {x2},160', f'M{x1},200L140,168L190,200L230,168L{x2},195']
    marks = [(75, '①'), (182, '②'), (135, '③'), (200, '④')]
    for k, d in enumerate(paths):
        o.append(f'<path id="work-paths-p{k}" class="s-red" d="{d}" stroke-width="1.8" fill="none" opacity="0.55"/>')
        t0, t1 = k / 4, k / 4 + 0.2
        o.append(f'<circle class="f-red" r="6" opacity="0">{phase_op("0;1;0", f"0;{f(t0)};{f(t1 + 0.04)}", dur)}'
                 f'<animateMotion dur="{dur}s" repeatCount="indefinite" keyPoints="0;0;1;1" keyTimes="0;{f(t0) if t0 else "0.0001"};{f(t1)};1" calcMode="linear"><mpath href="#work-paths-p{k}"/></animateMotion></circle>')
    for y, lab in marks:
        o.append(text(x1 - 10, y + 4, lab, 't-s', 'end'))
    o.append(text(352, 130, 'E', 't', 'end'))
    return ''.join(o)


@fig('contact-spheres', 'Контакт заряженных шаров: после соединения проводом потенциалы выравниваются, а заряд делится пропорционально радиусам (1 см и 3 см: 8 нКл → 2 и 6 нКл)', 360, 210)
def contact_spheres():
    dur = 8
    c1, R1, c2, R2, cy = (80, 22, 250, 60, 110)
    o = []
    o.append(f'<path class="s-ink" d="M{c1 + R1},{cy + 10}Q165,{cy + 60} {c2 - R2 + 4},{cy + 24}" stroke-width="2" fill="none" opacity="0">{phase_op("0;1;0", "0;0.2;0.92", dur)}</path>')
    o.append(f'<path class="s-red" d="M{c1 + R1},{cy + 10}Q165,{cy + 60} {c2 - R2 + 4},{cy + 24}" stroke-width="3" fill="none" stroke-dasharray="5 10" opacity="0">{flow(0.6, 15)}{phase_op("0;1;0", "0;0.2;0.6", dur)}</path>')
    o.append(f'<circle class="f-soft s-ink" cx="{c1}" cy="{cy}" r="{R1}" stroke-width="2"/><circle class="f-soft s-ink" cx="{c2}" cy="{cy}" r="{R2}" stroke-width="2"/>')
    # 8 зарядов на маленьком шаре: 2 остаются, 6 уходят; на большом появляются 6
    for k in range(8):
        a = k / 8 * 2 * math.pi
        x, y = c1 + (R1 - 6) * math.cos(a), cy + (R1 - 6) * math.sin(a)
        op = '' if k < 2 else f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;{f(0.22 + 0.04 * k)};{f(0.26 + 0.04 * k)};0.92;1" dur="{dur}s" repeatCount="indefinite"/>'
        o.append(f'<g>{op}{text(x, y + 4, "+", "t-red")}</g>')
    for k in range(6):
        a = k / 6 * 2 * math.pi + 0.4
        x, y = c2 + (R2 - 8) * math.cos(a), cy + (R2 - 8) * math.sin(a)
        o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{f(0.26 + 0.05 * k)};{f(0.3 + 0.05 * k)};0.92;1" dur="{dur}s" repeatCount="indefinite"/>{text(x, y + 4, "+", "t-red")}</g>')
    o.append(text(c1, cy + R1 + 20, 'R₁ = 1 см', 't-s') + text(c2, cy + R2 + 20, 'R₂ = 3 см', 't-s'))
    o.append(f'<g>{phase_op("1;0;1", "0;0.6;0.92", dur)}' + text(180, 26, 'до контакта: q₁ = 8 нКл, q₂ = 0', 't') + '</g>')
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.6;0.92", dur)}' + text(180, 26, "после: q₁' = 2 нКл, q₂' = 6 нКл", 't-red') + text(180, 44, 'φ₁ = φ₂', 't-s') + '</g>')
    return ''.join(o)


# ───────────────────────────── конденсаторы ─────────────────────────────

@fig('capacitor-charge', 'Конденсатор: после замыкания ключа на пластинах накапливаются равные по модулю и противоположные по знаку заряды, между пластинами возникает поле; q = CU', 360, 220)
def capacitor_charge():
    dur, n = 8, 25
    o = [markers('capacitor-charge', ('red',))]
    # провода и источник
    o.append('<path class="s-ink" d="M70,40H210V80M70,40V180H210V140" stroke-width="2" fill="none"/>')
    o.append(battery(70, 110, True, 'U'))
    # ключ
    o.append(f'<g><animateTransform attributeName="transform" type="rotate" values="-30 120 40;-30 120 40;0 120 40;0 120 40;-30 120 40" keyTimes="0;0.1;0.15;0.9;1" dur="{dur}s" repeatCount="indefinite"/><path class="s-ink" d="M120,40H150" stroke-width="2.6"/></g>')
    o.append('<rect class="f-paper" x="121" y="36" width="28" height="8"/><circle class="f-ink" cx="120" cy="40" r="3"/><circle class="f-ink" cx="150" cy="40" r="3"/>')
    # пластины
    o.append('<path class="s-ink" d="M160,80H260M160,140H260" stroke-width="4"/>')
    # заряды на пластинах
    for k in range(7):
        x = 168 + 14 * k
        t0 = 0.17 + 0.06 * k
        o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{f(t0)};{f(t0 + 0.02)};0.9;1" dur="{dur}s" repeatCount="indefinite"/>'
                 + text(x, 74, '+', 't-red') + text(x, 156, '−', 't-acc') + '</g>')
    # поле между пластинами
    for k in range(5):
        x = 175 + 18 * k
        o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.4;0.6;0.9;1" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<path class="s-red" d="M{x},86V132" stroke-width="1.6"/>{head(x, 134, 90, "f-red", 6)}</g>')
    # ток при зарядке
    o.append(f'<path class="s-red" d="M152,40H210V76" stroke-width="3" stroke-dasharray="5 9" fill="none" opacity="0">{flow(0.5, 14)}{phase_op("0;1;0", "0;0.15;0.62", dur, False)}</path>')
    o.append(f'<path class="s-red" d="M210,144V180H70V128" stroke-width="3" stroke-dasharray="5 9" fill="none" opacity="0">{flow(0.5, 14, True)}{phase_op("0;1;0", "0;0.15;0.62", dur, False)}</path>')
    o.append(text(270, 84, '+q', 't-red', 'start') + text(270, 144, '−q', 't-acc', 'start') + text(300, 114, 'q = CU', 't'))
    o.append(f'<text class="t-s" x="210" y="206" text-anchor="middle">идёт зарядка — ток в проводах{phase_op("0;1;0;0", "0;0.15;0.62;1", dur)}</text>')
    o.append(f'<text class="t-s" x="210" y="206" text-anchor="middle" opacity="0">заряжен: ток не идёт, U_c = U{phase_op("0;1;0", "0;0.62;0.9", dur)}</text>'.replace('U_c', 'U<tspan baseline-shift="sub" font-size="0.72em">c</tspan>'))
    return ''.join(o)


@fig('cap-series', 'Последовательное соединение конденсаторов: заряды одинаковы, а напряжение источника делится — на конденсаторе меньшей ёмкости напряжение больше', 360, 220)
def cap_series():
    dur = 6
    C1, C2, U = 2, 3, 10
    Cob = C1 * C2 / (C1 + C2)
    U1, U2 = U * Cob / C1, U * Cob / C2
    kt = '0;0.1;0.5;0.9;1'
    o = []
    o.append('<path class="s-ink" d="M40,60H110M130,60H210M230,60H280V160H40V60" stroke-width="2" fill="none"/>')
    o.append(cap_sym(120, 60, False, 10, 30, 'C₁ = 2 мкФ') + cap_sym(220, 60, False, 10, 30, 'C₂ = 3 мкФ'))
    o.append(battery(160, 160, False, 'U = 10 В'))
    for x in (120, 220):
        for k, y in enumerate((50, 60, 70)):
            o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{f(0.1 + 0.1 * k)};{f(0.15 + 0.1 * k)};0.9;1" dur="{dur}s" repeatCount="indefinite"/>'
                     + text(x - 12, y + 4, '+', 't-red', 'end') + text(x + 12, y + 4, '−', 't-acc', 'start') + '</g>')
    o.append(text(170, 104, 'q₁ = q₂ = 12 мкКл', 't'))
    # столбики напряжений
    base, sc = 205, 10
    for x, u, lab in [(300, U1, 'U₁ = 6 В'), (338, U2, 'U₂ = 4 В')]:
        o.append(f'<rect class="s-mute" x="{x - 12}" y="{base - sc * U}" width="24" height="{sc * U}" stroke-width="1" stroke-dasharray="3 3"/>')
        o.append(f'<rect class="f-acc" x="{x - 12}" width="24"><animate attributeName="height" values="0;0;{f(sc * u)};{f(sc * u)};0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y" values="{base};{base};{f(base - sc * u)};{f(base - sc * u)};{base}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></rect>')
        o.append(text(x, base + 14, lab.split(' = ')[0], 't-s') + text(x, base - sc * U - 4, lab.split(' = ')[1], 't-s'))
    o.append(text(170, 200, 'U = U₁ + U₂', 't-s'))
    return ''.join(o)


@fig('key-circuit', 'Пример конспекта: при разомкнутом ключе C_об = 4C/3, при замкнутом схема становится (C ∥ 2C) + (2C ∥ C) и C_об = 3C/2 — ёмкость растёт в 9/8 раз', 360, 220)
def key_circuit():
    dur = 6
    o = []
    o.append('<path class="s-ink" d="M20,110H70M70,50V170M70,50H125M145,50H215M235,50H290M70,170H125M145,170H215M235,170H290M290,50V170M290,110H340" stroke-width="2" fill="none"/>')
    o.append(cap_sym(135, 50, False, 10, 28, 'C') + cap_sym(225, 50, False, 10, 28, '2C') + cap_sym(135, 170, False, 10, 28, '2C') + cap_sym(225, 170, False, 10, 28, 'C'))
    o.append('<path class="s-ink" d="M180,50V90M180,130V170" stroke-width="2"/><circle class="f-ink" cx="180" cy="90" r="3"/><circle class="f-ink" cx="180" cy="130" r="3"/>')
    o.append(f'<g><animateTransform attributeName="transform" type="rotate" values="0 180 130;0 180 130;30 180 130;30 180 130;0 180 130" keyTimes="0;0.45;0.5;0.95;1" dur="{dur}s" repeatCount="indefinite"/>'
             '<path class="s-ink" d="M180,130V92" stroke-width="2.6"/></g>')
    o.append(text(190, 114, 'K', 't', 'start'))
    o.append(f'<text class="t" x="180" y="206" text-anchor="middle" opacity="0">ключ разомкнут: C_об = 4C/3{phase_op("0;1;0", "0;0.5;0.95", dur)}</text>'.replace('C_об', 'C<tspan baseline-shift="sub" font-size="0.72em">об</tspan>'))
    o.append(f'<text class="t-red" x="180" y="206" text-anchor="middle">ключ замкнут: C_об = 3C/2{phase_op("1;0;1", "0;0.5;0.95", dur)}</text>'.replace('C_об', 'C<tspan baseline-shift="sub" font-size="0.72em">об</tspan>'))
    o.append(f'<g>{phase_op("1;0;1", "0;0.5;0.95", dur)}<path class="s-red" d="M180,50V170" stroke-width="2.4" stroke-dasharray="4 4"/></g>')
    return ''.join(o)


@fig('plates-field', 'Поле конденсатора: поля двух разноимённых пластин складываются — между пластинами E = σ/εε₀, а снаружи они компенсируют друг друга (E = 0)', 360, 220)
def plates_field():
    dur = 9
    xp, xn = 140, 220
    o = [markers('plates-field', ('red', 'acc', 'ink'))]
    o.append(f'<rect class="f-red" x="{xp - 4}" y="30" width="8" height="150" rx="2"/><rect class="f-acc" x="{xn - 4}" y="30" width="8" height="150" rx="2"/>')
    o.append(text(xp, 22, '+σ', 't-red') + text(xn, 22, '−σ', 't-acc'))
    L = 34
    regions = [(70, 'left'), (180, 'mid'), (290, 'right')]
    red, blue, res = [], [], []
    for x, reg in regions:
        dr = -1 if reg == 'left' else 1          # от «+» пластины
        db = 1 if reg != 'right' else -1         # к «−» пластине
        red.append(mline('plates-field', x - dr * L / 2, 70, x + dr * L / 2, 70, 'red', 2.4))
        blue.append(mline('plates-field', x - db * L / 2, 100, x + db * L / 2, 100, 'acc', 2.4))
        if reg == 'mid':
            res.append(mline('plates-field', x - L, 140, x + L, 140, 'ink', 3))
        else:
            res.append(text(x, 145, 'E = 0', 't'))
    o.append(f'<g>{phase_op("1;1;1;0", "0;0.3;0.6;0.95", dur)}{"".join(red)}</g>')
    o.append(f'<g opacity="0">{phase_op("0;1;1;0", "0;0.3;0.6;0.95", dur)}{"".join(blue)}</g>')
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.6;0.95", dur)}{"".join(res)}</g>')
    o.append(f'<text class="t-s" x="180" y="204" text-anchor="middle">поле пластины +σ: E = σ/2εε₀ по обе стороны{phase_op("1;0;0", "0;0.3;0.95", dur)}</text>')
    o.append(f'<text class="t-s" x="180" y="204" text-anchor="middle" opacity="0">добавили поле пластины −σ{phase_op("0;1;0", "0;0.3;0.6", dur)}</text>')
    o.append(f'<text class="t" x="180" y="204" text-anchor="middle" opacity="0">внутри E = σ/εε₀, снаружи E = 0{phase_op("0;1;0", "0;0.6;0.95", dur)}</text>')
    return ''.join(o)


@fig('cap-two-cases', 'Раздвигаем пластины: если конденсатор подключён к источнику (U = const), энергия уменьшается; если заряжен и отключён (q = const), энергия растёт', 360, 230)
def cap_two_cases():
    dur, n = 8, 33
    us = lin(0, 1, n)
    k = [1 + (0.5 - 0.5 * math.cos(2 * math.pi * u)) for u in us]   # d: 1 → 2 → 1
    o = []
    for cx, title_, conn in [(95, 'подключён: U = const', True), (265, 'отключён: q = const', False)]:
        o.append(text(cx, 20, title_, 't'))
        d0 = 20
        top = [100 - d0 * v / 2 for v in k]
        bot = [100 + d0 * v / 2 for v in k]
        o.append(f'<rect class="f-ink" x="{cx - 40}" width="80" height="5">{anim("y", nums([t - 5 for t in top]), dur)}</rect>')
        o.append(f'<rect class="f-ink" x="{cx - 40}" width="80" height="5">{anim("y", nums(bot), dur)}</rect>')
        if conn:
            o.append(f'<path class="s-ink" fill="none" stroke-width="2">{anim("d", ";".join(f"M{cx},{f(t - 5)}V40H{cx - 70}V160H{cx}V{f(b + 5)}" for t, b in zip(top, bot)), dur)}</path>')
            o.append(battery(cx - 70, 100, True, ''))
        # столбики C и W
        base, h0 = 216, 30
        C = [1 / v for v in k]
        W = [1 / v for v in k] if conn else [v for v in k]
        for dx, vals, lab, cls in [(-28, C, 'C', 'f-acc'), (0, [1] * n if conn else k, 'U', 'f-grn'), (28, W, 'W', 'f-red')]:
            x = cx + dx
            o.append(f'<rect class="{cls}" x="{x - 9}" width="18">{anims(dur, y=[base - h0 * v for v in vals], height=[h0 * v for v in vals])}</rect>')
            o.append(text(x, base + 12, lab, 't-s'))
    o.append(text(180, 120, 'd ↑', 't-s'))
    return ''.join(o)


# ───────────────────────────── постоянный ток ─────────────────────────────

@fig('current-drift', 'Электрический ток в проводнике: свободные электроны медленно дрейфуют в одну сторону, а условное направление тока — противоположное', 360, 190)
def current_drift():
    dur = 6
    o = [markers('current-drift', ('red', 'acc'))]
    o.append('<rect class="f-soft s-ink" x="20" y="50" width="320" height="80" rx="40" stroke-width="2"/>')
    o.append('<clipPath id="current-drift-clip"><rect x="22" y="52" width="316" height="76" rx="38"/></clipPath>')
    rnd = random.Random(8)
    g = ['<g clip-path="url(#current-drift-clip)">']
    for i in range(5):
        for j in range(3):
            x, y = 50 + 62 * i + (j % 2) * 30, 70 + 20 * j
            g.append(f'<circle class="f-mute" cx="{x}" cy="{y}" r="5" opacity="0.6"/>')
    for i in range(16):
        x0 = rnd.uniform(0, 360)
        y = rnd.uniform(60, 120)
        g.append(f'<circle class="f-acc" r="4" cy="{f(y)}"><animate attributeName="cx" values="{f(x0)};{f(x0 - 360)}" dur="{dur}s" repeatCount="indefinite"/></circle>')
        g.append(f'<circle class="f-acc" r="4" cy="{f(y)}"><animate attributeName="cx" values="{f(x0 + 360)};{f(x0)}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    g.append('</g>')
    o += g
    o.append(mline('current-drift', 120, 30, 240, 30, 'red', 3) + text(180, 22, 'I — направление тока', 't-red'))
    o.append(mline('current-drift', 240, 152, 120, 152, 'acc', 3) + text(180, 176, 'движение электронов', 't-acc'))
    return ''.join(o)


@fig('charge-area', 'Заряд при меняющейся силе тока равен площади под графиком I(t); при линейном изменении q = Ī·Δt, где Ī = (I₁ + I₂)/2', 360, 210)
def charge_area():
    dur = 8
    gx, gy = 50, 186
    t1, t2 = 90, 300
    I1, I2 = 50, 140
    o = [f'<clipPath id="charge-area-clip"><rect x="{t1}" y="0" height="210" width="0"><animate attributeName="width" values="0;0;{t2 - t1};{t2 - t1}" keyTimes="0;0.05;0.5;1" dur="{dur}s" repeatCount="indefinite"/></rect></clipPath>']
    o.append(f'<path class="f-soft" d="M{t1},{gy}V{gy - I1}L{t2},{gy - I2}V{gy}Z" clip-path="url(#charge-area-clip)"/>')
    o.append(arrow(gx, gy, 350, gy, 's-ink', 'f-ink', 1.4, 6) + arrow(gx, gy, gx, 20, 's-ink', 'f-ink', 1.4, 6) + text(gx + 10, 30, 'I', 't', 'start') + text(346, gy + 16, 't', 't', 'end'))
    o.append(f'<path class="s-acc" d="M{t1 - 20},{gy - I1 + 9}L{t2 + 20},{gy - I2 - 9}" stroke-width="2.6"/>')
    for t, lab in [(t1, 't₁'), (t2, 't₂')]:
        o.append(f'<path class="s-mute" d="M{t},{gy}V{gy - 150}" stroke-width="1" stroke-dasharray="3 4"/>' + text(t, gy + 16, lab, 't-s'))
    Iav = (I1 + I2) / 2
    o.append(f'<g opacity="0">{phase_op("0;1;0", "0;0.55;0.97", dur)}<rect class="s-red" x="{t1}" y="{gy - Iav}" width="{t2 - t1}" height="{Iav}" fill="none" stroke-width="2" stroke-dasharray="6 4"/>'
             + text(t2 + 6, gy - Iav + 4, 'Ī', 't-red', 'start') + text((t1 + t2) / 2, gy - 30, 'q = Ī·Δt', 't-red') + '</g>')
    o.append(f'<g>{phase_op("1;0;1", "0;0.55;0.97", dur)}' + text((t1 + t2) / 2, gy - 30, 'S = q', 't-acc') + '</g>')
    return ''.join(o)


@fig('wire-resistance', 'Сопротивление проводника R = ρl/S: при удлинении провода сопротивление растёт, при утолщении (большей площади сечения) — уменьшается', 360, 200)
def wire_resistance():
    dur = 10
    kt = '0;0.1;0.35;0.5;0.6;0.85;1'
    L = [140, 140, 280, 280, 280, 280, 140]
    H = [16, 16, 16, 16, 32, 32, 16]
    R = [l / h for l, h in zip(L, H)]
    base = 180
    o = []
    o.append(f'<rect class="f-mute" x="30" rx="4"><animate attributeName="width" values="{nums(L)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="height" values="{nums(H)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="{nums([70 - h / 2 for h in H])}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></rect>')
    o.append(f'<line class="s-ink" x1="30" y1="104" y2="104" stroke-width="1.2"><animate attributeName="x2" values="{nums([30 + l for l in L])}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></line>')
    o.append(text(40, 120, 'l', 't', 'start'))
    o.append(text(20, 74, 'S', 't', 'end'))
    hb = [6 * r for r in R]
    o.append('<rect class="s-mute" x="314" y="60" width="30" height="120" stroke-width="1" stroke-dasharray="3 3"/>')
    o.append(f'<rect class="f-red" x="314" width="30"><animate attributeName="height" values="{nums(hb)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="{nums([base - h for h in hb])}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></rect>')
    o.append(text(329, 196, 'R', 't'))
    o.append(f'<text class="t-s" x="20" y="170" text-anchor="start">l × 2 → R × 2{phase_op("0;1;0", "0;0.1;0.5", dur)}</text>')
    o.append(f'<text class="t-s" x="20" y="170" text-anchor="start" opacity="0">S × 2 → R : 2{phase_op("0;1;0", "0;0.5;0.85", dur)}</text>')
    o.append(text(160, 150, 'R = ρl / S', 't'))
    return ''.join(o)


@fig('wheatstone', 'Мост Уитстона: меняем R₄ — стрелка прибора в диагонали отклоняется, пока не выполнится условие баланса R₁R₄ = R₂R₃ (R₁ = 2, R₂ = 4, R₃ = 3 → R₄ = 6 Ом)', 360, 230)
def wheatstone():
    dur, n = 10, 41
    R1, R2, R3 = 2, 4, 3
    us = lin(0, 1, n)
    R4 = [2 + 8 * (0.5 - 0.5 * math.cos(2 * math.pi * u)) for u in us]
    Va = R2 / (R1 + R2)
    defl = [max(-60, min(60, 300 * (Va - r / (R3 + r)))) for r in R4]
    L, T, Rr, B = (40, 40, 280, 170)
    mx = (L + Rr) / 2
    o = []
    o.append(f'<path class="s-ink" d="M10,105H{L}M{Rr},105H330V200H10V105M{L},105L{mx},{T}L{Rr},105L{mx},{B}Z" stroke-width="2" fill="none"/>')
    o.append(battery(170, 200, False, 'U'))
    for (x1, y1, x2, y2, lab) in [(L, 105, mx, T, 'R₁'), (mx, T, Rr, 105, 'R₂'), (L, 105, mx, B, 'R₃'), (mx, B, Rr, 105, 'R₄')]:
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        o.append(f'<g transform="rotate({f(ang)} {f(cx)} {f(cy)})"><rect class="f-paper s-ink" x="{f(cx - 18)}" y="{f(cy - 7)}" width="36" height="14" rx="2" stroke-width="2"/></g>')
        o.append(text(cx + (0 if cy < 105 else 0), cy + (-14 if cy < 105 else 24), lab, 't-s'))
    o.append(f'<path class="s-ink" d="M{mx},{T}V{B}" stroke-width="2"/>')
    o.append(dial(mx, 105, defl, dur, 'G', 18))
    o.append(f'<path class="s-red" d="M{mx + 34},{B - 22}l20,-20" stroke-width="2"/>' + head(mx + 56, B - 44, -45, 'f-red', 7))
    bal = [1 if abs(r - 6) < 0.35 else 0 for r in R4]
    o.append(f'<text class="t-red" x="352" y="30" text-anchor="end" opacity="0">R₄ = 6 Ом: баланс, I₀ = 0{anim("opacity", nums(bal), dur, " calcMode=\"discrete\"")}</text>')
    o.append(f'<text class="t-s" x="352" y="30" text-anchor="end">меняем R₄ (2…10 Ом){anim("opacity", nums([1 - b for b in bal]), dur, " calcMode=\"discrete\"")}</text>')
    o.append(text(352, 224, 'R₁R₄ = R₂R₃', 't', 'end'))
    return ''.join(o)


@fig('meters', 'Амперметр включают последовательно — через него идёт весь ток; вольтметр подключают параллельно, у него большое сопротивление и ток через него почти не идёт', 360, 220)
def meters():
    dur, n = 8, 33
    us = lin(0, 1, n)
    U = [0.4 + 0.6 * (0.5 - 0.5 * math.cos(2 * math.pi * u)) for u in us]
    o = []
    o.append('<path class="s-ink" d="M60,50H300V170H60V50M150,170V120H250V170" stroke-width="2" fill="none"/>')
    o.append(battery(60, 110, True, ''))
    o.append(resistor(170, 230, 170, 'R'))
    o.append(dial(180, 50, [-60 + 120 * u for u in U], dur, 'A'))
    o.append(dial(200, 120, [-60 + 120 * u for u in U], dur, 'V'))
    o.append(f'<path class="s-red" d="M84,50H160M200,50H300V170H250M150,170H60V130" stroke-width="3" stroke-dasharray="5 9" fill="none">{flow(0.6, 14)}</path>')
    o.append(text(180, 24, 'амперметр — последовательно', 't-s') + text(200, 98, 'вольтметр — параллельно R', 't-s'))
    o.append(text(180, 204, 'ток идёт через амперметр, а через вольтметр — почти нет', 't-s'))
    return ''.join(o)


@fig('lamps-series', 'Одинаковые лампочки последовательно при U = const: мощность P = U²/(nR) — чем больше лампочек, тем слабее светит каждая', 360, 210)
def lamps_series():
    dur = 10
    counts = [1, 2, 3, 5, 8]
    kt = '0;0.2;0.4;0.6;0.8'
    o = []
    o.append('<path class="s-ink" d="M30,60H330V160H30V60" stroke-width="2" fill="none"/>')
    o.append(battery(30, 110, True, ''))
    for i in range(8):
        x = 60 + 36 * i
        vis = ';'.join('1' if i < c else '0' for c in counts)
        glow = [min(1, 1 / c ** 2 * 1.0) for c in counts]
        glow_vals = ';'.join(f(g if i < c else 0) for g, c in zip(glow, counts))
        o.append(f'<g opacity="0"><animate attributeName="opacity" values="{vis}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>'
                 f'<rect class="f-paper" x="{x - 12}" y="48" width="24" height="24"/>'
                 f'<circle class="f-red-soft" cx="{x}" cy="60" r="20"><animate attributeName="opacity" values="{glow_vals}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></circle>'
                 f'<circle class="f-red" cx="{x}" cy="60" r="8"><animate attributeName="opacity" values="{glow_vals}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></circle>'
                 + lamp(x, 60) + '</g>')
    for c, k in zip(counts, kt.split(';')):
        t1 = {'0': '0.2', '0.2': '0.4', '0.4': '0.6', '0.6': '0.8', '0.8': '1'}[k]
        o.append(f'<text class="t" x="180" y="196" text-anchor="middle" opacity="0">n = {c}: P = U²/{c if c > 1 else ""}R<animate attributeName="opacity" values="0;1;0" keyTimes="0;{k if k != "0" else "0.0001"};{t1 if t1 != "1" else "0.9999"}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>'.replace('values="0;1;0" keyTimes="0;0.0001', 'values="1;1;0" keyTimes="0;0.0001'))
    return ''.join(o)


@fig('lamps-nominal', 'Лампы 100 Вт и 25 Вт (220 В): параллельно они горят в полную силу; последовательно лампа 25 Вт получает 16 Вт, а лампа 100 Вт — только 4 Вт', 360, 220)
def lamps_nominal():
    dur = 6
    kt = '0;0.15;0.85;1'
    def gl(v):
        return [0, v, v, 0]
    o = [text(90, 20, 'параллельно', 't') + text(270, 20, 'последовательно', 't')]
    o.append('<path class="s-ink" d="M30,50H150V170H30V50M30,110H150" stroke-width="2" fill="none"/>')
    o.append('<rect class="f-paper" x="20" y="150" width="20" height="24"/>' + battery(30, 160, True, ''))
    o.append(lamp(90, 50, gl(1.0), dur, kt=kt, label='') + lamp(90, 110, gl(0.25 ** 0.5), dur, kt=kt))
    o.append(text(118, 46, '100 Вт', 't-s', 'start') + text(118, 106, '25 Вт', 't-s', 'start'))
    o.append('<path class="s-ink" d="M210,60H330V170H210V60" stroke-width="2" fill="none"/>')
    o.append(battery(210, 150, True, ''))
    o.append(lamp(240, 60, gl((4 / 100) ** 0.5), dur, kt=kt) + lamp(300, 60, gl((16 / 100) ** 0.5), dur, kt=kt))
    o.append(text(270, 100, '100 Вт → 4 Вт', 't-s') + text(270, 122, '25 Вт → 16 Вт', 't-red'))
    o.append(text(180, 200, 'последовательно ярче лампа меньшей мощности', 't-s'))
    return ''.join(o)


@fig('full-circuit', 'Закон Ома для полной цепи I = ε/(R + r): уменьшаем внешнее сопротивление — ток растёт до тока короткого замыкания ε/r, а напряжение на клеммах падает', 360, 220)
def full_circuit():
    dur, n = 8, 41
    eps, r = 12, 1
    us = lin(0, 1, n)
    R = [0.2 + 9.8 * (0.5 + 0.5 * math.cos(2 * math.pi * u)) for u in us]
    I = [eps / (x + r) for x in R]
    Uo = [eps * x / (x + r) for x in R]
    o = []
    o.append('<rect class="s-mute" x="22" y="70" width="70" height="80" rx="6" stroke-width="1.2" stroke-dasharray="4 3"/>' + text(57, 164, 'источник', 't-s'))
    o.append('<path class="s-ink" d="M57,70V40H220V70M57,150V180H220V150" stroke-width="2" fill="none"/>')
    o.append(battery(57, 92, True, '') + resistor(116, 136, 57, '', vertical=True) + text(70, 130, 'r', 't-s', 'start') + text(76, 96, 'ε', 't', 'start'))
    o.append('<path class="s-ink" d="M57,98V116M57,136V150" stroke-width="2"/>')
    o.append(f'<rect class="f-paper s-ink" x="210" y="70" width="20" height="80" rx="2" stroke-width="2"/>' + text(240, 114, 'R', 't', 'start'))
    o.append(f'<path class="s-red" d="M234,150L206,70" stroke-width="2"/>' + head(206, 70, -110, 'f-red', 7))
    o.append(f'<path class="s-red" d="M57,40H220M220,180H57" stroke-width="3" stroke-dasharray="5 9" fill="none"><animate attributeName="stroke-dashoffset" values="14;0" dur="1s" repeatCount="indefinite"/></path>')
    base, sc = 200, 12
    for x, vals, lab, cls, top in [(290, I, 'I', 'f-red', 12), (330, Uo, 'U_внеш', 'f-acc', 12)]:
        o.append(f'<rect class="s-mute" x="{x - 12}" y="{base - sc * top}" width="24" height="{sc * top}" stroke-width="1" stroke-dasharray="3 3"/>')
        o.append(f'<rect class="{cls}" x="{x - 12}" width="24">{anims(dur, y=[base - sc * v for v in vals], height=[sc * v for v in vals])}</rect>')
        o.append(text(x, base + 14, lab, 't-s'))
    o.append(text(310, 40, 'I_кз = ε/r', 't-s'))
    o.append(text(180, 214, 'R ↓ → I ↑, U_внеш ↓', 't-s'))
    return ''.join(o)


@fig('max-power', 'Полезная мощность P = ε²R/(R + r)² максимальна при R = r и равна ε²/4r; КПД при этом 50 %', 360, 220)
def max_power():
    dur, n = 8, 61
    r = 1
    us = lin(0, 1, n)
    Rs = [0.05 + 4.95 * (0.5 - 0.5 * math.cos(2 * math.pi * u)) for u in us]
    P = lambda R: R / (R + r) ** 2   # в единицах ε²/r
    gx, gy, sx, sy = 40, 190, 60, 580
    o = [arrow(gx, gy, 352, gy, 's-ink', 'f-ink', 1.4, 6) + arrow(gx, gy, gx, 20, 's-ink', 'f-ink', 1.4, 6)]
    o.append(text(gx + 10, 30, 'P_полез', 't', 'start') + text(348, gy + 16, 'R', 't', 'end'))
    curve = 'L'.join(f'{f(gx + sx * R)},{f(gy - sy * P(R))}' for R in lin(0, 5, 60))
    o.append(f'<path class="s-acc" d="M{curve}" stroke-width="2.6" fill="none"/>')
    o.append(f'<path class="s-red" d="M{gx + sx * r},{gy}V{f(gy - sy * 0.25)}H{gx}" stroke-width="1.2" stroke-dasharray="4 4" fill="none"/>')
    o.append(text(gx + sx * r, gy + 16, 'R = r', 't-red') + text(gx + sx * r + 8, gy - sy * 0.25 - 6, 'ε²/4r', 't-red', 'start'))
    o.append(f'<circle class="f-red" r="6">{anims(dur, cx=[gx + sx * R for R in Rs], cy=[gy - sy * P(R) for R in Rs])}</circle>')
    eta = [R / (R + r) for R in Rs]
    o.append('<rect class="s-mute" x="318" y="60" width="24" height="100" stroke-width="1" stroke-dasharray="3 3"/>')
    o.append(f'<rect class="f-grn" x="318" width="24">{anims(dur, y=[160 - 100 * e for e in eta], height=[100 * e for e in eta])}</rect>' + text(330, 52, 'η', 't'))
    o.append('<path class="s-ink" d="M312,110H348" stroke-width="1" stroke-dasharray="2 3"/>' + text(312, 114, '50 %', 't-s', 'end'))
    return ''.join(o)


@fig('sources-connect', 'Последовательное соединение источников: при одинаковой полярности ЭДС складываются (3 × 1,5 = 4,5 В); если один источник перевернуть, его ЭДС вычитается (1,5 В), а внутренние сопротивления всё равно складываются', 360, 200)
def sources_connect():
    dur = 8
    o = []
    o.append('<path class="s-ink" d="M40,80H320V150H40V80" stroke-width="2" fill="none"/>')
    for k, x in enumerate((100, 180, 260)):
        if k < 2:
            o.append(battery(x, 80, False, '1,5 В'))
        else:
            o.append(f'<g><animateTransform attributeName="transform" type="rotate" values="0 {x} 80;0 {x} 80;180 {x} 80;180 {x} 80;0 {x} 80" keyTimes="0;0.4;0.5;0.9;1" dur="{dur}s" repeatCount="indefinite"/>{battery(x, 80, False, "")}</g>' + text(x, 64, '1,5 В', 't-s'))
    o.append(f'<rect class="f-acc" x="150" height="16" y="160"><animate attributeName="width" values="135;135;45;45;135" keyTimes="0;0.4;0.5;0.9;1" dur="{dur}s" repeatCount="indefinite"/></rect>')
    o.append(f'<text class="t" x="180" y="30" text-anchor="middle">ε_об = 1,5 + 1,5 + 1,5 = 4,5 В{phase_op("1;0;1", "0;0.45;0.95", dur)}</text>'.replace('ε_об', 'ε<tspan baseline-shift="sub" font-size="0.72em">об</tspan>'))
    o.append(f'<text class="t-red" x="180" y="30" text-anchor="middle" opacity="0">один наоборот: 1,5 + 1,5 − 1,5 = 1,5 В{phase_op("0;1;0", "0;0.45;0.95", dur)}</text>')
    o.append(text(140, 173, 'ε_об', 't-s', 'end') + text(180, 196, 'r_об = r₁ + r₂ + r₃ — в обоих случаях', 't-s'))
    return ''.join(o)


@fig('cap-dc', 'Конденсатор в цепи постоянного тока: при включении лампочка вспыхивает, пока конденсатор заряжается, потом ток прекращается — I = 0, q = Cε', 360, 210)
def cap_dc():
    dur, n = 8, 33
    us = lin(0, 1, n)
    on = 0.1
    I = [0 if u < on else math.exp(-(u - on) / 0.08) if u < 0.9 else 0 for u in us]
    Q = [0 if u < on else 1 - math.exp(-(u - on) / 0.08) if u < 0.9 else 0 for u in us]
    o = []
    o.append('<path class="s-ink" d="M50,50H310V160H50V50" stroke-width="2" fill="none"/>')
    o.append(battery(50, 105, True, 'ε'))
    o.append(lamp(150, 50, I, dur))
    o.append(cap_sym(250, 50, False, 12, 34, 'C'))
    for k, dy in enumerate((-10, 0, 10)):
        o.append(f'<g>{anim("opacity", nums([1 if q > 0.2 + 0.3 * k else 0 for q in Q]), dur, " calcMode=\"discrete\"")}' + text(236, 54 + dy, '+', 't-red', 'end') + text(264, 54 + dy, '−', 't-acc', 'start') + '</g>')
    o.append(f'<path class="s-red" d="M74,50H140M160,50H243M257,50H310V160H50V120" stroke-width="3" stroke-dasharray="5 9" fill="none">{flow(0.5, 14)}{anim("opacity", nums(I), dur)}</path>')
    hb = [90 * v for v in I]
    o.append(text(180, 190, 'ток быстро спадает до нуля: I = 0, q = Cε', 't-s'))
    o.append(f'<rect class="f-red" x="330" width="16">{anims(dur, y=[150 - h for h in hb], height=hb)}</rect>' + text(338, 166, 'I', 't'))
    return ''.join(o)


# ───────────────────────────── ток в средах ─────────────────────────────

@fig('rt-graphs', 'Сопротивление и температура: у металла R растёт линейно, у электролита линейно падает, у полупроводника резко падает, у диэлектрика очень большое и почти не меняется', 360, 220)
def rt_graphs():
    dur, n = 8, 41
    gx, gy, w = 40, 196, 290
    o = [arrow(gx, gy, gx + w + 14, gy, 's-ink', 'f-ink', 1.4, 6) + arrow(gx, gy, gx, 16, 's-ink', 'f-ink', 1.4, 6) + text(gx + 8, 26, 'R', 't', 'start') + text(gx + w + 10, gy + 16, 't', 't', 'end')]
    curves = [
        ('s-mute', 'f-mute', lambda u: 34, 'диэлектрик'),
        ('s-red', 'f-red', lambda u: 130 - 70 * u, 'металл'),
        ('s-grn', 'f-grn', lambda u: 100 + 40 * u, 'электролит'),
        ('s-acc', 'f-acc', lambda u: 60 + 116 * (1 - math.exp(-3.5 * u)), 'полупроводник'),
    ]
    us = lin(0, 1, n)
    xs = [gx + 8 + (w - 30) * (0.5 - 0.5 * math.cos(2 * math.pi * u)) for u in us]
    for scls, fcls, fy, lab in curves:
        pts = 'L'.join(f'{f(gx + 8 + (w - 30) * u)},{f(fy(u))}' for u in lin(0, 1, 40))
        o.append(f'<path class="{scls}" d="M{pts}" stroke-width="2.4" fill="none"/>')
        o.append(f'<circle class="{fcls}" r="5">{anims(dur, cx=xs, cy=[fy((x - gx - 8) / (w - 30)) for x in xs])}</circle>')
        o.append(text(gx + w - 20, fy(1) - (22 if lab == 'электролит' else 8), lab, 't-s', 'end'))
    o.append(f'<line class="s-mute" y1="20" y2="{gy}" stroke-width="1" stroke-dasharray="3 4">{anims(dur, x1=xs, x2=xs)}</line>')
    return ''.join(o)


@fig('electrolysis', 'Электролиз: катионы движутся к катоду (−), анионы — к аноду (+); на катоде оседает вещество, его масса m = kIt растёт со временем', 360, 220)
def electrolysis():
    dur = 6
    o = []
    o.append('<path class="s-ink" d="M40,60V200H320V60" stroke-width="2.4" fill="none"/><rect class="f-soft" x="42" y="80" width="276" height="118"/>')
    o.append('<path class="s-ink" d="M80,40V20H280V40" stroke-width="2" fill="none"/>' + battery(180, 20, False, ''))
    o.append('<rect class="f-red" x="72" y="40" width="16" height="140" rx="2"/><rect class="f-acc" x="272" y="40" width="16" height="140" rx="2"/>')
    o.append(text(80, 196, 'анод +', 't-red') + text(280, 196, 'катод −', 't-acc'))
    o.append(f'<rect class="f-ink" y="80" height="100" opacity="0.6"><animate attributeName="x" values="272;262" dur="{dur * 3}s" repeatCount="indefinite"/><animate attributeName="width" values="0;10" dur="{dur * 3}s" repeatCount="indefinite"/></rect>')
    rnd = random.Random(5)
    for i in range(7):
        y = 92 + 13 * i
        ph = rnd.uniform(0, dur)
        o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;170 0" dur="{dur}s" begin="{f(-ph)}s" repeatCount="indefinite"/>{chg(96, y, 1, 6)}</g>')
        ph2 = rnd.uniform(0, dur)
        o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;-170 0" dur="{dur}s" begin="{f(-ph2)}s" repeatCount="indefinite"/>{chg(264, y + 6, -1, 6)}</g>')
    o.append(text(180, 66, 'm = kIt', 't'))
    return ''.join(o)


def lattice(x0, y0, nx=3, ny=3, step=50, special=None):
    out = []
    for i in range(nx):
        for j in range(ny):
            x, y = x0 + i * step, y0 + j * step
            if i < nx - 1:
                out.append(f'<path class="s-mute" d="M{x + 12},{y - 3}H{x + step - 12}M{x + 12},{y + 3}H{x + step - 12}" stroke-width="1.6"/>')
            if j < ny - 1:
                out.append(f'<path class="s-mute" d="M{x - 3},{y + 12}V{y + step - 12}M{x + 3},{y + 12}V{y + step - 12}" stroke-width="1.6"/>')
    for i in range(nx):
        for j in range(ny):
            x, y = x0 + i * step, y0 + j * step
            lab = special if (special and i == 1 and j == 1) else 'Si'
            cls = 'f-red' if lab not in ('Si',) else 'f-mute'
            out.append(f'<circle class="{cls}" cx="{x}" cy="{y}" r="11"/>' + text(x, y + 3.5, lab, 't-ws'))
    return ''.join(out)


@fig('semi-holes', 'Собственная проводимость полупроводника: электрон из соседней связи перескакивает в дырку, и дырка перемещается навстречу электронам — ток создают электроны и дырки', 360, 210)
def semi_holes():
    dur = 8
    o = [markers('semi-holes', ('ink',))]
    o.append(lattice(60, 50, 5, 3, 60))
    # дырка движется вправо по верхнему ряду связей, электроны прыгают влево
    xs = [90 + 60 * k for k in range(4)]
    kt = ';'.join(f(k / 4) for k in range(4)) + ';1'
    vals = ';'.join(f'{f(x)}' for x in xs) + f';{f(xs[0])}'
    o.append(f'<circle class="s-red" cy="47" r="5" stroke-width="2" fill="none"><animate attributeName="cx" values="{vals}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></circle>')
    for k in range(3):
        x_from, x_to = xs[k + 1], xs[k]
        t0, t1 = (k + 1) / 4 - 0.08, (k + 1) / 4
        o.append(f'<circle class="f-acc" cy="47" r="4" opacity="0"><animate attributeName="opacity" values="0;1;0" keyTimes="0;{f(t0)};{f(t1)}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>'
                 f'<animate attributeName="cx" values="{x_from};{x_from};{x_to};{x_to}" keyTimes="0;{f(t0)};{f(t1)};1" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(mline('semi-holes', 150, 188, 60, 188, 'ink', 2) + text(105, 205, 'электроны', 't-acc'))
    o.append(mline('semi-holes', 220, 188, 310, 188, 'ink', 2) + text(265, 205, 'дырка', 't-red'))
    o.append(text(330, 30, 'I_e = I_дырки', 't-s', 'end'))
    return ''.join(o)


@fig('semi-np', 'Примесная проводимость: атом фосфора (V) в кремнии отдаёт лишний электрон — n-тип, донорная примесь; атом бора (III) создаёт дырку — p-тип, акцепторная примесь', 360, 220)
def semi_np():
    dur = 6
    o = []
    o.append(text(90, 20, 'n-тип: Si + P', 't') + text(270, 20, 'p-тип: Si + B', 't'))
    o.append(lattice(40, 60, 3, 3, 50, 'P'))
    o.append(lattice(220, 60, 3, 3, 50, 'B'))
    # лишний электрон фосфора уходит
    o.append(f'<circle class="f-acc" r="4.5"><animate attributeName="cx" values="98;98;150;150" keyTimes="0;0.2;0.7;1" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="cy" values="100;100;188;188" keyTimes="0;0.2;0.7;1" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="1;1;0" keyTimes="0;0.7;0.75" dur="{dur}s" repeatCount="indefinite"/></circle>')
    # дырка у бора заполняется электроном соседа
    o.append(f'<circle class="s-red" cx="283" cy="107" r="5" stroke-width="2" fill="none"><animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.5;0.55;0.9;1" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(f'<circle class="f-acc" r="4"><animate attributeName="cx" values="320;320;283;283" keyTimes="0;0.3;0.55;1" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="cy" values="107;107;107;107" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(text(90, 214, 'I_e ≫ I_дырки, донор', 't-s') + text(270, 214, 'I_e ≪ I_дырки, акцептор', 't-s'))
    return ''.join(o)
