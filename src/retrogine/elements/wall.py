import tkinter as tk

from typing import Dict, Tuple, List, Callable

class WallSegmentError(Exception):
    pass


class InvalidWallCoordinates(Exception):
    pass


class Wall:
    """
    Contains the walls around the playground or playfield 🧱
    """
    def __init__(self, coordinates: List, playground: object, color: str = "white", thickness = 20, responsive: bool = False):
        '''
        * wall comes up with start and end that each contain x and y coordinates
        * Example : [(0,0), (0,1000)] 
        * (x = 0,y = 0) is the starting point while (x = 0, y = 1000) is the ending point
        '''
        self.coordinates = coordinates

        self.playground = playground

        self.thickness = thickness

        self.color = color

        self.responsive = responsive

        self.__platform = self.playground.platform
        self.__platform_width = self.playground.platform_dimension['width']
        self.__platform_height = self.playground.platform_dimension['height']


        # self.check_walls()
        self.apply_thickness()
        self.render()

 
    def render(self):
        """
        Displays all of the wall on the given playground tkinter canvas
        """
        for start_bottom, end_bottom, start_top, end_top in self.coordinates:
            # self.__platform.create_line(start_bottom[0], start_bottom[1], end_bottom[0], end_bottom[1], fill='')
            # self.__platform.create_line(start_top[0], start_top[1], end_top[0], end_top[1], fill='')

            horizontal_wall = start_bottom[1] == end_bottom[1]
            vertical_wall = start_bottom[0] == end_bottom[0]

            if horizontal_wall:
                self.__platform.create_rectangle(
                    start_bottom[0], start_bottom[1] + self.thickness,
                    end_bottom[0], end_bottom[1],
                    fill=self.color, outline = self.color
                )

            elif vertical_wall:

                self.__platform.create_rectangle(
                    start_bottom[0] + self.thickness, start_bottom[1],
                    end_bottom[0], end_bottom[1],
                    fill=self.color, outline = self.color
                )

    def check_walls(self) -> None:
        """
        Checks if wall coordinates given are valid
        """
        for coordinate in self.coordinates:
            if (len(coordinate) != 2):
                raise InvalidWallCoordinates(f'Needs a partner for ending and starting point. Invalid: {coordinate}')

            starting_wall = coordinate[0]
            ending_wall = coordinate[1]

            if self.is_wall_exceeds(starting_wall) or self.is_wall_exceeds(ending_wall):
                raise WallSegmentError(
                        f"Invalid wall coordinates on side: {coordinate}. "
                        f"Coordinates exceed the bounds (width={self.__platform_width}, height={self.__platform_height})."
                    )
            

    def is_wall_exceeds(self, wall_num: int) -> None:
        """
        checks if the given wall coordinates are valid to its platform dimensions
        """
        return any(coord > limit or coord < 0 for coord, limit in zip(wall_num, (self.__platform_width, self.__platform_height)))
    

    def apply_thickness(self) -> None:
        """
        Applies thickness to the walls by adjusting coordinates

        forming a complete rectangular box (top, bottom, left, and right sides)
        """

        self.playground.window.update()
        print()
        print('New?', self.coordinates)
        print('Canvas Width: ', self.__platform.winfo_width())
        print('Canvas Height: ', self.__platform.winfo_height())
        print()

        thickened_walls = []

        half_thickness = self.thickness // 2

        # * Apply padding on the platform to not too compressed, this also helps to make the wall not overlapped when rendering with wall thickness
        padding = self.playground.platform_padding

        for start, end in self.coordinates:
            if start[1] == end[1]: # * Horizontal wall
                thickened_walls.append(
                    [
                        *self._create_horizontal_side(start, end, -half_thickness + padding, -half_thickness +
                                                        padding, +half_thickness + padding, -half_thickness + padding),
                        *self._create_horizontal_side(start, end, -half_thickness + padding, +half_thickness + padding, +half_thickness + padding, +half_thickness + padding)
                    ]
                )

                thickened_walls.append(
                    [
                        *self._create_vertical_side(start, -half_thickness + padding, -half_thickness +
                                                    padding, -half_thickness + padding, +half_thickness + padding),
                        *self._create_vertical_side(end, +half_thickness + padding, -half_thickness + padding, +half_thickness + padding, +half_thickness + padding)
                    ]
                )

                continue

            elif start[0] == end[0]: # * Vertical wall
                thickened_walls.append(
                    [
                        *self._create_vertical_side(start, -half_thickness + padding, -half_thickness +
                                                    padding, +half_thickness + padding, -half_thickness + padding),
                        *self._create_vertical_side(end, -half_thickness + padding, +half_thickness + padding, +half_thickness + padding, +half_thickness + padding)
                    ]
                )

                thickened_walls.append(
                    [
                        *self._create_horizontal_side(start, end, -half_thickness + padding, -half_thickness +
                                                    padding, -half_thickness + padding, +half_thickness + padding),
                        *self._create_horizontal_side(start, end, +half_thickness + padding, -half_thickness + padding, +half_thickness + padding, +half_thickness + padding)
                    ]
                )

        # * change old coordinates to new ones
        self.coordinates = thickened_walls


        def _create_horizontal_wall(self, start, end, half_thickness) -> None:
            pass

        def _create_vertical_wall(self, start, end, half_thickness) -> None:
            pass

    def _create_horizontal_side(self, start_point, end_point, adjust_x1, adjust_y1, adjust_x2, adjust_y2) -> None:
        return [
            ((start_point[0] + adjust_x1), (start_point[1] + adjust_y1)), 
            ((end_point[0]+ adjust_x2), (end_point[1] + adjust_y2))
        ]

    def _create_vertical_side(self, point, adjust_x1, adjust_y1, adjust_x2, adjust_y2) -> None:
        return [
            ((point[0] + adjust_x1), (point[1] + adjust_y1)),
            ((point[0] + adjust_x2), (point[1] + adjust_y2))
        ]
        
if __name__ == "__main__":
    pass