#!/usr/bin/env python3
"""Сборка сайта stealthnet.software.

Сайт — обычная статика, и GitHub Pages отдаёт её как есть. Этот скрипт
нужен только чтобы шапка, оглавление и подвал не разъезжались между
страницами и между языками: правится один шаблон, а не два десятка копий.

Языков два. Английский лежит в корне, русский — в /ru/:

    /            /docs/…        английский, язык по умолчанию
    /ru/         /ru/docs/…     русский

Тексты — в content_en.py и content_ru.py, журнал изменений — в
CHANGELOG.md и CHANGELOG.ru.md. Готовый HTML коммитится в репозиторий.

    python3 build.py
"""
import json
import os
import re

import content_en
import content_ru

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = 'stealthnet.software'

# Всё, что различается между языками. Английский идёт первым: он в корне.
LANGS = [
    {
        'code': 'en',
        'dir': '',                      # каталог внутри репозитория
        'label': 'EN',                  # надпись на переключателе
        'other': ('ru', 'Русский'),     # куда ведёт переключатель
        'content': content_en,
        'changelog': 'CHANGELOG.md',
        'search': 'search.en.json',
        'site_title': 'STEALTHNET SOFTWARE — VPN business panel',
        'site_desc': ('Open-source VPN control panel: nodes, subscriptions, plans, '
                      'payments and a Telegram bot. Runs on your own server.'),
        'nav': {'docs': 'Documentation', 'changelog': "What's new",
                'features': 'Features', 'search': 'Search the documentation',
                'nothing': 'nothing found'},
        'foot': 'STEALTHNET SOFTWARE — a panel for selling VPN. Runs on your own server.',
        'toc': [
            ('Getting started', [('index.html', 'Quick start'), ('nodes.html', 'Nodes')]),
            ('Setup', [('protocols.html', 'Protocols and profiles'),
                       ('subscriptions.html', 'Subscriptions'),
                       ('billing.html', 'Plans and payments')]),
            ('Running it', [('troubleshooting.html', 'When something breaks'),
                            ('faq.html', 'Questions'),
                            ('changelog.html', "What's new")]),
        ],
        'e404': {'title': 'Page not found', 'desc': 'There is no such page on this site.',
                 'lead': 'The address may have a typo, or the section has moved.',
                 'docs': 'Go to the documentation', 'home': 'Go to the home page'},
        'cl_desc': 'Changes in the STEALTHNET SOFTWARE panel.',
    },
    {
        'code': 'ru',
        'dir': 'ru',
        'label': 'RU',
        'other': ('en', 'English'),
        'content': content_ru,
        'changelog': 'CHANGELOG.ru.md',
        'search': 'search.ru.json',
        'site_title': 'STEALTHNET SOFTWARE — панель для продажи VPN',
        'site_desc': ('Открытая панель управления VPN: ноды, подписки, тарифы, приём '
                      'оплат и телеграм-бот. Ставится на свой сервер.'),
        'nav': {'docs': 'Документация', 'changelog': 'Что нового',
                'features': 'Возможности', 'search': 'Поиск по документации',
                'nothing': 'ничего не нашлось'},
        'foot': 'STEALTHNET SOFTWARE — панель для продажи VPN. Ставится на свой сервер.',
        'toc': [
            ('Начало', [('index.html', 'Быстрый старт'), ('nodes.html', 'Ноды')]),
            ('Настройка', [('protocols.html', 'Протоколы и профили'),
                           ('subscriptions.html', 'Подписки'),
                           ('billing.html', 'Тарифы и оплата')]),
            ('Эксплуатация', [('troubleshooting.html', 'Если что-то не работает'),
                              ('faq.html', 'Вопросы'),
                              ('changelog.html', 'Что нового')]),
        ],
        'e404': {'title': 'Такой страницы нет', 'desc': 'Такой страницы на сайте нет.',
                 'lead': 'Возможно, адрес набран с опечаткой или раздел переехал.',
                 'docs': 'К документации', 'home': 'На главную'},
        'cl_desc': 'Изменения панели STEALTHNET SOFTWARE.',
    },
]

LOGO = ('<span class="brand-mark">S</span>'
        '<span><span class="brand-name">STEALTHNET</span>'
        '<span class="brand-sub">SOFTWARE</span></span>')


def root_of(lang):
    """Корень языка: '/' для английского, '/ru/' для остальных."""
    return '/' + (lang['dir'] + '/' if lang['dir'] else '')


