import arcade, os
from configuraciones import Constantes as const
from clases.salas.interaccion_base import InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo_con_pinzas = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/maquinaria/con_pinzas.png")
fondo_sin_pinzas = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/maquinaria/sin_pinzas.png")
transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "transparente.png"))

class MaquinariaInterfaz(InteraccionBase):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.estado = "pinzas"
        self.sala = self.partida.sala

    def _sacar_pinzas(self):
        pinzas = arcade.Sprite(transparente, center_x=self.centro_x - 40, center_y= self.centro_y - 170)
        pinzas.width = 130
        pinzas.height = 130
        self.lista_interaccion.append(pinzas)

    def on_show_view(self):
        super().on_show_view()

        if not self.fondo:
            self.cambiar_fondo(fondo_con_pinzas)
        else:
            self.cambiar_fondo(self.fondo)
        if self.estado == "pinzas":
            self._sacar_pinzas()
    

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        if self.estado != "sin_pinzas":
            if arcade.get_sprites_at_point((x,y), self.lista_interaccion):
                if self.estado == "pinzas":
                    self.cambiar_fondo(fondo_sin_pinzas)
                    self.sala.inventario.agregar_objeto("pinzas")
                    mensaje = '"has obtenido pinzas"'
                    self.ejecutar_dialogo(mensaje, voz="Guia")
                    self.lista_interaccion.clear()
                    self.estado = "sin_pinzas"
        else:
            self.window.show_view(self.partida)
