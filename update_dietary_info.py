#!/usr/bin/env python3
"""
Update dietary information for country dishes in MongoDB.
Adds dietary classification arrays (vegetarian, meat, seafood, vegan) to each dish.
"""

import os
from pymongo import MongoClient


def get_mongo_client():
    """Connect to MongoDB Atlas using environment variables."""
    mongo_user = os.environ.get('MONGO_USER_NM', 'your_username')
    mongo_passwd = os.environ.get('MONGO_PASSWD', 'your_password')
    mongo_host = os.environ.get('MONGO_HOST', 'cluster0.dsx6edq.mongodb.net')

    connection_string = f"mongodb+srv://{mongo_user}:{mongo_passwd}@{mongo_host}/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"

    try:
        client = MongoClient(connection_string)
        # Test connection
        client.admin.command('ping')
        print("✓ Successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(f"✗ Error connecting to MongoDB: {e}")
        return None


def update_dietary_info():
    """Update all countries with dietary information."""

    # Dietary classifications for each country
    dietary_updates = {
        "MAR": {  # Morocco
            "nat_dish_dietary": ["vegetarian", "meat"],
            "pop_dish_1_dietary": ["vegetarian", "meat"],
            "pop_dish_2_dietary": ["meat"]
        },
        "IND": {  # India
            "nat_dish_dietary": ["vegetarian"],
            "pop_dish_1_dietary": ["vegetarian", "meat"],
            "pop_dish_2_dietary": ["meat"]
        },
        "SGP": {  # Singapore
            "nat_dish_dietary": ["meat"],
            "pop_dish_1_dietary": ["vegetarian", "meat", "seafood"],
            "pop_dish_2_dietary": ["vegetarian"]
        },
        "BGD": {  # Bangladesh
            "nat_dish_dietary": ["seafood"],
            "pop_dish_1_dietary": ["meat"],
            "pop_dish_2_dietary": ["meat"]
        },
        "PHL": {  # Philippines
            "nat_dish_dietary": ["meat"],
            "pop_dish_1_dietary": ["meat", "seafood", "vegetarian"],
            "pop_dish_2_dietary": ["vegetarian", "meat"]
        },
        "CHN": {  # China
            "nat_dish_dietary": ["meat"],
            "pop_dish_1_dietary": ["meat", "vegetarian"],
            "pop_dish_2_dietary": ["meat", "seafood", "vegetarian"]
        },
        "KOR": {  # South Korea
            "nat_dish_dietary": ["vegetarian"],
            "pop_dish_1_dietary": ["meat"],
            "pop_dish_2_dietary": ["meat", "vegetarian"]
        },
        "JPN": {  # Japan
            "nat_dish_dietary": ["vegetarian", "meat", "seafood"],
            "pop_dish_1_dietary": ["vegetarian"],
            "pop_dish_2_dietary": ["seafood"]
        },
        "MEX": {  # Mexico
            "nat_dish_dietary": ["meat", "vegetarian"],
            "pop_dish_1_dietary": ["vegetarian", "meat"],
            "pop_dish_2_dietary": ["vegetarian", "meat"]
        },
        "USA": {  # United States
            "nat_dish_dietary": ["meat"],
            "pop_dish_1_dietary": ["vegetarian", "meat"],
            "pop_dish_2_dietary": ["meat"]
        }
    }

    # Connect to MongoDB
    client = get_mongo_client()
    if not client:
        return

    db = client['sensDB']
    countries_collection = db['countries']

    # Update each country
    updated_count = 0
    failed_count = 0

    for country_id, dietary_data in dietary_updates.items():
        try:
            result = countries_collection.update_one(
                {"_id": country_id},
                {"$set": dietary_data}
            )

            if result.modified_count > 0:
                print(f"✓ Updated {country_id} with dietary info")
                updated_count += 1
            else:
                print(f"⚠ {country_id} not found or already up to date")
        except Exception as e:
            print(f"✗ Error updating {country_id}: {e}")
            failed_count += 1

    # Summary
    print("\n" + "=" * 50)
    print("Update complete!")
    print(f"  ✓ Successfully updated: {updated_count}")
    print(f"  ✗ Failed: {failed_count}")
    print("=" * 50)

    client.close()


if __name__ == "__main__":
    print("=" * 50)
    print("Updating Country Dietary Information")
    print("=" * 50 + "\n")

    update_dietary_info()
