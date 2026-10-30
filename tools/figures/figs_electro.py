"""Иллюстрации к конспекту по магнетизму, колебаниям и переменному току (стр. e01–e28)."""
import math
from figlib import *  # noqa: F401,F403

# ───────────────────────────── электродинамика ─────────────────────────────

@fig('diode', 'Ток в схеме с диодом: при прямом включении ток идёт по обеим ветвям, при обратном — только через 2R', 360, 200)
def diode():
    out = []
    for k, (ox, open_) in enumerate([(4, True), (186, False)]):
        g = [f'<g transform="translate({ox},18)">']
        g.append(text(85, 0, 'диод открыт' if open_ else 'диод закрыт', 't-s'))
        wires = 'M8,80H20V35H150V80H162M20,80V125H150'
        g.append(f'<path class="s-ink" d="{wires}" stroke-width="2"/>')
        if open_:
            g.append(f'<path class="s-acc" d="M8,80H20V35H150V80H162" stroke-width="3" stroke-dasharray="3 9" stroke-linecap="round">{flow(0.8)}</path>')
            g.append(f'<path class="s-acc" d="M20,80V125H150V80" stroke-width="3" stroke-dasharray="3 9" stroke-linecap="round">{flow(0.8)}</path>')
        else:
            g.append(f'<path class="s-acc" d="M162,80H150V125H20V80H8" stroke-width="3" stroke-dasharray="3 9" stroke-linecap="round">{flow(0.8)}</path>')
        # диод ▷| (направлен вправо), резисторы — поверх линий тока
        g.append('<path class="f-paper" d="M42,26h28v18h-28z"/>')
        g.append('<path class="f-ink" d="M46,27L62,35L46,43Z"/><path class="s-ink" d="M63,27V43" stroke-width="2.4"/>')
        g.append('<rect class="f-paper s-ink" x="88" y="28" width="38" height="14" stroke-width="2"/>' + text(107, 40, 'R', 't-s'))
        g.append('<rect class="f-paper s-ink" x="66" y="118" width="40" height="14" stroke-width="2"/>' + text(86, 130, '2R', 't-s'))
        left, right = ('+', '−') if open_ else ('−', '+')
        g.append(text(4, 85, left, 't'))
        g.append(text(167, 85, right, 't'))
        if open_:
            g.append(text(85, 158, 'R<tspan baseline-shift="sub" font-size="9">об</tspan> = 2R/3', 't'))
        else:
            g.append('<path class="s-red" d="M38,22L132,48M132,22L38,48" stroke-width="2"/>')
            g.append(text(85, 64, 'ток не проходит', 't-s'))
            g.append(text(85, 158, 'R<tspan baseline-shift="sub" font-size="9">об</tspan> = 2R', 't'))
        g.append('</g>')
        out.append(''.join(g))
    return ''.join(out)


@fig('mag-bar', 'Поле полосового магнита: замкнутые силовые линии, снаружи — от N к S', 360, 210)
def mag_bar():
    cx, cy = 180, 105
    o = []
    loops = [(60, 28), (95, 52), (130, 80)]
    for i, (dx, hgt) in enumerate(loops):
        for sgn in (-1, 1):
            y0 = cy + sgn * 9
            d = f'M{cx+62},{y0}C{cx+62+dx*0.35},{y0+sgn*hgt*1.25} {cx-62-dx*0.35},{y0+sgn*hgt*1.25} {cx-62},{y0}'
            o.append(f'<path class="s-mute" d="{d}" stroke-width="1.6"/>')
            o.append(f'<path class="s-acc" d="{d}" stroke-width="2.2" stroke-dasharray="4 10" stroke-linecap="round">{flow(1.1 + i * 0.25, 14)}</path>')
            ytop = y0 + sgn * hgt * 0.94
            o.append(head(cx - 4, ytop, 180, 'f-acc', 7))
    o.append(poles(cx - 64, cy - 11, 64, 22, 'S', 'f-red'))
    o.append(poles(cx, cy - 11, 64, 22, 'N', 'f-acc'))
    o.append(text(cx, 204, 'снаружи магнита линии идут от N к S и замыкаются внутри', 't-s'))
    return ''.join(o)


@fig('mag-wire', 'Правило буравчика: ток от нас — линии по часовой стрелке, ток к нам — против часовой', 360, 210)
def mag_wire():
    o = []
    for cx, clockwise, sym, cap in [(92, True, 'x', 'ток от нас ⊗ — по часовой'), (268, False, 'o', 'ток к нам ⊙ — против часовой')]:
        cy = 95
        for i, r in enumerate([26, 46, 66]):
            sw = 1 if clockwise else 0
            d = f'M{cx},{cy-r}A{r},{r} 0 1 {sw} {cx},{cy+r}A{r},{r} 0 1 {sw} {cx},{cy-r}'
            o.append(f'<path class="s-mute" d="{d}" stroke-width="1.4"/>')
            o.append(f'<path class="s-acc" d="{d}" stroke-width="2.4" stroke-dasharray="5 11" stroke-linecap="round">{flow(1.6 + i * 0.5, 16)}</path>')
        ang = 360 if clockwise else -360
        o.append(f'<g>{head(cx + 8 if clockwise else cx - 8, cy - 46, 0 if clockwise else 180, "f-acc", 9)}'
                 f'<animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};{ang} {cx} {cy}" dur="4.2s" repeatCount="indefinite"/></g>')
        o.append(cross_sym(cx, cy, 10) if sym == 'x' else dot_sym(cx, cy, 10))
        o.append(text(cx, 196, cap, 't-s'))
    return ''.join(o)


@fig('mag-parallel', 'Параллельные токи: одинаково направленные притягиваются, противоположные — отталкиваются', 360, 210)
def mag_parallel():
    o = []
    for ox, same in [(0, True), (180, False)]:
        g = [f'<g transform="translate({ox},0)">']
        dirs = [(-1, -1), (-1, 1)][0 if same else 1]
        shift = [0, -9, 0] if same else [0, 9, 0]
        for k, (x0, d) in enumerate([(60, dirs[0]), (120, dirs[1])]):
            sgn = 1 if k == 0 else -1
            mv = ';'.join(f'{f(sgn * -s)} 0' for s in shift)
            y1, y2 = (170, 30) if d < 0 else (30, 170)
            path = f'M{x0},{y1}V{y2}'
            cls = 's-acc' if k == 0 else 's-red'
            fl = 'f-acc' if k == 0 else 'f-red'
            g.append(f'<g><animateTransform attributeName="transform" type="translate" values="{mv}" keyTimes="0;0.5;1" dur="2.4s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>')
            g.append(f'<path class="s-ink" d="{path}" stroke-width="3"/>')
            g.append(f'<path class="{cls}" d="{path}" stroke-width="3" stroke-dasharray="4 9" stroke-linecap="round">{flow(0.7, 13)}</path>')
            g.append(head(x0, y2 - 2 if d < 0 else y2 + 2, -90 if d < 0 else 90, fl, 10))
            g.append(text(x0 + (-14 if k == 0 else 16), 42, f'I<tspan baseline-shift="sub" font-size="9">{k+1}</tspan>', 't'))
            fx = (x0 + 22) if (same == (k == 0)) else (x0 - 22)
            g.append(arrow(x0 + (6 if fx > x0 else -6), 100, fx, 100, 's-red', 'f-red', 2.4, 8))
            g.append('</g>')
        g.append(text(90, 200, 'притягиваются' if same else 'отталкиваются', 't'))
        g.append('</g>')
        o.append(''.join(g))
    o.append('<path class="s-mute" d="M180,20V180" stroke-width="1" stroke-dasharray="3 4"/>')
    return ''.join(o)


