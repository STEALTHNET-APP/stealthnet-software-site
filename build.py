#!/usr/bin/env python3
"""Build the bilingual presentation and complete public documentation for GitHub Pages."""
import html, json, posixpath, re, shutil
from pathlib import Path
from urllib.parse import urlsplit, quote
import markdown
from catalog import GROUPS
ROOT=Path(__file__).resolve().parent
GH='https://github.com/STEALTHNET-APP/STEALTHNET-SOFTWARE'
COMMUNITY='https://t.me/stealthnet_admin_panel'
DOMAIN='https://stealthnet.software'
WALLET='THQA9Qnx87NcHAwYrcCTBGSi6BhY72LXEZ'
SOURCE=json.loads((ROOT/'content/source.json').read_text())
VERSION=SOURCE['version']
assert re.fullmatch(r'\d+\.\d+\.\d+(?:-[a-zA-Z0-9.-]+)?', VERSION), 'Missing or invalid source version; run sync_docs.py'
E=lambda s:html.escape(str(s),quote=True)
LABELS={
 'en':dict(home='Project',docs='Documentation',install='Install STEALTHNET',community='Community',search='Search documentation',placeholder='Search for a question, setting or command…',close='Close',contents='Contents',onpage='On this page',prev='Previous',next='Next',edit='Edit on GitHub',copied='Copied',copy='Copy',failed='Could not copy. Select and copy the text manually.',empty='No results. Try “install”, “node” or “subscription”.',loading='Searching…',searcherror='Search could not load. Browse the categories below or try again.',browse='Browse documentation',all='All categories',release='Release',source='Open source · AGPL-3.0',skip='Skip to content',openimage='View full screenshot',demo='Real interfaces with demonstration data.',guide='Open guide',navigatetitle='Documentation navigation',support='Support the project',wallet='Copy TRC20 address',read='Read the guide',overview='Overview',article='Article',up='Back to top'),
 'ru':dict(home='Проект',docs='Документация',install='Установить STEALTHNET',community='Сообщество',search='Поиск по документации',placeholder='Вопрос, настройка или команда…',close='Закрыть',contents='Содержание',onpage='На этой странице',prev='Назад',next='Далее',edit='Изменить на GitHub',copied='Скопировано',copy='Копировать',failed='Не удалось скопировать. Выделите и скопируйте текст вручную.',empty='Ничего не найдено. Попробуйте «установка», «нода» или «подписка».',loading='Ищем…',searcherror='Поиск не загрузился. Откройте категорию ниже или попробуйте снова.',browse='Открыть документацию',all='Все категории',release='Релиз',source='Открытый код · AGPL-3.0',skip='Перейти к содержимому',openimage='Открыть скриншот',demo='Настоящие интерфейсы с демонстрационными данными.',guide='Открыть инструкцию',navigatetitle='Навигация по документации',support='Поддержать проект',wallet='Скопировать адрес TRC20',read='Читать инструкцию',overview='Обзор',article='Статья',up='Наверх')}
PATHS={x[0] for g in GROUPS for x in g[3]}
for lang in ('en','ru'):
 actual={str(p.relative_to(ROOT/'content'/lang).with_suffix('')) for p in (ROOT/'content'/lang).rglob('*.md')}-{'README'}
 if actual!=PATHS:raise SystemExit(f'Uncategorized or missing {lang}: {actual ^ PATHS}')

