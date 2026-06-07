import arcade
from PIL import Image, ImageDraw

PLAYER_SPEED = 7


# --- Clase del Personaje (Player) ---
class Player(arcade.Sprite):
    def __init__(self, imagen_path, center_x, center_y):
        # Crear texturas procedimentales para izquierda y derecha
        
        super().__init__(imagen_path, center_x=center_x, center_y=center_y)
        
        self.texture_right = self.texture
        self.texture_left = self.texture.flip_left_right()
        
        # Atributos de intención de movimiento
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

        self.velocidad = PLAYER_SPEED
        
        # Inicializar velocidades
        self.change_x = 0
        self.change_y = 0

    def update_por_teclado(self):
        
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
