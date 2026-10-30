"""Иллюстрации к конспекту по молекулярной физике и термодинамике (стр. m01–m21, h01)."""
import math
import random
from figlib import *  # noqa: F401,F403


def lin(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


def tri_wave(a, b, s0, k, dur):
    """Координата молекулы между стенками a и b: отражения от стенок, k полных проходов «туда-обратно» за dur.
    Возвращает (values, keyTimes) с точными моментами ударов — анимация замкнута по времени."""
    L = b - a
    v = 2 * L * k / dur
    sgn = 1 if k > 0 else -1
    v = abs(v)

    def pos(t):
        s = (s0 + sgn * v * t) % (2 * L)
        return a + (s if s <= L else 2 * L - s)
    ts = [0.0]
    # моменты, когда s проходит через кратные L
    s_start = s0
    s_end = s0 + sgn * v * dur
    lo, hi = sorted((s_start, s_end))
    j = math.floor(lo / L) + 1
    while j * L < hi - 1e-9:
        ts.append(abs(j * L - s0) / v)
        j += 1
    ts.append(dur)
    ts = sorted(set(round(t, 6) for t in ts))
    return [pos(t) for t in ts], [t / dur for t in ts]


def gas(fid, x1, y1, x2, y2, n, kmax, dur, seed, r=4.5, cls='f-acc', hi=None):
    """Хаотично движущиеся молекулы в прямоугольнике (упругие удары о стенки)."""
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        kx = rnd.choice([k for k in range(-kmax, kmax + 1) if k])
        ky = rnd.choice([k for k in range(-kmax, kmax + 1) if k])
        sx = rnd.uniform(0, 2 * (x2 - x1 - 2 * r))
        sy = rnd.uniform(0, 2 * (y2 - y1 - 2 * r))
        xv, xk = tri_wave(x1 + r, x2 - r, sx, kx, dur)
        yv, yk = tri_wave(y1 + r, y2 - r, sy, ky, dur)
        c = cls if (hi is None or i != hi) else 'f-red'
        out.append(f'<circle class="{c}" r="{r}">'
                   f'<animate attributeName="cx" values="{nums(xv)}" keyTimes="{";".join(f(k) if 0 < k < 1 else str(int(k)) for k in xk)}" dur="{dur}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="cy" values="{nums(yv)}" keyTimes="{";".join(f(k) if 0 < k < 1 else str(int(k)) for k in yk)}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    return ''.join(out)


def axes(x0, y0, x1, y1, xl, yl):
    return (arrow(x0, y0, x1, y0, 's-ink', 'f-ink', 1.4, 6) + arrow(x0, y0, x0, y1, 's-ink', 'f-ink', 1.4, 6)
            + text(x0 + 10, y1 + 10, yl, 't', 'start') + text(x1 - 2, y0 + 18, xl, 't', 'end'))


def thermometer(x, y, h, levels, dur, cls='f-red', keytimes=None):
    """Термометр: колонка высотой levels (доли 0…1)."""
    kt = keytimes or times(len(levels))
    hs = [h * v for v in levels]
    return (f'<rect class="f-paper s-ink" x="{x - 5}" y="{y - h}" width="10" height="{h}" rx="5" stroke-width="1.6"/>'
            f'<circle class="{cls}" cx="{x}" cy="{y + 6}" r="8"/>'
            f'<rect class="{cls}" x="{x - 2.5}" width="5"><animate attributeName="height" values="{nums(hs)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{nums([y - v for v in hs])}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></rect>')


def flame(x, y, dur, on_kt=None):
    """Пламя горелки; on_kt — (values, keyTimes) для opacity."""
    op = ''
    if on_kt:
        op = f'<animate attributeName="opacity" values="{on_kt[0]}" keyTimes="{on_kt[1]}" dur="{dur}s" repeatCount="indefinite"/>'
    return (f'<g>{op}<path class="f-red" d="M{x - 12},{y}C{x - 14},{y - 14} {x - 4},{y - 18} {x},{y - 30}C{x + 4},{y - 18} {x + 14},{y - 14} {x + 12},{y}Z">'
            f'<animateTransform attributeName="transform" type="scale" values="1 1;1 0.85;1 1.05;1 1" dur="0.6s" repeatCount="indefinite" additive="sum"/></path></g>'
            f'<rect class="f-mute" x="{x - 16}" y="{y}" width="32" height="8" rx="2"/>')


def dots_in(x_left, xs0, ys, scales, dur, r=3, cls='f-acc'):
    """Молекулы газа под поршнем: координата x растягивается вместе с объёмом."""
    out = []
    for x, y in zip(xs0, ys):
        out.append(f'<circle class="{cls}" cy="{f(y)}" r="{r}">{anim("cx", nums([x_left + (x - x_left) * s for s in scales]), dur)}</circle>')
    return ''.join(out)


# ───────────────────────────── МКТ ─────────────────────────────

@fig('gas-box', 'Идеальный газ: молекулы беспрерывно и хаотично движутся, ударяются о стенки сосуда чаще, чем друг о друга', 360, 210)
def gas_box():
    dur = 12
    o = ['<rect class="f-paper s-ink" x="20" y="20" width="200" height="170" stroke-width="3"/>']
    o.append(gas('gas-box', 22, 22, 218, 188, 16, 3, dur, 7, hi=0))
    o.append(text(232, 50, 'движение', 't-s', 'start') + text(232, 66, 'беспрерывное', 't-s', 'start') + text(232, 82, 'и хаотичное', 't-s', 'start'))
    o.append('<circle class="f-red" cx="238" cy="112" r="4.5"/>' + text(248, 116, '— одна молекула', 't-s', 'start'))
    o.append(text(232, 150, 'удары о стенки', 't-s', 'start') + text(232, 166, 'создают давление', 't-s', 'start'))
    return ''.join(o)


@fig('temp-speed', 'Температура — мера средней кинетической энергии: в более горячем газе молекулы движутся быстрее', 360, 200)
def temp_speed():
    dur = 12
    o = []
    for x, k, cls, lab in [(20, 1, 'f-acc', 'T₁ — холоднее'), (190, 3, 'f-red', 'T₂ > T₁ — горячее')]:
        o.append(f'<rect class="f-paper s-ink" x="{x}" y="20" width="150" height="140" stroke-width="2.6"/>')
        o.append(gas('temp-speed', x + 2, 22, x + 148, 158, 11, k, dur, 11 + k, cls=cls))
        o.append(text(x + 75, 184, lab, 't'))
    return ''.join(o)


# ───────────────────────────── изопроцессы ─────────────────────────────

def cylinder_h(x0, y0, h, xp, dur, vals_xp=None):
    """Горизонтальный цилиндр с поршнем; vals_xp — положения поршня (анимация)."""
    a = ''
    if vals_xp:
        a = f'<animateTransform attributeName="transform" type="translate" values="{";".join(f"{f(v - xp)} 0" for v in vals_xp)}" keyTimes="{times(len(vals_xp))}" dur="{dur}s" repeatCount="indefinite"/>'
    return (f'<path class="s-ink" d="M{x0 + 160},{y0}H{x0}V{y0 + h}H{x0 + 160}" stroke-width="3" fill="none"/>'
            f'<g>{a}<rect class="f-ink" x="{xp}" y="{y0 + 2}" width="9" height="{h - 4}" rx="1"/><path class="s-ink" d="M{xp + 9},{y0 + h / 2}H{xp + 44}" stroke-width="4"/></g>')


@fig('isotherm', 'Изотермический процесс (T = const): при уменьшении объёма давление растёт, при увеличении — падает; график p(V) — гипербола', 360, 220)
def isotherm():
    dur, n = 8, 41
    us = lin(0, 1, n)
    V = [2 + math.cos(2 * math.pi * u) for u in us]  # 3 → 1 → 3
    P = [3 / v for v in V]
    x0, y0, h = 20, 60, 80
    xp = [x0 + 2 + 48 * v for v in V]
    o = [f'<rect class="f-soft" x="{x0 + 2}" y="{y0 + 2}" height="{h - 4}">{anim("width", nums([x - x0 - 2 for x in xp]), dur)}</rect>']
    rnd = random.Random(3)
    pts = [(rnd.uniform(x0 + 6, x0 + 140), rnd.uniform(y0 + 8, y0 + h - 8)) for _ in range(16)]
    o.append(dots_in(x0 + 2, [p[0] for p in pts], [p[1] for p in pts], [v / 3 for v in V], dur))
    o.append(cylinder_h(x0, y0, h, xp[0], dur, xp))
    o.append(text(90, y0 - 14, 'T = const', 't-s'))
    # манометр-столбик
    o.append('<rect class="s-mute" x="20" y="166" width="140" height="14" stroke-width="1" stroke-dasharray="3 3"/>')
    o.append(f'<rect class="f-red" x="20" y="166" height="14">{anim("width", nums([140 * p / 3 for p in P]), dur)}</rect>')
    o.append(text(90, 198, 'давление p', 't-s'))
    # график p(V)
    gx, gy, sx, sy = 206, 196, 40, 48
    o.append(axes(gx, gy, 350, 24, 'V', 'p'))
    curve = 'L'.join(f'{f(gx + sx * v)},{f(gy - sy * 3 / v)}' for v in lin(0.9, 3.4, 40))
    o.append(f'<path class="s-acc" d="M{curve}" stroke-width="2.4"/>')
    o.append(f'<circle class="f-red" r="6">{anims(dur, cx=[gx + sx * v for v in V], cy=[gy - sy * p for p in P])}</circle>')
    o.append(text(294, 100, 'изотерма', 't-acc', 'start'))
    return ''.join(o)


@fig('isobar', 'Изобарный процесс (p = const): при нагревании объём газа растёт пропорционально температуре; график V(T) — прямая через начало координат', 360, 220)
def isobar():
    dur, n = 8, 41
    us = lin(0, 1, n)
    T = [1.5 - 0.5 * math.cos(2 * math.pi * u) for u in us]  # 1 → 2 → 1
    V = T
    bx, by, w = 40, 176, 80   # дно цилиндра
    yp = [by - 44 * v for v in V]
    o = [f'<rect class="f-soft" x="{bx + 2}" width="{w - 4}">{anim("y", nums(yp), dur)}{anim("height", nums([by - y for y in yp]), dur)}</rect>']
    rnd = random.Random(5)
    pts = [(rnd.uniform(bx + 8, bx + w - 8), rnd.uniform(6, 40)) for _ in range(12)]
    for x, d in pts:
        o.append(f'<circle class="f-acc" cx="{f(x)}" r="3">{anim("cy", nums([by - d * v for v in V]), dur)}</circle>')
    o.append(f'<path class="s-ink" d="M{bx},20V{by}H{bx + w}V20" stroke-width="3" fill="none"/>')
    o.append(f'<g>{move([(0, y - yp[0]) for y in yp], dur)}<rect class="f-ink" x="{bx + 2}" y="{yp[0] - 9}" width="{w - 4}" height="9"/>'
             f'<rect class="f-mute" x="{bx + 22}" y="{yp[0] - 31}" width="36" height="22" rx="2"/>{text(bx + 40, yp[0] - 15, "груз", "t-w")}</g>')
    heat = ';'.join('1' if 0 <= u < 0.5 else '0' for u in us)
    o.append(flame(bx + w / 2, by + 30, dur, (heat, times(n))))
    o.append(text(bx + w / 2, 14, 'p = const', 't-s'))
    o.append(thermometer(150, 150, 110, [(t - 0.8) / 1.4 for t in T], dur))
    gx, gy, sx, sy = 196, 196, 64, 70
    o.append(axes(gx, gy, 350, 24, 'T', 'V'))
    o.append(f'<path class="s-mute" d="M{gx},{gy}L{f(gx + sx * 0.9)},{f(gy - sy * 0.9)}" stroke-width="1.4" stroke-dasharray="4 4"/>')
    o.append(f'<path class="s-acc" d="M{f(gx + sx * 0.9)},{f(gy - sy * 0.9)}L{f(gx + sx * 2.2)},{f(gy - sy * 2.2)}" stroke-width="2.4"/>')
    o.append(f'<circle class="f-red" r="6">{anims(dur, cx=[gx + sx * t for t in T], cy=[gy - sy * v for v in V])}</circle>')
    o.append(text(346, 120, 'изобара', 't-acc', 'end'))
    return ''.join(o)


@fig('isochor', 'Изохорный процесс (V = const): в закрытом сосуде при нагревании давление растёт пропорционально температуре; график p(T) — прямая через начало координат', 360, 220)
def isochor():
    dur, n = 8, 41
    us = lin(0, 1, n)
    T = [1.5 - 0.5 * math.cos(2 * math.pi * u) for u in us]
    P = T
    o = ['<rect class="f-soft s-ink" x="30" y="60" width="100" height="100" rx="6" stroke-width="3"/>']
    o.append(gas('isochor', 34, 64, 126, 156, 9, 2, dur, 21, r=3.5))
    # манометр
    cx, cy = 80, 28
    o.append(f'<path class="s-ink" d="M80,60V44" stroke-width="3"/><circle class="f-paper s-ink" cx="{cx}" cy="{cy}" r="18" stroke-width="2"/>')
    angs = [-120 + 120 * (p - 0.8) / 1.4 * 2 for p in P]
    o.append(f'<g>{rot(angs, cx, cy, dur)}<line class="s-red" x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - 14}" stroke-width="2.4"/></g><circle class="f-ink" cx="{cx}" cy="{cy}" r="2.5"/>')
    heat = ';'.join('1' if 0 <= u < 0.5 else '0' for u in us)
    o.append(flame(80, 196, dur, (heat, times(n))))
    o.append(text(80, 214, 'V = const', 't-s'))
    o.append(thermometer(156, 150, 110, [(t - 0.8) / 1.4 for t in T], dur))
    gx, gy, sx, sy = 196, 196, 64, 70
    o.append(axes(gx, gy, 350, 24, 'T', 'p'))
    o.append(f'<path class="s-mute" d="M{gx},{gy}L{f(gx + sx * 0.9)},{f(gy - sy * 0.9)}" stroke-width="1.4" stroke-dasharray="4 4"/>')
    o.append(f'<path class="s-acc" d="M{f(gx + sx * 0.9)},{f(gy - sy * 0.9)}L{f(gx + sx * 2.2)},{f(gy - sy * 2.2)}" stroke-width="2.4"/>')
    o.append(f'<circle class="f-red" r="6">{anims(dur, cx=[gx + sx * t for t in T], cy=[gy - sy * p for p in P])}</circle>')
    o.append(text(346, 120, 'изохора', 't-acc', 'end'))
    return ''.join(o)


# ───────────────────────────── термодинамика ─────────────────────────────

@fig('gas-work', 'Работа газа: при расширении от V₁ до V₂ работа равна площади фигуры под графиком p(V); при расширении A > 0', 360, 220)
def gas_work():
    dur, n = 7, 41
    gx, gy, sx, sy = 40, 196, 70, 50
    V1, V2 = 1.0, 3.6
    p = lambda v: 3.2 - 0.55 * v
    us = lin(0, 1, n)
    kt = [0.65 * u for u in us] + [1]
    V = [V1 + (V2 - V1) * u for u in us] + [V2]
    ktv = ';'.join(f(k) for k in kt)
    o = [f'<clipPath id="gas-work-clip"><rect x="{gx + sx * V1}" y="0" height="220"><animate attributeName="width" values="{nums([sx * (v - V1) for v in V])}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite"/></rect></clipPath>']
    area = f'M{f(gx + sx * V1)},{gy}L{f(gx + sx * V1)},{f(gy - sy * p(V1))}L{f(gx + sx * V2)},{f(gy - sy * p(V2))}L{f(gx + sx * V2)},{gy}Z'
    o.append(f'<path class="f-soft" d="{area}" clip-path="url(#gas-work-clip)"/>')
    o.append(axes(gx, gy, 350, 20, 'V', 'p'))
    o.append(f'<path class="s-acc" d="M{f(gx + sx * V1)},{f(gy - sy * p(V1))}L{f(gx + sx * V2)},{f(gy - sy * p(V2))}" stroke-width="2.6"/>')
    for v, lab in [(V1, 'V₁'), (V2, 'V₂')]:
        o.append(f'<path class="s-mute" d="M{f(gx + sx * v)},{gy}V{f(gy - sy * p(v))}" stroke-width="1.2" stroke-dasharray="3 4"/>' + text(gx + sx * v, gy + 16, lab, 't-s'))
    o.append(f'<circle class="f-red" r="6"><animate attributeName="cx" values="{nums([gx + sx * v for v in V])}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="cy" values="{nums([gy - sy * p(v) for v in V])}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.3;0.4;1" dur="{dur}s" repeatCount="indefinite"/>'
             + text(gx + sx * (V1 + V2) / 2, gy - 34, 'A = S', 't-acc') + '</g>')
    o.append(text(346, 30, 'расширение: ΔV > 0, A > 0', 't-s', 'end'))
    return ''.join(o)


@fig('first-law', 'Первый закон термодинамики: переданная газу теплота Q идёт на изменение внутренней энергии ΔU и на работу газа A (пример конспекта: 1000 = 600 + 400)', 360, 220)
def first_law():
    dur = 7
    o = [markers('first-law', ('red', 'acc', 'grn'))]
    # цилиндр с поршнем
    x0, y0, h = 120, 60, 80
    kt = '0;0.15;0.6;0.9;1'
    xp = [190, 190, 236, 236, 190]
    o.append(f'<rect class="f-soft" x="{x0 + 2}" y="{y0 + 2}" height="{h - 4}"><animate attributeName="width" values="{nums([x - x0 - 2 for x in xp])}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></rect>')
    o.append(f'<rect class="f-red-soft" x="{x0 + 2}" y="{y0 + 2}" height="{h - 4}" opacity="0"><animate attributeName="width" values="{nums([x - x0 - 2 for x in xp])}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0;0;0.9;0.9;0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></rect>')
    o.append(f'<path class="s-ink" d="M{x0 + 170},{y0}H{x0}V{y0 + h}H{x0 + 170}" stroke-width="3" fill="none"/>')
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(f"{x - xp[0]} 0" for x in xp)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<rect class="f-ink" x="{xp[0]}" y="{y0 + 2}" width="9" height="{h - 4}"/><path class="s-ink" d="M{xp[0] + 9},{y0 + h / 2}H{xp[0] + 40}" stroke-width="4"/>'
             + mline('first-law', xp[0] + 44, y0 + h / 2, xp[0] + 74, y0 + h / 2, 'grn', 2.6) + text(xp[0] + 60, y0 + h / 2 - 10, 'A', 't-grn') + '</g>')
    # теплота
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.12;0.6;0.65;1" dur="{dur}s" repeatCount="indefinite"/>'
             + ''.join(f'<line class="s-red" x1="{x}" y1="{y0 + h + 40}" x2="{x}" y2="{y0 + h + 8}" stroke-width="2.6" marker-end="url(#first-law-m-red)" stroke-dasharray="6 5">{flow(0.5, 11)}</line>' for x in (140, 165, 190))
             + text(214, y0 + h + 34, 'Q', 't-red', 'start') + '</g>')
    o.append(thermometer(60, 170, 100, [0.25, 0.25, 0.75, 0.75, 0.25], dur, keytimes=kt))
    o.append(text(60, 40, 'ΔU', 't-acc'))
    # энергетический баланс
    bx, by = 160, 18
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.55;0.6;0.92;1" dur="{dur}s" repeatCount="indefinite"/>'
             + text(250, by + 4, 'Q = ΔU + A: 1000 = 600 + 400', 't') + '</g>')
    return ''.join(o)


