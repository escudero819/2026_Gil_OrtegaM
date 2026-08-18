"""
CLASE DE LA CLASE MESAVIEW
"""
# dependencias
import arcade, os
from ..interaccion_base import InteraccionBase
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/mesa.png")
pagina1 = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/pagina1.png")
pagina2 = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/pagina2.png")
transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "semitransparente_rojo.png"))

class CuadernoView(InteraccionBase):

    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = partida.sala
        self.estado = "pag1"

    def _paginas1(self):
        self.lista_interaccion.clear()
        print(self.fondo.width)
        self.pagina = arcade.Sprite(transparente, center_x= self.ancho + self.correccion_x - 85, center_y=self.alto/2 + self.correccion_y + 5)
        self.pagina.width = 60
        self.pagina.height = 60
        self.lista_interaccion.append(self.pagina)
        self._volver()

    def _volver(self):
        self.volver = arcade.Sprite(transparente, center_x= 40 + self.correccion_x, center_y= self.alto - 40 + self.correccion_y)
        self.volver.width = 50
        self.volver.height = 50
        print("volver")
        self.lista_interaccion.append(self.volver)

    def _paginas2(self):
        self.lista_interaccion.clear()
        self.pagina = arcade.Sprite(transparente, center_x= 70 + self.correccion_x, center_y= self.alto/2 + self.correccion_y + 15) 
        self.pagina.width = 60
        self.pagina.height = 60
        self.lista_interaccion.append(self.pagina)

    def on_show_view(self):
        super().on_show_view()

        if not self.fondo:
            self.cambiar_fondo(pagina1)
        else:
            self.cambiar_fondo(self.fondo)

        if self.estado == "pag1":
            self._paginas1()
        else:
            self._paginas2()

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        if self.estado == "pag1":
            if self.volver.collides_with_point((x, y)):
                self.partida.window.show_view(self.sala.mesa_interfaz)

            if self.pagina.collides_with_point((x, y)):
                self.estado = "pag2"
                self.cambiar_fondo(pagina2)
                self._paginas2()
        else:
            if self.pagina.collides_with_point((x, y)):
                self.estado = "pag1"
                self.cambiar_fondo(pagina1)
                self._paginas1()

        print(self.lista_interaccion)

class MesaView(InteraccionBase):

    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.sala = partida.sala

    def on_show_view(self):
        super().on_show_view()

        if not self.fondo:
            self.cambiar_fondo(fondo)
        else:
            self.cambiar_fondo(self.fondo)

        self.cuaderno = arcade.Sprite(transparente, center_x= 160 + self.correccion_x, center_y= self.fondo.height/2 - 140)
        self.cuaderno.height = 200
        self.cuaderno.width = 200
        
        self.lista_interaccion.append(self.cuaderno)
    
    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        if self.cuaderno.collides_with_point((x, y)):
            cuaderno = CuadernoView(self.partida)
            self.partida.window.show_view(cuaderno)
        