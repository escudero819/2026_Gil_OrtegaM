import arcade
from filtro import ColorFilter

class PauseManager:

    def __init__(self, title="PAUSA", overlay_color=(100, 100, 100, 160)):
        self._paused = False
        self.title = title
        self.overlay_color = overlay_color
        

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False

    def toggle(self):
        self._paused = not self._paused

    def is_paused(self):
        return self._paused

    def draw_overlay(self, window: arcade.Window):
        if not self._paused:
            return
        # overlay semitransparente
        arcade.draw_lrtb_rectangle_filled(0, window.width, window.height, 0, self.overlay_color)
        # texto central
        arcade.draw_text(self.title, window.width // 2, window.height // 2 + 40, arcade.color.WHITE, 48, anchor_x="center")
        # botón continuar
        btn_w, btn_h = 220, 50
        btn_x = window.width // 2
        btn_y = window.height // 2 - 40
        arcade.draw_rectangle_filled(btn_x, btn_y, btn_w, btn_h, arcade.color.DARK_BLUE)
        arcade.draw_text("Continuar", btn_x, btn_y, arcade.color.WHITE, 18, anchor_x="center", anchor_y="center")

    def handle_mouse_press(self, x, y, window: arcade.Window):
        """Devuelve True si el evento fue consumido por la UI de pausa."""
        if not self._paused:
            return False
        btn_w, btn_h = 220, 50
        btn_x = window.width // 2
        btn_y = window.height // 2 - 40
        if abs(x - btn_x) <= btn_w / 2 and abs(y - btn_y) <= btn_h / 2:
            self.resume()
            return True
        # otros controles de la UI podrían añadirse aquí
        return True

    def handle_key_press(self, symbol, modifiers):
        # tecla ESC o P reanuda
        if not self._paused:
            return False
        if symbol in (arcade.key.ESCAPE, arcade.key.P):
            self.resume()
            return True
        return False
