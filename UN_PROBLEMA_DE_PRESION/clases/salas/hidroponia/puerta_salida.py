"""
CLASE DE LA CLASE PUERTAVIEW
"""
# dependencias
import arcade, os
from ..interaccion_base import InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/puerta.png")
barra = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/barra.png")
transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "transparente.png"))

class PuertaView(InteraccionBase):

    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = partida.sala
        self.estado = {
            "lechuga": True,
            "margarita": True,
            "lavanda": True
        }
        self.fondo = fondo
        self.lechuga = None
        self.margarita = None
        self.lavanda = None
        self.manija = None


    def _barras(self):
        if not self.estado.get("lechuga"):
            self.lechuga = arcade.Sprite(barra, center_x=self.posicion_barras_x, center_y= self.posicion_lechuga_y)
            self.lista_interaccion.append(self.lechuga)

        if not self.estado.get("margarita"):
            self.margarita = arcade.Sprite(barra, center_x=self.posicion_barras_x, center_y= self.posicion_margarita_y)
            self.lista_interaccion.append(self.margarita)

        if not self.estado.get("lavanda"):
            self.lavanda = arcade.Sprite(barra, center_x=self.posicion_barras_x, center_y= self.posicion_lavanda_y)
            self.lista_interaccion.append(self.lavanda)

    def _manija(self):
        self.manija = arcade.Sprite(transparente, center_x= self.ancho/3*2.40 + self.correccion_x, center_y= self.alto/2 + self.correccion_y)
        self.manija.width = 100
        self.manija.height = 300
        print(self.manija.width, self.manija.height)
        self.lista_interaccion.append(self.manija)

    def on_show_view(self):
        super().on_show_view()
        self.cambiar_fondo(self.fondo)
        self.posicion_lechuga_y = self.alto/6*5.1 + self.correccion_y - 20
        self.posicion_margarita_y = self.alto/6*3 + self.correccion_y
        self.posicion_lavanda_y = self.alto/6*1 + self.correccion_y + 20
        self.posicion_barras_x = self.ancho/4*2.25 + self.correccion_x

        self._barras()
        if not self.lista_interaccion:
            print("manijia")
            self._manija()

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

        if self.manija:
            if self.manija.collides_with_point((x,y)):
                from victoria import VictoriaView
                victoria = VictoriaView()
                self.partida.window.show_view(victoria)