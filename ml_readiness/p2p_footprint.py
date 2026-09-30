"""P2P footprint of Polish Visa cards: where the card already moves money between people.

Builds three caches from the raw file (one pass each, a few minutes):
- cache/p2p_card_2026h1.parquet   card-level P2P / cash / group-bill features, Jan-Jun 2026
- cache/p2p_segment_month.parquet segment x month totals, Jan 2025 - Jun 2026
- cache/p2p_foreign_cards.parquet foreign cards paying in Poland, by issuer country
Card id = hash(pan), the same key as cache/slim and cache/card_month_panel.
"""
import duckdb
import pandas as pd

from paths import CACHE, DATA

NAME = "upper(regexp_replace(mrch_nm_raw, '[^A-Za-z ]', '', 'g'))"
SEND_NAMES = ("REVOLUT|ZEN ?COM|SKRILL|PAYSEND|REMITLY|TRANSFERGO|WISE|MONOVISA|PAYPAL|PROFEE|ACE MONEY"
              "|WESTERN UNION|MONEYGRAM|MONOBANK|TOPUP")
COLLECT_NAMES = "ZRZUTK|POMAGAM|SIEPOMAGA|PATRONITE|BUYCOFFEE|ESKARBONK"
N_BUCKETS = 16
GROUP_BILL_PLN = 200  # a restaurant / bar bill of 200+ PLN: ~3.5x the median bill, likely paid for a group

# Where the card already touches money between people (order matters: first match wins)
SEGMENT = f'''
CASE
  WHEN transaction_type = 'ATM' OR mrch_catg_cd = 6011 THEN 'cash_atm'
  WHEN mrch_catg_cd = 4829 AND nm LIKE '%POCZTA%' THEN 'post_office_bills'
  WHEN mrch_catg_cd = 4829 OR (mrch_catg_cd IN (6012, 6051, 6540) AND regexp_matches(nm, '{SEND_NAMES}'))
       THEN 'send_money'
  WHEN mrch_catg_cd = 7311 AND regexp_matches(nm, 'VINTED|OLX') THEN 'c2c_seller_fee'
  WHEN regexp_matches(nm, 'VINTED|OLX|LOKALNIE') THEN 'c2c_purchase'
  WHEN mrch_catg_cd = 8398 OR regexp_matches(nm, '{COLLECT_NAMES}') THEN 'collections'
  WHEN mrch_catg_cd IN (5812, 5813) AND cp_flag = 1 AND amt >= {GROUP_BILL_PLN} THEN 'group_bill'
END
'''
SEGMENTS = ["cash_atm", "post_office_bills", "send_money", "c2c_seller_fee", "c2c_purchase", "collections",
            "group_bill"]

BASE = f'''
SELECT hash(pymt_crd_acct_num_raw) AS card, prch_mnth_id AS month, {NAME} AS nm, mrch_catg_cd,
       transaction_type, cp_flag, channel_flg, transaction_pos_entry_mode AS entry_mode,
       mrch_ctry_nm = 'POLAND' AS merchant_pl, left(pstl_cd_enr, 2) AS postal2,
       CAST(cs_tran_amt AS DOUBLE) AS amt, prch_dt, CAST(tran_id_gmt_tm AS INT) // 10000 AS hour_gmt
FROM '{DATA.as_posix()}'
WHERE issr_ctry_nm = 'POLAND'
'''


def connect():
    con = duckdb.connect()
    con.sql("SET threads = 8")
    con.sql("SET memory_limit = '6GB'")
    con.sql(f"SET temp_directory = '{(CACHE / 'duckdb_tmp').as_posix()}'")
    con.sql("SET preserve_insertion_order = false")
    con.sql(f"CREATE OR REPLACE VIEW tx AS SELECT *, ({SEGMENT}) AS seg FROM ({BASE})")
    return con


def build(con, force=False):
    card_file = CACHE / "p2p_card_2026h1.parquet"
    month_file = CACHE / "p2p_segment_month.parquet"
    foreign_file = CACHE / "p2p_foreign_cards.parquet"

    if force or not card_file.exists():
        per_seg = ",\n".join(
            f"count(*) FILTER (WHERE seg = '{s}') AS n_{s}, "
            f"coalesce(sum(amt) FILTER (WHERE seg = '{s}'), 0) AS amt_{s}, "
            f"count(*) FILTER (WHERE seg = '{s}' AND entry_mode = 'Manual key entry') AS typed_{s}"
            for s in SEGMENTS)
        parts = []
        for b in range(N_BUCKETS):
            parts.append(con.sql(f'''
                SELECT card, count(*) AS n_tx, sum(amt) AS amt_total,
                       count(*) FILTER (WHERE cp_flag = 1) AS n_store,
                       mode(postal2) FILTER (WHERE cp_flag = 1 AND merchant_pl) AS home_postal2,
                       {per_seg}
                FROM tx WHERE month BETWEEN 202601 AND 202606 AND card % {N_BUCKETS} = {b}
                GROUP BY card
            ''').df())
        pd.concat(parts, ignore_index=True).to_parquet(card_file)

    if force or not month_file.exists():
        con.sql(f'''
            COPY (
                SELECT seg, month, count(*) AS n_tx, sum(amt) AS amount, count(DISTINCT card) AS cards,
                       count(*) FILTER (WHERE entry_mode = 'Manual key entry') AS typed,
                       count(*) FILTER (WHERE cp_flag = 0 AND channel_flg = 'mobile') AS cnp_phone,
                       count(*) FILTER (WHERE cp_flag = 0 AND channel_flg = 'eci') AS cnp_desktop
                FROM tx WHERE seg IS NOT NULL
                GROUP BY ALL
            ) TO '{month_file.as_posix()}' (FORMAT parquet)
        ''')

    if force or not foreign_file.exists():
        con.sql(f'''
            COPY (
                SELECT issr_ctry_nm AS issuer_country,
                       count(DISTINCT pymt_crd_acct_num_raw) AS cards, count(*) AS n_tx,
                       sum(CAST(cs_tran_amt AS DOUBLE)) AS amount,
                       count(*) FILTER (WHERE cp_flag = 0) AS n_cnp,
                       count(*) FILTER (WHERE cp_flag = 0 AND transaction_pos_entry_mode = 'Manual key entry') AS n_cnp_typed,
                       count(*) FILTER (WHERE transaction_type = 'ATM') AS n_atm,
                       sum(CAST(cs_tran_amt AS DOUBLE)) FILTER (WHERE transaction_type = 'ATM') AS amt_atm,
                       count(*) FILTER (WHERE mrch_catg_cd = 4829 OR mrch_catg_cd = 6012) AS n_send_money
                FROM '{DATA.as_posix()}'
                WHERE mrch_ctry_nm = 'POLAND' AND issr_ctry_nm <> 'POLAND'
                  AND prch_mnth_id BETWEEN 202601 AND 202606
                GROUP BY 1
            ) TO '{foreign_file.as_posix()}' (FORMAT parquet)
        ''')
    return card_file, month_file, foreign_file


if __name__ == "__main__":
    import time
    t0 = time.time()
    print(build(connect()), f"{time.time() - t0:.0f}s")
