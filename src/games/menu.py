from src.games.Snake import Snake
from src.games.Game import Game
from src.games.Colorfade import Colorfade


class Menu(Game):
    def __init__(self, input_q, output):
        super().__init__(input_q, output)
        self.input_q = input_q

        # Track if a gaming is currently running
        self.running = False;

        # List of available games
        self.current_selection = 0
        self.games = [Snake(input_q, output), Colorfade(input_q, output)]

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
        if self.input_q.qsize() > 0:
            cmd = self.input_q.get()

            if cmd == "left":
                self.move_left()
            elif cmd == "right":
                self.move_right()
            elif cmd == "action":
                self.start_game()

    def start(self):
        # Draw icon
        self.games[self.current_selection].draw_icon(self.output)

        # Read input queue and wait for commands
        while True:
            self.read_input()

