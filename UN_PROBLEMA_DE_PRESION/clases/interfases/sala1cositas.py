import arcade
import pyglet
import math
from filtro import modo_filtro
from pause import modo_pausa

display = pyglet.display.get_display()
screen = display.get_default_screen()
ANCHO_VENTANA = screen.width
ALTO_VENTANA = screen.height

def rotar_punto(x, y, cx, cy, ang):
    dx = x - cx
    dy = y - cy
    return (
        cx + dx * math.cos(ang) - dy * math.sin(ang),
        cy + dx * math.sin(ang) + dy * math.cos(ang),
    )

class MiVentana(arcade.Window):
    def __init__(self):
        super().__init__(ANCHO_VENTANA // 5 * 3, ALTO_VENTANA // 5 * 3, "Mi Ventana")
        arcade.set_background_color(arcade.color.WHITE)
        self.filter = modo_filtro(self.width, self.height)
        # gestor de pausa reutilizable
        self.modo_pausa = modo_pausa()

        # Estado de la forma giratoria
        self.angulo = 0.0
        self.centro = (self.width // 2, self.height // 2)
        self.puntos = [
            (self.centro[0] - 80, self.centro[1] - 40),
            (self.centro[0] + 80, self.centro[1]),
            (self.centro[0] - 80, self.centro[1] + 40),
        ]
        self.color_forma = arcade.color.CORNFLOWER_BLUE

    def on_update(self, delta_time):
        # Usar puede_actualizar() para verificar si se debe actualizar
        if self.modo_pausa.puede_actualizar():
            self.angulo += math.radians(90) * delta_time
            self.angulo %= math.pi * 2

    def on_draw(self):
        self.clear()
        self.filter.dibujar()

        roto = [
            rotar_punto(x, y, self.centro[0], self.centro[1], self.angulo)
            for x, y in self.puntos
        ]
        arcade.draw_polygon_filled(roto, self.color_forma)

        # dibujar overlay de pausa si está pausado
        self.modo_pausa.draw_overlay(self)

    def on_key_press(self, symbol, modifiers):
        # tecla P para pausar/reanudar (SOLO aquí se maneja P, nunca en manejar_tecla)
        if symbol == arcade.key.P:
            self.modo_pausa.alternar()
            return
        
        # Otras teclas cuando NO está pausado
        if not self.modo_pausa.esta_pausado():
            # Aquí podrías agregar otras teclas si lo necesitas
            return
        
        # Si está pausado, solo ESC reanuda (NO P porque ya se maneja arriba)
        if symbol == arcade.key.ESCAPE:
            self.modo_pausa.reanudar()
            return

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.filter.redimensionar(width, height)
        self.centro = (width // 2, height // 2)
        self.puntos = [
            (self.centro[0] - 80, self.centro[1] - 40),
            (self.centro[0] + 80, self.centro[1]),
            (self.centro[0] - 80, self.centro[1] + 40),
        ]
        # nada más que actualizar para pause (no mantiene tamaño)

def main():
    ventana = MiVentana()
    ventana.run()

if __name__ == "__main__":
    main()
