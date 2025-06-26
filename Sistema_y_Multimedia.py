
import time
import pyttsx3
import subprocess
import PyPDF2
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def cambiar_dispositivo_audio(hablar):
    try:
        comando = 'powershell -Command "Get-AudioDevice -List | Out-GridView -PassThru | Set-AudioDevice"'
        subprocess.run(comando, shell=True)
        hablar("Selecciona el dispositivo de audio en la ventana")
    except Exception as e:
        hablar("No pude cambiar el dispositivo de audio")
        print("[ERROR audio]:", e)


def leer_pdf(hablar):
    try:
        Tk().withdraw()
        archivo = askopenfilename(filetypes=[("Archivos PDF", "*.pdf"), ("Texto", "*.txt")])
        if not archivo:
            hablar("No se seleccionó ningún archivo")
            return

        texto = ""
        if archivo.endswith(".pdf"):
            with open(archivo, 'rb') as f:
                lector = PyPDF2.PdfReader(f)
                for pagina in lector.pages[:3]:
                    texto += pagina.extract_text()
        else:
            with open(archivo, 'r', encoding="utf-8") as f:
                texto = f.read()

        if texto:
            hablar("Leyendo el contenido del archivo")
            engine = pyttsx3.init()
            engine.say(texto)
            engine.runAndWait()
        else:
            hablar("No pude extraer texto del archivo")
    except Exception as e:
        hablar("Ocurrió un error al leer el archivo")
        print("[ERROR leer_archivo]:", e)


def tomar_nota_por_voz(hablar, escuchar):
    try:
        hablar("¿Qué quieres que anote?")
        nota = escuchar()
        if nota:
            nombre_archivo = f"nota_{int(time.time())}.txt"
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write(nota)
            hablar(f"He guardado tu nota en {nombre_archivo}")
        else:
            hablar("No capté lo que dijiste")
    except Exception as e:
        hablar("No pude guardar la nota")
        print("[ERROR nota]:", e)