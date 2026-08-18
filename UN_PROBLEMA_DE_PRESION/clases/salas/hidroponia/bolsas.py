"""
CLASE DE LA CLASE PUERTAVIEW
"""
# dependencias
import arcade, os
from ..interaccion_base import InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/bolsas.png")
transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "semitransparente_rojo.png"))

class BolsasView(InteraccionBase):

    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = partida.sala

        self.bolsa_potasio = None
        self.bolsa_nitrogeno = None
        self.bolsa_fosforo = None

    def _bolsas(self):
        self.bolsa_potasio = arcade.Sprite(transparente, center_x= self.posicion_potasio_x, center_y= self.posicion_potasio_y)
        self.bolsa_potasio.width = 100
        self.bolsa_potasio.height = 100
        self.lista_interaccion.append(self.bolsa_potasio)

        self.bolsa_nitrogeno = arcade.Sprite(transparente, center_x= self.posicion_nitrogeno_x, center_y= self.posicion_nitrogeno_y)
        self.bolsa_nitrogeno.width = 100
        self.bolsa_nitrogeno.height = 100
        self.lista_interaccion.append(self.bolsa_nitrogeno)

        self.bolsa_fosforo = arcade.Sprite(transparente, center_x= self.posicion_fosforo_x, center_y= self.posicion_fosforo_y)
        self.bolsa_fosforo.width = 100
        self.bolsa_fosforo.height = 100
        self.lista_interaccion.append(self.bolsa_fosforo)

    def agregar_potasio(self):
        self.sala.inventario.agregar_objeto("potasio")
        if not self.texto_potasio:
            self.ejecutar_dialogo("agarraste un poco de potasio")
            self.texto_potasio = True   

    def agregar_nitrogeno(self):
        self.sala.inventario.agregar_objeto("nitrogeno")
        if not self.texto_nitrogeno:
            self.ejecutar_dialogo("agarraste un poco de nitrogeno")
            self.texto_nitrogeno = True   

    def agregar_fosforo(self):
        self.sala.inventario.agregar_objeto("fosforo")
        if not self.texto_fosforo:
            self.ejecutar_dialogo("agarraste un poco de fosforo")
            self.texto_fosforo = True   

    def on_show_view(self):
        super().on_show_view()
        self.cambiar_fondo(fondo)
        self.posicion_potasio_x = self.ancho/2 + self.correccion_x + 35
        self.posicion_potasio_y = self.alto/6*5 + self.correccion_y - 70

        self.posicion_nitrogeno_x = self.ancho/4 + self.correccion_x - 30
        self.posicion_nitrogeno_y = self.alto/6*2.5 + self.correccion_y + 30

        self.posicion_fosforo_x = self.ancho/4*3 + self.correccion_x - 35
        self.posicion_fosforo_y = self.alto/6*1 + self.correccion_y + 25

        self._bolsas()

        self.texto_potasio = False
        self.texto_nitrogeno = False
        self.texto_fosforo = False

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

        if self.bolsa_potasio.collides_with_point((x,y)):
            self.agregar_potasio()

        if self.bolsa_nitrogeno.collides_with_point((x,y)):
            self.agregar_nitrogeno()

        if self.bolsa_fosforo.collides_with_point((x,y)):
            self.agregar_fosforo()
        