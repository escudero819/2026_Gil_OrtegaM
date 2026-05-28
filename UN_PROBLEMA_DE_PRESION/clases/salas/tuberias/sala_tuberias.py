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
        "nombre": "pared_sur",
        "x": ancho / 2,
        "y": 10,
        "ancho": ancho,
        "alto": 50
    },
    {
        "nombre": "pared_norte",
        "x": ancho / 3 * 2 - 10,
        "y": alto - 30,
        "ancho": ancho - 150,
        "alto": 50
    },
    {
        "nombre": "pared_este",
        "x": ancho - 10,
        "y": alto / 2,
        "ancho": 50,
        "alto": alto
    },
    {
        "nombre": "pared_oeste",
        "x": 20,
        "y": alto / 2,
        "ancho": 50,
        "alto": alto
    },
    {
        "nombre": "pared_lateral_salida",
        "x": 205,
        "y": 410,
        "ancho": 10,
        "alto": 200
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