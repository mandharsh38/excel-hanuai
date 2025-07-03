
import json
from datetime import datetime
# Load the JSON data
with open('first.json', 'r') as f:
    json_data = json.load(f)

processed_data = []

for item in json_data:
    # Format the timestamp into date and time
    timestamp = datetime.strptime(item["Timestamp on processed video"], "%Y-%m-%d %H:%M:%S")
    formatted_date = timestamp.strftime("%Y-%m-%d")
    formatted_time = timestamp.strftime("%H:%M:%S")
    
    # Create a new structured entry
    processed_entry = {
        "Assets number": item["Assets number"],
        "Date": formatted_date,
        "Time": formatted_time,
        "Asset type": item["Asset type"],
        "Category": item["category"],
        "Side": item["Side"],
        "Location": {
            "Latitude": item["Latitude"],
            "Longitude": item["Longitude"]
        },
        "Distance": item["Distance"],
        "Dimensions": {
            "Length": item["Length"],
            "Average width": item["Average width"]
        },
        "Remarks": item["Remarks"],
        "Image URL": item["image"]
    }
    
    processed_data.append(processed_entry)

# Save the processed data to a new JSON file
output_file = "processed_assets_report.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(processed_data, file, indent=4)

print(f"Processed data has been saved to {output_file}.")
