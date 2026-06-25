"""
    Vista de victoria y agradecimiento por probar el juego
"""
import arcade, time, os
from configuraciones import Constantes as const
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
imagen_victoria = CURRENT_PATH + "/menu/victoria.png"

class VictoriaView(arcade.View):

    def __init__(self):
        super().__init__()
        self.timer = time.time()
        self.tiempo_click = 3 #seg
        self.velocidad_fade = 150
        self.alpha_actual = 0
        self.mostrar_texto = False
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

        self.lista_fondo = arcade.SpriteList()
        fondo = arcade.Sprite(arcade.load_texture(imagen_victoria), center_x= const.ancho_ventana/2, center_y= const.alto_ventana/ 2, )
        factor_x = const.ancho_ventana / fondo.width 
        factor_y = const.alto_ventana / fondo.height
        factor = min(factor_x, factor_y)
        fondo.width = fondo.width * factor
        fondo.height = fondo.height * factor
        self.lista_fondo.append(fondo)

        self.texto_fade = arcade.Text(
            text="click para continuar",
            x=self.window.width / 2,
            y=self.window.height / 4 - 50,
            color=(255, 255, 255, self.alpha_actual), # El cuarto elemento es el Alpha (0-255)
            font_size=24,
            anchor_x="center",
            anchor_y="center",
            font_name="Kenney Pixel" # O cualquier fuente que uses
        )
    
    def on_update(self, delta_time: float):

        if not self.mostrar_texto:
            if time.time() - self.timer >= self.tiempo_click:
                self.mostrar_texto = True

        if self.mostrar_texto and self.alpha_actual < 255:

            self.alpha_actual += self.velocidad_fade * delta_time

            if self.alpha_actual > 255:
                self.alpha_actual = 255
            
            self.texto_fade.color = (255, 255, 255, int(self.alpha_actual))
    
    def on_draw(self):
        self.lista_fondo.draw()

        if self.mostrar_texto:
            self.texto_fade.draw()
    
    def on_mouse_press(self, x, y, button, modifiers):
        
        from menu import MenuView

        vista_menu = MenuView

        self.window.show_view(vista_menu)
        return