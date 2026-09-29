"""Shared feature pipeline for the online readiness model.

Snapshot T (month index, Jan 2025 = 0) uses the 6 months before T as the feature window and,
when labelled, the 3 months from T as the label window. Inputs are built by wallet_online.ipynb:
cache/card_month_panel, cache/card_first_online and cache/slim.
"""
import duckdb

from paths import CACHE

PANEL = (CACHE / "card_month_panel").as_posix()
FIRST_ONLINE = (CACHE / "card_first_online").as_posix()
SLIM = (CACHE / "slim").as_posix()
SLIM_PARTS = CACHE / "readiness_slim_parts"  # per snapshot x bucket
FEATURES = CACHE / "readiness_features_v2"   # one parquet file per snapshot
N_BUCKETS = 16

NOT_SHOPPING_MCC = "(4829, 6012, 6051, 6211, 6538, 6540)"
MACRO = '''
CASE
  WHEN mrch_catg_cd IN (5411, 5422, 5441, 5451, 5462, 5499, 5921) THEN 'grocery'
  WHEN mrch_catg_cd IN (5812, 5813) THEN 'restaurants_bars'
  WHEN mrch_catg_cd = 5814 THEN 'fast_food'
  WHEN mrch_catg_cd IN (5541, 5542, 5983, 7523, 7538, 5533, 4784, 7542) THEN 'car_fuel'
  WHEN mrch_catg_cd = 4121 THEN 'taxi'
  WHEN mrch_catg_cd IN (4111, 4112, 4131, 4789, 4011, 4411) THEN 'public_transport'
  WHEN mrch_catg_cd BETWEEN 3000 AND 3999 OR mrch_catg_cd IN (4511, 4722, 7011, 7512, 4582) THEN 'travel'
  WHEN mrch_catg_cd BETWEEN 5611 AND 5699 OR mrch_catg_cd IN (5941, 5655, 5661, 5139, 5137) THEN 'fashion_sport'
  WHEN mrch_catg_cd BETWEEN 5712 AND 5734 OR mrch_catg_cd IN (5200, 5211, 5231, 5251, 5261, 5065, 5946, 5045) THEN 'home_electronics'
  WHEN mrch_catg_cd IN (5912, 5977, 5122, 7230, 7298, 5975, 5976) OR mrch_catg_cd BETWEEN 8011 AND 8099 THEN 'health_beauty'
  WHEN mrch_catg_cd IN (5815, 5816, 5817, 5818, 4899, 7372, 5735) THEN 'digital_content'
  WHEN mrch_catg_cd IN (4812, 4814, 4900, 6300, 8220, 8299, 8211, 8241, 8244, 8249) THEN 'bills_telecom_edu'
  WHEN mrch_catg_cd IN (7832, 7922, 7929, 7991, 7996, 7997, 7999, 7941, 7995, 7932, 7933) THEN 'entertainment_betting'
  WHEN mrch_catg_cd IN (5262, 5399, 5311, 5310, 5300, 5331, 5964, 5969) THEN 'marketplace_general'
  WHEN mrch_catg_cd IN (5942, 5943, 5945, 5947, 5992, 5994, 5995, 5970, 5949, 5944) THEN 'hobby_books_gifts'
  ELSE 'other'
END
'''
GROUPS = ["grocery", "restaurants_bars", "fast_food", "car_fuel", "taxi", "public_transport", "travel",
          "fashion_sport", "home_electronics", "health_beauty", "digital_content", "bills_telecom_edu",
          "entertainment_betting", "marketplace_general", "hobby_books_gifts", "other"]

NUM = ["active_months", "tx_per_month", "tx_trend", "wallet_share", "wallet_share_last3", "wallet_ever",
       "months_since_first_wallet", "card_age_months", "cnp_other_share", "n_store_categories",
       "evening_share", "weekend_share", "abroad_share", "typical_store_amount"] + [f"s_{g}" for g in GROUPS]
CAT = ["card_type", "home_area"]

# Settings selected by time-based tuning in readiness_model.ipynb
BEST_PARAMS = {"num_leaves": 31, "min_child_samples": 400, "learning_rate": 0.03, "n_estimators": 300,
               "subsample": 0.8, "subsample_freq": 1, "colsample_bytree": 0.8}