def icon(name):
 shapes={'arrow':'<path d="M5 12h14m-6-6 6 6-6 6"/>','external':'<path d="M14 3h7v7m0-7L10 14M10 3H4a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1v-6"/>','search':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>','close':'<path d="m6 6 12 12M6 18 18 6"/>','copy':'<rect x="8" y="8" width="12" height="13" rx="2"/><path d="M16 8V3H3v13h5"/>','book':'<path d="M12 5v16M3 3h5a4 4 0 0 1 4 2 4 4 0 0 1 4-2h5v16h-5a4 4 0 0 0-4 2 4 4 0 0 0-4-2H3Z"/>','chevron':'<path d="m9 5 7 7-7 7"/>','menu':'<path d="M4 6h16M4 12h16M4 18h16"/>','telegram':'<path d="m3 10 18-7-4 18-6-5-4 3v-7m4 4 6-8-10 4-4-2Z"/>','github':'<path d="M9 20c-5 1-5-3-7-3m14 5v-4c0-1-.4-2-1-2.5 4-.5 6-2 6-6.5 0-1.5-.5-2.5-1.5-3.5.4-1 .3-2-.2-3-2 0-3 1-3.5 1.5a12 12 0 0 0-7.6 0C7.7 3.5 6.7 2.5 4.7 2.5c-.5 1-.6 2-.2 3C3.5 6.5 3 7.5 3 9c0 4.5 2 6 6 6.5-.6.5-1 1.5-1 2.5v4"/>'}
 return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{shapes[name]}</svg>'
MARK=(ROOT/'assets/logo.svg').read_text().strip()
def base(l):return '/ru/' if l=='ru' else '/'
def docurl(l,key):return base(l)+'docs/'+('index' if key=='README' else key)+'.html'
def title_for(l,key):return next((x[2 if l=='ru' else 1] for g in GROUPS for x in g[3] if x[0]==key),LABELS[l]['docs'])
def group_for(key):return next((g for g in GROUPS if any(x[0]==key for x in g[3])),None)
def linkbutton(url,label,primary=False,symbol='arrow'):
 return f'<a class="button{" primary" if primary else ""}" href="{E(url)}">{E(label)}{icon(symbol)}</a>'
def header(l,page,docs=False):
 t=LABELS[l];other='ru' if l=='en' else 'en'
 return f'''<a class="skip" href="#main">{t['skip']}</a><header class="site-header"><div class="header-inner"><a class="brand" href="{base(l)}" aria-label="STEALTHNET">{MARK}<span>STEALTHNET</span></a><nav aria-label="{'Основная навигация' if l=='ru' else 'Main navigation'}"><a class="nav-link {'active' if not docs else ''}" href="{base(l)}">{t['home']}</a><a class="nav-link {'active' if docs else ''}" href="{docurl(l,'README')}">{t['docs']}</a><a class="nav-link github-link" href="{GH}">{icon('github')} GitHub</a></nav><div class="header-actions">{f'<button class="search-trigger" data-search aria-label="{t["search"]}">{icon("search")}<span>{t["search"]}</span><kbd>⌘ K</kbd></button>' if docs else ''}<a class="language" href="{base(other)+page}" hreflang="{other}" lang="{other}" aria-label="{'Read this page in English' if l=='ru' else 'Читать эту страницу на русском'}">{other.upper()}</a>{'' if docs else linkbutton(docurl(l,'installation'),t['install'],True)}</div></div></header>'''
def footer(l):
 t=LABELS[l]
 return f'''<footer class="site-footer"><div class="footer-brand"><a class="brand" href="{base(l)}">{MARK}<span>STEALTHNET</span></a><p>{'Инфраструктура ваша. Управление — в одной панели.' if l=='ru' else 'Your infrastructure. One place to manage it.'}</p></div><div class="footer-links"><a href="{docurl(l,'README')}">{t['docs']}</a><a href="{GH}">GitHub</a><a href="{COMMUNITY}">{t['community']}</a><a href="{GH}/blob/main/LICENSE">AGPL-3.0</a></div><p class="footer-meta">© 2026 STEALTHNET · <a href="{GH}/releases/latest">{t['release']} {E(VERSION)}</a></p></footer>'''
def overlays(l):
 t=LABELS[l]
 return f'''<dialog class="search-dialog" id="search-dialog" aria-labelledby="search-title"><div class="dialog-top"><h2 id="search-title">{t['search']}</h2><button class="icon-button" data-close aria-label="{t['close']}">{icon('close')}</button></div><label class="search-field">{icon('search')}<span class="sr-only">{t['search']}</span><input type="search" autocomplete="off" id="search-input" placeholder="{t['placeholder']}" /></label><p class="search-status" id="search-status" role="status"></p><div id="search-results"></div><div class="search-bottom">{t['contents']}<a href="{docurl(l,'README')}">{t['all']}{icon('arrow')}</a></div></dialog><dialog class="image-dialog" id="image-dialog" aria-label="{t['openimage']}"><button class="icon-button" data-close aria-label="{t['close']}">{icon('close')}</button><p></p></dialog><div class="toast" id="toast" role="status"></div>'''
def document(l,title,desc,body,page,docs=False):
 t=LABELS[l];url=DOMAIN+base(l)+page;other='ru' if l=='en' else 'en'
 return f'''<!doctype html><html lang="{l}"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>{E(title)} · STEALTHNET</title><meta name="description" content="{E(desc)}"/><meta name="theme-color" content="{'#fafbf9' if docs else '#102522'}"/><link rel="canonical" href="{url}"/><link rel="alternate" hreflang="{other}" href="{DOMAIN+base(other)+page}"/><link rel="icon" href="/assets/favicon.svg"/><meta property="og:type" content="website"/><meta property="og:title" content="{E(title)} · STEALTHNET"/><meta property="og:description" content="{E(desc)}"/><meta property="og:url" content="{url}"/><meta property="og:image" content="{DOMAIN}/assets/media/panel-nodes-{l}.png"/><link rel="preload" href="/assets/fonts/onest.ttf" as="font" type="font/ttf" crossorigin/><link rel="stylesheet" href="/assets/site.css?v=20260914"/><script defer src="/assets/site.js?v=20260914"></script></head><body class="{'docs-page' if docs else 'landing-page'}" data-lang="{l}">{header(l,page,docs)}{body}{footer(l)}{overlays(l)}<script type="application/json" id="ui-strings">{json.dumps(t,ensure_ascii=False).replace('<','&lt;')}</script></body></html>'''
def write(url,text):
 p=ROOT/url.lstrip('/');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)

