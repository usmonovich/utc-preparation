// E2E: приложение открыто как артефакт claude.ai, память браузера при каждом входе пустая
// (так ведёт себя мобильное приложение Claude). Решения проверки и прогресс должны сохраняться
// в базе артефакта. База и пользователь имитируются: тот же интерфейс, что у window.claude.use().
// Запуск: node tools/serve.mjs & node tests/e2e/cloud.mjs
import { chromium } from 'playwright';
import assert from 'node:assert/strict';

const BASE = process.env.BASE ?? 'http://localhost:4173/';
const results = [];
async function step(name, fn) {
  try { await fn(); results.push(['PASS', name]); }
  catch (e) { results.push(['FAIL', name, e.message.split('\n')[0]]); }
}

// Общая «база артефакта» на стороне теста — переживает перезагрузки и разные устройства.
const docs = new Map();

/** Имитация window.claude: db (get/set/delete/onSnapshot через опрос) и user. */
function runtimeScript({ uid, owner }) {
  // память браузера пустая при каждом входе
  try { localStorage.clear(); sessionStorage.clear(); } catch { /* */ }
  const call = (op, path, data) => window.__dbCall(op, path, data ? JSON.stringify(data) : null).then((r) => (r ? JSON.parse(r) : null));
  const snap = (d) => ({ exists: !!d, data: () => d ?? undefined, metadata: { fromCache: false, hasPendingWrites: false } });
  const db = Object.freeze({
    doc: (path) => ({
      path,
      get: async () => snap(await call('get', path)),
      set: async (d) => { await call('set', path, d); },
      delete: async () => { await call('delete', path); },
      onSnapshot: (next) => {
        let last = '';
        const t = setInterval(async () => { const d = await call('get', path); const s = JSON.stringify(d); if (s !== last) { last = s; next(snap(d)); } }, 300);
        return () => clearInterval(t);
      },
    }),
  });
  const user = Object.freeze({ id: async () => uid, isOwner: async () => owner, canEdit: async () => owner });
  window.claude = Object.freeze({ use: async (name) => (name === 'db' ? db : name === 'user' ? user : null) });
}

const browser = await chromium.launch();
async function device({ uid, owner }) {
  const ctx = await browser.newContext({ viewport: { width: 380, height: 800 } });
  await ctx.route(/fonts\.(googleapis|gstatic)\.com/, (r) => r.abort());
  await ctx.exposeFunction('__dbCall', async (op, path, data) => {
    // правило артефакта: общий документ fpk/… пишет только владелец; личное — только сам человек
    if (op === 'set' || op === 'delete') {
      if (path.startsWith('fpk/') && !owner) throw Object.assign(new Error('denied'), { code: 'invalid_argument' });
      if (path.startsWith('data/users/') && !path.startsWith(`data/users/${uid}/`)) throw Object.assign(new Error('denied'), { code: 'invalid_argument' });
    }
    if (op === 'get') {
      if (path.startsWith('data/users/') && !path.startsWith(`data/users/${uid}/`)) return null;
      return docs.has(path) ? JSON.stringify(docs.get(path)) : null;
    }
    if (op === 'set') docs.set(path, JSON.parse(data));
    if (op === 'delete') docs.delete(path);
    return null;
  });
  await ctx.addInitScript(runtimeScript, { uid, owner });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  const go = async (h) => { await page.goto(BASE + '#/' + h); await page.waitForSelector('#main:not([aria-busy])', { timeout: 15000 }); await page.waitForTimeout(300); };
  return { ctx, page, go, errors };
}
const approvedText = async (page) => (await page.locator('.stat-grid').innerText()).replace(/\s+/g, ' ');

// ── телефон владельца ──
const phone = await device({ uid: 'u-owner', owner: true });

