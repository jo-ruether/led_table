import random
import numpy as np
from time import time, sleep

from games.Game import Game
from core.Postman import Topics, CMD

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Tetris(Game):
    def __init__(self, postman, output):
        super().__init__(postman, output)
        # Stores landed blocks as RGB values
        self.landed_blocks = np.zeros([self.output.rows, self.output.columns, 3])

        self.running = False
        self.score = 0
        self.current_block = None

    def check_user_input(self):
        """ Asks postman for user input """
        post = self.postman.request(Topics.INPUT)
        while post:
            cmd = post['message']
            if cmd == CMD.LEFT:
                self.current_block.move_left()
            elif cmd == CMD.RIGHT:
                self.current_block.move_right()
            elif cmd == CMD.DOWN:
                self.current_block.fall()
            elif cmd == CMD.X:
                self.current_block.rotate()
            elif cmd == CMD.START:
                self.running = False

            # Check if there is even more to read
            post = self.postman.request(Topics.INPUT)

    def start(self):
        self.running = True

        # Init variables
        t_last_falling = 0
        self.landed_blocks = np.zeros([self.output.rows, self.output.columns, 3])
        self.score = 0
        self.current_block = Tetromino(self, (0, self.output.columns // 2 - 1))
        self.output.empty_matrix()

        while self.running:
            speed = .8

            if (time() - t_last_falling) > speed:
                t_last_falling = time()

                # Check if block has landed
                if not self.current_block.fall():
                    if not self.current_block.dissolve():
                        # Game over
                        break
                    else:
                        # Create new block
                        self.current_block = Tetromino(self, (0, self.output.columns // 2 - 1))
                        # Immediately break if there is no space left
                        if not self.current_block.check_validity(self.current_block.origin,
                                                                 self.current_block.pixels):
                            break

            # Render matrix (order important!)
            self.render()
            self.current_block.render()
            self.output.show()

            # Check for user input
            self.check_user_input()

            self.remove_full_rows()

        # Game is over !
        self.running = False

        # Send score to user
        congratulations = f"Well done. You scored {self.score} points!"
        self.postman.send(Topics.OUTPUT, congratulations)

        # Block couldn't dissolve
        self.game_over_animation()

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
            self.output.show()
            sleep(.3)

    def render(self):
        for row, col in np.ndindex(self.landed_blocks.shape[0:2]):
            self.output.set_value_rgb(row, col, self.landed_blocks[row, col])

    def draw_icon(self, output):
        super().draw_icon(output)

        # Draw some blocks on the canvas
        Tetromino(self, origin=(9, 2), shape="T", color="red").render()
        Tetromino(self, origin=(10, 5), shape="I", color="blue").render()
        Tetromino(self, origin=(9, 7), shape="J", color="yellow").render()
        Tetromino(self, origin=(9, 10), shape="O", color="blue").render()
        Tetromino(self, origin=(8, 4), shape="L", color="purple").render()
        Tetromino(self, origin=(7, 4), shape="S", color="green").render()
        Tetromino(self, origin=(3, 6), shape="Z", color="red").render()

        self.output.show()


class Tetromino:
    """ Class representing one Tetris Block"""
    # List of initial coordinates for different block shapes
    # The coordinates are relative to the block's origin
    # Tuples are arranged in (row, col)
    shapes = {
        'I': {(0, -1), (0, 0), (0, 1), (0, 2)},
        'J': {(0, -1), (0, 0), (0, 1), (1, 1)},
        'L': {(1, -1), (1, 0), (1, 1), (0, 1)},
        'O': {(0, -1), (0, 0), (1, -1), (1, 0)},
        'T': {(1, -1), (1, 0), (0, 0), (1, 1)},
        'S': {(1, -1), (1, 0), (0, 0), (0, 1)},
        'Z': {(0, -1), (0, 0), (1, 0), (1, 1)}
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
            colormap = self.game.output.colormap
            self.color = random.choice(list(colormap.keys()))
        else:
            self. color = color

    def check_validity(self, intended_origin, intended_pixels):
        """  Check if block could be moved to an intended position

        Args:
            intended_origin: Origin of suggested block position
            intended_pixels: Pixels of suggested block

        Returns:
            bool: False if that position would produce a collision. True otherwise.
        """
        # Check validity for each pixel one by one
        for intended_pixel in intended_pixels:
            row = intended_origin[0] + intended_pixel[0]
            col = intended_origin[1] + intended_pixel[1]

            if (row < 0) or (row >= self.game.output.rows):
                return False
            if (col < 0) or (col >= self.game.output.columns):
                return False
            if np.any(self.game.landed_blocks[row, col]):
                # This pixel is already occupied by another fallen block
                return False

        # Intended position passed all tests
        return True

    def _get_absolute_pixels(self):
        absolute_pixels = set()
        for pixel in self.pixels:
            row = self.origin[0] + pixel[0]
            col = self.origin[1] + pixel[1]
            absolute_pixels.add((row, col))

        return absolute_pixels

    def rotate(self):
        """ Rotates block if possible.

        Returns:
            bool:   False if rotation is not possible, e.g. blocks would hit wall or other block.
        """
        new_pixels = set()

        # Rotate each pixel one by one in clockwise direction
        for pixel in self.pixels:
            rotated_pixel = (-pixel[1], pixel[0])
            new_pixels.add(rotated_pixel)

        if self.check_validity(self.origin, new_pixels):
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

        if self.check_validity(new_origin, self.pixels):
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

        if self.check_validity(new_origin, self.pixels):
            self.origin = new_origin
            return True
        else:
            return False

    def fall(self):
        """ Moves block one field down if possible.

        Returns:
            bool:   False, if falling is not possible, e.g. blocks would ground wall or other block.
        """
        new_origin = (self.origin[0]+1, self.origin[1])

        if self.check_validity(new_origin, self.pixels):
            self.origin = new_origin
            return True
        else:
            return False

    def dissolve(self):
        """ Blocks is transformed to permanent pixel.

        Is called when falling isn't possible anymore. Therefore the block is added to the
        landed_blocks of the game.

        Returns:
            bool: False, if dissolving would end in invalid move, e.g. game is over.
        """
        if not self.check_validity(self.origin, self.pixels):
            return False

        for pixel in self.pixels:
            row = self.origin[0] + pixel[0]
            col = self.origin[1] + pixel[1]

            self.game.landed_blocks[row, col] = self.game.output.color_to_rgb(self.color)

        return True

    def render(self):
        """ Adds this block to the outputs matrix. Note: Does not call Output.show()
        """
        for pixel in self.pixels:
            self.game.output.set_value_color(self.origin[0]+pixel[0],
                                             self.origin[1]+pixel[1],
                                             self.color)
