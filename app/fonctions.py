import os
from tkinter import messagebox

from pytube import YouTube


def mp3(URL: str) -> str:
    """Fonction de téléchargement de la vidéo en MP3"""

    assert URL != ""

    print(URL)

    yt = YouTube(URL)
    video = yt.streams.filter(only_audio=True).first()

    # download la video
    out_file = video.download(output_path='C:\Bureau\YouTube\Download')

    # sauvgarde la vidéo
    base, ext = os.path.splitext(out_file)
    base = base.replace(" ", "_")
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    return "Conversion to MP3 done"


def mp4(URL: str, directory: str) -> str:
    """Fonction de téléchargement de la vidéo en MP4"""

    assert URL != ""

    print(URL)

    video = YouTube(URL)
    stream = video.streams.get_highest_resolution()

    stream.download(output_path=directory)

    messagebox.showinfo("Pytube", "Téléchargement réussi")
    return "Conversion to MP4 done"