def head(lang, title, desc, depth):
    # depth — число уровней вложенности; строка означает готовый префикс.
    # Странице 404 нужен абсолютный путь: её отдают в ответ на любой адрес,
    # и относительные ссылки посчитались бы от несуществующего места.
    # Стили и скрипт общие для языков и лежат в /assets/: относительный
    # путь из /ru/docs/ увёл бы в несуществующий /ru/assets/.
    up = depth if isinstance(depth, str) else '../' * depth
    return f'''<!doctype html>
<html lang="{lang['code']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22><rect width=%2232%22 height=%2232%22 rx=%228%22 fill=%22%2312233D%22/><text x=%2216%22 y=%2222%22 font-size=%2218%22 font-family=%22sans-serif%22 font-weight=%22700%22 fill=%22white%22 text-anchor=%22middle%22>S</text></svg>">
<link rel="stylesheet" href="/assets/site.css">
<script>
  /* Тему ставим до отрисовки: иначе при тёмной будет вспышка белого. */
  (function(){{try{{var t=localStorage.getItem('sns_theme')||'light';
    document.documentElement.setAttribute('data-theme',t==='dark'?'dark':'light');
    document.documentElement.style.colorScheme=t==='dark'?'dark':'light';}}catch(e){{}}}})();
</script>
</head>
<body>'''


def lang_switch(lang, page):
    """Переключатель языка.

    Ведёт на ту же страницу в другом языке, а не на его главную: уводить
    читателя из раздела, который он открыл, — самый простой способ его
    потерять. `page` — путь внутри языка, например 'docs/nodes.html'."""
    code, name = lang['other']
    other = next(x for x in LANGS if x['code'] == code)
    return (f'<a class="lang" href="{root_of(other)}{page}" hreflang="{code}" '
            f'lang="{code}" title="{name}">{other["label"]}</a>')


def topbar(lang, page, depth, active):
    up = depth if isinstance(depth, str) else '../' * depth
    n = lang['nav']

    def link(href, label, key, cls=''):
        cur = ' aria-current="page"' if active == key else ''
        klass = f' class="{cls}"' if cls else ''
        return f'<a href="{up}{href}"{cur}{klass}>{label}</a>'

    return f'''
<header class="top">
  <div class="top-in">
    <a class="brand" href="{up}index.html">{LOGO}</a>
    <nav>
      {link('docs/index.html', n['docs'], 'docs')}
      {link('docs/changelog.html', n['changelog'], 'changelog', 'hide-sm')}
      {link('index.html#features', n['features'], '', 'hide-sm')}
      <a href="{lang['content'].GH_LINK}" class="hide-sm">GitHub</a>
      {lang_switch(lang, page)}
      <button class="icon-btn" id="themeBtn" onclick="__toggleTheme()" title="Theme"></button>
    </nav>
  </div>
</header>'''


def footer(lang, depth):
    up = depth if isinstance(depth, str) else '../' * depth
    n = lang['nav']
    return f'''
<footer>
  <div class="foot-in">
    <span>{lang['foot']}</span>
    <span class="right">
      <a href="{up}docs/index.html">{n['docs']}</a>
      <a href="{up}docs/changelog.html">{n['changelog']}</a>
      <a href="{lang['content'].GH_LINK}">GitHub</a>
    </span>
  </div>
</footer>
<script src="/assets/site.js"></script>
</body>
</html>'''


