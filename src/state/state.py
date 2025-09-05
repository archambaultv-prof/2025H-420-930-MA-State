import time
from abc import ABC, abstractmethod
from typing import Optional


# interface etat
class Etat(ABC):
    """Interface d'un état du feu de circulation."""

    def __init__(self, ctx: "FeuDeCirculation"):
        self.ctx = ctx
        self._entree_effectuee = False  # pour exécuter on_enter une seule fois

    # Hooks de cycle de vie
    def on_enter(self) -> None:
        """Appelé une fois à l'entrée de l'état."""
        self.ctx.minuteur = 0  # Par defaut : reset du minuteur

    def on_exit(self) -> None:
        """Appelé une fois à la sortie de l'état."""
        pass

    # Tick d'une seconde
    @abstractmethod
    def tic(self) -> None:
        ...

    # Pieton ou maintenance
    def demande_pieton(self) -> None:
        """Bouton piéton pressé (optionnel selon l'état)."""
        pass

    def mode_maintenance(self) -> None:
        self.ctx.changer_etat(Maintenance(self.ctx))

    def operation_normale(self) -> None:
        # Par défaut, ne fait rien (sauf en Maintenance)
        pass

    # Affichage
    @abstractmethod
    def affichage(self) -> str:
        ...

    #  s'assurer que on_enter() a ete appele
    def _ensure_enter(self) -> None:
        if not self._entree_effectuee:
            self.on_enter()
            self._entree_effectuee = True


# maintenant on passe a l'etat concret 
class Rouge(Etat):
    def on_enter(self) -> None:
        super().on_enter()
        # Rien de special pour Rouge

    def tic(self) -> None:
        self._ensure_enter()
        self.ctx.minuteur += 1
        if self.ctx.minuteur >= self.ctx.duree_rouge:
            self.ctx.changer_etat(Vert(self.ctx))

    def demande_pieton(self) -> None:
        # Etendre le rouge de 10s si on n’a pas encore atteint la duree prevue
        if self.ctx.minuteur < self.ctx.duree_rouge:
            self.ctx.duree_rouge += 10

    def affichage(self) -> str:
        restant = max(self.ctx.duree_rouge - self.ctx.minuteur, 0)
        return f"🔴 ROUGE ({restant}s restantes)"


class Vert(Etat):
    def tic(self) -> None:
        self._ensure_enter()
        self.ctx.minuteur += 1
        if self.ctx.minuteur >= self.ctx.duree_vert:
            self.ctx.changer_etat(Jaune(self.ctx))

    def affichage(self) -> str:
        restant = max(self.ctx.duree_vert - self.ctx.minuteur, 0)
        return f"🟢 VERT ({restant}s restantes)"


class Jaune(Etat):
    def tic(self) -> None:
        self._ensure_enter()
        self.ctx.minuteur += 1
        if self.ctx.minuteur >= self.ctx.duree_jaune:
            self.ctx.changer_etat(Rouge(self.ctx))

    def affichage(self) -> str:
        restant = max(self.ctx.duree_jaune - self.ctx.minuteur, 0)
        return f"🟡 JAUNE ({restant}s restantes)"


class Maintenance(Etat):
    def on_enter(self) -> None:
        # En maintenance : on ne compte pas vers une transition auto
        self.ctx.minuteur = 0

    def tic(self) -> None:
        # Clignotement conceptuel : pas de transition automatique
        self._ensure_enter()
        self.ctx.minuteur += 1  # incremente juste pour info

    def operation_normale(self) -> None:
        self.ctx.changer_etat(Rouge(self.ctx))

    def affichage(self) -> str:
        return "🔴 MAINTENANCE (clignotant)"


# --------- Contexte ---------
class FeuDeCirculation:
    """
    Contexte du patron State. Délègue le comportement à l'état courant.
    """

    def __init__(self) -> None:
        # Timers
        self.minuteur: int = 0
        self.duree_rouge: int = 30
        self.duree_jaune: int = 5
        self.duree_vert: int = 25

        # Etat courant
        self._etat: Etat = Rouge(self)

   
    def obtenir_etat_actuel(self) -> str:
        return type(self._etat).__name__.upper()

    def obtenir_minuteur(self) -> int:
        return self.minuteur

    def tic(self) -> None:
        self._etat.tic()

    def demande_pieton(self) -> None:
        self._etat.demande_pieton()

    def mode_maintenance(self) -> None:
        self._etat.mode_maintenance()

    def operation_normale(self) -> None:
        self._etat.operation_normale()

    def obtenir_affichage_statut(self) -> str:
        return self._etat.affichage()

    # Transition d'etat
    def changer_etat(self, nouvel_etat: Etat) -> None:
        # hook de sortie
        if self._etat is not None:
            self._etat.on_exit()
        # switch
        self._etat = nouvel_etat
        

    # tests/demo
    def set_durees(self, rouge: Optional[int] = None, jaune: Optional[int] = None, vert: Optional[int] = None) -> None:
        if rouge is not None:
            self.duree_rouge = rouge
        if jaune is not None:
            self.duree_jaune = jaune
        if vert is not None:
            self.duree_vert = vert


# --------- Demo ---------
def main() -> None:
    print("Système de Feu de Circulation (Patron State)")
    print("=" * 75)

    feu = FeuDeCirculation()

    print("\n--- Simulation d'Opération Normale ---")
    for seconde in range(90):  # Executer pendant 90 secondes
        print(f"Temps: {seconde:2d}s | {feu.obtenir_affichage_statut()}")

        # Événements
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
        time.sleep(0.1)  # Ralentir la simulation

    print("\n--- Statut Final ---")
    print(f"État actuel: {feu.obtenir_etat_actuel()}")