@fig('ampere', 'Сила Ампера: проводник с током к нам между полюсами S и N выталкивается вниз', 360, 220)
def ampere():
    o = [poles(14, 40, 58, 120, 'S', 'f-red'), poles(288, 40, 58, 120, 'N', 'f-acc')]
    for y in (60, 85, 110, 135):
        o.append(f'<path class="s-mute" d="M286,{y}H74" stroke-width="1.6"/>')
        o.append(f'<path class="s-acc" d="M286,{y}H74" stroke-width="2" stroke-dasharray="4 12">{flow(1.4, 16)}</path>')
        o.append(head(86, y, 180, 'f-acc', 7))
    o.append(text(250, 52, 'B', 't-acc'))
    path = [(0, -46), (0, 46)]
    ease = ' calcMode="spline" keySplines="0.5 0 0.9 0.6"'
    o.append(f'<g>{move(path, 2.6, ease)}'
             f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.12;0.85;1" dur="2.6s" repeatCount="indefinite"/>'
             f'{dot_sym(180, 98, 12)}' + arrow(180, 114, 180, 152, 's-red', 'f-red', 3, 10) + text(198, 146, 'F<tspan baseline-shift="sub" font-size="9">A</tspan>', 't-red', 'start') + '</g>')
    o.append(text(180, 208, 'ток ⊙ к нам, поле к S — сила Ампера вниз', 't-s'))
    return ''.join(o)


@fig('frame', 'Рамка с током в магнитном поле: силы Ампера на сторонах противоположны и поворачивают рамку', 360, 220)
def frame():
    o = [poles(6, 52, 36, 100, 'N', 'f-acc'), poles(150, 52, 36, 100, 'S', 'f-red')]
    for y in (68, 92, 116, 140):
        o.append(f'<path class="s-mute" d="M44,{y}H148" stroke-width="1.2"/>' + head(146, y, 0, 'f-mute', 6))
    loop = 'M96,170V40H130V170'
    o.append(f'<path class="s-ink" d="M62,170V40H130V170" stroke-width="2.4" fill="none"/>')
    o.append(f'<path class="s-acc" d="M62,170V40H130V170" stroke-width="2.6" stroke-dasharray="4 9" stroke-linecap="round" fill="none">{flow(0.9, 13)}</path>')
    o.append(text(58, 190, '+', 't') + text(134, 190, '−', 't'))
    o.append(f'<g>{cross_sym(62, 100, 8, "s-red")}<animate attributeName="opacity" values="1;0.35;1" dur="1.6s" repeatCount="indefinite"/></g>')
    o.append(f'<g>{dot_sym(130, 100, 8, "s-red", "f-red")}<animate attributeName="opacity" values="1;0.35;1" dur="1.6s" repeatCount="indefinite"/></g>')
    o.append(text(96, 210, 'вид спереди', 't-s'))
    # вид сверху: рамка — отрезок, силы вдоль ±z (на экране — вверх/вниз)
    cx, cy, a = 282, 104, 46
    o.append('<path class="s-mute" d="M204,104H352" stroke-width="1" stroke-dasharray="3 4"/>' + head(352, 104, 0, 'f-mute', 6) + text(344, 96, 'B', 't-s'))
    angs = [0, 0, 90, 90, 0]
    kt = '0;0.12;0.6;0.82;1'
    g = (f'<g><animateTransform attributeName="transform" type="rotate" values="{";".join(f"{x} {cx} {cy}" for x in angs)}" keyTimes="{kt}" dur="5s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;0.3 0 0.4 1;0 0 1 1;0.5 0 0.5 1"/>'
         f'<line class="s-ink" x1="{cx-a}" y1="{cy}" x2="{cx+a}" y2="{cy}" stroke-width="5" stroke-linecap="round"/>')
    for ex, up in [(cx - a, True), (cx + a, False)]:
        counter = ';'.join(f'{-x} {ex} {cy}' for x in angs)
        g += (f'<g><animateTransform attributeName="transform" type="rotate" values="{counter}" keyTimes="{kt}" dur="5s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;0.3 0 0.4 1;0 0 1 1;0.5 0 0.5 1"/>'
              + arrow(ex, cy, ex, cy - 34 if up else cy + 34, 's-red', 'f-red', 2.6, 8) + '</g>')
    g += '</g>'
    o.append(g)
    o.append(f'<circle class="f-ink" cx="{cx}" cy="{cy}" r="3"/>')
    o.append(text(282, 210, 'вид сверху', 't-s'))
    return ''.join(o)


@fig('lorentz-circle', 'Частица в магнитном поле, перпендикулярном скорости: сила Лоренца направлена к центру, частица движется по окружности', 360, 220)
def lorentz_circle():
    o = []
    for i in range(7):
        for j in range(4):
            x, y = 30 + i * 50, 30 + j * 52
            d = 4
            o.append(f'<path class="s-mute" d="M{x-d},{y-d}L{x+d},{y+d}M{x+d},{y-d}L{x-d},{y+d}" stroke-width="1.3"/>')
    cx, cy, r = 180, 108, 64
    o.append(f'<circle class="s-mute" cx="{cx}" cy="{cy}" r="{r}" stroke-width="1.6" stroke-dasharray="4 5"/>')
    o.append(f'<circle class="f-ink" cx="{cx}" cy="{cy}" r="2.5"/>')
    g = (f'<g><animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};360 {cx} {cy}" dur="5s" repeatCount="indefinite"/>'
         f'<line class="s-mute" x1="{cx}" y1="{cy}" x2="{cx-r}" y2="{cy}" stroke-width="1.2"/>'
         + arrow(cx - r, cy, cx - r, cy - 44, 's-acc', 'f-acc', 2.6, 9)
         + arrow(cx - r + 10, cy, cx - r + 42, cy, 's-red', 'f-red', 2.6, 9)
         + f'<g><animateTransform attributeName="transform" type="rotate" values="0 {cx-r} {cy};-360 {cx-r} {cy}" dur="5s" repeatCount="indefinite"/>'
         + f'<circle class="f-paper s-ink" cx="{cx-r}" cy="{cy}" r="9" stroke-width="2"/><path class="s-ink" d="M{cx-r-5},{cy}H{cx-r+5}" stroke-width="2"/></g></g>')
    o.append(g)
    o.append(text(18, 214, 'поле ⊗', 't-s', 'start'))
    o.append('<g transform="translate(250,200)">' + arrow(0, 0, 22, 0, 's-acc', 'f-acc', 2.4, 7) + text(28, 5, 'υ', 't-acc', 'start') + arrow(48, 0, 70, 0, 's-red', 'f-red', 2.4, 7) + text(76, 5, 'F<tspan baseline-shift="sub" font-size="9">л</tspan>', 't-red', 'start') + '</g>')
    return ''.join(o)


