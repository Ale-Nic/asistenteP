import speech_recognition as sr  # Biblioteca para convertir voz a texto
import pyttsx3  # Biblioteca para convertir texto a voz
from datetime import datetime
import pywhatkit
import webbrowser
import subprocess
import pyjokes
import time
import keyboard
import pygetwindow as gw
import pyautogui
import os
import pyautogui
from datetime import datetime
import threading
from abrir_apps import abrir_aplicacion
from volumen import cambiar_volumen
from cerrar_apps import cerrar_aplicacion
from mover_ventanas import mover_ventana
from mover_ventanas import pantalla_completa
from Sistema_y_Multimedia import (cambiar_dispositivo_audio,leer_pdf,tomar_nota_por_voz)
from productividad import (crear_recordatorio,abrir_calendario,temporizador,modo_escritura,comando_personalizado,limpieza)



engine = pyttsx3.init()# Inicializa el motor de texto a voz

def hablar(texto):
    engine.say(texto) #prepara lo que se va a decir.
    engine.runAndWait() #reproduce el texto hablado.

def escuchar():
    global modo_espera
    r = sr.Recognizer() #objeto que "entiende" el audio grabado.
    with sr.Microphone() as source: #abre el micrófono.
        print("Escuchando...")
        audio = r.listen(source) #graba tu voz cuando hablas
        try:
            texto = r.recognize_google(audio, language='es-ES') #Envia el audio a los servidores de Google para convertirlo en texto, language='es-ES' indica que hablamos español.

            print(f"Dijiste: {texto}")
            return texto.lower() # convierte todo a minúsculas (para evitar problemas al comparar texto luego).
        except sr.UnknownValueError: #Si el asistente no puede interpretar lo que dijiste, te lo dice y devuelve texto vacío
            if not modo_espera:
                hablar("No entendi lo que dijiste")
            return ""
        except sr.RequestError:
            hablar("No pude conectarme al servicio de reconocimiento")
            return ""

def decir_hora():
    ahora = datetime.now()
    hora_actual = ahora.strftime("%H:%M")
    hablar(f"La hora actual es {hora_actual}")

def buscar_en_google(comando):
    termino = comando.replace('busca', '').strip()
    if termino:
        hablar(f"Buscando {termino} en Google")
        pywhatkit.search(termino)
    else:
        hablar("No entendí qué quieres que busque")

def reproducir_musica_youtube(comando):
    cancion = comando.replace('reproduce', '').strip()
    if cancion:
        hablar(f"Reproduciendo {cancion} en YouTube")
        pywhatkit.playonyt(cancion)
    else:
        hablar("No entendí qué canción quieres escuchar")


def abrir_spotify():
    try:
        subprocess.Popen(["start", "spotify:"], shell=True)
        hablar("Abriendo Spotify y reproduciendo música")
        time.sleep(5)  # Espera a que la app abra
        keyboard.send("space")
    except Exception as e:
        hablar("No pude abrir y reproducir Spotify")
        print(e)

def contar_chiste():
    chiste = pyjokes.get_joke(language="es", category="all")
    hablar(chiste)

def cerrar_ventana_activa():
    try:
        ventana = gw.getActiveWindow()
        if ventana:
            ventana.close()
            hablar("He cerrado la ventana")
        else:
            hablar("No hay ninguna ventana activa para cerrar")
    except Exception as e:
        hablar("No pude cerrar la ventana")
        print(e)
def pausar_reproduccion(hablar):
    try:
        keyboard.send("space")
        hablar("He pausado la reproducción")
    except Exception as e:
        hablar("No pude pausar la reproducción")
        print(e)
def captura_pantalla(hablar):
    try:
        ahora = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo = f"screenshot_{ahora}.png"
        pyautogui.screenshot(archivo)
        hablar("He guardado una captura de pantalla")
        print(f"[INFO] Captura guardada como {archivo}")
    except Exception as e:
        hablar("No pude tomar la captura de pantalla")
        print(e)


