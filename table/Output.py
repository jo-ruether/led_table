import colorsys
from abc import ABC, abstractmethod
import numpy as np


class Output(ABC):
    def __init__(self, rows=12, columns=12):
        self.rows = rows
        self.columns = columns

        self.pixel_matrix = np.zeros([rows, columns, 3])
        self.colormap = {
                            "blue": [66, 133, 244],
                            "red": [219, 68, 55],
                            "yellow": [244, 180, 0],
                            "green": [15, 157, 88],
                            "orange": [244, 113, 0],
                            "purple": [139, 0, 221],
                            "brown": [109, 76, 65],
        }

    def set_value_rgb(self, row, col, rgb_values):
        self.pixel_matrix[row, col] = rgb_values

    def set_value_hsv(self, row, col, h, s, v):
        rgb = colorsys.hsv_to_rgb(h, s, v)
        # Scale from range 0-1 up to 255 for Neopixel library
        rgb_values = [round(255*row) for row in rgb]
        self.pixel_matrix[row, col] = rgb_values

    def set_value_color(self, row, col, color):
        if color in self.colormap:
            self.set_value_rgb(row, col, self.colormap[color])
        else:
            print("Color not predefined. Value is not changed!")

    @abstractmethod
    def show(self):
        pass

    def empty_matrix(self):
        """
        Clears pixelMatrix and writes it out to the table (callling showRGB())
        """
        self.pixel_matrix[:, :] = [0, 0, 0]
        self.show()

    def fill_matrix_rgb(self, rgb_values):
        self.pixel_matrix[:, :] = rgb_values
