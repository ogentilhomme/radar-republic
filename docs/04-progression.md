# Progression, missions, and consequences

## Campaign milestones

The following timings are playtest targets, not validated completion estimates. Grants are campaign-only and excluded from friend challenges.

| Stage | Target | Authority and proof | Unlock and new question |
|---|---|---|---|
| Induction | 0–5 minutes | Sergeant: 3 valid cases, dismiss one legal driver | Basic shift; can you distinguish a capture from a guess? |
| Trusted patrol | 5–12 minutes | Sergeant: 250 collected, 80% valid evidence | Mk II radar and 80 km/h bypass; which traffic is worth attention? |
| Logistics certificate | 15–25 minutes | Lieutenant: 800 lifetime collected, one survey, no unresolved tutorial | Fixed camera permit and 300 campaign grant; where should automation work? |
| District operator | Shifts 5–8 | Captain: 2,000 transferred, 2 functioning shifts, anger below 60 | Clerk and trailer; capacity or another device? |
| Regional service | Shifts 9–14 | Directorate: 6,000 transferred, oldest eligible backlog below 2 shifts | Section radar, border specialist, sedan; reach or throughput? |
| National experiment | Shifts 15–20 | Ministry: 14,000 transferred, resolve an audit | Political choices, interceptor and patrol module; which costs are acceptable? |
| Recovery review | By shift 24 | Commission: 25,000 transferred, solvency and public review | Ending, scorecard, replay seed |

Permit conditions use **lifetime collected cash** or **cumulative transfers**, as explicitly named; spending money never erases an earned qualification. Promotions remain unlocked. Failing an optional condition delays the benefit and offers a specific remediation task rather than silently blocking the campaign. A temporary fixed-camera loan introduces phase two if a novice has not reached it by the third tutorial shift; it cannot be sold and ends after the demonstration.

### First-camera affordability walkthrough

One illustrative clean tutorial route starts with 150 cr. Shift 1 costs 40 and processes four 100 cr cases. At shift 2 their 400 cr arrives; another 40 cr operating cost and the 250 cr handheld upgrade leave 220 cr. Six paid cases from shift 2 deliver 600 cr at shift 3; its 40 cr patrol cost leaves 780 cr. The player now exceeds the 800 cr lifetime-collection gate and has completed a site survey. The 300 cr certificate grant raises cash to 1,080; the 900 cr fixed camera leaves 180 for the next shift. These tutorial cases have scripted payment outcomes; normal campaign cases use the disclosed collection rules. This is an existence proof of an affordable route, not a promise that every player's case outcomes will match it.

The loan camera fallback teaches the same placement flow without silently handing out a saleable asset. It is available for one demonstration shift, has its setup and upkeep funded by training, and cannot enter a ranked challenge. No promotion requires buying a device that is itself locked behind that promotion.

## Roads and district identities

1. **Municipal approach:** village fringe, delivery depot, hedge, bus stop, 50/80 km/h roads. Slow enough to teach aiming. Buildings offer obvious concealment traps. First fixed camera belongs here.
2. **Commuter belt:** interchange, bridge, industrial strip, 80/110 km/h roads. Strong direction-specific rush hours and rapid route learning. Trailer rotation, clerks, and better cars become attractive.
3. **Alpine border corridor:** motorway approach, tunnels, service area, customs office, 120 km/h fictional limit. Longer lines of sight, visitors, foreign paperwork, and a good section-radar route. Higher access and operations costs prevent a strictly superior farming spot.

Road access is unlocked by competence and a one-time permit cost, not by buying speed limits. Each tier still contains low-risk lower-income spots. The player can revisit familiar roads without losing unlocks.

Starting permit costs: municipal approach and first bypass are free after certification; commuter-belt deployment costs 400 cr after district approval; border-corridor deployment costs 1,000 cr after regional approval. Unlocking previews the purchase without spending automatically. The permit covers new installation rights in that district, not a fee every time the player drives through it.

Vehicle ladder: basic tyres/brakes at 180 cr, engine service at 300, patrol sedan at 1,200 after regional review, and interceptor at 4,000 after national review. Each car shows its upkeep before purchase. Tyres improve braking and control; the engine package improves acceleration and raises the starter ceiling to 130 km/h. Both remain useful for early interception routes. Cosmetics are independent from handling stats.

### Reasons to keep playing after automation

Give each shift one strategic intention: survey a new road, clear an expiry-risk queue, improve a weak placement, take an optional interception, or save toward a particular upgrade. The HUD remembers the player's selected purchase and shows the shortfall. A site history chart separates traffic changes, learning, evidence quality, and office losses so a declining yield becomes a solvable problem.

