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
    __alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ']
    __space=26
    __tableSize=len(__alphabet)
    
    def __normalizeTables (self):
        for i in range (WordGenerator.__tableSize):
            s=0
            for j in range (WordGenerator.__tableSize):
                s+=self.__followingLetterProba[i][j]
            for j in range (WordGenerator.__tableSize):
                self.__followingLetterProba[i][j]/=s
    
    def saveTables (self):
        f = open(os.path.join(self.__workingDirectory,"LetterProbability.csv"),"w")
        for a in range (WordGenerator.__tableSize):
            for b in range (WordGenerator.__tableSize):
                f.write (str(self.__followingLetterProba[a][b]))
                if (b!=WordGenerator.__space):
                    f.write (";")
                else:
                    f.write ("\n")
        f.close()
        print ("Results stored in:", os.path.join(self.__workingDirectory,"LetterProbability.csv"))
    
    def printTables (self):
        for a in range (WordGenerator.__tableSize):
            print ("\nFrom", WordGenerator.__alphabet[a],"to:")
            for b in range (WordGenerator.__tableSize):
                print (WordGenerator.__alphabet[b],end=" ")
                print (str(self.__followingLetterProba[a][b]),end=" ")
    
    def __init__(self,directory):
        self.__followingLetterProba=[ [ 0 for i in range(WordGenerator.__tableSize) ] for j in range(WordGenerator.__tableSize) ]
        self.__workingDirectory=directory
        
        random.seed()
        for filename in os.listdir(self.__workingDirectory):
            print (os.path.join(self.__workingDirectory,filename),"...", end=" ")
            i=0
            e=0
            for line in open(os.path.join(self.__workingDirectory,filename)):
                i+=1
                try:
                    self.__followingLetterProba[WordGenerator.__space][string.ascii_lowercase.index(line[0])] +=1
                    for j in range (len(line)-1):
                        if (line[j+1]!="\r" and line[j+1]!="\n"):
                            self.__followingLetterProba[string.ascii_lowercase.index(line[j])][string.ascii_lowercase.index(line[j+1])] +=1
                        else:
                            self.__followingLetterProba[string.ascii_lowercase.index(line[j])][WordGenerator.__space] +=1
                except ValueError:
                    e+=1       
            print (i,"words parsed,",e,"errors")        
        self.__normalizeTables()           
        
    def createRandomWord(self):
        word=""
        newLetter=choice(WordGenerator.__alphabet, p=self.__followingLetterProba[WordGenerator.__space])
        while (newLetter!=" "):
            word+=newLetter
            newLetter=choice(WordGenerator.__alphabet, p=self.__followingLetterProba[string.ascii_lowercase.index(newLetter)])
        return word
            
    
# main           
frenchGenerator=WordGenerator("francais")
frenchGenerator.printTables()
englishGenerator=WordGenerator("English Open Word List (EOWL)")
englishGenerator.printTables()
for i in range (50):
    print (frenchGenerator.createRandomWord())
for i in range (50):
    print (englishGenerator.createRandomWord())

