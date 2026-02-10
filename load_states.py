import sys
import csv
import time
import states.states_queries as st


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
        state_dict = {}
        for i, fld in enumerate(col_names):
            state_dict[fld] = r[i].strip()

        # Normalize codes (helps avoid duplicates like "ny" vs "NY")
        state_dict["country_code"] = state_dict.get("country_code", "").strip().upper()
        state_dict["state_code"] = state_dict.get("state_code", "").strip().upper()

        rev_list.append(state_dict)

    return rev_list


def load(rev_list: list):
    created_count = 0
    updated_count = 0
    error_count = 0

    for state in rev_list:
        try:
            name = state.get("name")
            state_code = state.get("state_code")
            country_code = state.get("country_code")

            # Exists check using your current API
            try:
                st.read_one(state_code, country_code)
                action = "Updated"
                updated_count += 1
            except ValueError:
                action = "Created"
                created_count += 1

            extra_fields = {
                k: v for k, v in state.items()
                if k not in ["name", "state_code", "country_code"]
            }

            # Upsert (no custom _id)
            st.add_state(country_code, state_code, name, **extra_fields)

            print(f"✓ {action}: {name}")
            print(f"   Country: {country_code}")
            print(f"   State Code: {state_code}")

        except Exception as e:
            print(f"✗ Error loading {state.get('name', 'Unknown')}: {e}")
            error_count += 1

    time.sleep(0.5)
    st.load_cache()

    print(f"\n{'=' * 60}")
    print("Summary:")
    print(f"  Created: {created_count}")
    print(f"  Updated: {updated_count}")
    print(f"  Failed: {error_count}")
    print(f"  Total states in database: {st.count()}")
    print(f"{'=' * 60}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python load_states.py <csv_file>")
        print("Example: python load_states.py data/states.csv")
        sys.exit(1)

    print(f"Loading states from: {sys.argv[1]}\n")
    rows = extract(sys.argv[1])
    print(f"Extracted {len(rows) - 1} states from CSV")

    rev_list = transform(rows)
    print(f"Transformed {len(rev_list)} state records\n")

    load(rev_list)


if __name__ == "__main__":
    main()