@fig('adiabat', 'Адиабатный процесс (Q = 0): при сжатии температура газа растёт, при расширении падает; адиабата на диаграмме p–V идёт круче изотермы', 360, 220)
def adiabat():
    dur, n = 7, 41
    us = lin(0, 1, n)
    g = 1.4
    V = [2.2 + 1.2 * math.cos(2 * math.pi * u) for u in us]  # 3.4 → 1 → 3.4
    Va = 3.4
    pa = 0.9
    P = [pa * (Va / v) ** g for v in V]
    T = [p * v / (pa * Va) for p, v in zip(P, V)]
    x0, y0, h = 16, 54, 70
    xp = [x0 + 3 + 40 * v for v in V]
    o = [f'<rect class="f-soft" x="{x0 + 3}" y="{y0 + 3}" height="{h - 6}">{anim("width", nums([x - x0 - 3 for x in xp]), dur)}</rect>']
    o.append(f'<rect class="f-red-soft" x="{x0 + 3}" y="{y0 + 3}" height="{h - 6}">{anim("width", nums([x - x0 - 3 for x in xp]), dur)}'
             f'{anim("opacity", nums([min(max((t - 1) / (max(T) - 1), 0), 1) for t in T]), dur)}</rect>')
    o.append(f'<path class="s-ink" d="M{x0 + 160},{y0}H{x0}V{y0 + h}H{x0 + 160}" stroke-width="5" fill="none" stroke-dasharray="2 2"/>'
             f'<path class="s-ink" d="M{x0 + 160},{y0 - 3}H{x0 - 3}V{y0 + h + 3}H{x0 + 160}" stroke-width="1.4" fill="none"/>')
    o.append(f'<g>{move([(x - xp[0], 0) for x in xp], dur)}<rect class="f-ink" x="{xp[0]}" y="{y0 + 3}" width="8" height="{h - 6}"/><path class="s-ink" d="M{xp[0] + 8},{y0 + h / 2}H{xp[0] + 40}" stroke-width="4"/></g>')
    o.append(text(96, y0 - 14, 'теплоизоляция: Q = 0', 't-s'))
    comp = ';'.join('1' if u < 0.5 else '0' for u in us)
    expn = ';'.join('0' if u < 0.5 else '1' for u in us)
    o.append(f'<text class="t-red" x="96" y="160" text-anchor="middle">сжатие: T ↑<animate attributeName="opacity" values="{comp}" keyTimes="{times(n)}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>')
    o.append(f'<text class="t-acc" x="96" y="160" text-anchor="middle" opacity="0">расширение: T ↓<animate attributeName="opacity" values="{expn}" keyTimes="{times(n)}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>')
    o.append(thermometer(96, 206, 26, [0.15 + 0.85 * (t - 1) / (max(T) - 1) for t in T], dur, cls='f-red').replace(f'cx="96" cy="212"', 'cx="96" cy="212"'))
    gx, gy, sx, sy = 196, 200, 40, 30
    o.append(axes(gx, gy, 352, 20, 'V', 'p'))
    vs = lin(0.95, 3.6, 40)
    o.append(f'<path class="s-mute" d="M{"L".join(f"{f(gx + sx * v)},{f(gy - sy * pa * Va / v)}" for v in vs)}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    vs2 = lin(0.98, 3.6, 40)
    o.append(f'<path class="s-red" d="M{"L".join(f"{f(gx + sx * v)},{f(gy - sy * pa * (Va / v) ** g)}" for v in vs2)}" stroke-width="2.4"/>')
    o.append(f'<circle class="f-red" r="6">{anims(dur, cx=[gx + sx * v for v in V], cy=[gy - sy * p for p in P])}</circle>')
    o.append(text(250, 40, 'адиабата', 't-red', 'start') + text(300, 150, 'изотерма', 't-s', 'start'))
    return ''.join(o)


@fig('carnot', 'Цикл Карно: две изотермы и две адиабаты, обход по часовой стрелке; на 1–2 газ получает теплоту Q₁ от нагревателя, на 3–4 отдаёт Q₂ охладителю', 360, 230)
def carnot():
    dur, n = 12, 25
    g = 1.4
    V1, V2, V3 = 1.0, 2.0, 4.0
    V4 = V1 * V3 / V2
    TI = 1.0
    TII = TI * (V2 / V3) ** (g - 1)
    gx, gy, sx, sy = 40, 200, 70, 150

    def P(v, T):
        return T / v
    segs = [
        [(v, P(v, TI)) for v in lin(V1, V2, n)],
        [(v, P(V2, TI) * (V2 / v) ** g) for v in lin(V2, V3, n)],
        [(v, P(v, TII)) for v in lin(V3, V4, n)],
        [(v, P(V4, TII) * (V4 / v) ** g) for v in lin(V4, V1, n)],
    ]
    X = lambda v: gx + sx * v
    Y = lambda p: gy - sy * p
    o = [markers('carnot', ('red', 'acc'))]
    o.append(axes(gx, gy, 350, 22, 'V', 'p'))
    full = []
    for s in segs:
        full += s
    o.append(f'<path class="f-soft" d="M{"L".join(f"{f(X(v))},{f(Y(p))}" for v, p in full)}Z"/>')
    for k, s in enumerate(segs):
        cls = 's-red' if k == 0 else 's-acc' if k == 2 else 's-ink'
        o.append(f'<path class="{cls}" d="M{"L".join(f"{f(X(v))},{f(Y(p))}" for v, p in s)}" stroke-width="2.6" fill="none"/>')
    corners = [(V1, P(V1, TI), '1', -12, -6), (V2, P(V2, TI), '2', 8, -8), (V3, P(V3, TII), '3', 8, 4), (V4, P(V4, TII), '4', -8, 16)]
    for v, p, lab, dx, dy in corners:
        o.append(f'<circle class="f-ink" cx="{f(X(v))}" cy="{f(Y(p))}" r="3.5"/>' + text(X(v) + dx, Y(p) + dy, lab, 't'))
    # движущаяся точка
    kt, xs, ys = [], [], []
    for k, s in enumerate(segs):
        for i, (v, p) in enumerate(s):
            if k and i == 0:
                continue
            kt.append((k + i / (n - 1)) / 4)
            xs.append(X(v)); ys.append(Y(p))
    ktv = ';'.join(f(q) for q in kt)
    o.append(f'<circle class="f-red" r="6.5"><animate attributeName="cx" values="{nums(xs)}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="cy" values="{nums(ys)}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    stages = ['1–2: изотерма T_I, газ получает Q₁', '2–3: адиабата, Q = 0', '3–4: изотерма T_II, газ отдаёт Q₂', '4–1: адиабата, Q = 0']
    for k, lab in enumerate(stages):
        vals = ';'.join('1' if j == k else '0' for j in range(4)) + ';0'
        o.append(f'<text class="t" x="348" y="30" text-anchor="end" opacity="0">{subs(lab)}<animate attributeName="opacity" values="{vals}" keyTimes="0;0.25;0.5;0.75;1" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>')
    # Q1 и Q2
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="1;0;0;0;0" keyTimes="0;0.25;0.5;0.75;1" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>'
             + mline('carnot', X(1.5) + 6, Y(P(1.5, TI)) - 44, X(1.5), Y(P(1.5, TI)) - 8, 'red', 2.6) + text(X(1.5) + 14, Y(P(1.5, TI)) - 34, 'Q₁', 't-red', 'start') + '</g>')
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.25;0.5;0.75;1" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>'
             + mline('carnot', X(3), Y(P(3, TII)) + 8, X(3) + 4, Y(P(3, TII)) + 40, 'acc', 2.6) + text(X(3) + 12, Y(P(3, TII)) + 36, 'Q₂', 't-acc', 'start') + '</g>')
    o.append(text(348, 50, 'A = Q₁ − Q₂ — площадь цикла', 't-s', 'end'))
    return ''.join(o)


