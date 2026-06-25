"""
    Este archivo contendra las Views de las derrotas ya sea por eliminacion o tiempo
"""

import os, arcade, time
from configuraciones import Constantes as const

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

muerte_electricidad = CURRENT_PATH + "/menu/perder_electricidad.png"
muerte_tiempo = CURRENT_PATH + "/menu.perder_agua.png"

class Game_Over(arcade.View):

    def __init__(self, tipo_muerte):
        super().__init__()
        self.imagen_muerte = CURRENT_PATH + f"/menu/perder_{tipo_muerte}.png"
        self.bandera_texto = time.time()
        self.TIEMPO_PARA_APARECER = 3.0  # Aparecerá a los 3 segundos
        self.VELOCIDAD_FADE = 150
        self.alpha_actual = 0
        self.mostrar_texto = False

    
    def on_show_view(self):
        
        # Configuramos el color de fondo por defecto
        arcade.set_background_color(arcade.color.BLACK)

        self.lista_fondo = arcade.SpriteList()

        self.fondo = arcade.Sprite(arcade.load_texture(self.imagen_muerte), center_x=const.ancho_ventana/2, center_y=const.alto_ventana/2)
        factor_x = const.ancho_ventana / self.fondo.width
        factor_y = const.alto_ventana / self.fondo.height
        factor = min(factor_x, factor_y)
        self.fondo.width = self.fondo.width * factor 
        self.fondo.height = self.fondo.height * factor
        self.lista_fondo.append(self.fondo)

        self.texto_fade = arcade.Text(
            text="click para continuar",
            x=self.window.width / 2,
            y=self.window.height / 4,
            color=(255, 255, 255, self.alpha_actual), # El cuarto elemento es el Alpha (0-255)
            font_size=24,
            anchor_x="center",
            anchor_y="center",
            font_name="Kenney Pixel" # O cualquier fuente que uses
        )
    
    def on_update(self, delta_time: float):
        if not self.mostrar_texto:
           if time.time() - self.bandera_texto >= self.TIEMPO_PARA_APARECER:
               self.mostrar_texto = True

        # LÓGICA DEL FADE-IN
        if self.mostrar_texto and self.alpha_actual < 255:
            # Multiplicamos la velocidad por delta_time para que sea suave a 60 FPS
            self.alpha_actual += self.VELOCIDAD_FADE * delta_time
            
            # Evitamos que se pase del límite máximo de opacidad (255)
            if self.alpha_actual > 255:
                self.alpha_actual = 255
            
            # Aplicamos el nuevo Alpha al color del texto (Mantiene Blanco: 255, 255, 255)
            self.texto_fade.color = (255, 255, 255, int(self.alpha_actual))
    
    def on_draw(self):
        self.clear() # Limpia la pantalla
        
        self.lista_fondo.draw()
            
        # DIBUJAR EL TEXTO CON FADE
        if self.texto_fade:
            self.texto_fade.draw()
    
    def on_mouse_press(self, x, y, button, modifiers):

        from menu import MenuView

        vista_menu = MenuView()
        self.window.show_view(vista_menu)
        return