# Collection workflow

This dashboard is generated from `system/collections.json` and repository content. Pipeline stages are handled by the Atlas workflow. Only **awaiting editorial sign-off** requires the editor.

| Collection | Entries | Evidence | Claims | Pipeline stage | Sign-off | Review | Checkpoint |
|---|---:|---:|---:|---|---|---|---|
| 🔮 After the Internet / 🔌 Networks | 52 | 52 | 103 | Committed | Autonomous | [[system/reviews/after-the-internet-networks|Open report]] | `458df73` |
| 🔮 After the Internet / ⚡ Paradigms | 105 | 105 | 210 | Committed | Autonomous | [[system/reviews/after-the-internet-paradigms|Open report]] | `6d4bbb8` |
| 🔮 After the Internet / 👯 Culture | 70 | 70 | 140 | Synthesis Ready | Autonomous | [[system/reviews/after-the-internet-culture|Open report]] | — |
| 🔮 After the Internet / 👩‍⚖️ Rules | 13 | 13 | 30 | Committed | Completed | — | `07b8701` |
| 🧰 Nature of the Firm / 🌍 Ecosystems | 16 | 0 | 0 | Planned | Autonomous | — | — |
| 🧰 Nature of the Firm / ⚡️ Organization | 33 | 0 | 0 | Planned | Autonomous | — | — |
| 🧰 Nature of the Firm / 👯 Culture | 30 | 0 | 0 | Planned | Autonomous | — | — |
| 🧰 Nature of the Firm / 👩‍⚖️ Governance | 13 | 13 | 31 | Committed | Completed | [[system/reviews/nature-of-the-firm-governance|Open report]] | `daa1adb` |
| 🧑‍🎨 Power to Creators / 🤝 Communities | 15 | 0 | 0 | Planned | Autonomous | — | — |
| 🧑‍🎨 Power to Creators / ⚡️ Niches | 13 | 0 | 0 | Planned | Autonomous | — | — |
| 🧑‍🎨 Power to Creators / 😍 Vibe | 44 | 0 | 0 | Planned | Autonomous | — | — |
| 🧑‍🎨 Power to Creators / 🕹 Gameplay | 94 | 0 | 0 | Planned | Autonomous | — | — |
| 👩🏻‍🎓 How We Learn / 🔮 Futuring | 76 | 0 | 0 | Planned | Autonomous | — | — |
| 👩🏻‍🎓 How We Learn / 🏛 Architectures | 50 | 0 | 0 | Planned | Autonomous | — | — |
| 👩🏻‍🎓 How We Learn / ☯️ Sustaining | 36 | 0 | 0 | Planned | Autonomous | — | — |
| 👩🏻‍🎓 How We Learn / 💥 Transitions | 26 | 0 | 0 | Planned | Autonomous | — | — |

## Progress

- Collection checkpoints committed: 4/16
- Planned source entries: 686
- Preferred processing chunk: up to 25 entries

## Synthesis backlog

- Tracked propositions: 15
- Unresolved propositions: 15
- Promoted propositions: 0
- Retired propositions: 0
- Pipeline source of truth: `system/synthesis-backlog.json`

## Stage meanings

`planned → evidence ingested → metadata checked → claims extracted → synthesis ready` are pipeline stages.

`awaiting editorial sign-off` is the sole human gate. After the designated sign-off collection, later collections use autonomous validated checkpoints.
