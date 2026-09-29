"""
CardFlow — Predictive Models & Simulations
Generates simulation data for Visa QR Pay adoption, cannibalization, and ROI projections.
"""
import json
import numpy as np
import os

np.random.seed(42)
MONTHS = 36  # 3-year projection

# ═══════════════════════════════════════════════════════════════════════════
# MODEL 1: QR Pay Adoption S-Curve (Bass Diffusion Model)
# ═══════════════════════════════════════════════════════════════════════════
# Bass diffusion: F(t) = (1 - e^(-(p+q)*t)) / (1 + (q/p)*e^(-(p+q)*t))
# p = innovation coefficient (external influence — marketing)
# q = imitation coefficient (internal influence — word of mouth)

def bass_diffusion(p, q, m, T):
    """Bass diffusion model. m = total addressable market."""
    adopters = []
    cum = 0
    for t in range(1, T + 1):
        if cum >= m:
            adopters.append(0)
            continue
        new = (p + q * cum / m) * (m - cum)
        new = min(new, m - cum)
        cum += new
        adopters.append(new)
    return np.array(adopters), np.cumsum(adopters)

# Three scenarios for QR Pay adoption among Polish Visa cardholders
# Total addressable: ~8M Visa cards in Poland (est. from 45.2M total cards, Visa ~55% share ≈ 25M, active ~8M)
TAM_CARDS = 8_000_000

scenarios_adoption = {}
params = {
    "Conservative": {"p": 0.005, "q": 0.08, "label": "Slow start, limited marketing"},
    "Base":         {"p": 0.012, "q": 0.15, "label": "Moderate push, bank partnerships"},
    "Optimistic":   {"p": 0.025, "q": 0.25, "label": "Aggressive launch, viral adoption"},
}

for name, cfg in params.items():
    new_adopters, cum_adopters = bass_diffusion(cfg["p"], cfg["q"], TAM_CARDS, MONTHS)
    scenarios_adoption[name] = {
        "monthly_new": new_adopters.tolist(),
        "cumulative": cum_adopters.tolist(),
        "params": cfg,
        "penetration_pct": (cum_adopters / TAM_CARDS * 100).tolist(),
    }

# ═══════════════════════════════════════════════════════════════════════════
# MODEL 2: Transaction Volume Projection (per adopter activity model)
# ═══════════════════════════════════════════════════════════════════════════
# Assumptions per active user per month:
#   P2P: 2-4 tx/month (avg 80 PLN) — based on BLIK P2P patterns
#   E-commerce: 1-3 tx/month (avg 250 PLN) — from our Visa data
#   Services: 0.3-0.5 tx/month (avg 150 PLN) — plumber, tutor, etc.

activity_params = {
    "Conservative": {"p2p_tx": 1.5, "p2p_avg": 70, "ecom_tx": 0.8, "ecom_avg": 200, "svc_tx": 0.2, "svc_avg": 120, "active_rate": 0.4},
    "Base":         {"p2p_tx": 2.5, "p2p_avg": 80, "ecom_tx": 1.5, "ecom_avg": 250, "svc_tx": 0.3, "svc_avg": 150, "active_rate": 0.55},
    "Optimistic":   {"p2p_tx": 4.0, "p2p_avg": 90, "ecom_tx": 2.5, "ecom_avg": 280, "svc_tx": 0.5, "svc_avg": 180, "active_rate": 0.7},
}

scenarios_volume = {}
for name in ["Conservative", "Base", "Optimistic"]:
    adopt = np.array(scenarios_adoption[name]["cumulative"])
    ap = activity_params[name]
    active_users = adopt * ap["active_rate"]

    p2p_tx = active_users * ap["p2p_tx"]
    p2p_val = p2p_tx * ap["p2p_avg"]
    ecom_tx = active_users * ap["ecom_tx"]
    ecom_val = ecom_tx * ap["ecom_avg"]
    svc_tx = active_users * ap["svc_tx"]
    svc_val = svc_tx * ap["svc_avg"]

    total_tx = p2p_tx + ecom_tx + svc_tx
    total_val = p2p_val + ecom_val + svc_val

    scenarios_volume[name] = {
        "active_users": active_users.tolist(),
        "p2p_tx_monthly": p2p_tx.tolist(),
        "p2p_val_monthly": p2p_val.tolist(),
        "ecom_tx_monthly": ecom_tx.tolist(),
        "ecom_val_monthly": ecom_val.tolist(),
        "svc_tx_monthly": svc_tx.tolist(),
        "svc_val_monthly": svc_val.tolist(),
        "total_tx_monthly": total_tx.tolist(),
        "total_val_monthly": total_val.tolist(),
        "cumulative_tx": np.cumsum(total_tx).tolist(),
        "cumulative_val": np.cumsum(total_val).tolist(),
    }

