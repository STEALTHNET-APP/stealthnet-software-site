/* Обвязка сайта: тема, копирование кода и поиск по документации.
 *
 * Ничего, кроме этого файла, странице не нужно — ни сборки, ни зависимостей.
 */
'use strict';

/* ── тема ──
   Светлая по умолчанию, как в панели. Атрибут ставится до первой
   отрисовки скриптом в <head>, здесь только переключение. */
(function theme() {
  const KEY = 'sns_theme';
  const root = document.documentElement;
  const apply = (t) => {
    root.setAttribute('data-theme', t === 'dark' ? 'dark' : 'light');
    root.style.colorScheme = t === 'dark' ? 'dark' : 'light';
  };
  window.__toggleTheme = () => {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem(KEY, next); } catch (_) {}
    apply(next);
    paintThemeButton();
  };
  function paintThemeButton() {
    const b = document.getElementById('themeBtn');
    if (!b) return;
    const dark = root.getAttribute('data-theme') === 'dark';
    b.title = dark ? 'Светлая тема' : 'Тёмная тема';
    b.innerHTML = dark
      ? '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
      : '<svg viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>';
  }
  document.addEventListener('DOMContentLoaded', paintThemeButton);
})();

/* ── копирование команд ──
   Кнопку добавляем скриптом: в разметке она была бы лишним шумом в
   каждом блоке. Через data-атрибут, потому что кавычки внутри команд
   ломают обработчик, записанный прямо в onclick. */
document.addEventListener('DOMContentLoaded', () => {
  for (const pre of document.querySelectorAll('pre')) {
    const b = document.createElement('button');
    b.className = 'copy';
    b.type = 'button';
    b.textContent = 'копировать';
    b.addEventListener('click', () => {
      const text = pre.querySelector('code')?.innerText ?? pre.innerText;
      const done = () => { b.textContent = 'скопировано'; setTimeout(() => { b.textContent = 'копировать'; }, 1600); };
      const fail = () => { b.textContent = 'не вышло — выделите вручную'; };
      if (navigator.clipboard?.writeText) navigator.clipboard.writeText(text).then(done, fail);
      else fail();
    });
    pre.appendChild(b);
  }
});

/* ── поиск по документации ──
   Индекс собирается из содержимого самих страниц (assets/search.json).
   Совпадения ищем по заголовкам и первому абзацу раздела: этого хватает,
   чтобы попасть в нужное место, и не требует ни сервера, ни библиотеки. */
document.addEventListener('DOMContentLoaded', async () => {
  const input = document.getElementById('docSearch');
  const box = document.getElementById('searchHits');
  const nav = document.getElementById('docNav');
  if (!input || !box) return;

  let index = [];
  try {
    const res = await fetch(new URL('../assets/search.json', document.baseURI));
    if (res.ok) index = await res.json();
  } catch (_) { /* поиск не критичен: без него оглавление на месте */ }

  const norm = (s) => s.toLowerCase().replace(/ё/g, 'е');

  input.addEventListener('input', () => {
    const q = norm(input.value.trim());
    if (q.length < 2) {
      box.innerHTML = '';
      box.hidden = true;
      if (nav) nav.hidden = false;
      return;
    }
    const hits = index
      .map((it) => {
        const hay = norm(it.title + ' ' + it.section + ' ' + it.text);
        const at = hay.indexOf(q);
        return at < 0 ? null : { it, at };
      })
      .filter(Boolean)
      .sort((a, b) => a.at - b.at)
      .slice(0, 8);

    box.hidden = false;
    if (nav) nav.hidden = true;
    box.innerHTML = hits.length
      ? hits.map((h) => `<a class="hit" href="${h.it.url}"><b>${h.it.section}</b><br>${h.it.title}</a>`).join('')
      : '<div class="hit">ничего не нашлось</div>';
  });
});