@fig('spiral', 'Частица влетает под углом к линиям поля и движется по спирали с шагом d', 360, 200)
def spiral():
    o = [poles(4, 40, 40, 110, 'N', 'f-acc'), poles(316, 40, 40, 110, 'S', 'f-red')]
    for y in (55, 95, 135):
        o.append(f'<path class="s-mute" d="M46,{y}H314" stroke-width="1.2"/>' + head(312, y, 0, 'f-mute', 6))
    pts = []
    turns, step, r, tilt = 4.6, 50, 26, 0.75
    n = 260
    for i in range(n + 1):
        th = turns * 2 * math.pi * i / n
        x = 62 + step * th / (2 * math.pi) + tilt * r * math.sin(th)
        y = 95 + r * math.cos(th + math.pi)
        pts.append(f'{f(x)},{f(y)}')
    d = 'M' + 'L'.join(pts)
    o.append(f'<path id="spiral-path" class="s-mute" d="{d}" stroke-width="1.2" stroke-dasharray="2 4"/>')
    o.append(f'<path class="s-acc" d="{d}" stroke-width="2.4" pathLength="100" stroke-dasharray="100" stroke-linecap="round">'
             f'<animate attributeName="stroke-dashoffset" values="100;0;0" keyTimes="0;0.85;1" dur="6s" repeatCount="indefinite"/></path>')
    o.append('<g><circle class="f-red" r="6"/><path class="s-w" d="M-3.5,0H3.5M0,-3.5V3.5" stroke-width="1.6"/>'
             '<animateMotion dur="6s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.85;1" calcMode="linear"><mpath href="#spiral-path"/></animateMotion></g>')
    x1 = 62 + step * 2 + 0.0
    o.append(f'<path class="s-red" d="M{f(x1)},176V184H{f(x1+step)}V176" stroke-width="1.6"/>' + text(x1 + step / 2, 197, 'd — шаг спирали', 't-s'))
    return ''.join(o)


# ───────────────────────────── колебания и волны ─────────────────────────────

def pend_angles(n=41, amp=22):
    """Угол маятника по закону x = A cos ωt (отвели и отпустили)."""
    return sample(lambda u: amp * math.cos(2 * math.pi * u), n)


@fig('pendulum', 'Математический маятник: колебания между крайними точками A около точки равновесия O', 360, 220)
def pendulum():
    px, py, L = 180, 22, 150
    o = [f'<path class="s-ink" d="M120,{py}H240" stroke-width="2"/>']
    o.append(''.join(f'<path class="s-mute" d="M{x},{py}l-6,-8" stroke-width="1.2"/>' for x in range(126, 241, 12)))
    for a in (22, -22):
        x = px + L * math.sin(math.radians(a))
        y = py + L * math.cos(math.radians(a))
        o.append(f'<line class="s-mute" x1="{px}" y1="{py}" x2="{f(x)}" y2="{f(y)}" stroke-width="1" stroke-dasharray="3 4"/>'
                 f'<circle class="s-mute" cx="{f(x)}" cy="{f(y)}" r="11" stroke-width="1.2" stroke-dasharray="3 3"/>'
                 + text(x + (24 if a > 0 else -24), y + 4, 'A', 't-red') + text(x, y + 28, 'υ = 0', 't-s'))
    o.append(f'<line class="s-mute" x1="{px}" y1="{py}" x2="{px}" y2="{py+L+16}" stroke-width="1" stroke-dasharray="2 4"/>' + text(px, py + L + 32, 'O', 't'))
    ang = pend_angles()
    o.append(f'<g>{rot(ang, px, py, 2.4)}<line class="s-ink" x1="{px}" y1="{py}" x2="{px}" y2="{py+L}" stroke-width="2"/>'
             f'<circle class="f-ink" cx="{px}" cy="{py+L}" r="11"/></g>')
    return ''.join(o)


@fig('pend-energy', 'Энергия колебаний маятника: в крайней точке максимальна потенциальная, в точке равновесия — кинетическая', 360, 220)
def pend_energy():
    px, py, L = 120, 22, 150
    o = [f'<path class="s-ink" d="M70,{py}H170" stroke-width="2"/>']
    n = 41
    ang = pend_angles(n)
    o.append(f'<g>{rot(ang, px, py, 3)}<line class="s-ink" x1="{px}" y1="{py}" x2="{px}" y2="{py+L}" stroke-width="2"/><circle class="f-ink" cx="{px}" cy="{py+L}" r="11"/></g>')
    o.append(text(px, py + L + 30, 'O', 't'))
    base, hmax = 186, 140
    ep = sample(lambda u: math.cos(2 * math.pi * u) ** 2, n)
    ek = [1 - v for v in ep]
    for x, series, cls, lab in [(250, ek, 'f-acc', 'E<tspan baseline-shift="sub" font-size="9">к</tspan>'), (305, ep, 'f-red', 'E<tspan baseline-shift="sub" font-size="9">п</tspan>')]:
        o.append(f'<rect class="s-mute" x="{x-16}" y="{base-hmax}" width="32" height="{hmax}" stroke-width="1" stroke-dasharray="3 3"/>')
        ys = nums([base - hmax * v for v in series])
        hs = nums([hmax * v for v in series])
        o.append(f'<rect class="{cls}" x="{x-16}" width="32" rx="3">{anim("y", ys, 3)}{anim("height", hs, 3)}</rect>')
        o.append(text(x, base + 20, lab, 't'))
    o.append(text(277, 30, 'E = const', 't-s'))
    return ''.join(o)


