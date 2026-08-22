"""
CLASE DE LA CLASE LECHUGAVIEW
"""
# dependencias
import arcade, os
from clases.salas.hidroponia.plantio import PlantioView
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/lechuga.png")
computadora = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/comp_lech.png")

solucion = {
    "potasio": 4,
    "nitrogeno": 6,
    "fosforo": 2
}

class LechugaView(PlantioView):

    def __init__(self, partida):
        super().__init__(partida, fondo, computadora, "lechuga", solucion)

    def _solucionado(self):
        self.sala.puerta_interfaz.estado["lechuga"] = True

    def _no_solucionado(self):
        self.sala.puerta_interfaz.estado["lechuga"] = False

    def on_update(self, delta_time):
        super().on_update(delta_time)
        self._verificar()
