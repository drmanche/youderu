from pytube import YouTube, Playlist, Search as PSearch
from os.path import dirname, abspath
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter.ttk import Combobox
from pytube.helpers import safe_filename
from subprocess import check_output
from os import listdir
from platform import system as psystem

class YouDeru:
    def __init__(self) -> None:
        self.folDown = dirname(abspath(__file__))
        self.listdir = listdir(self.folDown)

    def linkFilter(self, usearch:str = None) -> list:
        adds:list[YouTube] = []
        usearch:list[str] = list(set(filter(lambda x: x != '', usearch.split('\n'))))
        for i in usearch:
            if not i.startswith('https://'):
                try: adds.append(PSearch(i).results[0])
                except: continue
            elif 'list=' in i and '?v=' not in i:
                try: adds.extend(Playlist(i).videos)
                except: continue
            else:
                try: adds.append(YouTube(i))
                except: continue
        return adds

    def downVidAud(self, youVid:YouTube = None, audioOnly:bool = True) -> None:
        try:
            nameFile = f'[YouDeru] {safe_filename(youVid.title)}.{formatDown.get()}'
            if nameFile not in self.listdir:
                streams = youVid.streams
                VidAud = streams.get_audio_only() if audioOnly else streams.get_highest_resolution()
                VidAud.download(output_path=self.folDown, filename=nameFile)
        except: return

    def selFolder(self) -> str:
        self.folDown = check_output(["zenity", "--file-selection", "--directory", "--title=Seleccionar Carpeta"], text=True).strip() if psystem() == 'Linux' else askdirectory()
        self.listdir = listdir(self.folDown)

    def download(self) -> None:
        formatVidAud = True if formatDown.get() == 'mp3' else False
        for i in self.linkFilter(inpText.get("1.0", "end")): self.downVidAud(i, formatVidAud)
        self.listdir = listdir(self.folDown)

youderu = YouDeru()

root = tk.Tk()
root.title("YouDeru")

# Ajustar el tamaño del input para que ocupe el 50% de la ventana
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1) 

inpText = tk.Text(root, wrap=tk.WORD, width=40, height=4)
inpText.grid(row=0, column=0, padx=0, pady=0, sticky="NSEW", columnspan=3)

butFolder = tk.Button(root, text="Folder", command=youderu.selFolder, font=('arial', 13))
butFolder.grid(row=1, column=0, padx=10, pady=10, sticky="W")

# Crear un Combobox para seleccionar el formato
formatDown = Combobox(root, values=["mp3", "mp4"], width=7, state="readonly", justify="center", font=('arial', 13))
formatDown.set("mp3")
formatDown.grid(row=1, column=1, padx=0, pady=0, sticky="E")

butDown = tk.Button(root, text="Download", command=youderu.download, font=('arial', 13))
butDown.grid(row=1, column=2, padx=10, pady=10, sticky="E")

root.geometry("700x300")
root.resizable(False, False)
root.mainloop()