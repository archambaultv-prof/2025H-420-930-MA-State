import time
from abc import ABC, abstractmethod


# ======================================================================
# AVANT  états était dispersé via if/elif.
# MAINTENANT : Chaque état est une classe.

class EtatFeu(ABC):
    @abstractmethod
    def demande_pieton(self, feu):
        ...
    @abstractmethod
    def tic(self, feu):
        ...
    @abstractmethod
    def afficher_etat(self): 
        ...
# avant Prolongement du rouge géré par if/elif
#--
# maintenant L'état ROUGE sait lui-même quoi faire 
class EtatRouge(EtatFeu): 
    def afficher_etat(self) -> str:
        return "rouge"
    
    def demande_pieton(self, feu):
    # rouge ici et non pas dans if/else
        if feu.minuteur < feu.duree_rouge:
            feu.duree_rouge += 10  

    def tic(self, feu):
        feu.minuteur += 1
        self.update_minuteur(feu)

    def update_minuteur(self, feu):
        if feu.minuteur >= feu.duree_rouge:
            feu.set_etat(EtatVert())
#Avant Transition vert->jaune par if/elif 
#--
#Aprè L'état VERT gère sa transition
class EtatVert(EtatFeu):
    def afficher_etat(self) -> str:
        return "vert"
    
    def demande_pieton(self, feu):
        # Aucun effet spécial a vert
        ...

    def tic(self, feu):
        feu.minuteur += 1
        self.update_minuteur(feu)

    def update_minuteur(self, feu):
        if feu.minuteur >= feu.duree_vert:
            feu.set_etat(EtatJaune())
#------------- Meme chose pour jaune
class EtatJaune(EtatFeu):
    def afficher_etat(self) -> str:
        return "jaune"

    def demande_pieton(self, feu):
        ...

    def tic(self, feu):
        feu.minuteur += 1
        self.update_minuteur(feu)

    def update_minuteur(self, feu):
        if feu.minuteur >= feu.duree_jaune:
            feu.set_etat(EtatRouge())
#Avant if/elif dispersé.
#---
#Maintenant : Un état dédié qui fige les transitions et ignore les demandes.
class EtatMaintenance(EtatFeu):
    def afficher_etat(self) -> str:
        return "maintenance (rouge clignotant)"

    # Ignorer les demandes en maintenance
    def demande_pieton(self, feu):
        ...

    def update_minuteur(self, feu):
        ...

    def tic(self, feu):
        ...
#--------------------------------------------------------------
class FeuDeCirculation:
    """
    Un système de feu de circulation qui cycle à travers différents états.
    """
    def __init__(self):
        self._etat = EtatRouge()
        self.minuteur = 0
        self.duree_rouge = 30
        self.duree_jaune = 5
        self.duree_vert = 25

#---
# AVANT : pas de méthode de switch. et tout transitait par if/elif.
#---
# Maintenant : set_etat() centralise le switch et réinitialise le timer.
    def set_etat(self, nouvel_etat: EtatFeu):  
        self._etat = nouvel_etat                
        self.minuteur = 0
        
    # Maintenant : on demande à l'état courant sa représentation.
    def obtenir_etat_actuel(self):
        return self._etat.afficher_etat()
    def obtenir_minuteur(self):
        return self.minuteur
    
    # Maintenant :  délègue à l'état courant.
    def tic(self):
        self._etat.tic(self)
    def demande_pieton(self):
        self._etat.demande_pieton(self)

    # maintenant un simple switch d'état.
    def mode_maintenance(self):
        self.set_etat(EtatMaintenance())
    def operation_normale(self):
        """Retourner à l'opération normale depuis le mode maintenance"""
        self.set_etat(EtatRouge())
    
    # Maintenant : on interroge l'état courant pour son nom et on calcule
    def obtenir_affichage_statut(self):
        etat = self._etat.afficher_etat()
        """Obtenir une chaîne d'affichage du statut"""
        if etat == "rouge":
            return f"🔴 ROUGE ({self.duree_rouge - self.minuteur}s restantes)"
        elif etat == "jaune":
            return f"🟡 JAUNE ({self.duree_jaune - self.minuteur}s restantes)"
        elif etat == "vert":
            return f"🟢 VERT ({self.duree_vert - self.minuteur}s restantes)"
        elif etat.startswith("maintenance"):
            return "🔴 MAINTENANCE (clignotant)"
        else:
            return "❓ ÉTAT INCONNU"



def main():
    """
    Démonstration du système de feu de circulation.
    """
    
    print("Système de Feu de Circulation")
    print("=" * 75)
    
    feu_de_circulation = FeuDeCirculation()
    
    # Simuler l'opération du feu de circulation
    print("\n--- Simulation d'Opération Normale ---")
    for seconde in range(90):  # Exécuter pendant 90 secondes
        print(f"Temps: {seconde:2d}s | {feu_de_circulation.obtenir_affichage_statut()}")
        
        # Simuler quelques événements
        if seconde == 15:
            print("           🚶 Bouton piéton pressé!")
            feu_de_circulation.demande_pieton()
        
        if seconde == 75:
            print("           🔧 Entrée en mode maintenance!")
            feu_de_circulation.mode_maintenance()
        
        if seconde == 85:
            print("           ✅ Retour à l'opération normale!")
            feu_de_circulation.operation_normale()

        feu_de_circulation.tic()
        
        time.sleep(0.1)  # Ralentir la simulation
    
    print("\n--- Statut Final ---")
    print(f"État actuel: {feu_de_circulation.obtenir_etat_actuel()}")


if __name__ == "__main__":
    main()