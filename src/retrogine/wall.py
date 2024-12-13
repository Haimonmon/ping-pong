import tkinter as tk

from typing import Dict, Tuple, List

class WallSegmentError(Exception):
    pass


class InvalidWallCoordinates(Exception):
    pass


class Wall:
    """
    Contains the walls around the playground or playfield 🧱
    """
    def __init__(self, wall_coordinates_segments: dict, thickness: float, platform: tk.Canvas, platform_width: int, platform_height: int, color: str = "white"):
        self.wall_coordinates_segments = wall_coordinates_segments
        self.thickness = thickness
        self.color = color

        self.__platform = platform
        self.__platform_width = platform_width
        self.__platform_height = platform_height

        self.check_walls()
        self.render()


    @property
    def coordinates(self) -> dict:
        return self.wall_coordinates_segments

    
    def render(self):
        """
        Displays all of the wall on the given playground tkinter canvas
        """
        for start, end in self.wall_coordinates_segments:
            self.__platform.create_line(start[0], start[1], end[0], end[1], fill=self.color, width=self.thickness)


    def check_walls(self) -> None:
        """
        Checks if wall coordinates given are valid
        """
        for coordinates in self.wall_coordinates_segments:
           
            if (len(coordinates) != 2):
                raise InvalidWallCoordinates(f'Needs a partner for ending and starting point. Invalid: {coordinates}')

            starting_wall = coordinates[0]
            ending_wall = coordinates[1]

            if self.is_wall_exceeds(starting_wall) or self.is_wall_exceeds(ending_wall):
                raise WallSegmentError(
                        f"Invalid wall coordinates on side: {coordinates}. "
                        f"Coordinates exceed the bounds (width={self.__platform_width}, height={self.__platform_height})."
                    )
            
    def is_wall_exceeds(self, wall_num: int) -> None:
        """
        checks if the given wall_num exceeds on its limit
        """
        return any(coord > limit or coord < 0 for coord, limit in zip(wall_num, (self.__platform_width, self.__platform_height)))

if __name__ == "__main__":
    pass
