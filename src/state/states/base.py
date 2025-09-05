# FICHIER : states/base.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..state import FeuDeCirculation

class Etat(ABC):
    """Interface d'état pour le feu de circulation."""
    def __init__(self, ctx: "FeuDeCirculation") -> None:
        self.ctx = ctx  # contexte (le 'lecteur' / feu de circulation)

    def entree(self) -> None:
        """Appelée dès qu’on *entre* dans cet état (ex.: reset du minuteur)."""
        pass

    @abstractmethod
    def tic(self) -> None:
        """Une seconde s’écoule : logique propre à l’état courant."""
        ...

    # Événements optionnels (NOP par défaut)
    def demande_pieton(self) -> None:
        pass

    def operation_normale(self) -> None:
        pass

    @abstractmethod
    def nom(self) -> str:
        ...

    def affichage(self) -> str:
        """Texte pour l’UI; les états concrets peuvent le surcharger."""
        return self.nom()
