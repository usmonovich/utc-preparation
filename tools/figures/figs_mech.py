"""Иллюстрации к конспекту по механике (стр. p01–p41R)."""
import math
from figlib import *  # noqa: F401,F403

G = 10  # в конспекте в расчётах g = 10 м/с²


def lin(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


def car(x, y, cls='f-acc'):
    return (f'<rect class="{cls}" x="{f(x)}" y="{f(y)}" width="34" height="14" rx="3"/>'
            f'<rect class="{cls}" x="{f(x+7)}" y="{f(y-8)}" width="18" height="9" rx="2"/>'
            f'<circle class="f-ink" cx="{f(x+8)}" cy="{f(y+15)}" r="4"/><circle class="f-ink" cx="{f(x+26)}" cy="{f(y+15)}" r="4"/>')


def ground(x1, x2, y, step=12):
    return (f'<path class="s-ink" d="M{x1},{y}H{x2}" stroke-width="2"/>'
            + ''.join(f'<path class="s-mute" d="M{x},{y}l-7,8" stroke-width="1.1"/>' for x in range(x1 + 8, x2, step)))


def appear(t, dur):
    """opacity 0 → 1 в момент t (доля периода) и до конца цикла."""
    t = min(max(t, 0.001), 0.998)
    return f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{f(t)};{f(t+0.001)};1" dur="{dur}s" repeatCount="indefinite"/>'


# ───────────────────────────── кинематика ─────────────────────────────

@fig('path-disp', 'Путь и перемещение: точка движется по кривой траектории — путь L равен её длине, перемещение S соединяет начало и конец', 360, 220)
def path_disp():
    d = 'M40,170C90,40 170,210 230,110S300,40 322,70'
    dur = 6
    o = [markers('path-disp', ('red',))]
    o.append(f'<path id="path-disp-tr" class="s-mute" d="{d}" stroke-width="1.4" stroke-dasharray="3 5"/>')
    o.append(f'<path class="s-acc" d="{d}" stroke-width="3" pathLength="100" stroke-dasharray="100" stroke-linecap="round">'
             f'<animate attributeName="stroke-dashoffset" values="100;0;0" keyTimes="0;0.7;1" dur="{dur}s" repeatCount="indefinite"/></path>')
    o.append(f'<g opacity="0">{appear(0.7, dur)}' + mline('path-disp', 40, 170, 318, 72, 'red', 2.6) + text(170, 140, 'S', 't-red') + '</g>')
    o.append('<circle class="f-ink" cx="40" cy="170" r="4"/>' + text(30, 190, 'начало', 't-s'))
    o.append(text(330, 92, 'конец', 't-s'))
    o.append(f'<circle class="f-ink" r="7"><animateMotion dur="{dur}s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.7;1" calcMode="linear"><mpath href="#path-disp-tr"/></animateMotion></circle>')
    o.append(text(16, 24, 'L — путь (длина траектории)', 't-acc', 'start') + text(16, 44, 'S — перемещение (прямая)', 't-red', 'start'))
    return ''.join(o)


@fig('uniform-graphs', 'Равномерное движение: за равные промежутки времени равные пути; график S(t) — прямая, υ(t) — горизонталь, площадь под ней — путь', 360, 230)
def uniform_graphs():
    dur, n = 5, 21
    o = [ground(10, 350, 60)]
    xs = lin(16, 300, n)
    o.append(f'<g>{move([(x - 16, 0) for x in xs], dur)}{car(16, 38)}</g>')
    for k in range(5):
        x = 16 + 17 + (300 - 16) * k / 4
        o.append(f'<g opacity="0">{appear(k / 4 * 0.999, dur)}<circle class="f-red" cx="{f(x)}" cy="72" r="3.5"/>{text(x, 88, f"{k} с", "t-s")}</g>')
    # S(t)
    o.append(arrow(30, 206, 165, 206, 's-ink', 'f-ink', 1.4, 6) + arrow(30, 206, 30, 104, 's-ink', 'f-ink', 1.4, 6))
    o.append(text(42, 112, 'S', 't') + text(160, 222, 't', 't-s'))
    o.append(f'<line class="s-acc" x1="30" y1="206" x2="150" y2="122" stroke-width="2.4"/>')
    o.append(f'<circle class="f-red" r="5">{anims(dur, cx=lin(30, 150, n), cy=lin(206, 122, n))}</circle>')
    # υ(t)
    o.append(arrow(200, 206, 345, 206, 's-ink', 'f-ink', 1.4, 6) + arrow(200, 206, 200, 104, 's-ink', 'f-ink', 1.4, 6))
    o.append(text(212, 112, 'υ', 't') + text(340, 222, 't', 't-s'))
    o.append(f'<rect class="f-soft" x="200" y="150" height="56">{anim("width", nums(lin(0, 130, n)), dur)}</rect>')
    o.append('<line class="s-acc" x1="200" y1="150" x2="330" y2="150" stroke-width="2.4"/>')
    o.append(f'<circle class="f-red" cy="150" r="5">{anim("cx", nums(lin(200, 330, n)), dur)}</circle>')
    o.append(text(265, 186, 'площадь = путь L', 't-s'))
    return ''.join(o)


@fig('river', 'Переправа через реку: ① лодку направляют перпендикулярно берегу — её сносит течением на l; ② при υл > υт лодку направляют под углом против течения, и она идёт поперёк реки', 360, 230)
def river():
    dur = 11
    vl, vt = 40, 24                      # длины стрелок υл и υт
    top, bot = 62, 176                   # куда доходит лодка
    drift = (bot - top) * vt / vl        # снос в случае ①
    ang = math.degrees(math.asin(vt / vl))
    vr2 = math.sqrt(vl * vl - vt * vt)
    o = [markers('river', ('acc', 'grn', 'red'))]
    o.append('<rect class="f-soft" x="0" y="40" width="360" height="152"/>')
    o.append('<path class="s-ink" d="M0,40H360M0,192H360" stroke-width="2"/>')
    for y in (76, 116, 156):
        o.append(f'<path class="s-grn" d="M0,{y}H360" stroke-width="1.6" stroke-dasharray="10 22" stroke-opacity="0.6">{flow(1.6, 32)}</path>')
    n = 16

    def phase(t0, t1, hold):
        return f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{f(t0)};{f(t0 + 0.001)};{f(hold)};{f(hold + 0.001)};1" dur="{dur}s" repeatCount="indefinite"/>'

    def boat(x0, x1, t0, t1, hold, heading, vres, label):
        kt = [0, t0] + [t0 + (t1 - t0) * i / (n - 1) for i in range(n)] + [1]
        xs = [x0, x0] + lin(x0, x1, n) + [x1]
        ys = [bot, bot] + lin(bot, top, n) + [top]
        tr = ';'.join(f'{f(x)} {f(y)}' for x, y in zip(xs, ys))
        return (f'<g opacity="0">{phase(t0, t1, hold)}'
                f'<path class="s-ink" d="M{x0},{bot}L{f(x1)},{top}" stroke-width="1.2" stroke-dasharray="3 4"/>'
                f'<g><animateTransform attributeName="transform" type="translate" values="{tr}" keyTimes="{";".join(f(k) for k in kt)}" dur="{dur}s" repeatCount="indefinite"/>'
                f'<path class="f-ink" d="M-7,8L-5,-9L0,-15L5,-9L7,8Z" transform="rotate({f(heading)})"/>'
                + f'<g><animate attributeName="opacity" values="1;0;1" keyTimes="0;{f(t1)};{f(hold)}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>'
                + mline('river', 0, 0, 0, -vl, 'acc', 2.4, extra=f' transform="rotate({f(heading)})"')
                + mline('river', 0, 0, vt, 0, 'grn', 2.4)
                + mline('river', 0, 0, vres[0], vres[1], 'red', 2.6)
                + '</g></g>' + text(180, 214, label, 't-s') + '</g>')
    o.append(boat(90, 90 + drift, 0.02, 0.32, 0.46, 0, (vt, -vl), '① курс перпендикулярно берегу — снос l'))
    o.append(boat(250, 250, 0.52, 0.895, 0.985, -ang, (0, -vr2), '② курс против течения — снос l = 0'))
    o.append(f'<g opacity="0">{phase(0.32, 0.32, 0.46)}<path class="s-mute" d="M90,{bot}V{top}" stroke-width="1" stroke-dasharray="2 4"/>'
             f'<path class="s-red" d="M90,{bot + 8}H{f(90 + drift)}M90,{bot + 2}V{bot + 14}M{f(90 + drift)},{bot + 2}V{bot + 14}" stroke-width="1.6" transform="translate(0,{top - bot - 16})"/>'
             + text(90 + drift / 2, top - 12, 'l', 't-red') + '</g>')
    o.append(text(352, 32, 'течение →', 't-grn', 'end'))
    o.append('<g transform="translate(8,30)"><line class="s-acc" x1="0" y1="-4" x2="14" y2="-4" stroke-width="2.4"/>' + text(18, 0, 'υ_л', 't-acc', 'start')
             + '<line class="s-grn" x1="50" y1="-4" x2="64" y2="-4" stroke-width="2.4"/>' + text(68, 0, 'υ_т', 't-grn', 'start')
             + '<line class="s-red" x1="100" y1="-4" x2="114" y2="-4" stroke-width="2.4"/>' + text(118, 0, 'υ_р', 't-red', 'start') + '</g>')
    return ''.join(o)

@fig('accel', 'Равноускоренное движение из покоя с a = 2 м/с²: каждую секунду скорость растёт на 2 м/с, расстояния между отметками увеличиваются', 360, 176)
def accel():
    dur, n = 5, 41
    a, sc = 2, 18  # 1 м = 18 px... путь за 4 с = 16 м
    o = [ground(10, 350, 70)]
    T = 4.0
    ts = lin(0, T, n)
    xs = [20 + sc * a * t * t / 2 * 0.95 for t in ts]
    kt = [0.8 * t / T for t in ts] + [1]
    tr = ';'.join(f'{f(x - 20)} 0' for x in xs + [xs[-1]])
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{tr}" keyTimes="{";".join(f(k) for k in kt)}" dur="{dur}s" repeatCount="indefinite"/>{car(20, 48)}</g>')
    o.append(text(14, 122, 't, с', 't-s', 'start') + text(14, 142, 'x, м', 't-s', 'start') + text(14, 162, 'υ, м/с', 't-s', 'start'))
    for k in range(5):
        x = 20 + 17 + sc * a * k * k / 2 * 0.95
        o.append(f'<g opacity="0">{appear(0.8 * k / T, dur)}<circle class="f-red" cx="{f(x)}" cy="80" r="4"/>'
                 f'{text(x, 98, str(k), "t-s")}'
                 f'{text(90 + 60 * k, 122, str(k), "t-s")}{text(90 + 60 * k, 142, str(a * k * k // 2), "t-s")}{text(90 + 60 * k, 162, str(a * k), "t-acc")}</g>')
    o.append(text(180, 24, 'a = 2 м/с²: каждую секунду υ растёт на 2 м/с', 't-s'))
    return ''.join(o)


@fig('vt-area', 'Путь и перемещение по графику υ(t): площадь над осью S₁, под осью S₂; путь L = S₁ + S₂, перемещение S = S₁ − S₂', 360, 220)
def vt_area():
    dur = 6
    x0, y0, x1 = 40, 110, 330
    o = ['<clipPath id="vt-area-clip"><rect x="40" y="10" height="200" width="0">'
         f'<animate attributeName="width" values="0;290;290" keyTimes="0;0.75;1" dur="{dur}s" repeatCount="indefinite"/></rect></clipPath>']
    # υ(t) = υ0 − a t: пересекает ось в середине
    xm = 200
    o.append(f'<g clip-path="url(#vt-area-clip)"><path class="f-soft" d="M{x0},{y0}V40L{xm},{y0}Z"/><path class="f-red-soft" d="M{xm},{y0}L310,{y0+48}V{y0}Z"/></g>')
    o.append(arrow(x0, y0, 350, y0, 's-ink', 'f-ink', 1.4, 6) + arrow(x0, 200, x0, 14, 's-ink', 'f-ink', 1.4, 6))
    o.append(f'<path class="s-acc" d="M{x0},40L310,{y0+48}" stroke-width="2.4"/>')
    o.append(f'<path class="s-mute" d="M310,{y0}V{y0+48}" stroke-width="1" stroke-dasharray="3 4"/>')
    o.append(text(x0 + 14, 24, 'υ', 't') + text(344, y0 + 18, 't', 't-s'))
    o.append(text(95, 92, 'S₁', 't-acc') + text(284, 128, 'S₂', 't-red'))
    o.append(f'<line class="s-mute" y1="14" y2="200" stroke-width="1" stroke-dasharray="3 4"><animate attributeName="x1" values="40;310;310" keyTimes="0;0.75;1" dur="{dur}s" repeatCount="indefinite"/><animate attributeName="x2" values="40;310;310" keyTimes="0;0.75;1" dur="{dur}s" repeatCount="indefinite"/></line>')
    o.append(text(180, 196, 'путь L = S₁ + S₂  ·  перемещение S = S₁ − S₂', 't-s'))
    return ''.join(o)


@fig('nth-second', 'Путь за пять секунд и путь за пятую секунду при υ₀ = 5 м/с, a = 2 м/с² (пример конспекта)', 360, 180)
def nth_second():
    dur, n = 6, 41
    v0, a, sc = 5, 2, 6.0
    xpos = lambda t: 22 + sc * (v0 * t + a * t * t / 2)
    o = [f'<path class="s-ink" d="M18,80H{f(xpos(5)+14)}" stroke-width="2"/>']
    for k in range(6):
        x = xpos(k)
        o.append(f'<path class="s-ink" d="M{f(x)},74V86" stroke-width="2"/>' + text(x, 104, f'{k} с', 't-s'))
        o.append(text(x, 66, f'{f(v0*k + a*k*k/2)} м', 't-s'))
    ts = lin(0, 5, n)
    kt = [0.7 * t / 5 for t in ts] + [1]
    cx = ';'.join(f(xpos(t)) for t in ts) + ';' + f(xpos(5))
    o.append(f'<circle class="f-ink" cy="80" r="7"><animate attributeName="cx" values="{cx}" keyTimes="{";".join(f(k) for k in kt)}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(f'<g opacity="0">{appear(0.72, dur)}<path class="s-acc" d="M{f(xpos(0))},128V136H{f(xpos(5))}V128" stroke-width="2"/>'
             f'{text((xpos(0)+xpos(5))/2, 152, "за пять секунд: 50 м", "t-acc")}</g>')
    o.append(f'<g opacity="0">{appear(0.8, dur)}<rect class="f-red-soft" x="{f(xpos(4))}" y="72" width="{f(xpos(5)-xpos(4))}" height="16"/>'
             f'<path class="s-red" d="M{f(xpos(4))},40V34H{f(xpos(5))}V40" stroke-width="2"/>{text((xpos(4)+xpos(5))/2, 26, "за пятую: 14 м", "t-red")}</g>')
    return ''.join(o)


@fig('free-fall', 'Свободное падение: ускорение g направлено вниз, скорость растёт, за равные промежутки тело проходит всё больший путь', 360, 230)
def free_fall():
    dur, n = 3, 31
    y0, sc = 20, 150
    o = [markers('free-fall', ('acc', 'red'))]
    ts = lin(0, 1, n)
    ys = [y0 + sc * t * t for t in ts]
    kt = [0.75 * t for t in ts] + [1]
    for k, t in enumerate([0, 1 / 3, 2 / 3, 1.0]):
        y = y0 + sc * t * t
        o.append(f'<g opacity="0">{appear(0.75 * t, dur)}<circle class="s-mute" cx="150" cy="{f(y)}" r="7" stroke-width="1.4" stroke-dasharray="3 3"/>'
                 f'<path class="s-mute" d="M128,{f(y)}H112" stroke-width="1" stroke-dasharray="2 3"/>{text(106, y + 4, f"{k}τ", "t-s", "end")}</g>')
    cy = ';'.join(f(y) for y in ys) + ';' + f(ys[-1])
    kts = ';'.join(f(k) for k in kt)
    vy = [y + 8 + 42 * t for y, t in zip(ys, ts)]
    o.append(f'<circle class="f-ink" cx="150" r="7"><animate attributeName="cy" values="{cy}" keyTimes="{kts}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(f'<line class="s-acc" x1="150" x2="150" stroke-width="2.6" marker-end="url(#free-fall-m-acc)">'
             f'<animate attributeName="y1" values="{cy}" keyTimes="{kts}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y2" values="{";".join(f(v) for v in vy)};{f(vy[-1])}" keyTimes="{kts}" dur="{dur}s" repeatCount="indefinite"/></line>')
    o.append(f'<text class="t-acc" x="160"><animate attributeName="y" values="{";".join(f(y + 26) for y in ys)};{f(ys[-1] + 26)}" keyTimes="{kts}" dur="{dur}s" repeatCount="indefinite"/>υ</text>')
    o.append(mline('free-fall', 250, 60, 250, 110, 'red', 2.6) + text(262, 92, 'g', 't-red', 'start'))
    o.append(text(250, 140, 'g = const', 't-s') + text(250, 158, 'τ — равные промежутки', 't-s'))
    return ''.join(o)


@fig('throw-up', 'Бросок вверх с υ₀ = 30 м/с: скорость 30 → 20 → 10 → 0 в верхней точке, затем 10 → 20 → 30 при падении', 360, 230)
def throw_up():
    dur, n = 6, 49
    sc = 3.6
    ybase = 206
    ts = lin(0, 6, n)
    hs = [30 * t - 5 * t * t for t in ts]
    vs = [30 - 10 * t for t in ts]
    o = [ground(80, 280, ybase + 10)]
    for k in range(7):
        h = 30 * k - 5 * k * k
        y = ybase - sc * h
        v = 30 - 10 * k
        side = -1 if k <= 3 else 1
        lab = '0' if v == 0 else f'{abs(v)}{"↑" if v > 0 else "↓"}'
        o.append(f'<g opacity="0">{appear(k / 6 * 0.999, dur)}<path class="s-mute" d="M{180 + side*12},{f(y)}H{180 + side*44}" stroke-width="1" stroke-dasharray="2 3"/>'
                 f'{text(180 + side*62, y + 5, lab, "t-acc" if v else "t-red")}</g>')
    o.append(f'<circle class="f-ink" cx="180" r="9">{anim("cy", nums([ybase - sc * h for h in hs]), dur)}</circle>')
    sy = ';'.join(f'1 {f(v / 30)}' for v in vs)
    ycs = [ybase - sc * h for h in hs]
    tr = ';'.join(f'180 {f(y)}' for y in ycs)
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{tr}" keyTimes="{times(n)}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<g><animateTransform attributeName="transform" type="scale" values="{sy}" keyTimes="{times(n)}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<path class="s-acc" d="M0,-11V-44" stroke-width="2.6" vector-effect="non-scaling-stroke"/><path class="f-acc" d="M-5,-40L0,-50L5,-40Z"/></g></g>')
    o.append(text(60, 30, 'скорость, м/с:', 't-s', 'start'))
    o.append(text(300, 30, 'g ↓ всё время', 't-red', 'end'))
    return ''.join(o)


@fig('circle-motion', 'Движение по окружности: радиус поворачивается на угол φ, угловая скорость ω — угол за единицу времени, линейная скорость υ — по касательной', 360, 220)
def circle_motion():
    cx, cy, r, dur = 150, 110, 80, 6
    o = [markers('circle-motion', ('acc',))]
    o.append(f'<circle class="s-mute" cx="{cx}" cy="{cy}" r="{r}" stroke-width="1.6" stroke-dasharray="4 5"/>')
    arc = f'M{cx+30},{cy}A30,30 0 1 0 {cx-30},{cy}A30,30 0 1 0 {cx+30},{cy}'
    o.append(f'<path class="s-red" d="{arc}" stroke-width="3" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100">'
             f'<animate attributeName="stroke-dashoffset" values="100;0" dur="{dur}s" repeatCount="indefinite"/></path>')
    o.append(f'<line class="s-mute" x1="{cx}" y1="{cy}" x2="{cx+r}" y2="{cy}" stroke-width="1.2"/>')
    g = (f'<g><animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};-360 {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>'
         f'<line class="s-ink" x1="{cx}" y1="{cy}" x2="{cx+r}" y2="{cy}" stroke-width="2"/>'
         + mline('circle-motion', cx + r, cy, cx + r, cy - 48, 'acc', 2.6)
         + f'<circle class="f-ink" cx="{cx+r}" cy="{cy}" r="7"/></g>')
    o.append(g + f'<circle class="f-ink" cx="{cx}" cy="{cy}" r="3"/>')
    o.append(text(cx + 40, cy - 8, 'φ', 't-red', 'start'))
    o.append(text(250, 60, 'ω = φ / t', 't', 'start') + text(250, 86, 'υ — по', 't-acc', 'start') + text(250, 104, 'касательной', 't-acc', 'start')
             + text(250, 130, 'T — один оборот', 't-s', 'start'))
    return ''.join(o)


@fig('cp-accel', 'Центростремительное ускорение: значение скорости постоянно, а направление меняется — ускорение направлено к центру', 360, 220)
def cp_accel():
    cx, cy, r, dur = 150, 110, 80, 5
    o = [markers('cp-accel', ('acc', 'red'))]
    o.append(f'<circle class="s-mute" cx="{cx}" cy="{cy}" r="{r}" stroke-width="1.6"/>')
    for k in range(8):
        a = math.radians(k * 45)
        x, y = cx + r * math.cos(a), cy - r * math.sin(a)
        tx, ty = -math.sin(a), -math.cos(a)
        o.append(f'<line class="s-acc" x1="{f(x)}" y1="{f(y)}" x2="{f(x + 24*tx)}" y2="{f(y + 24*ty)}" stroke-width="1.2" stroke-opacity="0.35" marker-end="url(#cp-accel-m-acc)"/>')
    g = (f'<g><animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};-360 {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>'
         + mline('cp-accel', cx + r, cy, cx + r, cy - 50, 'acc', 2.8)
         + mline('cp-accel', cx + r - 6, cy, cx + r - 46, cy, 'red', 2.8)
         + f'<circle class="f-ink" cx="{cx+r}" cy="{cy}" r="7"/></g>')
    o.append(g + f'<circle class="f-ink" cx="{cx}" cy="{cy}" r="3"/>')
    o.append(text(258, 74, 'υ = const', 't-acc', 'start') + text(258, 98, 'направление υ', 't-s', 'start') + text(258, 114, 'меняется', 't-s', 'start')
             + text(258, 146, 'aₙ — к центру', 't-red', 'start'))
    return ''.join(o)


@fig('belt-drive', 'Ленточная передача: у шкивов одинаковая линейная скорость υ₁ = υ₂, а меньший шкив вращается быстрее, ω₁ > ω₂', 360, 210)
def belt_drive():
    c1, r1, c2, r2, cy = (80, 26, 248, 58, 100)
    T2 = 12.0
    T1 = T2 * r1 / r2
    belt_v = 2 * math.pi * r2 / T2  # линейная скорость ленты = скорости обода
    o = []
    # лента: касательные (упрощённо — горизонтальные отрезки сверху и снизу шкивов)
    belt = f'M{c1},{cy-r1}L{c2},{cy-r2}A{r2},{r2} 0 0 1 {c2},{cy+r2}L{c1},{cy+r1}A{r1},{r1} 0 0 1 {c1},{cy-r1}Z'
    o.append(f'<path class="s-ink" d="{belt}" stroke-width="3" fill="none"/>')
    o.append(f'<path class="s-red" d="{belt}" stroke-width="3" stroke-dasharray="6 14" fill="none">{flow(f(20 / belt_v), 20)}</path>')
    for c, r, T, lab in [(c1, r1, T1, '1'), (c2, r2, T2, '2')]:
        spokes = ''.join(f'<line class="s-ink" x1="{c}" y1="{cy}" x2="{f(c + (r-4)*math.cos(math.radians(a)))}" y2="{f(cy + (r-4)*math.sin(math.radians(a)))}" stroke-width="2"/>' for a in (0, 120, 240))
        o.append(f'<circle class="f-soft s-acc" cx="{c}" cy="{cy}" r="{r}" stroke-width="2"/>')
        o.append(f'<g><animateTransform attributeName="transform" type="rotate" values="0 {c} {cy};360 {c} {cy}" dur="{f(T)}s" repeatCount="indefinite"/>{spokes}</g>')
        o.append(f'<circle class="f-ink" cx="{c}" cy="{cy}" r="4"/>' + text(c, cy + r + 22, f'R{"₁" if lab=="1" else "₂"}', 't'))
    o.append(text(180, 198, 'υ₁ = υ₂, R₁ < R₂ ⇒ ω₁ > ω₂', 't-s'))
    return ''.join(o)


@fig('horizontal', 'Горизонтальный бросок: тела с разной горизонтальной скоростью и без неё падают с одной высоты одновременно', 360, 230)
def horizontal():
    dur, n = 4, 31
    o = [ground(10, 350, 214), '<rect class="f-mute" x="10" y="30" width="24" height="184" opacity="0.35"/>']
    h, x0 = 176, 44
    tline = [30 + h * t * t for t in lin(0, 1, n)]
    ktl = ';'.join(f(0.75 * t) for t in lin(0, 1, n)) + ';1'
    o.append(f'<line class="s-mute" x1="20" x2="350" stroke-width="1" stroke-dasharray="4 4"><animate attributeName="y1" values="{nums(tline)};{f(tline[-1])}" keyTimes="{ktl}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y2" values="{nums(tline)};{f(tline[-1])}" keyTimes="{ktl}" dur="{dur}s" repeatCount="indefinite"/></line>')
    for k, (v, cls, lab) in enumerate([(0, 'f-ink', 'υ₀ = 0'), (100, 'f-acc', 'υ₀ = 20 м/с'), (250, 'f-red', 'υ₀ = 50 м/с')]):
        ts = lin(0, 1, n)
        xs = [x0 + v * t for t in ts]
        ys = [30 + h * t * t for t in ts]
        kt = [0.75 * t for t in ts] + [1]
        kts = ';'.join(f(q) for q in kt)
        pts = 'L'.join(f'{f(x)},{f(y)}' for x, y in zip(xs, ys))
        o.append(f'<path class="s-mute" d="M{pts}" stroke-width="1.2" stroke-dasharray="3 4"/>')
        o.append(f'<circle class="{cls}" r="8"><animate attributeName="cx" values="{";".join(f(x) for x in xs)};{f(xs[-1])}" keyTimes="{kts}" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="cy" values="{";".join(f(y) for y in ys)};{f(ys[-1])}" keyTimes="{kts}" dur="{dur}s" repeatCount="indefinite"/></circle>')
        o.append(f'<circle class="{cls}" cx="{232}" cy="{f(52 + 18 * k)}" r="5"/>' + text(242, 56 + 18 * k, lab, 't-s', 'start'))
    o.append(text(196, 22, 't₁ = t₂ = t₃ — все на одной высоте', 't-s'))
    return ''.join(o)


@fig('projectile', 'Бросок под углом: траектория — парабола, горизонтальная скорость постоянна, вертикальная сначала уменьшается, потом растёт', 360, 220)
def projectile():
    dur, n = 5, 41
    v0, a = 30, math.radians(55)
    vx, vy0 = v0 * math.cos(a), v0 * math.sin(a)
    T = 2 * vy0 / G
    sx = 300 / (vx * T)
    sy = 1.8
    x0, y0 = 30, 200
    ts = lin(0, T, n)
    xs = [x0 + sx * vx * t for t in ts]
    ys = [y0 - sy * (vy0 * t - G * t * t / 2) for t in ts]
    vys = [vy0 - G * t for t in ts]
    k = 2.0
    o = [markers('projectile', ('acc', 'grn', 'red')), ground(10, 350, y0 + 4)]
    o.append(f'<path class="s-mute" d="M{"L".join(f"{f(x)},{f(y)}" for x, y in zip(xs, ys))}" stroke-width="1.2" stroke-dasharray="3 4"/>')
    kt = [0.85 * t / T for t in ts] + [1]
    kts = ';'.join(f(q) for q in kt)
    def a_(vals):
        return ';'.join(f(v) for v in vals) + ';' + f(vals[-1])
    def ln(color, x2s, y2s):
        return (f'<line class="s-{color}" stroke-width="2.4" marker-end="url(#projectile-m-{color})">'
                f'<animate attributeName="x1" values="{a_(xs)}" keyTimes="{kts}" dur="{dur}s" repeatCount="indefinite"/>'
                f'<animate attributeName="y1" values="{a_(ys)}" keyTimes="{kts}" dur="{dur}s" repeatCount="indefinite"/>'
                f'<animate attributeName="x2" values="{a_(x2s)}" keyTimes="{kts}" dur="{dur}s" repeatCount="indefinite"/>'
                f'<animate attributeName="y2" values="{a_(y2s)}" keyTimes="{kts}" dur="{dur}s" repeatCount="indefinite"/></line>')
    o.append(ln('grn', [x + k * vx for x in xs], ys))
    o.append(ln('acc', xs, [y - k * v for y, v in zip(ys, vys)]))
    o.append(ln('red', [x + k * vx for x in xs], [y - k * v for y, v in zip(ys, vys)]))
    o.append(f'<circle class="f-ink" r="7"><animate attributeName="cx" values="{a_(xs)}" keyTimes="{kts}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="cy" values="{a_(ys)}" keyTimes="{kts}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append('<g transform="translate(200,26)"><line class="s-grn" x1="0" y1="0" x2="14" y2="0" stroke-width="2.4"/>' + text(18, 4, 'υx = const', 't-grn', 'start')
             + '<line class="s-acc" x1="0" y1="20" x2="14" y2="20" stroke-width="2.4"/>' + text(18, 24, 'υy', 't-acc', 'start')
             + '<line class="s-red" x1="70" y1="20" x2="84" y2="20" stroke-width="2.4"/>' + text(88, 24, 'υ', 't-red', 'start') + '</g>')
    return ''.join(o)


# ───────────────────────────── динамика ─────────────────────────────

@fig('parallelogram', 'Сложение сил по правилу параллелограмма: при изменении угла между силами меняется равнодействующая', 360, 220)
def parallelogram():
    dur, n = 8, 41
    ox, oy = 70, 170
    F1, F2 = 130, 90
    angs = [math.radians(30 + 120 * (0.5 - 0.5 * math.cos(2 * math.pi * u))) for u in lin(0, 1, n)]
    x2 = [ox + F2 * math.cos(a) for a in angs]
    y2 = [oy - F2 * math.sin(a) for a in angs]
    xr = [ox + F1 + F2 * math.cos(a) for a in angs]
    yr = [oy - F2 * math.sin(a) for a in angs]
    o = [markers('parallelogram', ('acc', 'grn', 'red'))]
    o.append(f'<line class="s-mute" x1="{ox+F1}" y1="{oy}" stroke-width="1.2" stroke-dasharray="4 4">{anims(dur, x2=xr, y2=yr)}</line>')
    o.append(f'<line class="s-mute" stroke-width="1.2" stroke-dasharray="4 4">{anims(dur, x1=x2, y1=y2, x2=xr, y2=yr)}</line>')
    o.append(mline('parallelogram', ox, oy, ox + F1, oy, 'acc', 2.6))
    o.append(f'<line class="s-grn" x1="{ox}" y1="{oy}" stroke-width="2.6" marker-end="url(#parallelogram-m-grn)">{anims(dur, x2=x2, y2=y2)}</line>')
    o.append(f'<line class="s-red" x1="{ox}" y1="{oy}" stroke-width="3" marker-end="url(#parallelogram-m-red)">{anims(dur, x2=xr, y2=yr)}</line>')
    o.append(f'<circle class="f-ink" cx="{ox}" cy="{oy}" r="4"/>')
    o.append(text(ox + F1 / 2, oy + 22, 'F₁', 't-acc'))
    o.append(f'<text class="t-grn" text-anchor="middle">{anims(dur, x=[(ox + x) / 2 - 14 for x in x2], y=[(oy + y) / 2 for y in y2])}F₂</text>')
    o.append(f'<text class="t-red" text-anchor="start">{anims(dur, x=[x + 8 for x in xr], y=[y - 6 for y in yr])}R</text>')
    o.append(text(352, 210, 'R — диагональ параллелограмма', 't-s', 'end'))
    return ''.join(o)


@fig('newton2', 'Второй закон Ньютона: одна и та же сила F разгоняет тело массой m вдвое быстрее, чем тело массой 2m — a ~ F/m', 360, 200)
def newton2():
    dur, n = 4, 31
    o = [markers('newton2', ('red',))]
    for row, (y, mass, a, lab) in enumerate([(60, 1, 2.0, 'm'), (150, 2, 1.0, '2m')]):
        o.append(ground(10, 350, y + 22))
        ts = lin(0, 1, n)
        xs = [24 + 260 * a / 2 * t * t for t in ts]
        kt = [0.8 * t for t in ts] + [1]
        tr = ';'.join(f'{f(x - 24)} 0' for x in xs + [xs[-1]])
        w = 30 + 14 * (mass - 1)
        o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{tr}" keyTimes="{";".join(f(k) for k in kt)}" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<rect class="f-soft s-ink" x="24" y="{y - 12 - 6*(mass-1)}" width="{w}" height="{34 + 6*(mass-1)}" rx="3" stroke-width="2"/>'
                 + text(24 + w / 2, y + 10, lab, 't')
                 + mline('newton2', 24 + w, y + 4, 24 + w + 36, y + 4, 'red', 2.6) + text(24 + w + 44, y, 'F', 't-red', 'start') + '</g>')
        o.append(text(346, y - 18, f'a = {"F/m" if mass == 1 else "F/2m"}', 't-s', 'end'))
    return ''.join(o)