@fig('spring', 'Пружинный маятник: брусок колеблется между крайними положениями A', 360, 180)
def spring():
    wall, rest, amp = 30, 210, 60
    o = [f'<path class="s-ink" d="M{wall},30V130H340" stroke-width="2.2"/>']
    o.append(''.join(f'<path class="s-mute" d="M{wall},{y}l-9,9" stroke-width="1.2"/>' for y in range(36, 130, 12)))
    o.append(''.join(f'<path class="s-mute" d="M{x},130l-8,9" stroke-width="1.2"/>' for x in range(46, 340, 14)))
    n = 41
    xs = sample(lambda u: amp * math.cos(2 * math.pi * u), n)
    coils = 12
    pts = [f'M{wall},100']
    seglen = (rest - 22 - wall) / (coils + 1)
    for i in range(coils):
        pts.append(f'L{f(wall + seglen * (i + 1))},{88 if i % 2 == 0 else 112}')
    pts.append(f'L{rest-22},100')
    scale = ';'.join(f'{f((rest - 22 - wall + x) / (rest - 22 - wall))} 1' for x in xs)
    o.append(f'<g transform="translate({wall},0)"><g><animateTransform attributeName="transform" type="scale" values="{scale}" keyTimes="{times(n)}" dur="2.4s" repeatCount="indefinite"/>'
             f'<g transform="translate({-wall},0)"><path class="s-acc" d="{"".join(pts)}" stroke-width="2.2" fill="none" vector-effect="non-scaling-stroke"/></g></g></g>')
    o.append(f'<g>{move([(x, 0) for x in xs], 2.4)}<rect class="f-soft s-ink" x="{rest-22}" y="78" width="44" height="44" rx="3" stroke-width="2"/></g>')
    for x, lab in [(rest - amp, 'A'), (rest, 'O'), (rest + amp, 'A')]:
        o.append(f'<path class="s-mute" d="M{x},60V140" stroke-width="1" stroke-dasharray="3 4"/>' + text(x, 160, lab, 't-red' if lab == 'A' else 't'))
    return ''.join(o)


@fig('osc-graph', 'График колебаний x = A cos ωt: точка повторяет движение тела, T — период', 360, 200)
def osc_graph():
    x0, x1, y0, A = 70, 345, 100, 58
    per = (x1 - x0) / 2.5
    pts = [f'{f(x0 + i)},{f(y0 - A * math.cos(2 * math.pi * i / per))}' for i in range(0, int(x1 - x0) + 1, 3)]
    o = [arrow(x0, 176, x0, 18, 's-ink', 'f-ink', 1.6, 7), arrow(x0, y0, 352, y0, 's-ink', 'f-ink', 1.6, 7),
         text(x0 - 10, 26, 'x', 't'), text(348, y0 + 18, 't', 't')]
    o.append(f'<path class="s-acc" d="M{"L".join(pts)}" stroke-width="2.4" fill="none"/>')
    o.append(f'<path class="s-red" d="M{x0},{y0-A-12}V{y0-A-18}H{f(x0+per)}V{y0-A-12}" stroke-width="1.6"/>' + text(x0 + per / 2, y0 - A - 22, 'T', 't-red'))
    o.append(text(x0 - 10, y0 - A + 4, 'A', 't-s', 'end') + text(x0 - 10, y0 + A + 4, '−A', 't-s', 'end'))
    dur, n = 5, 61
    ys = sample(lambda u: y0 - A * math.cos(2 * math.pi * 2.5 * u), n)
    o.append(f'<line class="s-mute" y1="18" y2="176" stroke-width="1" stroke-dasharray="3 4"><animate attributeName="x1" values="{x0};{x1}" dur="{dur}s" repeatCount="indefinite"/><animate attributeName="x2" values="{x0};{x1}" dur="{dur}s" repeatCount="indefinite"/></line>')
    o.append(f'<circle class="f-red" r="6"><animate attributeName="cx" values="{x0};{x1}" dur="{dur}s" repeatCount="indefinite"/>{anim("cy", nums(ys), dur)}</circle>')
    # тело на пружине слева — то же движение
    o.append(f'<path class="s-mute" d="M18,18H46" stroke-width="2"/>')
    o.append(f'<rect class="f-ink" x="22" width="20" height="16" rx="2">{anim("y", nums([y - 8 for y in ys]), dur)}</rect>')
    o.append(f'<line class="s-mute" x1="32" y1="18" x2="32" stroke-width="1.6" stroke-dasharray="2 2">{anim("y2", nums([y - 8 for y in ys]), dur)}</line>')
    return ''.join(o)


@fig('wave-trans', 'Поперечная волна: точки среды движутся вверх-вниз, а волна бежит вправо', 360, 200)
def wave_trans():
    o = []
    T, lam, A, y0 = 2.0, 120, 36, 100
    for x in range(20, 344, 12):
        tau = (x - 20) / lam * T
        begin = -(T - tau % T)
        ys = sample(lambda u: y0 - A * math.sin(2 * math.pi * u), 25)
        hl = x == 116
        o.append(f'<circle class="{"f-red" if hl else "f-acc"}" cx="{x}" r="{7 if hl else 5}"><animate attributeName="cy" values="{nums(ys)}" keyTimes="{times(25)}" dur="{T}s" begin="{f(begin)}s" repeatCount="indefinite"/></circle>')
    o.append(f'<path class="s-mute" d="M116,{y0-A-12}V{y0+A+12}" stroke-width="1" stroke-dasharray="3 4"/>')
    o.append(f'<path class="s-mute" d="M12,{y0}H350" stroke-width="1" stroke-dasharray="2 5"/>')
    o.append(arrow(262, 26, 340, 26, 's-ink', 'f-ink', 2, 8) + text(254, 31, 'направление волны', 't-s', 'end'))
    o.append(f'<path class="s-red" d="M20,170V176H{20+lam}V170" stroke-width="1.4"/>' + text(20 + lam / 2, 192, 'λ', 't-red'))
    o.append(text(344, 192, 'красная точка — только вверх-вниз', 't-s', 'end'))
    return ''.join(o)


@fig('wave-long', 'Продольная волна: слои среды колеблются вдоль направления волны, сгущения бегут вправо', 360, 170)
def wave_long():
    o = []
    T, lam, a = 2.0, 120, 9
    for x in range(20, 346, 8):
        tau = (x - 20) / lam * T
        begin = -(T - tau % T)
        dx = sample(lambda u: a * math.sin(2 * math.pi * u), 25)
        hl = x == 116
        o.append(f'<line class="{"s-red" if hl else "s-acc"}" x1="{x}" y1="36" x2="{x}" y2="116" stroke-width="{3 if hl else 2}">'
                 f'<animateTransform attributeName="transform" type="translate" values="{";".join(f(v) + " 0" for v in dx)}" keyTimes="{times(25)}" dur="{T}s" begin="{f(begin)}s" repeatCount="indefinite"/></line>')
    o.append(arrow(220, 148, 300, 148, 's-ink', 'f-ink', 2, 8) + text(212, 153, 'направление волны', 't-s', 'end'))
    o.append(text(116, 28, '↔', 't-red'))
    return ''.join(o)


# ───────────────────────────── индукция ─────────────────────────────

