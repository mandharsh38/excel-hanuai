# import os
# import requests


# api_base_url = "https://ndd.roadathena.com/api/surveys/roads/"

# json_folder = "jsons"  

# # road_furniture_44_updated.json
# ids = [3735,3736]

# for file_id in ids:
#     print(file_id)
#     json_file_path = os.path.join(json_folder, f"road_furniture_{file_id}.json")
    
    
#     if os.path.exists(json_file_path):
#         print(f"Processing {json_file_path}")
        
#         try:
            
#             with open(json_file_path, 'rb') as json_file:
                
#                 files = {
#                     'furniture_json': json_file
#                 }


#                 api_url = f"{api_base_url}{file_id}"
#                 response = requests.patch(api_url, files=files, headers={"Security-Password": "admin@123"})
                
#                 # Check if the request was successful
#                 if response.status_code == 200:
#                     print(f"Successfully patched data for ID {file_id}")
#                 else:
#                     print(f"Failed to patch data for ID {file_id}. Status code: {response.status_code}")
#                     print(f"Response: {response.text}")

#         except Exception as e:
#             print(f"Error processing ID {file_id}: {str(e)}")
#     else:
#         print(f"File {json_file_path} does not exist, skipping...")






import os
import requests


api_base_url = "https://ndd.roadathena.com/api/surveys/roads/"

json_folder = "./jsons"  

# road_furniture_44_updated.json
# ids = list(range(7505,7506))
# ids =[11980, 11983, 11982, 11977, 11975, 11999, 11992, 11996, 11995, 11979, 11985, 11989, 11987, 11981, 11988, 11984, 11976, 11986, 11978, 12000, 11993, 12611, 11994, 11990, 11991]
import id 
ids=id.ids
# ids = [3803]

for file_id in ids:
    json_file_path = os.path.join(json_folder, f"road_{file_id}.json")
    
    
    if os.path.exists(json_file_path):
        print(f"Processing {json_file_path}")
        
        try:
            
            with open(json_file_path, 'rb') as json_file:
                
                files = {
                    'furniture_json': json_file
                }


                api_url = f"{api_base_url}{file_id}"
                response = requests.patch(api_url, files=files, headers={"Security-Password": "admin@123"})
                
                # Check if the request was successful
                if response.status_code == 200:
                    print(f"Successfully patched data for ID {file_id}")
                else:
                    print(f"Failed to patch data for ID {file_id}. Status code: {response.status_code}")
                    print(f"Response: {response.text}")

        except Exception as e:
            print(f"Error processing ID {file_id}: {str(e)}")
    else:
        print(f"File {json_file_path} does not exist, skipping...")