def landing(l):
 ru=l=='ru';t=LABELS[l]
 gallery=[('panel-nodes','Панель' if ru else 'Admin panel','Вся сеть перед глазами' if ru else 'Your whole network in view','Ноды, профили, состояние серверов и доступ клиентов — в одной панели.' if ru else 'Nodes, profiles, server health and customer access in a single panel.'),('storefront','Сайт' if ru else 'Storefront','Ваш сервис начинается здесь' if ru else 'The front door to your service','Витрина с вашими тарифами, брендингом и входом в кабинет.' if ru else 'Your plans, your branding and a clear path to the customer account.'),('cabinet','Кабинет' if ru else 'Customer account','Подписка в руках клиента' if ru else 'Give customers control','Подписка, устройства, трафик и покупки без обращения к администратору.' if ru else 'Subscriptions, devices, traffic and purchases without asking an administrator.'),('miniapp','Mini App','Тот же сервис. В Telegram.' if ru else 'The same service. In Telegram.','Клиентский интерфейс открывается прямо из вашего Telegram-бота.' if ru else 'The customer experience opens directly from your Telegram bot.')]
 tabs=''.join(f'<a href="/assets/media/{k}-{l}.png" data-gallery="{k}" data-title="{E(title)}" data-description="{E(desc)}" class="gallery-tab{" selected" if i==0 else ""}" aria-current="{str(i==0).lower()}">{name}</a>' for i,(k,name,title,desc) in enumerate(gallery))
 features=[('profiles','Гибкость начинается с профиля','Начните с готового шаблона или импортируйте свой JSON. Настройте параметры, проверьте конфиг и отправьте его на тестовую ноду.','Start with a profile. Make it yours.','Choose a template or import your own JSON. Set the parameters, validate the configuration and try it on a test node.'),('sections/tariffs','Доступ и продажи связаны','Тарифы, лимиты трафика, устройства, оплаты и реферальная программа работают с общей карточкой клиента.','Access and sales, connected.','Plans, traffic limits, devices, payments and referrals share the same customer record.'),('cabinet-installation','Клиентский опыт — тоже ваш','Установите кабинет и Mini App, добавьте название, логотип и тарифы. Разместите клиентский сайт на сервере панели или отдельно.','A customer experience with your name on it.','Install the customer site and Mini App, add your name, logo and plans. Host them with the panel or on a separate server.')]
 featurehtml=''.join(f'<article class="feature-row"><h3>{x[1] if ru else x[3]}</h3><div><p>{x[2] if ru else x[4]}</p><a class="text-link" href="{docurl(l,x[0])}">{t["read"]}{icon("arrow")}</a></div></article>' for x in features)
 categorylinks=''.join(f'<a href="{base(l)}docs/category/{g[0]}.html"><span>{g[2] if ru else g[1]}</span>{icon("arrow")}</a>' for g in GROUPS)
 command="apt-get update\napt-get install -y git curl ca-certificates\ngit clone --depth 1 https://github.com/STEALTHNET-APP/STEALTHNET-SOFTWARE.git /root/stealthnet-installer\ncd /root/stealthnet-installer\nbash install.sh"
 body=f'''<main id="main"><section class="hero wrap"><div class="hero-title"><h1>{'Ваш VPN.<br/><em>Ваши правила.</em>' if ru else 'Your VPN.<br/><em>Your rules.</em>'}</h1></div><div class="hero-description"><p>{'Открытая панель для вашего VPN-проекта. Управляйте серверами, подписками и оплатами. Дайте клиентам свой сайт и приложение в Telegram.' if ru else 'An open-source control panel for your VPN project. Manage servers, subscriptions and payments. Give customers your own website and Telegram app.'}</p><div class="actions">{linkbutton(docurl(l,'installation'),t['install'],True)}{linkbutton(docurl(l,'README'),t['docs'],False,'book')}</div><p class="hero-meta"><a href="{GH}/blob/main/LICENSE">{t['source']}</a><span>Debian / Ubuntu</span></p></div></section>
<section class="product-gallery wrap" id="gallery" aria-label="{'Галерея интерфейсов' if ru else 'Interface gallery'}"><div class="gallery-toolbar"><div class="gallery-tabs">{tabs}</div><a class="gallery-expand" data-gallery-expand href="/assets/media/panel-nodes-{l}.png">{t['openimage']}{icon('external')}</a></div><a href="/assets/media/panel-nodes-{l}.png" class="gallery-stage" data-gallery-expand><img id="gallery-image" src="/assets/media/panel-nodes-{l}.png" alt="{E(gallery[0][2])}" width="1600" height="1000" fetchpriority="high"/></a><div class="gallery-caption"><h2 id="gallery-title">{gallery[0][2]}</h2><p id="gallery-description">{gallery[0][3]}</p><small>{t['demo']}</small></div></section>
<section class="feature-section wrap" id="features"><h2>{'От первого сервера<br/>до своего сервиса.' if ru else 'From your first server<br/>to your own service.'}</h2><div class="feature-list">{featurehtml}</div><div class="stack-line"><span>Rust + PostgreSQL</span><span>Xray</span><span>RU / EN</span><a href="{GH}">{'Исходный код' if ru else 'Explore the source'}{icon('external')}</a></div></section>
<section class="docs-showcase"><div class="wrap docs-showcase-inner"><div><h2>{'Ответы.<br/>По полочкам.' if ru else 'Find the answer.<br/>Build the next step.'}</h2><p>{'От установки до конкретной настройки. Полные инструкции на русском и английском: категории, поиск, команды и проверка результата.' if ru else 'From installation to a specific setting. Complete guides in English and Russian, with categories, search, commands and verification steps.'}</p>{linkbutton(docurl(l,'README'),t['browse'],True,'book')}</div><nav class="category-links" aria-label="{t['all']}">{categorylinks}</nav></div></section>
<section class="install-section wrap" id="install"><div><h2>{'Начните<br/>со своего сервера.' if ru else 'Start on<br/>your own server.'}</h2><p>{'Подключитесь по SSH к чистому серверу Debian или Ubuntu как root. Установщик скачает актуальный стабильный релиз и проведёт через настройку.' if ru else 'Connect over SSH to a clean Debian or Ubuntu server as root. The installer downloads the latest stable release and guides you through setup.'}</p><a class="text-link" href="{docurl(l,'installation')}">{'Требования и все шаги установки' if ru else 'Requirements and full installation guide'}{icon('arrow')}</a></div><div class="install-code"><div class="code-label"><span>{'Установка через GitHub' if ru else 'Install from GitHub'}</span><span>bash</span></div><pre><code class="language-bash">{E(command)}</code></pre></div></section>
<section class="community-section wrap"><div><h2>{'Делаем STEALTHNET вместе.' if ru else 'Build STEALTHNET with us.'}</h2><p>{'Обсуждения, новости и помощь в настройке — в сообществе. Код, предложения и новые релизы — на GitHub.' if ru else 'Join the community for discussions, news and setup help. Find the code, propose improvements and follow releases on GitHub.'}</p><div class="actions">{linkbutton(COMMUNITY,t['community'],True,'telegram')}{linkbutton(GH,'GitHub',False,'github')}</div></div><div class="donation"><h3>{t['support']}</h3><p>{'Добровольные пожертвования на разработку проекта.' if ru else 'Optional donations support project development.'}</p><span>TRON · TRC20</span><code>{WALLET}</code><button class="button" data-copy="{WALLET}">{t['wallet']}{icon('copy')}</button></div></section></main>'''
 write(base(l)+'index.html',document(l,'Ваш VPN. Ваши правила.' if ru else 'Your VPN. Your rules.','Открытая панель управления VPN, клиентский сайт, Telegram Mini App и полная документация.' if ru else 'Open-source VPN management, customer website, Telegram Mini App and complete documentation.',body,'index.html'))

