from ..sala_base import Sala
import os
import arcade

ANCHO = 1280
ALTO = 720

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo1 = arcade.load_texture(CURRENT_PATH + "/texturas/fondos/electrificado1.png")

fondo2 = arcade.load_texture(CURRENT_PATH + "/texturas/fondos/electrificado2.png")

FACTOR_X = ANCHO / fondo1.width
FACTOR_Y = ALTO / fondo1.height
FACTOR_ESCALAR = min(FACTOR_X, FACTOR_Y)
ancho = fondo1.width
alto = fondo1.height
#escalamos las texturas de fondo para que se ajusten a la pantalla, manteniendo su proporción original
def escalar_textura(textura):
    textura.width = textura.width * FACTOR_ESCALAR
    textura.height = textura.height * FACTOR_ESCALAR
    return textura

texturas_fondo = [
    escalar_textura(fondo1),
    escalar_textura(fondo2)
]

paredes = [
    {
        "nombre": "pared_sur",
        "x": ancho / 2 * FACTOR_ESCALAR,
        "y": 10 * FACTOR_ESCALAR,
        "ancho": ancho * FACTOR_ESCALAR,
        "alto": 50 * FACTOR_ESCALAR
    },
    {
        "nombre": "pared_norte",
        "x": ancho / 2 * FACTOR_ESCALAR,
        "y": (alto - alto / 10) * FACTOR_ESCALAR,
        "ancho": ancho * FACTOR_ESCALAR,
        "alto": 50 * FACTOR_ESCALAR
    },
    {
        "nombre": "pared_este",
        "x": (ancho - ancho / 100 * 3) * FACTOR_ESCALAR,
        "y": alto / 2 * FACTOR_ESCALAR,
        "ancho": ancho / 100 * 3 * FACTOR_ESCALAR,
        "alto": alto * FACTOR_ESCALAR
    },
    {
        "nombre": "pared_oeste",
        "x": 20 * FACTOR_ESCALAR,
        "y": alto / 2 * FACTOR_ESCALAR,
        "ancho": ancho / 100 * 5 * FACTOR_ESCALAR,
        "alto": alto * FACTOR_ESCALAR
    },
    {
        "nombre": "pared_lateral_salida",
        "x": ancho / 4 * FACTOR_ESCALAR,
        "y": alto / 5 * 3.75 * FACTOR_ESCALAR,
        "ancho": 20 * FACTOR_ESCALAR,
        "alto": alto / 10 * 4 * FACTOR_ESCALAR
    }
]

textura_valvulas = escalar_textura(arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/valvulas.png"))
textura_computadora = escalar_textura(arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/computadora.png"))
textura_panel = escalar_textura(arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/panel.png"))
textura_maquinaria = escalar_textura(arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/maquinaria.png"))


def func_valvulas():
    print("Has interactuado con las válvulas.")

def func_panel():
    print("Has interactuado con el panel.")

def func_comp1():
    print("Has interactuado con la computadora izq")

def func_comp2():
    print("Has interactuado con la computadora der")

def func_maquinaria():
    print("Has interactuado con la maqinaria")

interactuables = [
    {
        "nombre": "valvulas",
        "textura": textura_valvulas,
        "x": 570 * FACTOR_ESCALAR,
        "y": 470 * FACTOR_ESCALAR,
        "funcion": func_valvulas,
        "ubicacion_jugador": (0, - textura_valvulas.height / 2 - 20),
    },
    {
        "nombre": "panel",
        "textura": textura_panel,
        "x": 60 * FACTOR_ESCALAR,
        "y": 145 * FACTOR_ESCALAR,
        "funcion": func_panel,
        "ubicacion_jugador": (textura_panel.width/2 +10, 0),
    },
    {
        "nombre": "computadora1",
        "textura": textura_computadora,
        "x": 165 * FACTOR_ESCALAR,
        "y": 70 * FACTOR_ESCALAR,
        "funcion": func_comp1,
        "ubicacion_jugador": (0, textura_computadora.height / 2 + 5),
    },
    {
        "nombre": "computadora2",
        "textura": textura_computadora,
        "x": 425 * FACTOR_ESCALAR,
        "y": 70 * FACTOR_ESCALAR,
        "funcion": func_comp2,
        "ubicacion_jugador": (0, textura_computadora.height / 2 + 5),
    },
    {
        "nombre": "maquinaria",
        "textura": textura_maquinaria,
        "x": 700 * FACTOR_ESCALAR,
        "y": 120 * FACTOR_ESCALAR,
        "funcion": func_maquinaria,
        "ubicacion_jugador": (0, textura_maquinaria.height / 2 + 5),
    }
]

agua1 = escalar_textura(arcade.load_texture(CURRENT_PATH + "/texturas/agua1.png")) 
agua2 = escalar_textura(arcade.load_texture(CURRENT_PATH + "/texturas/agua2.png")) 

eliminadores = [
    {
        "imagen": agua1,
        "x": 275 * FACTOR_ESCALAR,
        "y": 310 * FACTOR_ESCALAR
    },
    {
        "imagen": agua2,
        "x": 710 * FACTOR_ESCALAR,
        "y": 240 * FACTOR_ESCALAR
    }
]

salida = {
    "x": 100 * FACTOR_ESCALAR,
    "y": 600 * FACTOR_ESCALAR,
    "ancho": 50 * FACTOR_ESCALAR,
    "alto": 50 * FACTOR_ESCALAR,
    "funcion": lambda: print("saliendo")
}

class Sala_Tuberias(Sala):
    
    def __init__(self):
        super().__init__()
        super().Fondo(texturas_fondo)
        super().Colisiones(paredes)
        super().Interactuables(interactuables)
        super().Salida(salida["x"], salida["y"], salida["ancho"], salida["alto"])
        super().Eliminadores(eliminadores)