@fig('heat-flow', 'Теплообмен: теплота переходит от горячего тела к холодному, пока температуры не станут одинаковыми — термодинамическое равновесие', 360, 210)
def heat_flow():
    dur, n = 8, 41
    us = lin(0, 1, n)
    k = [1 - math.exp(-5 * min(u / 0.8, 1)) for u in us]
    Th = [0.85 - 0.35 * q for q in k]
    Tc = [0.15 + 0.35 * q for q in k]
    o = [markers('heat-flow', ('red',))]
    o.append('<rect class="f-red" x="40" y="110" width="130" height="70" rx="4"/><rect class="f-acc" x="170" y="110" width="130" height="70" rx="4"/>')
    o.append(text(105, 150, 'T₁', 't-w') + text(235, 150, 'T₂', 't-w'))
    o.append(thermometer(105, 96, 70, Th, dur) + thermometer(235, 96, 70, Tc, dur, cls='f-acc'))
    fade = [max(0.0, 1 - q / 0.97) for q in k]
    o.append(f'<g>{anim("opacity", nums(fade), dur)}' + ''.join(
        f'<line class="s-red" x1="{140}" y1="{y}" x2="{208}" y2="{y}" stroke-width="2.6" stroke-dasharray="8 6" marker-end="url(#heat-flow-m-red)">{flow(0.5, 14)}</line>' for y in (130, 160)) + '</g>')
    o.append(f'<text class="t-red" x="170" y="200" text-anchor="middle">теплота: от горячего к холодному<animate attributeName="opacity" values="1;0" keyTimes="0;0.6" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>')
    o.append(f'<text class="t" x="170" y="200" text-anchor="middle" opacity="0">T₁ = T₂ — равновесие<animate attributeName="opacity" values="0;1" keyTimes="0;0.6" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>')
    return ''.join(o)


