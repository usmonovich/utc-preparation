"""Иллюстрации к конспекту по оптике, релятивистской и квантовой физике (стр. o02–o20)."""
import math
from figlib import *  # noqa: F401,F403

SPECTRUM = ['r', 'o', 'y', 'g', 'b', 'v']  # классы s-sp-* в styles.css


def lin(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


def ray_flow(d, cls='s-acc', w=2.4, dur=0.8, period=14, extra=''):
    """Луч со «световыми» штрихами, бегущими по направлению пути."""
    return (f'<path class="{cls}" d="{d}" stroke-width="{w}" fill="none"{extra}/>'
            f'<path class="s-w" d="{d}" stroke-width="{w * 0.5}" stroke-dasharray="3 {period - 3}" fill="none" opacity="0.7"{extra}>{flow(dur, period)}</path>')


def pts(seq):
    return 'L'.join(f'{f(x)},{f(y)}' for x, y in seq)


def anim_d(paths, dur, kt=None, extra=''):
    k = kt or times(len(paths))
    return f'<animate attributeName="d" values="{";".join(paths)}" keyTimes="{k}" dur="{dur}s" repeatCount="indefinite"{extra}/>'


# ───────────────────────────── геометрическая оптика ─────────────────────────────

@fig('shadow', 'Прямолинейное распространение света: лучи от источника идут по прямым, за непрозрачным шаром на экране возникает тень', 360, 236)
def shadow():
    dur, n = 6, 41
    S = (30, 110)
    cx, r, X = 170, 24, 330
    cys = [110 + 28 * math.sin(2 * math.pi * u) for u in lin(0, 1, n)]
    up, lo, tu, tl = [], [], [], []
    for cy in cys:
        dx, dy = cx - S[0], cy - S[1]
        d = math.hypot(dx, dy)
        a0 = math.atan2(dy, dx)
        da = math.asin(r / d)
        ys = []
        for a in (a0 - da, a0 + da):
            ys.append(S[1] + (X - S[0]) * math.tan(a))
        up.append(ys[0]); lo.append(ys[1])
    o = ['<rect class="f-mute" x="330" y="10" width="10" height="200" opacity="0.5"/>']
    o.append(f'<path class="f-ink" opacity="0.18">{anim_d([f"M{S[0]},{S[1]}L{X},{f(a)}L{X},{f(b)}Z" for a, b in zip(up, lo)], dur)}</path>')
    o.append(f'<rect class="f-ink" x="326" width="8">{anims(dur, y=up, height=[b - a for a, b in zip(up, lo)])}</rect>')
    for ys, in [(up,), (lo,)]:
        o.append(f'<line class="s-red" x1="{S[0]}" y1="{S[1]}" x2="{X}" stroke-width="1.6">{anims(dur, y2=ys)}</line>')
    for a in (-60, -30, 30, 60):
        y2 = S[1] + (X - S[0]) * math.tan(math.radians(a * 0.5))
        o.append(f'<line class="s-red" x1="{S[0]}" y1="{S[1]}" x2="{X}" y2="{f(y2)}" stroke-width="1" opacity="0.35"/>')
    o.append(f'<circle class="f-acc" cx="{cx}" r="{r}">{anim("cy", nums(cys), dur)}</circle>')
    o.append(f'<circle class="f-red" cx="{S[0]}" cy="{S[1]}" r="8"/>' + text(S[0], S[1] + 26, 'источник', 't-s'))
    o.append(text(340, 230, 'тень на экране', 't-s', 'end'))
    return ''.join(o)


@fig('reflection', 'Закон отражения: угол падения α равен углу отражения α′; оба угла отсчитываются от перпендикуляра к поверхности', 360, 210)
def reflection():
    dur, n = 8, 41
    P = (180, 160)
    angs = [20 + 50 * (0.5 - 0.5 * math.cos(2 * math.pi * u)) for u in lin(0, 1, n)]
    L = 130
    o = [markers('reflection', ('red',))]
    o.append('<rect class="f-mute" x="40" y="160" width="280" height="12" opacity="0.5"/><path class="s-ink" d="M40,160H320" stroke-width="3"/>')
    o.append('<path class="s-mute" d="M180,160V30" stroke-width="1.4" stroke-dasharray="5 4"/>')
    inc = [f'M{f(P[0] - L * math.sin(math.radians(a)))},{f(P[1] - L * math.cos(math.radians(a)))}L{P[0]},{P[1]}' for a in angs]
    ref = [f'M{P[0]},{P[1]}L{f(P[0] + L * math.sin(math.radians(a)))},{f(P[1] - L * math.cos(math.radians(a)))}' for a in angs]
    o.append(f'<path class="s-red" stroke-width="2.6" marker-end="url(#reflection-m-red)">{anim_d(inc, dur)}</path>')
    o.append(f'<path class="s-red" stroke-width="2.6" marker-end="url(#reflection-m-red)">{anim_d(ref, dur)}</path>')
    R = 40
    arcl = [f'M180,{P[1] - R}A{R},{R} 0 0 0 {f(P[0] - R * math.sin(math.radians(a)))},{f(P[1] - R * math.cos(math.radians(a)))}' for a in angs]
    arcr = [f'M180,{P[1] - R}A{R},{R} 0 0 1 {f(P[0] + R * math.sin(math.radians(a)))},{f(P[1] - R * math.cos(math.radians(a)))}' for a in angs]
    o.append(f'<path class="s-acc" stroke-width="2" fill="none">{anim_d(arcl, dur)}</path><path class="s-acc" stroke-width="2" fill="none">{anim_d(arcr, dur)}</path>')
    lx = [P[0] - (R + 14) * math.sin(math.radians(a / 2)) for a in angs]
    ly = [P[1] - (R + 14) * math.cos(math.radians(a / 2)) + 4 for a in angs]
    o.append(f'<text class="t-acc" text-anchor="middle">{anims(dur, x=lx, y=ly)}α</text>')
    o.append(f'<text class="t-acc" text-anchor="middle">{anims(dur, x=[2 * P[0] - x for x in lx], y=ly)}α′</text>')
    o.append(text(180, 196, 'α = α′', 't'))
    o.append(text(330, 154, 'зеркало', 't-s', 'end'))
    return ''.join(o)


@fig('refraction', 'Преломление (закон Снеллиуса): при переходе из воздуха (n₁ = 1) в стекло (n₂ = 1,5) луч приближается к перпендикуляру; частота не меняется, а скорость и длина волны уменьшаются', 360, 220)
def refraction():
    dur, n = 8, 41
    n1, n2 = 1.0, 1.5
    P = (180, 110)
    angs = [10 + 60 * (0.5 - 0.5 * math.cos(2 * math.pi * u)) for u in lin(0, 1, n)]
    bets = [math.degrees(math.asin(n1 * math.sin(math.radians(a)) / n2)) for a in angs]
    L = 110
    o = [markers('refraction', ('red',))]
    o.append('<rect class="f-soft" x="20" y="110" width="320" height="100"/><path class="s-ink" d="M20,110H340" stroke-width="2"/>')
    o.append('<path class="s-mute" d="M180,14V206" stroke-width="1.4" stroke-dasharray="5 4"/>')
    inc = [f'M{f(P[0] - L * math.sin(math.radians(a)))},{f(P[1] - L * math.cos(math.radians(a)))}L{P[0]},{P[1]}' for a in angs]
    rfr = [f'M{P[0]},{P[1]}L{f(P[0] + L * math.sin(math.radians(b)))},{f(P[1] + L * math.cos(math.radians(b)))}' for b in bets]
    o.append(f'<path class="s-red" stroke-width="2.6">{anim_d(inc, dur)}</path>')
    o.append(f'<path class="s-red" stroke-width="2.6" marker-end="url(#refraction-m-red)">{anim_d(rfr, dur)}</path>')
    # «гребни волн»: одинаковая частота, в стекле штрихи короче и медленнее
    o.append(f'<path class="s-w" stroke-width="1.4" stroke-dasharray="3 15" opacity="0.8">{anim_d(inc, dur)}{flow(1.0, 18)}</path>')
    o.append(f'<path class="s-w" stroke-width="1.4" stroke-dasharray="3 9" opacity="0.8">{anim_d(rfr, dur)}{flow(1.0, 12)}</path>')
    R = 34
    arca = [f'M180,{P[1] - R}A{R},{R} 0 0 0 {f(P[0] - R * math.sin(math.radians(a)))},{f(P[1] - R * math.cos(math.radians(a)))}' for a in angs]
    arcb = [f'M180,{P[1] + R}A{R},{R} 0 0 0 {f(P[0] + R * math.sin(math.radians(b)))},{f(P[1] + R * math.cos(math.radians(b)))}' for b in bets]
    o.append(f'<path class="s-acc" stroke-width="2" fill="none">{anim_d(arca, dur)}</path><path class="s-acc" stroke-width="2" fill="none">{anim_d(arcb, dur)}</path>')
    o.append(f'<text class="t-acc" text-anchor="middle">{anims(dur, x=[P[0] - (R + 12) * math.sin(math.radians(a / 2)) for a in angs], y=[P[1] - (R + 12) * math.cos(math.radians(a / 2)) + 4 for a in angs])}α</text>')
    o.append(f'<text class="t-acc" text-anchor="middle">{anims(dur, x=[P[0] + (R + 12) * math.sin(math.radians(b / 2)) for b in bets], y=[P[1] + (R + 12) * math.cos(math.radians(b / 2)) + 4 for b in bets])}β</text>')
    o.append(text(330, 30, 'воздух, n₁ = 1', 't-s', 'end') + text(330, 200, 'стекло, n₂ = 1,5', 't-s', 'end'))
    o.append(text(26, 30, 'sin α / sin β = n₂ / n₁', 't', 'start'))
    return ''.join(o)


@fig('tir', 'Полное внутреннее отражение: луч идёт из стекла (n₁ = 1,5) в воздух (n₂ = 1); при угле α₀ ≈ 41,8° (sin α₀ = n₂/n₁) преломлённый луч скользит вдоль границы, при большем угле свет полностью отражается', 360, 220)
def tir():
    dur, n = 10, 61
    n1, n2 = 1.5, 1.0
    a0 = math.degrees(math.asin(n2 / n1))
    P = (180, 100)
    angs = [20 + 45 * (0.5 - 0.5 * math.cos(2 * math.pi * u)) for u in lin(0, 1, n)]
    L = 110
    o = [markers('tir', ('red',))]
    o.append('<rect class="f-soft" x="20" y="100" width="320" height="110"/><path class="s-ink" d="M20,100H340" stroke-width="2"/>')
    o.append('<path class="s-mute" d="M180,14V206" stroke-width="1.4" stroke-dasharray="5 4"/>')
    inc = [f'M{f(P[0] - L * math.sin(math.radians(a)))},{f(P[1] + L * math.cos(math.radians(a)))}L{P[0]},{P[1]}' for a in angs]
    refl = [f'M{P[0]},{P[1]}L{f(P[0] + L * math.sin(math.radians(a)))},{f(P[1] + L * math.cos(math.radians(a)))}' for a in angs]
    rfr, op_r, op_refl = [], [], []
    for a in angs:
        s = n1 * math.sin(math.radians(a)) / n2
        if s < 1:
            b = math.degrees(math.asin(s))
            rfr.append(f'M{P[0]},{P[1]}L{f(P[0] + L * math.sin(math.radians(b)))},{f(P[1] - L * math.cos(math.radians(b)))}')
            op_r.append(1); op_refl.append(0.25)
        else:
            rfr.append(f'M{P[0]},{P[1]}L{P[0] + L},{P[1]}')
            op_r.append(0); op_refl.append(1)
    o.append(f'<path class="s-red" stroke-width="2.6">{anim_d(inc, dur)}</path>')
    o.append(f'<path class="s-red" stroke-width="2.6" marker-end="url(#tir-m-red)">{anim_d(rfr, dur)}{anim("opacity", nums(op_r), dur, " calcMode=\"discrete\"")}</path>')
    o.append(f'<path class="s-red" stroke-width="2.6" marker-end="url(#tir-m-red)">{anim_d(refl, dur)}{anim("opacity", nums(op_refl), dur, " calcMode=\"discrete\"")}</path>')
    R = 34
    arca = [f'M180,{P[1] + R}A{R},{R} 0 0 1 {f(P[0] - R * math.sin(math.radians(a)))},{f(P[1] + R * math.cos(math.radians(a)))}' for a in angs]
    o.append(f'<path class="s-acc" stroke-width="2" fill="none">{anim_d(arca, dur)}</path>')
    o.append(f'<text class="t-acc" text-anchor="middle">{anims(dur, x=[P[0] - (R + 12) * math.sin(math.radians(a / 2)) for a in angs], y=[P[1] + (R + 12) * math.cos(math.radians(a / 2)) + 4 for a in angs])}α</text>')
    # граница α0
    o.append(f'<path class="s-mute" d="M180,100L{f(180 - 120 * math.sin(math.radians(a0)))},{f(100 + 120 * math.cos(math.radians(a0)))}" stroke-width="1" stroke-dasharray="2 4"/>'
             + text(180 - 128 * math.sin(math.radians(a0)), 100 + 128 * math.cos(math.radians(a0)) + 6, 'α₀', 't-s', 'end'))
    lab_in = ';'.join('1' if a < a0 else '0' for a in angs)
    lab_out = ';'.join('0' if a < a0 else '1' for a in angs)
    o.append(f'<text class="t" x="26" y="30" text-anchor="start">α &lt; α₀: луч выходит в воздух<animate attributeName="opacity" values="{lab_in}" keyTimes="{times(n)}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>')
    o.append(f'<text class="t-red" x="26" y="30" text-anchor="start" opacity="0">α ≥ α₀: полное отражение<animate attributeName="opacity" values="{lab_out}" keyTimes="{times(n)}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>')
    o.append(text(334, 92, 'воздух, n₂ = 1', 't-s', 'end') + text(334, 202, 'стекло, n₁ = 1,5', 't-s', 'end'))
    return ''.join(o)


@fig('plane-mirror', 'Плоское зеркало: изображение мнимое, прямое, равное и симметричное предмету; при движении предмета к зеркалу со скоростью υ изображение движется со скоростью υ, при движении зеркала — со скоростью 2υ', 360, 210)
def plane_mirror():
    dur = 10
    o = [markers('plane-mirror', ('red', 'acc'))]
    base = 150
    def candle(x, cls, dash=''):
        return (f'<path class="{cls}" d="M{f(x)},{base}V{base - 60}" stroke-width="6" stroke-linecap="round"{dash}/>'
                f'<path class="{cls.replace("s-", "f-")}" d="M{f(x - 7)},{base - 62}L{f(x)},{base - 80}L{f(x + 7)},{base - 62}Z"{dash}/>')
    # фаза ①: 0–0.45 предмет движется к зеркалу; фаза ②: 0.5–0.95 зеркало движется к предмету
    kt = '0;0.05;0.45;0.5;0.95;1'
    xo = [40, 40, 120, 120, 120, 40]
    xm = [200, 200, 200, 200, 160, 200]
    xi = [2 * m - x for x, m in zip(xm, xo)] if False else [2 * m - x for m, x in zip(xm, xo)]
    def tr(vals, ref):
        return f'<animateTransform attributeName="transform" type="translate" values="{";".join(f"{v - ref} 0" for v in vals)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
    o.append(f'<path class="s-ink" d="M10,{base}H350" stroke-width="1.4"/>')
    o.append(f'<g>{tr(xm, 200)}<rect class="f-mute" x="200" y="30" width="8" height="{base - 30}" opacity="0.5"/><path class="s-ink" d="M200,30V{base}" stroke-width="3"/>'
             + text(204, 24, 'зеркало', 't-s') + '</g>')
    o.append(f'<g>{tr(xo, 40)}{candle(40, "s-red")}</g>')
    o.append(f'<g>{tr(xi, 360)}{candle(360, "s-red", " opacity=\"0.45\" stroke-dasharray=\"4 3\"")}</g>')
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.05;0.45;0.46;1" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>'
             + text(180, 186, '① предмет → υ, изображение ← υ', 't') + '</g>')
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1;0" keyTimes="0;0.5;0.95" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>'
             + text(180, 186, '② зеркало ← υ, изображение ← 2υ', 't') + '</g>')
    o.append(text(180, 204, 'предмет и изображение — на одинаковом расстоянии a', 't-s'))
    return ''.join(o)


