"""Run without app/Stripe dependencies: python -m unittest discover -s backend/scripts/tests."""
import ast
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "bootstrap_stripe_test_prices.py"
if not SCRIPT.exists():  # local isolated staging
    SCRIPT = Path(__file__).with_name("bootstrap_stripe_test_prices.py")
spec = importlib.util.spec_from_file_location("stripe_setup", SCRIPT)
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class Missing(Exception):
    code = "resource_missing"


class FakeStripe:
    def __init__(self):
        self.products, self.prices, self.writes = {}, {}, []
        self.Product = SimpleNamespace(retrieve=self.retrieve_product, create=self.create_product)
        self.Price = SimpleNamespace(list=self.list_prices, create=self.create_price)

    def retrieve_product(self, identifier):
        if identifier not in self.products:
            raise Missing()
        return self.products[identifier]

    def create_product(self, **params):
        identifier = params["id"]
        self.writes.append(("product", params))
        self.products[identifier] = {"id": identifier, "active": True, "livemode": False}
        return self.products[identifier]

    def list_prices(self, lookup_keys, limit):
        price = self.prices.get(lookup_keys[0])
        return {"data": [price] if price else [], "has_more": False}

    def create_price(self, **params):
        self.writes.append(("price", params))
        price = dict(params, id=f"price_test_{len(self.prices)}", active=True, livemode=False,
                     type="recurring", billing_scheme="per_unit")
        self.prices[params["lookup_key"]] = price
        return price


class SetupTests(unittest.TestCase):
    def test_preview_requires_no_sdk_or_key(self):
        from contextlib import redirect_stdout
        from io import StringIO
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(setup.main([]), 0)
        self.assertIn("7.99/month", output.getvalue())
        self.assertIn("149.99/year", output.getvalue())

    def test_live_and_publishable_keys_rejected_before_api_access(self):
        for key in ["", "sk_live_not_a_key", "pk_test_not_a_key", "rk_live_not_a_key", "sk_test_contains space"]:
            with self.subTest(key=key), self.assertRaises(setup.SetupError):
                setup.provision(object(), key)

    def test_create_four_prices_then_rerun_without_writes(self):
        stripe = FakeStripe()
        first = setup.provision(stripe, "sk_test_fake_local_only")
        self.assertEqual(len(first), 4)
        self.assertEqual(len(stripe.writes), 6)
        self.assertEqual(setup.provision(stripe, "sk_test_fake_local_only"), first)
        self.assertEqual(len(stripe.writes), 6)
        self.assertEqual([p["unit_amount"] for kind, p in stripe.writes if kind == "price"], [799,7999,1499,14999])
        self.assertTrue(all("idempotency_key" in p for _, p in stripe.writes))

    def test_mismatched_price_preflight_stops_all_writes(self):
        for field, value in [("unit_amount", 1), ("currency", "usd"), ("livemode", True), ("active", False), ("product", "prod_other")]:
            with self.subTest(field=field):
                stripe = FakeStripe()
                setup.provision(stripe, "sk_test_fake_local_only")
                next(iter(stripe.prices.values()))[field] = value
                stripe.writes.clear()
                with self.assertRaises(setup.SetupError):
                    setup.provision(stripe, "sk_test_fake_local_only")
                self.assertEqual(stripe.writes, [])

    def test_wrong_recurring_or_price_trial_is_rejected(self):
        for field, value in [("interval", "year"), ("interval_count", 2), ("usage_type", "metered"), ("trial_period_days", 7)]:
            stripe = FakeStripe()
            setup.provision(stripe, "sk_test_fake_local_only")
            next(iter(stripe.prices.values()))["recurring"][field] = value
            with self.subTest(field=field), self.assertRaises(setup.SetupError):
                setup.provision(stripe, "sk_test_fake_local_only")

    def test_unknown_product_error_never_creates(self):
        stripe = FakeStripe()
        def fail(identifier):
            raise RuntimeError("network error")
        stripe.Product.retrieve = fail
        with self.assertRaises(setup.SetupError):
            setup.provision(stripe, "sk_test_fake_local_only")
        self.assertEqual(stripe.writes, [])

    def test_partial_run_recovers_existing_objects(self):
        stripe = FakeStripe()
        setup.provision(stripe, "sk_test_fake_local_only")
        stripe.prices.pop(list(stripe.prices)[-1])
        stripe.writes.clear()
        self.assertEqual(len(setup.provision(stripe, "rk_test_fake_local_only")), 4)
        self.assertEqual([kind for kind, _ in stripe.writes], ["price"])

    def test_prices_match_application_catalog(self):
        catalog = SCRIPT.parents[1] / "app/services/subscription_catalog.py"
        if not catalog.exists():
            self.skipTest("Application catalog not present in isolated staging")
        tree = ast.parse(catalog.read_text())
        node = next(n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t,ast.Name) and t.id=="PRICES" for t in n.targets))
        prices = ast.literal_eval(node.value)
        self.assertEqual(setup.PRICES, {t:prices[t] for t in ("go","plus")})


if __name__ == "__main__":
    unittest.main()
