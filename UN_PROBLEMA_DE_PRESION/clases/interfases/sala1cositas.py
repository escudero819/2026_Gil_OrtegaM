import arcade
import pyglet
from filtro import ColorFilter
from pause import PauseManager

display = pyglet.canvas.get_display()
screen = display.get_default_screen()
ANCHO_VENTANA = screen.width
ALTO_VENTANA = screen.height

class MiVentana(arcade.Window):
    def __init__(self):
        super().__init__(ANCHO_VENTANA // 5 * 3, ALTO_VENTANA // 5 * 3, "Mi Ventana")
        arcade.set_background_color(arcade.color.WHITE)
        self.filter = ColorFilter(self.width, self.height, color=(0, 0, 120), alpha=90, visible=True)
        # gestor de pausa reutilizable
        self.pause = PauseManager()

    def on_draw(self):
        arcade.start_render()
        self.filter.draw()
        # dibujar overlay de pausa si está pausado
        self.pause.draw_overlay(self)

    def on_key_press(self, symbol, modifiers):
        # tecla P para pausar/reanudar
        if symbol == arcade.key.P:
            self.pause.toggle()
            return
        # si está pausado, dejar que el gestor maneje otras teclas
        if self.pause.handle_key_press(symbol, modifiers):
            return

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.filter.resize(width, height)
        # nada más que actualizar para pause (no mantiene tamaño)

def main():
    ventana = MiVentana()
    ventana.run()

if __name__ == "__main__":
    main()
