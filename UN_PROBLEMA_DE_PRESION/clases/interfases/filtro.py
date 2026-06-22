import arcade

class ColorFilter:
    def __init__(self, width, height, color=(192, 192, 192), alpha=100, visible=True):

        self.width = width
        self.height = height
        self.color = tuple(color)
        self.alpha = int(alpha)  # 0-255
        self.visible = bool(visible)

    def draw(self):
        if not self.visible:
            return
        arcade.draw_lrtb_rectangle_filled(
            0,
            self.width,
            self.height,
            0,
            (self.color[0], self.color[1], self.color[2], self.alpha),
        )

    def toggle(self):
        self.visible = not self.visible

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def set_color(self, color_tuple):
        self.color = tuple(color_tuple)

    def set_alpha(self, alpha):
        self.alpha = int(alpha)

    def resize(self, width, height):
        self.width = width
        self.height = height