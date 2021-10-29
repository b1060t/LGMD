import numpy as np

def getRadius(deg, dis):
	return dis * np.tan(deg * np.pi / 180)