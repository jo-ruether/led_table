import board
import neopixel
from table.Output import Output


class OutputTable(Output):
    def __init__(self, rows=12, columns=12):
        super().__init__(rows=rows, columns=columns)
        self.pixels = neopixel.NeoPixel(board.D18, rows*columns, brightness=0.2,
                                        auto_write=False, pixel_order=neopixel.GRB)
        self.pixels.fill((0, 0, 0))

    def xy_to_pixel(self, x, y):
        """
        Converts XY coordinates into Pixel number. The origin is located in the upper left corner
        of the matrix.
        """
        if y%2 == 0:
            value = x+y*12
        else:
            value = y*12 + 11-x
        return value

    def show(self):
        # if len(self.pixel_matrix) == self.rows and len(self.pixel_matrix[0]) == self.columns:
        for x, row in enumerate(self.pixel_matrix):
            for y, rgb_value in enumerate(row):
                pixel = self.xy_to_pixel(x, y)
                self.pixels[pixel] = rgb_value
        self.pixels.show()
