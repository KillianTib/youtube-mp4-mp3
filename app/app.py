from pytube import YouTube
from tkinter import *
import os
from fonctions import mp3, mp4

fenetre = Tk()
fenetre.title("Télécharger une vidéo MP3 / MP4")
fenetre.iconbitmap("assets/YouTube.ico")

fenetre.config(bg = "RED")

fenetre.geometry("640x300")

cadre1 = Frame(fenetre)
cadre1.pack()
cadre1.config(bg="#696969",)

texte1 = Label (cadre1, text = "Collez le lien de la vidéo puis choisissez le mode de téléchargement")
texte1.pack()

defaultPath = Label(cadre1, text="Le fichier sera enregistré dans \"C:\Bureau\YouTube\Download\"")
defaultPath.pack()

saisie = Entry (cadre1)
URL = saisie.get()
saisie.pack()

bouton1 = Button (cadre1, text = "MP4",command = lambda: mp4(saisie.get()))
bouton2 = Button (cadre1, text = "MP3",command = lambda: mp3(saisie.get()))
bouton1.pack()
bouton2.pack()

fenetre.mainloop()

print(f'Lien de la vidéo : {URL}')