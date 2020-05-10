import colorsys
from abc import ABC, abstractmethod
import numpy as np


class Output(ABC):
    def __init__(self, rows=12, columns=12):
        self.rows = rows
        self.columns = columns

        self.brightness = 0.8

        # RGB matrix set by the games
        self.pixel_matrix = np.zeros([rows, columns, 3], dtype=np.uint8)
        # RGB matrix corrected by a specified brightness value
        self.pixel_matrix_corrected = np.zeros([rows, columns, 3], dtype=np.uint8)

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

    def color_to_rgb(self, color):
        return self.colormap[color]

    @abstractmethod
    def show(self):
        # Apply brightness settings
        # Brightness formula (0.2126 * R + 0.7152 * G + 0.0722 * B)
        self.pixel_matrix_corrected = self.pixel_matrix * self.brightness

    def empty_matrix(self):
        """
        Clears pixelMatrix and writes it out to the table (callling showRGB())
        """
        self.pixel_matrix[:, :] = [0, 0, 0]
        self.show()

    def fill_matrix_rgb(self, rgb_values):
        self.pixel_matrix[:, :] = rgb_values
