"""QR on the card for P2P: aggregates from the p2p_footprint caches -> results/p2p_qr.json.

Only aggregates of 30+ cards (regions: 3,000+) leave this script.
"""
import json

import duckdb
import numpy as np
import pandas as pd

from p2p_footprint import SEGMENTS
from paths import CACHE

ROOT = CACHE.parent.parent.parent  # repository root (default CACHE = ml_readiness/data/cache)
OUT = ROOT / "ml_readiness" / "results" / "p2p_qr.json"
MIN_CARDS = 30


def load():
    cards = pd.read_parquet(CACHE / "p2p_card_2026h1.parquet")
    active = pd.read_parquet(CACHE / "all_cards_window_t18.parquet")  # active in Jan-Jun 2026 (3+ months)
    d = active.merge(cards, on="card", how="left", suffixes=("", "_p2p"))
    online = d.n_online > 0
    typed_share = d.n_typed / d.n_online.where(online)
    d["audience"] = np.select(
        [online & (typed_share >= 0.5), online & (d.n_typed > 0), online, d.first_online_m.isna()],
        ["A mostly typing", "D sometimes typing", "F never typing", "C+E never online"], default="L lapsed")
    return d


def segment_summary(d):
    rows = []
    n = len(d)
    for s in SEGMENTS:
        users = d[f"n_{s}"] > 0
        tx = d[f"n_{s}"].sum()
        rows.append(dict(segment=s, cards=int(users.sum()), share_of_active_cards=users.mean(),
                         tx=int(tx), amount_pln=float(d[f"amt_{s}"].sum()),
                         tx_per_user_month=tx / max(users.sum(), 1) / 6,
                         typed_share=d[f"typed_{s}"].sum() / max(tx, 1)))
    any_p2p = (d[[f"n_{s}" for s in SEGMENTS if s != "cash_atm"]] > 0).any(axis=1)
    return pd.DataFrame(rows), any_p2p.mean(), n


def overlap(d):
    """How P2P behaviours co-occur with the online-typing audiences."""
    flags = {s: d[f"n_{s}"] > 0 for s in SEGMENTS}
    flags["any_digital_p2p"] = (d[[f"n_{s}" for s in ["send_money", "c2c_seller_fee", "c2c_purchase",
                                                      "collections"]]] > 0).any(axis=1)
    out = pd.DataFrame({k: d.groupby("audience").apply(lambda g, v=v: v[g.index].mean()) for k, v in flags.items()})
    out["cards"] = d.groupby("audience").size()
    return out


def cash_vs_online(d):
    """Cash intensity (ATM share of card value) against online card usage."""
    atm_share = d.amt_cash_atm / d.amt_total.where(d.amt_total > 0)
    band = pd.cut(atm_share.fillna(0), [-0.01, 0, 0.1, 0.25, 0.5, 1.0],
                  labels=["no ATM", "0-10%", "10-25%", "25-50%", "50%+"])
    g = d.groupby(band, observed=True)
    return pd.DataFrame({"cards": g.size(), "online_any": g.apply(lambda x: (x.n_online > 0).mean()),
                         "typed_share_of_online": g.apply(lambda x: x.n_typed.sum() / max(x.n_online.sum(), 1)),
                         "wallet_share": g.wallet_share.mean(),
                         "any_digital_p2p": g.apply(lambda x: (x[["n_send_money", "n_c2c_purchase",
                                                                  "n_c2c_seller_fee", "n_collections"]] > 0)
                                                    .any(axis=1).mean())})


def regions(d):
    gus = json.load(open(ROOT / "gus_data.json", encoding="utf-8"))
    woj = d.home_postal2.map(gus["postal_to_woj_mapping"])
    d = d.assign(woj=woj)
    g = d.groupby("woj")
    r = pd.DataFrame({
        "cards": g.size(),
        "online_any": g.apply(lambda x: (x.n_online > 0).mean()),
        "typed_share_of_online": g.apply(lambda x: x.n_typed.sum() / max(x.n_online.sum(), 1)),
        "atm_share_of_value": g.apply(lambda x: x.amt_cash_atm.sum() / x.amt_total.sum()),
        "atm_users": g.apply(lambda x: (x.n_cash_atm > 0).mean()),
        "send_money_users": g.apply(lambda x: (x.n_send_money > 0).mean()),
        "c2c_users": g.apply(lambda x: ((x.n_c2c_purchase + x.n_c2c_seller_fee) > 0).mean()),
        "group_bill_users": g.apply(lambda x: (x.n_group_bill > 0).mean()),
    })
    pop = pd.Series({k: v["population"] for k, v in gus["population_woj"].items()})
    r["population_gus_2024"] = pop
    r["sample_cards_per_1000_inhabitants"] = r.cards / r.population_gus_2024 * 1000
    return r[r.cards >= 3000]


def monthly():
    m = pd.read_parquet(CACHE / "p2p_segment_month.parquet")
    m = m[m.cards >= MIN_CARDS].sort_values(["seg", "month"])
    return m


def run():
    d = load()
    seg, any_p2p, n = segment_summary(d)
    res = {
        "window": "Jan-Jun 2026, Polish cards active 3+ months",
        "active_cards": n,
        "any_p2p_footprint_share_excl_atm": any_p2p,
        "segments": seg.to_dict("records"),
        "audience_overlap": overlap(d).reset_index().to_dict("records"),
        "cash_vs_online": cash_vs_online(d).reset_index(names="atm_share_band").to_dict("records"),
        "regions": regions(d).reset_index(names="woj").to_dict("records"),
        "monthly": monthly().to_dict("records"),
    }
    f = pd.read_parquet(CACHE / "p2p_foreign_cards.parquet")
    f = f[f.cards >= MIN_CARDS].sort_values("cards", ascending=False)
    f["cnp_typed_share"] = f.n_cnp_typed / f.n_cnp.where(f.n_cnp > 0)
    res["foreign_cards_in_poland"] = f.head(20).to_dict("records")
    OUT.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    return res


if __name__ == "__main__":
    r = run()
    print(json.dumps({k: r[k] for k in ["active_cards", "any_p2p_footprint_share_excl_atm"]}))