await step('Владелец: входит по своему PIN и утверждает 30 вопросов — статус «сохранено в базе»', async () => {
  const { page, go } = phone;
  await go('admin');
  assert.equal(await page.locator('#pin2').count(), 0, 'создать свой PIN нельзя — только ввести PIN владельца');
  await page.fill('#pin', '1234');
  await page.click('#pin-submit'); await page.waitForSelector('#pin', { state: 'detached', timeout: 10000 });
  await go('admin/review');
  await page.check('#rq-all');
  await page.click('#bulk-approve');
  await page.getByRole('dialog').getByRole('button', { name: 'Утвердить' }).click();
  await page.waitForTimeout(1500);
  const st = await page.locator('#save-state-admin').innerText();
  assert.match(st, /сохранены в базе артефакта/, st);
  assert.ok(docs.has('fpk/admin'), 'общий документ решений создан');
  const shared = JSON.stringify([...docs].filter(([k]) => k.startsWith('fpk/')));
  assert.ok(!shared.includes('pinHash'), 'PIN не попадает в общий документ');
});

await step('Повторный вход с пустой памятью: решения на месте, PIN не нужно создавать заново', async () => {
  const { page, go } = phone;
  await page.reload(); // init-скрипт снова очищает localStorage и sessionStorage
  await go('admin');
  assert.equal(await page.locator('#pin2').count(), 0, 'должен спрашивать существующий PIN, а не создавать новый');
  await page.fill('#pin', '1234');
  await page.click('#pin-submit'); await page.waitForSelector('#pin', { state: 'detached', timeout: 10000 });
  assert.match(await approvedText(page), /30\s*\/\s*1141/);
});

await step('Прогресс ученика сохраняется после повторного входа', async () => {
  const { page, go } = phone;
  await go('topic/opt-tir');
  await page.getByRole('button', { name: /Отметить тему как изученную/ }).click();
  await page.waitForTimeout(1500);
  await page.reload();
  await go('topic/opt-tir');
  assert.ok(await page.getByRole('button', { name: /Изучено — снять отметку/ }).isVisible());
});

// ── другое устройство того же владельца ──
const laptop = await device({ uid: 'u-owner', owner: true });
await step('Другое устройство владельца видит те же решения и прогресс', async () => {
  const { page, go } = laptop;
  await go('admin');
  await page.fill('#pin', '1234');
  await page.click('#pin-submit'); await page.waitForSelector('#pin', { state: 'detached', timeout: 10000 });
  assert.match(await approvedText(page), /30\s*\/\s*1141/);
  await go('topic/opt-tir');
  assert.ok(await page.getByRole('button', { name: /Изучено — снять отметку/ }).isVisible());
});

await step('Изменение на одном устройстве появляется на другом без перезагрузки', async () => {
  await laptop.go('admin/review');
  await laptop.page.check('#rq-all');
  await laptop.page.click('#bulk-approve');
  await laptop.page.getByRole('dialog').getByRole('button', { name: 'Утвердить' }).click();
  await laptop.page.waitForTimeout(1500);
  await phone.go('admin');
  if (await phone.page.locator('#pin').count()) { await phone.page.fill('#pin', '1234'); await phone.page.click('#pin-submit'); await phone.page.waitForSelector('#pin', { state: 'detached', timeout: 10000 }); }
  await phone.page.waitForTimeout(1500);
  assert.match(await approvedText(phone.page), /60\s*\/\s*1141/);
});