@fig('newton3', 'Третий закон Ньютона: тела действуют друг на друга с силами, равными по значению и противоположными по направлению', 360, 180)
def newton3():
    dur = 4
    o = [markers('newton3', ('red', 'acc')), ground(10, 350, 120)]
    kt = '0;0.25;0.45;0.9;1'
    for side, cls in [(-1, 'f-acc'), (1, 'f-red')]:
        x = 180 + side * 22
        o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 0;{side*120} 0;{side*120} 0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;0 0 1 1;0.2 0.6 0.4 1;0 0 1 1"/>'
                 f'<rect class="{cls}" x="{x - 20}" y="80" width="40" height="40" rx="4"/>' + text(x, 106, '1' if side < 0 else '2', 't-w') + '</g>')
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.1;0.42;0.46;1" dur="{dur}s" repeatCount="indefinite"/>'
             + mline('newton3', 158, 64, 112, 64, 'acc', 2.8) + mline('newton3', 202, 64, 248, 64, 'red', 2.8)
             + text(134, 52, 'F₂,₁', 't-acc') + text(226, 52, 'F₁,₂', 't-red') + '</g>')
    o.append(text(180, 160, 'F₁,₂ = −F₂,₁', 't'))
    return ''.join(o)


@fig('hooke', 'Сила упругости: чем больше груз, тем больше растяжение пружины; график F(Δl) — прямая через (1; 100), (2; 200), (3; 300)', 360, 230)
def hooke():
    dur = 8
    o = ['<path class="s-ink" d="M30,20H130" stroke-width="2"/>']
    o.append(''.join(f'<path class="s-mute" d="M{x},20l-6,-8" stroke-width="1.1"/>' for x in range(36, 131, 12)))
    stages = [0, 1, 2, 3]
    kt = '0;0.04;0.22;0.26;0.46;0.5;0.72;0.92;1'
    exts = [0, 0, 1, 1, 2, 2, 3, 3, 0]
    L0, d = 60, 28
    coils = 10
    def spring_path(L):
        pts = ['M80,20']
        seg = L / (coils + 1)
        for i in range(coils):
            pts.append(f'L{80 + (10 if i % 2 == 0 else -10)},{f(20 + seg * (i + 1))}')
        pts.append(f'L80,{f(20 + L)}')
        return ''.join(pts)
    o.append(f'<path class="s-acc" fill="none" stroke-width="2.2" d="{spring_path(L0)}"><animate attributeName="d" values="{";".join(spring_path(L0 + d*e) for e in exts)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></path>')
    ys = [20 + L0 + d * e for e in exts]
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(f"0 {f(y - (20+L0))}" for y in ys)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<path class="s-ink" d="M80,{20+L0}V{20+L0+8}" stroke-width="2"/>')
    for k in range(3):
        o.append(f'<g opacity="0"><animate attributeName="opacity" values="{";".join("1" if e > k else "0" for e in exts)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>'
                 f'<rect class="f-ink" x="64" y="{20+L0+8+k*18}" width="32" height="16" rx="2"/></g>')
    o.append('</g>')
    # график
    gx, gy = 200, 200
    o.append(arrow(gx, gy, 350, gy, 's-ink', 'f-ink', 1.4, 6) + arrow(gx, gy, gx, 40, 's-ink', 'f-ink', 1.4, 6))
    o.append(text(gx + 12, 50, 'F', 't', 'start') + text(346, gy + 18, 'Δl', 't', 'end'))
    o.append(f'<path class="s-mute" d="M{gx},{gy}L{gx+120},{gy-120}" stroke-width="1.2" stroke-dasharray="4 4"/>')
    for k in range(1, 4):
        x, y = gx + 40 * k, gy - 40 * k
        t0 = [0.22, 0.46, 0.72][k - 1]
        o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{f(t0)};{f(t0+0.01)};0.92;1" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<circle class="f-red" cx="{x}" cy="{y}" r="5"/>{text(x, gy + 16, str(k), "t-s")}{text(gx - 6, y + 4, str(100 * k), "t-s", "end")}</g>')
    o.append(text(300, 70, 'F = kΔl', 't'))
    return ''.join(o)


