import os
import subprocess

# Diccionario con rutas personalizadas
apps_disponibles = {
    "python": r"C:\Program Files\JetBrains\PyCharm 2024.3.5\bin\pycharm64.exe",
    "clion": r"C:\Program Files\JetBrains\CLion 2025.1\bin\clion64.exe",
    "java": r"C:\Program Files\JetBrains\IntelliJ IDEA 2024.3\bin\idea64.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.exe",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.exe",
    "google": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "code": r"C:\Users\Nicolás\AppData\Local\Programs\Microsoft VS Code\Code.exe",

}

def abrir_aplicacion(nombre_app, hablar):
    for app in apps_disponibles:
        if app in nombre_app:
            ruta = apps_disponibles[app]
            try:
                subprocess.Popen(ruta)
                hablar(f"Abriendo {app}")
            except Exception as e:
                hablar(f"No pude abrir {app}")
                print(e)
            return
    hablar(f"App no encontrada")
