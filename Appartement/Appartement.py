

class Canape:
    def __init__(self,n=0,t=""):
        self.nbPlaces=n
        self.type=t
        
    def description(self):
        return "Canape de "+str(self.nbPlaces)+" places, en "+self.type
            
class Appartement:
    def __init__ (self,c,t):
        self.couleurMur=c
        self.typeSol=t
        self.listeCanapes=[]
    
    def description(self):
        s="Appartement avec des murs "+self.couleurMur+" et un sol en "+self.typeSol+".\n"
        if (len(self.listeCanapes)==0):
            s+="Sans canape.\n"
        else:
            s+="Avec "+str(len(self.listeCanapes))+" canape(s):\n"
            for canape in self.listeCanapes:
                s+=canape.description()+"\n"
        return s  
    
    def ajoutCanape(self,n=3,t="cuir"):
        self.listeCanapes.append(Canape(n,t))      

appart=Appartement("blanc","parquet")
print (appart.description())
appart.couleurMur="rouge"
print (appart.description())
appart.ajoutCanape()
print (appart.description())
appart.ajoutCanape(2,"tissu")
print (appart.description())



