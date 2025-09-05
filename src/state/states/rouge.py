from .base import Etat

class Rouge(Etat):
    def entree(self) -> None:
        self.ctx.minuteur = 0

    def tic(self) -> None:
        self.ctx.minuteur += 1
        if self.ctx.minuteur >= self.ctx.duree_rouge:
            # Import tardif pour casser la boucle d'import
            from .vert import Vert
            self.ctx.changer_etat(Vert(self.ctx))

    def demande_pieton(self) -> None:
        if self.ctx.minuteur < self.ctx.duree_rouge:
            self.ctx.duree_rouge += 10

    def nom(self) -> str:
        return "ROUGE"

    def affichage(self) -> str:
        restant = max(self.ctx.duree_rouge - self.ctx.minuteur, 0)
        return f"🔴 ROUGE ({restant}s restantes)"
