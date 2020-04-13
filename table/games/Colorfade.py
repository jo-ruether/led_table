from table.games.Game import Game
from time import time
from math import sqrt


class Colorfade(Game):
    def start(self):
        # Configuration
        speed = 0.5 # s per change
        period = 10 # steps per a whole hue iteration
        saturation = 1
        value = 1

        # Retrieve dimensions of
        columns = self.output.columns
        rows = self.output.rows

        # Center of color cycle (x,y)
        center = (5.5, 5.5)
        # Calculate maximal possible distance from center to norm hue later
        # TODO really calculate that
        max_distance = 7.78

        while True:
            # Check for termination signal (any command)
            if self.input_q.qsize() > 0:
                # Get element from queue so that command isn't processed twice
                cmd = self.input_q.get()
                return True

            t = time()
            for x in range(columns):
                for y in range(rows):
                    # Hue depends on the pixels distance to the center and on time
                    # TODO add time
                    hue = 255 - \
                          sqrt((x-center[0])**2 + (y-center[1])**2)/max_distance + \
                          (t//speed/period)
                    self.output.setValueHSV(x, y, hue, saturation, value)

            self.output.show()


    def draw_icon(self, output):
        super().draw_icon(output)

        # Retrieve dimensions of
        columns = 10
        rows = 10

        # Center of color cycle (x,y)
        center = (5, 5)
        # Calculate maximal possible distance from center to norm hue later
        # TODO really calculate that
        max_distance = 7

        for x in range(columns):
            for y in range(rows):
                # Hue depends on the pixels distance to the center and on time
                hue = sqrt((x-center[0])**2 + (y-center[1])**2)/max_distance
                self.output.setValueHSV(x+1, y+1, hue, 1, 1)

        output.show()
