from basicos import *
from transistor import *
from transistor_unit import *

def definePcells(lib):
    lib.definePcell(MyNotGate, "MyNotGate")
    lib.definePcell(MyTransistorUnit, "MyTransistorUnit")
    # lib.definePcell(MyTransistor, "MyTransistor")
