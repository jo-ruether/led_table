from games.Snake import Snake
from games.Game import Game
from games.Colorfade import Colorfade
from games.Clock import Clock
from games.Tetris import Tetris
from games.Spotify import Spotify
from games.Pong import Pong

from core.Postman import Topics, CMD

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class Menu(Game):
    def __init__(self, postman, output, config_handler):
        super().__init__(postman, output)

        # Track if a gaming is currently running
        self.running = False

        # List of available games
        self.current_selection = 0
        self.games = [Spotify(postman, output, config_handler),
                      Snake(postman, output),
                      Colorfade(postman, output),
                      Clock(postman, output),
                      Tetris(postman, output),
                      Pong(postman, output)]

    def move_left(self):
        self.current_selection -= 1

        if self.current_selection < 0:
            self.current_selection = len(self.games) - 1

        self.games[self.current_selection].draw_icon(self.output)

    def move_right(self):
        self.current_selection += 1

        if self.current_selection >= len(self.games):
            self.current_selection = 0

        self.games[self.current_selection].draw_icon(self.output)

    def start_game(self):
        # Check if game is running
        if self.running:
            return False

        # Start Snake and wait for return
        self.running = True
        self.games[self.current_selection].start()
        self.running = False

        # Return to menu and draw icon
        self.games[self.current_selection].draw_icon(self.output)

        return True

    def read_input(self):
        post = self.postman.request(Topics.INPUT)
        if post:
            cmd = post['message']

            if cmd == CMD.LEFT:
                self.move_left()
            elif cmd == CMD.RIGHT:
                self.move_right()
            elif cmd == CMD.X:
                self.start_game()

    def start(self):
        # Draw icon
        self.games[self.current_selection].draw_icon(self.output)

        # Read input queue and wait for commands
        while True:
            self.read_input()