@fig('gravity', 'Закон всемирного тяготения: при увеличении расстояния вдвое сила притяжения уменьшается в четыре раза', 360, 180)
def gravity():
    dur, n = 6, 41
    o = [markers('gravity', ('red',))]
    rs = [70 + 70 * (0.5 - 0.5 * math.cos(2 * math.pi * u)) for u in lin(0, 1, n)]  # 70…140
    c = 180
    x1 = [c - r for r in rs]
    x2 = [c + r for r in rs]
    Fl = [56 * (70 / r) ** 2 for r in rs]
    o.append(f'<circle class="f-acc" cy="90" r="20">{anim("cx", nums(x1), dur)}</circle>')
    o.append(f'<circle class="f-ink" cy="90" r="14">{anim("cx", nums(x2), dur)}</circle>')
    o.append(f'<line class="s-red" y1="90" y2="90" stroke-width="3" marker-end="url(#gravity-m-red)">{anims(dur, x1=[x + 22 for x in x1], x2=[x + 22 + l for x, l in zip(x1, Fl)])}</line>')
    o.append(f'<line class="s-red" y1="90" y2="90" stroke-width="3" marker-end="url(#gravity-m-red)">{anims(dur, x1=[x - 16 for x in x2], x2=[x - 16 - l for x, l in zip(x2, Fl)])}</line>')
    o.append(f'<line class="s-mute" y1="130" y2="130" stroke-width="1.2">{anims(dur, x1=x1, x2=x2)}</line>')
    o.append(f'<text class="t" y="150" text-anchor="middle" x="{c}">R</text>')
    o.append(text(180, 30, 'F ~ m₁m₂ / R²: R × 2 → F : 4', 't-s'))
    return ''.join(o)


