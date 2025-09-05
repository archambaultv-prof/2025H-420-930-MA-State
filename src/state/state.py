import time
from .states.base import Etat
from .states.rouge import Rouge
from .states.jaune import Jaune  # (utile si pour typer ailleurs)
from .states.vert import Vert
from .states.maintenance import Maintenance

class FeuDeCirculation:
    """
    Contexte du patron State : délègue son comportement à l'état courant.
    """

    def __init__(self):
        # Config “métier”
        self.duree_rouge = 30
        self.duree_jaune = 5
        self.duree_vert = 25

        # État interne partagé par les états
        self.minuteur = 0

        # État initial
        self.etat: Etat = Rouge(self)
        self.etat.entree()

    # ─── API publique inchangée ─────────────────────────────────────────────────
    def obtenir_etat_actuel(self) -> str:
        return self.etat.nom()

    def obtenir_minuteur(self) -> int:
        return self.minuteur

    def tic(self) -> None:
        self.etat.tic()

    def demande_pieton(self) -> None:
        self.etat.demande_pieton()

    def mode_maintenance(self) -> None:
        # Passage immédiat en maintenance (peu importe l'état courant)
        if not isinstance(self.etat, Maintenance):
            self.changer_etat(Maintenance(self))

    def operation_normale(self) -> None:
        # Seul l'état Maintenance réagit; les autres ignorent.
        self.etat.operation_normale()

    def obtenir_affichage_statut(self) -> str:
        return self.etat.affichage()

    # ─── Hook interne pour changer d’état ────────────────────────────────────────
    def changer_etat(self, nouvel_etat: Etat) -> None:
        self.etat = nouvel_etat
        self.etat.entree()

# ────────────────────────────────────────────────────────────────────────────────
# Démo (inchangée)
def main():
    print("Système de Feu de Circulation")
    print("=" * 75)

    feu = FeuDeCirculation()

    print("\n--- Simulation d'Opération Normale ---")
    for seconde in range(90):  # 90 secondes
        print(f"Temps: {seconde:2d}s | {feu.obtenir_affichage_statut()}")

        if seconde == 15:
            print("           🚶 Bouton piéton pressé!")
            feu.demande_pieton()

        if seconde == 75:
            print("           🔧 Entrée en mode maintenance!")
            feu.mode_maintenance()

        if seconde == 85:
            print("           ✅ Retour à l'opération normale!")
            feu.operation_normale()

        feu.tic()
        time.sleep(0.1)

    print("\n--- Statut Final ---")
    print(f"État actuel: {feu.obtenir_etat_actuel()}")

if __name__ == "__main__":
    main()
