import os
import shutil

def copy_files_recursive(source_dir_path, dest_dir_path):
    source_list = os.listdir(source_dir_path)
    for item in source_list:
        source_item = os.path.join(source_dir_path, item)
        dest_item = os.path.join(dest_dir_path, item)
        if os.path.isfile(source_item):
            shutil.copy(source_item, dest_item)
            print(f"Copying {source_item} to {dest_item}")
        elif os.path.isdir(source_item):
            os.mkdir(dest_item)
            print(f"Creating new directory {dest_item}")
            copy_files_recursive(source_item, dest_item)