def ejecutar_comando(comando):
    if 'hora' in comando:
        decir_hora()
    elif 'busca' in comando:
        buscar_en_google(comando)
    elif 'reproduce' in comando:
        reproducir_musica_youtube(comando)
    elif 'abre spotify' in comando:
        abrir_spotify()
    elif 'chiste' in comando:
        contar_chiste()
    elif 'cierra ventana' in comando or 'cerrar ventana' in comando:
        cerrar_ventana_activa()
    elif 'cierra' in comando or 'cerrar' in comando:
        nombre_app = comando.replace('cierra', '').replace('cerrar', '').strip()
        cerrar_aplicacion(nombre_app, hablar)
    elif 'abrir' in comando:
        nombre_app = comando.replace('abrir', '').strip()
        abrir_aplicacion(nombre_app, hablar)
    elif 'sube el volumen' in comando or 'subir volumen' in comando:
        cambiar_volumen("subir",hablar)
    elif 'baja el volumen' in comando or 'bajar volumen' in comando:
        cambiar_volumen("bajar",hablar)
    elif 'mueve' in comando or 'mover' in comando:
        if 'al monitor' in comando:
            partes = comando.split('al monitor')
            if len(partes) == 2:
                nombre_app = partes[0].replace('mueve', '').replace('mover', '').strip()
                num_monitor = partes[1].strip()
                mover_ventana(nombre_app, num_monitor, hablar)
            else:
                hablar("No entendí a qué monitor quieres mover la aplicación")
    elif 'pantalla completa' in comando:
        pantalla_completa(hablar)
    elif 'pausa' in comando:
        pausar_reproduccion(hablar)
    elif 'reanudar' in comando:
        pausar_reproduccion(hablar)
    elif 'captura de pantalla' in comando:
        captura_pantalla(hablar)
    elif 'cambiar salida de audio' in comando:
        cambiar_dispositivo_audio(hablar)
    elif 'lee archivo' in comando or 'leer archivo' in comando:
        leer_pdf(hablar)
    elif 'toma nota' in comando or 'escribe nota' in comando:
        tomar_nota_por_voz(hablar, escuchar)
    elif 'recuérdame' in comando:
        crear_recordatorio(hablar, comando)
    elif 'calendario' in comando:
        abrir_calendario(hablar)
    elif 'temporizador' in comando:
        temporizador(hablar, comando)
    elif 'escribir' in comando:
        modo_escritura(escuchar, hablar)
    elif 'compilar' in comando or 'actualiza' in comando or 'ejecutar' in comando or 'cierra pestaña' in comando or 'nueva pestaña' in comando:
        comando_personalizado(comando, hablar)
    elif 'hacer limpieza' in comando:
        limpieza(hablar)

    else:
        if not modo_espera:
            hablar("No entendí tu orden")


modo_espera = True
escucha_thread = None


def ciclo_escucha():
    """Bucle principal de escucha ejecutado en un hilo."""
    global modo_espera
    while not modo_espera:
        comando = escuchar()
        if comando == "":
            continue

        if 'salir' in comando or 'adios' in comando or 'adiós' in comando or 'termina' in comando:
            hablar("Hasta luego.")
            modo_espera = True
            break

        if 'silencio' in comando:
            modo_espera = True
            hablar("Entrando en modo silencio...")
            break

        if 'habla' in comando:
            modo_espera = False
            hablar("Saliendo del modo silencio...")
            continue

        ejecutar_comando(comando)


def activar_asistente():
    """Activa el asistente y comienza el hilo de escucha."""
    global escucha_thread, modo_espera
    if not modo_espera:
        return  # Ya estaba activo
    modo_espera = False
    hablar("Asistente activado")
    escucha_thread = threading.Thread(target=ciclo_escucha, daemon=True)
    escucha_thread.start()


def desactivar_asistente():
    """Detiene el asistente y vuelve al modo espera."""
    global modo_espera
    if modo_espera:
        return
    modo_espera = True
    hablar("Asistente desactivado")


if __name__ == "__main__":
    hablar("Modo espera. Pulsa F9 para activar el asistente")
    keyboard.add_hotkey('F9', activar_asistente)
    keyboard.add_hotkey('F10', desactivar_asistente)
    keyboard.wait()
