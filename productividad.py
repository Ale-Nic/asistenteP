import sched
import time
import threading
from datetime import datetime
import webbrowser
import re
import pyautogui
import keyboard
import shutil
import ctypes
import tempfile
import os


planificador = sched.scheduler(time.time, time.sleep)

def crear_recordatorio(hablar, comando):
    try:
        # Ejemplo de comando: "recuérdame llamar a Juan a las 17:30"
        if "a las" not in comando:
            hablar("Debes decir la hora, por ejemplo: recuérdame comprar pan a las 18:00")
            return

        partes = comando.split("a las")
        mensaje = partes[0].replace("recuérdame", "").strip()
        hora = partes[1].strip()

        hora_obj = datetime.strptime(hora, "%H:%M")
        ahora = datetime.now()
        momento_objetivo = ahora.replace(hour=hora_obj.hour, minute=hora_obj.minute, second=0)

        if momento_objetivo < ahora:
            hablar("La hora indicada ya pasó")
            return

        delay = (momento_objetivo - ahora).total_seconds()

        def tarea():
            hablar(f"Recordatorio: {mensaje}")

        planificador.enter(delay, 1, tarea)
        threading.Thread(target=planificador.run).start()

        hablar(f"Recordatorio guardado para las {hora}")
    except Exception as e:
        hablar("No pude programar el recordatorio")
        print("[ERROR recordatorio]:", e)

def abrir_calendario(hablar):
    try:
        webbrowser.open("https://calendar.google.com")
        hablar("Abriendo tu calendario")
    except Exception as e:
        hablar("No pude abrir el calendario")
        print("[ERROR calendario]:", e)


def temporizador(hablar, comando):
    try:
        # Busca una duración en minutos en el comando (ej. "temporizador de 5 minutos")
        match = re.search(r"(\\d+)", comando)
        if not match:
            hablar("Debes decir el tiempo del temporizador en minutos")
            return

        minutos = int(match.group(1))
        segundos = minutos * 60

        def alerta():
            time.sleep(segundos)
            hablar(f"El temporizador de {minutos} minutos ha terminado")

        threading.Thread(target=alerta).start()
        hablar(f"Temporizador iniciado por {minutos} minutos")
    except Exception as e:
        hablar("No pude iniciar el temporizador")
        print("[ERROR temporizador]:", e)


def modo_escritura(escuchar, hablar):
    hablar("Modo escritura activado. Dicta lo que quieres que escriba. Di 'termina de escribir' para finalizar.")

    texto_final = ""

    while True:
        frase = escuchar()
        if not frase:
            continue

        if "termina de escribir" in frase:
            break

        frase = frase.replace("salto de linea", "\\n")
        texto_final += frase + " "

    texto_final = texto_final.strip()
    texto_final = texto_final.replace("\\n", "\n")

    try:
        pyautogui.write(texto_final, interval=0.05)
        hablar("Texto escrito correctamente")
    except Exception as e:
        hablar("No pude escribir el texto")
        print("[ERROR escritura]:", e)




comandos_personalizados = {
    "compilar": ["ctrl+shift+b"],
    "ejecutar": ["mayus+f10"],
    "actualiza": ["ctrl+r"],
    "cierra pestaña": ["ctrl+w"],
    "nueva pestaña": ["ctrl+t"],
}

def comando_personalizado(comando, hablar):
    try:
        for frase, acciones in comandos_personalizados.items():
            if frase in comando:
                for accion in acciones:
                    keyboard.send(accion)
                    time.sleep(0.2)
                hablar(f"Ejecuté el comando personalizado para: {frase}")
                return
        hablar("No tengo un comando personalizado para eso")
    except Exception as e:
        hablar("No pude ejecutar el comando personalizado")
        print("[ERROR comando personalizado]:", e)


def limpieza(hablar):
    try:
        # 1. Vaciar papelera
        try:
            # SHEmptyRecycleBin (de shell32.dll)
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x0007)
            hablar("He vaciado la papelera de reciclaje")
        except Exception as e:
            hablar("No pude vaciar la papelera")
            print("[ERROR papelera]:", e)

        # 2. Eliminar archivos temporales
        try:
            temp_dir = tempfile.gettempdir()
            for archivo in os.listdir(temp_dir):
                ruta = os.path.join(temp_dir, archivo)
                try:
                    if os.path.isfile(ruta) or os.path.islink(ruta):
                        os.unlink(ruta)
                    elif os.path.isdir(ruta):
                        shutil.rmtree(ruta)
                except Exception:
                    continue  # Ignorar archivos en uso
            hablar("Archivos temporales eliminados")
        except Exception as e:
            hablar("No pude limpiar los archivos temporales")
            print("[ERROR temp]:", e)

    except Exception as e:
        hablar("Ocurrió un error al hacer la limpieza")
        print("[ERROR limpieza_basica]:", e)