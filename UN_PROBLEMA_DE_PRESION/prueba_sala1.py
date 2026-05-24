import os
import arcade
from PIL import Image, ImageDraw

# Configuración de Rutas de las Imágenes de Fondo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE1_PATH = os.path.join(BASE_DIR, "fondo1.png")
IMAGE2_PATH = os.path.join(BASE_DIR, "fondo2.png")

# Obtener dimensiones reales de las imágenes de fondo usando PIL de forma segura
try:
    with Image.open(IMAGE1_PATH) as img:
        SCREEN_WIDTH, SCREEN_HEIGHT = img.size
except Exception:
    # Dimensiones de respaldo en caso de que ocurra algún problema leyendo el archivo
    print(Exception)
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

SCREEN_TITLE = "Sala 1 - Mapa Animado Dinámico"


from clases.personajes.personaje import Player

# --- Clase Principal de la Ventana del Juego ---
class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        
        # Verificar que los archivos de imagen existan
        if not os.path.exists(IMAGE1_PATH) or not os.path.exists(IMAGE2_PATH):
            print(f"ADVERTENCIA: No se encontraron las imágenes {IMAGE1_PATH} o {IMAGE2_PATH} en el directorio.")
            print("Por favor, asegúrate de que fondo1.jpg y fondo2.jpg estén en la misma carpeta que el script.")

        self.background_textures = []
        self.current_bg_index = 0
        self.bg_timer = 0.0
        
        self.background_list = None
        self.player_list = None
        self.background_sprite = None
        self.player = None

        # Textos de la interfaz (pre-renderizados para evitar lags)
        self.text_shadow = None
        self.text_main = None

    def setup(self):
        # Cargar las imágenes de fondo como texturas
        try:
            self.background_textures.append(arcade.load_texture(IMAGE1_PATH))
            self.background_textures.append(arcade.load_texture(IMAGE2_PATH))
        except Exception as e:
            # Fallback en caso de que falle la carga (crear texturas de colores planos)
            print(f"Error cargando imágenes: {e}. Creando texturas alternativas...")
            img1 = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), (30, 30, 30))
            img2 = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), (60, 30, 60))
            try:
                self.background_textures.append(arcade.Texture(image=img1))
                self.background_textures.append(arcade.Texture(image=img2))
            except TypeError:
                self.background_textures.append(arcade.Texture("bg1", img1))
                self.background_textures.append(arcade.Texture("bg2", img2))

        # Inicializar listas de sprites (requerido para dibujo en Arcade 3.0+)
        self.background_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Configurar Sprite de fondo
        self.background_sprite = arcade.Sprite(self.background_textures[0])
        self.background_sprite.center_x = self.width / 2
        self.background_sprite.center_y = self.height / 2
        self.background_list.append(self.background_sprite)

        # Configurar Personaje
        self.player = Player()
        self.player.center_x = self.width / 2
        self.player.center_y = self.height / 2
        self.player_list.append(self.player)

        # Inicializar textos informativos con efecto de sombra
        self.text_shadow = arcade.Text(
            "WASD / Flechas: Moverse | Animación de mapa activa (0.5s)",
            x=16,
            y=self.height - 26,
            color=arcade.color.BLACK,
            font_size=11,
            bold=True
        )
        self.text_main = arcade.Text(
            "WASD / Flechas: Moverse | Animación de mapa activa (0.5s)",
            x=15,
            y=self.height - 25,
            color=arcade.color.WHITE,
            font_size=11,
            bold=True
        )

    def on_draw(self):
        self.clear()
        
        # 1. Dibujar el fondo actual
        self.background_list.draw()
        
        # 2. Dibujar el personaje
        self.player_list.draw()

        # 3. Dibujar textos instructivos
        if self.text_shadow and self.text_main:
            self.text_shadow.draw()
            self.text_main.draw()

    def on_update(self, delta_time: float):
        # Actualizar temporizador de la animación del fondo
        self.bg_timer += delta_time
        if self.bg_timer >= 0.4:
            self.bg_timer = 0.0
            # Cambiar textura del fondo (flicker)
            self.current_bg_index = (self.current_bg_index + 1) % len(self.background_textures)
            self.background_sprite.texture = self.background_textures[self.current_bg_index]

        # Actualizar la lógica del personaje
        self.player.update()

        # Limitar la posición del personaje para que no salga del mapa
        half_w = self.player.width / 2
        half_h = self.player.height / 2

        if self.player.center_x < half_w:
            self.player.center_x = half_w
        elif self.player.center_x > self.width - half_w:
            self.player.center_x = self.width - half_w

        if self.player.center_y < half_h:
            self.player.center_y = half_h
        elif self.player.center_y > self.height - half_h:
            self.player.center_y = self.height - half_h

    def on_key_press(self, key, modifiers):
        # Control de movimiento
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.move_up = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.move_down = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.move_left = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.move_right = True
            
        # Cerrar la ventana si se presiona la tecla de Escape
        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        # Desactivar intenciones de movimiento
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.move_up = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.move_down = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.move_left = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.move_right = False


def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
