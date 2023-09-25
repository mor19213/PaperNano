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
        y = 0.628
        w = 0.862
        m1 = 0.1
        Rect(Layer('NWELL'), Box(-0.064, 0, w+0.064, 1.094))

        Rect(Layer('NIMP'), Box(0, y, w, y+m1))
        Rect(Layer('PIMP'), Box(0, 0, w, 0.942))

        Rect(Layer('NIMP'), Box(0, -y, w, 0))

        Rect(Layer('M1'), Box(0, -y-0.02, w, -y-0.081))
