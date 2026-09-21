# Project working agreement

Read README.md, docs/07-production.md, and the document for the subsystem before editing it. Documentation and identifiers are English. Default game copy is English; use localization keys from the first UI implementation. The setting and fines are fictional.

This repository currently contains a design package and planning harness. Do not describe it as a playable game. Work one accepted milestone at a time; preserve the user's core fantasy and distinguish implemented behavior from proposals.

- Keep balance values in data/balance.json; state units, simulation scope, and seed.
- For design or balance changes, update affected contracts and record the consequence.
- Run `python3 tools/check.py` before handing off harness changes.
- A passing Python harness is not evidence that Godot rendering, driving, saves, or exports work. Attach appropriate game evidence once those exist.
- Do not add accounts, cloud services, paid assets, telemetry, or network-dependent runtime behavior merely to implement the first slice.
- Use original fictional organizations, signs, logos, and plates. Record source/license for imported assets in art/ASSET_REGISTER.csv.
- Save schema and balance changes need explicit version changes before shared challenges ship.
- Do not spawn other agents unless the user explicitly requests it. The task cards are suitable for either sequential execution or later user-authorized delegation.
- Do not commit generated binaries, secrets, imported engine caches, or local test reports.

Every implementation handoff states: files changed, scenario to try, checks run, known limits, and next task. Keep a single integration owner if multiple contributors are authorized later.
