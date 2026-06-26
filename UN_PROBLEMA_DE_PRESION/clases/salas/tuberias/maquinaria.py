import arcade, os
from configuraciones import Constantes as const

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

fondo_con_pinzas = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/maquinaria/con_pinzas.png")
fondo_sin_pinzas = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/maquinaria/sin_pinzas.png")
transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "transparente.png"))

class MaquinariaInterfaz(arcade.View):
    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.estado = "pinzas"
        self.sala = self.partida.sala
        self.centro_x = const.ancho_ventana / 2
        self.centro_y = const.alto_ventana / 2
        self.fondo = None
    
    def cambiar_fondo(self, fondo):
        self.fondo = fondo
        fondo = arcade.Sprite(fondo)
        factor_y = const.alto_interfaces / fondo.height 
        factor_x = const.ancho_interfaces/ fondo.width
        factor = min(factor_x, factor_y)
        fondo.height = fondo.height * factor
        fondo.width = fondo.width * factor
        fondo.center_x = self.centro_x
        fondo.center_y = self.centro_y
        if self.lista_fondo:
            self.lista_fondo.pop()
        self.lista_fondo.append(fondo)

    def _sacar_pinzas(self):
        pinzas = arcade.Sprite(transparente, center_x=self.centro_x - 40, center_y= self.centro_y - 170)
        pinzas.width = 130
        pinzas.height = 130
        self.lista_interaccion.append(pinzas)

    def on_show_view(self):

        self.lista_fondo = arcade.SpriteList()
        self.lista_interaccion = arcade.SpriteList()
        if not self.fondo:
            self.cambiar_fondo(fondo_con_pinzas)
        else:
            self.cambiar_fondo(self.fondo)
        if self.estado == "pinzas":
            self._sacar_pinzas()
    
    def on_draw(self):
        self.lista_fondo.draw()
        self.lista_interaccion.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if arcade.get_sprites_at_point((x,y), self.lista_fondo):
            if self.estado != "sin_pinzas":
                if arcade.get_sprites_at_point((x,y), self.lista_interaccion):
                    if self.estado == "pinzas":
                        self.cambiar_fondo(fondo_sin_pinzas)
                        self.sala.inventario.agregar_objeto("pinzas")
                        mensaje = '"has obtenido pinzas"'
                        self.partida.mostrar_texto(mensaje)
                        self.lista_interaccion.clear()
                        self.estado = "sin_pinzas"
            else:
                self.window.show_view(self.partida)
        else:
            self.window.show_view(self.partida)