@fig('satellite', 'Спутник на круговой орбите: в конспекте сила притяжения Земли равна центробежной, F_з = F_цб', 360, 220)
def satellite():
    cx, cy, R, dur = 150, 110, 82, 7
    o = [markers('satellite', ('red', 'acc', 'grn'))]
    o.append(f'<circle class="f-soft s-acc" cx="{cx}" cy="{cy}" r="38" stroke-width="2"/>' + text(cx, cy + 5, 'Земля', 't-s'))
    o.append(f'<circle class="s-mute" cx="{cx}" cy="{cy}" r="{R}" stroke-width="1.4" stroke-dasharray="4 5"/>')
    g = (f'<g><animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};-360 {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>'
         + mline('satellite', cx + R - 8, cy, cx + R - 36, cy, 'red', 2.6)
         + mline('satellite', cx + R + 8, cy, cx + R + 36, cy, 'grn', 2.6)
         + mline('satellite', cx + R, cy - 8, cx + R, cy - 46, 'acc', 2.6)
         + f'<rect class="f-ink" x="{cx+R-6}" y="{cy-6}" width="12" height="12" rx="2"/><path class="s-ink" d="M{cx+R-14},{cy}H{cx+R+14}" stroke-width="3"/></g>')
    o.append(g)
    o.append('<g transform="translate(262,70)">' + '<line class="s-red" x1="0" y1="0" x2="14" y2="0" stroke-width="2.4"/>' + text(20, 4, 'F_з', 't-red', 'start')
             + '<line class="s-grn" x1="0" y1="24" x2="14" y2="24" stroke-width="2.4"/>' + text(20, 28, 'F_цб', 't-grn', 'start')
             + '<line class="s-acc" x1="0" y1="48" x2="14" y2="48" stroke-width="2.4"/>' + text(20, 52, 'υ', 't-acc', 'start') + '</g>')
    o.append(text(300, 160, 'F_з = F_цб', 't'))
    return ''.join(o)


