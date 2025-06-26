import pygetwindow as gw
from screeninfo import get_monitors
import pygetwindow as gw

def texto_a_numero(texto):
    numeros = {
        "uno": 1, "dos": 2, "tres": 3,
        "cuatro": 4, "cinco": 5, "seis": 6
    }
    texto = texto.lower().strip()
    if texto.isdigit():
        return int(texto)
    return numeros.get(texto)

def mover_ventana(nombre_ventana, numero_monitor, hablar):
    try:
        numero_monitor = texto_a_numero(numero_monitor)
        if numero_monitor is None:
            hablar("No entendí a qué monitor te refieres")
            return

        numero_monitor -= 1
        monitores = get_monitors()
        if numero_monitor < 0 or numero_monitor >= len(monitores):
            hablar(f"El monitor {numero_monitor + 1} no está disponible")
            return

        ventanas = gw.getWindowsWithTitle(nombre_ventana)
        if not ventanas:
            hablar(f"No encontré una ventana que contenga {nombre_ventana}")
            return

        ventana = ventanas[0]
        monitor = monitores[numero_monitor]

        # Restaurar si está minimizada
        ventana.restore()

        # Posición segura con margen
        ventana.moveTo(monitor.x + 50, monitor.y + 50)
        ventana.activate()
        hablar(f"He movido {nombre_ventana} al monitor {numero_monitor + 1}")
    except Exception as e:
        hablar("Ocurrió un error al mover la ventana")
        print("[ERROR mover_ventana]:", e)


def pantalla_completa(hablar):
    try:
        ventana = gw.getActiveWindow()
        if ventana:
            ventana.maximize()
            hablar("Ventana puesta en pantalla completa")
        else:
            hablar("No hay una ventana activa para maximizar")
    except Exception as e:
        hablar("No pude poner en pantalla completa la ventana")
        print("[ERROR pantalla_completa]:", e)