// E2E-сценарии в настоящем Chromium (Playwright). Запуск: node tools/serve.mjs & node tests/e2e/flows.mjs
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const BASE = process.env.BASE ?? 'http://localhost:4173/';
const results = [];
async function step(name, fn) {
  try { await fn(); results.push(['PASS', name]); }
  catch (e) { results.push(['FAIL', name, e.message.split('\n')[0]]); }
}
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 360, height: 780 } });
await ctx.route(/fonts\.(googleapis|gstatic)\.com/, (r) => r.abort());
const page = await ctx.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));
// Физика живёт по адресам #/p/…, математика — #/m/…, стартовый экран — #/.
const go = async (h) => { await page.goto(BASE + '#/p/' + h); await page.waitForTimeout(250); };
const goM = async (h) => { await page.goto(BASE + '#/m/' + h); await page.waitForTimeout(250); };

await step('Стартовый экран UTC Preparation: два предмета, переход в каждый и обратно', async () => {
  await page.goto(BASE + '#/');
  await page.waitForTimeout(300);
  assert.ok(await page.getByRole('heading', { name: 'UTC Preparation' }).isVisible());
  assert.equal(await page.locator('.subject-card').count(), 2);
  assert.equal(await page.locator('.tabbar').count(), 0, 'на стартовом экране нет вкладок предмета');
  await page.locator('.subject-physics').click();
  await page.waitForTimeout(250);
  assert.ok(page.url().endsWith('#/p'), page.url());
  assert.ok(await page.getByRole('heading', { name: 'Физика' }).isVisible());
  await page.getByText('Предметы').first().click();
  await page.waitForTimeout(250);
  await page.locator('.subject-math').click();
  await page.waitForTimeout(250);
  assert.ok(page.url().endsWith('#/m'), page.url());
  assert.ok(await page.getByRole('heading', { name: 'Математика' }).isVisible());
  assert.equal(await page.title(), 'UTC Preparation');
});
await step('Старые адреса без префикса открывают физику', async () => {
  await page.goto(BASE + '#/topic/dyn-newton');
  await page.waitForTimeout(300);
  assert.ok(await page.getByText('Первый закон Ньютона').isVisible());
  // ссылки внутри экрана уже ведут на адреса физики
  assert.match(await page.locator('.source-chip').first().getAttribute('href'), /^#\/p\/page\//);
});

await step('Главная: 7 обязательных пунктов меню', async () => {
  await go('');
  for (const t of [/(Начать|Продолжить) обучение/, 'Все разделы физики', 'Тестирование', 'Повторение ошибок', 'Избранное', 'Мой прогресс', 'Настройки'])
    assert.ok(await page.getByText(t, { exact: false }).first().isVisible(), t);
});
await step('Просмотр разделов и всех 164 тем', async () => {
  await go('library');
  assert.equal(await page.locator('a.row').count(), 24);
  let total = 0;
  for (const s of ['kin', 'dyn', 'stat', 'fluids', 'cons', 'osc', 'mkt', 'td', 'sl', 'estat', 'capac', 'dc', 'ecur', 'mag', 'induct', 'emw', 'geo', 'lens', 'wave', 'rel', 'qphot', 'atom', 'nucl', 'radio']) { await go('sub/' + s); total += await page.locator('ol.topics li').count(); }
  assert.equal(total, 164);
  // порядок разделов в учебнике: электродинамика перед оптикой
  await go('library');
  const titles = await page.locator('section.block h2').allInnerTexts();
  assert.ok(titles.indexOf('Электродинамика и электромагнетизм') >= 0 && titles.indexOf('Электродинамика и электромагнетизм') < titles.indexOf('Оптика'), titles.join(' | '));
});
await step('Тема: теория, формулы с расшифровкой, источник открывает фото страницы', async () => {
  await go('topic/dyn-newton');
  assert.ok(await page.getByText('Первый закон Ньютона').isVisible());
  await page.getByRole('tab', { name: /Формулы/ }).click();
  assert.ok(await page.locator('.formula .katex').count() >= 3);
  await page.locator('.source-chip').first().click();
  await page.waitForTimeout(300);
  assert.match(page.url(), /#\/p\/page\/p14/);
  // фото конспектов есть только в рабочей копии владельца; без них — пояснение вместо фото
  if (fs.readdirSync(new URL('../../content/pages/', import.meta.url)).some((f) => f.endsWith('.webp'))) {
    const ok = await page.locator('.page-frame img').evaluate((i) => i.complete && i.naturalWidth > 0);
    assert.ok(ok, 'изображение страницы загрузилось');
  } else {
    await page.waitForTimeout(500);
    assert.ok(await page.getByText(/фотографии конспектов не публикуются/).isVisible(), 'вместо фото — пояснение');
  }
});
await step('Отметка «изучено» сохраняется после перезагрузки', async () => {
  await go('topic/kin-basics');
  await page.getByRole('button', { name: /Отметить тему как изученную/ }).click();
  await page.waitForTimeout(400);
  await page.reload(); await page.waitForTimeout(300);
  assert.ok(await page.getByRole('button', { name: /Изучено — снять отметку/ }).isVisible());
});
await step('Без утверждения вопросов тест недоступен', async () => {
  await go('test');
  assert.ok(await page.locator('#start-test').isDisabled());
});
await step('Админ: вход по PIN владельца (свой PIN задать нельзя) и массовое утверждение вопросов', async () => {
  await go('admin');
  assert.equal(await page.locator('#pin2').count(), 0, 'экрана создания PIN нет');
  await page.fill('#pin', '0000');
  await page.click('#pin-submit'); await page.waitForTimeout(1200);
  assert.match(await page.locator('.notice').last().innerText(), /Неверный PIN/);
  await page.fill('#pin', '1234');
  await page.click('#pin-submit'); await page.waitForSelector('#pin', { state: 'detached', timeout: 10000 });
  await go('admin/review');
  for (let i = 0; i < 40; i++) {
    const more = page.getByRole('button', { name: /Показать ещё/ });
    if (await more.count()) await more.click(); else break;
  }
  await page.check('#rq-all');
  await page.click('#bulk-approve');
  await page.getByRole('dialog').getByRole('button', { name: 'Утвердить' }).click();
  await page.waitForTimeout(300);
  await go('admin');
  const txt = await page.locator('.stat-grid').innerText();
  assert.match(txt, /1141\s*\/1141/);
});
await step('Режим A «По порядку»: первый вопрос курса — первый вопрос конспекта', async () => {
  await go('test');
  await page.locator('label:has(#order-source)').click();
  await page.click('#start-test'); await page.waitForTimeout(300);
  assert.match(await page.locator('.qprompt').innerText(), /материальная точка/i);
});
await step('Неверный ответ → подсказка → повтор → разбор; «Показать решение»', async () => {
  await go('test/topic/kin-motion-types');
  await page.click('#start-test'); await page.waitForTimeout(300);
  // q1 single: выбираем неверный вариант дважды
  const wrong = page.locator('.option').filter({ hasNotText: 'Криволинейное равномерное' }).first();
  await wrong.click(); await page.click('#submit-answer');
  assert.ok(await page.locator('.hintbox').isVisible(), 'подсказка показана');
  await wrong.click(); await page.click('#submit-answer');
  assert.ok(await page.locator('.verdict.bad').isVisible());
  assert.ok(await page.getByText('Объяснение ответа').isVisible());
  await page.click('#next-question');
  // q2 numeric: верный ответ 48 с первой попытки
  await page.fill('input[inputmode=decimal]', '48');
  await page.click('#submit-answer');
  assert.ok(await page.locator('.verdict.ok').isVisible());
  assert.ok(await page.getByText('Подстановка и вычисление').isVisible());
  await page.click('#next-question');
  await page.getByRole('button', { name: 'Показать решение' }).click();
  assert.ok(await page.getByText('Решение показано').isVisible());
});
await step('Результаты и очередь ошибок', async () => {
  await page.getByRole('button', { name: /Завершить тест/ }).click();
  await page.getByRole('dialog').getByRole('button', { name: 'Завершить' }).click();
  await page.waitForTimeout(300);
  assert.match(page.url(), /#\/p\/result\//);
  assert.ok(await page.locator('.score').isVisible());
  await go('mistakes');
  assert.ok((await page.locator('.list li').count()) >= 1);
});
await step('Режим B «Случайный»: разные попытки — разный порядок', async () => {
  const firstOf = async () => { await go('test/sub/kin'); await page.locator('label:has(#order-random)').click(); await page.click('#start-test'); await page.waitForTimeout(250); return page.locator('.qprompt').innerText(); };
  const seen = new Set();
  for (let i = 0; i < 4; i++) seen.add(await firstOf());
  assert.ok(seen.size >= 2, 'порядок меняется между попытками');
});
await step('Выбор количества: запрошено больше, чем есть — предупреждение', async () => {
  await go('test/topic/kin-basics');
  await page.fill('#q-count', '50');
  assert.ok(await page.getByText(/Запрошено 50, доступно 6/).first().isVisible());
});
await step('Экзамен: таймер, без подсказок', async () => {
  await go('test/exam'); await page.click('#start-test'); await page.waitForTimeout(300);
  assert.ok(await page.locator('.timer').isVisible());
  assert.equal(await page.getByRole('button', { name: 'Показать решение' }).count(), 0);
});
await step('Работа без интернета после загрузки', async () => {
  await go('topic/fl-archimedes');
  await ctx.setOffline(true);
  await page.getByRole('tab', { name: /Формулы/ }).click();
  assert.ok(await page.locator('.formula').count() > 0);
  await go('progress');
  assert.ok(await page.getByText('Доля верных ответов по дням').isVisible());
  await ctx.setOffline(false);
});
await step('Тёмная тема и крупный шрифт применяются', async () => {
  await go('settings');
  await page.getByRole('tab', { name: 'Тёмная' }).click();
  await page.getByRole('tab', { name: 'Крупный', exact: true }).click();
  assert.equal(await page.evaluate(() => document.documentElement.dataset.theme), 'dark');
  const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  assert.notEqual(bg, 'rgb(245, 247, 251)');
});
await step('Сброс прогресса только после подтверждения', async () => {
  await page.getByRole('button', { name: 'Сбросить прогресс' }).click();
  const confirm = page.getByRole('dialog').getByRole('button', { name: 'Сбросить' });
  assert.ok(await confirm.isDisabled(), 'без ввода слова кнопка заблокирована');
  await page.fill('#confirm-input', 'СБРОС'); await confirm.click(); await page.waitForTimeout(300);
  await go('progress');
  assert.match(await page.locator('.stat-grid').innerText(), /Пройдено тестов\s*0|0\s*Пройдено тестов/);
});
await step('Математика: план курса по книге, главы и пункты в порядке книги', async () => {
  await goM('library');
  assert.ok(await page.getByRole('heading', { name: 'План курса по книге' }).isVisible());
  assert.match(await page.locator('.block-head .muted').last().innerText(), /наполнено 131 из 131/);
  await goM('sub/ma-1-1');
  assert.equal(await page.locator('ol.topics li').count(), 6);
  assert.match(await page.locator('ol.topics li').first().innerText(), /1\.1\.1/);
  await goM('sub/ma-1-15');
  assert.equal(await page.locator('ol.topics li').count(), 13, 'пункты 1.15.1–1.15.13 наполнены');
  assert.match(await page.locator('ol.topics li').first().innerText(), /1\.15\.1\b/);
  assert.match(await page.locator('ol.topics li').last().innerText(), /1\.15\.13/);
  assert.equal(await page.locator('.plan-item').count(), 0, 'ненаполненных пунктов не осталось');
  await goM('sub/ma-3-13');
  assert.equal(await page.locator('ol.topics li').count(), 5);
  assert.match(await page.locator('ol.topics li').last().innerText(), /3\.13\.5/);
});
await step('Математика: тема — место в книге, таблица, формулы с обозначениями и «когда применять», пример с проверкой', async () => {
  await goM('topic/ma-1-1-5');
  assert.ok(await page.getByText(/Моя книга: Ч\. 1, 1\.1/).first().isVisible());
  assert.ok(await page.locator('.rich-table table').first().isVisible());
  assert.equal(await page.evaluate(() => document.documentElement.dataset.theme), 'dark', 'настройки общие для предметов');
  await page.getByRole('tab', { name: /Формулы/ }).click();
  assert.ok(await page.getByText('Когда применять:').first().isVisible());
  assert.ok(await page.getByText('Обозначения:').first().isVisible());
  await page.getByRole('tab', { name: /Примеры/ }).click();
  assert.ok(await page.getByText('Проверка:').first().isVisible());
  assert.ok(await page.getByText('Метод:').first().isVisible());
  // источник: место в книге без фото страницы, дополнительные источники — ссылки с датой проверки
  await page.locator('.book-chip').first().click();
  await page.waitForTimeout(300);
  assert.match(page.url(), /#\/m\/page\/b009/);
  assert.equal(await page.locator('.page-frame img').count(), 0, 'страницы книги не встраиваются');
  assert.ok(await page.getByText(/авторским правом/).isVisible());
});
await step('Математика: раздельные решения проверки и прогресс, общий PIN', async () => {
  await goM('admin');
  assert.ok(await page.getByRole('heading', { name: /Админ-панель · Математика/ }).isVisible(), 'PIN физики действует — повторно вводить не нужно');
  await goM('admin/review');
  for (let i = 0; i < 200; i++) { const more = page.getByRole('button', { name: /Показать ещё/ }); if (await more.count()) await more.click(); else break; }
  await page.check('#rq-all');
  await page.click('#bulk-approve');
  await page.getByRole('dialog').getByRole('button', { name: 'Утвердить' }).click();
  await page.waitForTimeout(300);
  await goM('admin');
  const m = (await page.locator('.stat-grid').innerText()).match(/(\d+)\s*\/(\d+)/);
  assert.ok(m && m[1] === m[2] && Number(m[1]) >= 50, 'все вопросы математики утверждены');
  await go('admin');
  assert.match(await page.locator('.stat-grid').innerText(), /1141\s*\/1141/, 'решения физики не изменились');
  await goM('topic/ma-1-1-1');
  await page.getByRole('button', { name: /Отметить тему как изученную/ }).click();
  await page.waitForTimeout(400);
  const st = await page.evaluate(() => ({ m: JSON.parse(localStorage.getItem('utc.math.user.v1')), p: JSON.parse(localStorage.getItem('fpk.user.v1')) }));
  assert.ok(st.m.topicProgress['ma-1-1-1'].studiedAt, 'прогресс математики сохранён');
  assert.ok(!Object.keys(st.p.topicProgress).some((k) => k.startsWith('ma-')), 'в прогрессе физики нет тем математики');
  await page.goto(BASE + '#/'); await page.waitForTimeout(300);
  assert.match(await page.locator('.subject-math').innerText(), /изучено 1/);
});
await step('Математика: тест — неверный ответ → подсказка → повтор → пошаговое решение', async () => {
  await goM('test/topic/ma-1-1-3');
  await page.locator('label:has(#order-source)').click();
  await page.click('#start-test'); await page.waitForTimeout(300);
  assert.match(await page.locator('.qprompt').innerText(), /1000/);
  await page.fill('input[inputmode=decimal]', '5'); await page.click('#submit-answer');
  assert.ok(await page.locator('.hintbox').isVisible(), 'сначала подсказка, а не решение');
  await page.fill('input[inputmode=decimal]', '7'); await page.click('#submit-answer');
  assert.ok(await page.locator('.verdict.bad').isVisible());
  assert.ok(await page.getByText('Метод:').first().isVisible());
  assert.ok(await page.locator('.solution ol.steps li').count() >= 2);
  await page.click('#next-question');
  await page.fill('input[inputmode=decimal]', '133'); await page.click('#submit-answer');
  assert.ok(await page.locator('.verdict.ok').isVisible());
});
await step('Нет горизонтальной прокрутки на 320/360/768 px', async () => {
  for (const w of [320, 360, 768]) {
    await page.setViewportSize({ width: w, height: 800 });
    for (const h of ['', 'library', 'topic/ma-1-1-5', 'topic/ma-1-1-2/formulas', 'sub/ma-1-15']) {
      await goM(h);
      const over = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      assert.ok(over <= 1, `${w}px #/m/${h}: +${over}px`);
    }
    await page.goto(BASE + '#/'); await page.waitForTimeout(200);
    assert.ok((await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth)) <= 1, `${w}px стартовый экран`);
  }
  await page.setViewportSize({ width: 360, height: 780 });
});
await step('Нет горизонтальной прокрутки на 320/360/768 px (физика)', async () => {
  for (const w of [320, 360, 768]) {
    await page.setViewportSize({ width: w, height: 800 });
    for (const h of ['', 'topic/kin-angle/formulas', 'admin/review', 'progress']) {
      await go(h);
      const over = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      assert.ok(over <= 1, `${w}px #/${h}: +${over}px`);
    }
  }
});
await step('Поиск по формулам и темам', async () => {
  await go('search'); await page.fill('#search-input', 'архимед'); await page.waitForTimeout(200);
  assert.ok(await page.getByText(/Темы · /).isVisible());
});
await step('Нет ошибок JavaScript', async () => { assert.deepEqual(errors, []); });

await browser.close();
for (const r of results) console.log(r.join(' | '));
const failed = results.filter((r) => r[0] === 'FAIL').length;
console.log(`\n${results.length - failed}/${results.length} пройдено`);
process.exit(failed ? 1 : 0);
