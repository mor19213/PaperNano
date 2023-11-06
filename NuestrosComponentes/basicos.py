__version__ = "$Revision: #3 $"
from cni.dlo import *
from cni.geo import *
from cni.constants import *

class MyNotGate(DloGen):

    @classmethod
    def defineParamSpecs(cls, specs):
        # define parameters and default values
        # first use variables to set default values for all parameters
        tranType = 'nmos'
        oxide = 'thin'
        width = specs.tech.getMosfetParams(tranType, oxide, 'minWidth')
        length = specs.tech.getMosfetParams(tranType, oxide, 'minLength')
    
        # now use these default parameter values in the parameter definitions
        specs('tranType', tranType, 'MOSFET type (pmos or nmos)', ChoiceConstraint(['pmos', 'nmos']))
        specs('oxide', oxide, 'Oxide (thin or thick)', ChoiceConstraint(['thin', 'thick']))
        specs('width', width, 'device width', RangeConstraint(width, 10*width, USE_DEFAULT))
        specs('length', length, 'device length', RangeConstraint(length, 10*length, USE_DEFAULT))

        specs('sourceDiffOverlap', 0.0)
        specs('drainDiffOverlap', 0.0)
        specs('xtorFillLayer', Layer('M1'))

    def setupParams(self, params):
        # save parameter values using class variables
        self.width = params['width']
        self.length = params['length']
        self.oxide = params['oxide']
        self.tranType = params['tranType']
        self.sourceDiffOverlap = params['sourceDiffOverlap']
        self.drainDiffOverlap = params['drainDiffOverlap']
        self.xtorFillLayer = params['xtorFillLayer']

        # readjust width and length parameter values, since minimum values may be different
        self.width = max(self.width, self.tech.getMosfetParams(self.tranType, self.oxide, 'minWidth'))
        self.length = max(self.length, self.tech.getMosfetParams(self.tranType, self.oxide, 'minLength'))

        # also snap width and length values to nearest grid points
        grid = Grid(self.tech.getGridResolution())
        self.width = grid.snap(self.width, SnapType.ROUND)
        self.length = grid.snap(self.length, SnapType.ROUND)

        # save layer values using class variables
        self.diffLayer = Layer('DIFF')
        self.gateLayer = Layer('PO')
        self.metalLayer = Layer('M1')

        # define the layers which should be used for enclosure rectangles
        if self.tranType == 'nmos':
            self.encLayers = [Layer('NIMP')]
        else:
            self.encLayers = [Layer('PIMP'), Layer('NWELL')]

        # determine minimum extension for gate poly layer
        self.endcap = self.tech.getPhysicalRule('minClearance', self.gateLayer, self.diffLayer)
    
    def genLayout(self):
        gateBox = Box(-self.endcap, 0, (self.width + self.endcap), self.length)
        grid = Grid(self.tech.getGridResolution())
        if self.tech.physicalRuleExists('minWidth', self.metalLayer):
            minWidth = self.tech.getPhysicalRule('minWidth', self.metalLayer)
            gateBox.expandForMinWidth(EAST, minWidth, grid)
        if self.tech.physicalRuleExists('minArea', self.metalLayer):
            minArea = self.tech.getPhysicalRule('minArea', self.metalLayer)
            gateBox.expandForMinArea(NORTH, minArea, grid)
        gateRect = Rect(self.metalLayer, gateBox)
        gateRect.fgAddEnclosingPolygon(Layer('NIMP'), filter=ShapeFilter(self.metalLayer))


        # # first construct the rectangle for the gate
        # gateBox = Box(-self.endcap, 0, (self.width + self.endcap), self.length)
        # #### UNCOMMENT FOLLOWING FOUR LINES TO REMOVE MINIMUM AREA DRC ERROR
        # if self.tech.physicalRuleExists('minArea', self.gateLayer):
        #     minArea = self.tech.getPhysicalRule('minArea', self.gateLayer)
        #     grid = Grid(self.tech.getGridResolution())
        #     gateBox.expandForMinArea(EAST, minArea, grid)
        # gateRect = Rect(self.gateLayer, gateBox)

        # # first construct the rectangle for the gate
        # gateBox1 = Box(-self.endcap, 0, (self.width + self.endcap), self.length)
        # #### UNCOMMENT FOLLOWING FOUR LINES TO REMOVE MINIMUM AREA DRC ERROR
        # if self.tech.physicalRuleExists('minArea', self.diffLayer):
        #     minArea1 = self.tech.getPhysicalRule('minArea', self.diffLayer)
        #     grid1 = Grid(self.tech.getGridResolution())
        #     gateBox1.expandForMinArea(NORTH, minArea1, grid1)
        # gateRect1 = Rect(self.diffLayer, gateBox1)