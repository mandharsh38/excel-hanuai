import requests
from collections import defaultdict
import json

# survey id
survey_id = 242

api_url = f"https://ndd.roadathena.com/api/surveys/{survey_id}"
headers = {"Security-Password": "admin@123"}

response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    roads = data.get("roads", [])
    print(f"Found {len(roads)} roads.")
    
    with open(f"dump.py", "w") as f:
        f.write(json.dumps(roads, indent=4))

else:
    print(f"Failed to fetch data — Status: {response.status_code}")
    print(response.text)
