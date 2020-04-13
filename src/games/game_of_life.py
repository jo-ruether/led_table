from output import Output
import random
import time
import copy

class World():
	def __init__(self,world_dim=(12, 12), color=(255, 255, 255), duration=-1):
		self.world = [[0 for x in range(world_dim[0])] for y in range(world_dim[1])]
		self.seed_world()
		#print(self.world)
		self.dims = world_dim
		self.color = color
		self.duration = duration
		self.output = Output(world_dim[0], world_dim[1])
		self.pixelMatrix = [[(0,0,0) for x in range(world_dim[0])] for y in range(world_dim[1])] 
		self.update_pixelMatrix()
		self.print_world()


	def seed_world(self):
		#print (self.world)

		for i in range(20):
			x = random.randint(3, 8)
			y = random.randint(3, 8)
			self.world[x][y] = 1
			#print (x, y)
			#print (self.world)

	def update_world(self):
		previous = copy.deepcopy(self.world)
		for idx1, row in enumerate(self.world):
			for idx2, val in enumerate(row):
				alive = previous[idx1][idx2]
				neighbours = -alive  # remove self from neighbour count
				for r in [-1, 0, 1]:
					for c in [-1, 0, 1]:
						if idx1+r >= 0 and idx1+r < self.dims[0] and idx2+c >= 0 and idx2+c < self.dims[1]:
							neighbours += previous[idx1+r][idx2+c]

				neighbours = max(0,neighbours)
				if alive:
					if neighbours < 2 or neighbours > 3:
						self.world[idx1][idx2] = 0
					else:
						self.world[idx1][idx2] = 1
				else:
					if neighbours == 3:
						self.world[idx1][idx2] = 1
					else:
						self.world[idx1][idx2] = 0

	def update_pixelMatrix(self):
		for idx1, row in enumerate(self.world):
			for idx2, val in enumerate(row):
				if (val == 1):
					self.pixelMatrix[idx1][idx2] = self.color
				else:
					self.pixelMatrix[idx1][idx2] = (0,0,0)


	def print_world(self):
		self.output.show(self.pixelMatrix)

	def start(self):
		if self.duration == -1:
			while True:
				self.update_world()
				self.update_pixelMatrix()
				self.print_world()
				time.sleep(0.5)

		else:
			for i in range(self.duration):
				self.update_world()
				self.update_pixelMatrix()
				self.print_world()
				time.sleep(0.5)
