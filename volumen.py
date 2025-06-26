from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes
import math

def cambiar_volumen(direccion, hablar):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volumen = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))

    current = volumen.GetMasterVolumeLevelScalar()  # entre 0.0 y 1.0
    step = 0.1  # 10% por paso

    if direccion == "subir":
        nuevo_volumen = min(current + step, 1.0)
        volumen.SetMasterVolumeLevelScalar(nuevo_volumen, None)
        hablar("Subiendo el volumen")
    elif direccion == "bajar":
        nuevo_volumen = max(current - step, 0.0)
        volumen.SetMasterVolumeLevelScalar(nuevo_volumen, None)
        hablar("Bajando el volumen")
