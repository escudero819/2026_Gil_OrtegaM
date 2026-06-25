import arcade, os
from configuraciones import Constantes as const

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
#cargar imagenes

sin_elementos_1 = arcade.load_texture(CURRENT_PATH +  "/texturas/interfaces/panel/sin_elem_1.png")
sin_elementos_2 = arcade.load_texture(CURRENT_PATH +  "/texturas/interfaces/panel/sin_elem_2.png")

transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "semitransparente_rojo.png"))


class PanelInterfaz(arcade.View):

    def __init__(self, partida):
        super().__init__()
        self.partida = partida
        self.estado = "sin_elem"
        self.sala = self.partida.sala
        self.centro_x = const.ancho_ventana / 2
        self.centro_y = const.alto_ventana / 2
        self.fondo = None
        self.parpadeo = 3
        self.fondo_parpadeo = False
        self.timer = 0.0
    
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
    
    
    def on_show_view(self):
        self.lista_fondo = arcade.SpriteList()
        self.lista_interaccion = arcade.SpriteList()
        if not self.fondo:
            self.fondo = self.cambiar_fondo(sin_elementos_1)
        else:
            self.cambiar_fondo(self.fondo)
        
        if self.estado == "sin_elem":
            self._colocar_elem()
    
    def on_draw(self):
        self.lista_fondo.draw()
        self.lista_interaccion.draw()
    
    def on_update(self, delta_time: float):
        if self.estado == "sin_elem":
            self.timer += delta_time

            if self.timer >= self.parpadeo:
                if self.fondo_parpadeo:
                    self.cambiar_fondo(sin_elementos_1)
                    self.fondo_parpadeo = False
                else:
                    self.cambiar_fondo(sin_elementos_2)
                    self.fondo_parpadeo = True
    
    def on_mouse_press(self, x, y, button, modifiers):
        if arcade.get_sprites_at_point((x,y), self.lista_fondo):
            if self.estado == "sin_elem":
                if arcade.get_sprites_at_point((x,y), self.lista_interaccion):
                    if self.sala.inventario.consultar("cables"):
                        #cambiar
                        self.lista_interaccion.clear()
                        self.estado = "prendida"
                    else:
                        mensaje = "no tengo con que trabajar"
                        self.partida.mostrar_texto(mensaje)
                if self.sala.inventario.consultar("cables"):
                    mensaje = "no tengo con que trabajar"
                    self.partida.mostrar_texto(mensaje)
            else:
                self.window.show_view(self.partida)
        else:
            self.window.show_view(self.partida)