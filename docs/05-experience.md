# UX/UI, visual design, and sound

## Presentation

A stylized low-poly 3D Franco-Alpine world: concrete municipal buildings, yellowed office paper, faded blue patrol cars, cream road signs, pine-covered hills, and excessively polished financial districts. Clean silhouettes and readable road geometry matter more than photorealism. Use an original police emblem and fictional licence plates.

The interface contrasts a functional field instrument with ridiculous administrative paperwork. Dark navy panels, warm off-white text, amber pending value, teal collected cash, and red problems. Color always has a label/icon partner. Sparse rubber-stamp animations make promotions tactile without slowing frequent actions.

## Screen hierarchy

| Context | Main content | Persistent essentials | Primary action |
|---|---|---|---|
| Patrol | Road, aim, target speed and limit | Cash, pending cases, shift time, next objective | Hold scan / issue case |
| Driving | Road and route | Own speed, selected opportunity, fuel/condition if relevant | Drive or pull over |
| Map | Road flow and owned devices | Cash, anger, queue warning | Inspect a site |
| Placement | Actual 3D ghost and lane corridor | Exposure, coverage, evidence, knowledge, cost | Confirm installation |
| Office | Queue trend and bottleneck summary | Collectable value, wages, expiry risk | Hire or change priority |
| Garage | Before/after vehicle stats | Purchase + ongoing cost | Buy improvement |
| Debrief | Collected net and causes | Promotion progress, anger change | Plan next shift |
| Friends | Comparable results for one ruleset | Seed, build, verification label | Import result / rematch |

Do not put the complete tycoon dashboard over the first-person roadside view. A single case receipt expands briefly then moves into history. Queue warnings aggregate; fifty simultaneous photos must not produce fifty popups.

## First five minutes

0:00–0:30: arrive in the bad car; one-line briefing, “The treasury has assigned you a speed gun.” Move and look immediately; skippable camera flourish.

0:30–1:30: scan a clear van. Speed and road limit are adjacent. A stable lock fills around the reticle, and a gentle tone rises. The resulting case says “100 cr pending,” not “100 cr cash.”

1:30–2:30: a legal car teaches dismissal and a truck creates an occlusion. The failed read explains why and offers another car promptly.

2:30–3:30: automatic desk processing turns a sample case into collected cash in a separate practice ledger, explicitly labeled “Training settlement.” This demonstration resets to the normal 150 cr opening budget before the first campaign shift and does not enter lifetime collection, challenges, or the affordability walkthrough. Normal payment delays then begin.

3:30–5:00: choose a better roadside position, complete a short wave, then see a three-line report and a meaningful upgrade. The tutorial must not require reading all four radar metrics before the first successful scan.

## Placement interaction

Transition from map to site in under two seconds on target hardware. Start in an elevated orbit view; a button previews driver eye height. Drag the ghost on eligible ground; Q/E rotate, wheel adjusts height only for supported mounts, and Shift provides fine movement. Ground/road bounds stay visible. Include on-screen controls and keyboard placement alternatives.

Right-side panel order:

```text
FIXED CAMERA · Bypass / Eastbound
Exposure             28%  Low housing visibility
Coverage             86%  Near lane partly blocked
Evidence quality     91%  Enough time for a clean read
Known location       42%  Commuters still remember this site

Estimated cases      10–16 / shift
Estimated net        420–680 cr / shift after listed costs
Office capacity      8 / shift · Backlog likely

Install cost         900 cr
Ongoing cost          45 cr / shift
[Driver view] [Show sample rays]
[Cancel]                       [Install]
```

These are layout example numbers, not a computed promise. Hover or focus each metric for a plain explanation. Always show the cause of a placement improvement: “Better plate angle, but housing visible earlier.” If a quote assumes a specialist or a free clerk, label that assumption. Show the effective state immediately after placement and refresh live results separately from forecasts.

An invalid position preserves the ghost and displays “Sensor is inside the wall,” “Service access blocked,” or “No valid lane corridor.” Do not silently snap to another location and spend money there.

Show “estimated” directly beside forecasts, with an expandable list of assumptions: flow, familiarity, eligible jurisdictions, office capacity, costs, and observation sample size. A range describes modeled variation, not a confidence guarantee. When pinning a site for comparison, retain those assumptions with the snapshot; changing traffic volume must not look like an improvement caused only by placement.

Empty/error states need designed text: “No eligible cases yet,” “Three foreign cases need a border specialist,” “Insufficient cash: 120 cr short,” “Save could not be written; previous save retained,” and “This result uses another ruleset.” No generic red exclamation mark without an action. Destructive save replacement and irreversible treasury transfers get explicit consequence copy; ordinary inspection and cancellation do not.

## Controls and accessibility

| Context | Default desktop controls |
|---|---|
| Move / drive | WASD; mouse look; Space brake while driving |
| Scan | Hold left mouse; optional toggle-to-lock |
| Case confirmation | F when valid; tutorial explains the state |
| Interact / enter car | E outside placement |
| Map / office | Tab / O |
| Placement | Pointer or arrows; Q/E rotate; Enter confirm; Escape cancel |
| Pause | Escape when no modal is open |

Controls are contextual, fully remappable, and never require fast repeated tapping. Show focused state, keyboard traversal, subtitles, readable text at 1280×720, UI scaling 100–150%, adjustable field of view, sensitivity, inverted look, motion blur off by default, and reduced camera shake. Offer reduced flash effects. Target controller support after the core mouse/keyboard layout works; it is not a P1 requirement.

At 16:9 the placement panel is about 340 px wide at 1080p. At 720p use tabs for forecast details but retain all four immediate placement metrics. Ultrawide expands the world view rather than stretching text. Keep simulation and UI resolution independent.

## Sound and feedback

Starter equipment: soft electrical whine, plastic button, paper printer. Better tools sound cleaner but no louder. A clean capture has a short click and restrained confirmation; a payment has a different office sound. The difference teaches evidence versus money without a tutorial paragraph.

Pursuits use engine pitch and tyre noise to communicate speed; no mandatory siren at maximum volume. Radar flash can be replaced with a subtle icon. Music evolves from lonely roadside radio to an absurdly confident administrative march, with independent volume sliders and subtitles for radio chatter.

## Assets and composition

First slice budget: one modular road kit, one hedge kit, four building shells, two civilian vehicles, one player car, handheld model, fixed radar housing, three office props, one daylight setup. Build collisions from simple proxies. Texture atlas and materials stay restrained; defer interiors beyond the desk and car dashboard.

For later generation on the GPU PC, create reference sheets before final assets: orthographic vehicle views, consistent palette, front/side/back camera housings, and a district composition sheet. Do not use generated raster images as a substitute for editable 3D meshes and tested collisions. Register provenance, license, and modifications for every imported asset.

## Playtest script

Give a friend no explanation beyond the goal. Watch the first scan, cash/pending distinction, first purchase, and first placement. Ask them to predict which of two sites earns more, then let them try both. Success targets: first valid capture within 90 seconds; at least 4/5 testers distinguish exposure and coverage after one example; at least 4/5 can explain the largest loss on their debrief. If they cannot, revise labels and feedback before adding more mechanics.

The local HTML study in `prototype/` explores this panel hierarchy and the concealment/coverage tradeoff. It deliberately uses authored site assumptions in a 2D diagram. Actual 3D inspection, ray sampling, keyboard driving, and performance validation belong to the Godot slice.
