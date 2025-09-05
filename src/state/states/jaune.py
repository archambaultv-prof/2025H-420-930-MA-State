
from .base import Etat

class Jaune(Etat):
    def entree(self) -> None:
        self.ctx.minuteur = 0

    def tic(self) -> None:
        self.ctx.minuteur += 1
        if self.ctx.minuteur >= self.ctx.duree_jaune:
            # Import tardif
            from .rouge import Rouge
            self.ctx.changer_etat(Rouge(self.ctx))

    def nom(self) -> str:
        return "JAUNE"

    def affichage(self) -> str:
        restant = max(self.ctx.duree_jaune - self.ctx.minuteur, 0)
        return f"🟡 JAUNE ({restant}s restantes)"
