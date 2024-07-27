from musique import Musique
from lecteur import Lecteur
from bibliothèque import Bibliotheque

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import os
from PIL import Image, ImageTk
import pygame


class MusicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MusicApp")
        self.root.minsize(920, 300)

        pygame.mixer.init()

        self.style = ttk.Style()
        self.style.theme_use("clam")

        list_frame = ttk.Frame(root)
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Liste des morceaux
        self.listbox = tk.Listbox(list_frame, font=("Helvetica", 12))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Frame for controls
        control_frame = ttk.Frame(root)
        control_frame.pack(fill=tk.X)

        # Frame to center buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(expand=True)

        # Charger les icônes pour les boutons
        self.icons = {
            "play": ImageTk.PhotoImage(Image.open("icons/play.png").resize((24, 24))),
            "pause": ImageTk.PhotoImage(Image.open("icons/pause.png").resize((24, 24))),
            "stop": ImageTk.PhotoImage(Image.open("icons/stop.png").resize((24, 24))),
            "next": ImageTk.PhotoImage(Image.open("icons/next.png").resize((24, 24))),
            "prev": ImageTk.PhotoImage(Image.open("icons/prev.png").resize((24, 24))),
            "add": ImageTk.PhotoImage(Image.open("icons/add.png").resize((24, 24)))
        }

        # Boutons avec icônes
        self.btn_ajouter = ttk.Button(button_frame, text=" Ajouter", image=self.icons["add"], compound=tk.LEFT,
                                      command=self.ajouter_morceau)
        self.btn_ajouter.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_jouer = ttk.Button(button_frame, text=" Jouer", image=self.icons["play"], compound=tk.LEFT,
                                    command=self.jouer_morceau)
        self.btn_jouer.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_precedent = ttk.Button(button_frame, text=" Précédent", image=self.icons["prev"], compound=tk.LEFT,
                                        command=self.precedent_morceau)
        self.btn_precedent.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_suivant = ttk.Button(button_frame, text=" Suivant", image=self.icons["next"], compound=tk.LEFT,
                                      command=self.suivant_morceau)
        self.btn_suivant.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_pause = ttk.Button(button_frame, text=" Pause", image=self.icons["pause"], compound=tk.LEFT,
                                    command=self.pause_morceau)
        self.btn_pause.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_arreter = ttk.Button(button_frame, text=" Arrêter", image=self.icons["stop"], compound=tk.LEFT,
                                      command=self.arreter_morceau)
        self.btn_arreter.pack(side=tk.LEFT, padx=5, pady=5)


        self.index_actuel = 0  # Pour suivre l'index de la piste actuelle
        self.charger_morceaux()

    def charger_morceaux(self):
        """Charge les morceaux de la bibliothèque dans la listbox."""
        self.listbox.delete(0, tk.END)
        morceaux = bibliotheque.obtenir_morceaux()
        for morceau in morceaux:
            self.listbox.insert(tk.END, f"{morceau.titre} - {morceau.artiste}")

    def ajouter_morceau(self):
        """Ajoute un morceau à la bibliothèque."""
        fichier = filedialog.askopenfilename(filetypes=[("Fichiers audio", "*.mp3 *.wav *.ogg")])
        if fichier:
            # On utilise le nom de fichier comme titre par défaut et "Artiste inconnu" par défaut
            titre = os.path.basename(fichier)
            morceau = Musique(titre=titre, artiste="Artiste inconnu", chemin_fichier=fichier)
            bibliotheque.ajouter_morceau(morceau)
            self.charger_morceaux()

    def jouer_morceau(self):
        """Joue le morceau sélectionné."""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            morceau = bibliotheque.obtenir_morceaux()[index]
            lecteur.charger_piste(morceau)
            lecteur.jouer()
        else:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un morceau à jouer.")

    @staticmethod
    def arreter_morceau():
        """Arrête la lecture du morceau."""
        lecteur.arreter()

    @staticmethod
    def pause_morceau():
        """Met en pause ou reprend la lecture du morceau."""
        lecteur.pause()

    def suivant_morceau(self):
        """Passe au morceau suivant dans la liste."""
        if self.index_actuel is not None:
            if self.index_actuel + 1 < len(bibliotheque.obtenir_morceaux()):
                self.index_actuel += 1
                morceau = bibliotheque.obtenir_morceaux()[self.index_actuel]
                lecteur.arreter()
                lecteur.charger_piste(morceau)
                lecteur.jouer()
                self.listbox.select_clear(0, tk.END)
                self.listbox.select_set(self.index_actuel)
            else:
                messagebox.showinfo("Fin de la liste", "Vous avez atteint la fin de la liste de lecture.")
        else:
            messagebox.showwarning("Aucune piste en cours", "Aucune piste n'est en cours de lecture.")

    def precedent_morceau(self):
        """Passe au morceau précédent dans la liste."""
        if self.index_actuel is not None:
            if self.index_actuel - 1 >= 0:
                self.index_actuel -= 1
                morceau = bibliotheque.obtenir_morceaux()[self.index_actuel]
                lecteur.arreter()
                lecteur.charger_piste(morceau)
                lecteur.jouer()
                self.listbox.select_clear(0, tk.END)
                self.listbox.select_set(self.index_actuel)
            else:
                messagebox.showinfo("Début de la liste", "Vous êtes au début de la liste de lecture.")
        else:
            messagebox.showwarning("Aucune piste en cours", "Aucune piste n'est en cours de lecture.")


if __name__ == "__main__":
    bibliotheque = Bibliotheque()
    lecteur = Lecteur()

    root = tk.Tk()
    app = MusicApp(root)
    root.mainloop()
