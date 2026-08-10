from clases.salas.tuberias.armario import ArmarioInterfaz
from clases.salas.tuberias.maquinaria import MaquinariaInterfaz
from clases.salas.tuberias.computadoras import PCInterfaz
from clases.salas.tuberias.panel import PanelInterfaz
from clases.salas.tuberias.valvulas import ValvulasInterfaz
from ..sala_base import Sala, Interactuable
import os
import arcade
from configuraciones import Constantes as const

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo_inicio_1 = arcade.load_texture(CURRENT_PATH + "/texturas/fondos/electrificado1.png")

fondo_inicio_2 = arcade.load_texture(CURRENT_PATH + "/texturas/fondos/electrificado2.png")

FACTOR_X = const.ancho_ventana / fondo_inicio_1.width
FACTOR_Y = const.alto_ventana / fondo_inicio_1.height
FACTOR_ESCALAR = min(FACTOR_X, FACTOR_Y)
ancho = fondo_inicio_1.width
alto = fondo_inicio_1.height
#escalamos las texturas de fondo para que se ajusten a la pantalla, manteniendo su proporción original
def escalar_textura(textura):
    textura.width = textura.width * FACTOR_ESCALAR
    textura.height = textura.height * FACTOR_ESCALAR
    return textura

texturas_fondo_inicio = [
    escalar_textura(fondo_inicio_1),
    escalar_textura(fondo_inicio_2)
]

fondo_post_valvulas_1 = arcade.load_texture(CURRENT_PATH + "/texturas/fondos/sin_agua1.png")
fondo_post_valvulas_2 = arcade.load_texture(CURRENT_PATH + "/texturas/fondos/sin_agua2.png")

texturas_post_valvulas = [
    escalar_textura(fondo_post_valvulas_1),
    escalar_textura(fondo_post_valvulas_2)
]

fondo_post_panel_1 = arcade.load_texture(CURRENT_PATH + "/texturas/fondos/no_electrificado1.png")
fondo_post_panel_2 = arcade.load_texture(CURRENT_PATH + "/texturas/fondos/no_electrificado2.png")

texturas_post_panel = [
    escalar_textura(fondo_post_panel_1),
    escalar_textura(fondo_post_panel_2)
]

fondo_post_porton = arcade.load_texture(CURRENT_PATH + "/texturas/fondos/salida.png")

texturas_post_porton = [
    escalar_textura(fondo_post_porton)
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
textura_armario = escalar_textura(arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/armario.png"))
textura_porton = escalar_textura(arcade.load_texture(CURRENT_PATH + "/texturas/interactuables/porton.png"))

def func_valvulas(partida):
    print("Has interactuado con las válvulas.")
    sala = partida.sala
    partida.window.show_view(sala.valvulas)

def func_panel(partida):
    print("Has interactuado con el panel.")
    sala = partida.sala
    partida.window.show_view(sala.panel)

def func_comp_der(partida):
    print("Has interactuado con la computadora der")
    sala = partida.sala
    partida.window.show_view(sala.pc_der)

def func_comp_izq(partida):
    print("Has interactuado con la computadora izq")
    sala = partida.sala
    partida.window.show_view(sala.pc_izq)

def func_maquinaria(partida):
    print("Has interactuado con la maqinaria")
    sala = partida.sala
    partida.window.show_view(sala.maquinaria)

def func_armario(partida):
    print("has interactuado con el armario")
    sala = partida.sala
    partida.window.show_view(sala.armario)

def func_porton(partida):
    partida.sala.PortonAbierto()

interactuables = [
    {
        "nombre": "valvulas",
        "textura": textura_valvulas,
        "x": 570 * FACTOR_ESCALAR,
        "y": 470 * FACTOR_ESCALAR,
        "funcion": func_valvulas,
        "ubicacion_jugador": (0,- 20),
    },
    {
        "nombre": "panel",
        "textura": textura_panel,
        "x": 60 * FACTOR_ESCALAR,
        "y": 145 * FACTOR_ESCALAR,
        "funcion": func_panel,
        "ubicacion_jugador": (10, 0),
    },
    {
        "nombre": "computadora_der",
        "textura": textura_computadora,
        "x": 165 * FACTOR_ESCALAR,
        "y": 70 * FACTOR_ESCALAR,
        "funcion": func_comp_der,
        "ubicacion_jugador": (0, 5),
    },
    {
        "nombre": "computadora_izq",
        "textura": textura_computadora,
        "x": 425 * FACTOR_ESCALAR,
        "y": 70 * FACTOR_ESCALAR,
        "funcion": func_comp_izq,
        "ubicacion_jugador": (0, 5),
    },
    {
        "nombre": "armario",
        "textura": textura_armario,
        "x": 784.5 * FACTOR_ESCALAR,
        "y": 250 * FACTOR_ESCALAR,
        "funcion": func_armario,
        "ubicacion_jugador": (-10, 0),
    },
    {
        "nombre": "maquinaria",
        "textura": textura_maquinaria,
        "x": 700 * FACTOR_ESCALAR,
        "y": 120 * FACTOR_ESCALAR,
        "funcion": func_maquinaria,
        "ubicacion_jugador": (0, 5),
    },
    {
        "nombre": "porton",
        "textura": textura_porton,
        "x": 120 * FACTOR_ESCALAR,
        "y": 360 * FACTOR_ESCALAR,
        "funcion": func_porton,
        "ubicacion_jugador": (0, -5),
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
    "x": 120 * FACTOR_ESCALAR,
    "y": 475 * FACTOR_ESCALAR,
    "ancho": 100 * FACTOR_ESCALAR,
    "alto": 100 * FACTOR_ESCALAR,
    "funcion": lambda: print("saliendo de la sala de tuberías")
}


class Sala_Tuberias(Sala):
    
    def __init__(self):
        super().__init__()
        super().Fondo(texturas_fondo_inicio)
        super().Colisiones(paredes)
        super().Interactuables(interactuables)
        super().Salida(salida["x"], salida["y"], salida["ancho"], salida["alto"], salida["funcion"])
        super().Eliminadores(eliminadores)
        self.texto_inicial = '"ya no puedo llegar a la puerta, el agua hizo contacto con los cables rotos..."'
        self.posicion_inicial = (const.ancho_ventana / 2, const.alto_ventana / 2)

    def InstanciarInterfaces(self, partida):
        #instanciar los objetos de las interfaces
        self.armario = ArmarioInterfaz(partida)
        self.maquinaria = MaquinariaInterfaz(partida)
        self.pc_izq = PCInterfaz(partida, "izq")     
        self.pc_der = PCInterfaz(partida, "der")  
        self.panel = PanelInterfaz(partida)   
        self.valvulas = ValvulasInterfaz(partida)
    
    def ValvulasResuelto(self):
        self.lista_eliminadores.pop(-1)
        super().Fondo(texturas_post_valvulas)
    
    def PanelResuelto(self):
        self.lista_eliminadores.pop(-1)
        super().Fondo(texturas_post_panel)
    
    def PortonAbierto(self):
        for objeto in self.lista_bloqueos:
            if isinstance(objeto, Interactuable) and objeto.nombre == "porton":
                self.lista_bloqueos.remove(objeto)
        super().Fondo(texturas_post_porton)

    def VerificarDerrota(self, jugador):
        if arcade.check_for_collision_with_list(jugador, self.lista_eliminadores):
            return (True, "El agua te alcanzó y te electrocutaste. ¡Has perdido!")

        tiempo_resultado = super().VerificarDerrota(jugador)
        if tiempo_resultado:
            return tiempo_resultado
        