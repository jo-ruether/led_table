from table.games.Game import Game
from time import time
from math import sqrt


class Colorfade(Game):
    def __init__(self, postman, output):
        super().__init__(postman, output)

        # Configuration
        self.speed = 0.5 # s per change
        self.period = 10 # steps per a whole hue iteration
        self.saturation = 1
        self.value = 1
        # Center of color cycle (x,y)
        self.center = (5.5, 5.5)

        # Is set to false when program should exit
        self.running = True

    def check_user_input(self):
        """ Asks postman for user input """
        post = self.postman.request('UserInput')
        if post:
            # Exit when there is any input during ColorFade
            self.running = False

    def check_settings(self):
        """ Asks postman for set commands"""
        post = self.postman.request('Settings')
        if post:
            cmd = post['message']

            # Todo Can we refactor that in to an iterable list for code clarity? So many lines...
            if cmd[0] == "speed":
                try:
                    value = float(cmd[1])
                    self.speed = value
                    self.postman.send('UserFeedback', "Speed set!")
                except ValueError:
                    self.postman.send('UserFeedback', "Value is not a convertible!")
            elif cmd[0] == "saturation":
                try:
                    value = float(cmd[1])
                    self.saturation = value
                    self.postman.send('UserFeedback', "Saturation set!")
                except ValueError:
                    self.postman.send('UserFeedback', "Value is not a convertible!")

    def start(self):
        # Retrieve dimensions of
        columns = self.output.columns
        rows = self.output.rows

        # Calculate maximal possible distance from center to norm hue later
        # TODO really calculate that
        max_distance = 7.78

        while self.running:
            # Check mailbox
            self.check_user_input()
            self.check_settings()

            t = time()
            for x in range(columns):
                for y in range(rows):
                    # Hue depends on the pixels distance to the center and on time
                    # TODO add time
                    hue = 255 - \
                          sqrt((x-self.center[0])**2 + (y-self.center[1])**2)/max_distance + \
                          (t//self.speed/self.period)
                    self.output.set_value_hsv(x, y, hue, self.saturation, self.value)

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
                self.output.set_value_hsv(x+1, y+1, hue, 1, 1)

        output.show()
