"""
CLASE ELEMENTOSVIEW
"""

# dependencias
import arcade, os, time
from ..interaccion_base import  InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "transparente.png"))
fondo_inicial = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/est_elementos.png")
fondo_final = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/est_elementos2.png")

class ElementosView(InteraccionBase):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = partida.sala
        self.estado = "inicial"
        self.destilador = None

    def on_show_view(self):
        super().on_show_view()

        if self.estado == "inicial":
            self.cambiar_fondo(fondo_inicial)
            self._destilador()
        else:
            self.cambiar_fondo(fondo_final)

    def _destilador(self):
        self.destilador = arcade.Sprite(transparente, center_x= self.ancho/2 + self.correccion_x + 30, center_y= self.alto/4*3 + self.correccion_y + 25)
        self.destilador.width = 150
        self.destilador.height = 150
        self.lista_interaccion.append(self.destilador)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

        if self.estado == "inicial":
            if self.destilador.collides_with_point((x, y)):
                self.estado = "final"
                self.ejecutar_dialogo("vamos a llevarlo a la mesa")
                self.sala.inventario.agregar_objeto("destilador")
                self.cambiar_fondo(fondo_final)
        else:
            self.ejecutar_dialogo("los demas elemento no hacen falta")
        