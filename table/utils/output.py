import board
import neopixel
import colorsys


class Output:
    def __init__(self, rows=12, columns=12):
        self.pixels = neopixel.NeoPixel(board.D18, rows*columns, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)
        self.pixels.fill((0, 0, 0))

        self.rows = rows
        self.columns = columns

        self.pixelMatrix = [[(0,0,0) for x in range(columns)] for y in range(rows)]
        self.colorMap ={}

    def XYToPixel(self,x,y):
        """
        Converts XY coordinates into Pixel number. The origin is located in the upper left corner
        of the matrix.
        """
        if y%2 == 0:
            value = x+y*12
        else:
            value = y*12 + 11-x
        return value

    def setValueRGB(self,x,y,rgbTuple):
        pixel = self.XYToPixel(x,y)
        self.pixels[pixel] = rgbTuple
        self.pixelMatrix[x][y] = rgbTuple

    def setValueHSV(self,x,y,h,s,v):
        rgb = colorsys.hsv_to_rgb(h,s,v)
        # Scale from range 0-1 up to 255 for Neopixel library
        rgbTuple = tuple([round(255*x) for x in rgb])

        pixel = self.XYToPixel(x,y)
        self.pixels[pixel] = rgbTuple
        self.pixelMatrix[x][y] = rgbTuple

    def setValueColor(self,x,y,color):
        if (color in self.colorMap):
            self.setValueRGB(x,y,self.colorMap[color])
        else:
            print ("Color not predefined. Value is not changed!")

    def show(self):
        if (len(self.pixelMatrix) == self.rows and len(self.pixelMatrix[0]) == self.columns):
            for x,row in enumerate(self.pixelMatrix):
                for y,rgbValue in enumerate(row):
                    self.setValueRGB(x,y,rgbValue)
            self.pixels.show()

    def emptyMatrix(self):
        """
        Clears pixelMatrix and writes it out to the table (callling showRGB())
        """
        self.pixelMatrix = [[(0,0,0) for x in range(self.columns)] for y in range(self.rows)]
        self.show()
