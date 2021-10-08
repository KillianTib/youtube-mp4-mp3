from pytube import YouTube, streams
from tkinter import *
import os 


def mp3(URL):
    '''télécharge une vidéo en mp3'''
    assert URL != ""
    print(URL)
    yt = YouTube(URL)
    video = yt.streams.filter(only_audio=True).first()
    #download la video
    out_file = video.download(output_path='C:\Bureau\youtube\download')
    #sauvgarde la vidéo
    base, ext = os.path.splitext(out_file)
    base = base.replace(" ","_")
    new_file = base + '.mp3'
    os.rename(out_file,new_file)

    return "conversion done"

def mp4(URL):
    '''prendre une vidéo youtube et la télécharge en mp4'''
    assert URL != ""
    print(URL)
    video = YouTube(URL)
    stream = video.streams.get_highest_resolution()
    stream.download(output_path='C:\Bureau\youtube\download')
    return "conversion done"

#URL = input("url de la vidéo : ")
#print(mp3(URL))


# Création d'une fenêtre avec la classe Tk :
fenetre = Tk()
# Ajout d'un titre à la fenêtre principale :
fenetre.title("Télécharger une vidéo")
# Définir un icone :
fenetre.iconbitmap("YouTube.ico")
# Personnaliser la couleur de l'arrière-plan de la fenêtre principale :
fenetre.config(bg = "RED")
# Définir les dimensions par défaut la fenêtre principale :
fenetre.geometry("640x300")
# Création d'un cadre dans la fenêtre :
cadre1 = Frame(fenetre)
cadre1.pack()
cadre1.config(bg="#696969",)
# Ajout de boutons dans le cadre :
texte1 = Label (cadre1, text = "copier le lien et choisir le mode de téléchargement")
texte1.pack()
saisie = Entry (cadre1)
URL = saisie.get()
saisie.pack()
bouton1 = Button (cadre1, text = "mp4",command = lambda: mp4(saisie.get()))
bouton2 = Button (cadre1, text = "mp3",command = lambda: mp3(saisie.get()))
bouton1.pack()
bouton2.pack()
# Affichage de la fenêtre créée :
fenetre.mainloop()
print(URL)