@fig('flux', 'Магнитный поток Φ = BS cos α: при повороте контура меняется угол между B и нормалью n и вместе с ним поток', 360, 220)
def flux():
    cx, cy, a = 140, 112, 64
    o = []
    for x in range(40, 250, 26):
        o.append(f'<path class="s-mute" d="M{x},204V16" stroke-width="1.4"/>' + head(x, 16, -90, 'f-mute', 6))
    o.append(text(262, 30, 'B', 't-acc'))
    n = 49
    angs = sample(lambda u: 360 * u, n)
    o.append(f'<g>{rot(angs, cx, cy, 8)}<line class="s-ink" x1="{cx-a}" y1="{cy}" x2="{cx+a}" y2="{cy}" stroke-width="6" stroke-linecap="round"/>'
             + arrow(cx, cy, cx, cy - 58, 's-red', 'f-red', 2.6, 9) + '</g>')
    o.append(text(18, 212, 'красная стрелка — нормаль n', 't-s', 'start'))
    o.append(f'<circle class="f-paper s-ink" cx="{cx}" cy="{cy}" r="4" stroke-width="2"/>')
    # индикатор потока: знак и величина cos α
    bx, by, bw = 300, 112, 70
    o.append(f'<rect class="s-mute" x="{bx-14}" y="{by-bw}" width="28" height="{2*bw}" stroke-width="1" stroke-dasharray="3 3"/>')
    o.append(f'<path class="s-mute" d="M{bx-20},{by}H{bx+20}" stroke-width="1.4"/>')
    cosv = [math.cos(math.radians(x)) for x in angs]
    ys = nums([by - bw * max(c, 0) for c in cosv])
    hs = nums([bw * abs(c) for c in cosv])
    o.append(f'<rect class="f-acc" x="{bx-14}" width="28">{anim("y", ys, 8)}{anim("height", hs, 8)}</rect>')
    o.append(text(bx, by - bw - 8, 'Φ', 't'))
    o.append(text(bx, by + bw + 18, 'Φ = BS cos α', 't-s'))
    return ''.join(o)


@fig('faraday', 'Опыт Фарадея: магнит вдвигают — стрелка отклоняется, магнит покоится — тока нет, магнит вынимают — стрелка отклоняется в другую сторону', 360, 230)
def faraday():
    o = []
    cx, top, bot = 120, 118, 206
    dur = 8
    kt = '0;0.12;0.38;0.62;0.88;1'
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 96;0 96;0 0;0 0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;0.4 0 0.6 1;0 0 1 1;0.4 0 0.6 1;0 0 1 1"/>'
             + poles(cx - 15, 8, 30, 34, 'S', 'f-red') + poles(cx - 15, 42, 30, 34, 'N', 'f-acc') + '</g>')
    for y in range(top, bot, 11):
        o.append(f'<path class="s-acc" d="M{cx-34},{y}A34,7 0 0 0 {cx+34},{y}" stroke-width="2.2" fill="none"/>')
    o.append(f'<path class="s-ink" d="M{cx+34},{top}H262V176M{cx+34},{bot}H262V200" stroke-width="2" fill="none"/>')
    gx, gy = 262, 188
    o.append(f'<circle class="f-paper s-ink" cx="{gx}" cy="{gy}" r="24" stroke-width="2"/>' + text(gx, gy + 18, 'G', 't-s'))
    o.append(f'<path class="s-mute" d="M{gx-16},{gy-6}A18,18 0 0 1 {gx+16},{gy-6}" stroke-width="1.2"/>')
    needle_kt = '0;0.12;0.16;0.34;0.38;0.62;0.66;0.84;0.88;1'
    needle = f'0 {gx} {gy};0 {gx} {gy};32 {gx} {gy};32 {gx} {gy};0 {gx} {gy};0 {gx} {gy};-32 {gx} {gy};-32 {gx} {gy};0 {gx} {gy};0 {gx} {gy}'
    o.append(f'<g><animateTransform attributeName="transform" type="rotate" values="{needle}" keyTimes="{needle_kt}" dur="{dur}s" repeatCount="indefinite"/>'
             + arrow(gx, gy + 4, gx, gy - 18, 's-red', 'f-red', 2.4, 7) + '</g>')
    labels = [('вдвигаем: ΔΦ ≠ 0', '0;0;1;1;0;0', '0;0.12;0.13;0.37;0.38;1'),
              ('магнит покоится: ΔΦ = 0', '0;0;1;1;0;0', '0;0.38;0.39;0.61;0.62;1'),
              ('вынимаем: ΔΦ ≠ 0', '0;0;1;1;0;0', '0;0.62;0.63;0.87;0.88;1')]
    for t, v, k in labels:
        o.append(f'<text class="t" x="262" y="40" text-anchor="middle" opacity="0">{t}<animate attributeName="opacity" values="{v}" keyTimes="{k}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>')
    return ''.join(o)


@fig('self-ind', 'Самоиндукция: при включении индукционный ток в катушке направлен против тока, при выключении — по току', 360, 230)
def self_ind():
    o = []
    o.append('<path class="s-ink" d="M150,40H60V160H110M210,160H300V40H190" stroke-width="2" fill="none"/>')
    o.append('<rect class="f-paper" x="54" y="86" width="12" height="28"/>')
    o.append(text(152, 30, '+', 't') + text(188, 30, '−', 't'))
    o.append('<circle class="f-ink" cx="152" cy="40" r="3"/><circle class="f-ink" cx="188" cy="40" r="3"/>')
    o.append(''.join(f'<path class="s-acc" d="M{x},160a10,10 0 0 1 20,0" stroke-width="2.4" fill="none"/>' for x in range(110, 210, 20)))
    o.append(text(160, 178, 'L', 't-s'))
    dur = 7
    kt = '0;0.06;0.1;0.52;0.56;1'
    o.append(f'<g><animateTransform attributeName="transform" type="rotate" values="-35 60 115;-35 60 115;0 60 115;0 60 115;-35 60 115;-35 60 115" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             '<line class="s-ink" x1="60" y1="115" x2="60" y2="85" stroke-width="3"/></g>')
    o.append('<circle class="f-ink" cx="60" cy="115" r="3"/><circle class="f-ink" cx="60" cy="85" r="3"/>')
    rise = '0;0;0.25;0.85;1;1;0.55;0;0'
    rkt = '0;0.1;0.16;0.3;0.42;0.56;0.62;0.76;1'
    o.append(f'<path class="s-acc" d="M140,40H60V160H110M210,160H300V40H190" stroke-width="3" stroke-dasharray="4 9" stroke-linecap="round" fill="none" opacity="0">{flow(0.8, 13)}<animate attributeName="opacity" values="{rise}" keyTimes="{rkt}" dur="{dur}s" repeatCount="indefinite"/></path>')
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="{rise}" keyTimes="{rkt}" dur="{dur}s" repeatCount="indefinite"/>{arrow(122, 128, 198, 128, "s-acc", "f-acc", 2.6, 9)}{text(160, 120, "I", "t-acc")}</g>')
    on = '0;0;1;1;0;0'
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="{on}" keyTimes="0;0.1;0.12;0.36;0.42;1" dur="{dur}s" repeatCount="indefinite"/>'
             + arrow(200, 196, 120, 196, 's-red', 'f-red', 2.8, 9) + text(160, 220, 'при включении: I<tspan baseline-shift="sub" font-size="9">и</tspan> против I', 't-red') + '</g>')
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="{on}" keyTimes="0;0.56;0.58;0.74;0.8;1" dur="{dur}s" repeatCount="indefinite"/>'
             + arrow(120, 196, 200, 196, 's-red', 'f-red', 2.8, 9) + text(160, 220, 'при выключении: I<tspan baseline-shift="sub" font-size="9">и</tspan> по току', 't-red') + '</g>')
    return ''.join(o)


