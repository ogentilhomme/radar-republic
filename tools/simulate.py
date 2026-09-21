#!/usr/bin/env python3
"""Single-camera economy experiment; not a campaign or geometry simulator."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_config(path: Path = ROOT / "data/balance.json") -> dict:
    config = json.loads(path.read_text(encoding="utf-8"))
    validate_config(config)
    return config


def validate_config(config: dict) -> None:
    if config["schema_version"] != 1:
        raise ValueError("Unsupported balance schema")
    for section in ("economy", "traffic", "awareness", "catalogue"):
        for key, value in config[section].items():
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                raise ValueError(f"Invalid nonnegative number: {section}.{key}")
            if section == "economy" and not key.endswith("probability") and not isinstance(value, int):
                raise ValueError(f"Expected integer credits or counts: {key}")
    probability_fields = {
        "economy": ("domestic_payment_probability", "foreign_payment_probability"),
        "traffic": ("base_speeding", "foreign_share"),
        "awareness": ("learning_rate", "forgetting_rate", "awareness_effect", "visual_response"),
    }
    for section, keys in probability_fields.items():
        for key in keys:
            if not 0 <= config[section][key] <= 1:
                raise ValueError(f"Probability outside [0,1]: {section}.{key}")
    for key in ("flow_per_shift", "flow_variation"):
        if not isinstance(config["traffic"][key], int):
            raise ValueError(f"Expected integer traffic count: {key}")
    if config["traffic"]["flow_variation"] > config["traffic"]["flow_per_shift"]:
        raise ValueError("Traffic variation cannot create negative flow")
    if config["economy"]["case_expiry_shifts"] < 1 or config["economy"]["payment_delay_shifts"] != 1:
        raise ValueError("Experiment requires positive expiry and one-shift payment delay")
    if not isinstance(config["shift_seconds"], int) or config["shift_seconds"] <= 0:
        raise ValueError("Shift length must be a positive integer")
    sites = config["sites"]
    if len(sites) < 2 or len({s["id"] for s in sites}) != len(sites):
        raise ValueError("Need at least two uniquely identified sites")
    for site in sites:
        if not site["corridor_id"] or not site["id"]:
            raise ValueError("Site and corridor IDs cannot be empty")
        for key in ("exposure", "coverage", "quality"):
            value = site[key]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"Invalid site probability: {site['id']}.{key}")


def draw(seed: int, *parts: object) -> float:
    """Stable keyed draws keep exogenous traffic independent of player actions."""
    key = json.dumps([seed, *parts], separators=(",", ":")).encode()
    return int.from_bytes(hashlib.sha256(key).digest()[:8], "big") / 2**64


def knowledge_step(known: float, exposure: float, active: bool, rules: dict) -> float:
    if active:
        return known + (1 - known) * rules["learning_rate"] * (0.25 + 0.75 * exposure)
    return known * (1 - rules["forgetting_rate"])


def capture_probability(config: dict, site: dict, known: float) -> float:
    rules = config["awareness"]
    return (config["traffic"]["base_speeding"]
            * (1 - rules["awareness_effect"] * known)
            * (1 - rules["visual_response"] * site["exposure"])
            * site["coverage"] * site["quality"])


def public_return(opening: int, cash: int, transfers: int = 0, liabilities: int = 0) -> int:
    return transfers + cash - opening - liabilities


@dataclass
class Case:
    case_id: str
    captured: int
    foreign: bool
    paid_roll: float
    state: str = "queued"
    due: int | None = None


def simulate(config: dict, *, seed: int = 42, shifts: int = 12,
             strategy: str = "static", clerks: int = 1, border: bool = False) -> dict:
    validate_config(config)
    if not 1 <= shifts <= 1000 or not 0 <= clerks <= 20 or strategy not in ("static", "rotate"):
        raise ValueError("Invalid experiment options")
    economy, traffic = config["economy"], config["traffic"]
    sites = config["sites"][:2]
    known = {site["corridor_id"]: 0.0 for site in sites}
    opening = economy["experiment_start_cash"]
    hiring = clerks * economy["clerk_hire"] + int(border) * economy["border_hire"]
    cash, spent, collected = opening - hiring, hiring, 0
    capacity = economy["base_capacity"] + clerks * economy["clerk_capacity"] + int(border) * economy["border_capacity"]
    cases: list[Case] = []
    rows = []
    active_index = 0

    def settle(shift: int) -> int:
        receipts = 0
        for case in cases:
            if case.state == "awaiting_payment" and case.due == shift:
                probability = economy["foreign_payment_probability" if case.foreign else "domestic_payment_probability"]
                case.state = "paid" if case.paid_roll < probability else "closed_unpaid"
                if case.state == "paid":
                    receipts += economy["experiment_fine"]
        return receipts

    for shift in range(1, shifts + 1):
        receipts = settle(shift)
        cash += receipts
        collected += receipts
        expired = 0
        for case in cases:
            if case.state == "queued" and shift - case.captured >= economy["case_expiry_shifts"]:
                case.state = "expired"
                expired += 1
        relocation = strategy == "rotate" and shift > 1 and (shift - 1) % 3 == 0
        if relocation:
            active_index = 1 - active_index
        site = sites[active_index]
        awareness_before = known[site["corridor_id"]]
        expenses = clerks * economy["clerk_wage"] + int(border) * economy["border_wage"]
        expenses += economy["relocation_cost"] if relocation else economy["fixed_upkeep"]
        cash -= expenses
        spent += expenses
        flow = traffic["flow_per_shift"] + int(draw(seed, "flow", shift) * (2 * traffic["flow_variation"] + 1)) - traffic["flow_variation"]
        captured = 0
        if not relocation:
            probability = capture_probability(config, site, awareness_before)
            for arrival in range(flow):
                if draw(seed, "capture", shift, arrival) < probability:
                    cases.append(Case(
                        f"{shift}:{arrival}", shift,
                        draw(seed, "foreign", shift, arrival) < traffic["foreign_share"],
                        draw(seed, "payment", shift, arrival)))
                    captured += 1
        remaining, processed = capacity, 0
        for case in cases:  # insertion order is capture age, then stable arrival ID
            if case.state != "queued" or (case.foreign and not border):
                continue
            cost = 2 if case.foreign else 1
            if cost <= remaining:
                remaining -= cost
                processed += 1
                case.state = "awaiting_payment"
                case.due = shift + economy["payment_delay_shifts"]
        for corridor in known:
            active = not relocation and corridor == site["corridor_id"]
            known[corridor] = knowledge_step(known[corridor], site["exposure"], active, config["awareness"])
        rows.append({
            "shift": shift, "site": site["id"], "offline": relocation,
            "knowledge": round(awareness_before, 4), "flow": flow,
            "captured": captured, "processed": processed, "work_used": capacity - remaining,
            "receipts": receipts, "expenses": expenses, "expired": expired,
            "queued": sum(c.state == "queued" for c in cases), "cash": cash,
        })
    settlement = settle(shifts + 1)
    cash += settlement
    collected += settlement
    states = {state: sum(c.state == state for c in cases)
              for state in ("queued", "awaiting_payment", "paid", "closed_unpaid", "expired")}
    return {
        "scope": "single owned fixed radar; illustrative aggregate experiment",
        "balance_version": config["balance_version"],
        "balance_hash": hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()[:16],
        "seed": seed, "shifts": shifts, "strategy": strategy, "clerks": clerks, "border": border,
        "opening_cash": opening, "hiring_cost": hiring, "collected": collected,
        "spent": spent, "closing_cash": cash, "net_return": public_return(opening, cash),
        "settlement_receipts": settlement, "cases_created": len(cases), "case_states": states,
        "knowledge": known, "rows": rows,
        "limits": "No 3D, campaign purchases, pursuits, public opinion, transfers, or insolvency suspension.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--shifts", type=int, default=12)
    parser.add_argument("--strategy", choices=("static", "rotate"), default="static")
    parser.add_argument("--clerks", type=int, default=1)
    parser.add_argument("--border", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = simulate(load_config(), seed=args.seed, shifts=args.shifts,
                          strategy=args.strategy, clerks=args.clerks, border=args.border)
    except ValueError as error:
        parser.error(str(error))
    if args.json:
        print(json.dumps(result, indent=2))
        return
    print(f"Economy experiment | {result['strategy']} | seed {result['seed']} | {result['balance_version']}")
    print("shift site              known  cases processed queued receipts expenses cash")
    for row in result["rows"]:
        site = "SETUP" if row["offline"] else row["site"]
        print(f"{row['shift']:>5} {site:<17} {row['knowledge']:>5.0%} {row['captured']:>5} "
              f"{row['processed']:>9} {row['queued']:>6} {row['receipts']:>8} {row['expenses']:>8} {row['cash']:>6}")
    print(f"Settlement: {result['settlement_receipts']} cr | Collected: {result['collected']} cr | Costs: {result['spent']} cr")
    print(f"Net return: {result['net_return']} cr | Closing cash: {result['closing_cash']} cr | Cases: {result['case_states']}")
    print(result["limits"])


if __name__ == "__main__":
    main()
