import os
import json
import id

def update_side_in_json(input_folder, output_folder):
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

            # for a in (data.get(
            #     "anomalies",
            #     []
            # )):
            #     print(a.get("Side"))
            #     break
            # break

            # Update the 'Side' field
            for asset in data.get("assets", []):
                if id.mcw_id: 
                    if asset.get("Side") == "Overhead":
                        asset["Side"] = "Avenue"
                    if asset.get("Side") == "Center":
                        asset["Side"] = "Median"   
                    if asset.get("Side") == "Left":
                        asset["Side"] = "Avenue"   
                    if asset.get("Side") == "Right":
                        asset["Side"] = "Median"     
                else: 
                    if asset.get("Side") == "Avenue":
                        asset["Side"] = "Left"
                    if asset.get("Side") == "Median":
                       asset["Side"] = "Right"
                    if asset.get("Side") == "Center":
                       asset["Side"] = "Right"

                    
            for anomaly in data.get("anomalies", []):
                if id.mcw_id: 
                    if anomaly.get("Side") == "Overhead":
                        anomaly["Side"] = "Avenue"
                    if anomaly.get("Side") == "Center":
                        anomaly["Side"] = "Median"   
                    if anomaly.get("Side") == "Left":
                        anomaly["Side"] = "Avenue"   
                    if anomaly.get("Side") == "Right":
                        anomaly["Side"] = "Median"     
                else: 
                    if anomaly.get("Side") == "Avenue":
                        anomaly["Side"] = "Left"
                    if anomaly.get("Side") == "Median":
                       anomaly["Side"] = "Right"
                    if anomaly.get("Side") == "Center":
                       anomaly["Side"] = "Right"

            # Write the modified JSON to the output folder
            with open(output_path, "w") as file:
                json.dump(data, file, indent=4)

            print(f"Processed: {filename}")

# Input and Output folder paths
input_folder = "jsons"  # Replace with your input folder path
output_folder = "jsons"  # Replace with your output folder path

# Call the function
if __name__ == "__main__":
    update_side_in_json(input_folder, output_folder)

