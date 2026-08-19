"""
CLASE QUIMICOSVIEW
"""

# dependencias
import arcade, os, time
from ..interaccion_base import  InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "transparente.png"))
fondo_inicial = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/est_cerrado.png")
fondo_abierto = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/est_abierto.png")
fondo_final = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/est_revisado.png")

class QuimicosView(InteraccionBase):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = partida.sala
        self.estado = "inicial"
        self.bandera_destilacion = None
        self.cerradura = None

    def on_show_view(self):
        super().on_show_view()

        if self.estado == "inicial":
            self.cambiar_fondo(fondo_inicial)
            self._cerradura()

        if self.estado == "abierto":
            self.cambiar_fondo(fondo_abierto)

        if self.estado == "final":
            self.cambiar_fondo(fondo_final)

    def _cerradura(self):
        self.cerradura = arcade.Sprite(transparente, center_x= self.ancho/2 + self.correccion_x + 40, center_y= self.alto/2 + self.correccion_y)
        self.cerradura.width = 100
        self.cerradura.height = 100
        self.lista_interaccion.append(self.cerradura)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

        if self.estado == "inicial":
            if self.cerradura.collides_with_point((x, y)):
                if self.sala.inventario.consultar("llave de quimicos"):
                    self.lista_interaccion.clear()
                    self.estado = "abierto"
                    self.ejecutar_dialogo("bien, ahora tengo con que trabajar")
                    self.cambiar_fondo(fondo_abierto)
                    self.cerradura = None
                else:
                    self.ejecutar_dialogo("necesito la llave...")

        elif self.estado == "abierto":
            self.estado = "final"
            self.cambiar_fondo(fondo_final)
            self.sala.inventario.agregar_objeto("quimicos estante")
        