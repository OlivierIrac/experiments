'''
Created on 6 juil. 2017

@author: irac1
'''
import os
import string
import matplotlib.pyplot as plt

def buildLetterProbability(directory):
    letterProbability= [ [ 0 for i in range(27) ] for j in range(27) ]
    for filename in os.listdir(directory):
        print (os.path.join(directory,filename),"...", end=" ")
        i=0
        e=0
        for line in open(os.path.join(directory,filename)):
            i+=1
            try:
                letterProbability[26][string.ascii_lowercase.index(line[0])] +=1
                for j in range (0,len(line)-1):
                    if (line[j+1]!="\r" and line[j+1]!="\n"):
                        letterProbability[string.ascii_lowercase.index(line[j])][string.ascii_lowercase.index(line[j+1])] +=1
                    else:
                        letterProbability[string.ascii_lowercase.index(line[j])][26] +=1
            except ValueError:
                e+=1       
        print (i,"words parsed,",e,"errors")
        
    f = open(os.path.join(directory,"LetterProbability.csv"),"w")
    for a in range (0,27):
        for b in range (0,26):
            f.write (str(letterProbability[a][b]))
            f.write (";")
        f.write (str(letterProbability[a][26]))
        f.write ("\n")
    f.close()
    print ("Results stored in:", os.path.join(directory,"LetterProbability.csv"))
#     for a in range (0,27):
#         print (chr(97+a), end=" ")
#         for b in range (0,27):
#             print (chr(97+b),letterProbability[a][b], end=" ")
#         print ("\n")
#         
#     plt.plot(letterProbability)
#     plt.show()
#             
buildLetterProbability("francais")
        