def sidebar(l,current):
 t=LABELS[l];gcur=group_for(current)
 groups=''
 for g in GROUPS:
  glabel=g[2 if l=='ru' else 1];active=g==gcur or current=='category/'+g[0]
  items=''.join(f'<a href="{docurl(l,k)}" {"aria-current=page" if k==current else ""}>{E(ru if l=="ru" else en)}</a>' for k,en,ru in g[3])
  groups+=f'<details class="nav-group" {"open" if active or current=="README" and g[0]=="start" else ""}><summary>{E(glabel)}{icon("chevron")}</summary><div>{items}</div></details>'
 return f'<aside class="doc-sidebar"><div class="sidebar-heading">{t["docs"]}<a href="{GH}/releases/latest">v{E(VERSION)}</a></div><a class="sidebar-overview" href="{docurl(l,"README")}" {"aria-current=page" if current=="README" else ""}>{icon("book")}{t["overview"]}</a><nav aria-label="{t["navigatetitle"]}">{groups}</nav><a class="sidebar-community" href="{COMMUNITY}">{icon("telegram")}{t["community"]}{icon("external")}</a></aside>'
def docframe(l,current,title,desc,article,toc=''):
 t=LABELS[l];g=group_for(current);path='docs/'+('index' if current=='README' else current)+'.html'
 crumb=f'<a href="{docurl(l,"README")}">{t["docs"]}</a>'+(f'{icon("chevron")}<a href="{base(l)}docs/category/{g[0]}.html">{g[2 if l=="ru" else 1]}</a>' if g else '')
 mobile=f'<details class="mobile-navigation"><summary>{icon("menu")}{t["contents"]}{icon("chevron")}</summary>{sidebar(l,current)}</details>'
 mobile_toc=f'<details class="article-contents"><summary>{t["onpage"]}{icon("chevron")}</summary>{toc}</details>' if toc and 'href=' in toc else ''
 body=f'''<div class="docs-layout">{sidebar(l,current)}<main class="doc-main" id="main">{mobile}<nav class="breadcrumbs" aria-label="{'Путь к статье' if l=='ru' else 'Breadcrumb'}">{crumb}</nav><article class="prose"><h1>{E(title)}</h1>{mobile_toc}{article}</article></main><aside class="doc-toc"><strong>{t['onpage']}</strong>{toc}<a class="toc-top" href="#main">{t['up']}</a></aside></div>'''
 write(base(l)+path,document(l,title,desc,body,path,True))
