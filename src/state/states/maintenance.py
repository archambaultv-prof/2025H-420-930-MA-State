from .base import Etat

class Maintenance(Etat):
    def entree(self) -> None:
        self.ctx.minuteur = 0

    def tic(self) -> None:
        # On “clignote”/attend; pas de transition automatique
        self.ctx.minuteur += 1

    def operation_normale(self) -> None:
        # Import tardif pour éviter tout cycle
        from .rouge import Rouge
        self.ctx.changer_etat(Rouge(self.ctx))

    def nom(self) -> str:
        return "MAINTENANCE"

    def affichage(self) -> str:
        return "🔴 MAINTENANCE (clignotant)"
