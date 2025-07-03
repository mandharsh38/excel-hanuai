import os
import json

# Folder containing your JSON files
FOLDER_PATH = "jsons"  # Replace with your actual path

# Target side values (case-insensitive and stripped)
target_sides = {"center", "overhead", "avenue", "median"}

# Set to collect matched sides
matched_sides = set()

# Loop through each JSON file
for filename in os.listdir(FOLDER_PATH):
    if filename.endswith(".json"):
        file_path = os.path.join(FOLDER_PATH, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for asset in data.get("assets", []):
                    side = asset.get("Side")
                    if side and side.strip().lower() in target_sides:
                        matched_sides.add(side.strip())
        except json.JSONDecodeError:
            print(f"❌ Error decoding JSON: {filename}")

# Print matched side values
print("Matched 'Side' values (Center, Overhead, Avenue, Median):")
for side in sorted(matched_sides):
    print(f"- {side}")
