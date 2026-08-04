#!/usr/bin/env python3
"""English copy for the site. Page markup lives here, the template is in build.py.

Everything here describes what the panel actually does: commands come from the
real installers, limits from checks against the live engine. When the panel
changes, this has to change too — documentation that lies is worse than none,
because people make decisions from it.

The Russian copy is content_ru.py. The two files hold the same pages in the
same order; when you add a section to one, add it to the other.
"""

# Репозиторий с кодом ещё не открыт, поэтому ссылки в шапке и на кнопке
# ведут на организацию — иначе посетитель упирается в 404. Когда код
# выложат, достаточно поменять GH_LINK на GH_REPO здесь и в content_ru.py.
GH_ORG = 'https://github.com/STEALTHNET-APP'
GH_REPO = 'https://github.com/STEALTHNET-APP/stealthnet-software'
GH_LINK = GH_ORG


def ic(path):
    return f'<span class="ic"><svg viewBox="0 0 24 24">{path}</svg></span>'


ICONS = {
    'server': '<rect x="2" y="3" width="20" height="7" rx="2"/><rect x="2" y="14" width="20" height="7" rx="2"/>',
    'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/>',
    'card': '<path d="M20 7H4a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2Z"/><path d="M2 11h20"/>',
    'chat': '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2Z"/>',
    'chart': '<path d="M3 17 9 11l4 4 8-8"/><path d="M15 7h6v6"/>',
    'link': '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
    'code': '<path d="m4 17 6-6-6-6"/><path d="M12 19h8"/>',
    'lock': '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
}


