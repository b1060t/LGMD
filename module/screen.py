import numpy as np
from module.hex import Hex
from module.utils import GetLine
from math import floor

class Screen:
	def __init__(self, width, height, hexRad):
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
			xy = hex.coord.xy * hexRad
			xRange = list(range(int(np.ceil(xy[0]-(np.sqrt(3)*hexRad/2))), int(np.ceil(xy[0]+(np.sqrt(3)*hexRad/2)))))
			yRange = list(range(int(np.ceil(xy[1]-hexRad)), int(np.ceil(xy[1]+hexRad))))
			k1, b1 = GetLine(xy[0]-np.sqrt(3)*hexRad/2, xy[1]-hexRad/2, xy[0], xy[1]-hexRad)
			k2, b2 = GetLine(xy[0]+np.sqrt(3)*hexRad/2, xy[1]-hexRad/2, xy[0], xy[1]-hexRad)
			k3, b3 = GetLine(xy[0]-np.sqrt(3)*hexRad/2, xy[1]+hexRad/2, xy[0], xy[1]+hexRad)
			k4, b4 = GetLine(xy[0]+np.sqrt(3)*hexRad/2, xy[1]+hexRad/2, xy[0], xy[1]+hexRad)
			for x in xRange:
				for y in yRange:
					if k1*x+b1 > y or k2*x+b2 > y or k3*x+b3 < y or k4*x+b4 < y:
						continue
					hex.pixels.append([x, y])
		# Now all pixels have been mapped to the hexagons
