'''
Created on 6 juil. 2017

@author: irac1
'''
import os
import string
import random
from numpy.random import choice

class WordGenerator:
    # a=0, b=1, ..., z=25, space=26    
    def __normalizeTables (self):
        for i in range (27):
            s=0
            for j in range (27):
                s+=self.__twoLettersProba[i][j]
            for j in range (27):
                self.__twoLettersProba[i][j]/=s
    
    def saveTables (self):
        f = open(os.path.join(self.__workingDirectory,"LetterProbability.csv"),"w")
        for a in range (0,27):
            for b in range (0,26):
                f.write (str(self.__twoLettersProba[a][b]))
                f.write (";")
            f.write (str(self.__twoLettersProba[a][26]))
            f.write ("\n")
        f.close()
        print ("Results stored in:", os.path.join(self.__workingDirectory,"LetterProbability.csv"))
    
    
    def __init__(self,directory):
        self.__alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ']
        self.__twoLettersProba=[ [ 0 for i in range(27) ] for j in range(27) ]
        self.__workingDirectory=directory
        
        random.seed()
        for filename in os.listdir(self.__workingDirectory):
            print (os.path.join(self.__workingDirectory,filename),"...", end=" ")
            i=0
            e=0
            for line in open(os.path.join(self.__workingDirectory,filename)):
                i+=1
                try:
                    self.__twoLettersProba[26][string.ascii_lowercase.index(line[0])] +=1
                    for j in range (0,len(line)-1):
                        if (line[j+1]!="\r" and line[j+1]!="\n"):
                            self.__twoLettersProba[string.ascii_lowercase.index(line[j])][string.ascii_lowercase.index(line[j+1])] +=1
                        else:
                            self.__twoLettersProba[string.ascii_lowercase.index(line[j])][26] +=1
                except ValueError:
                    e+=1       
            print (i,"words parsed,",e,"errors")        
        self.__normalizeTables()           
        
    def createRandomWord(self):
        word=""
        newLetter=choice(self.__alphabet, p=self.__twoLettersProba[26])
        while (newLetter!=" "):
            word+=newLetter
            index=string.ascii_lowercase.index(newLetter)
            newLetter=choice(self.__alphabet, p=self.__twoLettersProba[index])
        return word
            
    
# main           
frenchGenerator=WordGenerator("francais")
englishGenerator=WordGenerator("English Open Word List (EOWL)")
for i in range (50):
    print (frenchGenerator.createRandomWord())
for i in range (50):
    print (englishGenerator.createRandomWord())

