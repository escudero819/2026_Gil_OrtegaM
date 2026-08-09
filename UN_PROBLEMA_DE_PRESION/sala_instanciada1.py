import arcade
import os, math, asyncio, threading
from clases.salas.sala_base import Interactuable, Objeto
from clases.personajes.ingeniero import Ingeniero
from configuraciones import Constantes as consts
import edge_tts

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
SCREEN_TITLE = "Sala 1 - Mapa Animado Dinámico"
velocidad_jugador_click = 7

class SalaActualView(arcade.View):
    def __init__(self, sala_instanciada, manager):
        super().__init__()
        self.sala = sala_instanciada
        self.manager = manager
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

        # Control de voz (edge-tts / arcade sound player)
        self.reproductor_audio = None

    def ejecutar_dialogo(self, texto: str, voz: str = "es-ES-AlvaroNeural", velocidad: str = "+0%", tono: str = "+0Hz"):
        """
        Ejecuta voz y texto sincronizados.
        - velocidad: p. ej. '+25%' para desesperación/alarma, '-10%' para lentitud.
        - tono: p. ej. '+15Hz' para tono agudo/tembloroso, '-10Hz' para voz grave.
        """
        """
        # Detenemos cualquier audio anterior
        if self.reproductor_audio:
            arcade.stop_sound(self.reproductor_audio)
            self.reproductor_audio = None

        # 1. Crear un nombre único de archivo según el texto y entonación (Sistema de Caché)
        # Usamos hash para que textos iguales reutilicen el mismo MP3 ya descargado
        id_audio = abs(hash(f"{texto}_{voz}_{velocidad}_{tono}"))
        carpeta_cache = os.path.join(CURRENT_PATH, "cache_audio")
        os.makedirs(carpeta_cache, exist_ok=True)
        archivo_audio = os.path.join(carpeta_cache, f"dialogo_{id_audio}.mp3")

        # 2. Si el audio YA EXISTE en caché, se reproduce AL INSTANTE (sin lag)
        if os.path.exists(archivo_audio):
            try:
                audio = arcade.load_sound(archivo_audio)
                self.reproductor_audio = arcade.play_sound(audio)
                self.mostrar_texto(texto)
                return
            except Exception as e:
                print(f"[Aviso Caché] Error cargando audio existente: {e}")

        # 3. Si no existe, lo descargamos asíncronamente en segundo plano
        async def _generar_audio():
            try:
                # Usamos los parámetros rate y pitch nativos en lugar de código XML/SSML
                comunicador = edge_tts.Communicate(
                    text=texto, 
                    voice=voz, 
                    rate=velocidad, 
                    pitch=tono
                )
                await comunicador.save(archivo_audio)
                return True
            except Exception as e:
                print(f"[Aviso Edge-TTS] Error de red al generar voz: {e}")
                return False

        def _hilo_trabajador():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                exito = loop.run_until_complete(_generar_audio())
                loop.close()

                if exito:
                    def _reproducir_en_pantalla(dt):
                        if os.path.exists(archivo_audio):
                            try:
                                audio = arcade.load_sound(archivo_audio)
                                self.reproductor_audio = arcade.play_sound(audio)

                            except Exception as audio_err:
                                print(f"[Aviso Audio] Falló la carga del MP3: {audio_err}")

                    arcade.schedule_once(_reproducir_en_pantalla, 0)
            except Exception as thread_err:
                print(f"[Aviso Hilo Voice] Error secundario ignorado: {thread_err}")

        threading.Thread(target=_hilo_trabajador, daemon=True).start()
        """
        self.mostrar_texto(texto)

    def on_show_view(self):
        """ 
        MÉTODO CRÍTICO: Se ejecuta cuando el menú hace el cambio a esta vista.
        Aquí la ventana ya existe de forma activa, por lo que es seguro cargar personajes y físicas.
        """
        if not self.jugador:
            self.jugador = Ingeniero(center_x=self.sala.posicion_inicial[0], center_y=self.sala.posicion_inicial[1])
        self.jugador_lista = arcade.SpriteList()
        self.jugador_lista.append(self.jugador)

        self.motor_fisica = arcade.PhysicsEngineSimple(self.jugador, self.sala.lista_bloqueos)

        self.interfaz_texto = arcade.Text(
            text="",
            x=80,
            y=110,
            color=arcade.color.WHITE,
            font_size=20,
            font_name="Courier New",             
            bold=True,
            multiline=True,
            width=self.window.width - 160
        )

        # Cambiamos la llamada para que use la voz sintetizada junto al texto
        if not self.texto_inicial:
            self.ejecutar_dialogo(self.sala.texto_inicial, voz="es-ES-AlvaroNeural", velocidad="+30%", tono="+15Hz")
            self.texto_inicial = True

    """   CONTROL DE MOVIMIENTO COMBINADO    """

    def on_key_press(self, key, modifiers):

        if key in [arcade.key.UP, arcade.key.W, arcade.key.DOWN, arcade.key.S, arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D]:
            self.moviéndose_por_click = False
            self.objeto_objetivo = None

        if key == arcade.key.UP or key == arcade.key.W:
            self.jugador.move_up = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.jugador.move_down = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.jugador.move_left = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.jugador.move_right = True
            
        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
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
                if self.indice_letra >= len(self.texto_completo):
                    self.mostrar_cuadro_texto = False
                    # Si el jugador cierra el cuadro de texto, cortamos la voz si sigue hablando
                    if self.reproductor_audio:
                        arcade.stop_sound(self.reproductor_audio)
                        self.reproductor_audio = None
                    return

            self.moviéndose_por_click = True

            objetos_cliqueados = arcade.get_sprites_at_point((x, y), self.sala.lista_bloqueos)
            print(f"Objetos cliqueados: {objetos_cliqueados}")
            
            if objetos_cliqueados:
                if isinstance(objetos_cliqueados[0], Interactuable):
                    self.objeto_objetivo = objetos_cliqueados[0]
                    self.jugador.destino_x = self.objeto_objetivo.ubicacion_jugador["x"]
                    self.jugador.destino_y = self.objeto_objetivo.ubicacion_jugador["y"]
                    print(self.jugador.destino_x)
            
            else:
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
        self.bg_timer += delta_time
        if self.bg_timer >= 0.4:
            self.bg_timer = 0.0
            self.current_bg_index = (self.current_bg_index + 1) % len(self.sala.fondo_texturas)
            self.sala.fondo_sprite.texture = self.sala.fondo_texturas[self.current_bg_index]

        if self.sala.lista_eliminadores:
            contacto = arcade.check_for_collision_with_list(self.jugador, self.sala.lista_eliminadores)

            if contacto:
                print("has perdido por tocar el agua electrificada")

                from game_over import Game_Over
                vista_game_over = Game_Over("agua")
                self.window.show_view(vista_game_over)
                return
            
        salida_alcanzada = arcade.check_for_collision_with_list(self.jugador, self.sala.lista_salida)

        if salida_alcanzada:
            print("HAS SALIDOOOO")
            self.window.show_view(self.manager)
            return

        teclado_activo = self.jugador.move_left or self.jugador.move_right or self.jugador.move_up or self.jugador.move_down

        if teclado_activo:
            self.jugador.update_por_teclado()
        elif self.moviéndose_por_click:
            llegamos_al_destino = self.jugador.update_por_click()
            if llegamos_al_destino:
                print("Destino alcanzado")
                self.moviéndose_por_click = False
                if self.objeto_objetivo is not None:
                    self.objetivo_alcanzado = True

        else:
            self.jugador.change_x = 0
            self.jugador.change_y = 0
        
        self.motor_fisica.update()
        
        if self.objeto_objetivo is not None:
            if self.objetivo_alcanzado:  
                self.moviéndose_por_click = False
                self.jugador.change_x = 0
                self.jugador.change_y = 0
                
                self.listo_para_interactuar = True
                self.objetivo_alcanzado = False
                
        if getattr(self, 'listo_para_interactuar', False):
            self.listo_para_interactuar = False
            
            mueble_actual = self.objeto_objetivo
            self.objeto_objetivo = None 
            
            print(f"Ejecutando función de interacción: {mueble_actual.funcion.__name__}")
            mueble_actual.funcion(self)      
        
        if self.mostrar_cuadro_texto:
            if self.indice_letra < len(self.texto_completo):
                self.temporizador_letra += delta_time
                
                if self.temporizador_letra >= self.VELOCIDAD_TEXTO:
                    self.temporizador_letra = 0.0
                    self.texto_actual += self.texto_completo[self.indice_letra]
                    self.indice_letra += 1
                    
                    self.interfaz_texto.text = self.texto_actual

    def ejecutar_interaccion(self, interactuable):
        print(f"Ejecutando función de interacción: {interactuable.funcion.__name__}")
        interactuable.funcion(self)

    def on_draw(self):
        self.clear()

        self.sala.fondo_lista.draw()
        self.sala.lista_bloqueos.draw()  
        
        self.jugador_lista.draw()
        self.sala.interactuables_sprites.draw()

        self.sala.lista_salida.draw()

        if self.mostrar_cuadro_texto:
            ancho_pantalla = self.window.width
            
            margen_izquierdo = 40
            borde_inferior = 25
            ancho_caja = ancho_pantalla - 80
            alto_caja = 110

            arcade.draw_lbwh_rectangle_filled(
                left=margen_izquierdo,
                bottom=borde_inferior,
                width=ancho_caja,
                height=alto_caja,
                color=(15, 15, 15, 230)
            )
            
            arcade.draw_lbwh_rectangle_outline(
                left=margen_izquierdo,
                bottom=borde_inferior,
                width=ancho_caja,
                height=alto_caja,
                color=arcade.color.WHITE,
                border_width=3
            )
            
            if self.interfaz_texto:
                self.interfaz_texto.draw()