#!/usr/bin/env python3
"""Provision JUBA LISAN test products/prices; default is a no-network preview."""
import argparse
import os
import sys

PRICES = {"go": {"monthly": 799, "yearly": 7999}, "plus": {"monthly": 1499, "yearly": 14999}}
INTERVALS = {"monthly": "month", "yearly": "year"}


class SetupError(Exception):
    pass


def specifications():
    for tier, amounts in PRICES.items():
        for interval, amount in amounts.items():
            yield {
                "tier": tier, "interval": interval, "amount": amount,
                "product": f"juba_lisan_{tier}_test_v1",
                "lookup_key": f"juba_lisan_{tier}_{interval}_eur_{amount}_test_v1",
                "env": f"STRIPE_PRICE_{tier.upper()}_{interval.upper()}",
            }


def validate_key(key):
    # Restricted test keys also work if Products/Prices read+write are permitted.
    if not key or not key.startswith(("sk_test_", "rk_test_")) or any(c.isspace() for c in key):
        raise SetupError("Use a test secret key via STRIPE_SECRET_KEY; live/publishable keys are refused.")
    return key


def validate_product(product, identifier):
    if (product.get("id") != identifier or product.get("livemode") is not False
            or product.get("active") is not True):
        raise SetupError("Existing product is not an active test product; no changes were made to it.")


def validate_price(price, spec):
    recurring = price.get("recurring") or {}
    product = price.get("product")
    if isinstance(product, dict):
        product = product.get("id")
    if not (
        isinstance(price.get("id"), str) and price["id"].startswith("price_")
        and price.get("livemode") is False and price.get("active") is True
        and price.get("currency") == "eur" and price.get("unit_amount") == spec["amount"]
        and price.get("type") == "recurring" and price.get("billing_scheme") == "per_unit"
        and price.get("lookup_key") == spec["lookup_key"] and product == spec["product"]
        and recurring.get("interval") == INTERVALS[spec["interval"]]
        and recurring.get("interval_count") == 1 and recurring.get("usage_type") == "licensed"
        and recurring.get("trial_period_days") is None
        and price.get("transform_quantity") is None
    ):
        raise SetupError(f"Price conflict for {spec['env']}; existing prices are never modified or archived.")


def provision(stripe, key):
    """Preflight everything before writes. Reruns reuse stable IDs/lookup keys.

    Network timeouts may leave some objects created. Rerun with the same account
    and key: never rotate identifiers or silently replace an incompatible price.
    """
    stripe.api_key = validate_key(key)
    stripe.max_network_retries = 2
    products, existing = {}, {}
    specs = list(specifications())
    for tier in PRICES:
        identifier = f"juba_lisan_{tier}_test_v1"
        try:
            product = stripe.Product.retrieve(identifier)
        except Exception as exc:
            # Only the SDK's structured missing-resource code permits creation.
            if getattr(exc, "code", None) != "resource_missing":
                raise SetupError("Product lookup failed; check test account, permissions and connectivity.") from None
            product = None
        if product is not None:
            validate_product(product, identifier)
        products[tier] = product
    for spec in specs:
        matches = stripe.Price.list(lookup_keys=[spec["lookup_key"]], limit=2)
        data = matches.get("data", [])
        if matches.get("has_more") or len(data) > 1:
            raise SetupError("Ambiguous price lookup; resolve the conflict in the test dashboard.")
        if data:
            validate_price(data[0], spec)
            existing[spec["env"]] = data[0]
    for tier, product in products.items():
        if product is None:
            identifier = f"juba_lisan_{tier}_test_v1"
            product = stripe.Product.create(
                id=identifier, name=f"JUBA LISAN {tier.title()}",
                metadata={"application": "juba_lisan", "tier": tier, "setup_version": "1"},
                idempotency_key=f"juba-test-product-v1-{tier}",
            )
            validate_product(product, identifier)
    result = {}
    for spec in specs:
        price = existing.get(spec["env"])
        if price is None:
            price = stripe.Price.create(
                product=spec["product"], currency="eur", unit_amount=spec["amount"],
                recurring={"interval": INTERVALS[spec["interval"]], "interval_count": 1, "usage_type": "licensed"},
                lookup_key=spec["lookup_key"],
                metadata={"application": "juba_lisan", "tier": spec["tier"], "setup_version": "1"},
                idempotency_key=spec["lookup_key"],
            )
            validate_price(price, spec)
        result[spec["env"]] = price["id"]
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Create/reuse two products and four prices in Stripe TEST mode.")
    args = parser.parse_args(argv)
    if not args.apply:
        for spec in specifications():
            print(f"{spec['env']}: EUR {spec['amount'] / 100:.2f}/{INTERVALS[spec['interval']]} (TEST)")
        print("Preview only. Set STRIPE_SECRET_KEY securely and pass --apply to provision.")
        return 0
    try:
        key = validate_key(os.environ.get("STRIPE_SECRET_KEY", ""))
        import stripe
        result = provision(stripe, key)
    except SetupError as exc:
        print(f"Setup stopped: {exc}", file=sys.stderr)
        return 1
    except ImportError:
        print("Install backend/requirements.txt in your backend environment first.", file=sys.stderr)
        return 1
    except Exception:
        # Never print SDK exceptions: they can contain request details or secrets.
        print("Stripe setup failed. Some test objects may exist; rerun with the same account. No keys were printed.", file=sys.stderr)
        return 1
    for name, identifier in result.items():
        print(f"{name}={identifier}")
    print("Test prices verified. No subscriptions or charges were created. Restart the test backend after configuration.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
