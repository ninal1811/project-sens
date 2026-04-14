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


def update_states_food():
    """Update all states with food names and dietary info."""

    states_food_data = {
        # USA states
        'MA': {'food_name': 'Clam Chowder', 'food_dietary': ['seafood']},
        'PA': {'food_name': 'Philly Cheesesteak', 'food_dietary': ['meat']},
        'ME': {'food_name': 'Lobster Roll', 'food_dietary': ['seafood']},
        'GA': {'food_name': 'Southern Fried Chicken', 'food_dietary': ['meat']},
        'SC': {'food_name': 'Shrimp and Grits', 'food_dietary': ['seafood']},
        'NY': {'food_name': 'New York Pizza', 'food_dietary': ['vegetarian', 'meat']},

        # Bangladesh divisions
        'BD-A': {'food_name': 'Hilsa Fish Curry', 'food_dietary': ['seafood']},
        'BD-B': {'food_name': 'Mezban Beef Curry', 'food_dietary': ['meat']},
        'BD-C': {'food_name': 'Kacchi Biryani', 'food_dietary': ['meat']},
        'BD-D': {'food_name': 'Chingri Malai Curry', 'food_dietary': ['seafood']},
        'BD-H': {'food_name': 'Monda Sweet', 'food_dietary': ['vegetarian']},
        'BD-E': {'food_name': 'Kalai Ruti', 'food_dietary': ['vegetarian']},
        'BD-F': {'food_name': 'Bhapa Pitha', 'food_dietary': ['vegetarian']},
        'BD-G': {'food_name': 'Satkora Curry', 'food_dietary': ['meat']},

        # Philippines regions
        'LUZ': {'food_name': 'Sinigang', 'food_dietary': ['meat', 'seafood', 'vegetarian']},
        'VIS': {'food_name': 'Lechon', 'food_dietary': ['meat']},
        'MIN': {'food_name': 'Beef Rendang', 'food_dietary': ['meat']},

        # India states
        'AP': {'food_name': 'Hyderabadi Biryani', 'food_dietary': ['meat']},
        'KA': {'food_name': 'Masala Dosa', 'food_dietary': ['vegetarian']},
        'KL': {'food_name': 'Kerala Fish Curry', 'food_dietary': ['seafood']},
        'TN': {'food_name': 'Chettinad Chicken', 'food_dietary': ['meat']},
        'TG': {'food_name': 'Sarva Pindi', 'food_dietary': ['vegetarian']},

        # Mexico states
        'MEX': {'food_name': 'Tacos al Pastor', 'food_dietary': ['meat']},
        'PUE': {'food_name': 'Mole Poblano', 'food_dietary': ['meat', 'vegetarian']},
        'JAL': {'food_name': 'Birria', 'food_dietary': ['meat']},
        'OAX': {'food_name': 'Tlayuda', 'food_dietary': ['vegetarian', 'meat']},

        # Morocco regions
        'TTA': {'food_name': 'Seafood Pastilla', 'food_dietary': ['seafood']},
        'ORI': {'food_name': 'Berkoukes', 'food_dietary': ['vegetarian', 'meat']},
        'FEM': {'food_name': 'Rfissa', 'food_dietary': ['meat']},
        'RSK': {'food_name': 'Couscous', 'food_dietary': ['vegetarian', 'meat']},
        'BMK': {'food_name': 'Tagine', 'food_dietary': ['vegetarian', 'meat', 'seafood']},
        'CAS': {'food_name': 'Harira', 'food_dietary': ['vegetarian', 'meat']},
        'MAS': {'food_name': 'Tangia', 'food_dietary': ['meat']},
        'DRT': {'food_name': 'Medfouna', 'food_dietary': ['meat']},
        'SOM': {'food_name': 'Argan Oil Amlou', 'food_dietary': ['vegetarian', 'vegan']},
        'GON': {'food_name': 'Taguella Bread', 'food_dietary': ['vegetarian']},
        'LSH': {'food_name': 'Sahrawi Tea', 'food_dietary': ['vegetarian', 'vegan']},
        'DOD': {'food_name': 'Grilled Fish', 'food_dietary': ['seafood']},

        # Singapore
        'Singapore': {'food_name': 'Hainanese Chicken Rice', 'food_dietary': ['meat']},

        # Japan prefectures
        'JP-A': {'food_name': 'Miso Ramen', 'food_dietary': ['meat', 'vegetarian']},
        'JP-B': {'food_name': 'Gyutan', 'food_dietary': ['meat']},
        'JP-C': {'food_name': 'Sushi', 'food_dietary': ['seafood']},
        'JP-D': {'food_name': 'Miso Katsu', 'food_dietary': ['meat']},
        'JP-E': {'food_name': 'Takoyaki', 'food_dietary': ['seafood']},
        'JP-F': {'food_name': 'Okonomiyaki', 'food_dietary': ['meat', 'seafood', 'vegetarian']},
        'JP-G': {'food_name': 'Sanuki Udon', 'food_dietary': ['vegetarian', 'meat', 'seafood']},
        'JP-H': {'food_name': 'Hakata Ramen', 'food_dietary': ['meat']},

        # South Korea
        'KR-A': {'food_name': 'Korean BBQ', 'food_dietary': ['meat']},
        'KR-B': {'food_name': 'Makchang', 'food_dietary': ['meat']},
        'KR-C': {'food_name': 'Dwaeji Gukbap', 'food_dietary': ['meat']},
        'KR-D': {'food_name': 'Black Pork', 'food_dietary': ['meat']},

        # China regions
        'CN-A': {'food_name': 'Peking Duck', 'food_dietary': ['meat']},
        'CN-B': {'food_name': 'Buddha Jumps Over the Wall', 'food_dietary': ['seafood', 'meat']},
        'CN-C': {'food_name': 'Chongqing Hot Pot', 'food_dietary': ['meat', 'seafood', 'vegetarian']},
        'CN-D': {'food_name': 'Dim Sum', 'food_dietary': ['meat', 'seafood', 'vegetarian']},
        'CN-E': {'food_name': 'Lamb Kebab', 'food_dietary': ['meat']},
    }

    # Connect to MongoDB
    client = get_mongo_client()
    if not client:
        return

    db = client['sensDB']
    states_collection = db['states']

    # Update each state
    updated_count = 0
    failed_count = 0

    for state_code, food_data in states_food_data.items():
        try:
            result = states_collection.update_one(
                {"state_code": state_code},
                {"$set": food_data}
            )

            if result.modified_count > 0:
                print(f"✓ Updated {state_code} with food info")
                updated_count += 1
            elif result.matched_count > 0:
                print(f"⚠ {state_code} already up to date")
            else:
                print(f"✗ {state_code} not found in database")
                failed_count += 1
        except Exception as e:
            print(f"✗ Error updating {state_code}: {e}")
            failed_count += 1

    # Summary
    print("\n" + "=" * 50)
    print("States update complete!")
    print(f"  ✓ Successfully updated: {updated_count}")
    print(f"  ✗ Failed: {failed_count}")
    print("=" * 50)

    client.close()


if __name__ == "__main__":
    print("=" * 50)
    print("Updating Country Dietary Information")
    print("=" * 50 + "\n")

    update_dietary_info()

    print("\n" + "=" * 50)
    print("Updating States Food Information")
    print("=" * 50 + "\n")

    update_states_food()
