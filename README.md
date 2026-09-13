# STEALTHNET website

[**Open the website →**](https://stealthnet.software/) · [**Русская версия →**](https://stealthnet.software/ru/) · [Software repository](https://github.com/STEALTHNET-APP/STEALTHNET-SOFTWARE)

A bilingual product landing and categorized documentation for STEALTHNET. Static HTML is served by GitHub Pages from `main`, with the existing custom domain and HTTPS.

## Build

Python 3.11 or newer:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python build.py
python3 -m http.server 18770
```

Open `http://localhost:18770`. Generated HTML, the source Markdown snapshot and local assets are committed. GitHub Actions rebuilds the site and checks links, language counterparts, search destinations and generated-file drift on each push. Visitors do not need Python or JavaScript to read the guides.

## Update the documentation

Public guides originate in `docs/en` and `docs/ru` of the software repository. Correct the original guide first, then synchronize from the checkout containing the published release:

```bash
python3 sync_docs.py ../stealthnet-software
.venv/bin/python build.py
.venv/bin/python check.py
```

`content/source.json` records the software version and commit. `catalog.py` assigns every public guide to one category with localized navigation labels. Build fails for missing or uncategorized guides. English and Russian use matching paths; the language button retains the article.

## Structure

- `/` and `/ru/`: project presentation and real interface gallery.
- `/docs/` and `/ru/docs/`: categorized guides with sidebar, contents, copyable commands and full-text search.
- `assets/`: local styles, scripts, fonts and sanitized application screenshots.
- `content/`: a reproducible snapshot of public guides; no runtime settings, credentials or customer data.

## Sources and license

Screenshots are supplied by the project's demo gallery; see [media provenance](assets/media/README.md). The Onest font is bundled under [SIL OFL 1.1](assets/fonts/OFL.txt). Source and documentation are distributed under [AGPL-3.0-only](LICENSE), matching the software project.

---

Сайт и документация полностью доступны на русском и английском. Главная — презентация проекта; инструкции находятся в отдельном разделе с категориями, поиском и оглавлением. Источник инструкций — основной репозиторий: после правок синхронизируйте Markdown и пересоберите сайт командами выше. Изменения публикуются через `main` в GitHub Pages.

[Сообщество STEALTHNET](https://t.me/stealthnet_admin_panel)