@fig('mixing', 'Температура смеси: смешали равные массы одной жидкости при 20 °C и 80 °C — температура смеси равна среднему арифметическому, 50 °C', 360, 230)
def mixing():
    dur = 8
    kt = '0;0.1;0.6;0.92;1'
    o = []
    for x, cls, t in [(30, 'f-acc', '20 °C'), (250, 'f-red', '80 °C')]:
        o.append(f'<rect class="{cls}" x="{x + 2}" width="76" opacity="0.75"><animate attributeName="y" values="40;40;100;100;40" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="height" values="60;60;0;0;60" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></rect>')
        o.append(f'<path class="s-ink" d="M{x},20V100H{x + 80}V20" stroke-width="2.4" fill="none"/>')
        xs = x + 80 if x < 100 else x
        o.append(f'<path class="s-ink" d="M{xs},90H{180 - 30 if x < 100 else 180 + 30}" stroke-width="5"/>')
        o.append(text(x + 40, 16, f'm, {t}', 't-s'))
    for side, cls in [(-1, 'f-acc'), (1, 'f-red')]:
        xx = 180 + side * 30
        o.append(f'<rect class="{cls}" x="{xx - 2}" y="92" width="4" height="66" opacity="0"><animate attributeName="opacity" values="0;0.8;0.8;0;0" keyTimes="0;0.1;0.6;0.601;1" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></rect>')
    o.append(f'<rect class="f-acc" x="122" width="116" opacity="0.6"><animate attributeName="y" values="216;216;156;156;216" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="height" values="0;0;60;60;0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></rect>')
    o.append(f'<rect class="f-red" x="122" width="116" opacity="0.45"><animate attributeName="y" values="216;216;156;156;216" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="height" values="0;0;60;60;0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></rect>')
    o.append('<path class="s-ink" d="M120,130V218H240V130" stroke-width="2.4" fill="none"/>')
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.6;0.65;0.92;1" dur="{dur}s" repeatCount="indefinite"/>'
             + text(300, 170, '2m, θ = 50 °C', 't', 'middle') + text(300, 192, 'θ = (t₁ + t₂)/2', 't-s') + '</g>')
    return ''.join(o)