def rewrite(l,key,raw):
 origin='docs/'+l+'/'+key+'.md'
 def replace(m):
  attr,url=m.group(1),html.unescape(m.group(2));split=urlsplit(url)
  if split.scheme or url.startswith(('#','/','//','mailto:')):return m.group(0)
  dest=posixpath.normpath(posixpath.join(posixpath.dirname(origin),split.path));frag='#'+split.fragment if split.fragment else ''
  match=re.fullmatch(r'docs/(en|ru)/(.+)\.md',dest)
  if match:target=docurl(match[1],match[2])+frag
  elif dest in ('README.md','README.ru.md'):target=base('ru' if '.ru.' in dest else 'en')+frag
  elif dest.startswith('docs/media/') and not dest.endswith('.md'):target='/assets/media/'+dest[len('docs/media/'):]+frag
  else:target=GH+'/blob/main/'+quote(dest,safe='/')+frag
  return f'{attr}="{E(target)}"'
 return re.sub(r'(href|src)="([^"]+)"',replace,raw)
SEARCH={'en':[],'ru':[]};URLS=[]
def article(l,key):
 t=LABELS[l];raw=(ROOT/'content'/l/(key+'.md')).read_text();raw=raw[raw.find('\n# ')+1:] if '\n# ' in raw else raw
 raw=re.sub(r'^# .+\n','',raw,count=1)
 md=markdown.Markdown(extensions=['fenced_code','tables','toc','sane_lists'],extension_configs={'toc':{'permalink':False,'toc_depth':'2-3'}})
 body=rewrite(l,key,md.convert(raw));plain=html.unescape(re.sub('<[^>]+>',' ',body));plain=re.sub(r'\s+',' ',plain).strip()
 title=title_for(l,key);g=group_for(key);idx=list(PATHORDER).index(key)
 previous=PATHORDER[idx-1] if idx else None;nextkey=PATHORDER[idx+1] if idx+1<len(PATHORDER) else None
 related='<nav class="article-pagination">'+''.join(f'<a href="{docurl(l,k)}"><small>{label}</small><strong>{E(title_for(l,k))}{icon("arrow")}</strong></a>' for k,label in ((previous,t['prev']),(nextkey,t['next'])) if k)+'</nav>'
 body+=f'<div class="article-meta"><a href="{GH}/blob/main/docs/{l}/{key}.md">{icon("external")}{t["edit"]}</a><span>{t["release"]} {E(VERSION)}</span></div>'+related
 docframe(l,key,title,plain[:175],body,md.toc)
 SEARCH[l].append(dict(title=title,url=docurl(l,key),category=g[2 if l=='ru' else 1],text=plain))
 URLS.append(DOMAIN+docurl(l,key))
