#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 6 juil. 2017

@author: Olivier Irac
'''
import os
import random
import pickle
import sys
import argparse
from numpy.random import choice

class WordGenerator:
    # dupletsProba[char1][char2] stores probability of char1 followed by char 2
    # tripletsProba [char1][char2][char3] stores number of occurrences of char1 followed by char2 followed by char3
    # tables are normalized so that row sum=1 to be able to use numpy.random.choice duplets[char1], triplets [char1][char2]
    __alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ','’','-','\'','œ','ç','á','é','ú','à','À','è','ì','ù','â','ê','î','ô','û','ä','ë','ï','ö','ü','Ã','ß']
    __space=__alphabet.index(' ')
    __tableSize=len(__alphabet)
    
    def __verbosePrint(self,*args):
        if (self.__verbose):
            print (*args)
            
    def __charToIndex(self,char):
        try:
            return WordGenerator.__alphabet.index(char)
        except ValueError:
            raise ValueError ("Cannot decode character",char)
        
    def __normalizeProba (self):
        for i in range (WordGenerator.__tableSize):
            dupletsSum=0
            for j in range (WordGenerator.__tableSize):
                dupletsSum+=self.__dupletsProba[i][j]
                tripletsSum=0
                for k in range (WordGenerator.__tableSize):
                    tripletsSum+=self.__tripletsProba[i][j][k]
                for k in range (WordGenerator.__tableSize):
                    try:
                        self.__tripletsProba[i][j][k]/=tripletsSum
                    except ZeroDivisionError:
                        pass    
                    
            if (dupletsSum==0):
                self.__verbosePrint("No letter",WordGenerator.__alphabet[i])
            else:
                for j in range (WordGenerator.__tableSize):
                    try:
                        self.__dupletsProba[i][j]/=dupletsSum
                    except ZeroDivisionError:
                        pass
                    if (self.__dupletsProba[i][j]==0):
                        self.__verbosePrint("Empty proba", WordGenerator.__alphabet[i], WordGenerator.__alphabet[j])

                
    def saveDupletsProbaAsCsv (self):
        f = open(os.path.join(self.__workingDirectory,"DupletsProbability.csv"),"w")
        for a in range (WordGenerator.__tableSize):
            for b in range (WordGenerator.__tableSize):
                f.write (str(self.__dupletsProba[a][b]))
                if (b!=WordGenerator.__space):
                    f.write (";")
                else:
                    f.write ("\n")
        f.close()
        print ("Results stored in:", os.path.join(self.__workingDirectory,"DupletsProbability.csv"))
    
    def printDupletsProba (self):
        for a in range (WordGenerator.__tableSize):
            print ("\nFrom", WordGenerator.__alphabet[a],"to:")
            for b in range (WordGenerator.__tableSize):
                print (WordGenerator.__alphabet[b],end=" ")
                print (str(self.__dupletsProba[a][b]),end=" ")
    

        
    def __init__(self,directory,forceProbaTablesUpdate=False,verbose=False):
        self.__dupletsProba=[ [ 0 for _ in range(WordGenerator.__tableSize) ] for _ in range(WordGenerator.__tableSize) ]
        self.__tripletsProba=[ [ [ 0 for _ in range(WordGenerator.__tableSize) ] for _ in range(WordGenerator.__tableSize) ] for _ in range(WordGenerator.__tableSize) ]
        self.__workingDirectory=directory
        self.__verbose=verbose
        
        random.seed()
        if (not forceProbaTablesUpdate and os.path.isfile(os.path.join(self.__workingDirectory,"dupletsproba.sav")) and os.path.isfile(os.path.join(self.__workingDirectory,"tripletsproba.sav"))):
            # read proba tables from .sav files
            with open(os.path.join(self.__workingDirectory,"dupletsproba.sav"), 'rb') as fp:
                self.__dupletsProba=pickle.load(fp)
            with open(os.path.join(self.__workingDirectory,"tripletsproba.sav"), 'rb') as fp:
                self.__tripletsProba=pickle.load(fp)
            self.__verbosePrint ("Loaded probability tables from ", os.path.join(self.__workingDirectory,"dupletsproba.sav"), os.path.join(self.__workingDirectory,"tripletsproba.sav"))
        
        else:    
            # analayse each .txt file and fill duplets and triplets proba tables, store tables in .sav files 
            for filename in os.listdir(self.__workingDirectory):
                if filename.endswith('.txt'):
                    print (os.path.join(self.__workingDirectory,filename))
                    wordCount=0
                    errorCount=0
                    try:
                        #for line in open(os.path.join(self.__workingDirectory,filename),encoding="utf8"):
                        for line in open(os.path.join(self.__workingDirectory,filename)):
                            wordCount+=1
                            try:
                                # consider word starts with space
                                self.__dupletsProba[WordGenerator.__space][self.__charToIndex(line[0])] +=1
                                if (len(line)>2):
                                    # store triplet only if word is at least space-char1-char2 
                                    self.__tripletsProba[WordGenerator.__space][self.__charToIndex(line[0])][self.__charToIndex(line[1])] +=1
                                for j in range (len(line)-1):
                                    if (line[j+1]!="\r" and line[j+1]!="\n"):
                                        # break words on end of line or comma, store duplet normally and store triplet if next char is still not eof word
                                        self.__dupletsProba[self.__charToIndex(line[j])][self.__charToIndex(line[j+1])] +=1
                                        if (j<len(line)-2):
                                            if (line[j+2]!="\r" and line[j+2]!="\n"):
                                                self.__tripletsProba[self.__charToIndex(line[j])][self.__charToIndex(line[j+1])][self.__charToIndex(line[j+2])] +=1
                                            else:
                                                self.__tripletsProba[self.__charToIndex(line[j])][self.__charToIndex(line[j+1])][WordGenerator.__space] +=1
                                    else:
                                        # consider word ends with space
                                        self.__dupletsProba[self.__charToIndex(line[j])][WordGenerator.__space] +=1
                            except ValueError as e:
                                self.__verbosePrint ("Line", wordCount, e)
                                errorCount+=1       
                    except UnicodeDecodeError as e:
                        print(e)  
                    print (wordCount,"words parsed,",errorCount,"errors")  

            self.__normalizeProba()
            with open(os.path.join(self.__workingDirectory,"dupletsproba.sav"), 'wb') as fp:
                pickle.dump(self.__dupletsProba, fp)
            with open(os.path.join(self.__workingDirectory,"tripletsproba.sav"), 'wb') as fp:
                pickle.dump(self.__tripletsProba, fp)
        
    def __selectNextLetter(self,previousLetter,previousPreviousLetter="",nbCandidates=1):   
        if (previousLetter==" "):
            # Draw 1st letter
            newLetter=choice(WordGenerator.__alphabet, p=self.__dupletsProba[WordGenerator.__space])
        else:
            if (previousPreviousLetter==""):
                # Do not use triplets
                newLetter=choice(WordGenerator.__alphabet, p=self.__dupletsProba[self.__charToIndex(previousLetter)])
            else:
                # Draw nbCandidates letters from duplets probability and select best match from triplets 
                newLetterCandidates=[]
                for _ in range (nbCandidates):            
                    newLetterCandidates.append(choice(WordGenerator.__alphabet, p=self.__dupletsProba[self.__charToIndex(previousLetter)]))
                maxTripletProba=0
                for letter in newLetterCandidates:
                    if (self.__tripletsProba[self.__charToIndex(previousPreviousLetter)][self.__charToIndex(previousLetter)][self.__charToIndex(letter)]>=maxTripletProba):
                        maxTripletProba=self.__tripletsProba[self.__charToIndex(previousPreviousLetter)][self.__charToIndex(previousLetter)][self.__charToIndex(letter)]
                        newLetter=letter                
        return newLetter          
        
    def createRandomWord(self, minLen=1, maxLen=100, firstLetter="", nbCandidates=4):
        # higher number of candidates means less creative words
        word=""
        while (len(word)-1<minLen or len(word)-1>maxLen):
            word=""
            # select first letter
            if (firstLetter==""):
                word+=self.__selectNextLetter(" ")
            else:
                word+=firstLetter
            # select second letter
            word+=self.__selectNextLetter(word[len(word)-1]," ", nbCandidates)
            # select next letters
            while (word[len(word)-1]!=" "):
                word+=self.__selectNextLetter(word[len(word)-1], word[len(word)-2], nbCandidates)                            
        return word            
    
# main           
parser = argparse.ArgumentParser(description = "WordGenerator allows to generate random words based on language statistics.")
parser.add_argument("-l", "--language", help = "en, fr (default), de, it, sh", required = False, default = "fr")
parser.add_argument("-n", "--number", help = "number of words to generate, default 20", required = False, default = 20)
parser.add_argument("-min", "--minletters", help = "minimum number of letters per word, default 3", required = False, default = 3)
parser.add_argument("-max", "--maxletters", help = "maximum number of letters per word, default 10", required = False, default = 10)
parser.add_argument("-s", "--startletter", help = "forces word to start with a specific letter", required = False, default = "")
parser.add_argument("-c", "--creativity", help = "1-10, lower values are more creative but can give strange words, higher values more conservative", required = False, default = 4)
parser.add_argument("-f", "--force", help = "force tables generation instead of using .sav files, True/False(default)", required = False, default = False)
parser.add_argument("-v", "--verbose", help = "prints additional information, True/False(default)", required = False, default = False)
argument = parser.parse_args()
dictionary={'en':"English",'fr':"francais full", 'de':"German", 'it':"Italiano",'sh':"Shadok"}
wordGenerator=WordGenerator(dictionary[argument.language], argument.force, argument.verbose)
for _ in range (int(argument.number)):
    print (wordGenerator.createRandomWord(int(argument.minletters),int(argument.maxletters),argument.startletter,int(argument.creativity)))