@fig('phase-curve', 'График T(U): лёд нагревается до 0 °C, плавится при постоянной температуре, вода нагревается до 100 °C, кипит при постоянной температуре, затем нагревается пар; при охлаждении — обратные процессы', 360, 220)
def phase_curve():
    dur = 12
    gx, gy = 40, 196
    Y = lambda T: gy - 30 - 1.25 * T    # −20 °C → 196
    pts = [(gx + 4, -20), (78, 0), (128, 0), (196, 100), (296, 100), (334, 120)]
    o = [axes(gx, gy, 352, 14, 'U', 'T')]
    for T, lab in [(0, '0 °C'), (100, '100 °C')]:
        o.append(f'<path class="s-mute" d="M{gx},{f(Y(T))}H350" stroke-width="1" stroke-dasharray="3 4"/>' + text(gx - 4, Y(T) + 4, lab, 't-s', 'end'))
    o.append(f'<path class="s-acc" d="M{"L".join(f"{f(x)},{f(Y(T))}" for x, T in pts)}" stroke-width="2.6" fill="none"/>')
    labs = [(61, -10, 'лёд', 18), (103, 0, '', 0), (162, 50, 'вода', 18), (246, 100, '', 0), (315, 114, 'пар', 18)]
    for x, T, lab, dx in labs:
        if lab:
            o.append(text(x + dx, Y(T) + 4, lab, 't-s', 'start'))
    # точка: вперёд (нагревание) 0–0.48, назад (охлаждение) 0.52–1
    seg_t = [0, 0.06, 0.16, 0.26, 0.42, 0.48]
    kt = seg_t + [0.52 + (0.48 - t) for t in reversed(seg_t)]
    xs = [x for x, _ in pts] + [x for x, _ in reversed(pts)]
    ys = [Y(T) for _, T in pts] + [Y(T) for _, T in reversed(pts)]
    kt[-1] = 1
    ktv = ';'.join(f(q) for q in kt)
    o.append(f'<circle class="f-red" r="6"><animate attributeName="cx" values="{nums(xs)}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="cy" values="{nums(ys)}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    events = [('плавление (таяние)', 124, 0, 0.06, 0.16), ('кипение (испарение)', 246, 100, 0.26, 0.42),
              ('конденсация', 246, 100, 0.58, 0.74), ('затвердевание', 124, 0, 0.84, 0.94)]
    for lab, x, T, a, b in events:
        o.append(f'<text class="t-red" x="{x}" y="{f(Y(T) - 12)}" text-anchor="middle" opacity="0">{lab}<animate attributeName="opacity" values="0;1;0" keyTimes="0;{f(a)};{f(b)}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>')
    o.append(f'<text class="t-s" x="{gx + 8}" y="214" text-anchor="start">нагревание →<animate attributeName="opacity" values="1;0" keyTimes="0;0.5" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>')
    o.append(f'<text class="t-s" x="{gx + 8}" y="214" text-anchor="start" opacity="0">← охлаждение<animate attributeName="opacity" values="0;1" keyTimes="0;0.5" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>')
    return ''.join(o)


