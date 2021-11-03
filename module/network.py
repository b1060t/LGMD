from functools import reduce
import numpy as np

from module.screen import Screen
from module.unit import Funit, Unit, PUnit, SUnit
from module.config import Config

class Network:
	def __init__(self, scr:Screen, closeF=False):
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
			}, pre=[(p, 1.0)]), self.punit))

		# Generate I1unit
		self.i1unit = list(map(lambda p: Unit({
			'threshold': Config.I_THRESHOLD,
			'delay': Config.I1_DELAY,
			'tau': Config.I_TAU,
			'refractory': Config.I_REFRACTORY,
			'weight': Config.I1_WEIGHT
			}, pre=[(p, 1.0)]), self.punit))

		# Generate I1unit
		self.i2unit = list(map(lambda p: Unit({
			'threshold': Config.I_THRESHOLD,
			'delay': Config.I2_DELAY,
			'tau': Config.I_TAU,
			'refractory': Config.I_REFRACTORY,
			'weight': Config.I2_WEIGHT
			}, pre=[(p, 1.0)]), self.punit))

		# Generate Sunit
		self.sunit = list(map(lambda p: SUnit({
			'threshold': Config.S_THRESHOLD,
			'delay': Config.S_DELAY,
			'tau': Config.S_TAU,
			'refractory': Config.S_REFRACTORY,
			'weight': Config.S_WEIGHT
			}, pre=[(p, 1.0)], i1units=self.i1unit, i2units=self.i2unit), self.eunit))

		# Generate Funit
		self.funit = [Funit({
			'threshold': Config.F_THRESHOLD,
			'delay': Config.F_DELAY,
			'tau': Config.F_TAU,
			'refractory': Config.F_REFRACTORY,
			'weight': Config.F_WEIGHT
		}, pre=[(p, 1.0) for p in self.punit])]

		self.closeF = closeF

	def reset(self, closeF=False):
		for u in self.punit:
			u.reset()
		for u in self.eunit:
			u.reset()
		for u in self.i1unit:
			u.reset()
		for u in self.i2unit:
			u.reset()
		for u in self.sunit:
			u.reset()
		for u in self.funit:
			u.reset()
		self.closeF = closeF

	def update(self, objList):
		self.scr.render(objList)
		rst = list(map(lambda p: p.Update(), self.punit))
		rst = list(map(lambda p: p.Forward(), self.punit))
		rst = list(map(lambda e: e.Update(), self.eunit))
		rst = list(map(lambda e: e.Forward(), self.eunit))
		rst = list(map(lambda i1: i1.Update(), self.i1unit))
		rst = list(map(lambda i1: i1.Forward(), self.i1unit))
		rst = list(map(lambda i2: i2.Update(), self.i2unit))
		rst = list(map(lambda i2: i2.Forward(), self.i2unit))
		rst = list(map(lambda s: s.Update(), self.sunit))
		rst = list(map(lambda f: f.Update(), self.funit))
		val = reduce(lambda pre, nxt: pre + nxt, list(map(lambda u: u.output, self.sunit)))
		if not self.closeF:
			val += reduce(lambda pre, nxt: pre + nxt, list(map(lambda f: f.output, self.funit)))
		return val