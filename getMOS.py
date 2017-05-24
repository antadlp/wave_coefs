import re
import sys
from pyparsing import *

def searchAndPrintOut(inputFile, outputFile):




    #     1    1   H    1s        0.0000     0.0000     0.0000    -0.0003     0.0000

    num Word(nums).
    atomInInput= Word(nums)
    atomicNumber = 
    F = open(inputFile,'r')
    fileOut = open(outputFile, "w")

    lineNumber = 1 
    for line in F:
        lineNumber+= 1
        if lineNumber >= 2: #stay :w
            break

    for line in F:
        print(line)
        lineNumber+= 1
        if lineNumber >= 7: #ya no imprime 7, me quedo alli
            break


    print("sali header bloque 1")

    
    bloque = 1 #1, 2, 3, 4, 5
    while True:
        atomo = 1

        #verify wich atom for loop on orbitals
        Z = line.split().[2]
        Z = int(Z)

        for i in range(Z):
           info 

        
        
        
        
        lineNumber+= 1
        if lineNumber >=9:
            break



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




