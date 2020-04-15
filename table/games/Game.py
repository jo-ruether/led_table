from abc import ABC, abstractmethod


class Game(ABC):
    def __init__(self, postman, output):
        self.postman = postman
        self.output = output

    @abstractmethod
    def start(self):
        """
        Runs the game or program
        """
        pass

    def draw_icon(self, output):
        """
        Cleans matrix and draws border to indicate that a icon is displayed. Child classes draw
        their individual icon into the remaining centered submatrix of 10x10 pixel.

        Don't forget to call the super class's method when overwriting.
        """
        output.emptyMatrix()

        # Draw border around icon
        border_color = (255, 165, 0)    # orange
        cols = output.columns
        rows = output.rows
        for x in range(cols):
            output.setValueRGB(x, 0, border_color)
            output.setValueRGB(x, rows-1, border_color)

        for y in range(rows):
            output.setValueRGB(0, y, border_color)
            output.setValueRGB(cols-1, y, border_color)