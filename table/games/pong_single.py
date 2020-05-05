from output import Output
import time
import copy
from random import randint
from time import sleep

class Pong():
    """ This class implements the game snake.
    
    24.03.2019
    """
    def __init__(self, input_q, world_dim=(12, 12)):
        self.input_q = input_q
        self.world_dim = world_dim
        
        self.racket = [(5,0), (6,0), (7,0)]
        self.player_wall = [(x,0) for x in range(world_dim[0])] 
        self.neutral_wall_top = [(0,y) for y in range(world_dim[1])]
        self.neutral_wall_right = [(x,11) for x in range(world_dim[0])]
        self.neutral_wall_bottom = [(11,y) for y in range(world_dim[1])]
        
        self.ball = (5, 5)
        self.ball_direction = (1, 1)
        
        self.ball_color = (5, 255, 5)
        self.racket_color = (255, 0, 0)
        self.bground_color = (0, 0, 0)
        
        self.active = True
        
        self.output = Output(world_dim[0], world_dim[1])
        self.update_pixelMatrix()
        self.print_world()
        
    def ball_move(self):
        self.ball = (self.ball[0]+self.ball_direction[0], self.ball[1]+self.ball_direction[1])
        
    def update_direction(self):
        hasHitWall = self.hit_wall()
        hasHitRacket = self.hit_racket()
        if (hasHitWall and hasHitRacket):
            self.hit_wall()
        self.hit_player_wall()
        
    def hit_racket(self):
        # Influence area around the racket where action is necessary
        virtualMove = (self.ball[0]+self.ball_direction[0], self.ball[1]+self.ball_direction[1])
        racket_wall = [(x, 1) for x in range(self.racket[0][0]-1, self.racket[-1][0]+2)]
        if self.ball in racket_wall[1:-1]:
            self.ball_direction = (self.ball_direction[0], -self.ball_direction[1])
            return True
        elif virtualMove in self.racket:
            self.ball_direction = (-self.ball_direction[0], -self.ball_direction[1]) 
            return True
        else:
            return False    
        
    def hit_wall(self): 
        hasHitWall = False
        if self.ball in self.neutral_wall_top or self.ball in self.neutral_wall_bottom:
            self.ball_direction = (-self.ball_direction[0], self.ball_direction[1])
            hasHitWall = True
        if self.ball in self.neutral_wall_right:
            self.ball_direction = (self.ball_direction[0], -self.ball_direction[1])
            hasHitWall = True
        return hasHitWall
    def hit_player_wall(self):
        if self.ball in self.player_wall:
            self.game_over_animation()
            self.active = False
            
    def update_racket(self):
        if self.input_q.qsize() > 0:
            input = self.input_q.get()
            self.input_q.task_done()
            if input == CMD.RIGHT:
                self.racket = [(max(coord[0]-1, 0+i), coord[1]) for i, coord in enumerate(self.racket)]
            elif input == CMD.LEFT:
                self.racket = [(min(coord[0]+1, self.world_dim[0]-3+i), coord[1]) for i, coord in enumerate(self.racket)]

    def update_pixelMatrix(self):
        """Prepares the matrix, displaying the snake and the fruit 
        """
        for x, row in enumerate(self.output.pixelMatrix):
            for y, col in enumerate(self.output.pixelMatrix):
                self.output.pixelMatrix[x][y] = self.bground_color

        # Draw the ball
        self.output.pixelMatrix[self.ball[0]][self.ball[1]] = self.ball_color
        # Draw the racket
        i = 0
        for s in self.racket:
            self.output.pixelMatrix[s[0]][s[1]] = self.racket_color
        
    def print_world(self):
        """ Prints the world matrix to the table
        """
        self.output.show()
 
    def clean_world(self):
        """ Fill the whole matrix with zeros
        """
        for x, row in enumerate(self.output.pixelMatrix):
            for y, col in enumerate(self.output.pixelMatrix):
                self.output.pixelMatrix[x][y] = (0,0,0)
 
    def game_over_animation(self):
        """ Animation to show when the game is over
        """
        last_pixelMatrix = self.output.pixelMatrix
        for i in range(4):
            self.clean_world()
            self.print_world()
            sleep(0.3)
            self.output.pixelMatrix = last_pixelMatrix
            self.update_pixelMatrix()
            self.print_world()
            sleep(0.3)

    def start(self):
        """ Runs the game
        """
        while self.active==True:
            startTime = time.time()
            while(time.time() < startTime + 0.2):
                self.update_racket()
                self.update_pixelMatrix()
                self.print_world()
            self.update_direction()
            self.ball_move()
            self.update_pixelMatrix()
            self.print_world()
        self.game_over_animation()
        return False

