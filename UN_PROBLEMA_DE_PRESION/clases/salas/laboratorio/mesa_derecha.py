"""
CLASE MESA_QUIMICOSVIEW
"""

# dependencias
import arcade, os, time
from ..interaccion_base import  InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "semitransparente_rojo.png"))
fondo_inicial = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/mesa_quimicos.png")
fondo_final = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/mesa_quimicos2.png")

class Mesa_QuimicosView(InteraccionBase):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = partida.sala
        self.estado = "inicial"

    def on_show_view(self):
        super().on_show_view()

        if self.estado == "inicial":
            self.cambiar_fondo(fondo_inicial)

        if self.estado == "final":
            self.cambiar_fondo(fondo_final)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

        if self.estado == "inicial":
            self.cambiar_fondo(fondo_final)
            self.sala.inventario.agregar_objeto("quimicos mesa")
            self.estado = "final"
        else:
            self.ejecutar_dialogo("ya no necesito otra cosa")