import sys
import csv
import time
import cities.cities_queries as ct


def extract(flnm: str) -> list:
    rows = []
    with open(flnm, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rows.append(row)
    return rows


def transform(rows: list) -> list:
    rev_list = []
    col_names = rows.pop(0)

    for r in rows:
        city_dict = {}
        for i, fld in enumerate(col_names):
            city_dict[fld] = r[i].strip()

        # Normalize codes (helps avoid duplicates like "ny" vs "NY")
        city_dict["country_code"] = city_dict.get("country_code", "").strip().upper()
        city_dict["state_code"] = city_dict.get("state_code", "").strip().upper()

        rev_list.append(city_dict)

    return rev_list


def load(rev_list: list):
    created_count = 0
    updated_count = 0
    error_count = 0

    for city in rev_list:
        try:
            city_name = city.get("city")
            state_code = city.get("state_code")
            country_code = city.get("country_code")
            rec_restaurant = city.get("rec_restaurant")

            # Exists check using your current API
            try:
                ct.read_one(city_name, state_code, country_code)
                action = "Updated"
                updated_count += 1
            except ValueError:
                action = "Created"
                created_count += 1

            extra_fields = {
                k: v for k, v in city.items()
                if k not in ["city", "state_code", "country_code", "rec_restaurant"]
            }

            # Upsert (no custom _id)
            ct.add_city(country_code, state_code, city_name, rec_restaurant, **extra_fields)

            print(f"✓ {action}: {city_name}")
            print(f"   Country: {country_code}")
            print(f"   State Code: {state_code}")
            print(f"   Recommended Restaurant: {rec_restaurant}")

        except Exception as e:
            print(f"✗ Error loading {city.get('city', 'Unknown')}: {e}")
            error_count += 1

    time.sleep(0.5)
    ct.load_cache()

    print(f"\n{'=' * 60}")
    print("Summary:")
    print(f"  Created: {created_count}")
    print(f"  Updated: {updated_count}")
    print(f"  Failed: {error_count}")
    print(f"  Total cities in database: {ct.count()}")
    print(f"{'=' * 60}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python load_cities.py <csv_file>")
        print("Example: python load_cities.py data/cities.csv")
        sys.exit(1)

    print(f"Loading cities from: {sys.argv[1]}\n")
    rows = extract(sys.argv[1])
    print(f"Extracted {len(rows) - 1} cities from CSV")

    rev_list = transform(rows)
    print(f"Transformed {len(rev_list)} city records\n")

    load(rev_list)


if __name__ == "__main__":
    main()