def lens_sym(x, y1, y2, conv=True):
    """Значок линзы: собирающая — стрелки наружу, рассеивающая — внутрь."""
    if conv:
        return (f'<path class="s-ink" d="M{x},{y1}V{y2}" stroke-width="2.4"/>'
                + head(x, y1, -90, 'f-ink', 9) + head(x, y2, 90, 'f-ink', 9))
    return (f'<path class="s-ink" d="M{x},{y1}V{y2}" stroke-width="2.4"/>'
            + head(x, y1 + 8, 90, 'f-ink', 9) + head(x, y2 - 8, -90, 'f-ink', 9))


@fig('lens-rays', 'Построение изображения в собирающей линзе тремя лучами: параллельный оси — через фокус, через фокус — параллельно оси, через оптический центр — без преломления (F = 60, d = 150 → f = 100)', 360, 220)
def lens_rays():
    dur = 9
    O, ax, F = 170, 110, 60
    d, h = 150, 44
    fi = d * F / (d - F)          # 100
    H = h * fi / d                # 29,3
    xo, yo = O - d, ax - h
    xi, yi = O + fi, ax + H
    o = ['<path class="s-mute" d="M10,110H350" stroke-width="1.2"/>', lens_sym(O, 22, 198)]
    for x, lab in [(O - F, 'F'), (O + F, 'F'), (O - 2 * F, '2F'), (O + 2 * F, '2F')]:
        o.append(f'<circle class="f-ink" cx="{x}" cy="{ax}" r="3"/>' + text(x, ax + 18, lab, 't-s'))
    o.append(text(O + 10, ax + 18, 'O', 't-s', 'start'))
    o.append(arrow(xo, ax, xo, yo, 's-red', 'f-red', 3, 9))
    yF2 = ax - h + (ax - (ax - h)) * 0  # точка на линзе для луча через фокус
    y_lens3 = ax + (h * F / (d - F))  # луч через F перед линзой попадает в линзу на высоте
    y_lens3 = ax - h + h * (d / (d - F)) if False else ax + h * F / (d - F) * 1
    # ① параллельно оси → через F'
    r1 = [(xo, yo), (O, yo), (xi, yi), (350, yo + (yi - yo) * (350 - O) / (xi - O))]
    # ② через O
    r2 = [(xo, yo), (350, yo + (ax - yo) * (350 - xo) / (O - xo))]
    # ③ через F → параллельно оси
    yl = yo + (ax - yo) * (O - xo) / ((O - F) - xo)
    r3 = [(xo, yo), (O, yl), (350, yl)]
    for k, (rp, cls) in enumerate([(r1, 's-acc'), (r2, 's-grn'), (r3, 's-red')]):
        t0, t1 = 0.06 + k * 0.22, 0.24 + k * 0.22
        dpath = 'M' + pts(rp)
        o.append(f'<path class="{cls}" d="{dpath}" stroke-width="2.2" fill="none" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100">'
                 f'<animate attributeName="stroke-dashoffset" values="100;100;0;0;100" keyTimes="0;{f(t0)};{f(t1)};0.94;1" dur="{dur}s" repeatCount="indefinite"/></path>')
        o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{f(t0)};{f(t0 + 0.02)};0.94;1" dur="{dur}s" repeatCount="indefinite"/>'
                 + text(16, 24 + 16 * k, ['① ∥ оси → через F', '② через O — прямо', '③ через F → ∥ оси'][k], 't-' + cls[2:], 'start') + '</g>')
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.72;0.74;0.94;1" dur="{dur}s" repeatCount="indefinite"/>'
             + arrow(xi, ax, xi, yi, 's-red', 'f-red', 3, 9) + text(xi + 8, yi + 4, 'изображение', 't-s', 'start') + '</g>')
    o.append(text(xo - 4, ax + 34, 'предмет', 't-s', 'start'))
    return ''.join(o)


