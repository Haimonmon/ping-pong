import os
import json
from typing import Dict, List, Callable, Literal

from ..logic import *


class MapDataLoader:
    def __init__(self, map_path: str) -> None:
        self.__maps_path = map_path

    def get_map_details(self) -> None:
        if not os.path.exists(self.__maps_path):
            raise FileNotFoundError(f"The directory '{self.__maps_path}' does not exist.")
        
        items = os.listdir(self.__maps_path)
        maps = []

        for item in items:
            playground_data = PlaygroundDataLoader(self.__maps_path, item).load_playground_details()

            maps.append(
                {
                    'id': playground_data['id'],
                    'name': playground_data['name'],
                    'creator': playground_data['creator'],
                    'created': playground_data['created'],
                    'description': playground_data['description'],
                    'support': playground_data['support'],
                    'playground_platform': playground_data['platform'],
                    'playground_wall': playground_data['walls'],
                    'playground_paddles': playground_data['paddles']
                }
            )
        
        return maps

class MissingPlaygroundFile(Exception):
    pass

class PlaygroundDataLoader:
    def __init__(self, maps_path: str, playground_name: str) -> None:
        self.__playground_name = playground_name

        self.__maps_path = maps_path
        self.__playground_file = os.path.join(self.__maps_path, self.__playground_name,'playground.json')


    def load_playground_details(self) -> Dict:
        if not os.path.exists(self.__playground_file):
            raise MissingPlaygroundFile(f"Playground data file not found: {self.__playground_file}")
        
        with open(self.__playground_file, 'r') as playground:
            playground_data = json.load(playground)

        return playground_data
    

class GamemodeLoader:
    def __init__(self, maps_path: str, playground_name: str, gametype: str) -> None:
        self.__maps_path = maps_path
        self.__playground_name = playground_name
        self.__gametype = gametype.lower()

        self.__playground_mode_file = os.path.join(self.__maps_path, self.__playground_name, "modes", f'{self.__gametype}.json')
        
    def select_gametype(self, gametype: str) -> Callable:
        gametypes = {
            "survival": Survival,
            "rush": Rush,
            "double_ball": DualBall
        }

        if gametype.lower() not in gametypes:
            raise ValueError(f"Invalid gametype: {gametype}. Available options: {list(gametypes.keys())}")

        return gametypes[gametype.lower()](self.playground)
    

    def load_playground_gamemode_details(self) -> Dict:
        if not os.path.exists(self.__playground_mode_file):
            raise MissingPlaygroundFile(f"Playground data file mode not found: {self.__playground_mode_file}")
        
        with open(self.__playground_mode_file, 'r') as mode:
            playground_mode_data = json.load(mode)

        return playground_mode_data