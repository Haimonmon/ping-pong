import os
import tkinter as tk

from ..elements.playground import PlayGround
from .load_data import PlaygroundDataLoader, GamemodeLoader, MapDataLoader

from typing import Dict, Callable, List

class NotSupported(Exception):
    pass

class BruhIdontKnow(Exception):
    pass

class PongManager:
    """
    Wassupp!! 🎉, Im pong manager where i manage your round and i can startout the fun anytime 💖
    """
    def __init__(self) -> None:
        self.__tkinter_window = None
        self.__playground_name = None
        self.__gamemode = None
        self.__gametype = None
        self.__debug = None

        # * __file__ to get the exact location of the retro folder located
        self.__base_path = os.path.dirname(os.path.abspath(__file__))
        self.__maps_path = os.path.join(self.__base_path,'..', 'data', 'maps')

        self.__maps_data = MapDataLoader(self.__maps_path)

        self.__playground = None

    
    def customize_playground(self, window: tk.Tk, width: int = 1200, height: int = 700, color: str = 'black') -> PlayGround:
        """ Lets you to build and imagine your own playground to build and play with <3 """
        return PlayGround(window, width, height, color)

        
    def setup(self, tkinter_window: tk.Tk, playground_name: str, gamemode: str, gametype: str, debug: bool = False) -> None:
        ''' Lets it prepare the playground for you to get ready to play on <3 🏓'''
        self.__tkinter_window = tkinter_window
        self.__playground_name = playground_name
        self.__gamemode = gamemode.upper()
        self.__gametype = gametype
        self.__debug = debug

        self.__check_attributes()
        
        self._get_playground_data()


    def _get_playground_data(self) -> None:
        selected_map = self.__check_map_exist(self.__maps_path)

        playground_data = PlaygroundDataLoader(self.__maps_path, selected_map).load_playground_details()

        if self.__debug:
            self.display_map_detail(playground_data, selected_map)
            return
        
        playground_gamemode_data = GamemodeLoader(self.__maps_path, selected_map, self.__gametype).load_playground_gamemode_details()

        self.__check_gamemode_support(playground_data, self.__gamemode)

        platform_data = playground_data['platform']
        wall_data = playground_data['walls']
        paddle_data = playground_data['paddles'][self.__gamemode]
        ball_data = playground_data['ball']
        ball_data['count'] = playground_gamemode_data['ball_count']

        self.__prepare_playground(platform_data, wall_data, paddle_data, ball_data)


    def display_map_detail(self, playground_data: Dict, selected_map: str) -> None:
        
        map_directory = os.path.dirname(os.path.abspath(r"retro\data\maps"))

        print()
        print('=' * 50)
        print('Map Details')
        print('=' * 50)
        print(f'ID: {playground_data['id']}\nName: {playground_data['name']}\nCreator: {playground_data['creator']}\nCreated at: {playground_data['created']}\nSupported Gamemodes: {playground_data['support']['gametype']}\nDescription: {playground_data['description']}\nLocation: {os.path.join(map_directory, selected_map)}')
        print('=' * 50)
        print()


    def get_map_details(self) -> List:
        ''' Recieve a full list of maps that are available to play on 🏓'''
        return self.__maps_data.get_map_details()

    
    def __prepare_playground(self, platform_data: Dict, wall_data: Dict, paddle_data: List, ball_data: Dict) -> None:
        self.__playground = PlayGround(
            window = self.__tkinter_window,
            width = 1200,
            height = 700
        )

        self.__playground.add_platform(
            width = platform_data['width'],
            height = platform_data['height']
        )

        self.__playground.add_walls(
            coordinates = wall_data['coordinates'],
            thickness = wall_data['thickness']
        )

        for paddle in paddle_data:
            self.__playground.add_paddle(
                width = paddle['width'],
                height = paddle['height'],
                position = paddle['starting_position'],
                keys = paddle['key_binds'],
                controlled = paddle['controlled']
            )

        self.__playground.add_pong_ball(
            color = ball_data['color'],
            speed = ball_data['speed'],
            num = ball_data['count']
        )

        self.__playground.start()

    # ? Just data validation checkers
    def __check_map_exist(self, maps_path: str) -> str:
        if not os.path.exists(maps_path):
            raise FileNotFoundError(f"The directory '{maps_path}' does not exist.")

        items = os.listdir(maps_path)
        maps = [item for item in items if os.path.isdir(os.path.join(maps_path, item))]

        if self.__playground_name.lower() not in maps:
            raise FileNotFoundError(f"The map {self.__playground_name} does not exist.")

        return maps[maps.index(self.__playground_name)]
    

    def __check_gamemode_support(self, playground_data: Dict, gamemode: str) -> None:
        if gamemode not in playground_data['support']['gamemodes']:
            raise NotSupported(f'The gamemode ( {gamemode} ) given is not supported for this map')
        
    def __check_attributes(self) -> None:
        if not self.__gamemode and not self.__playground_name and not self.__gametype:
            raise BruhIdontKnow('Kindly Choose a map first pls :)')

if __name__ == "__main__":
      loader = PongManager(
           playground_name = "classic",
           gamemode = "pvp",
           gametype = "rush"
      )