import arcade
import os, math
from clases.salas.sala_base import Interactuable, Objeto
from clases.personajes.ingeniero import Ingeniero
from configuraciones import Constantes as consts

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
SCREEN_TITLE = "Sala 1 - Mapa Animado Dinámico"
velocidad_jugador_click = 7

class JuegoView(arcade.View):
    def __init__(self, sala_instanciada):
        super().__init__()
        self.sala = sala_instanciada
        self.texto_inicial = False
        self.sala.InstanciarInterfaces(self)
        
        # En el __init__ solo definimos las propiedades vacías
        self.jugador = None
        self.jugador_lista = None
        self.motor_fisica = None
        
        
        # Estado de la interacción
        self.objeto_objetivo = None
        self.moviéndose_por_click = False
        self.objetivo_alcanzado = False
        self.listo_para_interactuar = False

        # Integración de la animación de fondo
        self.current_bg_index = 0
        self.bg_timer = 0.0

        # variables para la logica de la caja de texto emergente
        self.mostrar_cuadro_texto = False
        self.texto_completo = ""       # El texto total que queremos mostrar
        self.texto_actual = ""         # Lo que se va escribiendo en pantalla poco a poco
        self.indice_letra = 0          # En qué letra del string vamos
        
        # Temporizadores para las letras
        self.temporizador_letra = 0.0
        self.VELOCIDAD_TEXTO = 0.03    # Tiempo en segundos entre cada letra (0.03 es ideal)
        
        # El objeto de texto de Arcade
        self.interfaz_texto = None

    def on_show_view(self):
        """ 
        MÉTODO CRÍTICO: Se ejecuta cuando el menú hace el cambio a esta vista.
        Aquí la ventana ya existe de forma activa, por lo que es seguro cargar personajes y físicas.
        """
        # Instanciamos al jugador y su lista de sprites de forma segura
        if not self.jugador:
            self.jugador = Ingeniero(center_x=self.sala.ancho/2, center_y=self.sala.alto/2)
        self.jugador_lista = arcade.SpriteList()
        self.jugador_lista.append(self.jugador)

        # Inicializamos el motor de física con la sala ya cargada
        self.motor_fisica = arcade.PhysicsEngineSimple(self.jugador, self.sala.lista_bloqueos)

        # Inicializamos el objeto de texto en la parte inferior de la ventana
        self.interfaz_texto = arcade.Text(
            text="",
            x=80,                          # Margen izquierdo para que no toque el borde de la pantalla
            y=110,                         # Altura interna de la caja de texto
            color=arcade.color.WHITE,
            font_size=20,
            font_name="Courier New",             
            bold=True,
            multiline=True,
            width=self.window.width - 160        # Se adapta al ancho de tu pantalla automáticamente
        )

        # vemos si hay que decir el texto inicial de la zona
        if not self.texto_inicial:
            self.mostrar_texto(self.sala.texto_inicial)
            self.texto_inicial = True

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

            if self.mostrar_cuadro_texto:
                 # Si ya se terminó de escribir todo el texto
                if self.indice_letra >= len(self.texto_completo):
                    self.mostrar_cuadro_texto = False  # Oculta la caja y deja seguir jugando
                    return

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

    def mostrar_texto(self, mensaje_nuevo):
        """ Configura y arranca la animación de letras desde cero """
        self.texto_completo = mensaje_nuevo
        self.texto_actual = ""
        self.indice_letra = 0
        self.temporizador_letra = 0.0
        self.interfaz_texto.text = ""
        self.mostrar_cuadro_texto = True

    def on_update(self, delta_time: float):
        #actualizar temporizador de la animación del fondo
        self.bg_timer += delta_time
        if self.bg_timer >= 0.4:
            self.bg_timer = 0.0
            # Cambiar textura del fondo (flicker)
            self.current_bg_index = (self.current_bg_index + 1) % len(self.sala.fondo_texturas)
            self.sala.fondo_sprite.texture = self.sala.fondo_texturas[self.current_bg_index]

        # verificamos si toco un eliminador (si es que hay)
        if self.sala.lista_eliminadores:
            contacto = arcade.check_for_collision_with_list(self.jugador, self.sala.lista_eliminadores)

            if contacto:
                print("has perdido por tocar el agua electrificada")

                from game_over import Game_Over
                vista_game_over = Game_Over("agua")
                self.window.show_view(vista_game_over)
                return
            
        #verificamos si ha tocado la salida
        salida_alcanzada = arcade.check_for_collision_with_list(self.jugador, self.sala.lista_salida)

        if salida_alcanzada:
            print("HAS SALIDOOOO")

            from victoria import VictoriaView

            vista_victoria = VictoriaView()
            self.window.show_view(vista_victoria)
            return

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
        
        # Actualizar física (por si choca con un muro invisible mientras camina)
        self.motor_fisica.update()
        
        if self.objeto_objetivo is not None:
            
            if self.objetivo_alcanzado:  
                # PASO 1: En este frame frenamos al jugador y dejamos que se aplique la textura Idle
                self.moviéndose_por_click = False
                self.jugador.change_x = 0
                self.jugador.change_y = 0
                
                # Activamos una nueva bandera interna para indicar que el juego ya lo registró quieto
                self.listo_para_interactuar = True
                self.objetivo_alcanzado = False # Apagamos para que no vuelva a entrar aquí
                
        # PASO 2: En el frame de actualización SUCESIVO (cuando el anterior ya se dibujó en pantalla)
        # disparamos la interfaz emergente de forma limpia
        if getattr(self, 'listo_para_interactuar', False):
            self.listo_para_interactuar = False # Reseteamos la bandera
            
            mueble_actual = self.objeto_objetivo
            self.objeto_objetivo = None 
            
            print(f"Ejecutando función de interacción: {mueble_actual.funcion.__name__}")
            mueble_actual.funcion(self)      
        
        # ANIMACIÓN DE TEXTO GRADUAL (MÁQUINA DE ESCRIBIR)
        if self.mostrar_cuadro_texto:
            # Si todavía faltan letras por escribir del mensaje completo
            if self.indice_letra < len(self.texto_completo):
                self.temporizador_letra += delta_time
                
                # Cuando pasa el tiempo configurado, añadimos el siguiente caracter
                if self.temporizador_letra >= self.VELOCIDAD_TEXTO:
                    self.temporizador_letra = 0.0
                    self.texto_actual += self.texto_completo[self.indice_letra]
                    self.indice_letra += 1
                    
                    # Actualizamos el contenido visual del objeto de texto
                    self.interfaz_texto.text = self.texto_actual

    def ejecutar_interaccion(self, interactuable):
        # Aquí disparas la lógica del Escape Room
        print(f"Ejecutando función de interacción: {interactuable.funcion.__name__}")
        interactuable.funcion(self)

    def on_draw(self):
        self.clear()

        self.sala.draw()
        
        self.sala.lista_bloqueos.draw()  # Para depuración, muestra las paredes invisibles  
        
        # 2. Dibujar el personaje
        self.jugador_lista.draw()

        self.sala.lista_salida.draw()

        if self.mostrar_cuadro_texto:
            ancho_pantalla = self.window.width
            
            # Configuramos las coordenadas de la caja usando la esquina inferior izquierda como base
            margen_izquierdo = 40
            borde_inferior = 25
            ancho_caja = ancho_pantalla - 80
            alto_caja = 110

            # 1. Fondo de la caja (Left, Bottom, Width, Height)
            arcade.draw_lbwh_rectangle_filled(
                left=margen_izquierdo,
                bottom=borde_inferior,
                width=ancho_caja,
                height=alto_caja,
                color=(15, 15, 15, 230)
            )
            
            # 2. Borde de la caja
            arcade.draw_lbwh_rectangle_outline(
                left=margen_izquierdo,
                bottom=borde_inferior,
                width=ancho_caja,
                height=alto_caja,
                color=arcade.color.WHITE,
                border_width=3
            )
            
            # 3. Renderizar las letras que se están escribiendo
            if self.interfaz_texto:
                self.interfaz_texto.draw()

                
    
    def _verificar_bloqueo(self, sprite):

        if arcade.check_for_collision_with_list(sprite, self.sala.lista_bloqueos):
            return True
        return False