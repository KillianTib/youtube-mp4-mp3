import io
import urllib.request
from pathlib import Path
from tkinter import *
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk
from pytube import YouTube, exceptions

from settings import COLOR_BG_FENETRE, COLOR_BG_BOUTONS, COLOR_TEXT_BOUTONS, APP_NAME

path = str(Path.home() / "Downloads")


def edit_path():
    """modifie l'emplacement de sauvegarde du fichier"""
    global path
    new_path = filedialog.askdirectory(initialdir=path)
    if new_path != "":
        path = new_path
        stringVarPath.set(f"Le fichier sera enregistré dans {path}")


def update_preview(*args, **kwargs):
    """ fonction appelée lors de la modification du champ d'entré """
    # global label_thumbnail  # necessaire pour afficher l'image

    url = saisieVar.get()

    # on vérifie si le string dans le champ correspond a l'url du video yt
    try:
        yt = YouTube(url)
        # on essaye de recup le titre car l'objet youtube ne leve pas d'erreur
        # si l'url resssemble a un url yt alors que le lien est faux
        title = yt.title
        thumbnail_url = yt.thumbnail_url.replace("sddefault", "mqdefault")

    except (exceptions.RegexMatchError, exceptions.VideoUnavailable):
        # si l'url n'exite pas on desactive le bouton
        # et on supprime les anciennes propositions de telechargement
        ButtonDownload['state'] = "disable"
        for widget in labelFrameQualities.winfo_children():
            widget.destroy()
        return

    # on active le bouton "telecharger"
    ButtonDownload['state'] = "normal"
    print(f"url valide video : {title}, {thumbnail_url}")

    stringVarVideoTitle.set(title)
    stringVarVideoChannel.set(yt.author)

    raw_data = urllib.request.urlopen(thumbnail_url).read()
    new_thumbnail = ImageTk.PhotoImage(Image.open(io.BytesIO(raw_data)))

    label_thumbnail.configure(image=new_thumbnail)
    label_thumbnail.image = new_thumbnail

    # on creer les choix de qualité
    varRadioButton.set(0)  # default value
    for i in yt.streams.filter(adaptive=True):
        if i.mime_type == "audio/webm":
            b = Radiobutton(labelFrameQualities, variable=varRadioButton,
                            text=f"{i.type} {i.abr}", value=i.itag)
            b.pack(side='left', expand=1)
        if i.mime_type == "video/webm":
            b = Radiobutton(labelFrameQualities, variable=varRadioButton, text=f"{i.type} {i.resolution} {i.fps}fps",
                            value=i.itag)
            b.pack(side='left', expand=1)


def download():
    """ fonction appelée lors du click sur le bouton telecharger """
    url = saisie.get()

    if url == "":
        messagebox.showwarning("Erreur", "le champ url est requis")
    else:
        itag = varRadioButton.get()

        yt = YouTube(url)
        stream = yt.streams.get_by_itag(itag)

        extensions = {"video": "mp4", "audio": "mp3"}
        # on supprime les caractere speciaux
        title = re.sub(r"[^a-zA-Z0-9]+", '_', yt.title)
        stream.download(output_path=path,
                        filename=f"{title}_{stream.resolution if stream.abr is None else stream.abr}\
                                    .{extensions[stream.type]}")
        messagebox.showinfo(APP_NAME, "Téléchargement en réussi")


fenetre = Tk()
fenetre.title(APP_NAME)
# fenetre.geometry("650x300")
fenetre.iconbitmap("assets/YouTube.ico")
fenetre.resizable(width=0, height=0)
fenetre.config(bg=COLOR_BG_FENETRE)

texteTelechargement = Label(
    fenetre, text="Collez le lien de la vidéo puis choisissez le mode de téléchargement")
texteTelechargement.config(bg=COLOR_BG_BOUTONS, fg=COLOR_TEXT_BOUTONS)
texteTelechargement.pack()

maLegende = Label(fenetre, text='URL : ')
maLegende.config(bg=COLOR_BG_BOUTONS, fg=COLOR_TEXT_BOUTONS)
maLegende.pack(padx=5, pady=5)

saisieVar = StringVar()
saisie = Entry(fenetre, textvariable=saisieVar)
saisieVar.trace("w", update_preview)
saisie.pack(padx=5, pady=5)

frameVideoInfo = Frame(fenetre)
frameVideoInfo.pack()

thumbnail = ImageTk.PhotoImage(file="assets/nyan-cat.gif")
label_thumbnail = Label(frameVideoInfo, image=thumbnail)
label_thumbnail.grid(row=0, column=0, rowspan=6)

stringVarVideoTitle = StringVar()
labelVideoTitle = Label(frameVideoInfo, textvariable=stringVarVideoTitle, font=("Arial Black", 16))
labelVideoTitle.grid(row=0, column=1, sticky="w")
stringVarVideoTitle.set("selectionner un url valide")

stringVarVideoChannel = StringVar()
labelVideoChannel = Label(frameVideoInfo, textvariable=stringVarVideoChannel)
labelVideoChannel.grid(row=1, column=1, sticky="w")
stringVarVideoChannel.set("le vide")

labelFrameQualities = LabelFrame(
    fenetre, text="Choisir la qualité", padx=20, pady=20)
labelFrameQualities.pack(fill="both", expand="yes")

varRadioButton = StringVar()

ButtonDownload = Button(fenetre, text="Télécharger !!!",
                        state="disable", command=download)
ButtonDownload.pack()

stringVarPath = StringVar()
labelSavePath = Label(fenetre, textvariable=stringVarPath)
labelSavePath.config(bg=COLOR_BG_BOUTONS, fg=COLOR_TEXT_BOUTONS)
labelSavePath.pack(pady=5)
stringVarPath.set(f"Le fichier sera enregistré dans {path}")

buttonEditPathFile = Button(fenetre, text="Changer l'emplacement du fichier", command=edit_path,
                            bg=COLOR_BG_BOUTONS, fg="white")
buttonEditPathFile.pack()

fenetre.mainloop()
