# -*- coding: utf-8 -*-
'''
Created on 11 mars 2018

@author: Olivier
'''
import random
import time


class interroTable:
    def __init__(self, nbQuestion=0):
        self.__tableMax = int(input("Table maximum? "))
        if (nbQuestion == 0):
            self.__nbQuestion = int(input("Nombre de questions? "))
        else:
            self.__nbQuestion = nbQuestion

    def start(self):
        startTime = time.time()
        goodAnswer = 0
        for i in range(self.__nbQuestion):
            a = random.randrange(2, self.__tableMax + 1)
            b = random.randrange(2, self.__tableMax + 1)
            answer = int(input("(question " + str(i + 1) + "/" + str(self.__nbQuestion) + ") " + str(a) + " x " + str(b) + " = ?"))
            if (answer == a * b):
                goodAnswer += 1
            else:
                print ("Faux, la réponse était " + str(a * b))
        print ("Score : " + str(goodAnswer) + "/" + str(self.__nbQuestion))
        print (str(round(time.time() - startTime)) + " secondes")


interro = interroTable()
interro.start()
