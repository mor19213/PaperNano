__version__ = "$Revision: #3 $"
from cni.dlo import *

class MyNotGate(DloGen):

    @classmethod
    def defineParamSpecs(cls, specs):
        # define parameters and default values
        specs('width', 1.0)
        specs('height', 2.0)
        specs('layer', Layer('M1'))

    def setupParams(self, params):
        # process parameter values entered by user
        self.width = params['width']
        self.height = params['height']
        self.layer = params['layer']
    
    def genLayout(self):
        Rect(Layer('NWELL'), Box(-0.064, 0, 0.926, 1.094))

        Rect(Layer('NIMP'), Box(0, 0.628, 0.862, 0.728))
        Rect(Layer('PIMP'), Box(0, 0, 0.862, 0.942))

        Rect(Layer('NIMP'), Box(0, -0.628, 0.862, 0))

        Rect(Layer('M1'), Box(0, -0.648, 0.862, -0.709))
        Rect(Layer('DIFF'), Box(0, -0.648, 0.862, -0.71))
        Rect(Layer('PIMP'), Box(0, -0.628, 0.862, -0.728))
