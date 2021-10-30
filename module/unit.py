from functools import reduce
from module.config import Config
from module.hex import HexCoord, Hex

class Unit:
	def __init__(self, dist, units):
		self.threshold = dist['threshold']
		self.delay = dist['delay']
		self.tau = dist['tau']
		self.refractory = dist['refractory']
		self.weight = dist['weight']
		self.isFinal = dist['isFinal']

		self.coord = HexCoord(dist['a'], dist['r'], dist['c'])

		# To simulate delay:
		# Maintain a list whose length = delay
		# e.g. delay = 2ms, interval = 1ms
		# Init: [F1 F2]
		# 1ms rest -> [F1 F2 F3] -> pop F1 -> [F2 F3] ->
		# 2ms excited -> [F2 F3 T4] -> pop F2 -> [F3 T4] ->
		# 3ms rest -> [F3 T4 F5] -> pop F3 -> [T4 F5] ->
		# 4ms rest -> [T4 F5 F6] -> pop T4 (output excitation) -> [F5 F6]
		# Input is at 2ms and output is at 4ms (2ms delay)
		self.excitations = [False for i in int(range(self.delay)/Config.INTERVAL)]

		self.units = units

		self.input = 0.0
		self.output = 0.0

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
		if self.input >= self.threshold:
			# Refractory time logic
			if self.delay != 0 and reduce(lambda pre, nxt: pre | nxt, self.excitations[-self.refractory:]):
				self.excitations.append(False)
			else:
				self.excitations.append(True)
		self.output = self.Response()

	def Forward(self):
		if not self.isFinal:
			for u in self.units:
				u.input += self.output
			return 0.0
		else:
			return self.output

class PUnit(Unit):
	def __init__(self, dist, units, hex:Hex):
		Unit.__init__(self, dist, units)
		self.hex = hex

	def Response(self):
		#return super().Response()
		res = 0.0
		self.duration = 0.0
		if self.excitations.pop(0):
			res = self.weight
			self.duration = 0.0
		else:
			if self.duration >= 1:
				res = 0.0
				self.duration = 0.0
			else:
				res = self.weight
				self.duration += Config.INTERVAL
		return res

	def GetIllumination():
		return 0
