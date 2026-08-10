from clases.salas.interaccion_base import InteraccionBase
import os, arcade

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/resistencias.png")
transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "transparente.png"))

class Caja(arcade.Sprite):
    def __init__(self, ohms, x, y, ancho, alto):
        super().__init__(transparente, center_x=x, center_y=y)
        self.width = ancho
        self.height = alto
        self.ohms = ohms



class Estanteria1Interfaz(InteraccionBase):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = self.partida.sala

    def _inicializar_sprites_fijos(self):
        """ Crea los sprites de fondo y estanterías de forma persistente en memoria """
        # Sprite del fondo metálico de la interfaz
        caja_100 = Caja("100", self.centro_x - 180, self.centro_y - 140, 130, 120)
        self.lista_interaccion.append(caja_100)
        caja_150 = Caja("150", self.centro_x - 25, self.centro_y - 135, 130, 130)
        self.lista_interaccion.append(caja_150)
        caja_200 = Caja("200", self.centro_x + 110, self.centro_y - 145, 70, 110)
        self.lista_interaccion.append(caja_200)

    def on_show_view(self):
        super().on_show_view()

        if not self.fondo:
            self.cambiar_fondo(fondo)
        else:
            self.cambiar_fondo(self.fondo)
        if self.estado == "indefinido":
            self._inicializar_sprites_fijos()

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        for caja in self.lista_interaccion:
            if caja.collides_with_point((x, y)):
                print(f"Click en caja con ohms: {caja.ohms}")
                # Aquí puedes agregar la lógica para manejar la interacción con la caja
                if self.partida.sala.inventario.consultar(f"resistencia_{caja.ohms}"):
                    self.ejecutar_dialogo(f'"Ya tengo de {caja.ohms} ohms."')
                self.partida.sala.inventario.agregar_objeto(f"resistencia_{caja.ohms}")
                self.ejecutar_dialogo(f"agarraste una resistencia de {caja.ohms} ohms.", voz="Guia")

    