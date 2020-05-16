import time
import copy
from random import randint
from time import sleep

from table.games.Game import Game
from table.core.Postman import Topics, CMD

class Pong(Game):
    """ This class implements the game snake.
    
    24.03.2019
    """
    ball_color = (5, 255, 5)
    racket_color = (255, 0, 0)
    background_color = (0, 0, 0)

    def __init__(self, postman, output):
        super().__init__(postman, output)

        self.racket = [(5, 0), (6, 0), (7, 0)]
        self.player_wall = [(x, 0) for x in range(self.output.rows)]
        self.neutral_wall_top = [(0, y) for y in range(self.output.columns)]
        self.neutral_wall_right = [(x, self.output.columns-1) for x in range(self.output.rows)]
        self.neutral_wall_bottom = [(self.output.rows-1, y) for y in range(self.output.columns)]
        
        self.ball = (5, 5)
        self.ball_direction = (1, 1)
        
        self.active = True

        self.update_pixel_matrix()

    def update_pixel_matrix(self):
        """
        Prepares the matrix, displaying the snake and the fruit
        """
        self.output.fill_matrix_rgb(self.background_color)

        # Draw the racket and ball
        for r in self.racket:
            self.output.pixel_matrix[r[0], r[1]] = self.racket_color
        self.output.pixel_matrix[self.ball] = self.ball_color

    def ball_move(self):
        self.ball = (self.ball[0]+self.ball_direction[0],
                     self.ball[1]+self.ball_direction[1])
        
    def update_direction(self):
        has_hit_wall = self.hit_wall()
        has_hit_racket = self.hit_racket()
        if has_hit_wall and has_hit_racket:
            self.hit_wall()
        self.hit_player_wall()
        
    def hit_racket(self):
        # Influence area around the racket where action is necessary
        virtual_move = (self.ball[0]+self.ball_direction[0], self.ball[1]+self.ball_direction[1])
        racket_wall = [(x, 1) for x in range(self.racket[0][0]-1, self.racket[-1][0]+2)]
        if self.ball in racket_wall[1:-1]:
            self.ball_direction = (self.ball_direction[0], -self.ball_direction[1])
            return True
        elif virtual_move in self.racket:
            self.ball_direction = (-self.ball_direction[0], -self.ball_direction[1]) 
            return True
        else:
            return False    
        
    def hit_wall(self):
        """
        Checks if ball has hit the wall, if yes updates the ball direction accordingly.

        Returns: True if ball has hit a wall, else False
        """

        has_hit_wall = False
        if self.ball in self.neutral_wall_top or self.ball in self.neutral_wall_bottom:
            self.ball_direction = (-self.ball_direction[0], self.ball_direction[1])
            has_hit_wall = True
        if self.ball in self.neutral_wall_right:
            self.ball_direction = (self.ball_direction[0], -self.ball_direction[1])
            has_hit_wall = True
        return has_hit_wall

    def hit_player_wall(self):
        if self.ball in self.player_wall:
            self.game_over_animation()
            self.active = False
            
    def update_racket(self):
        post = self.postman.request(Topics.INPUT)

        if post:
            cmd = post['message']
            # Change snake's direction according to input
            if cmd == CMD.RIGHT:
                self.racket = [(max(coord[0]-1, 0+i), coord[1]) for i, coord in enumerate(self.racket)]
            elif cmd == CMD.LEFT:
                self.racket = [(min(coord[0]+1, self.output.rows-3+i), coord[1]) for i, coord in enumerate(self.racket)]

    def print_world(self):
        """ Prints the world matrix to the table
        """
        self.output.show()

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
            start_time = time.time()

            # During a time of 0.2 seconds, allow a movement of the racket
            # but don't move the ball to limit the speed
            while time.time() < start_time + 0.2:
                self.update_racket()
                self.update_pixel_matrix()
                self.print_world()

            self.update_direction()
            self.ball_move()
            self.update_pixel_matrix()
            self.print_world()

        self.game_over_animation()
        return False

    def draw_icon(self, output):
        """
        Draws a dummy fruit and a dummy snake as icon on a given output.
        """
        super().draw_icon(output)

        # Draw the racket and ball
        for r in self.racket:
            output.pixel_matrix[r[0], r[1]+1] = self.racket_color

        output.pixel_matrix[self.ball[0], self.ball[0]] = self.ball_color
        output.pixel_matrix[self.ball[0]-1, self.ball[0]+1] = tuple(0.5 * x for x in self.ball_color)
        output.pixel_matrix[self.ball[0]-2, self.ball[0]+2] = tuple(0.2 * x for x in self.ball_color)

        output.show()

