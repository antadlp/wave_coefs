import os
import shelve
import sys
import config

import numpy as np
from pyparsing import *

DATASET = shelve.open('DB.shlv')
DATASETCFG = config.datasets['B']

class parseGeometry(object):
    def __init__(self):
        #Parser objetcts for geometry coordinates
        self.atomNumLine = Word(nums) + stringEnd
        self.atomNumLine.setParseAction(lambda tkn: int(tkn[0]))

        self.frameNumber = Literal("molec").suppress() + Word(nums)(
            "frameNumber") + stringEnd

        floatnum = Combine(Optional("-") + Word(nums) + Literal(".") + Word(
            nums))
        self.coords = Word(alphas).suppress() + floatnum("x") + floatnum(
            "y") + floatnum("z") + stringEnd
        #self.coords.setParseAction( lambda tkn: map(float, tkn ) )

        #Parser objects for Mulliken charges
        self.mullikenLine = Literal("mulliken charges").suppress() + floatnum(
            "mullikenCharges") + stringEnd

        self.chargeLine = Word(nums).suppress() + floatnum(
            "charge") + stringEnd

        #Parser objects for wave eq coefs
        #								1		  2		  3		  4		  5
        self.coefsNumsLine = Word(nums) + Word(nums) + Word(nums) + Word(
            nums) + Word(nums)
        #							 2.0000	 2.0000	 2.0000	 2.0000	 2.0000
        self.coefsNumsLine_2 = floatnum + floatnum + floatnum + floatnum + floatnum + stringEnd

        #	 1	1   H	1s		0.0000	-0.0000	-0.0000	-0.0000	 0.0000
        self.coefsAtomsLine = Word(nums)("orbitalNum") + Word(nums)(
            "atomNum") + Word(alphas)("atom") + Word(alphanums)(
                "orbitalName") + self.coefsNumsLine_2("coefs") + stringEnd

    def matrixFromGeometryFrames(self, geometriesFile):
        fin = open(geometriesFile, 'r')
        #newframe = True
        firstframe = True
        frameattributes = []
        framesList = []
        for l in fin:
            l = l.strip()

            try:
                self.atomNumLine.parseString(l)
                continue
            except:
                pass

            try:
                self.frameNumber.parseString(l)
                #newframe = True
                if not firstframe:
                    framesList.append(np.asarray(frameattributes))
                frameattributes = []
                firstframe = False
                continue
            except:
                pass

            try:
                coords = self.coords.parseString(l)
                frameattributes.append(float(coords.x))
                frameattributes.append(float(coords.y))
                frameattributes.append(float(coords.z))
            except:
                pass

        framesList.append(np.asarray(frameattributes))

        framesMatrix = np.array(framesList)
        print(framesMatrix)
        print('\n*** Shape of created dataset:',\
              framesMatrix.shape)
        return framesMatrix

    def matrixFromChargeFrames(self, mullikenFile):
        fin = open(mullikenFile, 'r')
        #newframe = True
        firstframe = True
        framecharges = []
        framesChargesList = []
        for l in fin:
            l = l.strip()

            try:
                self.mullikenLine.parseString(l)
                if not firstframe:
                    framesChargesList.append(np.asarray(framecharges))
                framecharges = []
                firstframe = False
                continue
            except:
                pass

            try:
                chargel = self.chargeLine.parseString(l)
                framecharges.append(float(chargel.charge))
            except:
                pass

        framesChargesList.append(np.asarray(framecharges))

        framesChargesList = np.array(framesChargesList)
        print(framesChargesList)
        print(framesChargesList.shape)
        return framesChargesList

    def energies(self,energiesFile):
        fin = open(energiesFile, 'r')
        _energies = [float(_.strip().split()[1]) for _ in fin]
        return np.asarray(_energies)

    def targetWaveEqCoeficientsFrame(self,
                                     outfilename='sMOsFrame1234_SCF8.out',
                                     depth=2,
                                     allowed_orbitals=['1s','2s','2py','2px','2pz']):
        targets = []
        _depth = 0
        change_block = True
        fin = open(outfilename, 'r')
        while _depth <= depth:
            l = fin.readline().strip()
            try:
                allowed_orbitals
                _parsedCoefs = self.coefsAtomsLine.parseString(l)
                if not _parsedCoefs.orbitalName in allowed_orbitals:
                    continue
                coefs = map(float, _parsedCoefs.coefs)
                print('\n', coefs)
                targets = targets + coefs
                change_block = False
            except:
                if not change_block:
                    _depth += 1
                    change_block = True

        return targets


