import arcade
from PIL import Image, ImageDraw

PLAYER_SPEED = 5


# --- Clase del Personaje (Player) ---
class Player(arcade.Sprite):
    def __init__(self, sprite):
        # Crear texturas procedimentales para izquierda y derecha
        
        self.sprite = sprite
        self.texture_right = self.sprite.texture
        self.texture_left = self.sprite.texture.flip_left_right()

        super().__init__(self.texture_right)
        
        # Atributos de intención de movimiento
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

    def update(self):
        # Inicializar velocidades
        self.change_x = 0
        self.change_y = 0

        # Aplicar intención de movimiento
        if self.move_left:
            self.change_x = -PLAYER_SPEED
        if self.move_right:
            self.change_x = PLAYER_SPEED
        if self.move_up:
            self.change_y = PLAYER_SPEED
        if self.move_down:
            self.change_y = -PLAYER_SPEED

        # Actualizar posiciones
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Cambiar orientación visual del sprite
        if self.change_x > 0:
            self.texture = self.texture_right
        elif self.change_x < 0:
            self.texture = self.texture_left
