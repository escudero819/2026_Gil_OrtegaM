from ..sala_base import Sala
import os
import arcade

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo1 = arcade.load_texture(CURRENT_PATH + "/texturas/fondos/electrificado1.png")


fondo2 = arcade.load_texture(CURRENT_PATH + "/texturas/fondos/electrificado2.png")


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
        "ancho": ancho / 100 * 3,
        "alto": alto
    },
    {
        "nombre": "pared_oeste",
        "x": 20,
        "y": alto / 2,
        "ancho": ancho / 100 * 5,
        "alto": alto
    },
    {
        "nombre": "pared_lateral_salida",
        "x": ancho / 4,
        "y": alto / 5 * 3.75,
        "ancho": 20,
        "alto": alto / 10 * 4
    }
]

textura_valvulas = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/valvulas.png")
def func_valvulas():
    print("Has interactuado con las válvulas. ¡Ahora puedes abrir la puerta de salida!")
interactuables = [
    {
        "nombre": "valvulas",
        "textura": textura_valvulas,
        "x": 570,
        "y": 470,
        "funcion": func_valvulas,
        "ubicacion_jugador": (0, - textura_valvulas.height / 2 - 20),
    }
]

objetos = []

class Sala_Tuberias(Sala):
    
    def __init__(self):
        super().__init__()
        super().Fondo(texturas_fondo)
        super().Colisiones(paredes)
        super().Interactuables(interactuables)

        #proximamente
        #super().Objetos(objetos)