The second fixed camera introduces coverage versus administration; the first trailer introduces timing; the section pair introduces route reasoning; the border specialist introduces jurisdiction; the interceptor introduces execution skill. New tools should not arrive in the same debrief unless a player deliberately saved for a large jump. Promotion animations can be skipped; cosmetic unlocks never affect a standardized challenge.

## Missions as short teaching contracts

Use at most three visible objectives: one required next step, one optional skill task, one strategic suggestion. Show progress and the concrete reward before acceptance. Avoid “issue 100 tickets” padding.

Examples: obtain three clean readings without targeting a legal driver; find a site with exposure below 40% and coverage above 70%; keep one installation profitable after three shifts; process a foreign case before expiry; finish a pursuit without contact; improve collected net while issuing fewer photos; explain a failed section pair by selecting the blocked endpoint.

Daily variation changes a decision: roadworks shift traffic, an event creates visitors, a newspaper spreads radar knowledge, rain reduces readable range, or office equipment breaks and adds a temporary capacity penalty. Events are previewed before spending when feasible and have one clear duration. No event should delete a large investment without recourse.

## Public anger

Start at 10/100. Compute once at shift end and show a breakdown. Provisional shift delta:

```text
anger_delta = 2 × unfair_case_rate + 6 × substantiated_incidents
              + 3 × surprise_campaign_flag + 2 × unresolved_backlog_flag
              − 3 × completed_safety_action − 1 × clean_shift_flag
```

`unfair_case_rate` is the fraction in [0,1] of issued cases found invalid, not the percentage from 0–100; it is zero if none were issued. Flags are 0/1. The surprise flag activates only for a high-volume concealed enforcement campaign (at least 20 issued cases at exposure below .25), not any hidden camera. A clean-shift reduction requires at least five valid processed cases, no incident, and no expired eligible case, so empty shifts cannot farm approval. Limit repeated safety actions to one benefit per shift and charge their actual cash/opportunity cost. Clamp resulting anger to [0,100]. These are later campaign rules, not implemented in the current economy harness.

| Anger | Visible consequence | Recovery option |
|---|---|---|
| 0–29 | Normal traffic and permits | Keep clean evidence |
| 30–49 | More warnings spread; small learning increase | Maintain a visible deterrent site |
| 50–69 | More appeals, a clearly quoted processing burden | Improve evidence, reduce overload |
| 70–84 | New installation permits paused next shift | Resolve incidents or fund a safety action |
| 85–100 for 2 shifts | Political review and temporary operational suspension | Campaign recovery mission; challenge ends |

Use hysteresis: permits resume below 60, avoiding flicker at the boundary. Announce escalation a shift ahead. Idle time alone cannot erase anger while still earning revenue from the network. Do not create a population simulation with dozens of opaque factions for the first release.

## Safety and the revenue contradiction

A visible radar can reduce speeding and therefore direct income. Give it a bounded alternative benefit: once a surveyed high-risk site meets its deterrence goal for two shifts, it earns one campaign safety grant and reduces anger. The grant has a site-level cooldown and is not repeatable by moving a metre. Friend challenges use predefined safety objectives with payouts included in the ruleset, or no grants at all in the initial standard preset.

This creates a concrete choice: a hidden camera earns more cases today, a visible site buys political breathing room, a relocated trailer follows uninformed traffic, and a section camera catches drivers who brake only at one point. The first standard challenge disables safety grants to simplify accounting.

## Reviews and story beats

Each review is a short playable debrief, not a wall of dialogue. Show the supervisor's portrait, one absurd line, three actual metrics, and a choice of next investment. The sergeant cares about clean readings, the lieutenant about logistics, the regional chief about queues, and the minister about a graph. Later authorities sometimes ask for contradictory targets; the player chooses among disclosed rewards and costs.

No forced manipulation of evidence is required to progress. A political request to hide bad statistics can be refused or exposed through a satirical event; any optional acceptance has explicit consequences. The joke is institutional incentives and accounting theatre.

## Endings and replay

- **The Balance Sheet Hero:** fund target met, anger below 50, solvent.
- **The Ministry of Flash:** fund target met but a hostile public forces reorganization.
- **The Popular Underperformer:** miss the fiscal target while maintaining low anger and good safety results.
- **The Emergency Commission:** unsustainable debt or repeated suspension ends the program.

Every ending displays the same ledger and player choices, and offers a rematch with the same seed. Cosmetic desk objects, profile titles, and discovered Easter eggs carry over. Permanent stat boosts do not enter equal-start challenges. Achievements celebrate unusual strategies rather than daily login streaks or endless grind.
