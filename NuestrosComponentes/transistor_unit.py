__version__ = "$Revision: #3 $"
from cni.dlo import *
from cni.geo import *
from cni.constants import *

class MyTransistorUnit(DloGen):

    @classmethod
    def defineParamSpecs(cls, specs):
        # first use variables to set default values for all parameters
        tranType = 'pmos'
        oxide = 'thin'
        width = specs.tech.getMosfetParams(tranType, oxide, 'minWidth')
        length = specs.tech.getMosfetParams(tranType,oxide,'minLength')
        # now use these default values in the parameter definitions
        specs('tranType', tranType, 'MOSFET type (pmos or nmos)', ChoiceConstraint(['pmos', 'nmos']))
        specs('oxide', oxide, 'Oxide type (thin or thick)', ChoiceConstraint(['thin', 'thick']))
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
        # readjust width and length, as minimum values may be different
        self.width = max(self.width,
        self.tech.getMosfetParams(self.tranType, self.oxide, 'minWidth'))
        self.length = max(self.length, self.tech.getMosfetParams(self.tranType, self.oxide, 'minLength'))
        # also snap width and length values to nearest grid points
        grid = Grid(self.tech.getGridResolution())
        self.width = grid.snap(self.width, SnapType.ROUND)
        self.length = grid.snap(self.length, SnapType.ROUND)
        # save layer values using class variables
        self.gateLayer = Layer('PO')
        self.diffLayer = Layer('DIFF')
        self.metalLayer = Layer('M1')
        # define layers which should be used for enclosure rectangles
        if self.tranType == 'nmos':
            self.encLayers = [Layer('NIMP')]
        else:
            self.encLayers = [Layer('PIMP'), Layer('NWELL')]
        if self.oxide == 'thick':
            self.encLayers.append(Layer('OD2'))
        # determine minimum extension for gate poly layer
        self.endcap = self.tech.getPhysicalRule('minClearance', self.gateLayer, self.diffLayer)
    
    def genLayout(self):
        # first create the rectangle for the gate
        gateBox = Box(-self.endcap, 0, (self.width + self.endcap), self.length)
        gateRect = Rect(self.gateLayer, gateBox)
        # now create contacts for the source and drain
        self.sourceContact = DeviceContact(self.diffLayer, self.metalLayer, gateBox, name = 'S')
        self.drainContact = DeviceContact(self.diffLayer, self.metalLayer, gateBox, name = 'D')
        # stretch source and drain contacts to full transistor extent
        sourceBox = self.sourceContact.getRect1().getBBox()
        self.sourceContact.stretch(self.metalLayer, sourceBox)
        drainBox = self.drainContact.getRect1().getBBox()
        self.drainContact.stretch(self.metalLayer, drainBox)
        # use smart place to place gate between source and drain
        fgPlace(self.sourceContact, SOUTH, gateRect)
        fgPlace(self.drainContact, NORTH, gateRect)
        # create the gate diffusion rectangle,
        # from top of source to bottom of drain
        bottom = self.sourceContact.getBBox().top
        top = self.drainContact.getBBox().bottom
        diffBox = Box(gateBox.left, top, gateBox.right, bottom)
        diffRect = Rect(self.diffLayer, diffBox)
        # add any extra diffusion outside source and drain contacts
        if self.sourceDiffOverlap > 0:
            sBox = self.sourceContact.getBBox(self.diffLayer)
            sBox.setBottom(sBox.bottom - self.sourceDiffOverlap)
            Rect(self.diffLayer, sBox)
        if self.drainDiffOverlap > 0:
            dBox = self.drainContact.getBBox(self.diffLayer)
            dBox.setTop(dBox.top + self.drainDiffOverlap)
            Rect(self.diffLayer, dBox)
        # define transistor enclosure rectangles on enclosure layers
        fgEnclose(self.makeGrouping(), self.encLayers)
        # add terminals for this transistor unit
        self.addTerm('S', TermType.INPUT_OUTPUT)
        self.addTerm('D', TermType.INPUT_OUTPUT) # drain terminal
        self.addTerm('G', TermType.INPUT) # gate terminal
        self.addTerm('B', TermType.INPUT_OUTPUT) # bulk terminal
        self.setTermOrder(['D','G','S','B'])
        # also define pins for this transistor unit
        self.addPin('G', 'G', gateBox, self.gateLayer)
        self.addPin('S', 'S',
        self.sourceContact.getBBox(self.metalLayer), self.metalLayer)
        self.addPin('D', 'D',
        self.drainContact.getBBox(self.metalLayer), self.metalLayer)