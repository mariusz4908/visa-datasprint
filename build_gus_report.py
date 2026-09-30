import json, os
ROOT = os.path.dirname(os.path.abspath(__file__))  # repository root, where the JSON results live

# Load data
with open(os.path.join(ROOT, "geo_results.json"), "r", encoding="utf-8") as f:
    geo = json.load(f)
with open(os.path.join(ROOT, "gus_data.json"), "r", encoding="utf-8") as f:
    gus = json.load(f)

postal_to_woj = gus["postal_to_woj_mapping"]
woj_pop = gus["population_woj"]

# --- Aggregate cardholder postal prefix data to województwa ---
woj_card_data = {}
for row in geo["by_postal_prefix"]:
    prefix = row["postal_prefix"]
    if prefix and prefix in postal_to_woj:
        woj = postal_to_woj[prefix]
        if woj not in woj_card_data:
            woj_card_data[woj] = {"tx_count": 0, "unique_cards": 0, "total_amount": 0, "card_sets": []}
        woj_card_data[woj]["tx_count"] += row["tx_count"]
        woj_card_data[woj]["unique_cards"] += row["unique_cards"]
        woj_card_data[woj]["total_amount"] += row["total_amount"]

# --- Aggregate merchant postal prefix data to województwa ---
woj_merchant_data = {}
for row in geo["by_merchant_postal"]:
    prefix = row["mrch_postal_prefix"]
    if prefix and len(prefix) == 2 and prefix in postal_to_woj:
        woj = postal_to_woj[prefix]
        if woj not in woj_merchant_data:
            woj_merchant_data[woj] = {"tx_count": 0, "total_amount": 0, "unique_merchants": 0, "unique_cards": 0}
        woj_merchant_data[woj]["tx_count"] += row["tx_count"]
        woj_merchant_data[woj]["total_amount"] += row["total_amount"]
        woj_merchant_data[woj]["unique_merchants"] += row["unique_merchants"]
        woj_merchant_data[woj]["unique_cards"] += row["unique_cards"]

# --- Build per-województwo analysis ---
woj_analysis = []
for woj_name, pop_data in woj_pop.items():
    pop = pop_data["population"]
    card = woj_card_data.get(woj_name, {"tx_count": 0, "unique_cards": 0, "total_amount": 0})
    merch = woj_merchant_data.get(woj_name, {"tx_count": 0, "total_amount": 0, "unique_merchants": 0, "unique_cards": 0})

    # Card penetration = unique cards / population (approximate, limited by data)
    cards_per_1000 = round(card["unique_cards"] / pop * 1000, 2) if pop > 0 else 0
    tx_per_capita = round(card["tx_count"] / pop, 2) if pop > 0 else 0
    spend_per_capita = round(card["total_amount"] / pop, 2) if pop > 0 else 0

    # Merchant density
    merch_tx_per_capita = round(merch["tx_count"] / pop, 2) if pop > 0 else 0
    merch_per_10k = round(merch.get("unique_merchants", 0) / pop * 10000, 2) if pop > 0 else 0

    woj_analysis.append({
        "name": woj_name,
        "population": pop,
        "unique_cards": card["unique_cards"],
        "cards_per_1000": cards_per_1000,
        "tx_count": card["tx_count"],
        "tx_per_capita": tx_per_capita,
        "total_amount": card["total_amount"],
        "spend_per_capita": spend_per_capita,
        "merch_tx_count": merch["tx_count"],
        "merch_tx_per_capita": merch_tx_per_capita,
        "unique_merchants": merch.get("unique_merchants", 0),
        "merch_per_10k": merch_per_10k,
    })

# Sort by cards_per_1000 for ranking
woj_analysis.sort(key=lambda x: x["cards_per_1000"], reverse=True)

# Calculate national averages
total_pop = sum(w["population"] for w in woj_analysis)
total_cards = sum(w["unique_cards"] for w in woj_analysis)
total_tx = sum(w["tx_count"] for w in woj_analysis)
total_amount = sum(w["total_amount"] for w in woj_analysis)
total_merchants = sum(w["unique_merchants"] for w in woj_analysis)

