"""
CLASE DE LA CLASE COMPUTADORAVIEW (tiene distintos fondo para cada planta)
"""
# dependencias
import arcade, os
from ..interaccion_base import InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "semitransparente_rojo.png"))

class ComputadoraView(InteraccionBase):

    def __init__(self, partida, plantio, fondo, planta):
        super().__init__()
        self.partida = partida
        self.plantio = plantio
        self.fondo = fondo
        self.planta = planta

    def _volver(self):
            self.volver = arcade.Sprite(transparente, center_x= 40 + self.correccion_x, center_y= self.alto - 40 + self.correccion_y)
            self.volver.width = 50
            self.volver.height = 50
            print("volver")
            self.lista_interaccion.append(self.volver)

    def _numeros(self):

        self.num_potasio = arcade.Text(
            text=f"{self.plantio.nutrientes["potasio"]}",
            x= self.ubicacion_numeros_x,
            y= self.ubicacion_potasio_y,
            color=arcade.color.FERN_GREEN,
            font_size=25,
            font_name="Courier New",
            bold=True,
            anchor_x="center",
            anchor_y="center"
        )

        self.num_nitrogeno = arcade.Text(
            text=f"{self.plantio.nutrientes["nitrogeno"]}",
            x= self.ubicacion_numeros_x,
            y= self.ubicacion_nitrogeno_y,
            color=arcade.color.FERN_GREEN,
            font_size=25,
            font_name="Courier New",
            bold=True,
            anchor_x="center",
            anchor_y="center"
        )

        self.num_fosforo = arcade.Text(
            text=f"{self.plantio.nutrientes["fosforo"]}",
            x= self.ubicacion_numeros_x,
            y= self.ubicacion_fosforo_y,
            color=arcade.color.FERN_GREEN,
            font_size=25,
            font_name="Courier New",
            bold=True,
            anchor_x="center",
            anchor_y="center"
        )

    def on_show_view(self):
        super().on_show_view()
        self.cambiar_fondo(self.fondo)
        self._volver()

        if self.planta == "lechuga":
            self.ubicacion_numeros_x = self.ancho/4*2.85 + self.correccion_x
            self.ubicacion_nitrogeno_y = self.alto/6 * 4.15 + self.correccion_y
            self.ubicacion_fosforo_y = self.alto/6 * 3.4 + self.correccion_y
            self.ubicacion_potasio_y = self.alto/6 * 2.65 + self.correccion_y

        if self.planta == "margarita":
            self.ubicacion_numeros_x = self.ancho/4*2.85 + self.correccion_x
            self.ubicacion_nitrogeno_y = self.alto/6 * 4.15 + self.correccion_y
            self.ubicacion_fosforo_y = self.alto/6 * 3.4 + self.correccion_y
            self.ubicacion_potasio_y = self.alto/6 * 2.65 + self.correccion_y

        if self.planta == "lavanda":
            self.ubicacion_numeros_x = self.ancho/4*2.85 + self.correccion_x
            self.ubicacion_nitrogeno_y = self.alto/6 * 4.15 + self.correccion_y
            self.ubicacion_fosforo_y = self.alto/6 * 3.4 + self.correccion_y
            self.ubicacion_potasio_y = self.alto/6 * 2.65 + self.correccion_y

        self._numeros()

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

        if self.volver.collides_with_point((x,y)):
            self.partida.window.show_view(self.plantio)

    def on_draw(self):
        super().on_draw()
        self.num_potasio.draw()
        self.num_nitrogeno.draw()
        self.num_fosforo.draw()