import time
from table.games.Game import Game
import numpy as np
from time import strftime


class Clock(Game):
    def __init__(self, postman, output):
        super().__init__(postman, output)

        self.num2words = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
                          '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'}
        self.digits = np.load('digits.npz')

    def update_pixel_matrix(self, time_string):
        """Prepares the matrix, displaying all four digits
        """
        canvas = np.zeros([self.output.rows, self.output.columns, 3])
        canvas[0:5, 1:5] = self.digits[self.num2words[time_string[0]]]
        canvas[0:5, 7:11] = self.digits[self.num2words[time_string[1]]]
        canvas[7:13, 1:5] = self.digits[self.num2words[time_string[2]]]
        canvas[7:13, 7:11] = self.digits[self.num2words[time_string[3]]]

        canvas = 255*canvas
        self.output.pixel_matrix = canvas

    def start(self):
        """ Runs the clock
        """
        while True:
            time_string = strftime("%H%M")
            self.update_pixel_matrix(time_string)
            self.output.show()
            time.sleep(0.2)
        #return False

    # TODO make static but how to access colors then?
    def draw_icon(self, output):
        """
        Draws a dummy fruit and a dummy snake as icon on a given output.
        """
        super().draw_icon(output)

        frame_color = [255, 255, 255]
        needle_color = [200, 50, 50]

        self.output.pixel_matrix[2, 4:8] = frame_color

        self.output.pixel_matrix[4, [3, 8]] = frame_color
        self.output.pixel_matrix[7, [3, 8]] = frame_color
        self.output.pixel_matrix[3, [3, 4, 7, 8]] = frame_color
        self.output.pixel_matrix[8, [3, 4, 7, 8]] = frame_color
        self.output.pixel_matrix[9, 4:8] = frame_color
        self.output.pixel_matrix[4:8, 2] = frame_color
        self.output.pixel_matrix[4:8, 9] = frame_color

        self.output.pixel_matrix[4, 4] = needle_color
        self.output.pixel_matrix[5, 5] = needle_color
        self.output.pixel_matrix[6, 6:9] = needle_color

        output.show()
