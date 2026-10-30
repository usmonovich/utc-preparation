// Исходные изображения для @capacitor/assets (иконки Android/iOS и заставка) из store/icon.svg.
// Запуск: node tools/android/make-assets.mjs → assets/*.png
// Затем на компьютере сборки: npx capacitor-assets generate --android (делает скрипт build-android.ps1).
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const out = path.join(root, 'assets');
fs.mkdirSync(out, { recursive: true });

const BLUE = '#2a47c7', NIGHT = '#141d4d';
const grid = (op) => `<g stroke="#ffffff" stroke-opacity="${op}" stroke-width="4">
  <path d="M0 128H1024M0 256H1024M0 384H1024M0 512H1024M0 640H1024M0 768H1024M0 896H1024"/>
  <path d="M128 0V1024M256 0V1024M384 0V1024M512 0V1024M640 0V1024M768 0V1024M896 0V1024"/></g>`;
// рисунок значка (траектория, вектор скорости, тело, горизонт) — как в store/icon.svg
const motif = `<path d="M250 800 Q 520 120 820 800" fill="none" stroke="#ffffff" stroke-width="44" stroke-linecap="round" stroke-dasharray="1 78"/>
  <path d="M250 800 L 360 580" stroke="#ffffff" stroke-width="30" stroke-linecap="round"/>
  <path d="M360 580 l-62 6 m62 -6 l10 62" stroke="#ffffff" stroke-width="30" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <circle cx="535" cy="460" r="54" fill="#ffffff"/>
  <path d="M215 810H860" stroke="#ffffff" stroke-width="22" stroke-linecap="round"/>`;
// центр рисунка ≈ (537, 555), размер ≈ 645 × 510; для адаптивной иконки — в безопасный круг (≈ 66 % стороны)
const centered = (scale) => `<g transform="translate(512 512) scale(${scale}) translate(-537 -555)">${motif}</g>`;

const files = {
  'icon-only.png': [1024, fs.readFileSync(path.join(root, 'store/icon.svg'), 'utf8')],
  'icon-background.png': [1024, `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><rect width="1024" height="1024" fill="${BLUE}"/>${grid(0.13)}<path d="M190 0V1024" stroke="#ff7781" stroke-width="10"/></svg>`],
  'icon-foreground.png': [1024, `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">${centered(0.68)}</svg>`],
  'splash.png': [2732, `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><rect width="1024" height="1024" fill="${BLUE}"/>${centered(0.36)}</svg>`],
  'splash-dark.png': [2732, `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><rect width="1024" height="1024" fill="${NIGHT}"/>${centered(0.36)}</svg>`],
};

const browser = await chromium.launch();
for (const [name, [size, svg]] of Object.entries(files)) {
  const page = await browser.newPage({ viewport: { width: size, height: size } });
  await page.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg ', `<svg width="${size}" height="${size}" `)}</body></html>`);
  await page.screenshot({ path: path.join(out, name), omitBackground: true, clip: { x: 0, y: 0, width: size, height: size } });
  await page.close();
  console.log(`assets/${name} ${size}×${size}`);
}
await browser.close();