def targetCoefsMatrix(outs_dir='./MosDemonAgua'):
    pG = parseGeometry()
    outsfilenames = os.listdir(outs_dir)
    orderedouts = [''] * len(outsfilenames)
    coefslistlist = [[]] * len(outsfilenames)

    for outfn in outsfilenames:
        _i = outfn.index('_')
        __i = outfn.index('rame') + len('rame')
        num = int(outfn[__i:_i]) - 1
        orderedouts[num] = outfn

    for i in xrange(len(orderedouts)):
        _coefs = pG.targetWaveEqCoeficientsFrame(os.path.join(outs_dir,
                                                              orderedouts[i]))
        coefslistlist[i] = _coefs

    return np.matrix(coefslistlist)


def createEntireDataset(geometriesfn=DATASETCFG['geometriesfn'],
                        outsdirfn=DATASETCFG['outsdirfn'],
                        energiesfn=DATASETCFG['energiesfn']):
    pG = parseGeometry()

    if 'geometries' not in DATASET:
        _geometries = pG.matrixFromGeometryFrames(geometriesfn)
        print('_geometries', _geometries.shape)
        DATASET['geometries'] = _geometries

    if 'coeficients' not in DATASET:
        _waveqcoefs = targetCoefsMatrix(outs_dir=outsdirfn)
        print('_waveqcoefs', _waveqcoefs.shape)
        DATASET['coeficients'] = _waveqcoefs

    if 'energies' not in DATASET:
        _energies = pG.energies(energiesfn)
        print('_energies', _energies.shape)
        DATASET['energies'] = _energies

    DATASET.close()

def testDataset():
    #print 'keys:', DATASET.keys()
    print('shape geometries', DATASET['geometries'].shape)
    print('shape coeficients', DATASET['coeficients'].shape)


def parsingTests():
    pG = parseGeometry()

    print('\n** Test atomline')
    atomline = pG.atomNumLine.parseString("   27")
    print(atomline)

    print('\n** Test frame number')
    framenum = pG.frameNumber.parseString(" molec	  1")
    print(framenum)
    print(framenum.frameNumber)

    print('\n** Test coordinates')
    coords = pG.coords.parseString("O		 -3.1351	  0.3995	 -2.4964")
    print(coords)
    print(float(coords.x), float(coords.y), float(coords.z))

    print('\n** Test mulliken line')
    mullikenl = pG.mullikenLine.parseString("mulliken charges   10.000")
    print(mullikenl)
    print(mullikenl.mullikenCharges)

    print('\n** Test charge line')
    chargel = pG.chargeLine.parseString("  15   -0.654")
    print(chargel)
    print(float(chargel.charge))

    print('\n** Wave coeficients line')
    coefsline = pG.coefsNumsLine.parseString("								1		  2		  3		  4		  5")
    print(coefsline)

    print('\n** Wave coeficients line 2')
    coefsline2 = pG.coefsNumsLine_2.parseString(
        "							 2.0000	 2.0000	 2.0000	 2.0000	 2.0000")
    print(coefsline2)

    print('\n** Coeficients atom line')
    coefsAtomsLine = pG.coefsAtomsLine.parseString(\
        "	 2	1   H	2s	   -0.0004	-0.0000	 0.0000	 0.0002	-0.0003")
    print(coefsAtomsLine)
    print("orbitalName:", coefsAtomsLine.orbitalName)
    print("coefs:", coefsAtomsLine.coefs)


def main():
    #createEntireDataset()
    #testDataset()
    #print targetCoefsMatrix().shape
    #print pG.targetWaveEqCoeficientsFrame()
    #pG.matrixFromGeometryFrames(sys.argv[1]) #geometries
    #pG.matrixFromChargeFrames(sys.argv[2]) #mulliken
    parsingTests()

if __name__ == '__main__':
    main()
