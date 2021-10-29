from functools import reduce

class Unit:
	def __init__(self, dist, units):
		self.threshold = dist['threshold']
		self.delay = dist['delay']
		self.tau = dist['tau']
		self.refractory = dist['refractory']
		self.weight = dist['weight']
		self.isFinal = dist['isFinal']

		# To simulate delay:
		# Maintain a list whose length = delay
		# e.g. delay = 2ms
		# Init: [F1 F2]
		# 1ms rest -> [F1 F2 F3] -> pop F1 -> [F2 F3] ->
		# 2ms excited -> [F2 F3 T4] -> pop F2 -> [F3 T4] ->
		# 3ms rest -> [F3 T4 F5] -> pop F3 -> [T4 F5] ->
		# 4ms rest -> [T4 F5 F6] -> pop T4 (output excitation) -> [F5 F6]
		# Input is at 2ms and output is at 4ms (2ms delay)
		self.excitations = [False for i in range(self.delay)]

		self.units = units

		self.input = 0
		self.output = 0

	def Update(self):
		# Update excitation list
		if self.input >= self.threshold:
			# Refractory time logic
			if self.delay != 0 and reduce(lambda pre, nxt: pre | nxt, self.excitations[-self.refractory:]):
				self.excitations.append(False)
			else:
				self.excitations.append(True)
		# Calculate output
		if self.excitations.pop(0):
			self.output = self.weight
		else:
			# For P-unit, tau = 1 can be used when time interval is 1ms
			self.output = self.output * (1 - 1 / self.tau)

	def Forward(self):
		if not self.isFinal:
			for u in self.units:
				u.input += self.output
			return 0
		else:
			return self.output

class PUnit(Unit):
	def __init__(self, dist, downstreamUnits):
		Unit.__init__(self, dist, downstreamUnits)

	def GetIllumination():
		return 0