# ───────────────────────────── переменный ток ─────────────────────────────

@fig('lc', 'Колебательный контур: заряд конденсатора и ток в катушке меняются по очереди, энергия переходит из W_C в W_L и обратно', 360, 220)
def lc():
    o = []
    o.append('<path class="s-ink" d="M50,40H170V200H50V132M50,108V40" stroke-width="2" fill="none"/>')
    o.append('<path class="s-ink" d="M28,108H72M28,132H72" stroke-width="3.4"/>')
    o.append(text(86, 124, 'C', 't-s', 'start'))
    coil = ''.join(f'<path class="s-acc" d="M170,{y}a10,10 0 0 1 0,20" stroke-width="2.4" fill="none"/>' for y in range(70, 170, 20))
    o.append(coil)
    o.append(text(186, 124, 'L', 't-s', 'start'))
    n, dur = 41, 4
    c = sample(lambda u: math.cos(2 * math.pi * u), n)
    s_ = sample(lambda u: -math.sin(2 * math.pi * u), n)  # I = −I0 sin ωt
    top_plus = nums([max(v, 0) for v in c])
    top_minus = nums([max(-v, 0) for v in c])
    o.append(f'<g>{anim("opacity", top_plus, dur)}{text(50, 102, "+ + +", "t-red")}{text(50, 150, "− − −", "t-acc")}</g>')
    o.append(f'<g>{anim("opacity", top_minus, dur)}{text(50, 102, "− − −", "t-acc")}{text(50, 150, "+ + +", "t-red")}</g>')
    # магнитное поле катушки — свечение ∝ |I|
    o.append(f'<ellipse class="f-soft" cx="176" cy="120" rx="30" ry="58">{anim("opacity", nums([abs(v) for v in s_]), dur)}</ellipse>')
    # стрелки тока: по часовой при I > 0, против при I < 0
    o.append(f'<g>{anim("opacity", nums([max(v, 0) for v in s_]), dur)}{arrow(90, 28, 140, 28, "s-acc", "f-acc", 2.6, 8)}</g>')
    o.append(f'<g>{anim("opacity", nums([max(-v, 0) for v in s_]), dur)}{arrow(140, 28, 90, 28, "s-acc", "f-acc", 2.6, 8)}</g>')
    o.append(text(115, 18, 'I', 't-acc'))
    base, hmax = 196, 140
    wc = [v * v for v in c]
    wl = [1 - v for v in wc]
    for x, series, cls, lab in [(262, wc, 'f-red', 'W<tspan baseline-shift="sub" font-size="9">C</tspan>'), (318, wl, 'f-acc', 'W<tspan baseline-shift="sub" font-size="9">L</tspan>')]:
        o.append(f'<rect class="s-mute" x="{x-15}" y="{base-hmax}" width="30" height="{hmax}" stroke-width="1" stroke-dasharray="3 3"/>')
        o.append(f'<rect class="{cls}" x="{x-15}" width="30" rx="3">{anim("y", nums([base - hmax * v for v in series]), dur)}{anim("height", nums([hmax * v for v in series]), dur)}</rect>')
        o.append(text(x, base + 18, lab, 't'))
    o.append(text(290, 44, 'W = const', 't-s'))
    return ''.join(o)


@fig('generator', 'Генератор переменного тока: рамка вращается в магнитном поле, ЭДС меняется по закону синуса', 360, 220)
def generator():
    o = [poles(6, 34, 34, 100, 'N', 'f-acc'), poles(150, 34, 34, 100, 'S', 'f-red')]
    for y in (52, 84, 116):
        o.append(f'<path class="s-mute" d="M42,{y}H148" stroke-width="1.2"/>' + head(146, y, 0, 'f-mute', 6))
    n, dur = 49, 4
    sv = sample(lambda u: math.sin(2 * math.pi * u), n)  # ширина рамки ∝ sin ωt, поток ∝ cos ωt
    scale = ';'.join(f'{f(v if abs(v) > 0.02 else (0.02 if v >= 0 else -0.02))} 1' for v in sv)
    o.append(f'<g transform="translate(95,84)"><g><animateTransform attributeName="transform" type="scale" values="{scale}" keyTimes="{times(n)}" dur="{dur}s" repeatCount="indefinite"/>'
             '<rect class="s-ink f-soft" x="-34" y="-52" width="68" height="104" stroke-width="3" vector-effect="non-scaling-stroke"/></g></g>')
    o.append('<path class="s-mute" d="M95,20V148" stroke-width="1" stroke-dasharray="4 4"/>')
    o.append('<path class="s-ink" d="M95,148V170M88,170H102" stroke-width="2"/>')
    o.append('<circle class="f-paper s-ink" cx="95" cy="190" r="14" stroke-width="2"/>' + '<path class="s-ink" d="M86,181L104,199M104,181L86,199" stroke-width="1.6"/>')
    o.append(f'<circle class="f-red-soft" cx="95" cy="190" r="22">{anim("opacity", nums([abs(v) for v in sv]), dur)}</circle>')
    # график ε(t) = ε0 sin ωt
    gx0, gx1, gy, A = 210, 352, 110, 46
    per = (gx1 - gx0)
    pts = [f'{f(gx0 + i)},{f(gy - A * math.sin(2 * math.pi * i / per))}' for i in range(0, per + 1, 2)]
    o.append(arrow(gx0, gy, 356, gy, 's-ink', 'f-ink', 1.4, 6) + arrow(gx0, 170, gx0, 46, 's-ink', 'f-ink', 1.4, 6))
    o.append(f'<path class="s-red" d="M{"L".join(pts)}" stroke-width="2.2" fill="none"/>')
    o.append(text(gx0 + 10, 52, 'ε', 't-red', 'start') + text(350, gy + 18, 't', 't-s'))
    o.append(f'<circle class="f-red" r="5.5"><animate attributeName="cx" values="{gx0};{gx1}" dur="{dur}s" repeatCount="indefinite"/>{anim("cy", nums([gy - A * v for v in sv]), dur)}</circle>')
    o.append(text(281, 196, 'ε = ε₀ sin ωt', 't-s'))
    return ''.join(o)


