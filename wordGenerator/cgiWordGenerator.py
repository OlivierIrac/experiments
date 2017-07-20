
#!/usr/bin/python3.6
'''
Created on 19 juil. 2017

@author: irac1
'''

import os
import random
import pickle
from numpy.random import choice
import cgitb
import cgi
cgitb.enable()


class WordGenerator:
    # dupletsProba[char1][char2] stores probability of char1 followed by char 2
    # tripletsProba [char1][char2][char3] stores number of occurrences of char1 followed by char2 followed by char3
    # tables are normalized so that row sum=1 to be able to use numpy.random.choice duplets[char1], triplets [char1][char2]
    __alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', '’', '-', '\'', 'œ', 'ç', 'á', 'é', 'ú', 'à', 'À', 'è', 'ì', 'ò', 'ù', 'â', 'ê', 'î', 'ô', 'û', 'ä', 'ë', 'ï', 'ö', 'ü', 'Ã', 'Ä', 'ß']
    __space = __alphabet.index(' ')
    __tableSize = len(__alphabet)

    def __verbosePrint(self, *args):
        if (self.__verbose):
            print(*args)

    def __charToIndex(self, char):
        try:
            return WordGenerator.__alphabet.index(char)
        except ValueError:
            raise ValueError("Cannot decode character", char)

    def __normalizeProba(self):
        for i in range(WordGenerator.__tableSize):
            dupletsSum = 0
            for j in range(WordGenerator.__tableSize):
                dupletsSum += self.__dupletsProba[i][j]
                tripletsSum = 0
                for k in range(WordGenerator.__tableSize):
                    tripletsSum += self.__tripletsProba[i][j][k]
                for k in range(WordGenerator.__tableSize):
                    try:
                        self.__tripletsProba[i][j][k] /= tripletsSum
                    except ZeroDivisionError:
                        pass

            if (dupletsSum == 0):
                self.__verbosePrint("No letter", WordGenerator.__alphabet[i])
            else:
                for j in range(WordGenerator.__tableSize):
                    try:
                        self.__dupletsProba[i][j] /= dupletsSum
                    except ZeroDivisionError:
                        pass
                    if (self.__dupletsProba[i][j] == 0):
                        self.__verbosePrint("Empty proba", WordGenerator.__alphabet[i], WordGenerator.__alphabet[j])



    def __init__(self, directory, forceProbaTablesUpdate=False, verbose=False):
        self.__dupletsProba = [[0 for _ in range(WordGenerator.__tableSize)] for _ in range(WordGenerator.__tableSize)]
        self.__tripletsProba = [[[0 for _ in range(WordGenerator.__tableSize)] for _ in range(WordGenerator.__tableSize)]for _ in range(WordGenerator.__tableSize)]
        self.__workingDirectory = directory
        self.__verbose = verbose

        random.seed()
        if (not forceProbaTablesUpdate and os.path.isfile(os.path.join(self.__workingDirectory, "dupletsproba.sav")) and os.path.isfile(os.path.join(self.__workingDirectory, "tripletsproba.sav"))):
            # read proba tables from .sav files
            with open(os.path.join(self.__workingDirectory, "dupletsproba.sav"), 'rb') as fp:
                self.__dupletsProba = pickle.load(fp)
            with open(os.path.join(self.__workingDirectory, "tripletsproba.sav"), 'rb') as fp:
                self.__tripletsProba = pickle.load(fp)
            self.__verbosePrint("Loaded probability tables from ", os.path.join(self.__workingDirectory, "dupletsproba.sav"), os.path.join(self.__workingDirectory, "tripletsproba.sav"))



    def __selectNextLetterBasedOnDupletsCandidates(self, previousLetter, previousPreviousLetter="", nbCandidates=1):
        # Draw nbCandidates letters from duplets probability table and select final candidate from from triplets highest proba
        if (previousLetter == " "):
            # Draw 1st letter
            newLetter = choice(WordGenerator.__alphabet, p=self.__dupletsProba[WordGenerator.__space])
        else:
            if (previousPreviousLetter == ""):
                # Do not use triplets
                newLetter = choice(WordGenerator.__alphabet, p=self.__dupletsProba[self.__charToIndex(previousLetter)])
            else:
                newLetterCandidates = []
                for _ in range(nbCandidates):
                    newLetterCandidates.append(choice(WordGenerator.__alphabet, p=self.__dupletsProba[self.__charToIndex(previousLetter)]))
                maxTripletProba = 0
                for letter in newLetterCandidates:
                    currentTripletProba = self.__tripletsProba[self.__charToIndex(previousPreviousLetter)][self.__charToIndex(previousLetter)][self.__charToIndex(letter)]
                    if (currentTripletProba >= maxTripletProba):
                        maxTripletProba = currentTripletProba
                        newLetter = letter
        return newLetter

    def __selectNextLetterBasedOnTriplets(self, previousLetter, previousPreviousLetter=" ", unused=0):
        return choice(WordGenerator.__alphabet, p=self.__tripletsProba[self.__charToIndex(previousPreviousLetter)][self.__charToIndex(previousLetter)])

    def createRandomWord(self, minLen=1, maxLen=100, firstLetter="", algorithm="triplets", nbCandidates=4):
        # for duplets algo, lower values for nbCandidates are more creative but can generate strange words, higher values are more conservative
        # for triplets algo, nbCandidates is not used
        if (algorithm == "duplets"):
            selectNextLetter = self.__selectNextLetterBasedOnDupletsCandidates
        else:
            selectNextLetter = self.__selectNextLetterBasedOnTriplets

        word = ""
        while (len(word) - 1 < minLen or len(word) - 1 > maxLen):
            word = ""
            # select first letter
            if (firstLetter == ""):
                word += selectNextLetter(" ")
            else:
                word += firstLetter
            # select second letter
            word += selectNextLetter(word[len(word) - 1], " ", nbCandidates)
            # select next letters
            while (word[len(word) - 1] != " "):
                word += selectNextLetter(word[len(word) - 1], word[len(word) - 2], nbCandidates)
        return word

form = cgi.FieldStorage() 

print ("Content-type: text/html\n\n")

print("""<html>
<style>
body {
  font-family: Arial;
}
</style>
<header><title>Random Words</title></header>
<body>""")

languageDirectory = {'en': "English", 'fr': "francais full", 'de': "German", 'it': "Italiano", 'sh': "Shadok", 'dir': "."}
directory = languageDirectory[form.getvalue('language')]

if form.getvalue('firstletter'):
    firstletter=form.getvalue('firstletter')
else:
    firstletter=""

try:
    wordGenerator = WordGenerator(directory)
    for _ in range(int(form.getvalue('nbwords'))):
        print(wordGenerator.createRandomWord(int(form.getvalue('min')), int(form.getvalue('max')), firstletter, form.getvalue('algo'), int(form.getvalue('nbcandidates'))).encode('ascii', 'xmlcharrefreplace').decode("ascii"))
        print("<br>")
except ValueError as e:
    print (e)

print("""
</body>
</html>""")

