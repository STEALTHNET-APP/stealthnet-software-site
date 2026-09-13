#!/usr/bin/env python3
"""Snapshot public bilingual guides from a software checkout, never runtime files."""
import argparse, json, shutil, subprocess, tomllib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('source',type=Path);a=p.parse_args();source=a.source.resolve();root=Path(__file__).resolve().parent
for lang in ('en','ru'):
    dest=root/'content'/lang
    if dest.exists(): shutil.rmtree(dest)
    shutil.copytree(source/'docs'/lang,dest,ignore=shutil.ignore_patterns('*~'))
media=root/'assets'/'media';media.mkdir(parents=True,exist_ok=True)
for name in ('panel-nodes','storefront','cabinet','miniapp'):
    for lang in ('en','ru'):shutil.copy2(source/'docs'/'media'/f'{name}-{lang}.png',media)
for image in media.glob('*.png'):
    (media/(image.name+'.json')).write_text(json.dumps({'prompt':'Pre-existing application screenshot supplied by STEALTHNET-SOFTWARE docs/media/'+image.name+'. Sanitized demo data, actual application UI; Mini App uses the actual /app interface with a local test Telegram bridge. No production statistics or customer credentials. Source: https://github.com/STEALTHNET-APP/STEALTHNET-SOFTWARE/tree/main/docs/media'},indent=2)+'\n')
version=tomllib.loads((source/'Cargo.toml').read_text())['workspace']['package']['version']
sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()
(root/'content'/'source.json').write_text(json.dumps({'repository':'STEALTHNET-APP/STEALTHNET-SOFTWARE','version':version,'commit':sha},indent=2)+'\n')
print('Synced',sum(1 for x in (root/'content').rglob('*.md')),'public guides')