@fig('elevator', 'Вес тела в лифте: при ускорении вверх P > mg, при равномерном движении P = mg, при ускорении вниз (торможении на подъёме) P < mg', 360, 230)
def elevator():
    dur, n = 10, 13
    # подъём: разгон (a ↑), равномерно, торможение (a ↓) — по кинематике, путь 30 + 60 + 30 px
    kt, ys, P = [0, 0.06], [0, 0], [1, 1]
    for i in range(1, n):
        u = i / (n - 1)
        kt.append(0.06 + 0.25 * u); ys.append(-30 * u * u); P.append(1.4)
    for i in range(1, n):
        u = i / (n - 1)
        kt.append(0.31 + 0.25 * u); ys.append(-30 - 60 * u); P.append(1.0)
    for i in range(1, n):
        u = i / (n - 1)
        kt.append(0.56 + 0.25 * u); ys.append(-90 - 30 * (2 * u - u * u)); P.append(0.6)
    kt += [0.811, 0.92, 1]; ys += [-120, -120, -120]; P += [1, 1, 1]
    P = [1.4 if 0.06 <= k < 0.309 else 1.0 if k < 0.559 else 0.6 if k < 0.809 else 1.0 for k in kt]  # discrete: значение действует до следующего ключа
    ktv = ';'.join(f(k) for k in kt)
    o = ['<path class="s-mute" d="M110,36V222M210,36V222" stroke-width="1.2"/>']
    o.append(f'<g><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.04;0.95;1" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animateTransform attributeName="transform" type="translate" values="{";".join(f"0 {f(y)}" for y in ys)}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite"/>'
             '<rect class="f-soft s-ink" x="114" y="160" width="92" height="60" rx="4" stroke-width="2"/>'
             '<circle class="f-ink" cx="160" cy="174" r="6"/><path class="s-ink" d="M160,180V200M160,186L151,195M160,186L169,195M160,200L154,212M160,200L166,212" stroke-width="2.4"/>'
             '<rect class="f-mute" x="146" y="212" width="28" height="6" rx="2"/></g>')
    hs = [60 * p for p in P]
    o.append('<rect class="s-mute" x="262" y="80" width="34" height="120" stroke-width="1" stroke-dasharray="3 3"/>')
    o.append('<path class="s-ink" d="M256,140H302" stroke-width="1.4" stroke-dasharray="3 3"/>' + text(306, 144, 'mg', 't-s', 'start'))
    o.append(f'<rect class="f-acc" x="262" width="34"><animate attributeName="height" values="{nums(hs)}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>'
             f'<animate attributeName="y" values="{nums([200 - h for h in hs])}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></rect>')
    o.append(text(279, 218, 'вес P', 't'))
    for lab, a, b in [('разгон вверх (a ↑): P > mg', 0.06, 0.31), ('равномерно (a = 0): P = mg', 0.31, 0.56), ('торможение (a ↓): P < mg', 0.56, 0.81)]:
        o.append(f'<text class="t" x="180" y="22" text-anchor="middle" opacity="0">{subs(lab)}<animate attributeName="opacity" values="0;1;0" keyTimes="0;{f(a)};{f(b)}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>')
    return ''.join(o)

@fig('block-forces', 'Динамическое уравнение: на брусок действуют N, mg и сила F₁; N = mg, а ma = F₁ — брусок разгоняется', 360, 200)
def block_forces():
    dur, n = 4, 31
    o = [markers('block-forces', ('red', 'acc', 'grn', 'ink')), ground(10, 350, 150)]
    ts = lin(0, 1, n)
    xs = [30 + 200 * t * t for t in ts]
    kt = [0.8 * t for t in ts] + [1]
    tr = ';'.join(f'{f(x - 30)} 0' for x in xs + [xs[-1]])
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{tr}" keyTimes="{";".join(f(k) for k in kt)}" dur="{dur}s" repeatCount="indefinite"/>'
             '<rect class="f-soft s-ink" x="30" y="110" width="56" height="40" rx="3" stroke-width="2"/>' + text(58, 135, 'm', 't')
             + mline('block-forces', 58, 110, 58, 64, 'grn', 2.6) + text(66, 72, 'N', 't-grn', 'start')
             + mline('block-forces', 58, 150, 58, 192, 'acc', 2.6) + text(66, 190, 'mg', 't-acc', 'start')
             + mline('block-forces', 86, 130, 128, 130, 'red', 2.6) + text(110, 122, 'F₁', 't-red')
             + mline('block-forces', 40, 96, 74, 96, 'ink', 2) + text(36, 92, 'a', 't', 'end') + '</g>')
    o.append(text(352, 30, 'N = mg', 't', 'end') + text(352, 52, 'ma = F₁', 't', 'end'))
    return ''.join(o)


@fig('friction', 'Сила трения: пока F < μN, трение покоя равно F и тело стоит; при F = μN трение скольжения перестаёт расти и тело трогается', 360, 230)
def friction():
    dur, n = 8, 41
    A = 60  # предел μN в пикселях стрелки
    us = lin(0, 1, n)
    Fs = [100 * u for u in us]  # 0…100
    Ft = [min(F, A) for F in Fs]
    xs = []
    v, x = 0, 0
    for i, F in enumerate(Fs):
        if i:
            dt = 1 / (n - 1)
            acc = max(F - A, 0) * 4
            v += acc * dt
            x += v * dt
        xs.append(x)
    o = [markers('friction', ('red', 'acc')), ground(10, 220, 100)]
    tr = ';'.join(f'{f(x)} 0' for x in xs)
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{tr}" keyTimes="{times(n)}" dur="{dur}s" repeatCount="indefinite"/>'
             '<rect class="f-soft s-ink" x="60" y="60" width="50" height="40" rx="3" stroke-width="2"/>'
             f'<line class="s-red" x1="110" y1="80" y2="80" stroke-width="2.6" marker-end="url(#friction-m-red)">{anim("x2", nums([112 + F for F in Fs]), dur)}</line>'
             f'<line class="s-acc" x1="60" y1="96" y2="96" stroke-width="2.6" marker-end="url(#friction-m-acc)">{anim("x2", nums([58 - t for t in Ft]), dur)}</line>'
             + text(85, 52, '', 't') + '</g>')
    o.append(text(20, 30, 'F', 't-red', 'start') + text(40, 30, '— тянем', 't-s', 'start') + text(110, 30, 'F_т', 't-acc', 'start') + text(136, 30, '— трение', 't-s', 'start'))
    # график F_т(F)
    gx, gy, w = 240, 200, 110
    o.append(arrow(gx, gy, gx + w + 6, gy, 's-ink', 'f-ink', 1.4, 6) + arrow(gx, gy, gx, 110, 's-ink', 'f-ink', 1.4, 6))
    o.append(text(gx + 8, 120, 'F_т', 't-s', 'start') + text(gx + w + 4, gy + 16, 'F', 't-s', 'end'))
    px = [gx + w * F / 100 for F in Fs]
    py = [gy - 70 * t / A * 0.857 for t in Ft]
    o.append(f'<path class="s-mute" d="M{gx},{gy}L{f(gx + w*A/100)},{f(gy - 60)}H{gx+w}" stroke-width="1.2" stroke-dasharray="3 4"/>')
    o.append(f'<circle class="f-red" r="5">{anims(dur, cx=px, cy=py)}</circle>')
    o.append(text(gx + 20, 222, 'покой', 't-s', 'start') + text(gx + w, 132, 'скольжение', 't-s', 'end'))
    o.append(text(20, 140, 'F < μN — покой,', 't-s', 'start') + text(20, 160, 'F > μN — движение', 't-s', 'start'))
    return ''.join(o)


