from .personaje import Player
import os

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

animaciones_idle = {
    "derecha": CURRENT_PATH + "/Animaciones/ingeniero/idle/der.png",
    "izquierda": CURRENT_PATH + "/Animaciones/ingeniero/idle/izq.png",
    "arriba":CURRENT_PATH + "/Animaciones/ingeniero/idle/arriba.png",
    "abajo": CURRENT_PATH + "/Animaciones/ingeniero/idle/abajo.png"
}
animaciones_caminando = {
    "derecha": [
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/der/frame_000.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/der/frame_001.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/der/frame_002.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/der/frame_003.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/der/frame_004.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/der/frame_005.png"
    ],
    "izquierda": [
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/izq/frame_000.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/izq/frame_001.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/izq/frame_002.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/izq/frame_003.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/izq/frame_004.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/izq/frame_005.png"
    ],
    "arriba":[
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/arriba/frame_000.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/arriba/frame_001.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/arriba/frame_002.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/arriba/frame_003.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/arriba/frame_004.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/arriba/frame_005.png"
    ],
    "abajo": [
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/abajo/frame_000.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/abajo/frame_001.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/abajo/frame_002.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/abajo/frame_003.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/abajo/frame_004.png",
        CURRENT_PATH + "/Animaciones/ingeniero/caminando/abajo/frame_005.png"
    ]
}

class Ingeniero(Player):

    def __init__(self, center_x, center_y):
        
        super().__init__(animaciones_idle, animaciones_caminando, center_x, center_y)