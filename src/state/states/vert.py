# # FICHIER : states/vert.py
# from .base import Etat
# # from .jaune import Jaune

# class Vert(Etat):
#     def entree(self) -> None:
#         self.ctx.minuteur = 0

#     def tic(self) -> None:
#         self.ctx.minuteur += 1
#         if self.ctx.minuteur >= self.ctx.duree_vert:
#             self.ctx.changer_etat(Jaune(self.ctx))

#     def nom(self) -> str:
#         return "VERT"

#     def affichage(self) -> str:
#         restant = max(self.ctx.duree_vert - self.ctx.minuteur, 0)
#         return f"🟢 VERT ({restant}s restantes)"

from .base import Etat

class Vert(Etat):
    def entree(self) -> None:
        self.ctx.minuteur = 0

    def tic(self) -> None:
        self.ctx.minuteur += 1
        if self.ctx.minuteur >= self.ctx.duree_vert:
            # Import tardif
            from .jaune import Jaune
            self.ctx.changer_etat(Jaune(self.ctx))

    def nom(self) -> str:
        return "VERT"

    def affichage(self) -> str:
        restant = max(self.ctx.duree_vert - self.ctx.minuteur, 0)
        return f"🟢 VERT ({restant}s restantes)"
