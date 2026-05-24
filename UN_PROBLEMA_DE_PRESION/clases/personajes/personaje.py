import arcade
from PIL import Image, ImageDraw

PLAYER_SPEED = 5

# --- Generador Procedural del Sprite del Personaje ---
def create_player_texture(facing_right=True):
    """
    Genera una textura de pixel art para el personaje usando PIL.
    Esto previene problemas de archivos faltantes o transparencias incorrectas.
    """
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Cuerpo (Ropa azul real/eléctrico)
    draw.ellipse([6, 8, 26, 28], fill=(65, 105, 225, 255)) 

    # Cabeza (Piel color melocotón)
    draw.ellipse([8, 2, 24, 18], fill=(255, 218, 185, 255)) 

    # Cabello (Castaño)
    draw.rectangle([10, 2, 22, 6], fill=(139, 69, 19, 255)) 

    # Ojos (Puntos negros, colocados según la dirección a la que mira)
    if facing_right:
        draw.rectangle([18, 8, 20, 10], fill=(0, 0, 0, 255))
        draw.rectangle([22, 8, 24, 10], fill=(0, 0, 0, 255))
    else:
        draw.rectangle([8, 8, 10, 10], fill=(0, 0, 0, 255))
        draw.rectangle([12, 8, 14, 10], fill=(0, 0, 0, 255))

    # Detalle / Mochila (Rojo escarlata)
    if facing_right:
        draw.rectangle([4, 12, 8, 24], fill=(220, 20, 60, 255))
    else:
        draw.rectangle([24, 12, 28, 24], fill=(220, 20, 60, 255))

    try:
        # Compatible con Arcade 3.0+
        return arcade.Texture(image=img)
    except TypeError:
        # Fallback para versiones más antiguas de Arcade
        name = f"player_texture_{'right' if facing_right else 'left'}"
        return arcade.Texture(name, img)


# --- Clase del Personaje (Player) ---
class Player(arcade.Sprite):
    def __init__(self):
        # Crear texturas procedimentales para izquierda y derecha
        self.texture_right = create_player_texture(facing_right=True)
        self.texture_left = create_player_texture(facing_right=False)
        
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
