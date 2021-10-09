import re
from pathlib import Path
from tkinter import *
from tkinter import filedialog, messagebox

from pytube import YouTube, exceptions

from settings import COLOR_BG_CADRE, COLOR_BG_FENETRE, COLOR_BG_BOUTONS, COLOR_TEXT_BOUTONS, APP_NAME

path = str(Path.home() / "Downloads")


def edit_path():
    global path
    new_path = filedialog.askdirectory(initialdir=path)
    if new_path != "":
        path = new_path
        var.set(f"Le fichier sera enregistré dans {path}")


def update_preview(*args, **kwargs):
    url = saisieVar.get()

    try:
        yt = YouTube(url)
        yt.title
    except (exceptions.RegexMatchError, exceptions.VideoUnavailable):
        ButtonDownload['state'] = "disable"
        for widget in labelFrameQualities.winfo_children():
            widget.destroy()
        return

    ButtonDownload['state'] = "normal"
    print(f"url valide video : {yt.title}")

    varRadioButton.set(0)  # default value
    for i in yt.streams.filter(adaptive=True):
        if i.mime_type == "audio/webm":
            b = Radiobutton(labelFrameQualities, variable=varRadioButton, text=f"{i.type} {i.abr}", value=i.itag)
            b.pack(side='left', expand=1)
        if i.mime_type == "video/webm":
            b = Radiobutton(labelFrameQualities, variable=varRadioButton, text=f"{i.type} {i.resolution} {i.fps}fps",
                            value=i.itag)
            b.pack(side='left', expand=1)


def download():
    url = saisie.get()

    if url == "":
        messagebox.showwarning("Erreur", "le champ url est requis")
    else:
        itag = varRadioButton.get()

        yt = YouTube(url)
        stream = yt.streams.get_by_itag(itag)

        extensions = {"video": "mp4", "audio": "mp3"}
        title = re.sub(r"[^a-zA-Z0-9]+", '_', yt.title)  # on supprime les caractere speciaux
        stream.download(output_path=path,
                        filename=f"{title}_{stream.resolution if stream.abr is None else stream.abr}.{extensions[stream.type]}")
        messagebox.showinfo(APP_NAME, "Téléchargement en réussi")


fenetre1 = Tk()
fenetre1.title(APP_NAME)
# fenetre1.iconbitmap("assets/YouTube.ico")

fenetre1.config(bg=COLOR_BG_FENETRE)

# fenetre1.geometry("650x570")
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

saisieVar = StringVar()
saisie = Entry(cadre2, textvariable=saisieVar)
saisieVar.trace("w", update_preview)
saisie.pack(padx=5, pady=5)

labelFrameQualities = LabelFrame(cadre3, text="Choisir la qualité", padx=20, pady=20)
labelFrameQualities.pack(fill="both", expand="yes")

varRadioButton = StringVar()

ButtonDownload = Button(cadre3, text="Télécharger !!!", state="disable", command=download)
ButtonDownload.pack()

var = StringVar()
defaultPath = Label(cadre3, textvariable=var)
defaultPath.config(bg=COLOR_BG_BOUTONS, fg=COLOR_TEXT_BOUTONS)
defaultPath.pack(pady=5)
var.set(f"Le fichier sera enregistré dans {path}")

buttonEditPathFile = Button(cadre3, text="Changer l'emplacement du fichier", command=edit_path,
                            bg=COLOR_BG_BOUTONS, fg="white")
buttonEditPathFile.pack()

f1.mainloop()