@fig('incline', 'Наклонная плоскость: сила тяжести раскладывается на силу скольжения F_с = mg sin α и давящую силу F_д = mg cos α; когда tg α становится больше μ, тело начинает скользить', 360, 228)
def incline():
    dur, n = 10, 26
    mu = 0.5
    a_crit = math.degrees(math.atan(mu))       # 26,6°
    px, py, L = 40, 190, 280
    a0, a1, t_rot = 15, 40, 0.5
    t_c = t_rot * (a_crit - a0) / (a1 - a0)    # момент, когда tg α = μ
    o = [markers('incline', ('red', 'acc', 'ink'))]
    kt_rot = [t_rot * u for u in lin(0, 1, n)] + [1]
    angs = lin(a0, a1, n) + [a1]
    ktr = ';'.join(f(k) for k in kt_rot)
    # скольжение с постоянным ускорением после t_c
    t_end = 0.8
    kt_s = [0, t_c] + [t_c + (t_end - t_c) * u for u in lin(0, 1, n)][1:] + [1]
    xs = [0, 0] + [-170 * u * u for u in lin(0, 1, n)][1:] + [-170]
    o.append(f'<g><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.03;0.94;1" dur="{dur}s" repeatCount="indefinite"/>'
             f'<g><animateTransform attributeName="transform" type="rotate" values="{";".join(f"{f(-a)} {px} {py}" for a in angs)}" keyTimes="{ktr}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<path class="s-ink" d="M{px},{py}H{px + L}" stroke-width="3"/>'
             f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(f"{f(x)} 0" for x in xs)}" keyTimes="{";".join(f(k) for k in kt_s)}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<rect class="f-soft s-ink" x="{px + 200}" y="{py - 30}" width="40" height="30" rx="3" stroke-width="2"/>')
    cxb, cyb = px + 220, py - 15
    sin_l = [70 * math.sin(math.radians(a)) for a in angs]
    cos_l = [70 * math.cos(math.radians(a)) for a in angs]
    o.append(f'<line class="s-red" x1="{cxb}" y1="{cyb}" y2="{cyb}" stroke-width="2.6" marker-end="url(#incline-m-red)"><animate attributeName="x2" values="{nums([cxb - v for v in sin_l])}" keyTimes="{ktr}" dur="{dur}s" repeatCount="indefinite"/></line>'
             f'<line class="s-acc" x1="{cxb}" y1="{cyb}" x2="{cxb}" stroke-width="2.6" marker-end="url(#incline-m-acc)"><animate attributeName="y2" values="{nums([cyb + v for v in cos_l])}" keyTimes="{ktr}" dur="{dur}s" repeatCount="indefinite"/></line>')
    o.append(f'<g><animateTransform attributeName="transform" type="rotate" values="{";".join(f"{f(a)} {cxb} {cyb}" for a in angs)}" keyTimes="{ktr}" dur="{dur}s" repeatCount="indefinite"/>'
             + mline('incline', cxb, cyb, cxb, cyb + 70, 'ink', 2.2) + text(cxb + 8, cyb + 64, 'mg', 't', 'start') + '</g></g></g></g>')
    o.append(f'<path class="s-ink" d="M20,{py}H350" stroke-width="1.4"/>')
    o.append(text(14, 214, 'μ = 0,5', 't-s', 'start'))
    o.append(f'<text class="t-acc" x="352" y="214" text-anchor="end">tg α &lt; μ — покоится<animate attributeName="opacity" values="1;0" keyTimes="0;{f(t_c)}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>')
    o.append(f'<text class="t-red" x="352" y="214" text-anchor="end" opacity="0">tg α &gt; μ — скользит<animate attributeName="opacity" values="0;1" keyTimes="0;{f(t_c)}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>')
    o.append('<g transform="translate(14,20)"><line class="s-red" x1="0" y1="0" x2="14" y2="0" stroke-width="2.4"/>' + text(18, 4, 'F_с = mg sin α', 't-red', 'start')
             + '<line class="s-acc" x1="0" y1="20" x2="14" y2="20" stroke-width="2.4"/>' + text(18, 24, 'F_д = mg cos α', 't-acc', 'start') + '</g>')
    return ''.join(o)

@fig('pressure-brick', 'Давление бруска: на узкой грани площадь меньше и давление больше — брусок глубже вдавливается в песок; p ~ 1/S', 360, 200)
def pressure_brick():
    dur = 4
    o = []
    for cx, w, h, depth, lab in [(100, 40, 90, 22, 'p₁ — больше'), (250, 110, 34, 7, 'p₂ — меньше')]:
        o.append(f'<rect class="f-mute" x="{cx - 75}" y="150" width="150" height="34" opacity="0.35"/>')
        o.append(f'<path class="s-ink" d="M{cx-75},150H{cx+75}" stroke-width="1.6"/>')
        dent = f'<rect class="f-paper" x="{cx - w/2}" y="150" width="{w}" height="0"><animate attributeName="height" values="0;0;{depth};{depth};0" keyTimes="0;0.3;0.55;0.9;1" dur="{dur}s" repeatCount="indefinite"/></rect>'
        o.append(dent)
        o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 -50;0 0;0 {depth};0 {depth};0 -50" keyTimes="0;0.3;0.55;0.9;1" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<rect class="f-red" x="{cx - w/2}" y="{150 - h}" width="{w}" height="{h}" rx="2"/></g>')
        o.append(text(cx, 198, lab, 't-s'))
    o.append(text(180, 24, 'F₁ = F₂ = mg, но S₁ < S₂', 't-s'))
    return ''.join(o)


@fig('hydrostatic', 'Гидростатическое давление p = ρgh: чем глубже датчик, тем больше давление', 360, 230)
def hydrostatic():
    dur, n = 6, 31
    o = ['<path class="s-ink" d="M40,30V210H200V30" stroke-width="3" fill="none"/>', '<rect class="f-soft" x="42" y="50" width="156" height="158"/>']
    o.append('<path class="s-acc" d="M42,50H198" stroke-width="2"/>')
    ds = [60 + 120 * (0.5 - 0.5 * math.cos(2 * math.pi * u)) for u in lin(0, 1, n)]
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(f"0 {f(d)}" for d in ds)}" keyTimes="{times(n)}" dur="{dur}s" repeatCount="indefinite"/>'
             '<circle class="f-paper s-ink" cx="120" cy="0" r="10" stroke-width="2"/><path class="s-ink" d="M120,-10V-80" stroke-width="1.6"/></g>')
    o.append(f'<line class="s-red" x1="210" y1="50" x2="210" stroke-width="1.6">{anim("y2", nums([50 + d for d in ds]), dur)}</line>')
    o.append(f'<text class="t-red" x="218">{anim("y", nums([50 + d / 2 for d in ds]), dur)}h</text>')
    hb = [d * 0.8 for d in ds]
    o.append('<rect class="s-mute" x="290" y="40" width="30" height="170" stroke-width="1" stroke-dasharray="3 3"/>')
    o.append(f'<rect class="f-acc" x="290" width="30">{anim("height", nums(hb), dur)}{anim("y", nums([210 - h for h in hb]), dur)}</rect>')
    o.append(text(305, 226, 'p', 't'))
    o.append(text(305, 30, 'p ~ h', 't-s'))
    return ''.join(o)


@fig('pascal', 'Закон Паскаля: давление поршня передаётся жидкостью во все стороны одинаково — струи из всех отверстий одинаковые', 360, 210)
def pascal():
    dur = 3
    cx, cy, R = 230, 110, 46
    o = [f'<rect class="f-soft s-ink" x="40" y="96" width="150" height="28" stroke-width="2"/>']
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;60 0;0 0" keyTimes="0;0.6;1" dur="{dur}s" repeatCount="indefinite"/>'
             '<rect class="f-ink" x="46" y="98" width="10" height="24"/><path class="s-ink" d="M20,110H46" stroke-width="4"/></g>')
    o.append(f'<circle class="f-soft s-ink" cx="{cx}" cy="{cy}" r="{R}" stroke-width="2"/>')
    for k in range(8):
        a = math.radians(-90 + k * 45)
        if abs(math.degrees(a) - 180) < 1 or abs(math.degrees(a) + 180) < 1:
            continue
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        x2, y2 = cx + (R + 40) * math.cos(a), cy + (R + 40) * math.sin(a)
        o.append(f'<line class="s-acc" x1="{f(x)}" y1="{f(y)}" x2="{f(x2)}" y2="{f(y2)}" stroke-width="3" stroke-dasharray="4 6" stroke-linecap="round">'
                 f'{flow(0.6, 10)}<animate attributeName="opacity" values="0.15;1;0.15" keyTimes="0;0.6;1" dur="{dur}s" repeatCount="indefinite"/></line>')
    o.append(text(180, 200, 'давление передаётся во всех направлениях одинаково', 't-s'))
    return ''.join(o)


@fig('communicating', 'Сообщающиеся сосуды: однородная жидкость в сосудах разной формы устанавливается на одном уровне', 360, 220)
def communicating():
    dur, n = 6, 31
    us = lin(0, 1, n)
    eq, chan = 96, 165
    amp = [52 * math.exp(-4 * u) * math.cos(6 * u) for u in us]
    vessels = [  # (внутренность сосуда, x-диапазон, уровень)
        ('M40,24H76V170H40Z', 40, 76, [eq - a for a in amp]),
        ('M104,24H186L160,170H130Z', 104, 186, [eq + 0.45 * a for a in amp]),
        ('M290,24H316L276,170H250Z', 250, 316, [eq + 0.45 * a for a in amp]),
    ]
    o = ['<defs>' + ''.join(f'<clipPath id="communicating-c{i}"><path d="{d}"/></clipPath>' for i, (d, *_r) in enumerate(vessels)) + '</defs>']
    o.append(f'<rect class="f-soft" x="40" y="{chan}" width="236" height="25"/>')
    for i, (d, x1, x2, lv) in enumerate(vessels):
        o.append(f'<g clip-path="url(#communicating-c{i})"><rect class="f-soft" x="{x1}" width="{x2 - x1}">{anim("y", nums(lv), dur)}{anim("height", nums([chan + 0.5 - l for l in lv]), dur)}</rect>'
                 f'<line class="s-acc" x1="{x1}" x2="{x2}" stroke-width="2.4">{anims(dur, y1=lv, y2=lv)}</line></g>')
    o.append('<path class="s-ink" d="M40,24V190H276V165L316,24M76,24V165H130L104,24M186,24L160,165H250L290,24" stroke-width="2.6" fill="none" stroke-linejoin="round"/>')
    o.append(f'<path class="s-red" d="M24,{eq}H336" stroke-width="1.2" stroke-dasharray="5 4"/>')
    o.append(text(180, 212, 'уровни выравниваются', 't-s'))
    return ''.join(o)


