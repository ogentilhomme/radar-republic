# Review 1 — mechanics and economic invariants

Performed after the initial design and runnable economy experiment were written. Read mechanics, economy, progression dependencies, configuration, and test output. This was a self-review, not an independent review or a player study.

## Findings and applied changes

| Finding | Why it mattered | Change applied |
|---|---|---|
| Expiry said “three subsequent shifts” but the example expired at shift 4 | Two possible implementations would disagree by one shift | Defined capture shift + two subsequent shifts, matching the harness and expiry test |
| Negative cash and unpaid liabilities could both represent one expense | Net score could penalize debt twice | Campaign uses zero-floor cash + liabilities; experiment uses signed cash only |
| New installation timing and relocation upkeep were incomplete | Forecasts could disagree with actual downtime | Added 30-second initial setup, whole-shift relocation, wages continuing, offline radar upkeep waived |
| Knowledge design was more detailed than its implementation | Readers might assume the harness validates spatial memory | Explicitly separated corridor-only experiment from 100 m/cohort game model |
| Multiple cameras could accelerate learning through repeated updates | Overlap could change behavior by callback count | Capped memory-cell learning to one combined update per shift |
| Boundary ordering was implicit | Last-minute captures and payments could resolve differently | Specified payment, expiry, commitments, capture, processing, learning, debrief order |

## Evidence

Twelve Python contract tests passed, including blocked sensor, capacity, expiry boundary, foreign eligibility, memory persistence, relocation downtime, score transfer invariance, and settlement. Accounting checks run across 20 seeds and both policies.

Seed 42, 12 shifts, one clerk, no specialist: static site returned 9,360 cr net; three-shift rotation returned 6,835 cr net. A separate 20-seed sweep averaged 10,065 versus 8,745 cr over 12 shifts, while 48 shifts averaged 21,385 versus 27,425 cr. Thus short-term relocation costs matter and long-term learning can favor moving in this simplified setup. This does not establish campaign balance.

At 10 cars/shift, 0/1/2 clerks averaged 945/−55/−1,055 cr net; at 80 cars/shift they averaged 8,070/10,050/9,050 cr. The office investment has a demand-dependent payoff instead of “more staff is always better.”

## Still unproven

Actual ray geometry, dynamic occlusion, manual skill income, multi-device saturation, and the full campaign purchasing curve need Godot implementation and further testing. Preserve that distinction in all handoffs.
