import json
import os
import requests

api_base_url = "https://ndd.roadathena.com/api/surveys/roads/"
file_base_url = "https://ndd.roadathena.com"
headers = {"Security-Password": "admin@123"}

#ids = list(range(8855,8898)) 
# ids =[10510, 10511]

import id 
ids= id.ids
# ids=[3803]

output_path = "jsons"

if not os.path.exists(output_path):
    os.makedirs(output_path)

def update_json_file(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    updated_assets = []
    new_anomalies = data.get('anomalies', [])

    for asset in data.get('assets', []):
        if asset.get("Asset type") == "DAMAGED_SIGN":
            anomaly = {
                "Anomaly number": asset.get("Assets number"),
                "Timestamp on processed video": asset.get("Timestamp on processed video"),
                "Anomaly type": asset.get("Asset type"),
                "Side": asset.get("Side"),
                "Latitude": asset.get("Latitude"),
                "Longitude": asset.get("Longitude"),
                "Distance": asset.get("Distance"),
                "Length": asset.get("Length"),
                "Average width": asset.get("Average width"),
                "Remarks": asset.get("Remarks"),
                "image": asset.get("image"),
                "category": asset.get("category")
            }
            new_anomalies.append(anomaly)
        else:
            updated_assets.append(asset)

    data['assets'] = updated_assets
    data['anomalies'] = new_anomalies

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Updated JSON file: {filepath}")

# Download and process each file
for file_id in ids:
    try:
        api_url = f"{api_base_url}{file_id}"
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            json_data = response.json()

            if 'furniture_json' in json_data:
                json_file_url = json_data['furniture_json']
                full_file_url = f"{file_base_url}{json_file_url}"

                file_response = requests.get(full_file_url, headers=headers)
                if file_response.status_code == 200:
                    json_file_path = os.path.join(output_path, f"road_{file_id}.json")
                    with open(json_file_path, 'wb') as json_file:
                        json_file.write(file_response.content)
                    print(f"✅ Downloaded: road_{file_id}.json")

                    # Update the JSON file to move DAMAGED_SIGN into anomalies
                    update_json_file(json_file_path)
                else:
                    print(f"❌ Failed to download JSON file for ID {file_id} — Status: {file_response.status_code}")
            else:
                print(f"⚠️ 'furniture_json' key not found for ID {file_id}")
        else:
            print(f"❌ Failed to fetch metadata for ID {file_id} — Status: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"❌ Error processing ID {file_id}: {str(e)}")

