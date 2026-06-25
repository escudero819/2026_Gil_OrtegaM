import arcade, os
from configuraciones import Constantes as const

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

derecha_apagada = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/computadoras/der/apagada.png")
derecha_prendida = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/computadoras/der/prendida.png")
izquierda_apagada = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/computadoras/izq/apagada.png")
izquierda_prendida = arcade.load_texture(CURRENT_PATH + "/texturas/interfaces/computadoras/izq/prendida.png")
transparente = arcade.load_texture(os.path.join(CURRENT_PATH, "..", "semitransparente_rojo.png"))

class PCInterfaz(arcade.View):

    def __init__(self, partida, tipo: str):
        super().__init__()
        self.tipo = tipo
        self.partida = partida
        self.estado = "apagada"
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
    
    def _prender(self):
        if self.tipo == "der":
            boton = arcade.Sprite(transparente, center_x = self.centro_x + 380, center_y = self.centro_y - 30)
        else:
            boton = arcade.Sprite(transparente, center_x = self.centro_x - 380, center_y = self.centro_y - 30)
        boton.width = 50
        boton.height = 50
        self.lista_interaccion.append(boton)
    
    def on_show_view(self):
        self.lista_fondo = arcade.SpriteList()
        self.lista_interaccion = arcade.SpriteList()
        if not self.fondo:
            if self.tipo == "der":
                self.fondo = self.cambiar_fondo(derecha_apagada)
            else:
                self.fondo = self.cambiar_fondo(izquierda_apagada)
        else:
            self.cambiar_fondo(self.fondo)
        
        if self.estado == "apagada":
            self._prender()

    def on_draw(self):
        self.lista_fondo.draw()
        self.lista_interaccion.draw()
    
    def on_mouse_press(self, x, y, button, modifiers):
        if arcade.get_sprites_at_point((x,y), self.lista_fondo):
            if self.estado == "apagada":
                if arcade.get_sprites_at_point((x,y), self.lista_interaccion):
                    if self.tipo == "der":
                        self.cambiar_fondo(derecha_prendida)
                    else:
                        self.cambiar_fondo(izquierda_prendida)
                    self.lista_interaccion.clear()
                    self.estado = "prendida"
            else:
                self.window.show_view(self.partida)
        else:
            self.window.show_view(self.partida)