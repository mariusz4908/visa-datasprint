"""Compliance check for the challenge's 3/75 rule on merchant-category results.

Every comparison group shown must contain at least 3 merchants and no merchant may exceed 75% of the group.
Merchant names are raw and messy ("ROSSMANN 01", "ROSSMANN 02"), so merchants are grouped by the first word of
the cleaned name. This merges more than it splits, so the top-merchant share is, if anything, overstated
(a conservative check).

Scopes:
- online card purchases of Polish cards (basis of the category results in wallet_online and target_audiences):
  per MCC category ("mcc"), per macro group ("macro") and per macro group x Polish / foreign merchant ("macro_x_pl");
- all transactions (basis of the category results in explore): per MCC category ("mcc_all") and macro group
  ("macro_all").
Output: results/check_3_75.csv (aggregated, no merchant names), read by readiness.passing_3_75().
"""
from pathlib import Path

import duckdb

import readiness as rd
from paths import DATA

con = duckdb.connect()
con.sql("SET memory_limit = '3GB'")
con.sql("SET threads = 4")

MERCHANT = "split_part(trim(regexp_replace(upper(coalesce(mrch_nm_raw, '')), '[^A-Z ]', ' ', 'g')), ' ', 1)"
con.sql(f'''
    CREATE TABLE merchant_tx AS
    SELECT mrch_catg_cd, mrch_catg_nm, ({rd.MACRO}) AS macro,
           mrch_ctry_nm = 'POLAND' AS merchant_pl,
           {MERCHANT} AS merchant,
           count(*) AS tx
    FROM '{DATA.as_posix()}'
    WHERE issr_ctry_nm = 'POLAND' AND transaction_type = 'POS'
      AND cp_flag = 0 AND mrch_catg_cd NOT IN {rd.NOT_SHOPPING_MCC}
    GROUP BY ALL
''')
con.sql(f'''
    CREATE TABLE merchant_tx_all AS
    SELECT mrch_catg_cd, mrch_catg_nm, ({rd.MACRO}) AS macro, {MERCHANT} AS merchant, count(*) AS tx
    FROM '{DATA.as_posix()}'
    GROUP BY ALL
''')


def check(keys, table="merchant_tx"):
    k = ", ".join(keys)
    return con.sql(f'''
        WITH m AS (SELECT {k}, merchant, sum(tx) AS tx FROM {table} GROUP BY ALL),
        g AS (
            SELECT {k}, count(*) AS merchants, sum(tx) AS tx, max(tx) / sum(tx) AS top_share
            FROM m GROUP BY ALL
        )
        SELECT *, merchants >= 3 AND top_share <= 0.75 AS passes FROM g ORDER BY tx DESC
    ''').df()


results = {
    "mcc": check(["mrch_catg_cd", "mrch_catg_nm"]),
    "macro": check(["macro"]),
    "macro_x_pl": check(["macro", "merchant_pl"]),
    "mcc_all": check(["mrch_catg_cd", "mrch_catg_nm"], "merchant_tx_all"),
    "macro_all": check(["macro"], "merchant_tx_all"),
}
out = []
for level, df in results.items():
    df.insert(0, "level", level)
    out.append(df)
    fails = df[~df.passes]
    print(f"== {level}: {len(df)} groups, {len(fails)} fail "
          f"({fails.tx.sum() / df.tx.sum():.1%} of payments in scope)")
    print(fails.head(15).to_string(index=False))

import pandas as pd  # noqa: E402

Path("results").mkdir(exist_ok=True)
pd.concat(out).to_csv("results/check_3_75.csv", index=False)
