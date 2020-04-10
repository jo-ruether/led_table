import board
import neopixel
import colorsys

class Output():
    def __init__(self, rows = 12, columns = 12):
        self.pixels = neopixel.NeoPixel(board.D18, rows*columns, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)
        self.pixels.fill((0, 0, 0))

        self.rows = rows
        self.columns = columns

        self.pixelMatrix = [[(0,0,0) for x in range(columns)] for y in range(rows)]
        self.colorMap ={}

    def XYToPixel(self,x,y):
        if y%2 == 0:
            value = x+y*12
        else:
            value = y*12 + 11-x
        return value

    def setValueRGB(self,x,y,rgbTuple):
        pixel = self.XYToPixel(x,y)
        self.pixels[pixel] = rgbTuple
        self.pixelMatrix[x][y] = rgbTuple

    def setValueColor(self,x,y,color):
        if (color in self.colorMap):
            self.setValueRGB(x,y,self.colorMap[color])
        else:
            print ("Color not predefined. Value is not changed!")

    def showRGB(self):
        if (len(self.pixelMatrix) == self.rows and len(self.pixelMatrix[0]) == self.columns):
            for x,row in enumerate(self.pixelMatrix):
                for y,rgbValue in enumerate(row):
                    self.setValueRGB(x,y,rgbValue)
            self.pixels.show()

    def showHSV(self):
        if (len(self.pixelMatrix) == self.rows and len(self.pixelMatrix[0]) == self.columns):
            for x,row in enumerate(self.pixelMatrix):
                for y,hsvValue in enumerate(row):
                    self.setValueRGB(x,y,colorsys.hsv_to_rgb(hsvValue[0],hsvValue[1],hsvValue[2]))
