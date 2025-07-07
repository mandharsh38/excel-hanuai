import requests
from collections import defaultdict

# survey id
survey_id = 43

api_url = f"https://ndd.roadathena.com/api/surveys/{survey_id}"
headers = {"Security-Password": "admin@123"}

valid_types = {"mcw rhs", "mcw lhs", "irl", "irr", "srl", "srr", "lrr", "lrl", "sll", "tl", "tr", "cr", "cl"}
categorized_ids = defaultdict(list)

response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    roads = data.get("roads", [])
    print(f"Found {len(roads)} roads.")

    for road_entry in roads:
        road_id = road_entry.get("id")
        road_info = road_entry.get("road")

        if isinstance(road_info, dict):
            road_type_raw = road_info.get("road_type")
            road_type = road_type_raw.lower() if isinstance(road_type_raw, str) else ""

            if road_id and road_type in valid_types:
                categorized_ids[road_type].append(road_id)
        else:
            print(f"Skipping road ID {road_id} — 'road' is missing or invalid.")


    print("\nCategorized Road IDs:")
    for key in sorted(valid_types):
        ids = sorted(categorized_ids.get(key, []))
        print(f"{key.upper()} ({len(ids)}): {ids}")

else:
    print(f"Failed to fetch data — Status: {response.status_code}")
    print(response.text)
