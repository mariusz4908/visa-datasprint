import os, json, decimal
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/mariu/Desktop/skrypty/credentials/restaurantclub-prod-62092a15751a.json"
from google.cloud import bigquery
client = bigquery.Client(project="restaurantclub-prod")

TABLE = "`restaurantclub-prod.rozne.datasprint_sample_data`"

queries = {
    "basic_stats": f"""
        SELECT
            COUNT(*) as total_transactions,
            COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards,
            COUNT(DISTINCT mrch_nm_raw) as unique_merchants,
            COUNT(DISTINCT mrch_city_nm_raw) as unique_cities,
            ROUND(AVG(cs_tran_amt),2) as avg_amount,
            ROUND(MIN(cs_tran_amt),2) as min_amount,
            ROUND(MAX(cs_tran_amt),2) as max_amount,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            MIN(prch_dt) as min_date,
            MAX(prch_dt) as max_date
        FROM {TABLE}
    """,
    "monthly_trends": f"""
        SELECT
            prch_mnth_id,
            COUNT(*) as tx_count,
            COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            ROUND(AVG(cs_tran_amt),2) as avg_amount
        FROM {TABLE}
        GROUP BY prch_mnth_id
        ORDER BY prch_mnth_id
    """,
    "top_categories": f"""
        SELECT
            mrch_catg_nm,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            ROUND(AVG(cs_tran_amt),2) as avg_amount,
            COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards
        FROM {TABLE}
        GROUP BY mrch_catg_nm
        ORDER BY tx_count DESC
        LIMIT 20
    """,
    "top_cities": f"""
        SELECT
            mrch_city_nm_raw,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards
        FROM {TABLE}
        GROUP BY mrch_city_nm_raw
        ORDER BY tx_count DESC
        LIMIT 20
    """,
    "transaction_types": f"""
        SELECT
            transaction_type,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            ROUND(AVG(cs_tran_amt),2) as avg_amount
        FROM {TABLE}
        GROUP BY transaction_type
        ORDER BY tx_count DESC
    """,
    "card_segments": f"""
        SELECT
            prod_id_pltfrm_cd_vcis,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            ROUND(AVG(cs_tran_amt),2) as avg_amount,
            COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards
        FROM {TABLE}
        GROUP BY prod_id_pltfrm_cd_vcis
        ORDER BY tx_count DESC
    """,
    "card_types": f"""
        SELECT
            crd_typ_nm,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            ROUND(AVG(cs_tran_amt),2) as avg_amount
        FROM {TABLE}
        GROUP BY crd_typ_nm
        ORDER BY tx_count DESC
    """,
    "channel": f"""
        SELECT
            channel_flg,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            ROUND(AVG(cs_tran_amt),2) as avg_amount
        FROM {TABLE}
        GROUP BY channel_flg
        ORDER BY tx_count DESC
    """,
    "cp_flag": f"""
        SELECT
            cp_flag,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            ROUND(AVG(cs_tran_amt),2) as avg_amount
        FROM {TABLE}
        GROUP BY cp_flag
        ORDER BY tx_count DESC
    """,
    "domestic_foreign": f"""
        SELECT
            issr_jurn,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            ROUND(AVG(cs_tran_amt),2) as avg_amount,
            COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards
        FROM {TABLE}
        GROUP BY issr_jurn
        ORDER BY tx_count DESC
    """,
    "hourly_pattern": f"""
        SELECT
            CAST(SUBSTR(tran_id_gmt_tm, 1, 2) AS INT64) as hour_gmt,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            ROUND(AVG(cs_tran_amt),2) as avg_amount
        FROM {TABLE}
        GROUP BY hour_gmt
        ORDER BY hour_gmt
    """,
    "day_of_week": f"""
        SELECT
            FORMAT_DATE('%A', PARSE_DATE('%Y-%m-%d', prch_dt)) as day_name,
            EXTRACT(DAYOFWEEK FROM PARSE_DATE('%Y-%m-%d', prch_dt)) as day_num,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            ROUND(AVG(cs_tran_amt),2) as avg_amount
        FROM {TABLE}
        GROUP BY day_name, day_num
        ORDER BY day_num
    """,
    "top_merchants": f"""
        SELECT
            mrch_nm_raw,
            mrch_catg_nm,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            ROUND(AVG(cs_tran_amt),2) as avg_amount
        FROM {TABLE}
        GROUP BY mrch_nm_raw, mrch_catg_nm
        ORDER BY tx_count DESC
        LIMIT 20
    """,
    "issuer_countries": f"""
        SELECT
            issr_ctry_nm,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards
        FROM {TABLE}
        GROUP BY issr_ctry_nm
        ORDER BY tx_count DESC
        LIMIT 15
    """,
    "fua_regions": f"""
        SELECT
            fua_enr,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards
        FROM {TABLE}
        GROUP BY fua_enr
        ORDER BY tx_count DESC
        LIMIT 15
    """,
    "weekly_trends": f"""
        SELECT
            myweek,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            COUNT(DISTINCT pymt_crd_acct_num_raw) as unique_cards
        FROM {TABLE}
        GROUP BY myweek
        ORDER BY myweek
    """,
    "pos_entry_mode": f"""
        SELECT
            transaction_pos_entry_mode,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount,
            ROUND(AVG(cs_tran_amt),2) as avg_amount
        FROM {TABLE}
        GROUP BY transaction_pos_entry_mode
        ORDER BY tx_count DESC
    """,
    "amount_distribution": f"""
        SELECT
            CASE
                WHEN cs_tran_amt < 10 THEN '0-10'
                WHEN cs_tran_amt < 50 THEN '10-50'
                WHEN cs_tran_amt < 100 THEN '50-100'
                WHEN cs_tran_amt < 200 THEN '100-200'
                WHEN cs_tran_amt < 500 THEN '200-500'
                WHEN cs_tran_amt < 1000 THEN '500-1000'
                ELSE '1000+'
            END as amount_bucket,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount
        FROM {TABLE}
        GROUP BY amount_bucket
        ORDER BY MIN(cs_tran_amt)
    """,
    "category_by_month": f"""
        SELECT
            prch_mnth_id,
            mrch_catg_nm,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount
        FROM {TABLE}
        WHERE mrch_catg_nm IN (
            SELECT mrch_catg_nm FROM {TABLE} GROUP BY mrch_catg_nm ORDER BY COUNT(*) DESC LIMIT 10
        )
        GROUP BY prch_mnth_id, mrch_catg_nm
        ORDER BY prch_mnth_id, tx_count DESC
    """,
    "online_vs_physical_monthly": f"""
        SELECT
            prch_mnth_id,
            cp_flag,
            COUNT(*) as tx_count,
            ROUND(SUM(cs_tran_amt),2) as total_amount
        FROM {TABLE}
        GROUP BY prch_mnth_id, cp_flag
        ORDER BY prch_mnth_id, cp_flag
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

with open("C:/Users/mariu/warp/visa_heckathon/analysis_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, default=convert, ensure_ascii=False)

print("DONE - all queries completed")
