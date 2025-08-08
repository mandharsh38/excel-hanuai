import os
from excel2 import process_json_data
from excel3 import process_json_data2
from excel4 import process_json_data3
from excel5 import process_json_data5
from excel_anomalies import process_anomaly_data

road_json_path = "jsons"
gpx_json_path = "gpx_jsons"
output_folder = "op"

import id
r_ids = id.ids

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support() 

    print("r_ids", r_ids)

    for i, roadId in enumerate(r_ids):
        # print(i, roadId)
        print("Processing road id: ", roadId)

        # process_anomaly_data(road_json_path, output_folder, roadId)  # for anomaly
        process_json_data(road_json_path, output_folder, roadId)
        process_json_data2(road_json_path, gpx_json_path, output_folder, roadId)
        process_json_data3(road_json_path, output_folder, roadId)
        process_json_data5(road_json_path, output_folder, roadId)
