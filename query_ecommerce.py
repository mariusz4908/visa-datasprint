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
    print(f"Running: {name} ...")
    result = client.query(sql).result()
    rows = [dict(r) for r in result]
    print(f"  -> {len(rows)} rows")
    return rows

results = {}

# 1. ecommerce_overall
results["ecommerce_overall"] = run_query("ecommerce_overall", f"""
SELECT cp_flag,
    COUNT(*) as tx_count,
    ROUND(SUM(cs_tran_amt),2) as total_amount,
    ROUND(AVG(cs_tran_amt),2) as avg_amount,
    COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards,
    COUNT(DISTINCT mrch_nm_raw) as unique_merchants
FROM {TABLE}
GROUP BY cp_flag
""")

# 2. ecommerce_top_categories
results["ecommerce_top_categories"] = run_query("ecommerce_top_categories", f"""
SELECT mrch_catg_nm,
    COUNT(*) as tx_count,
    ROUND(SUM(cs_tran_amt),2) as total_amount,
    ROUND(AVG(cs_tran_amt),2) as avg_amount,
    COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards,
    COUNT(DISTINCT mrch_nm_raw) as unique_merchants
FROM {TABLE}
WHERE cp_flag = 0
GROUP BY mrch_catg_nm
ORDER BY tx_count DESC
LIMIT 40
""")

# 3. ecommerce_top_merchants
results["ecommerce_top_merchants"] = run_query("ecommerce_top_merchants", f"""
SELECT mrch_nm_raw, mrch_catg_nm,
    COUNT(*) as tx_count,
    ROUND(SUM(cs_tran_amt),2) as total_amount,
    ROUND(AVG(cs_tran_amt),2) as avg_amount,
    COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards
FROM {TABLE}
WHERE cp_flag = 0
GROUP BY mrch_nm_raw, mrch_catg_nm
ORDER BY tx_count DESC
LIMIT 50
""")

# 4. ecommerce_monthly_trend
results["ecommerce_monthly_trend"] = run_query("ecommerce_monthly_trend", f"""
SELECT prch_mnth_id,
    SUM(CASE WHEN cp_flag = 0 THEN 1 ELSE 0 END) as online_tx,
    SUM(CASE WHEN cp_flag = 1 THEN 1 ELSE 0 END) as physical_tx,
    ROUND(SUM(CASE WHEN cp_flag = 0 THEN cs_tran_amt ELSE 0 END),2) as online_amount,
    ROUND(SUM(CASE WHEN cp_flag = 1 THEN cs_tran_amt ELSE 0 END),2) as physical_amount,
    ROUND(SUM(CASE WHEN cp_flag = 0 THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as online_tx_pct,
    ROUND(SUM(CASE WHEN cp_flag = 0 THEN cs_tran_amt ELSE 0 END) / SUM(cs_tran_amt) * 100, 2) as online_val_pct
FROM {TABLE}
GROUP BY prch_mnth_id
ORDER BY prch_mnth_id
""")

# 5. ecommerce_by_channel
results["ecommerce_by_channel"] = run_query("ecommerce_by_channel", f"""
SELECT channel_flg,
    COUNT(*) as tx_count,
    ROUND(SUM(cs_tran_amt),2) as total_amount,
    ROUND(AVG(cs_tran_amt),2) as avg_amount,
    COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards
FROM {TABLE}
WHERE cp_flag = 0
GROUP BY channel_flg
ORDER BY tx_count DESC
""")

# 6. ecommerce_amount_distribution
results["ecommerce_amount_distribution"] = run_query("ecommerce_amount_distribution", f"""
SELECT
    CASE
        WHEN cs_tran_amt < 10 THEN 'a) 0-10'
        WHEN cs_tran_amt < 30 THEN 'b) 10-30'
        WHEN cs_tran_amt < 50 THEN 'c) 30-50'
        WHEN cs_tran_amt < 100 THEN 'd) 50-100'
        WHEN cs_tran_amt < 200 THEN 'e) 100-200'
        WHEN cs_tran_amt < 500 THEN 'f) 200-500'
        WHEN cs_tran_amt < 1000 THEN 'g) 500-1000'
        ELSE 'h) 1000+'
    END as bucket,
    cp_flag,
    COUNT(*) as tx_count,
    ROUND(SUM(cs_tran_amt),2) as total_amount
FROM {TABLE}
GROUP BY bucket, cp_flag
ORDER BY bucket, cp_flag
""")

# 7. ecommerce_card_types
results["ecommerce_card_types"] = run_query("ecommerce_card_types", f"""
SELECT crd_typ_nm, cp_flag,
    COUNT(*) as tx_count,
    ROUND(SUM(cs_tran_amt),2) as total_amount,
    ROUND(AVG(cs_tran_amt),2) as avg_amount
FROM {TABLE}
GROUP BY crd_typ_nm, cp_flag
ORDER BY crd_typ_nm, cp_flag
""")

# 8. ecommerce_domestic_foreign
results["ecommerce_domestic_foreign"] = run_query("ecommerce_domestic_foreign", f"""
SELECT issr_jurn, cp_flag,
    COUNT(*) as tx_count,
    ROUND(SUM(cs_tran_amt),2) as total_amount,
    ROUND(AVG(cs_tran_amt),2) as avg_amount
FROM {TABLE}
GROUP BY issr_jurn, cp_flag
ORDER BY issr_jurn, cp_flag
""")

# 9. ecommerce_entry_mode
results["ecommerce_entry_mode"] = run_query("ecommerce_entry_mode", f"""
SELECT transaction_pos_entry_mode, cp_flag,
    COUNT(*) as tx_count,
    ROUND(SUM(cs_tran_amt),2) as total_amount,
    ROUND(AVG(cs_tran_amt),2) as avg_amount
FROM {TABLE}
GROUP BY transaction_pos_entry_mode, cp_flag
ORDER BY cp_flag, tx_count DESC
""")

# 10. subscription_merchants
results["subscription_merchants"] = run_query("subscription_merchants", f"""
SELECT mrch_nm_raw, mrch_catg_nm,
    COUNT(*) as tx_count,
    ROUND(SUM(cs_tran_amt),2) as total_amount,
    ROUND(AVG(cs_tran_amt),2) as avg_amount,
    COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards,
    ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT pymt_crd_acct_num_raw), 1) as tx_per_card
FROM {TABLE}
WHERE cp_flag = 0
GROUP BY mrch_nm_raw, mrch_catg_nm
HAVING COUNT(DISTINCT pymt_crd_acct_num_raw) > 1000
    AND COUNT(*) * 1.0 / COUNT(DISTINCT pymt_crd_acct_num_raw) > 3
ORDER BY unique_cards DESC
LIMIT 30
""")

# 11. ecommerce_consumer_vs_business
results["ecommerce_consumer_vs_business"] = run_query("ecommerce_consumer_vs_business", f"""
SELECT prod_id_pltfrm_cd_vcis, cp_flag,
    COUNT(*) as tx_count,
    ROUND(SUM(cs_tran_amt),2) as total_amount,
    ROUND(AVG(cs_tran_amt),2) as avg_amount
FROM {TABLE}
GROUP BY prod_id_pltfrm_cd_vcis, cp_flag
ORDER BY prod_id_pltfrm_cd_vcis, cp_flag
""")

# Save results
output_path = "C:/Users/mariu/warp/visa_heckathon/ecommerce_analysis.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, default=decimal_converter, ensure_ascii=False)

print(f"\nSaved to {output_path}")
print("\n=== Row count summary ===")
for key, rows in results.items():
    print(f"  {key}: {len(rows)} rows")
print(f"\nTotal queries: {len(results)}")
