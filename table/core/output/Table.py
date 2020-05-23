import board
import neopixel
from core.output.Output import Output
import numpy as np


class Table(Output):
    def __init__(self, rows=12, columns=12):
        super().__init__(rows=rows, columns=columns)
        self.pixels = neopixel.NeoPixel(board.D18, rows*columns, brightness=0.2,
                                        auto_write=False, pixel_order=neopixel.GRB)
        self.pixels.fill((0, 0, 0))

    def matrix_index_to_led_number(self, row, col):
        """
        Converts XY coordinates into Pixel number. The origin is located in the upper left corner
        of the matrix.
        """
        if row % 2 == 0:
            value = col + row*self.columns
        else:
            value = row*12 + 11-col
        return value

    def show(self):
        super().show()

        for id_row, id_col in np.ndindex(self.pixel_matrix.shape[0:2]):
            led_position = self.matrix_index_to_led_number(id_row, id_col)
            self.pixels[led_position] = self.pixel_matrix[id_row, id_col].astype('uint8')

        self.pixels.show()
