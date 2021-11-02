from functools import reduce
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

		self.hex:Hex = None

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

		# (unit, weight)
		self.units = []

		## Add this unit to preUnit.units
		if pre != None:
			pre[0].units.append((self, pre[1]))

		self.input = 0.0
		self.output = 0.0

	def InitializeHex(self, hex:Hex):
		self.hex = hex

	def Response(self):
		res = 0.0
		# Calculate output
		if self.excitations.pop(0):
			res = self.weight
		else:
			res = self.output * (1 - Config.INTERVAL / self.tau)
		return res

	def Update(self):
		# Update excitation list
		if self.input > self.threshold:
			# Refractory time logic
			if self.delay != 0 and reduce(lambda pre, nxt: pre | nxt, self.excitations[-self.refractory:]):
				self.excitations.append(False)
			else:
				self.excitations.append(True)
		else:
			self.excitations.append(False)
		self.output = self.Response()
		self.input = 0.0
		return self.output

	def Forward(self):
		u: Unit
		for u in self.units:
			u[0].input += self.output * u[1]
		return self.output

class PUnit(Unit):
	def __init__(self, dist, scr:Screen, hex:Hex):
		Unit.__init__(self, dist, None)
		self.scr = scr
		self.hex = hex
		# Previous Illumination Sum
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
