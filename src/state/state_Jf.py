import time
from abc import ABC, abstractmethod  

class State(ABC):
    @abstractmethod
    def gestion_tic(self):
       ...
    
    @abstractmethod
    def obtenir_etat(self):
       ...

    @abstractmethod
    def obtenir_affichage(self):
       ...

class LumiereRouge(State):
    def gestion_tic(self, feu):
        feu.minuteur += 1
        if feu.minuteur >= feu.duree_rouge:
            feu.set_etat(LumiereVert())
    
    def obtenir_etat(self):
        return "Rouge"
    
    def obtenir_affichage(self, feu):
        return f"🔴 ROUGE ({feu.duree_rouge - feu.minuteur}s restantes)"

class LumiereJaune(State):
    def gestion_tic(self, feu):
        feu.minuteur += 1
        if feu.minuteur >= feu.duree_jaune:
            feu.set_etat(LumiereRouge())
    
    def obtenir_etat(self):
        return "Jaune"
    
    def obtenir_affichage(self, feu):
        return f"🟡 JAUNE ({feu.duree_jaune - feu.minuteur}s restantes)"

class LumiereVert(State):
    def gestion_tic(self, feu):
        feu.minuteur += 1
        if feu.minuteur >= feu.duree_vert:
            feu.set_etat(LumiereJaune())
    
    def obtenir_etat(self):
        return "Vert"
    
    def obtenir_affichage(self, feu):
        return f"🟢 VERT ({feu.duree_vert - feu.minuteur}s restantes)"

class Maintenance(State):
    def gestion_tic(self, feu):
        # En maintenance, on ne fait rien
        pass
    
    def obtenir_etat(self):
        return "Maintenance"
    
    def obtenir_affichage(self, feu):
        return "🔴 MAINTENANCE (clignotant)"

class FeuDeCirculation:
    def __init__(self):
        self.etat = LumiereRouge()
        self.minuteur = 0
        self.duree_rouge = 30
        self.duree_jaune = 5
        self.duree_vert = 25
    
    def obtenir_etat(self):
        return self.etat
    
    def obtenir_affichage(self):
        return self.etat.obtenir_affichage(self)

    def tic(self):
        self.etat.gestion_tic(self)

    def set_etat(self, nouvel_etat):
        self.etat = nouvel_etat
        self.minuteur = 0
    
    def set_etat(self, nouvel_etat):
        self.etat = nouvel_etat
        self.minuteur = 0


def main():
   
    print("Système de Feu de Circulation")
    print("=" * 50)
    
    feu = FeuDeCirculation()
    
    for i in range(240):  
        print(f"Temps: {i:2d}s | {feu.obtenir_affichage()}")
        feu.tic()
        
        if i == 20:
            print("           🔧 Entrée en mode maintenance!")
            feu.set_etat(Maintenance())
        
        if i == 25:
            print("           ✅ Retour à l'opération normale!")
            feu.set_etat(LumiereRouge())
        
        time.sleep(0.1)  

if __name__ == "__main__":
    main() 