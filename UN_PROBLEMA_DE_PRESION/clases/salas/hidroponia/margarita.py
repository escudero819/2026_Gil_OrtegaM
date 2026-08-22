"""
CLASE DE LA CLASE MARGARITAVIEW
"""
# dependencias
import arcade, os
from clases.salas.hidroponia.plantio import PlantioView
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/margarita.png")
computadora = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/comp_marg.png")

solucion = {
    "potasio": 1,
    "nitrogeno": 4,
    "fosforo": 5
}

class MargaritaView(PlantioView):

    def __init__(self, partida):
        super().__init__(partida, fondo, computadora, "margarita", solucion)

    def _solucionado(self):
        self.sala.puerta_interfaz.estado["margarita"] = True

    def _no_solucionado(self):
        self.sala.puerta_interfaz.estado["margarita"] = False

    def on_update(self, delta_time):
        super().on_update(delta_time)
        self._verificar()