# ═══════════════════════════════════════════════════════════════════════════
# MODEL 3: BLIK Cannibalization Model
# ═══════════════════════════════════════════════════════════════════════════
# How much of QR Pay volume comes FROM BLIK vs NEW card volume?
# Assumptions: P2P mostly cannibalizes BLIK, E-com partially, Services = net new

cannibalization = {}
cannibal_rates = {
    "Conservative": {"p2p_from_blik": 0.70, "ecom_from_blik": 0.40, "svc_from_cash": 0.80},
    "Base":         {"p2p_from_blik": 0.60, "ecom_from_blik": 0.35, "svc_from_cash": 0.85},
    "Optimistic":   {"p2p_from_blik": 0.50, "ecom_from_blik": 0.30, "svc_from_cash": 0.90},
}

for name in ["Conservative", "Base", "Optimistic"]:
    sv = scenarios_volume[name]
    cr = cannibal_rates[name]

    # P2P: X% from BLIK, rest from cash/transfer
    p2p_from_blik = np.array(sv["p2p_val_monthly"]) * cr["p2p_from_blik"]
    p2p_from_cash = np.array(sv["p2p_val_monthly"]) * (1 - cr["p2p_from_blik"])

    # E-com: X% from BLIK, rest from cash-on-delivery + new
    ecom_from_blik = np.array(sv["ecom_val_monthly"]) * cr["ecom_from_blik"]
    ecom_new = np.array(sv["ecom_val_monthly"]) * (1 - cr["ecom_from_blik"])

    # Services: X% from cash (net new to card ecosystem)
    svc_from_cash = np.array(sv["svc_val_monthly"]) * cr["svc_from_cash"]
    svc_existing = np.array(sv["svc_val_monthly"]) * (1 - cr["svc_from_cash"])

    net_new_to_visa = p2p_from_cash + ecom_new + svc_from_cash
    from_blik = p2p_from_blik + ecom_from_blik
    total = np.array(sv["total_val_monthly"])

    cannibalization[name] = {
        "from_blik_monthly": from_blik.tolist(),
        "net_new_monthly": net_new_to_visa.tolist(),
        "from_existing_card": svc_existing.tolist(),
        "total_monthly": total.tolist(),
        "net_new_pct": (net_new_to_visa / np.maximum(total, 1) * 100).tolist(),
        "from_blik_pct": (from_blik / np.maximum(total, 1) * 100).tolist(),
        "cumulative_net_new": np.cumsum(net_new_to_visa).tolist(),
        "cumulative_from_blik": np.cumsum(from_blik).tolist(),
    }

# ═══════════════════════════════════════════════════════════════════════════
# MODEL 4: Revenue & ROI Model
# ═══════════════════════════════════════════════════════════════════════════
# Visa earns ~0.13-0.15% of transaction value (interchange share, network fees)
# Visa Direct: ~0.5% fee on P2P transfers

revenue = {}
costs = {
    "development": 5_000_000,       # Platform development
    "bank_integration": 3_000_000,  # Integration with Polish banks
    "marketing_y1": 8_000_000,      # Year 1 marketing
    "marketing_y2": 5_000_000,      # Year 2
    "marketing_y3": 3_000_000,      # Year 3
    "qr_stickers": 2_000_000,       # Physical QR stickers for existing cards
    "operations_annual": 2_000_000, # Annual ops
    "total_3yr": 5_000_000 + 3_000_000 + 8_000_000 + 5_000_000 + 3_000_000 + 2_000_000 + 6_000_000
}

