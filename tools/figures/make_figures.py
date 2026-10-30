#!/usr/bin/env python3
"""Генератор анимированных иллюстраций к теории: content/figures/<id>.svg.

Каждая иллюстрация повторяет рисунок или описание конспекта и оживляет его анимацией SMIL.
Значения движения (маятник, падение, линзы, газовые законы, фазы токов) считаются по формулам
конспекта, а не подбираются на глаз. Цвета задаются классами (s-*, f-*, t-*), их определяет
styles.css — поэтому рисунки сами меняются в тёмной теме.

Рисунки по разделам: figs_mech.py, figs_thermo.py, figs_elec.py (электричество), figs_electro.py (магнетизм, колебания), figs_optics.py, figs_atom.py (атом и ядро, а также темы, дополненные из интернета).
Запуск: python3 tools/figures/make_figures.py
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import FIGS, OUT  # noqa: E402
import figs_mech  # noqa: E402,F401
import figs_thermo  # noqa: E402,F401
import figs_elec  # noqa: E402,F401
import figs_electro  # noqa: E402,F401
import figs_optics  # noqa: E402,F401
import figs_atom  # noqa: E402,F401


def main():
    os.makedirs(OUT, exist_ok=True)
    for fid, (title, w, h, fn) in FIGS.items():
        body = fn()
        title = re.sub(r'_([0-9A-Za-zА-Яа-яЁё]+)', r'\1', title)  # индексы для экранного диктора — без «_»
        title = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="inherit">'
               f'<title>{title}</title>{body}</svg>\n')
        try:
            ET.fromstring(svg)
        except ET.ParseError as e:
            raise SystemExit(f'{fid}: SVG не разбирается как XML — {e}')
        with open(os.path.join(OUT, f'{fid}.svg'), 'w', encoding='utf8') as fh:
            fh.write(svg)
    print(f'рисунков: {len(FIGS)}')


if __name__ == '__main__':
    main()
