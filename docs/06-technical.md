# Technical architecture and score exchange

## Engine decision

Use **Godot 4.5.2 Standard, GDScript, Compatibility renderer initially**. Pin the same editor and export templates on both machines. This is a confirmed stable baseline, not a claim about the newest release. Godot offers a native 3D editor and command-line/headless workflows suited to a small game and automated checks. See [official sources](09-sources.md). No engine has been installed here.

The recommendation is about development scope: simple traffic, modest scenes, data-driven rules, and an inexpensive sharing workflow. A huge GPU can help with rendering and asset tools but does not remove design, debugging, or CPU simulation costs. Benchmark on an ordinary friend's computer before adding effects. Consider Forward+ only after measuring a concrete visual need; do not rewrite the simulation around a renderer choice.

Alternatives: a browser engine can reduce download friction but introduces browser export and performance constraints; Unity may suit an existing C# team; Unreal is reasonable for an experienced Unreal developer but unnecessary for the proposed visual scope. Revisit the engine only if browser play or a strong existing tool preference becomes a requirement.

## Boundaries

```text
GameSession
  World / RoadGraph / TrafficDirector
  PatrolController / PlayerVehicle / PursuitController
  RadarSystem / VisibilitySampler / EvidenceLedger
  Administration / PaymentSchedule / TreasuryLedger
  AwarenessMap / OpinionSystem / ProgressionDirector
  SaveService / ChallengeRules / ResultsExporter
  UI (observes state; submits validated commands)
```

Keep economics independent of rendered nodes. A radar produces an observation; validation produces a case; administration produces a processed case; payment changes the ledger. UI cannot directly mint cash. Use immutable IDs and one authoritative state transition per event. A duplicate callback is ignored, not paid twice.

Proposed signals: `measurement_completed`, `case_validated`, `case_processed`, `payment_resolved`, `radar_relocated`, `shift_closed`, `promotion_unlocked`. Commands have IDs and validate preconditions: `purchase`, `confirm_placement`, `hire`, `transfer`, `accept_pursuit`. Transfers and purchases commit atomically with their ledger entry.

## Time and simulation

Physics updates at 60 Hz; logical traffic decisions at 10 Hz; demand, awareness, administration, and political results close on shift boundaries. All financial values use integer credits. Use a monotonic simulation tick, not wall-clock time. A pause freezes traffic, lock timers, learning, office timers, and wages together. Fast-forward is only available in management view and affects every simulation system consistently; disable it during player driving or a pursuit.

Random streams are separate for traffic demand, driver traits, events, payments, and cosmetic effects. Stable seeds and IDs prevent turning a camera or changing a particle effect from changing payment rolls. Precompute challenge arrivals and event schedules. Do not claim cross-platform deterministic 3D physics: the first local challenges are trust-based comparable scenarios, not replay-verified authoritative simulations.

## Data contracts

| Record | Essential fields |
|---|---|
| Road | ID, directed lanes, arc length, speed limit, corridor ID, build areas |
| Radar | ID, device type, transform, road/corridor ID, active state, setup remaining |
| Observation | vehicle/trip ID, detector ID, capture tick, speed, limit, quality, exemption |
| Case | ID, episode ID, evidence reference, face value, jurisdiction, state, expiry, payment due |
| Ledger entry | ID, tick, account, signed integer amount, reason, originating command ID |
| Challenge | ID, seed, build/rules/balance hashes, shift budget, starting loadout, assistance category |
| Result | challenge identity, pseudonym, ledger totals, score, completion state, anger, incidents |

Validate imported types, bounds, lengths, enum values, and schema version. Do not execute scripts or load external paths from imported score files. Results need no real name, email, or actual licence plate.

## Saves

Versioned JSON or a similarly inspectable envelope with schema version, build ID, seed, RNG states, elapsed ticks, player inventory, transform, road knowledge, pending section pairs, complete case states, queued payments, ledger, event schedule, public anger, and progression. Save at shift boundaries for P1; add mid-shift save only after locking/section/pursuit state is covered.

Write a temporary file, validate it, replace the last save atomically, and retain one backup. Unsupported future schemas open a clear error instead of overwriting data. Save/load must not duplicate payments, reroll events, reset awareness, erase liabilities, or replenish challenge time. Campaign saves can resume freely; challenge resume stays in the same run ID and preserves remaining ticks. Edited/offline results remain explicitly unverified.

## Friends first: asynchronous challenges

P2 exports a small `.radar-result.json` and a readable result card. Friends import files into a local board. Compare only identical challenge ID, seed, build, ruleset, balance hash, and assistance category. Incompatible results remain visible in another group with a reason. Ties use the rules in [economy](03-economy.md). Duplicate run IDs replace identical records or report conflicting content; they never create extra wins.

The result card shows opening cash, collected receipts, purchases/operations, treasury transfers, closing cash, liabilities, pending uncollected value, and the final formula. An importer recomputes the score from the declared fields and rejects an arithmetic mismatch; this catches malformed data without pretending to verify the underlying gameplay. Limit an imported result to 64 KiB and a pseudonym to 32 characters. Treat names as text, never markup. A run records its completion status separately from its score.

The share code identifies a scenario, not a server: `RR1/<scenario>/<seed>/<rules-hash>`. Each friend must have that build and scenario. A result checksum detects corruption only; it cannot establish that the player did not edit the score. Label every initial submission **Local / unverified**. Friend trust is appropriate for this release, but do not market it as anti-cheat.

Later, if wanted, host an opt-in private room board with invitations, input validation, submission limits, and signed server receipts. Authentic score verification additionally requires server-authoritative outcomes or validated action logs with a suitable deterministic model; signing arbitrary client totals does not solve cheating. Hosted services, accounts, and maintenance are not dependencies for the first playable.

## Performance and observability

Initial budgets, to be measured: 60 fps at 1080p on a midrange PC, 30 fps low preset fallback, 100 active traffic vehicles, 8 active radars, 2 section pairs, under 250 ms placement feedback, and under 2 s site transitions. Record CPU/GPU frame time and memory on a named test machine before calling these achieved.

Pool civilian vehicles, simplify distant simulation, cache static visibility, and cap per-frame ray work. Never run all sample rays for every radar on every rendered frame. Traffic route nodes and camera transforms are cheap debug overlays; show case reasons and ledger transitions in a developer panel. Use event IDs to explain apparent money discrepancies.

Local debug logs contain scenario IDs and fictional records only; telemetry is off by default. Failure reports include build and balance hashes. The big-GPU PC produces screenshots, short capture videos, benchmark notes, and exported builds; the planning machine reviews them.

## Verification layers

1. Current Python harness: finite bounded parameters, accounting invariants, deterministic payments, capacity/expiry behavior, knowledge behavior, and configuration references.
2. Future Godot headless tests: evidence validation, section pairing, command idempotency, queues, save migration, ledger reconciliation, challenge matching.
3. Future 3D scenes: wall blocks readings; partially hidden housing retains the lane view; two-metre movement retains corridor knowledge; opposite-direction lane is not incorrectly targeted.
4. Future human sessions: aim feel, driving control, UI explanations, pursuit recovery, exports on clean Windows/Linux machines.

Do not replace layer 4 with screenshots of an empty scene or a headless process that only launches successfully.
