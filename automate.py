import id

# clear folders json gpx gpx_jsons op
if id.clear_folders:

    import clear_folders
    # get jsons and gpx
    import get_fur_jsons
    import get_gpx

# clear null distances
import clear_null_distance
clear_null_distance.clean_json_files("jsons")

# gpx converter
import automatic_converter

# import gpx_converter
# gpx_converter.convert()

# json patch
try: 
    import json_patch
except Exception as e:
    print(f"Error in json_patch: {e}")
    sys.exit(1)

# fix left right
import left_right
left_right.update_side_in_json("jsons","jsons")

# main
import main

# pdf reformat


# pdf_print

