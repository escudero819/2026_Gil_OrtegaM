"""
CLASE DE LA CLASE COMPUTADORAVIEW (tiene distintos fondo para cada planta)
"""
# dependencias
import arcade, os
from ..interaccion_base import InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "semitransparente_rojo.png"))

class ComputadoraView(InteraccionBase):

    def __init__(self, partida, plantio, fondo):
        super().__init__()
        self.partida = partida
        self.plantio = plantio
        self.fondo = fondo

    def _volver(self):
            self.volver = arcade.Sprite(transparente, center_x= 40 + self.correccion_x, center_y= self.alto - 40 + self.correccion_y)
            self.volver.width = 50
            self.volver.height = 50
            print("volver")
            self.lista_interaccion.append(self.volver)

    def on_show_view(self):
        super().on_show_view()
        self.cambiar_fondo(self.fondo)
        self._volver()

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

        if self.volver.collides_with_point((x,y)):
            self.partida.window.show_view(self.plantio)