for name in ["Conservative", "Base", "Optimistic"]:
    sv = scenarios_volume[name]

    # Revenue per transaction type
    p2p_rev = np.array(sv["p2p_val_monthly"]) * 0.005   # 0.5% Visa Direct fee
    ecom_rev = np.array(sv["ecom_val_monthly"]) * 0.0015  # 0.15% network fee
    svc_rev = np.array(sv["svc_val_monthly"]) * 0.005   # 0.5% (treated as P2P-like)

    monthly_rev = p2p_rev + ecom_rev + svc_rev
    cumulative_rev = np.cumsum(monthly_rev)

    # Monthly costs
    monthly_costs = np.zeros(MONTHS)
    monthly_costs[0] = costs["development"] + costs["bank_integration"] + costs["qr_stickers"]  # upfront
    for m in range(MONTHS):
        monthly_costs[m] += costs["operations_annual"] / 12
        if m < 12:
            monthly_costs[m] += costs["marketing_y1"] / 12
        elif m < 24:
            monthly_costs[m] += costs["marketing_y2"] / 12
        else:
            monthly_costs[m] += costs["marketing_y3"] / 12

    cumulative_costs = np.cumsum(monthly_costs)
    cumulative_profit = cumulative_rev - cumulative_costs
    monthly_profit = monthly_rev - monthly_costs

    # Find break-even month
    breakeven = None
    for i in range(MONTHS):
        if cumulative_profit[i] > 0:
            breakeven = i + 1
            break

    revenue[name] = {
        "monthly_revenue": monthly_rev.tolist(),
        "monthly_costs": monthly_costs.tolist(),
        "monthly_profit": monthly_profit.tolist(),
        "cumulative_revenue": cumulative_rev.tolist(),
        "cumulative_costs": cumulative_costs.tolist(),
        "cumulative_profit": cumulative_profit.tolist(),
        "breakeven_month": breakeven,
        "total_3yr_revenue": float(cumulative_rev[-1]),
        "total_3yr_cost": float(cumulative_costs[-1]),
        "total_3yr_profit": float(cumulative_profit[-1]),
        "roi_pct": float(cumulative_profit[-1] / cumulative_costs[-1] * 100) if cumulative_costs[-1] > 0 else 0,
        "p2p_rev": p2p_rev.tolist(),
        "ecom_rev": ecom_rev.tolist(),
        "svc_rev": svc_rev.tolist(),
    }

# ═══════════════════════════════════════════════════════════════════════════
# MODEL 5: E-Commerce Market Share Simulation
# ═══════════════════════════════════════════════════════════════════════════
# Simulate how QR Pay changes the card vs BLIK share in e-commerce

ecom_share = {}
# Total e-commerce market grows ~8% per year
ecom_base_monthly_pln = 65_000_000_000 / 12  # ~5.4B PLN/month

for name in ["Conservative", "Base", "Optimistic"]:
    sv = scenarios_volume[name]
    ecom_qr = np.array(sv["ecom_val_monthly"])

    market_growth = np.array([(1.08 ** (m/12)) for m in range(MONTHS)])
    monthly_market = ecom_base_monthly_pln * market_growth

    # Current shares (monthly PLN)
    blik_base = monthly_market * 0.67
    card_base = monthly_market * 0.16 * 0.55  # Visa's ~55% of card
    transfer_base = monthly_market * 0.10
    cod_base = monthly_market * 0.05
    other_base = monthly_market * 0.02

    # QR Pay cannibalizes some from BLIK, some from COD, grows the pie
    cr = cannibal_rates[name]
    qr_from_blik = ecom_qr * cr["ecom_from_blik"]
    qr_net_new = ecom_qr * (1 - cr["ecom_from_blik"])

    visa_total = card_base + ecom_qr
    blik_adjusted = blik_base - qr_from_blik
    market_adjusted = monthly_market + qr_net_new * 0.3  # some net new expands market

    visa_share = visa_total / market_adjusted * 100
    blik_share = blik_adjusted / market_adjusted * 100

    ecom_share[name] = {
        "visa_share_pct": visa_share.tolist(),
        "blik_share_pct": blik_share.tolist(),
        "visa_base_share": (card_base / monthly_market * 100).tolist(),
        "monthly_market_pln": market_adjusted.tolist(),
    }

# ═══════════════════════════════════════════════════════════════════════════
# MODEL 6: Sensitivity Analysis
# ═══════════════════════════════════════════════════════════════════════════
# What-if: vary key parameters and measure impact on 3-year revenue

sensitivity = []
base_ap = activity_params["Base"]
base_param = params["Base"]

