import re
import sys
from pyparsing import *

def searchAndPrintOut(inputFile, outputFile):



    AllOrbitalInfo = []
    #pyparsing construction for parsing a line of the
    #'sMOsT350Frame1110_SCF5.out file', the objective is to have
    #a matrix of all the ordered info, so it will be easy for
    #access

#     1    1   H    1s        0.0000     0.0000     0.0000    -0.0003     0.0000
    num = Word(nums).suppress()
    atomInInput = Word(nums)
    atomicSymbol = Word(alphas)
    orbitalSymbol = Word(alphanums)
    orbitalValues = OneOrMore( Combine(Optional("-") + \
        OneOrMore( Word( nums + "." + nums )) ))
    lineOrbitalOrder = num + atomInInput + atomicSymbol + \
            orbitalSymbol + orbitalValues


    F = open(inputFile,'r')
    fileOut = open(outputFile, "w")
    lineNumber = 1 
    for line in F:
        lineNumber+= 1
        if lineNumber >= 2: #stay :w
            break

    print('linea {0:0d}'.format(lineNumber))
    print(line)
    for line in F:
        print(line)
        lineNumber+= 1
        if lineNumber >= 7: #ya no imprime 7, me quedo alli
            break

    print("sali header bloque 1")
    print(lineNumber)
#    print(line + "LL")

    line = next(F)
    print(line + "LL2")

    
    bloque = 1 #1, 2, 3, 4, 5
    while True:
        atomo = 1

        #verify wich atom for loop on orbitals
        Z = line.split()[2]
        if Z == 'H':
            orbitales = 5

        for i in range(orbitales):
            AllOrbitalInfo.append(\
                    lineOrbitalOrder.parseString(line).asList())
            line = next(F)
            lineNumber+=1
            
            if lineNumber >= 12: #ya no imprime 12, me quedo alli
                break
        
        
        
        if lineNumber >=11:
            break

    numListas = sum(1 for x in AllOrbitalInfo if \
            isinstance(x, list))

    for j in range(numListas):
        print(AllOrbitalInfo[j])

    return;






#    for line in F:
#        print(step)
#        if "COORDINATES OF TIME STEP" in line:
#            fileOut.write('    30') 
#            fileOut.write('\n')
#            k=1 
#            j=1 
#            fileOut.write('molec    step    ')
#            fileOut.write('{}'.format(step))
#            fileOut.write('\n')
#            for j in range(4):
#                line = next(F)
#            
#
#            for k in range(30): 
#                fileOut.write(line.split()[1]) 
#                fileOut.write('     ')
#                fileOut.write(line.split()[2]) 
#                fileOut.write('   ')
#                fileOut.write(line.split()[3]) 
#                fileOut.write('   ')
#                fileOut.write(line.split()[4]) 
#                fileOut.write('\n')
#                line=next(F)                   
#
#            step += 1 
#                      
#
#
#    fileOut.close()
#    F.close()
    
    return;


searchAndPrintOut('sMOsT350Frame1110_SCF5.out', 'coeficientes')