@fig('torricelli', 'Опыт Торричелли: ртуть в трубке опускается до 760 мм — её удерживает атмосферное давление', 360, 230)
def torricelli():
    dur = 5
    top, base = 24, 196
    h760 = 120
    o = [markers('torricelli', ('red',))]
    o.append('<path class="s-ink" d="M60,170V212H300V170" stroke-width="2.4" fill="none"/><rect class="f-ink" x="62" y="186" width="236" height="24" opacity="0.55"/>')
    o.append(f'<rect class="f-paper s-ink" x="168" y="{top}" width="24" height="176" stroke-width="2"/>')
    o.append(f'<rect class="f-ink" x="170" width="20" opacity="0.75"><animate attributeName="y" values="{top+2};{top+2};{base-h760};{base-h760}" keyTimes="0;0.15;0.55;1" dur="{dur}s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;0.3 0 0.4 1;0 0 1 1"/>'
             f'<animate attributeName="height" values="{198-top};{198-top};{198-(base-h760)};{198-(base-h760)}" keyTimes="0;0.15;0.55;1" dur="{dur}s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;0.3 0 0.4 1;0 0 1 1"/></rect>')
    o.append(f'<g opacity="0">{"<animate attributeName=\"opacity\" values=\"0;0;1;1\" keyTimes=\"0;0.55;0.6;1\" dur=\"" + str(dur) + "s\" repeatCount=\"indefinite\"/>"}'
             f'<path class="s-red" d="M210,{base-h760}V{186}" stroke-width="1.6"/><path class="s-red" d="M204,{base-h760}H216M204,186H216" stroke-width="1.6"/>'
             + text(222, (base - h760 + 186) / 2 + 4, '760 мм', 't-red', 'start') + text(160, top + 26, 'пусто', 't-s', 'end') + '</g>')
    for x in (90, 130, 250, 290):
        o.append(mline('torricelli', x, 156, x, 182, 'red', 2.2))
    o.append(text(110, 150, 'p_атм', 't-red') + text(270, 150, 'p_атм', 't-red'))
    return ''.join(o)


@fig('hydraulic-press', 'Гидравлический пресс: малый поршень опускается на h₁ под силой F₁, большой поднимается на h₂ с большей силой F₂', 360, 220)
def hydraulic_press():
    dur = 4
    S1, S2 = 30, 120
    h1 = 60
    h2 = h1 * S1 / S2
    o = [markers('hydraulic-press', ('red',))]
    o.append('<path class="s-ink" d="M50,40V190H330V40M80,40V160H200V40" stroke-width="2.4" fill="none"/>')
    o.append('<rect class="f-soft" x="52" y="160" width="276" height="28"/>')
    kt = '0;0.45;0.55;1'
    o.append(f'<rect class="f-soft" x="52" width="26"><animate attributeName="y" values="70;{70+h1};{70+h1};70" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/><animate attributeName="height" values="90;{90-h1};{90-h1};90" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></rect>')
    o.append(f'<rect class="f-soft" x="202" width="126"><animate attributeName="y" values="120;{120-h2};{120-h2};120" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/><animate attributeName="height" values="40;{40+h2};{40+h2};40" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></rect>')
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 {h1};0 {h1};0 0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             '<rect class="f-ink" x="52" y="62" width="26" height="8"/>' + mline('hydraulic-press', 65, 20, 65, 58, 'red', 2.6) + text(80, 34, 'F₁', 't-red', 'start') + '</g>')
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 {-h2};0 {-h2};0 0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             '<rect class="f-ink" x="202" y="112" width="126" height="8"/>' + mline('hydraulic-press', 265, 108, 265, 56, 'red', 4) + text(282, 76, 'F₂', 't-red', 'start') + '</g>')
    o.append(text(65, 210, 'S₁', 't-s') + text(265, 210, 'S₂', 't-s'))
    o.append(text(180, 18, 'выигрыш в силе: F₂ > F₁', 't-s'))
    return ''.join(o)


@fig('archimedes', 'Закон Архимеда: погружённое тело вытесняет жидкость объёмом погружённой части, выталкивающая сила растёт, а вес на динамометре уменьшается', 360, 230)
def archimedes():
    dur, n = 8, 25
    # 0–0.45 опускаем тело, 0.45–0.9 держим, затем всё гаснет и начинается заново
    us = lin(0, 1, n)
    kt = [0.45 * u for u in us] + [1]
    ktv = ';'.join(f(k) for k in kt)
    sub = [min(max((u - 0.4) / 0.6, 0), 1) for u in us] + [1]  # доля погружения
    ys = [40 + 90 * u for u in us] + [130]

    def a(attr, v):
        return f'<animate attributeName="{attr}" values="{nums(v)}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite"/>'
    o = [markers('archimedes', ('red', 'acc'))]
    o.append(f'<g><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.03;0.9;0.97" dur="{dur}s" repeatCount="indefinite"/>')
    o.append('<path class="s-ink" d="M40,90V210H180V90" stroke-width="2.4" fill="none"/><path class="s-ink" d="M180,100H226V108" stroke-width="2.4" fill="none"/>')
    o.append('<rect class="f-soft" x="42" y="100" width="136" height="108"/>')
    # струя в стакан, пока тело погружается
    flow_on = [1 if 0 < sub[i] < 1 or (i + 1 < len(sub) and sub[i + 1] > sub[i]) else 0 for i in range(len(sub))]
    o.append(f'<path class="s-acc" d="M222,110V196" stroke-width="3" stroke-dasharray="5 6" opacity="0">{flow(0.4, 11)}'
             f'<animate attributeName="opacity" values="{nums(flow_on)}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></path>')
    o.append('<path class="s-ink" d="M196,150V214H252V150" stroke-width="2" fill="none"/>')
    o.append(f'<rect class="f-soft" x="198" width="52">{a("height", [44 * v for v in sub])}{a("y", [212 - 44 * v for v in sub])}</rect>')
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(f"0 {f(y - 40)}" for y in ys)}" keyTimes="{ktv}" dur="{dur}s" repeatCount="indefinite"/>'
             '<path class="s-ink" d="M110,-40V40" stroke-width="1.6"/><rect class="f-red" x="88" y="40" width="44" height="44" rx="3"/>'
             f'<line class="s-acc" x1="110" y1="84" x2="110" stroke-width="2.6" marker-end="url(#archimedes-m-acc)">{a("y2", [84 - 0.1 - 40 * v for v in sub])}{a("opacity", [1 if v > 0.02 else 0 for v in sub])}</line></g>')
    P = [120 - 50 * v for v in sub]
    o.append('<rect class="s-mute" x="300" y="40" width="30" height="130" stroke-width="1" stroke-dasharray="3 3"/>')
    o.append(f'<rect class="f-acc" x="300" width="30">{a("height", [p - 10 for p in P])}{a("y", [180 - p for p in P])}</rect>')
    o.append(text(315, 32, 'вес', 't-s') + text(315, 192, 'P′ = P₀ − F_A', 't-s'))
    o.append(text(110, 226, 'F_A — выталкивающая сила', 't-acc'))
    o.append('</g>')
    return ''.join(o)


@fig('floating', 'Плавание тел: тело плотнее жидкости тонет и ложится на дно, тело легче жидкости всплывает и плавает, частично погрузившись', 360, 220)
def floating():
    dur, n = 6, 41
    us = lin(0, 1, n)
    o = ['<path class="s-ink" d="M30,40V200H330V40" stroke-width="2.4" fill="none"/>', '<rect class="f-soft" x="32" y="70" width="296" height="128"/>',
         '<path class="s-acc" d="M32,70H328" stroke-width="2"/>']
    # тонущее: из y=80 до дна 170 (низ 198)
    sink = [80 + 92 * min(u / 0.6, 1) ** 1.6 for u in us]
    o.append(f'<rect class="f-ink" x="80" width="40" height="28" rx="3">{anim("y", nums(sink), dur)}</rect>')
    o.append(text(100, 34, 'ρ_т > ρ_ж — тонет', 't-s'))
    # всплывающее: из y=160 к равновесию (половина погружена: верх 56, низ 84)
    eq = 56
    rise = [eq + (160 - eq) * math.exp(-7 * u) * math.cos(8 * u) for u in us]
    o.append(f'<rect class="f-red" x="240" width="40" height="28" rx="3">{anim("y", nums(rise), dur)}</rect>')
    o.append(text(260, 34, 'ρ_т < ρ_ж — плавает', 't-s'))
    return ''.join(o)


