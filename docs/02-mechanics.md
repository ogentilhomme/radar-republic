# Core mechanics

## Phase one: roadside work

A shift lasts 300 simulation seconds. In the campaign the player can pause; menus that spend money and placement previews pause the world. An action cycle takes roughly 5–12 seconds: observe a lane, select a vehicle, hold a steady lock, read the speed and evidence quality, then issue a case or dismiss it. Case creation gives a satisfying confirmation; collected cash arrives through the office and is labeled separately.

The starter speed gun has a 70 m range, a 1.3 s stable lock, one target, and poor tolerance of occlusion. Upgrades improve range, locking speed, night reliability, or multi-lane tracking. They never invent a legal speed limit or change the true target speed. Record an immutable measurement and its road limit at capture time.

The tutorial uses a clearly speeding van, a legal driver, and an occluded car. The interface explains “Plate obstructed,” “Vehicle within limit,” or “Lost lock.” It does not punish the player for an invisible random failure. A marginal measurement displays uncertainty and can be dismissed; invalid cases cannot become money just because the player clicks faster.

The first car is a comic liability through slow acceleration, a wheezy engine, and a rattling interior. Avoid random engine stalls that remove control. The player drives between roadside bays in a compact area; exiting switches to a short first-person inspection or a stable shoulder camera. No elaborate walking simulation is required.

## Traffic model

Cars follow a small authored directed lane graph with speed profiles, headway, simple overtaking in designated areas, and persistent IDs for their trip. Full vehicle AI and full-city simulation are unnecessary. Representative traffic cohorts are cautious locals, habitual commuters, visitors, delivery drivers, and rare fast vehicles. Foreign registration is an administrative characteristic, not an automatic speeding tendency.

Each cohort has a desired-speed distribution, local route knowledge, a probability of noticing roadside objects, and time-of-day demand. Awareness changes speed upstream of a known site; the braking distance must be visible. Density affects occlusion and throughput. A faster road is not automatically more profitable: low traffic, better-informed commuters, longer evidence distances, and expensive access can offset larger fines.

Use three fixed road windows per shift: ordinary traffic, a disclosed demand change, then a short late wave. Challenge demand is pre-generated independently of player actions. Do not make a new random traffic population every time a menu is opened or a radar is moved.

## Phase two: inspect, install, operate, adapt

The map shows road families, direction, estimated flow, speed limit, local familiarity, and permitted service areas. Select any feasible roadside surface within unlocked land, then enter the actual 3D site. Move the camera freely within that area, rotate it, inspect from driver height, and confirm. “Anywhere” means geometric freedom within readable build boundaries, not inside traffic lanes, private buildings, or unreachable roofs.

The placement panel separates four quantities:

| Quantity | Meaning | Good direction |
|---|---|---|
| **Exposure** | Chance that an unalerted approaching driver can notice the housing early | Usually lower for surprise |
| **Measurement coverage** | Fraction of target lane samples that are in range, visible, and inside the sensor cone | Higher |
| **Evidence quality** | Expected plate readability and sufficient stable measurement time | Higher |
| **Known location** | Cohort knowledge accumulated over time, beyond what is visible now | Depends on revenue versus deterrence |

Never combine them into an unexplained “stealth score.” Moving behind a building can produce exposure 5%, coverage 0%, and no valid capture. A roadside billboard edge might produce exposure 30%, coverage 90%, and a useful but limited corridor. These are tutorial examples, not universal measured values.

### Geometry contract for the 3D implementation

1. Sample 20 upstream positions per affected lane, spaced by travel time, at driver eye height; weight them by the road's approach distribution.
2. Test rays to several points on the housing. A visible sample counts only inside an approach field of view and before the driver's reaction/braking horizon. Exposure is the weighted visible fraction, with documented size/contrast modifiers.
3. Separately sample the measurement corridor. Cast from the sensor to representative plate points at car and truck heights; test sensor range, facing, lane direction, plate angle, and occlusion.
4. Convert contiguous valid corridor length into dwell time using speed in m/s. If dwell time is below the device's lock requirement, coverage alone must not imply a valid capture.
5. Compute a static preview on placement changes, debounced to at most 5 Hz. Dynamic traffic causes live occlusion; show a yield range and a “busy-lane occlusion” warning, not a fake exact profit.
6. Use dedicated collision layers for measurement blockers and view blockers. Leaves can partly conceal housing but reduce readings; buildings block both. Decorative particles never count as walls.

The displayed exposure percentage is a game-model estimate, not a physical guarantee. Show sample rays on demand and a short cause sentence, e.g. “The wall hides the housing but blocks the near lane.” Confirming placement freezes its quoted construction cost. If conditions change before confirmation, refresh and explain.

### Placement states and costs

`Inspect → Ghost preview → Valid/invalid position → Quote → Confirm → Setup → Active`.

Escape cancels without spending. Invalid ghosts show the exact reason. A first fixed camera costs 900 credits; new installation is included. Redeployment costs 120 and removes it from service for one active shift. Canceling before confirmation is free; confirmed work cannot be repeatedly undone to reset drivers' memory. A service crew handles one redeployment at a time in the first management layer.

