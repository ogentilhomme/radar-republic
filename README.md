# Radar Republic

**A 3D roadside enforcement game that grows into a satirical radar-management tycoon.**

You inherit a battered patrol car, a temperamental speed gun, and an absurd order: rescue the Republic's finances. Catch speeders, improve your equipment, build a radar network, hire an administration, and survive the political consequences of your success.

Working title; fictional Franco-Alpine setting; English documentation, code, and default game text. French localization is planned. This is a **design and development preparation repository**, not a playable 3D game yet.

## Start here

1. [Game vision and scope](docs/01-vision.md)
2. [Radar, traffic, placement, and pursuit mechanics](docs/02-mechanics.md)
3. [Economy, administration, and simulation rules](docs/03-economy.md)
4. [Progression, missions, and public opinion](docs/04-progression.md)
5. [UX/UI, controls, art, and audio](docs/05-experience.md)
6. [Architecture, saves, and friend scores](docs/06-technical.md)
7. [Production plan and agent handoff](docs/07-production.md)
8. [Satire and Easter eggs](docs/08-satire.md)
9. [Research and design references](docs/09-sources.md)
10. [Three design reviews and resulting changes](docs/reviews/README.md)

## Available now

- Full design, staged delivery plan, acceptance criteria, and future agent task briefs.
- Editable [balance configuration](data/balance.json) and a deterministic Python **economy experiment**. It tests one fixed-radar site, not a complete campaign or 3D visibility.
- [Interactive placement UX study](prototype/index.html): a local HTML diagram with editable assumptions. Its illustrative values are not geometry measurements or a playable 3D world.
- Standard-library tests and CI configuration for the planning harness.

From this directory, with Python 3.11 or newer:

```sh
python3 tools/check.py
python3 tools/simulate.py --strategy static --seed 42 --shifts 12
python3 tools/simulate.py --strategy rotate --seed 42 --shifts 12
python3 -m http.server 8000 --bind 127.0.0.1 --directory prototype
```

Open `http://127.0.0.1:8000` after the last command, or open `prototype/index.html` directly. On Windows use `py` instead of `python3` if appropriate. No packages, accounts, or GPU are needed for these tools.

After changing `data/balance.json`, run `python3 tools/sync_prototype.py` to refresh the offline UI study, then run the checks. `tools/check.py` detects stale prototype data.

## Recommended first playable

Build one 3D district, one bad car, a manual speed gun, an upgrade, and one fixed camera. The 20–30 minute slice must prove that aiming is enjoyable, placement is understandable, drivers learn, and administrative capacity matters. Build the larger campaign only after friends want another run.

The proposed game engine is **Godot 4.5.2 Standard + GDScript**, a deliberate stable baseline rather than a claim that it is the latest version. Target downloadable Windows/Linux builds; platform confirmation is pending. The powerful PC does generation, implementation, rendering, and game validation; this machine can run the docs and balance harness. See [machine setup](docs/07-production.md#two-machine-workflow).

## Status and limitations

All prices, pacing, yields, and performance budgets are starting hypotheses. The simulator does not validate fun, driving, full balance, or GPU performance. No Godot runtime, game build, remote repository, leaderboard server, or generated art is included. Git is initialized locally; remote hosting and the final license are undecided.