@fig('continuity', 'Течение в трубе: в узких участках жидкость течёт быстрее, а давление в манометрических трубках ниже — Sυ = const', 360, 220)
def continuity():
    o = []
    o.append('<path class="s-ink" d="M10,120H110L140,135H220L240,145H350M10,200H110L140,185H220L240,175H350" stroke-width="2.4" fill="none"/>')
    o.append('<path class="f-soft" d="M10,120H110L140,135H220L240,145H350V175H240L220,185H140L110,200H10Z"/>')
    secs = [(10, 110, 160, 1.0, 70), (140, 220, 160, 0.5, 46), (240, 350, 160, 0.375, 30)]
    for x1, x2, y, sz, h in secs:
        dur = 1.6 * sz
        for dy in (-18 * sz / 1.0 if sz == 1 else -10 * sz / 0.5, 0, 18 * sz / 1.0 if sz == 1 else 10 * sz / 0.5):
            o.append(f'<path class="s-acc" d="M{x1},{f(y+dy)}H{x2}" stroke-width="2.4" stroke-dasharray="4 12" stroke-linecap="round">{flow(dur, 16)}</path>')
        xm = (x1 + x2) / 2
        top = 120 if sz == 1 else (135 if sz == 0.5 else 145)
        o.append(f'<path class="s-ink" d="M{xm-8},{top}V20M{xm+8},{top}V20" stroke-width="1.6"/><rect class="f-soft" x="{xm-7}" y="{top-h}" width="14" height="{h}"/>')
    o.append(text(60, 216, 'S₁: υ₁, p₁', 't-s') + text(180, 216, 'S₂: υ₂, p₂', 't-s') + text(295, 216, 'S₃: υ₃, p₃', 't-s'))
    o.append(text(352, 14, 'υ₁ < υ₂ < υ₃, p₁ > p₂ > p₃', 't-s', 'end'))
    return ''.join(o)


# ───────────────────────────── законы сохранения ─────────────────────────────

@fig('elastic-collision', 'Упругое столкновение одинаковых шаров: первый шар останавливается, второй уходит с его скоростью — тела меняются скоростями', 360, 170)
def elastic_collision():
    dur = 5
    o = [markers('elastic-collision', ('acc', 'red')), ground(10, 350, 120)]
    kt = '0;0.4;1'
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;110 0;110 0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             '<circle class="f-acc" cx="40" cy="98" r="20"/>' + text(40, 104, '1', 't-w')
             + f'<g>{"<animate attributeName=\"opacity\" values=\"1;1;0;0\" keyTimes=\"0;0.4;0.401;1\" dur=\"" + str(dur) + "s\" repeatCount=\"indefinite\"/>"}' + mline('elastic-collision', 40, 60, 84, 60, 'acc', 2.6) + text(62, 52, 'υ', 't-acc') + '</g></g>')
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;150 0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             '<circle class="f-red" cx="190" cy="98" r="20"/>' + text(190, 104, '2', 't-w')
             + f'<g opacity="0">{"<animate attributeName=\"opacity\" values=\"0;0;1;1\" keyTimes=\"0;0.4;0.401;1\" dur=\"" + str(dur) + "s\" repeatCount=\"indefinite\"/>"}' + mline('elastic-collision', 190, 60, 234, 60, 'red', 2.6) + text(212, 52, 'υ', 't-red') + '</g></g>')
    o.append(text(180, 156, 'm₁ = m₂: шары меняются скоростями', 't-s'))
    return ''.join(o)


@fig('inelastic', 'Неупругое столкновение: тележки сцепляются и едут вместе с меньшей скоростью u, часть энергии переходит в теплоту Q', 360, 170)
def inelastic():
    dur = 5
    o = [markers('inelastic', ('acc', 'red')), ground(10, 350, 120)]
    kt = '0;0.4;1'
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;116 0;196 0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             '<rect class="f-acc" x="20" y="80" width="50" height="34" rx="3"/>' + text(45, 102, 'm₁', 't-w') + '</g>')
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;80 0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             '<rect class="f-red" x="186" y="80" width="50" height="34" rx="3"/>' + text(211, 102, 'm₂', 't-w') + '</g>')
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.4;0.45;0.6;1" dur="{dur}s" repeatCount="indefinite"/>'
             '<circle class="f-red-soft" cx="186" cy="97" r="26"/>' + text(186, 62, 'Q', 't-red') + '</g>')
    o.append(f'<g>{"<animate attributeName=\"opacity\" values=\"1;1;0;0\" keyTimes=\"0;0.4;0.401;1\" dur=\"" + str(dur) + "s\" repeatCount=\"indefinite\"/>"}' + text(90, 50, 'υ₁ →', 't-acc') + text(260, 50, 'υ₂ = 0', 't-s') + '</g>')
    o.append(f'<g opacity="0">{"<animate attributeName=\"opacity\" values=\"0;0;1;1\" keyTimes=\"0;0.45;0.46;1\" dur=\"" + str(dur) + "s\" repeatCount=\"indefinite\"/>"}' + text(250, 50, 'вместе со скоростью u →', 't-acc') + '</g>')
    o.append(text(180, 156, 'm₁υ₁ = (m₁ + m₂)u', 't-s'))
    return ''.join(o)


@fig('wall-bounce', 'Удар о стенку: при упругом ударе мяч отскакивает с той же скоростью (Δp = 2mυ), при неупругом останавливается (Δp = mυ)', 360, 200)
def wall_bounce():
    dur = 4
    o = [markers('wall-bounce', ('acc', 'red')), '<rect class="f-mute" x="300" y="14" width="16" height="176" opacity="0.6"/>', '<path class="s-ink" d="M300,14V190" stroke-width="2.4"/>']
    kt = '0;0.5;0.5001;1'
    o.append(text(20, 24, 'упругий: отскок с той же υ — Δp = 2mυ', 't-s', 'start'))
    o.append(f'<circle class="f-acc" cy="74" r="16"><animate attributeName="cx" values="70;284;70" keyTimes="0;0.5;1" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(f'<line class="s-acc" y1="46" y2="46" stroke-width="2.6" marker-end="url(#wall-bounce-m-acc)"><animate attributeName="x1" values="55;269;299;85" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
             f'<animate attributeName="x2" values="85;299;269;55" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></line>')
    o.append(text(20, 114, 'неупругий: остановка — Δp = mυ', 't-s', 'start'))
    o.append(f'<circle class="f-red" cy="164" r="16"><animate attributeName="cx" values="70;284;284" keyTimes="0;0.5;1" dur="{dur}s" repeatCount="indefinite"/></circle>')
    o.append(f'<line class="s-red" y1="136" y2="136" stroke-width="2.6" marker-end="url(#wall-bounce-m-red)"><animate attributeName="x1" values="55;269" keyTimes="0;1" dur="{f(dur / 2)}s" repeatCount="indefinite"/>'
             f'<animate attributeName="x2" values="85;299" keyTimes="0;1" dur="{f(dur / 2)}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="1;0" keyTimes="0;0.5" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></line>')
    return ''.join(o)


@fig('work-sign', 'Знак работы A = FS cos α: при α < 90° работа положительна, при 90° равна нулю, при α > 90° отрицательна', 360, 220)
def work_sign():
    dur, n = 8, 41
    angs = [180 * (0.5 - 0.5 * math.cos(2 * math.pi * u)) for u in lin(0, 1, n)]
    o = [markers('work-sign', ('red', 'acc')), ground(10, 250, 150)]
    o.append('<rect class="f-soft s-ink" x="100" y="110" width="50" height="40" rx="3" stroke-width="2"/>')
    o.append(mline('work-sign', 100, 172, 200, 172, 'acc', 2.4) + text(150, 192, 'S', 't-acc'))
    L = 70
    o.append(f'<line class="s-red" x1="125" y1="130" stroke-width="2.8" marker-end="url(#work-sign-m-red)">{anims(dur, x2=[125 + L * math.cos(math.radians(a)) for a in angs], y2=[130 - L * math.sin(math.radians(a)) for a in angs])}</line>')
    o.append(f'<text class="t-red" text-anchor="middle">F{anims(dur, x=[125 + (L + 14) * math.cos(math.radians(a)) for a in angs], y=[134 - (L + 14) * math.sin(math.radians(a)) for a in angs])}</text>')
    # индикатор A
    cosv = [math.cos(math.radians(a)) for a in angs]
    bx, by = 300, 110
    o.append(f'<rect class="s-mute" x="{bx-14}" y="{by-70}" width="28" height="140" stroke-width="1" stroke-dasharray="3 3"/><path class="s-ink" d="M{bx-20},{by}H{bx+20}" stroke-width="1.4"/>')
    o.append(f'<rect class="f-acc" x="{bx-14}" width="28">{anims(dur, y=[by - 70 * max(c, 0) for c in cosv], height=[70 * abs(c) for c in cosv])}</rect>')
    o.append(text(bx, 30, 'A', 't') + text(bx + 22, by - 50, '+', 't-s', 'start') + text(bx + 22, by + 56, '−', 't-s', 'start'))
    o.append(text(bx, 206, 'A = FS cos α', 't-s'))
    return ''.join(o)


@fig('energy-fall', 'Закон сохранения механической энергии: при подъёме и падении W_к и W_п меняются, их сумма постоянна; на половине высоты W_к = W_п', 360, 230)
def energy_fall():
    dur, n = 5, 41
    ts = lin(0, 1, n)
    hs = [4 * t * (1 - t) for t in ts]  # 0…1…0
    ybase, H = 206, 170
    o = [ground(60, 200, ybase + 10)]
    o.append(f'<path class="s-red" d="M60,{ybase - H/2}H230" stroke-width="1.2" stroke-dasharray="5 4"/>' + text(60, ybase - H / 2 - 8, 'h_max/2: W_к = W_п', 't-red', 'start'))
    o.append(f'<path class="s-mute" d="M60,{ybase - H}H200" stroke-width="1" stroke-dasharray="2 4"/>' + text(64, ybase - H - 6, 'h_max', 't-s', 'start'))
    o.append(f'<circle class="f-ink" cx="130" r="10">{anim("cy", nums([ybase - H * h for h in hs]), dur)}</circle>')
    base, hm = 206, 120
    for x, series, cls, lab in [(262, [1 - h for h in hs], 'f-acc', 'W_к'), (316, hs, 'f-red', 'W_п')]:
        o.append(f'<rect class="s-mute" x="{x-14}" y="{base-hm}" width="28" height="{hm}" stroke-width="1" stroke-dasharray="3 3"/>')
        o.append(f'<rect class="{cls}" x="{x-14}" width="28">{anims(dur, y=[base - hm * v for v in series], height=[hm * v for v in series])}</rect>')
        o.append(text(x, base + 18, lab, 't'))
    o.append(text(289, 76, 'W = const', 't-s'))
    return ''.join(o)