# ───────────────────────────── жидкости ─────────────────────────────

@fig('drop', 'Капля на конце трубки: вес капли растёт, сила поверхностного натяжения удерживает её; когда mg ≥ F_повер, капля отрывается', 360, 220)
def drop():
    dur, n = 5, 31
    o = [markers('drop', ('red', 'acc'))]
    tip, Fpov = 70, 48
    o.append(f'<rect class="f-soft" x="114" y="0" width="12" height="{tip}"/><path class="s-ink" d="M112,0V{tip}M128,0V{tip}" stroke-width="2.4"/>')
    grow = lin(0, 1, n)
    kt = [0.65 * g for g in grow] + [0.9, 0.901, 1]
    ktv = ';'.join(f(k) for k in kt)
    R = [3 + 12 * g for g in grow] + [15, 3, 3]
    cy = [tip + r - 2 for r in R[:n]] + [tip + 150, tip + 1, tip + 1]
    spl = ';'.join(['0 0 1 1'] * (n - 1) + ['0.55 0 1 1', '0 0 1 1', '0 0 1 1'])
    o.append(f'<circle class="f-acc" cx="120"><animate attributeName="r" values="{nums(R)}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="cy" values="{nums(cy)}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite" calcMode="spline" keySplines="{spl}"/></circle>')
    hang = f'<animate attributeName="opacity" values="1;0;1" keyTimes="0;0.66;0.9" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>'
    o.append(f'<g>{hang}' + mline('drop', 104, tip + 2, 104, tip - Fpov / 2 - 6, 'red', 2.6) + mline('drop', 136, tip + 2, 136, tip - Fpov / 2 - 6, 'red', 2.6) + '</g>')
    o.append(text(100, 46, 'F_повер', 't-red', 'end'))
    mg = [Fpov * g ** 3 for g in grow] + [Fpov, 0, 0]
    o.append(f'<line class="s-acc" x1="120" x2="120" stroke-width="2.6" marker-end="url(#drop-m-acc)">{hang}'
             f'<animate attributeName="y1" values="{nums([c + r for c, r in zip(cy, R)])}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y2" values="{nums([c + r + 0.1 + m for c, r, m in zip(cy, R, mg)])}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite"/></line>')
    o.append(f'<text class="t-acc" x="128">{hang}<animate attributeName="y" values="{nums([c + r + m / 2 + 10 for c, r, m in zip(cy, R, mg)])}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite"/>mg</text>')
    # сравнение величин
    o.append('<g transform="translate(230,60)">' + text(0, -14, 'сравним:', 't-s', 'start')
             + f'<rect class="f-red" x="0" y="0" width="{Fpov * 2}" height="10"/>' + text(Fpov * 2 + 6, 9, 'F', 't-red', 'start')
             + f'<rect class="f-acc" x="0" y="20" height="10">{hang}<animate attributeName="width" values="{nums([2 * m for m in mg])}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite"/></rect>'
             + text(Fpov * 2 + 6, 29, 'mg', 't-acc', 'start') + '</g>')
    o.append(f'<text class="t-red" x="290" y="130" text-anchor="middle" opacity="0">mg ≥ F_повер — отрыв<animate attributeName="opacity" values="0;1;0" keyTimes="0;0.64;0.9" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>'.replace('F_повер', 'F<tspan baseline-shift="sub" font-size="0.72em">повер</tspan>'))
    o.append(text(290, 200, 'F_повер = σl, l = 2πR', 't-s'))
    return ''.join(o)


