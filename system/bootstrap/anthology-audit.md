# Bootstrap Structural Audit

- Raw file: `raw/thoughtforming-on-digital-transformation-2026-07-10.md`
- SHA-256: `42794efb22e69cef120d7cf5812b79e06dfbeca9904fde60916de94fe2bd036a`
- Source lines: 2793
- Gate: **PASS**

## Summary

| Measure | Count |
|---|---:|
| H1 domains | 4 |
| H2 collections | 16 |
| H3 entries | 686 |
| Quote bodies | 686 |
| Errors | 0 |
| Warnings | 6 |

## Editorial collections

| H1 | H2 | Entries |
|---|---|---:|
| 🔮 After the Internet | 🔌 Networks | 52 |
| 🔮 After the Internet | ⚡ Paradigms | 105 |
| 🔮 After the Internet | 👯 Culture | 70 |
| 🔮 After the Internet | 👩‍⚖️ Rules | 13 |
| 🧰 Nature of the Firm | 🌍 Ecosystems | 16 |
| 🧰 Nature of the Firm | ⚡️ Organization | 33 |
| 🧰 Nature of the Firm | 👯 Culture | 30 |
| 🧰 Nature of the Firm | 👩‍⚖️ Governance | 13 |
| 🧑‍🎨 Power to Creators | 🤝 Communities | 15 |
| 🧑‍🎨 Power to Creators | ⚡️ Niches | 13 |
| 🧑‍🎨 Power to Creators | 😍 Vibe | 44 |
| 🧑‍🎨 Power to Creators | 🕹 Gameplay | 94 |
| 👩🏻‍🎓 How We Learn | 🔮 Futuring | 76 |
| 👩🏻‍🎓 How We Learn | 🏛 Architectures | 50 |
| 👩🏻‍🎓 How We Learn | ☯️ Sustaining | 36 |
| 👩🏻‍🎓 How We Learn | 💥 Transitions | 26 |

## Issue summary

| Code | Count |
|---|---:|
| `heading.noncanonical` | 2 |
| `quote.multiline` | 2 |
| `url.suspicious_host` | 2 |

## Issue details

- **WARNING `heading.noncanonical`** — line 173, entry 41: H3 is recoverable but noncanonical (hidden Unicode before the link)
- **WARNING `quote.multiline`** — line 1193, entry 292: quote body spans 2 nonblank lines
- **WARNING `heading.noncanonical`** — line 1367, entry 334: H3 is recoverable but noncanonical (text before the link: '“')
- **WARNING `quote.multiline`** — line 1485, entry 362: quote body spans 2 nonblank lines
- **WARNING `url.suspicious_host`** — line 1762, entry 431: URL host appears incomplete: 'magazine'
- **WARNING `url.suspicious_host`** — line 2711, entry 666: URL host appears incomplete: 'boz'

## URL diagnostics

| Diagnostic | Count |
|---|---:|
| Plain Http Urls | 10 |
| Query Urls | 54 |
| Social Post Urls | 35 |
| Suspicious Hosts | 2 |
| Token Urls | 3 |

## Next gate

Review every error and decide whether to repair the raw source or register an explicit exception. Do not generate Evidence shells until the structural gate is accepted.
