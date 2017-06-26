# def add(a,b):
#     return a+b
# 
# def addFixedValue(a):
#     y = 5
#     return y +a
# 
# print (add(1,2))
# print (addFixedValue(1))
# print ("Hello World")
# print (1+2)
# a=10
# b=2
# print (a+b)
# 
# print (str(a)+"Olivier")

import random
import string

def exo1 ():
    bonjour = "Hello "
    monde = "World"
    phrase = bonjour+monde
    print (phrase)
    annee = 2017
    phrase = bonjour + monde + str(annee)
    print (phrase)
    for i in range (0, 20) :print (i)
    
    a="42"
    print (str(annee)+a)
    print (annee+int(a))
    
    x=13
    y=5
    print (x/y)
    print (float(x)/float(y))
    
    c1='a'
    c2='b'
    print (c1+c2)
    ctmp=c1
    c1=c2
    c2=ctmp
    print (c1+c2)

def exo2 ():
    nbInvites=input("Nb invites? ")
    if nbInvites==1:
        print("Solo")
    elif nbInvites==2:
        print ("Duo")
    elif nbInvites<=4:
        print ("Intime")
    else:
        print ("Rassemblement")
        
def exo3():
    x=input("x?")
    for i in range (0,x+1):
        print (i),
        
    print
    for i in range (-5,x+6):
        print (i),

def exo4():
    s=""
    for _ in range (0,10):
        s+="*"
    print (s)
    
def exo5():
    s=""
    for _ in range (0,10):
        for _ in range (0,10):
            s+='*'
        s+='\n'
    print (s)

def exo6():
    x=int(input("step?"))
    y=int(input("max?"))
    for i in range (0,y,x):
        print (i, end=' ')
        
def exo7():
        size=int(input("Size?"))
        middle=size/2;
        start=0;
        end=0;
        s="";
        
        for i in range (0,size):
            start = abs(middle-i)
            end = min (middle+i,size-abs(middle-i))
            for _ in range (0,start):
                s+=' '
            for _ in range (start,end):
                s+='*'
            s+='\n'
        print(s)
        

def exo8():
    maPhrase=["Bonjour", "tout", "le", "monde."]
    print (maPhrase)  
    for word in maPhrase:
        print (word,end=" ")
        
def afficherPhrase(phrase):
    for word in phrase:
        print (word,end=" ")
        
def exo9():
    maPhrase=["Bonjour", "tous", "les", "gars."]
    afficherPhrase(maPhrase)

def construireMotAleatoire(nbLettres):
    mot=""
    for _ in range (nbLettres):
        mot+=random.choice(string.ascii_lowercase)
    return mot

def construireTableauMotsAleatoire(nbLettres, nbMots):
    tableMotsAleatoires=[]
    for _ in range (nbMots):
        tableMotsAleatoires.append(construireMotAleatoire(nbLettres))
    return tableMotsAleatoires
     
def exo10():
    random.seed()
    for word in construireTableauMotsAleatoire(7,10):
        print (word)
    print (construireTableauMotsAleatoire(7,10))

def checkDico(mot,dico):
    for word in dico:
        if (word==mot): 
            return True
    return False
    
def exo11():
    dico={"buse","bute","nier","fuit","bare"}
    while (True):
        i=0
        found=False
        while (found==False):
            i+=1
            mot=construireMotAleatoire(4)
            found=checkDico(mot, dico)
        print (i)
        
        
    

exo11()