@fig('ac-phase', 'Сдвиг фаз: на резисторе ток и напряжение в фазе, на конденсаторе ток впереди на π/2, на катушке — позади', 360, 252)
def ac_phase():
    o = []
    x0, x1 = 96, 350
    per = (x1 - x0) / 1.5
    rows = [('R', 'Δφ = 0', lambda p: math.sin(p), lambda p: math.sin(p)),
            ('C', 'ток впереди', lambda p: math.cos(p), lambda p: -math.sin(p)),
            ('L', 'ток позади', lambda p: math.cos(p), lambda p: math.sin(p))]
    dur, n = 6, 61
    for k, (lab, cap, U, I) in enumerate(rows):
        yc = 44 + k * 78
        A, Ai = 24, 15
        o.append(f'<path class="s-mute" d="M{x0},{yc}H{x1}" stroke-width="1"/>')
        o.append(text(8, yc + 5, lab, 't', 'start'))
        o.append(text(8, yc + 22, cap, 't-s', 'start'))
        pu = [f'{f(x0 + i)},{f(yc - A * U(2 * math.pi * i / per))}' for i in range(0, int(x1 - x0) + 1, 3)]
        pi = [f'{f(x0 + i)},{f(yc - Ai * I(2 * math.pi * i / per))}' for i in range(0, int(x1 - x0) + 1, 3)]
        o.append(f'<path class="s-acc" d="M{"L".join(pu)}" stroke-width="2.2" fill="none"/>')
        o.append(f'<path class="s-red" d="M{"L".join(pi)}" stroke-width="2.2" stroke-dasharray="5 3" fill="none"/>')
        uy = sample(lambda u: yc - A * U(2 * math.pi * 1.5 * u), n)
        iy = sample(lambda u: yc - Ai * I(2 * math.pi * 1.5 * u), n)
        o.append(f'<circle class="f-acc" r="5"><animate attributeName="cx" values="{x0};{x1}" dur="{dur}s" repeatCount="indefinite"/>{anim("cy", nums(uy), dur)}</circle>')
        o.append(f'<circle class="f-red" r="4.5"><animate attributeName="cx" values="{x0};{x1}" dur="{dur}s" repeatCount="indefinite"/>{anim("cy", nums(iy), dur)}</circle>')
    o.append(f'<line class="s-mute" y1="14" y2="226" stroke-width="1" stroke-dasharray="3 4"><animate attributeName="x1" values="{x0};{x1}" dur="{dur}s" repeatCount="indefinite"/><animate attributeName="x2" values="{x0};{x1}" dur="{dur}s" repeatCount="indefinite"/></line>')
    o.append(f'<line class="s-acc" x1="120" y1="244" x2="146" y2="244" stroke-width="2.4"/>' + text(152, 248, 'U', 't-acc', 'start')
             + f'<line class="s-red" x1="196" y1="244" x2="222" y2="244" stroke-width="2.4" stroke-dasharray="5 3"/>' + text(228, 248, 'I', 't-red', 'start'))
    return ''.join(o)


@fig('transformer', 'Понижающий трансформатор: переменный поток в сердечнике, у вторичной обмотки меньше витков и меньше напряжение', 360, 230)
def transformer():
    o = ['<rect class="s-ink" x="96" y="20" width="168" height="130" rx="4" stroke-width="18" fill="none" stroke-opacity="0.18"/>',
         '<rect class="s-ink" x="96" y="20" width="168" height="130" rx="4" stroke-width="1.6" fill="none"/>']
    o.append('<path class="s-acc" d="M96,85V20H264V150H96Z" stroke-width="2.6" stroke-dasharray="5 10" fill="none" stroke-linecap="round">'
             '<animate attributeName="stroke-dashoffset" values="0;30;0" dur="2s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/></path>')
    for i in range(8):
        y = 40 + i * 11
        o.append(f'<path class="s-red" d="M82,{y}h28" stroke-width="3" stroke-linecap="round"/>')
    for i in range(3):
        y = 60 + i * 20
        o.append(f'<path class="s-grn" d="M250,{y}h28" stroke-width="3" stroke-linecap="round"/>')
    o.append(text(70, 34, 'N₁', 't-red', 'end') + text(292, 54, 'N₂', 't-grn', 'start'))
    # волны U1 (больше) и U2 (меньше) бегут в окнах clipPath
    for k, (x0, amp, cls) in enumerate([(14, 22, 's-red'), (196, 9, 's-grn')]):
        w, per = 150, 50
        cid = f'transformer-clip{k+1}'
        o.append(f'<clipPath id="{cid}"><rect x="{x0}" y="160" width="{w}" height="64"/></clipPath>')
        pts = [f'{f(x0 + i)},{f(192 - amp * math.sin(2 * math.pi * i / per))}' for i in range(0, w + per + 1, 2)]
        o.append(f'<g clip-path="url(#{cid})"><g><animateTransform attributeName="transform" type="translate" values="0 0;{-per} 0" dur="1s" repeatCount="indefinite"/>'
                 f'<path class="{cls}" d="M{"L".join(pts)}" stroke-width="2.2" fill="none"/></g></g>')
    o.append(text(90, 222, 'U₁', 't-red') + text(270, 222, 'U₂ &lt; U₁', 't-grn'))
    o.append(text(180, 92, 'k = N₁/N₂ &gt; 1', 't-s'))
    return ''.join(o)


@fig('em-wave', 'Электромагнитная волна: поля E и B перпендикулярны друг другу и направлению распространения', 360, 210)
def em_wave():
    o = ['<clipPath id="em-wave-clip"><rect x="24" y="0" width="316" height="210"/></clipPath>']
    y0, lam, AE, AB = 104, 100, 54, 34
    ox, oy = 0.35, 0.6    # косая проекция оси z (вниз-влево)
    xs = list(range(24 - lam, 340 + 1, 4))
    pe = [f'{f(x)},{f(y0 - AE * math.sin(2 * math.pi * (x - 24) / lam))}' for x in xs]
    pb = []
    for x in xs:
        z = AB * math.sin(2 * math.pi * (x - 24) / lam)
        pb.append(f'{f(x - z * ox)},{f(y0 + z * oy)}')
    g = [f'<g clip-path="url(#em-wave-clip)"><g><animateTransform attributeName="transform" type="translate" values="0 0;{lam} 0" dur="2s" repeatCount="indefinite"/>']
    for x in range(24 - lam, 341, 10):
        e = AE * math.sin(2 * math.pi * (x - 24) / lam)
        z = AB * math.sin(2 * math.pi * (x - 24) / lam)
        g.append(f'<line class="s-red" x1="{x}" y1="{y0}" x2="{x}" y2="{f(y0 - e)}" stroke-width="1.2" stroke-opacity="0.55"/>')
        g.append(f'<line class="s-acc" x1="{x}" y1="{y0}" x2="{f(x - z * ox)}" y2="{f(y0 + z * oy)}" stroke-width="1.2" stroke-opacity="0.55"/>')
    g.append(f'<path class="s-red" d="M{"L".join(pe)}" stroke-width="2.4" fill="none"/>')
    g.append(f'<path class="s-acc" d="M{"L".join(pb)}" stroke-width="2.4" fill="none"/></g></g>')
    o.append(''.join(g))
    o.append(arrow(20, y0, 350, y0, 's-ink', 'f-ink', 2, 9) + text(344, y0 - 10, 'υ', 't'))
    o.append(text(36, 40, 'E', 't-red') + text(16, 160, 'B', 't-acc'))
    o.append(text(190, 204, 'буравчик от E к B — направление волны', 't-s'))
    return ''.join(o)