def out_path(lang, *parts):
    path = os.path.join(ROOT, lang['dir'], *parts) if lang['dir'] \
        else os.path.join(ROOT, *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def doc_nav(lang, current):
    out = ['<nav id="docNav">']
    for group, pages in lang['toc']:
        out.append(f'<h4>{group}</h4>')
        for href, label in pages:
            cur = ' aria-current="page"' if href == current else ''
            out.append(f'<a href="{href}"{cur}>{label}</a>')
    out.append('</nav>')
    return '\n'.join(out)


def make_doc_page(lang):
    def doc_page(fname, title, desc, body, prev=None, nxt=None):
        steps = ''
        if prev or nxt:
            parts = []
            if prev:
                parts.append(f'<a class="btn" href="{prev[0]}">← {prev[1]}</a>')
            if nxt:
                parts.append(f'<a class="btn primary" href="{nxt[0]}">{nxt[1]} →</a>')
            steps = f'<div class="next">{"".join(parts)}</div>'

        html = (head(lang, f'{title} — STEALTHNET SOFTWARE', desc, 1)
                + topbar(lang, f'docs/{fname}', 1, 'docs')
                + f'''
<div class="wrap doc">
  <aside class="side">
    <input class="search" id="docSearch" type="search"
           placeholder="{lang['nav']['search']}" autocomplete="off"
           data-index="{lang['search']}" data-empty="{lang['nav']['nothing']}">
    <div id="searchHits" hidden></div>
    {doc_nav(lang, fname)}
  </aside>
  <main class="content">
    <h1>{title}</h1>
    {body}
    {steps}
  </main>
</div>'''
                + footer(lang, 1))
        with open(out_path(lang, 'docs', fname), 'w', encoding='utf-8') as f:
            f.write(html)
    return doc_page


def make_landing(lang):
    def landing(body):
        html = (head(lang, lang['site_title'], lang['site_desc'], 0)
                + topbar(lang, 'index.html', 0, 'home') + body + footer(lang, 0))
        with open(out_path(lang, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
    return landing


def md_inline(s):
    """Разметка внутри строки: код, жирный, ссылки."""
    s = (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    return s


def changelog(lang, doc_page):
    """Страница «Что нового» из CHANGELOG.

    Файл один на язык, чтобы запись не приходилось дублировать: правится
    markdown, страница пересобирается отсюда. Разбирается ровно та разметка,
    которая в нём используется, — заголовки, списки, абзацы и разделитель.

    Возвращает заголовок, первый абзац и три первых пункта последнего
    выпуска: витрина показывает их, чтобы попасть на страницу можно было
    с главной, а не только из оглавления документации."""
    path = os.path.join(ROOT, lang['changelog'])
    with open(path, encoding='utf-8') as f:
        text = f.read()
    # Комментарии — записки для тех, кто ведёт файл; посетителю они ни к чему.
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    lines = text.split('\n')

    out, in_list, seen_h1 = [], False, False
    latest = {'title': '', 'anchor': '', 'note': '', 'items': []}

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
            if latest['title'] and len(latest['items']) < 3:
                latest['items'].append(md_inline(item))
        elif line.startswith('### '):
            close_list()
            out.append(f'<h3>{md_inline(line[4:])}</h3>')
        elif line.startswith('## '):
            close_list()
            title = line[3:].strip()
            anchor = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') or 'v'
            out.append(f'<h2 id="{anchor}" class="rel">{md_inline(title)}</h2>')
            if not latest['title']:            # самый верхний выпуск — свежий
                latest.update(title=md_inline(title), anchor=anchor)
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
            if latest['title'] and not latest['note']:
                latest['note'] = md_inline(para)
        i += 1
    close_list()

    if not seen_h1:
        raise SystemExit(f'{lang["changelog"]}: нет заголовка первого уровня')
    if not latest['title']:
        raise SystemExit(f'{lang["changelog"]}: нет ни одного выпуска (заголовок «## …»)')

    title = lang['nav']['changelog']
    doc_page('changelog.html', title, lang['cl_desc'], '\n'.join(out),
             prev=(lang['toc'][-1][1][-2][0], lang['toc'][-1][1][-2][1]))
    return latest


def not_found(lang):
    """Страница для несуществующих адресов.

    GitHub Pages отдаёт её в ответ на любой ненайденный путь, поэтому все
    ссылки внутри — абсолютные. Файл в корне обслуживает и /ru/: своей
    страницы 404 для подкаталога Pages не поддерживает."""
    base = root_of(lang)
    e = lang['e404']
    html = (head(lang, f'{e["title"]} — STEALTHNET SOFTWARE', e['desc'], base)
            + topbar(lang, '', base, '404')  # ключа нет в меню: подсвечивать нечего
            + f'''
<div class="wrap notfound">
  <!-- Украшение: смысл несёт заголовок ниже, поэтому для чтения с экрана скрыто. -->
  <p class="code404" aria-hidden="true">404</p>
  <h1>{e['title']}</h1>
  <p class="lead">{e['lead']}</p>
  <div class="cta">
    <a class="btn primary" href="{base}docs/index.html">{e['docs']}</a>
    <a class="btn" href="{base}">{e['home']}</a>
  </div>
</div>'''
            + footer(lang, base))
    with open(out_path(lang, '404.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def build_search_index(lang):
    """Индекс для поиска: заголовки разделов и текст под ними.

    Собираем из готовых страниц, а не из отдельного источника, — тогда
    индекс не разъедется с содержимым."""
    items = []
    for _, pages in lang['toc']:
        for href, label in pages:
            path = out_path(lang, 'docs', href)
            if not os.path.exists(path):
                raise SystemExit(f'{href} есть в оглавлении {lang["code"]}, но файла нет')
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
                print(f'  внимание: {lang["code"]}/{href} не попала в поиск — нет разделов h2')
    with open(os.path.join(ROOT, 'assets', lang['search']), 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False)
    return len(items)


if __name__ == '__main__':
    for lang in LANGS:
        doc_page = make_doc_page(lang)
        # Сначала журнал: витрине нужен последний выпуск, чтобы показать его
        # на главной, а не прятать ссылку в оглавлении документации.
        latest = changelog(lang, doc_page)
        lang['content'].build(make_landing(lang), doc_page, latest)
        not_found(lang)
        n = build_search_index(lang)
        print(f'  {lang["code"]}: собрано, записей в поиске {n}')

    with open(os.path.join(ROOT, 'CNAME'), 'w') as f:
        f.write(DOMAIN + '\n')
    # .nojekyll: без него Pages прогоняет содержимое через Jekyll и
    # выбрасывает каталоги, начинающиеся с подчёркивания.
    open(os.path.join(ROOT, '.nojekyll'), 'w').close()
    print('готово')
