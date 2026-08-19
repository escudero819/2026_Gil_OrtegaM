"""
CLASE ESCRITORIOVIEW
"""

# dependencias
import arcade, os
from ..interaccion_base import  InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "transparente.png"))
fondo_inicial = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/esc_sin_llave.png")
fondo_llave = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/esc_con_llave.png")
fondo_final = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/esc_final.png")


class EscritorioView(InteraccionBase):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = partida.sala
        self.estado = "inicial"

    def _anotador(self):
        self.anotador = arcade.Sprite(transparente, center_x= self.ancho/3 + self.correccion_x - 25, center_y= self.alto/2 + self.correccion_y)
        self.anotador.width = 100
        self.anotador.height = 100
        self.lista_interaccion.append(self.anotador)

    def _llave(self):
        self.lista_interaccion.clear()
        self.llave = arcade.Sprite(transparente, center_x= self.ancho/3 + self.correccion_x - 55, center_y= self.alto/2 + self.correccion_y - 75)
        self.llave.width = 50
        self.llave.height = 50
        self.lista_interaccion.append(self.llave)

    def on_show_view(self):
        super().on_show_view()

        if self.estado == "inicial":
            self.cambiar_fondo(fondo_inicial)
            self._anotador()

        elif self.estado == "llave":
            self.cambiar_fondo(fondo_llave)
            self._llave()

        elif self.estado == "final":
            self.cambiar_fondo(fondo_final)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

        if self.estado == "inicial": 
            if self.anotador.collides_with_point((x, y)):
                self.estado = "llave"
                self.cambiar_fondo(fondo_llave)
                self._llave()
                self.anotador = None

        elif self.estado == "llave":
            if self.llave.collides_with_point((x, y)):
                self.estado = "final"
                self.cambiar_fondo(fondo_final)
                self.lista_interaccion.clear()
                self.llave = None
                self.anotador = None
                self.sala.inventario.agregar_objeto("llave de quimicos")
        