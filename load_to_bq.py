import os
from google.cloud import bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/mariu/Desktop/skrypty/credentials/restaurantclub-prod-62092a15751a.json"

client = bigquery.Client(project="restaurantclub-prod")

table_ref = "restaurantclub-prod.rozne.datasprint_sample_data"
parquet_file = "C:/Users/mariu/warp/visa_heckathon/datasprint_sample_data.parquet"

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
)

print(f"Loading {parquet_file} -> {table_ref} ...")

with open(parquet_file, "rb") as f:
    job = client.load_table_from_file(f, table_ref, job_config=job_config)

print("Waiting for load job to finish (17GB file, this may take a while)...")
job.result()

table = client.get_table(table_ref)
print(f"Done! Loaded {table.num_rows} rows, {table.num_bytes:,} bytes into {table_ref}")
