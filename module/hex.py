import numpy as np

ConvertMatrix = np.matrix([[np.sqrt(3)/2, 0, np.sqrt(3)], [3/2, 3, 0]])

# https://en.wikipedia.org/wiki/Hexagonal_Efficient_Coordinate_System
class HexCoord:
	def __init__(self):
		self.a = 0
		self.r = 0
		self.c = 0

	def __init__(self, a, r, c):
		self.coord = np.matrix([a, r, c]).T
		self.a = a
		self.r = r
		self.c = c

	@property
	def xy(self) -> np.matrix:
		coord = np.matrix([self.a, self.r, self.c]).T
		return ConvertMatrix * coord

class Hex:
	def __init__(self, a, r, c, rad):
		self.coord = HexCoord(a, r, c)
		self.radius = rad
		self.pixels = []

	def isNear(self, coord:HexCoord):
		a = coord.a
		r = coord.r
		c = coord.c
		nearList = [
			HexCoord(1-a, r-(1-a), c-(1-a)),
			HexCoord(1-a, r-(1-a), c+a),
			HexCoord(a, r, c-1),
			HexCoord(a, r, c+1),
			HexCoord(1-a, r+a, c-(1-a)),
			HexCoord(1-a, r+a, c+a)
			]
		for n in nearList:
			if self.coord.a == n.a and self.coord.r == n.r and self.coord.c == n.c:
				return True
		return False

	def isNextNear(self, coord:HexCoord):
		a = coord.a
		r = coord.r
		c = coord.c
		# Exclude self
		if self.coord.a == a and self.coord.r == r and self.coord.c == c:
			return False
		# Near
		nearList = [
			HexCoord(1-a, r-(1-a), c-(1-a)),
			HexCoord(1-a, r-(1-a), c+a),
			HexCoord(a, r, c-1),
			HexCoord(a, r, c+1),
			HexCoord(1-a, r+a, c-(1-a)),
			HexCoord(1-a, r+a, c+a)
			]
		nxtNearList = []
		for n in nearList:
			# Exclude Near
			if self.coord.a == n.a and self.coord.r == n.r and self.coord.c == n.c:
				return False
			a = n.a
			r = n.r
			c = n.c
			tmpList = [
				HexCoord(1-a, r-(1-a), c-(1-a)),
				HexCoord(1-a, r-(1-a), c+a),
				HexCoord(a, r, c-1),
				HexCoord(a, r, c+1),
				HexCoord(1-a, r+a, c-(1-a)),
				HexCoord(1-a, r+a, c+a)
				]
			nxtNearList += tmpList
		for nn in nxtNearList:
			if self.coord.a == nn.a and self.coord.r == nn.r and self.coord.c == nn.c:
				return True
		return False


	#def __init__(self, a, r, c, deg, dis):
	#	self.coord = HexCoord(a, r, c)
	#	self.radius = dis * np.tan(deg * np.pi / 180)
	#	self.pixels = []
