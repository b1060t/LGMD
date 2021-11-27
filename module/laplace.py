from functools import reduce
import numpy as np
from module.hex import Hex

from module.screen import Screen
from module.unit import Funit, Unit, Punit, Sunit
from module.config import Config

class L1unit:
    def __init__(self, scr:Screen, hex:Hex):
        self.scr = scr
        self.hex = hex
        self.nxt = []
        self.preSum = 0
        self.output = 0
        
    def Update(self):
        sum = 0.0
        for p in self.hex.pixels:
            sum += self.scr.map[p[0], p[1]]
        self.output = sum
        
    def Forward(self):
        u:Unit
        for u in self.nxt:
            u[0].input = self.output * u[1]
        
class L2unit:
    def __init__(self, scr:Screen, pre:L1unit, iunits):
        self.scr = scr
        
        self.hex = pre.hex
        pre.nxt.append((self, -6))
        
        ilist = list(filter(lambda u: u.hex.isNear(self.hex.coord), iunits))
        for i in ilist:
            i.nxt.append((self, 1))
        
        self.output = 0
        self.input = 0
        
    def Update(self):
        self.output = self.input

class Laplace:
    def __init__(self, scr:Screen):
        self.scr = scr
        
        self.l1unit = list(map(lambda h: L1unit(scr, h), scr.hexList))
        self.l2unit = list(map(lambda l: L2unit(scr, l, self.l1unit), self.l1unit))
        
    def update(self, objList):
        self.scr.render(objList)
        rst = list(map(lambda u: u.Update(), self.l1unit))
        rst = list(map(lambda u: u.Forward(), self.l1unit))
        rst = list(map(lambda u: u.Update(), self.l2unit))
        val = reduce(lambda pre, nxt: pre + nxt, list(map(lambda u: u.output, self.l2unit)))
        return val