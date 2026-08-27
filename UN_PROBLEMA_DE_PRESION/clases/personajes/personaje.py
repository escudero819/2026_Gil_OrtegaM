import arcade, math, time
from PIL import Image, ImageDraw

PLAYER_SPEED = 5
PLAYER_SPEED_AUTOMATICO = 7
VELOCIDAD_ANIMACION = 0.07
ESCALA = 1.75
# --- Clase del Personaje (Player) ---
class Player(arcade.Sprite):
    def __init__(self, frames_idle, frames_caminando, center_x, center_y):
        # Crear texturas procedimentales para izquierda y derecha
        
        self.texturas_idle = {
            "derecha": arcade.load_texture(frames_idle["derecha"]),
            "izquierda": arcade.load_texture(frames_idle["izquierda"]),
            "arriba": arcade.load_texture(frames_idle["arriba"]),
            "abajo": arcade.load_texture(frames_idle["abajo"])
        }

        self.texturas_caminando = {
            "derecha": list(map(lambda tex: arcade.load_texture(tex) ,frames_caminando["derecha"])),
            "izquierda": list(map(lambda tex: arcade.load_texture(tex) ,frames_caminando["izquierda"])),
            "arriba": list(map(lambda tex: arcade.load_texture(tex) ,frames_caminando["arriba"])),
            "abajo": list(map(lambda tex: arcade.load_texture(tex) ,frames_caminando["abajo"]))
        }

        super().__init__(self.texturas_idle["abajo"], center_x=center_x, center_y=center_y)
        self.scale = ESCALA

        # Definir una caja de colisión personalizada.
        # Los puntos se miden desde el centro (0, 0) del sprite.
        # Ejemplo: Una caja pequeña que solo cubre los pies/base del personaje.
        puntos_colision = [
            (-15, -20),  # Esquina inferior izquierda
            (15, -20),   # Esquina inferior derecha
            (15, -5),    # Esquina superior derecha (a la altura de la cintura)
            (-15, -5)    # Esquina superior izquierda
        ]
        
        self.hit_box = arcade.hitbox.HitBox(puntos_colision)
        
        # Atributos de intención de movimiento
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

        self.velocidad = PLAYER_SPEED
        
        # Inicializar velocidades
        self.change_x = 0
        self.change_y = 0

        self.destino_x = center_x
        self.destino_y = center_y

        # Inicializar variables animaciones
        self.frame_actual = 0
        self.caminando = False
        self.bandera_animacion = time.time()
        self.direccion = None


    def actualizar_animacion(self):
        # Aquí podrías agregar lógica para cambiar la textura del jugador según el estado (caminando, quieto, etc.)
        if time.time() - self.bandera_animacion > VELOCIDAD_ANIMACION:
            print("actualizando animacion")
            self.frame_actual += 1
            if self.frame_actual > 5:
                self.frame_actual = 0
            self.texture = self.texturas_caminando[self.direccion][self.frame_actual]
            self.bandera_animacion = time.time()

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

        self.actualizar_animacion()
        
    def update_por_click(self):
        # Cálculo de distancia restante
        dx = self.destino_x - self.center_x
        dy = self.destino_y - self.center_y
        distancia = math.sqrt(dx**2 + dy**2)

        # Si estamos lo suficientemente cerca (umbral mínimo de tolerancia)
        if distancia <= 10:
            self.change_x = 0
            self.change_y = 0
            self.texture = self.texturas_idle[self.direccion if self.direccion else "abajo"]
            return True # Llegamos al destino de forma absoluta

        # AJUSTE SUAVE: Si está a menos de 10 píxeles, reducimos la velocidad 
        # para que no impacte ni traspase la hitbox del objeto
        if distancia < 20:
            velocidad_actual = 2.0  # Velocidad de aproximación milimétrica
        else:
            velocidad_actual = PLAYER_SPEED_AUTOMATICO

        # Conseguimos un movimiento fluido usando vectores unitarios multiplicados por la velocidad ajustada
        self.change_x = (dx / distancia) * velocidad_actual
        self.change_y = (dy / distancia) * velocidad_actual

        # Determinar dirección para la animación (se mantiene igual)
        if abs(self.change_x) >= abs(self.change_y):
            if self.change_x > 0:
                self.direccion = "derecha"
            else:
                self.direccion = "izquierda"
        else:
            if self.change_y > 0:
                self.direccion = "arriba"
            else:
                self.direccion = "abajo"
        
        self.actualizar_animacion()
        return False # Aún en movimiento