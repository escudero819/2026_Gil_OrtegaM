from ..sala_base import Sala
import os
import arcade

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

texturas_fondo = [
    arcade.load_texture(CURRENT_PATH + "/texturas/fondo/fondo1.png"),
    arcade.load_texture(CURRENT_PATH + "/texturas/fondo/fondo2.png")
]
ancho = texturas_fondo[0].width
alto = texturas_fondo[0].height
paredes = [
    {
        "nombre": "pared_norte",
        "x": ancho / 2,
        "y": 200,
        "ancho": ancho,
        "alto": 50
    }
]

interactuables = [
    {
        "nombre": "bloque de prueba",
        "textura": arcade.load_texture(CURRENT_PATH + "/../semitransparente_rojo.png"),
        "x": ancho/2,
        "y": alto/2,
        "ancho": 50,
        "alto": 50,
        "funcion": lambda: print("interaccion")
    }
]

objetos = []

class Sala_Tuberias(Sala):
    
    def __init__(self):
        super().__init__()
        super().Fondo(texturas_fondo)
        super().Colisiones(paredes)
        super().Interactuables(interactuables)
        super().Objetos(objetos)