@fig('lens-images', 'Собирающая линза: предмет приближается от 4F к линзе — изображение меняется по таблице конспекта; при d = F изображения нет, при d < F оно мнимое, прямое, увеличенное', 360, 240)
def lens_images():
    dur, n = 14, 121
    O, ax, F, h = 200, 120, 38, 26
    us = lin(0, 1, n)
    # d: 4F → 0,5F за 0–0.9 (с задержкой на 2F и F), затем возврат скрыт
    def d_of(u):
        if u < 0.25:
            return 4 * F - (2 * F) * (u / 0.25)
        if u < 0.33:
            return 2 * F
        if u < 0.5:
            return 2 * F - 0.55 * F * ((u - 0.33) / 0.17)
        if u < 0.58:
            return 1.45 * F - 0.45 * F * ((u - 0.5) / 0.08)
        if u < 0.66:
            return F
        if u < 0.9:
            return F - 0.5 * F * min((u - 0.66) / 0.2, 1)
        return 0.5 * F
    ds = [d_of(u) for u in us]
    zone = []
    for u, d in zip(us, ds):
        if u < 0.25 and d > 2 * F + 0.5:
            zone.append(0)
        elif u < 0.33:
            zone.append(1)
        elif u < 0.5 or (u < 0.58 and d > 1.2 * F):
            zone.append(2)
        elif u < 0.66:
            zone.append(3)
        else:
            zone.append(4)
    xo = [O - d for d in ds]
    fis, Hs, show = [], [], []
    for d in ds:
        if abs(d - F) < 1e-6 or (F * 1.0 < d < F * 1.42) or (F * 0.72 < d < F):
            fis.append(None); Hs.append(0); show.append(0)
        else:
            fi = d * F / (d - F)
            fis.append(fi); Hs.append(h * fi / d); show.append(1)
    xi = [O + (fi if fi is not None else 0) for fi in fis]
    yi = [ax + H if fi is not None else ax for fi, H in zip(fis, Hs)]   # для мнимого fi < 0 → H < 0: изображение над осью
    o = [f'<clipPath id="lens-images-clip"><rect x="0" y="0" width="360" height="240"/></clipPath>',
         '<path class="s-mute" d="M4,120H356" stroke-width="1.2"/>', lens_sym(O, 34, 206)]
    for x, lab in [(O - F, 'F'), (O + F, 'F'), (O - 2 * F, '2F'), (O + 2 * F, '2F'), (O - 4 * F, '4F')]:
        o.append(f'<circle class="f-ink" cx="{x}" cy="{ax}" r="3"/>' + text(x, ax + 18, lab, 't-s'))
    # предмет
    o.append(f'<g>{move([(x - xo[0], 0) for x in xo], dur)}{arrow(xo[0], ax, xo[0], ax - h, "s-red", "f-red", 3, 9)}</g>')
    # лучи: ① ∥ оси → через F′; ② через O
    r1, r2, e1, e2 = [], [], [], []
    for x, fi, yv in zip(xo, fis, yi):
        top = ax - h
        y_end1 = top + (ax - top) * (356 - O) / F
        r1.append(f'M{f(x)},{f(top)}L{O},{f(top)}L356,{f(y_end1)}')
        y_end2 = top + (ax - top) * (356 - x) / (O - x)
        r2.append(f'M{f(x)},{f(top)}L356,{f(y_end2)}')
        if fi is not None and fi < 0:
            e1.append(f'M{O},{f(top)}L{f(O + fi)},{f(yv)}')
            e2.append(f'M{O},{ax}L{f(O + fi)},{f(yv)}')
        else:
            e1.append(f'M{O},{f(top)}L{O},{f(top)}')
            e2.append(f'M{O},{ax}L{O},{ax}')
    o.append(f'<path class="s-acc" stroke-width="1.8" fill="none" opacity="0.8">{anim_d(r1, dur)}</path>')
    o.append(f'<path class="s-grn" stroke-width="1.8" fill="none" opacity="0.8">{anim_d(r2, dur)}</path>')
    o.append(f'<path class="s-acc" stroke-width="1.4" stroke-dasharray="4 4" fill="none">{anim_d(e1, dur)}</path>')
    o.append(f'<path class="s-grn" stroke-width="1.4" stroke-dasharray="4 4" fill="none">{anim_d(e2, dur)}</path>')
    # изображение
    real = [1 if s and fi is not None and fi > 0 else 0 for s, fi in zip(show, fis)]
    virt = [1 if s and fi is not None and fi < 0 else 0 for s, fi in zip(show, fis)]
    xi_c = [min(max(x, 4), 356) for x in xi]
    o.append(f'<line class="s-red" stroke-width="3" y1="{ax}">{anims(dur, x1=xi_c, x2=xi_c, y2=yi)}{anim("opacity", nums(real), dur, " calcMode=\"discrete\"")}</line>')
    o.append(f'<line class="s-red" stroke-width="3" stroke-dasharray="5 4" y1="{ax}">{anims(dur, x1=xi_c, x2=xi_c, y2=yi)}{anim("opacity", nums(virt), dur, " calcMode=\"discrete\"")}</line>')
    labels = ['① d > 2F: действительное, перевёрнутое, уменьшенное', '② d = 2F: действительное, перевёрнутое, равное',
              '③ 2F > d > F: действительное, перевёрнутое, увеличенное', '④ d = F: изображения нет', '⑤ F > d > 0: мнимое, прямое, увеличенное']
    for k, lab in enumerate(labels):
        o.append(f'<text class="t-s" x="180" y="232" text-anchor="middle" opacity="0">{subs(lab)}<animate attributeName="opacity" values="{";".join("1" if z == k else "0" for z in zone)}" keyTimes="{times(n)}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>')
    return ''.join(o)


