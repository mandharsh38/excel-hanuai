import os
import json

def clean_json_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in {filename}, skipping.")
                    continue

            modified = False

            for key in ["assets", "anomalies"]:
                if key in data and isinstance(data[key], list):
                    original_len = len(data[key])
                    data[key] = [entry for entry in data[key] if entry.get("Distance") is not None]
                    if len(data[key]) != original_len:
                        print(f"{filename}: Removed {original_len - len(data[key])} null Distance entries from {key}")
                        modified = True

            if modified:
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=4)

if __name__ == "__main__":
    folder_path = "jsons"
    clean_json_files(folder_path)
