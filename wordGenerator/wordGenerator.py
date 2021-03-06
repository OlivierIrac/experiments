#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 6 juil. 2017

@author: Olivier Irac
'''
import os
import random
import pickle
import cchardet
from numpy.random import choice


class WordGenerator:
    # dupletsProba[char1][char2] stores probability of char1 followed by char 2
    # tripletsProba [char1][char2][char3] stores number of occurrences of char1 followed by char2 followed by char3
    # tables are normalized so that row sum=1 to be able to use numpy.random.choice duplets[char1], triplets [char1][char2]
    __alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', '’', '-', '\'', 'œ', 'ç', 'á', 'é', 'ú', 'à', 'À', 'è', 'ì', 'ò', 'ù', 'â', 'ê', 'î', 'ô', 'û', 'ä', 'ë', 'ï', 'ö', 'ü', 'Ã', 'Ä', 'ß', 'É', 'È']
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

    def saveDupletsProbaAsCsv(self):
        f = open(os.path.join(self.__workingDirectory, "DupletsProbability.csv"), "w")
        for a in range(WordGenerator.__tableSize):
            for b in range(WordGenerator.__tableSize):
                f.write(str(self.__dupletsProba[a][b]))
                if (b != WordGenerator.__space):
                    f.write(";")
                else:
                    f.write("\n")
        f.close()
        print("Results stored in:", os.path.join(self.__workingDirectory, "DupletsProbability.csv"))

    def printDupletsProba(self):
        for a in range(WordGenerator.__tableSize):
            print("\nFrom", WordGenerator.__alphabet[a], "to:")
            for b in range(WordGenerator.__tableSize):
                print(WordGenerator.__alphabet[b], end=" ")
                print(str(self.__dupletsProba[a][b]), end=" ")

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

        else:
            # analayse each .txt file and fill duplets and triplets proba tables, store tables in .sav files
            wordFound = False
            for filename in os.listdir(self.__workingDirectory):
                if filename.endswith('.txt'):
                    print(os.path.join(self.__workingDirectory, filename))
                    wordCount = 0
                    errorCount = 0
                    try:
                        # check file encoding and open file accordingly
                        with open(os.path.join(self.__workingDirectory, filename), 'rb') as f:
                            msg = f.read()
                        result = cchardet.detect(msg)
                        self.__verbosePrint(result)
                        f.close()

                        if (result['encoding'] == 'UTF-8-SIG'):
                            f = open(os.path.join(self.__workingDirectory, filename), encoding="utf8")
                        else:
                            f = open(os.path.join(self.__workingDirectory, filename))

                        # parse each line from the file and populates proba tables. Assuming one word per line
                        for line in f:
                            wordCount += 1
                            wordFound = True
                            try:
                                # consider word starts with space
                                self.__dupletsProba[WordGenerator.__space][self.__charToIndex(line[0])] += 1
                                self.__tripletsProba[WordGenerator.__space][WordGenerator.__space][self.__charToIndex(
                                    line[0])] += 1
                                if (len(line) > 2):
                                    # store triplet only if word is at least space-char1-char2
                                    self.__tripletsProba[WordGenerator.__space][self.__charToIndex(
                                        line[0])][self.__charToIndex(line[1])] += 1
                                for j in range(len(line) - 1):
                                    if (line[j + 1] != "\r" and line[j + 1] != "\n"):
                                        # break words on end of line or comma, store duplet normally and store
                                        # triplet if next char is still not eof word
                                        self.__dupletsProba[self.__charToIndex(line[j])][self.__charToIndex(line[j + 1])] += 1
                                        if (j < len(line) - 2):
                                            if (line[j + 2] != "\r" and line[j + 2] != "\n"):
                                                self.__tripletsProba[self.__charToIndex(line[j])][self.__charToIndex(line[j + 1])][self.__charToIndex(line[j + 2])] += 1
                                            else:
                                                self.__tripletsProba[self.__charToIndex(line[j])][self.__charToIndex(line[j + 1])][WordGenerator.__space] += 1
                                    else:
                                        # consider word ends with space
                                        self.__dupletsProba[self.__charToIndex(line[j])][WordGenerator.__space] += 1
                            except ValueError as e:
                                print("Line", wordCount, e)
                                errorCount += 1
                        f.close()
                    except UnicodeDecodeError as e:
                        print(e)
                    print(wordCount, "words parsed,", errorCount, "errors")

            if (not wordFound):
                raise ValueError("No language .txt or .sav files found in directory", directory)
            else:
                self.__normalizeProba()
                with open(os.path.join(self.__workingDirectory, "dupletsproba.sav"), 'wb') as fp:
                    pickle.dump(self.__dupletsProba, fp)
                with open(os.path.join(self.__workingDirectory, "tripletsproba.sav"), 'wb') as fp:
                    pickle.dump(self.__tripletsProba, fp)

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