@fig('lens-div', 'Рассеивающая линза: лучи, параллельные главной оптической оси, после линзы расходятся, а их продолжения (пунктир) сходятся в фокусе F', 360, 210)
def lens_div():
    O, ax, F = 200, 105, 70
    o = ['<path class="s-mute" d="M10,105H350" stroke-width="1.2"/>', lens_sym(O, 20, 190, conv=False)]
    for x, lab in [(O - F, 'F'), (O + F, 'F')]:
        o.append(f'<circle class="f-ink" cx="{x}" cy="{ax}" r="3"/>' + text(x, ax + 18, lab, 't-s'))
    for i, y in enumerate((45, 75, 105, 135, 165)):
        k = (y - ax) / F
        y_end = y + k * (350 - O)
        d = f'M20,{y}H{O}L350,{f(y_end)}'
        o.append(f'<path id="lens-div-r{i}" class="s-red" d="{d}" stroke-width="2.2" fill="none"/>')
        for j in range(3):
            o.append(f'<circle class="f-red" r="3.5"><animateMotion dur="3s" begin="{f(-j)}s" repeatCount="indefinite"><mpath href="#lens-div-r{i}"/></animateMotion></circle>')
        if y != ax:
            o.append(f'<path class="s-red" d="M{O},{y}L{O - F},{ax}" stroke-width="1.2" stroke-dasharray="4 4" opacity="0.7"/>')
    o.append(text(24, 24, 'продолжения лучей — через F', 't-s', 'start'))
    return ''.join(o)


