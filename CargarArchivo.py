from tkinter import Tk
from tkinter.filedialog import askopenfilename

def cargarArchivo():
    print ("Cargar archivo de entrada")
    root = Tk()
    root.withdraw()
    root.update()
    root.attributes("-topmost", True)
    pathString = askopenfilename(filetypes=[("Text files","*.lfp")])
    return pathString