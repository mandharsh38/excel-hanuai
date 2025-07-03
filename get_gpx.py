import os
import requests
import json 

api_base_url = "https://ndd.roadathena.com/api/surveys/roads/"
file_base_url= "https://ndd.roadathena.com"


#ids = list(range(5335,5342))  #srr
#ids = list(range(1203,1209 ))   #sll

#ids =[5900,1,121,1123,1119,11205901]
# ids =[10510, 10511]
import id
ids= id.ids

output_path = "gpx"


if not os.path.exists(output_path):
    os.makedirs(output_path)

for file_id in ids:
    try:
        api_url = f"{api_base_url}{file_id}"
        response = requests.get(api_url,headers = { "Security-Password": "admin@123" })

        if response.status_code == 200:
            json_data = response.json()  
            if 'json_file' in json_data:
                json_file_url = json_data['gpx_file']
                full_file_url = f"{file_base_url}{json_file_url}"
                file_response = requests.get(full_file_url,headers = { "Security-Password": "admin@123" })
                
                if file_response.status_code == 200:
                    json_file_path = os.path.join(output_path, f"road_{file_id}.gpx")
                    with open(json_file_path, 'wb') as json_file:
                        json_file.write(file_response.content)
                        
                    print(f"Successfully downloaded JSON file for ID {file_id}")
                else:
                    print(f"Failed to download file for ID {file_id}. Status code: 404")
            else:
                print(f"Key 'json_file' not found for ID {file_id}")
        else:
            print(f"Failed to fetch data for ID {file_id}. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"Error processing ID {file_id}: {str(e)}")
