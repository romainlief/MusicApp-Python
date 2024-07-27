from musique import Musique
import pygame


class Lecteur:
    def __init__(self):
        self.piste_actuelle = None
        self.en_lecture = False
        pygame.mixer.init()

    def charger_piste(self, piste):
        if isinstance(piste, Musique):
            self.piste_actuelle = piste
            print(f"Piste chargée: {piste.titre} par {piste.artiste}")

    def jouer(self):
        if self.piste_actuelle and not self.en_lecture:
            print(f"Lecture de: {self.piste_actuelle.titre}")
            pygame.mixer.music.load(self.piste_actuelle.chemin_fichier)
            pygame.mixer.music.play()
            self.en_lecture = True

    def arreter(self):
        if self.en_lecture:
            print("Arrêt de la lecture")
            pygame.mixer.music.stop()
            self.en_lecture = False

    def pause(self):
        if self.en_lecture:
            print("Pause de la lecture")
            pygame.mixer.music.pause()
            self.en_lecture = False
        else:
            print("Reprise de la lecture")
            pygame.mixer.music.unpause()
            self.en_lecture = True


