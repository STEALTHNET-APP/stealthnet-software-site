# What's new

<!--
  How to keep this file (comments are stripped, they never reach the page).

  One source: docs/changelog.html is built from here, so write only here.
  The Russian copy is CHANGELOG.ru.md — add the same entry to both.

  Write from the point of view of somebody using the panel: not "fixed the
  query in client.service" but "traffic did not add up in the client list".
  If a change is invisible from the outside, it does not belong here.

  A new release is a `## 0.2.0 — 14 September 2026` heading, with `###`
  sections by topic inside it.
-->

Changes in the STEALTHNET SOFTWARE panel. Newest first.

## In progress — 0.1.0

The first public release has not happened yet: the code opens together with it.
Below is what already works and has been checked on a live installation.

### Nodes and the engine
- The Xray version is set in the panel once and rolls out to the whole fleet:
  the agent compares its own on every poll, downloads the release, checks the
  binary runs and reports the right version, and only then replaces the working
  one. Nodes left behind are shown on the nodes page.
- A "Restart Xray" action in the node menu. The engine used to restart only on
  its own — on a config or client-list change — so picking up a renewed
  certificate meant going to the server by hand.
- Changing the profile redraws the node card: inbounds belong to a profile, and
  the old list was wrong afterwards. On the server the bindings also stayed with
  the previous profile, leaving the node with no inbounds at all.
- The agent no longer logs about nftables every fifteen seconds: with every
  plugin off it does not touch nftables at all, and a repeating failure is
  reported once. The installer now installs nftables up front.
- The agent is downloaded from a GitHub release; the panel stays as a fallback
  for air-gapped setups and self-built binaries. The installer checks that what
  it downloaded really is a binary: the panel serves its own page for any
  unknown address, and that page was being installed instead of the agent —
  systemd answered "Exec format error".
- The node's country is picked from a searchable list, by name or by code.
  It used to be typed by hand, where "GE" meant Georgia, not Germany.
- A deleted node frees its name. Deletion is soft, but the uniqueness rule did
  not tell live rows from deleted ones, so the name stayed taken forever.
- The "already taken" error names the field instead of saying "a record with
  this value already exists".
- The window shown after creating a node was rewritten for somebody with a bare
  server: the Docker-free path comes first, as numbered steps — log in over SSH,
  one command, wait. The command is shown in full instead of being cut off.
- The "Copy" buttons in the node and subscription-service install windows put the
  name of the tab into the clipboard instead of the command itself.
- Attaching a node is one command; the agent keeps in touch with the panel by
  itself, applies the profile and reports traffic, who is online and the load.
- Configurations are validated by the engine **before** they are applied.
  A bad profile can no longer take down a node that was working: it stays on
  the configuration it had.
- A node turns red when the engine fails to start, and states the reason on
  its card — no need to go digging through logs on the server.
- Geo databases update themselves weekly, and the engine restarts only when
  the files have actually changed.

### Protocols and profiles
- **Hysteria 2 stopped connecting in up-to-date clients.** In Xray 26.7 it became
  a transport of its own, while the subscription still sent `network: tcp` —
  apps answered "not hysteria transport" and refused to start at all. The
  transport is now right on both sides, and the panel rejects a profile with
  the wrong one.
- **Reality keys come from the profile only.** They used to be copied onto the
  host row, so reissuing them in the profile left the two out of step: the
  server expected one short id, the client sent another, and the location
  looked broken while the node was perfectly fine. The public key is derived
  from the private one — there is nothing to copy anywhere.
- Installing a node is one path again: certificate issuance was taken out of the
  installer. Reality does not need one, and anything over TLS needs a certificate
  for its own node's domain — a manual step, covered in the nodes section.
- Every profile preset now has a "?" button with step-by-step instructions on what
  it takes to make it work. The editor has the same button, where the hint is
  matched against what the config actually contains.

- Protocols: VLESS, VMess, Trojan, Shadowsocks 2022, Hysteria2.
- Transports: TCP, WebSocket, gRPC, XHTTP, HTTPUpgrade, mKCP.
- Encryption: Reality, TLS, or none behind a reverse proxy.
- Eleven ready-made configuration presets: pick one, it is created, then you
  adjust it. Each was verified with live traffic, not only from documentation.
- Nine ready-made routing blocks to drop into a profile.

### Clients and subscriptions
- Next to the traffic counter you can now see when it wipes and on what schedule.
  A scheduled reset used to look like a fault: two gigabytes yesterday, zero
  today, and nothing explaining why.
- The "reset strategy" field in the client card finally works: it was there, but
  its value went nowhere. Changing the schedule also recalculates the next reset
  date — otherwise the counter would still wipe on the old one.
- Small amounts of traffic were displayed as "0 MiB" and looked like a counter that
  had been wiped: anything under a gigabyte was rounded to megabytes. Small values
  now show in kibibytes and bytes, and a real zero says so.
- The subscription returns the reason in the format the app asked for. With the
  device limit reached it used to send a "# reason" line regardless, so an app
  expecting Xray JSON showed a parse error instead of an explanation. The
  device-limit wording is now editable like the others.

- Devices are counted by HWID, and the number of them is capped by the plan.
- Bulk actions on clients: enable, disable, reset traffic, revoke the
  subscription, delete — for the selected rows or for the whole filter.
- Changes to the client list reach the nodes on their own, with no profile edit.
- The subscription service moves to a separate server, and its address is taken
  at install time — it is no longer baked into the code.

### Money

- Refunds, full and partial, with the history kept.

### Appearance

- Light theme by default, dark by a switch.
- English interface.

---

The history of the site itself is in
[the repository's commits](https://github.com/STEALTHNET-APP/stealthnet-software-site/commits/main).
