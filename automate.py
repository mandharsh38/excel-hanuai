import sys
import id

try:
    if id.clear_folders:
        import clear_folders
        import get_fur_jsons
        import get_gpx

    import clear_null_distance
    clear_null_distance.clean_json_files("jsons")

    import automatic_converter

    try:
        import json_patch
    except Exception as e:
        print(f"Error in json_patch: {e}")
        sys.exit(1)

    import left_right
    left_right.update_side_in_json("jsons", "jsons")

    import main

except Exception as e:
    print(f"❌ Fatal error in automate.py: {e}")
    sys.exit(1)
