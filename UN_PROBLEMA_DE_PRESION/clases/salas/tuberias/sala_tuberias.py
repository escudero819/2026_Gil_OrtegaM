from ..sala_base import Sala
import os
import arcade

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo1 = arcade.load_texture(CURRENT_PATH + "/texturas/fondo/fondo1.png")
fondo1.height = 720
fondo1.width = 1280

fondo2 = arcade.load_texture(CURRENT_PATH + "/texturas/fondo/fondo2.png")
fondo2.height = 720
fondo2.width = 1280

texturas_fondo = [
    fondo1,
    fondo2
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
        "x": ancho / 2,
        "y": alto / 10 * 9.5,
        "ancho": ancho,
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
        "ancho": 80,
        "alto": alto
    },
    {
        "nombre": "pared_lateral_salida",
        "x": ancho / 4,
        "y": alto / 5 * 3.75,
        "ancho": 20,
        "alto": 300
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

        #proximamente
        """super().Interactuables(interactuables)
        super().Objetos(objetos)"""