# Production plan and execution handoff

## Delivery order and gates

Estimates are focused human-equivalent development days for someone familiar with the stack; generated code and assets still require integration and testing. Do not convert them into a promise based on GPU size.

| Milestone | Rough effort | Deliverable | Gate to proceed |
|---|---|---|---|
| M0 — preparation | This repository | Design, balance experiment, UX study, work contracts | Read scope and verify harness |
| M1 — scan toy | 1–2 days | Greybox road, traffic, aim, valid case, cash feedback | Ten minutes of enjoyable repeat scanning |
| M2 — first placement | 2–4 days | Fixed radar, free placement on buildable ground, two visibility measures, learning | Player explains three different placements |
| M3 — connected slice | 3–5 days | Small drivable district, upgrades, queue, clerk preview, debrief, save | 20–30 minute start-to-automation session |
| M4 — friends alpha | 3–5 days | Bounded pursuit, car upgrades, challenge, local score exchange, clean exports | Three friends finish and compare equivalent runs |
| M5 — full small game | 5–10 days | Other districts, section/mobile systems, border cases, political progression | Complete campaign and no dominant trivial strategy |
| M6 — polish | 3–5 days | Accessibility, performance, sound, errors, distribution | Repeatable install/play/export on target machines |

Expect iteration to move these ranges. The full small game is several weeks of focused work, whereas the first greybox can be quick. If time is short, ship M3 with local result cards and defer M4 pursuit complexity. Keep the full requested feature list in the later plan rather than implementing a shallow version of everything at once.

## Task cards for the implementation machine

| ID | Depends on | Scope and owned area | Acceptance evidence |
|---|---|---|---|
| T01 | M0 | Bootstrap `game/`, pinned engine, one scene, input and localization | Editor opens, window runs, documented engine version |
| T02 | T01 | Road graph and deterministic arrivals, `game/world/` | Fixed seed produces same arrival schedule; 20 vehicles flow |
| T03 | T02 | Manual lock and immutable evidence, `game/radar/` | Valid, legal-speed, occluded, and out-of-range examples |
| T04 | T03 | Cases, capacity, payment ledger, `game/economy/` | No duplicate payment; exact cash/pending distinction |
| T05 | T02,T03 | Placement preview and ray sampling, `game/placement/` | Wall, edge, open road examples with explanations |
| T06 | T04,T05 | Fixed operation and corridor memory | Long placement loses surprise; trivial move retains memory |
| T06A | T02 | Basic arcade patrol car and enter/exit; no pursuit logic | Drive between two bays, brake, recover if stuck |
| T07 | T04,T06,T06A | Tutorial, shop, debrief, promotion, `game/ui/` | Novice reaches first camera within target window |
| T08 | T07 | Save/load and exports | Reload preserves queues, knowledge, cash, and seed |
| T09 | T08 | Car upgrades and optional bounded interception | Successful identify/pull-over; recover from collision; escape cleanly |
| T10 | T08 | Challenge identity and local result import/export | Separate mismatched rules; reject malformed file |
| T11 | T06,T08 | Section pair and mobile trailer | Exit/incomplete/overlap cases; relocation cost and delay |
| T12 | T04,T07 | Border office and opinion/reviews | Foreign backlog visible; warning before suspension |
| T13 | T09–T12 | Final content, audio, performance and playtests | Complete campaign + friend playtest report |

T09 is deliberately after the core slice; complex driving must not delay proving the money/placement loop. Basic movement between bays in M3 may use a simple arcade controller; T09 adds interception behavior.

Do one task in a coherent branch, report its proof, then integrate. If the user later authorizes multiple agents, only delegate bounded independent areas after interface contracts are agreed. The roadmap itself is not an instruction to spawn agents.

## Reusable implementation brief

```text
Implement Txx in Radar Republic.
Read AGENTS.md, README.md, docs/07-production.md and the subsystem design.
State the exact implemented slice and dependencies before editing.
Use the pinned Godot version and current balance configuration.
Keep simulation independent from UI. Preserve ledger and case invariants.
Do not add later milestone features or runtime cloud dependencies.
Run appropriate checks and demonstrate the card's acceptance scenario.
Handoff: files changed, commands run, evidence, known limits, next task.
```

The harness orchestrates repeatable checks and task contracts; it does not install a local LLM, choose a GPU inference framework, or automatically run autonomous workers. Those choices require the actual GPU/VRAM, OS, and preferred agent runtime.

## Two-machine workflow

**Planning machine (current):** source of the design, data, review logs, and lightweight checks. Repository path: `/home/oscar/repos/radar-republic`. Use `python3 tools/check.py`; inspect the HTML study directly or serve it locally. All commands in this repository assume that working directory.

**Implementation/GPU machine:** install Git, Python 3.11+, Godot 4.5.2 Standard and its matching export templates. Use a native checkout for the editor and game even if an agent runs in another shell environment. Prefer moving changes through Git rather than synchronizing a live `.godot/` cache. Blender is optional once authored 3D assets replace primitives; it is not needed for M1.

No remote has been created. After choosing a host, push this local repository and clone it on the second machine. If using a private remote, keep it private until the release and asset license choices are settled. A local source archive can bootstrap the second machine without a hosting account, but commits and one integration branch should become the normal source of truth. The initial setup snapshot is authored by Codex using per-command Git identity; global user identity settings are unchanged.

Example checks after a Godot project and smoke runner exist (these are **future commands**, not currently runnable):

```sh
godot --version
godot --headless --path game --import
godot --headless --path game --script res://tests/run_smoke.gd
godot --path game --editor
```

Exports additionally need named presets, matching templates, and an existing destination directory. M1 must add a doctor check that fails clearly for a missing or wrong engine version. Current `tools/check.py` validates only the present planning artifacts.

## Release checklist at M4

- Archive includes executable, required resources, short controls/readme, credits, and version.
- Saves live in the engine's user-data directory, outside the install directory.
- A clean computer can start offline and complete a challenge without the editor or Python.
- Same challenge metadata produces one comparison group; differing balance builds do not mix.
- No private configuration or asset caches are distributed.
- Known issues and assistance category appear on the result card.
- Each build receives its own immutable version; do not silently replace the balance under an existing version.

## Risk register and cuts

| Risk | Early evidence | Mitigation / cut |
|---|---|---|
| Aiming gets dull | Testers stop after ten cars | Improve timing/feedback/target variety before progression |
| Placement feels arbitrary | Players cannot predict the better spot | Show sample rays and causes; reduce hidden modifiers |
| Automation becomes passive waiting | Long intervals without decisions | Short shifts, optional field work, meaningful forecast changes |
| Administration feels like busywork | Players avoid the office | Automatic routine processing, exceptions only |
| Driving dominates production | More time on collisions than the core loop | Restrict pursuit routes; defer general city driving |
| Economy snowballs or stalls | Extreme seed sweeps | Capacity and costs; tutorial loan; no mandatory expensive dead end |
| Scores are incomparable | Different starts/builds mix | Hard scenario grouping and clear unverified label |
| Big PC hides poor performance | Friends get frame drops | Cap content and benchmark on an ordinary PC |

## Open choices and current defaults

Working name Radar Republic; English source language; fictional setting; downloadable Windows/Linux; no hosted backend; no paid asset purchases; compact 3D districts; keyboard/mouse first. Confirm OS and browser preference when available. Device prices and campaign targets are tuning candidates. A project license and public hosting choice remain undecided; this does not block local development.
