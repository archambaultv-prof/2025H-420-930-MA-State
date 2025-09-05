from abc import ABC, abstractmethod
 
 
class IEtatLampe(ABC):
    @abstractmethod
    def appuyer_bouton(self, lampe):
        ...
 
    @abstractmethod
    def update_minuteur(self, lampe):
        ...
 
    @abstractmethod
    def afficher_etat(self) -> str:
        ...
 
class EtatEteinte(IEtatLampe):
    def afficher_etat(self) -> str:
        return "🌙 eteinte"
 
    def appuyer_bouton(self, lampe: "Lampe"):
        lampe.minuteur = None
        lampe.set_etat(EtatAllumer())
 
    def update_minuteur(self, lampe: "Lampe"):
        if lampe.minuteur is not None and lampe.minuteur <= 0:
            lampe.set_etat(EtatAllumer())
 
class EtatAllumer(IEtatLampe):
    def afficher_etat(self) -> str:
        return "💡 allumee"
 
    def appuyer_bouton(self, lampe: "Lampe"):
        lampe.minuteur = None
        lampe.set_etat(EtatEteinte())
 
    def update_minuteur(self, lampe: "Lampe"):
        if lampe.minuteur is not None and lampe.minuteur <= 0:
            lampe.set_etat(EtatEteinte())
 
class Lampe:
    def __init__(self):
        self.etat: IEtatLampe = EtatEteinte()
        self.minuteur = None
 
    def set_etat(self, etat: IEtatLampe):
        self.etat = etat
 
    def afficher_etat(self):
        return self.etat.afficher_etat()
 
    def tic(self):
        if self.minuteur is not None:
            self.minuteur -= 1
        self.etat.update_minuteur(self)
 
    def regler_minuteur(self, duree):
        self.minuteur = duree
        self.etat.update_minuteur(self)
 
    def appuyer_bouton(self):
        self.etat.appuyer_bouton(self)
 
 
if __name__ == "__main__":
    lampe = Lampe()
    print(lampe.afficher_etat())  # eteinte
    lampe.appuyer_bouton()
    print(lampe.afficher_etat())  # allumee
    lampe.appuyer_bouton()
    print(lampe.afficher_etat())  # eteinte
    print("-----Regler le minuteur-----")
    lampe.regler_minuteur(3)
    for _ in range(3):
        lampe.tic()
        print(f"{lampe.afficher_etat()} ({lampe.minuteur})")  # eteinte, eteinte, allumee
 
#Code de depart :
 
class Lampe:
    def __init__(self):
        self.etat = "eteinte" # "allumee"
        self.minuteur = None
 
    def get_etat(self):
        if self.etat == "eteinte":
            return "🌙 eteinte"
        elif self.etat == "allumee":
            return "💡 allumee"
        else:
            raise ValueError("etat incorrect")
 
    def tic(self):
        if self.minuteur is not None:
            self.minuteur -= 1
        self._verifier_minuteur()
 
    def regler_minuteur(self, duree):
        self.minuteur = duree
        self._verifier_minuteur()
 
    def appuyer_bouton(self):
        self.minuteur = None
        if self.etat == "eteinte":
            self.etat = "allumee"
        elif self.etat == "allumee":
            self.etat = "eteinte"
        else:
            raise ValueError("etat incorrect")
 
 
    def _verifier_minuteur(self):
        if self.minuteur is not None and self.minuteur <= 0:
            if self.etat == "eteinte":
                self.etat = "allumee"
            elif self.etat == "allumee":
                self.etat = "eteinte"
            else:
                raise ValueError("etat incorrect")
 
if __name__ == "__main__":
    lampe = Lampe()
    print(lampe.get_etat())  # eteinte
    lampe.appuyer_bouton()
    print(lampe.get_etat())  # allumee
    lampe.appuyer_bouton()
    print(lampe.get_etat())  # eteinte
    print("-----Regler le minuteur-----")
    lampe.regler_minuteur(3)
    for _ in range(3):
        lampe.tic()
        print(lampe.get_etat())  # eteinte, eteinte, allumee
 