def build(landing, doc_page, latest):
    # ─────────────────────────── витрина ───────────────────────────
    landing(f'''
<div class="wrap hero">
  <span class="pill">open source · runs on your own server</span>
  <h1>A panel for people<br>who sell VPN</h1>
  <p class="lead">Nodes, subscriptions, plans, payments and a Telegram bot in one place.
     Nothing leaves your machines: the panel, the database and the subscription service
     all run on your own hardware.</p>
  <div class="cta">
    <a class="btn primary" href="docs/index.html">
      <svg viewBox="0 0 24 24"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
      Quick start</a>
    <a class="btn" href="{GH_LINK}">Source code</a>
  </div>
  <p class="note">Rust and PostgreSQL. One command to install, one to attach a node.</p>
</div>

<section class="wrap" id="features">
  <h2>What you get</h2>
  <p class="sub">Not a checklist — the things you actually end up using every day.</p>
  <div class="grid">
    <div class="card"><h3>{ic(ICONS['server'])}Nodes</h3>
      <p>The agent keeps in touch with the panel, applies the profile and reports traffic,
         who is online and how loaded the box is. Attaching a node is one command;
         geo databases keep themselves up to date.</p></div>
    <div class="card"><h3>{ic(ICONS['shield'])}Protocols</h3>
      <p>VLESS, VMess, Trojan, Shadowsocks 2022, Hysteria2. Transports: Reality, WebSocket,
         gRPC, XHTTP, HTTPUpgrade, mKCP. Eleven ready-made configuration presets.</p></div>
    <div class="card"><h3>{ic(ICONS['link'])}Subscriptions</h3>
      <p>Xray JSON, Clash, sing-box, base64 — the format follows the client's app.
         The subscription service moves to its own domain, so blocking the panel
         does not cut people off.</p></div>
    <div class="card"><h3>{ic(ICONS['card'])}Payments</h3>
      <p>Plans with periods, promo codes, an affiliate programme, auto-renewal.
         Payment providers are wired up with keys inside the panel, with no file editing.</p></div>
    <div class="card"><h3>{ic(ICONS['chat'])}Telegram bot</h3>
      <p>Selling and renewal happen in the bot; its texts and buttons are edited in the
         panel. Broadcasts by segment, with scheduled sending.</p></div>
    <div class="card"><h3>{ic(ICONS['chart'])}Accounting</h3>
      <p>Traffic per client and per node, limits and scheduled resets, devices by HWID,
         what the servers cost you and what is left after them.</p></div>
  </div>
</section>

<section class="wrap">
  <h2>Installing</h2>
  <p class="sub">You need a Debian or Ubuntu server, a domain for the panel and a domain
     for subscriptions.</p>
  <pre><code>git clone https://github.com/STEALTHNET-APP/stealthnet-software.git
cd stealthnet-software
cp .env.example .env    # addresses, bot token, database access
docker compose up -d</code></pre>
  <p style="color:var(--text-2)">Then head to the <a href="docs/index.html">quick start</a>:
     first administrator, configuration profile, first node and first client.</p>
</section>

<section class="wrap">
  <h2>Honest about the limits</h2>
  <p class="sub">So you don't find out after installing.</p>
  <div class="grid">
    <div class="card"><h3>{ic(ICONS['lock'])}One currency</h3>
      <p>Prices and reports use a single currency for the whole service. Several at once
         would mean exchange rates, conversion and figures that disagree. The one exception
         is Telegram Stars: they have their own unit and their own price.</p></div>
    <div class="card"><h3>{ic(ICONS['code'])}No node plugins</h3>
      <p>There is no extension catalogue. Blocking and bypassing are done with routing
         rules inside the configuration profile — enough for nearly every case.</p></div>
    <div class="card"><h3>{ic(ICONS['server'])}Changing who has access</h3>
      <p>The engine reads its client list at start-up, so a purchase or a revoked
         subscription means restarting it on the node. The window is up to 15 seconds.</p></div>
  </div>
</section>

<section class="wrap">
  <h2>What's new</h2>
  <p class="sub">Every change to the panel has its own page, newest first.</p>
  <div class="release">
    <span class="pill">{latest['title']}</span>
    <p>{latest['note']}</p>
    <ul>{''.join(f'<li>{x}</li>' for x in latest['items'])}</ul>
    <a class="btn" href="docs/changelog.html#{latest['anchor']}">The full list of changes</a>
  </div>
</section>
''')

    # ─────────────────────── быстрый старт ───────────────────────
    doc_page('index.html', 'Quick start',
             'Installing the STEALTHNET SOFTWARE panel, the first node and the first client.', '''
<p class="lead-p">In one pass: bring up the panel, create a configuration profile, attach a
node, hand a client their subscription and confirm it works.</p>

<h2 id="requirements">What you need</h2>
<ul>
  <li>A server with Debian 12 or Ubuntu 22.04+, and root access.</li>
  <li>A domain for the panel and a separate domain for subscriptions — both A records
      pointing at the server.</li>
  <li>A Telegram bot token, if you sell through a bot.</li>
</ul>
<div class="note"><b>Why subscriptions get their own domain.</b> If the panel's domain is
blocked, clients keep refreshing their configs: the subscription service runs independently
and can live on another server with nothing but an API key.</div>

<h2 id="install">Installing</h2>
<pre><code>git clone https://github.com/STEALTHNET-APP/stealthnet-software.git
cd stealthnet-software
cp .env.example .env</code></pre>
<p>Fill in the panel and subscription addresses, database access and the bot token in
<code>.env</code>. Then:</p>
<pre><code>docker compose up -d
docker compose logs -f api</code></pre>
<p>The log will print the login and a one-time password for the first administrator.
Change it as soon as you are in.</p>

<h2 id="profile">Configuration profile</h2>
<p>A profile is the Xray config handed out to nodes. One profile serves many nodes:
the agent writes the clients into it locally.</p>
<ol>
  <li>Open <b>Infrastructure → Configuration profiles → New profile</b>.</li>
  <li>Pick a preset. Start with <b>VLESS + Reality (TCP)</b>: it needs neither a domain
      of your own nor a certificate.</li>
  <li>Open the editor and replace the fields written in capitals — the keys come from the
      “Reality keys” button on the same page.</li>
  <li>Save. The panel validates the config with the real engine and will not save one
      that does not run.</li>
</ol>
<div class="note warn"><b>Placeholders such as <code>YOUR_PRIVATE_KEY</code> fail validation
on purpose.</b> That way a forgotten field surfaces immediately, instead of arriving from
your clients a week later.</div>

<h2 id="node">The first node</h2>
<p>On the <b>Nodes</b> page press “Attach node”. The panel produces a ready command — run it
on the node's server. Details and special cases: <a href="nodes.html">Nodes</a>.</p>
<p>Within 15 seconds the node appears in the list, green. If it is red, the panel states
the reason right in the row.</p>

<h2 id="squad">Squad and plan</h2>
<p>A squad is the set of inbounds a client is given. The chain runs:</p>
<pre><code>plan → squads → inbounds → nodes</code></pre>
<ol>
  <li><b>Internal squads → Create squad</b>, tick the profile's inbounds.</li>
  <li><b>Plans → New plan</b>: code, name, duration and price, traffic and device limits,
      and the squads the client receives.</li>
</ol>

<h2 id="host">Hosts</h2>
<p>A host is the line a client sees as a location in their app. It points at a profile
inbound and adds what only the administrator knows: the public address, the port and the
name of the location.</p>
<p><b>Hosts → Add host</b>: a remark (say “🇩🇪 Frankfurt”), the node's address and port, and
the inbound. The order of hosts in the list is the order of locations for the client.</p>

<h2 id="client">The first client</h2>
<p><b>Clients → Create client</b>. Give a name and a plan. The card's “Subscription and VPN”
tab holds the link — that is what you hand over.</p>
<p>You can check it without leaving the panel: open the link in a browser and you get a page
with apps for each platform and an “Add subscription” button.</p>

<div class="note"><b>Nothing comes back?</b> A subscription hands out no configs if the client
has no active time left, or if not a single inbound from their squads is up on a live node.
Both causes are covered in <a href="troubleshooting.html">when something breaks</a>.</div>
''', nxt=('nodes.html', 'Nodes'))

    # ─────────────────────────── ноды ───────────────────────────
    doc_page('nodes.html', 'Nodes',
             'Attaching a node, certificates, geo databases and what its states mean.', '''
<p class="lead-p">A node is a server running the Xray engine and our agent. The agent pulls
the profile from the panel, writes the clients into it and reports traffic and load.</p>

<h2 id="install">Attaching</h2>
<p>On the <b>Nodes</b> page press “Attach node” — the panel assembles a command with the
address and the key. It installs the engine, the agent and a systemd unit:</p>
<pre><code>PANEL_URL=https://panel.your-domain NODE_SECRET=... bash install-node.sh</code></pre>
<p>The secret is shown once: only its hash is stored. If you lose it, issue a new one from
the node's menu.</p>
<p>The script takes the agent from a GitHub release, falling back to the panel itself when
that is unreachable. Point it elsewhere with <code>AGENT_URL</code>, or pin a release with
<code>AGENT_RELEASE</code>.</p>

<h2 id="tls">Certificate</h2>
<p>Reality needs no certificate — it hides behind somebody else's site. Trojan, Hysteria2
and anything running over TLS will not start without one at all.</p>
<p>A bare node has no certificate to begin with, so the installer issues one itself when you
give it a domain:</p>
<pre><code>NODE_DOMAIN=de1.your-domain PANEL_URL=... NODE_SECRET=... bash install-node.sh</code></pre>
<p>The domain must have an A record pointing at this machine, and port 80 must be free:
that is where the Let's Encrypt check goes. The certificate lands in
<code>/etc/sn-node/tls/</code>, renewal is checked daily, and the engine restarts when it
changes — otherwise three months later it would still be serving an expired one.</p>
<div class="note warn"><b>Point the profile at <u>this node's</u> certificate</b>, not the panel's domain. The Hysteria2 preset ships with a placeholder; leave the panel's domain in it and the engine on the node answers <code>no such file or directory</code> and refuses to start — taking the profile's other inbounds with it.<br><br>The paths go in <code>streamSettings.tlsSettings.certificates</code>:<br><code>/etc/sn-node/tls/your-node-domain.crt</code> and <code>.key</code>.</div>
<div class="note"><b>One profile across nodes.</b> If your nodes have different domains, a TLS inbound cannot live in a shared profile: the path in the config is a single value. Give those nodes a profile of their own.</div>

<h2 id="geo">Geo databases</h2>
<p>Rules like <code>geoip:ru</code> and <code>geosite:category-ads-all</code> rely on the
<code>geoip.dat</code> and <code>geosite.dat</code> files. The engine's archive installs them
once and they go stale from there, so the installer sets up a weekly update.</p>
<p><code>zapret.dat</code> — the list of resources blocked in Russia — is installed alongside.
You only need it if your rules mention <code>zapret:*</code>; without the file, the engine
refuses to start with such a rule.</p>
<p>An update replaces a file only when it has genuinely changed: the engine reads the
databases at start-up, and a needless restart is a needless drop of every connection.</p>

<h2 id="states">Node states</h2>
<table>
  <tr><th>Look</th><th>What it means</th></tr>
  <tr><td>Green</td><td>The agent is in touch, the engine runs, clients are served.</td></tr>
  <tr><td>Red</td><td>Either the agent is out of touch, or <b>the engine failed to start</b> —
      the reason is written in the row. The latter happens with a bad config or a missing
      certificate.</td></tr>
  <tr><td>Grey</td><td>Switched off by an administrator. Not a fault: it is deliberately not
      serving clients.</td></tr>
</table>
<div class="note"><b>The agent being alive is not the same as the engine running.</b> These are
different states and the panel tells them apart: a node that answers polls while Xray is down
shows as broken, not as fine.</div>

<h2 id="safety">Protection from a broken config</h2>
<p>Before replacing a working config, the agent asks the engine whether it would accept the
new one. If not, it stays on the old config and reports the reason to the panel. One typo in
a new protocol does not take the whole node down along with the locations that worked.</p>

<h2 id="traffic">Traffic and who is online</h2>
<p>The engine counts per client and per inbound; the agent collects the counters every
15 seconds and sends the delta. “Online” means “passed traffic within the last polling
window”: Xray does not expose a list of live connections, and this is an honest
approximation.</p>
''', prev=('index.html', 'Quick start'), nxt=('protocols.html', 'Protocols'))

    # ───────────────────── протоколы ─────────────────────
    doc_page('protocols.html', 'Protocols and profiles',
             'Which protocols and transports work, and the ready-made configuration presets.', '''
<p class="lead-p">A profile is the Xray config handed out to nodes. The panel ships eleven
presets: pick one, it is created, then you adjust it to fit.</p>

<h2 id="works">What works</h2>
<p>Verified with live traffic rather than from documentation: each variant was brought up on
a server and an external page was fetched through it.</p>
<table>
  <tr><th>Protocols</th><td>VLESS, VMess, Trojan, Shadowsocks 2022, Hysteria2</td></tr>
  <tr><th>Transports</th><td>TCP (raw), WebSocket, gRPC, XHTTP, HTTPUpgrade, mKCP</td></tr>
  <tr><th>Encryption</th><td>Reality, TLS, none (behind a reverse proxy)</td></tr>
</table>

<h2 id="limits">What the engine cannot do</h2>
<p>These are Xray's limits, not the panel's:</p>
<ul>
  <li><b>h2 and QUIC</b> were removed in Xray 26 — the engine itself suggests XHTTP instead.</li>
  <li><b>mKCP</b> is there, but the <code>header</code> and <code>seed</code> fields were
      dropped; the old syntax is rejected.</li>
  <li><b>TUIC</b> is absent.</li>
  <li><b>WireGuard</b> is accepted by the engine, but it is not a subscription protocol:
      it uses a key pair per peer rather than handing configs to clients.</li>
</ul>
<p>The panel rejects such configs with the engine's own reason, not a generic “error”.</p>

<h2 id="presets">Presets</h2>
<table>
  <tr><th>Preset</th><th>When to reach for it</th></tr>
  <tr><td>VLESS + Reality (TCP)</td><td>The default choice. Needs neither a domain nor a certificate.</td></tr>
  <tr><td>VLESS + Reality (gRPC)</td><td>Sometimes gets through where plain TCP is throttled.</td></tr>
  <tr><td>VLESS + WebSocket</td><td>Behind a reverse proxy or a CDN.</td></tr>
  <tr><td>VLESS + XHTTP</td><td>Survives where WebSockets get cut.</td></tr>
  <tr><td>VLESS + HTTPUpgrade</td><td>Lighter than WebSocket, passes most proxies.</td></tr>
  <tr><td>VLESS + mKCP</td><td>Over UDP, holds up better on a poor link.</td></tr>
  <tr><td>VMess + WebSocket</td><td>When your clients' apps have no VLESS support.</td></tr>
  <tr><td>Trojan + TLS</td><td>Looks like an ordinary HTTPS site. Needs a domain and a certificate.</td></tr>
  <tr><td>Shadowsocks 2022</td><td>No TLS at all, a separate key per client.</td></tr>
  <tr><td>Hysteria2</td><td>Its own congestion control, copes well with packet loss.</td></tr>
  <tr><td>Reality + WebSocket</td><td>Two entry points in one profile: a primary and a fallback.</td></tr>
</table>

<h2 id="hysteria">Hysteria2: two catches</h2>
<div class="note warn">
  <p><b>In Xray the protocol is called <code>hysteria</code>, not <code>hysteria2</code>.</b>
  With the second spelling the engine answers <code>unknown config id</code>. The version is
  given separately: <code>"version": 2</code>.</p>
  <p style="margin:8px 0 0"><b>The implementation runs over an ordinary transport, not over
  QUIC.</b> So Xray-based clients connect to it, while a standalone QUIC hysteria server
  does not.</p>
</div>
<p>A certificate is required — see <a href="nodes.html#tls">the node certificate</a>.</p>

<h2 id="shadowsocks">Shadowsocks: 2022 only</h2>
<p>The classic methods use one password for everybody, so handing different clients different
keys is impossible. Only the <code>2022-*</code> methods will do.</p>
<p>The inbound settings must include <code>password</code> — that is the server key. A client
connects with the pair “server key : personal key”, and without the server half the engine
answers <code>missing psk</code>. The panel derives the personal key from the client's UUID,
so revoking a subscription cuts access here too.</p>

<h2 id="routing">Routing</h2>
<p>Blocking and bypassing are done with rules in <code>routing.rules</code>. The editor has
ready-made blocks: block torrents and ads, Russian sites direct, sites blocked in Russia
through the tunnel, chaining to a second node, your own DNS.</p>
<div class="note"><b>List private networks explicitly</b> rather than using
<code>geoip:private</code>: if the file turns out to be missing on the node, a rule
referencing it brings the whole config down.</div>

<h2 id="service">The service inbound</h2>
<p><code>api-in</code> listens on the loopback only and exists for statistics — the agent reads
the counters through it. Without it traffic limits do not work. It is not offered in location
pickers: there is nothing to connect to.</p>
''', prev=('nodes.html', 'Nodes'), nxt=('subscriptions.html', 'Subscriptions'))

    # ───────────────────── подписки ─────────────────────
    doc_page('subscriptions.html', 'Subscriptions',
             'Delivery formats, a separate subscription server, devices and limits.', '''
<p class="lead-p">The subscription is the only thing a client ever sees. From one link their
app gets the list of locations in whichever format it understands.</p>

<h2 id="formats">Formats</h2>
<p>The format is chosen by the app's User-Agent. Rules are checked top to bottom and the first
match wins; if none matches, a built-in list of known apps decides.</p>
<table>
  <tr><th>Format</th><th>For</th></tr>
  <tr><td>Xray JSON</td><td>Happ, Streisand, v2Box, NekoBox</td></tr>
  <tr><td>Clash / Mihomo</td><td>Clash Meta, FlClash, Stash</td></tr>
  <tr><td>sing-box</td><td>sing-box, Hiddify</td></tr>
  <tr><td>base64 list</td><td>v2rayNG, Shadowrocket and anything unknown</td></tr>
  <tr><td>Web page</td><td>A browser: apps for the platform and an install button</td></tr>
</table>
<p>You can check what a particular app will get from inside the panel: the
<b>Response rules</b> section, the “Paste a User-Agent” field.</p>

<h2 id="separate">A server of its own</h2>
<p>The subscription service moves to another server and another domain: then blocking the
panel does not cut clients off from their configs, and the subscription machine has no
database access at all.</p>
<pre><code>SUB_MODE=api
PANEL_URL=https://panel.your-domain
SUB_SERVICE_TOKEN=&lt;key from the panel&gt;</code></pre>
<p>The key is issued in <b>Settings → Subscription service</b> and shown once. The same page
hands you the install commands and a Caddy block.</p>
<div class="note"><b>Next to the panel</b> the subscription service reads the database
directly: that is faster than a round trip through the API, and it needs no service key
at all.</div>

<h2 id="devices">Devices and the limit</h2>
<p>Apps identify themselves with headers (<code>x-hwid</code>, <code>x-device-os</code>,
<code>x-device-model</code>, <code>x-app-version</code>). From those the panel keeps the
client's device list and enforces the plan's limit.</p>
<p>The limit is only checked for a new device: one already registered keeps working even if
you later lower the limit — otherwise somebody would suddenly lose access on the phone they
used yesterday.</p>
<p>Over the limit, the client gets a clear line in the location list rather than emptiness:
how many devices are taken and what to do about it.</p>
<div class="note">A browser and <code>curl</code> do not count as devices: they send none of
those headers.</div>

<h2 id="inactive">When a subscription hands out nothing</h2>
<ul>
  <li>Time has run out, or traffic has.</li>
  <li>The client was switched off by an administrator.</li>
  <li>Not one inbound from their squads is up on a live node.</li>
  <li>The device limit is used up.</li>
</ul>
<p>In every case the reason arrives in place of the locations — the wording is set in
<b>Subscription settings</b> and supports <code>{date}</code>, <code>{days}</code> and
<code>{tariff}</code>.</p>

<h2 id="history">Who has been asking</h2>
<p>The <b>Subscription requests</b> section shows who fetched the link, with what and when.
Three requests from one address is normal — that is the refresh interval. Dozens of different
addresses within an hour means the link has leaked: revoke the subscription from the client's
card, which changes the short identifier and kills the old link.</p>
''', prev=('protocols.html', 'Protocols'), nxt=('billing.html', 'Plans and payments'))

    # ───────────────────── тарифы ─────────────────────
    doc_page('billing.html', 'Plans and payments',
             'Plans, periods, promo codes, payment providers and currency.', '''
<p class="lead-p">A plan ties together price, limits and access: what it costs, how much
traffic and how many devices, and which locations the client gets.</p>

<h2 id="currency">One currency</h2>
<div class="note warn"><b>The whole service runs on a single currency.</b> Several at once
would mean exchange rates, conversion and figures that disagree. You change it under
<b>Payments and currencies</b>, but prices already entered are not converted — you have to
go through them by hand.</div>
<p>The exception is Telegram Stars: they live in their own unit and cannot take ordinary
money, so the price in stars is a separate field.</p>

<h2 id="tariffs">Plans</h2>
<ul>
  <li><b>Code</b> — internal; past purchases are found by it. Best left alone on a plan
      that is in use.</li>
  <li><b>Periods and prices</b> — how many days and for how much. There can be several.</li>
  <li><b>Limits</b> — traffic, devices, and how the counter resets.</li>
  <li><b>Squads</b> — the set of locations the client receives.</li>
  <li><b>Visibility</b> — a hidden plan is reachable only by direct link or promo code.</li>
</ul>
<p>The order of plans in the list is the order in the bot and on the site; rows are dragged.</p>

<h2 id="providers">Payment providers</h2>
<p>Keys are entered in the panel, not in files on the server. They are kept in the database
and never handed back to the browser: only a “set” marker is shown. An empty field on save
means “keep the existing key”.</p>
<div class="note"><b>A price is useless if no enabled provider takes its currency:</b> the
client sees the amount but no pay button. The panel warns about this on the plan page.</div>
<p>For a provider with an ordinary REST API there is a generic “Custom provider” module: it
posts an amount, gets a payment link back and waits for a webhook with the status. No code
to write.</p>

<h2 id="refund">Refunds</h2>
<p>Money goes back through the provider's own dashboard — the panel does not do it for you:
refunds work differently everywhere, and a quiet “refund automatically” that failed would
mark a payment refunded while the money was still there.</p>
<p>The panel records that a refund happened and, if you want, revokes the subscription.
A partial refund leaves the payment successful and notes the amount returned; a full one
moves it to “refunded”, so the month's revenue does not count that money.</p>

<h2 id="promos">Promo codes and affiliates</h2>
<p>Promo codes give a percentage off, a fixed amount or bonus days; they can be limited by
number of uses, by date and to first purchase only.</p>
<p>An affiliate earns a percentage of every successful payment by a client they brought,
for life. A new rate applies to future payments — commission already earned is not
recalculated.</p>

<h2 id="infra">What the servers cost</h2>
<p>Each node carries its hosting provider, rental cost and billing day. The
<b>Infrastructure billing</b> section adds it up: what the fleet costs and what is left
after it.</p>
''', prev=('subscriptions.html', 'Subscriptions'), nxt=('troubleshooting.html', 'When something breaks'))

    # ───────────────────── разбор поломок ─────────────────────
    doc_page('troubleshooting.html', 'When something breaks',
             'Common failures: a red node, a client that will not connect, an empty subscription.', '''
<p class="lead-p">Always in this order: first check whether the engine runs on the node, then
whether the config reaches the client, and only then blame the app.</p>

<h2 id="node-red">A node is red</h2>
<p>Hover the marker — the tooltip carries the reason. Two different cases:</p>
<h3>The agent is out of touch</h3>
<pre><code>systemctl status sn-node
journalctl -u sn-node -n 50 --no-pager</code></pre>
<p>Usually a wrong panel address or a stale node secret. Issue a new secret from the node's
menu, then run the install command again.</p>
<h3>The engine did not start</h3>
<p>The reason is written in the node's row. To check by hand:</p>
<pre><code>xray -test -config /etc/sn-node/config.json</code></pre>
<p>Typical causes: unfilled fields from a preset, a missing certificate file, a port already
taken, a rule referencing a geo database that is not there.</p>
<div class="note"><b>This does not take the node down.</b> The agent will not replace a working
config with one the engine rejected — the locations that worked keep serving.</div>

<h2 id="empty-sub">The subscription comes back empty</h2>
<p>Walk the chain:</p>
<ol>
  <li>The client has time left and traffic left.</li>
  <li>The client belongs to a squad.</li>
  <li>The squad has inbounds ticked.</li>
  <li>Those inbounds are bound to a node, and the node is online.</li>
  <li>The inbounds have hosts, and the hosts are enabled.</li>
</ol>
<p>One break anywhere and the client has no locations.</p>

<h2 id="new-client">A new client cannot connect</h2>
<p>The client list reaches the node separately from the config, within 15 seconds. Look in
the agent's log:</p>
<pre><code>journalctl -u sn-node --since '2 min ago' | grep applying</code></pre>
<p>A line like <code>applying ... reason="client list changed"</code> means the change
arrived.</p>

<h2 id="cert">Trojan or Hysteria2 stopped working</h2>
<p>Almost always an expired certificate. Check:</p>
<pre><code>ls -l /etc/sn-node/tls/
openssl x509 -in /etc/sn-node/tls/your-domain.crt -noout -enddate</code></pre>
<p>Renewal and the engine restart are handled by the daily <code>sn-cert-sync</code> service.
If it is missing, reinstall the node with the <code>NODE_DOMAIN</code> variable.</p>

<h2 id="no-traffic">Traffic is not counted</h2>
<p>Check that the profile contains the <code>api-in</code> service inbound and the
<code>api</code>, <code>stats</code> and <code>policy</code> sections. Without them the engine
hands out no counters, which also means plan limits do not work. Every preset already has
them.</p>

<h2 id="logs">Where to look</h2>
<table>
  <tr><th>Service</th><th>Command</th></tr>
  <tr><td>Panel</td><td><code>journalctl -u sn-api -n 100</code></td></tr>
  <tr><td>Subscriptions</td><td><code>journalctl -u sn-sub -n 100</code></td></tr>
  <tr><td>Node agent</td><td><code>journalctl -u sn-node -n 100</code></td></tr>
  <tr><td>Bot</td><td><code>journalctl -u sn-bot -n 100</code></td></tr>
</table>
<p>The overall health of the services is in the panel, under <b>Help</b>: it checks the API,
the database and the subscription service.</p>
''', prev=('billing.html', 'Plans and payments'), nxt=('faq.html', 'Questions'))

    # ───────────────────────── вопросы ─────────────────────────
    doc_page('faq.html', 'Questions',
             'Frequently asked questions about the STEALTHNET SOFTWARE panel.', f'''
<h2 id="remnawave">How it differs from other panels</h2>
<p>Written from scratch in Rust, installs with one command, and lives in a single repository —
panel, subscription service, bot, worker and node agent. What is split is the artefacts, not
the sources: each service is its own binary and its own image, and the subscription service
deploys to a separate server.</p>

<h2 id="data">What leaves your machines</h2>
<p>Nothing. The panel, the database and the subscription service run on your own hardware.
Hosting-provider icons are drawn locally rather than fetched from third-party services —
otherwise such a request would tell them which servers you use.</p>

<h2 id="domains">Collecting visited sites</h2>
<p>Off by default, and turned on deliberately. It is a log of the sites your clients visit —
the most valuable thing that can leak out of a VPN panel. Before enabling it, make sure it is
allowed by your policy and by the law where you operate.</p>

<h2 id="restart">Why a purchase restarts the engine</h2>
<p>Xray reads its client list at start-up: its API in the current version cannot add clients
on the fly, only manage inbounds. So changing who has access means a restart. The polling
window is 15 seconds, and connections open at that moment are dropped.</p>

<h2 id="languages">Languages</h2>
<p>Russian and English, with a switch in the header. The translation is applied after
rendering, so adding a string does not require editing every screen.</p>

<h2 id="backup">Backups</h2>
<p>A PostgreSQL dump is enough: it holds the clients, the plans and the configuration
profiles. Files on the nodes are restored by running the installer again.</p>

<h2 id="contribute">Where to get the code</h2>
<p>The source repository is not open yet: it opens together with the first release, in the
<a href="{GH_LINK}">STEALTHNET-APP</a> organisation. The install commands on these pages are
written against it, so they will work as-is once it is published.</p>
<p>For now only the <a href="{GH_ORG}/stealthnet-software-site">site repository</a> is open —
a typo or an inaccuracy in the documentation can be fixed right there.</p>
''', prev=('troubleshooting.html', 'When something breaks'))
