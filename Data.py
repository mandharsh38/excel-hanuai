import os
import json
import requests
from collections import defaultdict

# Folder containing JSON files
FOLDER_PATH = 'jsons'  # Replace with your actual folder path

# Expected categories for asset/anomaly types
EXPECTED_CATEGORIES = {
    'INFORMATORY_SIGNS': 'Informatory Signs',
    'HAZARD': 'Cautionary Signs',
    'CHEVRON': 'Cautionary Signs',
    'PROHIBITORY_MANDATORY_SIGNS': 'Mandatory Signs',
    'CAUTIONARY_WARNING_SIGNS': 'Cautionary Signs',
}

# Function to validate coordinates
def is_valid_coordinate(value):
    return value not in [None, 0, 0.0, "", "0", "0.0"]

# Fetch road name from API based on roadId
def fetch_road_name(road_id):
    api_url = f"https://ndd.roadathena.com/api/surveys/roads/{road_id}"

    response = requests.get(api_url, headers={"Security-Password": "admin@123"})
    response.raise_for_status()
    road_data = response.json()
    name = road_data["road"]["name"]
    print (name)
    return road_data.get("road", {}).get("name", "Unknown road name")
    

def check_entry(entry, entry_type, file_name, counts):
    entry_label = entry.get(entry_type)
    category = entry.get('category')
    lat = entry.get('Latitude')
    lng = entry.get('Longitude')

    # Only count asset types with valid coordinates
    if entry_type == 'Asset type':
        if not (is_valid_coordinate(lat) and is_valid_coordinate(lng)):
            # Skipping invalid coordinate asset - no count
            return
        counts['asset'] += 1

    # Validate expected category
    if entry_label in EXPECTED_CATEGORIES:
        expected_category = EXPECTED_CATEGORIES[entry_label]
        if category != expected_category:
            print(
                f"[ERROR] In {file_name} -> {entry_type} '{entry_label}' "
                f"has wrong category '{category}', expected '{expected_category}'"
            )

def validate_json(file_path):
    counts = {'asset': 0}
    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"[INVALID JSON] {file_path}")
            return None, 0

        filename = os.path.basename(file_path)

        for anomaly in data.get('anomalies', []):
            check_entry(anomaly, 'Anomaly type', filename, counts)

        for asset in data.get('assets', []):
            check_entry(asset, 'Asset type', filename, counts)

    return filename, counts['asset']

def main():
    for file in os.listdir(FOLDER_PATH):
        if file.endswith('.json'):
            file_path = os.path.join(FOLDER_PATH, file)
            filename, asset_count = validate_json(file_path)
            if filename is None:
                continue

            # Assuming filename contains roadId like "road_6163.json"
            # Extract the road ID number from filename
            import re
            match = re.search(r'(\d+)', filename)
            if match:
                road_id = match.group(1)
                road_name = fetch_road_name(road_id)
            else:
                road_id = "Unknown"
                road_name = "Unknown"

            print(f"File: {filename}")
            print(f"Road ID: {road_id}")
            print(f"Total Asset Count (Valid Lat/Lng): {asset_count}")
            print(f"Road Name from API: {road_name}")
            print("-" * 40)

if __name__ == '_main_':
     main()