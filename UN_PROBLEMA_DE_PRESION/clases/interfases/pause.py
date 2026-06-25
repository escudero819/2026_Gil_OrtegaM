import arcade
from filtro import modo_filtro

<<<<<<< HEAD
class modo_pausa:
=======
class PauseManager():
>>>>>>> 2b53ecc (primera interaccion conseguida: armario.)

    def __init__(self, titulo="PAUSA", pausa=False, color_superposicion=(100, 100, 100, 160)):
        self.tateQuieto = pausa
        self.titulo = titulo
        self.color_superposicion = color_superposicion


    def pausar(self):
        self.tateQuieto = True

    def reanudar(self):
        self.tateQuieto = False

    def alternar(self):
        self.tateQuieto = not self.tateQuieto

    def esta_pausado(self):
        return self.tateQuieto

    def puede_actualizar(self):
        """Retorna True si se debe actualizar (cuando NO está pausado)."""
        return not self.tateQuieto

    def draw_overlay(self, window: arcade.Window):
        if not self.tateQuieto:
            return
        # overlay semitransparente
        arcade.draw_lrbt_rectangle_filled(0, window.width, 0, window.height, self.color_superposicion)
        # texto central
        arcade.draw_text(self.titulo, window.width // 2, window.height // 2 + 40, arcade.color.WHITE, 48, anchor_x="center")
        # botón continuar
        btn_w, btn_h = 220, 50
        btn_x = window.width // 2
        btn_y = window.height // 2 - 40
        arcade.draw_lbwh_rectangle_filled(btn_x - btn_w / 2, btn_y - btn_h / 2, btn_w, btn_h, arcade.color.DARK_BLUE)
        arcade.draw_text("Continuar", btn_x, btn_y, arcade.color.WHITE, 18, anchor_x="center", anchor_y="center")

    def manejar_click(self, x, y, window: arcade.Window):
        """Devuelve True si el evento fue consumido por la UI de pausa."""
        if not self.tateQuieto:
            return False
        btn_w, btn_h = 220, 50
        btn_x = window.width // 2
        btn_y = window.height // 2 - 40
        if abs(x - btn_x) <= btn_w / 2 and abs(y - btn_y) <= btn_h / 2:
            self.reanudar()
            return True
        # otros controles de la UI podrían añadirse aquí
        return True

    def manejar_tecla(self, symbol, modifiers):
        # tecla ESC o P reanuda
        if not self.tateQuieto:
            return False
        if symbol in (arcade.key.ESCAPE, arcade.key.P):
            self.reanudar()
            return True
        return False