# Vary each parameter ±30%
for param_name, base_val, mult_range in [
    ("P2P TX per user/month", base_ap["p2p_tx"], [0.5, 0.7, 1.0, 1.3, 1.5]),
    ("E-com TX per user/month", base_ap["ecom_tx"], [0.5, 0.7, 1.0, 1.3, 1.5]),
    ("Avg P2P amount (PLN)", base_ap["p2p_avg"], [0.5, 0.7, 1.0, 1.3, 1.5]),
    ("Active user rate", base_ap["active_rate"], [0.5, 0.7, 1.0, 1.3, 1.5]),
    ("Bass q (virality)", base_param["q"], [0.5, 0.7, 1.0, 1.3, 1.5]),
]:
    for mult in mult_range:
        val = base_val * mult

        # Recalculate with modified param
        ap_mod = dict(base_ap)
        bp_mod = dict(base_param)

        if "TX per user" in param_name and "P2P" in param_name:
            ap_mod["p2p_tx"] = val
        elif "TX per user" in param_name and "E-com" in param_name:
            ap_mod["ecom_tx"] = val
        elif "amount" in param_name:
            ap_mod["p2p_avg"] = val
        elif "Active" in param_name:
            ap_mod["active_rate"] = val
        elif "virality" in param_name:
            bp_mod["q"] = val

        _, cum_a = bass_diffusion(bp_mod["p"], bp_mod["q"], TAM_CARDS, MONTHS)
        active = cum_a * ap_mod["active_rate"]
        p2p_v = active * ap_mod["p2p_tx"] * ap_mod["p2p_avg"]
        ecom_v = active * ap_mod["ecom_tx"] * ap_mod["ecom_avg"]
        svc_v = active * ap_mod["svc_tx"] * ap_mod["svc_avg"]
        total_v = p2p_v + ecom_v + svc_v
        rev_3yr = np.sum(p2p_v * 0.005 + ecom_v * 0.0015 + svc_v * 0.005)

        sensitivity.append({
            "parameter": param_name,
            "multiplier": mult,
            "value": round(val, 2),
            "revenue_3yr_mln": round(rev_3yr / 1e6, 2),
        })

# ═══════════════════════════════════════════════════════════════════════════
# SAVE ALL MODELS
# ═══════════════════════════════════════════════════════════════════════════
output = {
    "adoption": scenarios_adoption,
    "volume": scenarios_volume,
    "cannibalization": cannibalization,
    "revenue": revenue,
    "ecom_share": ecom_share,
    "sensitivity": sensitivity,
    "costs": costs,
    "assumptions": {
        "tam_cards": TAM_CARDS,
        "months": MONTHS,
        "adoption_params": params,
        "activity_params": activity_params,
        "cannibal_rates": cannibal_rates,
        "ecom_base_monthly_pln": ecom_base_monthly_pln,
    },
}

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_results.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("=== MODEL RESULTS ===")
for name in ["Conservative", "Base", "Optimistic"]:
    a = scenarios_adoption[name]
    v = scenarios_volume[name]
    r = revenue[name]
    print(f"\n--- {name} ---")
    print(f"  Adopters Y1: {a['cumulative'][11]:,.0f}  Y2: {a['cumulative'][23]:,.0f}  Y3: {a['cumulative'][35]:,.0f}")
    print(f"  Penetration Y3: {a['penetration_pct'][35]:.1f}%")
    print(f"  Active users Y3: {v['active_users'][35]:,.0f}")
    print(f"  Monthly TX Y3: {v['total_tx_monthly'][35]:,.0f}")
    print(f"  Monthly value Y3: {v['total_val_monthly'][35]:,.0f} PLN")
    print(f"  3Y cumulative TX: {v['cumulative_tx'][35]:,.0f}")
    print(f"  3Y cumulative value: {v['cumulative_val'][35]:,.0f} PLN")
    print(f"  3Y revenue: {r['total_3yr_revenue']:,.0f} PLN")
    print(f"  3Y cost: {r['total_3yr_cost']:,.0f} PLN")
    print(f"  3Y profit: {r['total_3yr_profit']:,.0f} PLN")
    print(f"  ROI: {r['roi_pct']:.0f}%")
    print(f"  Break-even month: {r['breakeven_month']}")

print("\nDONE — saved to model_results.json")