@fig('capillary', 'Смачивание: смачивающая жидкость растекается по поверхности, несмачивающая собирается в шарик; в капиллярной трубке смачивающая жидкость поднимается на высоту h, тем большую, чем уже трубка', 360, 236)
def capillary():
    dur = 6
    o = []
    # сосуд и два капилляра (R₁ > R₂ ⇒ h₁ < h₂, h = 2σ/(ρgR))
    o.append('<rect class="f-soft" x="22" y="150" width="176" height="56"/><path class="s-ink" d="M20,110V208H200V110" stroke-width="2.4" fill="none"/><path class="s-acc" d="M22,150H198" stroke-width="2"/>')
    for x, w, h, lab in [(70, 16, 40, 'R₁'), (140, 8, 80, 'R₂')]:
        kt = '0;0.1;0.55;0.92;1'
        top = 150 - h
        o.append(f'<rect class="f-soft" x="{x - w / 2}" width="{w}"><animate attributeName="y" values="150;150;{top};{top};150" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;0.2 0.7 0.4 1;0 0 1 1;0 0 1 1"/>'
                 f'<animate attributeName="height" values="30;30;{30 + h};{30 + h};30" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;0.2 0.7 0.4 1;0 0 1 1;0 0 1 1"/></rect>')
        o.append(f'<path class="s-ink" d="M{x - w / 2 - 1},40V180M{x + w / 2 + 1},40V180" stroke-width="2"/>')
        o.append(text(x, 34, lab, 't-s'))
        o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.5;0.56;0.92;1" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<path class="s-red" d="M{x + w / 2 + 8},150V{top}M{x + w / 2 + 4},150H{x + w / 2 + 12}M{x + w / 2 + 4},{top}H{x + w / 2 + 12}" stroke-width="1.4"/>'
                 + text(x + w / 2 + 16, (150 + top) / 2 + 4, 'h' + ('₁' if lab == 'R₁' else '₂'), 't-red', 'start') + '</g>')
    o.append(text(110, 228, 'h = 2σ/(ρgR): R₁ > R₂ ⇒ h₁ < h₂', 't-s'))
    # капли на поверхности
    o.append('<path class="s-ink" d="M224,110H350" stroke-width="2.4"/><path class="s-ink" d="M224,190H350" stroke-width="2.4"/>')
    o.append('<path class="f-acc" d="M247,110C247,98 266,90 287,90S327,98 327,110Z" opacity="0.85"><animate attributeName="d" values="M267,110C267,86 276,78 287,78S307,86 307,110Z;M267,110C267,86 276,78 287,78S307,86 307,110Z;M235,110C238,102 262,98 287,98S336,102 339,110Z;M235,110C238,102 262,98 287,98S336,102 339,110Z;M267,110C267,86 276,78 287,78S307,86 307,110Z" keyTimes="0;0.15;0.55;0.92;1" dur="6s" repeatCount="indefinite"/></path>')
    o.append(text(287, 132, 'смачивает — растекается', 't-s'))
    o.append('<circle class="f-ink" cx="287" cy="171" r="18" opacity="0.8"/>')
    o.append(text(287, 212, 'не смачивает — шарик', 't-s'))
    return ''.join(o)


