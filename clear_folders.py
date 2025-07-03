import os
import shutil

# List of folder names to clear
folders_to_clear = ['jsons', 'gpx', 'gpx_jsons', 'op']

base_path = "."

def clear_folder(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")
    else:
        print(f"Folder not found: {folder_path}")


for folder in folders_to_clear:
    folder_path = os.path.join(base_path, folder)
    print(f"Clearing folder: {folder_path}")
    clear_folder(folder_path)