await step('Математика: решения и прогресс — в своих документах (fpk/math, data/users/<id>/math), физика не затронута', async () => {
  const { page } = phone;
  const physicsAdminBefore = JSON.stringify([...docs].filter(([k]) => k === 'fpk/admin' || k.startsWith('fpk/admin/')));
  const physicsUserBefore = JSON.stringify([...docs].filter(([k]) => k.startsWith('data/users/u-owner/state')));
  await page.goto(BASE + '#/m/admin/review'); await page.waitForSelector('#main:not([aria-busy])'); await page.waitForTimeout(300);
  if (await page.locator('#pin').count()) { await page.fill('#pin', '1234'); await page.click('#pin-submit'); await page.waitForSelector('#pin', { state: 'detached', timeout: 10000 }); }
  await page.check('#rq-all');
  await page.click('#bulk-approve');
  await page.getByRole('dialog').getByRole('button', { name: 'Утвердить' }).click();
  await page.waitForTimeout(1500);
  await page.goto(BASE + '#/m/topic/ma-1-1-2'); await page.waitForTimeout(400);
  await page.getByRole('button', { name: /Отметить тему как изученную/ }).click();
  await page.waitForTimeout(1500);
  assert.ok(docs.has('fpk/math'), 'решения математики — в общем документе fpk/math');
  assert.ok(docs.has('data/users/u-owner/math'), 'прогресс математики — в личном документе');
  assert.equal(JSON.stringify([...docs].filter(([k]) => k === 'fpk/admin' || k.startsWith('fpk/admin/'))), physicsAdminBefore, 'решения физики не изменились');
  assert.equal(JSON.stringify([...docs].filter(([k]) => k.startsWith('data/users/u-owner/state'))), physicsUserBefore, 'прогресс физики не изменился');
  // новый вход с пустой памятью: математика восстановлена из базы
  await page.reload(); await page.waitForSelector('#main:not([aria-busy])'); await page.waitForTimeout(300);
  await page.goto(BASE + '#/m/topic/ma-1-1-2'); await page.waitForTimeout(400);
  assert.ok(await page.getByRole('button', { name: /Изучено — снять отметку/ }).isVisible());
  await page.goto(BASE + '#/m/admin'); await page.waitForTimeout(400);
  if (await page.locator('#pin').count()) { await page.fill('#pin', '1234'); await page.click('#pin-submit'); await page.waitForSelector('#pin', { state: 'detached', timeout: 10000 }); }
  const m = (await approvedText(page)).match(/Вопросов в тестах (\d+)\s*\/\s*(\d+)/);
  assert.ok(m && Number(m[1]) >= 30 && m[2] !== '1141', `утверждения математики на месте: ${m?.[0]}`);
});

// ── одноклассник, которому открыли артефакт ──
const guest = await device({ uid: 'u-guest', owner: false });
await step('Не владелец видит утверждённые вопросы, но не может менять общую базу', async () => {
  const { page, go } = guest;
  await go('test');
  assert.ok(!(await page.locator('#start-test').isDisabled()), 'тест доступен по утверждённым вопросам');
  await go('admin');
  assert.equal(await page.locator('#pin2').count(), 0, 'свой PIN задать нельзя');
  await page.fill('#pin', '5555');
  await page.click('#pin-submit'); await page.waitForTimeout(1500);
  assert.match(await page.locator('.notice').last().innerText(), /Неверный PIN/);
  // даже зная PIN, не владелец артефакта не может изменить общую базу
  await page.fill('#pin', '1234');
  await page.click('#pin-submit'); await page.waitForSelector('#pin', { state: 'detached', timeout: 10000 });
  await go('admin/review');
  const before = JSON.stringify(docs.get('fpk/admin'));
  await page.check('#rq-all');
  await page.click('#bulk-approve');
  await page.getByRole('dialog').getByRole('button', { name: 'Утвердить' }).click();
  await page.waitForTimeout(1200);
  assert.equal(JSON.stringify(docs.get('fpk/admin')), before, 'общая база не изменилась');
  assert.match(await page.locator('#save-state-admin').innerText(), /только владелец/);
});

await step('Нет ошибок JavaScript', async () => {
  const all = [...phone.errors, ...laptop.errors, ...guest.errors];
  assert.equal(all.length, 0, all.join('; '));
});

await browser.close();
for (const r of results) console.log(r.join(' | '));
const fails = results.filter((r) => r[0] === 'FAIL').length;
console.log(`\n${results.length - fails}/${results.length} пройдено`);
process.exit(fails ? 1 : 0);
