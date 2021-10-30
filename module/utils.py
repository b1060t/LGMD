import numpy as np

def GetLine(x1, y1, x2, y2):
	k = (y2 - y1) / (x2 - x1)
	b = y1 - k * x1
	return k, b