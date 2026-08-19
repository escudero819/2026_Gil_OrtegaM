"""
CLASE PUERTAVIEW
"""

# dependencias
import arcade, os, time
from ..interaccion_base import  InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "semitransparente_rojo.png"))
fondo_inicial = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/puerta_inicial.png")
fondo_pista_1 = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/puerta_pista1.png")
fondo_pista_2 = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/puerta_pista2.png")
fondo_pista_3 = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/puerta_pista3.png")
fondo_pista_4 = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/puerta_pista4.png")
fondo_final = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/puerta_final.png")

class PuertaView(InteraccionBase):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = partida.sala
        self.estado = "inicial"

    def on_show_view(self):
        super().on_show_view()

        if self.estado == "inicial":
            self.cambiar_fondo(fondo_inicial)
            self.ejecutar_dialogo("la quimica! no la escucho")

        if self.estado == "pista1":
            self.cambiar_fondo(fondo_pista_1)

        if self.sala.mesa_dest.estado == "final" or self.sala.mesa_dest.estado == "terminado":
            self.estado = "pista2"
            self.cambiar_fondo(fondo_pista_2)

        if self.estado == "pista2" and self.sala.mesa_medidor.puzzle:
            self.estado = "pista3"
            self.cambiar_fondo(fondo_pista_3)

        if self.estado == "pista3" and self.sala.inventario.consultar("combinacion final"):
            self.estado = "pista4"
            self.cambiar_fondo(fondo_pista_4)
            self.ejecutar_dialogo("ahora queda tirarlo al cristal")

        if self.estado == "pista4":
            self.cambiar_fondo(fondo_pista_4)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        if self.estado == "inicial":
            self.estado = "pista1"
            self.cambiar_fondo(fondo_pista_1)
            self.ejecutar_dialogo("estendido, hare eso")

        if self.estado == "pista2":
            self.ejecutar_dialogo("debo reunir los 4 quimicos")

        if self.estado == "pista3":
            self.ejecutar_dialogo("parece ser la receta para un acido")

        if self.estado == 'pista4':
            self.cambiar_fondo(fondo_final)
            self.estado = "final"

        elif self.estado == "final":
            print("saliendo del laboratorio")
            self.partida.window.show_view(self.partida.manager)
        