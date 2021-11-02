import numpy as np

from module.screen import Screen
from module.unit import Unit, PUnit
from module.config import Config

class Network:
	def __init__(self, scr:Screen):
		# Get Screen
		self.scr = scr

		# Generate Punit
		self.punit = list(map(lambda h: PUnit({
			'threshold': Config.P_THRESHOLD,
			'delay': Config.P_DELAY,
			'tau': Config.P_TAU,
			'refractory': Config.P_REFRACTORY,
			'weight': Config.P_WEIGHT
			}, scr, h), scr.hexList))

		# Generate Eunit
		self.eunit = list(map(lambda p: Unit({
			'threshold': Config.E_THRESHOLD,
			'delay': Config.E_DELAY,
			'tau': Config.E_TAU,
			'refractory': Config.E_REFRACTORY,
			'weight': Config.E_WEIGHT
			}, pre=(p, 1.0)), self.punit))

		# Generate I1unit
		self.i1unit = list(map(lambda p: Unit({
			'threshold': Config.I_THRESHOLD,
			'delay': Config.I1_DELAY,
			'tau': Config.I_TAU,
			'refractory': Config.I_REFRACTORY,
			'weight': Config.I1_WEIGHT
			}, pre=(p, 1.0)), self.punit))

		# Generate I1unit
		self.i2unit = list(map(lambda p: Unit({
			'threshold': Config.I_THRESHOLD,
			'delay': Config.I2_DELAY,
			'tau': Config.I_TAU,
			'refractory': Config.I_REFRACTORY,
			'weight': Config.I2_WEIGHT
			}, pre=(p, 1.0)), self.punit))

		# Generate Sunit
		# Todo

	def update(self, objList):
		self.scr.render(objList)
		rst = list(map(lambda p: p.Update(), self.punit))
		rst = list(map(lambda p: p.Forward(), self.punit))
		rst = list(map(lambda e: e.Update(), self.eunit))
		rst = list(map(lambda i1: i1.Update(), self.i1unit))
		rst = list(map(lambda i2: i2.Update(), self.i2unit))
		return rst