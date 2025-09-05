# Natacha MEYER's edit

import time
from abc import ABC, abstractmethod

class IEtatFeu(ABC):
    def __init__(self):
        self.duree: int

    @abstractmethod
    def afficher_etat(self) -> str:
        ...

    @abstractmethod
    def afficher_statut(self, feu: "FeuDeCirculation") -> str:
        ...
    
    def update_minuteur(self, feu: "FeuDeCirculation") -> str:
        ...

    def demande_pieton(self):
        ...
    
    def toggle_maintenance(self, feu: "FeuDeCirculation"):
        ...

class EtatRouge(IEtatFeu):
    def __init__(self):
        self.duree: int = 30

    def afficher_etat(self) -> str:
        return "🔴 ROUGE"
    
    def afficher_statut(self, feu: "FeuDeCirculation"):
        reste = self.duree - feu.minuteur
        return f"{self.afficher_etat()} ({reste}s restantes)"
    
    def update_minuteur(self, feu: "FeuDeCirculation"):
        if feu.minuteur is not None and feu.minuteur >= self.duree:
            feu.set_etat(EtatVert())
            feu.set_minuteur(0)
    
    def demande_pieton(self):
        self.duree += 10

    def toggle_maintenance(self, feu: "FeuDeCirculation"):
        if feu.minuteur is not None:
            feu.set_etat(EtatMaintenance())
            feu.set_minuteur = 0
    
class EtatJaune(IEtatFeu):
    def __init__(self):
        self.duree: int = 5

    def afficher_etat(self) -> str:
        return "🟡 JAUNE"
    
    def afficher_statut(self, feu: "FeuDeCirculation"):
        reste = self.duree - feu.minuteur
        return f"{self.afficher_etat()} ({reste}s restantes)"
    
    def update_minuteur(self, feu: "FeuDeCirculation"):
        if feu.minuteur is not None and feu.minuteur >= self.duree:
            feu.set_etat(EtatRouge())
            feu.set_minuteur(0)
    
class EtatVert(IEtatFeu):
    def __init__(self):
        self.duree: int = 25

    def afficher_etat(self) -> str:
        return "🟢 VERT"
    
    def afficher_statut(self, feu: "FeuDeCirculation"):
        reste = self.duree - feu.minuteur
        return f"{self.afficher_etat()} ({reste}s restantes)"
    
    def update_minuteur(self, feu: "FeuDeCirculation"):
        if feu.minuteur is not None and feu.minuteur >= self.duree:
            feu.set_etat(EtatJaune())
            feu.set_minuteur(0)
    
class EtatMaintenance(IEtatFeu):
    def afficher_etat(self) -> str:
        return "⛔ MAINTENANCE"
    
    def afficher_statut(self, feu: "FeuDeCirculation"):
        return f"⛔ MAINTENANCE (clignotant)"
    
    def toggle_maintenance(self, feu: "FeuDeCirculation"):
        if feu.minuteur is not None:
            feu.set_etat(EtatRouge())
    
class FeuDeCirculation:
    """
    Un système de feu de circulation qui cycle à travers différents états.
    """
    
    def __init__(self):
        self.etat: IEtatFeu = EtatRouge()
        self.minuteur = 0
    
    def set_etat(self, etat: IEtatFeu):
        self.etat = etat

    def set_minuteur(self, minute: int):
        self.minuteur = minute

    def afficher_etat(self):
        return self.etat.afficher_etat()
        
    def obtenir_etat_actuel(self):
        return self.etat.afficher_etat()
    
    def obtenir_minuteur(self):
        return self.minuteur
    
    def tic(self):
        """Avancer le minuteur d'une seconde"""
        self.minuteur += 1
        self.etat.update_minuteur(self)
    
    def demande_pieton(self):
        """Bouton piéton pressé - étendre l'état actuel si possible"""
        self.etat.demande_pieton()
    
    def toggle_maintenance(self):
        self.etat.toggle_maintenance(self)
    
    def obtenir_affichage_statut(self):
        """Obtenir une chaîne d'affichage du statut"""
        return self.etat.afficher_statut(self)


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
            feu_de_circulation.toggle_maintenance()
        
        if seconde == 85:
            print("           ✅ Retour à l'opération normale!")
            feu_de_circulation.toggle_maintenance()

        feu_de_circulation.tic()
        
        time.sleep(0.1)  # Ralentir la simulation
    
    print("\n--- Statut Final ---")
    print(f"État actuel: {feu_de_circulation.obtenir_etat_actuel()}")


if __name__ == "__main__":
    main()