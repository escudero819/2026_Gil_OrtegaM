"""
CLASE DE LA CLASE LAVANDAVIEW
"""
# dependencias
import arcade, os
from clases.salas.hidroponia.plantio import PlantioView
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/lavanda.png")
computadora = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/comp_lava.png")


solucion = {
    "potasio": 1,
    "nitrogeno": 2,
    "fosforo": 2,
}

class LavandaView(PlantioView):

    def __init__(self, partida):
        super().__init__(partida, fondo, computadora, "lavanda", solucion)

    def _solucionado(self):
        self.sala.puerta_interfaz.estado["lavanda"] = True

    def _no_solucionado(self):
        self.sala.puerta_interfaz.estado["lavanda"] = False

    def on_update(self, delta_time):
        super().on_update(delta_time)
        self._verificar()

