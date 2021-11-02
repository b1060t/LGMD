import numpy as np

class Rectangle:
	def __init__(self, trace:list, width, height):
		# Top left
		self.trace = trace
		self.width = width
		self.height = height

	def pop(self):
		return self.trace.pop(0)