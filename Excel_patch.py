import os
import json
import requests

def fetch_report_id_map(api_url, range_start, range_end):
    """Fetch the report IDs from the Reports API based on surveyroad within a specific range."""
    try:
        response = requests.get(api_url, headers = { "Security-Password": "admin@123" })
        response.raise_for_status()
        data = response.json()
        
        report_id_map = {}
        for item in data:
            surveyroad = str(item.get("surveyroad"))  
            report_id = item.get("id")

            if surveyroad.isdigit():
                surveyroad_int = int(surveyroad)
                if range_start <= surveyroad_int <= range_end:
                    report_id_map[surveyroad] = report_id
        
        return report_id_map
    
    except requests.RequestException as e:
        print(f"Failed to fetch report IDs from {api_url}: {e}")
        return {}

def find_excel_files(folder_path, road_ids):
    """Find and match Excel files in the folder with road IDs."""
    matched_files = {}
    for filename in os.listdir(folder_path):
        if filename.endswith("_formatted.xlsx"):
            name_part = filename.replace("_formatted.xlsx", "")
            if name_part.isdigit():  
                road_id = int(name_part)
                if road_id in road_ids:  
                    matched_files[road_id] = os.path.join(folder_path, filename)
    return matched_files

def patch_excel_files(api_base_url, report_id_map, matched_files):
    """Patch the Excel files to the API using report IDs."""
    for road_id, file_path in matched_files.items():
        report_id = report_id_map.get(str(road_id)) 
        if report_id is None:
            print(f"No report ID found for road ID {road_id}. Skipping file {file_path}.")
            continue
        
        patch_url = f"{api_base_url}/{report_id}/"
        try:
            with open(file_path, 'rb') as file:
                files = {'excelreport': file}
                response = requests.patch(patch_url, files=files,headers = { "Security-Password": "admin@123" }  )
                response.raise_for_status()
                print(f"Successfully patched report ID {report_id} with file {file_path}")
        except requests.RequestException as e:
            print(f"Failed to patch report ID {report_id} with file {file_path}: {e}")

def fetch_road_names(api_url, range_start, range_end):
    """Fetch road names from the API."""
    road_names = {}
    for id in range(range_start, range_end + 1):
        url = f"{api_url}/{id}"
        try:
            response = requests.get(url,headers = { "Security-Password": "admin@123" }  )
            response.raise_for_status()
            data = response.json()
            road_name = data.get("road", {}).get("name", "")
            if road_name:
                road_names[id] = road_name
        except requests.RequestException as e:
            print(f"Failed to fetch road name for ID {id}: {e}")
    return road_names

def main():
    api_url = "https://ndd.roadathena.com/api/surveys/roads"

    range_start = 13255
    range_end = 13256
    folder_path = "op"

    api_base_url = "https://ndd.roadathena.com/api/surveys/reports"

    
    # Fetch the report ID mapping
    report_id_map = fetch_report_id_map(api_base_url, range_start, range_end)
    if not report_id_map:
        print("No report ID mapping found. Exiting.")
        return
    
    # Extract road IDs from the report ID map
    road_ids = list(map(int, report_id_map.keys()))
    
    # Find Excel files by road IDs
    matched_files = find_excel_files(folder_path, road_ids)
    if not matched_files:
        print("No matching Excel files found. Exiting.")
        return
    
    # Patch the Excel files
    patch_excel_files(api_base_url, report_id_map, matched_files)

if __name__ == "__main__":
    main()
