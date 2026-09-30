"""
Fetch population data from the Polish GUS (Central Statistical Office) BDL API.

Downloads population for:
- All 16 województwa (voivodeships) - unit level 2
- All powiaty (counties) - unit level 5

Also includes postal code prefix to województwo mapping.

BDL API docs: https://bdl.stat.gov.pl/api/v1/
Variable 72305 = total population
"""

import json
import os
import sys
import time
ROOT = os.path.dirname(os.path.abspath(__file__))  # repository root, where the JSON results live

try:
    import requests
except ImportError:
    print("requests library not found, installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

BASE_URL = "https://bdl.stat.gov.pl/api/v1"
VARIABLE_ID = 72305  # Total population
HEADERS = {"Accept": "application/json"}

# Preferred year order: try 2024 first, fall back to 2023
YEARS_TO_TRY = [2024, 2023, 2022]


def fetch_json(url, params=None):
    """Fetch JSON from the BDL API with retries."""
    for attempt in range(3):
        try:
            resp = requests.get(url, params=params, headers=HEADERS, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                print(f"  Rate limited, waiting 2s... (attempt {attempt+1})")
                time.sleep(2)
                continue
            else:
                print(f"  HTTP {resp.status_code} for {url}")
                if attempt < 2:
                    time.sleep(1)
                    continue
                return None
        except requests.exceptions.RequestException as e:
            print(f"  Request error: {e}")
            if attempt < 2:
                time.sleep(1)
                continue
            return None
    return None


def fetch_population_by_level(unit_level, year):
    """
    Fetch population data for a given unit level with pagination.
    unit_level=2 -> województwa (16 records)
    unit_level=5 -> powiaty (~380 records)
    """
    all_results = []
    page = 0
    page_size = 100

    while True:
        params = {
            "unit-level": unit_level,
            "year": year,
            "format": "json",
            "page-size": page_size,
            "page": page,
        }
        url = f"{BASE_URL}/data/by-variable/{VARIABLE_ID}"
        print(f"  Fetching page {page} for level {unit_level}, year {year}...")

        data = fetch_json(url, params)
        if data is None:
            print(f"  Failed to fetch page {page}")
            break

        results = data.get("results", [])
        if not results:
            if page == 0:
                print(f"  No data found for year {year}, level {unit_level}")
                return None
            break

        all_results.extend(results)
        total = data.get("totalRecords", 0)
        print(f"  Got {len(results)} records (total so far: {len(all_results)}/{total})")

        # Check if there are more pages
        links = data.get("links", {}) if isinstance(data.get("links"), dict) else {}
        # Sometimes links is a list of dicts with "rel" and "href"
        if isinstance(data.get("links"), list):
            has_next = any(
                link.get("rel") == "next" or link.get("rel") == "self"
                for link in data.get("links", [])
                if link.get("rel") == "next"
            )
        else:
            has_next = False

        if len(all_results) >= total:
            break

        page += 1
        time.sleep(0.3)  # Be nice to the API

    return all_results


def parse_population_results(results):
    """Parse API results into a clean dict: {name: {population, year, unit_id}}."""
    parsed = {}
    for item in results:
        name = item.get("name", "")
        unit_id = item.get("id", "")
        values = item.get("values", [])
        if values:
            # Take the most recent year's value
            val = values[-1]
            parsed[name] = {
                "population": val.get("val"),
                "year": val.get("year"),
                "unit_id": unit_id,
            }
    return parsed


def title_case_polish(name):
    """Convert 'MAŁOPOLSKIE' to 'Małopolskie', handling Polish chars."""
    # The API returns names in ALL CAPS, convert to title case
    return name.title() if name == name.upper() else name


def main():
    output = {}
    api_success = False

    # ---- Fetch województwa (voivodeships) ----
    print("=" * 60)
    print("Fetching województwa (voivodeships) population...")
    print("=" * 60)

    woj_data = None
    woj_year = None
    for year in YEARS_TO_TRY:
        results = fetch_population_by_level(unit_level=2, year=year)
        if results and len(results) == 16:
            woj_data = results
            woj_year = year
            print(f"\n  SUCCESS: Got all 16 województwa for year {year}")
            break
        elif results:
            woj_data = results
            woj_year = year
            print(f"\n  Got {len(results)} województwa for year {year}")
            break

    if woj_data:
        api_success = True
        parsed_woj = parse_population_results(woj_data)
        # Build clean output
        population_woj = {}
        for name, info in sorted(parsed_woj.items()):
            clean_name = title_case_polish(name)
            population_woj[clean_name] = {
                "population": info["population"],
                "year": int(info["year"]),
                "unit_id": info["unit_id"],
            }
        output["population_woj"] = population_woj
        output["data_year_woj"] = woj_year
        output["source"] = "GUS BDL API (https://bdl.stat.gov.pl/api/v1/)"
        output["variable_id"] = VARIABLE_ID
        output["variable_description"] = "Total population (ludność ogółem)"

        # Print summary
        total_pop = sum(v["population"] for v in population_woj.values())
        print(f"\n  Total population of Poland: {total_pop:,}")
        print(f"\n  Województwa ({len(population_woj)}):")
        for name, info in sorted(population_woj.items(), key=lambda x: -x[1]["population"]):
            print(f"    {name}: {info['population']:,}")
    else:
        print("\n  WARNING: Could not fetch voivodeship data from API.")
        print("  Using fallback hardcoded data.")

    # ---- Fetch powiaty (counties) ----
    print("\n" + "=" * 60)
    print("Fetching powiaty (counties) population...")
    print("=" * 60)

    powiat_data = None
    powiat_year = None
    for year in YEARS_TO_TRY:
        results = fetch_population_by_level(unit_level=5, year=year)
        if results and len(results) > 300:
            powiat_data = results
            powiat_year = year
            print(f"\n  SUCCESS: Got {len(results)} powiaty for year {year}")
            break
        elif results:
            powiat_data = results
            powiat_year = year
            print(f"\n  Got {len(results)} powiaty for year {year}")
            break

    if powiat_data:
        parsed_powiaty = parse_population_results(powiat_data)
        population_powiaty = {}
        for name, info in sorted(parsed_powiaty.items()):
            clean_name = title_case_polish(name)
            population_powiaty[clean_name] = {
                "population": info["population"],
                "year": int(info["year"]),
                "unit_id": info["unit_id"],
            }
        output["population_powiaty"] = population_powiaty
        output["data_year_powiaty"] = powiat_year
        output["powiaty_count"] = len(population_powiaty)

        total_powiat_pop = sum(v["population"] for v in population_powiaty.values())
        print(f"\n  Total powiaty population: {total_powiat_pop:,}")
        print(f"  Number of powiaty: {len(population_powiaty)}")

        # Show top 10
        top10 = sorted(population_powiaty.items(), key=lambda x: -x[1]["population"])[:10]
        print(f"\n  Top 10 powiaty by population:")
        for name, info in top10:
            print(f"    {name}: {info['population']:,}")
    else:
        print("\n  WARNING: Could not fetch powiat data from API.")

    # ---- Fallback if API failed ----
    if not api_success:
        print("\n  Using hardcoded fallback data for województwa.")
        fallback_woj = {
            "Dolnośląskie": {"population": 2891000, "year": 2023, "unit_id": "030200000000"},
            "Kujawsko-Pomorskie": {"population": 2049000, "year": 2023, "unit_id": "040400000000"},
            "Lubelskie": {"population": 2095000, "year": 2023, "unit_id": "060600000000"},
            "Lubuskie": {"population": 1007000, "year": 2023, "unit_id": "020800000000"},
            "Łódzkie": {"population": 2437000, "year": 2023, "unit_id": "051000000000"},
            "Małopolskie": {"population": 3410000, "year": 2023, "unit_id": "011200000000"},
            "Mazowieckie": {"population": 5425000, "year": 2023, "unit_id": "071400000000"},
            "Opolskie": {"population": 972000, "year": 2023, "unit_id": "031600000000"},
            "Podkarpackie": {"population": 2098000, "year": 2023, "unit_id": "061800000000"},
            "Podlaskie": {"population": 1162000, "year": 2023, "unit_id": "062000000000"},
            "Pomorskie": {"population": 2346000, "year": 2023, "unit_id": "042200000000"},
            "Śląskie": {"population": 4474000, "year": 2023, "unit_id": "012400000000"},
            "Świętokrzyskie": {"population": 1215000, "year": 2023, "unit_id": "052600000000"},
            "Warmińsko-Mazurskie": {"population": 1408000, "year": 2023, "unit_id": "042800000000"},
            "Wielkopolskie": {"population": 3498000, "year": 2023, "unit_id": "023000000000"},
            "Zachodniopomorskie": {"population": 1682000, "year": 2023, "unit_id": "023200000000"},
        }
        output["population_woj"] = fallback_woj
        output["data_year_woj"] = 2023
        output["source"] = "Hardcoded fallback (GUS approximate data)"
        output["variable_id"] = VARIABLE_ID

    # ---- Postal code prefix to województwo mapping ----
    postal_to_woj = {}
    mapping_ranges = [
        (range(0, 8), "Mazowieckie"),
        (range(8, 9), "Mazowieckie"),
        (range(9, 10), "Mazowieckie"),
        (range(10, 15), "Warmińsko-Mazurskie"),
        (range(15, 20), "Podlaskie"),
        (range(20, 25), "Lubelskie"),
        (range(25, 30), "Świętokrzyskie"),
        (range(30, 35), "Małopolskie"),
        (range(35, 40), "Podkarpackie"),
        (range(40, 45), "Śląskie"),
        (range(45, 50), "Opolskie"),
        (range(50, 60), "Dolnośląskie"),
        (range(60, 65), "Wielkopolskie"),
        (range(65, 70), "Lubuskie"),
        (range(70, 80), "Zachodniopomorskie"),
        (range(80, 85), "Pomorskie"),
        (range(85, 90), "Kujawsko-Pomorskie"),
        (range(90, 100), "Łódzkie"),
    ]

    for r, woj in mapping_ranges:
        for code in r:
            postal_to_woj[f"{code:02d}"] = woj

    output["postal_to_woj_mapping"] = postal_to_woj

    # Also add a human-readable range description
    output["postal_ranges"] = {
        "00-09": "Mazowieckie",
        "10-14": "Warmińsko-Mazurskie",
        "15-19": "Podlaskie",
        "20-24": "Lubelskie",
        "25-29": "Świętokrzyskie",
        "30-34": "Małopolskie",
        "35-39": "Podkarpackie",
        "40-44": "Śląskie",
        "45-49": "Opolskie",
        "50-59": "Dolnośląskie",
        "60-64": "Wielkopolskie",
        "65-69": "Lubuskie",
        "70-79": "Zachodniopomorskie",
        "80-84": "Pomorskie",
        "85-89": "Kujawsko-Pomorskie",
        "90-99": "Łódzkie",
    }

    # ---- Save to JSON ----
    output_path = os.path.join(ROOT, "gus_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"Data saved to: {output_path}")
    print(f"{'=' * 60}")

    # Summary
    woj_count = len(output.get("population_woj", {}))
    powiat_count = len(output.get("population_powiaty", {}))
    postal_count = len(output.get("postal_to_woj_mapping", {}))
    print(f"\nSummary:")
    print(f"  - {woj_count} województwa with population data")
    print(f"  - {powiat_count} powiaty with population data")
    print(f"  - {postal_count} postal code prefix mappings")
    print(f"  - Source: {output.get('source', 'unknown')}")


if __name__ == "__main__":
    main()
