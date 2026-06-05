import arcade
import os
from clases.salas.tuberias.sala_tuberias import Sala_Tuberias
from clases.personajes.personaje import Player

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
SCREEN_TITLE = "Sala 1 - Mapa Animado Dinámico"


class JuegoView(arcade.Window):
    def __init__(self, sala_instanciada):
        self.sala = sala_instanciada
        super().__init__(self.sala.ancho, self.sala.alto)
        
        self.jugador_sprite = arcade.Sprite(CURRENT_PATH + "/jugador.gif", center_x=self.sala.ancho/2, center_y=self.sala.alto/2)
        self.jugador = Player(self.jugador_sprite)
        self.jugador_lista = arcade.SpriteList()
        self.jugador_lista.append(self.jugador.sprite)
        
        # Inicializamos la física solo con los bloqueos de la sala
        self.motor_fisica = arcade.PhysicsEngineSimple(self.jugador.sprite, self.sala.lista_bloqueos)
        
        # Estado de la interacción
        self.objeto_objetivo = None
        self.destino_x = self.jugador.sprite.center_x
        self.destino_y = self.jugador.sprite.center_y
        self.velocidad_jugador = 5

        #integracion de la version anterior
        self.current_bg_index = 0
        self.bg_timer = 0.0
    
    def on_key_press(self, key, modifiers):
        # Control de movimiento
        if key == arcade.key.UP or key == arcade.key.W:
            self.jugador.move_up = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.jugador.move_down = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.jugador.move_left = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.jugador.move_right = True
            
        # Cerrar la ventana si se presiona la tecla de Escape
        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        # Desactivar intenciones de movimiento
        if key == arcade.key.UP or key == arcade.key.W:
            self.jugador.move_up = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.jugador.move_down = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.jugador.move_left = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.jugador.move_right = False

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # 1. Detectar si el clic colisionó con algún mueble interactuable
            objetos_cliqueados = arcade.get_sprites_at_point((x, y), self.sala.interactuables_sprites)
            
            if objetos_cliqueados:
                # Si tocamos un mueble, fijamos ese mueble como objetivo
                self.objeto_objetivo = objetos_cliqueados[0]
                self.destino_x = self.objeto_objetivo.center_x
                self.destino_y = self.objeto_objetivo.center_y
                print(self.destino_x)
            else:
                # Si hizo clic al suelo, solo se mueve, no hay interacción pendiente
                self.objeto_objetivo = None
                self.destino_x = x
                self.destino_y = y

    def on_update(self, delta_time: float):
        self.bg_timer += delta_time
        if self.bg_timer >= 0.4:
            self.bg_timer = 0.0
            # Cambiar textura del fondo (flicker)
            self.current_bg_index = (self.current_bg_index + 1) % len(self.sala.fondo_texturas)
            self.sala.fondo_sprite.texture = self.sala.fondo_texturas[self.current_bg_index]

        # 1. Calcular movimiento hacia el destino (Mover al jugador)
        # (Aquí puedes usar vectores o una interpolación simple para mover al jugador hacia destino_x/y)
        #self.mover_jugador_hacia_destino()
        self.jugador.update()
        
        # 2. Actualizar física (por si choca con un muro invisible mientras camina)
        self.motor_fisica.update()
        
        # 3. TRUCO DE CONTROL: Verificar si estamos cerca del objeto interactuable
        if self.objeto_objetivo is not None:
            # Medimos la distancia actual entre el jugador y el mueble
            distancia = arcade.get_distance_between_sprites(self.jugador_sprite, self.objeto_objetivo)
            
            # Si el jugador ya entró en el "radio" configurado en el diccionario...
            if distancia <= self.objeto_objetivo.distancia_minima:
                self.ejecutar_interaccion(self.objeto_objetivo.id)
                self.objeto_objetivo = None # Ya interactuó, vaciamos el objetivo
                # Frenamos al jugador en el sitio
                self.jugador.change_x = 0
                self.jugador.change_y = 0
    
    def on_draw(self):
        self.clear()

        self.sala.draw()
        
        self.sala.lista_bloqueos.draw()  # Para depuración, muestra las paredes invisibles  
        
        # 2. Dibujar el personaje
        self.jugador_lista.draw()
    
    def _verificar_bloqueo(self, sprite):

        if arcade.check_for_collision_with_list(sprite, self.sala.lista_bloqueos):
            return True
        return False

    def mover_jugador_hacia_destino(self):
        # Lógica matemática simple para otorgar velocidad al sprite en dirección al destino
        # (Para no complicar el ejemplo, reducimos la velocidad a 0 si está muy cerca del destino)
        if abs(self.jugador.center_x - self.destino_x) > 5:
            posicion_anterior_x = self.jugador.center_x
            self.jugador.change_x = self.velocidad_jugador if self.jugador.center_x < self.destino_x else -self.velocidad_jugador
            if self._verificar_bloqueo(self.jugador):
                self.jugador.center_x = posicion_anterior_x
                self.jugador.change_x = 0
        else:
            self.jugador.change_x = 0
            
        if abs(self.jugador.center_y - self.destino_y) > 5:
            posicion_anterior_y = self.jugador.center_y
            self.jugador.change_y = self.velocidad_jugador if self.jugador.center_y < self.destino_y else -self.velocidad_jugador
            if self._verificar_bloqueo(self.jugador):
                self.jugador.center_y = posicion_anterior_y
                self.jugador.change_y = 0
        else:
            self.jugador.change_y = 0

    def ejecutar_interaccion(self, objeto_id):
        # Aquí disparas la lógica del Escape Room
        if objeto_id == "caja_fuerte":
            print("Abriendo la interfaz de la caja fuerte: Introduce el código.")
        elif objeto_id == "escritorio":
            print("Encontraste una nota vieja sobre el escritorio.")


window = JuegoView(Sala_Tuberias())
arcade.run()