@fig('dew-point', 'Точка росы: при охлаждении воздуха масса пара в 1 м³ (ρ) не меняется, а плотность насыщенного пара ρ₀ уменьшается; когда ρ₀ = ρ, относительная влажность 100 % и пар конденсируется в росу', 360, 220)
def dew_point():
    dur, n = 9, 37
    us = lin(0, 1, n)
    kt = [0.7 * u for u in us] + [0.92, 1]
    ktv = ';'.join(f(k) for k in kt)
    rho = 60
    rho0 = [140 - 80 * u for u in us] + [60, 140]
    phi = [rho / r for r in rho0]
    T = [1 - 0.75 * u for u in us] + [0.25, 1]

    def a(attr, v, extra=''):
        return f'<animate attributeName="{attr}" values="{nums(v)}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite"{extra}/>'
    o = []
    o.append(thermometer(40, 176, 130, T, dur, cls='f-red', keytimes=ktv))
    o.append(text(40, 214, 'T ↓', 't-s'))
    base = 180
    o.append(f'<rect class="f-acc" x="90" y="{base - rho}" width="34" height="{rho}"/>' + text(107, base + 18, 'ρ', 't-acc'))
    o.append(f'<rect class="s-red" x="140" width="34" stroke-width="2" fill="none" stroke-dasharray="4 3">{a("y", [base - r for r in rho0])}{a("height", rho0)}</rect>' + text(157, base + 18, 'ρ₀', 't-red'))
    o.append(f'<path class="s-ink" d="M84,{base}H182" stroke-width="1.4"/>')
    o.append(text(134, 30, 'φ = ρ / ρ₀', 't'))
    o.append(f'<rect class="s-mute" x="196" y="40" width="20" height="140" stroke-width="1" stroke-dasharray="3 3"/>')
    o.append(f'<rect class="f-acc" x="196" width="20">{a("y", [base - 140 * p for p in phi])}{a("height", [140 * p for p in phi])}</rect>')
    o.append(text(206, 34, '100 %', 't-s') + text(206, base + 18, 'φ', 't'))
    # лист и капли росы
    o.append('<path class="f-grn" d="M240,180C250,120 310,110 344,104C338,150 300,182 240,180Z" opacity="0.85"/>')
    rnd = random.Random(2)
    for i in range(7):
        x, y = rnd.uniform(262, 330), rnd.uniform(130, 168)
        if (x - 240) * 0.7 + (180 - y) > 90:
            continue
        o.append(f'<circle class="f-acc s-w" cx="{f(x)}" cy="{f(y)}" r="0" stroke-width="1"><animate attributeName="r" values="0;0;{f(rnd.uniform(4.5, 6))};{f(rnd.uniform(4.5, 6))};0" keyTimes="0;0.7;0.78;0.92;1" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(f'<text class="t-acc" x="292" y="212" text-anchor="middle" opacity="0">точка росы: роса<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.7;0.72;0.92;1" dur="{dur}s" repeatCount="indefinite"/></text>')
    return ''.join(o)
