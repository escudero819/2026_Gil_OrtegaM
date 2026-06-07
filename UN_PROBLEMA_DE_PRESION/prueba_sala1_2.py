import arcade
import os, math
from clases.salas.tuberias.sala_tuberias import Sala_Tuberias
from clases.personajes.personaje import Player

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
SCREEN_TITLE = "Sala 1 - Mapa Animado Dinámico"


class JuegoView(arcade.Window):
    def __init__(self, sala_instanciada):
        self.sala = sala_instanciada
        super().__init__(self.sala.ancho, self.sala.alto)
        
        self.jugador = Player(CURRENT_PATH + "/jugador.gif", center_x=self.sala.ancho/2, center_y=self.sala.alto/2)
        self.jugador.scale = 3
        self.jugador_lista = arcade.SpriteList()
        self.jugador_lista.append(self.jugador)

        # Inicializamos la física solo con los bloqueos de la sala
        self.motor_fisica = arcade.PhysicsEngineSimple(self.jugador, self.sala.lista_bloqueos)
        
        # Estado de la interacción
        self.objeto_objetivo = None
        self.destino_x = self.jugador.center_x
        self.destino_y = self.jugador.center_y
        self.moviéndose_por_click = False

        #integracion de la version anterior
        self.current_bg_index = 0
        self.bg_timer = 0.0

    def on_key_press(self, key, modifiers):

        if key in [arcade.key.UP, arcade.key.W, arcade.key.DOWN, arcade.key.S, arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D]:
            self.moviéndose_por_click = False  # Si el jugador presiona una tecla de movimiento, desactivamos el movimiento por click
            self.objeto_objetivo = None  # Cancelamos cualquier interacción pendiente

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
            self.moviéndose_por_click = True

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
            
            print(f"Clic en: ({x}, {y}) - Objetivo: {self.objeto_objetivo} - Destino: ({self.destino_x}, {self.destino_y})")

    def on_update(self, delta_time: float):
        #actualizar temporizador de la animación del fondo
        self.bg_timer += delta_time
        if self.bg_timer >= 0.4:
            self.bg_timer = 0.0
            # Cambiar textura del fondo (flicker)
            self.current_bg_index = (self.current_bg_index + 1) % len(self.sala.fondo_texturas)
            self.sala.fondo_sprite.texture = self.sala.fondo_texturas[self.current_bg_index]

        # LÓGICA DE CONTROL DE MOVIMIENTO COMBINADO
        # Verificamos si el usuario está presionando activamente alguna tecla WASD/Flechas
        teclado_activo = self.jugador.move_left or self.jugador.move_right or self.jugador.move_up or self.jugador.move_down

        if teclado_activo:
            # Si usa el teclado, manda el teclado
            self.jugador.update_por_teclado()
        elif self.moviéndose_por_click:
            # Si no hay teclado pero el click está activo, calculamos ruta hacia el destino
            self.mover_jugador_hacia_destino()
        else:
            # Si no hay estímulos, el personaje se queda quieto
            self.jugador.change_x = 0
            self.jugador.change_y = 0
        
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
                self.moviéndose_por_click = False
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

        # Cálculo de distancia restante
        dx = self.destino_x - self.jugador.center_x
        dy = self.destino_y - self.jugador.center_y
        distancia = math.sqrt(dx**2 + dy**2)

        # Si estamos lo suficientemente cerca del punto destino, nos detenemos por completo
        if distancia > 5:
            # Conseguimos un movimiento fluido usando vectores unitarios multiplicados por la velocidad
            self.jugador.change_x = (dx / distancia) * self.jugador.velocidad
            self.jugador.change_y = (dy / distancia) * self.jugador.velocidad
            
            # Cambiar orientación visual con Click
            if self.jugador.change_x > 0:
                self.jugador.texture = self.jugador.texture_right
            elif self.jugador.change_x < 0:
                self.jugador.texture = self.jugador.texture_left
        else:
            self.jugador.change_x = 0
            self.jugador.change_y = 0
            self.moviéndose_por_click = False

    def ejecutar_interaccion(self, objeto_id):
        # Aquí disparas la lógica del Escape Room
        if objeto_id == "caja_fuerte":
            print("Abriendo la interfaz de la caja fuerte: Introduce el código.")
        elif objeto_id == "escritorio":
            print("Encontraste una nota vieja sobre el escritorio.")


window = JuegoView(Sala_Tuberias())
arcade.run()