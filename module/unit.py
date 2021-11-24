import numpy as np
from module.config import Config
from module.screen import Screen
from module.hex import Hex

class Unit:
	def __init__(self, dist, pre):
		self.threshold = dist['threshold']
		self.delay = dist['delay']
		self.tau = dist['tau']
		self.refractory = dist['refractory']
		self.weight = dist['weight']

		# To simulate delay:
		# Maintain a list whose length = delay
		# e.g. delay = 2ms, interval = 1ms
		# Init: [F1 F2]
		# 1ms rest -> [F1 F2 F3] -> pop F1 -> [F2 F3] ->
		# 2ms excited -> [F2 F3 T4] -> pop F2 -> [F3 T4] ->
		# 3ms rest -> [F3 T4 F5] -> pop F3 -> [T4 F5] ->
		# 4ms rest -> [T4 F5 F6] -> pop T4 (output excitation) -> [F5 F6]
		# Input is at 2ms and output is at 4ms (2ms delay)
		self.excitations = [False for i in range(int(self.delay/Config.INTERVAL))]

		# (unit, proportional_weight)
		self.nxt = []

		## Add this unit to preUnit.nxt
		if pre != []:
			# First unit coord
			self.hex = pre[0][0].hex
			for p in pre:
				p[0].nxt.append((self, p[1]))
				

		self.input = 0.0
		self.output = 0.0

		self.rfrTime = 0.0
	
	def reset(self):
		self.excitations = [False for i in range(int(self.delay/Config.INTERVAL))]
		self.input = 0.0
		self.output = 0.0
		self.rfrTime = 0.0

	def InitializeHex(self, hex:Hex):
		self.hex = hex

	def Response(self):
		res = 0.0
		# Calculate output
		if self.excitations.pop(0):
			res = 1.0 * np.exp(-Config.INTERVAL / self.tau)
		else:
			res = self.output * (1 - Config.INTERVAL / self.tau)
		return res

	def Update(self):
		# Update excitation list
		if self.input > self.threshold:
			# Refractory time logic
			if self.rfrTime >= self.refractory:
				self.excitations.append(True)
				self.rfrTime = 0.0
			else:
				self.excitations.append(False)
				self.rfrTime += Config.INTERVAL
		else:
			self.excitations.append(False)
			self.rfrTime += Config.INTERVAL
		self.output = self.Response()
		self.input = 0.0
		return self.output

	def Forward(self):
		u: Unit
		for u in self.nxt:
			u[0].input += self.output * self.weight * u[1]
		return self.output

class Punit(Unit):
	def __init__(self, dist, scr:Screen, hex:Hex):
		super().__init__(dist, [])
		self.scr = scr
		self.hex = hex
		# Previous Illumination Sum
		self.preSum = 0
		self.duration = 0.0

	def reset(self):
		super().reset()
		self.preSum = 0
		self.duration = 0.0

	def Update(self):
		# Update excitation list
		# No refractory time in Punit
		self.excitations.append(self.SumIllumination())
		self.output = self.Response()
		return self.preSum

	def Response(self):
		#return super().Response()
		res = 0.0
		if self.excitations.pop(0):
			res = self.weight
			self.duration = 0.0
		else:
			if self.duration < 1.0 and self.output > 0.0:
				res = self.weight
				self.duration += Config.INTERVAL
			else:
				res = 0.0
				self.duration = 0.0
		return res

	def SumIllumination(self):
		sum = 0.0
		for p in self.hex.pixels:
			sum += self.scr.map[p[0], p[1]]
		if sum != self.preSum:
			# Detailed logic needed
			self.preSum = sum
			return True
		else:
			return False


class Sunit(Unit):
	def __init__(self, dist, pre, i1units, i2units):
		super().__init__(dist, pre)

		i1list = list(filter(lambda u: u.hex.isNear(self.hex.coord), i1units))
		i2list = list(filter(lambda u: u.hex.isNextNear(self.hex.coord), i2units))

		for i in i1list:
			i.nxt.append((self, 1/6))
		for i in i2list:
			i.nxt.append((self, 1/12))


class Funit(Unit):
	def __init__(self, dist, pre):
		super().__init__(dist, pre)
		self.preActivation = 0.0
		self.preNum = len(pre)
		self.rate = 0.0

		self.excitations = [0.0 for i in range(int(self.delay/Config.INTERVAL))]

	def Response(self):
		# Calculate output
		return -self.excitations.pop(0)

	def Update(self):
		activation = self.input / self.preNum
		self.rate = activation - self.preActivation
		if self.rate > Config.F_THRESHOLD:
			self.excitations.append(self.rate)
		else:
			self.excitations.append(0.0)
		self.output = self.Response()
		self.preActivation = activation
		return self.output

	def reset(self):
		super().reset()
		self.preActivation = 0.0
		self.rate = 0.0
		self.excitations = [0.0 for i in range(int(self.delay/Config.INTERVAL))]