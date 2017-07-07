'''
Created on 6 juil. 2017

@author: irac1
'''
import os
import string
import random
from numpy.random import choice

def normalize (probaTable):
    for i in range (27):
        s=0
        for j in range (27):
            s+=probaTable[i][j]
        for j in range (27):
            probaTable[i][j]/=s
    return probaTable

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
        
    letterProbability=normalize(letterProbability)
        
    f = open(os.path.join(directory,"LetterProbability.csv"),"w")
    for a in range (0,27):
        for b in range (0,26):
            f.write (str(letterProbability[a][b]))
            f.write (";")
        f.write (str(letterProbability[a][26]))
        f.write ("\n")
    f.close()
    print ("Results stored in:", os.path.join(directory,"LetterProbability.csv"))
    
    return letterProbability


    
def createRandomWord(probaLetters):
    alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ']
    word=""
    newLetter=choice(alphabet, p=probaLetters[26])
    while (newLetter!=" "):
        word+=newLetter
        index=string.ascii_lowercase.index(newLetter)
        newLetter=choice(alphabet, p=probaLetters[index])
    return word
        
    
# main           
#probaLetters=buildLetterProbability("English Open Word List (EOWL)")
probaLetters=buildLetterProbability("francais")
random.seed()
for i in range (100):
    print (createRandomWord(probaLetters))
