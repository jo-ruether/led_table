import time
from src.games.Game import Game
from random import randint
from time import sleep


class Snake(Game):
    # Define snake, fruit and background color
    snake_color = (5, 255, 5)
    fruit_color = (255, 0, 0)
    head_color = (10, 255, 255)
    garden_color = (0, 0, 0)

    def __init__(self, input_q, output):
        super().__init__(input_q, output)

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
        self.update_pixelMatrix()
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

    def update_pixelMatrix(self):
        """Prepares the matrix, displaying the snake and the fruit 
        """
        for x, row in enumerate(self.output.pixelMatrix):
            for y, col in enumerate(self.output.pixelMatrix):
                self.output.pixelMatrix[x][y] = self.garden_color

        # Draw the fruit
        self.output.pixelMatrix[self.fruit[0]][self.fruit[1]] = self.fruit_color
        # Draw the snake
        i = 0
        for s in self.snake:
            self.output.pixelMatrix[s[0]][s[1]] = self.snake_color
            # if length(self.snake) > 5:
            # i = i+1
            # self.output.pixelMatrix[s[0]][s[1]] = (self.snake_color[0], self.snake_color[1]-i*20, self.snake_color[2])
        # Draw snake head
        self.output.pixelMatrix[self.snake[0][0]][self.snake[0][1]] = self.head_color

    def print_world(self):
        """ Prints the world matrix to the table
        """
        self.output.show()

    def update_direction(self):
        """ Reacts to commands in the input queue and updates the direction accordingly
        """
        # Check for existing input
        if self.input_q.qsize() > 0:
            input = self.input_q.get()
            self.input_q.task_done()
            # Change snake's direction according to input
            if input == 'right':
                self.direction = (self.direction - 1) % 4
            elif input == 'left':
                self.direction = (self.direction + 1) % 4

    def game_over_animation(self):
        """ Animation to show when the game is over
        """
        last_pixelMatrix = self.output.pixelMatrix
        for i in range(4):
            self.output.emptyMatrix()
            self.print_world()
            sleep(0.3)
            self.output.pixelMatrix = last_pixelMatrix
            self.update_pixelMatrix()
            self.print_world()
            sleep(0.3)

    def start(self):
        """ Runs the game
        """
        while self.active:
            self.update_direction()
            self.move_snake()
            self.update_pixelMatrix()
            self.print_world()
            time.sleep(0.2)
        self.game_over_animation()
        return False

    # TODO make static but how to access colors then?
    def draw_icon(self, output):
        """
        Draws a dummy fruit and a dummy snake as icon on a given output.
        """
        super().draw_icon(output)

        # dummy fruit
        output.setValueRGB(3, 4, self.fruit_color)
        # dummy snake
        output.setValueRGB(7, 2, self.snake_color)
        output.setValueRGB(7, 3, self.snake_color)
        output.setValueRGB(7, 4, self.snake_color)
        output.setValueRGB(7, 5, self.snake_color)
        output.setValueRGB(8, 5, self.snake_color)
        output.setValueRGB(8, 6, self.snake_color)
        output.setValueRGB(8, 7, self.snake_color)
        output.setValueRGB(8, 8, self.snake_color)
        output.setValueRGB(7, 8, self.snake_color)
        output.setValueRGB(6, 8, self.snake_color)
        output.setValueRGB(5, 8, self.snake_color)
        output.setValueRGB(4, 8, self.snake_color)

        output.show()
