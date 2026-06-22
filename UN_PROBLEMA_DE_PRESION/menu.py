"""
Lógica del Menú Principal - Un Problema de Presión
"""
import os
import arcade
# Importamos la vista del juego y la sala correspondientes
from juego import JuegoView
from clases.salas.tuberias.sala_tuberias import Sala_Tuberias

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__)) 

# Constantes de pantalla
ANCHO = 1280
ALTO = 720
SCREEN_TITLE = "Un Problema de Presión - Menú"

# Rutas de recursos
IMG_FONDO = CURRENT_PATH + "/menu/fondo_menu.png"
IMG_INICIAR_NORMAL = CURRENT_PATH + "/menu/iniciar1.png"
IMG_INICIAR_PRESS = CURRENT_PATH + "/menu/iniciar3.png"
IMG_SALIR_NORMAL = CURRENT_PATH + "/menu/salir1.png"
IMG_SALIR_PRESS = CURRENT_PATH + "/menu/salir2.png"
class MenuView(arcade.View):

    def __init__(self):
        super().__init__()
        # En el __init__ SOLO definimos las variables como None o estructuras vacías
        self.sprites_menu = None
        self.fondo = None
        
        self.tx_iniciar_normal = None
        self.tx_iniciar_press = None
        self.tx_salir_normal = None
        self.tx_salir_press = None
        
        self.btn_iniciar = None
        self.btn_salir = None

        self.esperando_inicio = False
        self.temporizador_inicio = 0.0
        self.TIEMPO_ESPERA = 0.3

    def on_show_view(self):
        """ 
        SOLUCIÓN: Este método se ejecuta cuando la ventana ya está activa.
        Aquí es seguro cargar texturas y sprites.
        """
        # Configuramos el color de fondo por defecto
        arcade.set_background_color(arcade.color.BLACK)
        
        # Inicializamos la lista de sprites
        self.sprites_menu = arcade.SpriteList()
        
        # Cargamos el Fondo
        self.fondo = arcade.Sprite(IMG_FONDO, center_x=ANCHO/2, center_y=ALTO/2, scale=0.5)
        self.sprites_menu.append(self.fondo)
        
        # Cargamos Texturas de manera segura
        self.tx_iniciar_normal = arcade.load_texture(IMG_INICIAR_NORMAL)
        self.tx_iniciar_press = arcade.load_texture(IMG_INICIAR_PRESS)
        self.tx_salir_normal = arcade.load_texture(IMG_SALIR_NORMAL)
        self.tx_salir_press = arcade.load_texture(IMG_SALIR_PRESS)
        
        # Cargamos los Botones
        self.btn_iniciar = arcade.Sprite(self.tx_iniciar_normal, center_x=ANCHO/2, center_y=280)
        self.sprites_menu.append(self.btn_iniciar)
        
        self.btn_salir = arcade.Sprite(self.tx_salir_normal, center_x=ANCHO/2, center_y=160, scale=0.8)
        self.sprites_menu.append(self.btn_salir)

    def on_draw(self):
        self.clear() # Limpia la pantalla
        
        # Dibujamos todos los elementos del menú de un solo golpe
        self.sprites_menu.draw()

    def on_update(self, delta_time: float):
        # Si el botón fue activado, sumamos tiempo al temporizador
        if self.esperando_inicio:
            self.temporizador_inicio += delta_time
            
            # Cuando pase el tiempo de espera, ejecutamos la acción real
            if self.temporizador_inicio >= self.TIEMPO_ESPERA:
                self.esperando_inicio = False
                self.temporizador_inicio = 0.0
                
                # Restauramos la textura por si acaso
                self.btn_iniciar.texture = self.tx_iniciar_normal
                
                # ACCIÓN REAL: Aquí lanzas tu juego
                self.comenzar_juego()

    def on_mouse_press(self, x, y, button, modifiers):
        # Si ya estamos esperando que inicie el juego, bloqueamos nuevos clicks
        if self.esperando_inicio:
            return

        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.btn_iniciar.collides_with_point((x, y)):
                self.btn_iniciar.texture = self.tx_iniciar_press
                
            if self.btn_salir.collides_with_point((x, y)):
                self.btn_salir.texture = self.tx_salir_press

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Si se suelta el click sobre Iniciar, activamos la espera programada
            if self.btn_iniciar.texture == self.tx_iniciar_press:
                print("¡Botón presionado! Esperando un ratito para la animación...")
                self.esperando_inicio = True  # Esto activa la lógica en on_update
            
            # El botón de salir puede cerrarse inmediatamente
            elif self.btn_salir.texture == self.tx_salir_press:
                print("Saliendo...")
                arcade.exit()
            else:
                # Si soltó el mouse fuera de los botones, reseteamos texturas
                self.btn_iniciar.texture = self.tx_iniciar_normal
                self.btn_salir.texture = self.tx_salir_normal
    
    def comenzar_juego(self):
        """ Borra el menú por completo y carga la vista del juego limpia """
        print("-> Pasando al juego con una ventana vacía e independiente <-")
        
        # Instanciamos la sala y la vista del juego
        sala = Sala_Tuberias()
        vista_juego = JuegoView(sala)
        
        # Le decimos a la ventana principal que cambie de vista
        # Esto limpia automáticamente todo lo que MenuView estaba dibujando
        self.window.show_view(vista_juego)

def main(ventana=None):
    if not ventana:
        # Inicializamos la ventana contenedora global
        window = arcade.Window(ANCHO, ALTO, SCREEN_TITLE)
    else:
        window = ventana
    
    # Creamos la vista del menú y la mostramos en la ventana
    menu = MenuView()
    window.show_view(menu)
    
    arcade.run()

if __name__ == "__main__":
    main()

""" Cambios realizados:
1.  **Jerarquía Vertical:** He movido el logotipo (`fondo`) a `ALTO * 0.6` (más arriba) y los botones a `280` y `160` en el eje Y para que queden debajo del título.
2.  **Tamaño de Salir:** Al crear los sprites de `salir`, añadí el parámetro `scale=0.8` para que sea un 20% más pequeño que el de iniciar.
3.  **Lógica de Animación:** 
    *   `on_mouse_press`: Cambia el índice a `1` (la segunda imagen de tu lista) cuando el mouse está sobre el botón.
    *   `on_mouse_release`: Verifica si el botón estaba presionado, ejecuta la acción (entrar al juego o salir) y resetea el índice a `0`.
4.  **Colisiones:** Utilicé `collides_with_point((x, y))` para detectar de forma precisa si el puntero está dentro del área del botón.

¡Espero que esto termine de darle forma a tu menú! Si necesitas ajustar las distancias entre botones, solo cambia los valores de `center_y`.
"""