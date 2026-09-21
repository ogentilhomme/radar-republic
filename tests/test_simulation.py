import copy
import unittest

from tools.simulate import capture_probability, knowledge_step, load_config, public_return, simulate, validate_config


class EconomyContractTests(unittest.TestCase):
    def setUp(self):
        self.config = load_config()

    def test_blocked_sensor_never_captures_even_when_hidden(self):
        self.assertEqual(capture_probability(self.config, self.config["sites"][2], 0), 0)

    def test_knowledge_reduces_yield_without_annihilating_visitors(self):
        site = self.config["sites"][0]
        fresh = capture_probability(self.config, site, 0)
        known = capture_probability(self.config, site, 1)
        self.assertGreater(known, 0)
        self.assertLess(known, fresh)

    def test_learning_and_forgetting_stay_bounded(self):
        for active in (True, False):
            for exposure in (0, 0.5, 1):
                value = 0.5
                for _ in range(1000):
                    value = knowledge_step(value, exposure, active, self.config["awareness"])
                    self.assertTrue(0 <= value <= 1)
                self.assertGreater(value, 0.5) if active else self.assertLess(value, 0.5)

    def test_cash_conservation_and_cases_have_one_terminal_or_pending_state(self):
        for seed in range(20):
            for strategy in ("static", "rotate"):
                result = simulate(self.config, seed=seed, strategy=strategy)
                self.assertEqual(result["closing_cash"], result["opening_cash"] + result["collected"] - result["spent"])
                self.assertEqual(result["net_return"], result["collected"] - result["spent"])
                self.assertEqual(result["cases_created"], sum(result["case_states"].values()))
                self.assertEqual(result["collected"], result["case_states"]["paid"] * self.config["economy"]["experiment_fine"])
                self.assertEqual(result["case_states"]["awaiting_payment"], 0)

    def test_seed_is_repeatable_and_demand_independent_of_strategy(self):
        static = simulate(self.config, seed=17)
        self.assertEqual(static, simulate(self.config, seed=17))
        rotate = simulate(self.config, seed=17, strategy="rotate")
        self.assertEqual([r["flow"] for r in static["rows"]], [r["flow"] for r in rotate["rows"]])

    def test_relocation_has_full_shift_downtime_and_cost(self):
        result = simulate(self.config, strategy="rotate")
        offline = [r for r in result["rows"] if r["offline"]]
        self.assertEqual([r["shift"] for r in offline], [4, 7, 10])
        for row in offline:
            self.assertEqual(row["captured"], 0)
            self.assertEqual(row["expenses"], 195)

    def test_same_corridor_move_preserves_memory(self):
        config = copy.deepcopy(self.config)
        config["sites"][1]["corridor_id"] = config["sites"][0]["corridor_id"]
        result = simulate(config, strategy="rotate", shifts=5)
        self.assertGreater(result["rows"][4]["knowledge"], 0)

    def test_queue_uses_work_units_and_expires(self):
        config = copy.deepcopy(self.config)
        config["traffic"].update(base_speeding=1, foreign_share=0, flow_per_shift=100, flow_variation=0)
        for site in config["sites"][:2]:
            site.update(exposure=0, coverage=1, quality=1)
        result = simulate(config, clerks=0, shifts=4)
        self.assertTrue(all(row["work_used"] <= 8 for row in result["rows"]))
        self.assertEqual(result["rows"][2]["expired"], 0)
        self.assertGreater(result["rows"][3]["expired"], 0)

    def test_foreign_cases_need_specialist_and_two_units(self):
        config = copy.deepcopy(self.config)
        config["traffic"].update(foreign_share=1, base_speeding=1, flow_per_shift=100, flow_variation=0)
        without = simulate(config, clerks=0, shifts=4)
        self.assertEqual(without["collected"], 0)
        with_border = simulate(config, clerks=0, border=True, shifts=4)
        self.assertGreater(with_border["collected"], 0)
        for row in with_border["rows"]:
            self.assertEqual(row["work_used"], 2 * row["processed"])
            self.assertLessEqual(row["work_used"], 20)

    def test_settlement_pays_processed_cases_without_extra_processing(self):
        config = copy.deepcopy(self.config)
        config["traffic"].update(foreign_share=0, base_speeding=1, flow_per_shift=100, flow_variation=0)
        config["economy"]["domestic_payment_probability"] = 1
        result = simulate(config, clerks=0, shifts=1)
        self.assertEqual(result["rows"][0]["receipts"], 0)
        self.assertEqual(result["settlement_receipts"], 800)
        self.assertGreater(result["case_states"]["queued"], 0)

    def test_treasury_transfers_do_not_multiply_score(self):
        self.assertEqual(public_return(1000, 500, 2000, 100), 1400)
        self.assertEqual(public_return(1000, 500, 2000, 100), public_return(1000, 200, 2300, 100))
        self.assertEqual(public_return(1000, 500), -500)

    def test_invalid_inputs_are_rejected(self):
        for invalid in (-0.1, 1.1, float("nan")):
            config = copy.deepcopy(self.config)
            config["sites"][0]["exposure"] = invalid
            with self.assertRaises(ValueError):
                validate_config(config)
        with self.assertRaises(ValueError):
            simulate(self.config, shifts=0)


if __name__ == "__main__":
    unittest.main()
