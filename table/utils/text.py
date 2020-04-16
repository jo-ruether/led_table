from letters import def_letters
from output import Output

class Text:
    def __init__(self, string, dim=(12, 12), style=def_letters, space=1):
        self.string = string
        self.dim = dim
        self.style = style
        self.letter_height = style['height']
        self.letter_width = style['width']
        self.space = 1
        self.matrix = self.createCompleteMatrix(string)
		
		
		self.output = Output(world_dim[0], world_dim[1])
        self.startIdx = 0
        self.update_pixel_matrix()

        self.output = Output(dim[0], dim[1])

    def moveLeft(self):
		""" Have text scroll leftwards over the screen
		"""
        self.startIdx += 1
        self.update_pixel_matrix()
		
    def moveRight(self):
		""" Have text scroll rightwards over the screen
		"""
        self.startIdx -=1
        self.update_pixel_matrix()

    def set_text(self, string):
        self.string = string
        self.matrix = self.createCompleteMatrix(string)
        #self.update_pixelMatrix()

    def convert2matrix(self, string):
        matrix = [[0 for x in range(self.dim[0])] for y in range(self.dim[1])]
        m, n = 0, 0
        for letter in string:
            if letter == '\n':
                n = 0
                m += self.letter_height + self.space
                continue
            if m <= self.dim[0] - self.letter_height and n <= self.max_length - self.letter_width:
                for i, row in enumerate(self.style[letter]):
                    for j, val in enumerate(row):
                        matrix[m+i][n+j] = val
                n += self.letter_width + self.space
            else:
                break
        return matrix

    def createCompleteMatrix(self, string):
        height = self.style['height']
        width = self.style['width']

        self.totalWidth = (width+1) * len(self.string)

        matrix = [[0 for x in range(self.totalWidth)] for y in range(height)]

        for idx,letter in enumerate(string):
            for i, row in enumerate(self.style[letter]):
                for j, val in enumerate(row):
                    matrix[i][idx*(width+1) + j] = val
        return matrix

    def update_pixelMatrix(self):
        for idx1, row in enumerate(self.output.pixelMatrix):
            for idx2, val in enumerate(row):
                idx2True = (idx2 + self.startIdx)%self.totalWidth
                if (idx1 >= len(self.matrix)):
                    continue
                else:
                    if self.matrix[idx1][idx2True] == 1:
                        self.output.pixelMatrix[idx2][idx1] = (255, 255, 255)
                    else:
                        self.output.pixelMatrix[idx2][idx1] = (0,0,0)

        #print (self.pixelMatrix)



        # for idx1, row in enumerate(self.matrix):
        #     for idx2, val in enumerate(row):
        #         if idx2 >= self.dim[1]:
        #             break
        #         if (val == 1):
        #             self.pixelMatrix[idx2][idx1] = (255, 255, 255)
        #         else:
        #             self.pixelMatrix[idx2][idx1] = (0,0,0)

    def show(self):
        self.output.show(self.pixelMatrix)
