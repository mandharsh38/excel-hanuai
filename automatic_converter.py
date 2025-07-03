import os
import sys
import json
import xml.etree.ElementTree as ET
import cv2
import numpy as np
import pandas as pd
import csv
import gpxpy.gpx
from datetime import datetime, timedelta
import gpxpy
from geopy import distance
import math
import argparse

gpx_folder = "gpx"
json_folder = "jsons"

def convert_to_utc(time_str):
            time_obj = datetime.strptime(time_str, "%m/%d/%Y %H:%M:%S")
            fixed_offset = timedelta(hours=5, minutes=30)
            time_utc = time_obj - fixed_offset
            return time_utc

def convert_to_ist(time_str):
    # time_str = time_str.split('+')[0]
    # time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

    time_str = time_str.text

    # Try parsing in multiple formats
    parsed = False
    for fmt in [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",          
        "%Y-%m-%dT%H:%M:%S",         
    ]:
        try:
            time_obj = datetime.strptime(time_str, fmt)
            parsed = True
            break
        except ValueError:
            continue

    if not parsed:
        print(f"Skipping {file_id}: Unrecognized GPX time format '{time_str}'")
        continue

    # set offset according to difference
    if var == 0: 
        fixed_offset = timedelta(hours=0,minutes=0)
    if var == 530:
        fixed_offset = timedelta(hours=5,minutes=30)

    time_ist = time_obj + fixed_offset
    return time_ist


def process_gpx(gpxFileName=None, all_gpx={}, save_path=None):
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
                    # print('file extraction completed..')
                    pass
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

    if save_path:
        with open(save_path, 'w') as json_file:
            json.dump(all_gpx, json_file, indent=4)

    # print(f"GPX data saved to {save_path}")


def convert():

    save_gpx_file = f'gpx_{filename.replace(".gpx", ".json")}'
    save_path = os.path.join("gpx_jsons", save_gpx_file)

    all_gpx = {}
    
    process_gpx(gpxFileName=gpx_path, all_gpx=all_gpx, save_path=save_path)
    print(f"Processed {filename} and saved JSON to {save_path}")

for filename in os.listdir(gpx_folder):
    if filename.endswith(".gpx"):
        file_id = filename.split('.')[0]
        gpx_path = os.path.join(gpx_folder, filename)
        json_path = os.path.join(json_folder, file_id + ".json")

        if not os.path.exists(json_path):
            print(f"Missing JSON file for {file_id}")

        try:
            tree = ET.parse(gpx_path)
            root = tree.getroot()

            ns = root.tag.split("}")[0].strip("{")

            trkpts = root.findall(f".//{{{ns}}}trkpt")
            time_elem = trkpts[0].find(f"{{{ns}}}time")

            gpx_time_str = time_elem.text

            # Try parsing in multiple formats
            parsed = False
            for fmt in [
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d %H:%M:%S",         
                "%Y-%m-%dT%H:%M:%S",         
            ]:
                try:
                    gpx_time = datetime.strptime(gpx_time_str, fmt)
                    parsed = True
                    break
                except ValueError:
                    continue

            if not parsed:
                print(f"Skipping {file_id}: Unrecognized GPX time format '{gpx_time_str}'")
                continue


            with open(json_path, "r") as f:
                data = json.load(f)
                assets = data.get("assets", [])
                if not assets:
                    print(f"Info: JSON 'assets' list is empty for {file_id}")
                    var = 0 
                    convert()
                    continue

                json_time_str = assets[0]["Timestamp on processed video"]
                json_time = datetime.strptime(json_time_str, "%Y-%m-%d %H:%M:%S")

            time_diff = abs((json_time - gpx_time).total_seconds()) / 60  # in minutes

            if 0 <= time_diff <= 30:
                var = 0
            elif 330 <= time_diff <= 360:
                var = 530
            else:
                raise ValueError(f"{file_id}: GPX and JSON mismatch (time diff = {time_diff:.1f} min)")

            print(f"{file_id}: Time diff = {time_diff:.1f} min → var = {var}")

            # converter
            convert()
        
        except Exception as e:
            print(f"Error processing {file_id}: {e}")
            sys.exit(1)
