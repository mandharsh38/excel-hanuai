import cv2
import numpy as np
import os
import pandas as pd
import csv
import gpxpy.gpx
from datetime import datetime, timedelta
import gpxpy
from geopy import distance
import json
import math
import argparse

def convert_to_utc(time_str):
    time_obj = datetime.strptime(time_str, "%m/%d/%Y %H:%M:%S")
    fixed_offset = timedelta(hours=5, minutes=30)
    time_utc = time_obj - fixed_offset
    return time_utc

def convert_to_ist(time_str):
    time_str = time_str.split('+')[0]
    time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    fixed_offset = timedelta(hours=0,minutes=0)
    # fixed_offset = timedelta(hours=5,minutes=30)
    time_ist = time_obj + fixed_offset
    return time_ist


def getGPXData(gpxFileName=None, all_gpx={}, save_path=None):
    gpx = gpxpy.parse(open(gpxFileName, 'r'))
    gpxData = {
        "chk_pnts": {}
    }
    dis = 0
    disInMeters = 0
    startPoint = [0, 0]
    dis_3d = 0

    for track in gpx.tracks:
        for segment in track.segments:
            for i, point in enumerate(segment.points):
                if i == 0:
                    startPoint[0], startPoint[1] = (point.latitude, point.longitude)

                try:
                    nxt = segment.points[i + 1]
                    newport_ri = (point.latitude, point.longitude)
                    cleveland_oh = (nxt.latitude, nxt.longitude)
                    dis += distance.distance(newport_ri, cleveland_oh).km
                    dis_bt_points = distance.distance(newport_ri, cleveland_oh).m
                    disInMeters += dis_bt_points
                    h = abs(nxt.elevation - point.elevation)
                    dis_3d += math.sqrt((h * h) + (dis_bt_points * dis_bt_points))
                except IndexError:
                    print('file extraction completed..')
                except:
                    print(i, len(segment.points))
                    print('Error in gpxParser.py > getGPXData() > line:28')
                    pass

                gpxData['chk_pnts'][str(point.time.replace(microsecond=0))] = {
                    "lat": point.latitude,
                    "lng": point.longitude,
                    "distanceInMeters": disInMeters
                }
                all_gpx[str(convert_to_ist(str(point.time.replace(microsecond=0))))] = {
                    "lat": point.latitude,
                    "lng": point.longitude,
                    "distanceInMeters": disInMeters
                }

    gpxData['dist_covered'] = disInMeters

    print("extraction ended.")

    if save_path:
        with open(save_path, 'w') as json_file:
            json.dump(all_gpx, json_file, indent=4)

    print(f"GPX data saved to {save_path}")

    print("Extraction ended.")

    return all_gpx

# if __name__ == "__main__":
#     # Define the input and output paths
#     gpx_dir = "gpx"
    
#     for gpx_file in os.listdir(gpx_dir):
        
#         gpx_path = os.path.join(gpx_dir, gpx_file)
#         save_gpx_file = f'gpx_{gpx_file.replace(".gpx", ".json")}'
#         print(save_gpx_file)
#         save_path = os.path.join("gpx_jsons" , save_gpx_file)
#         gpx_data = getGPXData(gpxFileName = gpx_path , save_path=save_path )
#         # print(gpx_data)
    
#     # getGPXData(gpxFileName=input_path, save_path=output_path)

def convert():
    gpx_dir = "gpx"
    
    for gpx_file in os.listdir(gpx_dir):
        gpx_path = os.path.join(gpx_dir, gpx_file)
        save_gpx_file = f'gpx_{gpx_file.replace(".gpx", ".json")}'
        save_path = os.path.join("gpx_jsons", save_gpx_file)
        
        # Reset the all_gpx dictionary for each GPX file
        all_gpx = {}
        
        gpx_data = getGPXData(gpxFileName=gpx_path, all_gpx=all_gpx, save_path=save_path)
        
        print(f"Processed {gpx_file} and saved JSON to {save_path}")

if __name__ == "__main__":
    # Define the input and output paths
    convert()
