"""
CLASE SALA HIDROPONIA HIJA DE SALA_BASE E INICIALIZACION DE LOS INTERACTUABLES
"""

# --- IMPORTACIONES ---

# dependencias
import os
import arcade
from configuraciones import Constantes as const

# clase padre y clase interactuable
from ..sala_base import Sala, Interactuable
# clases de interactuables
from clases.salas.hidroponia.lavanda import LavandaView
from clases.salas.hidroponia.lechuga import LechugaView
from clases.salas.hidroponia.margarita import MargaritaView
from clases.salas.hidroponia.bolsas import BolsasView
from clases.salas.hidroponia.mesa import MesaView
from clases.salas.hidroponia.puerta_salida import PuertaView

#from clases.salas.hidroponia.puerta_salida import PuertaView
# path actual del archivo
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


# --- CARGA DE IMAGENES ---

# fondo
fondo = arcade.load_texture(CURRENT_PATH + "/texturas/fondos/piso_hidroponia.png")

# interactuables
puerta = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/puerta.png")
margarita = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/margarita.png")
lechuga = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/lechuga.png")
lavanda = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/lavanda.png")
mesa = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/mesa.png")
bolsa = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/bolsa.png")

# --- FUNCIONES AUXILIARES ---

# FACTORES ESCALARES
FACTOR_X = const.ancho_ventana / fondo.width
FACTOR_Y = const.alto_ventana / fondo.height
FACTOR_ESCALAR = min(FACTOR_X, FACTOR_Y)
ancho = fondo.width
alto = fondo.height
#escalamos las texturas de fondo para que se ajusten a la pantalla, manteniendo su proporción original
def escalar_textura(textura):
    textura.width = textura.width * FACTOR_ESCALAR
    textura.height = textura.height * FACTOR_ESCALAR
    return textura

def escalar(valor):
    return valor * FACTOR_ESCALAR

def func_lavanda(partida):
    print("interactuando con plantio de lavanda")
    sala = partida.sala
    partida.window.show_view(sala.lavanda_interfaz)

def func_lechuga(partida):
    print("interactuando con plantio de lechuga")
    sala = partida.sala
    partida.window.show_view(sala.lechuga_interfaz)

def func_margarita(partida):
    print("interactuando con plantio de margarita")
    sala = partida.sala
    partida.window.show_view(sala.margarita_interfaz)

def func_bolsa(partida):
    print("interactuando con las bolsas")
    partida.window.show_view(partida.sala.bolsas_interfaz)

def func_mesa(partida):
    print("interactuando con la mesa")
    sala = partida.sala
    partida.window.show_view(sala.mesa_interfaz)

def func_puerta(partida):
    print("interactuando con la puerta")
    sala = partida.sala
    partida.window.show_view(sala.puerta_interfaz)

# --- PREPARACION DE DATOS ---
# Texturas de fondo
texturas_fondo = [
    escalar_textura(fondo)
]

# paredes de colision
paredes = [
    {
        "nombre": "pared_norte",
        "x": escalar(ancho / 2),
        "y": escalar(alto) - escalar(150),
        "ancho": escalar(ancho),
        "alto": escalar(50)
    },
    {
        "nombre": "pared_sur",
        "x": escalar(ancho / 2),
        "y": escalar(35),
        "ancho": escalar(ancho),
        "alto": escalar(50)
    },
    {
        "nombre": "pared_este",
        "x": escalar(ancho) - escalar(25),
        "y": escalar(alto / 2),
        "ancho": escalar(50),
        "alto": escalar(alto)
    },
    {
        "nombre": "pared_oeste",
        "x": escalar(25),
        "y": escalar(alto / 2),
        "ancho": escalar(50),
        "alto": escalar(alto)
    }
]

interactuables = [
    {
        "nombre": "plantio_lavanda",
        "textura": lavanda,
        "x": escalar(ancho/3 - 100),
        "y": escalar(alto/2 + 100),
        "funcion": func_lavanda,
        "ubicacion_jugador": (0, -10)
    },
    {
        "nombre": "plantio_lechuga",
        "textura": lechuga,
        "x": escalar(ancho/2),
        "y": escalar(alto/2 + 100),
        "funcion": func_lechuga,
        "ubicacion_jugador": (0, -10)
    },
    {
        "nombre": "plantio_margarita",
        "textura": margarita,
        "x": escalar(ancho/3 * 2 + 100),
        "y": escalar(alto/2 + 100),
        "funcion": func_margarita,
        "ubicacion_jugador": (0, -10)
    },
    {
        "nombre": "bolsas",
        "textura": bolsa,
        "x": escalar(ancho/3*2.45),
        "y": escalar(alto/4*1.15),
        "funcion": func_bolsa,
        "ubicacion_jugador": (-10, 0)
    },
    {
        "nombre": "mesa",
        "textura": mesa,
        "x": escalar(275),
        "y": escalar(250),
        "funcion": func_mesa,
        "ubicacion_jugador": (0, -10)
    },
    {
        "nombre": "puerta",
        "textura": puerta,
        "x": escalar(150),
        "y": escalar(alto - 120),
        "funcion": func_puerta,
        "ubicacion_jugador": (0, -10)
    }
]

# --- CLASE SALA HIDROPONIA ---

class Sala_Hidroponia(Sala):

    def __init__(self):
        super().__init__()
        super().Fondo(texturas_fondo)
        super().Colisiones(paredes)
        super().Interactuables(interactuables)
        #super().Salida(salida["x"], salida["y"], salida["ancho"], salida["alto"], salida["funcion"])
        self.posicion_inicial = (const.ancho_ventana / 2, const.alto_ventana / 3)
        self.texto_inicial = "la ultima sala, solo tengo que abrir la puerta y estare a salvo."
        for i in range(10):
            self.inventario.agregar_objeto("nitrogeno")
            self.inventario.agregar_objeto("fosforo")
            self.inventario.agregar_objeto("potasio")

    def InstanciarInterfaces(self, partida):
        self.lavanda_interfaz = LavandaView(partida)
        self.lechuga_interfaz = LechugaView(partida)
        self.margarita_interfaz = MargaritaView(partida)
        self.mesa_interfaz = MesaView(partida)
        self.puerta_interfaz = PuertaView(partida)
        self.bolsas_interfaz = BolsasView(partida)