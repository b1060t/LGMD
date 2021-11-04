import numpy as np
from module.hex import Hex
from module.utils import GetLine
from module.config import Config
from module.movement import Rectangle
from math import floor

class Screen:
	def __init__(self, width:int, height:int, hexRad):
		# width -> x, height -> y
		self.map = np.zeros((width, height))

		# maximum hexagons number
		rowNum = floor((height + hexRad) / (3 * hexRad)) * 2 + 1
		colNum = floor(width / (np.sqrt(3) * hexRad)) + 2

		rRange = range(0, int((rowNum - 1) / 2))
		cRange = range(0, colNum - 1)

		self.hexList:list[Hex] = []

		# a == 0
		for rIdx in rRange:
			if rIdx == 0:
				continue
			for cIdx in cRange[1:]:
				self.hexList.append(Hex(0, rIdx, cIdx, hexRad))
		
		# a == 1
		for rIdx in rRange:
			for cIdx in cRange[:-1]:
				self.hexList.append(Hex(1, rIdx, cIdx, hexRad))

		for hex in self.hexList:
			xy = [hex.coord.xy[0, 0] * hexRad, hex.coord.xy[1, 0] * hexRad]
			xRange = list(range(int(np.ceil(xy[0]-(np.sqrt(3)*hexRad/2))), int(np.ceil(xy[0]+(np.sqrt(3)*hexRad/2)))))
			yRange = list(range(int(np.ceil(xy[1]-hexRad)), int(np.ceil(xy[1]+hexRad))))
			k1, b1 = GetLine(xy[0]-np.sqrt(3)*hexRad/2, xy[1]-hexRad/2, xy[0], xy[1]-hexRad)
			k2, b2 = GetLine(xy[0]+np.sqrt(3)*hexRad/2, xy[1]-hexRad/2, xy[0], xy[1]-hexRad)
			k3, b3 = GetLine(xy[0]-np.sqrt(3)*hexRad/2, xy[1]+hexRad/2, xy[0], xy[1]+hexRad)
			k4, b4 = GetLine(xy[0]+np.sqrt(3)*hexRad/2, xy[1]+hexRad/2, xy[0], xy[1]+hexRad)
			for x in xRange:
				for y in yRange:
					if x >= width or y >= height or k1*x+b1 > y or k2*x+b2 > y or k3*x+b3 < y or k4*x+b4 < y:
						continue
					hex.pixels.append([x, y])
		# Now all pixels have been mapped to the hexagons

		self.eye = [width / 2, height / 2, -Config.DISTANCE]

	def render(self, objList:list):
		# Clear
		self.map.fill(0)
		# perspective projection
		# xy plane: z=0
		# line from the eye to the origin intersect the plane
		o: Rectangle
		for o in objList:
			if o.trace == []:
				continue
			origin = o.pop()
			# Ze/(Ze-Zo)
			scale = self.eye[2] / (self.eye[2] - origin[2])
			width = int(o.width * scale)
			height = int(o.height * scale)
			pos = [0, 0]
			# (y-ye)/(yo-ye)=Ze/(Ze-Zo)
			pos[0] = int((origin[0] - self.eye[0]) * scale + self.eye[0])
			pos[1] = int((origin[1] - self.eye[1]) * scale + self.eye[1])
			for w in range(0, width):
				for h in range(0, height):
					if pos[0] + w < self.map.shape[0] and pos[1] + h < self.map.shape[1]:
						self.map[w + pos[0], h + pos[1]] = Config.PIXEL
		

