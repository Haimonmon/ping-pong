# from typing import Dict

# class Saver:
#     def __init__(self, file_name):
#         self.__file_name = file_name
    
#     def save_to_json(self, content: Dict) -> None:
#         pass

#     def check_data_exist(self) -> None:
#         pass

# if __name__ == "__main__":
#       save = Saver()

import os

def get_all_maps_with_indexes(maps_folder):
    if not os.path.exists(maps_folder):
        raise FileNotFoundError(
            f"The directory '{maps_folder}' does not exist.")

    items = os.listdir(maps_folder)
    folders = [item for item in items if os.path.isdir(os.path.join(maps_folder, item))]
   
    return {
        "folders": folders
    }


# Example Usage
maps_directory = "retro\data\maps"

all_maps = get_all_maps_with_indexes(maps_directory)["folders"]
print()
print(all_maps)
print()
print("Map Folders with Indexes:")
for folder in all_maps:
    print(f"{folder}")

