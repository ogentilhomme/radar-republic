# Economy and administration

All currency is fictional **credits (cr)**. One shift is five simulation minutes; staff capacity and wages below are **per shift**, never per real-world minute. Numeric values are starting hypotheses, not predictions of real fines or government budgets.

## Money has three different states

1. **Pending face value:** photographed cases that may or may not be valid, processed, or paid. Never spendable.
2. **Operating cash:** collected money available for equipment, wages, fuel, relocation, and maintenance.
3. **Treasury contribution:** money permanently transferred toward recovery. Cannot be withdrawn or counted twice as cash.

Start the campaign with 150 cr, a car, and a handheld radar already owned. After each shift, resolve payments and expenses, then offer a transfer slider. Default recommendation: retain next-shift fixed costs plus the next chosen purchase, transfer part of the surplus. There is no compulsory early tax that makes the first camera unattainable. Transfers are irreversible and have a confirmation showing next-shift affordability.

The economy experiment starts with an already-owned fixed camera and 1,200 cr, intentionally different from campaign start. It tests operating decisions, not the acquisition curve. Equipment prices in the configuration are shared starting values; progression targets below require a later full-campaign simulation and human tests.

## Capture and payment pipeline

`Observed → Evidence captured → Validated → Queued → Processed → Awaiting payment → Paid / Rejected / Expired`.

- A validated domestic case costs one office work unit; an eligible foreign case costs two.
- The player has basic automatic domestic processing: 8 units/shift. Manual paperwork is an optional short tutorial interaction, never a compulsory action for every case.
- A clerk adds 20 units/shift and costs 75 cr/shift. Hiring costs 100 cr once. The player sees gross workload, oldest case age, and estimated collection delay before hiring.
- A border specialist adds 12 units/shift, costs 110 cr/shift, and unlocks foreign processing in campaign P3. The prototype can explicitly enable this assumption.
- A supervisor adds 15% pooled capacity rounded down, costs 180 cr/shift plus 250 hiring, and is limited to one. A technician costs 90 cr/shift plus 150 hiring and halves trailer setup time; fixed-camera transport still consumes a full shift. These are later roles, not multiplicative infinite-stacking upgrades.
- Queue discipline: earliest expiry first among eligible cases, stable case ID tie-break. Ineligible foreign cases remain visible and do not block eligible domestic ones.
- Unprocessed evidence is eligible during its capture shift and the next two shifts. A case captured at shift 1 can be processed through shift 3 and expires at the beginning of shift 4. Processing removes the evidence-expiry timer; payment then resolves next shift.
- The aggregate harness uses a 90% domestic and 70% eligible foreign payment probability. A failed payment becomes closed-unpaid, not an endless retry money machine. Campaign appeals can later replace this simplified outcome.
- Fines in the early experiment are uniformly 100 cr to isolate bottlenecks. Game severity bands begin at 60/100/160 cr, with exceptional cases capped at 300. A wealthy driver Easter egg must not destroy the progression curve.

Hiring staff improves throughput and eligibility, not arbitrary fine size. Firing takes effect next shift, gives one shift's notice cost, and never enables avoiding already accrued wages. All staff are gender-neutral roles; the requested secretaries become a visible administrative team with names and small personality details.

Boundary order is fixed: resolve payments already due; expire stale unprocessed cases; apply confirmed staffing and relocation commitments and charge operations; run the traffic/capture interval; process eligible evidence up to capacity; schedule payments for the next boundary; update knowledge and opinion; offer the debrief. Campaign transfers occur after the report and before the next operations commitment. Setup pauses and menu pauses never advance a boundary.

## Yield model and forecasts

For a single site in the aggregate experiment:

```text
expected_cases = flow_per_shift × adjusted_speeding_probability
                 × coverage × evidence_quality
```

All probabilities are in [0,1]. Readability and coverage are separate to reflect a clear sensor path that still offers too little plate detail. In the eventual 3D game, individual observations determine actual cases. Do not run this aggregate multiplication on top of already simulated vehicles.

