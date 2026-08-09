from clases.salas.interaccion_base import InteraccionBase
import os, arcade

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/transistores.png")
transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "semitransparente_rojo.png"))


class Estanteria4Interfaz(InteraccionBase):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = self.partida.sala

    def _inicializar_sprites_fijos(self):
        """ Crea los sprites de fondo y estanterías de forma persistente en memoria """
        # Sprite del fondo metálico de la interfaz
        caja = arcade.Sprite(transparente, center_x=self.centro_x - 80, center_y=self.centro_y)
        caja.width = 120
        caja.height = 120
        self.lista_interaccion.append(caja)

    def on_show_view(self):
        super().on_show_view()

        if not self.fondo:
            self.cambiar_fondo(fondo)
        else:
            self.cambiar_fondo(self.fondo)
        self._inicializar_sprites_fijos()

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        for caja in self.lista_interaccion:
            if caja.collides_with_point((x, y)):
                print(f"Click en caja con transistores")
                # Aquí puedes agregar la lógica para manejar la interacción con la caja
                if self.partida.sala.inventario.consultar(f"transistor1"):
                    if self.partida.sala.inventario.consultar(f"transistor2"):
                        self.ejecutar_dialogo(f'"Ya tengo suficientes transistores."')
                    else:
                        self.partida.sala.inventario.agregar_objeto(f"transistor2")
                        self.ejecutar_dialogo(f"agarraste un segundo transistor.", voz="Guia")
                else:
                    self.partida.sala.inventario.agregar_objeto(f"transistor1")
                    self.ejecutar_dialogo(f"agarraste un transistor.", voz="Guia")