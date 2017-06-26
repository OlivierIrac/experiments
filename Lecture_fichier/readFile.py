'''
Created on 13 juin 2017

@author: irac1
'''
for line in open("config.ini"):
    try:
        firstname, lastname, age =line.split(";",3)
        age=int(age)
        print ("Nom: %s, Prenom: %s, age: %i" %(firstname, lastname, age))
    except ValueError:
        print ("Error on line: ", line, end="")
    
    
    