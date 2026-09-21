# Review 3 — UX/UI and implementation readiness

Re-read the screen flows, time/payment explanation, comparison design, score exchange, and machine handoff. Exercised the local study in a real headless Chrome browser and visually inspected its desktop screenshot.

## Findings and applied refinements

- The tutorial's accelerated sample payment could be confused with the campaign ledger. It now belongs to a separate practice ledger that resets before the 150 cr campaign start, avoiding duplicate or unexplained early cash.
- A pinned forecast initially retained staff and knowledge but omitted traffic flow. The comparison now retains cars/shift too, so a changed demand assumption is not mistaken for better geometry.
- The interactive study showed a precise model average. Added immediate explanation that it is not guaranteed income and specified expandable assumptions and modeled ranges for the future game.
- Added concrete empty/error states and consequence copy for saves, funding, and incompatible friend results.
- Added result-card accounting fields and arithmetic validation; retained the clear distinction between a checksum and actual gameplay verification.
- Centralized the later-device/vehicle starting catalogue in the balance file and documented refreshing the generated offline UI data. The harness detects stale copies.

## Browser checks

The connected-browser tool could not attach to its extension. Used the installed Google Chrome in an isolated headless test profile through the local DevTools protocol instead; no browser package installation was needed.

- Initial authored scenario produced an illustrative expected net of 971 cr/shift.
- Selecting the blocked-building scenario produced 0% coverage and −120 cr/shift, with an explicit obstruction explanation.
- Raising location knowledge to 100% lowered expected net to 201 cr/shift.
- High traffic with no clerk displayed the office overload warning.
- Enabling the border specialist raised the selected office capacity to 40 work units.
- Pin/reset controls updated the comparison and restored defaults.
- After the review fix, pinned comparisons retained the 80 cars/shift assumption; an actual keyboard ArrowRight event advanced the focused knowledge slider from 20 to 21.
- Desktop 1440 px, 1280×720, and narrow 390×844 layouts had no horizontal document overflow.
- No JavaScript runtime exceptions were observed during those interactions.

Local screenshots and raw check output are in ignored `reports/local/`; they are machine-specific evidence, not required source assets. The narrow layout is useful for reviewing the study on a phone, not a mobile-game platform commitment.

## Remaining limits

No human friend playtest, Godot executable, 3D visibility test, controller test, engine export, game performance benchmark, or hosted score service exists yet. The complete plan, three review records, working planning tools, and UI study are ready for T01 on the implementation machine. English remains the source language and downloadable Windows/Linux remain defaults pending platform confirmation.
