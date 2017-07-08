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
    
    def __charToIndex(self,char):
        if (char==" "):
            return WordGenerator.__space
        else:
            return string.ascii_lowercase.index(char)
        
    def __normalizeDupletsProba (self):
        for i in range (WordGenerator.__tableSize):
            s=0
            for j in range (WordGenerator.__tableSize):
                s+=self.__dupletsProba[i][j]
            for j in range (WordGenerator.__tableSize):
                self.__dupletsProba[i][j]/=s
    
    def saveProbaTables (self):
        f = open(os.path.join(self.__workingDirectory,"LetterProbability.csv"),"w")
        for a in range (WordGenerator.__tableSize):
            for b in range (WordGenerator.__tableSize):
                f.write (str(self.__dupletsProba[a][b]))
                if (b!=WordGenerator.__space):
                    f.write (";")
                else:
                    f.write ("\n")
        f.close()
        print ("Results stored in:", os.path.join(self.__workingDirectory,"LetterProbability.csv"))
    
    def printDupletsProba (self):
        for a in range (WordGenerator.__tableSize):
            print ("\nFrom", WordGenerator.__alphabet[a],"to:")
            for b in range (WordGenerator.__tableSize):
                print (WordGenerator.__alphabet[b],end=" ")
                print (str(self.__dupletsProba[a][b]),end=" ")
    

        
    def __init__(self,directory):
        self.__dupletsProba=[ [ 0 for i in range(WordGenerator.__tableSize) ] for j in range(WordGenerator.__tableSize) ]
        self.__tripletsProba=[ [ [ 0 for i in range(WordGenerator.__tableSize) ] for j in range(WordGenerator.__tableSize) ] for k in range(WordGenerator.__tableSize) ]
        self.__workingDirectory=directory
        
        random.seed()
        for filename in os.listdir(self.__workingDirectory):
            print (os.path.join(self.__workingDirectory,filename),"...", end=" ")
            i=0
            e=0
            for line in open(os.path.join(self.__workingDirectory,filename)):
                i+=1
                try:
                    #consider line starts with space
                    self.__dupletsProba[WordGenerator.__space][string.ascii_lowercase.index(line[0])] +=1
                    if (len(line)>2):
                        self.__tripletsProba[WordGenerator.__space][string.ascii_lowercase.index(line[0])][string.ascii_lowercase.index(line[1])] +=1
                    for j in range (len(line)-1):
                        if (line[j+1]!="\r" and line[j+1]!="\n"):
                            self.__dupletsProba[string.ascii_lowercase.index(line[j])][string.ascii_lowercase.index(line[j+1])] +=1
                            if (j<len(line)-2):
                                if (line[j+2]!="\r" and line[j+2]!="\n"):
                                    self.__tripletsProba[string.ascii_lowercase.index(line[j])][string.ascii_lowercase.index(line[j+1])][string.ascii_lowercase.index(line[j+2])] +=1
                                else:
                                    self.__tripletsProba[string.ascii_lowercase.index(line[j])][string.ascii_lowercase.index(line[j+1])][WordGenerator.__space] +=1
                        else:
                            self.__dupletsProba[string.ascii_lowercase.index(line[j])][WordGenerator.__space] +=1
                except ValueError:
                    e+=1       
            print (i,"words parsed,",e,"errors")        
        self.__normalizeDupletsProba()
        
    def __selectNextLetter(self,previousLetter,previousPreviousLetter="",nbCandidates=1):   
        if (previousLetter==" "):
            newLetter=choice(WordGenerator.__alphabet, p=self.__dupletsProba[WordGenerator.__space])
        else:
            if (previousPreviousLetter==""):
                newLetter=choice(WordGenerator.__alphabet, p=self.__dupletsProba[string.ascii_lowercase.index(previousLetter)])
            else:
                newLetterCandidates=[]
                for _ in range (nbCandidates):            
                    newLetterCandidates.append(choice(WordGenerator.__alphabet, p=self.__dupletsProba[string.ascii_lowercase.index(previousLetter)]))
                maxTripletProba=0
                for letter in newLetterCandidates:
                    if (self.__tripletsProba[self.__charToIndex(previousPreviousLetter)][self.__charToIndex(previousLetter)][self.__charToIndex(letter)]>=maxTripletProba):
                        maxTripletProba=self.__tripletsProba[self.__charToIndex(previousPreviousLetter)][self.__charToIndex(previousLetter)][self.__charToIndex(letter)]
                        newLetter=letter                
        return newLetter          
        
    def createRandomWord(self,minNbLetter=1):
        word=""
        while (len(word)<minNbLetter):
            word=""
            word+=self.__selectNextLetter(" ")
            newLetter=""        
            while (newLetter!=" "):
                if (len(word)>=2):
                    #start evaluating candidates based on triplets
                    newLetter=self.__selectNextLetter(word[len(word)-1],word[len(word)-2],10)
                else:
                    newLetter=self.__selectNextLetter(word[len(word)-1])
                word+=newLetter            
        return word
            
    
# main           
'''
frenchGenerator=WordGenerator("francais")
for i in range (50):
    print (frenchGenerator.createRandomWord())
'''

englishGenerator=WordGenerator("English Open Word List (EOWL)")
for i in range (50):
    print (englishGenerator.createRandomWord())

