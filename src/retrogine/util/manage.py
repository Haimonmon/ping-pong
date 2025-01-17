import os
import tkinter as tk

from ..elements.playground import PlayGround
from .load_data import PlaygroundDataLoader, GamemodeLoader, MapDataLoader

from typing import Dict, Callable, List, Literal

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
        self.__responsiveness = None

        # * __file__ to get the exact location of the retro folder located
        self.__base_path = os.path.dirname(os.path.abspath(__file__))
        self.__maps_path = os.path.join(self.__base_path,'..', 'data', 'maps')

        self.__maps_data = MapDataLoader(self.__maps_path)

        self.__playground = None

    
    def customize_playground(self, window: tk.Tk, width: int = 1200, height: int = 700, color: str = 'black', render: bool = True) -> PlayGround:
        """ Lets you to build and imagine your own playground to build and play with <3 """
        return PlayGround(window, width, height, color, render = render)

        
    def setup(self, tkinter_window: tk.Tk, playground_name: str, gamemode: str, gametype: str, automatic_start = True, request: Literal['map-details', 'playable-maps'] = None, responsiveness = False) -> Dict:
        ''' Lets it prepare the playground for you to get ready to play on <3 🏓'''
        self.__tkinter_window = tkinter_window
        self.__playground_name = playground_name
        self.__gamemode = gamemode.upper()
        self.__gametype = gametype
        self.__request = request
        self.__responsiveness = responsiveness

        self.__check_attributes()
        
        return self._get_playground_data(automatic_start)


    def _get_playground_data(self, automatic_start: bool) -> Dict:
        selected_map = self.__check_map_exist(self.__maps_path)

        playground_data = PlaygroundDataLoader(self.__maps_path, selected_map).load_playground_details()

        if self.__request == 'playable-maps':
            self.__list_maps()
            return

        if self.__request == 'map-details':
            self.display_map_detail(playground_data, selected_map)
            return
        
        playground_gamemode_data = GamemodeLoader(self.__maps_path, selected_map, self.__gametype).load_playground_gamemode_details()

        self.__check_gamemode_support(playground_data, self.__gamemode)

        platform_data = playground_data['platform']
        wall_data = playground_data['walls']
        paddle_data = playground_data['paddles'][self.__gamemode]
        ball_data = playground_data['ball']
        ball_data['count'] = playground_gamemode_data['ball_count']

        return self.__prepare_playground(platform_data, wall_data, paddle_data, ball_data, automatic_start)

    def __list_maps(self) -> None:
        """ Wanna see some available Maps? """

        maps: Dict = self.__maps_data.get_map_details()

        col1_width = max(len(map['id']) for map in maps) + 7
        col2_width = max(len(map['name']) for map in maps) + 10
        col3_width = max(len(map['created']) for map in maps) + 10
        col4_width = max(len(map['creator']) for map in maps) + 4

        total_width = col1_width + col2_width + col3_width + col4_width + 4

        print()
        print('-' * total_width)
        print(f"|{'Pong - Playable Maps':^{total_width - 2}}|")
        print('-' * total_width)
        print(f"|{'ID':^{col1_width}}|{'Name':^{col2_width}}|{'Creator':^{col4_width}}|{'Date Created':^{col3_width - 1}}|")
        print('-' * total_width)

        for map in maps:
            print(f"|{map['id']:^{col1_width}}|{map['name']:^{col2_width}}|{map['creator']:^{col4_width}}|{map['created']:^{col3_width - 1}}|")
        print('-' * total_width)
        print(f"|{'':^{total_width - 2}}|")
        print('-' * total_width)
        print()

    def display_map_detail(self, playground_data: Dict, selected_map: str) -> None:
        
        map_directory = os.path.dirname(os.path.abspath(r"retro\data\maps"))

        print()
        print('=' * 50)
        print('Map Details')
        print('=' * 50)
        print(f'ID: {playground_data['id']}\nName: {playground_data['name']}\nCreator: {playground_data['creator']}\nCreated at: {playground_data['created']}\nSupported Gamemodes: {playground_data['support']['gametype']}\nDescription: {playground_data['description']}\nLocation: {os.path.join(map_directory, selected_map)}')
        print('=' * 50)
        print()


    def get_map_details(self, map_name: str = None) -> List:
        ''' Recieve a full list of maps that are available to play on 🏓'''

        list_maps = self.__maps_data.get_map_details()

        if map_name:
            map_data = next((map for map in list_maps if map["name"].lower() == map_name.lower()), None)
            return map_data

        return list_maps

    
    def __prepare_playground(self, platform_data: Dict, wall_data: Dict, paddle_data: List, ball_data: Dict, automatic_start: bool) -> Dict:
        self.__playground = PlayGround(
            window = self.__tkinter_window,
            width = 1300,
            height = 730,
            color = "#1D313C"
        )


        if self.__responsiveness:
            platform = self.__playground.add_platform(
                width = platform_data['width'],
                height = platform_data['height'],
                color = platform_data['background_color'],
                responsive = True,
                new_width=919,
                new_height= 520,
                padding = 80,
                pos_y = 0.45
            )

        else:
            platform = self.__playground.add_platform(
                width=platform_data['width'],
                height=platform_data['height'],
                color=platform_data['background_color']
            )

        self.__playground.add_walls(
            coordinates = wall_data['coordinates'],
            thickness = wall_data['thickness'],
            color = wall_data['color']
        )

        for paddle in paddle_data:
            self.__playground.add_paddle(
                width = paddle['width'],
                height = paddle['height'],
                position = paddle['starting_position'],
                keys = paddle['key_binds'],
                controlled = paddle['controlled'],
                color = paddle['color']
            )

        self.__playground.add_pong_ball(
            color = ball_data['color'],
            speed = ball_data['speed'],
            num = ball_data['count']
        )

        if automatic_start:
            self.__playground.start_roundloop()
            self.__playground.start()
            
        return {
            "platform_canvas": platform,
        }

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