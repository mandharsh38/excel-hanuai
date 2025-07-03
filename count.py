# import os
# import json
# from collections import defaultdict

# # Path to your folder containing JSON files
# FOLDER_PATH = "jsons"  # Replace with your actual path

# # Dictionary to store total counts per asset type
# asset_type_counts = defaultdict(int)

# # Loop through each file in the folder
# for filename in os.listdir(FOLDER_PATH):
#     if filename.endswith(".json"):
#         file_path = os.path.join(FOLDER_PATH, filename)
#         with open(file_path, "r", encoding="utf-8") as f:
#             try:
#                 data = json.load(f)
#                 assets = data.get("assets", [])
#                 for asset in assets:
#                     asset_type = asset.get("Asset type")
#                     if asset_type:
#                         asset_type_counts[asset_type] += 1
#             except json.JSONDecodeError:
#                 print(f"Error decoding JSON in file: {filename}")

# # Print the counts
# print("Total count of each asset type:")
# for asset_type, count in asset_type_counts.items():
#     print(f"{asset_type}: {count}")

# # Optional: print total asset count overall
# print(f"\nTotal assets across all files: {sum(asset_type_counts.values())}")




# 2nd code new furniture json get


import os
import json
from collections import defaultdict

# Path to your folder containing JSON files
FOLDER_PATH = "jsons"  # Replace with your actual path

# Dictionary to store total counts per asset type
asset_type_counts = defaultdict(int)

# Loop through each file in the folder
for filename in os.listdir(FOLDER_PATH):
    if filename.endswith(".json"):
        file_path = os.path.join(FOLDER_PATH, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                assets = data.get("assets", [])
                for asset in assets:
                    distance = asset.get("Distance")
                    asset_type = asset.get("Asset type")
                    if asset_type and distance is not None:
                        asset_type_counts[asset_type] += 1
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {filename}")

# Print the counts
print("Total count of each asset type (excluding Distance=null):")
for asset_type, count in asset_type_counts.items():
    print(f"{asset_type}: {count}")

# Optional: print total asset count overall
print(f"\nTotal valid assets across all files: {sum(asset_type_counts.values())}")