Expected collected value also depends on expiry, processing capacity, eligibility, payment delay, collection probability, and costs. The planning panel must distinguish “estimated evidence value” from “estimated collected net.” Early estimates use a visibly broad range; surveying a site narrows uncertainty without giving access to future random outcomes.

Example with 80 cars, .35 base speeding, .25 exposure, .20 knowledge, .85 coverage, .90 evidence:

`80 × .35 × (1 − .75 × .20) × (1 − .45 × .25) × .85 × .90 ≈ 16.2 cases/shift`.

At 25% foreign traffic without a specialist, roughly 12.1 domestic cases are eligible. The starter office can process only 8. Even 8 processed cases yield an expected 720 cr next shift before upkeep, not an immediate 1,620 cr. This example is a high-flow management scenario, not the starting manual-scanning income target.

## Expenses, debt, and recovery

| Expense | Starting hypothesis | Why it exists |
|---|---|---|
| Manual patrol operations | 40/shift | Keeps idle patrols from being free |
| Active fixed radar | 45/shift | Places matter even after purchase |
| Redeployment | 120 + one shift offline | Stops costless memory resets |
| Clerk | 75/shift + 100 hiring | Makes throughput an investment |
| Border specialist | 110/shift + 150 hiring | Makes border access a choice |
| Larger car operations | 65–100/shift | Fast pursuit has ongoing cost |
| Reviewable incident | 100–500 depending on severity | Makes reckless pursuit expensive |

The campaign can remain insolvent briefly: cash bottoms out at zero, unpaid costs become liabilities, and optional purchases are suspended. Do not both make cash negative and book the same unpaid cost as a liability. Later receipts settle due liabilities before becoming spendable. After two consecutive insolvent shifts offer selling an asset at 50% cost, a basic patrol assignment, or a one-time 400 cr recovery advance repaid from later collections. Never sell the last basic speed gun. An advance increases cash and liabilities equally; it cannot increase competitive score. A challenge ends with a report if insolvency persists, rather than creating an infinite loan loop. The narrower experiment uses signed cash without a separate liability account; these are alternative representations, not amounts to add together.

National “recovery” is a fictional program target of 25,000 cr transferred by shift 24, not repayment of a real country's debt. Endings respond to contribution, liabilities, public anger, and incidents. Display progress as “Recovery fund,” with the ridiculous scale mismatch acknowledged by the narrator.

## Fair scoring

The primary comparison metric is **Net public return**:

```text
score = treasury_transfers + closing_cash − opening_cash − closing_liabilities
```

All purchases, wages, fines for incidents, grants, and transfers go through the ledger. Challenges have no campaign promotion grants; any scenario grant must be part of opening cash. No residual value is awarded for unsold assets. Selling yields at most the specified resale fraction and the sale proceeds enter cash once. Pending cases and equipment list prices do not count. Negative scores are allowed.

Example: opening cash 1,000, transfers 2,000, closing cash 500, liabilities 100 gives score 1,400. Moving 300 from cash to the treasury leaves score unchanged. This prevents a transfer-button exploit.

Final active-shift cases receive a fixed **settlement stage**: process the remaining active shift normally, then resolve its already-scheduled payments once. Do not generate traffic or grant extra processing capacity after time expires. Everything still unprocessed is reported as uncollected and earns zero. The final HUD warns about the deadline before the last shift.

Public anger must remain below suspension thresholds for the run to continue. Within completed runs, rank by net public return, then lower final anger, then fewer incidents. Offer “Popular administration” as a separate achievement, not an opaque multiplier that secretly dominates revenue. Complete challenges and terminated runs appear in separate groups.

## Experiments and exploit checks

Compare a static site with rotating between two sites under the same exogenous demand seed. Look at collected net, backlog, expired evidence, and known location; do not optimize solely on ticket count. A healthy result is that rotation can beat staying when knowledge is high, but rotation every shift loses useful operating time. A stronger clerk can improve net at busy sites and cost more than it earns at quiet sites.

Later campaign sweeps must include no purchases, rush fixed radar, rush staff, pursuit-focused, safe-operation, constant rotation, and emergency recovery. Run at least 20 seeds per policy and review medians and extremes. Automated sweeps screen for dead ends; they cannot establish that an action is enjoyable.
