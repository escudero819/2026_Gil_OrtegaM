from clases.salas.interaccion_base import InteraccionBase
import os, arcade

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/num_tornillos.png")

class Estanteria3Interfaz(InteraccionBase):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = self.partida.sala

    def on_show_view(self):
        super().on_show_view()

        if not self.fondo:
            self.cambiar_fondo(fondo)
        else:
            self.cambiar_fondo(self.fondo)