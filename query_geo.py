import os, json, decimal
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/mariu/Desktop/skrypty/credentials/restaurantclub-prod-62092a15751a.json"
from google.cloud import bigquery
client = bigquery.Client(project="restaurantclub-prod")

TABLE = "`restaurantclub-prod.rozne.datasprint_sample_data`"

queries = {
    "by_postal_prefix": f"""
        SELECT
            SUBSTR(pstl_cd_enr, 1, 2) as postal_prefix,
            COUNT(*) as tx_count,
            COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            ROUND(AVG(cs_tran_amt),2) as avg_amount,
            COUNT(DISTINCT mrch_nm_raw) as unique_merchants
        FROM {TABLE}
        WHERE pstl_cd_enr IS NOT NULL
          AND issr_ctry_nm = 'POLAND'
        GROUP BY postal_prefix
        ORDER BY postal_prefix
    """,
    "by_lau": f"""
        SELECT
            lau_enr,
            COUNT(*) as tx_count,
            COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            ROUND(AVG(cs_tran_amt),2) as avg_amount
        FROM {TABLE}
        WHERE lau_enr IS NOT NULL
          AND issr_ctry_nm = 'POLAND'
        GROUP BY lau_enr
        ORDER BY unique_cards DESC
        LIMIT 500
    """,
    "by_fua": f"""
        SELECT
            fua_enr,
            COUNT(*) as tx_count,
            COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            ROUND(AVG(cs_tran_amt),2) as avg_amount
        FROM {TABLE}
        WHERE fua_enr IS NOT NULL
          AND issr_ctry_nm = 'POLAND'
        GROUP BY fua_enr
        ORDER BY unique_cards DESC
    """,
    "by_merchant_postal": f"""
        SELECT
            SUBSTR(mrch_postal_code, 1, 2) as mrch_postal_prefix,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards,
            COUNT(DISTINCT mrch_nm_raw) as unique_merchants
        FROM {TABLE}
        WHERE mrch_postal_code IS NOT NULL
          AND mrch_ctry_nm = 'POLAND'
        GROUP BY mrch_postal_prefix
        ORDER BY mrch_postal_prefix
    """,
    "cardholder_vs_merchant_region": f"""
        SELECT
            SUBSTR(pstl_cd_enr, 1, 2) as card_region,
            SUBSTR(mrch_postal_code, 1, 2) as mrch_region,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount
        FROM {TABLE}
        WHERE pstl_cd_enr IS NOT NULL
          AND mrch_postal_code IS NOT NULL
          AND mrch_ctry_nm = 'POLAND'
          AND issr_ctry_nm = 'POLAND'
        GROUP BY card_region, mrch_region
        HAVING COUNT(*) > 10000
        ORDER BY card_region, tx_count DESC
    """
}

results = {}
for name, q in queries.items():
    print(f"Running: {name}...")
    rows = list(client.query(q).result())
    results[name] = [dict(r) for r in rows]
    print(f"  -> {len(rows)} rows")

def convert(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError(f"{type(obj)}")

with open("C:/Users/mariu/warp/visa_heckathon/geo_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, default=convert, ensure_ascii=False)

print("DONE")
