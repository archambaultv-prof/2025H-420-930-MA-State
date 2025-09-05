import time

class FeuDeCirculation:
    """
    Un système de feu de circulation qui cycle à travers différents états.
    """
    
    def __init__(self):
        self.etat_actuel = "ROUGE"
        self.minuteur = 0
        self.duree_rouge = 30
        self.duree_jaune = 5
        self.duree_vert = 25
        
    def obtenir_etat_actuel(self):
        return self.etat_actuel
    
    def obtenir_minuteur(self):
        return self.minuteur
    
    def tic(self):
        """Avancer le minuteur d'une seconde"""
        self.minuteur += 1
        self._verifier_transition_etat()
    
    def _verifier_transition_etat(self):
        """Vérifier si nous devons passer à un nouvel état basé sur le minuteur"""
        if self.etat_actuel == "ROUGE":
            if self.minuteur >= self.duree_rouge:
                self.etat_actuel = "VERT"
                self.minuteur = 0
        elif self.etat_actuel == "VERT":
            if self.minuteur >= self.duree_vert:
                self.etat_actuel = "JAUNE"
                self.minuteur = 0
        elif self.etat_actuel == "JAUNE":
            if self.minuteur >= self.duree_jaune:
                self.etat_actuel = "ROUGE"
                self.minuteur = 0
    
    def demande_pieton(self):
        """Bouton piéton pressé - étendre l'état actuel si possible"""
        if self.etat_actuel == "ROUGE":
            # Étendre le feu rouge de 10 secondes pour les piétons
            if self.minuteur < self.duree_rouge:
                self.duree_rouge += 10
    
    def mode_maintenance(self):
        """Mettre le feu de circulation en mode maintenance (rouge clignotant)"""
        if self.etat_actuel != "MAINTENANCE":
            self.etat_actuel = "MAINTENANCE"
            self.minuteur = 0
    
    def operation_normale(self):
        """Retourner à l'opération normale depuis le mode maintenance"""
        if self.etat_actuel == "MAINTENANCE":
            self.etat_actuel = "ROUGE"
            self.minuteur = 0
    
    def obtenir_affichage_statut(self):
        """Obtenir une chaîne d'affichage du statut"""
        if self.etat_actuel == "ROUGE":
            return f"🔴 ROUGE ({self.duree_rouge - self.minuteur}s restantes)"
        elif self.etat_actuel == "JAUNE":
            return f"🟡 JAUNE ({self.duree_jaune - self.minuteur}s restantes)"
        elif self.etat_actuel == "VERT":
            return f"🟢 VERT ({self.duree_vert - self.minuteur}s restantes)"
        elif self.etat_actuel == "MAINTENANCE":
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