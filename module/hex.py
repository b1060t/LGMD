import numpy as np

ConvertMatrix = np.matrix([[np.sqrt(3)/2, 0, np.sqrt(3)], [3/2, 3, 0]])

# https://en.wikipedia.org/wiki/Hexagonal_Efficient_Coordinate_System
class HexCoord:
	def __init__(self):
		self.coord = np.matrix([0, 0, 0]).T

	def __init__(self, a, r, c):
		self.coord = np.matrix([a, r, c]).T

	@property
	def a(self):
		return self.coord[0]
	@a.setter
	def a(self, val):
		self.coord[0] = val

	@property
	def r(self):
		return self.coord[1]
	@r.setter
	def r(self, val):
		self.coord[1] = val

	@property
	def c(self):
		return self.coord[2]
	@c.setter
	def c(self, val):
		self.coord[2] = val

	@property
	def xy(self) -> np.matrix:
		return ConvertMatrix * self.coord

class Hex:
	def __init__(self, a, r, c, rad):
		self.coord = HexCoord(a, r, c)
		self.radius = rad
		self.pixels = []

	#def __init__(self, a, r, c, deg, dis):
	#	self.coord = HexCoord(a, r, c)
	#	self.radius = dis * np.tan(deg * np.pi / 180)
	#	self.pixels = []