@fig('eye', 'Глаз — оптическая система с собирающей линзой: на сетчатке возникает действительное, перевёрнутое, уменьшенное изображение', 360, 200)
def eye():
    dur, n = 8, 41
    ax = 100
    cx, R = 270, 60
    lens_x, ret_x = cx - R + 8, cx + R - 4
    fl = ret_x - lens_x
    ds = [130 + 60 * (0.5 - 0.5 * math.cos(2 * math.pi * u)) for u in lin(0, 1, n)]
    h = 50
    xo = [lens_x - d for d in ds]
    Hs = [h * fl / d for d in ds]
    o = [f'<circle class="f-soft s-ink" cx="{cx}" cy="{ax}" r="{R}" stroke-width="2.4"/>',
         f'<path class="s-red" d="M{ret_x - 6},{ax - 40}A{R - 4},{R - 4} 0 0 1 {ret_x - 6},{ax + 40}" stroke-width="4" fill="none" opacity="0.6"/>',
         f'<ellipse class="f-paper s-acc" cx="{lens_x}" cy="{ax}" rx="9" ry="26" stroke-width="2.4"/>',
         '<path class="s-mute" d="M10,100H340" stroke-width="1" stroke-dasharray="3 4"/>']
    o.append(f'<g>{move([(x - xo[0], 0) for x in xo], dur)}{arrow(xo[0], ax, xo[0], ax - h, "s-grn", "f-grn", 3, 9)}</g>')
    top = [f'M{f(x)},{ax - h}L{lens_x},{ax}L{ret_x},{f(ax + H)}' for x, H in zip(xo, Hs)]
    bot = [f'M{f(x)},{ax}L{ret_x},{ax}' for x in xo]
    o.append(f'<path class="s-red" stroke-width="1.6" fill="none">{anim_d(top, dur)}</path>')
    o.append(f'<line class="s-grn" stroke-width="3" x1="{ret_x - 3}" x2="{ret_x - 3}" y1="{ax}">{anim("y2", nums([ax + H for H in Hs]), dur)}</line>')
    o.append(text(lens_x - 12, ax - 46, 'хрусталик', 't-s', 'end') + text(352, 40, 'сетчатка', 't-s', 'end'))
    o.append(text(180, 190, 'на сетчатке: действительное, перевёрнутое, уменьшенное', 't-s'))
    return ''.join(o)


