#!/usr/bin/env python3
"""Анимированные иллюстрации к теории математики: content/math/figures/<id>.svg.

Те же правила, что у физики (figlib.py): SVG + SMIL, цвета — классами s-*, f-*, t-* (тёмная тема),
все id внутри файла начинаются с «<id>-». Значения на рисунках посчитаны по формулам темы.
Рисунки — в figs_math.py. Запуск: python3 tools/figures/make_math_figures.py
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib  # noqa: E402
import figs_elec  # noqa: E402,F401  — общие функции; его рисунки физики регистрируются здесь и сразу убираются
figlib.FIGS.clear()
import figs_math  # noqa: E402,F401

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'content', 'math', 'figures')


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith('.svg') and f[:-4] not in figlib.FIGS:
            os.remove(os.path.join(OUT, f))
    for fid, (title, w, h, fn) in figlib.FIGS.items():
        body = fn()
        title = re.sub(r'_([0-9A-Za-zА-Яа-яЁё]+)', r'\1', title)
        title = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="inherit">'
               f'<title>{title}</title>{body}</svg>\n')
        try:
            ET.fromstring(svg)
        except ET.ParseError as e:
            raise SystemExit(f'{fid}: SVG не разбирается как XML — {e}')
        with open(os.path.join(OUT, f'{fid}.svg'), 'w', encoding='utf8') as fh:
            fh.write(svg)
    print(f'рисунков математики: {len(figlib.FIGS)}')


if __name__ == '__main__':
    main()
