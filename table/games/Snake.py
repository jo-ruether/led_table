import time
from random import randint
from time import sleep

from table.games.Game import Game
from table.Postman import Topics

class Snake(Game):
    # Define snake, fruit and background color
    snake_color = (5, 255, 5)
    fruit_color = (255, 0, 0)
    head_color = (10, 255, 255)
    garden_color = (0, 0, 0)

    def __init__(self, postman, output):
        super().__init__(postman, output)

        # Initialize directions
        self.compass = ["north", "east", "south", "west"]
        self.direction = randint(1, 3)

        # Snake is a list of coordinates
        self.snake = [(5, 5), (5, 6), (5, 7)]
        # Fruit coordinate
        self.fruit = (randint(5, 11), randint(7, 11))

        # Checks if game is still running. Thread is terminated if False.
        self.active = True

        # Initialize display elements
        self.update_pixel_matrix()
        self.print_world()

    def move_snake(self):
        """ Performs the snake's next step
        """
        # Check if game is over because snake bit itself        
        if self.snake[0] in self.snake[1:]:
            print("Game over")
            self.active = False

        else:
            # Check if fruit was eaten
            if self.snake[0] == self.fruit:
                # Place new fruit, but not where the snake currently is
                while True:
                    self.fruit = (randint(0, 11), randint(0, 11))
                    if self.fruit not in self.snake:
                        break
            else:
                # Delete tail element of snake
                self.snake.pop()
            # Check for direction and place head accordingly
            if self.compass[self.direction] == "east":
                x_new = self.snake[0][0] + 1
                y_new = self.snake[0][1]
            elif self.compass[self.direction] == "west":
                x_new = self.snake[0][0] - 1
                y_new = self.snake[0][1]
            elif self.compass[self.direction] == "north":
                x_new = self.snake[0][0]
                y_new = self.snake[0][1] + 1
            elif self.compass[self.direction] == "south":
                x_new = self.snake[0][0]
                y_new = self.snake[0][1] - 1
            self.snake = [(x_new % 12, y_new % 12)] + self.snake

    def update_pixel_matrix(self):
        """Prepares the matrix, displaying the snake and the fruit 
        """
        self.output.fill_matrix_rgb(self.garden_color)

        # Draw the fruit
        self.output.pixel_matrix[self.fruit[0], self.fruit[1]] = self.fruit_color
        # Draw the snake
        i = 0
        for s in self.snake:
            self.output.pixel_matrix[s[0], s[1]] = self.snake_color
        # Draw snake head
        self.output.pixel_matrix[self.snake[0][0], self.snake[0][1]] = self.head_color

    def print_world(self):
        """ Prints the world matrix to the table
        """
        self.output.show()

    def update_direction(self):
        """ Reacts to commands in the input queue and updates the direction accordingly
        """
        post = self.postman.request(Topics.INPUT)
        if post:
            cmd = post['message']
            # Change snake's direction according to input
            if cmd == 'right':
                self.direction = (self.direction + 1) % 4
            elif cmd == 'left':
                self.direction = (self.direction - 1) % 4

    def game_over_animation(self):
        """ Animation to show when the game is over
        """
        last_pixel_matrix = self.output.pixel_matrix
        for i in range(4):
            self.output.empty_matrix()
            self.print_world()
            sleep(0.3)
            self.output.pixel_matrix = last_pixel_matrix
            self.update_pixel_matrix()
            self.print_world()
            sleep(0.3)

    def start(self):
        """ Runs the game
        """
        while self.active:
            self.update_direction()
            self.move_snake()
            self.update_pixel_matrix()
            self.print_world()
            time.sleep(0.2)
        self.postman.send(Topics.OUTPUT, f"Well done. Your snake grew up to a size of "
                                         f"{len(self.snake)}")
        self.game_over_animation()
        return False

    # TODO make static but how to access colors then?
    def draw_icon(self, output):
        """
        Draws a dummy fruit and a dummy snake as icon on a given output.
        """
        super().draw_icon(output)

        # dummy fruit
        output.set_value_rgb(3, 4, self.fruit_color)
        # dummy snake
        output.pixel_matrix[7, 2:6] = self.snake_color
        output.pixel_matrix[8, 5:9] = self.snake_color
        output.pixel_matrix[8, 5:9] = self.snake_color
        output.pixel_matrix[4:9, 8] = self.snake_color

        output.show()
