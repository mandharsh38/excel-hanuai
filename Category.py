import os
import json

def update_asset_type_in_json(input_folder, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):  # Process only JSON files
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Load the JSON file
            with open(input_path, "r") as file:
                data = json.load(file)

            # Update the 'Asset type' field
            for asset in data.get("assets", []):
                if asset.get("Asset type") == "FADED_INFORMATORY_SIGNS":
                    asset["Asset type"] = "DAMAGED_SIGNS"

            # Write the modified JSON to the output folder
            with open(output_path, "w") as file:
                json.dump(data, file, indent=4)

            print(f"Processed: {filename}")

# Input and Output folder paths
input_folder = "jsons2"   # Replace with your input folder path
output_folder = "jsons3" # Replace with your output folder path

# Call the function
update_asset_type_in_json(input_folder, output_folder)
