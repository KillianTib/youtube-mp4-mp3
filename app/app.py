from pathlib import Path
from tkinter import *
from tkinter import filedialog, messagebox
import re

from pytube import YouTube
from fonctions import titre
from settings import COLOR_BG_CADRE, COLOR_BG_FENETRE, COLOR_BG_BOUTONS, COLOR_TEXT_BOUTONS, APP_NAME, URL_TEST

path = str(Path.home() / "Downloads")

#definir là où la vidéo sera enregistrer
def edit_path():
    global path
    new_path = filedialog.askdirectory(initialdir=path)
    if new_path != "":
        path = new_path
        var.set(f"Le fichier sera enregistré dans {path}")

#download 
def download():
    url = saisie.get()

    if url == "":
        messagebox.showwarning("Erreur", "le champ url est requis")
    else:
        # ['mp3', '1080p', '702p']
        quality = varGr.get()
        print(quality)

        yt = YouTube(url)

        print(yt.streams.filter(res=quality))

        stream = yt.streams.filter(res=quality).first()  # on choisie la qualité qui correspond

        extensions = {"1080p": "mp4", "720p": "mp4"}
        title = re.sub(r"[^a-zA-Z0-9]+", ' ', yt.title)
        stream.download(output_path=path, filename=f"{title}{quality}.{extensions[quality]}")

#fenetre
fenetre1 = Tk()
fenetre1.title(APP_NAME)
fenetre1.iconbitmap("assets/YouTube.ico")

fenetre1.config(bg=COLOR_BG_FENETRE)

fenetre1.geometry("650x570")
fenetre1.resizable(width=0, height=0)
f1 = Frame(fenetre1, bd=5)
f1.config(bg="pink")
f1.pack(pady=25, padx=25)

cadre1 = Frame(f1, bd=5)
cadre1.config(bg="green")
cadre1.pack()

cadre2 = Frame(f1, bd=5)
cadre2.config(bg=COLOR_BG_CADRE)
cadre2.pack()

cadre3 = Frame(f1, bd=5)
cadre3.config(bg="blue")
cadre3.pack()

texteTelechargement = Label(
    cadre1, text="Collez le lien de la vidéo puis choisissez le mode de téléchargement")
texteTelechargement.config(bg=COLOR_BG_BOUTONS, fg=COLOR_TEXT_BOUTONS)
texteTelechargement.pack()

maLegende = Label(cadre2, text='URL : ')
maLegende.config(bg=COLOR_BG_BOUTONS, fg=COLOR_TEXT_BOUTONS)
maLegende.pack(padx=5, pady=5, side=LEFT)

saisie = Entry(cadre2)
saisie.pack(padx=5, pady=5)




labelFrameQualities = LabelFrame(cadre3, text="Choisir la qualité", padx=20, pady=20)
labelFrameQualities.pack(fill="both", expand="yes")

vals = ['mp3', '1080p', '702p']
etiqs = ['mp3', '1080p', '702p']
varGr = StringVar()
varGr.set(vals[1])  # default value
for i in range(3):
    b = Radiobutton(labelFrameQualities, variable=varGr, text=etiqs[i], value=vals[i])
    b.pack(side='left', expand=1)

ButtonDownload = Button(cadre3, text="Télécharger !!!", command=download).pack()

var = StringVar()
defaultPath = Label(cadre3, textvariable=var)
defaultPath.config(bg=COLOR_BG_BOUTONS, fg=COLOR_TEXT_BOUTONS)
defaultPath.pack(pady=5)
var.set(f"Le fichier sera enregistré dans {path}")


buttonEditPathFile = Button(cadre3, text="Changer l'emplacement du fichier", command=edit_path,
                            bg=COLOR_BG_BOUTONS, fg="white")
buttonEditPathFile.pack()


"""en dev"""
#name = titre (URL_TEST)
#titre = Label (cadre3, textvariable = name)
#titre.pack()

f1.mainloop()

