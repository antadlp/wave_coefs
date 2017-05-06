import re
import sys

#The purpose of this script is to get the potential energy on every step of
#the the molecular dynamic generated by deMon2k
#http://www.demon-software.com/public_html/program.html 

def searchAndPrintOut(inputFile, outputFile):

    F = open(inputFile,'r')
    #The input file is the general output of the software package deMon2k
    #http://www.demon-software.com/public_html/program.html 

    fileOut = open(outputFile, "w")
    #The ouput file will be two arrays {step number, energy of the frame}

    step = 1 #Equivalent to the first step on the water dynamic
    for line in F:
        print(step)
        if "POTENTIAL ENERGY" in line:
            fileOut.write('{}'.format(step))
            fileOut.write('    ')

            for k in range(30): 
                fileOut.write(line.split()[1]) #get the atom index, i.e: H or O
                fileOut.write('     ')
                fileOut.write(line.split()[2]) #get x coordinate
                fileOut.write('   ')
                fileOut.write(line.split()[3]) #get y coordinate
                fileOut.write('   ')
                fileOut.write(line.split()[4]) #get z coordinate
                fileOut.write('\n')
                line=next(F)                   #jump to next atom

            step += 1 #when this loops ends, the outside loop search for the
                      #next step on the dynamic that's why step+=1


    fileOut.close()
    F.close()
    
    return;


searchAndPrintOut('../../data/deMon.out', 'geometries.xyz')



