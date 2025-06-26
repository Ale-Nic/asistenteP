import psutil

def cerrar_aplicacion(nombre_app, hablar):
    nombre_app = nombre_app.lower()
    cerrado = False

    for proc in psutil.process_iter(['name']):
        try:
            nombre_proceso = proc.info['name'].lower()
            if nombre_app in nombre_proceso:
                proc.kill()
                cerrado = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if cerrado:
        hablar(f"He cerrado {nombre_app}")
    else:
        hablar(f"No encontré ninguna aplicación llamada {nombre_app}")
