import os
import json
import tkinter as tk

from ..logic import *

from ..elements.playground import PlayGround
from typing import Dict, Callable, List

class NotSupported(Exception):
    pass

class PongManager:
    def __init__(self, tkinter_window: tk.Tk, playground_name: str, gamemode: str, gametype: str, debug: bool = False) -> None:
        self.__tkinter_window = tkinter_window
        self.__playground_name = playground_name
        self.__gamemode = gamemode.upper()
        self.__gametype = gametype
        self.__debug = debug

        # * __file__ to get the exact location of the retro folder located
        self.__base_path = os.path.dirname(os.path.abspath(__file__))
        self.__maps_path = os.path.join(self.__base_path,'..', 'data', 'maps')

        self.selected_map = self.check_map_exist(self.__maps_path)

        self.__playground_data = PlaygroundDataLoader(self.__maps_path, self.__playground_name).load_playground_details()
        self.__playground_gamemode_data = GamemodeLoader(self.__maps_path, self.__playground_name, self.__gametype).load_playground_gamemode_details()

        self.check_gamemode_support(self.__gamemode)

        self.__platform_data = self.__playground_data['platform']
        self.__wall_data = self.__playground_data['walls']
        self.__paddle_data = self.__playground_data['paddles'][self.__gamemode]
        self.__ball_data = self.__playground_data['ball']
        self.__ball_data['count'] = self.__playground_gamemode_data['ball_count']

        if self.__debug:
            self.display_map_detail()
        else:
            self.prepare()


    def display_map_detail(self) -> None:
        map_directory = os.path.dirname(os.path.abspath(r"retro\data\maps"))

        print()
        print('=' * 50)
        print('Map Details')
        print('=' * 50)
        print(f'ID: {self.__playground_data['id']}\nName: {self.__playground_data['name']}\nCreator: {self.__playground_data['creator']}\nCreated at: {self.__playground_data['created']}\nSupported Gamemodes: {self.__playground_data['support']['gametype']}\nDescription: {self.__playground_data['description']}\nLocation: {os.path.join(map_directory, self.__playground_name)}')
        print('=' * 50)
        print()


    def prepare(self) -> None:
        playground = PlayGround(
            window = self.__tkinter_window,
            width = 1200,
            height = 700
        )

        playground.add_platform(
            width = self.__platform_data['width'],
            height = self.__platform_data['height']
        )

        playground.add_walls(
            coordinates = self.__wall_data['coordinates'],
            thickness = self.__wall_data['thickness']
        )

        for paddle in self.__paddle_data:
            playground.add_paddle(
                width = paddle['width'],
                height = paddle['height'],
                position = paddle['starting_position'],
                keys = paddle['key_binds'],
                controlled = paddle['controlled']
            )

        playground.add_pong_ball(
            color = self.__ball_data['color'],
            speed = self.__ball_data['speed'],
            num = self.__ball_data['count']
        )

        playground.start()

        
    def check_map_exist(self, maps_path: str) -> str:
        if not os.path.exists(maps_path):
            raise FileNotFoundError(f"The directory '{maps_path}' does not exist.")

        items = os.listdir(maps_path)
        maps = [item for item in items if os.path.isdir(os.path.join(maps_path, item))]

        if self.__playground_name.lower() not in maps:
            raise FileNotFoundError(f"The map {self.__playground_name} does not exist.")

        return maps[maps.index(self.__playground_name)]
    

    def check_gamemode_support(self, gamemode: str) -> None:
        if gamemode not in self.__playground_data['support']['gamemodes']:
            raise NotSupported(f'The gamemode ( {gamemode} ) given is not supported for this map')


class MissingPlaygroundFile(Exception):
    pass


class PlaygroundDataLoader:
    def __init__(self, maps_path, playground_name: str):
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


if __name__ == "__main__":
      loader = PongManager(
           playground_name = "classic",
           gamemode = "pvp",
           gametype = "rush"
      )