# ───────────────────────────── волновая оптика ─────────────────────────────

@fig('interference', 'Интерференция когерентных волн от источников A₁ и A₂: где разность хода Δx = kλ, волны усиливают друг друга (светлые полосы), между ними — ослабляют', 360, 220)
def interference():
    dur, lam = 1.6, 24
    A1, A2 = (40, 80), (40, 140)
    o = [f'<clipPath id="interference-clip"><rect x="40" y="0" width="290" height="220"/></clipPath>']
    g = ['<g clip-path="url(#interference-clip)">']
    for S, cls in [(A1, 's-acc'), (A2, 's-red')]:
        for i in range(13):
            r0 = i * lam
            g.append(f'<circle class="{cls}" cx="{S[0]}" cy="{S[1]}" stroke-width="1.6" fill="none">'
                     f'<animate attributeName="r" values="{r0};{r0 + lam}" dur="{dur}s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="{f(max(0.9 - r0 / 330, 0.05))};{f(max(0.9 - (r0 + lam) / 330, 0.05))}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    g.append('</g>')
    o += g
    for S, lab in [(A1, 'A₁'), (A2, 'A₂')]:
        o.append(f'<circle class="f-ink" cx="{S[0]}" cy="{S[1]}" r="5"/>' + text(S[0] - 10, S[1] + 5, lab, 't', 'end'))
    # экран: интенсивность I ~ cos²(πΔx/λ)
    X = 336
    for y in range(4, 216, 3):
        dx = math.hypot(X - A1[0], y - A1[1]) - math.hypot(X - A2[0], y - A2[1])
        I = math.cos(math.pi * dx / lam) ** 2
        o.append(f'<rect class="f-acc" x="{X}" y="{y}" width="14" height="3" opacity="{f(0.1 + 0.9 * I)}"/>')
    o.append(text(343, 16, 'экран', 't-s'))
    return ''.join(o)


@fig('prism', 'Дисперсия в треугольной призме: белый свет раскладывается в спектр; с ростом частоты показатель преломления растёт, поэтому фиолетовые лучи отклоняются сильнее красных', 360, 220)
def prism():
    dur = 6
    A, B, C = (170, 30), (100, 170), (240, 170)
    o = [f'<path class="f-soft s-ink" d="M{A[0]},{A[1]}L{B[0]},{B[1]}L{C[0]},{C[1]}Z" stroke-width="2"/>']
    entry = (128, 113)
    o.append(f'<path class="s-ink" d="M10,140L{entry[0]},{entry[1]}" stroke-width="3" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100">'
             f'<animate attributeName="stroke-dashoffset" values="100;0;0;100" keyTimes="0;0.15;0.92;1" dur="{dur}s" repeatCount="indefinite"/></path>')
    o.append(text(16, 160, 'белый свет', 't-s', 'start'))
    for k, c in enumerate(SPECTRUM):
        ey = 100 + k * 4.5
        ex = (A[0] + (C[0] - A[0]) * (ey - A[1]) / (C[1] - A[1]), ey)
        end = (350, 116 + k * 17)
        d = f'M{entry[0]},{entry[1]}L{f(ex[0])},{f(ex[1])}L{end[0]},{end[1]}'
        o.append(f'<path class="s-sp-{c}" d="{d}" stroke-width="2.4" fill="none" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100">'
                 f'<animate attributeName="stroke-dashoffset" values="100;100;0;0;100" keyTimes="0;0.15;0.45;0.92;1" dur="{dur}s" repeatCount="indefinite"/></path>')
    o.append(text(352, 106, 'красный', 't-s', 'end') + text(352, 216, 'фиолетовый', 't-s', 'end'))
    o.append(text(170, 200, 'ν↑ ⇒ n↑ ⇒ отклонение больше', 't-s'))
    return ''.join(o)


# ───────────────────────────── релятивистская физика ─────────────────────────────

@fig('rel-length', 'Релятивистские эффекты: с ростом скорости тела длина в направлении движения уменьшается, l = l₀√(1 − υ²/c²), а масса растёт, m = m₀/√(1 − υ²/c²)', 360, 210)
def rel_length():
    dur, n = 8, 41
    us = lin(0, 1, n)
    beta = [0.95 * (0.5 - 0.5 * math.cos(2 * math.pi * u)) for u in us]
    g = [math.sqrt(1 - b * b) for b in beta]
    l0 = 120
    o = []
    o.append(f'<rect class="s-mute" x="30" y="40" width="{l0}" height="40" rx="10" stroke-width="1.4" stroke-dasharray="4 4"/>' + text(30 + l0 / 2, 30, 'l₀ (в покое)', 't-s'))
    o.append(f'<rect class="f-acc" x="30" y="40" height="40" rx="10">{anim("width", nums([l0 * q for q in g]), dur)}</rect>')
    o.append(f'<path class="s-ink" d="M30,92H150" stroke-width="1" opacity="0.4"/>')
    o.append(f'<text class="t" y="108" text-anchor="middle">{anim("x", nums([30 + l0 * q / 2 for q in g]), dur)}l</text>')
    # скорость
    o.append('<rect class="s-mute" x="30" y="140" width="120" height="12" stroke-width="1" stroke-dasharray="3 3"/>')
    o.append(f'<rect class="f-red" x="30" y="140" height="12">{anim("width", nums([120 * b for b in beta]), dur)}</rect>')
    o.append(text(30, 172, 'υ / c: 0 → 0,95', 't-s', 'start') + text(152, 150, 'c', 't-s', 'start'))
    # масса
    bx, base, hm = 260, 190, 150
    o.append(f'<rect class="s-mute" x="{bx - 18}" y="{base - hm}" width="36" height="{hm}" stroke-width="1" stroke-dasharray="3 3"/>')
    o.append(f'<path class="s-ink" d="M{bx - 24},{base - 46}H{bx + 24}" stroke-width="1.2" stroke-dasharray="3 3"/>' + text(bx + 28, base - 42, 'm₀', 't-s', 'start'))
    ms = [min(46 / q, hm) for q in g]
    o.append(f'<rect class="f-red" x="{bx - 18}" width="36">{anims(dur, y=[base - m for m in ms], height=ms)}</rect>')
    o.append(text(bx, 34, 'масса m', 't'))
    return ''.join(o)


# ───────────────────────────── квантовая физика ─────────────────────────────

def photon(x1, y1, x2, y2, cls, t0, t1, dur, amp=4, waves=4):
    """Фотон — волнистая стрелка, пролетающая от (x1,y1) к (x2,y2) за [t0, t1]."""
    L = math.hypot(x2 - x1, y2 - y1)
    a = math.degrees(math.atan2(y2 - y1, x2 - x1))
    seg = ''.join(f'q{f(L / waves / 4)},{-amp if i % 2 == 0 else amp} {f(L / waves / 2)},0' for i in range(waves * 2))
    d = f'M{-L / 2},0{seg}'
    kt = f'0;{f(t0)};{f(t1)};1'
    return (f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;{f(t0)};{f(t1)};{f(min(t1 + 0.01, 1))}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>'
            f'<g><animateTransform attributeName="transform" type="translate" values="{f(x1)} {f(y1)};{f(x1)} {f(y1)};{f(x2)} {f(y2)};{f(x2)} {f(y2)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<g transform="rotate({f(a)})"><path class="{cls}" d="{d}" stroke-width="2" fill="none" transform="scale(0.35,1)" vector-effect="non-scaling-stroke"/></g></g></g>')


def electron(x1, y1, x2, y2, t0, t1, dur):
    kt = f'0;{f(t0)};{f(t1)};1'
    return (f'<circle class="f-acc" r="4.5" opacity="0"><animate attributeName="opacity" values="0;1;0;0" keyTimes="0;{f(t0)};{f(t1)};1" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/>'
            f'<animate attributeName="cx" values="{f(x1)};{f(x1)};{f(x2)};{f(x2)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="{f(y1)};{f(y1)};{f(y2)};{f(y2)}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></circle>')


@fig('photoeffect', 'Законы Столетова: при большей интенсивности света (больше фотонов) вылетает больше фотоэлектронов, но с той же скоростью; при большей частоте электроны вылетают быстрее', 360, 220)
def photoeffect():
    dur = 12
    plate = 150
    o = [f'<rect class="f-mute" x="{plate}" y="40" width="16" height="140" opacity="0.7"/><path class="s-ink" d="M{plate},40V180" stroke-width="2"/>']
    o.append(text(plate + 8, 198, 'металл', 't-s'))
    phases = [(0.0, 0.32, 2, 's-red', 1.0), (0.34, 0.66, 5, 's-red', 1.0), (0.68, 1.0, 2, 's-sp-v', 1.8)]
    for p0, p1, cnt, cls, speed in phases:
        for i in range(cnt):
            y = 60 + (i + 0.5) * 100 / cnt
            for rep in range(2):
                t0 = p0 + 0.02 + rep * (p1 - p0) / 2 + i * 0.01
                t1 = t0 + 0.07
                o.append(photon(20, y - 20, plate - 6, y, cls, t0, t1, dur))
                te = t1 + 0.12 / speed
                o.append(electron(plate - 4, y, plate - 4 - 120, y + 30 * (i % 2 * 2 - 1) * 0.5, t1, te, dur))
    labs = [('меньше фотонов — меньше электронов', 0.0, 0.33),
            ('больше фотонов — больше электронов, скорость та же', 0.33, 0.67),
            ('больше частота — электроны быстрее (E_к больше)', 0.67, 1.0)]
    for lab, a, b in labs:
        o.append(f'<text class="t-s" x="352" y="24" text-anchor="end" opacity="0">{subs(lab)}<animate attributeName="opacity" values="0;1;0" keyTimes="0;{f(a) if a else "0.0001"};{f(b) if b < 1 else "0.9999"}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>'.replace('values="0;1;0" keyTimes="0;0.0001', 'values="1;1;0" keyTimes="0;0.0001'))
    o.append(text(30, 212, 'фотоны', 't-red', 'start') + text(plate - 120, 212, '', 't-s'))
    o.append(text(352, 212, 'hν = A + E_к', 't', 'end'))
    return ''.join(o)


@fig('red-limit', 'Красная граница фотоэффекта: пока hν < A, электроны не вылетают; когда hν ≥ A, электрон вылетает с энергией E_к = hν − A', 360, 220)
def red_limit():
    dur, n = 10, 41
    us = lin(0, 1, n)
    hv = [0.35 + 0.6 * (0.5 - 0.5 * math.cos(2 * math.pi * u)) for u in us]
    A = 0.6
    base, hm = 196, 150
    o = []
    bx = 250
    o.append(f'<path class="s-ink" d="M{bx - 50},{base}H{bx + 90}" stroke-width="1.4"/>')
    o.append(f'<rect class="f-red" x="{bx - 40}" width="34">{anims(dur, y=[base - hm * v for v in hv], height=[hm * v for v in hv])}</rect>' + text(bx - 23, base + 18, 'hν', 't'))
    o.append(f'<path class="s-ink" d="M{bx - 50},{base - hm * A}H{bx + 80}" stroke-width="1.6" stroke-dasharray="5 4"/>' + text(bx + 84, base - hm * A + 5, 'A', 't', 'start'))
    o.append(text(352, 30, 'A — работа выхода', 't-s', 'end'))
    ek = [max(v - A, 0) for v in hv]
    o.append(f'<rect class="f-acc" x="{bx + 20}">{anims(dur, y=[base - hm * A - hm * e for e in ek], height=[hm * e for e in ek])}</rect>'.replace(f'x="{bx + 20}"', f'x="{bx + 20}" width="34"'))
    o.append(text(bx + 37, base + 18, 'E_к', 't-acc'))
    # пластина и вылет электрона
    o.append('<rect class="f-mute" x="120" y="60" width="14" height="130" opacity="0.7"/><path class="s-ink" d="M120,60V190" stroke-width="2"/>')
    on = [1 if v >= A else 0 for v in hv]
    for k in range(6):
        y = 80 + k * 18
        ph = (k * 0.17) % 1
        o.append(f'<line class="s-red" x1="20" y1="{y - 14}" x2="44" y2="{y - 6}" stroke-width="2.2" stroke-dasharray="4 3"><animateTransform attributeName="transform" type="translate" values="0 0;72 8" dur="1.2s" begin="{f(ph * 1.2)}s" repeatCount="indefinite"/></line>')
    o.append(f'<g>{anim("opacity", nums(on), dur, " calcMode=\"discrete\"")}' + ''.join(
        f'<circle class="f-acc" r="4.5" cx="116" cy="{100 + k * 20}"><animate attributeName="cx" values="116;40" dur="{f(0.6 + 0.4 * (k % 2))}s" begin="{f(k * 0.3)}s" repeatCount="indefinite"/>'
        f'<animate attributeName="cy" values="{100 + k * 20};{80 + k * 26}" dur="{f(0.6 + 0.4 * (k % 2))}s" begin="{f(k * 0.3)}s" repeatCount="indefinite"/></circle>' for k in range(3)) + '</g>')
    o.append(f'<text class="t" x="20" y="30" text-anchor="start">ν &lt; ν_к — фотоэффекта нет<animate attributeName="opacity" values="{nums([1 - x for x in on])}" keyTimes="{times(n)}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>'.replace('ν_к', 'ν<tspan baseline-shift="sub" font-size="0.72em">к</tspan>'))
    o.append(f'<text class="t-acc" x="20" y="30" text-anchor="start" opacity="0">ν ≥ ν_к — электроны вылетают<animate attributeName="opacity" values="{nums(on)}" keyTimes="{times(n)}" dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>'.replace('ν_к', 'ν<tspan baseline-shift="sub" font-size="0.72em">к</tspan>'))
    o.append(text(20, 214, 'частота света ν меняется', 't-s', 'start'))
    return ''.join(o)