# ───────────────────────── страница o01: контур с антенной, интенсивность ─────────────────────────

@fig('radio', 'Колебательный контур с антенной и заземлением: заряд конденсатора и ток в катушке периодически меняются, антенна излучает электромагнитные волны, λ = c·2π√(LC)', 360, 220)
def radio():
    dur, n = 3, 41
    c = sample(lambda u: math.cos(2 * math.pi * u), n)
    s_ = sample(lambda u: -math.sin(2 * math.pi * u), n)
    o = ['<path class="s-ink" d="M70,30V70H40V180H130V70H100V30" stroke-width="2" fill="none"/>']
    # антенна и заземление
    o.append('<path class="s-ink" d="M70,30H100M85,30V20M75,24L85,20L95,24" stroke-width="2"/>')
    o.append('<path class="s-ink" d="M85,180V196M71,196H99M75,201H95M80,206H90" stroke-width="2"/>')
    # конденсатор слева, катушка справа
    o.append('<path class="s-ink" d="M40,112V112M22,112H58M22,128H58" stroke-width="3.4"/><rect class="f-paper" x="36" y="113" width="8" height="14"/>')
    coil = ''.join(f'<path class="s-acc" d="M130,{y}a9,9 0 0 1 0,18" stroke-width="2.4" fill="none"/>' for y in range(84, 160, 18))
    o.append('<rect class="f-paper" x="126" y="84" width="8" height="72"/>' + coil)
    o.append(text(14, 124, 'C', 't-s', 'end').replace('x="14"', 'x="16"') + text(150, 124, 'L', 't-s', 'start'))
    o.append(f'<g>{anim("opacity", nums([max(v, 0) for v in c]), dur)}{text(40, 106, "+", "t-red")}{text(40, 142, "−", "t-acc")}</g>')
    o.append(f'<g>{anim("opacity", nums([max(-v, 0) for v in c]), dur)}{text(40, 106, "−", "t-acc")}{text(40, 142, "+", "t-red")}</g>')
    # волны от антенны (дуги вправо)
    def arc(r):
        a1, a2 = math.radians(-40), math.radians(40)
        return f'M{f(85 + r * math.cos(a1))},{f(20 + r * math.sin(a1))}A{r},{r} 0 0 1 {f(85 + r * math.cos(a2))},{f(20 + r * math.sin(a2))}'
    for i in range(4):
        r0 = 8 + i * 10
        o.append(f'<path class="s-red" fill="none" stroke-width="2" d="{arc(r0)}"><animate attributeName="d" values="{arc(r0)};{arc(r0 + 10)}" dur="{f(dur / 2)}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="{f(1 - i / 4)};{f(1 - (i + 1) / 4)}" dur="{f(dur / 2)}s" repeatCount="indefinite"/></path>')
    # волна, уходящая вправо: E(x, t)
    lam = 88
    wave = ['M' + 'L'.join(f'{f(180 + x)},{f(120 - 34 * math.cos(2 * math.pi * (x / lam - u)))}' for x in range(0, 171, 5)) for u in lin(0, 1, n)]
    o.append(f'<path class="s-red" stroke-width="2.2" fill="none"><animate attributeName="d" values="{";".join(wave)}" keyTimes="{times(n)}" dur="{dur}s" repeatCount="indefinite"/></path>')
    o.append('<path class="s-mute" d="M180,120H352" stroke-width="1" stroke-dasharray="3 4"/>')
    o.append(f'<path class="s-ink" d="M180,170H{180 + lam}M180,164V176M{180 + lam},164V176" stroke-width="1.4"/>' + text(180 + lam / 2, 190, 'λ = cT', 't'))
    o.append(text(352, 212, 'λ = c·2π√(LC)', 't-s', 'end'))
    return ''.join(o)


@fig('intensity-spread', 'Интенсивность волн от точечного источника: та же энергия на расстоянии 2R проходит через площадь в 4 раза больше, поэтому I ~ 1/R²', 360, 220)
def intensity_spread():
    dur = 3
    S = (30, 110)
    o = []
    # конус лучей через квадрат на расстоянии R и 2R (вид сбоку с перспективой)
    R1, R2 = 140, 280
    a1, a2 = 22, 44
    for (x, a, lab, k) in [(S[0] + R1, a1, 'R', 1), (S[0] + R2, a2, '2R', 2)]:
        w = 12 + k * 6
        tf = f' transform="skewY(-12)" transform-origin="{f(x)} {S[1]}"'
        cells = ''.join(f'<rect class="s-acc" x="{f(x - w / 2 + i * w / k)}" y="{f(S[1] - a + j * 2 * a / k)}" width="{f(w / k)}" height="{f(2 * a / k)}" stroke-width="1.4" fill="none"{tf}/>' for j in range(k) for i in range(k))
        o.append(f'<rect class="f-soft" x="{f(x - w / 2)}" y="{S[1] - a}" width="{w}" height="{2 * a}"{tf}/>' + cells)
        o.append(text(x, S[1] + a + 30, lab, 't'))
    for dy in (-1, 1):
        o.append(f'<path class="s-red" d="M{S[0]},{S[1]}L{S[0] + R2},{S[1] + dy * a2}" stroke-width="1.4" stroke-dasharray="4 4"/>')
    # «порции» энергии летят по конусу и растягиваются
    for i in range(6):
        y0 = (i - 2.5) / 2.5
        o.append(f'<circle class="f-red" r="3.5" cx="{S[0]}" cy="{S[1]}"><animate attributeName="cx" values="{S[0]};{S[0] + R2}" dur="{dur}s" begin="{f(i * dur / 6)}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="cy" values="{S[1]};{f(S[1] + y0 * a2 * 0.9)}" dur="{dur}s" begin="{f(i * dur / 6)}s" repeatCount="indefinite"/></circle>')
    o.append(f'<circle class="f-ink" cx="{S[0]}" cy="{S[1]}" r="6"/>')
    o.append(text(180, 24, 'площадь × 4 ⇒ I : 4', 't-s') + text(352, 212, 'I ~ 1/R²', 't', 'end'))
    return ''.join(o)
