import arcade
import os, math
from clases.salas.sala_base import Interactuable, Objeto
from clases.salas.tuberias.sala_tuberias import Sala_Tuberias
from clases.personajes.ingeniero import Ingeniero

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
SCREEN_TITLE = "Sala 1 - Mapa Animado Dinámico"
velocidad_jugador_click = 7

class JuegoView(arcade.View):
    def __init__(self, sala_instanciada):
        super().__init__()
        self.sala = sala_instanciada
        
        # En el __init__ solo definimos las propiedades vacías
        self.jugador = None
        self.jugador_lista = None
        self.motor_fisica = None
        
        # Estado de la interacción
        self.objeto_objetivo = None
        self.moviéndose_por_click = False
        self.objetivo_alcanzado = False  

        # Integración de la animación de fondo
        self.current_bg_index = 0
        self.bg_timer = 0.0

    def on_show_view(self):
        """ 
        MÉTODO CRÍTICO: Se ejecuta cuando el menú hace el cambio a esta vista.
        Aquí la ventana ya existe de forma activa, por lo que es seguro cargar personajes y físicas.
        """
        # Instanciamos al jugador y su lista de sprites de forma segura
        self.jugador = Ingeniero(center_x=self.sala.ancho/2, center_y=self.sala.alto/2)
        self.jugador_lista = arcade.SpriteList()
        self.jugador_lista.append(self.jugador)

        # Inicializamos el motor de física con la sala ya cargada
        self.motor_fisica = arcade.PhysicsEngineSimple(self.jugador, self.sala.lista_bloqueos)


    """   CONTROL DE MOVIMIENTO COMBINADO    """

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
            objetos_cliqueados = arcade.get_sprites_at_point((x, y), self.sala.lista_bloqueos)  # Verificamos contra los bloqueos porque los interactuables también están ahí
            print(f"Objetos cliqueados: {objetos_cliqueados}")
            
            if objetos_cliqueados:
                if isinstance(objetos_cliqueados[0], Interactuable):
                    # Si tocamos un mueble, fijamos ese mueble como objetivo
                    self.objeto_objetivo = objetos_cliqueados[0]
                    self.jugador.destino_x = self.objeto_objetivo.ubicacion_jugador["x"]
                    self.jugador.destino_y = self.objeto_objetivo.ubicacion_jugador["y"]
                    print(self.jugador.destino_x)
            
            else:
                # Si hizo clic al suelo, solo se mueve, no hay interacción pendiente
                self.objeto_objetivo = None
                self.jugador.destino_x = x
                self.jugador.destino_y = y
            
            print(f"Clic en: ({x}, {y}) - Objetivo: {self.objeto_objetivo} - Destino: ({self.jugador.destino_x}, {self.jugador.destino_y})")


    """  LÓGICA DE JUEGO Y DIBUJADO    """

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
            llegamos_al_destino = self.jugador.update_por_click()
            if llegamos_al_destino:
                print("Destino alcanzado")
                self.moviéndose_por_click = False
                if self.objeto_objetivo is not None:
                    self.objetivo_alcanzado = True  # Marcamos que hemos alcanzado el objetivo para ejecutar la interacción en el siguiente ciclo de actualización

        else:
            # Si no hay estímulos, el personaje se queda quieto
            self.jugador.change_x = 0
            self.jugador.change_y = 0
        
        # 2. Actualizar física (por si choca con un muro invisible mientras camina)
        self.motor_fisica.update()
        
        # 3. TRUCO DE CONTROL: Verificar si estamos cerca del objeto interactuable
        if self.objeto_objetivo is not None:
            
            if self.objetivo_alcanzado:  # Si estamos lo suficientemente cerca del objetivo
                print(f"Interacción con {self.objeto_objetivo.nombre}")
                self.ejecutar_interaccion()  # Ejecutamos la función de interacción del objeto
                self.objeto_objetivo = None # Ya interactuó, vaciamos el objetivo
                self.objetivo_alcanzado = False # Reseteamos el estado de objetivo alcanzado
                # Frenamos al jugador en el sitio
                self.moviéndose_por_click = False
                self.jugador.change_x = 0
                self.jugador.change_y = 0

    def ejecutar_interaccion(self):
        # Aquí disparas la lógica del Escape Room
        print(f"Ejecutando función de interacción: {self.objeto_objetivo.funcion.__name__}")
        self.objeto_objetivo.funcion()

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