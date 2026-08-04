#!/usr/bin/env python3
"""Сборка сайта stealthnet.software.

Сайт — обычная статика, и GitHub Pages отдаёт её как есть. Этот скрипт
нужен только чтобы шапка, оглавление и подвал не разъезжались между
страницами: правится один шаблон, а не восемь копий.

Готовый HTML лежит в репозитории и коммитится. Хотите поправить одну
страницу — правьте HTML напрямую, скрипт запускать не обязательно.

    python3 build.py
"""
import json
import os
import re

import content

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = 'stealthnet.software'

# Оглавление документации: заголовок раздела → список страниц.
NAV = [
    ('Начало', [
        ('index.html', 'Быстрый старт'),
        ('nodes.html', 'Ноды'),
    ]),
    ('Настройка', [
        ('protocols.html', 'Протоколы и профили'),
        ('subscriptions.html', 'Подписки'),
        ('billing.html', 'Тарифы и оплата'),
    ]),
    ('Эксплуатация', [
        ('troubleshooting.html', 'Если что-то не работает'),
        ('faq.html', 'Вопросы'),
        ('changelog.html', 'Что нового'),
    ]),
]

LOGO = ('<span class="brand-mark">S</span>'
        '<span><span class="brand-name">STEALTHNET</span>'
        '<span class="brand-sub">SOFTWARE</span></span>')


def head(title, desc, depth):
    # depth — число уровней вложенности; строка означает готовый префикс.
    # Странице 404 нужен абсолютный '/': её отдают в ответ на любой путь,
    # и относительные ссылки посчитались бы от несуществующего адреса.
    up = depth if isinstance(depth, str) else '../' * depth
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22><rect width=%2232%22 height=%2232%22 rx=%228%22 fill=%22%2312233D%22/><text x=%2216%22 y=%2222%22 font-size=%2218%22 font-family=%22sans-serif%22 font-weight=%22700%22 fill=%22white%22 text-anchor=%22middle%22>S</text></svg>">
<link rel="stylesheet" href="{up}assets/site.css">
<script>
  /* Тему ставим до отрисовки: иначе при тёмной будет вспышка белого. */
  (function(){{try{{var t=localStorage.getItem('sns_theme')||'light';
    document.documentElement.setAttribute('data-theme',t==='dark'?'dark':'light');
    document.documentElement.style.colorScheme=t==='dark'?'dark':'light';}}catch(e){{}}}})();
</script>
</head>
<body>'''


def topbar(depth, active):
    up = depth if isinstance(depth, str) else '../' * depth
    link = lambda href, label, key, cls='': (
        f'<a href="{up}{href}"{" aria-current=\"page\"" if active == key else ""}'
        f'{f" class=\"{cls}\"" if cls else ""}>{label}</a>')
    return f'''
<header class="top">
  <div class="top-in">
    <a class="brand" href="{up}index.html">{LOGO}</a>
    <nav>
      {link('docs/index.html', 'Документация', 'docs')}
      {link('index.html#features', 'Возможности', '', 'hide-sm')}
      <a href="{content.GH_LINK}" class="hide-sm">GitHub</a>
      <button class="icon-btn" id="themeBtn" onclick="__toggleTheme()" title="Тема"></button>
    </nav>
  </div>
</header>'''


def footer(depth):
    up = depth if isinstance(depth, str) else '../' * depth
    return f'''
<footer>
  <div class="foot-in">
    <span>STEALTHNET SOFTWARE — панель для продажи VPN. Ставится на свой сервер.</span>
    <span class="right">
      <a href="{up}docs/index.html">Документация</a>
      <a href="{content.GH_LINK}">GitHub</a>
    </span>
  </div>
</footer>
<script src="{up}assets/site.js"></script>
</body>
</html>'''


def doc_nav(current):
    out = ['<nav id="docNav">']
    for group, pages in NAV:
        out.append(f'<h4>{group}</h4>')
        for href, label in pages:
            cur = ' aria-current="page"' if href == current else ''
            out.append(f'<a href="{href}"{cur}>{label}</a>')
    out.append('</nav>')
    return '\n'.join(out)


def doc_page(fname, title, desc, body, prev=None, nxt=None):
    nav_html = doc_nav(fname)
    steps = ''
    if prev or nxt:
        parts = []
        if prev:
            parts.append(f'<a class="btn" href="{prev[0]}">← {prev[1]}</a>')
        if nxt:
            parts.append(f'<a class="btn primary" href="{nxt[0]}">{nxt[1]} →</a>')
        steps = f'<div class="next">{"".join(parts)}</div>'

    html = (head(f'{title} — STEALTHNET SOFTWARE', desc, 1)
            + topbar(1, 'docs')
            + f'''
<div class="wrap doc">
  <aside class="side">
    <input class="search" id="docSearch" type="search" placeholder="Поиск по документации" autocomplete="off">
    <div id="searchHits" hidden></div>
    {nav_html}
  </aside>
  <main class="content">
    <h1>{title}</h1>
    {body}
    {steps}
  </main>
