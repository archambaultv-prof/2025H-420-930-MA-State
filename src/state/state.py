import time
from abc import ABC, abstractmethod

# Classe abstraite pour les états du feu
class EtatFeu(ABC):
    @abstractmethod
    def verifier_transition(self, feu):
        pass

    @abstractmethod
    def obtenir_affichage_statut(self, feu):
        pass

    @abstractmethod
    def obtenir_nom(self):
        pass

    def demande_pieton(self, feu):
        pass

    def mode_maintenance(self, feu):
        pass

    def operation_normale(self, feu):
        pass

# État rouge du feu
class EtatRouge(EtatFeu):
    def obtenir_nom(self):
        return "ROUGE"
    
    def verifier_transition(self, feu):
        if feu.minuteur >= feu.duree_rouge:
            feu.set_etat(EtatVert())

    def obtenir_affichage_statut(self, feu):
        return f"🔴 ROUGE ({feu.duree_rouge - feu.minuteur}s restantes)"

    def demande_pieton(self, feu):
        # Étendre le feu rouge de 10 secondes pour les piétons
        if feu.minuteur < feu.duree_rouge:
            feu.duree_rouge += 10

    def mode_maintenance(self, feu):
        feu.set_etat(EtatMaintenance())

# État vert du feu
class EtatVert(EtatFeu):
    def obtenir_nom(self):
        return "VERT"
    
    def verifier_transition(self, feu):
        if feu.minuteur >= feu.duree_vert:
            feu.set_etat(EtatJaune())            

    def obtenir_affichage_statut(self, feu):
        return f"🟢 VERT ({feu.duree_vert - feu.minuteur}s restantes)"

    def mode_maintenance(self, feu):
        feu.set_etat(EtatMaintenance())

# État jaune du feu
class EtatJaune(EtatFeu):
    def obtenir_nom(self):
        return "JAUNE"
    def verifier_transition(self, feu):
        if feu.minuteur >= feu.duree_jaune:
            feu.set_etat(EtatRouge())

    def obtenir_affichage_statut(self, feu):
        return f"🟡 JAUNE ({feu.duree_jaune - feu.minuteur}s restantes)"

    def mode_maintenance(self, feu):
        feu.set_etat(EtatMaintenance())

# État maintenance du feu
class EtatMaintenance(EtatFeu):
    def obtenir_nom(self):
        return "MAINTENANCE"
    def verifier_transition(self, feu):
        pass  

    def obtenir_affichage_statut(self, feu):
        return "🔴 MAINTENANCE (clignotant)"

    def operation_normale(self, feu):
        feu.set_etat(EtatRouge())
class FeuDeCirculation:
    """
    Un système de feu de circulation qui cycle à travers différents états.
    """
    
    def __init__(self):
        self.etat= EtatRouge()
        self.minuteur = 0
        self.duree_rouge = 30
        self.duree_jaune = 5
        self.duree_vert = 25

     # Changer l'état du feu
    def set_etat(self, nouvel_etat):
        self.etat = nouvel_etat
        self.minuteur = 0

    def obtenir_etat_actuel(self):
        return self.etat.obtenir_nom()

    def obtenir_minuteur(self):
        return self.minuteur
    
    def tic(self):
        """Avancer le minuteur d'une seconde"""
        self.minuteur += 1
        self.etat.verifier_transition(self)

    def demande_pieton(self):
        """Bouton piéton pressé - étendre l'état actuel si possible"""
        self.etat.demande_pieton(self)
    
    def mode_maintenance(self):
        """Mettre le feu de circulation en mode maintenance (rouge clignotant)"""
        self.etat.mode_maintenance(self)
    
    def operation_normale(self):
        """Retourner à l'opération normale depuis le mode maintenance"""
        self.etat.operation_normale(self)
    
    def obtenir_affichage_statut(self):
        """Obtenir une chaîne d'affichage du statut"""
        return self.etat.obtenir_affichage_statut(self)


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