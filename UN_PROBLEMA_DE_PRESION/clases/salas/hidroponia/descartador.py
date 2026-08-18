"""
CLASE DE LA CLASE DESCARTADORVIEW
"""
# dependencias
import arcade, os, time
from ..interaccion_base import InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo1 = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/descartador1.png")
fondo2 = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/descartador2.png")
transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "semitransparente_rojo.png"))

class DescartadorView(InteraccionBase):
    def __init__(self, partida, plantio):
        super().__init__()
        self.partida = partida
        self.plantio = plantio
        self.descartando = False
        self.bandera_descartando = None
        self.bandera_parpadeo = None
        self.num_fondo = 0

    def descartar(self):
        for nutriente in self.plantio.nutrientes.keys():
            if self.plantio.nutrientes[nutriente] > 0:
                self.plantio.nutrientes[nutriente] -= 1
        self.descartando = True
        self.bandera_descartando = time.time()
        self.bandera_parpadeo = self.bandera_descartando

    def _descartador(self):
        self.descartar_sprite = arcade.Sprite(transparente, center_x= self.ancho/2 + self.correccion_x, center_y= self.alto/5 + self.correccion_y)
        self.descartar_sprite.width = 100
        self.descartar_sprite.height = 100
        self.lista_interaccion.append(self.descartar_sprite)

    def on_show_view(self):
        super().on_show_view()
        self.cambiar_fondo(fondo1)
        self._descartador()

    def on_update(self, delta_time):
        super().on_update(delta_time)

        if self.bandera_descartando:
            if time.time() - self.bandera_descartando < 2:
                if time.time() - self.bandera_parpadeo < 0.5:
                    if self.num_fondo:
                        self.num_fondo = 0
                        self.cambiar_fondo(fondo1)
                    else:
                        self.num_fondo = 1
                        self.cambiar_fondo(fondo2)
            else:
                self.cambiar_fondo(fondo1)
                self.bandera_descartando = None

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

        if self.descartar_sprite.collides_with_point((x, y)):
            self.descartar()