def yyyymm(m):
    return (2025 + m // 12) * 100 + m % 12 + 1


def connect(memory_limit="2GB"):
    con = duckdb.connect()
    con.sql(f"SET memory_limit = '{memory_limit}'")
    con.sql("SET threads = 4")
    con.sql("SET preserve_insertion_order = false")
    con.sql(f"CREATE OR REPLACE VIEW panel AS SELECT *, (month // 100 - 2025) * 12 + month % 100 - 1 AS m "
            f"FROM read_parquet('{PANEL}/*.parquet')")
    con.sql(f"CREATE OR REPLACE VIEW attrs AS SELECT card, card_type, home_fua "
            f"FROM read_parquet('{FIRST_ONLINE}/*.parquet')")
    return con


def top_fuas(con, n=15):
    return con.sql(f'''
        SELECT home_fua FROM attrs WHERE home_fua IS NOT NULL GROUP BY 1 ORDER BY count(*) DESC LIMIT {n}
    ''').df().home_fua.tolist()


def build_slim_parts(con, t):
    """In-store transaction features for snapshot t, one file per bucket (skips existing files)."""
    SLIM_PARTS.mkdir(exist_ok=True)
    local_hour = "((ts % 1000000) // 10000 + CASE WHEN month % 100 BETWEEN 4 AND 10 THEN 2 ELSE 1 END) % 24"
    day = "make_date(CAST(ts // 10000000000 AS INT), CAST(ts // 100000000 % 100 AS INT), CAST(ts // 1000000 % 100 AS INT))"
    shares = ", ".join(f"avg(CAST(({MACRO}) = '{g}' AS DOUBLE)) FILTER (WHERE cp_flag = 1) AS s_{g}" for g in GROUPS)
    for b in range(N_BUCKETS):
        out = SLIM_PARTS / f"t{t:02d}_b{b:02d}.parquet"
        if out.exists():
            continue
        con.sql(f'''
            COPY (
                SELECT card, {t} AS snapshot,
                       count(DISTINCT mrch_catg_cd) FILTER (WHERE cp_flag = 1) AS n_store_categories,
                       avg(({local_hour} >= 19)::INT) FILTER (WHERE cp_flag = 1) AS evening_share,
                       avg((dayofweek({day}) IN (0, 6))::INT) FILTER (WHERE cp_flag = 1) AS weekend_share,
                       avg((NOT merchant_pl)::INT) FILTER (WHERE cp_flag = 1) AS abroad_share,
                       exp(avg(ln(1 + greatest(amt, 0))) FILTER (WHERE cp_flag = 1)) - 1 AS typical_store_amount,
                       {shares}
                FROM read_parquet('{SLIM}/bucket={b}/*.parquet')
                WHERE month BETWEEN {yyyymm(t - 6)} AND {yyyymm(t - 1)}
                GROUP BY card
            ) TO '{out.as_posix()}' (FORMAT parquet)
        ''')


def build_snapshot(con, t, labelled=True):
    """Card features for snapshot t written to FEATURES/t{t}.parquet (skips an existing file).

    Population: no online purchase before t, >= 3 active months and >= 20 transactions in the
    feature window; when labelled, also active in the label window.
    """
    FEATURES.mkdir(exist_ok=True)
    out = FEATURES / f"t{t:02d}.parquet"
    if out.exists():
        return out
    build_slim_parts(con, t)
    fua_list = ", ".join(f"'{f}'" for f in top_fuas(con))
    label_cte = (f", lab AS (SELECT card, sum(n_online) > 0 AS label FROM panel "
                 f"WHERE m BETWEEN {t} AND {t} + 2 GROUP BY card)") if labelled else ""
    label_col = "l.label::INT AS label" if labelled else "NULL::INT AS label"
    label_join = "JOIN lab l USING (card)" if labelled else ""
    con.sql(f'''
      COPY (
        WITH hist AS (
            SELECT card, sum(n_online) AS online_before, min(m) AS first_m,
                   min(m) FILTER (WHERE n_wallet_store > 0) AS first_wallet_m
            FROM panel WHERE m < {t} GROUP BY card
        ),
        win AS (
            SELECT card,
                   count(*) AS active_months,
                   sum(n_tx) AS n_tx,
                   sum(n_store) AS n_store,
                   sum(n_wallet_store) AS n_wallet,
                   sum(n_tx - n_store - n_online) AS n_cnp_other,
                   sum(n_tx) FILTER (WHERE m >= {t} - 3) AS n_tx_last3,
                   sum(n_wallet_store) FILTER (WHERE m >= {t} - 3) AS n_wallet_last3,
                   sum(n_store) FILTER (WHERE m >= {t} - 3) AS n_store_last3
            FROM panel WHERE m BETWEEN {t} - 6 AND {t} - 1 GROUP BY card
        ),
        slim_feat AS (
            SELECT * FROM read_parquet('{SLIM_PARTS.as_posix()}/t{t:02d}_b*.parquet')
        ){label_cte}
        SELECT w.card, {t} AS snapshot,
               w.active_months,
               w.n_tx / w.active_months AS tx_per_month,
               coalesce(w.n_tx_last3, 0) / nullif(w.n_tx - coalesce(w.n_tx_last3, 0), 0) AS tx_trend,
               w.n_wallet / nullif(w.n_store, 0) AS wallet_share,
               coalesce(w.n_wallet_last3, 0) / nullif(w.n_store_last3, 0) AS wallet_share_last3,
               (h.first_wallet_m IS NOT NULL)::INT AS wallet_ever,
               {t} - h.first_wallet_m AS months_since_first_wallet,
               CASE WHEN h.first_m = 0 THEN 99 ELSE {t} - h.first_m END AS card_age_months,
               w.n_cnp_other / w.n_tx AS cnp_other_share,
               a.card_type,
               CASE WHEN a.home_fua IS NULL THEN 'UNKNOWN'
                    WHEN a.home_fua IN ({fua_list}) THEN a.home_fua ELSE 'OTHER' END AS home_area,
               a.home_fua,
               f.* EXCLUDE (card, snapshot),
               {label_col}
        FROM win w
        JOIN hist h USING (card)
        {label_join}
        LEFT JOIN attrs a USING (card)
        LEFT JOIN slim_feat f ON f.card = w.card
        WHERE h.online_before = 0 AND w.active_months >= 3 AND w.n_tx >= 20
      ) TO '{out.as_posix()}' (FORMAT parquet)
    ''')
    return out