PATHORDER=[x[0] for g in GROUPS for x in g[3]]
def indexes(l):
 t=LABELS[l];ru=l=='ru'
 intro='Выберите, что хотите настроить. Для нового проекта начните с установки панели, затем пройдите первый запуск.' if ru else 'Choose what you want to set up. For a new project, start with panel installation, then follow the first setup guide.'
 rows=''.join(f'<section class="category-entry"><h2><a href="{base(l)}docs/category/{g[0]}.html">{g[2 if ru else 1]}{icon("arrow")}</a></h2><ul>'+''.join(f'<li><a href="{docurl(l,k)}">{E(r if ru else e)}</a></li>' for k,e,r in g[3])+'</ul></section>' for g in GROUPS)
 content=f'<p class="doc-lead">{intro}</p><div class="start-links">{linkbutton(docurl(l,"installation"),t["install"],True)}{linkbutton(docurl(l,"sections/getting-started"),"Первый запуск" if ru else "First setup")}</div><div class="category-directory">{rows}</div>'
 docframe(l,'README',t['docs'],intro,content)
 for g in GROUPS:
  title=g[2 if ru else 1]
  entries=''.join(f'<a class="category-article" href="{docurl(l,k)}"><span>{E(r if ru else e)}</span>{icon("arrow")}</a>' for k,e,r in g[3])
  docframe(l,'category/'+g[0],title,title,f'<p class="doc-lead">{("Инструкции по теме «"+title+"». Выберите нужную задачу.") if ru else ("Guides for "+title.lower()+". Choose the task you want to complete.")}</p><div class="category-articles">{entries}</div>')
  URLS.append(DOMAIN+base(l)+'docs/category/'+g[0]+'.html')
# Remove only generated documentation before rebuilding, eliminating stale advice.
for l in ('en','ru'):
 directory=ROOT/base(l).lstrip('/')/'docs'
 if directory.exists():shutil.rmtree(directory)
 landing(l);indexes(l)
 for key in PATHORDER:article(l,key)
 (ROOT/'assets'/f'search.{l}.json').write_text(json.dumps(SEARCH[l],ensure_ascii=False,separators=(',',':')))
 URLS.extend([DOMAIN+base(l),DOMAIN+docurl(l,'README')])
# Preserve incoming links from the former documentation without carrying obsolete text.
legacy={'nodes':'node-installation','protocols':'profiles','subscriptions':'subscription-installation','billing':'payment-gateways','faq':'troubleshooting','changelog':'releases'}
for l in ('en','ru'):
 for old,new in legacy.items():
  if old in PATHS:continue
  target=docurl(l,new)
  write(base(l)+'docs/'+old+'.html',f'<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="{DOMAIN+target}"><title>STEALTHNET</title></head><body><a href="{target}">{LABELS[l]["docs"]}</a></body></html>')
for l in ('en','ru'):
 title='Страница не найдена' if l=='ru' else 'Page not found'
 body=f'<main id="main" class="not-found wrap"><h1>{title}</h1><p>{"Откройте главную или найдите нужную инструкцию в документации." if l=="ru" else "Open the home page or find the guide you need in the documentation."}</p><div class="actions">{linkbutton(base(l),LABELS[l]["home"],True)}{linkbutton(docurl(l,"README"),LABELS[l]["docs"])}</div></main>'
 write(base(l)+'404.html',document(l,title,title,body,'404.html'))
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{E(u)}</loc></url>' for u in URLS)+'</urlset>')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+DOMAIN+'/sitemap.xml\n')
print(f'Built 2 landing pages and {len(PATHORDER)*2} articles in {len(GROUPS)} bilingual categories')