For the first installation, the crew takes 30 simulation seconds after confirmation; show a visible setup timer and produce no cases during it. For relocation, teardown and transport consume the entire next shift, with no radar upkeep during that offline shift; staff wages continue. The 120 cr quote includes the move's service costs. The current experiment starts after initial installation, with the device already owned.

## Driver learning and relocation

Knowledge belongs to a **road corridor and cohort**, not to a camera ID or exact coordinate. A 100 m road-distance neighborhood initially shares memory. Moving two metres, selling/rebuying, rotating, or changing the camera skin cannot reset it. New sites on the same corridor inherit nearby knowledge. Topological road distance avoids sharing memory across unrelated roads stacked on a bridge.

For the starting aggregate model, each shift updates knowledge `A` in [0,1]:

```text
active:   A_next = A + (1 - A) × learning_rate × (0.25 + 0.75 × exposure)
inactive: A_next = A × (1 - forgetting_rate)
speeding_probability = base_speeding × (1 - awareness_effect × A)
                       × (1 - visual_response × exposure)
```

The harness begins with learning rate .18, forgetting .08, awareness effect .75, and visual response .45. These are balance parameters. Full traffic implementation applies upstream speed behavior per cohort instead of multiplying camera income a second time. Never count both reduced speeding and an extra arbitrary “old camera” income penalty.

Knowledge grows even for a hidden radar: repeat observations and warnings spread its presence. Visitors prevent all traffic becoming perfectly informed. An inactive district cools gradually. Rotation restores some yield but costs transport, downtime, and administration. Preview “stay versus move over three shifts”; do not make optimal play a mandatory relocation every minute.

The planning harness stores one knowledge value per corridor and does not implement the 100 m falloff or separate cohorts. In the game, update a corridor/cohort memory cell once per shift using combined evidence of presence, capped at one update; adding overlapping cameras must not multiply the learning rate. Remembered locations remain after a device is removed, and one idle shift is not enough to forget them.

## Radar roles

| Device | Job and tradeoff | Initial price / unlock |
|---|---|---|
| Handheld Mk I | Active aiming; cheap, slow lock, one lane | Starter |
| Handheld Mk II | Faster lock and longer corridor; still player attention | 250 / first review |
| Fixed camera | Passive, stable capacity; location becomes known | 900 / logistics certification |
| Mobile trailer | Easier relocation, lower throughput, setup delay | 1,800 / district operator |
| Section pair | Mean speed across a corridor; expensive, two endpoints | 3,600 / regional approval |
| Patrol-mounted module | Scans on a moving patrol route; needs upgraded car | 2,600 / regional approval |

Numbers outside the runnable harness are provisional catalogue values. Avoid shipping many visually different devices with identical gameplay.

For the initial catalogue, a mobile trailer moves for 70 cr and spends the first 60 simulation seconds of the next shift setting up; an assigned technician reduces that to 30 seconds. Trailer throughput caps at 12 cases/shift to preserve a fixed camera's stationary niche. Section pairs cost 90 cr/shift and require both endpoints to operate. The patrol module adds 30 cr/shift to car operations and creates ordinary evidence, not a separate currency source. These later-device parameters are recorded in the catalogue but not simulated by the single-camera experiment.

### Section radar details

Pair entry and exit plate IDs with timestamps. Mean speed is `3.6 × certified_distance_m / elapsed_seconds`. Use the route's certified drivable distance, not straight-line distance between portals. The MVP section has no ambiguous shortcuts; cars leaving the section produce incomplete records that expire without a fine. Cars taking a legal intermediate exit are not treated as exceeding an average speed.

An entry alone never creates revenue. Endpoint failures invalidate pairs. Avoid duplicate charges for the same speeding episode: entry/exit and an overlapping spot radar use an episode ID; keep one strongest valid case. A clearly separate trip can produce a new case. Explain the section on the map with direction arrows and paired status.

## Pursuit and vehicle progression

An exceptional vehicle can be too fast for a stable roadside reading or produce an unreadable plate. Mark it as an **interception opportunity**, not a paid ticket. The player opts in, follows a bounded route, approaches within a readable distance, and holds identification for 3 seconds. Completing a safe pull-over produces the evidence needed to open the case. Do not require pursuing an already fully identified ordinary offender just to collect its fine.

Starter compact: 115 km/h, poor acceleration. Patrol sedan: 155 km/h with improved handling. Interceptor: 200 km/h, expensive upkeep. These are game values; final route lengths and acceleration must make speed upgrades useful. Offer tyres/brakes, sensor mount, then engine upgrades so top speed is not the only stat. Quotes show what opportunities the next purchase enables.

One pursuit lasts 45–90 seconds, ends at a bounded escape point, and pauses optional dispatch prompts. Ramming increases incident costs and anger; it is not the win condition. Collision recovery returns control quickly and does not trap a car behind scenery. Abandoning retains ordinary shift earnings. Campaign driving assistance uses the same payout; separate assisted and unassisted challenge categories only if tests show assistance changes score potential.

## Edge cases to lock before implementation

No revenue through walls; no duplicate tickets from overlapping detectors; no menu-time earnings; no reloaded random rerolls; no cash for incomplete average-speed pairs; no unpaid cases silently counted as spendable cash; no paid relocation with invalid destination; no fines for emergency vehicles in scripted exempt roles. A blocked radar explains the obstruction and keeps its history when moved.
