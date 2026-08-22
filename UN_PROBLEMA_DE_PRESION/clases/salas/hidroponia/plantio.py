"""
CLASE DE LA CLASE PLANTIOVIEW
"""
# dependencias
import arcade, os
from ..interaccion_base import InteraccionBase
from clases.salas.hidroponia.computadora import ComputadoraView
from clases.salas.hidroponia.toldo import ToldoView
from clases.salas.hidroponia.descartador import DescartadorView
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "semitransparente_rojo.png"))

class PlantioView(InteraccionBase):

    def __init__(self, partida, fondo, computadora, planta, solucion):
        super().__init__()
        self.partida = partida
        self.sala = partida.sala
        self.fondo = fondo
        self.computadora = ComputadoraView(self.partida, self, computadora, planta)
        self.toldo = ToldoView(self.partida, self)
        self.descartador = DescartadorView(self.partida, self)
        self.nutrientes = {
            "potasio": 0,
            "nitrogeno": 0,
            "fosforo": 0
        }
        self.cant_max_nutrientes = 8
        self.solucion = solucion
        self.solucionado = False

    def _computadora(self):
        computadora = arcade.Sprite(transparente, center_x = self.ancho/6 + self.correccion_x, center_y= self.alto/2 + self.correccion_y)
        computadora.width = self.ancho/3
        computadora.height = self.alto
        self.computadora_interaccion = computadora
        self.lista_interaccion.append(computadora)

    def _toldo(self):
        toldo = arcade.Sprite(transparente, center_x= self.ancho/6 * 5 + self.correccion_x, center_y= self.alto/4 * 3 + self.correccion_y)
        toldo.width = self.ancho/3
        toldo.height = self.alto/2
        self.toldo_interaccion = toldo
        self.lista_interaccion.append(toldo)

    def _descartador(self):
        descartador = arcade.Sprite(transparente, center_x= self.ancho/6 * 5 + self.correccion_x, center_y= self.alto/4 * 1 + self.correccion_y)
        descartador.width = self.ancho/3
        descartador.height = self.alto/2
        self.descartador_interaccion = descartador
        self.lista_interaccion.append(descartador)

    def on_show_view(self):
        super().on_show_view()
        self.cambiar_fondo(self.fondo)
        self._computadora()
        self._toldo()
        self._descartador()

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

        if self.computadora_interaccion.collides_with_point((x, y)):
            self.partida.window.show_view(self.computadora)

        if self.toldo_interaccion.collides_with_point((x, y)):
            self.partida.window.show_view(self.toldo)

        if self.descartador_interaccion.collides_with_point((x, y)):
            self.partida.window.show_view(self.descartador)

    def _verificar(self):
        for nutriente in self.nutrientes.keys():
            if self.nutrientes[nutriente] != self.solucion[nutriente]:
                if self.solucionado:
                    self._no_solucionado()
                return
        self._solucionado()

    def _solucionado(self):
        pass

    def _no_solucionado(self):
        pass