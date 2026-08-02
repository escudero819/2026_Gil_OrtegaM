"""
CLASE HIJA DE SALA, CONFIGURACIÓN ESPECÍFICA PARA LA SALA DE ALMACÉN
""" 
from ..sala_base import Sala, Interactuable
from configuraciones import Constantes as const
import os
import arcade
from clases.salas.almacen.estanteria1 import Estanteria1Interfaz
from clases.salas.almacen.estanteria2 import Estanteria2Interfaz
from clases.salas.almacen.estanteria3 import Estanteria3Interfaz
from clases.salas.almacen.estanteria4 import Estanteria4Interfaz
from clases.salas.almacen.estanteria5 import Estanteria5Interfaz
# from clases.salas.almacen.montacargas import Montacargas
# from clases.salas.almacen.puerta_almacen import PuertaAlmacen


# Ruta de la carpeta actual
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


# FONDO DE PRUEBAS Y AJUSTE DE PAREDES Y ESCALADO DE TEXTURAS
fondo = arcade.load_texture(CURRENT_PATH + "/texturas/fondos/fondo2.png") 

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

# Texturas de fondo
texturas_fondo = [
    escalar_textura(fondo)
]


# PAREDES DE COLICIONES DE LA SALA DE ALMACÉN

paredes = [
    {
        "nombre": "pared_sur",
        "x": escalar(ancho/2),
        "y": escalar(10),
        "ancho": escalar(ancho),
        "alto": escalar(50)
    },
    {
        "nombre": "pared_norte",
        "x": escalar(ancho/2 + ancho/2 * 0.23),
        "y": escalar(alto - 200),
        "ancho": escalar(ancho/4 * 3.5),
        "alto": escalar(80)
    },
    {
        "nombre": "pared_este",
        "x": escalar(ancho - 10),
        "y": escalar(alto / 2),
        "ancho": escalar(80),
        "alto": escalar(alto)
    },
    {
        "nombre": "pared_oeste",
        "x": escalar(10),
        "y": escalar(alto / 2),
        "ancho": escalar(50),
        "alto": escalar(alto)
    },
    {
        "nombre": "pared_baranda",
        "x": escalar(ancho/4 - 100),
        "y": escalar(alto / 3 * 2 - 200),
        "ancho": escalar(50),
        "alto": escalar(alto / 3 * 2 + 200)
    }
]

# texturas de los interactuables
textura_estanteria_num1 = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/estanteria1.1.png")
textura_estanteria_num2 = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/estanteria2.1.png")
textura_estanteria_num3 = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/estanteria3.1.png")
textura_estanteria_num4 = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/estanteria4.1.png")
textura_estanteria_num5 = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/estanteria5.1.png")
textura_estanteria_num6 = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/estanteria6.1.png")
textura_montacargas = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/montacargas.png")

# funciones de los interactuables (se ejecutan cuando llega a la ubicacion definida en el interactuable)
def func_estanteria_num1(partida):
    print("interactuando con estanteria 1")
    # proximamente: abrir pantalla emergente con informacion de la estanteria 1
    sala = partida.sala
    partida.window.show_view(sala.estanteria1_interfaz)

def func_estanteria_num2(partida):
    print("interactuando con estanteria 2")
    # proximamente: abrir pantalla emergente con informacion de la estanteria 2
    sala = partida.sala
    partida.window.show_view(sala.estanteria2_interfaz)

def func_estanteria_num3(partida):
    print("interactuando con estanteria 3")
    # proximamente: abrir pantalla emergente con informacion de la estanteria 3
    sala = partida.sala
    partida.window.show_view(sala.estanteria3_interfaz)

def func_estanteria_num4(partida):
    print("interactuando con estanteria 4")
    # proximamente: abrir pantalla emergente con informacion de la estanteria 4
    sala = partida.sala
    partida.window.show_view(sala.estanteria4_interfaz)

def func_estanteria_num5(partida):
    print("interactuando con estanteria 5")
    # proximamente: abrir pantalla emergente con informacion de la estanteria 5
    sala = partida.sala
    partida.window.show_view(sala.estanteria5_interfaz)

def func_montacargas(partida):
    print("interactuando con montacargas")
    # proximamente: abrir pantalla emergente con informacion del montacargas
    sala = partida.sala
    partida.window.show_view(sala.montacargas_interfaz)

# lista de interactuables de la sala de almacen, ubicacion, ubicacion del jugador y funcion a ejecutar

ubi_x_1 = escalar(ancho/2)
ubi_x_2 = ubi_x_1 + textura_estanteria_num1.width/2 + textura_estanteria_num2.width/2
ubi_x_3 = ubi_x_2 + textura_estanteria_num2.width/2 + textura_estanteria_num3.width/2
ubi_y_1 = escalar(1550)
ubi_y_3 = escalar(alto/2)
interactuables = [
    {
        "nombre": "estanteria_num1",
        "textura": textura_estanteria_num1,
        "x": ubi_x_1,
        "y": ubi_y_1,
        "funcion": func_estanteria_num1,
        "ubicacion_jugador": (0, escalar(-50))
    },
    {
        "nombre": "estanteria_num2",
        "textura": textura_estanteria_num2,
        "x": ubi_x_2,
        "y": ubi_y_1,
        "funcion": func_estanteria_num2,
        "ubicacion_jugador": (0, escalar(-50))
    },
    {
        "nombre": "estanteria_num3",
        "textura": textura_estanteria_num3,
        "x": ubi_x_3,
        "y": ubi_y_1,
        "funcion": func_estanteria_num3,
        "ubicacion_jugador": (0, escalar(-50))
    },
    {
        "nombre": "estanteria_num4",
        "textura": textura_estanteria_num4,
        "x": ubi_x_1,
        "y": ubi_y_3,
        "funcion": func_estanteria_num4,
        "ubicacion_jugador": (0, escalar(-50))
    },
    {
        "nombre": "estanteria_num5",
        "textura": textura_estanteria_num5,
        "x": ubi_x_3,
        "y": ubi_y_3,
        "funcion": func_estanteria_num5,
        "ubicacion_jugador": (0, escalar(-50))
    },
    {
        "nombre": "montacargas",
        "textura": textura_montacargas,
        "x": escalar(ancho/2 + 250),
        "y": escalar(350),
        "funcion": func_montacargas,
        "ubicacion_jugador": (escalar(-50), 0)
    }
]

class Sala_Almacen(Sala):
    def __init__(self):
        super().__init__()
        super().Fondo(texturas_fondo)
        super().Colisiones(paredes)
        super().Interactuables(interactuables)
        #super().Salida(salida["x"], salida["y"], salida["ancho"], salida["alto"], salida["funcion"])
        #super().Eliminadores(eliminadores)
        self.texto_inicial = '"entre al almacen"'
        self.posicion_inicial = (const.ancho_ventana / 2, const.alto_ventana / 2)

    def InstanciarInterfaces(self, partida):
        #instanciar los objetos de las interfaces
        self.estanteria1_interfaz = Estanteria1Interfaz(partida)
        self.estanteria2_interfaz = Estanteria2Interfaz(partida)
        self.estanteria3_interfaz = Estanteria3Interfaz(partida)
        self.estanteria4_interfaz = Estanteria4Interfaz(partida)
        self.estanteria5_interfaz = Estanteria5Interfaz(partida)

    def InstanciarEscaleras(self, partida):
        #instanciar los sprites de las escaleras 
        pass

    # PROXIMAMENTE: hacer las funciones que hagan los cambios de estado de la sala, como abrir puertas, activar maquinaria, etc.