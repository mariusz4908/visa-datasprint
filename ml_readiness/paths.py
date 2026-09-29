"""Location of the Visa data and of the local cache (both are git-ignored).

By default everything lives in ml_readiness/data/. Set the VISA_DATA_DIR environment variable
to use another folder that contains datasprint_sample_data.parquet.
"""
import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("VISA_DATA_DIR", Path(__file__).resolve().parent / "data"))
DATA = DATA_DIR / "datasprint_sample_data.parquet"
CACHE = DATA_DIR / "cache"
