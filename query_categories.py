import os
import json
import decimal

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/mariu/Desktop/skrypty/credentials/restaurantclub-prod-62092a15751a.json"

from google.cloud import bigquery
ROOT = os.path.dirname(os.path.abspath(__file__))  # repository root, where the JSON results live

client = bigquery.Client(project="restaurantclub-prod")
TABLE = "`restaurantclub-prod.rozne.datasprint_sample_data`"


def decimal_converter(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def run_query(name, sql):
    print(f"Running query: {name} ...")
    result = client.query(sql).result()
    rows = [dict(row) for row in result]
    print(f"  -> {len(rows)} rows")
    return rows


results = {}

# 1. all_categories
results["all_categories"] = run_query("all_categories", f"""
SELECT mrch_catg_cd, mrch_catg_nm,
  COUNT(*) as tx_count,
  ROUND(SUM(cs_tran_amt),2) as total_amount,
  ROUND(AVG(cs_tran_amt),2) as avg_amount,
  COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards
FROM {TABLE}
GROUP BY mrch_catg_cd, mrch_catg_nm
ORDER BY tx_count DESC
""")

# 2. category_online_offline
results["category_online_offline"] = run_query("category_online_offline", f"""
SELECT mrch_catg_nm,
  cp_flag,
  COUNT(*) as tx_count,
  ROUND(SUM(cs_tran_amt),2) as total_amount,
  ROUND(AVG(cs_tran_amt),2) as avg_amount
FROM {TABLE}
GROUP BY mrch_catg_nm, cp_flag
ORDER BY mrch_catg_nm, cp_flag
""")

# 3. category_channel
results["category_channel"] = run_query("category_channel", f"""
SELECT mrch_catg_nm, channel_flg,
  COUNT(*) as tx_count,
  ROUND(SUM(cs_tran_amt),2) as total_amount
FROM {TABLE}
WHERE mrch_catg_nm IN (
  SELECT mrch_catg_nm FROM {TABLE} GROUP BY mrch_catg_nm ORDER BY COUNT(*) DESC LIMIT 30
)
GROUP BY mrch_catg_nm, channel_flg
ORDER BY mrch_catg_nm, tx_count DESC
""")

# 4. category_pos_entry
results["category_pos_entry"] = run_query("category_pos_entry", f"""
SELECT mrch_catg_nm, transaction_pos_entry_mode,
  COUNT(*) as tx_count,
  ROUND(SUM(cs_tran_amt),2) as total_amount
FROM {TABLE}
WHERE mrch_catg_nm IN (
  SELECT mrch_catg_nm FROM {TABLE} GROUP BY mrch_catg_nm ORDER BY COUNT(*) DESC LIMIT 30
)
GROUP BY mrch_catg_nm, transaction_pos_entry_mode
ORDER BY mrch_catg_nm, tx_count DESC
""")

# 5. category_card_segment
results["category_card_segment"] = run_query("category_card_segment", f"""
SELECT mrch_catg_nm, prod_id_pltfrm_cd_vcis,
  COUNT(*) as tx_count,
  ROUND(SUM(cs_tran_amt),2) as total_amount,
  ROUND(AVG(cs_tran_amt),2) as avg_amount
FROM {TABLE}
WHERE mrch_catg_nm IN (
  SELECT mrch_catg_nm FROM {TABLE} GROUP BY mrch_catg_nm ORDER BY COUNT(*) DESC LIMIT 20
)
GROUP BY mrch_catg_nm, prod_id_pltfrm_cd_vcis
ORDER BY mrch_catg_nm, tx_count DESC
""")

# 6. total_stats
results["total_stats"] = run_query("total_stats", f"""
SELECT COUNT(*) as total_tx, ROUND(SUM(cs_tran_amt),2) as total_amount
FROM {TABLE}
""")

# Save to JSON
output_path = os.path.join(ROOT, "category_analysis.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, default=decimal_converter, ensure_ascii=False)

print(f"\nAll results saved to {output_path}")
print("\nSummary:")
for key, rows in results.items():
    print(f"  {key}: {len(rows)} rows")