</div>'''
            + footer(1))
    with open(os.path.join(ROOT, 'docs', fname), 'w', encoding='utf-8') as f:
        f.write(html)


def landing(body):
    html = head('STEALTHNET SOFTWARE — панель для продажи VPN',
                'Открытая панель управления VPN: ноды, подписки, тарифы, приём оплат '
                'и телеграм-бот. Ставится на свой сервер.', 0) \
        + topbar(0, 'home') + body + footer(0)
    with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def md_inline(s):
    """Разметка внутри строки: код, жирный, ссылки."""
    s = (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    return s


def changelog():
    """Страница «Что нового» из CHANGELOG.md.

    Файл один, чтобы запись не приходилось дублировать: правится CHANGELOG.md,
    страница пересобирается отсюда. Разбирается ровно та разметка, которая в
    нём используется, — заголовки, списки, абзацы и разделитель."""
    path = os.path.join(ROOT, 'CHANGELOG.md')
    with open(path, encoding='utf-8') as f:
        text = f.read()
    # Комментарии — записки для тех, кто ведёт файл; посетителю они ни к чему.
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    lines = text.split('\n')

    out, in_list, seen_h1 = [], False, False

    def close_list():
        nonlocal in_list
        if in_list:
            out.append('</ul>')
            in_list = False

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        # Пункт списка может занимать несколько строк — собираем целиком.
        if line.startswith('- '):
            item = line[2:].strip()
            while i + 1 < len(lines) and lines[i + 1].startswith('  ') \
                    and lines[i + 1].strip():
                i += 1
                item += ' ' + lines[i].strip()
            if not in_list:
                out.append('<ul>')
                in_list = True
            out.append(f'<li>{md_inline(item)}</li>')
        elif line.startswith('### '):
            close_list()
            out.append(f'<h3>{md_inline(line[4:])}</h3>')
        elif line.startswith('## '):
            close_list()
            title = line[3:].strip()
            anchor = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') or 'v'
            out.append(f'<h2 id="{anchor}" class="rel">{md_inline(title)}</h2>')
        elif line.startswith('# '):
            close_list()
            seen_h1 = True          # заголовок страницы ставит doc_page
        elif line.strip() == '---':
            close_list()
            out.append('<hr>')
        elif line.strip():
            close_list()
            para = line.strip()
            while i + 1 < len(lines) and lines[i + 1].strip() \
                    and not lines[i + 1].startswith(('#', '- ', '---')):
                i += 1
                para += ' ' + lines[i].strip()
            out.append(f'<p>{md_inline(para)}</p>')
        i += 1
    close_list()

    if not seen_h1:
        raise SystemExit('CHANGELOG.md: нет заголовка первого уровня')

    doc_page('changelog.html', 'Что нового',
             'Изменения панели STEALTHNET SOFTWARE.',
             '\n'.join(out), prev=('faq.html', 'Вопросы'))


def not_found():
    """Страница для несуществующих адресов.

    GitHub Pages отдаёт её в ответ на любой ненайденный путь, поэтому все
    ссылки внутри — абсолютные."""
    html = (head('Страница не найдена — STEALTHNET SOFTWARE',
                 'Такой страницы на сайте нет.', '/')
            + topbar('/', '404')  # ключ, которого нет в меню: подсвечивать нечего
            + '''
<div class="wrap notfound">
  <!-- Украшение: смысл несёт заголовок ниже, поэтому для чтения с экрана скрыто. -->
  <p class="code404" aria-hidden="true">404</p>
  <h1>Такой страницы нет</h1>
  <p class="lead">Возможно, адрес набран с опечаткой или раздел переехал.</p>
  <div class="cta">
    <a class="btn primary" href="/docs/index.html">К документации</a>
    <a class="btn" href="/">На главную</a>
  </div>
</div>'''
            + footer('/'))
    with open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def build_search_index():
    """Индекс для поиска: заголовки разделов и текст под ними.

    Собираем из готовых страниц, а не из отдельного источника, — тогда
    индекс не разъедется с содержимым."""
    items = []
    for _, pages in NAV:
        for href, label in pages:
            path = os.path.join(ROOT, 'docs', href)
            if not os.path.exists(path):
                raise SystemExit(f'{href} есть в оглавлении, но файла нет')
            html = open(path, encoding='utf-8').read()
            body = html.split('<main class="content">', 1)[-1]
            # Атрибуты у h2 могут быть любые — иначе страница молча выпадает
            # из поиска, и заметить это можно только случайно.
            before = len(items)
            for m in re.finditer(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>(.*?)(?=<h2 |</main>)',
                                 body, re.S):
                anchor, title, chunk = m.group(1), m.group(2), m.group(3)
                text = re.sub(r'<[^>]+>', ' ', chunk)
                text = re.sub(r'\s+', ' ', text).strip()[:400]
                items.append({'url': f'{href}#{anchor}', 'section': label,
                              'title': re.sub(r'<[^>]+>', '', title), 'text': text})
            if len(items) == before:
                print(f'  внимание: {href} не попала в поиск — нет разделов h2')
    with open(os.path.join(ROOT, 'assets', 'search.json'), 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False)
    return len(items)


if __name__ == '__main__':
    content.build(landing, doc_page)
    changelog()
    not_found()
    n = build_search_index()
    with open(os.path.join(ROOT, 'CNAME'), 'w') as f:
        f.write(DOMAIN + '\n')
    # .nojekyll: без него Pages прогоняет содержимое через Jekyll и
    # выбрасывает каталоги, начинающиеся с подчёркивания.
    open(os.path.join(ROOT, '.nojekyll'), 'w').close()
    print(f'собрано; записей в поиске: {n}')
