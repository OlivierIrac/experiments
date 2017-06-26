'''
Created on 13 juin 2017

@author: irac1
'''

class Felin:
    def __init__ (self,nom="", espece ="", age=0):
        self.nom=nom
        self.espece=espece
        self.age=age
        
    def sePresenter (self):
        return "Je suis un felin de de nom %s, d'espece %s, d'age %i" % (self.nom, self.espece, self.age)
    
    def __str__ (self):
        return self.sePresenter()
    
    def seNourrir (self):
        return "Je mange de la viande"
    
class ChatSauvage(Felin):
    def __init__ (self,nom="", age=0, proie="Oiseaux"):
        Felin.__init__(self, nom, "Chat Sauvage", age)
        self.proie=proie
    
    def seNourrir (self,proieDuJour=""):
        if (proieDuJour==""):
            return "Je mange %s" % (self.proie)
        else:    
            return "Je mange %s" % (proieDuJour)
    
class ChatDomestique(Felin):
    def __init__ (self,nom="", age=0, couleurCollier="rouge"):
        Felin.__init__(self, nom, "Chat Domestique", age)
        self.couleurCollier=couleurCollier
    
    def seNourrir (self):
        return "Je mange des croquettes" 
    
    def sePresenter (self):
        return Felin.sePresenter(self) + " et j'ai un collier de couleur %s" %(self.couleurCollier)
        

mesFelins={ChatSauvage("Tigrou",10,"Oliphant"),ChatDomestique("Twenty",5,"noir")}
for felin in mesFelins:
    print (felin)
    print (felin.seNourrir())
    
    
    