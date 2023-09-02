__version__ = "$Revision: #3 $"
from cni.dlo import *

class MyTransistor(DloGen):

    @classmethod
    def defineParamSpecs(cls, specs):
        # define parameters and default values
        specs('width', 1.0)
        specs('height', 2.0)
        specs('layer', Layer('metal1'))

    def setupParams(self, params):
        # process parameter values entered by user
        self.width = params['width']
        self.height = params['height']
        self.layer = params['layer']
    
    def genLayout(self):
        # generate rectangle layout
        x = self.width
        y = self.height
        Rect(Layer('nwell'), Box(-x, 0, x, y))
        Rect(Layer('nimp'), Box(-x, -y, x, 0))
        Rect(Layer('pimp'), Box(-x, -y, x, -y-y/4))