from musique import Musique


class Bibliotheque:
    def __init__(self):
        self.morceaux = []

    def ajouter_morceau(self, morceau):
        if isinstance(morceau, Musique):
            self.morceaux.append(morceau)
            print(f"Morceau ajouté: {morceau.titre} par {morceau.artiste}")

    def obtenir_morceaux(self):
        return self.morceaux