nat_cards_per_1000 = round(total_cards / total_pop * 1000, 2)
nat_tx_per_capita = round(total_tx / total_pop, 2)
nat_spend_per_capita = round(total_amount / total_pop, 2)
nat_merch_per_10k = round(total_merchants / total_pop * 10000, 2)

# --- FUA analysis ---
fua_data = geo["by_fua"]

# --- Mobility / cross-region flow analysis ---
flow_data = geo["cardholder_vs_merchant_region"]

# Aggregate flows to województwo level
woj_flow = {}
for row in flow_data:
    card_prefix = row["card_region"]
    mrch_prefix = row["mrch_region"]
    if card_prefix in postal_to_woj and mrch_prefix in postal_to_woj:
        card_woj = postal_to_woj[card_prefix]
        mrch_woj = postal_to_woj[mrch_prefix]
        key = (card_woj, mrch_woj)
        if key not in woj_flow:
            woj_flow[key] = {"tx_count": 0, "total_amount": 0}
        woj_flow[key]["tx_count"] += row["tx_count"]
        woj_flow[key]["total_amount"] += row["total_amount"]

# Calculate % of local vs outgoing transactions per woj
woj_mobility = {}
for (card_woj, mrch_woj), data in woj_flow.items():
    if card_woj not in woj_mobility:
        woj_mobility[card_woj] = {"local": 0, "outgoing": 0, "total": 0}
    woj_mobility[card_woj]["total"] += data["tx_count"]
    if card_woj == mrch_woj:
        woj_mobility[card_woj]["local"] += data["tx_count"]
    else:
        woj_mobility[card_woj]["outgoing"] += data["tx_count"]

for woj in woj_mobility:
    total = woj_mobility[woj]["total"]
    woj_mobility[woj]["local_pct"] = round(woj_mobility[woj]["local"] / total * 100, 1) if total else 0
    woj_mobility[woj]["outgoing_pct"] = round(woj_mobility[woj]["outgoing"] / total * 100, 1) if total else 0

# --- Compile output ---
output = {
    "woj_analysis": woj_analysis,
    "national_avg": {
        "cards_per_1000": nat_cards_per_1000,
        "tx_per_capita": nat_tx_per_capita,
        "spend_per_capita": nat_spend_per_capita,
        "merch_per_10k": nat_merch_per_10k,
        "total_pop": total_pop,
        "total_cards": total_cards,
    },
    "fua_data": fua_data,
    "woj_mobility": {k: v for k, v in woj_mobility.items()},
    "top_inflows": [],
}

# Top inflows (which woj attracts most external card transactions)
woj_inflow = {}
for (card_woj, mrch_woj), data in woj_flow.items():
    if card_woj != mrch_woj:
        if mrch_woj not in woj_inflow:
            woj_inflow[mrch_woj] = 0
        woj_inflow[mrch_woj] += data["tx_count"]

output["woj_inflow"] = dict(sorted(woj_inflow.items(), key=lambda x: x[1], reverse=True))

with open(os.path.join(ROOT, "gus_cross_analysis.json"), "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("=== RANKING WOJ by cards_per_1000 ===")
for i, w in enumerate(woj_analysis):
    gap = round(((nat_cards_per_1000 - w["cards_per_1000"]) / nat_cards_per_1000) * 100, 1)
    print(f"{i+1:2}. {w['name']:25s} pop={w['population']:>10,}  cards/1000={w['cards_per_1000']:>7.2f}  tx/cap={w['tx_per_capita']:>7.2f}  spend/cap={w['spend_per_capita']:>10.2f}  gap={gap:>+6.1f}%")

print(f"\nNational avg: cards/1000={nat_cards_per_1000}, tx/cap={nat_tx_per_capita}, spend/cap={nat_spend_per_capita}")

print("\n=== MOBILITY (% local transactions) ===")
for woj, data in sorted(woj_mobility.items(), key=lambda x: x[1]["local_pct"]):
    print(f"  {woj:25s} local={data['local_pct']:>5.1f}%  outgoing={data['outgoing_pct']:>5.1f}%")

print("\n=== INFLOW RANKING ===")
for woj, count in sorted(woj_inflow.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {woj:25s} inflow_tx={count:>12,}")

print("\nDONE")
