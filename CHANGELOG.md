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

- Protocols: VLESS, VMess, Trojan, Shadowsocks 2022, Hysteria2.
- Transports: TCP, WebSocket, gRPC, XHTTP, HTTPUpgrade, mKCP.
- Encryption: Reality, TLS, or none behind a reverse proxy.
- Eleven ready-made configuration presets: pick one, it is created, then you
  adjust it. Each was verified with live traffic, not only from documentation.
- Nine ready-made routing blocks to drop into a profile.

### Clients and subscriptions

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
