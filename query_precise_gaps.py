import os, json, decimal

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/mariu/Desktop/skrypty/credentials/restaurantclub-prod-62092a15751a.json"
from google.cloud import bigquery

client = bigquery.Client(project="restaurantclub-prod")
TABLE = "`restaurantclub-prod.rozne.datasprint_sample_data`"


def decimal_converter(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def run_query(name, sql):
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print(f"{'='*60}")
    result = client.query(sql).result()
    rows = [dict(r) for r in result]
    print(f"  -> {len(rows)} rows returned")
    for row in rows[:10]:
        print(f"  {row}")
    if len(rows) > 10:
        print(f"  ... and {len(rows) - 10} more rows")
    return rows


results = {}

# 1. small_transactions
results["small_transactions"] = run_query("small_transactions", f"""
SELECT
    CASE
        WHEN cs_tran_amt < 5 THEN 'a) 0-5'
        WHEN cs_tran_amt < 10 THEN 'b) 5-10'
        WHEN cs_tran_amt < 20 THEN 'c) 10-20'
        WHEN cs_tran_amt < 30 THEN 'd) 20-30'
        WHEN cs_tran_amt < 50 THEN 'e) 30-50'
        WHEN cs_tran_amt < 100 THEN 'f) 50-100'
        WHEN cs_tran_amt < 200 THEN 'g) 100-200'
        WHEN cs_tran_amt < 500 THEN 'h) 200-500'
        ELSE 'i) 500+'
    END as bucket,
    COUNT(*) as tx_count,
    ROUND(SUM(cs_tran_amt),2) as total_amount,
    ROUND(AVG(cs_tran_amt),2) as avg_amount
FROM {TABLE}
GROUP BY bucket
ORDER BY bucket
""")

# 2. small_tx_by_category
results["small_tx_by_category"] = run_query("small_tx_by_category", f"""
SELECT mrch_catg_nm, COUNT(*) as tx_count,
    ROUND(SUM(cs_tran_amt),2) as total_amount,
    ROUND(AVG(cs_tran_amt),2) as avg_amount
FROM {TABLE}
WHERE cs_tran_amt < 20
GROUP BY mrch_catg_nm
ORDER BY tx_count DESC
LIMIT 30
""")

# 3. online_detailed
results["online_detailed"] = run_query("online_detailed", f"""
WITH totals AS (
    SELECT mrch_catg_nm, COUNT(*) as total_tx, SUM(cs_tran_amt) as total_amt
    FROM {TABLE}
    GROUP BY mrch_catg_nm
    HAVING COUNT(*) > 10000
),
online AS (
    SELECT mrch_catg_nm, COUNT(*) as online_tx, SUM(cs_tran_amt) as online_amt
    FROM {TABLE}
    WHERE cp_flag = 0
    GROUP BY mrch_catg_nm
)
SELECT t.mrch_catg_nm,
    t.total_tx,
    COALESCE(o.online_tx, 0) as online_tx,
    ROUND(COALESCE(o.online_tx, 0) / t.total_tx * 100, 2) as online_tx_pct,
    ROUND(t.total_amt, 2) as total_amt,
    ROUND(COALESCE(o.online_amt, 0), 2) as online_amt,
    ROUND(COALESCE(o.online_amt, 0) / t.total_amt * 100, 2) as online_val_pct
FROM totals t
LEFT JOIN online o ON t.mrch_catg_nm = o.mrch_catg_nm
ORDER BY online_tx_pct ASC
""")

# 4. channel_all_categories
results["channel_all_categories"] = run_query("channel_all_categories", f"""
SELECT mrch_catg_nm, channel_flg,
    COUNT(*) as tx_count,
    ROUND(SUM(cs_tran_amt),2) as total_amount,
    ROUND(AVG(cs_tran_amt),2) as avg_amount
FROM {TABLE}
WHERE mrch_catg_nm IN (
    SELECT mrch_catg_nm FROM {TABLE} GROUP BY mrch_catg_nm HAVING COUNT(*) > 50000
)
GROUP BY mrch_catg_nm, channel_flg
ORDER BY mrch_catg_nm, tx_count DESC
""")

# 5. low_volume_categories
results["low_volume_categories"] = run_query("low_volume_categories", f"""
SELECT mrch_catg_nm, mrch_catg_cd,
    COUNT(*) as tx_count,
    ROUND(SUM(cs_tran_amt),2) as total_amount,
    ROUND(AVG(cs_tran_amt),2) as avg_amount,
    COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards,
    COUNT(DISTINCT mrch_nm_raw) as unique_merchants
FROM {TABLE}
GROUP BY mrch_catg_nm, mrch_catg_cd
HAVING COUNT(*) BETWEEN 1000 AND 100000
ORDER BY tx_count ASC
""")

# 6. cash_vs_card_by_amount
results["cash_vs_card_by_amount"] = run_query("cash_vs_card_by_amount", f"""
SELECT
    CASE
        WHEN cs_tran_amt < 10 THEN 'a) Under 10'
        WHEN cs_tran_amt < 50 THEN 'b) 10-50'
        WHEN cs_tran_amt < 100 THEN 'c) 50-100'
        WHEN cs_tran_amt < 200 THEN 'd) 100-200'
        WHEN cs_tran_amt < 500 THEN 'e) 200-500'
        ELSE 'f) 500+'
    END as amount_bucket,
    channel_flg,
    COUNT(*) as tx_count,
    ROUND(SUM(cs_tran_amt),2) as total_amount
FROM {TABLE}
GROUP BY amount_bucket, channel_flg
ORDER BY amount_bucket, tx_count DESC
""")

# 7. recurring_vs_onetime
results["recurring_vs_onetime"] = run_query("recurring_vs_onetime", f"""
SELECT
    CASE
        WHEN card_merchant_count >= 12 THEN 'Monthly+ recurring'
        WHEN card_merchant_count >= 6 THEN '6-11 visits'
        WHEN card_merchant_count >= 3 THEN '3-5 visits'
        WHEN card_merchant_count = 2 THEN '2 visits'
        ELSE 'One-time'
    END as frequency,
    COUNT(*) as pair_count,
    SUM(total_tx) as total_transactions,
    ROUND(SUM(total_amount), 2) as total_amount
FROM (
    SELECT pymt_crd_acct_num_raw, mrch_nm_raw,
        COUNT(*) as card_merchant_count,
        COUNT(*) as total_tx,
        SUM(cs_tran_amt) as total_amount
    FROM {TABLE}
    GROUP BY pymt_crd_acct_num_raw, mrch_nm_raw
) sub
GROUP BY frequency
ORDER BY frequency
""")

# Save all results
output_path = "C:/Users/mariu/warp/visa_heckathon/precise_gaps.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, default=decimal_converter, ensure_ascii=False)

print(f"\n{'='*60}")
print(f"All results saved to {output_path}")
print(f"{'='*60}")
print("\nRow counts summary:")
for k, v in results.items():
    print(f"  {k}: {len(v)} rows")
