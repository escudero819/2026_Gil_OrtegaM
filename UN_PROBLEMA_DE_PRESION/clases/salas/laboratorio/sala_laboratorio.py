"""
CLASE SALA HIDROPONIA HIJA DE SALA_BASE E INICIALIZACION DE LOS INTERACTUABLES
"""

# --- IMPORTACIONES ---

# dependencias
import os
import arcade
from configuraciones import Constantes as const

# clase padre 
from ..sala_base import Sala

# interfaces
from clases.salas.laboratorio.escritorio import EscritorioView
from clases.salas.laboratorio.mesa_izquierda import DestiladorView
from clases.salas.laboratorio.mesa_derecha import Mesa_QuimicosView
from clases.salas.laboratorio.mesa_central import MedidorView
from clases.salas.laboratorio.estante_elementos import ElementosView
from clases.salas.laboratorio.estante_quimicos import QuimicosView
from clases.salas.laboratorio.puerta_salida import PuertaView

# path actual del archivo
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


# --- CARGA DE IMAGENES ---

fondo = arcade.load_texture(CURRENT_PATH + "/texturas/fondos/lab1.png")
escritorio = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/escritorio.png")
mesa_dest = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/mesa_destilador.png")
mesa_quimicos = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/mesa_quimicos.png")
mesa_quimicos2 = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/mesa_quimicos2.png")
mesa_medidor = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/mesa_medidor.png")
mesa = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/mesa.png")
est_quimicos = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/est_quimicos.png")
est_elementos = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/est_elementos.png")
puerta = arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/puerta.png")

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

def func_mesa_dest(partida):
    print("interactuando con la mesa izq")
    partida.window.show_view(partida.sala.mesa_dest)

def func_mesa_quimicos(partida):
    print("interactuando con la mesa derecha")
    partida.window.show_view(partida.sala.mesa_quimicos)
    
def func_mesa_med(partida):
    print("interactuando con la mesa central")
    partida.window.show_view(partida.sala.mesa_medidor)

def func_escritorio(partida):
    print("interactuando con el escritorio")
    partida.window.show_view(partida.sala.escritorio)

def func_puerta(partida):
    print("interactuando con la puerta")
    partida.window.show_view(partida.sala.puerta)

def func_est_quimicos(partida):
    print("interactuando con el estante de quimicos")
    partida.window.show_view(partida.sala.est_quimicos)

def func_est_elementos(partida):
    print("interactuando con el estante de elementos")
    partida.window.show_view(partida.sala.est_elementos)


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
        "y": escalar(alto) - escalar(200),
        "ancho": escalar(ancho),
        "alto": escalar(20)
    },
    {
        "nombre": "pared_sur",
        "x": escalar(ancho / 2),
        "y": escalar(35),
        "ancho": escalar(ancho),
        "alto": escalar(20)
    },
    {
        "nombre": "pared_este",
        "x": escalar(ancho) - escalar(25),
        "y": escalar(alto / 2),
        "ancho": escalar(20),
        "alto": escalar(alto)
    },
    {
        "nombre": "pared_oeste",
        "x": escalar(25),
        "y": escalar(alto / 2),
        "ancho": escalar(20),
        "alto": escalar(alto)
    }
]

interactuables = [
    {
        "nombre": "escritorio",
        "textura": escritorio,
        "x": escalar(150),
        "y": escalar(250),
        "funcion": func_escritorio,
        "ubicacion_jugador": (0, -10)
    },
    {
        "nombre": "destilador",
        "textura": mesa_dest,
        "x": escalar(ancho/4) - escalar(50),
        "y": escalar(alto/2),
        "funcion": func_mesa_dest,
        "ubicacion_jugador": (10, 0)
    },
    {
        "nombre": "mesa central",
        "textura": mesa_medidor,
        "x": escalar(ancho/2),
        "y": escalar(alto/2) - escalar(50),
        "funcion": func_mesa_med, 
        "ubicacion_jugador": (-10, -0)
    },
    {
        "nombre": "mesa derecha",
        "textura": mesa_quimicos,
        "x": escalar(ancho) - escalar(100),
        "y": escalar(alto/2),
        "funcion": func_mesa_quimicos,
        "ubicacion_jugador": (-10, -0)
    },
    {
        "nombre": "estante quimicos",
        "textura": est_quimicos,
        "x": escalar(ancho/5*4) + escalar(40),
        "y": escalar(alto) - escalar(200),
        "funcion": func_est_quimicos,
        "ubicacion_jugador": (0, -20)
    },
    {
        "nombre": "estante elementos",
        "textura": est_elementos,
        "x": escalar(ancho/4) + escalar(70),
        "y": escalar(alto) - escalar(200),
        "funcion": func_est_elementos,
        "ubicacion_jugador": (0, -20)
    },
    {
        "nombre": "puerta de cristal",
        "textura": puerta,
        "x": escalar(ancho/2) - escalar(85),
        "y": escalar(alto) - escalar(150),
        "funcion": func_puerta,
        "ubicacion_jugador": (0, -10)
    }
]

# --- CLASE SALA LABORATORIO ---

class Sala_Laboratorio(Sala):

    def __init__(self):
        super().__init__()
        super().Fondo(texturas_fondo)
        super().Colisiones(paredes)
        super().Interactuables(interactuables)
        self.posicion_inicial = (const.ancho_ventana / 2, const.alto_ventana / 3)
        self.texto_inicial = "casi se derrumba la escalera... hay que seguir"

    def InstanciarInterfaces(self, partida):
        self.mesa_dest = DestiladorView(partida)
        self.mesa_quimicos = Mesa_QuimicosView(partida)
        self.mesa_medidor = MedidorView(partida)
        self.escritorio = EscritorioView(partida)
        self.puerta = PuertaView(partida)
        self.est_quimicos = QuimicosView(partida)
        self.est_elementos = ElementosView(partida)