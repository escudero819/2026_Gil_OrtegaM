"""
CLASE HIJA DE SALA, CONFIGURACIÓN ESPECÍFICA PARA LA SALA DE ALMACÉN
""" 
from ..sala_base import Sala, Interactuable
from configuraciones import Constantes as const
import os
import arcade

# Ruta de la carpeta actual
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


# FONDO DE PRUEBAS Y AJUSTE DE PAREDES Y ESCALADO DE TEXTURAS
fondo = arcade.load_texture(CURRENT_PATH + "/texturas/fondos/fondo_pruebas.png") 

# FACTORES ESCALARES
FACTOR_X = const.ancho_ventana / fondo.width
FACTOR_Y = const.alto_ventana / fondo.height
FACTOR_ESCALAR = min(FACTOR_X, FACTOR_Y)
ancho = fondo.width
alto = fondo.height
correccion_x = (const.ancho_ventana - (ancho * FACTOR_ESCALAR)) / 2
#escalamos las texturas de fondo para que se ajusten a la pantalla, manteniendo su proporción original
def escalar_textura(textura):
    textura.width = textura.width * FACTOR_ESCALAR
    textura.height = textura.height * FACTOR_ESCALAR
    return textura

# Texturas de fondo
texturas_fondo = [
    escalar_textura(fondo)
]



class Sala_Almacen(Sala):
    def __init__(self):
        super().__init__()
        super().Fondo(texturas_fondo)
        #super().Colisiones(paredes)
        #super().Interactuables(interactuables)
        #super().Salida(salida["x"], salida["y"], salida["ancho"], salida["alto"], salida["funcion"])
        #super().Eliminadores(eliminadores)
        self.texto_inicial = '"entre al almacen"'
        self.posicion_inicial = (const.ancho_ventana / 2, const.alto_ventana / 2)

    def InstanciarInterfaces(self, partida):
        #instanciar los objetos de las interfaces
        pass

    # PROXIMAMENTE: hacer las funciones que hagan los cambios de estado de la sala, como abrir puertas, activar maquinaria, etc.