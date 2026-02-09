import sys
import csv
import time
import countries.country_queries as cntry


def extract(flnm: str) -> list:
    """Read CSV file and return list of rows"""
    country_list = []
    with open(flnm, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            country_list.append(row)
    return country_list


def transform(country_list: list) -> list:
    """Convert list to dictionaries with proper field mapping"""
    rev_list = []
    col_names = country_list.pop(0)  # Remove header row

    for country in country_list:
        country_dict = {}
        for i, fld in enumerate(col_names):
            country_dict[fld] = country[i]
        rev_list.append(country_dict)

    return rev_list


def load(rev_list: list):
    """Insert each country into MongoDB"""
    success_count = 0
    error_count = 0
    created_count = 0
    updated_count = 0

    for country in rev_list:
        try:
            # Check if country already exists
            country_id = country.get('_id')
            name = country.get('name')
            capital = country.get('capital')

            # Check if it exists before adding
            try:
                cntry.get_country(country_id)
                action = "Updated"
                updated_count += 1
            except ValueError:
                action = "Created"
                created_count += 1

            # Extract optional fields (nat_dish, pop_dish_1, pop_dish_2)
            extra_fields = {
                k: v for k, v in country.items()
                if k not in ['_id', 'name', 'capital']
            }

            # Call add_country with extra fields
            cntry.add_country(country_id, name, capital, **extra_fields)

            print(f"✓ {action}: {name} ({country_id})")
            print(f"   Capital: {capital}")
            print(f"   National Dish: {extra_fields.get('nat_dish', 'N/A')}")
            dishes = f"{extra_fields.get('pop_dish_1', 'N/A')}, {extra_fields.get('pop_dish_2', 'N/A')}"
            print(f"   Popular Dishes: {dishes}")
            success_count += 1

        except Exception as e:
            print(f"✗ Error loading {country.get('name', 'Unknown')}: {e}")
            error_count += 1

    # Force reload cache after ALL inserts are done
    time.sleep(0.5)
    cntry.load_cache()

    print(f"\n{'=' * 60}")
    print("Summary:")
    print(f"  Created: {created_count}")
    print(f"  Updated: {updated_count}")
    print(f"  Failed: {error_count}")
    print(f"  Total countries in database: {cntry.num_countries()}")
    print(f"{'=' * 60}")


def main():
    # exit(1)  # ← COMMENT THIS OUT!
    if len(sys.argv) < 2:
        print("Usage: python load_countries.py <csv_file>")
        print("Example: python load_countries.py data/countries.csv")
        sys.exit(1)

    print(f"Loading countries from: {sys.argv[1]}\n")
    country_list = extract(sys.argv[1])
    print(f"Extracted {len(country_list) - 1} countries from CSV")

    rev_list = transform(country_list)
    print(f"Transformed {len(rev_list)} country records\n")

    load(rev_list)


if __name__ == "__main__":
    main()
