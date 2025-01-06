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
    def __init__(self, wall_coordinates_segments: List, playground: object, color: str = "white", thickness = 20):
        self.wall_coordinates_segments = wall_coordinates_segments

        self.playground = playground

        self.thickness = thickness
        self.color = color

        self.__platform = self.playground.platform
        self.__platform_width = self.playground.platform_dimension['width']
        self.__platform_height = self.playground.platform_dimension['height']

        self.check_walls()
        self.apply_thickness()
        self.render()


    @property
    def coordinates(self) -> dict:
        return self.wall_coordinates_segments

    
    def render(self):
        """
        Displays all of the wall on the given playground tkinter canvas
        """
        for start_bottom, end_bottom, start_top, end_top in self.wall_coordinates_segments:
            self.__platform.create_line(start_bottom[0], start_bottom[1], end_bottom[0], end_bottom[1], fill='blue')
            self.__platform.create_line(start_top[0], start_top[1], end_top[0], end_top[1], fill='blue')

            horizontal_wall = start_bottom[1] == end_bottom[1]
            vertical_wall = start_bottom[0] == end_bottom[0]



            # if horizontal_wall:
            #     self.__platform.create_rectangle(
            #         start_bottom[0], start_bottom[1] + self.thickness, 
            #         end_bottom[0], end_bottom[1], 
            #         fill=self.color, outline="blue"
            #     )

            # elif vertical_wall:
                
            #     self.__platform.create_rectangle(
            #         start_bottom[0] + self.thickness, start_bottom[1], 
            #         end_bottom[0], end_bottom[1], 
            #         fill=self.color, outline="blue"
            #     )


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

    
    def apply_thickness(self) -> None:
        """
        Applies thickness to the walls by adjusting coordinates for both horizontal and vertical walls.
        """

        thickened_walls = []

        half_thickness = (self.thickness / 2)

        padding = self.playground.platform_padding

        for start, end in self.wall_coordinates_segments:

            horizontal_wall = start[1] == end[1]
            vertical_wall = start[0] == end[0]

            if horizontal_wall:
                thickened_walls.append(
                    [
                        ((start[0] - half_thickness) + padding, (start[1] - half_thickness) + padding), ((end[0] + half_thickness) + padding, (end[1] - half_thickness) + padding),
                        ((start[0] - half_thickness) + padding, (start[1] + half_thickness) + padding), ((end[0] + half_thickness) + padding, (end[1] + half_thickness) + padding)
                    ]
                )

                thickened_walls.append(
                    [
                        ((start[0] - half_thickness) + padding, (start[1] - half_thickness) + padding), ((start[0] - half_thickness) + padding, (start[1] + half_thickness) + padding),
                        ((end[0] + half_thickness) + padding, (end[1] - half_thickness) + padding), ((end[0] + half_thickness) + padding, (end[1] + half_thickness) + padding)
                    ]
                )

            elif vertical_wall:
                thickened_walls.append(
                    [
                        ((start[0] - half_thickness) + padding, (start[1] - half_thickness) + padding), ((start[0] + half_thickness) + padding, (start[1] - half_thickness) + padding),
                        ((end[0] - half_thickness) + padding, (end[1] + half_thickness) + padding), ((end[0] + half_thickness) + padding, (end[1] + half_thickness) + padding)
                    ]
                )

                thickened_walls.append(
                    [
                        # * Top Side
                        ((start[0] - half_thickness) + padding, (start[1] - half_thickness) + padding), ((end[0] - half_thickness) + padding, (end[1] + half_thickness) + padding),
                        # * Bottom Side
                        ((start[0] + half_thickness) + padding, (start[1] - half_thickness) + padding), ((end[0] + half_thickness) + padding, (end[1] + half_thickness) + padding)
                    ]
                )

        self.wall_coordinates_segments = thickened_walls

if __name__ == "__main__":
    pass

# if horizontal_wall:
#                 thickened_walls.append(
#                     {
#                         'top': ((start[0] - half_thickness, start[1] - half_thickness), (end[0] + half_thickness, end[1] - half_thickness)),
#                         'bottom': ((start[0] - half_thickness, start[1] + half_thickness), (end[0] + half_thickness, end[1] + half_thickness)),
#                         'left': ((start[0] - half_thickness, start[1] - half_thickness), (start[0] - half_thickness, start[1] + half_thickness)),
#                         'right': ((end[0] + half_thickness, end[1] - half_thickness), (end[0] + half_thickness, end[1] + half_thickness))
#                     }
#                 )

#             elif vertical_wall:
#                 thickened_walls.append(
#                     {
#                         'top': ((start[0] - half_thickness, start[1] - half_thickness), (end[0] - half_thickness, end[1] + half_thickness)),
#                         'bottom': ((start[0] + half_thickness, start[1] - half_thickness), (end[0] + half_thickness, end[1] + half_thickness)),
#                         'left': ((start[0] - half_thickness, start[1] - half_thickness), (start[0] + half_thickness, start[1] - half_thickness)),
#                         'right': ((end[0] - half_thickness, end[1] + half_thickness), (end[0] + half_thickness, end[1] + half_thickness))
#                     }
#                 )