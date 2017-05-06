import re
import sys


def searchAndPrintOut(inputFile, outputFile):

    F = open(inputFile,'r')
    fileOut = open(outputFile, "w")

    step = 1
    for line in F:
        print(step)
        if "COORDINATES OF TIME STEP" in line:
            fileOut.write('    30') 
            fileOut.write('\n')
            # 30 is the total number of atmos, as we are training/testing with 10
            # waters molecules they are 30 atoms.
            k=1
            j=1
            fileOut.write('molec    step    ')
            fileOut.write('{}'.format(step))
            fileOut.write('\n')
            for j in range(4):
                line = next(F)
            
            #positioned on line for atom 1. Example for step 1:
            # 1  H        3.137918      0.417859     -0.908692       1     1.008

            for k in range(30):
                fileOut.write(line.split()[1])
                fileOut.write('     ')
                fileOut.write(line.split()[2])
                fileOut.write('   ')
                fileOut.write(line.split()[3])
                fileOut.write('   ')
                fileOut.write(line.split()[4])
                fileOut.write('\n')
                line=next(F)

            step += 1


    fileOut.close()
    F.close()
    
    return;


searchAndPrintOut('../../data/deMon.out', 'geometries.xyz')




