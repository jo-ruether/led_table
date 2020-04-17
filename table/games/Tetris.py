from table.games.Game import Game
import random
import numpy as np
from time import sleep


class Tetris(Game):
    def __init__(self, postman, output):
        super().__init__(postman, output)
        # Stores landed blocks as RGB values
        self.landed_blocks = np.zeros([self.output.rows, self.output.columns, 3])

        self.running = True
        self.score = 0

    def start(self):
        while self.running:
            speed = .8
            current_block = Tetromino(self, (0, self.output.columns // 2 - 1))

            while current_block.fall():
                sleep(speed)

            # Block has landed
            if not current_block.dissolve():
                # Block couldn't dissolve
                self.game_over_animation()

            self.remove_full_rows()

            # Render matrix
            current_block.render()
            self.render()

        # The Game has ended!
        return True

    def remove_full_rows(self):
        for index, row in enumerate(self.landed_blocks):
            # Check if this row is full
            if np.count_nonzero(row.sum(axis=1)) == self.landed_blocks.shape[1]:
                self.score += 1
                # Now move all rows above one pixel down
                for r in range(index, 1, -1):
                    self.landed_blocks[r] = self.landed_blocks[r - 1]
                # Clear top row
                self.landed_blocks[0] = np.zeros([12, 3])

    def game_over_animation(self):
        for i in range(4):
            self.output.empty_matrix()
            sleep(.3)
            self.render()
            sleep(.3)

    def render(self):
        for row, col in np.ndindex(self.landed_blocks.shape[0:2]):
            self.output.set_value_rgb(row, col, self.landed_blocks[row, col])

    def draw_icon(self, output):
        super().draw_icon(output)

        # Draw some blocks on the canvas
        Tetromino(self, origin=(9, 1), shape="T", color="red").dissolve()
        Tetromino(self, origin=(10, 4), shape="I", color="blue").dissolve()
        Tetromino(self, origin=(9, 6), shape="J", color="yellow").dissolve()
        Tetromino(self, origin=(9, 9), shape="O", color="blue").dissolve()
        Tetromino(self, origin=(8, 3), shape="L", color="purple").dissolve()
        Tetromino(self, origin=(7, 3), shape="S", color="brown").dissolve()
        Tetromino(self, origin=(3, 5), shape="Z", color="red").dissolve()

        self.output.show()


class Tetromino:
    """ Class representing one Tetris Block"""
    # List of initial coordinates for different block shapes
    # The coordinates are relative to the block's origin
    # Tuples are arranged in (row, col)
    shapes = {
        'I': {(0, 0), (0, 1), (0, 2), (0, 3)},
        'J': {(0, 0), (0, 1), (0, 2), (1, 2)},
        'L': {(1, 0), (1, 1), (1, 2), (0, 2)},
        '0': {(0, 0), (0, 1), (1, 0), (1, 1)},
        'T': {(1, 0), (1, 0), (1, 0), (1, 2)},
        'S': {(1, 0), (1, 1), (0, 1), (0, 2)},
        'Z': {(0, 0), (0, 1), (1, 1), (1, 2)}
    }

    def __init__(self, GameInstance, origin=(0, 5), shape=None, color=None):
        self.game = GameInstance
        self.origin = origin

        # Set shape
        if shape is None:
            # Select shape and color randomly
            random.seed()
            letter, self.pixels = random.choice(list(self.shapes.items()))
        else:
            self.pixels = self.shapes[shape]

        # Choose color
        if color is None:
            # Todo Select random color from output class
            self.color = "red"
        else:
            self. color = color

    def _check_validity(self, intended_origin, intended_pixels):
        """  Check if block could be moved to an intended position

        Args:
            intended_origin: Origin of suggested block position
            intended_pixels: Pixels of suggested block

        Returns:
            bool: False if that position would produce a collision. True otherwise.
        """
        # Check validity for each pixel one by one
        for intended_pixel in intended_pixels:
            row = intended_origin(0) + intended_pixel(0)
            col = intended_origin(1) + intended_pixel(1)

            if (row < 0) or (row > self.game.output.rows):
                return False
            if (col < 0) or (col > self.game.output.columns):
                return False
            if (self.game.landed_blocks[row, col] != (0, 0, 0)) and \
                    (intended_pixel not in self.pixels):
                # This pixel is already occupied by another fallen block
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
            rotated_pixel = (pixel[0], -pixel[1])
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
        new_origin = (self.origin[0], self.origin[1] - 1)

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
        new_origin = (self.origin[0], self.origin[1] + 1)

        if self._check_validity(new_origin, self.pixels):
            self.origin = new_origin
            return True
        else:
            return False

    def fall(self):
        """ Moves block one field down if possible.

        Returns:
            bool:   False, if falling is not possible, e.g. blocks would ground wall or other block.
        """
        new_origin = (self.origin[0] + 1, self.origin[1])

        if self._check_validity(new_origin, self.pixels):
            self.origin = new_origin
            return True
        else:
            return False

    def dissolve(self):
        """ Blocks is transformed to permanent pixel.

        Is called when falling isn't possible anymore. Therefore the block is added to the
        pixel_matrix as permament pixel and the class instance is destructed.

        Returns:
            bool: False, if dissolving would end in invalid move, e.g. game is over.
        """
        for pixel in self.pixels:
            self.game.output.set_value_color(pixel[0], pixel[1], self.color)

    def render(self):
        """ Adds this block to the outputs matrix. Note: Does not call Output.show()
        """
        for pixel in self.pixels:
            self.game.output.set_value_color(pixel[0], pixel[1], self.color)
