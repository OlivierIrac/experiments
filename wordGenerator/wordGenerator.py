'''
Created on 6 juil. 2017

@author: irac1
'''
import os
import string
# encoding: utf-8

def buildLetterProbability(directory):
#    letterProbability=[[0]*27]*27
    letterProbability= [ [ 0 for i in range(27) ] for j in range(27) ]
    for filename in os.listdir(directory):
        print (filename,"...", end=" ")
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
        print (i,"words parsed",e,"errors")
    print (letterProbability)
    for a in range (0,27):
        print (chr(97+a), end=" ")
        for b in range (0,27):
            print (chr(97+b),letterProbability[a][b], end=" ")
        print ("\n")
            
buildLetterProbability("English Open Word List (EOWL)")
        
