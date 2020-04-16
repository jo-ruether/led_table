from table.games.Game import Game
import random
import numpy as np

class Tetris(Game):
    def __init__(self, postman, output):
        super().__init__(postman, output)

    def start(self):


    def draw_icon(self, output):
        raise NotImplemented


class Tetromino():
    """ Class representing one Tetris Block"""
    # Unrotated list of coordinates for different block shapes
    # The coordinates are relative to the block's origin
    # Tuples are arranged in (row, col)
    shapes = {
        'I': {(0, 0), (0, 1), (0, 2), (0, 3)},
        'J': {(-1, 0), (-1, 1), (-1, 2), (0, 0)},
        'L': {(-1, 0), (-1, 1), (-1, 2), (0, 2)},
        '0': {(0, 0), (0, 1), (-1, 0), (-1, 1)},
        'T': {(0, 0), (0, 1), (-1, ), (-1, 1)},
        'S': {(-1, 0), (-1, 1), (0, 1), (0, 2)},
        'Z': {(-1, 0), (-1, 1), (0, 1), (0, 2)}
    }

    def __init__(self, GameInstance: Tetris, origin: tuple):
        self.game = GameInstance
        self.origin = origin

        # Select shape and color randomly
        random.seed()
        letter, self.pixels = random.choice(list(self.shapes.items()))
        # Todo Select random color from output class
        self.color = "red"

        # Create occupancy matrix of same dimensions like pixel_matrix
        rows = GameInstance.output.rows
        cols = GameInstance.output.columns
        self.occupancy_matrix = np.zeros(rows, cols)

    def _check_validity(self, intended_origin, intended_pixels):
        # Check validity for each pixel one by one
        for pixel in intended_pixels:
            row = intended_origin(0)+pixel(0)
            col = intended_origin(1)+pixel(1)

            if (row < 0) or (row > self.occupancy_matrix.shape[0]):
                return False
            if (col < 0) or (col > self.occupancy_matrix.shape[1]):
                return False
            if self.occupancy_matrix[row, col]:
                return False

        # Intended position passed all tests
        return True


    def rotate(self):
        """ Rotates block if possible.

        Returns:
            bool:   False if rotation is not possible, e.g. blocks would hit wall or other block.
        """
        new_pixels = set()

        # Rotate each pixel one by one in clockwise direction
        for pixel in self.pixels:
            rotated_pixel = (pixel(0), -pixel(1))
            new_pixels.add(rotated_pixel)

        if self._check_validity(self.origin, new_pixels):
            self.pixels = new_pixels
            return True
        else:
            return False

    def move_left(self):
        """ Moves block left if possible.

        Returns:
            bool:   False if moving is not possible, e.g. blocks would hit wall or other block.
        """
        new_origin = (self.origin(0), self.origin(1)-1)

        if self._check_validity(new_origin, self.pixels):
            self.origin = new_origin
            return True
        else:
            return False

    def move_right(self):
        """ Moves block right if possible.

        Returns:
            bool:   False if moving is not possible, e.g. blocks would hit wall or other block.
        """
        new_origin = (self.origin(0), self.origin(1)+1)

        if self._check_validity(new_origin, self.pixels):
            self.origin = new_origin
            return True
        else:
            return False

    def fall(self):
        """ Moves block one field down if possible.

        Returns:
            bool:   False if falling is not possible, e.g. blocks would ground wall or other block.
        """
        new_origin = (self.origin(0)+1, self.origin(1))

        if self._check_validity(new_origin, self.pixels):
            self.origin = new_origin
            return True
        else:
            return False

    def render(self):
        """"
        Adds this block to the pixelMatrix. Note: Does not call Output.show()
        """
        for pixel in self.pixels:
            self.game.output.set_value_color(pixel(0), pixel(1), self.color)

